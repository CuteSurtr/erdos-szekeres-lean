"""Realize small abstract witnesses by real integer points: annealing on the number of wrongly oriented triples.
Accepted only after exact verification (orientation signs equal; then states re-derived by the exact checker).
usage: realize_small.py <in.jsonl with fields T, m, sig, states> <out.jsonl> [max_records] [iters]"""
import sys, json, random, itertools, math
import fl
from fl import *
def realize(m, sig, rng, iters=200000, R=10**6):
    T = list(itertools.combinations(range(m), 3)); s = [1 if c == '+' else -1 for c in sig]
    by = [[] for _ in range(m)]
    for q, t in enumerate(T):
        for p in t: by[p].append(q)
    xs = sorted(rng.sample(range(-R, R), m)); P = [[xs[i], rng.randint(-R, R)] for i in range(m)]
    def sgn(q):
        i, j, k = T[q]
        d = (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
        return 1 if d > 0 else (-1 if d < 0 else 0)
    bad = [sgn(q) != s[q] for q in range(len(T))]; cost = sum(bad)
    for it in range(iters):
        if cost == 0: break
        # pick a point of a violated triple
        q = rng.choice([q for q in range(len(T)) if bad[q]]); p = rng.choice(T[q])
        old = list(P[p]); sc = rng.choice([10, 100, 1000, 10000, 100000, R])
        ny = old[1] + rng.randint(-sc, sc); nx = old[0]
        if rng.random() < 0.3:
            lo = P[p - 1][0] + 1 if p > 0 else -4 * R; hi = P[p + 1][0] - 1 if p + 1 < m else 4 * R
            if hi > lo: nx = rng.randint(lo, hi)
        P[p] = [nx, ny]
        newbad = {q2: (sgn(q2) != s[q2]) for q2 in by[p]}
        delta = sum(newbad.values()) - sum(bad[q2] for q2 in by[p])
        if delta <= 0 or rng.random() < math.exp(-delta / 0.3):
            for q2, b in newbad.items(): bad[q2] = b
            cost += delta
        else: P[p] = old
    return [tuple(p) for p in P] if cost == 0 else None
if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]; mx = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    iters = int(sys.argv[4]) if len(sys.argv) > 4 else 200000
    attempts = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    only = set(int(x) for x in sys.argv[6].split(',')) if len(sys.argv) > 6 else None
    rng = random.Random(7); ok = fail = 0
    import os
    have = set()
    if os.path.exists(out):
        for line in open(out): have.add(tuple(json.loads(line)['T']))
    for line in open(src):
        r = json.loads(line)
        if r.get('status', 'SAT') != 'SAT': continue
        if tuple(r['T']) in have: continue
        if only is not None and not (set(r['T']) & only): continue
        if ok + fail >= mx: break
        P = None
        for attempt in range(attempts):
            P = realize(r['m'], r['sig'], rng, iters)
            if P: break
        if P is None: fail += 1; print('not realized', r['T'], flush=True); continue
        S = Set66(P); assert S.ok and S.in_state == r['states'] and all(t in S.in_state for t in r['T'])
        ok += 1
        with open(out, 'a') as f: f.write(json.dumps({'T': r['T'], 'P': P}) + '\n')
    print(f'realized {ok}, failed {fail}', flush=True)
