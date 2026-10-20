#!/usr/bin/env python3
"""C3a: compact CNF for n = 3m points in general position, invariant under a rotation R by 120
degrees about a centre c not in the set, with no k points in convex position.

Model (see README.md for the derivation; identities re-checked by check_identities.py):
  Coordinates are rotated so that a line l through c avoiding S is the y-axis, and S is
  mapped by phi(x, y) = (y/x, 1/x) to S'.  Points are labelled 0..n-1 by increasing X' = y/x.
  Then R(i) = (i - m) mod n on labels.

Variables
  C[t]    chi'(t) = orientation of S' on sorted label triples (true = +), one variable per
          R-orbit: chi'(Ri,Rj,Rk) = chi'(i,j,k) eps_i eps_j eps_k, eps_i = +1 iff i < m.
  s[r]    sigma (x < 0) of label r < m; sigma_{r+m} = not s[r], sigma_{r+2m} = s[r].
  inv     inv_ij (i < j): Y'_i > Y'_j.
  B       B_ij (i < j): i is left of j in S;  B_ij = inv_ij xor sigma_i xor sigma_j.
  T[t]    chi_S(t) (true = ccw) per R-orbit;  T = C xor sigma_i xor sigma_j xor sigma_k.
  Y[x,b,c]   c is right of x and (x,b,c) is ccw:  Y <- B(x,c) and ccw_S(x,b,c).
  W[r][x,a,b] there is a chain x | p1..pr (pr-1 = a, pr = b) of points right of x, angularly
          increasing about x, with left turns at p2..p(r-1).  (2 <= r <= k-2)
Clauses
  sig     signotope axioms on chi' (3-term monotonicity on every 4-set)
  sb      sigma_0 = 0 (point reflection p -> -p, which keeps labels and the class)
  prefix  inversion pattern of a triple is a prefix of (ij,ik,jk) if chi'+, of (jk,ik,ij) if chi'-
  forced  sigma_i = 0, sigma_j = 1 -> inv_ij;  sigma_i = 1, sigma_j = 0 -> not inv_ij
  xorB, xorT  the parity definitions above
  Y, W    one-directional (upward) chain definitions
  gon     no chain of k-1 points: W[k-2] and Y and left turn -> false   (written last)
Soundness: a chain x | p1..p(k-1) with all p right of x, consecutive ccw about x (so angles
increase inside the open right half-plane, total span < 180 degrees) and left turns at
p1..p(k-1)'s interior is a convex k-gon; conversely every convex k-gon gives such a chain
from its leftmost vertex.
"""
import argparse
import itertools
import json


