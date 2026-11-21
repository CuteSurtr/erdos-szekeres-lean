"""Greedy-insertion residual sets (larger than deletion-pruned ones), then the C1 checks of check_c1.check."""
import json, random, sys
from geo import Conf
from check_c1 import check, new_tally

def try_add(P, p):
    Q = sorted(P + [p])
    xs = [q[0] for q in Q]
    if len(set(xs)) != len(xs):
        return None
    try:
        C = Conf(Q)
    except ValueError:
        return None
    return Q if C.residual() else None

def sample(rng, mode):
    x = rng.randint(-10**6, 10**6)
    if mode == 'unif':
        return (x, rng.randint(-10**6, 10**6))
    if mode == 'para':
        return (x, x*x//10**6 + rng.randint(-80000, 80000))
    sgn = rng.choice((1, -1))
    return (x, sgn*x*x//10**6 + rng.randint(-80000, 80000))

seed, nsets, trials, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = random.Random(seed)
t = new_tally(); sizes = []
for rep in range(nsets):
    P = []
    for _ in range(trials):
        Q = try_add(P, sample(rng, mode))
        if Q is not None:
            P = Q
    sizes.append(len(P))
    check(P, t)
t['size_min'] = min(sizes); t['size_max'] = max(sizes); t['size_mean'] = sum(sizes)/len(sizes)
t['mode'] = mode; t['seed'] = seed; t['trials'] = trials
print(json.dumps(t))
