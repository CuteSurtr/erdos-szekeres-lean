"""Phase 2 (20:35 KST): write the certificate CNF for a lazymono state and exit (no solver in this process).
Same clause stream as lazymono_cert.py:
  [1 .. n_eager]            eager clauses of lazymono.LazyMono(W)          (sub-CNF of mono66.generate)
  [.. n_geo]                the 12 clauses of every activated (quadruple, order), lazymono.quad_clauses
  units                     sel of the fixed states (etv_common.FIXED_OCC), then the cube units
  rows                      one clause (-sel of the support) per demand-one row of rows_file inside W (hints)
  card                      pysat CardEnc.atmost(seqcounter) over the hole literals (-sel of the non-fixed states), bound L
usage: p2_write.py <state.json> <outdir> [rows: keep|none] [L override]
writes outdir/cert.cnf and outdir/layout.json (ranges of the families, the row list in clause order, SHA-256)."""
import sys, json, os, time, hashlib
import etv_common as ec, lazymono
from pysat.card import CardEnc, EncType
assert ec.A == 4 and ec.B == 4 and ec.N == 70
st = json.load(open(sys.argv[1])); od = sys.argv[2]
userows = (sys.argv[3] if len(sys.argv) > 3 else 'keep') == 'keep'
L = int(sys.argv[4]) if len(sys.argv) > 4 else st['L']
os.makedirs(od, exist_ok=True)
W = st['W']; idx = {s: i for i, s in enumerate(W)}
t0 = time.time(); cnfp = os.path.join(od, 'cert.cnf'); body = cnfp + '.body'
nc = 0; buf = []
f = open(body, 'w')
def emit(c):
    global nc
    buf.append(' '.join(map(str, c)) + ' 0\n'); nc += 1
    if len(buf) >= 200000: f.write(''.join(buf)); buf.clear()
E = lazymono.LazyMono(W, emit=emit)
n_eager = nc
act = [tuple(q) for q in st['activated']]
assert len(set(act)) == len(act)
for q in act:
    for c in E.quad_clauses(*q): emit(c)
n_geo = nc
for s in ec.FIXED_OCC:
    if s in idx: emit([E.sel[idx[s]]])
cube = [list(x) for x in st.get('cube', [])]
for s_, bit in cube: emit([E.sel[idx[s_]] if bit else E.nsel[idx[s_]]])
n_units = nc
rows = []
if userows and st.get('rows_file', 'none') != 'none':
    rows = [sorted(s) for s, d in json.load(open(st['rows_file'])) if d == 1 and all(x in idx for x in s)]
for s in rows: emit([E.nsel[idx[x]] for x in s])
n_rows = nc
enc = CardEnc.atmost(lits=[E.nsel[i] for i in range(E.n) if W[i] not in ec.FIXED_OCC], bound=L, top_id=E.top, encoding=EncType.seqcounter)
for c in enc.clauses: emit(c)
top = max(E.top, enc.nv)
n_card = nc
sb_pairs = st.get('sb_pairs')
if sb_pairs:                      # lex-leader symmetry breaking for tau on the selectors (p2_sb.py, README 6.7)
    import p2_sb
    assert len(W) == ec.N
    sbc, top = p2_sb.sb_clauses({W[i]: E.sel[i] for i in range(E.n)}, sb_pairs, top)
    for c in sbc: emit(c)
f.write(''.join(buf)); f.close()
h = hashlib.sha256()
with open(cnfp, 'wb') as g:
    hd = f'p cnf {top} {nc}\n'.encode(); g.write(hd); h.update(hd)
    with open(body, 'rb') as b:
        while True:
            chunk = b.read(1 << 26)
            if not chunk: break
            g.write(chunk); h.update(chunk)
os.remove(body)
lay = {'state': os.path.abspath(sys.argv[1]), 'W': W, 'L': L, 'cube': cube, 'rows_file': st.get('rows_file', 'none') if userows else 'none',
       'vars': top, 'clauses': nc, 'eager': [1, n_eager], 'quad': [n_eager + 1, n_geo], 'units': [n_geo + 1, n_units],
       'rows': [n_units + 1, n_rows], 'card': [n_rows + 1, n_card], 'sb': [n_card + 1, nc], 'sb_pairs': sb_pairs or [],
       'card_top': max(E.top, enc.nv), 'sel': [E.sel[0], E.sel[-1]], 'mono_top': E.top,
       'activated_quadruples': len(act), 'row_list': rows, 'cnf_sha256': h.hexdigest(), 'cnf_bytes': os.path.getsize(cnfp),
       'write_seconds': round(time.time() - t0, 1)}
json.dump(lay, open(os.path.join(od, 'layout.json'), 'w'))
print(json.dumps({k: v for k, v in lay.items() if k not in ('W', 'row_list')}), flush=True)
