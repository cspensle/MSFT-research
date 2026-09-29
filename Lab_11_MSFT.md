# Lab 11 — Microsoft pro-forma sensitivity

**Company:** Microsoft Corporation (MSFT) · **Base model:** [Lab 10](Lab_10_MSFT.md)  
**Question:** Which assumptions drive Microsoft's forecast and value, and what explains their effects?

[Lab instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-06/lab-11-proforma-what-if.md) · [Model](../../proforma.py) · [Saved output](Lab_11_MSFT_output.txt)

## Inputs and reproducible ranges

| Driver | Lower | Base | Higher | Years | Range reason |
|---|---|---|---|---|---|
| Revenue growth | Base − 2.0 percentage points each year | 15%, 13%, 12%, 11%, 10% | Base + 2.0 percentage points each year | FY2027E–FY2031E | A symmetric range around a judgment path; it remains within a plausible fade from Microsoft's recent mid-to-high-teens growth. |
| Cash capital spending | Base − $20,000m each year | $135,000m, $145,000m, $150,000m, $155,000m, $160,000m | Base + $20,000m each year | FY2027E–FY2031E | About one-sixth of FY2026 cash capex, large enough to test AI-infrastructure intensity without changing lease additions. |

Outputs are FY2031E operating income, FY2031E **FCFE**, and value per diluted share. Each run starts from a fresh deep copy of the base inputs. Only the named independent input changes; all linked statement balances recalculate.

## Locked changed-input record

**Locked at 2026-09-29 16:37:42 EDT before the official saved run.**

- Revenue growth, base → +2.0 percentage points per year: operating income, FCFE, and value should rise. Rough expectation: final-year operating income roughly **+$25 billion** and value approximately **+$30/share**, because the cumulative revenue effect flows through gross profit and operating leverage while working capital absorbs part of the gain.
- Cash capital spending, base → +$20,000 million per year: final-year operating income should be **unchanged** because this model forecasts operating margin above D&A, while FCFE and value should fall. Rough expectation: final-year FCFE roughly **−$10 billion** after added depreciation partially offsets the cash outlay, and value roughly **−$20/share**.
- Unit check: revenue changes are percentage-point shifts, not percent changes; capex changes are USD millions. Finance-lease additions, margins, working-capital days, tax, financing, and valuation assumptions stay at base.

## Results

| Driver and case | FY2031 operating income | Change | FY2031 FCFE | Change | Value/share | Change | Checks |
|---|---:|---:|---:|---:|---:|---:|---|
| Revenue growth −2.0 pp | 260,865.8 | −24,553.1 | 172,013.7 | −19,984.6 | $252.09 | −$27.51 | Pass |
| Revenue growth base | 285,418.9 | — | 191,998.2 | — | $279.60 | — | Pass |
| Revenue growth +2.0 pp | 311,786.9 | +26,367.9 | 213,373.3 | +21,375.1 | $308.92 | +$29.32 | Pass |
| Cash capex −$20,000m | 285,418.9 | 0.0 | 201,614.0 | +9,615.8 | $298.07 | +$18.47 | Pass |
| Cash capex base | 285,418.9 | — | 191,998.2 | — | $279.60 | — | Pass |
| Cash capex +$20,000m | 285,418.9 | 0.0 | 182,382.4 | −9,615.8 | $261.13 | −$18.47 | Pass |

The base run before sensitivity and the restored base both report FY2031 operating income of **$285,418.9 million**, FCFE of **$191,998.2 million**, and value of **$279.60/share**—an exact match. Every scenario's balance-sheet gap is zero within displayed precision and every cash-floor check passes.

## Prediction reconciliation and causal trace

The revenue prediction was directionally and approximately correct: the higher case adds **$26.4 billion** of final-year operating income and **$29.32/share** of value. The effect is asymmetric around base because a two-point annual growth shift compounds across all five years. Higher revenue increases gross profit and operating income; taxes and additional receivables/inventory absorb part of the gain before FCFE.

The capex prediction was also directionally and approximately correct: the higher case leaves operating income unchanged, reduces final-year FCFE by **$9.6 billion**, and reduces value by **$18.47/share**. Each extra $20 billion outlay increases PP&E; the resulting depreciation add-back partly offsets later FCFE effects. Gross margin already includes the operating effect of depreciation, so subtracting D&A again in operating income would double-count it.

## Main driver over these ranges

| Driver | Operating-income span | FCFE span | Value/share span |
|---|---:|---:|---:|
| Revenue growth | $50,921.1m | $41,359.6m | $56.82 |
| Cash capital spending | $0.0m | $19,231.5m | $36.94 |

**Over these ranges**, revenue growth is the larger driver of operating income, FCFE, and value. That ranking is conditional on the chosen ranges; it is not evidence that growth is inherently more important than reinvestment. Cash capex has no operating-income span because the model holds gross margin constant and treats D&A as embedded in cost of revenue. The valuation conclusion remains defer/watch: even the higher-growth result of **$308.92/share** remains well below the September 28 market close of $509.22, so the research priority is still the conversion of AI/data-center spending into sustainable cash returns.

One-at-a-time sensitivity is not a probability forecast. It changes one independent input while holding the others at base, so it does not capture correlations—for example, higher capex may enable higher revenue growth.

## Partner evidence

Q1: NVDA - Revenue Groth and gross margin
Q2: 3.29% Change per 1-4% in revenue growth, Gross margin had 1.8% per 1%
Q3: Growth was convex shaped


Run from the course workspace:

```bash
python3 proforma.py --sensitivity
```

**Integrity note:** The locked prediction above is an AI-assisted analytical prediction. This file does not claim partner verification, a Git commit, GitHub upload, or Brightspace submission.

