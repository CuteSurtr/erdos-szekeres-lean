"""Try to realize an abstract signotope (sign string over triples, '+' = cup = counter-clockwise) by integer points
with increasing x.  Gradient descent on a hinge loss, random restarts; exact integer verification at the end.
usage: realize.py m signstring [restarts]   -> prints JSON {"realized": bool, "P": [[x,y],...]}"""
import sys, json, itertools, random
import numpy as np
comb = itertools.combinations
def realize(m, s, restarts=200, seed=1, iters=4000):
    tr = np.array(list(comb(range(m), 3))); sg = np.array([1.0 if c == '+' else -1.0 for c in s])
    rng = np.random.default_rng(seed)
    for r in range(restarts):
        dx = np.abs(rng.normal(1, 0.5, m)) + 0.2; y = rng.normal(0, 3, m)
        lr = 0.02
        for it in range(iters):
            x = np.cumsum(dx)
            ax, ay = x[tr[:, 0]], y[tr[:, 0]]; bx, by = x[tr[:, 1]], y[tr[:, 1]]; cx, cy = x[tr[:, 2]], y[tr[:, 2]]
            det = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
            scale = (cx - ax) * np.sqrt((cx - ax) ** 2 + (cy - ay) ** 2) + 1e-9
            viol = 0.05 - sg * det / scale          # normalised margin
            act = viol > 0
            if not act.any(): break
            # gradient of sum(viol[act]) wrt x,y (treat scale as constant)
            w = np.where(act, -sg / scale, 0.0)
            gx = np.zeros(m); gy = np.zeros(m)
            np.add.at(gx, tr[:, 0], w * (-(cy - ay) + (by - ay))); np.add.at(gx, tr[:, 1], w * (cy - ay)); np.add.at(gx, tr[:, 2], w * (-(by - ay)))
            np.add.at(gy, tr[:, 0], w * (-(bx - ax) + (cx - ax))); np.add.at(gy, tr[:, 1], w * (-(cx - ax))); np.add.at(gy, tr[:, 2], w * (bx - ax))
            gdx = np.cumsum(gx[::-1])[::-1]
            dx = np.maximum(dx - lr * gdx, 0.05); y = y - lr * gy
        x = np.cumsum(dx)
        for sc in (10**4, 10**6):
            P = [(int(round(x[i] * sc)), int(round(y[i] * sc))) for i in range(m)]
            if len({p[0] for p in P}) < m: continue
            ok = True
            for (i, j, k), c in zip(comb(range(m), 3), s):
                d = (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
                if d == 0 or (d > 0) != (c == '+'): ok = False; break
            if ok and all(P[i][0] < P[i + 1][0] for i in range(m - 1)): return P
    return None
if __name__ == '__main__':
    m = int(sys.argv[1]); s = sys.argv[2]; R = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    P = realize(m, s, R)
    print(json.dumps({'realized': P is not None, 'P': P}))
