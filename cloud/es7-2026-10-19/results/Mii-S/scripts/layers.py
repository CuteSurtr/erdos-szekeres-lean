#!/usr/bin/env python3
"""Nested convex-layer split for sub-case (ii) (generalises hullsplit.py to two layers).

A layer is given by its leftmost label p (its mirror 34-p is the rightmost), its upper pairs U,
lower pairs L (labels < 17) and, for layers after the first, whether the axis point 17 is its
top vertex ('T'), bottom vertex ('B') or not a vertex ('-').  Layer t is the convex hull of
the points not in layers 1..t-1.  The cube of a layer sequence is the union over layers of
  (a) every remaining point r (not in earlier layers, not an endpoint) strictly left of
      every ccw edge of the layer;
  (b) every ccw-ordered triple of the layer's vertices is ccw;
  (c) every upper vertex v lies above every chord (i,k), i < v < k, of remaining points, and
      every lower vertex lies below.
(Layer 1 with p = 1 and no axis vertex is exactly hullsplit.py's case cube.)
Usage:
  layers.py sub2 U1 L1 OUT.icnf OUT.json     all layer-2 cases below the layer-1 case (U1, L1)
  layers.py next SPEC                        print the specs of all next-layer cases below SPEC
  layers.py case CNF SPEC OUT.cnf            SPEC = "U1/L1;U2/L2/A" e.g. "8/;5//T"
"""
import itertools, json, sys
N = 33; M = 34; AX = 17
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}

def rep(t):
    i, j, k = t
    return min(idx[(i, j, k)], idx[tuple(sorted((M - k, M - j, M - i)))])

def ccw_lit(p, q, r):
    t = (p, q, r); s = tuple(sorted(t))
    inv = sum(1 for x, y in itertools.combinations(t, 2) if x > y)
    v = rep(s); return v if inv % 2 == 0 else -v

def polygon(p, U, L, A):
    U = sorted(U); L = sorted(L)
    lower = [p] + L + (["AX"] if A == "B" else []) + [M - a for a in reversed(L)] + [M - p]
    upper = [p] + U + (["AX"] if A == "T" else []) + [M - a for a in reversed(U)] + [M - p]
    H = lower + list(reversed(upper))[1:-1]
    return [AX if v == "AX" else v for v in H]

def layer_lits(H, rem, upv, lov, lits):
    m = len(H)
    for t in range(m):
        p, q = H[t], H[(t + 1) % m]
        for r in rem:
            if r not in (p, q): lits.add(ccw_lit(p, q, r))
    for x, y, z in itertools.combinations(range(m), 3):
        lits.add(ccw_lit(H[x], H[y], H[z]))
    for v in upv | lov:
        for i in rem:
            for k in rem:
                if i < v < k:
                    l = rep((i, v, k)); lits.add(-l if v in upv else l)

def cube(layers):
    """layers: list of (U, L, A); layer 1 must have A == '-'."""
    rem = list(range(1, N + 1)); lits = set(); polys = []
    for U, L, A in layers:
        p = min(rem)
        H = polygon(p, U, L, A); polys.append(H)
        assert all(v in rem for v in H), (layers, H)
        upv = set(U) | {M - a for a in U} | ({AX} if A == "T" else set())
        lov = set(L) | {M - a for a in L} | ({AX} if A == "B" else set())
        layer_lits(H, rem, upv, lov, lits)
        rem = [r for r in rem if r not in H]
    assert not any(-l in lits for l in lits), layers
    return sorted(lits, key=abs), polys

def next_cases(prev):
    """All options (U, L, A) for the layer after the layers `prev` (a list of (U, L, A))."""
    rem = [r for r in range(1, N + 1) if r not in layer_points(prev)]
    p = min(rem); P = [a for a in rem if p < a < AX]
    axis_free = AX in rem
    out = []
    if axis_free:
        for A in "TB": out.append(((), (), A))
    for a in P:
        for A in ("-TB" if axis_free else "-"):
            out.append(((a,), (), A)); out.append(((), (a,), A))
    for a, b in itertools.combinations(P, 2):
        out.append(((a, b), (), "-")); out.append(((), (a, b), "-"))
    for a in P:
        for b in P:
            if a != b: out.append(((a,), (b,), "-"))
    return out

def layer_points(prev):
    rem = list(range(1, N + 1)); pts = set()
    for U, L, A in prev:
        H = polygon(min(rem), U, L, A); pts |= set(H); rem = [r for r in rem if r not in H]
    return pts

def sub_cases(U1, L1):
    """All second-layer (U2, L2, A) given layer 1 = (U1, L1, '-')."""
    return next_cases([(tuple(U1), tuple(L1), "-")])

def parse(spec):
    out = []
    for n, part in enumerate(spec.split(";")):
        f = part.split("/") + ["-"]
        U = tuple(int(x) for x in f[0].split(",") if x); L = tuple(int(x) for x in f[1].split(",") if x)
        out.append((U, L, f[2] if n else "-"))
    return out

def spec(layers):
    return ";".join(",".join(map(str, U)) + "/" + ",".join(map(str, L)) + ("/" + A if n else "")
                    for n, (U, L, A) in enumerate(layers))

def read_cnf(path):
    hdr = None; body = []
    for line in open(path):
        if line.startswith('p'): hdr = line.split()
        elif not line.startswith('c'): body.append(line)
    return int(hdr[2]), int(hdr[3]), body

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "sub2":
        U1 = tuple(int(x) for x in sys.argv[2].split(",") if x); L1 = tuple(int(x) for x in sys.argv[3].split(",") if x)
        meta = []
        with open(sys.argv[4], "w") as f:
            for c2 in sub_cases(U1, L1):
                ls = [(U1, L1, "-"), c2]; c, polys = cube(ls)
                f.write("a " + " ".join(map(str, c)) + " 0\n")
                meta.append({"spec": spec(ls), "polys": polys, "nlits": len(c)})
        json.dump(meta, open(sys.argv[5], "w")); print(len(meta), "sub-cases")
    elif cmd == "next":
        ls = parse(sys.argv[2])
        for c in next_cases(ls): print(spec(ls + [c]))
    elif cmd == "case":
        nv, nc, body = read_cnf(sys.argv[2]); c, _ = cube(parse(sys.argv[3]))
        with open(sys.argv[4], "w") as f:
            f.write(f"p cnf {nv} {nc + len(c)}\n"); f.writelines(body); f.writelines(f"{l} 0\n" for l in c)
