#!/usr/bin/env python3
"""Independent exact-integer check of the index maps of reductions A and B (finding A5-2).

Written from scratch for this verification; it does not import any project or auditor code.

Model (angular normal form of C2C34/README.md section 1): 17 antipodal pairs about c = (0,0). The labelling started at
a point h of the set gives class 0 to {h, -h} with representative h; every other pair is represented by its point in
the open half-plane left of the directed line c -> h, and the representatives are numbered 1..16 by increasing angle
from h. A point gets the label (class, side), side 0 = representative, side 1 = antipode.

Claims checked, for every parallelogram-hull set and every one of its 4 hull vertices as the first point
(hull case P_a = the other hull class is a):
  A : restart at p_a (label (a,0)), no reflection:
      old (i,s) -> new ((i-a) mod 17, s xor [i < a]);  new hull case P_(17-a);
      second-layer class set V -> {(i-a) mod 17}.
  A': restart at -p_a (label (a,1)): same class map, side flips for i >= a.
  B : reflect (x,y) -> (-x,y), restart at the image of p_a:
      old (i,s) -> new ((a-i) mod 17, s xor [i > a]);  new hull case P_a;
      second-layer class set V -> {(a-i) mod 17}.
  B': reflect, restart at the image of -p_a: same class map, side flips for i <= a.
Also, in each labelling: the hull cube of P_a holds (every point not on a hull edge strictly left of each ccw hull
edge (0,0)->(a,0)->(0,1)->(a,1)), and, when the second layer has 4 or 6 vertices with class set V (sorted
v1<v2[<v3]), the second-layer cube holds: polygon (v1,0),(v2,0)[,(v3,0)],(v1,1),(v2,1)[,(v3,1)] in that order and
every other point of classes != 0,a strictly left of each edge.  Finally the cube of the predicted subcase holds in
the new labelling and no other subcase cube of the same case holds.
"""
import functools
import itertools
import random
import sys

T = 17


def det2(p, q):
    return p[0] * q[1] - p[1] * q[0]


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def neg(p):
    return (-p[0], -p[1])


def in_general_position(P):
    for a, b, c in itertools.combinations(P, 3):
        if orient(a, b, c) == 0:
            return False
    return True


def hull(P):
    """Strict convex hull, ccw (exact; general position assumed)."""
    pts = sorted(set(P))
    if len(pts) <= 2:
        return pts
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
    """dict point -> (class, side) for the normal form started at h; also returns list of representatives."""
    assert h in P
    reps = []
    seen = {h, neg(h)}
    for p in P:
        if p in seen:
            continue
        seen.add(p)
        seen.add(neg(p))
        d = det2(h, p)
        assert d != 0
        reps.append(p if d > 0 else neg(p))
    # increasing angle from h within the open upper half-plane relative to h: p before q iff det2(p,q) > 0
    reps.sort(key=functools.cmp_to_key(lambda p, q: -1 if det2(p, q) > 0 else 1))
    reps = [h] + reps
    assert len(reps) == T
    lab = {}
    for i, r in enumerate(reps):
        lab[r] = (i, 0)
        lab[neg(r)] = (i, 1)
    assert len(lab) == 2 * T
    # sanity: representatives strictly ccw-sorted, all in open left half-plane
    for i in range(1, T):
        assert det2(h, reps[i]) > 0
        if i > 1:
            assert det2(reps[i - 1], reps[i]) > 0
    return lab, reps


def point_of(reps, lbl):
    i, s = lbl
    return reps[i] if s == 0 else neg(reps[i])


def cube_holds(P, reps, poly_labels, inner_labels):
    """every point of inner_labels other than the edge's endpoints strictly left of each edge of poly (in order)."""
    poly = [point_of(reps, l) for l in poly_labels]
    inner = [point_of(reps, l) for l in inner_labels]
    k = len(poly)
    for e in range(k):
        u, w = poly[e], poly[(e + 1) % k]
        for x in inner:
            if x == u or x == w:
                continue
            if orient(u, w, x) <= 0:
                return False
    return True


def hull_cube_holds(P, reps, a):
    poly = [(0, 0), (a, 0), (0, 1), (a, 1)]
    allp = [(i, s) for i in range(T) for s in (0, 1)]
    return cube_holds(P, reps, poly, allp)


