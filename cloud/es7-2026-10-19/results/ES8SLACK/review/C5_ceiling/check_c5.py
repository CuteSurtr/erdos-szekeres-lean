#!/usr/bin/env python3
"""Independent re-check of claim C5 (ceiling of the omission route).

Standard library only, exact integers.  Written from scratch (does not import or reuse
ES8SLACK/check_witnesses.py).  It

  1. hashes the JSON catalogs and checks the hashes recorded by the 311/313 Lean exports;
  2. parses the *Lean literal* catalogs that the kernel-checked bridges use:
       - BalancedCatalogData.lean / ResidualCatalogData.lean (state profiles, index order),
       - OmissionBalanced Catalog.lean (2,685 base rows; extracted from the repo tarball),
       - BalancedCoverCutsV2.lean (446 cut rows; also cross-checks each cutK theorem's demand),
       - Residual32Bridge2650/Catalog.lean (2,650 residual rows);
  3. checks JSON rows == Lean literal rows, and JSON states == Lean catalog order;
  4. checks each witness against the Lean literal rows (and separately against the JSON rows);
  5. checks P1 and P1' in profile terms (both column conventions) and state-0 occupancy;
  6. prints the resulting population / threshold arithmetic.

Usage: python3 -I check_c5.py
"""
import gzip, hashlib, json, os, re, sys

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
REPO = ROOT
EXP = REPO + '/experiments'
HERE = os.path.dirname(os.path.abspath(__file__))

BAL_JSON = EXP + '/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
RES_JSON = EXP + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
BAL_BASE_LEAN = HERE + '/extract_balbase/Catalog.lean'          # from omission-balanced-lean-2026-10-09/sources.tar.gz
BAL_CUTS_LEAN = EXP + '/omission-cover-certificates-2026-10-10/BalancedCoverCutsV2.lean'
RES_LEAN = EXP + '/omission-residual32-bridge2650-2026-10-11/Residual32Bridge2650/Catalog.lean'
BAL_STATES_LEAN = REPO + '/ErdosSzekeres/Omission/BalancedCatalogData.lean'
RES_STATES_LEAN = REPO + '/ErdosSzekeres/Omission/ResidualCatalogData.lean'
WIT = TOP + '/witnesses.json'

failures = []


