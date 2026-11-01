#!/usr/bin/env python3
"""Independent exact test of the two solved fivefold CNFs on a real 35-point fivefold set (written from scratch,
no code from the repository or the auditor).

Geometry: exact arithmetic in Z[zeta], zeta = exp(2 pi i / 5). An element is a length-5 integer vector c with value
sum c_k zeta^k (modulo the all-ones vector, since 1+zeta+...+zeta^4 = 0). Rotation by 72 degrees = cyclic shift.
orient(p,q,r) = sign Im(conj(q-p)(r-p)); Im(sum c_k zeta^k) = sin36 * ((c1-c4) phi + (c2-c3)), phi = (1+sqrt5)/2,
whose sign is decided exactly with integers.

Configuration: 7 nested pentagons (radius ratio 0.72 < cos 36 deg, random rotations), centre c = 0 as the auxiliary
point. Checks general position of all 36 points exactly, peels the convex layers exactly, labels the set in
  - angle normal form (P1): orbit 0 and (0,0) chosen, (o,0) = the point of orbit o in the open sector from the ray
    c->(0,0) to the ray c->(0,1), orbits 1..6 sorted counter-clockwise;
  - layer normal form (L1): orbit o = o-th layer, same sector representatives;
assigns every triple-orbit variable from the real chirotope (checking consistency over each orbit), then streams the
CNF: every clause on triple variables only must hold; the conv_r variables get their least model by forward chaining
in file order; a K-set clause is violated iff all its conv_6 literals are true. The number of violated K-set clauses
must equal (number of convex 7-subsets)/5, counted independently by a DFS with exact inside-triangle masks.

usage: realtest.py CNF MAP.json {angle|layer} SEED [orbit0_layer_index] [--mutate]
"""
import itertools
import json
import math
import random
import sys

M = 5


# ---------------- Z[zeta5] exact arithmetic ----------------
def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b):
    c = [0] * M
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[(i + j) % M] += x * y
    return tuple(c)


def conj(a):
    return tuple(a[(-k) % M] for k in range(M))


def rot(a, k=1):
    """multiply by zeta^k: coefficient of zeta^i moves to zeta^(i+k)"""
    return tuple(a[(i - k) % M] for i in range(M))


def sign_im(w):
    d1 = w[1] - w[4]
    d2 = w[2] - w[3]
    A = d1 + 2 * d2          # 2*((d1) phi + d2) = A + d1 sqrt5
    B = d1
    if A >= 0 and B >= 0:
        return 0 if (A == 0 and B == 0) else 1
    if A <= 0 and B <= 0:
        return -1
    t = A * A - 5 * B * B
    if A > 0:                # B < 0
        return (t > 0) - (t < 0)
    return (-t > 0) - (-t < 0)   # A < 0 < B


def orient(p, q, r):
    return sign_im(mul(conj(sub(q, p)), sub(r, p)))


def numeric(a):
    z = complex(0, 0)
    for k, x in enumerate(a):
        z += x * complex(math.cos(2 * math.pi * k / M), math.sin(2 * math.pi * k / M))
    return z


def from_complex(z, scale=1):
    """an element of Z[zeta] near z (uses basis 1, zeta)"""
    s72 = math.sin(2 * math.pi / M)
    c72 = math.cos(2 * math.pi / M)
    y = z.imag / s72
    x = z.real - y * c72
    return (round(x), round(y), 0, 0, 0)


# ---------------- configuration ----------------
def build(seed):
    rng = random.Random(seed)
    bases = []
    R = 10 ** 7
    for o in range(7):
        th = rng.uniform(0, 2 * math.pi)
        bases.append(from_complex(complex(R * math.cos(th), R * math.sin(th))))
        R = R * 0.72
    order = list(range(7))
    rng.shuffle(order)       # the orbits are listed in random order (the labelling must find the layers itself)
    return [bases[i] for i in order]


def hull_vertices(pts):
    """exact convex hull vertex set (general position assumed): p is a vertex iff it is not inside any triangle"""
    idx = list(range(len(pts)))
    verts = []
    for i in idx:
        inside = False
        others = [j for j in idx if j != i]
        for a, b, c in itertools.combinations(others, 3):
            o1 = orient(pts[a], pts[b], pts[i])
            if o1 == orient(pts[b], pts[c], pts[i]) == orient(pts[c], pts[a], pts[i]):
                inside = True
                break
        if not inside:
            verts.append(i)
    return verts


