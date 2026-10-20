# Lab 14 — Portfolio Baselines

**Case:** Meridian Foundation Reserve  
**Engine:** [`portfolio.py`](portfolio.py)  
**Mandate checker:** [`mandate.py`](mandate.py)  
**Official instructions:** [FIN43900 Lab 14](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/lab-14-portfolio-baselines.md)

## D — Decision question

What does each simple portfolio earn and risk, and does any meet the Meridian mandate?

## R — Inputs and conventions

The four sleeve returns, volatilities, and correlation table in `portfolio.py` are **course-authored training inputs**, not market estimates. Annual expected returns and standard deviations use decimal inputs. The 6.5% return objective is 2.5% estimated CPI plus the mandate's 4.0% spread. Weights are fractions in calculations and percentages in the display; results are rounded only when displayed. Treasury bills and the Treasury 10-year note are reserve eligible.

Covariance is `correlation × volatility_i × volatility_j`; expected return is `Σ weight_i × return_i`; volatility is `sqrt(Σ_i Σ_j weight_i × weight_j × covariance_ij)`. Returns are arithmetic expectations, and no compounding or time-series estimation is used.

## I/V — Run and known-answer check

From the course workspace:

```bash
python3 ColinSpensley/MSFT/mandate.py
python3 ColinSpensley/MSFT/portfolio.py
```

| Portfolio | Bills / 10-year / IG / equity weights | Expected return | Volatility | Reserve eligible | Meets 6.5%? |
|---|---:|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0% | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0% | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6% | 3.77% | 1.05% | 90.3% | No |

All displayed values match the lab's known answers. For the benchmark, the variance calculation is `0.40² × 0.06² + 0.60² × 0.16² + 2 × 0.40 × 0.60 × 0.06 × 0.16 × 0.25 = 0.010944`. Its square root is 10.46% after display rounding. The correlation term adds 0.001152 to variance; ignoring it would understate risk.

**Correlation probes:** Setting both IG–equity correlations to 0.50 produced 11.00% benchmark volatility. Setting both to 1.3 raised `ValueError: Correlation [2, 3] must be between -1 and 1.` Changing one cell only raised `ValueError: Correlation table is not symmetric at [2, 3].` The original 0.25 inputs remain in the file.

**Mandate cross-check:** Candidate E is the 40% IG / 60% equity benchmark. It passes weight total, long-only, five-day liquidity, and issuer concentration checks, but has **0.0% reserve eligible versus the 3.0% minimum**. The checker reports one failed rule. Thus the benchmark meets the estimated return objective but is not mandate compliant as written. The calendar-year loss statement still requires CIO clarification.

## Interpretation and remaining live steps

Inverse volatility assigns 84.3% to Treasury bills because their assumed 0.5% volatility is much lower than the other sleeves' 6–16%; the method does not optimize expected return. The benchmark is the clearest first comparison for the CIO because it is the stated reference and exposes a direct conflict with the reserve rule. It should not be presented as an adoptable portfolio under the current mandate.

**Live partner work (student-reported):** We swapped laptops and ran both versions of `portfolio.py`; both ran correctly. I explained the correlation matrix in my `portfolio.py` to my partner. A line-by-line explanation of the portfolio-volatility calculation, the partner-file invalid-correlation test, and the student AI quiz are not claimed as completed here. The separate Thursday prework needs the student's own Project 2 mandate and a sourced five-year monthly adjusted-close data set; no prices or download dates have been invented.

### Streamlit preparation for Lab 15

The [Week 9 course page](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-09/README.md) links to Streamlit's [installation guide](https://docs.streamlit.io/get-started/installation/command-line), which runs the built-in Hello demo. Streamlit 1.66.0 was installed in this workspace's `.venv` from the local package cache. The demo started on local port 8502 and returned HTTP 200. Run it again from the course workspace with:

```bash
.venv/bin/python -m streamlit hello
```

The Hello demo is bundled with the installed package, so it needs no separate downloaded source file. The existing root `requirements.txt` declares Streamlit for a fresh installation on another machine.

## AI-use record

AI wrote the standard-library engine, added benchmark candidate E, ran the known-answer and invalid-input checks, and drafted this record. The student should review the code and make the final CIO interpretation in the live exercise.
