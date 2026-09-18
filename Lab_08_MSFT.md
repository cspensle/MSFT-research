# Lab 08 — Microsoft peer P/E and DCF triangulation

**Company:** Microsoft Corporation (MSFT). **Valuation and comparison date:** September 10, 2026.  
**Question:** What would one Microsoft share be worth at defensible peer P/E multiples, and how does that compare with the saved Week 3 DCF?  
[Lab instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-04/lab-08-deal-triangulation.md) · [Calculator](../../comps.py) · [Saved output](Lab_08_MSFT_output.txt) · [Week 3 DCF](Lab_06_MSFT.md)

## Define and discover

Microsoft earns money through three broad groups: Productivity and Business Processes (including Microsoft 365, LinkedIn, and Dynamics), Intelligent Cloud (including Azure and server products), and More Personal Computing (including Windows, devices, gaming, and search). The business combines subscriptions and consumption-based cloud revenue with licensing, advertising, content, and hardware. Its FY2026 reported GAAP diluted EPS is positive at **$17.95**. The annual result was published July 29, 2026, before the valuation date. [Microsoft FY2026 earnings release](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast), Fiscal Year 2026 Results; [Microsoft FY2026 10-K](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/MSFT_FY26Q4_10K.docx), Item 1 and Note 2.

The focused research need is to find listed operating companies with meaningful enterprise cloud and recurring software economics while identifying business-mix, capital-intensity, leverage, and earnings-quality differences that can make their P/Es diverge from Microsoft's.

## Policy written before candidate selection

Admit a U.S.-listed operating company whose material businesses include enterprise cloud infrastructure, platforms, or applications and recurring software subscriptions or support. Require positive latest annual reported GAAP diluted EPS public by September 10, 2026, a USD share price from the same trading date, and a compatible ordinary-share basis. Qualify rather than automatically exclude a company for advertising, hardware, services, on-premise software, fiscal-year timing, capital intensity, or leverage when enterprise cloud/software economics remain material. Exclude a company if those economics are immaterial, annual GAAP EPS is nonpositive or unavailable, the price/EPS share or currency bases cannot be reconciled, or the security is a fund, financing vehicle, or non-operating shell.

Before inspecting the numbers, the expected rejection evidence was: cloud/software being incidental rather than economically material; earnings dominated by an unrepresentative event without adequate disclosure; an incompatible security or currency; nonpositive earnings; or a price/EPS date and share basis that could not be verified.

## Candidate investigation and decisions

| Candidate | Decision | Business evidence and important difference |
|---|---|---|
| Oracle (ORCL) | **Use, with capital-structure and reinvestment qualification** | Oracle supplies enterprise applications and infrastructure through cloud, on-premise, and hybrid models; its three businesses are cloud and software, hardware, and services. Cloud was 51% of FY2026 revenue. This is a close match to Microsoft's enterprise cloud/software economics. Oracle is much more concentrated in enterprise IT and its FY2026 capital expenditures of $55.663 billion exceeded operating cash flow of $31.977 billion, while interest expense was $4.599 billion. Those reinvestment and leverage differences can affect the P/E. [Oracle FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm), Item 1 Business and Item 7 cash-flow and interest tables. |
| Alphabet Class A (GOOGL) | **Qualify, include** | Google Cloud earns consumption fees and subscriptions from infrastructure, platform, applications, Workspace, and other enterprise services, which overlaps Azure and Microsoft 365. However, Alphabet primarily monetizes advertising: FY2025 Google advertising revenue was $294.691 billion versus Google Cloud revenue of $58.705 billion. Alphabet also reported $24.080 billion of net equity-security gains in other income. Its consolidated EPS therefore reflects a substantially different mix and earnings-quality exposure. [Alphabet FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm), Item 1 Google Cloud; Item 7 revenue and other-income tables; Note 15 segments. |

Both candidates meet the prewritten threshold, but neither is a pure Microsoft twin. Oracle is the closer operating match; Alphabet remains useful only with the advertising and investment-gain qualification visible.

## Inputs and calculation

Prices are unadjusted regular-session closes in USD/share on **September 10, 2026**. Earnings are the latest annual **reported GAAP diluted EPS** public by that date; adjusted EPS is not mixed into the calculation. Fiscal-year timing differs and is disclosed rather than silently treated as identical. Calculations retain full input precision; displayed prices round to cents and multiples to six decimals.

