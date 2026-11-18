#!/usr/bin/env python3
"""CNF: n points sorted by x, signotope axioms, no (maxcap+1)-cap, no
(maxcup+1)-cup, no convex octagon.  Sound relaxation of real point sets.

Octagon with leftmost s, rightmost t = a-cap s..t (above) + b-cup s..t (below),
a+b = 10, 2<=a<=maxcap, 2<=b<=maxcup (a=2 or b=2 is an 8-cup / 8-cap, already
excluded when maxcup, maxcap < 8).  Chains from s are tracked by their last pair:
  SU_b(s,j,k): a b-cup starts at s and ends with (j,k)   (3 <= b <= maxcup)
  SC_b(s,j,k): a b-cap starts at s and ends with (j,k)   (3 <= b <= maxcap)
UNSAT at n proves N(8; cap<=maxcap, cup<=maxcup) <= n-1 for real points.
"""
import itertools, sys

def build(n, maxcap, maxcup, out, gon=8):
    nv = 0
    def new():
        nonlocal nv
        nv += 1
        return nv
    O = {t: new() for t in itertools.combinations(range(n), 3)}
    SU = {b: {t: new() for t in itertools.combinations(range(n), 3)} for b in range(3, maxcup + 1)}
    SC = {b: {t: new() for t in itertools.combinations(range(n), 3)} for b in range(3, maxcap + 1)}
    pairs = list(itertools.combinations(range(n), 2))
    U = {b: {p: new() for p in pairs} for b in range(3, maxcup + 1)}
    K = {a: {p: new() for p in pairs} for a in range(3, maxcap + 1)}
    cl = []
    for i, j, k, l in itertools.combinations(range(n), 4):
        seq = [O[(i, j, k)], O[(i, j, l)], O[(i, k, l)], O[(j, k, l)]]
        for a, b, c in itertools.combinations(range(4), 3):
            x, y, z = seq[a], seq[b], seq[c]
            cl.append((-x, y, -z)); cl.append((x, -y, z))
    for s, j, k in itertools.combinations(range(n), 3):
        cl.append((-O[(s, j, k)], SU[3][(s, j, k)]))
        cl.append((O[(s, j, k)], SC[3][(s, j, k)]))
    for s, i, j, k in itertools.combinations(range(n), 4):
        o = O[(i, j, k)]
        for b in range(4, maxcup + 1):
            cl.append((-SU[b - 1][(s, i, j)], -o, SU[b][(s, j, k)]))
        cl.append((-SU[maxcup][(s, i, j)], -o))          # no (maxcup+1)-cup
        for a in range(4, maxcap + 1):
            cl.append((-SC[a - 1][(s, i, j)], o, SC[a][(s, j, k)]))
        cl.append((-SC[maxcap][(s, i, j)], o))           # no (maxcap+1)-cap
    for s, j, t in itertools.combinations(range(n), 3):
        for b in range(3, maxcup + 1):
            cl.append((-SU[b][(s, j, t)], U[b][(s, t)]))
        for a in range(3, maxcap + 1):
            cl.append((-SC[a][(s, j, t)], K[a][(s, t)]))
    for p in pairs:
        for a in range(3, maxcap + 1):
            b = gon + 2 - a
            if 3 <= b <= maxcup:
                cl.append((-K[a][p], -U[b][p]))
    with open(out, 'w') as f:
        f.write(f'p cnf {nv} {len(cl)}\n')
        for c in cl:
            f.write(' '.join(map(str, c)) + ' 0\n')
    return nv, len(cl)

if __name__ == '__main__':
    n, mc, mu = map(int, sys.argv[1:4])
    gon = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    print(build(n, mc, mu, sys.argv[4], gon))
