# Lab 06 — Microsoft Sensitivity and Reverse DCF

**Company:** Microsoft Corporation (MSFT). **Prepared:** September 10, 2026.  
**Call:** Watch / defer. The lease-adjusted estimate is **$114.68 per share**, versus **$492.44** at the September 10 regular-session close. This is a classroom valuation built from explicit analyst estimates, not a company forecast or proof that the market is wrong.

[Assignment](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-03/lab-06-sensitivity-and-reverse-dcf.md) · [Single Python file](../../dcf.py) · [MSFT terminal output](Lab_06_MSFT_output.txt) · [Training verification](Lab_06_training_output.txt)

## Sources and five input rows

Historical inputs are from the latest annual filing, FY2026 ended June 30, filed July 29, 2026. The [Microsoft-hosted 10-K](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/MSFT_FY26Q4_10K.docx) is saved [locally](MSFT_FY26Q4_10K.docx). Locators below are the filing's named statements, notes, and table rows; no page numbers are inferred. Market observations and forecasts are dated separately. This lab updates the earlier report's historical cutoff to September 10.

All monetary inputs are **USD millions**, shares are **millions**, and rates are nominal annual decimals in code.

| Required input | Model value | Status and as-of date | Exact locator and derivation |
|---|---|---|---|
| Starting FCFF | 45,641.0331 | **Estimate**, FY ended June 30, 2026 | 10-K cash flow statement: net cash from operations 182,935; additions to property and equipment 115,948. Note 10, paragraph after debt table: cash interest 1,500 (rounded). Note 13, Other Information: operating cash flows from finance leases 2,547; finance-lease ROU additions 24,608. Income statement: taxes 32,185 / pretax income 165,934. Reconciliation below. |
| Growth, Years 1–5 | 15%, 12%, 10%, 8%, 6% | **Analyst forecast**, September 10, 2026 | 10-K Item 7, Results of Operations and Liquidity and Capital Resources; historical revenue and cash-flow comparisons. This path assumes cash recovery and then a fade; it is not extracted guidance. |
| WACC | 10.202614% | **Estimate**, September 10, 2026 | [H.15](https://www.federalreserve.gov/releases/h15/), nominal 10-year row, September 9 column; [MSFT quote](https://stockanalysis.com/stocks/msft/), Beta field; 10-K Notes 10 and 13; market weights and calculations below. |
| Terminal growth | 3.00% | **Analyst estimate**, September 10, 2026 | [Federal Reserve July 10 report](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part3.htm), Table 1: June projections' longer-run median real growth 2%, PCE inflation 2%. A 3% nominal perpetual assumption is below the approximately 4.04% combined benchmark; this is not a Fed forecast for MSFT. |
| Cash / debt / diluted shares | 73,043 / 106,888 / 7,453 | Historical June 30 balances; FY2026 diluted average; **bridge estimates** | Balance sheet: cash and short-term investments 76,843. Note 1, Contract Balances and Other Receivables: restricted short-term investments 3,800 excluded. Note 10: total borrowing 40,294; Note 13: finance-lease liabilities 66,594. Note 2: common stock and equivalents (C), 7,453. |

**Reverse-DCF target:** **$492.44 per share, September 10, 2026, 4:00 p.m. EDT**, regular-session close. Source: [Stock Analysis, quote header](https://stockanalysis.com/stocks/msft/), accessed September 10. The page separately shows after-hours trading; the model consistently uses the regular close. The quote is a vendor observation, not a company filing.

### Starting FCFF and lease treatment

The lab's cash-capex bridge is:

```text
Tax-rate estimate = 32,185 / 165,934 = 19.396266%
Cash-interest proxy = 1,500 debt interest + 2,547 finance-lease interest = 4,047
After-tax cash-interest proxy = 4,047 × (1 − tax rate) = 3,262.0331
Cash-basis FCFF = 182,935 + after-tax interest − 115,948 = 70,249.0331
Lease-adjusted starting FCFF = cash-basis FCFF − 24,608 = 45,641.0331
```

**Explicit extension to the lab's cash-only calculation:** I include finance-lease asset additions as capital expenditure and finance-lease liabilities as debt. This avoids forecasting a capital-intensive business as though newly leased assets were free. Finance-lease principal payments are financing cash flows, so they are not deducted again from FCFF. Operating-lease cash costs remain in operations and operating-lease liabilities are not separately deducted from enterprise value.

**Estimation limits:** Note 10 rounds debt cash interest to billions and does not separately identify here the amount attributable to interest capitalized into assets. Adding the entire disclosed amount back is an approximation; the effective tax rate is also a proxy for the marginal interest tax shield. These are labeled estimates, not exact unlevered cash flow. The treatment does not separately strip all investment income from operating cash flow, expense stock compensation, or forecast capitalized interest. Those refinements could change value.

The cash-only bridge, holding other inputs fixed, would produce **$178.96 per share**; it also remains below the price. It is a comparison, not the selected centre case. All runnable results use the lease-adjusted starting value.

### WACC build

| Component | Input and basis |
|---|---|
| Risk-free rate | 4.83%; September 9 Treasury 10-year observation in the September 10 H.15 release, the latest available column in that release. |
| Beta | 1.11; Stock Analysis field accessed September 10. Vendor estimate; lookback methodology not established here. |
| Equity risk premium | 5%; assignment convention, not a newly measured premium. |
| Cost of equity | 4.83% + 1.11 × 5% = **10.38%**. |
| Borrowing cost proxy | 5.49%; Note 10's upper effective rate for the 2024 issuance. Conservative selected proxy within the debt note, not a current traded yield or company-wide average. |
| Finance-lease cost proxy | 4.5%; Note 13 weighted-average finance-lease discount rate. |
| Equity market-value proxy | $492.44 × 7,427 June 30 basic shares = **3,657,351.88**. Shares are dated, not a claim of an exact September 10 count. |
| Debt market-value proxy | Note 10 borrowing fair value 36,500 + Note 13 lease liability 66,594 = **103,094**. Lease book value proxies fair value. |
| Weighted debt cost | (36,500 × 5.49% + 66,594 × 4.5%) / 103,094 = **4.850505%**, before tax. |

Equity weight = 97.258463%; debt weight = 2.741537%.

**WACC = equity weight × 10.38% + debt weight × debt cost × (1 − tax rate) = 10.202614%.** Full precision is retained in code. The equity bridge uses debt carrying value; WACC uses disclosed debt fair value plus a lease proxy. The differing totals are intentional.

### Forecast rationale and conventions

The 10-K income statement implies revenue growth of 17.79%, while cash flow less cash capex fell 6.46% year over year. I therefore do not equate revenue growth with FCFF growth. The forecast assumes 15% initial FCFF recovery, tapering to 6% by Year 5, as investment yields cash and the business matures. **This recovery assumption is uncertain**, especially because the starting measure subtracts heavy lease-funded investment.

Cash of 73,043 is assumed non-operating after excluding disclosed restricted short-term investments; no further operating-cash reserve is assumed. Other long-term investments are not separately added. Diluted shares follow the lab's weighted-average EPS requirement and stay constant; they are not a complete forward dilution model.

Five annual forecast periods start at the valuation date; FY2026 is the historical run-rate baseline, not a claim that those periods precisely coincide with future fiscal years. Cash flows occur at each year-end. Year 6 FCFF sets terminal value at the end of Year 5, discounted five periods. No midyear or stub-period adjustment is used. Dollar calculations retain full precision; the first twelve lines show four decimals, grids show cents.

## Reasonableness

The model gives **$114.68** beside **$492.44**, a ratio of **0.2329×**. The lab's 0.5×–2× band is **$246.22–$984.88**, so the estimate is **outside and below** that band. I have not adjusted the forecast or WACC to force a match.

The input I distrust most is the **five-year FCFF growth path**. A single growth sequence cannot distinguish temporary infrastructure expansion from recurring replacement needs, or capture the timing of returns on that investment. The market may imply a faster cash-flow recovery, but that needs evidence rather than an automatic upward revision. Terminal value contributes **73.30%** of enterprise value, so long-run assumptions also matter substantially.

## Grid and direction

| WACC / terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9.2026% | $118.74 | $134.38 | $156.02 |
| 10.2026% | $103.28 | $114.68 | $129.75 |
| 11.2026% | $91.19 | $99.79 | $110.79 |

The exact base WACC is 10.20261404%; the displayed grid rounds its label. The **centre is $114.68**. Value decreases down each column as WACC rises and increases rightward as terminal growth rises. The corner range is **$91.19–$156.02**, from high WACC/low terminal growth to low WACC/high terminal growth. The other corners are $118.74 and $110.79. Every cell is below the target price.

The directional prediction is that high WACC and low terminal growth produce the lowest value, while low WACC and high terminal growth produce the highest. This is an analytical prediction, not a claim that a pre-run classroom response was recorded. Code marks terminal growth greater than or equal to WACC as `INVALID`.

## Reverse DCF

**Solved variable:** one additive shift to all five explicit annual FCFF growth rates. This is a change in percentage points, not a proportional percentage increase.

The required **−5 to +10 percentage-point bracket has no solution** for $492.44. The script reports that fact. A separately disclosed **−5 to +100-point diagnostic bracket** then solves to **+39.898609 percentage points**. Widening the numerical search does not change the base forecast or endorse such growth.

Implied annual path: **54.898609%, 51.898609%, 49.898609%, 47.898609%, 45.898609%**. Repricing gives **$492.440000** within $0.0000001 tolerance.

Held fixed: starting FCFF 45,641.0331; WACC 10.20261404%; terminal growth 3%; cash 73,043; debt 106,888; diluted shares 7,453; five explicit years; annual end-of-year cash flows; terminal value discounted five years. The base growth path's relative differences also stay fixed. WACC is not recalculated as the solver changes growth.

This is one set of growth assumptions consistent with the price under the chosen model. It is not proof of mispricing. The unusually high implied path highlights the importance of starting cash flow and the model's treatment of reinvestment.

## Conditional call

**Watch / defer. Initiate only if price falls to $91.74 or below** (an analyst-selected 20% margin below this base estimate) **and subsequent evidence supports the forecast and lease/cash-flow treatment; otherwise remain on watch.** A higher entry threshold would require a documented new cash-flow forecast and a rerun, not simply the current market price.

**Monitor:** quarterly operating cash flow less cash PP&E spending and finance-lease asset additions, reconciled to the same after-tax-interest convention. Sustained improvement should support the forecast; deterioration would weaken it.

## Verification and reproducibility

Training was run before the MSFT run. All twelve original values match, all nine training grid cells round to the assignment's table, and the training reverse DCF at $30 solves to **+1.777948 points**. See [saved training output](Lab_06_training_output.txt).

Also checked: MSFT grid centre and both directions; an independent discounted-value calculation; reverse-DCF repricing; unreachable targets; rejection of growth at or below −100%; invalid brackets; invalid terminal-growth cells; both command-line modes. No second valuation script was created.

From the course workspace:

```bash
python3 dcf.py
```

To reproduce training:

```bash
python3 dcf.py --training
```

**Prepared artifacts:** this write-up, `dcf.py`, source filing, and both output logs. GitHub upload and Brightspace submission have not been performed. No partner participation, quiz answers, or student reflection is fabricated. Review the forecast and conditional call as your own analytical choices before submitting.
