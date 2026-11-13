#!/usr/bin/env python3
"""Write a nest/nest3 init file (t lines "lr th") from a gen.py SAT model: phases in the model's psi-order (and H for
odd m), log-radii from a crude fit of the model's orientation signs (perceptron on the polar linear forms).
usage: seed_from_model.py BASE.cnf MODEL OUT.init [passes]
MODEL: a cadical output with v-lines, or a JSON list of true variables (cegar *.model.json)."""
import os, sys, json, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'C7UPPER'))
import gen

base, model, out = sys.argv[1], sys.argv[2], sys.argv[3]
passes = int(sys.argv[4]) if len(sys.argv) > 4 else 300
meta = json.load(open(base + '.json'))
m, K, t = meta['m'], meta['K'], meta['t']
if model.endswith('.json'):
    val = set(json.load(open(model)))
else:
    val = set()
    for l in open(model):
        if l.startswith('v '):
            val.update(int(x) for x in l.split()[1:] if int(x) > 0)
E = gen.Enc(m, K, t)
rank = {0: 0}
for i in range(1, t):
    rank[i] = 1 + sum(1 for j in range(1, t) if j != i and
                      ((E.Y[(min(i, j), max(i, j))] in val) == (j < i)))
unit = math.pi / m if m % 2 else 2 * math.pi / m
th = []
for i in range(t):
    psi = 0.0 if i == 0 else unit * rank[i] / t
    if m % 2 and i > 0 and E.H[i] not in val:
        psi += math.pi / m
    th.append(psi)
ang = lambda x: th[x // m] + 2 * math.pi * (x % m) / m
rows = []
for C, v in E.tvar.items():
    a, b, c = C
    s = 1 if v in val else -1
    co = [0.0] * t
    # orient(a,b,c) ~ u_a sin(g-b) + u_b sin(a-g) + u_c sin(b-a)  (polar formula, u = 1/r)
    A, B, G = ang(a), ang(b), ang(c)
    co[a // m] += math.sin(G - B); co[b // m] += math.sin(A - G); co[c // m] += math.sin(B - A)
    rows.append([s * x for x in co])
u = [1.0 + 0.15 * i for i in range(t)]
best = (-1, u[:])
rnd = random.Random(1)
for p in range(passes):
    rnd.shuffle(rows)
    bad = 0
    for r in rows:
        d = sum(x * y for x, y in zip(r, u))
        if d <= 1e-3:
            bad += 1
            nr = sum(x * x for x in r) or 1.0
            step = (1e-3 - d) / nr
            u = [y + step * x for x, y in zip(r, u)]
    u = [max(y, 1e-6) for y in u]
    u = sorted(u)                          # nesting: radii decrease with the layer index
    ok = sum(1 for r in rows if sum(x * y for x, y in zip(r, u)) > 0)
    if ok > best[0]:
        best = (ok, u[:])
    if bad == 0:
        break
ok, u = best
print(json.dumps({'m': m, 't': t, 'rank': [rank[i] for i in range(t)], 'satisfied': ok, 'rows': len(rows)}))
with open(out, 'w') as f:
    for i in range(t):
        f.write('%.17g %.17g\n' % (-math.log(u[i] / u[0]), th[i]))
