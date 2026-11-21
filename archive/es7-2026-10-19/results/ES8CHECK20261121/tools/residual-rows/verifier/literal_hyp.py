"""Does the parenthetical hypothesis (no 6-cap, no 8-cup, no junction; octagons allowed) suffice for the
k = 2 'N66 class' claim?  Search for such sets whose A_2 owners contain a convex octagon."""
import json, random, sys
from geo import Conf, sub, otable

def prune_lit(P, rng):
    P = sorted(P)
    while True:
        C = Conf(P); n = C.n
        bad = [v for v in range(n) if C.capEnd[v] >= 6]
        if not bad:
            bad = [v for v in range(n) if C.cupEnd[v] >= 6 and C.capStart[v] >= 5]
        if not bad:
            bad = [v for v in range(n) if C.cupEnd[v] >= 8]
        if not bad:
            return P, C
        d = rng.choice(bad); P = P[:d] + P[d+1:]

def try_add(P, p):
    Q = sorted(P + [p])
    if len(set(q[0] for q in Q)) != len(Q): return None
    try: C = Conf(Q)
    except ValueError: return None
    ok = C.longcap <= 5 and C.longcup <= 7 and not C.junction()
    return (Q, C) if ok else None

seed, nsets, trials = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
cnt = dict(sets=0, R_has_octagon=0, A2_has_octagon=0, a_fail=0, b2_fail=0)
example = None
for rep in range(nsets):
    P = []; C = None
    for _ in range(trials):
        x = rng.randint(-10**6, 10**6); s = rng.choice((1, -1, 0))
        y = s * x * x // 10**6 + rng.randint(-120000, 120000) if s else rng.randint(-10**6, 10**6)
        r = try_add(P, (x, y))
        if r: P, C = r
    if C is None: continue
    cnt['sets'] += 1
    S = C.states()
    if C.gon() >= 8: cnt['R_has_octagon'] += 1
    for v in range(C.n):
        if S[v][3] >= 1 and S[v][3] + C.cupStart[v] > 7: cnt['a_fail'] += 1
    own = [v for v in range(C.n) if S[v][3] >= 2]
    if own:
        C2 = Conf(sub(C.P, own))
        if C2.longcup > 5: cnt['b2_fail'] += 1
        if C2.gon() >= 8:
            cnt['A2_has_octagon'] += 1
            if example is None:
                example = dict(points=C.P, A2_owner_idx=own, A2_gon=C2.gon(), A2_longcap=C2.longcap, A2_longcup=C2.longcup)
print(json.dumps(cnt))
if example: print(json.dumps(example))
