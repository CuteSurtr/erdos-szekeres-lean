"""Referee check: n_in statistics of zcnf.py convex4_patterns over all 16 sign patterns, and which patterns are
realizable by real 4-point sets (exhaustive over a small integer grid, exact)."""
import itertools

def parity_sort(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return (tuple(sorted(t)), -1 if inv & 1 else 1)

def n_in(pat):
    base = {(0, 1, 2): pat[0], (0, 1, 3): pat[1], (0, 2, 3): pat[2], (1, 2, 3): pat[3]}
    def O(x, y, z):
        s, sg = parity_sort((x, y, z))
        return sg * base[s]
    return sum(O(a, b, d) == O(b, c, d) == O(c, a, d) for d in range(4) for a, b, c in
               [tuple(q for q in range(4) if q != d)])

def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def sgn(x):
    return (x > 0) - (x < 0)

# realizable patterns, with convexity, from all 4-tuples of distinct points of a 4x4 grid in general position
real = {}
grid = [(x, y) for x in range(4) for y in range(4)]
for Q in itertools.permutations(grid, 4):
    tr = [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]
    pat = tuple(sgn(orient(*[Q[i] for i in T])) for T in tr)
    if 0 in pat:
        continue
    # convex position: no point strictly inside triangle of others
    conv = True
    for d in range(4):
        a, b, c = [Q[i] for i in range(4) if i != d]
        s = (sgn(orient(a, b, Q[d])), sgn(orient(b, c, Q[d])), sgn(orient(c, a, Q[d])))
        if s[0] == s[1] == s[2]:
            conv = False
    real.setdefault(pat, set()).add(conv)

hist = {}
for pat in itertools.product((1, -1), repeat=4):
    k = n_in(pat)
    r = real.get(pat)
    tag = "non-realizable" if r is None else ("convex" if r == {True} else ("non-convex" if r == {False} else "MIXED"))
    hist.setdefault((k, tag), []).append(pat)
for (k, tag), pats in sorted(hist.items()):
    print(f"n_in={k} {tag:15s} {len(pats)} patterns: {pats}")
kept = [p for p in itertools.product((1, -1), repeat=4) if n_in(p) == 0]
assert all(real.get(p) == {True} for p in kept), "a kept pattern is not always convex"
print("kept (n_in == 0):", len(kept), "all realizable and always convex: OK")
