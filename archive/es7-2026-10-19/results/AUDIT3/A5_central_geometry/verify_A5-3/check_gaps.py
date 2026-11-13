#!/usr/bin/env python3
"""Independent check of audit finding A5-3 (wording of the 'canonical cases' argument).

Claim under test (C2C34/README.md sec. 2, SYMZ/README.md 147-151):
  "The numbers of antipodal classes between consecutive hull vertices form a cyclic sequence
   [SYMZ: of two or three positive integers] summing to 17 ... least under rotation and reversal:
   8 quadrilaterals and 24 hexagons (canonical.txt)."

Part 1 (combinatorial, all 136 cases of hullcubes.py, t = 17):
  index gaps g, classes strictly between s = g - 1, full-polygon strict point counts; sums,
  positivity, canonical sets under the dihedral action for g and for s, vs canonical.txt / cubes.txt.
Part 2 (geometric, exact integers): for every one of the 136 cases build random centrally symmetric
  34-point sets in general position realizing it, then from EVERY hull vertex of the set and of its
  mirror image recompute the angular normal form of zcnf.py --hull from scratch (class 0 = start
  vertex, representatives in the open half-plane left of c -> start, sorted ccw), and count
  geometrically the classes strictly between consecutive hull vertices.
usage: check_gaps.py RESULTS_DIR [instances_per_case] [seed]
"""
import functools, itertools, math, random, sys

R = sys.argv[1]
INST = int(sys.argv[2]) if len(sys.argv) > 2 else 3
random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 20261101)
T = 17
fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


canon_file = [l.strip() for l in open(f"{R}/C2C34/canonical.txt") if l.strip()]
cube_names = [l.split()[0] for l in open(f"{R}/C2C34/cubes.txt") if l.strip()]


def cases():
    for a in range(1, T):
        yield f"P{a}", (0, a)
    for a, b in itertools.combinations(range(1, T), 2):
        yield f"H{a}-{b}", (0, a, b)


def name_of(K):
    K = sorted(K)
    assert K[0] == 0
    return f"P{K[1]}" if len(K) == 2 else f"H{K[1]}-{K[2]}"


def gaps(K):
    K = sorted(K)
    return tuple((K[(i + 1) % len(K)] - K[i]) % T for i in range(len(K)))


def strict(K):
    return tuple(g - 1 for g in gaps(K))


def full_strict(K):
    pos = sorted(list(K) + [k + T for k in K])            # positions in the 34-point angular cycle
    n = len(pos)
    return tuple((pos[(i + 1) % n] - pos[i]) % (2 * T) - 1 for i in range(n))


def dihedral(seq):
    n = len(seq)
    rs = seq[::-1]
    return [tuple(seq[(i + k) % n] for k in range(n)) for i in range(n)] + \
           [tuple(rs[(i + k) % n] for k in range(n)) for i in range(n)]


def canon(seq):
    return min(dihedral(seq))


def name_from_gaps(g):
    if len(g) == 2:
        return f"P{g[0]}"
    return f"H{g[0]}-{g[0] + g[1]}"


# ---------------- Part 1 ----------------
allc = list(cases())
check([n for n, _ in allc] == cube_names, "case list differs from cubes.txt order/names")
sum_g, sum_s, sum_full, zero_s = {}, {}, {}, []
can_g, can_s = set(), set()
for nm, K in allc:
    g, s, fs = gaps(K), strict(K), full_strict(K)
    sum_g.setdefault(sum(g), []).append(nm)
    sum_s.setdefault((len(K), sum(s)), []).append(nm)
    sum_full.setdefault((len(K), sum(fs)), []).append(nm)
    check(min(g) >= 1, f"{nm}: index gap not positive {g}")
    if min(s) == 0:
        zero_s.append(nm)
    if canon(g) == g:
        can_g.add(nm)
    if canon(s) == s:
        can_s.add(nm)
