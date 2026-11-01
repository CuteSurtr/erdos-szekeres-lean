# Side check (numerical, HiGHS via scipy): LP value of the balanced/residual systems with and without the C6 constraints.
import gzip, json, numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
def load(p):
    raw = open(p, 'rb').read(); d = json.loads(gzip.decompress(raw) if p.endswith('.gz') else raw)
    return len(d['states']), [(r['support'], int(r['rhs'])) for r in d['constraints']]
def lp(n, rows, extra_eq0=(), extra_le=()):
    A = lil_matrix((len(rows) + len(extra_le), n)); b = []
    for k, (s, d) in enumerate(rows):
        for i in s: A[k, i] = -1.0
        b.append(-d)
    for k, (s, cap) in enumerate(extra_le):
        for i in s: A[len(rows) + k, i] = 1.0
        b.append(cap)
    bounds = [(0, 0) if i in extra_eq0 else (0, 1) for i in range(n)]
    r = linprog(np.ones(n), A_ub=A.tocsr(), b_ub=np.array(b, float), bounds=bounds, method='highs')
    return r.fun
nb, rb = load(ROOT + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json')
nr, rr = load(ROOT + '/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz')
print('balanced LP plain          %.4f' % lp(nb, rb))
print('balanced LP + h0=h1=0, h2+h3<=1  %.4f' % lp(nb, rb, (0, 1), [((2, 3), 1)]))
print('residual LP plain          %.4f' % lp(nr, rr))
print('residual LP + h0=0         %.4f' % lp(nr, rr, (0,)))
print('residual LP + h0=0, h1+h2+h4+h7<=3  %.4f' % lp(nr, rr, (0,), [((1, 2, 4, 7), 3)]))
