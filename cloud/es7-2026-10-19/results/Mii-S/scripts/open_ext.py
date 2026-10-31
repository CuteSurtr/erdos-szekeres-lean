#!/usr/bin/env python3
"""Certifiable hybrid CNF for one C2 open cube o:
  G_o = F + units(o) + { -e_c v l : l in cube(c) } for the 450 hull cases c + ( e_1 v .. v e_450 )
with fresh variables e_c = nv + 1 + index(c).  If F & o had a model nu, extending it by
e_c := [nu satisfies cube(c)] satisfies G_o, because the certified hull cover (cover.py) gives
some c with nu |= cube(c).  So UNSAT of G_o (checked by cake_lpr) refutes F & o.
  open_ext.py CNF OPEN_CUBE_LITS(comma-separated) OUT.cnf"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import hullsplit as H
cnf, ocs, out = sys.argv[1:4]; o = [int(x) for x in ocs.split(",")]
nv, nc, body = H.read_cnf(cnf); cs = H.cases(); cl = [f"{l} 0\n" for l in o]
for n, (U, L) in enumerate(cs):
    e = nv + 1 + n; cl += [f"{-e} {l} 0\n" for l in H.cube(U, L)]
cl.append(" ".join(str(nv + 1 + n) for n in range(len(cs))) + " 0\n")
with open(out, "w") as f:
    f.write(f"p cnf {nv + len(cs)} {nc + len(cl)}\n"); f.writelines(body); f.writelines(cl)
