# validate geo.convex_counts (angular DP) against brute force (extreme-point test on every subset)
import random, itertools, sys
from geo import Z4, Z5, Config, extreme_points, convex_counts
rnd = random.Random(7)
def brute(cfg, kmax):
    c = {k: 0 for k in range(3, kmax + 1)}
    for k in range(3, kmax + 1):
        for S in itertools.combinations(range(cfg.n), k):
            if len(extreme_points(cfg, S)) == k:
                c[k] += 1
    return c
tested = 0
for ring, t in [(Z4, 3), (Z5, 2), (Z4, 4), (Z5, 3)]:
    for trial in range(6 if t <= 3 else 2):
        while True:
            if ring is Z4:
                reps = [(rnd.randint(-60, 60), rnd.randint(-60, 60)) for _ in range(t)]
            else:
                reps = [tuple(rnd.randint(-30, 30) for _ in range(4)) + (0,) for _ in range(t)]
            cfg = Config(ring, reps)
            if cfg.general_position():
                break
        kmax = 7
        a, best = convex_counts(cfg, kmax)
        b = brute(cfg, kmax)
        assert a == b, (a, b)
        mx = max([k for k in b if b[k]] + [2])
        assert best == mx or (best >= kmax and mx == kmax), (best, mx)
        tested += 1
        print(ring.__name__, cfg.n, a, "largest", best)
print("DP == brute force on", tested, "configurations")
