# Project 1 Video Guide

Use this as a recording checklist, not a script to read. Speak naturally and
make sure the relevant file, code, output, or app screen is readable while you
discuss it. The checklist is designed to cover the project evidence described
in the submission instructions; it cannot guarantee a particular grade. Follow
any more specific rubric or recording directions posted in Brightspace.

## Before recording

- Use the final, consistent project files and code from the repository.
- Close unrelated windows and enlarge the text or app so it is legible.
- Keep each video within its time limit. Do not spend recording time installing
  packages; prepare the environment beforehand.
- Do not claim that you personally performed work that you did not perform.
- Upload each video as Unlisted or Public, then watch it once and confirm the
  link works. Prepare a corrected plain-text transcript for each video.

## Video 1 - Research evolution and AI-output check (maximum 3:00)

**Goal:** Show how the analysis developed from Edition A to Edition B, what
evidence informed the judgment, and how you checked one consequential
AI-assisted output.

### 0:00-0:25 - Edition A and initial decision

**Show:** `Research-Evolution.pdf`, Edition A pages 1-2. Keep the decision and
the initial thesis visible.

**Describe:** Your original Microsoft recommendation and the central question:
whether AI/cloud growth can turn into durable free cash flow after the required
infrastructure spending.

### 0:25-1:15 - Evolution into Edition B

**Show:** Edition B pages 3-4, especially the change table and valuation
summary.

**Describe:** What new work or evidence was added: the linked five-year
pro-forma, FCFF DCF, FCFE cross-check, starting-cash-flow DCF, and peer
comparison. State the integrated FCFF estimate ($238.17/share), its causal
range ($187.75-$290.97), and the saved market reference ($509.22 on September
28, 2026). Explain that the market and WACC observations have different dates
and why that limits the comparison. Say whether the conclusion changed and
why.

### 1:15-2:20 - Check one AI-assisted output

**Show:** `workbench.py` at the relevant FCFF/lease treatment and the matching
section of `Validation-and-AI-Use.pdf`.

**Describe:** AI proposed the integrated FCFF layer. Explain how you checked
finance-lease additions against the filing and earlier DCF treatment: lease
additions are capital investment in FCFF, while the lease liability is included
as debt in the equity bridge. State the limitation you identified: stock
compensation is added back while the share count is held constant, so future
dilution is simplified. Briefly state that you checked valuation direction
(higher WACC lowers value; higher terminal growth raises value) and that the
model rejects terminal growth equal to WACC.

### 2:20-2:55 - Final judgment

**Show:** Edition B's conclusion or the Decision Memo recommendation.

**Describe:** In your own words, why the expanded evidence confirmed or changed
your watch/defer judgment. Do not just repeat valuation outputs; connect the
cash-conversion evidence, reinvestment needs, and valuation gap to the decision.

## Video 2 - Codebase walkthrough (maximum 5:00)

**Goal:** Demonstrate that the submitted project is reproducible and explain
how the financial model, valuation, and automated checks fit together. This is
a repository/code/test walkthrough. Save the interactive live app failure
demonstration for Video 3.

### 0:00-0:35 - Repository and reproducibility

**Show:** The repository root, `README.md`, and the file tree. Point out
`requirements.txt`, `app.py`, `proforma.py`, `workbench.py`, `comps.py`, and
`test_workbench.py`.

**Describe:** The project can be installed and run using the README. If you
choose to demonstrate commands, run these from the repository root (ideally
before recording once to confirm they work):

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest -v test_workbench.py
```

The first command is only needed for setup; during recording, it is fine to
show the already completed setup and run the test command. Show the passing
test summary. Explain that the app itself is launched with `streamlit run
app.py`; do not use this video for the interactive input demonstration.

### 0:35-1:45 - Trace the model and data flow

**Show:** `proforma.py` assumptions and forecast, then the corresponding
functions in `workbench.py`, then the app entry point in `app.py`.

```text
proforma.py assumptions
    -> five linked forecast years
    -> workbench.py forecast_fcff()
    -> value_forecast_fcff()
    -> enterprise-to-equity bridge
    -> app.py interface
