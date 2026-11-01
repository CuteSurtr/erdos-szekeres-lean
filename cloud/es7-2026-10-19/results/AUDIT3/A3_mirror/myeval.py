#!/usr/bin/env python3
"""Independent exact-arithmetic clause evaluator for zcnf.py mirror CNFs (auditor A3, written from the README's
semantics, not from zvalidate.py / zrandtest.py / review/indep.py).

For each random mirror-symmetric integer configuration in the README's normal form
  - axis = y-axis; pair o: (o,0) = L_o = (-a_o, b_o), (o,1) = R_o = (a_o, b_o), a_o > 0, index 2o, 2o+1;
  - pairs by strictly decreasing height b; axis points (0, c_j) at indices 2t, 2t+1; with two, upper first;
  - Z = index N, homogeneous vector (0, 1, 0); points (1, x, y); chi = sign det;
it checks, with exact integers:
  1. the zero triples are exactly {Z, L_i, R_i}, and these are exactly the triples missing from the variable map;
  2. every variable class of the map is consistent (chi(T) * s constant over the class) -> value of X_v;
  3. the convexity variables, numbered independently (canonical subsets in lexicographic order, sizes 4..K-1),
     get the actual convex-position value (edge-count test, independent of the 4-point criterion);
  4. every clause of the CNF is true, except clauses whose literal set equals the K-clause of a canonical K-set
     that is actually in convex position; and the multiset of violated clauses equals the multiset of K-clauses of
     canonical convex K-sets (two-way check).
usage: myeval.py CNF MAP.json t K axis NCONF SEED [--mode M] [--bad B]
  --bad: deliberately break the normal form (unsorted | swaplr | axisorder) for sensitivity tests.
"""
import argparse, itertools, json, random, sys
from collections import Counter


def det3(u, v, w):
    return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0]))


def sgn(x):
    return (x > 0) - (x < 0)


