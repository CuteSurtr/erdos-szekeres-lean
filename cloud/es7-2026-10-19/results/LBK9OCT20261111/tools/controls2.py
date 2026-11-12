#!/usr/bin/env python3
"""Positive controls (exact computation): real 8-fold configurations derived from exact sets -- the set itself, its
mirror image (complex conjugation), and subsets of its layers (any subset of the octagons of a real configuration is
again a real configuration of nested regular octagons in general position) -- must satisfy every clause without chain
variables: gen.py's order/angle/nest families, chord, cone, threshold-order (thr2), cell rules B = 2 (cone and
threshold) and bin-order clauses, for the matching number of layers t'.  All values are exact (label8.py: Z[sqrt2];
bins by angle doubling as in check_cells.py).
usage: controls2.py FAMDIR_PATTERN SET.pts [SET.pts ...]
  FAMDIR_PATTERN: e.g. 'cnf/fam/t{t}' (for t = 16 the files of cnf/ are used via cnf/fam/t16 symlinks)
Each set is tested as itself, mirrored, all drop-one-layer subsets, the outermost and innermost k layers and 6 random
k-subsets (seeded) for k in SIZES (env, default 10,12,14,15; k < number of layers), each also mirrored.  Prints one line per configuration and a total."""
import sys, os, json, random, functools, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import label8 as L8
s_ = importlib.util.spec_from_file_location('gen', os.path.join(HERE, 'gen.py'))
G = importlib.util.module_from_spec(s_); s_.loader.exec_module(G)

SIZES = [int(x) for x in os.environ.get('SIZES', '10,12,14,15').split(',')]   # subset sizes with families
FAMS = ['chord.clauses', 'cone.clauses', 'thr2.clauses', 'cellB2.clauses', 'cellthrB2.clauses', 'binorderB2.clauses']
_cache = {}


def families(pattern, t):
    if t in _cache:
        return _cache[t]
    d = pattern.format(t=t)
    fam = {}
    for f in FAMS:
        fam[f] = [[int(x) for x in line.split()[:-1]] for line in open(os.path.join(d, f)) if line.strip()]
    nv0 = int(open(os.path.join(d, 'nv0.txt')).read())
    E = G.Enc(8, 9, t)
    E.cls = []; E.ncls = 0; E.body = None
    E.fam_order(); fam['gen_order'] = list(E.cls); E.cls = []
    E.fam_angle(); fam['gen_angle'] = list(E.cls); E.cls = []
    E.fam_nest(); fam['gen_nest'] = list(E.cls); E.cls = []
    _cache[t] = (fam, nv0)
    return _cache[t]


def orbits_radial(rows):
    """list of seeds (row 8o) of the orbits, sorted by decreasing radius (exact)"""
    n = len(rows) // 8
    seeds = [tuple(list(rows[8 * o]) + [0] * (8 - len(rows[8 * o]))) for o in range(n)]
    def r2(w):
        X, Y = L8.coords(w)
        return L8.zadd(L8.zmul(X, X), L8.zmul(Y, Y))
    R = [r2(s) for s in seeds]
    order = sorted(range(n), key=functools.cmp_to_key(lambda a, b: L8.zsign(*L8.zsub(R[b], R[a]))))
    return [seeds[o] for o in order]


def rows_from_seeds(seeds, mirror=False):
    rows = []
    for s in seeds:
        w = list(s)
        if mirror:
            w = [w[0]] + [w[8 - j] for j in range(1, 8)]      # conj(zeta^j) = zeta^(8-j)
        for k in range(8):
            rows.append(tuple(w[8 - k:] + w[:8 - k]))       # zeta^k * seed (cyclic shift)
    return rows


def zvals(t, reps, nv0):
    def cmul(a, b):
        return (L8.zsub(L8.zmul(a[0], b[0]), L8.zmul(a[1], b[1])), L8.zadd(L8.zmul(a[0], b[1]), L8.zmul(a[1], b[0])))
    p0 = reps[0]
    conj0 = (p0[0], (-p0[1][0], -p0[1][1]))
    zeta = ((0, 1), (0, 1))
    out = {}
    for i in range(1, t):
        w = cmul(reps[i], conj0); w2 = cmul(w, w)
        d = L8.zsign(*L8.det(w2, zeta)); assert d != 0
        out[nv0 + i] = d > 0
    return out


def check(rows, pattern):
    t, P, ids, reps = L8.label(rows)
    E, val = L8.assignment(t, P, ids, reps)
    fam, nv0 = families(pattern, t)
    val.update(zvals(t, reps, nv0))
    res = {}
    for name, cls in fam.items():
        bad = 0
        for cl in cls:
            if not any(val.get(abs(l)) == (l > 0) for l in cl):
                bad += 1
        res[name] = (len(cls), bad)
    ph = sorted(range(1, t), key=lambda i: sum(1 for j in range(1, t) if j != i and
                                               (val[E.Y[(j, i)]] if j < i else not val[E.Y[(i, j)]])))
    mono = 'incr' if ph == list(range(1, t)) else ('decr' if ph == list(range(t - 1, 0, -1)) else 'other')
    zs = ''.join('1' if val[nv0 + i] else '0' for i in range(1, t))
    return t, res, mono, zs


if __name__ == '__main__':
    pattern = sys.argv[1]
    total_cfg = 0; total_bad = 0; total_cl = 0
    for fn in sys.argv[2:]:
        seeds = orbits_radial(L8.read_pts(fn))
        n = len(seeds)
        rnd = random.Random(20261111)
        subsets = [('all', list(range(n)))]
        subsets += [('drop%d' % k, [i for i in range(n) if i != k]) for k in range(n)]
        sizes = [k for k in SIZES if k < n]
        subsets += [('prefix%d' % k, list(range(k))) for k in sizes]
        subsets += [('suffix%d' % k, list(range(n - k, n))) for k in sizes]
        for q in range(6):
            k = rnd.choice(sizes)
            subsets.append(('rand%d' % q, sorted(rnd.sample(range(n), k))))
        for tag, S in subsets:
            for mir in (False, True):
                rows = rows_from_seeds([seeds[i] for i in S], mirror=mir)
                t, res, mono, zs = check(rows, pattern)
                nb = sum(b for _, b in res.values()); nc = sum(c for c, _ in res.values())
                total_cfg += 1; total_bad += nb; total_cl += nc
                print('%s %-8s %-6s t=%2d order=%-5s Z=%-15s clauses %7d violated %d %s' % (
                    os.path.basename(fn), tag, 'mirror' if mir else '', t, mono, zs, nc, nb,
                    '' if nb == 0 else str({k: v for k, v in res.items() if v[1]})), flush=True)
    print('TOTAL configurations %d, clause evaluations %d, violations %d' % (total_cfg, total_cl, total_bad))
