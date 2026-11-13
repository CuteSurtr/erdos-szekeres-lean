#!/usr/bin/env python3
"""Independent adversarial re-check of claim C3 (residual Boolean tightness, h_R^min = 33).

Independent of ES8SLACK/check_witnesses.py:
  * rows are taken from TWO sources and compared: the gzipped JSON catalog and the
    literal Lean catalog Residual32Bridge2650/Catalog.lean (the exact object that the Lean
    definition Excludes2650Zero quantifies over); the Lean file is parsed directly;
  * Lean numerals of type Fin 154 are checked to be < 154 (no silent wrap-around);
  * each Lean row code is recomputed as rowCode base support = sum_{i in S} base^i
    (as the Lean file claims, checked there by decide +kernel) and compared;
  * witness feasibility is evaluated with bitmasks + int.bit_count (exact, unbounded ints),
    not with Python sets;
  * witness 0 is compared with the repository CP-SAT record;
  * pairwise overlaps, distinctness, P1' (states 1,2,4,7) are recomputed.
Usage: python3 -I check_C3.py
"""
import gzip, hashlib, json, re, sys, itertools

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
E = ROOT + '/experiments'
JSON_SRC = E + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
LEAN_CAT = E + '/omission-residual32-bridge2650-2026-10-11/Residual32Bridge2650/Catalog.lean'
CPSAT = E + '/omission-residual32-cpsat-2026-10-11/results.json'
WIT = TOP + '/witnesses.json'

out = {}

# ---------- JSON catalog ----------
raw_gz = open(JSON_SRC, 'rb').read()
raw = gzip.decompress(raw_gz)
out['json_sha256_decompressed'] = hashlib.sha256(raw).hexdigest()
out['json_sha256_archive'] = hashlib.sha256(raw_gz).hexdigest()
d = json.loads(raw)
N = len(d['states'])
jrows = []
for r in d['constraints']:
    sup = r['support']
    assert all(isinstance(i, int) and 0 <= i < N for i in sup), 'json index out of range'
    assert len(set(sup)) == len(sup), 'duplicate index in json support'
    rhs = r['rhs']
    assert isinstance(rhs, int)
    jrows.append((frozenset(sup), rhs))
out['json_states'] = N
out['json_rows'] = len(jrows)

# ---------- Lean literal catalog ----------
txt = open(LEAN_CAT, encoding='utf-8').read()
out['lean_catalog_sha256'] = hashlib.sha256(txt.encode('utf-8')).hexdigest()
mbase = re.search(r'^def base : ℕ := (\d+)$', txt, re.M)
base = int(mbase.group(1))
chunk_names = re.search(r'^def rowChunks := #\[(.*)\]$', txt, re.M).group(1).split(', ')
row_re = re.compile(r'\(\{([0-9, ]*)\}, (\d+), (\d+)\)')
lrows = []
for name in chunk_names:
    m = re.search(r'^def ' + re.escape(name) + r' : Array \(Finset \(Fin 154\) × ℕ × ℕ\) := #\[\n(.*?)\n\]$',
                  txt, re.M | re.S)
    body = m.group(1)
    lines = body.split('\n')
    for ln in lines:
        ln = ln.strip()
        if ln.endswith(','):
            ln = ln[:-1]
        mm = row_re.fullmatch(ln)
        assert mm, ('unparsed line', ln[:80])
        elems = [int(x) for x in mm.group(1).split(', ')] if mm.group(1) else []
        assert all(0 <= e < 154 for e in elems), 'Fin 154 literal >= 154 (would wrap)'
        dem = int(mm.group(2)); code = int(mm.group(3))
        assert code == sum(base ** e for e in set(elems)), 'rowCode mismatch'
        lrows.append((frozenset(elems), dem))
out['lean_rows'] = len(lrows)
out['lean_base'] = base
out['lean_eq_json_rowwise'] = (lrows == jrows)
# the Lean accessor is row r = rowChunks[r/128][r%128]; confirm chunk sizes are 128 except last
sizes = []
for name in chunk_names:
    m = re.search(r'^def ' + re.escape(name) + r' : Array .*? := #\[\n(.*?)\n\]$', txt, re.M | re.S)
    sizes.append(len(m.group(1).split('\n')))
