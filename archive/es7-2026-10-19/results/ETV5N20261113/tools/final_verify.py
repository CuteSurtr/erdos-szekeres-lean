"""Independent re-verification of a justification file (no search): for every row of the subset,
  cycle: the stored list order passes the six-order test on all triples (table recomputed, cache bypassed);
  core: core_certs.jsonl has 's VERIFIED UNSAT' for that support;
  transported: sigma is injective with image = the row, every test of the template holds for sigma, and the
               template's CNF is 's VERIFIED UNSAT' in template_certs.jsonl.
Also checks that the justified (support, demand) multiset equals the rows file.
usage: final_verify.py <dir containing justification.json, template_certs.jsonl, core_certs.jsonl>"""
import json, sys, os, hashlib, collections
import numpy as np
import etv_common as ec
d = sys.argv[1]
TT = ec.triple_table(ec.DPLAIN)
assert (TT == ec.TT).all(), 'cached triple table differs from a fresh computation'
D = [[ec.dom_ref(s, t) for t in range(ec.N)] for s in range(ec.N)]
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
bad = []; cnt = collections.Counter()
for j in J['justifications']:
    S = j['support']; k = j['kind']; cnt[k] += 1
    if k == 'cycle':
        L = j['order']
        if sorted(L) != S or j['demand'] != len(S) - 7 or not all(TT[L[a], L[b], L[c]] for a in range(len(L)) for b in range(a + 1, len(L)) for c in range(b + 1, len(L))): bad.append(j)
    elif k == 'block':
        import itertools
        okb = len(S) >= 23 and j['demand'] == len(S) - 22 and any(
            all(z[0] in K for a, b in itertools.permutations(S, 2) for z in D[a][b])
            for K in itertools.combinations(range(1, ec.A + 1), 2))
        if not okb: bad.append(j)
    elif k == 'core':
        if j['demand'] != 1 or not C.get(tuple(S), False): bad.append(j)
    elif k == 'transported':
        ok, tests, core = T[j['template']]; sig = j['sigma']
        if not ok or j['demand'] != 1 or len(set(sig)) != len(sig) or sorted(sig) != S or len(sig) != len(core) or not all(good(t, sig) for t in tests): bad.append(j)
    else: bad.append(j)
want = collections.Counter((tuple(sorted(s)), dd) for s, dd in rows)
got = collections.Counter((tuple(j['support']), j['demand']) for j in J['justifications'])
print(json.dumps({'rows': len(rows), 'kinds': cnt, 'bad': len(bad), 'rows_match': want == got,
                  'templates_verified': sum(v[0] for v in T.values()), 'templates': len(T), 'cores_verified': sum(C.values()), 'cores': len(C)}))
