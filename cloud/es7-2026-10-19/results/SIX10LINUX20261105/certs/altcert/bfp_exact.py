"""Exact rational re-solve of a BFP dual vertex: integer kernel of A_B^T (flint), positive integer weights,
greedy support reduction, then write the certificate JSON for check_bfp.py."""
import sys, os, json
import numpy as np
import flint
sys.path.insert(0, '<six10-work-dir>/altcert/lp')
from bfp import *
nm = sys.argv[1]; out = os.path.join('<six10-work-dir>/altcert/lp', nm)
rows = np.load(os.path.join(out, 'cert_rows.npy')); prov = np.load(os.path.join(out, 'cert_prov.npy')); y = np.load(os.path.join(out, 'cert_y.npy'))
order = np.argsort(-y); rows = rows[order]; prov = prov[order]; y = y[order]
def kernel_pos(idx):
    """integer positive kernel vector of A_idx^T if the kernel is 1-dim and positive; else None"""
    R = rows[idx]; vs = sorted({int(v) for v in R.ravel() if v > 0}); vi = {v: k for k, v in enumerate(vs)}
    Mt = [[0] * len(idx) for _ in vs]
    for c, r in enumerate(R):
        for k, sg in ((0, 1), (1, 1), (2, -1), (3, -1)):
            if r[k] > 0: Mt[vi[int(r[k])]][c] += sg
    K, nul = flint.fmpz_mat(Mt).nullspace()
    return K, nul, len(vs)
idx = list(range(len(rows)))
K, nul, nv = kernel_pos(idx)
print('support', len(idx), 'vars', nv, 'kernel dim', nul, flush=True)
if nul == 1:
    w = [int(K[i, 0]) for i in range(len(idx))]
    if all(x <= 0 for x in w): w = [-x for x in w]
    assert all(x > 0 for x in w), 'kernel vector not positive'
else:
    # several kernel vectors: find positive combination close to float y via least squares, then rationalize
    B = np.array([[float(K[i, k]) for k in range(nul)] for i in range(len(idx))])
    coef, *_ = np.linalg.lstsq(B, y, rcond=None)
    from fractions import Fraction
    best = None
    for den in (1, 2, 4, 8, 16, 64, 256, 1024, 10**4, 10**6):
        cq = [Fraction(round(c * den * 1e6)) / (den * 10**6) for c in coef]
        cq = [Fraction(c).limit_denominator(den) for c in coef]
        w = [sum(cq[k] * int(K[i, k]) for k in range(nul)) for i in range(len(idx))]
        if all(x > 0 for x in w): best = w; break
    assert best is not None, 'no positive rational combination found'
    import math
    L = math.lcm(*[x.denominator for x in best]); w = [int(x * L) for x in best]
g = 0
import math
for x in w: g = math.gcd(g, x)
w = [x // g for x in w]
comps = []; clause = set()
pos = load_model(nm)
for r, p, wt in zip(rows[idx], prov[idx], w):
    a, b, c, d, e, m, j = map(int, p)
    comps.append({'quintuple': [a, b, c, d, e], 'minority': m, 'other': j, 'weight': wt})
    for T in [(a, b, c), (a, d, e), (a, b, d), (a, c, e), (a, b, e), (a, c, d)]:
        v = abs(E.o(*T)); clause.add(-v if v in pos else v)
cert = {'model': nm, 'type': 'biquadratic final polynomial (GP 3-term identities, rotation-orbit magnitudes)',
        'clause': sorted(clause, key=abs), 'comparisons': comps}
json.dump(cert, open(os.path.join(out, 'bfp_cert.json'), 'w'))
print('certificate written: comparisons', len(comps), 'clause length', len(clause), 'max weight', max(w))
