# SAB Guide — Learning Checklist

A running list of what you should be able to explain in your own words. Boxes get checked only after you've shown it (restated it or answered a quiz correctly).

**Status:** Stage 1 in progress · Last updated: Sep 23, 2026

---

## Stage 1 — The problem (the guideline)

### Why this guideline exists
- [ ] Why *S. aureus* bacteremia (SAB) matters: leading cause of bloodstream-infection death worldwide; 15–30% die within 30 days; worse with MRSA
- [x] Why the old "complicated vs uncomplicated" labels failed: definitions vary; risk factors were treated as if they *were* a diagnosis; up to 1 in 3 hidden (occult) foci are missed at first → under- or over-treatment
- [ ] Why these are "consensus statements," not graded recommendations: too little head-to-head evidence; >75% panel agreement required
- [ ] Who wrote it: IDSA + ESCMID jointly (with PIDS, ESPID, SHEA, SIDP, ASHP)

### The new framework (Figure 1) — three layers
- [ ] Layer 1 — Initial evaluation for everyone: history & exam, follow-up blood cultures, TTE, remove central line, ID consult
- [ ] Layer 2 — Risk stratification: **low risk** (zero risk factors) vs **increased risk** (≥1)
- [x] Layer 3 — Classification after workup: **with** vs **without** a deep-seated/metastatic focus → drives duration

### The risk factors
- [ ] The 3 key factors: community-onset, positive culture ≥48 h after the first, intracardiac device
- [ ] The 8 other factors: valve condition, injection drug use, endovascular graft, SAB in prior 90 days, signs of deep focus, embolic events, >1 non-contiguous focus, unknown focus
- [ ] Why ONE factor is enough: no single factor is reliable enough to *rule out* deep infection
- [ ] Why "community-onset" is a risk: the infection had time to seed before anyone drew cultures
- [ ] The list is not exhaustive; risk is dynamic

### The 7 statements
- [ ] S1 Risk stratification (above)
- [ ] S2 Follow-up cultures: ≥2 sets at 48 h, then 1–2 sets every 24–48 h until negative; clearance day = Day 1
- [ ] S3 TTE for all adults (no group proven safe to skip)
- [ ] S4 TEE after negative TTE: *suggested* for device, valve condition, culture+ ≥48 h, emboli, >1 focus; *consider* for community-onset or IDU; *may be unnecessary* with good-quality TTE and none of these
- [ ] S5 Increased risk + unknown focus → whole-body imaging (FDG-PET/CT) OR a combination of targeted imaging
- [ ] S6 Low risk, no focus → 14 days (not shorter, not longer)
- [ ] S7 Increased risk, no focus → 14 days if symptoms resolved and workup negative; consider longer if prolonged bacteremia or incomplete workup

### Edge cases in the guideline
- [ ] Source control after clearance → count from the source-control date
- [ ] Skip phenomenon moves the clearance date
- [ ] Hospital-onset can be mislabeled if cultures were drawn late
- [ ] What the guideline does NOT cover: antibiotic choice (MRSA vs MSSA), focus-specific durations

---

## Stage 2 — The solution (the app)

### Design decisions & why
- [ ] One question per screen (progressive disclosure) → less mental load on a busy shift
- [ ] Adults-only gate on screen 1 and why children are excluded
- [ ] Why the old step 5 was split into "Risk & workup" and "Workup results" (one screen per job, minimal scrolling), and why low-risk patients skip the results screen
- [ ] "Positive culture ≥48 h" is asked once and carried forward (never asked twice)
- [ ] "None of these" must be tapped deliberately — silence ≠ "no"
- [ ] Color meaning: green = low risk / no focus, amber = increased risk, coral = deep focus
- [ ] Calm teal palette, 44-pt touch targets, 4.5:1 contrast, Reduce-Motion respected
- [ ] Colored icon tiles (like iPhone Settings): each icon means one thing everywhere (heart = echo/valve, test tube = cultures, clock = ≥48 h) so the eye finds items without reading
- [ ] Computer preview shows the app inside an iPhone frame; on a real phone it fills the screen
- [ ] Nothing is saved; "Start over" wipes everything (privacy)

### Business logic & edge cases the app handles
- [ ] "Provisional" low risk when cultures or TTE are still pending
- [ ] TTE showing endocarditis jumps straight to "with focus"
- [ ] Limited-quality TTE with no risk features → "use judgment" (the guideline is silent here)
- [ ] Increased risk, no focus, symptoms NOT resolved → app refuses to give 14 days yet
- [ ] Longer-course flags: prolonged bacteremia, incomplete workup, retained device, new graft, DVT at line site
- [ ] Day counter: Day 1 = clearance day (or source-control day if later); 14-day course ends on Day 1 + 13

### The 8 files
- [ ] What each file does (index.html, manifest.json, sw.js, 3 icons, README.md, LICENSE)

---

### How we know it's right
- [ ] What the 400-patient validation does (synthetic patients → real app screens → independent answer key)
- [ ] Why the 7 first-run mismatches were an answer-key error (imaging advice comes before the workup result)
- [ ] Why planting deliberate bugs proves the test works
- [ ] Limits: same reader of the guideline for both sides; not a real-iPhone Safari test

---

## Stage 3 — Broader context & impact
- [ ] Who benefits: hospitalists, ED, ICU, pharmacists — not only ID
- [ ] Impact: fewer missed hidden infections, fewer unnecessarily long courses (antibiotic stewardship)
- [ ] Why the app never replaces ID consult or judgment, and why it's labeled a clinical educational tool for clinicians
- [ ] Why the label says "No patient data stored or sent" rather than "HIPAA compliant" (no official HIPAA certification exists; the app handles no PHI)
- [ ] IDSA copyright: written permission is needed before distributing guideline content inside software
- [ ] The framework still needs validation — what could change in future updates
- [ ] What comes next: MRSA/MSSA antibiotic-choice statements

---

## Session log
- Sep 23: Files built. Starting point: "start me from zero."
- Sep 23: Lesson 1 quiz — correct on "what decides duration" and "why old labels were dropped"; needed help on "why one risk factor is enough."
- Sep 25: 400-patient validation: 400/400 correct after one answer-key fix; 3/3 planted bugs caught.
- Sep 25: v1.9 — labeled as a clinical educational tool for clinicians; privacy card and "No patient data stored or sent" badge.
- Sep 25: v1.8 — first screen titled "Assess" (centered) above "New patient".
- Sep 25: v1.7 — About: "Source" renamed "References" and moved last; "Developed by MDGadgetz LLC" credit; centered titles on Definitions and About.
- Sep 25: v1.6 — every step now fits one iPhone screen (at most a few points of scroll); flow is 7 steps.
- Sep 23: v1.2 — computer preview now always shows a phone frame (with status bar) scaled to fit any window.
- Sep 23: v1.1 — icons on every question/row/definition, iPhone frame preview, bolder question text.
