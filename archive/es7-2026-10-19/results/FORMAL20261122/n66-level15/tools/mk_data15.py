"""Level-15 data for the Lean encoder (UNTRUSTED conversion; soundness never depends on it: the cover theorem holds
for every split tree, the printer prints only clauses of fullCnf R0_15 c, and M9 binds the printed bytes).

Writes, from p2/c15/campaign_status.json (sha256 pinned) and the 105 certified leaves:
  lean/N66E15/data/tree15.txt   the split tree as a Lean term (base levels 25,12,16,29,17,37, then the re-splits;
                                children (occupied, hole) in that order; asserted against `children`/`lits`)
  tools/leaf_order15.txt        leaf index (DFS order, occupied child first) -> cube id
  lean/N66E15/data/rows_used15.txt   R0_15: the distinct row supports of the 105 trims, in mono/rows_1832.json
                                order (from used_ids.txt + layout.json ranges/row_list; checked = union of the
                                105 used_rows.json files)
usage: python3 -I mk_data15.py"""
import hashlib, json, sys
W = '/home/jay/research/data/n66-20261113'
D = '/home/jay/research/data/formalize-20261122/n66-level15'
CS = f'{W}/p2/c15/campaign_status.json'
assert hashlib.sha256(open(CS, 'rb').read()).hexdigest() == '4802dc9a946cefa3b855b8c495becc0fb33491a89e5472c9722ccb9d0c8138f5'
st = json.load(open(CS))
cubes = st['cubes']
assert st['final'] is True and st['cover']['leaves'] == 105 and st['cover']['certified_cover_ok'] is True
BASE = [25, 12, 16, 29, 17, 37]
bylits = {}
for cid, c in cubes.items():
    key = tuple(map(tuple, c['lits']))
    assert key not in bylits, cid
    bylits[key] = cid
leaves, used = [], set()

def build(pre):
    """Lean term of the subtree at literal prefix `pre`."""
    cid = bylits.get(tuple(pre))
    if cid is None:
        assert len(pre) < 6, pre                       # only the 6 base levels may be implicit
        s = BASE[len(pre)]
        assert not any(x[0] == s for x in pre)
        return f'(.node {s} {build(pre + [(s, 1)])} {build(pre + [(s, 0)])})'
    c = cubes[cid]; used.add(cid)
    assert len(pre) >= 6 and [list(x) for x in pre] == c['lits'], cid
    if c['status'] == 'certified':
        leaves.append(cid)
        return '.leaf'
    assert c['status'] == 'split', (cid, c['status'])
    s = c['split_on']
    assert not any(x[0] == s for x in pre)
    co, ch = c['children']
    assert cubes[co]['lits'] == c['lits'] + [[s, 1]] and cubes[ch]['lits'] == c['lits'] + [[s, 0]], cid
    return f'(.node {s} {build(pre + [(s, 1)])} {build(pre + [(s, 0)])})'

term = build([])
assert used == set(cubes), set(cubes) - used                # every campaign cube is a node of the tree
assert len(leaves) == 105 and len(set(leaves)) == 105
assert sorted(leaves) == sorted(k for k, c in cubes.items() if c['status'] == 'certified')
open(f'{D}/lean/N66E15/data/tree15.txt', 'w').write(term + '\n')
open(f'{D}/tools/leaf_order15.txt', 'w').write(''.join(x + '\n' for x in leaves))

# R0_15
R = json.load(open(f'{W}/mono/rows_1832.json'))
rows = [sorted(s) for s, d in R if d == 1]
assert len(rows) == len(R) == 15648
used_rows, used_rows_json = set(), set()
for cid in leaves:
    c = cubes[cid]; cd = f'{W}/' + c['certdir']
    lay = json.load(open(f'{cd}/layout.json'))
    assert lay['L'] == 15 and lay['W'] == list(range(70)) and lay['rows_file'] == 'mono/rows_1832.json', cid
    assert lay['row_list'] == rows, cid                 # every leaf writes the same 15,648 rows in file order
    assert lay['cube'] == c['lits'], cid
    r0, r1 = lay['rows']
    ids = [int(l) for l in open(f'{cd}/used_ids.txt') if l.strip()]
    for i in ids:
        if r0 <= i <= r1: used_rows.add(tuple(rows[i - r0]))
    try:
        for s, d in json.load(open(f'{cd}/used_rows.json')):
            assert d == 1; used_rows_json.add(tuple(sorted(s)))
    except FileNotFoundError:
        pass                                            # UP-refuted leaves use no row
assert used_rows == used_rows_json, (len(used_rows), len(used_rows_json))
R0 = [r for r in rows if tuple(r) in used_rows]
assert len(R0) == len(used_rows) and len(set(map(tuple, R0))) == len(R0)
txt = ''.join(' '.join(map(str, r)) + '\n' for r in R0)
open(f'{D}/lean/N66E15/data/rows_used15.txt', 'w').write(txt)
print(json.dumps({'leaves': len(leaves), 'cubes': len(cubes), 'R0_15': len(R0),
                  'rows_used15_sha256': hashlib.sha256(txt.encode()).hexdigest(),
                  'tree15_sha256': hashlib.sha256((term + '\n').encode()).hexdigest()}))
