"""Independent answer key, written directly from the 2026 IDSA/ESCMID SAB
consensus statements (Figure 1, Statements 1-7). Shares no code with the app.
Output: expected.json
"""
import json
from datetime import date, timedelta

cases = json.load(open('cases.json'))

# Statement 4: features that make TEE "suggested" after a negative TTE
TEE_SUGGESTED_FEATURES = {'valve', 'embolic', 'multi'}         # + device, FUBC >=48 h
# Statement 4: community-onset or IDU -> "consider" TEE
TEE_CONSIDER_FEATURES = {'idu'}                                  # + community-onset


def expected(c):
    other = set(c['other'])
    fubc_pos = c['fubc48'] == 'pos'
    endocarditis_on_tte = c['tte'] == 'ie'

    # --- Statement 1: at least one risk factor (or a deep focus already seen) = increased risk
    has_factor = c['community'] or fubc_pos or c['device'] or bool(other) or endocarditis_on_tte
    if has_factor:
        risk = 'increased'
    elif c['fubc48'] == 'pending' or c['tte'] == 'pending':
        risk = 'low-provisional'      # low risk requires FUBC and TTE results (Statement 1 remarks)
    else:
        risk = 'low'

    # --- Statements 3 & 4: echocardiography
    if c['tte'] == 'pending':
        tee = 'obtain-tte'            # TTE for all adults
    elif endocarditis_on_tte:
        tee = 'focus-found'
    elif c['device'] or fubc_pos or (other & TEE_SUGGESTED_FEATURES):
        tee = 'suggested'
    elif c['community'] or (other & TEE_CONSIDER_FEATURES):
        tee = 'consider'
    elif c['tte'] == 'neg-good':
        tee = 'may-be-unnecessary'
    else:
        tee = 'use-judgment'          # limited TTE, no features: guideline silent (app design choice)

    # --- Statement 5: increased risk + unknown focus -> whole-body or combined imaging.
    # Judged as advice on the workup screen, i.e. BEFORE workup results exist
    # (v1 of this key wrongly used the later workup result; see VALIDATION_REPORT.md).
    wbi = risk == 'increased' and 'unknown' in other and not endocarditis_on_tte

    # --- Figure 1 classification
    if endocarditis_on_tte or (risk == 'increased' and c['focus'] == 'yes'):
        cls = 'with-focus'
    elif risk == 'low':
        cls = 'without-focus'
    elif risk == 'increased' and c['focus'] == 'no':
        cls = 'without-focus'
    else:
        cls = 'pending'

    # --- Statements 6 & 7: duration
    flags = []
    if cls == 'with-focus':
        duration, days = '4+ weeks', 28
    elif cls == 'without-focus' and risk == 'low':
        duration, days = '14 days', 14
    elif cls == 'without-focus':
        if c['resolved'] is False:
            duration, days = 'not-ready', None       # 14 d only if signs/symptoms resolved
        else:
            duration, days = '14 days', 14
            if fubc_pos: flags.append('prolonged bacteremia')
            if c['workupComplete'] is False: flags.append('workup incomplete')
            names = {'retained': 'retained device', 'newgraft': 'new graft', 'dvt': 'dvt'}
            flags += [names[x] for x in c['longer']]
    else:
        duration, days = 'none', None

    # --- Statement 2: Day 1 = clearance day; if source control came later, that date
    day1 = last = None
    if days:
        clear = date.fromisoformat(c['clearDate'])
        src = date.fromisoformat(c['sourceDate']) if c['sourceDate'] else None
        start = src if (src and src > clear) else clear
        day1, last = start.isoformat(), (start + timedelta(days=days - 1)).isoformat()

    return dict(id=c['id'], risk=risk, tee=tee, wbi=wbi, classification=cls,
                duration=duration, flags=sorted(flags), day1=day1, lastDay=last,
                results_screen=(risk == 'increased' and not endocarditis_on_tte))


json.dump([expected(c) for c in cases], open('expected.json', 'w'), indent=1)
print('wrote expected.json')
