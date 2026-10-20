"""Lab 14 Meridian portfolio baselines; inputs are course training values."""

from math import isfinite, sqrt


# Editable inputs. Returns and volatilities are decimals (0.035 means 3.5%).
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160},
}
CORRELATIONS = (
    (1.00, 0.10, 0.05, 0.00),
    (0.10, 1.00, 0.80, -0.10),
    (0.05, 0.80, 1.00, 0.25),
    (0.00, -0.10, 0.25, 1.00),
)
OBJECTIVE_RETURN = 0.065  # Estimated CPI 2.5% + mandate spread 4.0%.
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def validate_inputs(sleeves: dict, correlations: tuple) -> None:
    """Reject inconsistent inputs before calculating any portfolio result."""
    n = len(sleeves)
    if n == 0 or len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must be square and match the sleeve count.")
    for name, values in sleeves.items():
        if not isfinite(values["return"]) or not isfinite(values["volatility"]):
            raise ValueError(f"{name}: return and volatility must be finite.")
        if values["volatility"] <= 0:
            raise ValueError(f"{name}: volatility must be positive for inverse weighting.")
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation [{i}, {j}] must be between -1 and 1.")
            if abs(value - correlations[j][i]) > 1e-12:
                raise ValueError(f"Correlation table is not symmetric at [{i}, {j}].")
        if abs(correlations[i][i] - 1) > 1e-12:
            raise ValueError(f"Correlation [{i}, {i}] must equal 1.")


def covariance_matrix(sleeves: dict, correlations: tuple) -> tuple:
    """Annual covariance = correlation × annual volatility × annual volatility."""
    validate_inputs(sleeves, correlations)
    volatilities = [item["volatility"] for item in sleeves.values()]
    return tuple(
        tuple(correlations[i][j] * volatilities[i] * volatilities[j] for j in range(len(sleeves)))
        for i in range(len(sleeves))
    )


def benchmark_weights(sleeves: dict) -> dict[str, float]:
    weights = dict.fromkeys(sleeves, 0.0)
    weights["Investment-grade bond fund"] = 0.40
    weights["Global equity index fund"] = 0.60
    return weights


def equal_weights(sleeves: dict) -> dict[str, float]:
    return dict.fromkeys(sleeves, 1.0 / len(sleeves))


def inverse_volatility_weights(sleeves: dict) -> dict[str, float]:
    inverse = {name: 1.0 / item["volatility"] for name, item in sleeves.items()}
    denominator = sum(inverse.values())
    return {name: value / denominator for name, value in inverse.items()}


def expected_return(weights: dict[str, float], sleeves: dict) -> float:
    return sum(weights[name] * item["return"] for name, item in sleeves.items())


def portfolio_volatility(weights: dict[str, float], covariance: tuple) -> float:
    vector = list(weights.values())
    variance = sum(
        vector[i] * vector[j] * covariance[i][j]
        for i in range(len(vector))
        for j in range(len(vector))
    )
    if variance < -1e-12:
        raise ValueError("Portfolio variance is negative; check the correlation table.")
    return sqrt(max(variance, 0.0))


def reserve_eligible_weight(weights: dict[str, float]) -> float:
    return sum(weights.get(name, 0.0) for name in RESERVE_ELIGIBLE)


def meets_objective(portfolio_return: float, objective: float) -> bool:
    return portfolio_return >= objective


def main() -> None:
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": benchmark_weights(SLEEVES),
        "Equal weight": equal_weights(SLEEVES),
        "Inverse volatility": inverse_volatility_weights(SLEEVES),
    }
    print(f"Meridian baselines | objective {OBJECTIVE_RETURN:.2%}")
    print("Weight order: " + " / ".join(SLEEVES))
    for name, weights in portfolios.items():
        portfolio_return = expected_return(weights, SLEEVES)
        volatility = portfolio_volatility(weights, covariance)
        reserve = reserve_eligible_weight(weights)
        print(f"\n{name}")
        print("  Weights (%): " + " / ".join(f"{weight * 100:.1f}" for weight in weights.values()))
        print(f"  Expected return: {portfolio_return:.2%}")
        print(f"  Volatility: {volatility:.2%}")
        print(f"  Reserve-eligible: {reserve:.1%}")
        print(f"  Meets objective: {'yes' if meets_objective(portfolio_return, OBJECTIVE_RETURN) else 'no'}")


if __name__ == "__main__":
    main()
