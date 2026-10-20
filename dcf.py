"""Lab 6: MSFT DCF, sensitivity, and reverse DCF; standard library only.

Run: python3 dcf.py
Training check: python3 dcf.py --training
Sources and conventions: ColinSpensley/MSFT/Lab_06_MSFT.md
"""

# EDITABLE INPUTS: USD millions, shares in millions, rates as decimals.
# FY2026 10-K: cash flow statement; Notes 1, 2, 10, 11, and 13.
OPERATING_CASH_FLOW = 182935.0
DEBT_CASH_INTEREST = 1500.0  # Rounded filing disclosure; see estimation caveat.
FINANCE_LEASE_CASH_INTEREST = 2547.0
TAX_RATE = 32185.0 / 165934.0  # Effective tax rate, used as an estimate.
CASH_CAPEX = 115948.0
FINANCE_LEASE_ASSET_ADDITIONS = 24608.0
CASH_BASIS_FCFF = (OPERATING_CASH_FLOW
                   + (DEBT_CASH_INTEREST + FINANCE_LEASE_CASH_INTEREST)
                   * (1 - TAX_RATE) - CASH_CAPEX)
# Include lease-funded investment because finance leases are treated as debt.
STARTING_FCFF = CASH_BASIS_FCFF - FINANCE_LEASE_ASSET_ADDITIONS
GROWTH_RATES = [0.15, 0.12, 0.10, 0.08, 0.06]  # Analyst forecast, not guidance.
TERMINAL_GROWTH = 0.03  # Analyst long-run nominal estimate.
NON_OPERATING_CASH = 76843.0 - 3800.0  # Exclude restricted short-term investments.
DEBT = 40294.0 + 66594.0  # Borrowing carrying value plus finance leases.
DILUTED_SHARES = 7453.0  # FY2026 EPS note, as the lab requires.
TARGET_SHARE_PRICE = 492.44
PRICE_AS_OF = "2026-09-10 16:00 EDT, regular-session close"

# WACC estimate: latest published Treasury observation, vendor beta,
# course ERP, filing debt rate and lease rate, approximate market weights.
RISK_FREE_RATE = 0.0483  # H.15: Sep 9 observation, released Sep 10.
BETA = 1.11  # Stock Analysis, retrieved Sep 10; vendor estimate.
EQUITY_RISK_PREMIUM = 0.05  # Lab convention, not a measured market premium.
BORROWING_COST = 0.0549  # Note 10 upper effective rate for 2024 issuance.
LEASE_COST = 0.045  # Note 13 weighted-average finance-lease discount rate.
BASIC_SHARES_FOR_MARKET_CAP = 7427.0  # June 30 balance sheet; dated proxy.
MARKET_EQUITY = TARGET_SHARE_PRICE * BASIC_SHARES_FOR_MARKET_CAP
MARKET_DEBT = 36500.0 + 66594.0  # Note 10 fair value + lease carrying proxy.
COST_OF_EQUITY = RISK_FREE_RATE + BETA * EQUITY_RISK_PREMIUM
COST_OF_DEBT = (36500.0 * BORROWING_COST + 66594.0 * LEASE_COST) / MARKET_DEBT
WACC = (MARKET_EQUITY * COST_OF_EQUITY
        + MARKET_DEBT * COST_OF_DEBT * (1 - TAX_RATE)) / (MARKET_EQUITY + MARKET_DEBT)
WACC_VALUES = [WACC - 0.01, WACC, WACC + 0.01]
TERMINAL_GROWTH_VALUES = [0.02, 0.03, 0.04]
SHIFT_LOWER = -0.05
SHIFT_UPPER = 0.10  # Required first bracket; may honestly have no solution.
EXTENDED_SHIFT_UPPER = 1.00  # Separate diagnostic, never changes the forecast.
PRICE_TOLERANCE = 0.0000001

import argparse
import math


