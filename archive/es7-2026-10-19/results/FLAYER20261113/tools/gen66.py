"""Generators of (6,6;8)-sets (no 6-cap, no 6-cup, no convex octagon), exact validity at every step.
modes:
  anneal <seed> <iters> <out.jsonl> [init.json] [piece]   simulated annealing; piece = 'size' or a
        comma list of state indices (maximize the number of occupied in-states of that family, tie-break size)
  sub64 <seed> <nfiles> <out.jsonl>     large (6,6)-subsets of the known 64-point octagon-free sets
  greedy <seed> <iters> <out.jsonl> <mode>   greedy insertion + swaps (box/para/circ/gauss)
"""
import sys, random, json, math, time, os, glob
import fl
from fl import Set66, valid, quick

def score(P, fam):
    if fam is None:
        return len(P) if valid(P) else None
    try:
        S = Set66(P)
    except ValueError:
        return None
    if not S.ok: return None
    occ = set(S.in_state)
    return len(occ & fam) + 0.01 * len(P)

def anneal(seed, iters, init=None, fam=None, T0=0.6, R=10**6, log=None):
    rng = random.Random(seed)
    P = list(init) if init else []
    cur = score(P, fam) if P else 0
    if cur is None: raise SystemExit('bad init')
    best = (cur, list(P))
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.02
        r = rng.random(); Q = list(P)
        if r < 0.40 or len(Q) < 5:
            Q.append((rng.randint(-R, R), rng.randint(-R, R)))
        elif r < 0.80:
            k = rng.randrange(len(Q)); x, y = Q[k]
            s = rng.choice([100, 1000, 10000, 100000, R])
            Q[k] = (x + rng.randint(-s, s), y + rng.randint(-s, s))
        elif r < 0.90:
            k = rng.randrange(len(Q)); Q[k] = (rng.randint(-R, R), rng.randint(-R, R))
        else:
            Q.pop(rng.randrange(len(Q)))
        if len({q[0] for q in Q}) < len(Q): continue
        v = score(Q, fam)
        if v is None: continue
        if v >= cur or rng.random() < math.exp((v - cur) / T):
            P, cur = Q, v
            if cur > best[0]: best = (cur, list(P))
    return best

def scale_to_int(P):
    return [(int(x), int(y)) for x, y in P]

def sub64(seed, files, out):
    rng = random.Random(seed)
    for fn in files:
        P = [tuple(map(int, l.split())) for l in open(fn) if l.strip()]
        best = []
        for rep in range(6):
            order = P[:]; rng.shuffle(order)
            Q = []
            for p in order:
                if valid(Q + [p]): Q.append(p)
            # improvement: swap one out, try to add two
            for it in range(300):
                rest = [p for p in P if p not in Q]
                if not rest: break
                k = rng.randrange(len(Q)); Q2 = Q[:k] + Q[k+1:]
                rng.shuffle(rest); added = 0
                for p in rest:
                    if valid(Q2 + [p]): Q2.append(p); added += 1
                if added >= 1 and len(Q2) >= len(Q): Q = Q2
            if len(Q) > len(best): best = Q
        print(os.path.basename(fn), len(best), flush=True)
        with open(out, 'a') as f:
            f.write(json.dumps({'src': os.path.basename(fn), 'P': sorted(best)}) + '\n')

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'anneal':
        seed, iters, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        init = None; fam = None; tag = 'size'
        if len(sys.argv) > 5 and sys.argv[5] != '-':
            init = [tuple(p) for p in json.load(open(sys.argv[5]))]
        if len(sys.argv) > 6 and sys.argv[6] != 'size':
            tag = sys.argv[6]; fam = set(int(x) for x in tag.split(','))
        t0 = time.time()
        v, P = anneal(seed, iters, init, fam)
        print(seed, tag[:40], v, len(P), '%.0fs' % (time.time() - t0), flush=True)
        with open(out, 'a') as f:
            f.write(json.dumps({'seed': seed, 'piece': tag, 'value': v, 'P': sorted(P)}) + '\n')
    elif mode == 'sub64':
        seed, nfiles, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        files = sorted(glob.glob('/home/jay/research/lean/erdos-szekeres-lean/experiments/es8-lower-bound-search-2026-10-11/family/sets/*.txt'))
        random.Random(seed).shuffle(files)
        sub64(seed, files[:nfiles], out)
