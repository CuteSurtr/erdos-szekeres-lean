#!/usr/bin/env python3
"""Remove-and-reinsert scan (float evaluator; evidence only until exact checks).
For a configuration (m, lr, th, centre) and each choice of orbits to delete (one orbit, each in turn, or a given
list), re-insert the same number of new orbits one at a time on a 2D grid of (log radius, phase), keeping the BEAM
best partial configurations, then refine the best grid points by a local pattern search.  Configurations with N8 = 0
are written to OUT/found_*.json.
usage: reinsert.py --m 3 --init CFG.json --out DIR --tag T [--delete 7 | --delete-each 0..k] [--nr 300 --nth 360]"""
import sys, os, json, math, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evm import countm
from ptsio import read_cfg, write_cfg


def n8(m, lr, th, c, abort=0):
    cnt, r = countm(m, lr, th, c, abort)
    return (cnt[8] if r == 0 else 10 ** 9), cnt[7]


def grid_insert(m, lr, th, c, LR, TH, beam):
    res = []
    best = 10 ** 9
    for a in LR:
        for b in TH:
            lr2 = np.append(lr, a); th2 = np.append(th, b)
            k8, k7 = n8(m, lr2, th2, c, abort=max(best * 4, 50))
            res.append((k8, k7, a, b))
            if k8 < best:
                best = k8
    res.sort(key=lambda x: (x[0], x[1]))
    return res[:beam]


def refine(m, lr, th, c, rng, iters=3000):
    """pattern search on the last orbit (the inserted one) and small moves of all orbits, energy N8 then N7"""
    k8, k7 = n8(m, lr, th, c)
    cur = (k8, k7, lr.copy(), th.copy())
    for it in range(iters):
        if cur[0] == 0:
            break
        lr2, th2 = cur[2].copy(), cur[3].copy()
        i = len(lr2) - 1 if rng.random() < 0.5 else int(rng.integers(len(lr2)))
        s = 10 ** rng.uniform(-6, -1)
        if rng.random() < 0.5:
            lr2[i] += rng.normal(0, s)
        else:
            th2[i] += rng.normal(0, s)
        a8, a7 = n8(m, lr2, th2, c, abort=cur[0] + 1)
        if (a8, a7) < (cur[0], cur[1]):
            cur = (a8, a7, lr2, th2)
    return cur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--init', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--tag', default='ri')
    ap.add_argument('--delete', default='', help='comma list of orbits (radial order) deleted together')
    ap.add_argument('--delete-each', default='', help='LO:HI: delete each single orbit in this range in turn')
    ap.add_argument('--add', type=int, default=0, help='insert this many orbits in addition to the deleted ones')
    ap.add_argument('--centre', type=int, default=-1, help='override the centre flag of the input')
    ap.add_argument('--nr', type=int, default=240)
    ap.add_argument('--nth', type=int, default=240)
    ap.add_argument('--beam', type=int, default=6)
    ap.add_argument('--lrmin', type=float, default=-16)
    ap.add_argument('--stop-at', type=float, default=0)
    ap.add_argument('--seed', type=int, default=0)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    logf = open(os.path.join(a.out, 'log_%s.txt' % a.tag), 'a')

    def log(*x):
        logf.write(time.strftime('%H:%M:%S ') + ' '.join(str(v) for v in x) + '\n'); logf.flush()
    rng = np.random.default_rng(a.seed)
    _, lr0, th0, c = read_cfg(a.init)
    m = a.m; U = 2 * math.pi / m
    o = np.argsort(-lr0); lr0 = lr0[o] - lr0[o][0]; th0 = th0[o]
    t = len(lr0)
    jobs = []
    if a.centre >= 0:
        c = a.centre
    if a.delete:
        jobs.append([int(x) for x in a.delete.split(',')])
    if a.add and not jobs:
        jobs.append([])
    if a.delete_each:
        lo, hi = map(int, a.delete_each.split(':'))
        jobs += [[i] for i in range(lo, hi + 1)]
    LR = np.linspace(a.lrmin, 0.7, a.nr)
    TH = (np.arange(a.nth) + 0.5) / a.nth * U
    nf = 0
    for D in jobs:
        if a.stop_at and time.time() > a.stop_at:
            break
        keep = [i for i in range(t) if i not in D]
        lr, th = lr0[keep], th0[keep]
        b8, b7 = n8(m, lr, th, c)
        log('delete', D, '-> remaining N8', b8, 'N7', b7)
        beams = [(b8, b7, lr, th)]
        for step in range(len(D) + a.add):
            nb = []
            for (_, _, l1, t1) in beams:
                for k8, k7, x, y in grid_insert(m, l1, t1, c, LR, TH, a.beam):
                    nb.append((k8, k7, np.append(l1, x), np.append(t1, y)))
            nb.sort(key=lambda z: (z[0], z[1]))
            beams = nb[:a.beam]
            log('  step', step, 'grid best N8', [z[0] for z in beams])
        for k, (k8, k7, l1, t1) in enumerate(beams):
            r = refine(m, l1, t1, c, rng)
            log('  beam', k, 'grid N8', k8, '-> refined N8', r[0], 'N7', r[1])
            cnt, _ = countm(m, r[2], r[3], c)
            write_cfg(os.path.join(a.out, 'beam_%s_del%s_%d.json' % (a.tag, '_'.join(map(str, D)), k)), m, r[2], r[3], c, cnt,
                      note='reinsert beam result, deleted %s' % D)
            if r[0] == 0:
                nf += 1
                fn = os.path.join(a.out, 'found_%s_%d.json' % (a.tag, nf))
                cnt, _ = countm(m, r[2], r[3], c)
                write_cfg(fn, m, r[2], r[3], c, cnt, note='reinsert, deleted %s' % D)
                log('N8 = 0 FOUND', fn)
    log('done')


if __name__ == '__main__':
    main()
