#!/usr/bin/env python3
"""Controls for c2_example_check.py: the DP self-test does real work, a mutated DP is caught,
and convex sets of size 7..12 are recognised."""
import importlib.util, itertools, math, random, sys, collections
spec = importlib.util.spec_from_file_location("chk", sys.argv[1])
src = open(sys.argv[1]).read().replace("\nmain()\n", "\n")
chk = {}
exec(compile(src, sys.argv[1], "exec"), chk)
cross, bf_conv, dp = chk["cross"], chk["in_convex_position"], chk["largest_convex"]

rng = random.Random(7)
hist = collections.Counter(); tested = 0; mismatch_mut = 0
def dp_mut(pts):
    # mutation: reverse the intermediate turn test (the closing turn is implied by the angular order, cross is cyclic)
    n = len(pts); best = min(n, 2)
    import functools
    for s in range(n):
        p = pts[s]; up = [q for q in pts if (q[1], q[0]) > (p[1], p[0])]
        up.sort(key=functools.cmp_to_key(lambda a, b: -1 if cross(p, a, b) > 0 else (1 if cross(p, a, b) < 0 else 0)))
        m = len(up); L = [[-1] * m for _ in range(m)]
        for j in range(m):
            for i in range(j):
                v = 3
                for k in range(i):
                    if L[k][i] > 0 and cross(up[k], up[i], up[j]) < 0: v = max(v, L[k][i] + 1)
                L[i][j] = v; best = max(best, v)
    return best
while tested < 200:
    n = rng.randint(7, 11)
    pts = list({(rng.randint(-40, 40), rng.randint(-40, 40)) for _ in range(n)})
    if any(cross(a, b, c) == 0 for a, b, c in itertools.combinations(pts, 3)): continue
    bf = max(k for k in range(len(pts) + 1) for sub in itertools.combinations(pts, k) if bf_conv(list(sub)))
    assert bf == dp(pts), pts
    hist[bf] += 1; tested += 1
    if dp_mut(pts) != bf: mismatch_mut += 1
print("random sets tested:", tested, "largest-convex histogram:", dict(sorted(hist.items())))
print("mutated DP disagrees with brute force on", mismatch_mut, "of", tested, "sets (must be > 0)")
# convex controls: integer points near a circle, kept only if in convex and general position
for m in range(7, 13):
    pts = [(round(1000 * math.cos(2 * math.pi * t / m + 0.1)), round(1000 * math.sin(2 * math.pi * t / m + 0.1))) for t in range(m)]
    assert bf_conv(pts) and all(cross(a, b, c) != 0 for a, b, c in itertools.combinations(pts, 3))
    print(f"convex {m}-gon: DP gives {dp(pts)}")
ok = mismatch_mut > 0
print("CONTROLS OK" if ok else "CONTROLS FAILED"); sys.exit(0 if ok else 1)
