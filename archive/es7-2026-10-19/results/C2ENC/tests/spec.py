"""Generator of the clause families of proof.md, and a family-by-family multiset comparison with a CNF.

Written from the statements in proof.md (sections 3-9), not from zcnf.py.  Scope (referee note R4): the comparison
shows coverage, i.e. the families of proof.md account for the CNF exactly; for the GP generic path and for A4 the
enumeration follows the encoder's, so it is not an independent derivation of those two families.  Triple literals use
the encoder's map only for the naming of variables (which variable and which polarity stand for a triple); the map
itself is first checked against the hand-derived classes (classes.py).  conv variables use the numbering of
classes.conv_numbering.

Families (in the order zcnf.py writes them): GP, A4, CONV4, CONV5.., KGON, SB, HULL.
A clause is normalised as the sorted tuple of its distinct literals; a family is compared by
(count, sum of 128-bit BLAKE2b hashes mod 2^128, xor of the hashes, histogram of clause lengths).

usage: spec.py CNF MAP [--no-sb] [--hull] [--skip-cnf]
"""
import argparse
import array
import hashlib
import itertools
import json
import sys
import time

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import classes  # noqa: E402
import geom     # noqa: E402

MASK128 = (1 << 128) - 1


class Fam:
    def __init__(self, name):
        self.name, self.n, self.sum, self.xor, self.hist = name, 0, 0, 0, {}

    def add(self, clause):
        c = tuple(sorted(set(clause)))
        assert 0 not in c
        hv = int.from_bytes(hashlib.blake2b(array.array("i", c).tobytes(), digest_size=16).digest(), "little")
        self.n += 1
        self.sum = (self.sum + hv) & MASK128
        self.xor ^= hv
        self.hist[len(c)] = self.hist.get(len(c), 0) + 1

    def key(self):
        return (self.n, self.sum, self.xor, tuple(sorted(self.hist.items())))


def convex_patterns_by_realization():
    """sign patterns (abc, abd, acd, bcd) of 4 points in convex position, found from real point sets:
    a convex quadrilateral in all 24 labellings (and its mirror image)"""
    quad = [(0, 0), (10, 1), (12, 9), (1, 7)]
    pats = set()
    for Q in (quad, [(x, -y) for x, y in quad]):
        assert geom.convex4(Q)
        for perm in itertools.permutations(Q):
            a, b, c, d = perm
            pats.add(tuple(geom.sgn(geom.orient(*T)) for T in [(a, b, c), (a, b, d), (a, c, d), (b, c, d)]))
    nonconvex = set()
    tri = [(0, 0), (10, 0), (5, 9), (5, 3)]          # last point inside
    for Q in (tri, [(x, -y) for x, y in tri]):
        for perm in itertools.permutations(Q):
            a, b, c, d = perm
            nonconvex.add(tuple(geom.sgn(geom.orient(*T)) for T in [(a, b, c), (a, b, d), (a, c, d), (b, c, d)]))
    assert len(pats) == 6 and len(nonconvex) == 8 and not (pats & nonconvex)
    return sorted(pats)


