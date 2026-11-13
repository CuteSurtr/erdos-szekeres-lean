"""The real assignment of a labelled configuration, for a zcnf.py rot (m = 2) CNF.

Given the labelled points X[0..N-1] and X[N] = c (X[2o+1] = h(X[2o])), the assignment of proof.md (Theorem 1) is
  triple variable v:  true iff chi(T) * s_T = +1 for the triples T of its class (the map gives v, s_T);
  conv variable of a set Q (numbering of classes.conv_numbering): true iff Q is in convex position.
All signs are exact (Python integers).  Also computed: the identity check (every class gives one value), the zero
check (exactly the triples missing from the map are collinear), and the canonical K-sets in convex position.
"""
import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import classes  # noqa: E402
import geom     # noqa: E402


def popcount(x):
    return bin(x).count("1")


class Model:
    def __init__(self, mappath, check=True):
        info = json.load(open(mappath))
        self.info = info
        if check:
            ok, msgs, tv = classes.check_map(info)
            if not ok:
                raise SystemExit("map check failed: " + "; ".join(msgs))
        else:
            tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
        self.tv = tv
        self.t, self.N, self.K, self.Z = info["t"], info["N"], info["K"], info["Z"]
        self.V = info["vars"]
        self.X_vars = info["X_vars"]
        self.sets = classes.conv_numbering(self.N, self.K, self.X_vars)
        assert self.X_vars + len(self.sets) == self.V
        self.even = sum(1 << (2 * o) for o in range(self.t))
        self.classes_of = {}
        for T, (v, s) in tv.items():
            self.classes_of.setdefault(v, []).append((T, s))

    def hmask(self, m):
        e = self.even
        return ((m & e) << 1) | ((m >> 1) & e)

    def is_canonical(self, m):
        """lexicographic order of sorted tuples: the set holding min(symmetric difference) is smaller"""
        hm = self.hmask(m)
        if hm == m:
            return True
        d = m ^ hm
        low = d & -d
        return bool(m & low)

    def assignment(self, X):
        """returns (bytearray of V+1 values in {1, 255(-1)}, report dict)"""
        N, Z = self.N, self.Z
        rep = {}
        chi = {}
        zero_ok = True
        for T in itertools.combinations(range(N + 1), 3):
            o = geom.orient(X[T[0]], X[T[1]], X[T[2]])
            if (T in self.tv) != (o != 0):
                zero_ok = False
            chi[T] = geom.sgn(o)
        rep["zero_pattern_matches_map"] = zero_ok
        val = bytearray(self.V + 1)
        ident_ok = True
        for v, lst in self.classes_of.items():
            vals = {chi[T] * s for T, s in lst}
            if len(vals) != 1 or 0 in vals:
                ident_ok = False
            x = next(iter(vals))
            val[v] = 1 if x > 0 else 255
        rep["identities_hold"] = ident_ok
        # convexity of all 4-sets of points (exact orientation), then r-sets by the 4-point criterion
        pts = X[:N]
        conv = {}
        for Q in itertools.combinations(range(N), 4):
            conv[sum(1 << i for i in Q)] = geom.convex4([pts[i] for i in Q])
        levels = {4: conv}
        bitvals = [1 << i for i in range(N)]
        for r in range(5, self.K):
            prev = levels[r - 1]
            cur = {}
            for Q in itertools.combinations(bitvals, r):
                m = sum(Q)
                cur[m] = all(prev[m ^ b] for b in Q)
            levels[r] = cur
        for i, Q in enumerate(self.sets):
            m = sum(1 << j for j in Q)
            val[self.X_vars + 1 + i] = 1 if levels[len(Q)][m] else 255
        # canonical K-sets in convex position, as ranks among canonical K-sets in lexicographic order
        top = levels[self.K - 1]
        rank = 0
        convex_ranks = []
        for Q in itertools.combinations(bitvals, self.K):
            m = sum(Q)
            if not self.is_canonical(m):
                continue
            if all(top[m ^ b] for b in Q):
                convex_ranks.append(rank)
            rank += 1
        rep["canonical_K_sets"] = rank
        rep["convex_K_ranks"] = convex_ranks
        self._levels = levels
        return val, rep

    def spot_check_convexity(self, X, rng, samples=3000):
        """independent check: r-set convexity by the 4-point criterion equals convexity by hull size"""
        bad = 0
        for _ in range(samples):
            r = rng.randint(4, self.K - 1)
            Q = sorted(rng.sample(range(self.N), r))
            m = sum(1 << j for j in Q)
            if self._levels[r][m] != geom.in_convex_position([X[j] for j in Q]):
                bad += 1
        return bad
