#!/usr/bin/env python3
"""C3-S: hull normalization for the 3-fold class (centre-pencil normal form of C3a/C3b).

Labels 0..n-1 (n = 3m) by direction of the line through the centre c, R(i) = (i - m) mod n
(R = rotation by +120 deg), sigma_i = [x_i < 0], sigma_{r+m} = 1 - sigma_r, sigma_{r+2m} = sigma_r.

WLOG (see ../README.md): label 0 is a vertex of conv(S) and sigma_0 = 0.  The hull vertex set
H is R-invariant, has 3 or 6 elements when there is no convex 7-gon (k <= 9 here: |H| <= k-1 < 9
and 3 | |H|), and
  H3        : H = {0, m, 2m}
  H6(a, s)  : H = {0, m, 2m, a, a+m, a+2m}, 1 <= a <= m // 2 (a and m - a are exchanged by
              moving label 0 to the other hull orbit), s = sigma_a.
Counter-clockwise order of H (= angular order about c, which is interior to conv(S)):
  H3        : 0, 2m, m
  H6(a, 0)  : 0, a, 2m, a+2m, m, a+m
  H6(a, 1)  : 0, a+m, 2m, a, m, a+2m
Case clauses: sigma_a = s (H6), and ccw(u, v, w) for every directed hull edge (u, v) and every
other point w (strictly left of every edge <=> H is the hull in this cyclic order).
"""


