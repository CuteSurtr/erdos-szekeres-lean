#!/usr/bin/env python3
"""Do the three 33-hole residual witnesses violate instances of ALREADY-PROVED Lean templates?

Each coupled template T (Lean: ErdosSzekeres.Omission.CoupledTemplate*, and the two experiment
templates Sixth / SixthRelaxed) proves, via `hole_bound`, that for every injective sigma with
`Compatible sigma` the support image(sigma) contains a missing state in every actual residual
configuration.  If image(sigma) lies inside the occupied set of a witness, that witness violates a
geometrically valid row that is NOT in the 2,650-row catalog (it cannot be: the witness satisfies all
catalog rows).

The compatibility semantics are re-implemented exactly as in the repository's
experiments/omission-residual32-fourth-global-variants-2026-10-10/search.py, whose output maps were
afterwards kernel-checked against the Lean `check` function (positive control below reproduces its
3 maps on the case-4 32-hole witness).  A map found here is a CANDIDATE row: its Lean `check sigma`
evaluation has not been run.  Exhaustive "none found" results are relative to this re-implementation.
Usage: <python with numpy> -I template_instances.py [seconds_per_search]
"""
import ast, gzip, hashlib, json, re, sys, time
from itertools import permutations
import numpy as np

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
R = ROOT
E = R + '/experiments'
LIMIT = float(sys.argv[1]) if len(sys.argv) > 1 else 60.0
TEMPLATES = {
    'Base': R + '/ErdosSzekeres/Omission/CoupledTemplate.lean',
    'Second': R + '/ErdosSzekeres/Omission/CoupledTemplateSecond.lean',
    'Third': R + '/ErdosSzekeres/Omission/CoupledTemplateThird.lean',
    'Fourth': R + '/ErdosSzekeres/Omission/CoupledTemplateFourth.lean',
    'Fifth': R + '/ErdosSzekeres/Omission/CoupledTemplateFifth.lean',
    'Nine': R + '/ErdosSzekeres/Omission/CoupledTemplateNine.lean',
    'Sixth': E + '/omission-residual32-sixth-variants-2026-10-10/SixthTemplate.lean',
    'SixthRelaxed': E + '/omission-residual32-sixth-relaxed-2026-10-10/SixthRelaxedTemplate.lean',
}

raw = gzip.decompress(open(E + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read())
assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
cat = json.loads(raw)
states = cat['states']
catalog_supports = {frozenset(r['support']) for r in cat['constraints']}
N = len(states)


def cells(s):
    return {(i + 1, y) for i, h in enumerate(s[:4]) for y in range(1, h + 1)}

C = [cells(s) for s in states]
# pair boxes and triple table (same formulas as the repository model.py)
nonempty = np.zeros((N, N), bool)
mn = np.zeros((2, N, N), np.int16)
mx = np.zeros((2, N, N), np.int16)
for a in range(N):
    for b in range(N):
        d = C[b] - C[a]
        if d:
            nonempty[a, b] = True
            mn[0, a, b] = min(z[0] for z in d); mx[0, a, b] = max(z[0] for z in d)
            mn[1, a, b] = min(z[1] for z in d); mx[1, a, b] = max(z[1] for z in d)
idx = np.arange(N, dtype=np.int16)
A_, B_, C_ = np.meshgrid(idx, idx, idx, indexing='ij')
TT = (A_ != B_) & (B_ != C_) & (A_ != C_)
grids = (A_, B_, C_)
for perm in permutations(range(3)):
    odd = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3)) % 2
    coord = 1 if odd else 0
    p, q, r = (grids[perm[k]] for k in range(3))
    present = nonempty[p, q] & nonempty[q, r] & nonempty[p, r]
    forced = mx[coord][q, r] <= mn[coord][p, q]
    TT &= (~present) | forced
del A_, B_, C_, grids
diff = [[C[b] - C[a] - {(1, 6)} for b in range(N)] for a in range(N)]


def load_template(path):
    txt = open(path).read()
    crit = []
    k = None
    for name, kind in [('emptyTests', 'empty'), ('domainTests', 'domain'), ('positiveTests', 'positive')]:
        m = re.search(r'def ' + name + r' : List \(Fin (\d+)[^\n]+:= (\[[^\n]*\])', txt)
        assert m, (path, name)
        k = int(m.group(1))
        crit.extend((kind, tuple(t)) for t in ast.literal_eval(m.group(2)))
    return k, crit, hashlib.sha256(txt.encode()).hexdigest()


