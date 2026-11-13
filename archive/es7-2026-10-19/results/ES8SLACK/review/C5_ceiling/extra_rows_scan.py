#!/usr/bin/env python3
"""Scope probe for C5: are there residual supports in the repository's Lean sources (outside the
2,650-row catalog) that the three 33-hole residual witnesses fail to hit?

Extracts literal 154-state supports of the forms
  def support : Finset (Fin 154) := {..}
  def support : List (Fin 154) := [..]
  def states : Fin k → Fin 154 := ![..]
  def stateNNN : Fin 13 → Fin 154 := ![..]           (variant families)
  def <name> : List (Fin 154) := [..]                  (cycle lists etc.)
from every .lean file under ErdosSzekeres/Omission and experiments/ (skipping files > 3 MB, which
are generated catalogs/certificates).  For every extracted set it reports whether each witness has
at least one hole in it, and whether some 2,650-catalog row with demand >= 1 is contained in it
(which would make it implied).  Demands are NOT inferred here; any miss must be followed up by
reading the corresponding theorem.  Usage: python3 -I extra_rows_scan.py
"""
import gzip, json, os, re

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
REPO = ROOT
res = json.loads(gzip.decompress(open(REPO + '/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read()))
cat = [(frozenset(c['support']), c['rhs']) for c in res['constraints']]
catsets = {s for s, d in cat}
W = json.load(open(TOP + '/witnesses.json'))
Hs = [frozenset(h) for h in W['residual_2650_33_hole_witnesses_state0_occupied']]

pats = [
    re.compile(r'def (support\w*) : Finset \(Fin 154\) := \{([0-9,\s]+)\}'),
    re.compile(r'def (\w+) : List \(Fin 154\) := \[([0-9,\s]+)\]'),
    re.compile(r'def (\w+) : Fin \d+ → Fin 154 := !\[([0-9,\s]+)\]'),
]
found = []
for root in (REPO + '/ErdosSzekeres/Omission', REPO + '/experiments'):
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
                    if not vals or max(vals) >= 154:
                        continue
                    found.append((os.path.relpath(p, REPO), m.group(1), frozenset(vals), len(vals)))

uniq = {}
for path, name, s, ln in found:
    uniq.setdefault(s, []).append((path, name, ln))
print('extracted literal sets:', len(found), ' distinct:', len(uniq))
in_cat = sum(1 for s in uniq if s in catsets)
print('distinct sets that are literally a catalog support:', in_cat)

misses = []
for s, srcs in uniq.items():
    hit = [len(s & H) for H in Hs]
    implied = any(cs <= s and d >= 1 for cs, d in cat)
    if min(hit) == 0:
        misses.append((s, srcs, hit, implied))
print('sets missed (no hole) by at least one witness:', len(misses))
for s, srcs, hit, implied in sorted(misses, key=lambda t: (len(t[0]), sorted(t[0]))):
    print(f'  |S|={len(s):3d} hits per witness={hit} implied_by_catalog_row={implied} in_catalog={s in catsets}')
    for path, name, ln in srcs[:4]:
        print(f'      {path} :: {name} (list length {ln})')
    print('      S =', sorted(s))
