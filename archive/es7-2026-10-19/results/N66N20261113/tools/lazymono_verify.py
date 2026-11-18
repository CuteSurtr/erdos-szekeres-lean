"""Independent re-check of a lazymono certificate (no solver):
 1. regenerate the monolithic clause stream with mono66.generate (the generator whose families have the written
    soundness argument and the real-point-set control mono_check.py) for the state set W and check that every
    geometric clause of cert.cnf (as a set of literals) occurs in it;
 2. check the remaining clauses of cert.cnf: unit clauses sel_0, sel_1; row clauses = negated selectors of a listed
    row; the cardinality block = pysat CardEnc.atmost(seqcounter) over the 68 hole literals with bound L, re-encoded;
 3. recompute the SHA-256 of cert.cnf and compare with info.json; require cake_lpr's verdict in info.json.
usage: lazymono_verify.py <state.json> <certdir>"""
import sys, json, os, hashlib
import etv_common as ec, mono66
from pysat.card import CardEnc, EncType
st = json.load(open(sys.argv[1])); od = sys.argv[2]; info = json.load(open(os.path.join(od, 'info.json')))
W = st['W']; L = st['L']; idx = {s: i for i, s in enumerate(W)}
cnfp = os.path.join(od, 'cert.cnf')
h = hashlib.sha256()
with open(cnfp, 'rb') as g:
    for chunk in iter(lambda: g.read(1 << 24), b''): h.update(chunk)
ok_hash = h.hexdigest() == info['cnf_sha256']
n_geo = info['geometric_clauses']
want = {}
tail = []
with open(cnfp) as g:
    header = g.readline().split(); nv, nc = int(header[2]), int(header[3])
    for k, line in enumerate(g):
        lits = tuple(sorted(int(x) for x in line.split()[:-1]))
        if k < n_geo: want[hash(lits)] = want.get(hash(lits), 0) + 1
        else: tail.append(lits)
total_geo = sum(want.values())
found = set(); stream = [0]
sel_holder = {}
def emit(c, own):
    stream[0] += 1
    key = hash(tuple(sorted(list(c) + [-sel_holder['sel'][o] for o in own])))
    if key in want: found.add(key)
import coupled5
probe = coupled5.CNF(W, static=False); sel_holder['sel'] = [probe.nv + 1 + i for i in range(len(W))]; del probe
cnf, sel, top, C, U, CE, UE = mono66.generate(emit, S=W)
missing = len(set(want) - found)
# tail
exp = [tuple([sel[idx[s]]]) for s in ec.FIXED_OCC if s in idx] + [tuple([sel[idx[s_]] if bit else -sel[idx[s_]]]) for s_, bit in st.get('cube', [])]
rows_ok = True; nrows = info['row_clauses']
rowset = None
if nrows:
    rowset = set(tuple(sorted(-sel[idx[x]] for x in s)) for s, d in json.load(open(st['rows_file'])) if d == 1 and all(x in idx for x in s))
enc = CardEnc.atmost(lits=[-sel[i] for i in range(len(W)) if W[i] not in ec.FIXED_OCC], bound=L, top_id=top, encoding=EncType.seqcounter)
card = [tuple(sorted(c)) for c in enc.clauses]
t_units = tail[:len(exp)]; t_rows = tail[len(exp):len(exp) + nrows]; t_card = tail[len(exp) + nrows:]
units_ok = [tuple(sorted(u)) for u in exp] == t_units
rows_ok = all(r in rowset for r in t_rows) if nrows else True
card_ok = t_card == card
res = {'cnf_sha256_ok': ok_hash, 'geometric_clauses': total_geo, 'distinct': len(want), 'missing_from_mono66_stream': missing, 'mono66_stream_clauses': stream[0],
       'fixed_units_ok': units_ok, 'row_clauses': nrows, 'row_clauses_ok': rows_ok, 'cardinality_block_ok': card_ok, 'budget': L, 'cube': st.get('cube', []),
       'cake_lpr': info.get('cake_lpr'), 'ALL_OK': bool(ok_hash and missing == 0 and units_ok and rows_ok and card_ok and info.get('cake_lpr') == 's VERIFIED UNSAT')}
json.dump(res, open(os.path.join(od, 'verify.json'), 'w'), indent=1); print(json.dumps(res))
