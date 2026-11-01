"""Shared loaders for the ES8SLACK probes (read-only access to the repository catalogs)."""
import gzip, json, os
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
# repository root = probes/../../../../.. (results/ES8SLACK/probes); ES_REPO_ROOT overrides it
ROOT = os.environ.get('ES_REPO_ROOT') or os.path.normpath(os.path.join(_HERE, '..', '..', '..', '..', '..'))
R = ROOT + '/experiments'
BAL_V2 = R + '/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
BAL_V1 = R + '/omission-cover-certificates-2026-10-10/balanced-source.json'
RES_2650 = R + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'


def load(path):
    d = json.load(gzip.open(path) if path.endswith('.gz') else open(path))
    states = d['states']
    rows = [(sorted(r['support']), int(r['rhs'])) for r in d['constraints']]
    return states, rows


def matrix(n, rows):
    from scipy.sparse import csr_matrix
    data, ind, ptr = [], [], [0]
    for s, _ in rows:
        ind += s
        data += [1.0] * len(s)
        ptr.append(len(ind))
    A = csr_matrix((np.array(data), np.array(ind), np.array(ptr)), shape=(len(rows), n))
    b = np.array([d for _, d in rows], float)
    return A, b


def check_exact(rows, holes):
    """Exact integer check: returns list of violated row indices."""
    H = set(holes)
    return [k for k, (s, d) in enumerate(rows) if sum(1 for i in s if i in H) < d]
