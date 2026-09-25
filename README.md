# SAB Guide — Adult *Staphylococcus aureus* Bacteremia

A calm, one-question-at-a-time iPhone web app that walks a physician through the **2026 IDSA/ESCMID Consensus Statements on *S. aureus* bacteremia** for **adults only**: risk stratification, diagnostic workup, final classification, and treatment duration with a day counter.

Designed for iPhone 13 Pro Max and newer (428 × 926 points), works on any modern phone, installs to the Home Screen, and opens offline. Opened on a computer (any window size), it shows inside an iPhone frame scaled to fit, so you see what the phone shows.

## Files

| File | What it does |
|---|---|
| `index.html` | The whole app — screens, styling, and clinical logic |
| `manifest.json` | Lets the app install to the iPhone Home Screen with its name and icon |
| `sw.js` | Saves a copy on the phone so the app opens without internet |
| `icon-192.png`, `icon-512.png` | App icons (Android / general) |
| `apple-touch-icon.png` | iPhone Home Screen icon |
| `README.md` | This page |
| `LICENSE` | Code license + note on guideline copyright |
| `validation_400/` | 400-patient accuracy test suite and report |

## How to use it on an iPhone

1. Put the repository on GitHub Pages (Settings → Pages → Deploy from branch `main`).
2. Open the link in Safari → Share → **Add to Home Screen**.

## The clinical flow

1. **Patient** — adult (18+) with ≥1 blood culture growing *S. aureus*. Children are out of scope.
2. **Initial evaluation** — history & exam, follow-up blood cultures, TTE, remove central line, ID consult.
3. **Key risk factors** — community-onset, positive culture ≥48 h after the first, intracardiac device.
4. **Other risk factors** — valve condition, injection drug use, endovascular graft, SAB in prior 90 days, signs of a deep focus, embolic events, >1 non-contiguous focus, unknown focus.
5. **Risk & workup** — low vs increased risk; TEE guidance; symptom-directed imaging; whole-body imaging when the focus is unknown.
6. **Workup results** — increased-risk patients only: focus found? symptoms resolved? workup complete? (Low-risk patients and TTE-proven endocarditis skip this screen.)
7. **Plan** — with vs without deep-seated focus; 14 days vs 4+ weeks; Day 1 = first negative culture (or source control if later). The bottom button copies a summary for the chart.

Every step is sized to fit one iPhone 13 Pro Max screen with little or no scrolling.

## Validation

`validation_400/` holds a 400-synthetic-patient test suite that taps through the real app and checks every answer against an independent answer key built from the guideline. Latest result: **400/400 correct** (see `validation_400/VALIDATION_REPORT.md`). Re-run after any change.

## Style tokens

```css
/* Color — light */
--c-bg:#F4F7F6;  --c-surface:#FFFFFF;  --c-surface-2:#EEF3F1;  --c-line:#DCE4E1;
--c-ink:#1C2A2E;        /* 13.7:1 */
--c-ink-2:#4F5F64;      /* 6.2:1  */
--c-primary:#0B6B66;    /* 6.3:1 on white */
--c-primary-ink:#FFFFFF; --c-primary-soft:#E2F1EE;
--c-low:#0E6B45;   --c-low-bg:#E3F4EB;    /* 5.7:1 */
--c-inc:#874A00;   --c-inc-bg:#FCF0DC;    /* 6.2:1 */
--c-focus:#A1352A; --c-focus-bg:#FBE8E5;  /* 5.8:1 */

/* Color — dark */
--c-bg:#111719; --c-surface:#1B2326; --c-surface-2:#232D30; --c-line:#2E3A3D;
--c-ink:#E8EEEC; --c-ink-2:#A9B6B9; --c-primary:#5FD1C4; --c-primary-ink:#0B1F1D;
--c-primary-soft:#173331; --c-low:#7FE0B0; --c-low-bg:#15291F;
--c-inc:#F5C27A; --c-inc-bg:#2E2310; --c-focus:#F4A195; --c-focus-bg:#33191A;

/* Icon tiles — white glyph on color (iOS Settings style) */
--i-teal:#0B6B66; --i-blue:#2A64A8; --i-green:#2C7A4B; --i-amber:#A45F00;
--i-coral:#B8402F; --i-rose:#A8385A; --i-slate:#52636A; --i-indigo:#4C5AA6;

/* Type (San Francisco system font) */
--t-large-title:700 34px/41px; --t-title:700 22px/28px; --t-headline:600 17px/22px;
--t-body:400 17px/24px; --t-callout:400 16px/22px; --t-footnote:400 13px/18px;
--t-caption:600 12px/16px (uppercase, +0.06em);

/* Shape & space */
--r-sm:10px; --r-md:14px; --r-lg:20px; --r-pill:999px;
--s-1:4px … --s-8:32px (4-pt grid); --gutter:20px; --touch:44px;

/* Motion */
--ease:cubic-bezier(.2,.8,.2,1); --ease-spring:cubic-bezier(.34,1.4,.64,1);
--d-fast:140ms; --d-med:260ms; --d-slow:420ms;  /* all 0ms with Reduce Motion */
```

All text/background pairs meet WCAG AA (4.5:1 or better) in both light and dark mode.

## Source

Liu C, Chambers HF, Kern WV, Vandenesch F, et al. *2026 Consensus Statements by the Infectious Diseases Society of America (IDSA) and European Society of Clinical Microbiology and Infectious Diseases (ESCMID) on Staphylococcus aureus Bacteremia: Risk Stratification, Diagnostic Evaluation, and Management of Adults and Children.* Consensus Statements 1–7.

**Not covered:** antibiotic choice (MRSA vs MSSA — future IDSA/ESCMID publications), focus-specific durations, children.

## Intended use & privacy

- **Clinical educational tool for clinicians** (physicians, advanced practice providers, pharmacists). Not a substitute for clinical judgment or ID consultation.
- **No protected health information (PHI):** the app asks for no patient identifiers, saves nothing, and sends nothing over the internet (no accounts, tracking or analytics). Designed for HIPAA-conscious use. Users should not enter identifiers.

## Disclaimer

Educational aid only. Does not replace clinical judgment or infectious diseases consultation. The guideline content is the copyrighted property of IDSA; IDSA requires written permission to incorporate its guidelines into software products.
