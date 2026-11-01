#!/usr/bin/env python3
"""Cross-check dpcheck (C, three DPs) against an independent brute force (Python DFS over subsets in convex
position: a set in general position is convex iff no point lies in a triangle of three others).
Part A: random subsets of the 253-point set (orientation table from exact_orient.py).
Part B: random generic integer point sets (exact integer orientations), including near-convex configurations.
usage: bruteforce_test.py outdir_p9 workdir dpcheck_binary"""
import sys, os, random, subprocess

def load_table(d):
    n = int(open(os.path.join(d, 'ranks.txt')).readline())
    tab = open(os.path.join(d, 'orient_upper.bin'), 'rb').read()
    assert len(tab) == n ** 3
    return n, tab

def make_orient(n, tab):
    n2 = n * n
    def ori(a, b, c):
        s = 1
        if a > b: a, b = b, a; s = -s
        if b > c: b, c = c, b; s = -s
        if a > b: a, b = b, a; s = -s
        v = tab[a * n2 + b * n + c]
        return s if v == 1 else (-s if v == 255 else 0)
    return ori

def brute_max_convex(S, ori):
    """largest subset of S in convex position (DFS, each extension checked against all triples)"""
    m = len(S)
    loc = {}
    for i in range(m):
        for j in range(m):
            for k in range(m):
                if i != j and j != k and i != k:
                    loc[i, j, k] = ori(S[i], S[j], S[k])
    def in_tri(x, a, b, c):
        o1 = loc[a, b, x]; o2 = loc[b, c, x]; o3 = loc[c, a, x]
        return o1 == o2 == o3
    best = [min(m, 2)]
    cur = []
    def dfs(start):
        if len(cur) > best[0]: best[0] = len(cur)
        if len(cur) + (m - start) <= best[0]: return
        for x in range(start, m):
            ok = True
            s = len(cur)
            for i in range(s):
                if not ok: break
                for j in range(i + 1, s):
                    if not ok: break
                    for k in range(j + 1, s):
                        a, b, c = cur[i], cur[j], cur[k]
                        if in_tri(x, a, b, c) or in_tri(a, x, b, c) or in_tri(b, x, a, c) or in_tri(c, x, a, b):
                            ok = False; break
            if ok:
                cur.append(x); dfs(x + 1); cur.pop()
    dfs(0)
    return best[0]

def run_dp(dp, ranks, table, subset_file=None):
    args = [dp, ranks, table] + ([subset_file] if subset_file else [])
    out = subprocess.run(args, capture_output=True, text=True, check=True).stdout
    line = [l for l in out.splitlines() if l.startswith('RESULT')][0].split()
    oks = [l for l in out.splitlines() if 'witness ok=' in l]
    wit_ok = all(('witness ok=1' in l) for l in oks)
    return int(line[1]), int(line[2]), int(line[3]), line[4], wit_ok

