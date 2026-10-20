# Lab 12 — Microsoft full-analysis presentation and review

**Company:** Microsoft Corporation (MSFT)  
**Current conclusion:** **Watch / defer.** Microsoft has a strong operating franchise, but the analysis does not yet establish that the returns from current AI and cloud infrastructure investment justify the market price.  
**Presentation question:** How did I get from choosing Microsoft to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?

[Lab instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-06/lab-12-proforma-present.md) · [Company research](Microsoft_Company_Research_Report.md) · [DCF](Lab_06_MSFT.md) · [Peer comparison](Lab_08_MSFT.md) · [Pro forma](Lab_10_MSFT.md) · [Sensitivity](Lab_11_MSFT.md)

## Opening conclusion

I would not initiate Microsoft at the saved market prices. The September 10, 2026 peer P/E analysis supports **$470.89–$551.77 per share** and contains the observed **$492.44** price, but the lease-adjusted FCFF DCF produces only **$114.68 per diluted share**. The later five-year FCFE pro forma produces **$279.60 per diluted share** versus the September 28, 2026 close of **$509.22**. I do not average these methods because they answer different questions and treat reinvestment differently. The central unresolved issue is whether Microsoft's unusually high AI and data-center investment is a temporary growth investment that will generate future cash flow or a persistent capital requirement.

All per-share figures are USD. The DCF, peer comparison, and reverse DCF use a September 10, 2026 comparison date; the pro forma uses the latest completed close available when it was run, September 28, 2026. Both intrinsic-value models use 7,453 million FY2026 weighted-average diluted shares, which is an EPS basis rather than a fully reconciled valuation-date share count.

## 1. Target selection

- I selected Microsoft because its strong reported growth and operating earnings create a useful valuation question: does growth become distributable cash after the investment needed to support Azure and AI demand?
- The company is suitable for analysis because it has audited financial history, identifiable operating segments, positive earnings, public peers, and unusually consequential cash and lease-financed infrastructure spending.
- My initial view was **watch / defer initiation pending valuation**. The bullish case required incremental software and infrastructure investment to earn adequate returns; the bearish case was that demand growth could consume capital without creating enough incremental value.

**Evidence to show:** [Project 1 Edition A](Project_1_Edition_A.md) and [company research report](Microsoft_Company_Research_Report.md).

## 2. Company and evidence

Microsoft earns money through Productivity and Business Processes, Intelligent Cloud, and More Personal Computing. The model focuses on consolidated results while recognizing that subscription software, cloud consumption, advertising, gaming, licensing, and hardware have different economics.

Key FY2026 facts from Microsoft's 10-K and earnings materials, in USD millions except EPS:

| Item | FY2026 | Why it matters |
|---|---:|---|
| Revenue | 331,839 | Starting scale; 17.79% year-over-year growth |
| Operating income | 155,237 | Operating earnings base |
| Net income | 133,749 | Includes non-operating investment effects |
| Diluted EPS | $17.95 | Peer P/E denominator |
| Operating cash flow | 182,935 | Starting point for cash conversion analysis |
| Cash PP&E additions | 115,948 | Major cash reinvestment burden |
| Finance-lease asset additions | 24,608 | Noncash capacity investment captured separately |
| Cash, equivalents, and short-term investments | 76,843 | Relevant to the equity bridge, subject to excess-cash judgment |

The reported facts come primarily from Microsoft's FY2026 10-K and earnings release; the model assumptions are separately labeled as judgment. A major limitation is that maintenance and growth capex are not disclosed separately. Another is that operating cash flow less cash capex is only a diagnostic, not automatically valid FCFF.

