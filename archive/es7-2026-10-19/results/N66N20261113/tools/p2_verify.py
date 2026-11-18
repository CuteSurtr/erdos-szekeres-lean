"""Phase 2: independent check of a trimmed certificate CNF (no solver).  Every clause of trim.cnf must belong to one of
  geometric : the clause stream of mono66.generate for W (the generator with the written soundness argument, README
              section 6), compared EXACTLY as sorted literal tuples (selector guards appended as in mono66.py);
  units     : sel of a fixed state (the empty diagram, the single cell) or a cube unit of layout.json;
  rows      : -sel over the support of a row that the verified justification file justifies (final_verify66.py run
              on that directory: kinds cycle / core / transported / mirror, 0 bad, rows_match);
  card      : pysat CardEnc.atmost(seqcounter) over the hole literals, bound L, top_id = mono66's last variable,
              re-encoded here.
Also: header variable count, SHA-256 of trim.cnf and trim.lrat, cake_lpr verdict line in cake.out.
usage: p2_verify.py <certdir> [<tcert dir with justification.json> | none]"""
import sys, json, os, hashlib, subprocess, time
import etv_common as ec, mono66, coupled5
from pysat.card import CardEnc, EncType
assert ec.A == 4 and ec.B == 4 and ec.N == 70
od = sys.argv[1]; tdir = sys.argv[2] if len(sys.argv) > 2 else 'none'
t0 = time.time()
lay = json.load(open(os.path.join(od, 'layout.json')))
W = lay['W']; L = lay['L']; idx = {s: i for i, s in enumerate(W)}
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as g:
        for chunk in iter(lambda: g.read(1 << 24), b''): h.update(chunk)
    return h.hexdigest()
cnfp = os.path.join(od, 'trim.cnf')
clauses = []
with open(cnfp) as g:
    hd = g.readline().split(); nv, nc = int(hd[2]), int(hd[3])
    for line in g:
        t = line.split()
        if not t or t[0] == 'c': continue
        assert t[-1] == '0'
        clauses.append(tuple(sorted(int(x) for x in t[:-1])))
assert len(clauses) == nc, (len(clauses), nc)
maxvar = max(abs(x) for c in clauses for x in c)
pending = set(clauses)
# selectors as mono66.py numbers them
probe = coupled5.CNF(W, static=False); sel = [probe.nv + 1 + i for i in range(len(W))]; del probe
assert [sel[0], sel[-1]] == lay['sel']
kinds = {'units': 0, 'rows': 0, 'card': 0, 'geometric': 0}
units = set([(sel[idx[s]],) for s in ec.FIXED_OCC if s in idx] + [((sel[idx[s_]] if bit else -sel[idx[s_]]),) for s_, bit in lay['cube']])
for c in list(pending):
    if c in units: pending.discard(c); kinds['units'] += 1
jrows = set(); jinfo = None
if tdir != 'none':
    J = json.load(open(os.path.join(tdir, 'justification.json')))
    jrows = set(tuple(sorted(-sel[idx[x]] for x in j['support'])) for j in J['justifications'] if j['demand'] == 1 and all(x in idx for x in j['support']))
    jinfo = {'rows_file': J['rows_file'], 'justified_rows': len(J['justifications'])}
for c in list(pending):
    if c in jrows: pending.discard(c); kinds['rows'] += 1
enc = CardEnc.atmost(lits=[-sel[i] for i in range(len(W)) if W[i] not in ec.FIXED_OCC], bound=L, top_id=lay['mono_top'], encoding=EncType.seqcounter)
card = set(tuple(sorted(c)) for c in enc.clauses)
for c in list(pending):
    if c in card: pending.discard(c); kinds['card'] += 1
if lay.get('sb_pairs'):           # lex-leader clauses for tau, regenerated from the recorded pair list (p2_sb.py checks the pairs)
    import p2_sb
    sbc, _ = p2_sb.sb_clauses({W[i]: sel[i] for i in range(len(W))}, lay['sb_pairs'], max(lay['mono_top'], enc.nv))
    sbset = set(tuple(sorted(c)) for c in sbc); kinds['sb'] = 0
    for c in list(pending):
        if c in sbset: pending.discard(c); kinds['sb'] += 1
stream = [0]; geo_found = set()
def emit(c, own):
    stream[0] += 1
    key = tuple(sorted(list(c) + [-sel[o] for o in own]))
    if key in pending: geo_found.add(key)
cnf, sel2, top, C, U, CE, UE = mono66.generate(emit, S=W)
assert sel2 == sel and top == lay['mono_top'], (top, lay['mono_top'])
kinds['geometric'] = len(geo_found)
missing = pending - geo_found
cake = open(os.path.join(od, 'cake.out')).read() if os.path.exists(os.path.join(od, 'cake.out')) else ''
res = {'trim_cnf_sha256': sha(cnfp), 'trim_lrat_sha256': sha(os.path.join(od, 'trim.lrat')) if os.path.exists(os.path.join(od, 'trim.lrat')) else None,
       'clauses': nc, 'distinct_clauses': len(set(clauses)), 'kinds': kinds, 'unclassified': len(missing), 'unclassified_sample': sorted(missing)[:5],
       'header_vars': nv, 'max_var': maxvar, 'vars_ok': maxvar <= nv, 'mono66_stream_clauses': stream[0], 'budget': L, 'cube': lay['cube'],
       'justification': jinfo, 'sb_pairs': lay.get('sb_pairs', []), 'cake_lpr': 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in cake.splitlines() else cake[-300:],
       'seconds': round(time.time() - t0, 1)}
res['ALL_OK'] = bool(not missing and maxvar <= nv and res['cake_lpr'] == 's VERIFIED UNSAT')
json.dump(res, open(os.path.join(od, 'verify.json'), 'w'), indent=1); print(json.dumps(res), flush=True)
