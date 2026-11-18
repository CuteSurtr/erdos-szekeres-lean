"""Certificate for a lazymono result "no model with at most L holes".
Writes the sub-CNF  = eager clauses + the 12 clauses of every activated (quadruple, order) + fixed-state units
                      + optional row clauses over the selectors (hints, each to be justified separately)
                      + "at most L holes" (pysat CardEnc seqcounter, as mono66.tail_clauses),
runs CaDiCaL 2.1.3 with LRAT, checks the proof with cake_lpr, and traces which row clauses the proof uses.
usage: lazymono_cert.py <state.json> <outdir> [rows: keep|none] [cadical extra option, e.g. --plain]
Output: outdir/cert.cnf (kept), outdir/info.json, outdir/used_rows.json ([[support, 1], ...])."""
import sys, json, os, time, hashlib, subprocess
import etv_common as ec, lazymono, mono66
from pysat.card import CardEnc, EncType
st = json.load(open(sys.argv[1])); od = sys.argv[2]; userows = (sys.argv[3] if len(sys.argv) > 3 else 'keep') == 'keep'
opt = sys.argv[4:] if len(sys.argv) > 4 else []
os.makedirs(od, exist_ok=True)
W = st['W']; L = st['L']; idx = {s: i for i, s in enumerate(W)}
t0 = time.time(); cnfp = os.path.join(od, 'cert.cnf'); body = cnfp + '.body'
nc = 0; buf = []
f = open(body, 'w')
def emit(c):
    global nc
    buf.append(' '.join(map(str, c)) + ' 0\n'); nc += 1
    if len(buf) >= 200000: f.write(''.join(buf)); buf.clear()
E = lazymono.LazyMono(W, emit=emit)
n_eager = nc
for q in st['activated']:
    for c in E.quad_clauses(*q): emit(c)
n_geo = nc
for s in ec.FIXED_OCC:
    if s in idx: emit([E.sel[idx[s]]])
for s_, bit in st.get('cube', []): emit([E.sel[idx[s_]] if bit else E.nsel[idx[s_]]])
rows = []
if userows and st.get('rows_file', 'none') != 'none':
    rows = [s for s, d in json.load(open(st['rows_file'])) if d == 1 and all(x in idx for x in s)]
row_first = nc + 1
for s in rows: emit([E.nsel[idx[x]] for x in s])
row_last = nc
enc = CardEnc.atmost(lits=[E.nsel[i] for i in range(E.n) if W[i] not in ec.FIXED_OCC], bound=L, top_id=E.top, encoding=EncType.seqcounter)
for c in enc.clauses: emit(c)
top = max(E.top, enc.nv)
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
info = {'state': sys.argv[1], 'W': len(W), 'L': L, 'vars': top, 'clauses': nc, 'eager_clauses': n_eager, 'activated_quadruples': len(st['activated']),
        'geometric_clauses': n_geo, 'row_clauses': len(rows), 'cube': st.get('cube', []), 'cnf_sha256': h.hexdigest(), 'cnf_bytes': os.path.getsize(cnfp), 'cadical_options': opt}
print(json.dumps(info), flush=True)
lrat = os.path.join(od, 'cert.lrat'); t = time.time()
r = subprocess.run(['cadical', '-q'] + opt + ['--lrat=true', '--binary=false', cnfp, lrat], capture_output=True, text=True)
info['cadical_exit'] = r.returncode; info['cadical_seconds'] = round(time.time() - t, 1)
print(json.dumps({'cadical_exit': r.returncode, 'seconds': info['cadical_seconds']}), flush=True)
if r.returncode == 20:
    info['lrat_bytes'] = os.path.getsize(lrat)
    hh = hashlib.sha256()
    with open(lrat, 'rb') as g:
        for chunk in iter(lambda: g.read(1 << 24), b''): hh.update(chunk)
    info['lrat_sha256'] = hh.hexdigest()
    t = time.time()
    c = subprocess.run([os.path.expanduser('~/.local/bin/cake_lpr'), cnfp, lrat], capture_output=True, text=True, env=dict(os.environ, CML_HEAP_SIZE=os.environ.get('CAKE_HEAP', '3000'), CML_STACK_SIZE=os.environ.get('CAKE_STACK', '500')))
    info['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else (c.stdout + c.stderr)[-300:]
    info['cake_seconds'] = round(time.time() - t, 1)
    print(json.dumps({'cake_lpr': info['cake_lpr'], 'seconds': info['cake_seconds']}), flush=True)
    # rows used by the proof
    hints = {}; empty = None
    with open(lrat) as g:
        for line in g:
            tk = line.split()
            if len(tk) > 1 and tk[1] == 'd': continue
            cid = int(tk[0]); z = tk.index('0', 1)
            hints[cid] = [abs(int(x)) for x in tk[z + 1:-1]]
            if z == 1: empty = cid
    used = set(); stack = [empty]; seen = set()
    while stack:
        x = stack.pop()
        if x in seen: continue
        seen.add(x)
        if x <= nc: used.add(x); continue
        stack.extend(hints.get(x, []))
    ur = sorted(x - row_first for x in used if row_first <= x <= row_last)
    info['used_original_clauses'] = len(used); info['used_rows'] = len(ur)
    info['used_geometric_clauses'] = sum(1 for x in used if x <= n_geo)
    json.dump([[rows[i], 1] for i in ur], open(os.path.join(od, 'used_rows.json'), 'w'))
    json.dump(sorted(used), open(os.path.join(od, 'used_clause_ids.json'), 'w'))
    os.remove(lrat)
info['seconds'] = round(time.time() - t0, 1)
json.dump(info, open(os.path.join(od, 'info.json'), 'w'), indent=1)
print(json.dumps(info), flush=True)
