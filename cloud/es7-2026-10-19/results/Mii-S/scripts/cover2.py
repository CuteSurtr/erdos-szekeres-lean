#!/usr/bin/env python3
"""SAT-certified cover of a layers.py node by its next-layer children (generalises cover.py,
whose root and up:U obligations are the case PARENT = "" here).

For a parent spec P (layers already fixed; "" = nothing fixed), R = points not in P's layers,
p = min R.  An upper option is (U, T): the next layer's upper chain is p, U..., then either
the axis point 17 (T = True, only if 17 in R and P != "") or directly 34 - u_last.
UPR(U, T) = for consecutive chain vertices v -> q (left half plus the crossing edge; the right
half is the mirror image and has the same orbit literals), orient(v,q,r) < 0 for r in R - {v,q}.
Obligations:
  P|up        F + cube(P) + { -UPR(o) : o upper option }
  P|up:U:T    F + cube(P) + UPR(U,T) + { -cube(P + child) : child of P whose upper part is (U,T) }
Usage: cover2.py list PARENT | cover2.py cnf CNF OBLIGATION OUT.cnf
"""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layers as LY
AX = 17

def ctx(parent):
    prev = LY.parse(parent) if parent else []
    R = [r for r in range(1, 34) if r not in LY.layer_points(prev)]
    return prev, R

def upr(R, U, T):
    p = min(R); pts = [p] + list(U) + ([AX] if T else [])
    end = [] if T else [34 - pts[-1]]
    lits = set()
    for v, q in zip(pts, pts[1:] + end):
        lits |= {-LY.ccw_lit(v, q, r) for r in R if r not in (v, q)}
    return sorted(lits, key=abs)

def kids(prev):
    return LY.next_cases(prev) if prev else [(U, L, "-") for U, L in __import__("hullsplit").cases()]

def options(prev):
    seen = []
    for U, L, A in kids(prev):
        o = (tuple(U), A == "T")
        if o not in seen: seen.append(o)
    return seen

def build(ob):
    parent, rest = ob.split("|")
    prev, R = ctx(parent)
    base = LY.cube(prev)[0] if prev else []
    if rest == "up":
        return base, [upr(R, U, T) for U, T in options(prev)]
    _, u, t = rest.split(":"); U = tuple(int(x) for x in u.split(",") if x); T = t == "T"
    ch = [c for c in kids(prev) if tuple(c[0]) == U and (c[2] == "T") == T]
    return sorted(set(base) | set(upr(R, U, T)), key=abs), [LY.cube(prev + [c])[0] for c in ch]

def obligations(parent):
    prev, R = ctx(parent)
    return [parent + "|up"] + [parent + "|up:" + ",".join(map(str, U)) + ":" + ("T" if T else "-")
                               for U, T in options(prev)]

if __name__ == "__main__":
    if sys.argv[1] == "list":
        for o in obligations(sys.argv[2] if len(sys.argv) > 2 else ""): print(o)
    else:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        nv, nc, body = LY.read_cnf(sys.argv[2]); units, blocks = build(sys.argv[3])
        cl = [f"{l} 0\n" for l in units] + [" ".join(str(-l) for l in c) + " 0\n" for c in blocks]
        with open(sys.argv[4], "w") as f:
            f.write(f"p cnf {nv} {nc + len(cl)}\n"); f.writelines(body); f.writelines(cl)
