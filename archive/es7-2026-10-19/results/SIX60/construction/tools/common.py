"""Common helpers for the realization probes (evidence-only numerics; exact checks live in exact_check.py)."""
import os, json, importlib.util, itertools
import numpy as np
from pathlib import Path
RES = Path(os.environ.get('ES_RESULTS', '<results-dir>'))
HM = RES / 'SIX10CEGAR/hard_models'
MODELS = Path('<six10-work-dir>/models')


def load_mod(name, p):
    s = importlib.util.spec_from_file_location(name, str(p)); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


G = load_mod('enc', RES / 'C7UPPER/gen.py')
E = G.Enc(6, 8, 10)
C = sorted(E.tvar, key=E.tvar.get)          # canonical triples, index = var-1
T = np.array(C, dtype=np.int64)             # (5710,3)
TL = T // 6; TK = T % 6
NT = len(C)
CUBES = ['c00000', 'c00001', 'c01001', 'c10000', 'c10100', 'c11000', 'c11001', 'c11011', 'c11110', 'c11111']


def core(cube):
    """CUBE may be a cube name (hard-core cluster representative) or a path to a model JSON (list of true vars).
    returns dict: want (+-1 per triple var, representative), free (bool mask), pos (set of true vars incl. phase)"""
    if cube.endswith('.json'):
        pos = set(json.load(open(cube)))
        want = np.array([1 if (v + 1) in pos else -1 for v in range(NT)], dtype=np.int64)
        return {'cube': cube, 'pos': pos, 'want': want, 'free': np.zeros(NT, bool), 'free_vars': [], 'free_phase': [], 'members': []}
    d = json.load(open(HM / f'cluster_{cube}.json'))
    pos = set(d['representative_true_vars'])
    want = np.array([1 if (v + 1) in pos else -1 for v in range(NT)], dtype=np.int64)
    free = np.zeros(NT, bool)
    for v in d['free_triple_vars']:
        free[v - 1] = True
    return {'cube': cube, 'pos': pos, 'want': want, 'free': free, 'free_vars': d['free_triple_vars'],
            'free_phase': d['free_phase_vars'], 'members': d['members']}


def less(pos, i, j):
    if i == j: raise ValueError
    if i == 0: return True
    if j == 0: return False
    if i < j: return E.Y[(i, j)] in pos
    return not (E.Y[(j, i)] in pos)


def phase_order(pos):
    """layers sorted by increasing theta (layer 0 first)"""
    import functools
    return sorted(range(10), key=functools.cmp_to_key(lambda a, b: 0 if a == b else (-1 if less(pos, a, b) else 1)))


W = np.exp(1j * np.pi / 3)


def orient_z(z):
    """float orientation of every canonical triple for seeds z (complex, len 10): orient(a,b,c) = Im(conj(b-a)(c-a))."""
    P = z[TL] * W ** TK
    a, b, c = P[:, 0], P[:, 1], P[:, 2]
    return (np.conj(b - a) * (c - a)).imag


def wrong(z, want, free=None, mask=None):
    o = orient_z(z)
    bad = np.sign(o) != want
    if free is not None: bad &= ~free
    if mask is not None: bad &= mask
    return bad


def layer_mask(layers):
    s = np.zeros(10, bool); s[list(layers)] = True
    return s[TL].all(axis=1)


def convention_ok(z, tol=0.0):
    """theta_0 = 0 (up to global rotation), theta_i in (0,60deg) after rotating so theta_0=0, radii decreasing"""
    z = np.asarray(z) / z[0] * abs(z[0])
    th = np.angle(z) % (2 * np.pi)
    r = np.abs(z)
    ok_th = all(0 < th[i] < np.pi / 3 for i in range(1, 10))
    ok_r = all(r[i] > r[i + 1] for i in range(9))
    return ok_th, ok_r, th, r


def read_pts(path):
    """ES8SYM .pts: rows of 6 integers w_j, point = sum_j w_j zeta^j, zeta = exp(2 pi i/6). Returns int rows and complex."""
    rows = []
    for line in open(path):
        if line.startswith('#') or not line.strip(): continue
        rows.append([int(x) for x in line.split()])
    zeta = np.exp(2j * np.pi / 6)
    pts = np.array([sum(w * zeta ** j for j, w in enumerate(r)) for r in rows])
    return rows, pts


def normalize_seeds(z):
    """Given one complex seed per layer (any vertex), return seeds in the encoding convention: layers sorted by
    decreasing radius, global rotation so that the layer-0 seed is on the positive real axis, each seed rotated by a
    multiple of 60 deg into angle [0, 60)."""
    z = np.asarray(z, complex)
    z = z[np.argsort(-np.abs(z))]
    z = z * abs(z[0]) / z[0]
    out = []
    for x in z:
        a = np.angle(x) % (np.pi / 3)
        out.append(abs(x) * np.exp(1j * a))
    return np.array(out)


def chi_from_z(z):
    """full orientation table chi[a,b,c] (float sign) for points id 6i+k = w^k z_i"""
    n = 6 * len(z)
    P = np.array([z[x // 6] * W ** (x % 6) for x in range(n)])
    A = P[:, None, None]; B = P[None, :, None]; Cc = P[None, None, :]
    return np.sign((np.conj(B - A) * (Cc - A)).imag).astype(np.int8)


def chi_from_want(want, nlayers=10):
    n = 6 * nlayers
    chi = np.zeros((n, n, n), np.int8)
    for a, b, c in itertools.combinations(range(n), 3):
        s = E.o(a, b, c)
        v = want[abs(s) - 1] * (1 if s > 0 else -1)
        for (x, y, zz), sg in (((a, b, c), 1), ((b, c, a), 1), ((c, a, b), 1), ((b, a, c), -1), ((a, c, b), -1), ((c, b, a), -1)):
            chi[x, y, zz] = v * sg
    return chi


def model_core(path):
    """a model file (JSON list of true vars) as a core dict with no free signs"""
    pos = set(json.load(open(path)))
    want = np.array([1 if (v + 1) in pos else -1 for v in range(NT)], dtype=np.int64)
    return {'cube': os.path.basename(path), 'pos': pos, 'want': want, 'free': np.zeros(NT, bool), 'free_vars': [], 'free_phase': [], 'members': []}
