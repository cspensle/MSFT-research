# Microsoft Project 1 - Corporate Finance Application

## Decision and intended user

This repository supports a buy-side Investment Committee deciding whether to
initiate, watch/defer, or not initiate Microsoft Corporation (Nasdaq: MSFT).
The current conditional recommendation is **watch/defer**. The analysis does
not establish a sufficient valuation margin at the saved market observations,
and the decisive unresolved issue is whether AI and data-center investment will
convert into durable free cash flow.

All monetary model inputs are USD millions except per-share values. Historical
company facts use Microsoft's FY2026 filing and July 29, 2026 earnings
materials. Market observations are dated in the relevant analysis; the
workbench displays the September 28, 2026 regular-session close of $509.22 as a
historical reference, not a live price.

## Product

`app.py` is a semi-adjustable Streamlit workbench. It exposes bounded shifts to
revenue growth and gross margin, year-specific FY2030/FY2031 cash capital
spending controls, WACC, and terminal growth.
It displays the linked five-year forecast, lease-adjusted FCFF valuation,
enterprise-to-equity bridge, FCFE cross-check, causal cases, WACC-growth
sensitivity, and validation checks. A dedicated demonstration control forces
terminal growth equal to WACC so the Gordon-growth check fails loudly and the
valuation is blocked.

The accounting engine remains in `proforma.py`. `workbench.py` consumes that
engine and adds the Project 1 FCFF product layer. The original `dcf.py` and
`comps.py` preserve the earlier DCF/reverse-DCF and peer-analysis exercises.

## Setup and run

Python 3.11 or newer is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
streamlit run app.py
```

The browser should open automatically. If it does not, use the local URL shown
in the terminal.

Run the noninteractive workbench and tests with:

```bash
python3 workbench.py
python3 -m unittest -v test_workbench.py
python3 dcf.py --training
python3 dcf.py
python3 comps.py
python3 proforma.py
python3 proforma.py --sensitivity
```

## Repository map

| Path | Purpose |
|---|---|
| `app.py` | Adjustable analyst interface and visible validation panel |
| `workbench.py` | Pro-forma-driven FCFF, bridge, cases, grid, and checks |
| `proforma.py` | Five-year linked income statement, balance sheet, cash flow, and FCFE cross-check |
| `dcf.py` | Starting-FCFF DCF, WACC grid, reverse DCF, and training case |
| `comps.py` | Comparable-company P/E analysis and qualified EV/revenue cross-check |
| `test_workbench.py` | Regression, boundary, and valuation-direction tests |
| `ColinSpensley/MSFT/` | Research, filing, sources, lab records, and working submission documents |

## Base outputs

The integrated base case produces:

- Pro-forma-driven FCFF value: **$238.17 per diluted share**
- FCFE cross-check: **$279.60 per diluted share**
- Causal downside/base/upside range: **$187.75-$290.97 per share**
- Qualified Oracle EV/revenue cross-check: **$360.90 per share**
- Enterprise value: **$1.809 trillion**
- Equity value: **$1.775 trillion**
- Terminal share of enterprise value: **80.3%**

These values are analyst estimates rather than company guidance. They should
not be mechanically averaged with the $114.68 starting-FCFF DCF or the
$470.89-$551.77 peer P/E range because the methods use different cash-flow,
reinvestment, and accounting conventions.

## Data sources

Primary source records and locators are in
`ColinSpensley/MSFT/sources.md`, with the FY2026 filing saved as
`ColinSpensley/MSFT/MSFT_FY26Q4_10K.docx`. Market inputs and their dates are
documented in `ColinSpensley/MSFT/Lab_06_MSFT.md`,
`ColinSpensley/MSFT/Lab_08_MSFT.md`, and
`ColinSpensley/MSFT/Lab_10_MSFT.md`.

## Known limitations

- The workbench retains the course model's constant FY2026 weighted-average
  diluted share count and therefore does not forecast dilution.
- Stock compensation is added back as noncash while forward dilution remains
  simplified.
- Maintenance and growth capital expenditure are not separately disclosed.
- Flat residual balance-sheet buckets simplify the five-year forecast.
- WACC inputs are dated September 10 while the displayed market reference is
  September 28; the mismatch is disclosed and should be refreshed for a live
  investment decision.
- Terminal value is a large share of enterprise value, making WACC and terminal
  growth material.
- The interface is locally runnable; hosting is intentionally not required.

## AI-use and academic-integrity boundary

Project-specific AI assistance is disclosed in the working validation and
AI-use record. The Microsoft Edition A remains unchanged, and the locked
changed-input prediction was written and committed before execution. The
student must still confirm the final investment judgment, record the videos,
verify the transcripts, and complete the submission manifest.