def perm_sign(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return -1 if inv % 2 else 1


def gen_config(t, axis, rng, mode, bad=None):
    """returns list of (x, y) integer points in index order, or None if general position fails"""
    R = rng.choice([30, 200, 10 ** 4, 10 ** 9]) if mode == "mixed" else 1000
    pairs = []
    if mode in ("uniform", "mixed"):
        for _ in range(t):
            pairs.append((rng.randint(1, R), rng.randint(-R, R)))
    elif mode == "circle":                      # near a circle: many convex subsets
        import math
        for _ in range(t):
            th = rng.uniform(-math.pi / 2, math.pi / 2)
            r = 10 ** 6 * (1 + rng.uniform(-0.02, 0.02))
            pairs.append((max(1, int(r * math.cos(th))), int(r * math.sin(th))))
    elif mode == "neardeg":                     # nearly equal heights, tiny / huge a, axis near pair heights
        base = rng.randint(-10 ** 6, 10 ** 6)
        for i in range(t):
            a = rng.choice([1, 2, rng.randint(1, 10 ** 6), 10 ** 7 + rng.randint(0, 9)])
            b = base + rng.choice([i, -i, 3 * i + rng.randint(0, 2), rng.randint(-10 ** 6, 10 ** 6)])
            pairs.append((a, b))
    else:
        raise ValueError(mode)
    hs = [b for _, b in pairs]
    if len(set(hs)) != t:
        return None
    pairs.sort(key=lambda ab: -ab[1])          # normal form: decreasing height
    if bad == "unsorted" and t >= 2:
        i = rng.randrange(t - 1)
        pairs[i], pairs[i + 1] = pairs[i + 1], pairs[i]
    pts = []
    for i, (a, b) in enumerate(pairs):
        if bad == "swaplr" and i == 0:
            pts += [(a, b), (-a, b)]
        else:
            pts += [(-a, b), (a, b)]
    cs = []
    for _ in range(axis):
        if mode == "neardeg" and pairs:
            c = rng.choice(pairs)[1] + rng.choice([-1, 1, 2, -2])
        else:
            c = rng.randint(-2 * R, 2 * R)
        cs.append(c)
    if len(set(cs)) != axis:
        return None
    cs.sort(reverse=True)                      # two axis points: upper first
    if bad == "axisorder" and axis == 2:
        cs.reverse()
    pts += [(0, c) for c in cs]
    # general position, exactly
    for p, q, r in itertools.combinations(pts, 3):
        if det3((1,) + p, (1,) + q, (1,) + r) == 0:
            return None
    return pts


class Inst:
    def __init__(self, cnf, mp, t, K, axis):
        self.t, self.K, self.axis = t, K, axis
        self.NP = 2 * t
        self.N = 2 * t + axis
        self.Z = self.N
        with open(mp) as f:
            info = json.load(f)
        assert info["kind"] == "mirror" and info["t"] == t and info["K"] == K and info.get("axis", 0) == axis
        assert info["Z"] == self.N
        self.nX = info["X_vars"]
        self.tmap = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
        self.clauses = []
        with open(cnf) as f:
            hdr = None
            cur = []
            for line in f:
                if line.startswith("c"):
                    continue
                if line.startswith("p"):
                    _, _, nv, nc = line.split()
                    hdr = (int(nv), int(nc))
                    continue
                for tok in line.split():
                    l = int(tok)
                    if l == 0:
                        self.clauses.append(tuple(cur))
                        cur = []
                    else:
                        assert abs(l) <= hdr[0], "literal out of range"
                        cur.append(l)
            assert not cur, "unterminated clause"
        self.nv, self.nc = hdr
        assert len(self.clauses) == self.nc, (len(self.clauses), self.nc)
        # independent numbering of convexity variables
        self.conv = {}
        nxt = self.nX
        for r in range(4, K):
            for S in itertools.combinations(range(self.N), r):
                if self.canon(S) == S:
                    nxt += 1
                    self.conv[S] = nxt
        assert nxt == self.nv, ("variable count", nxt, self.nv)

    def sigma(self, i):
        if i >= self.NP:
            return i
        return i ^ 1

    def canon(self, S):
        T = tuple(sorted(self.sigma(x) for x in S))
        return min(S, T)

    def evaluate(self, pts):
        N, Z, K = self.N, self.Z, self.K
        vec = [(1, x, y) for x, y in pts] + [(0, 1, 0)]
        chi = {}
        for T in itertools.combinations(range(N + 1), 3):
            chi[T] = sgn(det3(*(vec[i] for i in T)))
        # 1. zero pattern
        expect_zero = {tuple(sorted((Z, 2 * o, 2 * o + 1))) for o in range(self.t)}
        zeros = {T for T, s in chi.items() if s == 0}
        assert zeros == expect_zero, ("zero pattern", sorted(zeros ^ expect_zero)[:5])
        assert set(self.tmap) == set(chi) - zeros, "map triples != nonzero triples"
        # 2. class consistency
        val = {}
        bad_classes = 0
        for T, (v, s) in self.tmap.items():
            x = chi[T] * s
            if v in val and val[v] != x:
                bad_classes += 1
            val.setdefault(v, x)
        assert len(val) == self.nX
        assign = [None] * (self.nv + 1)
        for v, x in val.items():
            assign[v] = (x == 1)

        def ch(a, b, c):
            T = tuple(sorted((a, b, c)))
            return perm_sign((a, b, c)) * chi[T]

        # 3. actual convexity (edge count)
        def convex(S):
            n = len(S)
            edges = 0
            for p, q in itertools.combinations(S, 2):
                sides = {ch(p, q, r) for r in S if r != p and r != q}
                if len(sides) == 1:
                    edges += 1
            return edges == n

        for S, v in self.conv.items():
            assign[v] = convex(S)
        assert all(x is not None for x in assign[1:]), "unassigned variable"
        # expected violated clauses: K-clauses of canonical convex K-sets
        exp = Counter()
        nconvK = 0
        for S in itertools.combinations(range(N), K):
            if self.canon(S) != S:
                continue
            if convex(S):
                nconvK += 1
                key = frozenset(-self.conv[self.canon(S[:i] + S[i + 1:])] for i in range(K))
                exp[key] += 1
        # 4. evaluate
        viol = Counter()
        for cl in self.clauses:
            if not any(assign[abs(l)] == (l > 0) for l in cl):
                viol[frozenset(cl)] += 1
        unexplained = viol - exp
        missing = exp - viol
        return dict(bad_classes=bad_classes, violated=sum(viol.values()), convK=nconvK,
                    unexplained=sum(unexplained.values()), missing=sum(missing.values()),
                    sample_unexplained=[sorted(k) for k in list(unexplained)[:3]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf"); ap.add_argument("map")
    ap.add_argument("t", type=int); ap.add_argument("K", type=int); ap.add_argument("axis", type=int)
    ap.add_argument("nconf", type=int); ap.add_argument("seed", type=int)
    ap.add_argument("--mode", default="all")
    ap.add_argument("--bad", default=None)
    a = ap.parse_args()
    inst = Inst(a.cnf, a.map, a.t, a.K, a.axis)
    rng = random.Random(a.seed)
    modes = ["uniform", "mixed", "circle", "neardeg"] if a.mode == "all" else [a.mode]
    tot = Counter()
    fails = []
    done = 0
    tries = 0
    while done < a.nconf and tries < 100 * a.nconf:
        tries += 1
        mode = modes[done % len(modes)]
        pts = gen_config(a.t, a.axis, rng, mode, a.bad)
        if pts is None:
            continue
        try:
            r = inst.evaluate(pts)
        except AssertionError as e:
            fails.append(("assert", str(e), pts))
            done += 1
            continue
        done += 1
        tot["configs"] += 1
        tot["with_convK"] += r["convK"] > 0
        tot["without_convK"] += r["convK"] == 0
        tot["violated"] += r["violated"]
        tot["convK"] += r["convK"]
        if r["bad_classes"] or r["unexplained"] or r["missing"]:
            fails.append((mode, r, pts))
    print(json.dumps({"cnf": a.cnf.split("/")[-1], "t": a.t, "K": a.K, "axis": a.axis, "bad": a.bad,
                      "clauses": inst.nc, "vars": inst.nv, **tot, "failures": len(fails)}))
    for f in fails[:3]:
        print("FAIL", f[0], f[1] if f[0] != "assert" else f[1], file=sys.stderr)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
