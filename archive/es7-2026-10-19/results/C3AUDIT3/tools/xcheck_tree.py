"""cross-check mycompose's tree and units against hullcase (C3U copy at the given path)."""
import random, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import mycompose as Y
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, os.path.join(sys.argv[1], "..", "..", "C3a"))
import hullcase as H
from c3cnf import C3Enc
random.seed(1)
bad = n = 0
for m, k in [(5, 6), (6, 6), (7, 5), (7, 6), (7, 7), (9, 7), (11, 7)]:
    E = C3Enc(m, k)
    frontier = [()]
    for depth in range(4):
        nxt = []
        for lay in frontier:
            a = sorted(Y.kname(Y.key(c, ())) for c in Y.layer_children(m, k, lay))
            b = sorted(H.layers_name(c) for c in H.tree_children(m, k, [list(L) for L in lay], mirror=True))
            # hullcase names are sorted inside a layer already? compare via key
            b2 = sorted(Y.kname(Y.key(Y.parse(x)[0], ())) for x in b)
            n += 1; bad += a != b2
            if a != b2 and bad < 4: print("tree", m, k, lay, len(a), len(b2))
            kids = Y.layer_children(m, k, lay)
            nxt += random.sample(kids, min(3, len(kids)))
            if lay:
                fr = Y.free(m, lay, ())
                cube = tuple((r, random.randint(0, 1)) for r in fr[:2])
                u1 = Y.units(m, E, lay, cube)
                u2 = H.node_units(m, Y.kname((lay, cube)), E.ccw, E.sig)
                n += 1; bad += u1 != u2
                if u1 != u2 and bad < 4: print("units", m, k, lay, cube)
                if len(lay) >= 2 and len(Y.free(m, lay, cube)) >= 2:
                    a = sorted(Y.kname(x) for x in Y.cube_layer_kids(m, k, lay, cube))
                    b = sorted(Y.kname(Y.key(*Y.parse(H.node_name(L, C)))) for L, C in H.cube_layer_children(m, k, [list(L) for L in lay], list(cube)))
                    n += 1; bad += a != b
                    bits, ch = H.sigma_children(m, [list(L) for L in lay], list(cube), 2)
                    a = sorted(Y.kname(x) for x in Y.sigma_kids(m, lay, cube, Y.free(m, lay, cube)[:2]))
                    b = sorted(Y.kname(Y.key(*Y.parse(H.node_name(L, C)))) for L, C in ch)
                    n += 1; bad += a != b
        frontier = nxt
print({"comparisons": n, "mismatches": bad})
