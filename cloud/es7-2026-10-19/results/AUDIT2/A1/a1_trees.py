# A1 independent decoder: Lean tree/data sources -> leaf literal sets per case,
# compared with cake_lpr-verified records (V3 re-check records, Haudit t5).
import re, json, sys, os, glob, hashlib
R = sys.argv[1]  # results dir
V = R + '/V2-L/V2L'
def declit(d): return d//2 if d % 2 == 0 else -(d//2)
def unpack(k, n, base):
    out = []
    for _ in range(k):
        out.append(declit(n % base)); n //= base
    return out[::-1]
# --- Data.lean: caseSpecs and casePacked
data = open(V + '/Data.lean').read()
def block(name):
    i = data.index('def %s ' % name); j = data.index(':= [', i) + 4
    k = data.index('\n\n', j); return data[j:k]
specs = []
for m in re.finditer(r'\(\[([0-9, ]*)\], \[([0-9, ]*)\]\)', block('caseSpecs')):
    f = lambda s: [int(x) for x in s.split(',') if x.strip()]
    specs.append((tuple(f(m.group(1))), tuple(f(m.group(2)))))
packed = [(int(a), int(b, 0)) for a, b in re.findall(r'\((\d+), (0x[0-9a-fA-F]+|\d+)\)', block('casePacked'))]
assert len(specs) == 450 and len(packed) == 450, (len(specs), len(packed))
cubes = [unpack(k, n, 65536) for k, n in packed]
# compare with Mii-S cases.icnf and cases.jsonl
icnf = [l.split()[1:-1] for l in open(R + '/Mii-S/cases.icnf') if l.startswith('a ')]
icnf = [[int(x) for x in l] for l in icnf]
cj = [json.loads(l) for l in open(R + '/Mii-S/cases.jsonl')]
assert len(icnf) == 450 and len(cj) == 450
name_of = {}
for i in range(450):
    assert cubes[i] == icnf[i], ('cube mismatch', i)
    assert (tuple(cj[i]['U']), tuple(cj[i]['L'])) == specs[i], ('spec mismatch', i)
    name_of[specs[i]] = cj[i]['case']
assert len(set(specs)) == 450
print('Data.lean: 450 specs/cubes equal Mii-S cases.icnf and cases.jsonl order; specs distinct')
# --- Trees
tbl = open(V + '/Trees/Table.lean').read()
ent = re.findall(r'\(\(\[([0-9, ]*)\], \[([0-9, ]*)\]\), (\.leaf|Trees\.tree(\d+))\)', tbl)
assert len(ent) == 450
f = lambda s: tuple(int(x) for x in s.split(',') if x.strip())
treeof = {}
for u, l, t, num in ent:
    s = (f(u), f(l)); assert s not in treeof; treeof[s] = num or None
assert list(treeof) == specs
defs = {}
for fn in glob.glob(V + '/Trees/T*.lean'):
    src = open(fn).read()
    for m in re.finditer(r'^def (n\d+_\d+) : List \(List Int × CTree\) := \[(.*)\]$', src, re.M):
        kids = []
        for mm in re.finditer(r'(lf|nd) (\d+) (0x[0-9a-f]+|\d+)(?: (n\d+_\d+))?', m.group(2)):
            kids.append((mm.group(1), unpack(int(mm.group(2)), int(mm.group(3), 0), 1 << 20), mm.group(4)))
        # sanity: count items equals count of "lf "/"nd " tokens
        assert len(kids) == m.group(2).count('lf ') + m.group(2).count('nd ')
        defs[m.group(1)] = kids
    for m in re.finditer(r'^def tree(\d+) : CTree := \.node (n\d+_\d+)$', src, re.M):
        defs['tree' + m.group(1)] = m.group(2)
def leaves(name):
    out = []
    for kind, cube, sub in defs[name]:
        if kind == 'lf': out.append(cube)
        else: out += [cube + x for x in leaves(sub)]
    return out
lean_leaves = {}
for s in specs:
    t = treeof[s]
    lean_leaves[name_of[s]] = [[]] if t is None else leaves(defs['tree' + t])
tot = sum(len(v) for v in lean_leaves.values())
print('Lean tree leaves total', tot, 'cases with .leaf', sum(1 for s in specs if treeof[s] is None))
# --- verified records
ver = {}  # case -> set of frozensets
nrec = 0
for p in open(R + '/V3Z/aggregate_inputs.txt').read().split():
    path = os.path.join(R, '..', p)
    for line in open(path):
        r = json.loads(line)
        if r.get('kind') == 'leaf' and r.get('cake_lpr') == 's VERIFIED UNSAT':
            ver.setdefault(r['case'], set()).add(frozenset(r['lits'])); nrec += 1
direct = {}
for line in open(R + '/Haudit/t5_all172.jsonl'):
    r = json.loads(line)
    if r['cake_lpr'] == 's VERIFIED UNSAT': direct[r['case']] = r['cnf_sha256']
print('V3 verified leaf records', nrec, 'cases', len(ver), '; Haudit t5 verified direct', len(direct))
bad = 0; kinds = {'direct': 0, 'v3': 0}
for i, s in enumerate(specs):
    c = name_of[s]
    for l in lean_leaves[c]:
        if len(set(l)) != len(l): print('dup lit in leaf', c, l)
        if 0 in l: print('zero lit', c, l); bad += 1
        if l == [] and c in direct and cj[i]['method'] == 'direct' and direct[c] == cj[i]['cnf_sha256']:
            kinds['direct'] += 1; continue
        if frozenset(l) in ver.get(c, ()):
            kinds['v3'] += 1; continue
        bad += 1
        if bad < 20: print('UNVERIFIED Lean leaf', c, l)
print('Lean leaves matched:', kinds, 'unmatched:', bad)
extra = {c: len(ver[c] - {frozenset(l) for l in lean_leaves.get(c, [])}) for c in ver}
print('verified leaves not in Lean trees:', {c: n for c, n in extra.items() if n})
