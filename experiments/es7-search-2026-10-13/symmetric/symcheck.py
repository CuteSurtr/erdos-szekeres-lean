#!/usr/bin/env python3
"""Independent checker for models of symcnf.py CNFs.

Reads the map JSON (triple variables) and a model (CaDiCaL output with 'v' lines, or one line of
integer literals), rebuilds chi on all P points and verifies, with code that does not use the
generator's clause construction:
  * symmetry  chi(pi a, pi b, pi c) = chi(a,b,c)
  * A4 (interiority) on every 4-subset, GP 3-term relations on every 5-subset of all P points
  * centre facts and the labelling normal form (reported, not required for soundness)
  * no convex K-gon among the set points by the 4-point criterion (exact DFS over convex
    subsets; also the maximum convex subset size)
  * writes <model>.sig (1-based, set points relabelled 1..N) for the C brute force brute_kgon

usage: symcheck.py map.json model.txt [--sig out.sig] [--quiet]
       symcheck.py map.json --brute-all   (enumerate all 2^X assignments, count the ones
                                           satisfying all constraints: tiny instances only)
"""
import itertools
import json
import sys


def parity(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return -1 if inv & 1 else 1


class Chi:
    def __init__(self, info, vals):
        """vals: dict var -> bool for the triple-orbit variables"""
        self.info = info
        self.P = info["P"]
        self.m = info["m"]
        self.c = info["center_index"]
        self.setpts = info["setpts"]
        self.sig = {}
        for a, b, c, v, s in info["triples"]:
            self.sig[(a, b, c)] = s * (1 if vals[v] else -1)
        assert len(self.sig) == len(list(itertools.combinations(range(self.P), 3)))

    def O(self, a, b, c):
        return parity((a, b, c)) * self.sig[tuple(sorted((a, b, c)))]

    def pi(self, i, k=1):
        if i == self.c:
            return i
        o, r = divmod(i, self.m)
        return o * self.m + (r + k) % self.m

    def check_symmetry(self):
        bad = 0
        for T in itertools.combinations(range(self.P), 3):
            v = self.O(*T)
            for k in range(1, self.m):
                if self.O(*[self.pi(x, k) for x in T]) != v:
                    bad += 1
        return bad

    def check_axioms(self):
        O = self.O
        badA4 = badGP = 0
        for S in itertools.combinations(range(self.P), 4):
            for t in S:
                p, q, r = [x for x in S if x != t]
                for s in (1, -1):
                    if O(t, q, r) == s and O(p, t, r) == s and O(p, q, t) == s and O(p, q, r) != s:
                        badA4 += 1
        for S in itertools.combinations(range(self.P), 5):
            for x in S:
                y1, y2, y3, y4 = [y for y in S if y != x]
                t1 = O(x, y1, y2) * O(x, y3, y4)
                t2 = -O(x, y1, y3) * O(x, y2, y4)
                t3 = O(x, y1, y4) * O(x, y2, y3)
                if t1 == t2 == t3:
                    badGP += 1
        return badA4, badGP

    def check_center_facts(self):
        if self.c is None:
            return 0
        bad = 0
        m = self.m
        for a in range(self.P):
            if a == self.c:
                continue
            for k in range(1, m):
                want = 1 if 2 * k < m else -1
                if self.O(self.c, a, self.pi(a, k)) != want:
                    bad += 1
        return bad

    def check_sb(self):
        """labelling normal form of symcnf.py (returns number of violated constraints)"""
        import math
        m, t = self.m, self.info["t"]
        pt = lambda o, r: o * m + r
        bad = 0
        if t < 2:
            return 0
        if m % 2 == 1:
            c = self.c
            for o in range(1, t):
                bad += self.O(c, pt(0, 0), pt(o, 0)) != 1
                bad += self.O(c, pt(0, 1), pt(o, 0)) != -1
            for o in range(1, t):
                for o2 in range(o + 1, t):
                    bad += self.O(c, pt(o, 0), pt(o2, 0)) != 1
        else:
            h = m // 2
            qx, qy = math.cos(math.pi / m), math.sin(math.pi / m)
            for o in range(1, t):
                for j in range(h):
                    ax, ay = math.cos(2 * math.pi * j / m), math.sin(2 * math.pi * j / m)
                    d = (-ax - ax) * (qy - ay) - (-ay - ay) * (qx - ax)
                    want = 1 if d > 0 else -1
                    bad += self.O(pt(0, j), pt(0, j + h), pt(o, 0)) != want
            for o in range(1, t):
                for o2 in range(o + 1, t):
                    bad += self.O(pt(0, 0), pt(o, 0), pt(o2, 0)) != 1
        return bad

    # ---- convex position by the 4-point criterion
    def inside(self, d, a, b, c):
        o = self.O(a, b, d)
        return o == self.O(b, c, d) == self.O(c, a, d)

    def _ok_add(self, cur, p):
        for a, b, c in itertools.combinations(cur, 3):
            if self.inside(p, a, b, c) or self.inside(a, b, c, p) or self.inside(b, a, c, p) or self.inside(c, a, b, p):
                return False
        return True

    def max_convex(self, K=None):
        """largest convex subset of the set points (exact DFS; subsets of convex sets are convex).
        If K is given, also returns the number of convex K-subsets (capped at 10^6)."""
        pts = self.setpts
        n = len(pts)
        best = 0
        countK = 0

        def dfs(cur, start):
            nonlocal best, countK
            best = max(best, len(cur))
            if K is not None and len(cur) == K:
                countK += 1
                return
            for i in range(start, n):
                if K is None and len(cur) + (n - i) <= best:
                    break
                p = pts[i]
                if self._ok_add(cur, p):
                    cur.append(p)
                    dfs(cur, i + 1)
                    cur.pop()
                    if countK >= 10 ** 6:
                        return

        dfs([], 0)
        return best, countK

    def write_sig(self, path):
        pts = self.setpts
        idx = {p: i + 1 for i, p in enumerate(pts)}
        with open(path, "w") as f:
            for a, b, c in itertools.combinations(pts, 3):
                f.write(f"{idx[a]} {idx[b]} {idx[c]} {self.O(a, b, c)}\n")


def read_model(path):
    vals = {}
    status = None
    with open(path) as f:
        for line in f:
            if line.startswith("s "):
                status = line.strip()
                continue
            if line.startswith("v "):
                line = line[2:]
            elif line.startswith("c"):
                continue
            for tok in line.split():
                v = int(tok)
                if v != 0:
                    vals[abs(v)] = v > 0
    return status, vals


def full_check(info, vals, K, sig_path=None, quiet=False):
    chi = Chi(info, vals)
    sym = chi.check_symmetry()
    a4, gp = chi.check_axioms()
    cf = chi.check_center_facts()
    sb = chi.check_sb()
    best, cnt = chi.max_convex(K)
    res = {"symmetry_violations": sym, "A4_violations": a4, "GP_violations": gp,
           "center_fact_violations": cf, "sb_violations": sb, "max_convex": best, f"convex_{K}_subsets": cnt}
    if sig_path:
        chi.write_sig(sig_path)
    if not quiet:
        print(json.dumps(res))
    return res


def brute_all(info):
    """count assignments of the X variables that satisfy symmetry+axioms+centre+sb+no K-gon directly"""
    nX = info["X_vars"]
    K = info["K"]
    good = []
    for bits in itertools.product((True, False), repeat=nX):
        vals = {i + 1: bits[i] for i in range(nX)}
        chi = Chi(info, vals)
        if chi.check_axioms() != (0, 0):
            continue
        if chi.check_center_facts() or chi.check_sb():
            continue
        best, _ = chi.max_convex()
        if best >= K:
            continue
        good.append(tuple(sorted((i + 1) if bits[i] else -(i + 1) for i in range(nX))))
    return good


def main():
    args = sys.argv[1:]
    info = json.load(open(args[0]))
    if "--brute-all" in args:
        good = brute_all(info)
        print(f"brute-all: X_vars={info['X_vars']} assignments={2**info['X_vars']} satisfying={len(good)}")
        if "--dump" in args:
            out = args[args.index("--dump") + 1]
            with open(out, "w") as f:
                for g in good:
                    f.write(" ".join(map(str, g)) + "\n")
        return
    status, vals = read_model(args[1])
    sig = None
    if "--sig" in args:
        sig = args[args.index("--sig") + 1]
    if status:
        print(status)
    full_check(info, vals, info["K"], sig, "--quiet" in args)


if __name__ == "__main__":
    main()
