#!/usr/bin/env python3
"""Try to realize a gen.py model (orientation signs of all triple orbits) by nested regular m-gons: gradient descent on
a hinge loss over (u_i = 1/r_i, phases theta_i), polar formula.  Heuristic search only; any hit is re-verified exactly
elsewhere.  usage: realize.py BASE.cnf MODEL.json OUT.init seconds seed"""
import os, sys, json, math, random, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'C7UPPER'))
import gen

base, model, out, secs, seed = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
meta = json.load(open(base + '.json'))
m, K, t = meta['m'], meta['K'], meta['t']
val = set(json.load(open(model)))
E = gen.Enc(m, K, t)
rank = {0: 0}
for i in range(1, t):
    rank[i] = 1 + sum(1 for j in range(1, t) if j != i and
                      ((E.Y[(min(i, j), max(i, j))] in val) == (j < i)))
unit = math.pi / m if m % 2 else 2 * math.pi / m
hoff = [0.0] * t
if m % 2:
    for i in range(1, t):
        if E.H[i] not in val:
            hoff[i] = math.pi / m
rows = []   # (s, la, lb, lc, ka, kb, kc) angles = th[l] + 2 pi k/m
for C, v in E.tvar.items():
    a, b, c = C
    rows.append((1 if v in val else -1, a // m, b // m, c // m,
                 2 * math.pi * (a % m) / m, 2 * math.pi * (b % m) / m, 2 * math.pi * (c % m) / m))
rnd = random.Random(seed)
order = sorted(range(1, t), key=lambda i: rank[i])


def phases(x):
    # x: t-1 positive gaps -> psi in (0, unit) increasing in rank order
    tot = sum(x) + 1.0
    th = [0.0] * t
    acc = 0.0
    for i, g in zip(order, x):
        acc += g
        th[i] = unit * acc / tot + hoff[i]
    return th


def evaluate(lu, x, need_grad):
    u = [math.exp(z) for z in lu]
    th = phases(x)
    nbad = 0
    loss = 0.0
    gu = [0.0] * t
    gth = [0.0] * t
    for s, la, lb, lc, ka, kb, kc in rows:
        A, B, G = th[la] + ka, th[lb] + kb, th[lc] + kc
        s1, s2, s3 = math.sin(G - B), math.sin(A - G), math.sin(B - A)
        f = s * (u[la] * s1 + u[lb] * s2 + u[lc] * s3)
        sc = u[la] + u[lb] + u[lc] + 1e-300
        mg = f / sc
        if mg <= 0:
            nbad += 1
        if mg < 0.02 and need_grad:
            loss += 0.02 - mg
            c1, c2, c3 = math.cos(G - B), math.cos(A - G), math.cos(B - A)
            # d f / d u, d f / d angles (ignoring the normalisation derivative)
            gu[la] -= s * s1 * u[la] / sc; gu[lb] -= s * s2 * u[lb] / sc; gu[lc] -= s * s3 * u[lc] / sc
            gth[la] -= s * (u[lb] * c2 - u[lc] * c3) / sc
            gth[lb] -= s * (-u[la] * c1 + u[lc] * c3) / sc
            gth[lc] -= s * (u[la] * c1 - u[lb] * c2) / sc
    return nbad, loss, gu, gth


best = None
t0 = time.time()
restart = 0
while time.time() - t0 < secs:
    lu = sorted(rnd.uniform(0, 4) for _ in range(t)); lu = [z - lu[0] for z in lu]
    x = [rnd.uniform(0.2, 1.0) for _ in range(t - 1)]
    lr = 0.05
    for it in range(4000):
        nbad, loss, gu, gth = evaluate(lu, x, True)
        if best is None or nbad < best[0]:
            best = (nbad, lu[:], x[:])
            print('restart', restart, 'it', it, 'violated', nbad, 'loss %.3f' % loss, 'time %.0f' % (time.time() - t0),
                  flush=True)
            with open(out, 'w') as f:
                th = phases(x)
                for i in range(t):
                    f.write('%.17g %.17g\n' % (-(lu[i] - lu[0]), th[i]))
        if nbad == 0 or time.time() - t0 > secs:
            break
        ng = math.sqrt(sum(g * g for g in gu) + sum(g * g for g in gth)) + 1e-12
        step = lr * (0.999 ** it)
        gu = [g / ng for g in gu]; gth = [g / ng for g in gth]
        lu = [max(min(z - step * g, 12.0), -12.0) for z, g in zip(lu, gu)]
        lu[0] = 0.0
        # gradient wrt gaps via finite structure: move each layer's phase, then re-derive gaps
        th = phases(x)
        newth = [th[i] - hoff[i] - step * 0.3 * gth[i] for i in range(t)]
        seq = [newth[i] for i in order]
        seq = [min(max(v, 1e-4 * unit), unit * (1 - 1e-4)) for v in seq]
        seq.sort()
        gaps = [seq[0]] + [max(seq[j] - seq[j - 1], 1e-5) for j in range(1, len(seq))]
        tot_target = unit - seq[-1]
        sc = 1.0 / max(tot_target, 1e-5)
        x = [g * sc for g in gaps]
    if best[0] == 0:
        break
    restart += 1
print('BEST violated', best[0], 'of', len(rows))