**Evidence to show:** [Lab 10 history and sources](Lab_10_MSFT.md#three-year-history-and-sources), [saved FY2026 filing](MSFT_FY26Q4_10K.docx), and [sources log](sources.md).

## 3. Pro forma

The five-year model covers FY2027E–FY2031E and links the income statement, balance sheet, and cash flow statement. Its company-specific feature separates cash PP&E additions from finance-lease asset additions. Both increase PP&E; new finance leases also increase the lease liability. Cash is calculated last from FCFE, dividends, and repurchases.

Key assumptions are:

- Revenue growth fades from **15% to 10%**.
- Gross margin gradually recovers from **67.8% to 68.5%**.
- R&D declines modestly from **10.8% to 10.4% of revenue**, rather than assuming a sharp efficiency gain.
- Cash capex rises from **$135.0 billion to $160.0 billion**; finance-lease additions rise from **$30.0 billion to $40.0 billion**.
- Cost of equity is **10.38%**, terminal growth is **3.00%**, and annual year-end discounting is used.

The base forecast reaches FY2031 revenue of **$589.7 billion**, operating income of **$285.4 billion**, and FCFE before distributions of **$192.0 billion**. The FCFE valuation is **$2.084 trillion**, or **$279.60 per diluted share**. Terminal value supplies **78.5%** of present value.

Every annual balance-sheet gap is within $0.1 million, the $10.0 billion cash floor passes, and no revolver is required. The model's main accounting simplifications are flat other assets and liabilities, zero other income/expense, and constant weighted-average diluted shares.

**Evidence to show:** [Lab 10 assumptions and checks](Lab_10_MSFT.md#assumption-set), [saved base output](Lab_10_MSFT_output.txt), and [model](../../proforma.py).

## 4. Valuation

| Method | Result | Main interpretation or limitation |
|---|---:|---|
| Lease-adjusted FCFF DCF | **$114.68/share**; grid **$91.19–$156.02** | Starts from $45.641 billion of FY2026 FCFF after cash and lease-funded investment; 10.202614% WACC and 3% terminal growth. It may understate normalized cash flow if current infrastructure spending is temporarily elevated. |
| Peer P/E | **$470.89–$551.77/share**; median **$511.33** | Oracle and Alphabet are imperfect peers. P/E capitalizes reported earnings rather than deducting capex and is affected by business mix and investment gains. |
| Five-year FCFE pro forma | **$279.60/share** | Forecasts linked statements and future cash conversion, but depends on revenue, margins, capex, lease additions, and a terminal value equal to 78.5% of present value. |

The FCFF DCF enterprise value is **$888.543 billion**. Adding $73.043 billion of cash and deducting $106.888 billion of debt and finance-lease liabilities gives equity value of **$854.698 billion**, or $114.68 per diluted share.

The reverse DCF holds the $45.641 billion starting FCFF, 10.202614% WACC, 3% terminal growth, cash, debt, shares, and timing fixed. The required −5 to +10 percentage-point growth-shift bracket has no solution. A wider diagnostic bracket requires a **+39.898609 percentage-point** shift, producing annual FCFF growth of approximately **54.9%, 51.9%, 49.9%, 47.9%, and 45.9%** to reprice to $492.44. This is a price-consistent scenario, not a forecast.

The methods disagree principally because the P/E method values accounting earnings before capital expenditure, the FCFF DCF starts from cash flow after heavy cash and lease-funded investment, and the pro forma assumes future FCFE improves as revenue grows and investment moderates relative to scale. Differences in forecast structure and dates also mean the two intrinsic values should not be treated as directly interchangeable.

**Evidence to show:** [Lab 6 DCF and reverse DCF](Lab_06_MSFT.md), [Lab 6 output](Lab_06_MSFT_output.txt), [Lab 8 triangulation](Lab_08_MSFT.md#triangulation-with-the-week-3-dcf), and [Lab 10 valuation](Lab_10_MSFT.md#base-results-and-checks).

## 5. Sensitivity and drivers

Lab 11 changes one input at a time and recalculates every linked statement:

| Driver | Tested range | Value/share range | Span |
|---|---|---:|---:|
| Revenue growth | Base path ±2.0 percentage points each year | $252.09–$308.92 | $56.82 |
| Cash capex | Base path ±$20.0 billion each year | $261.13–$298.07 | $36.94 |

**Causal trace — higher revenue growth:** +2 percentage points per year → higher cumulative revenue → higher gross profit and operating income, partly offset by taxes and working-capital investment → FY2031 FCFE increases **$21.375 billion** → value increases **$29.32 per share** to **$308.92**.

**Causal trace — higher cash capex:** +$20.0 billion per year → higher PP&E and cash investment → operating income remains unchanged because the model holds gross margin constant and embeds depreciation in cost of revenue → later depreciation add-backs partially offset the outlay → FY2031 FCFE decreases **$9.616 billion** → value decreases **$18.47 per share** to **$261.13**.

Revenue growth is the larger driver **over these tested ranges**. That is not a probability statement and does not prove growth is inherently more important. The one-at-a-time method omits interactions: additional capex may enable additional growth. Even the $308.92 high-growth case remains below the saved $509.22 market price, so the sensitivity does not change the watch/defer conclusion.

**Evidence to show:** [Lab 11 results and causal trace](Lab_11_MSFT.md#results) and [saved sensitivity output](Lab_11_MSFT_output.txt).

## 6. Interpretation

**Conditional recommendation:** remain on watch and do not initiate from this analysis. A purchase case needs sourced evidence that incremental Azure and AI capacity is converting into operating cash flow rapidly enough to support normalized FCFF materially above the FY2026 lease-adjusted baseline, followed by a valuation rerun that provides an acceptable margin of safety.

The evidence most likely to change my view is:

- Sustained operating-cash-flow growth relative to cash PP&E spending and finance-lease additions.
- Disclosure or credible evidence separating maintenance from growth investment.
- Improving utilization, margins, or cash returns from recent AI and data-center capacity.
- A reconciled valuation-date diluted share count and equity bridge.
- Evidence supporting a normalized treatment of R&D and infrastructure investment without simply adding either expense back.

Since target selection, the conclusion remains watch/defer, but the reason is now more precise. The peer analysis shows that the market price is not obviously excessive relative to reported earnings. The intrinsic models show that the investment decision turns on cash conversion and reinvestment. The next research priority is therefore the return on incremental AI/data-center capital, not another mechanical valuation multiple.

## Live partner-review record — complete without AI

**This section records the live exchange from the notes provided.**

### As presenter

- **Partner name and company:** Drew Scheiderer — NVIDIA (NVDA).
- **Business outlook question received:** What part of Microsoft will earn the most money moving forward?
- **My answer:** Cloud integration with Copilot, or a related combination of Microsoft's cloud platform and AI assistant products, is the most likely earnings driver.
- **Model/valuation question received:** Why did the valuation methods produce such different values?
- **My answer:** The models treat reinvestment differently and use different cash-flow measures. The FCFF DCF begins with cash flow after heavy cash and lease-funded infrastructure investment, while the FCFE pro forma forecasts linked future statements and improving cash generation. The peer P/E method values reported earnings rather than cash flow after capital expenditure.
- **Strategy/interpretation question received:** Do you think Microsoft's approach to AI is correct?
- **My answer:** Yes. Microsoft is using its existing strengths in enterprise software and cloud distribution rather than trying to win solely by developing the best standalone AI model. I view that as a sensible approach for Microsoft.

### As reviewer

- **Selection/evidence question I asked:** Why did you select the technology sector?
- **Drew's answer:** Technology is the most interesting sector right now.
- **Model/valuation questions I asked:** How accurate is the beta used in your analysis? Which valuation do you trust more—the DCF or the pro forma?
- **Drew's answer on beta and capital structure:** His model uses a beta of **1.8**, but he believes a more realistic beta may be approximately **2.2**, so he is uncertain about the model input. He also noted that NVIDIA's capital structure is approximately **99.8% equity capital**, which materially affects the valuation.
- **Drew's preferred valuation:** He trusts the pro forma more because the beta and heavily equity-weighted capital structure have a large effect on the DCF valuation.

## Reproducibility and integrity note

On October 1, 2026, the existing scripts were rerun from the course workspace:

```bash
python3 dcf.py
python3 comps.py
python3 proforma.py --sensitivity
```

The saved conclusions reproduce: DCF value **$114.6784/share**, peer median **$511.33/share**, pro-forma base **$279.60/share**, and passing sensitivity/restored-base checks. This file prepares the presentation from existing work. It does not claim that the required live presentation, partner questions, evidence check, explanation-back, feedback, reflection, GitHub upload, or Brightspace checkout has occurred.
