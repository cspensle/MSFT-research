"""Regression and directional tests for the integrated Project 1 workbench."""

import math
import unittest

from proforma import project
from workbench import (
    BASE_TERMINAL_GROWTH,
    BASE_WACC,
    scenario_assumptions,
    validation_checks,
    value_forecast_fcff,
)


class WorkbenchTests(unittest.TestCase):
    def test_base_checks_and_finite_value(self):
        assumptions = scenario_assumptions()
        results = project(assumptions)
        checks = validation_checks(results, assumptions, BASE_WACC, BASE_TERMINAL_GROWTH)
        self.assertTrue(all(passed for passed, _ in checks.values()))
        self.assertTrue(math.isfinite(value_forecast_fcff(results, assumptions).value_per_share))

    def test_higher_wacc_reduces_value(self):
        assumptions = scenario_assumptions()
        results = project(assumptions)
        lower = value_forecast_fcff(results, assumptions, BASE_WACC - 0.01).value_per_share
        higher = value_forecast_fcff(results, assumptions, BASE_WACC + 0.01).value_per_share
        self.assertGreater(lower, higher)

    def test_higher_terminal_growth_increases_value(self):
        assumptions = scenario_assumptions()
        results = project(assumptions)
        lower = value_forecast_fcff(results, assumptions, terminal_growth=0.02).value_per_share
        higher = value_forecast_fcff(results, assumptions, terminal_growth=0.04).value_per_share
        self.assertGreater(higher, lower)

    def test_year_specific_cash_capex_overrides(self):
        assumptions = scenario_assumptions(
            cash_capex_overrides={2030: 125_000.0, 2031: 120_000.0}
        )
        self.assertEqual(
            assumptions["cash_capex"],
            [135_000.0, 145_000.0, 150_000.0, 125_000.0, 120_000.0],
        )
        base_assumptions = scenario_assumptions()
        base_results = project(base_assumptions)
        changed_results = project(assumptions)
        base_value = value_forecast_fcff(base_results, base_assumptions).value_per_share
        changed_value = value_forecast_fcff(changed_results, assumptions).value_per_share
        self.assertGreater(changed_value, base_value)

    def test_failure_demo_blocks_gordon_growth(self):
        assumptions = scenario_assumptions()
        results = project(assumptions)
        checks = validation_checks(results, assumptions, BASE_WACC, BASE_WACC)
        self.assertFalse(checks["Terminal convention"][0])
        with self.assertRaises(ValueError):
            value_forecast_fcff(results, assumptions, BASE_WACC, BASE_WACC)


if __name__ == "__main__":
    unittest.main()