def main():
    cnf, mapf, form, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    orbit0_layer = int(sys.argv[5]) if len(sys.argv) > 5 and not sys.argv[5].startswith("--") else 0
    mutate = "--mutate" in sys.argv
    info = json.load(open(mapf))
    assert info["m"] == M and info["N"] == 35 and info["center_index"] == 35
    X = info["X_vars"]
    bases = build(seed)
    zero = (0,) * M
    allpts = [rot(b, r) for b in bases for r in range(M)] + [zero]   # provisional order, centre last
    # exact general position of all 36 points
    for a, b, c in itertools.combinations(range(36), 3):
        assert orient(allpts[a], allpts[b], allpts[c]) != 0, ("collinear", a, b, c)
    # exact layers of the 35 set points
    rem = list(range(35))
    layers = []
    while rem:
        hv = hull_vertices([allpts[i] for i in rem])
        layer = sorted(rem[j] for j in hv)
        layers.append(layer)
        rem = [i for i in rem if i not in set(layer)]
    orbit_of = {i: i // M for i in range(35)}
    layer_orbits = [sorted({orbit_of[i] for i in L}) for L in layers]
    assert all(len(L) == M and len(o) == 1 for L, o in zip(layers, layer_orbits)), layer_orbits
    layer_seq = [o[0] for o in layer_orbits]          # provisional orbit index of layer 0, 1, ...
    # choose orbit 0 and its point (0,0)
    o0 = layer_seq[orbit0_layer]
    p00 = bases[o0]
    p01 = rot(p00)
    c = zero

    def sector_rep(b):
        reps = [rot(b, r) for r in range(M) if orient(c, p00, rot(b, r)) > 0 and orient(c, p01, rot(b, r)) < 0]
        assert len(reps) == 1
        return reps[0]

    others = [o for o in range(7) if o != o0]
    if form == "angle":
        reps = {o: sector_rep(bases[o]) for o in others}
        # sort counter-clockwise inside the sector: p before q iff orient(c,p,q) > 0
        import functools
        seq = sorted(others, key=functools.cmp_to_key(lambda a, b: -orient(c, reps[a], reps[b])))
        order = [o0] + seq
    elif form == "layer":
        assert orbit0_layer == 0
        order = layer_seq
        reps = {o: sector_rep(bases[o]) for o in others}
    else:
        raise SystemExit("form must be angle or layer")
    rep = {o0: p00}
    rep.update(reps)
    if mutate:   # swap the labels of two orbits (wrong labelling, must violate a normal-form unit)
        order = [order[0], order[2], order[1]] + order[3:]
    pts = [rot(rep[o], r) for o in order for r in range(M)] + [zero]   # index o*5+r = (o,r), 35 = c
    # assign triple-orbit variables
    val = [0] * (info["vars"] + 1)
    for a, b, cc, v, s in info["triples"]:
        x = s * orient(pts[a], pts[b], pts[cc])
        if val[v] == 0:
            val[v] = x
        else:
            assert val[v] == x, ("orbit inconsistency", a, b, cc, v)
    assert all(val[v] != 0 for v in range(1, X + 1))
    # stream the CNF
    true_aux = bytearray(info["vars"] + 1)
    n_tri = n_tri_bad = n_def4 = n_defr = n_k = n_k_bad = 0
    bad_examples = []
    last_head_r = 0
    seen_r = False
    with open(cnf) as f:
        for line in f:
            if line[0] in "cp":
                continue
            lits = list(map(int, line.split()))
            assert lits[-1] == 0
            lits.pop()
            if all(abs(l) <= X for l in lits):
                n_tri += 1
                if not any((val[l] > 0) if l > 0 else (val[-l] < 0) for l in lits):
                    n_tri_bad += 1
                    if len(bad_examples) < 5:
                        bad_examples.append(lits)
                continue
            pos_aux = [l for l in lits if l > X]
            if len(pos_aux) == 1:
                h = pos_aux[0]
                body = [l for l in lits if l != h]
                if all(abs(l) <= X for l in body):        # conv_4 definition: pattern -> head
                    assert not seen_r, "conv_4 definition after a conv_r definition"
                    n_def4 += 1
                    if all(not ((val[l] > 0) if l > 0 else (val[-l] < 0)) for l in body):
                        true_aux[h] = 1
                else:                                     # conv_r definition: AND body -> head
                    assert all(l < 0 and -l > X and -l < h for l in body), lits
                    assert h > last_head_r
                    last_head_r = h
                    seen_r = True
                    n_defr += 1
                    if all(true_aux[-l] for l in body):
                        true_aux[h] = 1
            elif len(pos_aux) == 0 and all(l < 0 and -l > X for l in lits):
                n_k += 1
                if all(true_aux[-l] for l in lits):
                    n_k_bad += 1
            else:
                raise SystemExit(f"unexpected clause shape: {lits}")
    print(f"form={form} seed={seed} orbit0_layer={orbit0_layer} mutate={mutate}")
    print(f"  layer sequence (provisional orbit ids, outermost first): {layer_seq}; label order {order}")
    print(f"  triple-only clauses: {n_tri}, violated: {n_tri_bad} {bad_examples}")
    print(f"  conv4 defs: {n_def4}, conv_r defs: {n_defr}, K-set clauses: {n_k}, violated: {n_k_bad}")
    if mutate:
        return
    # independent count of convex 7-subsets of the 35 set points
    P = pts[:35]
    n = 35
    inside = {}
    for a, b, cc in itertools.combinations(range(n), 3):
        o = orient(P[a], P[b], P[cc])
        mask = 0
        for x in range(n):
            if x in (a, b, cc):
                continue
            if orient(P[a], P[b], P[x]) == o and orient(P[b], P[cc], P[x]) == o and orient(P[cc], P[a], P[x]) == o:
                mask |= 1 << x
        inside[(a, b, cc)] = mask
    cnt = [0] * 8

    def dfs(T, Tmask, U, start):
        k = len(T)
        cnt[k] += 1
        if k == 7:
            return
        for x in range(start, n):
            if (U >> x) & 1:
                continue
            add = 0
            for i, j in itertools.combinations(T, 2):
                add |= inside[(i, j, x)]          # i < j < x
            if add & Tmask:
                continue
            dfs(T + [x], Tmask | (1 << x), U | add, x + 1)

    dfs([], 0, 0, 0)
    print(f"  convex k-subsets k=4..7: {cnt[4:]}; convex 7-subsets / 5 = {cnt[7] / 5}; K-set violations {n_k_bad}")
    print("  MATCH" if cnt[7] == 5 * n_k_bad and n_tri_bad == 0 else "  MISMATCH")


if __name__ == "__main__":
    main()
