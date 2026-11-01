#!/usr/bin/env python3
"""Non-essential consistency spot check (not part of P8): for given point files, report gon, and for every hull
vertex v the largest v-cap of S\\{v} (via my phi map + exact cap DP), i.e. 1 + (largest convex polygon through v).
Also prints the binomial constants used in the claim."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from math import comb
import g

print("C(8,3) =", comb(8, 3), "| ETV sum_{i=0}^{3} C(5,i) =", sum(comb(5, i) for i in range(4)),
      "| Baek C(6,2)+2 =", comb(6, 2) + 2)
for f in sys.argv[1:]:
    S = [tuple(int(t) for t in line.split()) for line in open(f) if line.strip()]
    assert g.general_position(S)
    H = g.hull(S)
    caps = []
    for v in H:
        T = [p for p in S if p != v]
        Q = g.phi_map(T, v, g.separating_normal(T, v))
        caps.append(g.max_cap_xsorted(list(Q.values())))
    print(os.path.basename(f), "n =", len(S), "gon =", g.gon(S), "hull =", len(H),
          "max v-cap per hull vertex:", caps)