def search(k, criteria, targets, limit, stop_after=None):
    def good(item, Smap):
        kind, q = item
        a, b = Smap[q[0]], Smap[q[1]]
        if kind == 'positive':
            return bool(TT[a, b, Smap[q[2]]])
        return (not diff[a][b]) if kind == 'empty' else ((q[2], q[3]) not in diff[a][b])
    scopes = [set(q[:3] if kind == 'positive' else q[:2]) for kind, q in criteria]
    checks = [[(c, sc) for c, sc in zip(criteria, scopes) if i in sc] for i in range(k)]
    start = time.monotonic()
    st = dict(nodes=0, maps=0, halted=None)
    found = {}

    def dfs(Smap, used, assigned):
        st['nodes'] += 1
        if stop_after and len(found) >= stop_after:
            st['halted'] = 'stop_after'; return
        if time.monotonic() - start > limit:
            st['halted'] = 'time limit'; return
        if len(assigned) == k:
            st['maps'] += 1
            assert all(good(c, Smap) for c in criteria)
            key = frozenset(Smap)
            assert len(key) == k
            found.setdefault(key, list(Smap))
            return
        best = None
        for i in sorted(set(range(k)) - assigned):
            ready = [c for c, sc in checks[i] if sc - {i} <= assigned]
            opts = []
            for v in targets:
                if v in used:
                    continue
                Smap[i] = v
                if all(good(c, Smap) for c in ready):
                    opts.append(v)
            Smap[i] = None
            score = (len(opts), -len(ready), -len(checks[i]))
            if best is None or score < best[0]:
                best = (score, i, opts)
            if not opts:
                return
        _, i, opts = best
        for v in opts:
            Smap[i] = v
            dfs(Smap, used | {v}, assigned | {i})
            if st['halted']:
                return
        Smap[i] = None

    dfs([None] * k, set(), set())
    return dict(complete=st['halted'] is None, stop=st['halted'], nodes=st['nodes'], maps=st['maps'],
                distinct_supports=len(found), supports=[sorted(s) for s in found],
                ordered_maps=list(found.values())[:20], seconds=round(time.monotonic() - start, 3))

out = {'limit_s': LIMIT, 'templates': {}, 'controls': {}, 'witness_results': {}}
tpl = {}
for name, path in TEMPLATES.items():
    k, crit, h = load_template(path)
    tpl[name] = (k, crit)
    out['templates'][name] = {'owners': k, 'criteria': len(crit), 'sha256': h, 'path': path.replace(R, '$REPO')}

# positive control: case-4 32-hole witness, Fourth template, occupied states -> repo found exactly 3 maps
w4 = json.load(open(E + '/omission-residual32-case4-2026-10-10/witness.json'))
occ4 = sorted(set(range(N)) - set(w4['holes']))
ctl = search(*tpl['Fourth'], occ4, LIMIT)
ref = json.load(open(E + '/omission-residual32-fourth-global-variants-2026-10-10/variants.json'))
out['controls']['fourth_case4'] = {k2: ctl[k2] for k2 in ('complete', 'maps', 'distinct_supports', 'seconds')}
out['controls']['fourth_case4_matches_repo'] = sorted(map(sorted, ctl['supports'])) == sorted(sorted(s) for s in ref['supports'])

W = json.load(open(TOP + '/witnesses.json'))['residual_2650_33_hole_witnesses_state0_occupied']
for wi, holes in enumerate(W):
    occ = sorted(set(range(N)) - set(holes))
    for name, (k, crit) in tpl.items():
        res = search(k, crit, occ, LIMIT, stop_after=50)
        res['any_support_in_catalog'] = any(frozenset(s) in catalog_supports for s in res['supports'])
        res['all_supports_inside_occupied'] = all(not (set(s) & set(holes)) for s in res['supports'])
        out['witness_results'][f'w{wi}:{name}'] = res
        print(f'w{wi} {name}: complete={res["complete"]} maps={res["maps"]} supports={res["distinct_supports"]} '
              f'{res["seconds"]}s', file=sys.stderr, flush=True)
json.dump(out, open(HERE + '/template_instances_out.json', 'w'), indent=1)
summary = {key: (v['complete'], v['distinct_supports']) for key, v in out['witness_results'].items()}
print(json.dumps({'controls': out['controls'], 'summary(complete, distinct supports)': summary}, indent=1))
