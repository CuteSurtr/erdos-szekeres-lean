#!/usr/bin/env python3
"""Coverage add-on for direct_lemmas.py: count nontrivial splits whose finite z lies on a line
through a point of A and a point of B (ties in the z-order across parts), and re-run the
Lemma 2/3/Cor 4 checks on exactly those."""
import os, sys, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import direct_lemmas as dl
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 99)
stats = {'splits': 0, 'nontrivial': 0, 'nontrivial_finite': 0, 'L2_fail': 0, 'L3_fail': 0, 'C4_fail': 0,
         'types': set(), 'instances': 0}
hit = 0
for t in range(4000):
    S = dl.rand_pts(rng.randint(5, 8), 30, rng) if t % 2 == 0 else dl.structured(rng)
    # force z onto the extension of a random segment
    for _ in range(50):
        a, b = rng.sample(S, 2); k = rng.choice([2, 3, 5, -1, -2, -4])
        zv = (a[0]+k*(b[0]-a[0]), a[1]+k*(b[1]-a[1]))
        if dl.z_outside_hull(S, ('pt', zv)):
            break
    else:
        continue
    z = ('pt', zv); n = len(S)
    for mask in range(1, (1 << n) - 1):
        A = [S[i] for i in range(n) if mask >> i & 1]; B = [S[i] for i in range(n) if not mask >> i & 1]
        if len(A) >= 2 and len(B) >= 2 and dl.is_split(A, B, z):
            if any(dl.orient(p, q, zv) == 0 for p in A for q in B):
                hit += 1
                dl.check_split(S, A, B, z, stats)
stats.pop('types')
print('nontrivial splits with z on an A-B line:', hit, stats)
