"""Annealing over (6,6;8)-sets with exact validity; records every visited in-state occupancy mask.
usage: gen2.py <seed> <iters> <tag> <init.json|-> <pred> [T0] [minsize_for_masks]
  pred: python expression in f (state tuple) or 'size'; objective = #points with pred(state) + 0.01 n
  outputs: appends best set to sets_<tag>.jsonl ; masks to masks_<tag>_<seed>.json (list of ints; bit i = state i occupied)
"""
import sys, random, json, math, time
import fl, fast
from fl import STATES, N

def run(seed, iters, init, pred, T0=0.6, R=10**6, minmask=0, addp=0.40, movep=0.40, replp=0.10):
    rng = random.Random(seed)
    w = None
    if pred != 'size':
        w = [1 if eval(pred, {'f': f}) else 0 for f in STATES]
    def score(P):
        r = fast.instates(P)
        if r is None: return None
        st = r[0]
        m = 0
        for s in st: m |= 1 << s
        if w is None: return len(P), m
        return sum(w[s] for s in st) + 0.01 * len(P), m
    P = list(init) if init else []
    cur, m = score(P) if P else (0, 0)
    best = (cur, list(P)); masks = set()
    if len(P) >= minmask: masks.add(m)
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.02
        r = rng.random(); Q = list(P)
        if r < addp or len(Q) < 5:
            Q.append((rng.randint(-R, R), rng.randint(-R, R)))
        elif r < addp + movep:
            k = rng.randrange(len(Q)); x, y = Q[k]
            s = rng.choice([100, 1000, 10000, 100000, R])
            Q[k] = (x + rng.randint(-s, s), y + rng.randint(-s, s))
        elif r < addp + movep + replp:
            k = rng.randrange(len(Q)); Q[k] = (rng.randint(-R, R), rng.randint(-R, R))
        else:
            Q.pop(rng.randrange(len(Q)))
        if len({q[0] for q in Q}) < len(Q): continue
        sc = score(Q)
        if sc is None: continue
        v, m = sc
        if v >= cur or rng.random() < math.exp((v - cur) / T):
            P, cur = Q, v
            if len(P) >= minmask: masks.add(m)
            if cur > best[0]: best = (cur, list(P))
    return best, masks

if __name__ == '__main__':
    seed, iters, tag, initf, pred = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
    T0 = float(sys.argv[6]) if len(sys.argv) > 6 else 0.6
    minmask = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    init = None
    if initf != '-': init = [tuple(p) for p in json.load(open(initf))]
    t0 = time.time()
    (v, P), masks = run(seed, iters, init, pred, T0, minmask=minmask)
    print(seed, tag, 'value', v, 'n', len(P), 'masks', len(masks), '%.0fs' % (time.time() - t0), flush=True)
    with open(f'sets_{tag}.jsonl', 'a') as f:
        f.write(json.dumps({'seed': seed, 'pred': pred, 'value': v, 'P': sorted(P)}) + '\n')
    json.dump(sorted(masks), open(f'masks_{tag}_{seed}.json', 'w'))
