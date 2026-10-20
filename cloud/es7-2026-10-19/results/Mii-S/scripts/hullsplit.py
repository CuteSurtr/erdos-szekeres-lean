#!/usr/bin/env python3
"""Hull-pair split of sub-case (ii) (m33k7int.sub.cnf, N = 33, pairs i <-> 34-i, axis 17).

A case is (U, L): disjoint sets of pair labels a in 2..16 (pair a <-> 34-a) with
1 <= |U| + |L| <= 2.  U = pairs on the upper hull (above chord 1-33), L = pairs on the
lower hull.  Hull, counter-clockwise: lower chain 1, l1, l2, .., 34-l2, 34-l1, 33, then upper
chain 33, 34-u_max, .., 34-u1, u1, .., u_max, 1 reversed appropriately (see hull_ccw).

The cube of a case is the set of orbit-substituted literals
  (a) orient(h_t, h_t+1, r) = ccw for every hull edge and every other point r;
  (b) orient(p, q, s) = ccw for every ccw-ordered triple of hull vertices;
  (c) X(i, v, k) = false for every upper hull vertex v and i < v < k,
      X(i, v, k) = true  for every lower hull vertex v and i < v < k.
Usage: hullsplit.py cubes OUT.icnf OUT.json | cover CNF OUT.cnf  | case CNF U L OUT.cnf
"""
import itertools, json, sys
N = 33; M = N + 1
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}

def rep(v_triple):
    i, j, k = v_triple
    a = idx[(i, j, k)]; b = idx[tuple(sorted((M - k, M - j, M - i)))]
    return min(a, b)

def ccw_lit(p, q, r):
    """Literal (orbit-substituted) meaning orient(p,q,r) > 0."""
    t = (p, q, r); s = tuple(sorted(t))
    inv = sum(1 for x, y in itertools.combinations(t, 2) if x > y)
    v = rep(s)
    return v if inv % 2 == 0 else -v

def hull_ccw(U, L):
    U = sorted(U); L = sorted(L)
    lower = [1] + L + [M - a for a in reversed(L)] + [N]          # left to right
    upper = [1] + U + [M - a for a in reversed(U)] + [N]          # left to right
    return lower + list(reversed(upper))[1:-1]

def cases():
    P = range(2, 17)
    out = []
    for a in P:
        out.append(((a,), ()))
        out.append(((), (a,)))
    for a, b in itertools.combinations(P, 2):
        out.append(((a, b), ()))
        out.append(((), (a, b)))
    for a in P:
        for b in P:
            if a != b:
                out.append(((a,), (b,)))
    return out

def cube(U, L):
    H = hull_ccw(U, L); m = len(H); lits = set()
    for t in range(m):
        p, q = H[t], H[(t + 1) % m]
        for r in range(1, N + 1):
            if r not in (p, q):
                lits.add(ccw_lit(p, q, r))
    for x, y, z in itertools.combinations(range(m), 3):
        lits.add(ccw_lit(H[x], H[y], H[z]))
    upv = set(U) | {M - a for a in U}; lov = set(L) | {M - a for a in L}
    for v in upv | lov:
        for i in range(1, v):
            for k in range(v + 1, N + 1):
                l = rep((i, v, k))
                lits.add(-l if v in upv else l)
    assert not any(-l in lits for l in lits), (U, L)
    return sorted(lits, key=abs)

def name(U, L):
    return "U" + "-".join(map(str, U)) + "_L" + "-".join(map(str, L))

def read_cnf(path):
    with open(path) as f:
        hdr = None; body = []
        for line in f:
            if line.startswith('p'): hdr = line.split()
            elif line.startswith('c'): continue
            else: body.append(line)
    return int(hdr[2]), int(hdr[3]), body

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "cubes":
        meta = []
        with open(sys.argv[2], "w") as f:
            for U, L in cases():
                c = cube(U, L)
                f.write("a " + " ".join(map(str, c)) + " 0\n")
                meta.append({"case": name(U, L), "U": list(U), "L": list(L), "hull": hull_ccw(U, L), "nlits": len(c)})
        json.dump(meta, open(sys.argv[3], "w"))
        print(len(meta), "cases")
    elif cmd == "cover":
        nv, nc, body = read_cnf(sys.argv[2])
        cl = [" ".join(str(-l) for l in cube(U, L)) + " 0\n" for U, L in cases()]
        with open(sys.argv[3], "w") as f:
            f.write(f"p cnf {nv} {nc + len(cl)}\n"); f.writelines(body); f.writelines(cl)
    elif cmd == "case":
        nv, nc, body = read_cnf(sys.argv[2])
        U = tuple(int(x) for x in sys.argv[3].split(",") if x)
        L = tuple(int(x) for x in sys.argv[4].split(",") if x)
        c = cube(U, L)
        with open(sys.argv[5], "w") as f:
            f.write(f"p cnf {nv} {nc + len(c)}\n"); f.writelines(body)
            f.writelines(f"{l} 0\n" for l in c)
