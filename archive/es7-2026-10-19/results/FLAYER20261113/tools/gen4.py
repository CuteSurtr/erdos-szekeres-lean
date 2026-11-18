"""Scale-free annealing (moves relative to the current bounding box at random scales), exact validity.
usage: gen4.py <seed> <iters> <tag> <init.json|-> <pred|size> [T0] [minsize_for_masks] [transform]
 transform: none | rot180 | xrev | ymir  applied to the init set."""
import sys, random, json, math, time
import fl, fast
from fl import STATES, N
def run(seed, iters, init, pred, T0=0.3, minmask=0):
    rng = random.Random(seed)
    w = None if pred == 'size' else [1 if eval(pred, {'f': f}) else 0 for f in STATES]
    def score(P):
        r = fast.instates(P)
        if r is None: return None
        st = r[0]; m = 0
        for s in st: m |= 1 << s
        if w is None: return len(P), m
        return sum(w[s] for s in st) + 0.01 * len(P), m
    P = list(init) if init else [(0, 0), (10**6, 10**5), (2 * 10**6, 5 * 10**5)]
    cur, m = score(P)
    best = (cur, list(P)); masks = set()
    if len(P) >= minmask: masks.add(m)
    LIM = 2**60
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.02
        xs = [p[0] for p in P]; ys = [p[1] for p in P]
        W = max(xs) - min(xs) + 1; H = max(ys) - min(ys) + 1
        r = rng.random(); Q = list(P)
        def near(p):
            sx = W * 10 ** (-rng.uniform(0, 7)); sy = H * 10 ** (-rng.uniform(0, 7))
            return (p[0] + int(rng.uniform(-sx, sx)), p[1] + int(rng.uniform(-sy, sy)))
        if r < 0.20:
            Q.append((min(xs) - W // 5 + rng.randrange(W + 2 * (W // 5) + 1), min(ys) - H // 5 + rng.randrange(H + 2 * (H // 5) + 1)))
        elif r < 0.45:
            Q.append(near(rng.choice(Q)))
        elif r < 0.85:
            k = rng.randrange(len(Q)); Q[k] = near(Q[k])
        else:
            if len(Q) > 3: Q.pop(rng.randrange(len(Q)))
        if len({q[0] for q in Q}) < len(Q): continue
        if any(abs(c) > LIM for q in Q for c in q): continue
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
    T0 = float(sys.argv[6]) if len(sys.argv) > 6 else 0.3
    minmask = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    tr = sys.argv[8] if len(sys.argv) > 8 else 'none'
    init = None
    if initf != '-':
        init = [tuple(p) for p in json.load(open(initf))]
        if tr == 'rot180': init = [(-x, -y) for x, y in init]
        elif tr == 'xrev': init = [(-x, y) for x, y in init]
        elif tr == 'ymir': init = [(x, -y) for x, y in init]
    t0 = time.time()
    (v, P), masks = run(seed, iters, init, pred, T0, minmask)
    print(seed, tag, 'value', v, 'n', len(P), 'masks', len(masks), '%.0fs' % (time.time() - t0), flush=True)
    with open(f'sets_{tag}.jsonl', 'a') as f:
        f.write(json.dumps({'seed': seed, 'pred': pred, 'value': v, 'P': sorted(P)}) + '\n')
    json.dump(sorted(masks), open(f'masks_{tag}_{seed}.json', 'w'))