class Spec:
    def __init__(self, info, sb=True, hull=False):
        ok, msgs, tv = classes.check_map(info)
        if not ok:
            raise SystemExit("map check failed: " + "; ".join(msgs))
        self.info, self.tv = info, tv
        self.t, self.N, self.K, self.Z = info["t"], info["N"], info["K"], info["Z"]
        self.sb, self.hull = sb, hull
        self.sets = classes.conv_numbering(self.N, self.K, info["X_vars"])
        self.convvar = {S: info["X_vars"] + 1 + i for i, S in enumerate(self.sets)}
        assert info["X_vars"] + len(self.sets) == info["vars"]

    # ---- naming
    def L(self, a, b, c):
        """literal that is true iff chi(a, b, c) = +, or 0 for a zero triple"""
        T = (a, b, c)
        S = tuple(sorted(T))
        if S not in self.tv:
            return 0
        v, s = self.tv[S]
        return classes.perm_sign(T) * s * v

    def h(self, i):
        return i if i == self.Z else i ^ 1

    def canon(self, S):
        img = tuple(sorted(self.h(x) for x in S))
        return min(S, img)

    def zero(self, T):
        return tuple(sorted(T)) not in self.tv

    # ---- families
    def gp(self, fam):
        P = self.N + 1
        for F in itertools.combinations(range(P), 5):
            if self.canon(F) != F:
                continue
            for x in F:
                a, b, c, d = [y for y in F if y != x]
                terms = [(1, self.L(x, a, b), self.L(x, c, d)), (-1, self.L(x, a, c), self.L(x, b, d)),
                         (1, self.L(x, a, d), self.L(x, b, c))]
                nz = [(k, l1, l2) for k, l1, l2 in terms if l1 != 0 and l2 != 0]
                if not nz:
                    continue
                vs = sorted({abs(l) for _, l1, l2 in nz for l in (l1, l2)})
                if len(nz) == 3 and len(vs) == 6:
                    # forbidden: all three products k*val(l1)*val(l2) equal to sigma
                    for sigma in (1, -1):
                        for u in itertools.product((1, -1), repeat=3):
                            cl = []
                            for (k, l1, l2), u1 in zip(nz, u):
                                u2 = sigma * k * u1            # value of l2 forced by product = sigma
                                cl += [-u1 * l1, -u2 * l2]     # a literal required to have value u enters as -u*l
                            fam.add(cl)
                    continue
                for bits in itertools.product((1, -1), repeat=len(vs)):
                    val = dict(zip(vs, bits))
                    sg = {k * (val[abs(l1)] if l1 > 0 else -val[abs(l1)]) * (val[abs(l2)] if l2 > 0 else -val[abs(l2)])
                          for k, l1, l2 in nz}
                    if not (1 in sg and -1 in sg):
                        fam.add([-val[v] * v for v in vs])

    def a4(self, fam):
        P = self.N + 1
        for S in itertools.combinations(range(P), 4):
            if any(self.zero(T) for T in itertools.combinations(S, 3)):
                continue
            for t in S:
                p, q, r = [x for x in S if x != t]
                for s in (1, -1):
                    cl = [-s * self.L(t, q, r), -s * self.L(p, t, r), -s * self.L(p, q, t), s * self.L(p, q, r)]
                    if any(-l in cl for l in cl):
                        continue
                    fam.add(cl)

    def conv4(self, fam):
        pats = convex_patterns_by_realization()
        for S in self.sets:
            if len(S) != 4:
                continue
            a, b, c, d = S
            lits = [self.L(a, b, c), self.L(a, b, d), self.L(a, c, d), self.L(b, c, d)]
            for pat in pats:
                cl = [-pat[i] * lits[i] for i in range(4)]
                if any(-l in cl for l in cl):
                    continue
                fam.add(cl + [self.convvar[S]])

    def convr(self, fam, r):
        for S in self.sets:
            if len(S) != r:
                continue
            fam.add([-self.convvar[self.canon(S[:i] + S[i + 1:])] for i in range(r)] + [self.convvar[S]])

    def kgon(self, fam):
        K = self.K
        for S in itertools.combinations(range(self.N), K):
            if self.canon(S) != S:
                continue
            fam.add([-self.convvar[self.canon(S[:i] + S[i + 1:])] for i in range(K)])

    def sbu(self, fam):
        u = set()
        for o in range(1, self.t):
            u.add(self.L(self.Z, 0, 2 * o))
        for o in range(1, self.t):
            for o2 in range(o + 1, self.t):
                u.add(self.L(self.Z, 2 * o, 2 * o2))
        assert not any(-l in u for l in u)
        for l in u:
            fam.add([l])

    def hullc(self, fam):
        q = 0
        for a, b, d in itertools.combinations(range(1, self.N), 3):
            for s in (1, -1):
                cl = [-s * self.L(a, b, q), -s * self.L(b, d, q), -s * self.L(d, a, q)]
                if any(-l in cl for l in cl):
                    continue
                fam.add(cl)

    def families(self):
        fams = []
        for name, fn in [("GP", self.gp), ("A4", self.a4), ("CONV4", self.conv4)]:
            f = Fam(name)
            t0 = time.time()
            fn(f)
            fams.append(f)
            print(f"  spec {name}: {f.n} clauses ({time.time() - t0:.0f} s)", flush=True)
        for r in range(5, self.K):
            f = Fam(f"CONV{r}")
            self.convr(f, r)
            fams.append(f)
            print(f"  spec CONV{r}: {f.n} clauses", flush=True)
        f = Fam("KGON")
        t0 = time.time()
        self.kgon(f)
        fams.append(f)
        print(f"  spec KGON: {f.n} clauses ({time.time() - t0:.0f} s)", flush=True)
        if self.sb:
            f = Fam("SB")
            self.sbu(f)
            fams.append(f)
        if self.hull:
            f = Fam("HULL")
            self.hullc(f)
            fams.append(f)
        return fams


def hash_cnf(path, counts):
    """stream the CNF; split its clauses into consecutive families of the given sizes; hash each family"""
    fams = [Fam(name) for name, _ in counts]
    bounds = []
    acc = 0
    for _, n in counts:
        acc += n
        bounds.append(acc)
    i = 0
    fi = 0
    taut = 0
    header = None
    with open(path) as f:
        for line in f:
            if line[0] == "c":
                continue
            if line[0] == "p":
                header = line.split()
                continue
            lits = list(map(int, line.split()))
            assert lits[-1] == 0 and 0 not in lits[:-1], f"malformed clause line {i + 1}"
            cl = lits[:-1]
            if any(-l in cl for l in cl):
                taut += 1
            while fi < len(bounds) and i >= bounds[fi]:
                fi += 1
            if fi >= len(fams):
                fams.append(Fam("EXTRA"))
                bounds.append(float("inf"))
            fams[fi].add(cl)
            i += 1
    return header, i, fams, taut


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf")
    ap.add_argument("map")
    ap.add_argument("--no-sb", action="store_true")
    ap.add_argument("--hull", action="store_true")
    a = ap.parse_args()
    info = json.load(open(a.map))
    t0 = time.time()
    sp = Spec(info, sb=not a.no_sb, hull=a.hull)
    fams = sp.families()
    print(f"spec generated in {time.time() - t0:.0f} s; total {sum(f.n for f in fams)} clauses", flush=True)
    t0 = time.time()
    header, n, cf, taut = hash_cnf(a.cnf, [(f.name, f.n) for f in fams])
    print(f"CNF streamed in {time.time() - t0:.0f} s: header {' '.join(header)}, {n} clause lines, "
          f"{taut} tautological", flush=True)
    ok = (int(header[3]) == n == sum(f.n for f in fams)) and taut == 0 and len(cf) == len(fams)
    for f, g in zip(fams, cf):
        same = f.key() == g.key()
        ok &= same
        print(f"  {f.name:6s} spec n={f.n:9d}  cnf n={g.n:9d}  lengths {dict(sorted(f.hist.items()))}  "
              f"{'MATCH' if same else 'DIFFER'}")
    for g in cf[len(fams):]:
        print(f"  extra CNF family {g.name}: {g.n} clauses")
    print("SPEC COMPARISON", "PASSED: the CNF equals the specified clause multiset family by family"
          if ok else "FAILED")


if __name__ == "__main__":
    main()
