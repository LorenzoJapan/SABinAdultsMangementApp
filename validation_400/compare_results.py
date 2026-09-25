"""Compare what the app displayed (app_results.json) with the independent
answer key (expected.json). Output: comparison.csv + summary printed."""
import json, csv
from datetime import date
from collections import Counter, defaultdict

cases = {c['id']: c for c in json.load(open('cases.json'))}
exp = {e['id']: e for e in json.load(open('expected.json'))}
app = {a['id']: a for a in json.load(open('app_results.json'))}

RISK = {'Low-risk SAB (provisional)': 'low-provisional', 'Low-risk SAB': 'low', 'Increased-risk SAB': 'increased'}
TEE = {'Get a TTE': 'obtain-tte', 'Endocarditis on TTE': 'focus-found', 'TEE suggested': 'suggested',
       'Consider TEE': 'consider', 'TEE: use judgment': 'use-judgment', 'TEE may be unnecessary': 'may-be-unnecessary'}
FLAG = {'Prolonged bacteremia (≥48 h)': 'prolonged bacteremia', 'Workup incomplete or limited': 'workup incomplete',
        'Intracardiac device left in place': 'retained device', 'Recently placed endovascular graft': 'new graft',
        'Clot (DVT) at a central line site': 'dvt'}


def cls_of(t):
    if t.startswith('SAB with a'): return 'with-focus'
    if t.startswith('SAB without'): return 'without-focus'
    if t.startswith('Classification not final'): return 'pending'
    return 'UNKNOWN: ' + t


def dur_of(num, unit):
    if num is None: return 'none'
    if num == '—': return 'not-ready'
    return f'{num} {unit}'


def pretty(iso):  # US display, e.g. "Sun, Sep 20"
    d = date.fromisoformat(iso); return d.strftime('%a, %b ') + str(d.day)


FIELDS = ['flow', 'risk', 'tee', 'wbi', 'results_screen', 'classification', 'duration', 'flags', 'day1', 'lastDay']
ok = Counter(); rows = []; misses = defaultdict(list)
for cid, e in exp.items():
    a = app[cid]
    got = {}
    if a['error']:
        got = {f: 'ERROR' for f in FIELDS}; got['flow'] = a['error']
    else:
        got['flow'] = 'ok'
        got['risk'] = RISK.get(a['riskText'], 'UNKNOWN: ' + a['riskText'])
        tee_titles = [t for t in a['advice'] if t in TEE]
        got['tee'] = TEE[tee_titles[0]] if len(tee_titles) == 1 else f'UNKNOWN: {a["advice"]}'
        got['wbi'] = 'Whole-body imaging' in a['advice']
        got['results_screen'] = a['results_screen']
        got['classification'] = cls_of(a['classText'])
        got['duration'] = dur_of(a['durNum'], a['durUnit'])
        got['flags'] = sorted(FLAG.get(f, 'UNKNOWN: ' + f) for f in a['flags'])
        got['day1'] = a.get('dates', [None, None])[0] if a.get('dates') else None
        got['lastDay'] = a.get('dates', [None, None])[1] if a.get('dates') else None
    want = dict(e); want['flow'] = 'ok'
    want['day1'] = pretty(e['day1']) if e['day1'] else None
    want['lastDay'] = pretty(e['lastDay']) if e['lastDay'] else None
    row = {'id': cid, 'category': cases[cid]['category']}
    all_ok = True
    for f in FIELDS:
        match = got[f] == want[f]
        ok[f] += match; all_ok &= match
        row[f'{f}_expected'] = want[f]; row[f'{f}_app'] = got[f]
        if not match: misses[f].append((cid, want[f], got[f]))
    row['ALL_MATCH'] = all_ok; ok['ALL'] += all_ok
    rows.append(row)

with open('comparison.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

n = len(rows)
print(f'Cases: {n}')
for f in FIELDS + ['ALL']:
    print(f'{f:16s} {ok[f]:4d}/{n}  {100*ok[f]/n:5.1f}%')
for f, lst in misses.items():
    print(f'\nMISMATCHES in {f}: {len(lst)}')
    for m in lst[:10]: print('  ', m)
json.dump({'n': n, 'ok': dict(ok), 'misses': {k: v for k, v in misses.items()}}, open('summary.json', 'w'), indent=1, default=str)
