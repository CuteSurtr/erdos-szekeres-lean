"""C3AUDIT4: own implementation of the Lemma H6M reduction (results/C3PLAN/PLAN.md 3a), written from the lemma's
text, patched into C3AUDIT3's mycompose.layer_children for runcomp.py 'mine --mirror-h6'.
Below H6(a, s) (layers == (((0,0),(a,s)),), 1 <= a <= m//2), keep a layer-2 option O iff key(O) <= key(phi(O)),
phi(r, v) = ((a - r) mod m, v xor [r < a] xor [s = 0]), None stays None; key = sorted (r, -1 if None else v)."""


def install(Y):
    orig = Y.layer_children

    def phi(m, a, s, O):
        return tuple(((a - r) % m, None if v is None else v ^ int(r < a) ^ int(s == 0)) for r, v in O)

    def key(O):
        return tuple(sorted((r, -1 if v is None else v) for r, v in O))

    def lc(m, k, layers):
        out = orig(m, k, layers)
        if len(layers) == 1 and len(layers[0]) == 2 and layers[0][0] == (0, 0):
            a, s = layers[0][1]
            if 1 <= a <= m // 2 and s in (0, 1):
                out = [c for c in out if key(c[-1]) <= key(phi(m, a, s, c[-1]))]
        return out
    Y.layer_children = lc