out['lean_chunk_sizes_ok'] = all(s == 128 for s in sizes[:-1]) and sizes[-1] == 2650 - 128 * (len(sizes) - 1)
out['lean_chunk_order_ok'] = chunk_names == ['rows%d' % (128 * k) for k in range(len(chunk_names))]

# demand statistics
out['demand_values'] = sorted(set(dm for _, dm in jrows))

# ---------- witnesses ----------
W = json.load(open(WIT))
wits = W['residual_2650_33_hole_witnesses_state0_occupied']
masks_rows = [(sum(1 << i for i in s), dm) for s, dm in lrows]


def check(h):
    res = {}
    res['len'] = len(h)
    res['distinct_indices'] = len(set(h)) == len(h)
    res['in_range'] = all(isinstance(i, int) and 0 <= i < N for i in h)
    hm = sum(1 << i for i in set(h))
    res['popcount'] = hm.bit_count()
    res['state0_occupied'] = not (hm & 1)
    viol = [r for r, (sm, dm) in enumerate(masks_rows) if (sm & hm).bit_count() < dm]
    tight = sum(1 for (sm, dm) in masks_rows if (sm & hm).bit_count() == dm)
    res['violated_rows'] = viol
    res['tight_rows'] = tight
    # P1': at least one of states 1,2,4,7 occupied
    res['P1prime_ok'] = sum((hm >> i) & 1 for i in (1, 2, 4, 7)) <= 3
    # alternative-convention variant (columns indexed the other way): states [a,0,0,0,0], a=1..4
    alt = [d['states'].index([a, 0, 0, 0, 0]) for a in (1, 2, 3, 4)]
    res['P1prime_alt_states'] = alt
    res['P1prime_alt_ok'] = sum((hm >> i) & 1 for i in alt) <= 3
    res['min_hole_index'] = min(h)
    return res, hm

results = []
hms = []
for k, h in enumerate(wits):
    r, hm = check(h)
    results.append(r)
    hms.append(hm)
out['witness_checks'] = results
out['witnesses_distinct'] = len(set(hms)) == len(hms)
out['pairwise_overlap'] = {f'{a}-{b}': (hms[a] & hms[b]).bit_count() for a, b in itertools.combinations(range(len(hms)), 2)}
out['pairwise_hamming'] = {f'{a}-{b}': (hms[a] ^ hms[b]).bit_count() for a, b in itertools.combinations(range(len(hms)), 2)}

# P1' state identities
out['state_profiles_1_2_4_7'] = {i: d['states'][i] for i in (0, 1, 2, 4, 7)}

# witness 0 vs CP-SAT record
cp = json.load(open(CPSAT))
out['cpsat_sha_field'] = cp['source_decompressed_sha256']
out['witness0_equals_cpsat'] = sorted(cp['best_assignment_holes']) == sorted(wits[0])

ok = (out['json_sha256_decompressed'] == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
      and out['lean_catalog_sha256'] == '5b97f861a4bf4272d2d3d7bbadbb076261f5d7c3c9bd2e86fbf4b1a9e87a1c71'
      and out['json_rows'] == 2650 and out['lean_rows'] == 2650 and out['json_states'] == 154
      and out['lean_eq_json_rowwise'] and out['lean_chunk_sizes_ok'] and out['lean_chunk_order_ok']
      and out['witnesses_distinct']
      and all(r['len'] == 33 and r['popcount'] == 33 and r['distinct_indices'] and r['in_range']
              and r['state0_occupied'] and not r['violated_rows'] and r['P1prime_ok'] for r in results))
out['ALL_OK'] = ok
print(json.dumps(out, indent=1, default=str))
json.dump(out, open(HERE + '/check_C3_out.json', 'w'), indent=1, default=str)
sys.exit(0 if ok else 1)