def main():
    d, work, dp = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(work, exist_ok=True)
    log = open(os.path.join(work, 'bruteforce_test.log'), 'w')
    def out(*a):
        s = ' '.join(str(x) for x in a); print(s, flush=True); log.write(s + '\n'); log.flush()
    n, tab = load_table(d)
    ori = make_orient(n, tab)
    rng = random.Random(1102)
    p, t = 9, 28
    centre = n - 1
    mism = 0; total = 0
    # Part A
    kinds = []
    for it in range(60):
        kind = it % 6
        if kind == 0:     # uniform random
            S = rng.sample(range(n), rng.randint(14, 18))
        elif kind == 1:   # one cluster (same sector, many layers)
            s0 = rng.randrange(p); layers = rng.sample(range(t), rng.randint(14, 20))
            S = [l * p + s0 for l in layers]
        elif kind == 2:   # two adjacent clusters + centre
            s0 = rng.randrange(p); S = set([centre])
            while len(S) < rng.randint(15, 19):
                S.add(rng.randrange(t) * p + (s0 + rng.randrange(2)) % p)
            S = sorted(S)
        elif kind == 3:   # three or four consecutive clusters
            s0 = rng.randrange(p); w = rng.choice([3, 4]); S = set()
            while len(S) < rng.randint(15, 18):
                S.add(rng.randrange(t) * p + (s0 + rng.randrange(w)) % p)
            S = sorted(S)
        elif kind == 4:   # few layers, all sectors (orbits)
            layers = rng.sample(range(t), 2)
            S = [l * p + s for l in layers for s in range(p)]
            if rng.random() < 0.5: S.append(centre)
        else:             # all sectors, random layers, with centre
            S = set([centre])
            while len(S) < rng.randint(15, 18):
                S.add(rng.randrange(n))
            S = sorted(S)
        S = sorted(set(S))
        fn = os.path.join(work, 'subset.txt')
        with open(fn, 'w') as f: f.write(' '.join(map(str, S)) + '\n')
        r1, r2, r3, agree, wok = run_dp(dp, os.path.join(d, 'ranks.txt'), os.path.join(d, 'orient_upper.bin'), fn)
        b = brute_max_convex(S, ori)
        ok = (r1 == r2 == r3 == b) and agree == 'AGREE' and wok
        total += 1; mism += (not ok)
        out('A kind=%d size=%d  DP %d %d %d  brute %d  %s' % (kind, len(S), r1, r2, r3, b, 'ok' if ok else 'MISMATCH'))
    # Part B: generic integer point sets
    def gen_points(m, mode):
        while True:
            if mode == 'uniform':
                P = [(rng.randrange(10 ** 6), rng.randrange(10 ** 6)) for _ in range(m)]
            elif mode == 'circle':   # perturbed circle: large convex subsets
                import math
                P = []
                for _ in range(m):
                    th = rng.random() * 2 * math.pi; r = 10 ** 6 * (1 + 0.05 * rng.random())
                    P.append((int(r * math.cos(th)), int(r * math.sin(th))))
            else:                    # clustered (two-level), mimics the structured sets
                P = []
                cs = [(rng.randrange(10 ** 7), rng.randrange(10 ** 7)) for _ in range(rng.randint(2, 4))]
                for _ in range(m):
                    cx, cy = rng.choice(cs)
                    P.append((cx + rng.randrange(-10 ** 4, 10 ** 4), cy + rng.randrange(-10 ** 4, 10 ** 4)))
            if len(set(P)) < m: continue
            okgp = True
            for i in range(m):
                for j in range(i + 1, m):
                    for k in range(j + 1, m):
                        (ax, ay), (bx, by), (cx, cy) = P[i], P[j], P[k]
                        if (bx - ax) * (cy - ay) - (by - ay) * (cx - ax) == 0: okgp = False; break
                    if not okgp: break
                if not okgp: break
            if okgp: return P
    for it in range(45):
        mode = ['uniform', 'circle', 'cluster'][it % 3]
        m = rng.randint(12, 17)
        P = gen_points(m, mode)
        tabB = bytearray(m ** 3)
        for i in range(m):
            for j in range(i + 1, m):
                for k in range(j + 1, m):
                    (ax, ay), (bx, by), (cx, cy) = P[i], P[j], P[k]
                    v = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
                    tabB[i * m * m + j * m + k] = 1 if v > 0 else 255
        yr = sorted(range(m), key=lambda i: (P[i][1], P[i][0])); xr = sorted(range(m), key=lambda i: (P[i][0], P[i][1]))
        yrank = [0] * m; xrank = [0] * m
        for r, i in enumerate(yr): yrank[i] = r
        for r, i in enumerate(xr): xrank[i] = r
        rk = os.path.join(work, 'B_ranks.txt'); tb = os.path.join(work, 'B_orient.bin')
        with open(rk, 'w') as f:
            f.write('%d\n' % m)
            for i in range(m): f.write('%d %d\n' % (yrank[i], xrank[i]))
        with open(tb, 'wb') as f: f.write(tabB)
        r1, r2, r3, agree, wok = run_dp(dp, rk, tb)
        b = brute_max_convex(list(range(m)), make_orient(m, tabB))
        ok = (r1 == r2 == r3 == b) and agree == 'AGREE' and wok
        total += 1; mism += (not ok)
        out('B mode=%s size=%d  DP %d %d %d  brute %d  %s' % (mode, m, r1, r2, r3, b, 'ok' if ok else 'MISMATCH'))
    out('TOTAL tests', total, 'mismatches', mism)
    log.close()

if __name__ == '__main__':
    main()
