"""Try to realize an abstract signotope by integer points: alternating LPs (y for fixed x, x for fixed y)
maximizing the minimum signed determinant.  A candidate is accepted only after EXACT integer verification."""
import sys, json, itertools, random
import numpy as np
from scipy.optimize import linprog
def realize(n, sig, rounds=40, seed=0, M=1000.0):
    rng = random.Random(seed)
    T = list(itertools.combinations(range(n), 3)); s = np.array([1.0 if c == '+' else -1.0 for c in sig])
    x = np.cumsum([rng.uniform(0.5, 1.5) for _ in range(n)]); x = (x - x.mean()) / (x.max() - x.min()) * 2 * M * 0.9
    y = np.array([rng.uniform(-M, M) for _ in range(n)])
    I = np.array([t[0] for t in T]); J = np.array([t[1] for t in T]); K = np.array([t[2] for t in T])
    best = None
    for rd in range(rounds):
        for var in ('y', 'x'):
            # det = (xj-xi)(yk-yi) - (yj-yi)(xk-xi)
            A = np.zeros((len(T), n + 1)); r = np.arange(len(T))
            if var == 'y':
                # coefficients of y_i, y_j, y_k
                np.add.at(A, (r, I), -(x[J] - x[I]) + (x[K] - x[I])); np.add.at(A, (r, J), -(x[K] - x[I])); np.add.at(A, (r, K), (x[J] - x[I]))
                extraA = []; extrab = []
            else:
                # det as a function of x: (xj-xi)(yk-yi) - (yj-yi)(xk-xi)
                np.add.at(A, (r, I), -(y[K] - y[I]) + (y[J] - y[I])); np.add.at(A, (r, J), (y[K] - y[I])); np.add.at(A, (r, K), -(y[J] - y[I]))
            # s*det >= t * scale  ->  -s*A z + t <= 0
            Aub = -(s[:, None] * A); Aub[:, n] = 1.0
            bub = np.zeros(len(T))
            if var == 'x':
                # keep x increasing: x_i - x_{i+1} + 1e-3 <= 0
                B = np.zeros((n - 1, n + 1))
                for i in range(n - 1): B[i, i] = 1; B[i, i + 1] = -1
                Aub = np.vstack([Aub, B]); bub = np.concatenate([bub, -1e-3 * np.ones(n - 1)])
            c = np.zeros(n + 1); c[n] = -1.0
            res = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(-M, M)] * n + [(None, 1e6)], method='highs')
            if res.status != 0: continue
            z = res.x[:n]
            if var == 'y': y = z
            else: x = z
            t = res.x[n]
        if t > 1e-9:
            # scale to integers and verify exactly
            for scale in (10**6, 10**9, 10**12):
                P = [(int(round(x[i] * scale)), int(round(y[i] * scale))) for i in range(n)]
                if len({p[0] for p in P}) < n or any(P[i][0] >= P[i + 1][0] for i in range(n - 1)): continue
                ok = True
                for q, (i, j, k) in enumerate(T):
                    d = (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
                    if d == 0 or (d > 0) != (s[q] > 0): ok = False; break
                if ok: return P, rd
        best = t
    return None, best
if __name__ == '__main__':
    d = json.load(open(sys.argv[1])); n, sig = d['n'], d['sig']
    for seed in range(int(sys.argv[2]) if len(sys.argv) > 2 else 3):
        P, info = realize(n, sig, seed=seed)
        print('seed', seed, 'realized' if P else 'failed', info, flush=True)
        if P:
            json.dump(P, open(sys.argv[1].replace('.json', '_points.json'), 'w')); break
