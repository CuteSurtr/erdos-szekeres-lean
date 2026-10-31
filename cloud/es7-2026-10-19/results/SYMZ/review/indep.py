#!/usr/bin/env python3
"""Independent exact-arithmetic soundness audit of zcnf.py 'mirror --axis 1' CNFs (does not use zvalidate/zrandtest).

For a real reflection-symmetric set (axis = y-axis, one point on the axis, general position), labelled pairs top to
bottom / left point first / axis point = 2t / Z = 2t+1 = (0,1,0):
  * triple variables get values from exact determinants via the MAP (every listed triple must be consistent);
  * the unlisted triples must be exactly the real zero triples;
  * conv variables are renumbered independently (canonical r-sets, r = 4..K-1, in combinations order, after X_vars)
    and set to actual convex position (4-point criterion, cross-checked against a monotone-chain hull on small N);
  * every clause of the CNF is evaluated; a violated clause is acceptable only if it is literally the K-set clause of
    a canonical K-set that is really in convex position (hull check).
"""
import itertools, json, os, random, subprocess, sys, time
from itertools import combinations

ZCNF = os.environ.get("ZCNF", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "zcnf.py"))
HERE = os.path.dirname(os.path.abspath(__file__))


def sgn(x):
    return (x > 0) - (x < 0)


def orient(a, b, c):
    return sgn((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


def det3(u, v, w):
    return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0]))


def hull_size(P):
    P = sorted(P)
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return len(lo) + len(up) - 2


def general_position(P):
    return len(set(P)) == len(P) and all(orient(a, b, c) != 0 for a, b, c in combinations(P, 3))


def config_points(lefts, ax):
    return [q for (x, y) in lefts for q in ((x, y), (-x, y))] + [ax]


def label(lefts, ax):
    t = len(lefts)
    order = sorted(lefts, key=lambda p: -p[1])
    assert len({p[1] for p in order}) == t and ax[0] == 0 and ax[1] not in {p[1] for p in order}
    pts2 = {}
    for o, (x, y) in enumerate(order):
        assert x < 0
        pts2[2 * o], pts2[2 * o + 1] = (x, y), (-x, y)
    pts2[2 * t] = ax
    vec = {i: (1, p[0], p[1]) for i, p in pts2.items()}
    vec[2 * t + 1] = (0, 1, 0)
    return pts2, vec


def nonconvex4(pts2, N):
    bad = set()
    for Q in combinations(range(N), 4):
        for d in Q:
            a, b, c = [q for q in Q if q != d]
            if orient(pts2[a], pts2[b], pts2[d]) == orient(pts2[b], pts2[c], pts2[d]) == orient(pts2[c], pts2[a], pts2[d]):
                bad.add(Q)
                break
    return bad


def read_header(cnf):
    with open(cnf) as f:
        for line in f:
            if line.startswith("p cnf"):
                _, _, nv, nc = line.split()
                return int(nv), int(nc)


def assignment(info, pts2, vec, t, K, nv_header, hullcheck=False):
    N, NP, Z = 2 * t + 1, 2 * t, 2 * t + 1
    assert info["N"] == N and info["Z"] == Z and info["K"] == K and info.get("axis") == 1 and info["t"] == t
    listed = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    problems = []
    real = {}
    for T in combinations(range(N + 1), 3):
        x = sgn(det3(vec[T[0]], vec[T[1]], vec[T[2]]))
        real[T] = x
        if (x == 0) != (T not in listed):
            problems.append(("zero-pattern", T, x))
    val = {}
    for T, (v, s) in listed.items():
        x = real[T] * s
        if v in val and val[v] != x:
            problems.append(("identity-violated", T, v))
        val.setdefault(v, x)
    nX = info["X_vars"]
    assert set(val) == set(range(1, nX + 1))
    flipi = lambda i: i ^ 1 if i < NP else i
    bad4 = nonconvex4(pts2, N)
    setof, nxt = {}, nX
    for r in range(4, K):
        for S in combinations(range(N), r):
            if tuple(sorted(flipi(i) for i in S)) < S:
                continue
            nxt += 1
            c = not any(Q in bad4 for Q in combinations(S, 4))
            if hullcheck:
                assert c == (hull_size([pts2[i] for i in S]) == r)
            val[nxt] = 1 if c else -1
            setof[nxt] = S
    if nxt != nv_header:
        problems.append(("var-count", nxt, nv_header))
    return val, setof, bad4, problems


