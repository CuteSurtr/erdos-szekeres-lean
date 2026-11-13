#!/usr/bin/env python3
"""Exact configurations for the big-CNF evaluator (evalbig.c).
usage: mkconf.py MAP.json t axis NCONF SEED OUT.txt OUT.json
Writes, for each configuration (normal form of zcnf.py's README: axis = y-axis, pairs by decreasing height, left
point first; Z = (0,1,0)):
  line 1: the nX values of the triple-class variables ('1' = chi(root) positive), after checking that every class of
          the map is consistent on this configuration and that the zero triples are exactly {Z, L_i, R_i};
  line 2: chi of every sorted triple of the N points (no Z), lexicographic order, as '+'/'-'.
Configuration families: the 7-gon-free 32-point mirror set of results/SYMMAX plus an axis point (t=16, axis=1) or
plus one extra pair (t=17, axis=0); uniform random; near-degenerate; near a circle."""
import itertools, json, math, os, random, sys

R32 = os.path.join(os.environ.get("ES7_RESULTS", "."), "SYMMAX/mirror_32points.txt")


def det3(u, v, w):
    return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0]))


def sgn(x):
    return (x > 0) - (x < 0)


def load32():
    P = [tuple(map(int, l.split())) for l in open(R32) if l.strip()]
    S = set(P)
    assert len(S) == 32 and all((-x, y) in S for x, y in P) and all(x != 0 for x, y in P)
    pairs = sorted({(abs(x), y) for x, y in P}, key=lambda ab: -ab[1])
    assert len(pairs) == 16
    return pairs


def build(pairs, axis_cs):
    pairs = sorted(pairs, key=lambda ab: -ab[1])
    if len({b for _, b in pairs}) != len(pairs) or any(a <= 0 for a, _ in pairs):
        return None
    pts = []
    for a, b in pairs:
        pts += [(-a, b), (a, b)]
    pts += [(0, c) for c in sorted(axis_cs, reverse=True)]
    if len(set(pts)) != len(pts):
        return None
    for p, q, r in itertools.combinations(pts, 3):
        if det3((1,) + p, (1,) + q, (1,) + r) == 0:
            return None
    return pts


def families(t, axis, rng, n):
    out = []
    base = load32()
    hs = sorted(b for _, b in base)
    # 1. 32-point 7-gon-free set plus an axis point / plus one pair
    want_struct = n // 3
    cand = []
    if axis == 1 and t == 16:
        cand += [hs[-1] + 1, hs[-1] + 1000, hs[0] - 1, hs[0] - 1000]
        cand += [(hs[i] + hs[i + 1]) // 2 for i in range(len(hs) - 1)]
        cand += [h + d for h in hs for d in (1, -1)]
        rng.shuffle(cand)
        for c in cand:
            if len(out) >= want_struct:
                break
            pts = build(base, [c])
            if pts:
                out.append(("sub32+axis c=%d" % c, pts))
    elif axis == 0 and t == 17:
        while len(out) < want_struct:
            a = rng.choice([1, 5, rng.randint(1, 700), rng.randint(1, 50)])
            b = rng.choice([rng.randint(-600, 650), rng.choice(hs) + rng.choice([1, -1])])
            pts = build(base + [(a, b)], [])
            if pts:
                out.append(("sub32+pair (%d,%d)" % (a, b), pts))
    # 2. random families, each with its own quota
    rest = n - len(out)
    quota = {"neardeg": rest // 4, "circle": rest // 4}
    quota["uniform"] = rest - quota["neardeg"] - quota["circle"]
    for mode, q in quota.items():
        got = 0
        attempts = 0
        while got < q and attempts < 20000:
            attempts += 1
            if mode == "uniform":
                Rr = rng.choice([100, 10 ** 4, 10 ** 8])
                pairs = [(rng.randint(1, Rr), rng.randint(-Rr, Rr)) for _ in range(t)]
                cs = [rng.randint(-2 * Rr, 2 * Rr) for _ in range(axis)]
            elif mode == "neardeg":
                # nearly equal pair heights (spacing 2), some pairs very close to the axis (distinct small a) or
                # very far, axis points one unit above/below a pair height
                b0 = rng.randint(-10 ** 6, 10 ** 6)
                hts = rng.sample(range(t + 6), t)
                small = rng.sample(range(1, 60), t)
                pairs = [(small[i] if rng.random() < 0.5 else rng.randint(10 ** 6, 10 ** 9), b0 + 2 * h)
                         for i, h in enumerate(hts)]
                cs = [rng.choice(pairs)[1] + rng.choice([-1, 1]) for _ in range(axis)]
            else:
                pairs = []
                for _ in range(t):
                    th = rng.uniform(-math.pi / 2, math.pi / 2)
                    r = 10 ** 7 * (1 + rng.uniform(-0.01, 0.01))
                    pairs.append((max(1, int(r * math.cos(th))), int(r * math.sin(th))))
                cs = [rng.randint(-10 ** 7, 10 ** 7) for _ in range(axis)]
            pts = build(pairs, cs)
            if pts:
                out.append((mode, pts))
                got += 1
    return out


def main():
    mp, t, axis, n, seed, outp, outj = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), \
        int(sys.argv[5]), sys.argv[6], sys.argv[7]
    assert n <= 64
    info = json.load(open(mp))
    nX = info["X_vars"]
    m = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    NP = 2 * t; N = NP + axis; Z = N
    assert info["N"] == N and info["Z"] == Z
    rng = random.Random(seed)
    confs = families(t, axis, rng, n)
    zero = {tuple(sorted((Z, 2 * o, 2 * o + 1))) for o in range(t)}
    with open(outp, "w") as f:
        f.write(f"{N} {NP} {nX} {len(confs)}\n")
        for name, pts in confs:
            vec = [(1, x, y) for x, y in pts] + [(0, 1, 0)]
            chi = {T: sgn(det3(*(vec[i] for i in T))) for T in itertools.combinations(range(N + 1), 3)}
            assert {T for T, s in chi.items() if s == 0} == zero
            val = {}
            for T, (v, s) in m.items():
                x = chi[T] * s
                assert val.setdefault(v, x) == x, "class inconsistent"
            assert sorted(val) == list(range(1, nX + 1))
            f.write("".join("1" if val[v] == 1 else "0" for v in range(1, nX + 1)) + "\n")
            f.write("".join("+" if chi[T] == 1 else "-" for T in itertools.combinations(range(N), 3)) + "\n")
    json.dump([{"family": name, "points": pts} for name, pts in confs], open(outj, "w"))
    print(f"{len(confs)} configurations written; families:",
          {k: sum(1 for nm, _ in confs if nm.split()[0] == k) for k in {nm.split()[0] for nm, _ in confs}})


if __name__ == "__main__":
    main()
