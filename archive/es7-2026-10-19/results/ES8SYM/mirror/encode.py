#!/usr/bin/env python3
"""Independent CNF encoder (written from scratch, 2026-11-01).

Question encoded:  n points p_0,...,p_{n-1} in the plane, sorted by strictly increasing
x-coordinate, no three collinear, such that
   (a) there is no 4-cap, and
   (b) no K points are in convex position (K = 8 for the claim).

Variables
  O(a,b,c), a<b<c : true  <=>  orient(p_a,p_b,p_c) > 0  (left turn; p_b lies BELOW the line p_a p_c;
                    a "cup triple").  false <=> right turn (p_b above the line; a "cap triple").
  E(k,a,c,d)      : k = 3..K-1, a < c < d, c >= a+k-2 :
                    "there is a k-cup whose first point is a and whose last two points are c,d".
                    Only the implication  (k-cup exists) => E  is encoded (one-directional), which is
                    all the soundness argument needs.

Clauses
  (SIG)  signotope axioms: for a<b<c<d the sign sequence O(abc),O(abd),O(acd),O(bcd) has at most
         one sign change; encoded as: no 3 of the 4 entries (in this order) read +,-,+ or -,+,-.
  (CAP4) no 4-cap:          O(a,b,c) or O(b,c,d)                        for a<b<c<d
  (E3)   O(a,b,c) -> E(3,a,b,c)
  (EK)   E(k-1,a,b,c) & O(b,c,d) -> E(k,a,c,d)                          for 4<=k<=K-1
  (CUPK) no K-cup:          not( E(K-1,a,b,c) & O(b,c,d) )
  (OCT)  no (K-1)-cup a..c,d together with a point p, a<p<d, above the chord a d:
                            E(K-1,a,c,d) -> O(a,p,d)                    for every a<p<d
  Modes:  "full"   = all of the above
          "cupcap" = without (OCT)  (only "no 4-cap and no K-cup"; Erdos-Szekeres says the
                     maximum is C(K,K-2)=C(K,2) points; used as a sanity check)
Optional symmetry breaking: none (soundness then needs no extra argument).

Usage: encode.py n K out.cnf [full|cupcap]
Writes out.cnf and out.cnf.vars (JSON map of the O-variables, for decoding models).
"""
import sys, itertools, json


def build(n, K, mode="full"):
    var = {}
    nv = 0
    for a, b, c in itertools.combinations(range(n), 3):
        nv += 1
        var[("O", a, b, c)] = nv
    for k in range(3, K):
        for a in range(n):
            for c in range(a + k - 2, n):
                for d in range(c + 1, n):
                    nv += 1
                    var[("E", k, a, c, d)] = nv

    def O(a, b, c):
        return var[("O", a, b, c)]

    def E(k, a, c, d):
        return var.get(("E", k, a, c, d))

    cls = []
    # (SIG)
    for a, b, c, d in itertools.combinations(range(n), 4):
        t = [O(a, b, c), O(a, b, d), O(a, c, d), O(b, c, d)]
        for i, j, k in itertools.combinations(range(4), 3):
            cls.append((-t[i], t[j], -t[k]))
            cls.append((t[i], -t[j], t[k]))
    # (CAP4)
    for a, b, c, d in itertools.combinations(range(n), 4):
        cls.append((O(a, b, c), O(b, c, d)))
    # (E3)
    for a, b, c in itertools.combinations(range(n), 3):
        cls.append((-O(a, b, c), E(3, a, b, c)))
    # (EK)
    for k in range(4, K):
        for a, b, c, d in itertools.combinations(range(n), 4):
            e_prev = E(k - 1, a, b, c)
            e_new = E(k, a, c, d)
            if e_prev is None:
                continue
            assert e_new is not None
            cls.append((-e_prev, -O(b, c, d), e_new))
    # (CUPK)
    for a, b, c, d in itertools.combinations(range(n), 4):
        e = E(K - 1, a, b, c)
        if e is not None:
            cls.append((-e, -O(b, c, d)))
    # (OCT)
    if mode == "full":
        for a, c, d in itertools.combinations(range(n), 3):
            e = E(K - 1, a, c, d)
            if e is None:
                continue
            for p in range(a + 1, d):
                cls.append((-e, O(a, p, d)))
    elif mode != "cupcap":
        raise SystemExit("unknown mode " + mode)
    return nv, cls, var


def main():
    n = int(sys.argv[1])
    K = int(sys.argv[2])
    out = sys.argv[3]
    mode = sys.argv[4] if len(sys.argv) > 4 else "full"
    nv, cls, var = build(n, K, mode)
    with open(out, "w") as f:
        f.write("c mirror46_indep encoder: n=%d K=%d mode=%s (no 4-cap, no K points in convex position)\n" % (n, K, mode))
        f.write("p cnf %d %d\n" % (nv, len(cls)))
        for c in cls:
            f.write(" ".join(map(str, c)) + " 0\n")
    omap = {"%d,%d,%d" % (k[1], k[2], k[3]): v for k, v in var.items() if k[0] == "O"}
    with open(out + ".vars", "w") as f:
        json.dump({"n": n, "K": K, "mode": mode, "O": omap}, f)
    print("n=%d K=%d mode=%s vars=%d clauses=%d -> %s" % (n, K, mode, nv, len(cls), out))


if __name__ == "__main__":
    main()
