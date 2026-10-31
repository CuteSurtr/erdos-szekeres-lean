"""verify2.py - second independent exact check (pure Python integers).
Reads columns a b (Eisenstein coordinates a + b*w), maps them to the integer
lattice (2a - b, b), an affine image of the Euclidean points, which preserves
collinearity and convex position. Counts hull sizes of all 7-subsets with
Andrew's monotone chain and checks the 3-fold symmetry."""
import sys, itertools
def load(fn):
    pts = []
    for line in open(fn):
        if line.startswith('#') or not line.strip(): continue
        a, b = map(int, line.split()[:2]); pts.append((a, b))
    return pts
def cross(o, p, q): return (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
def hull_size(ps):
    ps = sorted(ps); lo = []; up = []
    for p in ps:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(ps):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return len(lo) + len(up) - 2
pts = load(sys.argv[1]); n = len(pts)
xy = [(2*a - b, b) for a, b in pts]
assert n == 33 and len(set(xy)) == 33, "need 33 distinct points"
col = sum(1 for t in itertools.combinations(xy, 3) if cross(*t) == 0)
print("points", n, "collinear_triples", col)
S = set(pts); rot = lambda p: (-p[1], p[0]-p[1])
print("3fold_symmetric", all(rot(p) in S for p in pts))
if col: sys.exit(1)
dist = {}
for s in itertools.combinations(xy, 7):
    h = hull_size(s); dist[h] = dist.get(h, 0) + 1
print("7-subsets hull-size distribution", dict(sorted(dist.items())))
print("convex7", dist.get(7, 0))
