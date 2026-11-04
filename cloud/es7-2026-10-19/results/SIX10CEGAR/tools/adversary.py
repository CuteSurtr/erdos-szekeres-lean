#!/usr/bin/env python3
"""adversary.py OUT.json [SAMPLE] : numerical attack on the shared cuts (evidence only, independent of the checkers).
A cut forbids the sign pattern s_t on its records t; it is valid iff no real seed vector z gives s_t*orient_t(z) > 0
for all of them.  For each cut, maximise min_t s_t*orient_t(z)/|z|^2 over z in R^20 (softmin + L-BFGS, several
random starts, including starts on the model0090 face).  The certificates imply the maximum is <= 0, so a clearly
positive value would expose an unsound cut.  Default: every cut without a surviving witness plus 300 others."""
import sys, json, random, numpy as np, importlib.util
from pathlib import Path
from scipy.optimize import minimize
W = Path('<run-dir>')
RES = Path('<review-results>')
s = importlib.util.spec_from_file_location('enc', RES / 'C7UPPER/gen.py'); G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
E = G.Enc(6, 8, 10); inv = {v: C for C, v in E.tvar.items()}
cuts = [[int(x) for x in l.split()[:-1]] for l in (W / 'cuts.clauses').read_text().splitlines() if l.strip()]
aud = {int(r.split('\t')[0]): r.split('\t')[1] for r in (W / 'audit1' / 'audit.tsv').read_text().splitlines()}
nowit = [i for i, st in aud.items() if st == 'none']
others = [i for i in range(len(cuts)) if aud.get(i) != 'none']
random.seed(7); pick = nowit + random.sample(others, min(300, len(others)))
if len(sys.argv) > 2: pick = pick[:int(sys.argv[2])]
w6 = np.exp(1j * np.pi / 3)


def prep(c):
    T = np.array([inv[abs(l)] for l in c]); sg = np.array([-1.0 if l > 0 else 1.0 for l in c])
    return T // 6, T % 6, sg


def vals(p, L, K, sg):
    z = p[:10] + 1j * p[10:]; P = z[L] * w6 ** K
    a, b, c = P[:, 0], P[:, 1], P[:, 2]
    o = ((np.conj(b - a)) * (c - a)).imag
    return sg * o / (np.sum(p * p) + 1e-300)


def obj(p, L, K, sg, tau):
    v = vals(p, L, K, sg); return float(tau * np.logaddexp.reduce(-v / tau))   # smooth -min


rng = np.random.default_rng(3)
worst = []; out = {}
for n, i in enumerate(pick):
    L, K, sg = prep(cuts[i]); best = -np.inf
    for st in range(6):
        if st < 3:
            p = rng.normal(size=20)
        else:   # near the model0090 face: layer 0 free, layers 1..4 = w*z_5, layers 5..8 = z_5, layer 9 = 0
            z = np.zeros(10, complex); z[0] = 1.0; vv = (0.4 + 0.1j) * np.exp(1j * rng.uniform(0, 1))
            z[1:5] = vv * w6; z[5:9] = vv; z += 1e-3 * (rng.normal(size=10) + 1j * rng.normal(size=10))
            p = np.concatenate([z.real, z.imag])
        for tau in (1e-2, 1e-3, 1e-4):
            p = minimize(obj, p, args=(L, K, sg, tau), method='L-BFGS-B', options={'maxiter': 200}).x
        best = max(best, float(vals(p, L, K, sg).min()))
    out[i] = best; worst.append((best, i))
    if n % 200 == 0: print(n, 'done; max so far %.3g' % max(worst)[0], flush=True)
worst.sort(reverse=True)
json.dump({'tested': len(pick), 'without_witness_tested': len([i for i in pick if i in set(nowit)]),
           'max_of_max_min': worst[0][0], 'top5': worst[:5], 'positive_over_1e-9': [i for b, i in worst if b > 1e-9]},
          open(sys.argv[1], 'w'), indent=1)
print('tested %d cuts; largest max-min value %.3g (cut %d); cuts with value > 1e-9: %d' % (len(pick), worst[0][0], worst[0][1], sum(b > 1e-9 for b, _ in worst)))
