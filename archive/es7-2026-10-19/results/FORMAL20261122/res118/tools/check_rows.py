#!/usr/bin/env python3
"""Independent check (own parser, not gen_rows.py) that the Lean data equals the slice row files.

res118-lean, 22 Nov 2026. Parses lean/Res118/Rows.lean (blocks rowsP/Q/U/A from their chunk definitions) and the
index lists fIndices/loIndices of lean/Res118/LemmaA.lean, then compares with every slice's extra.json:
capacity rows (F, T), (Lo, B - T) and the unit rows in file order. Exit code 0 only if everything matches.
"""
import gzip, hashlib, json, re, sys
from pathlib import Path

D = Path('/home/jay/research/data/formalize-20261122/res118')
W = Path('/home/jay/research/data/es308-20261114/inputs')
LO = Path('/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113')
SLICES = {  # name: (file, B, T, block expression)
    'b33s18': (LO / 'data/cert_66_55_leanrows/extra_66_55_leanrows.json', 33, 18, []),
    'b34s18': (W / 's18-v13/extra.json', 34, 18, ['P', 'Q']),
    'b34s19': (W / 's19/extra.json', 34, 19, ['P']),
    'b35s18': (W / 'b35s18-v13/extra.json', 35, 18, ['P', 'Q']),
    'b35s19': (W / 'b35s19-v16/extra.json', 35, 19, ['P', 'Q', 'U']),
    'b35s20': (W / 'b35s20-v169/extra.json', 35, 20, ['P', 'Q', 'A']),
}
import argparse
ap = argparse.ArgumentParser()
ap.add_argument('--rows', default=str(D / 'lean/Res118/Rows.lean'))
ap.add_argument('--lemma', default=str(D / 'lean/Res118/LemmaA.lean'))
ARGS = ap.parse_args()
text = Path(ARGS.rows).read_text()
defs = dict(re.findall(r'def (rows[PQUA]_\d\d) : List \(List Nat\) := \[(.*?)\n\]', text, re.S))
blocks = {}
for b in 'PQUA':
    m = re.search(rf'def rows{b} : List \(List Nat\) := (.*)\n', text)
    names = [x.strip() for x in m.group(1).split('++')]
    rows = []
    for nm in names:
        body = defs[nm]
        rows += [[int(t) for t in r.split(',')] for r in re.findall(r'\[([0-9, ]+)\]', body)]
    blocks[b] = rows
lemma = Path(ARGS.lemma).read_text()
def lean_list(name):
    m = re.search(rf'def {name} : List ℕ := \[(.*?)\]', lemma, re.S)
    return [int(t) for t in m.group(1).replace('\n', ' ').split(',')]
fI, loI = lean_list('fIndices'), lean_list('loIndices')
src = json.loads(gzip.decompress((W / 'source-2650.json.gz').read_bytes()))
st = src['states']
ok = True
ok &= fI == [i for i, s in enumerate(st) if s[0] >= 5] and loI == [i for i, s in enumerate(st) if s[0] <= 4]
report = {'blocks': {b: len(v) for b, v in blocks.items()}, 'f_lo_lists_match_states': ok, 'slices': {}}
for k, (p, B, T, expr) in SLICES.items():
    ex = json.loads(Path(p).read_text())
    want = [r['support'] for r in ex[2:]]
    got = [s for b in expr for s in blocks[b]]
    r = {'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest(),
         'capacity_F': ex[0] == {'support': fI, 'rhs': T}, 'capacity_Lo': ex[1] == {'support': loI, 'rhs': B - T},
         'unit_rhs_all_1': all(x['rhs'] == 1 for x in ex[2:]), 'unit_rows_equal_in_order': got == want,
         'unit_rows': len(want)}
    report['slices'][k] = r
    ok &= all(v for kk, v in r.items() if kk not in ('sha256', 'unit_rows'))
# The nine L4 rows, recounted from the JSON (independent of the Lean proof).
nine = [973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315]
cnt = {}
for j in nine:
    c = src['constraints'][j]
    assert c['rhs'] == 6
    for i in c['support']:
        cnt[i] = cnt.get(i, 0) + 1
report['nine_rows_cover_F_three_times'] = sorted(cnt) == fI and set(cnt.values()) == {3}
ok &= report['nine_rows_cover_F_three_times']
report['rows_lean_sha256'] = hashlib.sha256(Path(ARGS.rows).read_bytes()).hexdigest()
report['ok'] = bool(ok)
print(json.dumps(report, indent=1))
sys.exit(0 if ok else 1)
