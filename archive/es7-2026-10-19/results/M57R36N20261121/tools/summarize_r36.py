#!/usr/bin/env python3
"""summarize_r36.py -- end-of-session accounting for the rung N = 36 cube campaign (stdlib only).

Reads cubes2/ (drive2.py, both cases; jobs handed over per cubes2/handed.json are counted there only), cubes/state.json, cubes/results.tsv (case A driver; its B jobs never ran) and cubes_b/state.json,
cubes_b/results.tsv (B-only driver).  A leaf counts as certified only if a results.tsv row says
'verified' (driver or reverify.py) AND its .cake file holds the exact line 's VERIFIED UNSAT'.
Prints per case: certified leaves, the covered fraction sum 2^-|cube| over certified leaves (EXACT, Fraction),
open jobs (queued / running / timeout leaves), splits, CaDiCaL seconds and conflicts of certified leaves,
LRAT bytes, cake heaps; and writes summary.json.
"""
import json, os
from fractions import Fraction

D = os.path.dirname(os.path.abspath(__file__))


def exact_line(path):
    try:
        return any(l.strip() == 's VERIFIED UNSAT' for l in open(path, errors='replace'))
    except FileNotFoundError:
        return False


def load(sub, case):
    st = json.load(open(os.path.join(D, sub, 'state.json')))
    jobs = [j for j in st['jobs'] if j['case'] == case]
    rows = {}
    res = os.path.join(D, sub, 'results.tsv')
    if os.path.exists(res):
        for line in open(res):
            f = line.rstrip('\n').split('\t')
            if len(f) >= 11 and f[1] == case:
                rows.setdefault(f[0], []).append(f)
    return jobs, rows


out = {}
hp = os.path.join(D, 'cubes2', 'handed.json')
handed = set(json.load(open(hp))) if os.path.exists(hp) else set()
for case, subs in (('A', ['cubes', 'cubes2']), ('B', ['cubes_b', 'cubes2'])):
    cert, open_jobs, splits, cpu, conf, lb, heaps = [], [], 0, 0.0, 0, 0, []
    cover = Fraction(0)
    for sub in subs:
        jobs, rows = load(sub, case)
        for j in jobs:
            if sub != 'cubes2' and j['id'] in handed and j['status'] == 'queued':
                continue          # handed over to drive2.py; counted there
            rs = rows.get(j['id'], [])
            ver = [r for r in rs if r[3] == 'verified']
            if j['status'] == 'split':
                splits += 1
                continue
            if ver and exact_line(os.path.join(D, sub, j['id'] + '.cake')):
                r = ver[-1]
                cert.append(j['id'])
                cover += Fraction(1, 2 ** len(j['units']))
                done = [x for x in rs if x[4]]
                cpu += float(done[0][4]) if done and done[0][4] else 0.0
                conf += int(done[0][5]) if done and done[0][5].isdigit() else 0
                lb += int(r[7]) if r[7].isdigit() else 0
                heaps.append(r[11] if len(r) > 11 else '')
            else:
                open_jobs.append((j['id'], j['status']))
    out[case] = {'certified_leaves': len(cert), 'covered_fraction': str(cover), 'covered_float': float(cover),
                 'open': len(open_jobs), 'open_by_status': {s: sum(1 for _, x in open_jobs if x == s)
                                                            for s in sorted({x for _, x in open_jobs})},
                 'splits': splits, 'cadical_wall_s_certified': round(cpu, 1), 'conflicts_certified': conf,
                 'lrat_bytes_certified': lb, 'heaps': sorted(set(heaps)), 'certified': sorted(cert)}
mono = os.path.join(D, 'run/c36_tle22.out')
out['B_mono'] = {'out': open(mono).read().strip() if os.path.exists(mono) else '',
                 'cake_exact_line': exact_line(os.path.join(D, 'run/c36_tle22.cake'))}
json.dump(out, open(os.path.join(D, 'summary.json'), 'w'), indent=1)
for k, v in out.items():
    print(k, {x: y for x, y in v.items() if x != 'certified'})