def eval_py(cnf, val):
    viol, idx = [], 0
    with open(cnf) as f:
        for line in f:
            if line[0] in "cp":
                continue
            lits = list(map(int, line.split()))
            assert lits and lits[-1] == 0 and 0 not in lits[:-1] and len(lits) > 1, ("malformed", idx, line)
            lits = lits[:-1]
            if not any((val[abs(l)] > 0) == (l > 0) for l in lits):
                viol.append((idx, lits))
            idx += 1
    return viol, idx


def classify(viol, setof, pts2, t, K):
    NP, N = 2 * t, 2 * t + 1
    flipi = lambda i: i ^ 1 if i < NP else i
    fl = lambda S: tuple(sorted(flipi(i) for i in S))
    canon = lambda S: min(S, fl(S))
    varof = {S: v for v, S in setof.items()}
    bad, ok_sets = [], set()
    for idx, lits in viol:
        found = None
        if all(l < 0 and -l in setof and len(setof[-l]) == K - 1 for l in lits):
            A = setof[-lits[0]]
            cands = set()
            others = [setof[-l] for l in lits[1:]] or [A]
            for B in (A, fl(A)):
                for C in (others[0], fl(others[0])):
                    D = set(C) - set(B)
                    if len(D) == 1:
                        cands.add(tuple(sorted(B + tuple(D))))
                if len(lits) == 1:
                    cands |= {tuple(sorted(B + (x,))) for x in range(N) if x not in B}
            for S in cands:
                if canon(S) != S:
                    continue
                cl = {-varof[canon(S[:i] + S[i + 1:])] for i in range(K)}
                if cl == set(lits):
                    found = S
                    break
        if found is not None and hull_size([pts2[i] for i in found]) == K:
            ok_sets.add(found)
        else:
            bad.append((idx, lits))
    return len(ok_sets), bad


def run_case(cnf, info, lefts, ax, t, K, nv, py=True, hullcheck=False):
    pts2, vec = label(lefts, ax)
    val, setof, bad4, problems = assignment(info, pts2, vec, t, K, nv, hullcheck)
    if py:
        viol, nparsed = eval_py(cnf, val)
    else:
        abin = os.path.join(HERE, "assign.bin")
        b = bytearray(nv + 1)
        for v, x in val.items():
            b[v] = 1 if x > 0 else 0
        open(abin, "wb").write(bytes(b))
        out = os.path.join(HERE, "viol.txt")
        r = subprocess.run([os.path.join(HERE, "evalcnf"), cnf, abin, out], capture_output=True, text=True)
        print("   evalcnf:", r.stdout.strip(), r.stderr.strip())
        viol = []
        for line in open(out):
            xs = list(map(int, line.split()))
            viol.append((xs[0], xs[1:-1]))
    nK, bad = classify(viol, setof, pts2, t, K)
    kfree = not any(not any(Q in bad4 for Q in combinations(S, 4)) for S in combinations(range(2 * t + 1), K)) \
        if 2 * t + 1 <= 15 else None
    return dict(problems=problems, violated=len(viol), explained_Kgon=nK, unexplained=bad[:5], n_unexplained=len(bad),
                kfree=kfree)


# ---------------- configuration generators
def random_config(t, rng, C):
    while True:
        lefts = [(-rng.randint(1, C), rng.randint(-C, C)) for _ in range(t)]
        ax = (0, rng.randint(-C, C))
        if general_position(config_points(lefts, ax)):
            return lefts, ax


def tricky_config(t, rng, C, mode):
    """axis point at the top / bottom / within height 1 of a pair; pairs with nearly equal heights."""
    while True:
        lefts, ax = random_config(t, rng, C)
        ys = sorted(p[1] for p in lefts)
        if mode == "top":
            ax = (0, ys[-1] + rng.randint(1, 3))
        elif mode == "bottom":
            ax = (0, ys[0] - rng.randint(1, 3))
        elif mode == "near":
            ax = (0, rng.choice(ys) + rng.choice((-1, 1)))
        elif mode == "closepairs":
            y0 = lefts[0][1]
            lefts = [lefts[0]] + [(x, y0 + k + 1) for k, (x, _) in enumerate(lefts[1:])]
        if general_position(config_points(lefts, ax)):
            return lefts, ax


def count_kgons(lefts, ax, K):
    pts2, _ = label(lefts, ax)
    N = len(pts2)
    bad4 = nonconvex4(pts2, N)
    return sum(1 for S in combinations(range(N), K) if not any(Q in bad4 for Q in combinations(S, 4)))


