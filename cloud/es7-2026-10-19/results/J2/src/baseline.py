#!/usr/bin/env python3
"""Baselines for task J2, same local search (ls33, same ITERS) as pb.py.

mode random : uniform random integer starts in [0, 2^24)^2 (33 points)
mode seeds  : no-learning control: a random training set (a 33-point near-miss
              seed, or a 32-point heptagon-free set plus one uniform random
              point, with the same 70/30 mix as pb.py's training batches) passed
              through enc.encode/enc.decode (random rotation, same quantization
              noise as model samples), then ls33.

usage: baseline.py MODE OUTDIR HOURS NPROC
"""
import os, sys, json, time, random, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import enc, common

MODE, OUT, HOURS, NPROC = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
ITERS = int(os.environ.get('ITERS', 800))
BATCH = int(os.environ.get('BATCH', 200))
IN = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../inputs')
rng = random.Random(12345 if MODE == 'random' else 54321)
os.makedirs(OUT, exist_ok=True)
T0 = time.time()

sets32, seeds33 = [], []
for f in sorted(glob.glob(IN + '/distinct_K7*.txt')):
    sets32 += enc.load_sets(f)
for f in sorted(glob.glob(IN + '/nearfull_p2*.txt')):
    seeds33 += enc.load_sets(f)
seed_canon = set(common.canon(seeds33))


def start():
    if MODE == 'random':
        return [(rng.randrange(1 << 24), rng.randrange(1 << 24)) for _ in range(33)]
    if rng.random() < 0.7:
        P = rng.choice(seeds33)
    else:
        P = list(rng.choice(sets32))
        xs = [p[0] for p in P]; ys = [p[1] for p in P]
        P.append((rng.randint(min(xs), max(xs)), rng.randint(min(ys), max(ys))))
    return enc.decode(enc.encode(P, rng), rng)


hist = {}
found = {}
best = None
b = 0
log = open(os.path.join(OUT, 'timeline.jsonl'), 'a')
while time.time() - T0 < HOURS * 3600:
    res = common.run_ls([start() for _ in range(BATCH)], ITERS, NPROC, seed=b + 1)
    for r in res:
        hist[r[1]] = hist.get(r[1], 0) + 1
        if r[1] == 0:
            with open(os.path.join(OUT, 'ZERO_CANDIDATES.txt'), 'a') as f:
                f.write(common.fmt_set(r[3]) + '\n')
    good = [r for r in res if r[1] <= 1]
    for c, r in zip(common.canon([r[3] for r in good]), good):
        if c not in found or (r[1], r[2]) < found[c][:2]:
            found[c] = (r[1], r[2], r[3])
    bb = min(res, key=lambda r: (r[1], r[2]))
    if best is None or (bb[1], bb[2]) < best[:2]:
        best = (bb[1], bb[2], bb[3])
        with open(os.path.join(OUT, 'best.txt'), 'w') as f:
            f.write('# E7=%d c6=%d\n' % (best[0], best[1]) + '\n'.join('%d %d' % p for p in best[2]) + '\n')
    E = np.array([r[1] for r in res])
    rec = dict(batch=b, wall=round(time.time() - T0, 1), cpu=round(common.self_cpu() + common.child_cpu(), 1),
               starts=sum(hist.values()), E7_min_so_far=best[0], E7_min=int(E.min()), E7_med=float(np.median(E)),
               n_le1_total=sum(v for k, v in hist.items() if k <= 1), distinct_ot_le1=len(found),
               new_ot_le1_vs_seeds=len(set(found) - seed_canon),
               c6_min_le1=min((v[1] for v in found.values()), default=None),
               hist_small={str(k): hist.get(k, 0) for k in range(6)})
    log.write(json.dumps(rec) + '\n'); log.flush()
    b += 1
with open(os.path.join(OUT, 'found_top.txt'), 'w') as f:
    for v in sorted(found.values(), key=lambda v: (v[0], v[1]))[:200]:
        f.write('%d %d %s\n' % (v[0], v[1], common.fmt_set(v[2])))
