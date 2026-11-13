#!/usr/bin/env python3
"""Independent check of claim C6 (early-vertex occupancy), exact integer arithmetic only.

Re-implements, from the Lean definitions (ActualRanks.EndingPath/rank/labels, ResidualRanks.StartingPath/
rank/labels, BalancedStates.column, ResidualStates.column, BalancedCatalog/ResidualCatalog.ownerIndex):
  E_color(u,v) = max length of a path ending with the exact pair (u,v)  [EndingPath]
  F(u,v)       = max length of a cap starting with the exact pair (u,v) [StartingPath, color false]
  d_B(u,v) = (E_false-1, E_true-1);  d_R(u,v) = (6-F, E_true-1)
  column(v,i) = max_{u<v} (d2 if i+1 <= d1 else 0)   (0 if v = 0)
  balanced owner = catalog index of [column(v,0..4)]; residual owner = index of [column(v,0..3)] + [0]
and checks, for (a) random real-point configurations with integer coordinates and (b) ALL Boolean triple
colourings for small n, that
  balanced: owner(0)=0, owner(1)=1, owner(2) in {2,3}
  residual: owner(0)=0, owner(1) in {1,2,4,7}
Catalog order is read from the JSON sources used by the 311/313 certificates.
Usage: python3 -I check_early_vertex.py
"""
import gzip, itertools, json, random, sys

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
BAL = ROOT + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
RES = ROOT + '/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'

bal_states = [tuple(x) for x in json.load(open(BAL))['states']]
res_states = [tuple(x) for x in json.loads(gzip.decompress(open(RES, 'rb').read()))['states']]
assert len(bal_states) == 252 and len(res_states) == 154
BIDX = {s: i for i, s in enumerate(bal_states)}
RIDX = {s: i for i, s in enumerate(res_states)}
assert len(BIDX) == 252 and len(RIDX) == 154
print('balanced idx 0..3 :', bal_states[:4])
print('residual idx 0,1,2,4,7:', [res_states[i] for i in (0, 1, 2, 4, 7)])


def ranks(n, cup):
    """cup(i,j,k) -> bool for i<j<k. Returns dicts E[color][(u,v)], F[(u,v)] by brute DP."""
    E = {False: {}, True: {}}
    for v in range(n):
        for u in range(v):
            for col in (False, True):
                best = 2
                for t in range(u):
                    if cup(t, u, v) == col:
                        best = max(best, E[col][(t, u)] + 1)
                E[col][(u, v)] = best
    F = {}
    for u in range(n - 1, -1, -1):
        for v in range(n - 1, u, -1):
            best = 2
            for w in range(v + 1, n):
                if cup(u, v, w) is False:
                    best = max(best, F[(v, w)] + 1)
            F[(u, v)] = best
    return E, F


def columns(v, labels, ncol):
    out = []
    for i in range(ncol):
        m = 0
        for u in range(v):
            d1, d2 = labels[(u, v)]
            if i + 1 <= d1:
                m = max(m, d2)
        out.append(m)
    return out


def analyse(n, cup):
    E, F = ranks(n, cup)
    maxcap = max(E[False].values(), default=1 if n else 0)
    maxcup = max(E[True].values(), default=1 if n else 0)
    res = {}
    # balanced: no 7-cap, no 7-cup  (octagon-freeness is irrelevant to labels at vertices 0..2)
    if maxcap < 7 and maxcup < 7:
        lab = {k: (E[False][k] - 1, E[True][k] - 1) for k in E[False]}
        own = [BIDX[tuple(columns(v, lab, 5))] for v in range(n)]
        assert len(set(own)) == n, 'balanced owners not injective?!'
        res['bal'] = own
    # residual: no 6-cap, no 8-cup, no junction (incoming 6-cup and outgoing 5-cap at one vertex)
    junction = any(any(E[True][(t, u)] >= 6 for t in range(u)) and any(F[(u, v)] >= 5 for v in range(u + 1, n))
                   for u in range(n))
    if maxcap < 6 and maxcup < 8 and not junction:
        lab = {k: (6 - F[k], E[True][k] - 1) for k in F}
        for k, (a, b) in lab.items():
            assert 1 <= a <= 4 and 1 <= b <= 6
        own = [RIDX[tuple(columns(v, lab, 4) + [0])] for v in range(n)]
        assert len(set(own)) == n, 'residual owners not injective?!'
        res['res'] = own
    return res


