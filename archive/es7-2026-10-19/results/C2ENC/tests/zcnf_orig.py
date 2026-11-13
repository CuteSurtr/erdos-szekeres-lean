#!/usr/bin/env python3
"""CNF for N = m t points in the plane with no K points in convex position, symmetric under a group that contains an
involution tau pairing the points, with the "centre" Z of tau as an extra chirotope element (non-uniform model).

Kinds
  rot   : m-fold rotation R about c, m even (tau = R^(m/2), the half-turn). Point (o,r) = R^r (o,0), index o*m + r.
          Z = c, the common midpoint of all pairs {p, tau p}.
  mirror: reflection sigma in a line A (m = 2, tau = sigma), with t pairs and --axis b in {0, 1, 2} points on A (indices
          2t .. 2t+b-1, fixed by sigma; at most 2 by general position). Point (o,0) is the left point of pair o,
          (o,1) = sigma (o,0) the right one. Z = the point at infinity in the direction perpendicular to A (to the
          right), i.e. the vector (0, 1, 0) in homogeneous coordinates (1, x, y) when A is the y-axis.

Chirotope chi on the N points and Z (chi(a,b,c) = sign det(v_a, v_b, v_c), v = (1, x, y), + = counter-clockwise).
  Zero triples: exactly {Z, p, tau p} (general position of the N points: if Z, p, q were collinear with q != tau p,
  then so would be tau p and tau q, giving 3 collinear points of the set).
  Identities (every real configuration satisfies them):
    rot   : v_c = (v_p + v_(tau p))/2, so chi(c, p, q) = chi(tau p, p, q) for every p and q != p, tau p.
    mirror: v_Z = (v_(o,1) - v_(o,0)) / (x_(o,1) - x_(o,0)) with x_(o,1) > x_(o,0), so
            chi(Z, (o,0), q) = chi((o,1), (o,0), q) and chi(Z, (o,1), q) = chi((o,1), (o,0), q).
    group : rot: chi(R a, R b, R c) = chi(a, b, c) (R fixes c, det R = +1).
            mirror: chi(sigma a, sigma b, sigma c) = -chi(a, b, c) on triples of points, and
            chi(Z, sigma a, sigma b) = +chi(Z, a, b) (sigma negates v_Z and has det -1).
  Variables: one per class of nonzero triples under these identities (a union-find with signs; a class containing a
  triple and its negation would be a contradiction and is checked for).

Clauses (all valid for real configurations)
  GP  3-term Grassmann-Pluecker relations for every 5-set of the N+1 elements and every special element x: the three
      products are either all 0 or include both signs (zero triples handled exactly; clauses forbid each violating
      sign pattern of the distinct variables involved).
  A4  acyclicity on 4-element circuits (Knuth's interiority) for every 4-set without a zero triple (the vectors are
      acyclic: v_0 + eps v_1 is positive on all of them).
  K   no K points of the set in convex position, as in symcnf.py (4-point criterion, layered conv variables, one per
      orbit of point sets under the group; convex position is invariant under the group).
  SB  labelling normal form (sound: every symmetric set has such a labelling):
      rot   : (0,0) arbitrary; for o >= 1, (o,0) is the point of orbit o in the open sector (0, 2 pi/m) from the ray
              c -> (0,0); orbits 1..t-1 sorted by angle: chi(c,(0,0),(o,0)) = +, chi(c,(0,1),(o,0)) = - (m >= 4),
              chi(c,(o,0),(o',0)) = + for 1 <= o < o'. For m = 2 the sector is the open half-plane left of c -> (0,0).
      mirror: pairs numbered from top to bottom: chi(Z,(o,0),(o',0)) = sign(y_o - y_o') = + for o < o'; with two axis
              points, the upper one first.
"""
import argparse, itertools, json, sys


