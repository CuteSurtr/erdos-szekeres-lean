#!/usr/bin/env python3
"""Search, inside the occupied states of each known 33-hole residual vector, for a
support S with a two-level compression (cap or cup) and |S| >= 23.  Such an S would be a
violated Baek block row h(S) >= |S| - 22.  Greedy removal of the most conflicted state,
many randomized restarts.  The compression is any function of the label (weaker
requirement than the Lean 'active cells + thresholds' format; a hit needs that check)."""
import gzip, json, random, sys
from collections import Counter
ROOT = '/home/jay/research/lean/erdos-szekeres-lean/'
cat = json.load(gzip.open(ROOT + 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'))
S, C = cat['states'], cat['constraints']; n = len(S)
cells = [frozenset((a + 1, y) for a in range(4) for y in range(1, s[a] + 1)) for s in S]
D = {}
for i in range(n):
    for j in range(n):
        if i != j:
            D[i, j] = (cells[j] - cells[i]) - {(1, 6)}
def conflicts(X, coord):
    """labels forced low/high with the middle states that force them"""
    low = {}; high = {}
    for y in X:
        inn = set().union(*[D[x, y] for x in X if x != y])
        out = set().union(*[D[y, z] for z in X if z != y])
        for l1 in inn:
            for l2 in out:
                if l2[coord] > l1[coord]:
                    low.setdefault(l1, set()).add(y); high.setdefault(l2, set()).add(y)
    bad = set(low) & set(high)
    blame = Counter()
    for l in bad:
        for y in low[l] | high[l]: blame[y] += 1
        # also blame the sources/targets that create the label at those middles
    return bad, blame
def greedy(X, coord, rng):
    X = list(X)
    while True:
        bad, blame = conflicts(X, coord)
        if not bad: return X
        top = max(blame.values())
        cands = [y for y, v in blame.items() if v == top]
        X.remove(rng.choice(cands))
R = ROOT + 'cloud/es7-2026-10-19/results/'
w = json.load(open(R + 'ES8SLACK/witnesses.json'))['residual_2650_33_hole_witnesses_state0_occupied']
t = json.load(open(R + 'ES8SLACK/review/C3_residual/template_closure_probe_out.json'))['milp']['holes']
vecs = [set(x) for x in w] + [set(t)]
rng = random.Random(13)
out = []
for vi, H in enumerate(vecs):
    occ = [i for i in range(n) if i not in H]
    occF = [i for i in occ if S[i][0] >= 5]
    best = {}
    for coord in (0, 1):
        for seed_set, name in ((occF, 'F'), (occ, 'all')):
            for rep in range(int(sys.argv[1]) if len(sys.argv) > 1 else 6):
                X = greedy(seed_set, coord, rng)
                k = (coord, name)
                if len(X) > len(best.get(k, [])):
                    best[k] = sorted(X)
    for k, X in best.items():
        known = any(set(X) <= set(r['support']) and len(set(r['support'])) - r['rhs'] <= 22 for r in C)
        print(f'vector {vi} coord {"cap" if k[0]==0 else "cup"} seed {k[1]}: best compressible |S| = {len(X)}'
              f'{"  VIOLATED BAEK ROW" if len(X) >= 23 else ""}  (inside an existing block: {known})', flush=True)
        out.append({'vector': vi, 'coord': k[0], 'seed': k[1], 'support': X})
json.dump(out, open('block_greedy_out.json', 'w'))