```

**Describe:** How NOPAT, depreciation, stock compensation, cash capex, finance
lease additions, and operating working capital affect FCFF. Explain the lease
consistency: lease additions are treated as investment in FCFF and the lease
liability is included in debt in the bridge, without deducting principal a
second time. Identify `comps.py` as the P/E analysis plus the qualified Oracle
EV/revenue cross-check ($360.90/share reference), and state that the cross-check
does not control for differences in growth, profitability, or business mix.

### 1:45-2:40 - Accounting and valuation checks

**Show:** `validation_checks()` in `workbench.py`, then the corresponding tests
in `test_workbench.py`; show the passing test summary in the terminal if time
allows.

**Describe:** The checks cover balance-sheet articulation, cash-flow-to-cash
tie, minimum cash, terminal growth below WACC, positive diluted shares, and
valuation direction when WACC or terminal growth changes. Explain that tests
provide evidence the programmed behavior works for these cases; they do not
prove the forecast assumptions are correct.

### 2:40-3:35 - Invalid terminal-growth case in code

**Show:** `test_failure_demo_blocks_gordon_growth` in `test_workbench.py`, the
terminal-convention check in `workbench.py`, and the passing test result.

**Describe:** Gordon growth requires WACC to exceed terminal growth. When the
two rates are equal, the denominator `WACC - terminal_growth` is zero, so the
valuation must be rejected. The automated test confirms the check fails and
the valuation function raises an error. Do not switch to the live app here;
Video 3 shows the user-facing failure and recovery.

### 3:35-4:30 - Locked changed-input test

**Show:** The locked prediction and results in `Validation-and-AI-Use.pdf` or
the validation Markdown record. Make the timestamp, pre-run commit, exact
inputs, and before/after outputs readable.

**Describe:** FY2030 cash capital spending changed from $155.0B to $125.0B and
FY2031 from $160.0B to $120.0B. FCFF value moved from $238.17 to $285.08 per
share (+$46.91, or 19.70%), as predicted; watch/defer stayed the decision.
Explain the causal direction: lower modeled cash investment increases cash
available to investors, holding other assumptions constant. Distinguish this
controlled scenario from a forecast that AI spending will actually decline.

### 4:30-4:55 - Limitation

**Show:** The model limitation in the validation record or README.

**Describe:** The constant diluted-share treatment and stock-compensation
add-back simplify future dilution. End by stating that model checks validate
implementation behavior, while source quality and assumptions still require
analyst judgment.

## Video 3 - Live product demonstration and committee defense (maximum 5:00)

**Goal:** Operate the delivered workbench live, show that an invalid valuation
input is visibly blocked and recoverable, then defend the investment judgment.

### 0:00-1:05 - Required live product opening

**Show:** Start with the Streamlit workbench already open. Keep the current
inputs, validation panel, and per-share output visible as you work.

1. Read the base FCFF value ($238.17/share) and watch/defer decision.
2. Change FY2030/FY2031 cash capital spending to $125.0B/$120.0B. Show the
   updated value ($285.08/share) and explain that lowering forecast investment
   raises FCFF, all else equal.
3. Briefly trace the effect from cash capex through FCFF to enterprise/equity
   value.
4. Press **Reset base case** and show the base case returns.
5. Turn on the control that forces terminal growth equal to WACC. Show the
   failed check and that valuation is blocked.
6. Turn the control off or reset, then show the valid valuation recovers.

**Describe the failure clearly:** Gordon growth divides terminal cash flow by
`WACC - terminal_growth`. If the rates are equal, the denominator is zero, so
the app must not present that result as a valid valuation. This live
failure-and-recovery sequence belongs in Video 3; Video 2 covers the code and
automated test for the same rule.

### 1:05-1:35 - Recommendation first

**Show:** The Decision Memo recommendation or the valuation summary in the
workbench.

**Describe:** Recommend watch/defer and say you would not initiate at the saved
market observation. Compare the integrated FCFF range ($187.75-$290.97/share)
with $509.22 on September 28, 2026, and identify the differing WACC/market dates
as a limitation.

### 1:35-2:40 - Explain why valuation methods differ

**Show:** The method comparison in Edition B or the Decision Memo.

**Describe:** P/E reflects reported earnings before infrastructure cash
investment; Oracle EV/revenue includes capital structure but does not adjust
for profitability, growth, or business mix; the starting-FCFF DCF applies the
current investment burden immediately; the integrated model forecasts future
cash conversion. Explain why these measures answer different questions and
should not be mechanically averaged.

### 2:40-3:35 - Thesis and supporting evidence

**Show:** Edition B's Microsoft operating evidence and the relevant forecast or
source table.

**Describe:** Summarize Microsoft's operating strengths, FY2026 operating cash
flow, cash PP&E spending, and finance-lease additions. Explain why the return
on incremental AI/data-center capital is the decisive unresolved question.

### 3:35-4:25 - Risks and reversal evidence

**Show:** Edition B's risks, assumptions, or reversal triggers.

**Describe:** Address terminal-value dependence, maintenance versus growth
capex, dilution, and market/WACC date mismatch. Name concrete future evidence
that would change the recommendation, such as sustained cash conversion
relative to cash and lease-funded investment and a refreshed valuation with a
margin of safety.

### 4:25-4:55 - Committee ask

**Show:** The Decision Memo conclusion.

**Describe:** Ask the committee to keep Microsoft on watch, monitor quarterly
cash conversion relative to cash and lease-funded investment, and require a
complete valuation refresh before initiating. End before 5:00.

## Transcript and final quality check

- Correct company/ticker, terminology, dates, values, units, and percentages.
- Ensure the recommendation, valuation figures, and limitations match Edition
  B, the memo, validation record, and app output.
- Do not overstate a scenario as a prediction: the capex change is a controlled
  assumption test, not evidence that Microsoft's spending will fall.
- Ensure Video 1 shows Edition A then Edition B and one checked AI output;
  Video 2 shows the repository, code flow, tests, and locked test; Video 3 shows
  the live app failure and recovery plus the committee defense.
- Save each corrected transcript as plain text named exactly
  `transcript-video-1.txt`, `transcript-video-2.txt`, and
  `transcript-video-3.txt`. Confirm each transcript matches its final uploaded
  video and record each stable video URL and duration in the manifest.
