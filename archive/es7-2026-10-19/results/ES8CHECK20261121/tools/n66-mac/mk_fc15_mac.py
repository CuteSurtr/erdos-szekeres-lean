"""mk_fc15_mac.py (n66-mac, 21 Nov 2026): rebuild the level-15 base CNF F_c on the Mac from the transferred Linux inputs and
compare it with the recorded hash (VERIFY_N66CUBES15.md section 3: 1,647,847 variables, 9,710,978 clauses, SHA-256 2f78368f...).
F_c = p2_write.py output for the state p2_batch_cube.py saves for a cube, with cube = []: activated = sorted(q.json + tau images)
(the --tauclose code of p2_batch_cube.py), L 15, rows file mono/rows_1832.json, sb_pairs = p2_sb.default_pairs() (mono/freq.json).
Run inside the Mac work dir with ETV_A=4 ETV_B=4.  usage: mk_fc15_mac.py <outdir> [expected sha256]"""
import json, os, sys, subprocess, itertools
sys.path.insert(0, os.getcwd())          # the campaign tools live in the work dir (run from there)
import etv_common as ec, lazymono, p2_sb
assert ec.A == 4 and ec.B == 4 and ec.N == 70
od = sys.argv[1]; want = sys.argv[2] if len(sys.argv) > 2 else '2f78368f5e00ba52dc04104bbfb66289212d3dbf05d1aa3e0c798a814c4fee29'
cellidx = {frozenset((x + 1, y) for x in range(4) for y in range(1, f[x] + 1)): i for i, f in enumerate(ec.STATES)}
TAU = [cellidx[frozenset((b, x) for x, b in c)] for c in (frozenset((x + 1, y) for x in range(4) for y in range(1, f[x] + 1)) for f in ec.STATES)]
E = lazymono.LazyMono(list(range(ec.N)), emit=lambda c: None); del E.cnf
def okquad(q): return len(set(q)) == 4 and all(E.can[x][y] for x, y in itertools.combinations(q, 2))
act = set()
for q in json.load(open('p2/s15/q.json'))['activated']:
    q = tuple(int(x) for x in q); assert okquad(q); act.add(q)
n_warm = len(act)
for q in list(act): act.add(tuple(TAU[x] for x in q))
os.makedirs(od, exist_ok=True)
st = {'W': list(range(ec.N)), 'L': 15, 'status': 'F_c rebuild (mk_fc15_mac.py)', 'rows_file': 'mono/rows_1832.json', 'cube': [],
      'activated': sorted(act), 'sb_pairs': p2_sb.default_pairs()}
sp = os.path.join(od, 'fc_state.json'); json.dump(st, open(sp, 'w'))
r = subprocess.run([sys.executable, '-u', 'p2_write.py', sp, od, 'keep'], capture_output=True, text=True)
if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
lay = json.load(open(os.path.join(od, 'layout.json')))
res = {'warm_quads': n_warm, 'tau_closed_quads': len(act), 'vars': lay['vars'], 'clauses': lay['clauses'], 'card_top': lay['card_top'],
       'sb_pairs_first4': lay['sb_pairs'][:4], 'cnf_sha256': lay['cnf_sha256'], 'expected': want, 'FC_MATCH': lay['cnf_sha256'] == want,
       'expected_counts_match': (len(act), lay['vars'], lay['clauses'], lay['card_top']) == (683670, 1647847, 9710978, 1647821)}
print(json.dumps(res)); json.dump(res, open(os.path.join(od, 'fc_check.json'), 'w'), indent=1)
sys.exit(0 if res['FC_MATCH'] else 3)
