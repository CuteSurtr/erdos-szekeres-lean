#!/usr/bin/env python3
"""Cross-check the JSON catalogs used by the certificate replay against the Lean literal sources.

1. Balanced/residual state lists: JSON == Lean `catalog` literal, and == the claimed profile sets.
2. Balanced base rows 0..2684: JSON support == set(cycle), rhs == len(cycle)-7, from the extracted
   Geometry*.lean files (and their hashes vs balanced-rows-export.json if recorded).
3. Balanced cuts 2685..3130: JSON == BalancedCoverCutsV2.lean literals; exact replay of every cut
   margin as stated in the Lean source (CoverCuts.rounded_cover_cut):
       C*(q-1) + sum_i (L_i - [i in s]*C)_+  <  sum_p w_p d_p      (natural subtraction)
   with parents restricted to base rows or strictly earlier cuts.
4. Residual catalog composition (cycle rows |S|-7, block rows |S|-22, etc.).
Usage: python3 -I catalog_check.py
"""
import glob, gzip, hashlib, itertools, json, os, re, sys

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
R = ROOT
X = R + '/experiments'
HERE = os.path.dirname(os.path.abspath(__file__))
ok = True
report = {}


def fail(msg):
    global ok
    ok = False
    print('FAIL:', msg)


def lean_catalog(path):
    txt = open(path).read()
    m = re.search(r'def catalog : List \(List Nat\) := (\[\[.*?\]\])', txt, re.S)
    return json.loads(m.group(1))


