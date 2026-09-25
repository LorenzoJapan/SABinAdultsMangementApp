"""Generate 400 synthetic adult S. aureus bacteremia cases (no real patient data).

Stratified so every branch of the 2026 IDSA/ESCMID framework is exercised,
plus deliberate edge cases. Fixed seed -> identical file every run.
Output: cases.json
"""
import json, random
from datetime import date, timedelta

rng = random.Random(20260925)

OTHER = ['valve', 'idu', 'graft', 'prior90', 'signs', 'embolic', 'multi', 'unknown']
LONGER = ['retained', 'newgraft', 'dvt']


def rand_date():
    # Mix of ordinary dates and calendar edge cases (month/year ends, leap years)
    edge = [date(2026, 12, 25), date(2026, 12, 31), date(2027, 2, 20), date(2028, 2, 20),
            date(2028, 2, 28), date(2027, 12, 20), date(2026, 1, 31), date(2026, 4, 30)]
    if rng.random() < 0.3:
        return rng.choice(edge)
    return date(2025, 1, 1) + timedelta(days=rng.randrange(0, 365 * 4))


def dates():
    clear = rand_date()
    r = rng.random()
    if r < 0.45:   src = None                                           # no source control
    elif r < 0.60: src = clear - timedelta(days=rng.randint(1, 5))      # before clearance
    elif r < 0.70: src = clear                                           # same day
    else:          src = clear + timedelta(days=rng.randint(1, 9))      # after clearance
    return clear.isoformat(), (src.isoformat() if src else None)


def base():
    return dict(adult=True, saConfirmed=True, fubc48='neg', tte='neg-good', community=False,
                device=False, other=[], focus=None, resolved=None, workupComplete=None, longer=[])


def with_workup(c, focus=None):
    """Fill workup answers for an increased-risk case."""
    c['focus'] = focus or rng.choice(['yes', 'no', 'no', 'ongoing'])
    if c['focus'] == 'no':
        c['resolved'] = rng.random() > 0.2
        c['workupComplete'] = rng.random() > 0.35
        c['longer'] = [l for l in LONGER if rng.random() < 0.2]
    return c


cases = []
def add(cat, c):
    c['clearDate'], c['sourceDate'] = dates()
    c['id'] = f'SAB-{len(cases)+1:03d}'
    c['category'] = cat
    cases.append(c)

# A. Low risk, clean (30)
for _ in range(30): add('A low risk', base())
# B. Low risk, limited-quality TTE (15)
for _ in range(15): c = base(); c['tte'] = 'neg-limited'; add('B low risk, limited TTE', c)
# C. No risk factors but results pending (25)
for i in range(25):
    c = base(); c['fubc48'], c['tte'] = [('pending', 'neg-good'), ('neg', 'pending'), ('pending', 'pending')][i % 3]
    add('C provisional (pending)', c)
# D. Exactly one KEY factor (60 = 20 each)
for k in ['community', 'fubc', 'device']:
    for _ in range(20):
        c = base()
        if k == 'fubc': c['fubc48'] = 'pos'
        else: c[k] = True
        add(f'D single key: {k}', with_workup(c))
# E. Exactly one OTHER factor (80 = 10 each)
for f in OTHER:
    for _ in range(10):
        c = base(); c['other'] = [f]; add(f'E single other: {f}', with_workup(c))
# F. Random multi-factor (100)
for _ in range(100):
    c = base()
    c['community'] = rng.random() < 0.5
    c['device'] = rng.random() < 0.25
    c['fubc48'] = rng.choice(['neg', 'neg', 'pos', 'pending'])
    c['tte'] = rng.choice(['neg-good', 'neg-good', 'neg-limited', 'pending'])
    c['other'] = [f for f in OTHER if rng.random() < 0.2]
    if not (c['community'] or c['device'] or c['fubc48'] == 'pos' or c['other']):
        c['other'] = [rng.choice(OTHER)]
    add('F multi-factor', with_workup(c))
# G. TTE shows endocarditis (30)
for _ in range(30):
    c = base(); c['tte'] = 'ie'
    c['community'] = rng.random() < 0.4; c['device'] = rng.random() < 0.3
    c['fubc48'] = rng.choice(['neg', 'pos', 'pending'])
    c['other'] = [f for f in OTHER if rng.random() < 0.15]
    add('G TTE shows endocarditis', c)
# H. Targeted edge cases (60)
for _ in range(20):
    c = base(); c['community'] = True; c = with_workup(c, 'no'); c['resolved'] = False; add('H symptoms not resolved', c)
for _ in range(20):
    c = base(); c['other'] = [rng.choice(OTHER)]; c['focus'] = 'ongoing'; add('H still looking', c)
for _ in range(20):
    c = base(); c['fubc48'] = 'pos'; c['focus'] = 'no'; c['resolved'] = True
    c['workupComplete'] = False; c['longer'] = [l for l in LONGER if rng.random() < 0.6]
    add('H all longer-course flags', c)

assert len(cases) == 400, len(cases)
json.dump(cases, open('cases.json', 'w'), indent=1)
print('wrote', len(cases), 'cases')
