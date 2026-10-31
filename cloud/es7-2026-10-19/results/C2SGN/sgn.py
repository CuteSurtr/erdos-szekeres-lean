#!/usr/bin/env python3
"""Signotope encoding of 'n points in general position, sorted by x, with no K points in convex position'.

Points are 1..n in increasing x-order. o(i,j,k) (i<j<k) is true iff the turn i -> j -> k is to the left
(det(p_j - p_i, p_k - p_i) > 0), i.e. j lies below the segment ik.
- Signotope axioms: for i<j<k<l the sequence o(ijk), o(ijl), o(ikl), o(jkl) changes sign at most once.
- No convex K-gon: a set is in convex position iff it is an s-cup and a t-cap with the same first and last point,
  s + t = K + 2 (a cup: consecutive triples turn left; a cap: right). U_k(a,j,l): a k-cup starts at a and ends with
  j, l; it is forced by U_{k-1}(a,i,j) and o(i,j,l). EU_k(a,b): some k-cup runs from a to b.
- --sym (central symmetry about a point c): p_{n+1-i} = -p_i, so o(n+1-k, n+1-j, n+1-i) = -o(i,j,k); the cap
  from a to b of size t is the image of a cup from n+1-b to n+1-a, so caps reuse the cup variables.
- --par (hull is a parallelogram): the x-direction is taken just off the outward normal of a hull edge, tilted
  towards the counter-clockwise later vertex of that edge. Then p_n and p_{n-1} are that edge's vertices (later,
  earlier), p_1 = -p_n, p_2 = -p_{n-1}, and the hull is p_{n-1} -> p_n -> p_2 -> p_1 counter-clockwise; every other
  point lies strictly left of each of these four edges.
- --hexk k (hexagonal hull): with the same choice of x-direction, the hull is p_{n-1} -> p_n -> p_k -> p_2 -> p_1 ->
  p_{n+1-k} counter-clockwise (p_k is the vertex after p_n); the hexagonal case is the union over k = 3..n-2.
- --centre: adds the centre c as an element between p_{n/2} and p_{n/2+1} with chi(c,p,q) = chi(-p,p,q), and the
  signotope axioms for every 4-set containing c and no antipodal pair.
usage: sgn.py n K [--sym] [--par] [--centre] [--units FILE] -o OUT.cnf [--map MAP.json]"""
import argparse, itertools, json