print("Part 1: 136 cases =", len(allc), "; matches cubes.txt:", [n for n, _ in allc] == cube_names)
print("  sums of index gaps g:", {k: len(v) for k, v in sum_g.items()})
print("  sums of classes strictly between s = g-1, keyed (hull classes, sum):",
      {k: len(v) for k, v in sum_s.items()})
print("  sums of points strictly between consecutive vertices of the full polygon:",
      {k: len(v) for k, v in sum_full.items()})
print("  cases where some 'classes strictly between' count is 0 (so not 'positive'):", len(zero_s),
      "e.g.", zero_s[:4])
print("  examples: P1 g=%s s=%s | P8 g=%s s=%s | H1-2 g=%s s=%s | H5-11 g=%s s=%s" % (
    gaps((0, 1)), strict((0, 1)), gaps((0, 8)), strict((0, 8)), gaps((0, 1, 2)), strict((0, 1, 2)),
    gaps((0, 5, 11)), strict((0, 5, 11))))
cf = set(canon_file)
print("  canonical by gaps:   %d P + %d H; equals canonical.txt: %s" % (
    sum(n[0] == 'P' for n in can_g), sum(n[0] == 'H' for n in can_g), can_g == cf))
print("  canonical by strict: %d P + %d H; equals canonical.txt: %s" % (
    sum(n[0] == 'P' for n in can_s), sum(n[0] == 'H' for n in can_s), can_s == cf))
check(set(sum_g) == {17}, "index gaps do not always sum to 17")
check(set(sum_s) == {(2, 15), (3, 14)}, "strict sums not 15/14")
check(can_g == cf and can_s == cf, "canonical sets differ")
# the s <-> g bijection commutes with rotation/reversal, so orbits correspond one to one
orb_g = {canon(gaps(K)) for _, K in allc}
orb_s = {canon(strict(K)) for _, K in allc}
check(len(orb_g) == len(orb_s) == 32, "orbit counts")
print("  dihedral orbits: by g %d, by s %d" % (len(orb_g), len(orb_s)))


# ---------------- Part 2 ----------------
def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def general_position(P):
    for a, b, c in itertools.combinations(P, 3):
        if orient(a, b, c) == 0:
            return False
    return True


def hull_ccw(P):
    pts = sorted(set(P))
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def labelling(P, h):
    """normal form of zcnf.py rot m=2 --hull with start point h: index of every point's class."""
    neg = lambda p: (-p[0], -p[1])
    reps = []
    for p in P:
        if p == h or p == neg(h):
            continue
        cr = cross(h, p)
        assert cr != 0
        if cr > 0:
            reps.append(p)
    assert len(reps) == T - 1
    reps.sort(key=functools.cmp_to_key(lambda p, q: -1 if cross(p, q) > 0 else 1))
    for i in range(len(reps) - 1):            # strict angular order inside the open half-plane
        assert cross(reps[i], reps[i + 1]) > 0
    idx = {h: 0, neg(h): 0}
    for i, p in enumerate(reps, 1):
        idx[p] = i
        idx[neg(p)] = i
    return idx


def geometric_strict(P, hull, start):
    """points strictly (angularly about c) between consecutive hull vertices, ccw from start."""
    j = hull.index(start)
    V = hull[j:] + hull[:j]
    out = []
    for i in range(len(V)):
        u, w = V[i], V[(i + 1) % len(V)]
        assert cross(u, w) > 0                # c strictly inside: consecutive vertices subtend < pi
        out.append(sum(1 for p in P if p not in (u, w) and cross(u, p) > 0 and cross(p, w) > 0))
    return out