def parity_sort(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return (tuple(sorted(t)), -1 if inv & 1 else 1)


def convex4_patterns():
    convex = []
    for pat in itertools.product((1, -1), repeat=4):
        base = {(0, 1, 2): pat[0], (0, 1, 3): pat[1], (0, 2, 3): pat[2], (1, 2, 3): pat[3]}

        def O(x, y, z):
            s, sg = parity_sort((x, y, z))
            return sg * base[s]
        n_in = sum(O(a, b, d) == O(b, c, d) == O(c, a, d) for d in range(4) for a, b, c in
                   [tuple(q for q in range(4) if q != d)])
        if n_in == 0:
            convex.append(pat)
    assert len(convex) == 6
    return convex


class Sink:
    def __init__(self, path):
        self.f = open(path, "w")
        self.n = 0

    def add(self, cl):
        self.n += 1
        self.f.write(" ".join(map(str, cl)) + " 0\n")


class ZEncoding:
    def __init__(self, kind, t, K, m=2, body=None, axis=0):
        assert kind in ("rot", "mirror")
        if kind == "mirror":
            m = 2
        assert m % 2 == 0 and m >= 2
        assert axis == 0 or (kind == "mirror" and axis <= 2)
        self.kind, self.t, self.K, self.m, self.axis = kind, t, K, m, axis
        self.NP = t * m                       # points in pairs/orbits; axis points are NP .. NP+axis-1
        self.N = t * m + axis
        self.Z = self.N
        self.P = self.N + 1
        self.sink = Sink(body)
        self.stats = {}
        # group generator acting on elements; sign on point-triples and on Z-triples
        if kind == "rot":
            self.gen = [self.rot(i) for i in range(self.P)]
            self.gsign = (1, 1)
        else:
            self.gen = [self.flip(i) for i in range(self.P)]
            self.gsign = (-1, 1)
        self.G = [list(range(self.P))]
        g = self.gen
        while True:
            nxt = [g[x] for x in self.G[-1]]
            if nxt == self.G[0]:
                break
            self.G.append(nxt)
        self._uf()

    # ---- elements
    def pt(self, o, r):
        return o * self.m + r

    def rot(self, i):
        if i == self.Z:
            return i
        o, r = divmod(i, self.m)
        return o * self.m + (r + 1) % self.m

    def flip(self, i):
        if i >= self.NP:                      # axis points and Z are fixed
            return i
        o, r = divmod(i, 2)
        return o * 2 + (1 - r)

    def tau(self, i):
        o, r = divmod(i, self.m)
        return o * self.m + (r + self.m // 2) % self.m

    def is_zero(self, T):
        if self.Z not in T:
            return False
        a, b = [x for x in T if x != self.Z]
        return a < self.NP and b < self.NP and self.tau(a) == b

    # ---- union-find with signs over sorted nonzero triples
    def _find(self, x):
        s = 1
        root = x
        while self.par[root][0] != root:
            s *= self.par[root][1]
            root = self.par[root][0]
        # path compression
        y, sy = x, s
        while self.par[y][0] != root:
            nxt, sg = self.par[y]
            self.par[y] = (root, sy)
            sy *= sg
            y = nxt
        return root, s

    def _union(self, a, b, s):
        """record chi(a) = s * chi(b) for sorted triples a, b"""
        ra, sa = self._find(a)
        rb, sb = self._find(b)
        if ra == rb:
            if sa != s * sb:
                raise ValueError(f"contradictory identification {a} = {s} * {b}")
            return
        # chi(a) = sa chi(ra), chi(b) = sb chi(rb); chi(ra) = sa * s * sb * chi(rb)
        self.par[ra] = (rb, sa * s * sb)

    def _uf(self):
        P, Z = self.P, self.Z
        self.par = {}
        for T in itertools.combinations(range(P), 3):
            if not self.is_zero(T):
                self.par[T] = (T, 1)
        # group
        sP, sZ = self.gsign
        for T in list(self.par):
            img = tuple(self.gen[x] for x in T)
            S, s = parity_sort(img)
            mult = sZ if Z in T else sP
            # chi(img) = mult * chi(T), chi(img) = s * chi(S)  =>  chi(S) = s * mult * chi(T)
            self._union(S, T, s * mult)
        # centre identities
        for p in range(self.NP):
            tp = self.tau(p)
            if self.kind == "rot":
                sp = 1
                base = (tp, p)            # chi(Z,p,q) = chi(tau p, p, q)
            else:
                left = p if p % 2 == 0 else tp
                right = self.tau(left)
                base = (right, left)      # chi(Z,p,q) = chi(right, left, q) for both points of the pair
                sp = 1
            for q in range(self.N):
                if q in (p, tp):
                    continue
                S1, s1 = parity_sort((Z, p, q))
                S2, s2 = parity_sort((base[0], base[1], q))
                # chi(Z,p,q) = s1 chi(S1) ; chi(base,q) = s2 chi(S2) ; chi(Z,p,q) = sp chi(base,q)
                self._union(S1, S2, s1 * sp * s2)
        roots = {}
        self.tv = {}
        for T in self.par:
            r, s = self._find(T)
            if r not in roots:
                roots[r] = len(roots) + 1
            self.tv[T] = (roots[r], s)
        self.nv = len(roots)
        self.nX = self.nv
        self.stats["triple_classes"] = self.nv

    def lit(self, a, b, c):
        S, s = parity_sort((a, b, c))
        if S not in self.tv:
            return 0
        v, sg = self.tv[S]
        return s * sg * v

    def new(self):
        self.nv += 1
        return self.nv

    def canon(self, S):
        best = S
        for g in self.G[1:]:
            T = tuple(sorted(g[x] for x in S))
            if T < best:
                best = T
        return best

    # ---- clause helpers
    def forbid(self, assign):
        """assign: dict var -> bool (the forbidden assignment) -> clause"""
        self.sink.add([(-v if val else v) for v, val in sorted(assign.items())])

    def add_gp(self):
        cnt = 0
        for S in itertools.combinations(range(self.P), 5):
            if self.canon(S) != S:
                continue
            cnt += 1
            for x in S:
                y = [q for q in S if q != x]
                pairs = [((y[0], y[1]), (y[2], y[3]), 1), ((y[0], y[2]), (y[1], y[3]), -1), ((y[0], y[3]), (y[1], y[2]), 1)]
                terms = []      # each: (const sign, [lit, lit]) or None for zero
                for (a, b), (c, d), k in pairs:
                    l1, l2 = self.lit(x, a, b), self.lit(x, c, d)
                    terms.append(None if (l1 == 0 or l2 == 0) else (k, (l1, l2)))
                if all(tm is not None for tm in terms) and len({abs(l) for tm in terms for l in tm[1]}) == 6:
                    (_, (l12, l34)), (_, (l13, l24)), (_, (l14, l23)) = terms
                    for s1, s2, s3 in itertools.product((1, -1), repeat=3):
                        self.sink.add([-s1 * l12, -s1 * l34, -s2 * l13, s2 * l24, -s3 * l14, -s3 * l23])
                        self.sink.add([-s1 * l12, s1 * l34, -s2 * l13, -s2 * l24, -s3 * l14, s3 * l23])
                    continue
                nz = [tm for tm in terms if tm is not None]
                if not nz:
                    continue
                vars_ = sorted({abs(l) for tm in nz for l in tm[1]})
                for bits in itertools.product((True, False), repeat=len(vars_)):
                    val = dict(zip(vars_, bits))
                    sg = set()
                    for k, (l1, l2) in nz:
                        v1 = 1 if (val[abs(l1)] == (l1 > 0)) else -1
                        v2 = 1 if (val[abs(l2)] == (l2 > 0)) else -1
                        sg.add(k * v1 * v2)
                    if not (1 in sg and -1 in sg):
                        self.forbid(val)
        self.stats["gp_5sets"] = cnt

    def add_a4(self):
        cnt = 0
        for S in itertools.combinations(range(self.P), 4):
            if any(self.is_zero(T) for T in itertools.combinations(S, 3)):
                continue
            cnt += 1
            for t in S:
                p, q, r = [x for x in S if x != t]
                for s in (1, -1):
                    cl = [-s * self.lit(t, q, r), -s * self.lit(p, t, r), -s * self.lit(p, q, t), s * self.lit(p, q, r)]
                    if any(-l in cl for l in cl):
                        continue
                    self.sink.add(sorted(set(cl), key=abs))
        self.stats["a4_4sets"] = cnt

    def add_kgon(self):
        K = self.K
        pts = list(range(self.N))
        convex = convex4_patterns()
        self.conv = {}
        n = {}
        for S in itertools.combinations(pts, 4):
            if self.canon(S) != S:
                continue
            v = self.new()
            self.conv[S] = v
            a, b, c, d = S
            lits = [self.lit(a, b, c), self.lit(a, b, d), self.lit(a, c, d), self.lit(b, c, d)]
            for pat in convex:
                cl = [-pat[i] * lits[i] for i in range(4)]
                if any(-l in cl for l in cl):
                    continue
                self.sink.add(sorted(set(cl), key=abs) + [v])
        n[4] = len(self.conv)
        for r in range(5, K):
            cnt = 0
            for S in itertools.combinations(pts, r):
                if self.canon(S) != S:
                    continue
                v = self.new()
                self.conv[S] = v
                cnt += 1
                self.sink.add([-self.conv[self.canon(S[:i] + S[i + 1:])] for i in range(r)] + [v])
            n[r] = cnt
        cnt = 0
        for S in itertools.combinations(pts, K):
            if self.canon(S) != S:
                continue
            cnt += 1
            self.sink.add(sorted({-self.conv[self.canon(S[:i] + S[i + 1:])] for i in range(K)}, key=abs))
        n["K-sets"] = cnt
        self.stats["conv"] = n

    def add_centre_facts(self):
        """rot, m >= 4: R is the counter-clockwise rotation by 2 pi/m, so chi(c, p, R^k p) = + for 0 < k < m/2 and
        - for m/2 < k < m, for every point p (the same rotation for all orbits)."""
        u = set()
        if self.kind == "rot" and self.m >= 4:
            for p in range(self.N):
                q = p
                for k in range(1, self.m):
                    q = self.rot(q)
                    if 2 * k == self.m:
                        continue
                    u.add((1 if 2 * k < self.m else -1) * self.lit(self.Z, p, q))
        assert not any(-l in u for l in u)
        for l in sorted(u, key=abs):
            self.sink.add([l])
        self.stats["centre_units"] = len(u)

    def add_sb(self):
        m, t, Z = self.m, self.t, self.Z
        u = []
        if self.kind == "rot":
            for o in range(1, t):
                u.append(self.lit(Z, self.pt(0, 0), self.pt(o, 0)))
                if m >= 4:
                    u.append(-self.lit(Z, self.pt(0, 1), self.pt(o, 0)))
            for o in range(1, t):
                for o2 in range(o + 1, t):
                    u.append(self.lit(Z, self.pt(o, 0), self.pt(o2, 0)))
        else:
            for o in range(t):
                for o2 in range(o + 1, t):
                    u.append(self.lit(Z, self.pt(o, 0), self.pt(o2, 0)))
            if self.axis == 2:                # the two axis points, upper one first
                u.append(self.lit(Z, self.NP, self.NP + 1))
        units = sorted(set(u), key=abs)
        assert not any(-l in units for l in units), "contradictory SB units"
        for l in units:
            self.sink.add([l])
        self.stats["sb_units"] = len(units)

    def add_hull_sb(self):
        """rot: (0,0) may be chosen as a vertex of conv(S) (any point can be (0,0) in the normal form, and conv(S) has
        vertices): (0,0) is not inside any triangle of other points of the set."""
        q = self.pt(0, 0)
        cnt = 0
        for a, b, d in itertools.combinations([x for x in range(self.N) if x != q], 3):
            for s in (1, -1):
                cl = [-s * self.lit(a, b, q), -s * self.lit(b, d, q), -s * self.lit(d, a, q)]
                if any(-l in cl for l in cl):
                    continue
                self.sink.add(sorted(set(cl), key=abs))
                cnt += 1
        self.stats["hull_sb_clauses"] = cnt

    def build(self, sb=True, hull=False):
        self.add_gp()
        self.add_a4()
        self.add_centre_facts()
        self.add_kgon()
        if sb:
            self.add_sb()
        if hull:
            assert self.kind == "rot" and sb
            self.add_hull_sb()

    def write(self, path, mappath=None, body=None):
        self.sink.f.close()
        with open(path, "w") as f:
            f.write(f"c zcnf kind={self.kind} m={self.m} t={self.t} axis={self.axis} N={self.N} K={self.K}\n")
            f.write(f"p cnf {self.nv} {self.sink.n}\n")
            with open(body) as b:
                import shutil
                shutil.copyfileobj(b, f)
        import os
        os.remove(body)
        info = {"kind": self.kind, "m": self.m, "t": self.t, "axis": self.axis, "N": self.N, "K": self.K, "Z": self.Z,
                "vars": self.nv, "X_vars": self.nX, "clauses": self.sink.n, "stats": self.stats}
        if mappath:
            info["triples"] = [[a, b, c, v, s] for (a, b, c), (v, s) in sorted(self.tv.items())]
            with open(mappath, "w") as f:
                json.dump(info, f)
        return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["rot", "mirror"])
    ap.add_argument("t", type=int, help="number of orbits (pairs for mirror)")
    ap.add_argument("K", type=int)
    ap.add_argument("--m", type=int, default=2)
    ap.add_argument("--no-sb", action="store_true")
    ap.add_argument("--axis", type=int, default=0, help="mirror: number of points on the axis (0, 1 or 2)")
    ap.add_argument("--hull", action="store_true", help="rot: also require (0,0) to be a vertex of the convex hull")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--map")
    a = ap.parse_args()
    enc = ZEncoding(a.kind, a.t, a.K, a.m, body=a.out + ".body", axis=a.axis)
    enc.build(sb=not a.no_sb, hull=a.hull)
    info = enc.write(a.out, a.map, a.out + ".body")
    info.pop("triples", None)
    print(json.dumps(info))


if __name__ == "__main__":
    main()
