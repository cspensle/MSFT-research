"""Streamlit interface for the Microsoft Project 1 valuation workbench."""

from __future__ import annotations

import math

import streamlit as st

from proforma import project, valuation
from workbench import (
    BASE_TERMINAL_GROWTH,
    BASE_WACC,
    MARKET_PRICE,
    MARKET_PRICE_AS_OF,
    case_table,
    scenario_assumptions,
    sensitivity_grid,
    validation_checks,
    value_forecast_fcff,
)


st.set_page_config(page_title="MSFT Valuation Workbench", layout="wide")
st.title("Microsoft Project 1 — Valuation Workbench")
st.caption(
    "Five-year linked pro forma → lease-adjusted FCFF DCF → enterprise-to-equity bridge. "
    "USD millions except per-share values."
)


def reset_controls() -> None:
    """Restore every exposed control to the documented base case."""
    st.session_state["growth_shift_pp"] = 0.0
    st.session_state["margin_shift_pp"] = 0.0
    st.session_state["cash_capex_2030"] = 155_000
    st.session_state["cash_capex_2031"] = 160_000
    st.session_state["wacc_percent"] = BASE_WACC * 100.0
    st.session_state["terminal_growth_percent"] = BASE_TERMINAL_GROWTH * 100.0
    st.session_state["force_failure"] = False


for control_key, base_value in {
    "growth_shift_pp": 0.0,
    "margin_shift_pp": 0.0,
    "cash_capex_2030": 155_000,
    "cash_capex_2031": 160_000,
    "wacc_percent": BASE_WACC * 100.0,
    "terminal_growth_percent": BASE_TERMINAL_GROWTH * 100.0,
    "force_failure": False,
}.items():
    st.session_state.setdefault(control_key, base_value)


with st.sidebar:
    st.header("Bounded driver panel")
    st.caption("Bounds are analyst-selected scenarios, not company guidance.")
    st.button("Reset base case", on_click=reset_controls, width="stretch")
    growth_shift_pp = st.slider(
        "Annual revenue-growth shift", -3.0, 3.0, step=0.5,
        format="%.1f pp", key="growth_shift_pp"
    )
    margin_shift_pp = st.slider(
        "Annual gross-margin shift", -1.0, 1.0, step=0.25,
        format="%.2f pp", key="margin_shift_pp"
    )
    cash_capex_2030 = st.slider(
        "FY2030 cash capital spending ($m)", 100_000, 190_000, step=5_000,
        key="cash_capex_2030",
        help="Base case: $155,000m. Locked test value: $125,000m.",
    )
    cash_capex_2031 = st.slider(
        "FY2031 cash capital spending ($m)", 100_000, 195_000, step=5_000,
        key="cash_capex_2031",
        help="Base case: $160,000m. Locked test value: $120,000m.",
    )
    wacc_percent = st.slider(
        "WACC", 8.0, 13.0, step=0.1,
        format="%.2f%%", key="wacc_percent"
    )
    terminal_growth_percent = st.slider(
        "Terminal growth", 1.0, 5.0, step=0.1,
        format="%.1f%%", key="terminal_growth_percent"
    )
    force_failure = st.checkbox(
        "Validation demo: force terminal growth equal to WACC",
        help="Creates an incoherent Gordon-growth input so the check fails loudly.",
        key="force_failure",
    )

assumptions = scenario_assumptions(
    growth_shift_pp / 100.0,
    margin_shift_pp / 100.0,
    cash_capex_overrides={2030: float(cash_capex_2030), 2031: float(cash_capex_2031)},
)
results = project(assumptions)
wacc = wacc_percent / 100.0
terminal_growth = wacc if force_failure else terminal_growth_percent / 100.0
checks = validation_checks(results, assumptions, wacc, terminal_growth)
all_pass = all(passed for passed, _ in checks.values())

if all_pass:
    dcf = value_forecast_fcff(results, assumptions, wacc, terminal_growth)
    fcfe = valuation(results, {**assumptions, "terminal_growth": terminal_growth})
    columns = st.columns(4)
    columns[0].metric("FCFF value/share", f"${dcf.value_per_share:,.2f}", f"${dcf.value_per_share - MARKET_PRICE:,.2f} vs market")
    columns[1].metric("FCFE cross-check", f"${fcfe['value_per_share']:,.2f}")
    columns[2].metric("Enterprise value", f"${dcf.enterprise_value / 1_000:,.1f}bn")
    columns[3].metric("Terminal value share", f"{dcf.terminal_share:.1%}")
    st.caption(
        f"FCFE cross-check uses a separate {assumptions['cost_of_equity']:.2%} "
        "cost of equity; the WACC control applies to FCFF."
    )
    st.info(
        f"Conditional call: **watch/defer** at the saved market reference of "
        f"**${MARKET_PRICE:,.2f} ({MARKET_PRICE_AS_OF})**. This call must be revisited "
        "if evidence supports materially stronger cash conversion or the price changes."
    )
else:
    dcf = None
    st.error("Valuation blocked: one or more controls violate a required model condition.")

st.subheader("Validation panel")
for name, (passed, detail) in checks.items():
    if passed:
        st.success(f"PASS — {name}: {detail}")
    else:
        st.error(f"FAIL — {name}: {detail}")

if dcf is not None:
    st.subheader("Five-year forecast")
    forecast_rows = []
    for row, fcff in zip(results, dcf.fcff):
        forecast_rows.append(
            {
                "Year": f"FY{row.year}E",
                "Revenue ($m)": row.revenue,
                "Operating income ($m)": row.operating_income,
                "Net income ($m)": row.net_income,
                "Cash capex ($m)": row.cash_capex,
                "Lease additions ($m)": row.finance_lease_additions,
                "FCFF ($m)": fcff,
                "FCFE ($m)": row.fcfe,
                "Cash ($m)": row.cash,
                "Balance gap ($m)": row.balance_gap,
            }
        )
    st.dataframe(forecast_rows, width="stretch", hide_index=True)

    st.subheader("Enterprise-to-equity bridge")
    st.dataframe(
        [
            {"Bridge item": "Enterprise value", "USD millions": dcf.enterprise_value},
            {"Bridge item": "Add: non-operating cash", "USD millions": 73_043.0},
            {"Bridge item": "Less: borrowing and finance leases", "USD millions": -106_888.0},
            {"Bridge item": "Equity value", "USD millions": dcf.equity_value},
        ],
        width="stretch",
        hide_index=True,
    )

    st.subheader("Causal low/base/high cases")
    st.dataframe(case_table(), width="stretch", hide_index=True)

    st.subheader("WACC–terminal-growth sensitivity")
    grid = sensitivity_grid(results, assumptions, wacc, terminal_growth)
    display_grid = [
        {
            "WACC": f"{record['WACC']:.2%}",
            "Terminal growth": f"{record['Terminal growth']:.2%}",
            "Value/share": None if math.isnan(record["Value/share"]) else round(record["Value/share"], 2),
        }
        for record in grid
    ]
    st.dataframe(display_grid, width="stretch", hide_index=True)

with st.expander("Model conventions and limitations"):
    st.markdown(
        """
- Annual end-of-year discounting; terminal value at FY2031 year-end.
- Finance-lease additions are treated as investment and finance-lease liabilities as debt.
- Non-operating cash excludes $3.8 billion of restricted short-term investments.
- FY2026 weighted-average diluted shares remain constant; forward dilution is not modeled.
- Stock compensation is added back as noncash, so the constant-share assumption is a material limitation.
- Low/base/high cases are causal scenarios, not probabilities or price targets.
- Market and filing inputs are historical classroom observations, not live market data.
"""
    )
