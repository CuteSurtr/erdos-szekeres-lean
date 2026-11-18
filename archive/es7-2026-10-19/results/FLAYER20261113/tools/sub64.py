"""Large (6,6)-subsets (no 6-cap, no 6-cup; octagon-free inherited) of the known 64-point octagon-free sets."""
import sys, random, json, glob, os
import fl
from fl import valid
def run(seed, nfiles, out, reps=3, iters=150):
    rng = random.Random(seed)
    files = sorted(glob.glob('/home/jay/research/lean/erdos-szekeres-lean/experiments/es8-lower-bound-search-2026-10-11/family/sets/*.txt'))
    rng.shuffle(files)
    for fn in files[:nfiles]:
        P = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]
        best = []
        for rep in range(reps):
            order = P[:]; rng.shuffle(order); Q = []
            for p in order:
                if valid(Q + [p]): Q.append(p)
            for it in range(iters):
                rest = [p for p in P if p not in Q]
                k = rng.randrange(len(Q)); Q2 = Q[:k] + Q[k+1:]
                rng.shuffle(rest); added = 0
                for p in rest:
                    if valid(Q2 + [p]): Q2.append(p); added += 1
                if added >= 1 and len(Q2) >= len(Q): Q = Q2
            if len(Q) > len(best): best = Q
        print(os.path.basename(fn), len(best), flush=True)
        with open(out, 'a') as f: f.write(json.dumps({'src': os.path.basename(fn), 'P': sorted(best)}) + '\n')
if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
