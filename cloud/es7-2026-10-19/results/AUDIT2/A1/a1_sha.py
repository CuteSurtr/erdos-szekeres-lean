# A1: from the Lean-emitted F and the Lean data (decoded by a1_trees.py's code), rebuild the
# DIMACS text of every case CNF and of every tree-leaf CNF (V3 normal form: F body, case cube
# units sorted by abs, extra leaf units sorted by abs) and compare sha256 with the records.
import sys, json, hashlib, re, os
R, FPATH = sys.argv[1], sys.argv[2]
src = open('/tmp/claude-0/s/a1_trees.py').read().split('# --- verified records')[0]
sys.argv = ['x', R]; exec(src)
raw = open(FPATH, 'rb').read()
print('F sha256', hashlib.sha256(raw).hexdigest(), 'bytes', len(raw))
nl = raw.index(b'\n'); hdr = raw[:nl].split(); body = raw[nl + 1:]
nv, nc = int(hdr[2]), int(hdr[3]); print('header', hdr)
lines = body.split(b'\n'); assert lines[-1] == b''; lines = lines[:-1]
assert len(lines) == nc, (len(lines), nc)
badz = sum(1 for l in lines if l.split()[-1] != b'0' or l.split()[:-1].count(b'0'))
mx = max(abs(int(t)) for l in lines for t in l.split())
print('F lines', len(lines), 'lines with a misplaced 0 token:', badz, 'max |lit|', mx)
# case CNFs in Lean order
hcache = {}
def prefix(n):
    if n not in hcache:
        h = hashlib.sha256(); h.update(f'p cnf {nv} {nc + n}\n'.encode()); h.update(body); hcache[n] = h
    return hcache[n].copy()
mism = 0
for i, s in enumerate(specs):
    h = prefix(len(cubes[i])); h.update(''.join(f'{x} 0\n' for x in cubes[i]).encode())
    if h.hexdigest() != cj[i]['cnf_sha256']: mism += 1
print('case CNF (Lean order) sha256 = Mii-S cases.jsonl cnf_sha256 for', 450 - mism, 'of 450')
rec = {}
for p in open(R + '/V3Z/aggregate_inputs.txt').read().split():
    for line in open(os.path.join(R, '..', p)):
        r = json.loads(line)
        if r.get('kind') == 'leaf' and r.get('cake_lpr') == 's VERIFIED UNSAT':
            rec.setdefault((r['case'], frozenset(r['lits'])), set()).add(r['cnf_sha256'])
ok = bad = 0
for i, s in enumerate(specs):
    c = name_of[s]; cube = sorted(cubes[i], key=abs); cs = set(cube)
    for l in lean_leaves[c]:
        if treeof[s] is None and cj[i].get('method') == 'direct': continue
        extra = sorted(set(x for x in l if x not in cs), key=abs)
        h = prefix(len(cube) + len(extra)); h.update(''.join(f'{x} 0\n' for x in cube + extra).encode())
        if h.hexdigest() in rec.get((c, frozenset(l)), ()): ok += 1
        else:
            bad += 1
            if bad < 10: print('no verified record with this CNF sha', c, l)
print('wave tree leaves whose rebuilt CNF sha256 equals a verified record sha256:', ok, 'not:', bad)
# --- the 122 obligations, rebuilt from the Lean terms rootCnf / upCnf (writeDimacs format)
ups = re.findall(r'^  \[([0-9, ]*)\][,\]]', block('upSets'), re.M)
upsets = [tuple(int(x) for x in u.split(',') if x.strip()) for u in ups]
upp = [(int(a), int(b, 0)) for a, b in re.findall(r'\((\d+), (0x[0-9a-fA-F]+|\d+)\)', block('upPacked'))]
assert len(upsets) == 121 and len(upp) == 121, (len(upsets), len(upp))
upcubes = [unpack(k, n, 65536) for k, n in upp]
def text_sha(extra_clauses):
    h = hashlib.sha256(); h.update(f'p cnf {nv} {nc + len(extra_clauses)}\n'.encode()); h.update(body)
    h.update(''.join(' '.join(map(str, c + [0])) + '\n' for c in extra_clauses).encode()); return h.hexdigest()
neg = lambda c: [-z for z in c]
obl = {'root': text_sha([neg(c) for c in upcubes])}
for U, uc in zip(upsets, upcubes):
    cases_U = [cubes[i] for i, s in enumerate(specs) if s[0] == U]
    obl['up:' + ','.join(map(str, U))] = text_sha([[z] for z in uc] + [neg(c) for c in cases_U])
for f in ('Mii-S/cover_lrat.jsonl', 'Haudit/t3_cover_lrat.jsonl'):
    recs = [json.loads(l) for l in open(R + '/' + f)]
    good = {r['obligation']: r['cnf_sha256'] for r in recs if r['cake_lpr'] == 's VERIFIED UNSAT'}
    print(f, 'verified obligations', len(good), 'sha256 equal to Lean-rebuilt:',
          sum(1 for k in obl if good.get(k) == obl[k]), 'of', len(obl),
          'missing/mismatch:', [k for k in obl if good.get(k) != obl[k]][:10])