def build(K, scale=10 ** 6, tries=200):
    """random 34-point centrally symmetric set about (0,0) realizing case K from its first hull vertex."""
    k = len(K)
    g = gaps(K)
    for _ in range(tries):
        base = [math.pi * j / k for j in range(k)]
        th = [0.0] + [base[j] + random.uniform(-0.25, 0.25) * math.pi / k for j in range(1, k)]
        rr = scale * random.uniform(0.9, 1.1)
        hullv = [(round(rr * math.cos(t)), round(rr * math.sin(t))) for t in th]
        bounds = th + [math.pi]
        inner = []
        for j in range(k):
            lo_, hi_ = bounds[j], bounds[j + 1]
            width = hi_ - lo_
            for _ in range(g[j] - 1):
                phi = random.uniform(lo_ + 0.02 * width, hi_ - 0.02 * width)
                r = rr * random.uniform(0.05, 0.6) * math.cos(width / 2)
                inner.append((round(r * math.cos(phi)), round(r * math.sin(phi))))
        half = hullv + inner
        P = half + [(-x, -y) for x, y in half]
        if len(set(P)) != 2 * T or not general_position(P):
            continue
        H = hull_ccw(P)
        if len(H) != 2 * k or set(H) != set(hullv) | {(-x, -y) for x, y in hullv}:
            continue
        return P, hullv[0]
    raise RuntimeError(f"could not build case {K}")


n_conf = n_lab = 0
seen_cases = set()
for nm, K in allc:
    k = len(K)
    for inst in range(INST):
        P, h0 = build(K)
        n_conf += 1
        variants = [("orig", P), ("mirror", [(-x, y) for x, y in P])]
        seqs = {}
        reached = set()
        for tag, Q in variants:
            H = hull_ccw(Q)
            check(len(H) == 2 * k, f"{nm}: hull size")
            for v in H:
                idx = labelling(Q, v)
                Kv = sorted({idx[u] for u in H})
                case_v = name_of(Kv)
                reached.add(case_v)
                n_lab += 1
                gs = geometric_strict(Q, H, v)
                # half-turn part: the first k sectors (from v to -v)
                check(tuple(gs[:k]) == strict(Kv), f"{nm} {tag}: geometric strict {gs[:k]} != {strict(Kv)}")
                check(tuple(gs[k:]) == strict(Kv), f"{nm} {tag}: second half differs")
                check(sum(gs[:k]) == T - k, f"{nm} {tag}: strict half-turn sum {sum(gs[:k])}")
                check(sum(gs) == 2 * T - 2 * k, f"{nm} {tag}: full sum")
                check(sum(gaps(Kv)) == T, f"{nm} {tag}: gap sum")
                seqs[(tag, v)] = gaps(Kv)
            if tag == "orig":
                # start at the constructed first vertex reproduces the intended case
                check(name_of(sorted({labelling(Q, h0)[u] for u in H})) == nm, f"{nm}: construction")
                g0 = seqs[(tag, h0)]
                j0 = H.index(h0)
                for i in range(2 * k):        # starting at the i-th next vertex rotates the sequence by i
                    v = H[(j0 + i) % (2 * k)]
                    rot = tuple(g0[(i + m) % k] for m in range(k))
                    check(seqs[(tag, v)] == rot, f"{nm}: rotation claim fails at offset {i}")
        g0 = seqs[("orig", h0)]
        rev = set(dihedral(g0)[k:])               # rotations of the reversed sequence
        for (tag, v), s in seqs.items():
            if tag == "mirror":
                check(s in rev, f"{nm}: mirror sequence {s} not a reversal of {g0}")
        cn = name_from_gaps(canon(g0))
        check(cn in cf, f"{nm}: canonical {cn} not in canonical.txt")
        check(cn in reached, f"{nm}: canonical case {cn} not reached by any labelling")
        check(len(reached & cf) == 1, f"{nm}: reached canonical cases {sorted(reached & cf)}")
        seen_cases.add(nm)

print(f"Part 2: {n_conf} exact configurations ({INST} per case, all {len(seen_cases)} cases), "
      f"{n_lab} normal-form labellings (every hull vertex, original and mirror image)")
print("  in every labelling: classes strictly between consecutive hull classes sum to 17 - k "
      "(15 for k=2, 14 for k=3); index gaps sum to 17; start change = rotation; mirror = reversal;")
print("  the canonical case is reached and is the unique case from canonical.txt reached.")
print("FAILURES:", len(fails))
for f in fails[:20]:
    print("  ", f)
sys.exit(1 if fails else 0)
