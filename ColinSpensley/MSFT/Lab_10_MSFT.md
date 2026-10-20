# Lab 10 — Microsoft five-year pro forma

**Company:** Microsoft Corporation (MSFT)  
**Forecast period:** FY2027E–FY2031E · **Units:** USD millions except per-share data  
**Question:** What are five years of Microsoft's statements worth, built from assumptions that can be defended?

[Lab instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-10-proforma-your-company.md) · [Model](../../proforma.py) · [Saved output](Lab_10_MSFT_output.txt)

## Company-specific line

The line that makes this model different is **data-center reinvestment financed partly with finance leases**. Cash additions to PP&E and noncash finance-lease asset additions are separate assumptions. Both increase PP&E; new finance leases also increase the lease liability. This preserves the financing link and prevents lease-funded capacity from disappearing from the investment analysis.

## Three-year history and sources

The figures below are reported GAAP amounts. FY2024 comes from Microsoft's [FY2024 10-K](https://www.sec.gov/Archives/edgar/data/789019/000095017024087843/msft-20240630.htm), FY2025 from the [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm), and FY2026 from the [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm). Every item was also retrieved from the SEC XBRL facts attached to those filings. SG&A is sales and marketing plus general and administrative expense.

| History item | FY2024 | FY2025 | FY2026 | Filing location |
|---|---:|---:|---:|---|
| Revenue | 245,122 | 281,724 | 331,839 | Consolidated statements of income |
| Gross profit | 171,008 | 193,893 | 225,465 | Consolidated statements of income |
| SG&A | 32,065 | 32,877 | 34,666 | Consolidated statements of income; two reported lines summed |
| Net income | 88,136 | 101,832 | 133,749 | Consolidated statements of income |
| Inventory | 1,246 | 938 | 1,397 | Consolidated balance sheets |
| PP&E, net | 135,591 | 204,966 | 313,076 | Consolidated balance sheets |
| Stockholders' equity | 268,477 | 343,479 | 442,387 | Consolidated balance sheets |

Manual checks: I traced FY2026 revenue of **$331,839 million** to the FY2026 income statement and FY2025 PP&E of **$204,966 million** to the comparative balance sheet. These are filing values, not provider estimates.

## Historical ratios

| Ratio | FY2024 | FY2025 | FY2026 |
|---|---:|---:|---:|
| Reported revenue growth | 15.67% | 14.93% | 17.79% |
| Gross margin | 69.76% | 68.82% | 67.94% |
| SG&A / gross profit | 18.75% | 16.96% | 15.38% |
| Inventory days | 6.14 | 3.90 | 4.79 |
| Depreciation / opening PP&E | 15.89% | 16.23% | 16.73% |
| Effective tax rate | 18.23% | 17.63% | 19.40% |
| Cash capital spending | 44,477 | 64,551 | 115,948 |
| Finance-lease asset additions | 11,633 | 20,511 | 24,608 |

