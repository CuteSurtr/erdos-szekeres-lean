import random, collections
import rg
from test_rg import rand_set
rng = random.Random(7)
dist = collections.Counter(); ns = collections.Counter()
for t in range(400):
    n = rng.randint(6, 12)
    pts = rand_set(rng, n, t % 3)
    mb, _ = rg.max_convex_bf(pts)
    m1, w1 = rg.max_convex_cupcap(pts); m2 = rg.max_convex_angular(pts)
    assert mb == m1 == m2 and rg.convex_position_bf(w1) and len(w1) == m1, (pts, mb, m1, m2)
    dist[(n, mb)] += 1
print(sorted(dist.items()))
# mutation test: a cup/cap DP that ignores the sign condition on caps must be caught
orig = rg.orient
def broken(a, b, c):
    v = orig(a, b, c)
    return v if v > 0 else -abs(v) // 2 - 1 if v < 0 else 0
caught = 0
for t in range(100):
    pts = rand_set(rng, 8, 1)
    mb, _ = rg.max_convex_bf(pts)
    # broken angular DP: accept right turns too
    def bad_angular(pts):
        from functools import cmp_to_key
        best = 2
        for p in pts:
            above = [q for q in pts if (q[1], q[0]) > (p[1], p[0])]
            above.sort(key=cmp_to_key(lambda q1, q2: -rg.sgn(rg.orient(p, q1, q2))))
            m = len(above)
            f = [[3 if i < j else 0 for j in range(m)] for i in range(m)]
            for j in range(m):
                for i in range(j):
                    for l in range(j + 1, m):
                        if f[i][j] + 1 > f[j][l] and rg.orient(above[i], above[j], above[l]) >= -10**9:
                            f[j][l] = f[i][j] + 1
            if m >= 2: best = max(best, max(max(r) for r in f))
        return best
    if bad_angular(pts) != mb: caught += 1
print("mutant caught in", caught, "of 100")
