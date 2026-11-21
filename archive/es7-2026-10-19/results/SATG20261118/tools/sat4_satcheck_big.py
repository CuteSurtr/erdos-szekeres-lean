#!/usr/bin/env python3
"""satcheck_big.py -- exact K-gon saturation check with Python integers/Fractions, no coordinate bound
(worker satg, 21 Nov 2026; independent of satcheck.cpp's rank logic and of the record's checkers).
Usage: python3 -I satcheck_big.py points.txt K
Cells: for every line l = (i, j), the distinct crossing parameters t (Fractions) split l into edges; for each edge an
explicit interior parameter t* (midpoint, or t1 - 1 / tlast + 1 for the rays) is taken and the sign of every other
line at P_i + t* D is evaluated exactly; with +/- for l itself this is the sign vector of the two cells along the edge.
Distinct vectors must equal the Euler count 1 + L + sum_v (k_v - 1) (vertices deduplicated by exact coordinates).
Each cell passes iff some convex (K-1)-gon of S has exactly one edge visible from q and passes the 4-point test.
Small sets only (pure Python)."""
import sys
from fractions import Fraction
from itertools import combinations


def main():
    pts = [tuple(map(int, l.split()[:2])) for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
    K = int(sys.argv[2]); n = len(pts)
    o = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    sg = lambda v: (v > 0) - (v < 0)
    assert len(set(pts)) == n
    O = {}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if len({a, b, c}) == 3:
                    O[a, b, c] = sg(o(pts[a], pts[b], pts[c]))
    coll = sum(1 for a, b, c in combinations(range(n), 3) if O[a, b, c] == 0)
    print(f"n={n} K={K} max_abs_coord={max(max(abs(x), abs(y)) for x, y in pts)} collinear={coll}")
    if coll:
        print("VERDICT CHECK_FAILED not_in_general_position"); return
    # convex subsets by growth (exactly one visible edge), polygons CCW
    cnt = [0] * (K + 1); polys = []
    def grow(poly, last):
        m = len(poly); cnt[m] += 1
        if m == K - 1: polys.append(poly)
        if m == K: return
        for z in range(last + 1, n):
            if m < 2: grow(poly + [z], z); continue
            if m == 2:
                grow([poly[0], poly[1], z] if O[poly[0], poly[1], z] > 0 else [poly[0], z, poly[1]], z); continue
            vis = [i for i in range(m) if O[poly[i], poly[(i + 1) % m], z] < 0]
            if len(vis) == 1:
                i = vis[0]; grow(poly[:i + 1] + [z] + poly[i + 1:], z)
    grow([], -1)
    largest = max(s for s in range(K + 1) if cnt[s])
    print("convex_subsets", {s: cnt[s] for s in range(3, K + 1)}, "largest", largest)
    if largest != K - 1:
        print("VERDICT CHECK_FAILED largest_convex_subset_not_K-1"); return
    lines = [(i, j) for i in range(n) for j in range(i + 1, n)]; L = len(lines)
    def at(l, P):  # orient(P_a, P_b, P) for a point P with Fraction coordinates
        a, b = lines[l]; A, B = pts[a], pts[b]
        return sg((B[0] - A[0]) * (P[1] - A[1]) - (B[1] - A[1]) * (P[0] - A[0]))
    cells = set(); verts = {}
    for l, (i, j) in enumerate(lines):
        Pi = pts[i]; D = (pts[j][0] - Pi[0], pts[j][1] - Pi[1])
        ts = []
        for m, (a, c) in enumerate(lines):
            if m == l: continue
            E = (pts[c][0] - pts[a][0], pts[c][1] - pts[a][1])
            den = E[0] * D[1] - E[1] * D[0]
            if den == 0: continue
            num = E[0] * (pts[a][1] - Pi[1]) - E[1] * (pts[a][0] - Pi[0])
            t = Fraction(num, den); ts.append(t)
            v = (Pi[0] + t * D[0], Pi[1] + t * D[1]); verts.setdefault(v, set()).update((l, m))
        ts = sorted(set(ts))
        probes = [ts[0] - 1] + [(ts[k] + ts[k + 1]) / 2 for k in range(len(ts) - 1)] + [ts[-1] + 1]
        for t in probes:
            P = (Pi[0] + t * D[0], Pi[1] + t * D[1])
            v = [at(m, P) for m in range(L)]
            assert v[l] == 0 and all(v[m] != 0 for m in range(L) if m != l)
            for s in (1, -1):
                v[l] = s; cells.add(tuple(v))
    F = 1 + L + sum(len(s) - 1 for s in verts.values())
    print(f"lines={L} vertices={len(verts)} F_euler={F} distinct_cells={len(cells)}")
    if F != len(cells):
        print("VERDICT CHECK_FAILED cell_count"); return
    li = {(a, b): k for k, (a, b) in enumerate(lines)}
    def chi(v, a, b, c):  # q = index n
        if a == n: a, b, c = b, c, a
        elif b == n: a, b, c = c, a, b
        if c == n:
            return v[li[a, b]] if a < b else -v[li[b, a]]
        return O[a, b, c]
    def convex4(v, P):
        for a, b, c in combinations(P, 3):
            s = chi(v, a, b, c)
            for d in P:
                if d not in (a, b, c) and chi(v, a, b, d) == s and chi(v, b, c, d) == s and chi(v, c, a, d) == s:
                    return False
        return True
    import os
    unb = set()
    if os.environ.get('SATCHECK_UNB'):  # diagnostics: sign vectors of the 2L unbounded cells (far points in direction u)
        import math
        dirs = []
        for (a, b) in lines:
            dx, dy = pts[b][0] - pts[a][0], pts[b][1] - pts[a][1]
            dirs += [math.atan2(dy, dx), math.atan2(-dy, -dx)]
        dirs.sort()
        for k in range(len(dirs)):
            th = (dirs[k] + (dirs[(k + 1) % len(dirs)] + (2 * math.pi if k + 1 == len(dirs) else 0))) / 2
            u = (Fraction(math.cos(th)), Fraction(math.sin(th)))
            unb.add(tuple(sg((pts[b][0] - pts[a][0]) * u[1] - (pts[b][1] - pts[a][1]) * u[0]) for (a, b) in lines))
        print(f"unbounded_cells={len(unb)} (expected 2L={2 * L})")
    fails = 0
    for v in cells:
        ok = False
        for P in polys:
            m = len(P)
            if sum(1 for e in range(m) if chi(v, P[e], P[(e + 1) % m], n) < 0) == 1 and convex4(v, P + [n]):
                ok = True; break
        fails += not ok
        if not ok and unb:
            print("  failing cell unbounded" if v in unb else "  failing cell bounded")
    print(f"cells={len(cells)} fail={fails}")
    print("VERDICT SATURATED" if fails == 0 else f"VERDICT NOT_SATURATED fails={fails}")


main()
