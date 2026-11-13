import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from indep_splits import read_points, verify_split, brute_longest
P = read_points(sys.argv[1])
n = len(P)
parts = []
for k in (6, 16, 26):
    X = frozenset(range(k)); Y = frozenset(range(n)) - X
    parts += [(X, Y), (Y, X)]
# witnesses printed by tools/splits.py (splits_rerun.log; homogeneous, z3 > 0 means the finite point (z1/z3, z2/z3))
W = [((6,26),(16694,-1016694,0)), ((26,6),(-290,1000290,3141)), ((16,16),(870,-1055701,0)),
     ((16,16),(-299,1031253,37)), ((26,6),(71,-1092033,0)), ((6,26),(-456,1590246,0))]
used = set()
for sizes, z in W:
    zz = (Fraction(z[0], z[2]), Fraction(z[1], z[2]), Fraction(1)) if z[2] else z
    hits = [i for i, (A, B) in enumerate(parts) if verify_split(P, A, B, zz)[0]]
    for i in hits:
        A, B = parts[i]
        assert (len(A), len(B)) == sizes
        print(sizes, z, "certifies A =", (min(A), max(A)), "capA", brute_longest(P, A, zz, "cap"), "cupB", brute_longest(P, B, zz, "cup"))
    used.update(hits)
print("distinct partitions certified by the tools/splits.py witnesses:", len(used))
