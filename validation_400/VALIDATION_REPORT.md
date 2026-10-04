# SAB Guide — 400-Patient Validation Report

**App version:** 2.5 · **Run date:** October 4, 2026 (first run on v1.9, September 25 — also 400/400) · **Result: 400 / 400 patients fully correct (100%)**

## What was tested

400 synthetic (fake) adult patients with *S. aureus* bacteremia were run through the **real app screens** at iPhone 13 Pro Max size by an automated tester that tapped every answer, exactly as a clinician would. What the app displayed was compared against an **independent answer key** written separately from the 2026 IDSA/ESCMID consensus statements (Figure 1, Statements 1–7). The answer key shares no code with the app.

## Results

| What was checked | Correct |
|---|---|
| Completed the flow without getting stuck | 400 / 400 |
| Risk: low / low (provisional) / increased (Statement 1) | 400 / 400 |
| Echo advice: TTE, TEE suggested / consider / may be unnecessary (Statements 3–4) | 400 / 400 |
| Whole-body imaging advice for unknown focus (Statement 5) | 400 / 400 |
| Workup-results screen shown only when needed | 400 / 400 |
| Final classification: with / without deep-seated focus / pending (Figure 1) | 400 / 400 |
| Duration: 14 days / 4+ weeks / not ready / none (Statements 6–7) | 400 / 400 |
| Longer-course warning flags | 400 / 400 |
| Day 1 date (clearance, or source control if later) | 400 / 400 |
| Last-day date | 400 / 400 |
| **Every field correct for the patient** | **400 / 400** |

No screen errors occurred in any run.

## What the 400 patients covered

- **Risk:** 45 low, 25 low-provisional (results pending), 330 increased.
- **Echo advice:** 153 TEE suggested, 71 consider TEE, 97 TEE may be unnecessary, 15 limited TTE / use judgment, 34 TTE still needed, 30 endocarditis on TTE.
- **Outcomes:** 213 without a deep focus, 78 with a deep focus, 109 still pending.
- **Durations:** 165 × 14 days, 78 × 4+ weeks, 48 "not ready" (symptoms not resolved), 109 no duration yet.
- **Longer-course flags:** 92 patients (prolonged bacteremia, incomplete workup, retained device, new graft, DVT at line site).
- **Dates:** 243 day-counter calculations: source control none (169), after clearance (133), before (67) and same day (31). Dates included month ends, year ends and leap-year February (2028).
- Every risk factor was tested alone (10–20 patients each) and in random combinations (100 patients).

## One finding, and it was in the answer key, not the app

The first comparison showed 7 mismatches (98.2%). All 7 were patients with an **unknown focus** whose later workup **found** the source. The app correctly advised whole-body imaging on the "Risk & workup" screen, which comes *before* the workup. The first version of the answer key wrongly used the later result to say the advice shouldn't appear. Statement 5 recommends this imaging precisely to find an unknown focus, so the answer key was corrected. After the correction, all 400 patients matched. The app was not changed.

## Proof the test catches real mistakes

Three errors were deliberately planted in throwaway copies of the app. The test caught every one:

| Planted error | Patients flagged |
|---|---|
| Community-onset no longer prompts "consider TEE" | 52 |
| Course counted as 13 days instead of 14 | 243 |
| Source-control date ignored when setting Day 1 | 86 |

## Limitations

- The patients are synthetic. This checks that the app follows the guideline, not how patients actually do.
- The answer key and the app were written by the same assistant from the same reading of the guideline. The code is separate, so programming mistakes are caught, but a shared misreading of the guideline would not be. A clinician or ID pharmacist review of the logic is still recommended.
- "Limited-quality TTE with no endocarditis features" isn't directly addressed by the guideline. Both the app and the answer key show "use judgment / discuss with ID" for this, which is a design choice.
- The test ran in Chrome's engine at iPhone size, not on a physical iPhone in Safari.

## How to re-run (after any change to the app)

```
python3 generate_cases.py        # makes cases.json (same 400 patients every time)
python3 reference_oracle.py      # makes expected.json (the answer key)
node run_app_validation.js       # taps through the app, makes app_results.json
python3 compare_results.py       # prints the scorecard, makes comparison.csv
```

`comparison.csv` lists every patient with the expected and displayed answer for every field.
