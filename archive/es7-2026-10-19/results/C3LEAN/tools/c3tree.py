#!/usr/bin/env python3
"""Tree semantics of the threefold (m = 11, k = 7) case split, written independently of results/C3U2/tools/hullcase.py
but mirroring it (and the Lean file C3Cover.lean) definition by definition.  Used by gen_c3lean.py.

A node is (layers, C):
  layers: list of layers, a layer a list of tokens (r, s), s in {0, 1, None}
  C:      list of (r, v), sorted by residue (the sigma cube), [] for a plain node
Names exactly as hullcase.node_name: layers joined by '_', tokens by '-', token "r" or "rs<s>", then "__" + cube.

Compact key (the Lean `Node.key`):
  token code   t(r, s) = 3 r + (0 | 1 | 2)   for s = 0 | 1 | None          (0 .. 32)
  layer code   1 + t1                 for a one-token layer                     (1 .. 33)
               34 + 33 t1 + t2        for a two-token layer (tokens in name order)  (34 .. 1122)
  layer key    lk = digits of the layer codes in base 2048, first layer most significant (all digits >= 1)
  node key     lk * 2^22 + cubeMask * 2^11 + cubeVals   (bit r of cubeMask: r in C; bit r of cubeVals: C[r] = 1)
"""

M = 11
K7 = 7


# ---------------------------------------------------------------- names
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


def parse_node(name):
    if "__" not in name:
        return parse_layers(name), []
    lay, cub = name.split("__")
    C = []
    for tok in cub.split("-"):
        r, v = tok.split("s")
        if not (r.isdigit() and v in ("0", "1")):
            raise ValueError(f"bad sigma bit {tok!r} in {name!r}")
        C.append((int(r), int(v)))
    if not C or len({r for r, _ in C}) != len(C):
        raise ValueError(f"bad cube in {name!r}")
    return parse_layers(lay), C


def node_name(layers, C):
    return layers_name(layers) + ("__" + "-".join(f"{r}s{v}" for r, v in C) if C else "")


# ---------------------------------------------------------------- keys
def tok_code(r, s):
    assert 0 <= r < M and s in (0, 1, None)
    return 3 * r + (2 if s is None else s)


def layer_code(L):
    if len(L) == 1:
        return 1 + tok_code(*L[0])
    assert len(L) == 2
    return 34 + 33 * tok_code(*L[0]) + tok_code(*L[1])


def decode_layer(c):
    def tok(t):
        r, x = divmod(t, 3)
        return (r, None if x == 2 else x)
    if 1 <= c <= 33:
        return [tok(c - 1)]
    assert 34 <= c <= 1122
    t1, t2 = divmod(c - 34, 33)
    return [tok(t1), tok(t2)]


def layers_key(layers):
    k = 0
    for L in layers:
        k = k * 2048 + layer_code(L)
    return k


def node_key(layers, C):
    cm = sum(1 << r for r, _ in C)
    cv = sum(1 << r for r, v in C if v)
    return (layers_key(layers) << 22) + (cm << 11) + cv


def decode_key(key):
    cv = key & 2047
    cm = (key >> 11) & 2047
    lk = key >> 22
    codes = []
    while lk:
        lk, c = divmod(lk, 2048)
        assert c != 0
        codes.append(c)
    layers = [decode_layer(c) for c in reversed(codes)]
    C = [(r, (cv >> r) & 1) for r in range(M) if (cm >> r) & 1]
    assert cv & ~cm == 0
    return layers, C


# ---------------------------------------------------------------- the split (mirrors hullcase.py)
def top_cases():
    out = [[(0, 0)]]
    for a in range(1, M // 2 + 1):
        for s in (0, 1):
            out.append([(0, 0), (a, s)])
    return out


def layer_options(used):
    rem = [r for r in range(M) if r not in used]
    out = [[(r, None)] for r in rem]
    for i, b in enumerate(rem):
        for c in rem[i + 1:]:
            for sb in (0, 1):
                for sc in (0, 1):
                    out.append([(b, sb), (c, sc)])
    return out


def okey(L):
    return tuple((r, -1 if s is None else s) for r, s in sorted(L))


def mirror(L):
    return sorted(((M - r) % M, (None if s is None else 1 - s)) for r, s in L)


def phi(a, s, L):
    return sorted(((a - r) % M, (None if sg is None else sg ^ int(r < a) ^ int(s == 0))) for r, sg in L)


def depth1_children(top):
    """kept second layers below a top case (Lemma 5 for H3, Lemma H6M for H6(a, s))."""
    used = {r for r, _ in top}
    opts = layer_options(used)
    if top == [(0, 0)]:
        return [o for o in opts if okey(o) <= okey(mirror(o))]
    (_, _), (a, s) = top
    return [o for o in opts if okey(o) <= okey(phi(a, s, o))]


def roots():
    return [[t, o] for t in top_cases() for o in depth1_children(t)]


def free_residues(layers, C):
    used = {r for L in layers for r, _ in L} | {r for r, _ in C}
    return [r for r in range(1, M) if r not in used]


def sigma_children(layers, C, K):
    bits = free_residues(layers, C)[:K]
    assert len(bits) == K
    out = []
    for i in range(2 ** K):
        vals = [(i >> (K - 1 - j)) & 1 for j in range(K)]
        out.append((layers, sorted(C + list(zip(bits, vals)))))
    return bits, out


def conflicts(layer, C):
    cv = dict(C)
    return any(s is not None and r in cv and cv[r] != s for r, s in layer)


def layer_children(layers, C):
    """children of a layer split of a node with >= 2 layers (no reduction below depth 1)."""
    assert len(layers) >= 2
    used = {r for L in layers for r, _ in L}
    return [(layers + [o], C) for o in layer_options(used) if not conflicts(o, C)]