def kfree_config(t, K, rng, C, iters=3000):
    lefts, ax = random_config(t, rng, C)
    cur = count_kgons(lefts, ax, K)
    for _ in range(iters):
        if cur == 0:
            return lefts, ax
        nl, na = list(lefts), ax
        j = rng.randrange(t + 1)
        big = rng.random() < 0.3
        if j < t:
            x, y = nl[j]
            nl[j] = (-rng.randint(1, C), rng.randint(-C, C)) if big else \
                (min(-1, x + rng.randint(-C // 20, C // 20)), y + rng.randint(-C // 20, C // 20))
        else:
            na = (0, rng.randint(-C, C) if big else ax[1] + rng.randint(-C // 20, C // 20))
        if not general_position(config_points(nl, na)):
            continue
        s = count_kgons(nl, na, K)
        if s <= cur:
            lefts, ax, cur = nl, na, s
    return None


def gen_cnf(zcnf, t, K, tag):
    cnf = os.path.join(HERE, f"{tag}_t{t}k{K}a1.cnf")
    mp = cnf[:-4] + ".json"
    subprocess.run([sys.executable, zcnf, "mirror", str(t), str(K), "--axis", "1", "-o", cnf, "--map", mp],
                   check=True, capture_output=True)
    return cnf, mp


def small(seed, zcnf=ZCNF, tag="orig", cases=((3, 5), (4, 6), (5, 6), (4, 7), (5, 7), (6, 7)), nrand=6, nfree=2):
    rng = random.Random(seed)
    allok = True
    for t, K in cases:
        cnf, mp = gen_cnf(zcnf, t, K, tag)
        info = json.load(open(mp))
        nv, nc = read_header(cnf)
        cfgs = [("random", random_config(t, rng, 10 ** 6)) for _ in range(nrand)]
        cfgs += [(m, tricky_config(t, rng, 10 ** 6, m)) for m in ("top", "bottom", "near", "closepairs")]
        cfgs += [("small-coords", random_config(t, rng, 12))]
        for _ in range(nfree):
            c = kfree_config(t, K, rng, 1000)
            if c:
                cfgs.append(("Kgon-free", c))
        for name, (lefts, ax) in cfgs:
            r = run_case(cnf, info, lefts, ax, t, K, nv, hullcheck=(name == "random"))
            ok = not r["problems"] and r["n_unexplained"] == 0 and (r["kfree"] is not True or r["violated"] == 0)
            allok &= ok
            print(f"[{tag}] t={t} K={K} {name:12s} kfree={r['kfree']!s:5s} violated={r['violated']:5d} "
                  f"explained_by_convex_K-set={r['explained_Kgon']:5d} unexplained={r['n_unexplained']} "
                  f"problems={r['problems'][:3]} {'OK' if ok else 'FAIL ' + str(r['unexplained'][:2])}")
    return allok


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "small":
        ok = small(int(sys.argv[2]))
        print("ALL OK" if ok else "SOME FAILURE")
    elif mode == "mutant":
        zc, tag = sys.argv[2], sys.argv[3]
        ok = small(int(sys.argv[4]), zcnf=zc, tag=tag, cases=((4, 6), (5, 7)), nrand=3, nfree=1)
        print(f"mutant {tag}: {'NOT DETECTED' if ok else 'DETECTED'}")
    elif mode == "big":
        cnf, mp, src = sys.argv[2], sys.argv[3], sys.argv[4]
        t, K = 16, 7
        info = json.load(open(mp))
        nv, nc = read_header(cnf)
        rng = random.Random(int(sys.argv[5]) if len(sys.argv) > 5 else 1)
        if src == "random":
            lefts, ax = random_config(t, rng, 10 ** 6)
        else:
            P = [tuple(map(int, l.split()[:2])) for l in open(src) if l.strip() and not l.startswith("#")]
            S = set(P)
            assert len(P) == 32 and all((-x, y) in S for x, y in P) and not any(x == 0 for x, y in P)
            lefts = [p for p in P if p[0] < 0]
            ys = sorted(p[1] for p in lefts)
            while True:
                ax = (0, rng.randint(ys[0] - 20, ys[-1] + 20))
                if general_position(config_points(lefts, ax)):
                    break
        print("axis point", ax, "heights", sorted(p[1] for p in lefts))
        t0 = time.time()
        r = run_case(cnf, info, lefts, ax, t, K, nv, py=False)
        print(f"big {src}: {r}  ({time.time() - t0:.1f}s)")
