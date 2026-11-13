"""Referee's independent evaluation of the full central base CNF (zcnf.py rot 17 7 --m 2 --hull, sha b0061e90...).

Own code throughout (no import from ../../tests): exact integer geometry, own normal-form labelling, own
convexity DP, own streamed clause evaluation (numpy, 32 MB chunks; the CNF is never loaded whole).
For each labelling the violated clauses (as sorted literal tuples) must equal exactly:
  * the KGON clauses {-conv(canon(Q - x))} of the canonical 7-sets Q in convex position, and
  * for a non-hull first point (control): the HULL clauses of the triangles of other points containing it.
usage: refbase.py BASE.cnf BASE.json SYM32.txt
"""
import itertools
import json
import random
import sys
import time

import numpy as np

T, K = 17, 7
N = 2 * T
Z = N


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def sg(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


def inside(q, a, b, d):
    s = (sg(cross(a, b, q)), sg(cross(b, d, q)), sg(cross(d, a, q)))
    return s[0] != 0 and s[0] == s[1] == s[2]


def label(P, c, p0):
    h = lambda q: (2 * c[0] - q[0], 2 * c[1] - q[1])
    reps = [q for q in P if q not in (p0, h(p0)) and cross(c, p0, q) > 0]
    assert len(reps) == T - 1
    rest, order = list(reps), []
    while rest:
        f = [r for r in rest if all(r == s or cross(c, r, s) > 0 for s in rest)]
        assert len(f) == 1
        order.append(f[0])
        rest.remove(f[0])
    X = [p0, h(p0)]
    for r in order:
        X += [r, h(r)]
    return X + [c]


def convexity_tables(P):
    """point-space bitmask -> convex, for all 4-, 5-, 6-subsets; and the list of convex 7-subsets"""
    n = len(P)
    c4 = {}
    for Q in itertools.combinations(range(n), 4):
        pts = [P[i] for i in Q]
        ok = not any(inside(pts[i], *[pts[j] for j in range(4) if j != i]) for i in range(4))
        c4[sum(1 << i for i in Q)] = ok
    levels = {4: c4}
    for r in (5, 6):
        prev, cur = levels[r - 1], {}
        for Q in itertools.combinations(range(n), r):
            m = sum(1 << i for i in Q)
            cur[m] = all(prev[m ^ (1 << i)] for i in Q)
        levels[r] = cur
    conv7 = []
    for m6, ok in levels[6].items():
        if not ok:
            continue
        top = m6.bit_length() - 1
        for x in range(top + 1, n):
            m7 = m6 | (1 << x)
            if all(levels[6][m7 ^ (1 << i)] for i in range(n) if m7 >> i & 1):
                conv7.append(m7)
    return levels, conv7


def main():
    cnf, mp, symf = sys.argv[1:4]
    t0 = time.time()
    info = json.load(open(mp))
    assert (info["t"], info["K"], info["N"], info["Z"]) == (T, K, N, Z)
    V, XV = info["vars"], info["X_vars"]
    tv = {(a, b, d): (v, s) for a, b, d, v, s in info["triples"]}
    h = lambda i: i ^ 1
    canon = lambda S: min(tuple(S), tuple(sorted(h(x) for x in S)))
    convsets = [S for r in (4, 5, 6) for S in itertools.combinations(range(N), r) if canon(S) == S]
    assert XV + len(convsets) == V
    convvar = {S: XV + 1 + i for i, S in enumerate(convsets)}
    perm_sign = lambda tr: (-1) ** sum(1 for i in range(3) for j in range(i + 1, 3) if tr[i] > tr[j])

    def lit_of(a, b, d):
        v, s = tv[tuple(sorted((a, b, d)))]
        return perm_sign((a, b, d)) * s * v

    print(f"map and conv numbering ready ({time.time() - t0:.0f} s): {XV} triple vars, {len(convsets)} conv vars")
    sym32 = []
    for line in open(symf):
        line = line.split("#")[0].strip()
        if line:
            x, y = line.replace(",", " ").split()[:2]
            sym32.append((int(x), int(y)))
    assert len(sym32) == 32
    rng = random.Random(77)
    configs = [("sym32+near(-134,-269843)", sym32 + [(-134, -269843), (134, 269843)], (0, 0), "all"),
               ("sym32+near(94,270158)", sym32 + [(94, 270158), (-94, -270158)], (0, 0), "one")]
    while True:                                   # a random configuration with a non-parallelogram hull
        c = (rng.randint(-40, 40), rng.randint(-40, 40))
        P = []
        for _ in range(T):
            q = (rng.randint(-10 ** 5, 10 ** 5) + c[0], rng.randint(-10 ** 5, 10 ** 5) + c[1])
            P += [q, (2 * c[0] - q[0], 2 * c[1] - q[1])]
        if len(set(P)) == N and c not in P and all(cross(a, b, d) != 0 for a, b, d in itertools.combinations(P, 3)):
            configs.append(("random", P, c, "one"))
            break
    labellings = []                              # (name, onhull, val array, expected sorted list of clause tuples)
    for name, P, c, which in configs:
        assert len(set(P)) == N and all(cross(a, b, d) != 0 for a, b, d in itertools.combinations(P, 3))
        hullv = [p for p in P if not any(inside(p, a, b, d) for a, b, d in
                                         itertools.combinations([q for q in P if q != p], 3))]
        inner = [p for p in P if p not in hullv]
        levels, conv7 = convexity_tables(P)
        firsts = [(p, True) for p in (hullv if which == "all" else hullv[:1])] + [(inner[0], False)]
        print(f"{name}: |hull| = {len(hullv)}, convex 7-subsets (all) = {len(conv7)} ({time.time() - t0:.0f} s)")
        for p0, onhull in firsts:
            X = label(P, c, p0)
            pos = {p: i for i, p in enumerate(X[:N])}
            val = np.zeros(V + 1, dtype=np.int8)
            ok = True
            for (a, b, d), (v, s) in tv.items():
                o = sg(cross(X[a], X[b], X[d])) * s
                if o == 0 or (val[v] != 0 and val[v] != o):
                    ok = False
                val[v] = o
            zeros = {tr for tr in itertools.combinations(range(N + 1), 3) if cross(*[X[i] for i in tr]) == 0}
            ok &= zeros == set(itertools.combinations(range(N + 1), 3)) - set(tv)
            ptidx = [P.index(X[i]) for i in range(N)]
            for S, v in convvar.items():
                val[v] = 1 if levels[len(S)][sum(1 << ptidx[i] for i in S)] else -1
            assert (val[1:] != 0).all()
            exp = set()
            for m7 in conv7:
                Q = tuple(sorted(pos[P[i]] for i in range(N) if m7 >> i & 1))
                Qc = canon(Q)
                exp.add(tuple(sorted({-convvar[canon(Qc[:i] + Qc[i + 1:])] for i in range(K)})))
            exp = sorted(exp)
            if not onhull:
                for a, b, d in itertools.combinations(range(1, N), 3):
                    if inside(X[0], X[a], X[b], X[d]):
                        s = sg(cross(X[a], X[b], X[0]))
                        exp.append(tuple(sorted({-s * lit_of(a, b, 0), -s * lit_of(b, d, 0), -s * lit_of(d, a, 0)})))
                exp.sort()
            labellings.append((name, p0, onhull, ok, val, exp))
            print(f"  labelling p0={p0} onhull={onhull}: classes consistent and zero pattern exact: {ok}; "
                  f"expected violated clauses {len(exp)}")
    # stream the CNF
    viol = [[] for _ in labellings]
    ncl = 0
    hdr = None
    leftover = b""
    with open(cnf, "rb") as f:
        while hdr is None:
            line = f.readline()
            if line.startswith(b"p cnf"):
                hdr = line.split()
        while True:
            buf = f.read(32 << 20)
            if not buf and not leftover:
                break
            buf = leftover + buf
            cut = buf.rfind(b"\n") + 1 if buf else 0
            if cut == 0:
                cut = len(buf)
            part, leftover = buf[:cut], buf[cut:]
            if not part:
                break
            arr = np.array(part.split(), dtype=np.int64)
            ends = np.flatnonzero(arr == 0)
            assert len(ends) and ends[-1] == len(arr) - 1, "chunk does not end with a clause terminator"
            starts = np.r_[0, ends[:-1] + 1]
            lens = ends - starts
            assert lens.min() >= 1 and lens.max() <= 7
            M = np.zeros((len(ends), 7), dtype=np.int64)
            cols = np.arange(7)[None, :]
            valid = cols < lens[:, None]
            M[valid] = arr[(starts[:, None] + cols)[valid]]
            A = np.abs(M)
            assert A.max() <= V
            S = np.sign(M)
            for k, (_, _, _, _, val, _) in enumerate(labellings):
                sat = ((val[A] == S) & valid).any(axis=1)
                for i in np.flatnonzero(~sat):
                    viol[k].append(tuple(sorted(set(int(x) for x in M[i, :lens[i]]))))
            ncl += len(ends)
            if not buf:
                break
    assert ncl == int(hdr[3]), (ncl, hdr)
    print(f"streamed {ncl} clauses (header {hdr[2].decode()} vars, {hdr[3].decode()} clauses) ({time.time() - t0:.0f} s)")
    allok = True
    for (name, p0, onhull, ok, _, exp), vl in zip(labellings, viol):
        good = ok and sorted(vl) == exp
        allok &= good
        print(f"  {name} p0={p0} onhull={onhull}: violated {len(vl)}, expected {len(exp)} -> {'OK' if good else 'FAIL'}")
    print("REFEREE FULL-BASE EVALUATION", "PASSED" if allok else "FAILED", f"({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
