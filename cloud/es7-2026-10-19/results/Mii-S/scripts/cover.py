#!/usr/bin/env python3
"""SAT-certified cover of sub-case (ii) by the 450 hull-pair cases (hullsplit.py).

Obligations (each is "this CNF is UNSAT", to be checked with cake_lpr):
  root      F + { -UP(U) : U in UPS }                     i.e. F |= OR_U UP(U)
  up:U      F + UP(U) units + { -cube(U,L) : (U,L) a case }  i.e. F & UP(U) |= OR_L cube(U,L)
where F = m33k7int.sub.cnf, UPS = all U subsets of 2..16 with |U| <= 2 (121 chains), and
UP(U) = upper-chain edge literals: for consecutive vertices v -> q of 1, u1, .., u_k, 34-u_k
(the right half of the chain is the mirror image and has the same orbit literals), every
other point r is strictly below line vq: orient(v,q,r) < 0.  The leaves are the case CNFs
F + cube(U,L).  Since cube(U,L) contains UP(U), the cover argument is: a model of F satisfies
some UP(U) (root), then some cube(U,L) (up:U), contradicting UNSAT of that case CNF.
Usage: cover.py list | cover.py cnf CNF OBLIGATION OUT.cnf
"""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hullsplit as H
UPS = [()] + [(a,) for a in range(2, 17)] + list(itertools.combinations(range(2, 17), 2))

def up(U):
    pts = [1] + list(U); lits = set()
    for v, q in zip(pts, pts[1:] + [34 - pts[-1]]):
        lits |= {-H.ccw_lit(v, q, r) for r in range(1, 34) if r not in (v, q)}
    return sorted(lits, key=abs)

def obligations():
    return ["root"] + ["up:" + ",".join(map(str, U)) for U in UPS]

def build(ob):
    """(units, blocking cubes) of an obligation."""
    if ob == "root": return [], [up(U) for U in UPS]
    U = tuple(int(x) for x in ob[3:].split(",") if x)
    return up(U), [H.cube(U2, L) for U2, L in H.cases() if U2 == U]

if __name__ == "__main__":
    if sys.argv[1] == "list":
        for o in obligations(): print(o)
    else:
        nv, nc, body = H.read_cnf(sys.argv[2]); units, blocks = build(sys.argv[3])
        cl = [f"{l} 0\n" for l in units] + [" ".join(str(-l) for l in c) + " 0\n" for c in blocks]
        with open(sys.argv[4], "w") as f:
            f.write(f"p cnf {nv} {nc + len(cl)}\n"); f.writelines(body); f.writelines(cl)
