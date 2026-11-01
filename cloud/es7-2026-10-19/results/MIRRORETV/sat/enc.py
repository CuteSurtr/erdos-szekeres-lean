#!/usr/bin/env python3
"""
CNF for: n points (x-sorted, general position) with no 4-cap and no K points in convex position.
Written for mirrorM/theory (independent of mirror46_indep/encode.py and sat_rmax/enc_rmax.py).

Variables
  t(i,j,k), i<j<k        : true iff orient(p_i,p_j,p_k) > 0 (cup triple; p_j strictly below p_i p_k)
  B(l,i,j,e), 3<=l<=K-1, i<j<e : intended "some l-cup starts with p_i, p_j and ends at p_e"
Clauses
  (SIG)  for i<j<k<l, T = (t(ijk), t(ijl), t(ikl), t(jkl)), and each 3-subsequence (Tp,Tq,Tr):
         (-Tp | Tq | -Tr) and (Tp | -Tq | Tr)       [no + - + and no - + - ; THEORY/README proof]
  (CAP4) t(ijk) | t(jkl)                             [no 4-cap]
  (B3)   -t(i,j,e) | B(3,i,j,e)
  (BL)   -t(i,j,m) | -B(l-1,j,m,e) | B(l,i,j,e)      for 4<=l<=K-1, i<j<m<e
  (KCUP) -t(i,j,m) | -B(K-1,j,m,e)                   [no K-cup]
  (UP)   -B(K-1,i,j,e) | t(i,p,e)  for i<p<e         [no (K-1)-cup with a point above its chord]
Soundness (real sets): see README.md.  Optional: a points file gives unit clauses t = real orientation.
Usage: enc.py n K out.cnf [points.txt]
"""
import sys
from itertools import combinations


def main():
    n, K, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    pts = None
    if len(sys.argv) > 4:
        pts = []
        for line in open(sys.argv[4]):
            if line.startswith('#') or not line.strip():
                continue
            x, y = map(int, line.split())
            pts.append((x, y))
        pts.sort()
        assert len(pts) == n and len(set(p[0] for p in pts)) == n
    assert K >= 4
    var = {}

    def v(*key):
        if key not in var:
            var[key] = len(var) + 1
        return var[key]

    # allocate t first (stable numbering)
    for i, j, k in combinations(range(n), 3):
        v('t', i, j, k)
    cls = []

    def t(i, j, k):
        return v('t', i, j, k)

    for i, j, k, l in combinations(range(n), 4):
        T = [t(i, j, k), t(i, j, l), t(i, k, l), t(j, k, l)]
        for p, q, r in combinations(range(4), 3):
            cls.append([-T[p], T[q], -T[r]])
            cls.append([T[p], -T[q], T[r]])
        cls.append([t(i, j, k), t(j, k, l)])
    for i, j, e in combinations(range(n), 3):
        cls.append([-t(i, j, e), v('B', 3, i, j, e)])
    for L in range(4, K):
        for i, j, m, e in combinations(range(n), 4):
            cls.append([-t(i, j, m), -v('B', L - 1, j, m, e), v('B', L, i, j, e)])
    # K-cup: i followed by a (K-1)-cup starting with j, m (K-1 >= 3)
    for i, j, m, e in combinations(range(n), 4):
        cls.append([-t(i, j, m), -v('B', K - 1, j, m, e)])
    for i, j, e in combinations(range(n), 3):
        b = v('B', K - 1, i, j, e)
        for p in range(i + 1, e):
            cls.append([-b, t(i, p, e)])
    if pts is not None:
        def orient(a, b, c):
            return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
        for i, j, k in combinations(range(n), 3):
            o = orient(pts[i], pts[j], pts[k])
            assert o != 0
            cls.append([t(i, j, k)] if o > 0 else [-t(i, j, k)])
    with open(out, 'w') as f:
        f.write(f"p cnf {len(var)} {len(cls)}\n")
        for c in cls:
            f.write(" ".join(map(str, c)) + " 0\n")
    print(f"n={n} K={K} vars={len(var)} clauses={len(cls)} -> {out}")


if __name__ == '__main__':
    main()
