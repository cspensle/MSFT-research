# Project 1 - Validation and AI-Use Record

> The locked changed-input prediction and test are complete. The student
> confirmed the complete AI disclosure and that the interpretation reflects
> the student's own judgment.

## Model identity

- Company: Microsoft Corporation (MSFT)
- Decision: initiate, watch/defer, or do not initiate
- Base recommendation: watch/defer; do not initiate at saved market observations
- Company-information cutoff: July 29, 2026
- Market observations: separately dated September 10 and September 28, 2026
- Units: USD millions except per-share values; rates are nominal annual decimals
- Timing: annual year-end discounting; terminal value at FY2031 year-end

## Automated validation completed

| Test | Result | Evidence |
|---|---|---|
| Balance-sheet articulation | PASS | Maximum annual assets less liabilities and equity gap: $0.0000m |
| Cash-flow tie to cash | PASS | Maximum calculated-versus-balance-sheet cash gap: $0.0000m |
| Minimum cash | PASS | Lowest base forecast cash: $32,215.2m versus $10,000.0m floor |
| Terminal convention | PASS | 3.00% terminal growth is below 10.202614% WACC |
| WACC direction | PASS | A 1 pp higher WACC reduces value; a 1 pp lower WACC increases value |
| Terminal-growth direction | PASS | Higher terminal growth increases value within valid bounds |
| Failure demonstration | PASS | Forcing terminal growth equal to WACC visibly fails and blocks valuation |
| Restored-base check | PASS | Existing sensitivity program reproduces the opening base exactly |
| Synthetic known answer | PASS | Training DCF reproduces $30.00/share reverse-DCF target and published outputs |
| Peer-policy and multiple consistency | PASS | P/E uses price and GAAP diluted EPS on a consistent share basis; EV/revenue uses market capitalization plus borrowing, finance leases, and preferred stock less non-operating cash for both Microsoft and Oracle |

Automated command:

```bash
python3 -m unittest -v test_workbench.py
python3 comps.py
```

## Base executed output

- Pro-forma FCFF value/share: $238.17
- Pro-forma FCFE cross-check: $279.60
- Enterprise value: $1,808,949.7m
- Equity value: $1,775,104.7m
- Terminal share of enterprise value: 80.3%
- Forecast FCFF FY2027-FY2031: $39,209.9m, $66,598.9m, $99,465.2m,
  $132,918.0m, and $165,095.5m
- Causal case range: $187.75-$290.97/share

## Locked Changed-Input Record

- Student-selected input and units: Annual cash capital spending (USD millions per forecast year)
- Old value: FY2030E $155,000m FY2031E $160,000m
- New value: FY2030E $125,000m, and FY2031E $120,000m
- Human-authored expected output direction: The FCFF intrinsic value per share will increase in value
- Human-authored finance explanation preserved from the locked pre-run commit: I am reducing the spending in those years because I believe MSFT will not be spending that much on AI focused developement as that will begin to slow due to government internvention and the ability of AI slowing.
- Expected decision effect: This would increase the intrinsic value per share, and I would move closer to an initiation.
- Timestamp before execution: 2026-10-19 13:06:53 EDT
- Pre-run repository commit: 46a44aacfd0149f5687b06c9572a40a3ebb0402c
- Post-run clarification written by the student: I believe Microsoft's AI
  spending will peak before 2030. After the heavy AI-infrastructure investment
  cycle, capital spending is likely to normalize as Microsoft generates returns
  from the installed capacity. If utilization of its existing AI data-center
  capacity improves, Microsoft could reduce capital spending while maintaining
  or increasing revenue growth.


Post-run fields:

- Exact command/action: Held every other base assumption constant and changed
  only `cash_capex` to $125,000m for FY2030 and $120,000m for FY2031 through
  `scenario_assumptions(cash_capex_overrides={2030: 125000.0, 2031: 120000.0})`.
- Preserved before output: FCFF intrinsic value was $238.17/share; FY2030 and
  FY2031 FCFF were $132,918.0m and $165,095.5m, respectively.
- Preserved after output: FCFF intrinsic value was $285.08/share; FY2030 and
  FY2031 FCFF were $162,918.0m and $200,076.5m, respectively. Enterprise value
  was $2,158,576.7m, equity value was $2,124,731.7m, and all validation checks
  passed.
- Actual direction and decision effect: Intrinsic value increased by
  $46.91/share, or 19.70%, as predicted. The result moved closer to initiation,
  but remained $224.14/share below the saved $509.22 market reference, so the
  conditional decision remained watch/defer.
