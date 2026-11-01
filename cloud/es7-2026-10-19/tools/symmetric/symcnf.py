#!/usr/bin/env python3
"""CNF for: N points in the plane with an m-fold rotational symmetry and no K points in
convex position (abstract chirotope / CC-system model, Knuth-style axioms).

Points and symmetry
  The rotation R by 2*pi/m (counter-clockwise) about a centre c acts on the point set.
  Orbit o (0 <= o < t) consists of the points (o,0), (o,1)=R(o,0), ..., (o,m-1); point
  (o,r) has index o*m + r.  pi(i) is the index permutation induced by R.
  The centre may be
    * absent      (even m: the centre is collinear with antipodal pairs, so it cannot be a
                   point of a general-position set and is not used),
    * an auxiliary point (odd m, N = m*t): it is added to the chirotope as index m*t but is
                   excluded from the "no convex K-gon" constraints,
    * a member of the set (odd m, N = m*t + 1, --center-in-set): it is a point of the set.

Variables
  chi(a,b,c) = orientation sign of the ordered triple; antisymmetric under odd permutations
  (built in: one variable per *orbit* of unordered triples under pi, with the sign bookkeeping
  chi(pi a, pi b, pi c) = chi(a,b,c), which holds for every rotation since det R = +1).
  Auxiliary: conv_r(S) for r-subsets S (4 <= r <= K-1) of the set points; conv_r(S) is
  implied by "S is in convex position" (upward only); one variable per pi-orbit of subsets.

Clauses (all sound for real point sets in general position, see README)
  A4  interiority (Knuth axiom 4, = acyclicity on 4 points): for every 4-set and every
      choice of t in it and sign s:  chi(tqr)=chi(ptr)=chi(pqt)=s  ->  chi(pqr)=s.   8 clauses
  GP  3-term Grassmann-Pluecker relations for every 5-set {x,y1..y4} and special element x:
      the three products chi(x y1 y2)chi(x y3 y4), -chi(x y1 y3)chi(x y2 y4),
      chi(x y1 y4)chi(x y2 y3) are not all positive and not all negative.   80 clauses
      (A4 + GP = all 5-point restrictions are realizable; models are exactly the CC systems /
      acyclic uniform rank-3 oriented matroids with the symmetry.)
  C   centre facts (odd m, centre present): chi(c, a, pi^k a) = + for k < m/2, - for k > m/2.
  K   no convex K-gon via the 4-point criterion (a set is in convex position iff no point is
      inside the triangle of three others, iff every 4-subset is in convex position):
        conv_4(T)  <- [T is one of the 6 labelled convex 4-patterns]
        conv_r(S)  <- AND_{x in S} conv_{r-1}(S minus x)       (5 <= r <= K-1)
        for every K-set S: OR_{x in S} NOT conv_{K-1}(S minus x)
      (--kgon direct instead writes, for every K-set, OR over its 4-subsets of NOT conv_4.)
  SB  labelling normal form (sound: every realizable symmetric set has such a labelling):
      orbit 0 and its point (0,0) are arbitrary;  for o >= 1 the representative (o,0) is the
      unique point of orbit o in the open angular sector (0, 2*pi/m) measured at the centre
      from the ray to (0,0); orbits 1..t-1 are sorted by angle.
        odd m  (centre c present): chi(c,(0,0),(o,0)) = +, chi(c,(0,1),(o,0)) = -  (sector)
                                   chi(c,(o,0),(o',0)) = + for 1 <= o < o'       (order)
        even m (no centre): the sector is cut out by the m/2 diameters (0,j)(0,j+m/2); the sign
               pattern of a point in the sector is read off a regular m-gon; the order uses the
               angular order about (0,0): chi((0,0),(o,0),(o',0)) = + for 1 <= o < o'
               (all representatives lie in the open half-plane above the line through (0,0)
               and the centre, in which the angular order about (0,0) is total).
      The reflection symmetry (mirror image) is NOT broken.
"""
import argparse
import itertools
import json
import math
import sys


