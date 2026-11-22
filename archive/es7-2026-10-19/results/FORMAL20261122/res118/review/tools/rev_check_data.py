#!/usr/bin/env python3
"""Reviewer's own data check for res118-lean (independent of the worker's tools/*.py).

Read-only on every input. Writes one JSON report (argv[1]).
Checks, per slice: sha256 of the row file, the capacity rows (F, T) and (Lo, B - T) against F/Lo recomputed from
the source states, rhs == 1 for every other row, row well-formedness, the packet master's budget/source/extra
binding; the Lean literal blocks (parsed here from Rows.lean / LemmaA.lean by my own parser) against the JSON row
lists in file order; distinct-support counts; the nine L4 rows; pool812 = P.
"""
import gzip, hashlib, json, re, sys, tarfile, io
from pathlib import Path

W = Path('/home/jay/research/data/es308-20261114')
REPO = Path('/home/jay/research/lean/erdos-szekeres-lean')
LO33 = REPO / 'archive/es7-2026-10-19/results/LO33N20261113'
LEAN = Path('/home/jay/research/data/formalize-20261122/res118/lean/Res118')
RAW_SHA = 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'

def sha(b): return hashlib.sha256(b).hexdigest()

rep = {'ok': True, 'notes': []}
def need(cond, msg):
    if not cond:
        rep['ok'] = False
        rep['notes'].append('FAIL: ' + msg)
    return cond

