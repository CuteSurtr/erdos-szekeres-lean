"""Control for realize_small.realize: signatures of REAL 14-point FL(5,5) sets (so realizable by construction)
are given to the triple-violation annealer; the success rate calibrates the failures on abstract configurations.
usage: realize_control.py <nsets> <iters> <attempts>"""
import sys, json, random, itertools
import realize_small, anneal_ab
nsets, iters, attempts = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(5); n = 14; T = list(itertools.combinations(range(n), 3)); ok = 0; tot = 0
while tot < nsets:
    v, Q = anneal_ab.run(5, 5, 'size', rng.randrange(10**9), 40000)
    if len(Q) < n: continue
    P = sorted(Q)[:n] if len(Q) > n else sorted(Q)
    sig = ''.join('+' if (P[j][0]-P[i][0])*(P[k][1]-P[i][1]) - (P[j][1]-P[i][1])*(P[k][0]-P[i][0]) > 0 else '-' for i, j, k in T)
    tot += 1; got = False
    for a_ in range(attempts):
        if realize_small.realize(n, sig, rng, iters): got = True; break
    ok += got
    print(f'control set {tot}: {"realized" if got else "FAILED"}', flush=True)
print(f'realized {ok} of {tot} real 14-point signatures ({attempts} attempts x {iters} steps)', flush=True)
