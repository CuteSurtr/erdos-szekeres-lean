"""Python wrapper for libesgeo.so: exact cap/cup/convex-polygon analysis.
Points: list of (x, y) Python ints, |coords| < 2^62, distinct x, general position."""
import ctypes, os, itertools
import numpy as np
_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libesgeo.so'))
_P = ctypes.POINTER
_lib.analyze.argtypes = [ctypes.c_int, _P(ctypes.c_longlong), _P(ctypes.c_longlong)] + [_P(ctypes.c_int)]*6
_lib.quick.argtypes = [ctypes.c_int, _P(ctypes.c_longlong), _P(ctypes.c_longlong), _P(ctypes.c_int), _P(ctypes.c_int)]

def orient(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])

def _arr(P):
    n = len(P)
    X = (ctypes.c_longlong*n)(*[p[0] for p in P]); Y = (ctypes.c_longlong*n)(*[p[1] for p in P])
    return X, Y

def quick(P):
    """P sorted by x. Returns (largest convex polygon, max cap, max cup); negative first entry on error."""
    P = sorted(P); X, Y = _arr(P); mc = ctypes.c_int(); mu = ctypes.c_int()
    r = _lib.quick(len(P), X, Y, ctypes.byref(mc), ctypes.byref(mu))
    return r, mc.value, mu.value

class Analysis:
    def __init__(self, P, between=True):
        P = sorted(P); self.P = P; n = self.n = len(P)
        X, Y = _arr(P)
        bufs = [np.zeros(n*n, dtype=np.int32) for _ in range(6)]
        ptr = lambda a: a.ctypes.data_as(_P(ctypes.c_int))
        r = _lib.analyze(n, X, Y, *[ptr(b) for b in bufs[:4]], *( [ptr(b) for b in bufs[4:]] if between else [None, None]))
        if r != 0: raise ValueError('bad point set %d' % r)
        self.capE, self.cupE, self.capS, self.cupS, self.capB, self.cupB = [b.reshape(n, n) for b in bufs]
        # per-point
        self.cup_end = [max([1]+[int(self.cupE[i, j]) for i in range(j)]) for j in range(n)]
        self.cap_end = [max([1]+[int(self.capE[i, j]) for i in range(j)]) for j in range(n)]
        self.cup_start = [max([1]+[int(self.cupS[i, j]) for j in range(i+1, n)]) for i in range(n)]
        self.cap_start = [max([1]+[int(self.capS[i, j]) for j in range(i+1, n)]) for i in range(n)]
    def gon(self):
        n = self.n
        return max([0]+[int(self.capB[s, t]+self.cupB[s, t]-2) for s in range(n) for t in range(s+1, n)])
    def o(self, a, b, c):
        return orient(self.P[a], self.P[b], self.P[c])

def brute(P):
    """Brute force (small n): max cap, max cup, max convex polygon."""
    P = sorted(P); n = len(P)
    def is_chain(idx, sgn):
        return all((orient(P[idx[k]], P[idx[k+1]], P[idx[k+2]]) > 0) == (sgn > 0) for k in range(len(idx)-2))
    mc = mu = 1; mg = 0
    for r in range(2, n+1):
        for idx in itertools.combinations(range(n), r):
            if is_chain(idx, -1): mc = max(mc, r)
            if is_chain(idx, +1): mu = max(mu, r)
            if r >= 3 and mg < r:
                # convex position test via hull size
                pts = [P[i] for i in idx]
                lo = []; up = []
                for p in pts:
                    while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0: lo.pop()
                    lo.append(p)
                for p in reversed(pts):
                    while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0: up.pop()
                    up.append(p)
                if len(lo)+len(up)-2 == r: mg = r
    return mg, mc, mu

_lib.gon_witness.argtypes = [ctypes.c_int, _P(ctypes.c_longlong), _P(ctypes.c_longlong), ctypes.c_int, _P(ctypes.c_int)]
def gon_witness(P, k):
    """P sorted by x. Returns indices (into sorted P) of a convex k-gon, or None."""
    P = sorted(P); X, Y = _arr(P); out = (ctypes.c_int*64)()
    r = _lib.gon_witness(len(P), X, Y, k, out)
    if r < 0: raise ValueError('bad set')
    return sorted(out[i] for i in range(r)) if r else None

def is_convex_position(pts):
    pts = sorted(pts)
    lo = []; up = []
    for p in pts:
        while len(lo) >= 2 and orient(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and orient(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return len(lo) + len(up) - 2 == len(pts)
