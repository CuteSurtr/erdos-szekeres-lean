"""Independent exact verification of a REAL point set in FL(a,b) without a strong (Pascal) split.
Pure Python, integer arithmetic only (no SAT solver, no C library, no numpy):
 1. distinct x-coordinates, no three points collinear;
 2. no a-cap, no b-cup, no ((a-1)-cap,(b-1)-cup)-gon          (brute force over all subsets);
 3. for every one of the 2^n partitions S1 + S2: S1 contains an (a-1)-cap or an ((a-2),(b-1))-gon, or
    S2 contains a (b-1)-cup or an ((a-1),(b-2))-gon           (brute force).
usage: verify_real_nosplit.py <file.jsonl with records {n, P}> [a b]"""
import sys, json, itertools
a = int(sys.argv[2]) if len(sys.argv) > 2 else 5; b = int(sys.argv[3]) if len(sys.argv) > 3 else 5
def verify(P):
    P = sorted(tuple(p) for p in P); n = len(P)
    assert all(isinstance(c, int) for p in P for c in p)
    assert len({p[0] for p in P}) == n, 'x-coordinates not distinct'
    det = lambda i, j, k: (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
    sg = {}
    for t in itertools.combinations(range(n), 3):
        d = det(*t); assert d != 0, 'collinear triple'
        sg[t] = 1 if d > 0 else -1
    def chains(L, s): return [idx for idx in itertools.combinations(range(n), L) if all(sg[idx[q], idx[q + 1], idx[q + 2]] == s for q in range(L - 2))]
    assert not chains(a, -1), 'has an a-cap'
    assert not chains(b, 1), 'has a b-cup'
    capsA1 = chains(a - 1, -1); cupsB1 = chains(b - 1, 1); capsA2 = chains(a - 2, -1); cupsB2 = chains(b - 2, 1)
    def gons(caps, cups):
        by = {}
        for c in cups: by.setdefault((c[0], c[-1]), []).append(c)
        return [frozenset(c) | frozenset(u) for c in caps for u in by.get((c[0], c[-1]), [])]
    assert not gons(capsA1, cupsB1), 'has a first-layer gon'
    m = lambda s: sum(1 << p for p in s)
    bad1 = sorted(set([m(c) for c in capsA1] + [m(g) for g in gons(capsA2, cupsB1)]))
    bad2 = sorted(set([m(c) for c in cupsB1] + [m(g) for g in gons(capsA1, cupsB2)]))
    full = (1 << n) - 1; good = 0
    for S1 in range(1 << n):
        S2 = full ^ S1
        if any(x & S1 == x for x in bad1): continue
        if any(x & S2 == x for x in bad2): continue
        good += 1
    return n, len(capsA1), len(cupsB1), good
if __name__ == '__main__':
    for line in open(sys.argv[1]):
        d = json.loads(line); n, c4, u4, good = verify(d['P'])
        print(f'record {d.get("record")}: real set of {n} points in FL({a},{b}) ({c4} {a-1}-caps, {u4} {b-1}-cups); partitions tested {1 << n}; valid strong splits: {good}', flush=True)
