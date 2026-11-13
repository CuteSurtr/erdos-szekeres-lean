#!/usr/bin/env python3
"""CNF: n points (sorted by x), signotope axioms, no 5-cap, no convex 8-gon.

Sound relaxation of real point sets in general position with distinct
x-coordinates: every real set with no 5-cap and no convex octagon gives a
satisfying assignment (each auxiliary variable set to its semantic value).
UNSAT at n therefore proves N(5-cap, 8-gon) <= n-1 for real points.

Variables
  o(i,j,k), i<j<k : orientation positive (cup triple).
  CE3(j,k), CE4(j,k): some cap of length >=3 / >=4 ends with pair (j,k).
  S_b(s,j,k), b=3..7: some cup of length b starts at s and ends with (j,k).
  C7(s,t), C6(s,t): some 7-/6-cup from s to t.  K3(s,t), K4(s,t): 3-/4-cap s..t.
Octagons in a 5-cap-free set: 8-cup, (3-cap,7-cup), (4-cap,6-cup) on common
endpoints (cap above, cup below the chord => convex position).
"""
import itertools, sys

def build(n, out, maxcap=4):
    nv = 0
    def new():
        nonlocal nv
        nv += 1
        return nv
    O = {}
    for t in itertools.combinations(range(n), 3):
        O[t] = new()
    CE3 = {}; CE4 = {}
    for p in itertools.combinations(range(n), 2):
        CE3[p] = new(); CE4[p] = new()
    S = {b: {} for b in range(3, 8)}
    for b in range(3, 8):
        for t in itertools.combinations(range(n), 3):
            S[b][t] = new()
    C7 = {}; C6 = {}; K3 = {}; K4 = {}
    for p in itertools.combinations(range(n), 2):
        C7[p] = new(); C6[p] = new(); K3[p] = new(); K4[p] = new()
    cl = []
    # signotope monotonicity on (ijk, ijl, ikl, jkl)
    for i, j, k, l in itertools.combinations(range(n), 4):
        seq = [O[(i, j, k)], O[(i, j, l)], O[(i, k, l)], O[(j, k, l)]]
        for a, b, c in itertools.combinations(range(4), 3):
            x, y, z = seq[a], seq[b], seq[c]
            cl.append((-x, y, -z))
            cl.append((x, -y, z))
    # caps ending with a pair
    for i, j, k in itertools.combinations(range(n), 3):
        o = O[(i, j, k)]
        cl.append((o, CE3[(j, k)]))                       # cap i,j,k
        if maxcap == 4:
            cl.append((-CE3[(i, j)], o, CE4[(j, k)]))     # extend 3-cap
            cl.append((-CE4[(i, j)], o))                  # no 5-cap
        else:
            cl.append((-CE3[(i, j)], o))                  # no 4-cap
    # cups starting at s
    for s, j, k in itertools.combinations(range(n), 3):
        cl.append((-O[(s, j, k)], S[3][(s, j, k)]))
    for s, i, j, k in itertools.combinations(range(n), 4):
        o = O[(i, j, k)]
        for b in range(4, 8):
            cl.append((-S[b - 1][(s, i, j)], -o, S[b][(s, j, k)]))
        cl.append((-S[7][(s, i, j)], -o))                 # no 8-cup
    for s, i, t in itertools.combinations(range(n), 3):
        cl.append((-S[7][(s, i, t)], C7[(s, t)]))
        cl.append((-S[6][(s, i, t)], C6[(s, t)]))
        cl.append((O[(s, i, t)], K3[(s, t)]))             # 3-cap s,i,t
    if maxcap == 4:
        for s, k, l, t in itertools.combinations(range(n), 4):
            cl.append((O[(s, k, l)], O[(k, l, t)], K4[(s, t)]))  # 4-cap s,k,l,t
    for p in itertools.combinations(range(n), 2):
        cl.append((-C7[p], -K3[p]))
        if maxcap == 4:
            cl.append((-C6[p], -K4[p]))
    with open(out, 'w') as f:
        f.write(f'p cnf {nv} {len(cl)}\n')
        for c in cl:
            f.write(' '.join(map(str, c)) + ' 0\n')
    return nv, len(cl)

if __name__ == '__main__':
    n = int(sys.argv[1])
    mc = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    print(build(n, sys.argv[2], mc))