def check(res, stats):
    ok = True
    if 'bal' in res:
        o = res['bal']
        n = len(o)
        holes = set(range(252)) - set(o)
        if n >= 1: ok &= (o[0] == 0)
        if n >= 2: ok &= (o[1] == 1)
        if n >= 3:
            ok &= (o[2] in (2, 3)); stats['bal2'][o[2]] = stats['bal2'].get(o[2], 0) + 1
            ok &= (0 not in holes and 1 not in holes and len({2, 3} & holes) <= 1)
        stats['bal_n'] += 1
    if 'res' in res:
        o = res['res']
        n = len(o)
        holes = set(range(154)) - set(o)
        if n >= 1: ok &= (o[0] == 0)
        if n >= 2:
            ok &= (o[1] in (1, 2, 4, 7)); stats['res1'][o[1]] = stats['res1'].get(o[1], 0) + 1
            ok &= len({1, 2, 4, 7} & holes) <= 3
        stats['res_n'] += 1
    return ok


def det(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def random_config(n, rng, mode):
    while True:
        xs = rng.sample(range(-10**6, 10**6), n)
        xs.sort()
        if mode == 'uniform':
            pts = [(x, rng.randint(-10**6, 10**6)) for x in xs]
        elif mode == 'concave':  # perturbed concave arc: produces long caps starting at (0,1)
            pts = [(x, -(x * x) // 10**6 + rng.randint(-2 * 10**5, 2 * 10**5)) for x in xs]
        else:  # convex arc perturbed: produces long cups
            pts = [(x, (x * x) // 10**6 + rng.randint(-2 * 10**5, 2 * 10**5)) for x in xs]
        if all(det(pts[i], pts[j], pts[k]) != 0 for i, j, k in itertools.combinations(range(n), 3)):
            return pts


def main():
    rng = random.Random(20261101)
    stats = {'bal2': {}, 'res1': {}, 'bal_n': 0, 'res_n': 0}
    allok = True
    # (a) real point sets, exact integer orientation
    trials = 0
    for n in list(range(1, 16)) + [18, 22, 26]:
        for mode in ('uniform', 'concave', 'convex'):
            reps = 300 if n <= 12 else 60
            for _ in range(reps):
                pts = random_config(n, rng, mode)
                cup = lambda i, j, k, P=pts: det(P[i], P[j], P[k]) > 0
                r = analyse(n, cup)
                allok &= check(r, stats)
                trials += 1
    print('point trials', trials, 'balanced-valid', stats['bal_n'], 'residual-valid', stats['res_n'])
    print('  balanced owner(2) distribution', dict(sorted(stats['bal2'].items())))
    print('  residual owner(1) distribution', dict(sorted(stats['res1'].items())))
    # (b) exhaustive Boolean colourings (the Lean statements hold for any cup function)
    for n in range(1, 7):
        triples = list(itertools.combinations(range(n), 3))
        st = {'bal2': {}, 'res1': {}, 'bal_n': 0, 'res_n': 0}
        for bits in range(1 << len(triples)):
            col = {t: bool((bits >> k) & 1) for k, t in enumerate(triples)}
            cup = lambda i, j, k, C=col: C[(i, j, k)]
            r = analyse(n, cup)
            allok &= check(r, st)
        print(f'exhaustive n={n}: colourings {1 << len(triples)}, balanced-valid {st["bal_n"]}, residual-valid {st["res_n"]}, '
              f'owner(2) {dict(sorted(st["bal2"].items()))}, residual owner(1) {dict(sorted(st["res1"].items()))}')
    print('ALL CHECKS PASSED' if allok else 'FAILURE')
    return 0 if allok else 1


if __name__ == '__main__':
    sys.exit(main())
