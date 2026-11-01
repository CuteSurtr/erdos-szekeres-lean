#!/usr/bin/env python3
"""C3b encoder: n = 3m points with 3-fold rotational symmetry (centre not in the set), no
convex k-gon.  Independent of symcnf.py / C3a.

Model (see README for the derivation; identities checked exactly by identities.py):
  Take the centre c to the origin, a line l through c avoiding S to the y-axis, and map
  phi(x,y) = (y/x, 1/x).  Labels 0..n-1 by increasing y/x (= increasing X' of phi(S)).
  Then R(i) = (i - m) mod n, and with s_i = [x_i < 0], e_i = +1 (i < m), -1 (i >= m):
    chi_S(ijk) = chi'(ijk) (-1)^(s_i+s_j+s_k)      chi' = orientation of phi(S)
    chi'(Ri,Rj,Rk) = chi'(ijk) e_i e_j e_k           s_{Ri} = s_i XOR [i >= m]
    i<j: i precedes j in x-order of S  iff  inv_ij XOR s_i XOR s_j,  inv_ij = [Y'_i > Y'_j]

Variables
  X  chi'(T): one variable per R-orbit of triples (sign bookkeeping with e and parity)
  Y  chi_S(T): one variable per R-orbit of triples (chi_S is R-invariant)
  s  s_0..s_{m-1}  (s_{r+m} = NOT s_r, s_{r+2m} = s_r);  unit NOT s_0 (point reflection)
  I  inv_ij, i<j
  O  o_ij = [i precedes j in the x-order of S], i<j
  C  C^l_p(q,r), 2 <= l <= k-2: there is a chain q_1..q_l = ..., q, r of points to the right
     of p (x-order of S), increasing in slope order about p (chi_S(p,q_t,q_t+1)=+), with
     left turns chi_S(q_t,q_t+1,q_t+2)=+   (upward implications only)

Clauses
  SIG  chi' is a signotope: for a<b<c<d, (abc,abd,acd,bcd) has at most one sign change
  ACY  chi_S is acyclic on every 4-set (forbid the 2 totally cyclic patterns)
  XOR  Y = X xor s_i xor s_j xor s_k ;  O = I xor s_i xor s_j
  INV  per triple: inv prefix rule given chi';  opposite s force inv
  SB   NOT s_0
  KGON chain definitions and, for every apex p: no chain of k-1 points
       (p = the leftmost vertex of a convex k-gon in S; the others sorted by slope about p
        form exactly such a chain; conversely such a chain plus p is a convex k-gon)
usage: gen_c3b.py m k -o out.cnf [--map out.json]
"""
import argparse
import itertools
import json
import random