def l2_cube_holds(P, reps, a, V):
    V = sorted(V)
    poly = [(v, 0) for v in V] + [(v, 1) for v in V]
    inner = [(i, s) for i in range(1, T) if i != a for s in (0, 1)]
    return cube_holds(P, reps, poly, inner)


def hull_case(P, lab):
    H = hull(P)
    cls = sorted({lab[p][0] for p in H})
    return H, cls


def second_layer(P, H):
    rest = [p for p in P if p not in set(H)]
    return hull(rest)


def make_set(rng, a_target, l2_kind):
    """Random centrally symmetric 34-point set with a parallelogram hull; aims at hull case a_target from the
    first hull vertex and a second layer with l2_kind pairs (2 or 3) or random (0). Returns None on failure."""
    R = 10 ** 6
    # hull vertices u (angle ~0) and w (angle phi in (0, pi))
    for _ in range(50):
        u = (R + rng.randint(-R // 20, R // 20), rng.randint(-R // 20, R // 20))
        phi_pt = (rng.randint(-R, R), rng.randint(R // 10, R))
        if det2(u, phi_pt) <= 0:
            continue
        w = phi_pt
        par = [u, w, neg(u), neg(w)]
        if hull(par) and len(hull(par)) == 4:
            break
    else:
        return None
    # points strictly inside the parallelogram as convex combos with random barycentric weights
    def inside(scale):
        while True:
            x, y = rng.random() * 2 - 1, rng.random() * 2 - 1  # coefficients of u and w
            if abs(x) + abs(y) < 0.999:  # strictly inside the parallelogram conv(+-u, +-w)
                x *= scale
                y *= scale
                p = (int(x * u[0] + y * w[0]), int(x * u[1] + y * w[1]))
                if p != (0, 0):
                    return p
    need_low = a_target - 1  # representatives with angle in (0, angle(w))
    need_high = 16 - a_target
    pairs = []
    low = high = 0
    tries = 0
    l2n = l2_kind
    while len(pairs) < 15 and tries < 20000:
        tries += 1
        k = len(pairs)
        scale = 0.97 if k < l2n else (0.35 if l2n else rng.choice([0.3, 0.6, 0.9]))
        p = inside(scale)
        r = p if det2(u, p) > 0 else neg(p)
        if det2(u, r) == 0:
            continue
        is_low = det2(r, w) > 0
        if is_low and low < need_low:
            low += 1
            pairs.append(r)
        elif (not is_low) and high < need_high:
            high += 1
            pairs.append(r)
    if len(pairs) < 15:
        return None
    P = [u, neg(u), w, neg(w)]
    for r in pairs:
        P += [r, neg(r)]
    if len(set(P)) != 34 or not in_general_position(P):
        return None
    if len(hull(P)) != 4:
        return None
    return P


def main():
    nsets = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 20261101
    rng = random.Random(seed)
    stats = dict(sets=0, labellings=0, A=0, Aprime=0, B=0, Bprime=0, l2_4=0, l2_6=0, l2_big=0,
                 subcase_A=0, subcase_B=0, unique_subcase=0)
    seen_aV = set()
    fails = []
    gen_fail = 0
    while stats["sets"] < nsets:
        a_target = rng.randint(1, 16)
        l2_kind = rng.choice([0, 2, 2, 3, 3])
        P = make_set(rng, a_target, l2_kind)
        if P is None:
            gen_fail += 1
            continue
        stats["sets"] += 1
        H = hull(P)
        L2 = second_layer(P, H)
        for h in H:
            lab, reps = labelling(P, h)
            stats["labellings"] += 1
            Hc = sorted({lab[p] for p in H})
            # hull vertices must be (0,0),(0,1),(a,0),(a,1)
            hcls = sorted({c for c, _ in Hc})
            if len(hcls) != 2 or hcls[0] != 0 or len(Hc) != 4:
                fails.append(("hull labels", Hc))
                continue
            a = hcls[1]
            if not hull_cube_holds(P, reps, a):
                fails.append(("hull cube fails", a))
            for b in range(1, T):
                if b != a and hull_cube_holds(P, reps, b):
                    fails.append(("second hull cube holds", a, b))
            V = sorted({lab[p][0] for p in L2})
            if len(L2) in (4, 6):
                stats["l2_4" if len(L2) == 4 else "l2_6"] += 1
                seen_aV.add((a, tuple(V)))
                if 0 in V or a in V or len(V) * 2 != len(L2):
                    fails.append(("l2 classes", a, V))
                if not l2_cube_holds(P, reps, a, V):
                    fails.append(("l2 cube fails", a, V))
                # no other subcase cube of P_a holds
                others = [W for k in (2, 3) for W in itertools.combinations([o for o in range(1, T) if o != a], k)
                          if list(W) != V and l2_cube_holds(P, reps, a, W)]
                if others:
                    fails.append(("another l2 cube holds", a, V, others[:3]))
                else:
                    stats["unique_subcase"] += 1
            else:
                stats["l2_big"] += 1
            pa = point_of(reps, (a, 0))
            # ---- A and A' (no reflection) ----
            for start, flip_rule, key in ((pa, lambda i: i < a, "A"), (neg(pa), lambda i: i >= a, "Aprime")):
                lab2, reps2 = labelling(P, start)
                ok = True
                for x in P:
                    i, s = lab[x]
                    j, s2 = lab2[x]
                    if j != (i - a) % T or s2 != (s ^ int(flip_rule(i))):
                        ok = False
                        fails.append((key, "point map", a, (i, s), (j, s2)))
                        break
                Hc2 = sorted({lab2[p][0] for p in H})
                if Hc2 != [0, T - a]:
                    ok = False
                    fails.append((key, "hull case", a, Hc2))
                if not hull_cube_holds(P, reps2, T - a):
                    ok = False
                    fails.append((key, "new hull cube fails", a))
                if len(L2) in (4, 6):
                    V2 = sorted({lab2[p][0] for p in L2})
                    if V2 != sorted((i - a) % T for i in V):
                        ok = False
                        fails.append((key, "V map", a, V, V2))
                    if not l2_cube_holds(P, reps2, T - a, V2):
                        ok = False
                        fails.append((key, "new l2 cube fails", a, V2))
                    elif key == "A":
                        stats["subcase_A"] += 1
                if ok:
                    stats[key] += 1
            # ---- B and B' (reflection (x,y) -> (-x,y)) ----
            sig = lambda p: (-p[0], p[1])
            Ps = [sig(p) for p in P]
            Hs = [sig(p) for p in H]
            L2s = [sig(p) for p in L2]
            for start, flip_rule, key in ((sig(pa), lambda i: i > a, "B"), (sig(neg(pa)), lambda i: i <= a, "Bprime")):
                lab3, reps3 = labelling(Ps, start)
                ok = True
                for x in P:
                    i, s = lab[x]
                    j, s3 = lab3[sig(x)]
                    if j != (a - i) % T or s3 != (s ^ int(flip_rule(i))):
                        ok = False
                        fails.append((key, "point map", a, (i, s), (j, s3)))
                        break
                Hc3 = sorted({lab3[p][0] for p in Hs})
                if Hc3 != [0, a]:
                    ok = False
                    fails.append((key, "hull case", a, Hc3))
                if not hull_cube_holds(Ps, reps3, a):
                    ok = False
                    fails.append((key, "new hull cube fails", a))
                if len(L2) in (4, 6):
                    V3 = sorted({lab3[p][0] for p in L2s})
                    if V3 != sorted((a - i) % T for i in V):
                        ok = False
                        fails.append((key, "V map", a, V, V3))
                    if not l2_cube_holds(Ps, reps3, a, V3):
                        ok = False
                        fails.append((key, "new l2 cube fails", a, V3))
                    elif key == "B":
                        stats["subcase_B"] += 1
                if ok:
                    stats[key] += 1
        if stats["sets"] % 100 == 0:
            print(f"{stats['sets']} sets, fails {len(fails)}", flush=True)
    hull_cases = sorted({a for a, _ in seen_aV})
    print("seed", seed, "generation retries", gen_fail)
    print("stats", stats)
    print("distinct (a, V) with 4/6-vertex second layer:", len(seen_aV), "; hull cases seen:", hull_cases)
    print("FAILURES", len(fails))
    for f in fails[:30]:
        print("  ", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