bal = json.load(open(X + '/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))
res_raw = gzip.decompress(open(X + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read())
res = json.loads(res_raw)

# 1. states
bl = lean_catalog(R + '/ErdosSzekeres/Omission/BalancedCatalogData.lean')
rl = lean_catalog(R + '/ErdosSzekeres/Omission/ResidualCatalogData.lean')
bal_set = {t for t in itertools.product(range(6), repeat=5) if all(t[i] >= t[i + 1] for i in range(4))}
res_set = {t + (0,) for t in itertools.product(range(7), repeat=4)
           if all(t[i] >= t[i + 1] for i in range(3)) and (t[0] < 6 or t[1] == 6)}
report['balanced_states'] = dict(json=len(bal['states']), lean=len(bl), claimed_set=len(bal_set),
                                 json_eq_lean=bal['states'] == bl,
                                 set_eq=set(map(tuple, bl)) == bal_set and len(set(map(tuple, bl))) == len(bl))
report['residual_states'] = dict(json=len(res['states']), lean=len(rl), claimed_set=len(res_set),
                                 json_eq_lean=res['states'] == rl,
                                 set_eq=set(map(tuple, rl)) == res_set and len(set(map(tuple, rl))) == len(rl))
for k in ('balanced_states', 'residual_states'):
    v = report[k]
    if not (v['json_eq_lean'] and v['set_eq']):
        fail(k)

rows = [(frozenset(c['support']), int(c['rhs'])) for c in bal['constraints']]
assert len(rows) == 3131

# 2. base rows vs extracted Geometry cycles
ext = HERE + '/extract_balanced_rows'
cyc = {}
for f in sorted(glob.glob(ext + '/Geometry*.lean')):
    txt = open(f).read()
    start = int(re.search(r'cycles\[r\.val - (\d+)\]!', txt).group(1))
    body = re.search(r'def cycles : Array \(List \(Fin 252\)\) := #\[(.*?)\n\]', txt, re.S).group(1)
    lists = [json.loads(x) for x in re.findall(r'\[[0-9, ]+\]', body)]
    for j, l in enumerate(lists):
        cyc[start + j] = l
exp = json.load(open(X + '/omission-global-assembly-2026-10-10/balanced-rows-export.json'))
fh = exp.get('files', {})
hash_ok = hash_n = 0
for f in sorted(glob.glob(ext + '/*.lean')):
    b = os.path.basename(f)
    keys = [k for k in fh if k.endswith('/' + b) or k == b]
    if keys:
        hash_n += 1
        hash_ok += hashlib.sha256(open(f, 'rb').read()).hexdigest() == fh[keys[0]]
bad = [r for r in range(2685) if r not in cyc or len(set(cyc[r])) != len(cyc[r])
       or frozenset(cyc[r]) != rows[r][0] or len(cyc[r]) - 7 != rows[r][1]]
lens = {}
for r in range(2685):
    lens[len(cyc[r])] = lens.get(len(cyc[r]), 0) + 1
report['balanced_base_rows'] = dict(cycles_parsed=len(cyc), mismatches=len(bad), first_bad=bad[:5],
                                    cycle_length_hist=dict(sorted(lens.items())),
                                    source_files_hashed=hash_n, source_hash_matches=hash_ok)
if bad or len(cyc) != 2685:
    fail('balanced base rows')

# 3. cuts
txt = open(X + '/omission-cover-certificates-2026-10-10/BalancedCoverCutsV2.lean').read()
sup = {int(k): frozenset(json.loads('[' + v + ']'))
       for k, v in re.findall(r'def support(\d+) : Finset \(Fin 252\) := \{([0-9, ]*)\}', txt)}
dem_line = re.search(r'def demand : Fin 446 → ℕ := !\[([0-9, ]*)\]', txt).group(1)
dem = [int(x) for x in dem_line.split(',')]
sup_line = re.search(r'def support : Fin 446 → Finset \(Fin 252\) := !\[([a-z0-9, ]*)\]', txt).group(1)
assert [x.strip() for x in sup_line.split(',')] == ['support%d' % k for k in range(446)]
thm = re.findall(r'theorem cut(\d+) \(holes.*?\n\s+(\d+) ≤ ∑ i ∈ support(\d+), holes i := by\n'
                 r'\s+apply rounded_cover_cut !\[(.*?)\] !\[(.*?)\] !\[(.*?)\]\n\s+support(\d+) (\d+) (\d+) \(by decide \+kernel\)',
                 txt, re.S)
assert len(thm) == 446, len(thm)
cut_json = json.load(open(X + '/omission-cover-certificates-2026-10-10/balanced-v2-cuts.json'))['proofs']
cbad = []
min_margin = None
for (k, tgt, k2, ps, ds, ws, k3, C, q) in thm:  # rounded_cover_cut (s) (capacity target)
    k, tgt, q, C = int(k), int(tgt), int(q), int(C)
    assert int(k2) == k == int(k3)
    if tgt != q or dem[k] != q:
        cbad.append((k, 'target')); continue
    if rows[2685 + k] != (sup[k], q):
        cbad.append((k, 'json row')); continue
    parents = [p.strip() for p in ps.split(',')]
    dlist = [d.strip() for d in ds.split(',')]
    wl = [int(w) for w in ws.split(',')]
    psup, pdem = [], []
    for p, d in zip(parents, dlist):
        m1 = re.fullmatch(r'OmissionBalanced\.support (\d+)', p)
        m2 = re.fullmatch(r'support(\d+)', p)
        if m1:
            n = int(m1.group(1)); assert n < 2685
            assert d == 'OmissionBalanced.demand %d' % n
            psup.append(rows[n][0]); pdem.append(rows[n][1])
        elif m2:
            j = int(m2.group(1))
            if not j < k:
                cbad.append((k, 'forward ref')); break
            assert int(d) == dem[j]
            psup.append(sup[j]); pdem.append(dem[j])
        else:
            raise ValueError(p)
    L = [0] * 252
    for s_, w in zip(psup, wl):
        for i in s_:
            L[i] += w
    lhs = C * (q - 1) + sum(max(0, L[i] - (C if i in sup[k] else 0)) for i in range(252))
    rhs = sum(w * d for w, d in zip(wl, pdem))
    margin = rhs - lhs
    min_margin = margin if min_margin is None else min(min_margin, margin)
    if margin < 1:
        cbad.append((k, 'margin', margin))
    cj = cut_json[k]
    if frozenset(cj['support']) != sup[k] or cj['rhs'] != q or cj['capacity'] != C:
        cbad.append((k, 'cuts.json mismatch'))
report['balanced_cuts'] = dict(parsed=len(thm), problems=cbad[:10], n_problems=len(cbad), min_margin=min_margin,
                               demand_hist={d: dem.count(d) for d in sorted(set(dem))})
if cbad:
    fail('balanced cuts')

# 4. residual composition
rr = [(frozenset(c['support']), int(c['rhs'])) for c in res['constraints']]
orig = rr[:1187]
cyc_rows = [r for r in orig if r[1] == len(r[0]) - 7]
blk_rows = [r for r in orig if r[1] == len(r[0]) - 22]
other = [r for r in orig if r not in cyc_rows and r not in blk_rows]
report['residual_rows'] = dict(total=len(rr), original=len(orig), cycle_like=len(cyc_rows),
                               block_like=len(blk_rows),
                               block_demands=sorted({r[1] for r in blk_rows}),
                               block_support_sizes=sorted({len(r[0]) for r in blk_rows}),
                               other_in_first_1187=len(other),
                               demand_hist_all={d: sum(1 for r in rr if r[1] == d) for d in sorted({r[1] for r in rr})},
                               segment_demands={'1187-2294': sorted({r[1] for r in rr[1187:2295]}),
                                                '2295-2468': sorted({r[1] for r in rr[2295:2469]}),
                                                '2469-2649': sorted({r[1] for r in rr[2469:]})})
print(json.dumps(report, indent=1))
print('CATALOG CHECKS PASSED' if ok else 'CATALOG CHECK FAILURE')
sys.exit(0 if ok else 1)
