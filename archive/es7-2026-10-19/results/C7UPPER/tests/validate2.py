#!/usr/bin/env python3
"""Streaming soundness test of a CNF written by gen.py against real configurations.

usage: validate2.py CNF (pts FILE.pts [t] | random N seed [extra.cnf])
The real assignment of the triple-orbit variables (orientations from coordinates, float64; min|det| reported)
and of Y/H (from the phases) is extended to the chain variables by one pass in file order (the chain clauses
are written level by level, so one pass computes the least fixpoint).  Reports unsatisfied clauses per family.
Optional extra.cnf: further clauses (e.g. lazily added GP clauses) that must also hold for real configurations.
"""
import sys, json, math, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import gen
from validate import orient_f, layers_to_points, read_pts, random_layers


def real_assign(E, m, layers):
    pts, lay = layers_to_points(m, layers)
    assign = {}
    mind = float('inf')
    for C, v in E.tvar.items():
        d = orient_f(pts[C[0]], pts[C[1]], pts[C[2]])
        mind = min(mind, abs(d))
        assign[v] = d > 0
    unit = math.pi / m if m % 2 else 2 * math.pi / m
    psi = [th % unit for (_, th) in lay]
    for (i, j), v in E.Y.items():
        assign[v] = psi[i] < psi[j]
    for i, v in E.H.items():
        assign[v] = lay[i][1] < math.pi / m
    return assign, mind


def stream_check(cnf, meta, assign, base, extra=None):
    ranges = meta['ranges']
    fam_of = []
    for fam, (a, b) in ranges.items():
        fam_of.append((a, b, fam))
    bad = {f: 0 for f in ranges}
    idx = -1
    def lv(l):
        x = assign.get(abs(l), False)
        return x if l > 0 else not x
    with open(cnf) as f:
        f.readline()
        for line in f:
            idx += 1
            cl = list(map(int, line.split()))[:-1]
            fam = None
            for a, b, fm in fam_of:
                if a <= idx < b:
                    fam = fm
                    break
            if any(lv(l) for l in cl):
                continue
            if fam == 'chain':
                pos = [l for l in cl if l > base]
                if pos:
                    assign[pos[0]] = True
                    continue
            bad[fam] = bad.get(fam, 0) + 1
    bad['_clauses_read'] = idx + 1
    bad['_chainvars_true'] = sum(1 for v, x in assign.items() if v > base and x)
    if extra:
        bad['extra'] = 0
        with open(extra) as f:
            for line in f:
                if line.startswith('p') or line.startswith('c'):
                    continue
                cl = list(map(int, line.split()))[:-1]
                if not any(lv(l) for l in cl):
                    bad['extra'] += 1
    return bad


if __name__ == '__main__':
    cnf = sys.argv[1]
    meta = json.load(open(cnf + '.json'))
    m, K, t = meta['m'], meta['K'], meta['t']
    E = gen.Enc(m, K, t)
    base = E.nv          # triple + Y + H variables; chain variables are above
    mode = sys.argv[2]
    if mode == 'pts':
        layers = read_pts(sys.argv[3], m)
        print('layers in file:', len(layers), 'radii ratios:',
              ' '.join('%.3f' % (layers[i + 1][0] / layers[i][0]) for i in range(len(layers) - 1)))
        layers = layers[:t]
        assign, mind = real_assign(E, m, layers)
        print('pts', sys.argv[3], 'min|det| %.3g' % mind, stream_check(cnf, meta, assign, base,
                                                                       sys.argv[4] if len(sys.argv) > 4 else None))
    else:
        N = int(sys.argv[3]); rng = random.Random(int(sys.argv[4]))
        extra = sys.argv[5] if len(sys.argv) > 5 else None
        tot = {}
        for s in range(N):
            layers = random_layers(m, t, rng, 'needle' if s % 2 else 'free')
            assign, mind = real_assign(E, m, layers)
            if mind < 1e-9:
                continue
            bad = stream_check(cnf, meta, assign, base, extra)
            for k, v in bad.items():
                if v and k != 'chain' and not str(k).startswith('_'):
                    print('VIOLATION', k, v, layers)
                tot[k] = tot.get(k, 0) + (v > 0)
        print('random', N, 'configs with >=1 unsatisfied clause, per family:', tot)