def need(cond, msg):
    print(('  ok   ' if cond else '  FAIL ') + msg)
    if not cond:
        failures.append(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- parsing helpers
def parse_int_set(txt):
    txt = txt.strip()
    if txt in ('', '∅'):
        return frozenset()
    parts = [p.strip() for p in txt.split(',')]
    vals = [int(p) for p in parts]
    return vals


def parse_packed_catalog(path, nstates):
    """Parse `def rowsN : Array (Finset (Fin k) × ℕ × ℕ) := #[ ({..}, d, code), ... ]` blocks and
    the `def rowChunks := #[rows0, ...]` order.  Returns list of (list_of_indices, demand)."""
    src = open(path, encoding='utf-8').read()
    blocks = {}
    for m in re.finditer(r'def (rows\d+) : Array \(Finset \(Fin (\d+)\) × ℕ × ℕ\) := #\[(.*?)\n\]', src, re.S):
        name, k, body = m.group(1), int(m.group(2)), m.group(3)
        assert k == nstates, (path, name, k)
        rows = []
        for t in re.finditer(r'\(\{([0-9, ]*)\}, (\d+), (\d+)\)', body):
            rows.append((parse_int_set(t.group(1)), int(t.group(2))))
        # sanity: number of tuples equals number of top-level entries
        n_entries = len(re.findall(r'^\s*\(', body, re.M))
        assert n_entries == len(rows), (path, name, n_entries, len(rows))
        blocks[name] = rows
    order = re.search(r'def rowChunks := #\[([^\]]*)\]', src).group(1)
    order = [x.strip() for x in order.split(',')]
    out = []
    for nm in order:
        out.extend(blocks[nm])
    return out, src


def parse_states(path):
    src = open(path, encoding='utf-8').read()
    m = re.search(r'def catalog : List \(List Nat\) := \[(.*)\]\s*\n', src, re.S)
    body = m.group(1)
    return [list(map(int, t.split(','))) for t in re.findall(r'\[([0-9,]+)\]', body)]


def parse_cuts(path):
    src = open(path, encoding='utf-8').read()
    sup = {}
    for m in re.finditer(r'^def support(\d+) : Finset \(Fin 252\) := \{([0-9, ]*)\}\s*$', src, re.M):
        sup[int(m.group(1))] = parse_int_set(m.group(2))
    order = re.search(r'^def support : Fin 446 → Finset \(Fin 252\) := !\[(.*)\]\s*$', src, re.M).group(1)
    order = [int(x.strip()[len('support'):]) for x in order.split(',')]
    dem = re.search(r'^def demand : Fin 446 → ℕ := !\[(.*)\]\s*$', src, re.M).group(1)
    dem = [int(x) for x in dem.split(',')]
    # each theorem cutK concludes `D ≤ ∑ i ∈ supportK, holes i`
    thm = {}
    for m in re.finditer(r'theorem cut(\d+) \(holes.*?\n\s+(\d+) ≤ ∑ i ∈ support(\d+), holes i := by', src, re.S):
        k, d, k2 = int(m.group(1)), int(m.group(2)), int(m.group(3))
        assert k == k2, (k, k2)
        thm[k] = d
    return sup, order, dem, thm


# ---------------------------------------------------------------- 1. hashes
print('[1] catalog hashes')
bal_raw = open(BAL_JSON, 'rb').read()
res_raw = gzip.decompress(open(RES_JSON, 'rb').read())
need(sha(bal_raw) == 'acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72',
     'balanced-v2-source.json sha256 = acaf6323... (311 export.json source_sha256)')
need(sha(res_raw) == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6',
     'source-2650.json (decompressed) sha256 = e800d5f8... (313 final-report / export)')
exp311 = json.load(open(EXP + '/omission-final311-2026-10-14/certificate/export.json'))
need(exp311['source_sha256'] == sha(bal_raw) and exp311['rows'] == 3131 and exp311['budget'] == 63,
     '311 export manifest binds this exact balanced source (3131 rows, budget 63)')
rep313 = json.load(open(EXP + '/omission-final313-2026-10-11/final-report.json'))
need(rep313['certificate_inputs']['source-2650.json'] == sha(res_raw), '313 final-report binds this exact residual source')
need(sha(open(BAL_BASE_LEAN, 'rb').read()) == '17080b3c93264fcffd6b5b075ec00c2e713a01914290e3d11e53e516b648583c',
     'extracted base Catalog.lean sha256 = 17080b3c... (recorded as BalancedProof/Catalog.lean)')
resl_src = open(RES_LEAN, encoding='utf-8').read()
need('source SHA-256: e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6' in resl_src,
     'Residual32Bridge2650/Catalog.lean header names the same source hash')

bal = json.loads(bal_raw)
res = json.loads(res_raw)

# ---------------------------------------------------------------- 2. Lean literal catalogs
print('[2] parse Lean literal catalogs')
bstates = parse_states(BAL_STATES_LEAN)
rstates = parse_states(RES_STATES_LEAN)
need(len(bstates) == 252 and len(set(map(tuple, bstates))) == 252, 'Lean balanced catalog: 252 distinct profiles')
need(len(rstates) == 154 and len(set(map(tuple, rstates))) == 154, 'Lean residual catalog: 154 distinct profiles')
need(bstates == bal['states'], 'JSON balanced states == Lean balanced catalog order')
need(rstates == res['states'], 'JSON residual states == Lean residual catalog order')

base_rows, _ = parse_packed_catalog(BAL_BASE_LEAN, 252)
res_rows, _ = parse_packed_catalog(RES_LEAN, 154)
need(len(base_rows) == 2685, f'Lean base balanced rows parsed: {len(base_rows)}')
need(len(res_rows) == 2650, f'Lean residual rows parsed: {len(res_rows)}')
csup, corder, cdem, cthm = parse_cuts(BAL_CUTS_LEAN)
need(len(csup) == 446 and corder == list(range(446)) and len(cdem) == 446, 'Lean cut rows: 446 supports, order 0..445, 446 demands')
need(len(cthm) == 446 and all(cthm[k] == cdem[k] for k in range(446)), 'each cutK theorem demand equals demand[K]')
cut_rows = [(csup[k], cdem[k]) for k in range(446)]
lean_bal_rows = base_rows + cut_rows

# duplicates inside literal Finsets would be collapsed by Lean; record whether any occur
dup = sum(1 for s, _ in lean_bal_rows + res_rows if len(set(s)) != len(s))
need(dup == 0, f'no repeated index inside any literal support ({dup} found)')
rng = all(0 <= i < 252 for s, _ in lean_bal_rows for i in s) and all(0 <= i < 154 for s, _ in res_rows for i in s)
need(rng, 'all literal support indices in range')

# ---------------------------------------------------------------- 3. JSON vs Lean
print('[3] JSON rows vs Lean literal rows')
META = {'kind', 'derivation_row', 'ordered_template_map', 'provenance_path', 'provenance_sha256'}
ok_keys = all({'support', 'rhs'} <= set(c) and set(c) - {'support', 'rhs'} <= META
              for c in bal['constraints'] + res['constraints'])
need(ok_keys, 'every JSON constraint = {support, rhs} plus metadata only (kind/provenance; no coefficients or weights)')
jb = [(sorted(c['support']), int(c['rhs'])) for c in bal['constraints']]
jr = [(sorted(c['support']), int(c['rhs'])) for c in res['constraints']]
lb = [(sorted(set(s)), d) for s, d in lean_bal_rows]
lr = [(sorted(set(s)), d) for s, d in res_rows]
need(jb == lb, 'JSON balanced 3131 rows == Lean base(2685)+cuts(446), row by row, same order')
need(jr == lr, 'JSON residual 2650 rows == Lean Residual32Bridge2650 rows, row by row, same order')

# ---------------------------------------------------------------- 4. witnesses
print('[4] witnesses')
W = json.load(open(WIT))
hb = W['balanced_v2_72_hole_witness']
hrs = W['residual_2650_33_hole_witnesses_state0_occupied']


def check(rows, n, holes, label):
    H = set(holes)
    need(len(H) == len(holes) and all(isinstance(i, int) and 0 <= i < n for i in holes),
         f'{label}: {len(holes)} distinct in-range holes')
    # explicit indicator vector, exact sums (mirrors the Lean statement d_r <= sum_{i in S_r} h_i)
    h = [1 if i in H else 0 for i in range(n)]
    viol = [r for r, (s, d) in enumerate(rows) if not (d <= sum(h[i] for i in set(s)))]
    tight = sum(1 for (s, d) in rows if sum(h[i] for i in set(s)) == d)
    need(not viol, f'{label}: all {len(rows)} rows satisfied (violations {len(viol)}, tight {tight})')
    return h


h_b = check(lean_bal_rows, 252, hb, 'balanced witness vs Lean rows')
need(sum(h_b) == 72, f'balanced witness hole count = {sum(h_b)}')
check([(c['support'], c['rhs']) for c in bal['constraints']], 252, hb, 'balanced witness vs JSON rows')
# also the 2,685 geometric (base) rows alone, as stated in OmissionBalanced.ExcludesHoleBudget
check(base_rows, 252, hb, 'balanced witness vs base 2685 rows')

h_rs = []
for k, hr in enumerate(hrs):
    h_r = check(res_rows, 154, hr, f'residual witness {k} vs Lean rows')
    check([(c['support'], c['rhs']) for c in res['constraints']], 154, hr, f'residual witness {k} vs JSON rows')
    need(sum(h_r) == 33, f'residual witness {k} hole count = {sum(h_r)}')
    h_rs.append(h_r)
need(len({tuple(x) for x in h_rs}) == 3, 'the three residual witnesses are pairwise distinct')

# ---------------------------------------------------------------- 5. P1, P1', state 0
print('[5] P1 / P1\' / state-0 occupancy in profile terms')
bidx = {tuple(p): i for i, p in enumerate(bstates)}
ridx = {tuple(p): i for i, p in enumerate(rstates)}
e0 = bidx[(0, 0, 0, 0, 0)]; e1 = bidx[(1, 0, 0, 0, 0)]; e2 = bidx[(1, 1, 0, 0, 0)]; e3 = bidx[(2, 0, 0, 0, 0)]
print(f'  balanced indices: empty={e0}, [1]={e1}, [1,1]={e2}, [2]={e3}')
need(h_b[e0] == 0 and h_b[e1] == 0 and h_b[e2] + h_b[e3] <= 1, 'balanced witness satisfies P1 (a),(b),(c)')
z = ridx[(0, 0, 0, 0, 0)]
rowconv = [ridx[(1, 0, 0, 0, 0)], ridx[(1, 1, 0, 0, 0)], ridx[(1, 1, 1, 0, 0)], ridx[(1, 1, 1, 1, 0)]]
colconv = [ridx[(1, 0, 0, 0, 0)], ridx[(2, 0, 0, 0, 0)], ridx[(3, 0, 0, 0, 0)], ridx[(4, 0, 0, 0, 0)]]
print(f'  residual indices: empty={z}, P1\' set (columns = 1st coord)={rowconv}, transposed convention={colconv}')
for k, h_r in enumerate(h_rs):
    need(h_r[z] == 0, f'residual witness {k}: state 0 (empty profile) occupied')
    need(sum(h_r[i] for i in rowconv) <= 3, f'residual witness {k}: P1\' holds (one of {rowconv} occupied)')
    need(sum(h_r[i] for i in colconv) <= 3, f'residual witness {k}: transposed-convention P1\' also holds')
# smallest hole indices (all earlier states occupied)
print('  min balanced hole:', min(hb), ' min residual holes:', [min(x) for x in hrs])

# ---------------------------------------------------------------- 6. arithmetic
print('[6] arithmetic consequences')
nB, nR = 252 - sum(h_b), 154 - sum(h_rs[0])
print(f'  n_B = {nB}, n_R = {nR}, 1 + n_B + n_R = {1 + nB + nR}, forcing threshold B+R+2 = {nB + nR + 2}')
need((nB, nR, 1 + nB + nR, nB + nR + 2) == (180, 121, 302, 303), 'n_B=180, n_R=121, |S|=302 consistent, ES(8)<=303 best')
# Lean bound formulas: BalancedBound (251 - b) from ExcludesHoleBudget b; ResidualBound (153 - b)
need(251 - 71 == 180 and 153 - 32 == 121, 'best provable budgets: balanced b<=71 -> 180, residual b<=32 -> 121')

print()
print('RESULT:', 'ALL CHECKS PASSED' if not failures else f'{len(failures)} FAILURE(S)')
sys.exit(0 if not failures else 1)
