#!/usr/bin/env python3
"""image_test.py NMODELS : would images of earlier cuts under relabelings have excluded later models?

A cut is valid for all seed vectors z (points p_{6i+k}(z) = R^k z_i), so it stays valid after substituting
z_l -> R^{s_l} z_l (p_x -> p_{sigma x}, sigma shifts the labels of layer l by s_l) or z -> conj z (orientations flip,
labels k -> -k).  For a model M and a cut C, search all sigma in Z6^10 (one layer fixed, since the global shift acts
trivially on the orbit variables), with and without the mirror, for an image of C that M falsifies."""
import importlib.util, json, os, random, sys, time
from pathlib import Path

W = Path('<run-dir>')
RES = Path('<review-results>')
s = importlib.util.spec_from_file_location('enc', RES / 'C7UPPER/gen.py'); G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
E = G.Enc(6, 8, 10)
inv = {v: C for C, v in E.tvar.items()}
cuts = [[int(x) for x in l.split()[:-1]] for l in (W / 'cuts.clauses').read_text().splitlines() if l.strip()]
# a cut literal -s*v forbids orient(t) having sign s, t the canonical triple of v
recs = [[(inv[abs(l)], -1 if l > 0 else 1) for l in c] for c in cuts]


def search(M, rec, mirror):
    """sigma (dict layer->shift) with sign_M(orient(sigma t)) == s*(-1 if mirror) for all records, or None"""
    layers = sorted({x // 6 for t, _ in rec for x in t})
    byl = {}
    for t, sg in rec:
        byl.setdefault(max(layers.index(x // 6) for x in t), []).append((t, -sg if mirror else sg))
    sig = {}

    def img(x):
        i, k = divmod(x, 6)
        return 6 * i + ((-k if mirror else k) + sig[i]) % 6

    def rec_ok(d):
        for t, sg in byl.get(d, ()):
            lit = E.o(img(t[0]), img(t[1]), img(t[2]))
            if (1 if (lit in M) else -1) != sg:
                return False
        return True

    def bt(d):
        if d == len(layers):
            return mirror or any(sig.values())   # the identity image is the cut itself
        for sh in ((0,) if d == 0 else range(6)):
            sig[layers[d]] = sh
            if rec_ok(d) and bt(d + 1):
                return True
        del sig[layers[d]]
        return False
    return dict(sig) if bt(0) else None


mfiles = sorted(W.glob('runs/*/g*/model*.json'), key=lambda p: p.stat().st_mtime)
# time a cut became available: earliest witness file carrying that clause (cuts without a surviving witness predate
# the per-generation directories, hence predate every model sampled here)
ctime = {}
for wp in list(W.glob('runs/**/face_witness.json')) + list(W.glob('runs/**/witness.json')):
    try: w = json.loads(wp.read_text())
    except Exception: continue
    key = frozenset(w['candidate_clause']) if 'candidate_clause' in w else frozenset(-r['variable'] * r['required_sign'] for r in w['records'])
    ctime[key] = min(ctime.get(key, 1e18), wp.stat().st_mtime)
cut_t = [ctime.get(frozenset(c), 0) for c in cuts]
random.seed(1); pick = random.sample(mfiles, min(int(sys.argv[1]), len(mfiles)))
t0 = time.time(); hits = 0
for mp in pick:
    pos = set(json.loads(mp.read_text())); M = pos | {-v for v in range(1, E.ntriplevars + 1) if v not in pos}
    mt = mp.stat().st_mtime; found = None
    for ci, rec in enumerate(recs):
        if cut_t[ci] >= mt: continue
        for mirror in (False, True):
            sg = search(M, rec, mirror)
            if sg is not None:
                found = (ci, mirror, sg); break
        if found: break
    hits += found is not None
    nprev = sum(1 for t in cut_t if t < mt)
    print(mp.relative_to(W), 'earlier cuts', nprev, ('EXCLUDED by image of cut %d%s %s' % (found[0], ' (mirror)' if found[1] else '', found[2])) if found else 'no image excludes it')
    sys.stdout.flush()
print('models %d, excluded by an image of a stored cut %d, %.0fs' % (len(pick), hits, time.time() - t0))
