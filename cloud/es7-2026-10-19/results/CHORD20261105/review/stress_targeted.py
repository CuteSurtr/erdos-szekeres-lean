#!/usr/bin/env python3
"""Targeted adversarial configurations per chord clause (mpmath, 80 digits).

For every clause whose triple uses layers {i (one point), j (two points)} and every delta = theta_i - theta_j scenario
in which the clause's Y literal is false (the clause then asserts the orientation literal), build configurations with
  * delta within eps of either end of the scenario interval (eps in {1e-9, 1e-12}),
  * the radius ratio between the two layers either tight (every layer from min(i,j) to max(i,j) at 1 - 1e-12 of its
    maximal nesting ratio cos30/cos(d)) or tiny (1e-12 per step), other layers random,
and evaluate the clause exactly as in stress.py (untrusted orientations counted, never reported as violations).
One-layer clauses are evaluated on random configurations.  usage: stress_targeted.py OUTLOG"""
import sys, json, random
import mpmath as mp
import stress
from indep_enc import TRIPLE_OF, YINV, NTRIP

mp.mp.dps = 80
rng = random.Random(4242)


def radii(th, tight_lo, tight_hi, mode):
    rs = [mp.mpf(1)]
    for a in range(9):
        x = (th[a + 1] - th[a] - 30) % 60
        d = min(x, 60 - x)
        mx = mp.cos(mp.radians(30)) / mp.cos(mp.radians(d))
        if tight_lo <= a < tight_hi:
            f = (1 - mp.mpf(10) ** -12) if mode == 'tight' else mp.mpf(10) ** -12
        else:
            f = mp.mpf(rng.uniform(0.05, 0.99))
        rs.append(rs[-1] * mx * f)
    return rs


def phases(i, j, end, lo, hi, eps):
    th = [mp.mpf(0)] + [mp.mpf(rng.uniform(1, 59)) for _ in range(9)]
    target = (lo + eps) if end == 'lo' else (hi - eps)          # target delta = theta_i - theta_j
    if j == 0:
        th[i] = target
    elif i == 0:
        th[j] = -target
    else:
        # choose theta_j so that theta_i = theta_j + target lies in (0,60) with both strictly inside
        if target > 0:
            th[j] = mp.mpf(rng.uniform(0, 1)) * (60 - target)
            if th[j] <= 0: th[j] = (60 - target) / 2
        else:
            th[j] = -target + mp.mpf(rng.uniform(0, 1)) * (60 + target)
            if th[j] >= 60: th[j] = (60 - target) / 2
        th[i] = th[j] + target
    # make the remaining phases distinct from these
    return th


cls = stress.CHORD
nconf = viol = und = 0
out = open(sys.argv[1], 'w')
for cl in cls:
    L = [x for x in cl if abs(x) <= NTRIP][0]
    t = TRIPLE_OF[abs(L)]
    ls = [x // 6 for x in t]
    if len(set(ls)) == 1:
        for _ in range(8):
            rs, th = stress.gen(rng, rng.choice(['uniform', 'multiscale', 'phase_edge', 'phase_cluster', 'mixed']))
            v, u = stress.evaluate(rs, th, [cl]); nconf += 1; viol += len(v); und += u
        continue
    j = max(set(ls), key=ls.count); i = min(set(ls), key=ls.count)
    if j == 0:
        scen = [(0, 60, None)]
    elif i == 0:
        scen = [(-60, 0, None)]
    else:
        scen = [(-60, 0, 'i<j'), (0, 60, 'i>j')]
    for lo, hi, rel in scen:
        for end in ('lo', 'hi'):
            for eps in (mp.mpf(10) ** -9, mp.mpf(10) ** -12):
                for rmode in ('tight', 'tiny'):
                    th = phases(i, j, end, lo, hi, eps)
                    if not all(0 < th[a] < 60 for a in range(1, 10)) or len(set(th)) < 10:
                        continue
                    a, b = min(i, j), max(i, j)
                    rs = radii(th, a, b, rmode)
                    v, u = stress.evaluate(rs, th, [cl]); nconf += 1; und += u
                    if v:
                        viol += 1
                        out.write(json.dumps({'clause': cl, 'r': [mp.nstr(x, 30) for x in rs],
                                              'theta': [mp.nstr(x, 30) for x in th]}) + '\n')
res = {'clauses': len(cls), 'configs': nconf, 'violations': viol, 'undetermined': und}
out.write(json.dumps(res) + '\n'); out.close()
print(json.dumps(res))
