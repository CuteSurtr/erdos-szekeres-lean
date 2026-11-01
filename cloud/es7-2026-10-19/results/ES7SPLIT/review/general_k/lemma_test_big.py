"""Larger splits (|A|,|B| up to 8, |S| up to 14) for lemma_test.py; same checks."""
import random, sys
import lemma_test as LT
seed = int(sys.argv[1]); n = int(sys.argv[2])
rng = random.Random(seed)
stats = {'L2': 0, 'L2_viol': 0, 'L3': 0, 'L3_viol': 0, 'C4': 0, 'C4_viol': 0, 'types': {}}
done = 0; big = 0
while done < n:
    finite = (done % 2 == 0)
    r = LT.gen_split(rng, finite, 8, 8, tries=800)
    if r is None: continue
    z, A, B = r
    if len(A) + len(B) > 14 or len(A) < 2 or len(B) < 2: continue
    LT.test_split(z, A, B, stats); done += 1
    big += (len(A) + len(B) >= 13)
types = stats.pop('types')
print("seed", seed, "splits", done, "with |S|>=13:", big, stats)
cd = {}
for (na, nb, c, d), m in types.items(): cd[(c, d)] = cd.get((c, d), 0) + m
print("(c,d) histogram:", dict(sorted(cd.items())))
