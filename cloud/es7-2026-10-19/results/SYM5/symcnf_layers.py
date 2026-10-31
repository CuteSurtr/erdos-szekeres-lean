#!/usr/bin/env python3
"""Variant of symcnf.py for m >= 4 with t >= 2 orbits and no centre in the set (N = m t), using the convex-layer
normal form instead of sorting the orbits by angle (odd m: auxiliary centre as in symcnf.py; even m: no centre).

Fact (m >= 4, K <= 2m): in a set S with an m-fold rotation and no K points in convex position, every convex layer is
exactly one orbit. The vertex set of conv(S) is invariant under the rotation, so it is a union of orbits; two orbits
would give 2m >= K points in convex position. Removing the hull orbit leaves a smaller m-fold set, so by induction
the orbits are nested: O_0 is the hull of S, O_1 the hull of S minus O_0, and so on, and every point of O_o' with
o' > o lies strictly inside conv(O_o) (general position).

Normal form: orbit o is the o-th layer (outermost first); (0,0) is any point of O_0; for o >= 1 the representative
(o,0) is the point of O_o in the open sector (0, 2 pi/m) from the ray to (0,0) at the centre (as in symcnf.py).
(o,r) = R^r (o,0) with R the counter-clockwise rotation, so O_o is the convex polygon (o,0),(o,1),...,(o,m-1) in
counter-clockwise order and p is inside it iff chi((o,j),(o,j+1),p) = + for every j. By the symmetry
chi((o,j),(o,j+1),p) = chi((o,0),(o,1),R^-j p), so the unit clauses below cover every edge.
Units added (replacing the angle-order clauses of symcnf.py; the sector clauses are kept):
  chi((o,0),(o,1),(o,k)) = +   for 2 <= k < m       (O_o is a convex polygon in counter-clockwise order)
  chi((o,0),(o,1),c) = +                             (the centre is inside O_o)
  chi((o,0),(o,1),(o',r)) = +  for o < o', all r     (O_o' is inside conv(O_o))
"""
import argparse, json, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symcnf import SymEncoding


class LayerEncoding(SymEncoding):
    def add_sb(self):
        m, t, c = self.m, self.t, self.c
        assert not self.center_in_set and t >= 2 and 4 <= m and self.K <= 2 * m
        sb = []
        if m % 2 == 1:
            assert self.has_center
            for o in range(1, t):
                sb.append([self.lit(c, self.pt(0, 0), self.pt(o, 0))])
                sb.append([-self.lit(c, self.pt(0, 1), self.pt(o, 0))])
        else:
            # even m: no centre in the chirotope; the sector clauses of symcnf.py (diameters of orbit 0)
            h = m // 2
            qx, qy = math.cos(math.pi / m), math.sin(math.pi / m)
            for j in range(h):
                ax, ay = math.cos(2 * math.pi * j / m), math.sin(2 * math.pi * j / m)
                d = (-ax - ax) * (qy - ay) - (-ay - ay) * (qx - ax)
                s = 1 if d > 0 else -1
                for o in range(1, t):
                    sb.append([s * self.lit(self.pt(0, j), self.pt(0, j + h), self.pt(o, 0))])
        for o in range(t):
            e0, e1 = self.pt(o, 0), self.pt(o, 1)
            for k in range(2, m):
                sb.append([self.lit(e0, e1, self.pt(o, k))])
            if c is not None:
                sb.append([self.lit(e0, e1, c)])
            for o2 in range(o + 1, t):
                for r in range(m):
                    sb.append([self.lit(e0, e1, self.pt(o2, r))])
        self.clauses.extend(sb)
        self.stats["sb_clauses"] = len(sb)
        self.stats["normal_form"] = "layers"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int)
    ap.add_argument("K", type=int)
    ap.add_argument("m", type=int)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--map")
    a = ap.parse_args()
    enc = LayerEncoding(a.N, a.K, a.m, body=a.out + ".body")
    enc.build()
    info = enc.write(a.out, a.map)
    info.pop("triples", None)
    print(json.dumps(info))


if __name__ == "__main__":
    main()
