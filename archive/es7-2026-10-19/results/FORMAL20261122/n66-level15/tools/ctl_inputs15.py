"""Control inputs for `n66print15 full` (untrusted conversion, control only): the activated quadruples of one leaf's
level-15 state file `<state>_L15.json` (cert.json `state` with `_L15`; the order p2_write.py writes them) and
mono/rows_1832.json as text (sorted supports, d = 1, file order). Also reports whether that activated set is the
tau-closure of the warm file p2/s15/q.json (informational). usage: ctl_inputs15.py LEAFINDEX OUTDIR"""
import json, sys
W = '/home/jay/research/data/n66-20261113'
D = '/home/jay/research/data/formalize-20261122/n66-level15'
i, out = int(sys.argv[1]), sys.argv[2]
order = [l.strip() for l in open(f'{D}/tools/leaf_order15.txt') if l.strip()]
cid = order[i]
c = json.load(open(f'{W}/p2/c15/campaign_status.json'))['cubes'][cid]
cd = f'{W}/' + c['certdir']
cj = json.load(open(f'{cd}/cert.json'))
stp = cj['state'].replace('.json', '_L15.json')
st = json.load(open(stp))
assert st['L'] == 15 and st['cube'] == c['lits'] and st['certdir'].rstrip('/').endswith(c['certdir']), (st['certdir'], c['certdir'])
act = [tuple(q) for q in st['activated']]
assert len(set(act)) == len(act) == cj['activated_quadruples'] == 683670
open(f'{out}/act_{i}.txt', 'w').write(''.join('%d %d %d %d\n' % q for q in act))
R = json.load(open(f'{W}/mono/rows_1832.json'))
rows = [sorted(s) for s, d in R if d == 1]
open(f'{out}/rows1832.txt', 'w').write(''.join(' '.join(map(str, s)) + '\n' for s in rows))
lay = json.load(open(f'{cd}/layout.json'))
# tau-closure of q.json, with TAU as in p2_batch_cube.py over etv_common.profiles() for A = B = 4 (recomputed here,
# so that nothing from W is imported: importing etv_common may write its table cache into W)
import itertools
STATES = sorted((f for f in itertools.product(range(5), repeat=4) if all(f[k] >= f[k + 1] for k in range(3))), key=lambda f: (sum(f), f))
assert len(STATES) == 70
cellidx = {frozenset((x + 1, y) for x in range(4) for y in range(1, f[x] + 1)): k for k, f in enumerate(STATES)}
TAU = [cellidx[frozenset((b, x) for x, b in cc)] for cc in (frozenset((x + 1, y) for x in range(4) for y in range(1, f[x] + 1)) for f in STATES)]
q = {tuple(int(x) for x in t) for t in json.load(open(f'{W}/p2/s15/q.json'))['activated']}
qt = q | {tuple(TAU[x] for x in t) for t in q}
print(json.dumps({'leaf': i, 'cube': cid, 'state_file': stp, 'activated': len(act), 'sorted': act == sorted(act),
                  'layout_activated': lay['activated_quadruples'], 'rows': len(rows), 'rows_equal_layout': rows == lay['row_list'],
                  'q_json': len(q), 'q_tau_closure': len(qt), 'act_eq_q_tau_closure': set(act) == qt,
                  'cnf_sha256': lay['cnf_sha256'], 'cert_full_cnf_sha256': cj['full_cnf_sha256']}))
