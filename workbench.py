"""Integrated Microsoft pro-forma workbench and FCFF valuation layer.

The existing ``proforma.py`` remains unchanged so its saved Lab 10/11 results
stay reproducible.  This module consumes that accounting engine and adds the
Project 1 product outputs: forecast FCFF, an enterprise-to-equity bridge,
low/base/high cases, a WACC-growth grid, and explicit validation checks.

All monetary amounts are USD millions except per-share values.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Iterable

from dcf import DEBT, NON_OPERATING_CASH, WACC
from proforma import BASE_ASSUMPTIONS, OPENING, TOLERANCE, YEARS, YearResult, project, valuation


BASE_WACC = WACC
BASE_TERMINAL_GROWTH = 0.03
MARKET_PRICE = 509.22
MARKET_PRICE_AS_OF = "2026-09-28 regular-session close"


@dataclass(frozen=True)
class DCFResult:
    fcff: tuple[float, ...]
    pv_explicit: float
    terminal_value: float
    pv_terminal: float
    enterprise_value: float
    equity_value: float
    value_per_share: float
    terminal_share: float


def scenario_assumptions(
    revenue_growth_shift: float = 0.0,
    gross_margin_shift: float = 0.0,
    cash_capex_shift: float = 0.0,
    cash_capex_overrides: dict[int, float] | None = None,
) -> dict:
    """Return fresh assumptions with only the named operating inputs changed."""
    assumptions = copy.deepcopy(BASE_ASSUMPTIONS)
    assumptions["revenue_growth"] = [
        value + revenue_growth_shift for value in assumptions["revenue_growth"]
    ]
    assumptions["gross_margin"] = [
        value + gross_margin_shift for value in assumptions["gross_margin"]
    ]
    assumptions["cash_capex"] = [
        value + cash_capex_shift for value in assumptions["cash_capex"]
    ]
    for year, value in (cash_capex_overrides or {}).items():
        if year not in YEARS:
            raise ValueError(f"Cash-capex override year must be one of {YEARS}.")
        if value < 0:
            raise ValueError("Cash-capex overrides cannot be negative.")
        assumptions["cash_capex"][YEARS.index(year)] = float(value)
    return assumptions


def forecast_fcff(results: Iterable[YearResult], assumptions: dict) -> tuple[float, ...]:
    """Calculate lease-adjusted FCFF from each linked forecast year.

    Finance-lease additions are treated as capital investment and the related
    liability is included in debt in the enterprise-to-equity bridge. Stock
    compensation is added back as a noncash charge; its dilution limitation is
    disclosed because the share count is held constant in this course model.
    """
    rate = assumptions["tax_rate"]
    return tuple(
        row.operating_income * (1.0 - rate)
        + row.depreciation
        + row.stock_compensation
        - row.cash_capex
        - row.finance_lease_additions
        - row.change_operating_assets
        + row.change_operating_liabilities
        for row in results
    )


def value_forecast_fcff(
    results: list[YearResult],
    assumptions: dict,
    wacc: float = BASE_WACC,
    terminal_growth: float = BASE_TERMINAL_GROWTH,
) -> DCFResult:
    """Discount pro-forma FCFF and bridge enterprise value to equity value."""
    if not 0.0 < wacc < 1.0:
        raise ValueError("WACC must be between 0% and 100%.")
    if not -1.0 < terminal_growth < wacc:
        raise ValueError("Terminal growth must be below WACC and above -100%.")
    shares = assumptions["diluted_shares"]
    if shares <= 0:
        raise ValueError("Diluted shares must be positive.")

    fcff = forecast_fcff(results, assumptions)
    if fcff[-1] <= 0:
        raise ValueError("Terminal-year FCFF must be positive for Gordon growth.")
    pv_explicit = sum(value / (1.0 + wacc) ** year for year, value in enumerate(fcff, 1))
    terminal_value = fcff[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1.0 + wacc) ** len(fcff)
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    return DCFResult(
        fcff=fcff,
        pv_explicit=pv_explicit,
        terminal_value=terminal_value,
        pv_terminal=pv_terminal,
        enterprise_value=enterprise_value,
        equity_value=equity_value,
        value_per_share=equity_value / shares,
        terminal_share=pv_terminal / enterprise_value,
    )


def validation_checks(
    results: list[YearResult], assumptions: dict, wacc: float, terminal_growth: float
) -> dict[str, tuple[bool, str]]:
    """Return visible checks instead of hiding failures behind a single verdict."""
    maximum_gap = max(abs(row.balance_gap) for row in results)
    minimum_cash = min(row.cash for row in results)

    prior_cash = OPENING["cash"]
    cash_tie_gap = 0.0
    for row in results:
        expected_cash = prior_cash + row.fcfe - row.dividends - row.buybacks
        cash_tie_gap = max(cash_tie_gap, abs(expected_cash - row.cash))
        prior_cash = row.cash

    return {
        "Balance sheet articulation": (
            maximum_gap <= TOLERANCE,
            f"maximum assets minus liabilities and equity = ${maximum_gap:,.4f}m",
        ),
        "Cash-flow tie": (
            cash_tie_gap <= TOLERANCE,
            f"maximum calculated-versus-balance-sheet cash gap = ${cash_tie_gap:,.4f}m",
        ),
        "Minimum cash": (
            minimum_cash + TOLERANCE >= assumptions["minimum_cash"],
            f"lowest forecast cash = ${minimum_cash:,.1f}m; floor = ${assumptions['minimum_cash']:,.1f}m",
        ),
        "Terminal convention": (
            terminal_growth < wacc,
            f"terminal growth {terminal_growth:.2%}; WACC {wacc:.2%}",
        ),
        "Diluted shares": (
            assumptions["diluted_shares"] > 0,
            f"FY2026 weighted-average diluted shares = {assumptions['diluted_shares']:,.1f}m",
        ),
    }


def sensitivity_grid(
    results: list[YearResult], assumptions: dict, wacc: float, terminal_growth: float
) -> list[dict[str, float]]:
    records = []
    for grid_wacc in (wacc - 0.01, wacc, wacc + 0.01):
        for grid_growth in (terminal_growth - 0.01, terminal_growth, terminal_growth + 0.01):
            try:
                price = value_forecast_fcff(
                    results, assumptions, grid_wacc, grid_growth
                ).value_per_share
            except ValueError:
                price = float("nan")
            records.append(
                {"WACC": grid_wacc, "Terminal growth": grid_growth, "Value/share": price}
            )
    return records


def case_table() -> list[dict[str, float | str]]:
    """Causal cases: downside/base/upside rather than arbitrary value haircuts."""
    cases = (
        ("Downside", -0.02, -0.005, 20_000.0),
        ("Base", 0.0, 0.0, 0.0),
        ("Upside", 0.02, 0.005, -20_000.0),
    )
    records = []
    for name, growth_shift, margin_shift, capex_shift in cases:
        assumptions = scenario_assumptions(growth_shift, margin_shift, capex_shift)
        results = project(assumptions)
        dcf = value_forecast_fcff(results, assumptions)
        records.append(
            {
                "Case": name,
                "Revenue growth shift": growth_shift,
                "Gross-margin shift": margin_shift,
                "Annual cash-capex shift ($m)": capex_shift,
                "FY2031 FCFF ($m)": dcf.fcff[-1],
                "Value/share": dcf.value_per_share,
            }
        )
    return records


def main() -> None:
    assumptions = scenario_assumptions()
    results = project(assumptions)
    dcf = value_forecast_fcff(results, assumptions)
    fcfe = valuation(results, assumptions)
    checks = validation_checks(results, assumptions, BASE_WACC, BASE_TERMINAL_GROWTH)

    print("MICROSOFT PROJECT 1 WORKBENCH — BASE CASE")
    print(f"Market reference: ${MARKET_PRICE:,.2f}; {MARKET_PRICE_AS_OF}")
    print(f"Pro-forma FCFF value/share: ${dcf.value_per_share:,.2f}")
    print(f"Pro-forma FCFE cross-check: ${fcfe['value_per_share']:,.2f}")
    print(f"Enterprise value: ${dcf.enterprise_value:,.1f}m")
    print(f"Equity value: ${dcf.equity_value:,.1f}m")
    print(f"Terminal share of enterprise value: {dcf.terminal_share:.1%}")
    print("Forecast FCFF: " + ", ".join(f"${value:,.1f}m" for value in dcf.fcff))
    print("\nVALIDATION")
    for name, (passed, detail) in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} — {name}: {detail}")
    print("\nCAUSAL CASES")
    for record in case_table():
        print(
            f"{record['Case']}: ${record['Value/share']:,.2f}/share; "
            f"FY2031 FCFF ${record['FY2031 FCFF ($m)']:,.1f}m"
        )


if __name__ == "__main__":
    main()
