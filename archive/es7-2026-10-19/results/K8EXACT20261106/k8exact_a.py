#!/usr/bin/env python3
"""Exact check of the 7-fold 64-point octagon-free sets against encoder A's 9-layer formula (C7UPPER/gen.py 7 8 9).

usage: python3 -I -B k8exact_a.py [--dump DIR] CNF SET.pts [SET.pts ...]     (gen.py's meta file CNF.json next to CNF)
Writes one JSON object per line to stdout; exit status 1 if any clause is violated or H(1) does not flip.
Python standard library only.  With --dump, the full assignment of each case is written to
DIR/A.<set>.<case>.assign for satcheck.py.

Geometry (exact computation): the sign routines, the normalisation and the orientation table are those of k8exact.py
(loaded from this directory, not copied): coordinates in Z[zeta_7], every sign the certified sign of an integer
polynomial of degree <= 2 at c = 2 cos(2 pi/7).  Same conventions as encoder A's docstring: layer 0 outermost,
id = 7 i + k, point (i, k) has angle theta_i + 2 pi k/7 with theta_0 = 0 and theta_i in [0, 2 pi/7),
psi_i = theta_i mod pi/7, Y(i, j) = [psi_i < psi_j] (i < j), H(i) = [theta_i < pi/7].

Encoder A's variable map.
  * Orbit variables: V(C) = [orient(C) = +] for the canonical triple C of each rotation orbit, C = the
    lexicographically least sorted rotation of the triple, numbered 1, 2, ... in order of first appearance over
    itertools.combinations(range(63), 3).  This map is derived here from that definition and then compared with the
    generator's own table (C7UPPER/gen.py, class Enc, constructor only; nothing is written).
  * Y and H: from gen.py's meta file (CNF.json), compared with Enc.Y and Enc.H.
  * Chain variables: everything above the 5,673 + 28 + 8 = 5,709 geometric variables.  They get their least model
    under the fixed geometric assignment (the chain clauses are Horn in them; k8exact.least_chain_model), and every
    clause is then evaluated (k8exact.evaluate).  A violation would mean no extension exists.
  * Families from the meta file's clause ranges: order (Y-transitivity), angle, nest, chain; the split is checked
    against the clause contents.
Certificate link.  The 10-layer certificate formula is A(7,8,10) plus the unit clause H(1) (C7UPPER/addunits.py,
literal 7857; regen_hashes_a.sh checks that 7857 is H(1) there).  At 9 layers H(1) is variable meta['H']['1'];
the check records, for each set, which of the set and its mirror satisfies A(7,8,9) together with the unit H(1).
"""
import collections
import hashlib
import importlib.util
import itertools
import json
import math
import random
import resource
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent
START = time.monotonic()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


K = load('k8exact', HERE / 'k8exact.py')
M, T = 7, 9
FAM_NAMES = {'order': 'transitivity', 'angle': 'angular', 'nest': 'nesting', 'chain': 'chain'}