| Company | September 10 close | Annual GAAP diluted EPS | Fiscal year-end | EPS publication date and source |
|---|---:|---:|---|---|
| Microsoft, target | $492.44 | $17.95 | June 30, 2026 | July 29, 2026; [Microsoft release](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast), Fiscal Year 2026 Results |
| Oracle, peer | $152.94 | $5.83 | May 31, 2026 | June 10, 2026; [Oracle release](https://investor.oracle.com/investor-news/news-details/2026/Oracle-Announces-Record-Q4-and-FY-2026-Results-Driven-by-Cloud-Infrastructure--Cloud-Applications/), Financial Results for FY2026; confirmed in [10-K](https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm), income statement |
| Alphabet Class A, qualified peer | $332.60 | $10.82 | December 31, 2025 | February 4, 2026; [Alphabet release](https://abc.xyz/investor/news/news-details/2026/Alphabet-Announces-Fourth-Quarter-2025-and-Fiscal-Year-Results-2026-KEvZIMKBLS/default.aspx); [10-K](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm), Note 12 Class A diluted net income per share |

Historical closes: [MSFT](https://stockanalysis.com/stocks/msft/history/), [ORCL](https://stockanalysis.com/stocks/orcl/history/), and [GOOGL](https://stockanalysis.com/stocks/googl/history/), September 10, 2026 rows. Stock Analysis is a market-data vendor, not a company filing. GOOGL's **Class A $10.82** EPS is paired with the Class A price; the filing's consolidated diluted EPS is $10.81.

```text
ORCL P/E = $152.94 / $5.83 = 26.233276×
GOOGL Class A P/E = $332.60 / $10.82 = 30.739372×
Peer median P/E = (26.233276× + 30.739372×) / 2 = 28.486324×

MSFT at ORCL P/E = 26.233276× × $17.95 = $470.89/share
MSFT at GOOGL P/E = 30.739372× × $17.95 = $551.77/share
MSFT at peer median = 28.486324× × $17.95 = $511.33/share
MSFT observed P/E = $492.44 / $17.95 = 27.433983×
```

The peer-implied range is **$470.89–$551.77/share** and the two-peer median estimate is **$511.33/share**. The September 10 market close of $492.44 lies inside the range and is 3.69% below its midpoint. The range comes from only two qualified peers and is not a statistical confidence interval.

## Validation and changed-peer test

The Oracle arithmetic checks independently: **$152.94 ÷ $5.83 = 26.233276×**, and **26.233276× × $17.95 = $470.8873**, or $470.89/share.

Before removal, the prediction was that removing Oracle, the lower-multiple peer, would raise the remaining reference to Alphabet's estimate; removing Alphabet would lower it to Oracle's estimate. The calculator confirms:

- Remove Oracle: one-peer Alphabet reference **$551.77**, a **+$40.44** change from the full-set median.
- Remove Alphabet: one-peer Oracle reference **$470.89**, a **−$40.44** change.

Each removal eliminates the range and leaves only a single reference. The direction follows mechanically from which P/E remains; it is not a reason to reject either company.

## Triangulation with the Week 3 DCF

| Method | Microsoft's result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | Base **$114.68/share**; sensitivity **$91.19–$156.02**, September 10, 2026 | Lease-adjusted FY2026 starting FCFF, five-year recovery path, WACC, terminal growth, and cash/debt bridge; highly sensitive to whether current infrastructure investment is temporary growth investment or recurring capital need. |
| Peer P/E | **$470.89–$551.77/share**; median **$511.33**, September 10, 2026 | Only two imperfect peers; different fiscal periods, business mixes, leverage/reinvestment, and investment gains; values reported equity earnings rather than FCFF. |

The methods should not be averaged. The P/E result says Microsoft's observed price is broadly consistent with how two cloud/software comparables price reported earnings. The DCF instead capitalizes a lease-adjusted cash-flow baseline after unusually heavy infrastructure investment. Their large gap is evidence that the treatment and expected payoff of current AI/cloud investment—not arithmetic—is the decisive issue.

## Skeptical AI review and judgment

**Criticism received:** The weakest supported assumption is that current lease-adjusted FCFF is a representative starting point for a five-year DCF while peer P/Es capitalize reported earnings that do not deduct capital expenditure. There is also an earnings-quality mismatch: Microsoft FY2026 GAAP EPS includes a $0.67 benefit from OpenAI investment gains, Alphabet's FY2025 other income includes $24.080 billion of equity-security gains, and Oracle has a materially different reinvestment and financing profile. The question that could change the decision is: **What sourced evidence shows that Microsoft's present infrastructure and finance-lease additions will generate incremental operating cash flow rather than recur at roughly the same intensity?**

**Judgment: accept.** Microsoft's release discloses the $0.67 OpenAI EPS benefit; Alphabet's 10-K discloses the equity-security gains; Oracle's 10-K discloses negative FY2026 free cash flow under its stated measure; and the saved Microsoft DCF explicitly subtracts finance-lease asset additions. The criticism is supported and explains why the P/E range is a market-pricing check, not a resolution of the DCF's reinvestment question. It does not identify a company/date/share-basis error in the calculations.

## Conditional conclusion

**Watch / defer.** The defensible P/E evidence is **$470.89–$551.77/share**, which contains the $492.44 market price, but the saved DCF range of **$91.19–$156.02** is irreconcilably lower under its current cash-flow and lease treatment. The P/E evidence weakens a simple claim that Microsoft is obviously overvalued relative to cloud/software peers, while the DCF prevents an initiation based only on relative multiples.

I would initiate only after a sourced update demonstrates that incremental Azure/AI capacity is converting to operating cash flow quickly enough to support normalized FCFF materially above the FY2026 lease-adjusted baseline, and a rerun produces acceptable value with a margin of safety. Evidence that infrastructure and finance-lease additions remain persistently high without proportional cash-flow growth would reinforce the defer decision. This directly answers the skeptical question: no current source in the analysis yet demonstrates the necessary cash conversion, so that point remains unresolved rather than assumed.

Run from the course workspace:

```bash
python3 comps.py
```

**Integrity note:** This file does not claim partner discussion, a second independent AI response, a quiz attempt, a GitHub upload, or Brightspace submission. Those course steps must be completed and represented by the student.
