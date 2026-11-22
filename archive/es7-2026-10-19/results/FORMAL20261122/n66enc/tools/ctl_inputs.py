"""Control inputs for `n66print full` (untrusted conversion): the activated quadruples of one cube's state file
(in the order p2_write.py writes them) and mono/rows_1832.json as text (sorted supports, d = 1, file order)."""
import json, sys, hashlib
W = '/home/jay/research/data/n66-20261113'
cube, out = sys.argv[1], sys.argv[2]
st = json.load(open(f'{W}/p2/c14/{cube}_L14.json'))
act = [tuple(q) for q in st['activated']]
assert len(set(act)) == len(act)
open(f'{out}/act_{cube}.txt', 'w').write(''.join('%d %d %d %d\n' % q for q in act))
R = json.load(open(f'{W}/mono/rows_1832.json'))
rows = [sorted(s) for s, d in R if d == 1]
open(f'{out}/rows1832.txt', 'w').write(''.join(' '.join(map(str, s)) + '\n' for s in rows))
lay = json.load(open(f'{W}/p2/c14/{cube}/it1/layout.json'))
print(json.dumps({'cube': cube, 'activated': len(act), 'layout_activated': lay['activated_quadruples'],
                  'rows': len(rows), 'layout_rows': len(lay['row_list']), 'rows_equal': rows == lay['row_list'],
                  'state_cube': st['cube'], 'layout_cube': lay['cube'], 'cnf_sha256': lay['cnf_sha256']}))
