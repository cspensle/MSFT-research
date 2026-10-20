"""Microsoft five-year pro-forma and one-at-a-time sensitivity analysis.

Lab 10 base run:       python3 proforma.py
Lab 11 sensitivity:    python3 proforma.py --sensitivity

All monetary inputs and outputs are USD millions except per-share values.
Historical sources and assumption labels are documented in
ColinSpensley/MSFT/Lab_10_MSFT.md.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from typing import Iterable


YEARS = (2027, 2028, 2029, 2030, 2031)
TOLERANCE = 0.1


# FY2026 opening balance sheet. The broad residual buckets preserve every
# reported asset and liability while keeping the forecast links auditable.
OPENING = {
    "revenue": 331_839.0,
    "cash": 20_935.0,
    "short_term_investments": 55_908.0,
    "receivables": 80_876.0,
    "inventory": 1_397.0,
    "ppe": 313_076.0,
    "other_assets": 286_184.0,
    "accounts_payable": 42_416.0,
    "debt": 40_294.0,
    "finance_lease_liability": 66_594.0,
    "other_liabilities": 166_685.0,
    "equity": 442_387.0,
}


BASE_ASSUMPTIONS = {
    "revenue_growth": [0.15, 0.13, 0.12, 0.11, 0.10],
    "gross_margin": [0.678, 0.679, 0.681, 0.683, 0.685],
    "rd_percent_revenue": [0.108, 0.107, 0.106, 0.105, 0.104],
    "sga_percent_revenue": [0.104, 0.102, 0.100, 0.098, 0.097],
    "tax_rate": 0.1940,
    "depreciation_percent_opening_ppe": 0.1673,
    "cash_capex": [135_000.0, 145_000.0, 150_000.0, 155_000.0, 160_000.0],
    "finance_lease_additions": [30_000.0, 33_000.0, 36_000.0, 38_000.0, 40_000.0],
    "finance_lease_principal_percent": 0.0500,
    "receivable_days": 80_876.0 / 331_839.0 * 365.0,
    "inventory_days": 1_397.0 / (331_839.0 - 225_465.0) * 365.0,
    "payable_days": 42_416.0 / (331_839.0 - 225_465.0) * 365.0,
    "stock_comp_percent_revenue": 12_405.0 / 331_839.0,
    "dividends": [28_600.0, 30_900.0, 33_400.0, 36_100.0, 39_000.0],
    "buybacks": [22_000.0] * 5,
    "debt_repayment": [4_000.0] * 5,
    "cost_of_equity": 0.1038,
    "terminal_growth": 0.0300,
    "diluted_shares": 7_453.0,
    "minimum_cash": 10_000.0,
}


@dataclass(frozen=True)
class YearResult:
    year: int
    revenue: float
    gross_profit: float
    research_development: float
    sga: float
    operating_income: float
    pretax_income: float
    tax: float
    net_income: float
    depreciation: float
    stock_compensation: float
    cash_capex: float
    finance_lease_additions: float
    change_operating_assets: float
    change_operating_liabilities: float
    net_borrowing: float
    fcfe: float
    dividends: float
    buybacks: float
    cash: float
    short_term_investments: float
    receivables: float
    inventory: float
    ppe: float
    other_assets: float
    accounts_payable: float
    debt: float
    finance_lease_liability: float
    other_liabilities: float
    equity: float
    balance_gap: float


def project(assumptions: dict) -> list[YearResult]:
    """Project five linked years from fresh independent input data."""
    a = copy.deepcopy(assumptions)
    prior = dict(OPENING)
    results: list[YearResult] = []

    for i, year in enumerate(YEARS):
        revenue = prior["revenue"] * (1.0 + a["revenue_growth"][i])
        gross_profit = revenue * a["gross_margin"][i]
        cost_of_revenue = revenue - gross_profit
        research_development = revenue * a["rd_percent_revenue"][i]
        sga = revenue * a["sga_percent_revenue"][i]
        operating_income = gross_profit - research_development - sga
        pretax_income = operating_income  # No repeat of FY2026's OpenAI investment gain.
        tax = max(0.0, pretax_income) * a["tax_rate"]
        net_income = pretax_income - tax

        depreciation = prior["ppe"] * a["depreciation_percent_opening_ppe"]
        stock_compensation = revenue * a["stock_comp_percent_revenue"]
        cash_capex = a["cash_capex"][i]
        lease_additions = a["finance_lease_additions"][i]

        receivables = revenue * a["receivable_days"] / 365.0
        inventory = cost_of_revenue * a["inventory_days"] / 365.0
        ppe = prior["ppe"] + cash_capex + lease_additions - depreciation
        short_term_investments = prior["short_term_investments"]
        other_assets = prior["other_assets"]

        accounts_payable = cost_of_revenue * a["payable_days"] / 365.0
        debt_repayment = min(prior["debt"], a["debt_repayment"][i])
        debt = prior["debt"] - debt_repayment
        lease_principal = prior["finance_lease_liability"] * a["finance_lease_principal_percent"]
        lease_liability = prior["finance_lease_liability"] + lease_additions - lease_principal
        other_liabilities = prior["other_liabilities"]

        dividends = a["dividends"][i]
        buybacks = a["buybacks"][i]
        equity = (prior["equity"] + net_income + stock_compensation
                  - dividends - buybacks)

        change_operating_assets = ((receivables - prior["receivables"])
                                   + (inventory - prior["inventory"]))
        change_operating_liabilities = accounts_payable - prior["accounts_payable"]
        net_borrowing = ((debt - prior["debt"])
                         + (lease_liability - prior["finance_lease_liability"]))
        total_capex = cash_capex + lease_additions
        fcfe = (net_income + depreciation + stock_compensation - total_capex
                - change_operating_assets + change_operating_liabilities
                + net_borrowing)
        cash = prior["cash"] + fcfe - dividends - buybacks

        total_assets = (cash + short_term_investments + receivables + inventory
                        + ppe + other_assets)
        total_liabilities_equity = (accounts_payable + debt + lease_liability
                                    + other_liabilities + equity)
        balance_gap = total_assets - total_liabilities_equity

        result = YearResult(
            year, revenue, gross_profit, research_development, sga,
            operating_income, pretax_income, tax, net_income, depreciation,
            stock_compensation, cash_capex, lease_additions,
            change_operating_assets, change_operating_liabilities,
            net_borrowing, fcfe, dividends, buybacks, cash,
            short_term_investments, receivables, inventory, ppe, other_assets,
            accounts_payable, debt, lease_liability, other_liabilities, equity,
            balance_gap,
        )
        results.append(result)
        prior = {
            "revenue": revenue,
            "cash": cash,
            "short_term_investments": short_term_investments,
            "receivables": receivables,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "accounts_payable": accounts_payable,
            "debt": debt,
            "finance_lease_liability": lease_liability,
            "other_liabilities": other_liabilities,
            "equity": equity,
        }
    return results


def assert_balanced(results: Iterable[YearResult], minimum_cash: float) -> None:
    for result in results:
        if abs(result.balance_gap) > TOLERANCE:
            raise ValueError(
                f"FY{result.year}E balance sheet gap {result.balance_gap:.4f} exceeds tolerance"
            )
        if result.cash < minimum_cash - TOLERANCE:
            raise ValueError(
                f"FY{result.year}E cash {result.cash:.1f} is below minimum {minimum_cash:.1f}"
            )


def valuation(results: list[YearResult], assumptions: dict) -> dict[str, float]:
    cost = assumptions["cost_of_equity"]
    growth = assumptions["terminal_growth"]
    if cost <= growth:
        raise ValueError("Cost of equity must exceed terminal growth.")
    pv_explicit = sum(row.fcfe / (1.0 + cost) ** i
                      for i, row in enumerate(results, 1))
    terminal_value = results[-1].fcfe * (1.0 + growth) / (cost - growth)
    pv_terminal = terminal_value / (1.0 + cost) ** len(results)
    equity_value = pv_explicit + pv_terminal
    return {
        "pv_explicit": pv_explicit,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "equity_value": equity_value,
        "terminal_share": pv_terminal / equity_value,
        "value_per_share": equity_value / assumptions["diluted_shares"],
    }


def row(label: str, values: Iterable[float]) -> str:
    return f"{label:<31}" + "".join(f"{value:>14,.1f}" for value in values)


def print_base(results: list[YearResult], assumptions: dict) -> None:
    assert_balanced(results, assumptions["minimum_cash"])
    value = valuation(results, assumptions)
    print("MICROSOFT PRO-FORMA — USD millions except per share")
    print(f"{'':31}" + "".join(f"FY{year}E".rjust(14) for year in YEARS))
    print("\nINCOME STATEMENT")
    for label, field in [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"),
        ("Research & development", "research_development"),
        ("Sales, general & admin.", "sga"),
        ("Operating income", "operating_income"),
        ("Income taxes", "tax"), ("Net income", "net_income"),
    ]:
        print(row(label, (getattr(r, field) for r in results)))

    print("\nBALANCE SHEET")
    for label, field in [
        ("Cash", "cash"), ("Short-term investments", "short_term_investments"),
        ("Accounts receivable", "receivables"), ("Inventory", "inventory"),
        ("PP&E, net", "ppe"), ("Other assets", "other_assets"),
        ("Accounts payable", "accounts_payable"), ("Borrowings", "debt"),
        ("Finance lease liability", "finance_lease_liability"),
        ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
    ]:
        print(row(label, (getattr(r, field) for r in results)))

    print("\nCASH FLOW / FCFE")
    for label, field in [
        ("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Stock compensation", "stock_compensation"),
        ("Cash capital spending", "cash_capex"),
        ("Finance lease additions", "finance_lease_additions"),
        ("Change in operating assets", "change_operating_assets"),
        ("Change in operating liab.", "change_operating_liabilities"),
        ("Net borrowing", "net_borrowing"), ("FCFE", "fcfe"),
        ("Dividends", "dividends"), ("Share repurchases", "buybacks"),
    ]:
        print(row(label, (getattr(r, field) for r in results)))

    print("\nCHECK BLOCK")
    print(row("Assets - liabilities - equity", (r.balance_gap for r in results)))
    print(row("Cash above minimum", (r.cash - assumptions["minimum_cash"] for r in results)))
    print("Status: PASS — every balance gap is within +/- $0.1 million; cash floor passes.")

    print("\nFCFE VALUATION")
    print(f"PV of explicit FCFE: ${value['pv_explicit']:,.1f} million")
    print(f"PV of terminal value: ${value['pv_terminal']:,.1f} million")
    print(f"Equity value: ${value['equity_value']:,.1f} million")
    print(f"Share of value after FY2031: {value['terminal_share']:.1%}")
    print(f"Value per diluted share: ${value['value_per_share']:,.2f}")


def changed_keys(base: dict, changed: dict) -> list[str]:
    return sorted(key for key in base if base[key] != changed[key])


def sensitivity() -> None:
    base_inputs = copy.deepcopy(BASE_ASSUMPTIONS)
    base_results = project(base_inputs)
    assert_balanced(base_results, base_inputs["minimum_cash"])
    base_value = valuation(base_results, base_inputs)["value_per_share"]
    base_outputs = (base_results[-1].operating_income,
                    base_results[-1].fcfe, base_value)
    records = []

    scenarios = [
        ("Revenue growth", "-2.0 pp each year", "revenue_growth", -0.02, "%"),
        ("Revenue growth", "base", "revenue_growth", 0.00, "%"),
        ("Revenue growth", "+2.0 pp each year", "revenue_growth", 0.02, "%"),
        ("Cash capital spending", "-$20,000m each year", "cash_capex", -20_000.0, "USDm"),
        ("Cash capital spending", "base", "cash_capex", 0.0, "USDm"),
        ("Cash capital spending", "+$20,000m each year", "cash_capex", 20_000.0, "USDm"),
    ]
    for driver, case, key, shift, units in scenarios:
        inputs = copy.deepcopy(base_inputs)
        if shift:
            inputs[key] = [value + shift for value in inputs[key]]
        expected_changed = [] if shift == 0 else [key]
        actual_changed = changed_keys(base_inputs, inputs)
        if actual_changed != expected_changed:
            raise AssertionError(
                f"{driver} {case}: changed {actual_changed}, expected {expected_changed}"
            )
        results = project(inputs)
        assert_balanced(results, inputs["minimum_cash"])
        value_per_share = valuation(results, inputs)["value_per_share"]
        outputs = (results[-1].operating_income, results[-1].fcfe, value_per_share)
        max_gap = max(abs(r.balance_gap) for r in results)
        records.append((driver, case, units, inputs[key], *outputs, max_gap))

    print("MICROSOFT ONE-AT-A-TIME SENSITIVITY")
    print("Every scenario starts from a fresh deep copy of the base inputs.")
    print("Only the named independent input changes; linked statements recalculate.")
    print("\nDriver / scenario                         FY2031 operating income"
          "       FY2031 FCFE     Value/share    Check")
    for driver, case, units, values, op_income, fcfe, value_ps, max_gap in records:
        label = f"{driver}: {case}"
        print(f"{label:<43} ${op_income:>16,.1f}m  ${fcfe:>16,.1f}m  "
              f"${value_ps:>13,.2f}    PASS")
        if case != "base":
            print(f"  actual inputs ({units}): " + ", ".join(f"{v:.4f}" for v in values))
            print(f"  change from base: operating income {op_income-base_outputs[0]:+,.1f}m; "
                  f"FCFE {fcfe-base_outputs[1]:+,.1f}m; value/share "
                  f"{value_ps-base_outputs[2]:+,.2f}; max balance gap {max_gap:.4f}m")

    print("\nOUTPUT SPANS (maximum - minimum over lower/base/higher)")
    for driver in ("Revenue growth", "Cash capital spending"):
        subset = [r for r in records if r[0] == driver]
        print(f"{driver}: operating income "
              f"${max(r[4] for r in subset)-min(r[4] for r in subset):,.1f}m; "
              f"FCFE ${max(r[5] for r in subset)-min(r[5] for r in subset):,.1f}m; "
              f"value/share ${max(r[6] for r in subset)-min(r[6] for r in subset):,.2f}")

    restored_inputs = copy.deepcopy(base_inputs)
    restored_results = project(restored_inputs)
    assert_balanced(restored_results, restored_inputs["minimum_cash"])
    restored_outputs = (restored_results[-1].operating_income,
                        restored_results[-1].fcfe,
                        valuation(restored_results, restored_inputs)["value_per_share"])
    if restored_inputs != base_inputs or restored_outputs != base_outputs:
        raise AssertionError("Restored base does not match the opening base run.")
    print("\nRESTORED-BASE CHECK")
    print(f"Opening base:  FY2031 operating income ${base_outputs[0]:,.1f}m; "
          f"FCFE ${base_outputs[1]:,.1f}m; value/share ${base_outputs[2]:,.2f}")
    print(f"Restored base: FY2031 operating income ${restored_outputs[0]:,.1f}m; "
          f"FCFE ${restored_outputs[1]:,.1f}m; value/share ${restored_outputs[2]:,.2f}")
    print("Status: PASS — exact match; all scenario accounting checks pass.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sensitivity", action="store_true",
                        help="Run the Lab 11 one-at-a-time sensitivity analysis.")
    args = parser.parse_args()
    if args.sensitivity:
        sensitivity()
    else:
        results = project(BASE_ASSUMPTIONS)
        print_base(results, BASE_ASSUMPTIONS)


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError) as error:
        raise SystemExit(f"ERROR: {error}")
