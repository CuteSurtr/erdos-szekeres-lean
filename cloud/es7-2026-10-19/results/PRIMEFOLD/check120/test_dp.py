#!/usr/bin/env python3
"""Validate cvxcount (DPA, DPB) against brute force bf on
   (a) random integer point sets of several shapes (exact integer orientations),
   (b) random subsets of a real point set given by its exact orientation table + orders.
Usage: test_dp.py OUTDIR FULL_OTAB FULL_ORDERS NTRIALS_RANDOM NTRIALS_SUBSET
"""
import sys, os, random, subprocess, math, itertools

OUT = sys.argv[1]
FULL_OTAB, FULL_ORD = sys.argv[2], sys.argv[3]
NR, NS = int(sys.argv[4]), int(sys.argv[5])
CVX = os.path.join(OUT, 'cvxcount'); BF = os.path.join(OUT, 'bf')
TMP = os.path.join(OUT, 'tmp_test'); os.makedirs(TMP, exist_ok=True)

def write_table(path, n, sgn):
    with open(path, 'wb') as f:
        f.write(('%d\n' % n).encode())
        f.write(bytes((sgn(a, b, c) & 0xFF) for a in range(n) for b in range(n) for c in range(n)))

def parse_counts(txt, tag):
    d = {}
    for line in txt.splitlines():
        if tag == 'cvx' and line.startswith('convex'):
            k = int(line.split()[1].split('-')[0]); parts = line.split()
            d[k] = (int(parts[3]), int(parts[5]))
        if tag == 'bf' and line.startswith('bf convex'):
            k = int(line.split()[2].split('-')[0]); d[k] = int(line.split()[3])
    return d

def run_pair(otab, orders, K):
    r1 = subprocess.run([CVX, otab, orders, str(K)], capture_output=True, text=True)
    r2 = subprocess.run([BF, otab, str(K)], capture_output=True, text=True)
    if r1.returncode not in (0, 3):
        raise SystemExit('cvxcount failed: ' + r1.stdout + r1.stderr)
    a = parse_counts(r1.stdout, 'cvx'); b = parse_counts(r2.stdout, 'bf')
    ok = all(a[k][0] == a[k][1] == b[k] for k in range(3, K + 1))
    return ok, a, b

def gen_points(n, shape, rng):
    pts = set()
    while len(pts) < n:
        if shape == 'uniform':
            p = (rng.randint(-1000, 1000), rng.randint(-1000, 1000))
        elif shape == 'circle':
            t = rng.random() * 2 * math.pi
            r = 1000 * (1 if rng.random() < 0.7 else rng.random())
            p = (round(r * math.cos(t)), round(r * math.sin(t)))
        elif shape == 'twocircles':
            t = rng.random() * 2 * math.pi
            r = 1000 if rng.random() < 0.5 else 300
            p = (round(r * math.cos(t)), round(r * math.sin(t)))
        else:  # parabola-ish cups and caps
            x = rng.randint(-1000, 1000)
            y = (x * x) // 1000 + rng.randint(-3, 3)
            if rng.random() < 0.5: y = -y + 50
            p = (x, y)
        pts.add(p)
    return list(pts)

def orient_int(P, a, b, c):
    (x1, y1), (x2, y2), (x3, y3) = P[a], P[b], P[c]
    d = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    return (d > 0) - (d < 0)

rng = random.Random(20261102)
fails = 0; done = 0; maxk_seen = {}
shapes = ['uniform', 'circle', 'twocircles', 'parab']
for trial in range(NR):
    shape = shapes[trial % 4]
    n = rng.randint(10, 17)
    while True:
        P = gen_points(n, shape, rng)
        if all(orient_int(P, a, b, c) != 0 for a, b, c in itertools.combinations(range(n), 3)):
            break
    K = 10
    otab = os.path.join(TMP, 'r.otab'); ordf = os.path.join(TMP, 'r.orders')
    write_table(otab, n, lambda a, b, c: orient_int(P, a, b, c))
    oy = sorted(range(n), key=lambda i: (P[i][1], P[i][0]))
    ox = sorted(range(n), key=lambda i: (P[i][0], P[i][1]))
    with open(ordf, 'w') as f:
        f.write(' '.join(map(str, oy)) + '\n' + ' '.join(map(str, ox)) + '\n')
    ok, a, b = run_pair(otab, ordf, K)
    mk = max([k for k in range(3, K + 1) if b[k]] or [0])
    maxk_seen[(shape, mk)] = maxk_seen.get((shape, mk), 0) + 1
    done += 1
    if not ok:
        fails += 1
        print('RANDOM MISMATCH', shape, n, a, b)
print('random sets: %d tested, %d mismatches; (shape, largest convex subset) histogram: %s'
      % (done, fails, sorted(maxk_seen.items())))

# (b) subsets of the real set
d = open(FULL_OTAB, 'rb').read(); h = d.index(b'\n'); N = int(d[:h]); FT = d[h + 1:]
lines = open(FULL_ORD).read().split('\n')
OY = list(map(int, lines[0].split())); OX = list(map(int, lines[1].split()))
def fsg(a, b, c):
    v = FT[(a * N + b) * N + c]
    return v - 256 if v > 127 else v
sfails = 0; sdone = 0; hist = {}
for trial in range(NS):
    n = rng.randint(14, 18)
    mode = trial % 3
    if mode == 0:
        sub = sorted(rng.sample(range(N), n))
    elif mode == 1:   # biased to the cluster + outer layer (where large convex sets live)
        pool = list(range(0, 8)) + list(range(8, 112))
        sub = sorted(rng.sample(pool, n))
    else:             # whole layers: pick 2 layers fully
        L = rng.sample(range(N // 8), 2)
        sub = sorted([8 * l + k for l in L for k in range(8)])
        n = len(sub)
    idx = {v: i for i, v in enumerate(sub)}
    otab = os.path.join(TMP, 's.otab'); ordf = os.path.join(TMP, 's.orders')
    write_table(otab, n, lambda a, b, c: fsg(sub[a], sub[b], sub[c]))
    oy = [idx[v] for v in OY if v in idx]; ox = [idx[v] for v in OX if v in idx]
    with open(ordf, 'w') as f:
        f.write(' '.join(map(str, oy)) + '\n' + ' '.join(map(str, ox)) + '\n')
    K = 10
    ok, a, b = run_pair(otab, ordf, K)
    mk = max([k for k in range(3, K + 1) if b[k]] or [0])
    hist[mk] = hist.get(mk, 0) + 1
    sdone += 1
    if not ok:
        sfails += 1
        print('SUBSET MISMATCH', sub, a, b)
print('real-set subsets: %d tested, %d mismatches; largest convex subset histogram: %s'
      % (sdone, sfails, sorted(hist.items())))