def value_dcf(start, growth, wacc, terminal_growth, cash, debt, shares):
    """Return five FCFFs followed by the seven original Session 5 outputs."""
    values = [start, *growth, wacc, terminal_growth, cash, debt, shares]
    if not all(math.isfinite(x) for x in values):
        raise ValueError("All inputs must be finite numbers.")
    if len(growth) != 5:
        raise ValueError("Provide exactly five yearly growth rates.")
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be less than WACC.")
    if wacc <= -1 or terminal_growth <= -1:
        raise ValueError("WACC and terminal growth must exceed -100%.")
    if shares <= 0:
        raise ValueError("Diluted shares must be greater than zero.")
    if start <= 0:
        raise ValueError("Nonpositive FCFF requires an explicit cash-flow path, not this growth model.")
    if any(g <= -1 for g in growth):
        raise ValueError("Annual growth must exceed -100%.")
    fcff = start
    yearly_fcff = []
    for rate in growth:
        fcff *= 1 + rate
        yearly_fcff.append(fcff)
    pv_explicit = sum(f / (1 + wacc) ** year
                      for year, f in enumerate(yearly_fcff, 1))
    terminal_value = yearly_fcff[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** 5
    enterprise = pv_explicit + pv_terminal
    equity = enterprise + cash - debt
    result = yearly_fcff + [pv_explicit, terminal_value, pv_terminal,
                           enterprise, equity, equity / shares, pv_terminal / enterprise]
    if not all(math.isfinite(x) for x in result):
        raise ValueError("Inputs produce non-finite valuation results.")
    return result


def reverse_dcf(start, growth, wacc, terminal_growth, cash, debt, shares,
                target, lower, upper):
    """Bisection of uniform growth shift; None means no root in bracket."""
    if not all(math.isfinite(x) for x in [target, lower, upper]):
        raise ValueError("Target and bounds must be finite.")
    if target <= 0 or lower >= upper:
        raise ValueError("Target must be positive and lower bound below upper bound.")
    if any(g + lower <= -1 or g + upper <= -1 for g in growth):
        raise ValueError("Refusing bracket: an annual growth rate reaches -100% or below.")

    def residual(shift):
        return value_dcf(start, [g + shift for g in growth], wacc,
                         terminal_growth, cash, debt, shares)[10] - target

    low_error, high_error = residual(lower), residual(upper)
    if abs(low_error) <= PRICE_TOLERANCE:
        return lower  # A verified endpoint root, not an unreachable target.
    if abs(high_error) <= PRICE_TOLERANCE:
        return upper
    if low_error * high_error > 0:
        return None
    for _ in range(200):
        middle = (lower + upper) / 2
        error = residual(middle)
        if abs(error) <= PRICE_TOLERANCE:
            return middle
        if low_error * error < 0:
            upper = middle
        else:
            lower, low_error = middle, error
    raise ValueError("Bisection did not converge to the requested price tolerance.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--training', action='store_true', help='Use the original Lab 5/6 inputs.')
    args = parser.parse_args()
    if args.training:
        start, growth, wacc, tg, cash, debt, shares = 100., [.08, .06, .05, .04, .03], .10, .03, 50., 300., 50.
        target, wacc_grid, tg_grid = 30., [.09, .10, .11], [.02, .03, .04]
        mode, as_of = 'TRAINING', 'Hypothetical training target; no market timestamp'
    else:
        start, growth, wacc, tg = STARTING_FCFF, GROWTH_RATES, WACC, TERMINAL_GROWTH
        cash, debt, shares = NON_OPERATING_CASH, DEBT, DILUTED_SHARES
        target, wacc_grid, tg_grid = TARGET_SHARE_PRICE, WACC_VALUES, TERMINAL_GROWTH_VALUES
        mode, as_of = 'MSFT — analyst estimates; see Lab_06_MSFT.md', PRICE_AS_OF
    result = value_dcf(start, growth, wacc, tg, cash, debt, shares)
    labels = [f'FCFF Year {year}' for year in range(1, 6)] + [
        'PV of explicit FCFF', 'Terminal value, Year 5', 'PV of terminal value',
        'Enterprise value', 'Equity value', 'Value per diluted share',
        'PV of TV / enterprise value']
    for label, value in zip(labels, result):
        print(f'{label}: {value:.4f}')
    print(f'\nSensitivity grid — {mode} — USD/share')
    print(f'{"WACC / g":>12}' + ''.join(f'{g:>13.2%}' for g in tg_grid))
    for rate in wacc_grid:
        cells = []
        for g in tg_grid:
            try:
                price = value_dcf(start, growth, rate, g, cash, debt, shares)[10]
                cells.append(f'{price:13.2f}')
            except (ValueError, OverflowError):
                cells.append(f'{"INVALID":>13}')
        print(f'{rate:>12.4%}' + ''.join(cells))
    print(f'\nReverse DCF — {mode}')
    print(f'Target price: ${target:.4f}; {as_of}')
    print('Solved variable: uniform additive shift to all five explicit growth rates.')
    print(f'Held fixed: starting FCFF={start:.4f}; WACC={wacc:.8%}; '
          f'terminal growth={tg:.4%}; cash={cash:.4f}; debt={debt:.4f}; '
          f'diluted shares={shares:.4f}; five years; annual end-of-year timing.')
    print('Original growth path: ' + ', '.join(f'{g:.4%}' for g in growth))
    brackets = [(SHIFT_LOWER, SHIFT_UPPER)]
    if not args.training and EXTENDED_SHIFT_UPPER is not None:
        brackets.append((SHIFT_LOWER, EXTENDED_SHIFT_UPPER))
    for lower, upper in brackets:
        print(f'Shift bracket: {lower * 100:+.2f} to {upper * 100:+.2f} percentage points')
        shift = reverse_dcf(start, growth, wacc, tg, cash, debt, shares, target, lower, upper)
        if shift is None:
            print('No solution in that bracket.')
            continue
        implied = [g + shift for g in growth]
        print(f'Solved shift: {shift * 100:+.6f} percentage points')
        print('Implied growth path: ' + ', '.join(f'{g:.6%}' for g in implied))
        print(f'Repriced value per share: ${value_dcf(start, implied, wacc, tg, cash, debt, shares)[10]:.6f}')
        break
    print('A conditional price-consistent scenario, not proof of mispricing.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OverflowError) as error:
        raise SystemExit(f'Error: {error}')
