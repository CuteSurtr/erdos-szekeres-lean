#!/usr/bin/env python3
"""Sequential LP with free phases (evidence only; any configuration found is checked by the float evaluator and then
by the exact pipeline).  Input: a 'bestmodel' JSON of pfenc (orbit-variable signs s_v of a SAT model of the
phase-fixed formula, the phases th and the radii of its LP point).  The model's signs are octagon-free for the fixed
radius ORDER (chain clauses); here the phases may move too.  Each step linearises the forms
   f_v(u, th) = u_p sin(a_s - a_q) + u_q sin(a_p - a_s) + u_s sin(a_q - a_p),   a = th_layer + 2 pi k/m,
in th around the current point (exactly linear in u) and solves
   max delta  s.t.  s_v (A_v(th0) u + g_v(u0, th0) . dth) / |A_v(th0)| >= delta,  u ordered, u_0 = 1,
                    |dth_i| <= rho, dth_0 = 0;
then re-solves the exact fixed-phase LP at th0 + dth; rho shrinks when the true margin does not improve.
usage: slp.py BESTMODEL.json OUTDIR TAG [iters] [rho0]"""
import sys, os, json, math, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, hstack, vstack
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'py'))
import pfenc
from evm import countm
from ptsio import write_cfg

src, out, tag = sys.argv[1], sys.argv[2], sys.argv[3]
iters = int(sys.argv[4]) if len(sys.argv) > 4 else 60
rho = float(sys.argv[5]) if len(sys.argv) > 5 else 2e-3
os.makedirs(out, exist_ok=True)
d = json.load(open(src))
m, centre = d['m'], int(d['centre'])
th = np.array(d['th'], float); t = len(th)
s = np.array(d['signs'], float)
P = pfenc.PF(m, t, centre, th)
C = np.array([P.Cof[v] for v in range(1, P.ntv + 1)])
L = C // m; K = C % m


def forms(th):
    a = th[L] + 2 * math.pi * K / m
    A = np.zeros((len(C), t)); G = None
    s1 = np.sin(a[:, 2] - a[:, 1]); s2 = np.sin(a[:, 0] - a[:, 2]); s3 = np.sin(a[:, 1] - a[:, 0])
    np.add.at(A, (np.arange(len(C)), L[:, 0]), s1)
    np.add.at(A, (np.arange(len(C)), L[:, 1]), s2)
    np.add.at(A, (np.arange(len(C)), L[:, 2]), s3)
    return A, a


def grad_th(a, u):
    """d f / d th_l for each row (u fixed)"""
    u1, u2, u3 = u[L[:, 0]], u[L[:, 1]], u[L[:, 2]]
    c32 = np.cos(a[:, 2] - a[:, 1]); c13 = np.cos(a[:, 0] - a[:, 2]); c21 = np.cos(a[:, 1] - a[:, 0])
    d1 = u2 * c13 - u3 * c21      # d/da1
    d2 = -u1 * c32 + u3 * c21     # d/da2
    d3 = u1 * c32 - u2 * c13      # d/da3
    G = np.zeros((len(C), t))
    np.add.at(G, (np.arange(len(C)), L[:, 0]), d1)
    np.add.at(G, (np.arange(len(C)), L[:, 1]), d2)
    np.add.at(G, (np.arange(len(C)), L[:, 2]), d3)
    return G


def fixed_lp(th):
    A, _ = forms(th)
    Ap = np.vstack([np.zeros(t), A])
    delta, u, _ = pfenc.lp_check(Ap, s, t, np.arange(1, P.ntv + 1))
    return delta, u


def slp_step(th, u0, rho):
    A, a = forms(th)
    G = grad_th(a, u0)
    nrm = np.linalg.norm(A, axis=1)
    R1 = (A * s[:, None]) / nrm[:, None]
    R2 = (G * s[:, None]) / nrm[:, None]
    N = len(C)
    nv = t + t + 1          # u, dth, delta
    cobj = np.zeros(nv); cobj[-1] = -1
    A_ub = np.hstack([-R1, -R2, np.ones((N, 1))])
    ordr = np.zeros((t - 1, nv))
    for i in range(t - 1):
        ordr[i, i] = 1; ordr[i, i + 1] = -1
    A_ub = np.vstack([A_ub, ordr]); b_ub = np.zeros(N + t - 1)
    A_eq = np.zeros((2, nv)); A_eq[0, 0] = 1; A_eq[1, t] = 1
    bounds = [(0, None)] * t + [(-rho, rho)] * t + [(None, 1.0)]
    res = linprog(cobj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0, 0.0], bounds=bounds, method='highs')
    if res.status != 0:
        return None
    return res.x[t:2 * t]


log = open(os.path.join(out, 'slp_%s.log' % tag), 'a')
def LOG(x):
    log.write(time.strftime('%H:%M:%S ') + x + '\n'); log.flush(); print(x, flush=True)
delta, u = fixed_lp(th)
LOG('start %s: fixed-phase margin %.3e' % (src, delta))
best = (delta, th.copy(), u)
for it in range(iters):
    dth = slp_step(best[1], best[2], rho)
    if dth is None:
        LOG('LP failure'); break
    th2 = best[1] + dth
    d2, u2 = fixed_lp(th2)
    if d2 is not None and d2 > best[0]:
        best = (d2, th2, u2)
        rho = min(rho * 1.5, 5e-2)
    else:
        rho *= 0.5
    LOG('it %d rho %.2e margin %.3e (best %.3e)' % (it, rho, d2 if d2 is not None else float('nan'), best[0]))
    if best[0] > 1e-9 and (it % 5 == 0 or best[0] > 1e-6):
        lr = -np.log(best[2] / best[2][0])
        cnt, _ = countm(m, lr, best[1], centre)
        LOG('POSITIVE margin %.3e: float N8 %d N7 %d' % (best[0], cnt[8], cnt[7]))
        if cnt[8] == 0:
            fn = os.path.join(out, 'cand_slp_%s.json' % tag)
            json.dump(dict(m=m, centre=centre, lr=lr.tolist(), th=list(map(float, best[1])), delta=float(best[0]),
                           counts={str(k): int(cnt[k]) for k in range(3, 9)}, note='slp from %s' % src), open(fn, 'w'), indent=1)
            LOG('float N8 = 0 -> %s' % fn)
            break
        if best[0] > 1e-5:
            break
    if rho < 1e-9:
        break
