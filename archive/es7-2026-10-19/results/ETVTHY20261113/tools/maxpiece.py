"""Local search maximizing a piece size (e.g. |R6|, |R7|, |L4|) over 5-cap-free octagon-free sets."""
import sys, random, json, math, time
import numpy as np
sys.path.insert(0, '/home/jay/research/data/etvthy-20261113')
from esgeo import Analysis

def evaluate(P, piece):
    try:
        A = Analysis(P)
    except ValueError:
        return None
    n = A.n
    if n >= 2:
        if A.capB.max() > 4 or A.cupB.max() > 7: return None
        if (A.capB + A.cupB).max() - 2 > 7: return None
    beta = A.cup_end; cp = A.cap_start; cm = A.cap_end
    if piece == 'R6': v = sum(1 for b in beta if b >= 6)
    elif piece == 'R7': v = sum(1 for b in beta if b >= 7)
    elif piece == 'B6': v = sum(1 for b in beta if b == 6)
    elif piece == 'L4': v = sum(1 for c in cp if c >= 4)
    elif piece == 'M': v = sum(1 for i in range(n) if cp[i] >= 4 and cm[i] >= 4)
    elif piece == 'Y': v = sum(1 for i in range(n) if beta[i] == 6 and cp[i] >= 4)
    elif piece == 'size': v = n
    elif piece == 'DR': v = sum(1 for i in range(n) if cm[i] + beta[i] >= 9)
    elif piece == 'DRL4': v = sum(1 for i in range(n) if cm[i] + beta[i] >= 9 and cp[i] >= 4)
    else: raise ValueError(piece)
    return v

def run(seed, piece, iters, init=None, T0=0.6):
    random.seed(seed); R = 10**6
    P = list(init) if init else []
    cur = evaluate(P, piece) if P else 0
    best = (cur, list(P))
    gen = lambda: (random.randint(-R, R), random.randint(-R, R))
    for it in range(iters):
        T = T0 * (1 - it/iters) + 0.02
        r = random.random(); Q = list(P)
        if r < 0.45 or len(Q) < 5:
            Q.append(gen())
        elif r < 0.85:
            k = random.randrange(len(Q)); x, y = Q[k]
            s = random.choice([1000, 10000, 100000, R])
            Q[k] = (x + random.randint(-s, s), y + random.randint(-s, s))
        else:
            Q.pop(random.randrange(len(Q)))
        if len({q[0] for q in Q}) < len(Q): continue
        v = evaluate(Q, piece)
        if v is None: continue
        score_new = v + 0.01*len(Q); score_cur = cur + 0.01*len(P)
        if score_new >= score_cur or random.random() < math.exp((score_new - score_cur)/T):
            P, cur = Q, v
            if (cur, len(P)) > (best[0], len(best[1])): best = (cur, list(P))
    return best

if __name__ == '__main__':
    seed, piece, iters, out = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4]
    init = None
    if len(sys.argv) > 5:
        init = [tuple(p) for p in json.load(open(sys.argv[5]))]
    t0 = time.time()
    v, P = run(seed, piece, iters, init)
    print(seed, piece, v, len(P), '%.0fs' % (time.time()-t0), flush=True)
    with open(out, 'a') as f: f.write(json.dumps({'seed': seed, 'piece': piece, 'value': v, 'P': sorted(P)}) + '\n')