Cash capital spending matches the filing and the [Stock Analysis provider field](https://stockanalysis.com/stocks/msft/financials/cash-flow-statement/) in all three years. Microsoft's filing describes reported growth and constant-currency growth, but not a consolidated organic or same-store measure. I therefore use reported growth and do not relabel constant-currency growth as organic growth.

## Assumption set

| Assumption | Value | Label | Reason |
|---|---|---|---|
| Revenue growth, FY2027E–FY2031E | 15%, 13%, 12%, 11%, 10% | Judgment | Starts below FY2026's 17.8% and fades as scale rises; management guided to double-digit FY2027 revenue growth. |
| Gross margin | 67.8%, 67.9%, 68.1%, 68.3%, 68.5% | Judgment | FY2024–FY2026 margin fell as AI infrastructure scaled; the path assumes only a gradual efficiency recovery. |
| R&D / revenue | 10.8%, 10.7%, 10.6%, 10.5%, 10.4% | Judgment | Near FY2026's 10.7%, with modest leverage rather than a sharp cut. |
| SG&A / revenue | 10.4%, 10.2%, 10.0%, 9.8%, 9.7% | Judgment | Continues the historical scale benefit at a slowing pace. |
| Effective tax rate | 19.40% | History | FY2026 tax expense divided by pretax income; close to management's approximately 20% FY2027 outlook. |
| Depreciation / opening PP&E | 16.73% | History | FY2026 depreciation of 34,300 divided by FY2025 PP&E of 204,966. |
| Cash capital spending | 135,000; 145,000; 150,000; 155,000; 160,000 | Judgment | FY2026 cash additions were 115,948 and management expects continued high investment; the path rises but decelerates. |
| Finance-lease additions | 30,000; 33,000; 36,000; 38,000; 40,000 | Judgment | Extends the reported 11,633 → 20,511 → 24,608 pattern, while acknowledging classification may shift toward operating leases. |
| Receivable / inventory / payable days | 88.96 / 4.79 / 145.51 days | History | FY2026 closing balances divided by the matching revenue or cost-of-revenue base. |
| Stock compensation | 3.738% of revenue | History | FY2026 stock compensation of 12,405 divided by revenue. |
| Dividends | 28,600 → 39,000 | Judgment | Approximately 8% annual growth from the FY2026 cash dividend base. |
| Share repurchases | 22,000 annually | Judgment | Holds near FY2026's 22,271 rather than assuming acceleration. |
| Borrowing repayment | 4,000 annually | Judgment | Gradual run-off against FY2026 borrowings of 40,294; no speculative refinancing. |
| Finance-lease principal | 5% of opening liability | Judgment | Rounded from FY2026 principal payments relative to the opening liability. |
| Other assets and liabilities | Flat | Judgment | Avoids inventing acquisition, investment-gain, tax, or legal-event forecasts; this is a material simplification. |
| Other income / expense | Zero | Judgment | Does not repeat FY2026's OpenAI investment gain in operating forecasts. |
| Cost of equity / terminal growth | 10.38% / 3.00% | Judgment | Carries the CAPM convention from Lab 06 and a long-run nominal growth assumption. |
| Diluted shares | 7,453 million | Fact | FY2026 diluted share count used for EPS. |

Microsoft's FY2026 call said calendar-2026 capex remained approximately **$175 billion** after a lease-classification effect, and FY2027 capex would grow year over year. It also said FY2027 free cash flow should remain positive. Those statements anchor direction, not the exact five-year path. [Microsoft FY2026 Q4 earnings call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4).

## Opening balance sheet

FY2026 reported assets of 758,376 equal reported liabilities of 315,989 plus equity of 442,387. The model separately identifies cash 20,935; short-term investments 55,908; receivables 80,876; inventory 1,397; PP&E 313,076; accounts payable 42,416; borrowings 40,294; and finance-lease liabilities 66,594. The residual **other assets of 286,184** and **other liabilities of 166,685** keep every reported balance in scope without pretending to forecast immaterial lines individually.

## Base results and checks

| Output | FY2027E | FY2031E |
|---|---:|---:|
| Revenue | 381,614.8 | 589,708.5 |
| Operating income | 177,832.5 | 285,418.9 |
| Net income | 143,333.0 | 230,047.6 |
| FCFE before dividends and buybacks | 61,880.2 | 191,998.2 |
| Ending cash | 32,215.2 | 372,476.2 |
| Assets − liabilities − equity | 0.0 | 0.0 |

Every annual balance check passes within **$0.1 million**, the $10,000 million cash floor passes, and no revolver is required. Cash is computed last from linked FCFE, dividends, and repurchases. The model refuses before valuation if either check fails.

The five-year FCFE valuation is **$2,083,859.5 million**, or **$279.60 per diluted share**. Terminal value supplies 78.5% of total present value. The latest completed close available when this lab was run was **$509.22 on September 28, 2026**; the model is **$229.62 below** that price on the same diluted-share basis. [Historical price source](https://www.marketbeat.com/stocks/NASDAQ/MSFT/chart/). This is a research question, not a recommendation: does the market assume a much faster payoff from AI capacity, a lower reinvestment burden, or both?

## Partner fresh-eyes review

**Required human step — not fabricated:** the assigned partner's specific attack, my two-sentence response, and the attack I perform on the partner's model must be added after the live exchange. The strongest judgment to challenge is the cash-capex path because it drives FCFE while management's lease-classification change makes headline capex less comparable.

## Reflection

The label I would defend longest is the zero forecast for other income: repeating an investment gain would obscure operating economics. The surprising filing number is FY2026 total capital investment of **$140,556 million** when cash PP&E additions and finance-lease additions are combined.

Run from the course workspace:

```bash
python3 proforma.py
```

**Integrity note:** This file does not claim that a partner exchange, GitHub upload, Brightspace checkout, or independent manual student action occurred when it did not.