def parity_sort(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return tuple(sorted(t)), (-1 if inv & 1 else 1)


class C3Enc:
    def __init__(self, m, k, sb=True):
        self.m, self.k, self.n = m, k, 3 * m
        self.nv = 0
        self.sections = []  # (name, first clause index, count)
        self.clauses = []
        self.sb = sb
        n = self.n
        self.R = [(i - m) % n for i in range(n)]
        self.eps = [1 if i < m else -1 for i in range(n)]
        trip = list(itertools.combinations(range(n), 3))
        # chi' orbit variables
        self.C = self._orbits(trip, lambda t, Rt: self.eps[t[0]] * self.eps[t[1]] * self.eps[t[2]])
        self.nC = self.nv
        self.s = [self.new() for _ in range(m)]
        self.inv = {p: self.new() for p in itertools.combinations(range(n), 2)}
        self.Bv = {p: self.new() for p in itertools.combinations(range(n), 2)}
        self.T = self._orbits(trip, lambda t, Rt: 1)

    def new(self):
        self.nv += 1
        return self.nv

    def _orbits(self, trip, factor):
        """literal map for sorted triples, one fresh variable per R-orbit.
        rule: value(sorted(R t)) = parity(R t) * factor(t) * value(t)."""
        lit = {}
        for t in trip:
            if t in lit:
                continue
            v = self.new()
            lit[t] = v
            cur, cl = t, v
            for _ in range(3):
                Rt = tuple(self.R[i] for i in cur)
                st, par = parity_sort(Rt)
                nl = par * factor(cur, Rt) * cl
                if st in lit:
                    assert lit[st] == nl, ("inconsistent orbit", t, st)
                else:
                    lit[st] = nl
                cur, cl = st, nl
        return lit

    # literals
    def sig(self, i):
        r, w = i % self.m, i // self.m
        return -self.s[r] if w == 1 else self.s[r]

    def Clit(self, t):
        return self.C[t]

    def B(self, p, q):
        return self.Bv[(p, q)] if p < q else -self.Bv[(q, p)]

    def ccw(self, p, q, r):
        st, par = parity_sort((p, q, r))
        return par * self.T[st]

    def add(self, cl):
        s = set()
        for l in cl:
            if -l in s:
                return
            s.add(l)
        self.clauses.append(sorted(s, key=abs))

    def xor0(self, lits):
        """clauses for XOR(lits) = false (even number true)."""
        cnt = {}
        const = 0
        for l in lits:
            if l < 0:
                const ^= 1
            cnt[abs(l)] = cnt.get(abs(l), 0) ^ 1
        vs = [v for v, c in cnt.items() if c]
        # XOR(vs) = const
        for bits in itertools.product((0, 1), repeat=len(vs)):
            if sum(bits) % 2 != const:  # forbidden assignment
                self.add([(-v if b else v) for v, b in zip(vs, bits)])
        if not vs and const:
            self.clauses.append([])

    def section(self, name, start):
        self.sections.append((name, start, len(self.clauses) - start))

    def build(self):
        n, m, k = self.n, self.m, self.k
        cl = self.clauses
        st = len(cl)
        seen = set()
        for i, j, kk, l in itertools.combinations(range(n), 4):
            s = [self.C[(i, j, kk)], self.C[(i, j, l)], self.C[(i, kk, l)], self.C[(j, kk, l)]]
            for p, q, r in itertools.combinations(range(4), 3):
                for c in ([-s[p], s[q], -s[r]], [s[p], -s[q], s[r]]):
                    key = tuple(sorted(c))
                    if key not in seen:
                        seen.add(key)
                        self.add(c)
        self.section("sig", st)
        st = len(cl)
        if self.sb:
            self.add([-self.sig(0)])
        self.section("sb", st)
        st = len(cl)
        for i, j, kk in itertools.combinations(range(n), 3):
            c = self.C[(i, j, kk)]
            a, b, d = self.inv[(i, j)], self.inv[(i, kk)], self.inv[(j, kk)]
            self.add([-c, -b, a])
            self.add([-c, -d, b])
            self.add([c, -b, d])
            self.add([c, -a, b])
        self.section("prefix", st)
        st = len(cl)
        for i, j in itertools.combinations(range(n), 2):
            si, sj, v = self.sig(i), self.sig(j), self.inv[(i, j)]
            self.add([si, -sj, v])
            self.add([-si, sj, -v])
        self.section("forced", st)
        st = len(cl)
        for i, j in itertools.combinations(range(n), 2):
            self.xor0([self.Bv[(i, j)], self.inv[(i, j)], self.sig(i), self.sig(j)])
        self.section("xorB", st)
        st = len(cl)
        done = set()
        for t, tl in self.T.items():
            if abs(tl) in done:
                continue
            done.add(abs(tl))
            self.xor0([tl, self.C[t], self.sig(t[0]), self.sig(t[1]), self.sig(t[2])])
        self.section("xorT", st)
        # chain
        st = len(cl)
        self.Y = {}
        for x in range(n):
            for b, c in itertools.permutations([q for q in range(n) if q != x], 2):
                v = self.new()
                self.Y[(x, b, c)] = v
                self.add([-self.B(x, c), -self.ccw(x, b, c), v])
        self.section("Y", st)
        st = len(cl)
        self.W = {}
        for r in range(2, k - 1):
            for x in range(n):
                for a, b in itertools.permutations([q for q in range(n) if q != x], 2):
                    self.W[(r, x, a, b)] = self.new()
        for x in range(n):
            for a, b in itertools.permutations([q for q in range(n) if q != x], 2):
                self.add([-self.B(x, a), -self.Y[(x, a, b)], self.W[(2, x, a, b)]])
        gon = []
        for r in range(2, k - 1):
            for x in range(n):
                others = [q for q in range(n) if q != x]
                for a, b in itertools.permutations(others, 2):
                    w = self.W[(r, x, a, b)]
                    for c in others:
                        if c == a or c == b:
                            continue
                        body = [-w, -self.Y[(x, b, c)], -self.ccw(a, b, c)]
                        if r + 1 <= k - 2:
                            self.add(body + [self.W[(r + 1, x, b, c)]])
                        else:
                            gon.append(body)
        self.section("W", st)
        st = len(cl)
        for g in gon:
            self.add(g)
        self.section("gon", st)

    def write(self, path, mappath=None):
        with open(path, "w") as f:
            f.write(f"p cnf {self.nv} {len(self.clauses)}\n")
            for c in self.clauses:
                f.write(" ".join(map(str, c)) + " 0\n")
        info = {"m": self.m, "k": self.k, "n": self.n, "vars": self.nv, "clauses": len(self.clauses),
                "C_vars": self.nC, "sections": self.sections, "sb": self.sb}
        if mappath:
            mp = dict(info)
            mp["C"] = [[*t, l] for t, l in sorted(self.C.items())]
            mp["T"] = [[*t, l] for t, l in sorted(self.T.items())]
            mp["s"] = self.s
            mp["inv"] = [[*p, v] for p, v in sorted(self.inv.items())]
            mp["B"] = [[*p, v] for p, v in sorted(self.Bv.items())]
            with open(mappath, "w") as f:
                json.dump(mp, f)
        return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("k", type=int)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--map")
    ap.add_argument("--no-sb", action="store_true")
    a = ap.parse_args()
    e = C3Enc(a.m, a.k, sb=not a.no_sb)
    e.build()
    print(json.dumps(e.write(a.out, a.map)))


if __name__ == "__main__":
    main()
