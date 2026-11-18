"""Independent re-verification of a justification file for the (4,4) catalog (no search).  For every row:
  cycle      : the stored list order passes the six-order test on all triples (table recomputed, cache bypassed);
  core       : core_certs.jsonl has 's VERIFIED UNSAT' for that support;
  transported: sigma is injective with image = the row, every test of the template holds for sigma, and the
               template's CNF is 's VERIFIED UNSAT' in template_certs.jsonl;
  mirror     : the row is the image under tau (state transposition, recomputed here from the profiles) of a
               support whose own justification ('of': core or transported) is verified as above.
Also checks that the justified (support, demand) multiset equals the rows file, that the catalog is the 4x4 one
(70 states), and that the two fixed states are the empty diagram and the single cell.
usage: final_verify66.py <dir containing justification.json, template_certs.jsonl, core_certs.jsonl>"""
import json, sys, os, hashlib, collections
import numpy as np
import etv_common as ec
d = sys.argv[1]
assert ec.A == 4 and ec.B == 4 and ec.N == 70
assert [ec.STATES[i] for i in ec.FIXED_OCC] == [(0, 0, 0, 0), (1, 0, 0, 0)]
TT = ec.triple_table(ec.DPLAIN)
assert (TT == ec.TT).all(), 'cached triple table differs from a fresh computation'
D = [[ec.dom_ref(s, t) for t in range(ec.N)] for s in range(ec.N)]
# tau recomputed independently of sym66: conjugate partition via cell sets
cellidx = {frozenset((a + 1, y) for a in range(4) for y in range(1, f[a] + 1)): i for i, f in enumerate(ec.STATES)}
TAU = [cellidx[frozenset((b, a) for a, b in c)] for c in (frozenset((a + 1, y) for a in range(4) for y in range(1, f[a] + 1)) for f in ec.STATES)]
J = json.load(open(os.path.join(d, 'justification.json')))
rows = json.load(open(J['rows_file']))
assert hashlib.sha256(open(J['rows_file'], 'rb').read()).hexdigest() == J['rows_sha256']
T = {}
for l in open(os.path.join(d, 'template_certs.jsonl')):
    r = json.loads(l); T[r['id']] = (r['verdict'] == 's VERIFIED UNSAT', [tuple(x) for x in r['tests']], r['core'])
C = {}
for l in open(os.path.join(d, 'core_certs.jsonl')):
    r = json.loads(l); C[tuple(r['support'])] = r['verdict'] == 's VERIFIED UNSAT'
def good(t, sig):
    if t[0] == 'positive': return bool(TT[sig[t[1]], sig[t[2]], sig[t[3]]])
    if t[0] == 'empty': return not D[sig[t[1]]][sig[t[2]]]
    if t[0] == 'domain': return (t[3], t[4]) not in D[sig[t[1]]][sig[t[2]]]
    raise ValueError(t)
def ok_direct(j):
    S = j['support']; k = j['kind']
    if S != sorted(set(S)): return False
    if k == 'core': return j['demand'] == 1 and C.get(tuple(S), False)
    if k == 'transported':
        ok, tests, core = T[j['template']]; sig = j['sigma']
        return bool(ok and j['demand'] == 1 and len(set(sig)) == len(sig) and sorted(sig) == S and len(sig) == len(core)
                    and all(good(t, sig) for t in tests))
    return False
bad = []; cnt = collections.Counter()
for j in J['justifications']:
    S = j['support']; k = j['kind']; cnt[k] += 1
    if k == 'cycle':
        L = j['order']
        if sorted(L) != S or len(set(L)) != len(L) or j['demand'] != len(S) - 7 or not all(TT[L[a], L[b], L[c]] for a in range(len(L)) for b in range(a + 1, len(L)) for c in range(b + 1, len(L))): bad.append(j)
    elif k in ('core', 'transported'):
        if not ok_direct(j): bad.append(j)
    elif k == 'mirror':
        o = j['of']
        if j['demand'] != 1 or sorted(TAU[s] for s in o['support']) != S or o['kind'] not in ('core', 'transported') or not ok_direct(o): bad.append(j)
    else: bad.append(j)
want = collections.Counter((tuple(sorted(s)), dd) for s, dd in rows)
got = collections.Counter((tuple(j['support']), j['demand']) for j in J['justifications'])
print(json.dumps({'rows': len(rows), 'kinds': cnt, 'bad': len(bad), 'rows_match': want == got,
                  'templates_verified': sum(v[0] for v in T.values()), 'templates': len(T), 'cores_verified': sum(C.values()), 'cores': len(C)}))