class Enc:
    def __init__(s, n, K, sym, centre):
        s.n, s.K, s.sym, s.centre = n, K, sym, centre
        s.nv = 0; s.cl = set(); s.ov = {}
        for t in itertools.combinations(range(1, n + 1), 3):
            c, _ = s.canon(t)
            if c not in s.ov:
                s.nv += 1; s.ov[c] = s.nv
        s.no = s.nv

    def canon(s, t):
        if not s.sym:
            return t, 1
        i, j, k = t; m = (s.n + 1 - k, s.n + 1 - j, s.n + 1 - i)
        assert m != t
        return (t, 1) if t < m else (m, -1)

    def o(s, i, j, k):
        c, sg = s.canon((i, j, k)); return sg * s.ov[c]

    def chi(s, a, b, c):
        """orientation literal of the ordered triple (a,b,c) of distinct points: true iff c is left of a -> b"""
        t = tuple(sorted((a, b, c))); inv = (a > b) + (a > c) + (b > c)
        l = s.o(*t); return l if inv % 2 == 0 else -l

    def new(s):
        s.nv += 1; return s.nv

    def add(s, c):
        c = tuple(sorted(set(c), key=abs))
        if any(-l in c for l in c):
            return
        s.cl.add(c)

    def mono(s, seq):
        for a, b, c in itertools.combinations(range(len(seq)), 3):
            s.add([-seq[a], seq[b], -seq[c]]); s.add([seq[a], -seq[b], seq[c]])

    def signotope(s):
        for i, j, k, l in itertools.combinations(range(1, s.n + 1), 4):
            s.mono([s.o(i, j, k), s.o(i, j, l), s.o(i, k, l), s.o(j, k, l)])

    def centre_axioms(s):
        n = s.n; h = n // 2; C = 0.5 + h     # position of c
        anti = lambda p: n + 1 - p
        def lit(x, y, z):                   # sorted triple that may contain C
            if C not in (x, y, z):
                return s.o(x, y, z)
            p, q = [v for v in (x, y, z) if v != C]
            # chi(c,p,q) = chi(-p,p,q); the sorted triple is a permutation of (c,p,q)
            base = s.chi(anti(p), p, q)
            perm = [v if v != C else -1 for v in (x, y, z)]     # c represented as -1 in (c,p,q) order
            ref = [-1, p, q]
            inv = sum(1 for a, b in itertools.combinations(range(3), 2) if ref.index(perm[a]) > ref.index(perm[b]))
            return base if inv % 2 == 0 else -base
        cnt = 0
        for T in itertools.combinations(range(1, n + 1), 3):
            if any(anti(a) in T for a in T):
                continue
            Q = sorted(list(T) + [C])
            seq = [lit(*t) for t in itertools.combinations(Q, 3)]
            s.mono(seq); cnt += 1
        return cnt

    def kgon(s):
        n, K = s.n, s.K
        U = {}
        for k in range(3, K + 1):
            for a, j, l in itertools.combinations(range(1, n + 1), 3):
                if j - a >= k - 2:
                    U[k, a, j, l] = s.new()
        for a, j, l in itertools.combinations(range(1, n + 1), 3):
            s.add([-s.o(a, j, l), U[3, a, j, l]])
        for k in range(4, K + 1):
            for a, i, j, l in itertools.combinations(range(1, n + 1), 4):
                if (k - 1, a, i, j) in U:
                    s.add([-U[k - 1, a, i, j], -s.o(i, j, l), U[k, a, j, l]])
        EU = {}
        for k in range(3, K + 1):
            for a, b in itertools.combinations(range(1, n + 1), 2):
                if b - a >= k - 1:
                    EU[k, a, b] = s.new()
                    for j in range(a + 1, b):
                        if (k, a, j, b) in U:
                            s.add([-U[k, a, j, b], EU[k, a, b]])
        if s.sym:
            EC = {(k, a, b): EU[k, n + 1 - b, n + 1 - a] for (k, a, b) in EU}
        else:
            V = {}
            for k in range(3, K + 1):
                for a, j, l in itertools.combinations(range(1, n + 1), 3):
                    if j - a >= k - 2:
                        V[k, a, j, l] = s.new()
            for a, j, l in itertools.combinations(range(1, n + 1), 3):
                s.add([s.o(a, j, l), V[3, a, j, l]])
            for k in range(4, K + 1):
                for a, i, j, l in itertools.combinations(range(1, n + 1), 4):
                    if (k - 1, a, i, j) in V:
                        s.add([-V[k - 1, a, i, j], s.o(i, j, l), V[k, a, j, l]])
            EC = {}
            for k in range(3, K + 1):
                for a, b in itertools.combinations(range(1, n + 1), 2):
                    if b - a >= k - 1:
                        EC[k, a, b] = s.new()
                        for j in range(a + 1, b):
                            if (k, a, j, b) in V:
                                s.add([-V[k, a, j, b], EC[k, a, b]])
        for a, b in itertools.combinations(range(1, n + 1), 2):
            for k in range(2, K + 1):
                t = K + 2 - k
                if not 2 <= t <= K:
                    continue
                c = []
                if k > 2:
                    if (k, a, b) not in EU: continue
                    c.append(-EU[k, a, b])
                if t > 2:
                    if (t, a, b) not in EC: continue
                    c.append(-EC[t, a, b])
                s.add(c)

    def rs_break(s):
        """--par only. With hull V1=p_{n-1} -> V2=p_n -> -V1=p_2 -> -V2=p_1, the diagonals split the inner pairs into
        the class of edge V1V2 (one point of the pair in triangle c V1 V2) and the class of edge V2(-V1). Choosing the
        edge pair whose class is larger gives r >= ceil(m/2) of the m inner pairs in the class of V1V2. Pair {p_i,
        p_{n+1-i}} (3 <= i <= n/2) is in that class iff chi(c,V1,p_i) = chi(c,p_i,V2), where chi(c,V1,q) =
        chi(-V1,V1,q) = chi(p_2,p_{n-1},q) and chi(c,q,V2) = -chi(-V2,V2,q) = -chi(p_1,p_n,q)."""
        n = s.n; m = n // 2 - 2; need = (m + 1) // 2
        ys = []
        for i in range(3, n // 2 + 1):
            a = s.chi(2, n - 1, i); b = -s.chi(1, n, i); y = s.new(); ys.append(y)
            s.add([-y, -a, b]); s.add([-y, a, -b]); s.add([y, a, b]); s.add([y, -a, -b])
        # at least `need` of ys: sequential counter R[j][c] = "at least c of ys[0..j]"
        R = {}
        for j, y in enumerate(ys):
            for c in range(1, need + 1):
                R[j, c] = s.new()
                prev_c = R.get((j - 1, c)); prev_c1 = R.get((j - 1, c - 1)) if c > 1 else None
                # R[j,c] -> R[j-1,c] or (y and (c == 1 or R[j-1,c-1]))
                if c == 1:
                    s.add([-R[j, c], y] + ([prev_c] if prev_c else []))
                else:
                    if prev_c1 is None:
                        s.add([-R[j, c]] + ([prev_c] if prev_c else []))
                    else:
                        s.add([-R[j, c], y] + ([prev_c] if prev_c else []))
                        s.add([-R[j, c], prev_c1] + ([prev_c] if prev_c else []))
        s.add([R[len(ys) - 1, need]])
        return {"inner_pairs": m, "at_least": need}

    def par_units(s, k=None):
        n = s.n; hull = [n - 1, n, 2, 1] if k is None else [n - 1, n, k, 2, 1, n + 1 - k]
        u = set()
        for e in range(len(hull)):
            a, b = hull[e], hull[(e + 1) % len(hull)]
            for x in range(1, n + 1):
                if x not in (a, b):
                    u.add(s.chi(a, b, x))
        assert not any(-l in u for l in u)
        for l in u:
            s.add([l])
        return len(u)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int); ap.add_argument("K", type=int)
    ap.add_argument("--sym", action="store_true"); ap.add_argument("--par", action="store_true")
    ap.add_argument("--centre", action="store_true"); ap.add_argument("--units")
    ap.add_argument("--rs", action="store_true", help="with --par: the chosen edge's class has at least half the inner pairs")
    ap.add_argument("--mirror", nargs=3, type=int, metavar=("I", "J", "K"),
                    help="with --par --rs and an odd number of inner pairs: o(I,J,K) false for an inner triple")
    ap.add_argument("--hexk", type=int, help="hexagonal hull p_{n-1} -> p_n -> p_k -> p_2 -> p_1 -> p_{n+1-k}")
    ap.add_argument("-o", required=True); ap.add_argument("--map")
    a = ap.parse_args()
    assert not a.centre or a.sym
    e = Enc(a.n, a.K, a.sym, a.centre)
    e.signotope()
    st = {}
    if a.centre:
        st["centre_4sets"] = e.centre_axioms()
    if a.par:
        st["par_units"] = e.par_units()
    if a.rs:
        assert a.par and a.sym
        st["rs"] = e.rs_break()
    if a.mirror:
        # Mirror reduction. With an odd number m of inner pairs the --rs edge pair is unique and mirror-invariant. For a
        # real set S, label S and its reflection R(S) in this normal form; up to a perturbation that keeps the order
        # type (so that no two inner points have the same distance to the chosen edge), the labelling of R(S) is that
        # of S with labels 1<->2 and n-1<->n swapped, so every triple of inner points (labels 3..n-2) has the opposite
        # orientation in R(S). Hence one of S, R(S) has o(I,J,K) false (mirrortest.py checks the relabelling).
        I, J, K = sorted(a.mirror); m = a.n // 2 - 2
        assert a.par and a.rs and m % 2 == 1 and 3 <= I and K <= a.n - 2
        e.add([-e.o(I, J, K)]); st["mirror_unit"] = [I, J, K]
    if a.hexk:
        assert a.sym and not a.par and 3 <= a.hexk <= a.n - 2
        st["hex_units"] = e.par_units(a.hexk)
    e.kgon()
    if a.units:
        for line in open(a.units):
            if line.strip():
                e.add([int(x) for x in line.split()])
    with open(a.o, "w") as f:
        f.write(f"c sgn n={a.n} K={a.K} sym={a.sym} par={a.par} centre={a.centre}\n")
        f.write(f"p cnf {e.nv} {len(e.cl)}\n")
        for c in sorted(e.cl, key=lambda c: (len(c), [abs(x) for x in c])):
            f.write(" ".join(map(str, c)) + " 0\n")
    if a.map:
        json.dump({"n": a.n, "K": a.K, "sym": a.sym, "o_vars": e.no,
                   "triples": [[*t, v] for t, v in e.ov.items()]}, open(a.map, "w"))
    print(json.dumps({"n": a.n, "K": a.K, "vars": e.nv, "o_vars": e.no, "clauses": len(e.cl), **st}))


if __name__ == "__main__":
    main()