# --- source catalog (two paths that trees name)
srcs = {}
for p in [W / 'inputs/source-2650.json.gz', REPO / 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz']:
    raw = gzip.decompress(p.read_bytes())
    srcs[str(p)] = sha(raw)
    need(sha(raw) == RAW_SHA, f'source raw sha {p}')
src = json.loads(gzip.decompress((W / 'inputs/source-2650.json.gz').read_bytes()))
states, cons = src['states'], src['constraints']
need(len(states) == 154 and len(cons) == 2650, 'source sizes')
F = [i for i, s in enumerate(states) if s[0] >= 5]
LO = [i for i, s in enumerate(states) if s[0] <= 4]
need(len(F) == 84 and len(LO) == 70 and sorted(F + LO) == list(range(154)), 'F/Lo partition')
need(states[0] == [0, 0, 0, 0, 0], 'state 0 profile')
rep['source_raw_sha256'] = srcs

# --- my own parser for the Lean literal data
def lean_lists(text, name):
    """Return the List (List Nat) literal of every `def <name>_NN` chunk, concatenated in the order of the
    `def <name> := a ++ b ++ ...` line."""
    defs = {}
    for m in re.finditer(r'def (\w+) : List \(List Nat\) := \[(.*?)\n\]', text, re.S):
        body = m.group(2)
        rows = [[int(x) for x in re.findall(r'\d+', r)] for r in re.findall(r'\[([^\[\]]*)\]', body)]
        defs[m.group(1)] = rows
    m = re.search(rf'def {name} : List \(List Nat\) := ([\w ]+(?:\+\+[\w ]+)*)\n', text)
    parts = [x.strip() for x in m.group(1).split('++')]
    out = []
    for q in parts:
        out += defs[q]
    return out, parts

rows_text = (LEAN / 'Rows.lean').read_text()
blocks = {}
for b in ['rowsP', 'rowsQ', 'rowsU', 'rowsA']:
    blocks[b], parts = lean_lists(rows_text, b)
rep['lean_block_sizes'] = {b: len(v) for b, v in blocks.items()}
need([len(blocks[b]) for b in ['rowsP', 'rowsQ', 'rowsU', 'rowsA']] == [812, 208, 35, 970], 'block sizes')

lemma_text = (LEAN / 'LemmaA.lean').read_text()
def lean_nat_list(name):
    m = re.search(rf'def {name} : List ℕ := \[(.*?)\]', lemma_text, re.S)
    return [int(x) for x in re.findall(r'\d+', m.group(1))]
fI, loI = lean_nat_list('fIndices'), lean_nat_list('loIndices')
need(fI == F, 'fIndices == F (JSON states s[0] >= 5)')
need(loI == LO, 'loIndices == Lo (JSON states s[0] <= 4)')

P, Q, U, A = blocks['rowsP'], blocks['rowsQ'], blocks['rowsU'], blocks['rowsA']
slices = [
    # name, B, T, extra file, expected unit-row list, packet
    ('b33s18', 33, 18, LO33 / 'data/cert_66_55_leanrows/extra_66_55_leanrows.json', [], 'tar'),
    ('b34s18', 34, 18, W / 'inputs/s18-v13/extra.json', P + Q, W / 'runs/s18/bb'),
    ('b34s19', 34, 19, W / 'inputs/s19/extra.json', P, W / 'runs/s19/bb'),
    ('b35s18', 35, 18, W / 'inputs/b35s18-v13/extra.json', P + Q, W / 'runs/b35s18/bb'),
    ('b35s19', 35, 19, W / 'inputs/b35s19-v16/extra.json', P + Q + U, W / 'runs/b35s19/bb'),
    ('b35s20', 35, 20, W / 'inputs/b35s20-v169/extra.json', P + Q + A, W / 'runs/b35s20/bb-s1'),
]
rep['slices'] = {}
for name, B, T, xp, expect, pk in slices:
    xb = xp.read_bytes()
    ex = json.loads(xb)
    r = {'extra': str(xp), 'extra_sha256': sha(xb), 'rows_total': 2650 + len(ex)}
    need(ex[0] == {'support': F, 'rhs': T}, f'{name}: row 2650 == (F, {T})')
    need(ex[1] == {'support': LO, 'rhs': B - T}, f'{name}: row 2651 == (Lo, {B - T})')
    units = ex[2:]
    need(all(set(u) == {'support', 'rhs'} for u in ex), f'{name}: row keys')
    need(all(u['rhs'] == 1 for u in units), f'{name}: every unit row has rhs 1')
    need(all(isinstance(u['support'], list) and len(u['support']) >= 2 and u['support'] == sorted(set(u['support']))
             and all(type(i) is int and 0 <= i < 154 for i in u['support']) for u in units),
         f'{name}: unit rows sorted, distinct, in range, size >= 2')
    need([u['support'] for u in units] == expect, f'{name}: unit rows == Lean block concatenation in file order')
    r['unit_rows'] = len(units)
    r['min_support'] = min((len(u['support']) for u in units), default=None)
    r['units_containing_state0'] = sum(1 for u in units if 0 in u['support'])
    # the packet master
    if pk == 'tar':
        tb = (LO33 / 'data/cert_66_55_leanrows/contexts_66_55_leanrows.tar').read_bytes()
        r['tar_sha256'] = sha(tb)
        with tarfile.open(fileobj=io.BytesIO(tb)) as t:
            m = json.load(t.extractfile('master.json'))
            names = t.getnames()
        r['tar_members'] = len(names)
        mx = Path(m['extra'])
        msrc = Path(m['source']) if Path(m['source']).is_absolute() else REPO / m['source']
    else:
        mb = (pk / 'master.json').read_bytes()
        m = json.loads(mb)
        r['master_sha256'] = sha(mb)
        mx, msrc = Path(m['extra']), Path(m['source'])
    need(m['budget'] == B and type(m['budget']) is int, f'{name}: master budget == {B}')
    need(mx.exists() and sha(mx.read_bytes()) == sha(xb), f'{name}: master extra file has the row file hash')
    need(sha(gzip.decompress(msrc.read_bytes())) == RAW_SHA, f'{name}: master source raw hash')
    need(m['root'] == 0 and m['nodes'][0]['type'] == 'branch' and m['nodes'][0]['vertex'] != 0,
         f'{name}: master root does not branch on state 0 (state 0 fixed by the replay envelope)')
    r['master_budget'], r['master_extra'], r['master_source'] = m['budget'], str(mx), str(msrc)
    r['master_contexts'] = m['contexts']
    rep['slices'][name] = r

# --- distinct supports and nesting
allrows = P + Q + U + A
rep['block_rows'] = len(allrows)
rep['distinct_supports'] = len({tuple(x) for x in allrows})
rep['U_cap_A'] = len({tuple(x) for x in U} & {tuple(x) for x in A})
rep['dups_within_blocks'] = {b: len(v) - len({tuple(x) for x in v}) for b, v in blocks.items()}
basesets = {tuple(c['support']) for c in cons}
rep['extra_equal_to_base_support'] = sum(1 for x in {tuple(x) for x in allrows} if x in basesets)

# --- pool812 == P
pb = (W / 'inputs/pool812.json').read_bytes()
pool = json.loads(pb)
rep['pool812_sha256'] = sha(pb)
need([p['support'] for p in pool] == P and all(p['rhs'] == 1 for p in pool), 'pool812 == P in order, rhs 1')

# --- the nine L4 rows
nine = [973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315]
cov = [0] * 154
for r in nine:
    need(cons[r]['rhs'] == 6 and set(cons[r]['support']) <= set(F), f'L4 row {r}: demand 6, inside F')
    for i in cons[r]['support']:
        cov[i] += 1
need(all(cov[i] == (3 if i in F else 0) for i in range(154)), 'L4: F covered 3 times, Lo 0 times')

print(json.dumps(rep, indent=1))
Path(sys.argv[1]).write_text(json.dumps(rep, indent=1) + '\n')