def cases(m, k):
    assert 5 <= k <= 9, "hull sizes 3 and 6 only"
    out = [("H3",)]
    if k - 1 >= 6:
        for a in range(1, m // 2 + 1):
            for s in (0, 1):
                out.append(("H6", a, s))
    return out


def case_name(c):
    return "H3" if c[0] == "H3" else f"H6a{c[1]}s{c[2]}"


def parse_case(name):
    if name == "H3":
        return ("H3",)
    assert name.startswith("H6a")
    a, s = name[3:].split("s")
    return ("H6", int(a), int(s))


def hull_order(m, c):
    if c[0] == "H3":
        return [0, 2 * m, m]
    _, a, s = c
    assert 1 <= a <= m // 2 and s in (0, 1)
    if s == 0:
        return [0, a, 2 * m, a + 2 * m, m, a + m]
    return [0, a + m, 2 * m, a, m, a + 2 * m]


def hull_clauses(m, c, ccw, sig_true):
    """ccw(p,q,r): literal 'p,q,r counter-clockwise in S';  sig_true(i): literal 'sigma_i = 1'."""
    n = 3 * m
    cl = []
    if c[0] == "H6":
        lit = sig_true(c[1])
        cl.append([lit if c[2] else -lit])
    H = hull_order(m, c)
    for t in range(len(H)):
        u, v = H[t], H[(t + 1) % len(H)]
        for w in range(n):
            if w != u and w != v:
                cl.append([ccw(u, v, w)])
    return cl


# ---------------------------------------------------------------------------------------------
# Convex layers (generalization).  A layer spec is a list of layers L1, L2, ...; each layer is a
# list of (residue, sigma) pairs (sigma None for a one-orbit layer below the top).  Layer L_j is
# the hull vertex set of P_j = S minus (L_1 .. L_{j-1}); it is R-invariant, has 3 or 6 points
# (no convex 7-gon) and contains c in its interior, so its ccw order is the angular order about
# c, i.e. the order of the keys (sigma_i, i).  For one orbit {r, r+m, r+2m} that cyclic order is
# r, r+2m, r+m whatever sigma_r is, so one-orbit layers need no sigma.
# Name: layers joined by '_', residues of a layer by '-', sigma as suffix 's0'/'s1'.
# The top layer always carries sigma (label 0 has sigma 0), as legacy_to_layers and tree_children
# build it:
#   "0s0" = H3,  "0s0-2s1" = H6a2s1,  "0s0_5" = H3 then L2 = orbit 5,
#   "0s0_3s0-7s1" = H3 then L2 = orbits 3, 7.
# (C3-S comments and C3-S/README.md wrote these as "0", "0-2s1", "0_5", "0_3s0-7s1"; those strings
# are not the tree's names: compose.py never counts them, and "0-2s1" is not even a valid layer.)


def parse_layers(name):
    out = []
    for lay in name.split("_"):
        L = []
        for tok in lay.split("-"):
            if "s" in tok:
                r, s = tok.split("s")
                L.append((int(r), int(s)))
            else:
                L.append((int(tok), None))
        out.append(L)
    return out


def layers_name(layers):
    return "_".join("-".join(f"{r}" if s is None else f"{r}s{s}" for r, s in L) for L in layers)


def legacy_to_layers(c):
    return [[(0, 0)]] if c[0] == "H3" else [[(0, 0), (c[1], c[2])]]


def layer_order(m, L):
    if len(L) == 1:
        r = L[0][0]
        return [r, r + 2 * m, r + m]
    key = []
    for r, s in L:
        assert s is not None
        for w, i in enumerate((r, r + m, r + 2 * m)):
            key.append(((s if w != 1 else 1 - s), i))
    return [i for _, i in sorted(key)]


def layer_clauses(m, layers, ccw, sig_true):
    n = 3 * m
    used = set()
    cl = []
    for L in layers:
        for r, s in L:
            if s is not None and r != 0:
                lit = sig_true(r)
                cl.append([lit if s else -lit])
        H = layer_order(m, L)
        rest = [w for w in range(n) if w not in used]
        for t in range(len(H)):
            u, v = H[t], H[(t + 1) % len(H)]
            for w in rest:
                if w != u and w != v:
                    cl.append([ccw(u, v, w)])
        used |= set(H)
    return cl


def layer2_options(m, top):
    """all second layers below top layer `top` (list of (r, s)), as lists of (r, s)."""
    rem = [r for r in range(m) if r not in {r for r, _ in top}]
    out = [[(r, None)] for r in rem]
    for i, b in enumerate(rem):
        for c in rem[i + 1:]:
            for sb in (0, 1):
                for sc in (0, 1):
                    out.append([(b, sb), (c, sc)])
    return out


# ---------------------------------------------------------------------------------------------
# Mirror reduction inside H3 (see ../soundness.md, Lemma 5).  The reflection (x, y) -> (-x, y) in
# the frame of l maps S to a set of the class; with l turned just past the image of label 0 the
# labels map i -> (-i) mod n and sigma -> 1 - sigma (label 0 keeps sigma 0), so the top case H3 is
# kept and a layer with residues r (sigma s) maps to residues m - r (sigma 1 - s).


def mirror_layer(m, L):
    return sorted(((m - r) % m, (None if s is None else 1 - s)) for r, s in L)


def h3_layer2_kept(m):
    """layer-2 options below H3 kept by the mirror reduction: O kept iff key(O) <= key(mirror(O))."""
    key = lambda L: tuple((r, -1 if s is None else s) for r, s in sorted(L))
    return [o for o in layer2_options(m, [(0, 0)]) if key(o) <= key(mirror_layer(m, o))]


# ---------------------------------------------------------------------------------------------
# Mirror reduction below H6(a, s) (results/C3PLAN/PLAN.md section 3a, Lemma H6M).  OFF by default
# (mirror_h6=False); no task may use it before results/C3AUDIT2 accepts the lemma.
#   phi_{a,s}: (r, sigma) -> ((a - r) mod m, sigma xor [r < a] xor [s = 0]), None stays None.


def h6_phi(m, a, s, L):
    return sorted(((a - r) % m, (None if sg is None else sg ^ int(r < a) ^ int(s == 0))) for r, sg in L)


def h6_layer2_kept(m, a, s):
    """layer-2 options below H6(a, s) kept by Lemma H6M: O kept iff key(O) <= key(phi(O))."""
    key = lambda L: tuple((r, -1 if sg is None else sg) for r, sg in sorted(L))
    return [o for o in layer2_options(m, [(0, 0), (a, s)]) if key(o) <= key(h6_phi(m, a, s, o))]


def tree_children(m, k, layers, mirror=True, mirror_h6=False):
    """children of a node of the layer tree (the shard plan's tree).  Root: the top hull cases.
    Below: every next layer on the unused residues; with mirror=True the children of the H3 node
    are reduced to h3_layer2_kept (Lemma 5); with mirror_h6=True (default off) the children of
    each H6(a, s) node are reduced to h6_layer2_kept (PLAN.md 3a)."""
    if not layers:
        return [legacy_to_layers(c) for c in cases(m, k)]
    if mirror and layers == [[(0, 0)]]:
        return [layers + [o] for o in h3_layer2_kept(m)]
    if (mirror_h6 and len(layers) == 1 and len(layers[0]) == 2 and layers[0][0] == (0, 0)
            and layers == legacy_to_layers(("H6", layers[0][1][0], layers[0][1][1]))
            and 1 <= layers[0][1][0] <= m // 2 and layers[0][1][1] in (0, 1)):
        return [layers + [o] for o in h6_layer2_kept(m, layers[0][1][0], layers[0][1][1])]
    used = [r for L in layers for r, _ in L]
    return [layers + [o] for o in layer2_options(m, [(r, None) for r in used])]
