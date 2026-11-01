#!/usr/bin/env python3
"""Scope probe, part 2.
(a) Balanced: literal 252-state supports in Lean sources (<= 3 MB) that are not catalog supports;
    report those the 72-hole witness does not hit.
(b) JSON row files under experiments/ (<= 30 MB, gz allowed) that carry a 'states' list of length
    154 or 252 and a 'constraints'/'rows' list of {support, rhs|demand}: check the matching witness
    against every row with its stated demand; report files with violations (rows there are not
    necessarily proved; any violation must be followed up).
Usage: python3 -I extra_rows_scan2.py
"""
import gzip, json, os, re

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
REPO = ROOT
EXP = REPO + '/experiments'
bal = json.load(open(EXP + '/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))
res = json.loads(gzip.decompress(open(EXP + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read()))
bcat = {frozenset(c['support']) for c in bal['constraints']}
W = json.load(open(TOP + '/witnesses.json'))
HB = frozenset(W['balanced_v2_72_hole_witness'])
HR = [frozenset(h) for h in W['residual_2650_33_hole_witnesses_state0_occupied']]

# (a)
pats = [
    re.compile(r'def (\w+) : Finset \(Fin 252\) := \{([0-9,\s]+)\}'),
    re.compile(r'def (\w+) : List \(Fin 252\) := \[([0-9,\s]+)\]'),
    re.compile(r'def (\w+) : Fin \d+ → Fin 252 := !\[([0-9,\s]+)\]'),
]
found = {}
for root in (REPO + '/ErdosSzekeres', EXP):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith('.lean'):
                continue
            p = os.path.join(dp, f)
            if os.path.getsize(p) > 3_000_000:
                continue
            src = open(p, encoding='utf-8', errors='replace').read()
            for pat in pats:
                for m in pat.finditer(src):
                    vals = [int(x) for x in m.group(2).replace('\n', ' ').split(',') if x.strip()]
                    if vals and max(vals) < 252:
                        found.setdefault(frozenset(vals), []).append((os.path.relpath(p, REPO), m.group(1)))
nonc = {s: v for s, v in found.items() if s not in bcat}
print('(a) balanced literal sets:', len(found), ' not catalog supports:', len(nonc))
miss = [(s, v) for s, v in nonc.items() if not (s & HB)]
print('    of those, missed by the 72-hole witness:', len(miss))
for s, v in miss[:20]:
    print('   ', len(s), sorted(s), v[:3])

# (b)
print('(b) JSON row files')
skipped = 0
for dp, dn, fn in os.walk(EXP):
    for f in fn:
        if not (f.endswith('.json') or f.endswith('.json.gz')):
            continue
        p = os.path.join(dp, f)
        if os.path.getsize(p) > 30_000_000:
            skipped += 1
            continue
        try:
            raw = open(p, 'rb').read()
            if f.endswith('.gz'):
                raw = gzip.decompress(raw)
            d = json.loads(raw)
        except Exception:
            continue
        if not isinstance(d, dict) or not isinstance(d.get('states'), list):
            continue
        n = len(d['states'])
        if n not in (154, 252):
            continue
        rows = d.get('constraints') or d.get('rows')
        if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict) or 'support' not in rows[0]:
            continue
        Hlist = [HB] if n == 252 else HR
        out = []
        for k, H in enumerate(Hlist):
            bad = 0
            for r in rows:
                dem = r.get('rhs', r.get('demand'))
                if dem is None:
                    continue
                if len(frozenset(r['support']) & H) < int(dem):
                    bad += 1
            out.append(bad)
        flag = '  <-- VIOLATIONS' if any(out) else ''
        print(f'    {os.path.relpath(p, EXP)}: states {n}, rows {len(rows)}, violations per witness {out}{flag}')
print('    skipped (>30MB):', skipped)
