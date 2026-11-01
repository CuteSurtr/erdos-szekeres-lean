"""Compare c3tree's children with results/C3U2/tools/hullcase.py at every split node of the cover (read-only import)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c3tree as T, cover
R = sys.argv[1]
sys.path.insert(0, os.path.join(R, "C3U2", "tools"))
import hullcase as H
D = cover.load(R)
nl = ns = bad = 0
for r in T.roots():
    t = cover.tree(r, [], D)
    for (lay, C), d in cover.walk(t, r, []):
        if d[0] == "L":
            nl += 1
            mine = [(l, c) for l, c in T.layer_children(lay, C)]
            theirs = H.cube_layer_children(11, 7, lay, C, mirror=True, mirror_h6=True)
            bad += mine != [(l, list(c)) for l, c in theirs]
        elif d[0] == "S":
            ns += 1
            bad += T.sigma_children(lay, C, d[1]) != H.sigma_children(11, lay, C, d[1])
            bad += T.free_residues(lay, C)[:d[1]] != H.free_residues(11, lay, C)[:d[1]]
print({"layer_splits_compared": nl, "sigma_splits_compared": ns, "mismatches": bad})
