"""Independent brute-force verification that an abstract FL(a,b)-configuration has NO strong (Pascal) split:
all 2^n partitions are tested with a pure-Python exact DP (no SAT solver involved)."""
import sys, json, itertools
d = json.load(open(sys.argv[1])); a, b, n, sig = d['a'], d['b'], d['n'], d['sig']
T = list(itertools.combinations(range(n), 3)); sg = {t: (1 if c == '+' else -1) for t, c in zip(T, sig)}
# 1. signotope axioms
for i, j, k, l in itertools.combinations(range(n), 4):
    x = [sg[i, j, k], sg[i, j, l], sg[i, k, l], sg[j, k, l]]
    assert sum(1 for q in range(3) if x[q] != x[q + 1]) <= 1
# 2. chains by brute force over subsets (n <= 14): caps/cups of given sizes
def is_chain(idx, s):
    return all(sg[idx[q], idx[q + 1], idx[q + 2]] == s for q in range(len(idx) - 2))
def chains(L, s): return [idx for idx in itertools.combinations(range(n), L) if is_chain(idx, s)]
assert not chains(a, -1) and not chains(b, 1), 'has an a-cap or a b-cup'
capsA1 = chains(a - 1, -1); cupsB1 = chains(b - 1, 1); capsA2 = chains(a - 2, -1); cupsB2 = chains(b - 2, 1)
def gons(caps, cups):
    out = []
    byend = {}
    for c in cups: byend.setdefault((c[0], c[-1]), []).append(c)
    for c in caps:
        for u in byend.get((c[0], c[-1]), []):
            out.append(frozenset(c) | frozenset(u))
    return out
assert not gons(capsA1, cupsB1), 'has a first-layer gon'
print(f'valid FL({a},{b}) signotope on {n} points: {len(capsA1)} {a-1}-caps, {len(cupsB1)} {b-1}-cups')
# 3. forbidden structures as bitmasks
m = lambda s: sum(1 << p for p in s)
bad1 = sorted(set([m(c) for c in capsA1] + [m(g) for g in gons(capsA2, cupsB1)]))   # must not lie inside S1
bad2 = sorted(set([m(c) for c in cupsB1] + [m(g) for g in gons(capsA1, cupsB2)]))   # must not lie inside S2
full = (1 << n) - 1; good = 0
for S1 in range(1 << n):
    S2 = full ^ S1
    if any(x & S1 == x for x in bad1): continue
    if any(x & S2 == x for x in bad2): continue
    good += 1
print(f'partitions tested: {1 << n}; valid strong splits: {good}')