def parity_sort(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return (tuple(sorted(t)), -1 if inv & 1 else 1)


def convex4_patterns():
    """The labelled sign patterns (chi(abc),chi(abd),chi(acd),chi(bcd)) of 4 points a<b<c<d in
    convex position, the one-inside patterns, and the cyclic (non-acyclic) patterns."""
    convex, inside, cyclic = [], [], []
    for pat in itertools.product((1, -1), repeat=4):
        base = {(0, 1, 2): pat[0], (0, 1, 3): pat[1], (0, 2, 3): pat[2], (1, 2, 3): pat[3]}

        def O(x, y, z):
            s, sg = parity_sort((x, y, z))
            return sg * base[s]

        def ins(d, a, b, c):
            return O(a, b, d) == O(b, c, d) == O(c, a, d)

        n_in = sum(ins(d, *[q for q in range(4) if q != d]) for d in range(4))
        if n_in == 0:
            convex.append(pat)
        elif n_in == 1:
            inside.append(pat)
        else:
            cyclic.append(pat)
    assert len(convex) == 6 and len(inside) == 8 and len(cyclic) == 2, (convex, inside, cyclic)
    return convex, inside, cyclic


class ClauseSink:
    """Writes clauses to a body file as they are produced (keeps memory flat for ~10^7 clauses)."""

    def __init__(self, path):
        self.f = open(path, "w") if path else None
        self.n = 0
        self.mem = [] if path is None else None

    def append(self, cl):
        self.n += 1
        if self.f:
            self.f.write(" ".join(map(str, cl)) + " 0\n")
        else:
            self.mem.append(cl)

    def extend(self, cls):
        for cl in cls:
            self.append(cl)

    def __len__(self):
        return self.n

    def close(self):
        if self.f:
            self.f.close()


class SymEncoding:
    def __init__(self, N, K, m, center_in_set=False, sb=True, kgon="layered", center=None, body=None):
        self.N, self.K, self.m = N, K, m
        self.center_in_set = center_in_set
        if center_in_set:
            assert m % 2 == 1 and (N - 1) % m == 0, "centre in set needs odd m and N = m t + 1"
            self.t = (N - 1) // m
            self.has_center = True
        else:
            assert N % m == 0, "N must be a multiple of m"
            self.t = N // m
            if center is None:
                center = (m % 2 == 1)
            if center:
                assert m % 2 == 1, "an auxiliary centre is only in general position for odd m"
            self.has_center = center
        self.norb = self.t * m                      # orbit points 0..norb-1
        self.c = self.norb if self.has_center else None
        self.P = self.norb + (1 if self.has_center else 0)   # all chirotope points
        # set points (those subject to the K-gon constraint)
        self.setpts = list(range(self.norb)) + ([self.c] if center_in_set else [])
        assert len(self.setpts) == N
        self.sb = sb
        self.kgon = kgon
        self.PI = [[self.pi(i, k) for i in range(self.P)] for k in range(m)]
        self.nv = 0
        self.clauses = ClauseSink(body)
        self.tv = {}
        self._triples()
        self.nX = self.nv

    # ---- symmetry
    def pi(self, i, k=1):
        if i == self.c:
            return i
        o, r = divmod(i, self.m)
        return o * self.m + (r + k) % self.m

    def pt(self, o, r):
        return o * self.m + r

    def canon(self, S):
        """lexicographically least image of the sorted tuple S under the powers of pi"""
        best = S
        for k in range(1, self.m):
            P = self.PI[k]
            T = tuple(sorted(P[x] for x in S))
            if T < best:
                best = T
        return best

    def new(self):
        self.nv += 1
        return self.nv

    def _triples(self):
        for T in itertools.combinations(range(self.P), 3):
            if T in self.tv:
                continue
            v = self.new()
            seen = {}
            for k in range(self.m):
                P = self.PI[k]
                S, s = parity_sort((P[T[0]], P[T[1]], P[T[2]]))
                # chi(pi^k T) = chi(T) = v ; chi(pi^k T) = s * chi(S)  =>  chi(S) = s * v
                if S in seen:
                    assert seen[S] == s, ("inconsistent triple orbit", T, S)
                else:
                    seen[S] = s
            for S, s in seen.items():
                self.tv[S] = (v, s)

    def lit(self, a, b, c):
        """literal that is true iff chi(a,b,c) = +1"""
        S, s = parity_sort((a, b, c))
        v, sg = self.tv[S]
        return s * sg * v

    # ---- axioms
    def add_axioms(self):
        n4 = n5 = 0
        for S in itertools.combinations(range(self.P), 4):
            if self.canon(S) != S:
                continue
            n4 += 1
            for t in S:
                p, q, r = [x for x in S if x != t]
                for s in (1, -1):
                    self.clauses.append([-s * self.lit(t, q, r), -s * self.lit(p, t, r),
                                         -s * self.lit(p, q, t), s * self.lit(p, q, r)])
        for S in itertools.combinations(range(self.P), 5):
            if self.canon(S) != S:
                continue
            n5 += 1
            for x in S:
                y1, y2, y3, y4 = [y for y in S if y != x]
                l12, l34 = self.lit(x, y1, y2), self.lit(x, y3, y4)
                l13, l24 = self.lit(x, y1, y3), self.lit(x, y2, y4)
                l14, l23 = self.lit(x, y1, y4), self.lit(x, y2, y3)
                for s1, s2, s3 in itertools.product((1, -1), repeat=3):
                    # all three terms positive: chi12=chi34=s1, chi13=s2, chi24=-s2, chi14=chi23=s3
                    self.clauses.append([-s1 * l12, -s1 * l34, -s2 * l13, s2 * l24, -s3 * l14, -s3 * l23])
                    # all three terms negative: chi12=s1, chi34=-s1, chi13=chi24=s2, chi14=s3, chi23=-s3
                    self.clauses.append([-s1 * l12, s1 * l34, -s2 * l13, -s2 * l24, -s3 * l14, s3 * l23])
        self.stats = {"orbits4": n4, "orbits5": n5}

    def add_center_facts(self):
        if not self.has_center:
            return
        c, m = self.c, self.m
        units = set()
        for a in range(self.norb):
            for k in range(1, m):
                sgn = 1 if 2 * k < m else -1
                units.add(sgn * self.lit(c, a, self.pi(a, k)))
        for u in sorted(units):
            self.clauses.append([u])
        self.stats["center_units"] = len(units)

    # ---- no convex K-gon
    def add_kgon(self):
        K = self.K
        pts = self.setpts
        convex, _, _ = convex4_patterns()
        self.convvar = {}
        # conv_4
        for S in itertools.combinations(pts, 4):
            if self.canon(S) != S:
                continue
            v = self.new()
            self.convvar[S] = v
            a, b, c, d = S
            lits = [self.lit(a, b, c), self.lit(a, b, d), self.lit(a, c, d), self.lit(b, c, d)]
            for pat in convex:
                self.clauses.append([-pat[i] * lits[i] for i in range(4)] + [v])
        n_conv = {4: len(self.convvar)}
        if self.kgon == "direct":
            cnt = 0
            for S in itertools.combinations(pts, K):
                if self.canon(S) != S:
                    continue
                cnt += 1
                self.clauses.append([-self.convvar[self.canon(T)] for T in itertools.combinations(S, 4)])
            n_conv["K-sets"] = cnt
        else:
            for r in range(5, K):
                cnt = 0
                for S in itertools.combinations(pts, r):
                    if self.canon(S) != S:
                        continue
                    v = self.new()
                    self.convvar[S] = v
                    cnt += 1
                    cl = [-self.convvar[self.canon(S[:i] + S[i + 1:])] for i in range(r)]
                    cl.append(v)
                    self.clauses.append(cl)
                n_conv[r] = cnt
            cnt = 0
            for S in itertools.combinations(pts, K):
                if self.canon(S) != S:
                    continue
                cnt += 1
                self.clauses.append([-self.convvar[self.canon(S[:i] + S[i + 1:])] for i in range(K)])
            n_conv["K-sets"] = cnt
        self.stats["conv_orbits"] = n_conv

    # ---- symmetry breaking (labelling normal form)
    def add_sb(self):
        if not self.sb or self.t < 2:
            self.stats["sb_clauses"] = 0
            return
        m, t = self.m, self.t
        sb = []
        if m % 2 == 1:
            assert self.has_center
            c = self.c
            for o in range(1, t):
                sb.append([self.lit(c, self.pt(0, 0), self.pt(o, 0))])
                sb.append([-self.lit(c, self.pt(0, 1), self.pt(o, 0))])
            for o in range(1, t):
                for o2 in range(o + 1, t):
                    sb.append([self.lit(c, self.pt(o, 0), self.pt(o2, 0))])
        else:
            # diameters (0,j),(0,j+m/2); sign pattern of a point at angle pi/m (mid-sector)
            h = m // 2
            qx, qy = math.cos(math.pi / m), math.sin(math.pi / m)
            pattern = []
            for j in range(h):
                ax, ay = math.cos(2 * math.pi * j / m), math.sin(2 * math.pi * j / m)
                bx, by = -ax, -ay
                d = (bx - ax) * (qy - ay) - (by - ay) * (qx - ax)
                assert abs(d) > 1e-9
                pattern.append(1 if d > 0 else -1)
            for o in range(1, t):
                for j in range(h):
                    sb.append([pattern[j] * self.lit(self.pt(0, j), self.pt(0, j + h), self.pt(o, 0))])
            for o in range(1, t):
                for o2 in range(o + 1, t):
                    sb.append([self.lit(self.pt(0, 0), self.pt(o, 0), self.pt(o2, 0))])
            self.stats["sector_pattern"] = pattern
        self.clauses.extend(sb)
        self.stats["sb_clauses"] = len(sb)

    def build(self):
        self.add_axioms()
        self.add_center_facts()
        self.add_kgon()
        self.add_sb()

    def write(self, path, mappath=None):
        self.clauses.close()
        with open(path, "w") as f:
            f.write(f"c symmetric chirotope CNF N={self.N} K={self.K} m={self.m} center={'set' if self.center_in_set else ('aux' if self.has_center else 'none')} sb={self.sb} kgon={self.kgon}\n")
            f.write(f"c triple-orbit variables 1..{self.nX}; see map file\n")
            f.write(f"p cnf {self.nv} {len(self.clauses)}\n")
            if self.clauses.mem is not None:
                for cl in self.clauses.mem:
                    f.write(" ".join(map(str, cl)) + " 0\n")
            else:
                with open(self.clauses.f.name) as b:
                    import shutil
                    shutil.copyfileobj(b, f)
                import os
                os.remove(self.clauses.f.name)
        info = {"N": self.N, "K": self.K, "m": self.m, "t": self.t, "P": self.P,
                "center": ("set" if self.center_in_set else ("aux" if self.has_center else "none")),
                "center_index": self.c, "setpts": self.setpts, "vars": self.nv, "X_vars": self.nX,
                "clauses": len(self.clauses), "sb": self.sb, "kgon": self.kgon, "stats": self.stats}
        if mappath:
            info["triples"] = [[a, b, c, v, s] for (a, b, c), (v, s) in sorted(self.tv.items())]
            with open(mappath, "w") as f:
                json.dump(info, f)
        return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int)
    ap.add_argument("K", type=int)
    ap.add_argument("m", type=int)
    ap.add_argument("--center-in-set", action="store_true")
    ap.add_argument("--no-center", action="store_true", help="odd m: do not add the auxiliary centre (disables sb)")
    ap.add_argument("--no-sb", action="store_true")
    ap.add_argument("--kgon", choices=["layered", "direct"], default="layered")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--map", help="write JSON map (triple variables) here")
    args = ap.parse_args()
    center = None
    sb = not args.no_sb
    if args.no_center:
        center = False
        if args.m % 2 == 1:
            sb = False
    enc = SymEncoding(args.N, args.K, args.m, center_in_set=args.center_in_set, sb=sb,
                      kgon=args.kgon, center=center, body=args.out + ".body")
    enc.build()
    info = enc.write(args.out, args.map)
    info.pop("triples", None)
    print(json.dumps(info))


if __name__ == "__main__":
    main()