- Reconciliation or failure diagnosis: The direction matched the prediction.
  Lower cash capital spending raised FY2030 FCFF dollar-for-dollar by $30,000m.
  FY2031 FCFF rose by $34,981.0m rather than exactly $40,000m because lower
  FY2030 capex also reduced FY2031 opening PP&E and therefore FY2031
  depreciation and its tax shield. No validation failure occurred.
- Post-run timestamp: 2026-10-19 13:28:32 EDT

## Highest-risk failure test

The interface includes a validation-demo checkbox that forces terminal growth
equal to WACC. The terminal-convention check turns red and the valuation is
blocked rather than producing a nonsensical or infinite Gordon-growth result.
The control can then be cleared to restore the validated base.

## Independent input/source check

FY2026 revenue, operating income, operating cash flow, cash PP&E additions,
finance-lease additions, borrowing, finance-lease liabilities, cash and
short-term investments, and diluted shares were reconciled to the saved FY2026
filing and the locators recorded in `Lab_06_MSFT.md`, `Lab_10_MSFT.md`, and
`sources.md`. The $3.8 billion restricted short-term-investment exclusion is
identified separately in the equity bridge. The qualified EV/revenue
cross-check independently reconciles Microsoft and Oracle shares, annual
revenue, borrowing, finance leases, preferred stock, and non-operating cash to
their FY2026 SEC filings and September 10, 2026 prices.

## AI output checked

AI assisted with the integrated FCFF workbench architecture and proposed using
pro-forma operating income, depreciation, stock compensation, capital spending,
finance-lease additions, and operating working capital to calculate forecast
FCFF. The output was **qualified** rather than accepted without modification:
finance-lease additions are treated as investment and the liability as debt;
the constant diluted-share treatment and stock-compensation add-back are
explicit limitations. This is the specific checked AI output discussed in
Video 1.

## Named AI tools and uses

- OpenAI Codex: code scaffolding, debugging, tests, documentation drafting, and
  packaging assistance; correction of automatically generated video transcripts.
- macOS Speech Recognition: generated draft text from the student's three
  recorded videos. Codex corrected finance terms and numbers against the video
  screens and project record. The student must review the final transcripts
  against the recordings before submission.
- No other generative-AI, AI-search, or coding tools were used for Project 1.

AI did not perform the Microsoft Edition A file, the required locked human
prediction, the student's final investment judgment, or the student's recorded
defense. The Microsoft Edition A remains unchanged.

## Cold-run record

- Clean environment or fresh virtual environment: Fresh temporary Python
  3.14.7 virtual environment created outside the repository.
- Installation command and result: `uv pip install --offline --python
  <temporary-venv>/bin/python -r requirements.txt`; 33 packages installed,
  including Streamlit 1.66.0.
- App launch command and result: `streamlit run app.py --server.headless true
  --server.port 8765`; server started and `/_stcore/health` returned `ok`.
- Base output reproduced: $238.17/share FCFF, $279.60/share FCFE cross-check,
  $1,808,949.7m enterprise value, and all five base validation checks passed.
- Test suite result: `python -m unittest -v test_workbench.py`; five of five
  tests passed.
- Failure demonstration and recovery: Streamlit AppTest confirmed the
  terminal-growth-equals-WACC control blocks valuation; clearing it and using
  Reset restored the base FY2030/FY2031 capex inputs and valid output.
- Timestamp and tested code commit: 2026-10-19 13:31:47 EDT;
  `b5a883a50f851b4457f2af954427459551f16cd7`.

## Known limitations

- Constant FY2026 weighted-average diluted shares do not forecast dilution.
- Stock compensation is added back as noncash while share issuance is simplified.
- Maintenance and growth capex are not disclosed separately.
- Residual balance-sheet buckets are held flat.
- WACC and the displayed market reference use different September dates.
- Terminal value is 80.3% of enterprise value.
- Low/base/high cases are scenarios, not probability-weighted outcomes.

## Post-recording interface correction

Review of the first Video 3 recording exposed an interface inconsistency: the
app passed the FCFF WACC (10.202614%) as the discount rate for its FCFE
cross-check, displaying $287.14/share while the standalone pro-forma and
written artifacts used the 10.38% cost of equity and reported $279.60/share.
The app now uses the pro-forma's separate cost of equity for FCFE while the
WACC control remains specific to FCFF. This does not change the $238.17/share
FCFF base, $285.08/share locked cash-capex result, or watch/defer decision.
The corrected app displayed $279.60/share in a fresh Streamlit AppTest run
without exceptions, and all five workbench unit tests passed after the change.
