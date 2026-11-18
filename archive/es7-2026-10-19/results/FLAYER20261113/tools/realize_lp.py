"""Stronger realizer for abstract configurations (signotopes): search over the x-coordinates only; for fixed
x the y-coordinates are found by a linear programme.

For x_0 < ... < x_{n-1} the orientation of (i,j,k), i<j<k, is the sign of the second divided difference
  f[x_i,x_j,x_k] = y_i/((x_i-x_j)(x_i-x_k)) + y_j/((x_j-x_i)(x_j-x_k)) + y_k/((x_k-x_i)(x_k-x_j)),
which is linear in y.  LP: maximize t subject to sig_ijk * f[x_i,x_j,x_k] >= t, |y_i| <= 1, y_0 = y_{n-1} = 0
(adding an affine function to y changes nothing).  The configuration is realizable iff t*(x) > 0 for some x.
Annealing over the gaps of x maximizes t*(x).  A positive value is only a proposal: the point set is rounded
to integers and ALL orientation signs are re-checked exactly.
usage: realize_lp.py <file.jsonl|.json with n (or m), sig> <restarts> <steps> <out.jsonl> [only_uncertified 0/1] [max_records]
"""
import sys, json, itertools, math, random, time
import numpy as np
from scipy.optimize import linprog

class LPRealizer:
    def __init__(self, n, sig):
        self.n = n; self.T = list(itertools.combinations(range(n), 3))
        self.s = np.array([1.0 if c == '+' else -1.0 for c in sig])
        self.I = np.array([t[0] for t in self.T]); self.J = np.array([t[1] for t in self.T]); self.K = np.array([t[2] for t in self.T])
        self.rows = np.arange(len(self.T))
    def margin(self, x):
        n = self.n; I, J, K, s = self.I, self.J, self.K, self.s
        xi, xj, xk = x[I], x[J], x[K]
        ci = 1.0 / ((xi - xj) * (xi - xk)); cj = 1.0 / ((xj - xi) * (xj - xk)); ck = 1.0 / ((xk - xi) * (xk - xj))
        # normalize each constraint (scale-free margin): divide by the largest coefficient
        nrm = np.maximum(np.maximum(np.abs(ci), np.abs(cj)), np.abs(ck))
        A = np.zeros((len(self.T), n + 1))
        A[self.rows, I] = -s * ci / nrm; A[self.rows, J] = -s * cj / nrm; A[self.rows, K] = -s * ck / nrm
        A[:, n] = 1.0                                   # -s*f/nrm + t <= 0
        c = np.zeros(n + 1); c[n] = -1.0
        bounds = [(0, 0)] + [(-1, 1)] * (n - 2) + [(0, 0)] + [(None, 1.0)]
        res = linprog(c, A_ub=A, b_ub=np.zeros(len(self.T)), bounds=bounds, method='highs-ds')
        if res.status != 0: return -1.0, None
        return float(res.x[n]), res.x[:n]
    def search(self, rng, steps, T0=0.02):
        n = self.n
        g = np.array([math.exp(rng.uniform(-1.0, 1.0)) for _ in range(n - 1)])
        def xs(g): return np.concatenate([[0.0], np.cumsum(g)]) / g.sum()
        cur, y = self.margin(xs(g)); best = (cur, xs(g), y)
        for it in range(steps):
            if best[0] > 1e-7: break
            g2 = g.copy(); k = rng.randrange(n - 1)
            if rng.random() < 0.8: g2[k] *= math.exp(rng.gauss(0, 0.6))
            else:
                k2 = rng.randrange(n - 1); g2[k] *= math.exp(rng.gauss(0, 0.4)); g2[k2] *= math.exp(rng.gauss(0, 0.4))
            g2 = np.clip(g2 / g2.sum(), 1e-6, None)
            v, y2 = self.margin(xs(g2))
            Tm = T0 * (1 - it / steps) + 1e-4
            if v >= cur or rng.random() < math.exp((v - cur) / Tm):
                g, cur = g2, v
                if cur > best[0]: best = (cur, xs(g), y2)
        return best
    def exact_points(self, x, y):
        """round to integers at increasing scales; return points iff every orientation sign is right (exact)"""
        for sx, sy in ((10**6, 10**9), (10**8, 10**13), (10**10, 10**17), (10**12, 10**21)):
            P = [(int(round(float(x[i]) * sx)), int(round(float(y[i]) * sy))) for i in range(self.n)]
            if any(P[i][0] >= P[i + 1][0] for i in range(self.n - 1)): continue
            ok = True
            for q, (i, j, k) in enumerate(self.T):
                d = (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
                if d == 0 or (d > 0) != (self.s[q] > 0): ok = False; break
            if ok: return P
        return None

def realize(n, sig, restarts, steps, seed=0):
    R = LPRealizer(n, sig); rng = random.Random(seed); bestv = -9
    for r in range(restarts):
        v, x, y = R.search(rng, steps)
        bestv = max(bestv, v)
        if v > 1e-7:
            P = R.exact_points(x, y)
            if P: return P, v
    return None, bestv

if __name__ == '__main__':
    fn, restarts, steps, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    only_unc = len(sys.argv) > 5 and sys.argv[5] == '1'; mx = int(sys.argv[6]) if len(sys.argv) > 6 else 10**9
    recs = [json.loads(l) for l in open(fn)] if fn.endswith('.jsonl') else [json.load(open(fn))]
    tot = got = 0; t0 = time.time()
    for k, d in enumerate(recs):
        if only_unc and d.get('nonrealizable_certificate') is not None: continue
        if tot >= mx: break
        n = d.get('n') or d.get('m'); tot += 1
        P, v = realize(n, d['sig'], restarts, steps, seed=1000 + k)
        if P:
            got += 1
            with open(out, 'a') as f: f.write(json.dumps({'record': d.get('record', k), 'n': n, 'sig': d['sig'], 'P': P}) + '\n')
        print(f'record {d.get("record", k)}: {"REALIZED (exact check passed)" if P else "not realized, best margin %.2e" % v}  [{time.time()-t0:.0f}s]', flush=True)
    print(f'{got} of {tot} realized', flush=True)