def parity_sort(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return tuple(sorted(t)), (-1 if inv & 1 else 1)


def four_point_patterns():
    """Classify sign patterns (abc,abd,acd,bcd) of 4 labelled points by sampling real point
    sets: returns (convex, nonconvex) sets of realizable patterns.  The 2 remaining patterns
    are the totally cyclic ones."""
    rng = random.Random(12345)
    conv, nonc = set(), set()
    det = lambda p, q, r: (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    while len(conv) + len(nonc) < 14:
        P = [(rng.randint(-50, 50), rng.randint(-50, 50)) for _ in range(4)]
        ds = {}
        ok = True
        for T in itertools.combinations(range(4), 3):
            d = det(*[P[t] for t in T])
            if d == 0:
                ok = False
            ds[T] = 1 if d > 0 else -1
        if not ok:
            continue
        pat = (ds[0, 1, 2], ds[0, 1, 3], ds[0, 2, 3], ds[1, 2, 3])
        inside = False
        for t in range(4):
            a, b, c = [x for x in range(4) if x != t]
            s1, s2, s3 = det(P[a], P[b], P[t]), det(P[b], P[c], P[t]), det(P[c], P[a], P[t])
            if (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0):
                inside = True
        (nonc if inside else conv).add(pat)
    assert len(conv) == 6 and len(nonc) == 8 and not (conv & nonc)
    allp = set(itertools.product((1, -1), repeat=4))
    cyc = allp - conv - nonc
    assert cyc == {(1, -1, 1, -1), (-1, 1, -1, 1)}, cyc
    return sorted(conv), sorted(nonc), sorted(cyc)


class Enc:
    def __init__(self, m, k, d3=False):
        self.m, self.k, self.d3 = m, k, d3
        self.n = n = 3 * m
        self.nv = 0
        self.groups = []          # (name, first clause index, count)
        self.cls = []
        self.R = [(i - m) % n for i in range(n)]
        self.e = [1 if i < m else -1 for i in range(n)]
        # triple orbits
        self.X, self.Y = {}, {}
        self.reps = []
        for T in itertools.combinations(range(n), 3):
            if T in self.X:
                continue
            v, w = self.new(), self.new()
            self.reps.append((T, v, w))
            cur, sx, sy = T, 1, 1          # chi'(cur ordered) = sx * v ; chi_S(cur) = sy * w
            for _ in range(3):
                S, p = parity_sort(cur)
                ent = (v, sx * p), (w, sy * p)
                if S in self.X:
                    assert self.X[S] == ent[0] and self.Y[S] == ent[1], ("orbit inconsistent", T, S)
                else:
                    self.X[S], self.Y[S] = ent
                # apply R: chi'(R cur) = chi'(cur) * e(cur)
                sx *= self.e[cur[0]] * self.e[cur[1]] * self.e[cur[2]]
                cur = tuple(self.R[x] for x in cur)
            assert cur == T and sx == 1 and sy == 1, ("orbit does not close", T)
        self.s = [self.new() for _ in range(m)]
        self.I, self.O = {}, {}
        for i in range(n):
            for j in range(i + 1, n):
                self.I[i, j] = self.new()
        for i in range(n):
            for j in range(i + 1, n):
                self.O[i, j] = self.new()
        self.nprim = self.nv

    def new(self):
        self.nv += 1
        return self.nv

    # literals (true = '+', i.e. counter-clockwise)
    def chip(self, a, b, c):
        S, p = parity_sort((a, b, c))
        v, sg = self.X[S]
        return p * sg * v

    def chis(self, a, b, c):
        S, p = parity_sort((a, b, c))
        v, sg = self.Y[S]
        return p * sg * v

    def sig(self, i):
        """(variable, flip): s_i = s_{i mod m} xor flip"""
        return self.s[i % self.m], (1 if i // self.m == 1 else 0)

    def right(self, p, q):
        """literal: q is to the right of p in the x-order of S"""
        return self.O[p, q] if p < q else -self.O[q, p]

    def add(self, cl):
        self.cls.append(cl)

    def group(self, name, fn):
        a = len(self.cls)
        fn()
        self.groups.append((name, a, len(self.cls) - a))

    def xor(self, lits, parity):
        """clauses for XOR(vars of lits) == parity; lits are positive vars (duplicates cancel)"""
        cnt = {}
        for v in lits:
            cnt[v] = cnt.get(v, 0) ^ 1
        vs = sorted(v for v, c in cnt.items() if c)
        for bits in itertools.product((0, 1), repeat=len(vs)):
            if sum(bits) % 2 != parity:
                # forbid this assignment
                self.add([(-v if b else v) for v, b in zip(vs, bits)])

    def build(self):
        n, m, k = self.n, self.m, self.k
        conv, nonc, cyc = four_point_patterns()
        self.patterns = {"convex": conv, "nonconvex": nonc, "cyclic": cyc}

        def sig_cl():
            seen = set()
            for a, b, c, d in itertools.combinations(range(n), 4):
                L = [self.chip(a, b, c), self.chip(a, b, d), self.chip(a, c, d), self.chip(b, c, d)]
                for x, y, z in itertools.combinations(range(4), 3):
                    for s in (1, -1):
                        cl = tuple(sorted((-s * L[x], s * L[y], -s * L[z])))
                        if cl not in seen:
                            seen.add(cl)
                            self.add(list(cl))

        def acy_cl():
            seen = set()
            for a, b, c, d in itertools.combinations(range(n), 4):
                L = [self.chis(a, b, c), self.chis(a, b, d), self.chis(a, c, d), self.chis(b, c, d)]
                for pat in cyc:
                    cl = tuple(sorted(-pat[t] * L[t] for t in range(4)))
                    if cl not in seen:
                        seen.add(cl)
                        self.add(list(cl))

        def xor_cl():
            for T, v, w in self.reps:
                lits, par = [v, w], 0
                for x in T:
                    sv, f = self.sig(x)
                    lits.append(sv)
                    par ^= f
                self.xor(lits, par)
            for (i, j), o in self.O.items():
                (si, fi), (sj, fj) = self.sig(i), self.sig(j)
                self.xor([o, self.I[i, j], si, sj], fi ^ fj)

        def inv_cl():
            I = self.I
            for i, j, kk in itertools.combinations(range(n), 3):
                x = self.chip(i, j, kk)
                a, b, c = I[i, j], I[i, kk], I[j, kk]
                # chi'=+ : prefix of (ij,ik,jk): ik->ij, jk->ik
                self.add([-x, -b, a])
                self.add([-x, -c, b])
                # chi'=- : prefix of (jk,ik,ij): ik->jk, ij->ik
                self.add([x, -b, c])
                self.add([x, -a, b])
            for i in range(n):
                for j in range(i + 1, n):
                    (si, fi), (sj, fj) = self.sig(i), self.sig(j)
                    li = -si if fi else si      # literal "s_i = 1"
                    lj = -sj if fj else sj
                    if li == lj:
                        continue                # s_i = s_j identically
                    if li == -lj:
                        # s_i != s_j identically: inv_ij = s_j  (s_i=0,s_j=1 -> 1; s_i=1,s_j=0 -> 0)
                        self.add([-lj, I[i, j]])
                        self.add([lj, -I[i, j]])
                        continue
                    self.add([li, -lj, I[i, j]])
                    self.add([-li, lj, -I[i, j]])

        def sb_cl():
            self.add([-self.s[0]])

        self.group("SIG", sig_cl)
        self.group("ACY", acy_cl)
        self.group("XOR", xor_cl)
        self.group("INV", inv_cl)
        self.group("SB", sb_cl)

        def d3_cl():
            # optional D3: a mirror M through c.  WLOG (choice of the gap containing l) the
            # point on M's axis has label (n-1)/2; then the gap containing l is M-invariant and
            # contains the perpendicular to the axis, so labels i -> n-1-i and s is preserved;
            # chi_S and chi' are reversed.  inv and o depend on the exact position of l in the
            # gap and get no mirror constraint.  Only for odd n (one point on the axis).
            assert n % 2 == 1
            M = lambda i: n - 1 - i
            for a, b, c in itertools.combinations(range(n), 3):
                for f in (self.chis, self.chip):
                    l1, l2 = f(M(a), M(b), M(c)), f(a, b, c)
                    assert l1 != l2
                    if l1 != -l2:
                        self.add([l1, l2])
                        self.add([-l1, -l2])
            for r in range(m):
                a, b = self.s[r], self.s[m - 1 - r]
                if a != b:
                    self.add([-a, b])
                    self.add([a, -b])
        if self.d3:
            self.group("D3", d3_cl)
        self.nonkgon = len(self.cls)
        # chain variables
        self.C = {}
        for l in range(2, k - 1):
            for p in range(n):
                for q in range(n):
                    for r in range(n):
                        if len({p, q, r}) == 3:
                            self.C[l, p, q, r] = self.new()

        def kgon_cl():
            C = self.C
            for p in range(n):
                others = [x for x in range(n) if x != p]
                for q in others:
                    for r in others:
                        if q != r:
                            self.add([-self.right(p, q), -self.right(p, r), -self.chis(p, q, r), C[2, p, q, r]])
                for l in range(2, k - 1):
                    for o in others:
                        for q in others:
                            if q == o:
                                continue
                            c0 = -C[l, p, o, q]
                            for r in others:
                                if r == o or r == q:
                                    continue
                                cl = [c0, -self.chis(o, q, r), -self.chis(p, q, r), -self.right(p, r)]
                                if l + 1 <= k - 2:
                                    cl.append(C[l + 1, p, q, r])
                                self.add(cl)

        self.group("KGON", kgon_cl)

    def write(self, path, mappath=None):
        with open(path, "w") as f:
            f.write(f"c C3b encoding m={self.m} n={self.n} k={self.k}\n")
            f.write(f"p cnf {self.nv} {len(self.cls)}\n")
            f.write("".join(" ".join(map(str, cl)) + " 0\n" for cl in self.cls))
        info = {"m": self.m, "n": self.n, "k": self.k, "d3": self.d3, "vars": self.nv, "clauses": len(self.cls),
                "primary_vars": self.nprim, "nonkgon_clauses": self.nonkgon,
                "groups": self.groups, "patterns": self.patterns}
        if mappath:
            full = dict(info)
            full["X"] = [[a, b, c, v, s] for (a, b, c), (v, s) in sorted(self.X.items())]
            full["Y"] = [[a, b, c, v, s] for (a, b, c), (v, s) in sorted(self.Y.items())]
            full["s"] = self.s
            full["I"] = [[i, j, v] for (i, j), v in sorted(self.I.items())]
            full["O"] = [[i, j, v] for (i, j), v in sorted(self.O.items())]
            with open(mappath, "w") as f:
                json.dump(full, f)
        return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("k", type=int)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--map")
    ap.add_argument("--d3", action="store_true", help="add a mirror symmetry (D3 class)")
    a = ap.parse_args()
    e = Enc(a.m, a.k, a.d3)
    e.build()
    print(json.dumps(e.write(a.out, a.map)))


if __name__ == "__main__":
    main()
