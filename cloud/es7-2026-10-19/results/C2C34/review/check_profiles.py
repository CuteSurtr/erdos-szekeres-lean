#!/usr/bin/env python3
"""For every admissible profile of t=17: build real nested 34-point sets with that profile (plain and near-degenerate),
label in the normal form for EVERY choice of (0,0), and check that every unit zlayers emits (strict mode, as in
lane.sh) is true for the real chirotope; also compare with lay/units files already produced by the lane."""
import sys, os, json, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import advlib, zlayers
L = os.environ.get('C2C_LAY', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lay'))
info = json.load(open(f'{L}/r2_t17k7_nosb.json'))
tv = {(a, b, c): (v, s) for a, b, c, v, s in info['triples']}
t, Z = info['t'], info['Z']
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)

class Mini:  # just what my_units_from_geometry needs
    pass
M = Mini(); M.t, M.Z, M.tv = t, Z, tv

def truthT(X):
    val = {}
    for a, b, c, v, s in info['triples']:
        r = advlib.sgn(advlib.cross(X[a], X[b], X[c]))
        assert r != 0
        x = s * r
        assert val.setdefault(v, x) == x, "identity violated"
    return val

stats = dict(profiles=0, labelings=0, false=0, geom_mismatch=0, file_mismatch=0, files_checked=0)
t0 = time.time()
for prof in zlayers.profiles(t):
    stats['profiles'] += 1
    u_strict = zlayers.layer_units(tv, Z, t, prof)       # exactly what lane.sh writes
    fn = f"{L}/units/L{'_'.join(map(str, prof))}.txt"
    if os.path.exists(fn):
        stats['files_checked'] += 1
        if open(fn).read() != "".join(f"{l} 0\n" for l in u_strict):
            stats['file_mismatch'] += 1; print("units file differs", prof)
    for near in (False, True):
        P = advlib.gen_nested(prof, rng, near=near)
        assert P is not None, prof
        Ls = advlib.layers_of(P)
        for p00 in Ls[0]:
            pr, X, L2, order = advlib.normal_form(P, p00)
            assert pr == prof
            assert not advlib.check_ccw_claim(L2, order)
            val = truthT(X)
            false = [l for l in u_strict if val[abs(l)] * (1 if l > 0 else -1) < 0]
            stats['labelings'] += 1
            if false:
                stats['false'] += 1; print("FALSE units", prof, near, false[:5])
            if set(u_strict) != advlib.my_units_from_geometry(M, X, L2):
                stats['geom_mismatch'] += 1; print("geom mismatch", prof)
print(stats, f"{time.time()-t0:.0f}s")
