#!/usr/bin/env python3
"""Exact tests of the encoders on the project's extremal 7-gon-free examples and their mirror images (audit A4).

usage: test_real.py m POINTS_FILE MAXN_INMEM STREAM_N [STREAM_N ...]
- parses the orbits (m consecutive lines each; checked to be rotations), verifies general position (and for m = 5
  the centre off all lines through two points), the largest convex subset (angular DP), and single-orbit layers;
- for every whole-orbit subset with t >= 2 orbits and N = m t <= MAXN_INMEM: evaluates c{m}L_N (and c5A_N for m = 5)
  in memory for every choice of (0,0) (angle form: every orbit 0 and every (0,0));
- for N in STREAM_N: evaluates the full-size CNF by streaming, for a few labellings.
Point file formats: m = 5: four integers a0..a3 = a0 + a1 z + a2 z^2 + a3 z^3, z = exp(2 pi i/5); m = 4: x y.
Lines starting with '#' or 'FOUND' are skipped."""
import sys, itertools, json, time, random
from geo import Z4, Z5, Config, convex_layers, convex_counts
from labels import layer_labelling, angle_labelling
from evalcnf import CNF
from evalstream import StreamCNF

m = int(sys.argv[1]); path = sys.argv[2]; MAXN = int(sys.argv[3]); STREAM = [int(x) for x in sys.argv[4:]]
ring = {4: Z4, 5: Z5}[m]
rnd = random.Random(99)
pts = []
for l in open(path):
    if not l.strip() or l.startswith(("#", "FOUND")):
        continue
    xs = list(map(int, l.split()))
    pts.append(Z5.norm(tuple(xs) + (0,)) if m == 5 else tuple(xs))
centre_in = [p for p in pts if p == ring.zero]
pts_nc = [p for p in pts if p != ring.zero]
assert len(pts_nc) % m == 0
reps = []
seen = set()
for p in pts_nc:
    if p in seen:
        continue
    orb = [ring.rot(p, k) for k in range(m)]
    assert all(q in pts_nc for q in orb), "not closed under rotation"
    seen.update(orb)
    reps.append(p)
print(f"{path}: {len(pts)} points, centre included: {bool(centre_in)}, {len(reps)} orbits", flush=True)


def mirror(p):
    return Z5.conj(p) if m == 5 else (p[0], -p[1])


cache = {}


def formula(enc, N):
    key = (enc, N)
    if key not in cache:
        if N <= MAXN:
            cache[key] = CNF(f"work/c{m}{enc}_{N}.cnf", f"work/c{m}{enc}_{N}.json")
        else:
            cache[key] = StreamCNF(f"work/c{m}{enc}_{N}.cnf", f"work/c{m}{enc}_{N}.json")
    return cache[key]


tot = {"subsets": 0, "evaluations": 0, "T": 0, "D": 0, "K": 0, "stream_evaluations": 0}
for mir in (False, True):
    R = [mirror(p) for p in reps] if mir else list(reps)
    full = Config(ring, R)
    assert full.general_position()
    if m == 5:
        assert full.centre_general()
    # whole set including the centre if present: largest convex subset
    if centre_in:
        cfgc = Config(ring, R)
        cfgc.pts = cfgc.pts + [ring.zero]; cfgc.n += 1
        assert cfgc.general_position()
        cc, bc = convex_counts(cfgc, 7)
        print(f"  mirror={mir}: with centre: {cfgc.n} points, general position, largest convex subset {bc}")
    cnt, best = convex_counts(full, 7)
    layers = convex_layers(full)
    lo = [L[0] // m for L in layers]
    single = all(len(L) == m and len({i // m for i in L}) == 1 for L in layers)
    print(f"  mirror={mir}: {full.n} points, largest convex subset {best}, layers single orbits: {single}, "
          f"layer orbit order {lo}", flush=True)
    assert best < 7 and single
    for t in range(2, len(R) + 1):
        N = m * t
        for sub in itertools.combinations(range(len(R)), t):
            cfg = Config(ring, [R[i] for i in sub])
            layers = convex_layers(cfg)
            assert all(len(L) == m and len({i // m for i in L}) == 1 for L in layers)
            lo = [L[0] // m for L in layers]
            if N <= MAXN:
                labs = [("L", j, layer_labelling(cfg, lo, j00=j)) for j in range(m)]
                if m == 5:
                    labs += [("A", (o0, j), angle_labelling(cfg, o0, j00=j)) for o0 in range(t) for j in range(m)]
            elif N in STREAM:
                labs = [("L", j, layer_labelling(cfg, lo, j00=j)) for j in rnd.sample(range(m), 2)]
                if m == 5:
                    o0 = rnd.randrange(t)
                    labs += [("A", (o0, 0), angle_labelling(cfg, o0, j00=0))]
            else:
                continue
            tot["subsets"] += 1
            for enc, key, lab in labs:
                if m == 5:
                    lab[m * t] = ring.zero
                F = formula(enc, N)
                tval = F.triple_values(lambda a, b, c: ring.orient(lab[a], lab[b], lab[c]))
                t0 = time.time()
                res, _ = F.evaluate(tval)
                tot["evaluations"] += 1
                if N > MAXN:
                    tot["stream_evaluations"] += 1
                    print(f"    stream N={N} enc={enc} mirror={mir} subset={sub} key={key}: {res} "
                          f"({time.time() - t0:.0f} s)", flush=True)
                for k in "TDK":
                    tot[k] += res[k]
    print(f"  after mirror={mir}: {tot}", flush=True)
print("TOTAL", json.dumps(tot))