def orbit_map():
    """canonical triple -> variable, from the definition in gen.py's docstring (independent of gen.Enc)"""
    rot = lambda x, s: (x // M) * M + (x % M + s) % M
    tvar, size = {}, collections.Counter()
    for tri in itertools.combinations(range(M * T), 3):
        C = min(tuple(sorted(rot(x, s) for x in tri)) for s in range(M))
        if C not in tvar:
            tvar[C] = len(tvar) + 1
        size[C] += 1
    assert set(size.values()) == {M}                          # every orbit has exactly 7 triples
    return tvar


def variable_map(meta):
    tvar = orbit_map()
    G = load('c7upper_gen', RESULTS / 'C7UPPER/gen.py')
    E = G.Enc(M, 8, T)
    assert E.tvar == tvar, 'orbit-variable numbering differs from gen.Enc'
    Y = {tuple(map(int, k.split(','))): v for k, v in meta['Y'].items()}
    H = {int(k): v for k, v in meta['H'].items()}
    assert Y == E.Y and H == E.H
    n3 = len(tvar)
    assert n3 == math.comb(M * T, 3) // M == meta['ntriple'] == 5673
    assert sorted(Y) == list(itertools.combinations(range(1, T), 2)) and sorted(Y.values()) == list(range(n3 + 1, n3 + 29))
    assert sorted(H) == list(range(1, T)) and sorted(H.values()) == list(range(n3 + 29, n3 + 37))
    return tvar, Y, H, n3 + 36


def families(meta, cls, maxgeo):
    rg = meta['ranges']
    assert list(rg) == ['order', 'angle', 'nest', 'chain']
    pos = 0
    fam = []
    for name, (a, b) in rg.items():
        assert a == pos and b >= a
        fam += [FAM_NAMES[name]] * (b - a)
        pos = b
    assert pos == len(cls) == meta['ncl']
    cnt = collections.Counter(fam)
    assert cnt['transitivity'] == 2 * math.comb(T - 1, 3)
    assert cnt['angular'] == meta['angle']['unit'] + meta['angle']['cond']
    assert cnt['nesting'] == math.comb(T, 2) * M
    ny = 5673 + 28
    for cl, f in zip(cls, fam):
        vs = [abs(l) for l in cl]
        if f == 'chain':
            assert any(v > maxgeo for v in vs)
        else:
            assert all(v <= maxgeo for v in vs)
        if f == 'transitivity':
            assert len(cl) == 3 and all(5673 < v <= ny for v in vs)
        if f == 'nesting':
            assert len(cl) == 1 and vs[0] <= 5673
    nunit = sum(1 for cl, f in zip(cls, fam) if f == 'angular' and len(cl) == 1)
    return fam, nunit


def main():
    args = sys.argv[1:]
    dump = None
    if args[0] == '--dump':
        dump = Path(args[1]); args = args[2:]
        dump.mkdir(parents=True, exist_ok=True)
    cnf, sets = args[0], args[1:]
    print(json.dumps({'rigor': 'exact computation', 'encoder': 'A (C7UPPER/gen.py)',
                      'identities_checked': K.identities(),
                      'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'k8exact_sha256': hashlib.sha256((HERE / 'k8exact.py').read_bytes()).hexdigest(),
                      'gen_py_sha256': hashlib.sha256((RESULTS / 'C7UPPER/gen.py').read_bytes()).hexdigest(),
                      'python': sys.version.split()[0]}), flush=True)
    sha, nv, cls = K.read_cnf(cnf)
    meta = json.loads(Path(cnf + '.json').read_text())
    assert (meta['m'], meta['K'], meta['t'], meta['nv'], meta['ncl']) == (M, 8, T, nv, len(cls))
    tvar, Yv, Hv, maxgeo = variable_map(meta)
    fam, nunit = families(meta, cls, maxgeo)
    assert nunit == meta['angle']['unit']
    print(json.dumps({'cnf': Path(cnf).name, 'sha256': sha, 'variables': nv, 'clauses': len(cls),
                      'families': dict(collections.Counter(fam)), 'angular_units': nunit,
                      'orbit_vars': len(tvar), 'orbit_map_matches_gen_Enc': True, 'H1_var': Hv[1],
                      'geometric_vars': maxgeo}), flush=True)
    total_viol = 0; flips_ok = True; unit_ok = True
    for path in sets:
        raw, rows = K.read_set(path)
        name = Path(path).stem
        res = {}
        for mirror in (False, True):
            K.STATS.clear()
            t0 = time.monotonic()
            cfg = K.configuration(rows, mirror)
            p0_invariant = all((c['H'], c['Y']) == (cfg['H'], cfg['Y'])
                               for c in (K.configuration(rows, mirror, k) for k in range(1, 7)))
            sg, sc = K.orientations(cfg['P'])
            rot_bad = K.rotation_check(sg)
            nz, zbad = K.z7exact_check(cfg, sg, sc)
            assert rot_bad == 0 and p0_invariant and zbad == 0
            val = [None] * (nv + 1)
            for C, v in tvar.items():
                val[v] = sg[C] > 0                      # C is sorted, so sg[C] = orient(C)
            for (i, j), v in Yv.items():
                val[v] = cfg['Y'][(i, j)]
            for i, v in Hv.items():
                val[v] = cfg['H'][i]
            assert all(x is not None for x in val[1:maxgeo + 1]) and all(x is None for x in val[maxgeo + 1:])
            viol, ntrue, full = K.evaluate(cls, fam, val)
            nviol = sum(viol.values()); total_viol += nviol
            out = {'set': name, 'sha256': hashlib.sha256(raw).hexdigest(), 'case': 'mirror' if mirror else 'original',
                   'triples_nonzero': len(sg) + len(sc), 'rotation_invariance_failures': rot_bad,
                   'phase_independent_of_p0': p0_invariant, 'z7exact_agreement': '%d/%d' % (nz - zbad, nz),
                   'H': ''.join('1' if cfg['H'][i] else '0' for i in range(1, 9)), 'H1': cfg['H'][1],
                   'psi_order': cfg['order'], 'clauses': len(cls), 'violations': viol, 'violations_total': nviol,
                   'chain_vars_true': ntrue,
                   'satisfies_A9_plus_unit_H1': nviol == 0 and full[Hv[1]],
                   'sign_stats': dict(K.STATS), 'seconds': round(time.monotonic() - t0, 2)}
            if not mirror:
                mut = {}
                unit = next(cl[0] for cl, f in zip(cls, fam) if f == 'angular' and len(cl) == 1)
                ctl = [('flip_first_angular_unit_var', abs(unit)), ('flip_H1', Hv[1]), ('flip_H8', Hv[8]),
                       ('flip_Y12', Yv[(1, 2)])]
                ctl += [('flip_orbit_var_%d' % v, v)
                        for v in random.Random(20261106).sample(sorted(tvar.values()), 5)]
                for label, var in ctl:
                    v2 = list(val); v2[var] = not v2[var]
                    mv, _, _ = K.evaluate(cls, fam, v2)
                    mut[label] = sum(mv.values())
                out['negative_controls_violations'] = mut
                assert mut['flip_first_angular_unit_var'] > 0, mut
            if dump:
                text = ' '.join(str(v if full[v] else -v) for v in range(1, len(full))) + ' 0\n'
                fn = dump / ('A.%s.%s.assign' % (name, out['case']))
                fn.write_text(text)
                out['assignment_sha256'] = hashlib.sha256(text.encode()).hexdigest()
            res[mirror] = (cfg, out)
            print(json.dumps(out), flush=True)
        (o, oo), (mr, mo) = res[False], res[True]
        flip = {'set': name, 'H1_original': o['H'][1], 'H1_mirror': mr['H'][1],
                'H1_flips': o['H'][1] != mr['H'][1],
                'all_H_flip': all(o['H'][i] != mr['H'][i] for i in range(1, 9)),
                'all_Y_reverse': all(o['Y'][k] != mr['Y'][k] for k in o['Y']),
                'case_satisfying_A9_plus_unit_H1': [c['case'] for c in (oo, mo) if c['satisfies_A9_plus_unit_H1']]}
        flips_ok &= flip['H1_flips']
        unit_ok &= len(flip['case_satisfying_A9_plus_unit_H1']) == 1
        print(json.dumps(flip), flush=True)
    status = 'PASS' if total_viol == 0 and flips_ok and unit_ok else 'FAIL'
    print(json.dumps({'status': status, 'encoder': 'A', 'sets': len(sets), 'cases': 2 * len(sets),
                      'violations_total': total_viol, 'H1_flips_in_all': flips_ok,
                      'exactly_one_case_per_set_satisfies_A9_plus_unit_H1': unit_ok,
                      'elapsed_seconds': round(time.monotonic() - START, 1),
                      'max_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024}), flush=True)
    sys.exit(0 if status == 'PASS' else 1)


if __name__ == '__main__':
    main()
