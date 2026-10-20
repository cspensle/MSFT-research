"""Lab 08: Microsoft comparable-company P/E and EV/revenue analysis.

Run from the course workspace: python3 comps.py
Inputs are September 10, 2026 closes and latest annual reported GAAP diluted
EPS public by that date. All inputs are USD/share.
"""

from statistics import median
import math


# Microsoft: FY2026 ended June 30, 2026; reported July 29, 2026.
TARGET = {"ticker": "MSFT", "name": "Microsoft", "price": 492.44, "eps": 17.95}
PEERS = [
    # Oracle: FY2026 ended May 31, 2026; reported June 10, 2026.
    {"ticker": "ORCL", "name": "Oracle", "price": 152.94, "eps": 5.83},
    # Alphabet Class A: FY2025 ended December 31, 2025; reported February 4, 2026.
    {"ticker": "GOOGL", "name": "Alphabet Class A", "price": 332.60, "eps": 10.82},
]

COMPARISON_DATE = "September 10, 2026"
EARNINGS_BASIS = "latest annual reported GAAP diluted EPS public by that date"

# Enterprise-value inputs are USD millions. The comparison uses the same
# September 10, 2026 share-price date as P/E and the latest filed annual
# revenue and balance-sheet data public on that date. Oracle is the closest
# operating peer and is used as a qualified one-peer EV/revenue cross-check.
EV_TARGET = {
    "ticker": "MSFT",
    "price": 492.44,
    "shares": 7_425.545491,
    "revenue": 331_839.0,
    "borrowing": 40_294.0,
    "finance_leases": 66_594.0,
    "preferred_stock": 0.0,
    "non_operating_cash": 73_043.0,
}
EV_PEER = {
    "ticker": "ORCL",
    "price": 152.94,
    "shares": 2_880.471,
    "revenue": 67_357.0,
    "borrowing": 129_541.0,
    "finance_leases": 7_701.0,
    "preferred_stock": 4_954.0,
    "non_operating_cash": 31_894.0,
}


def positive_number(value):
    """Reject missing, nonnumeric, nonfinite, and nonpositive inputs."""
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value > 0)


def ticker_key(company):
    return str(company.get("ticker", "")).strip().upper()


def usable_peers(target, candidates):
    """Return valid peers plus an audit trail for omitted rows."""
    target_key = ticker_key(target)
    seen = set()
    valid, omitted = [], []
    for company in candidates:
        key = ticker_key(company)
        label = company.get("name", key or "Unnamed peer")
        if not key:
            omitted.append((label, "missing ticker"))
        elif key == target_key:
            omitted.append((label, "target excluded"))
        elif key in seen:
            omitted.append((label, "duplicate ticker"))
        else:
            seen.add(key)
            if not positive_number(company.get("price")) or not positive_number(company.get("eps")):
                omitted.append((label, "price or EPS not meaningful"))
            else:
                valid.append((key, label, company["price"] / company["eps"]))
    return valid, omitted


def enterprise_value(company):
    """Market capitalization plus debt-like claims less non-operating cash."""
    return (
        company["price"] * company["shares"]
        + company["borrowing"]
        + company["finance_leases"]
        + company["preferred_stock"]
        - company["non_operating_cash"]
    )


def ev_revenue_cross_check(target=EV_TARGET, peer=EV_PEER):
    """Return observed EV/revenue and the peer-implied target equity value."""
    target_ev = enterprise_value(target)
    peer_ev = enterprise_value(peer)
    peer_multiple = peer_ev / peer["revenue"]
    implied_target_ev = target["revenue"] * peer_multiple
    implied_target_equity = (
        implied_target_ev
        + target["non_operating_cash"]
        - target["borrowing"]
        - target["finance_leases"]
        - target["preferred_stock"]
    )
    return {
        "target_ev": target_ev,
        "target_multiple": target_ev / target["revenue"],
        "peer_ev": peer_ev,
        "peer_multiple": peer_multiple,
        "implied_target_ev": implied_target_ev,
        "implied_target_equity": implied_target_equity,
        "implied_target_price": implied_target_equity / target["shares"],
    }


def report(target=TARGET, candidates=PEERS):
    name = target.get("name", ticker_key(target) or "Target")
    print(f"Target: {name} ({ticker_key(target)})")
    print(f"Inputs: USD/share; {COMPARISON_DATE} closes / {EARNINGS_BASIS}.")
    peers, omitted = usable_peers(target, candidates)
    for label, reason in omitted:
        print(f"Omitted {label}: {reason}.")
    for key, label, multiple in peers:
        print(f"{label} ({key}) P/E: {multiple:.6f}×")

    if positive_number(target.get("eps")) and positive_number(target.get("price")):
        print(f"Target observed P/E (comparison only): "
              f"{target['price'] / target['eps']:.6f}×")
    else:
        print("Target observed P/E: not meaningful (price or EPS missing/nonpositive).")
    if not positive_number(target.get("eps")):
        print("Target EPS not meaningful; no implied price calculation.")
        return
    if not peers:
        print("No usable peers; no estimate.")
        return

    eps = target["eps"]
    multiples = [multiple for _, _, multiple in peers]
    full_estimate = median(multiples) * eps
    print(f"Peer median P/E: {median(multiples):.6f}×")
    if len(peers) == 1:
        print(f"One-peer reference estimate: ${full_estimate:.2f}; no range.")
    else:
        print(f"Peer-implied range: ${min(multiples) * eps:.2f}–${max(multiples) * eps:.2f}")
        print(f"Median-implied price: ${full_estimate:.2f}")

    for removed_key, removed_label, _ in peers:
        remaining = [multiple for key, _, multiple in peers if key != removed_key]
        if not remaining:
            print(f"Remove {removed_label} ({removed_key}): no estimate remains.")
            continue
        estimate = median(remaining) * eps
        change = estimate - full_estimate  # Both estimates retain unrounded multiples.
        print(f"Remove {removed_label} ({removed_key}): remaining median-implied "
              f"${estimate:.2f}; change {change:+.2f} dollars.")

    ev_check = ev_revenue_cross_check()
    print("\nQualified enterprise-value cross-check (USD millions):")
    print(f"MSFT observed EV/revenue: {ev_check['target_multiple']:.6f}x")
    print(f"ORCL observed EV/revenue: {ev_check['peer_multiple']:.6f}x")
    print(f"MSFT at ORCL EV/revenue: ${ev_check['implied_target_price']:.2f}/share")


if __name__ == "__main__":
    report()
