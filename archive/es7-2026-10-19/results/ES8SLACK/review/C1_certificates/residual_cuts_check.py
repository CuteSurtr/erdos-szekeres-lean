#!/usr/bin/env python3
"""Exact replay of the 1,108 residual V2 rounded cuts as written in ResidualCoverCutsV2.lean, and comparison
with rows 1187..2294 of source-2650.json.gz.  Margin (CoverCuts.rounded_cover_cut, natural subtraction):
    C*(q-1) + sum_i (L_i - [i in s]*C)_+  <  sum_p w_p d_p ,  argument order `support_k C q`.
Parents: OmissionResidual.support N (original row N < 1187, taken from the JSON, which was checked
against the kernel-checked cycle sources for cycle rows) or an earlier cut.
Usage: python3 -I residual_cuts_check.py
"""
import gzip, json, re, sys

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
X = ROOT + '/experiments'
src = json.loads(gzip.decompress(open(X + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read()))
rows = [(frozenset(c['support']), int(c['rhs'])) for c in src['constraints']]
txt = open(X + '/omission-cover-certificates-2026-10-10/ResidualCoverCutsV2.lean').read()
sup = {int(k): frozenset(json.loads('[' + v + ']'))
       for k, v in re.findall(r'def support(\d+) : Finset \(Fin 154\) := \{([0-9, ]*)\}', txt)}
dem = [int(x) for x in re.search(r'def demand : Fin 1108 → ℕ := !\[([0-9, ]*)\]', txt).group(1).split(',')]
sl = re.search(r'def support : Fin 1108 → Finset \(Fin 154\) := !\[([a-z0-9, ]*)\]', txt).group(1)
assert [x.strip() for x in sl.split(',')] == ['support%d' % k for k in range(1108)]
thm = re.findall(r'theorem cut(\d+) \(holes.*?\n\s+(\d+) ≤ ∑ i ∈ support(\d+), holes i := by\n'
                 r'\s+apply rounded_cover_cut !\[(.*?)\] !\[(.*?)\] !\[(.*?)\]\n\s+support(\d+) (\d+) (\d+) \(by decide \+kernel\)',
                 txt, re.S)
assert len(thm) == 1108, len(thm)
bad, minm = [], None
for (k, tgt, k2, ps, ds, ws, k3, C, q) in thm:
    k, tgt, C, q = int(k), int(tgt), int(C), int(q)
    assert int(k2) == k == int(k3)
    if tgt != q or dem[k] != q or rows[1187 + k] != (sup[k], q):
        bad.append((k, 'literal/json')); continue
    psup, pdem = [], []
    for p, d in zip([x.strip() for x in ps.split(',')], [x.strip() for x in ds.split(',')]):
        m1 = re.fullmatch(r'OmissionResidual\.support (\d+)', p)
        m2 = re.fullmatch(r'support(\d+)', p)
        if m1:
            n = int(m1.group(1)); assert n < 1187 and d == 'OmissionResidual.demand %d' % n
            psup.append(rows[n][0]); pdem.append(rows[n][1])
        elif m2 and int(m2.group(1)) < k:
            j = int(m2.group(1)); assert int(d) == dem[j]
            psup.append(sup[j]); pdem.append(dem[j])
        else:
            bad.append((k, 'parent ' + p)); break
    wl = [int(w) for w in ws.split(',')]
    L = [0] * 154
    for s_, w in zip(psup, wl):
        for i in s_:
            L[i] += w
    margin = sum(w * d for w, d in zip(wl, pdem)) - (C * (q - 1) + sum(max(0, L[i] - (C if i in sup[k] else 0)) for i in range(154)))
    minm = margin if minm is None else min(minm, margin)
    if margin < 1:
        bad.append((k, 'margin', margin))
print(json.dumps({'cuts': len(thm), 'problems': bad[:10], 'n_problems': len(bad), 'min_margin': minm}))
print('ALL 1108 RESIDUAL V2 CUTS REPLAY EXACTLY AND MATCH JSON ROWS 1187-2294' if not bad else 'FAILURE')
sys.exit(0 if not bad else 1)
