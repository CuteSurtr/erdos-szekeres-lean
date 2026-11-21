#!/usr/bin/env python3
"""final_check.py [R36DIR] -- read-only end-of-campaign accounting for rung N = 36 (r36-audit, 21 Nov 2026).

Independent of drive.py's own bookkeeping.  For each case (A, B) of cubes/state.json:
  * leaves = jobs whose status is not 'split'; every unit is +-(32759+s), s in 2..55, no variable twice;
  * the leaves are pairwise disjoint (some variable with opposite signs) and sum of 2^-|units| == 1
    (exact Fraction): together this is a complete case split of the base CNF -- for ANY choice of
    split variables, so soundness of the split does not depend on what occ[s] means;
  * every split job has exactly its two children (cube + x, cube - x) in the job list;
  * a leaf counts only if: status 'verified' (or 'cake_failed' followed by a reverify.py VERIFIED row), its .cake file has the exact line 's VERIFIED UNSAT',
    its results.tsv row says VERIFIED, and the recorded cnf_sha equals SHA-256 of
    (header with clause count + |units|) + (base body) + ('%d 0\\n' per unit), recomputed here from
    the base CNF (whose own SHA-256 is checked against the record first).
Case B alternatively closes by the monolithic run: run/c36_tle22.out has exit=20 and a cake_lpr
output file given with --monocake has the exact line.
Prints per case: CLOSED (all leaves pass) or OPEN with the list of failing leaves.
"""
import sys, os, json, hashlib
from fractions import Fraction

R = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else \
    '<scratch>/r36'
MONOCAKE = (R + '/run/c36_tle22.cake') if os.path.exists(R + '/run/c36_tle22.cake') else None
for i, a in enumerate(sys.argv):
    if a == '--monocake':
        MONOCAKE = sys.argv[i + 1]
OCC0 = 32759
BASE = {'A': ('run/c36_rle13.cnf', 'aba65111d42151131a55e7596043721bd86fe94d05c8fea0b2750212d2808bbe'),
        'B': ('run/c36_tle22.cnf', '08b8ea9c9c588aa242485163a3d4836a0c79f8bd91c61ac25357010dc2bd9339')}


def exact_line(path):
    try:
        with open(path) as f:
            return any(l.strip() == 's VERIFIED UNSAT' for l in f)
    except FileNotFoundError:
        return False


st = json.load(open(R + '/cubes/state.json'))
rows = {}
if os.path.exists(R + '/cubes/results.tsv'):
    for line in open(R + '/cubes/results.tsv'):
        x = line.rstrip('\n').split('\t')
        if len(x) >= 10:
            rows.setdefault(x[0], []).append(x)
ids = {j['id']: j for j in st['jobs']}
assert len(ids) == len(st['jobs']), 'duplicate job ids'

verdict = {}
for case in ('A', 'B'):
    jobs = [j for j in st['jobs'] if j['case'] == case]
    leaves = [j for j in jobs if j['status'] != 'split']
    probs = []
    for j in jobs:
        vs = [abs(u) for u in j['units']]
        if len(set(vs)) != len(vs) or not all(OCC0 + 2 <= v <= OCC0 + 55 for v in vs):
            probs.append(('bad units', j['id']))
        if j['status'] == 'split':
            kids = [k for k in jobs if k.get('parent') == j['id']]
            ku = sorted(tuple(k['units']) for k in kids)
            ok = len(kids) == 2 and all(list(k[:-1]) == j['units'] for k in ku) and ku[0][-1] == -ku[1][-1]
            if not ok:
                probs.append(('split without its two children', j['id']))
    meas = sum(Fraction(1, 2 ** len(j['units'])) for j in leaves)
    sets = [{u for u in j['units']} for j in leaves]
    disjoint = all(any(-u in sets[b] for u in sets[a]) for a in range(len(sets)) for b in range(a + 1, len(sets)))
    cover = disjoint and meas == 1
    # verified leaves: recompute the cube CNF hash
    path, rec = BASE[case]
    with open(R + '/' + path, 'rb') as f:
        hdr = f.readline()
        body = f.read()
    hb = hashlib.sha256(hdr); hb.update(body)
    base_ok = hb.hexdigest() == rec
    _, _, nv, nc = hdr.split()
    good, bad = [], []
    for j in leaves:
        why = []
        r = rows.get(j['id'], [])
        if j['status'] not in ('verified', 'cake_failed') or not any(x[3] == 'verified' for x in r):
            # 'cake_failed' + a later VERIFIED row = re-checked by reverify.py with a larger heap
            why.append('status ' + j['status'])
        else:
            if not exact_line(R + '/cubes/' + j['id'] + '.cake'):
                why.append('no exact cake line')
            r = rows.get(j['id'], [])
            if not any(x[3] == 'verified' and x[9] == 'VERIFIED' for x in r):
                why.append('no VERIFIED row')
            h = hashlib.sha256(b'p cnf %s %d\n' % (nv, int(nc) + len(j['units'])))
            h.update(body)
            h.update(''.join('%d 0\n' % u for u in j['units']).encode())
            if not any(x[6] == h.hexdigest() for x in r):
                why.append('cnf_sha differs from base+units')
        (bad if why else good).append((j['id'], why))
    print(f'case {case}: base sha {"OK" if base_ok else "MISMATCH"}; jobs {len(jobs)}, leaves {len(leaves)}, '
          f'measure {meas}, pairwise disjoint {disjoint}, structural problems {probs[:5]}')
    print(f'  leaves passing all checks: {len(good)}; failing: {len(bad)}')
    for b in bad[:12]:
        print('   ', b[0], '; '.join(b[1]))
    closed = base_ok and cover and not probs and not bad
    if case == 'B' and not closed:
        out = open(R + '/run/c36_tle22.out').read() if os.path.exists(R + '/run/c36_tle22.out') else ''
        mono = 'exit=20' in out and MONOCAKE is not None and exact_line(MONOCAKE)
        print('  monolithic case B:', out.strip().replace('\n', ' | '), '| cake file', MONOCAKE,
              '->', 'CLOSED by monolithic run' if mono else 'not closed')
        closed = closed or mono
    verdict[case] = closed
    print(f'  case {case}:', 'CLOSED' if closed else 'OPEN')
print('RUNG 36:', 'BOTH CASES CLOSED (CNF level)' if all(verdict.values()) else 'NOT CLOSED')
