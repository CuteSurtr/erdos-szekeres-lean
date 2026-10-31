"""Decode V2L/Data.lean exactly as the Lean defs do and rebuild the CNFs named by
RootCertificate / UpCertificates / caseCnf; compare sha256 with Mii-S records."""
import re, sys, json, hashlib
R = sys.argv[1]
src = open(R + '/V2-L/V2L/Data.lean').read()
def block(name):
    m = re.search(r'def ' + name + r' : [^\n]*:= \[\n(.*?)\]\n', src, re.S); return m.group(1)
def declit(d): return d//2 if d % 2 == 0 else -(d//2)
def unpack(k, n):
    acc = []
    for _ in range(k): acc.insert(0, declit(n % 65536)); n //= 65536
    return acc
def packed(name):
    return [unpack(int(a), int(b, 16)) for a, b in re.findall(r'\((\d+), (0x[0-9a-f]+)\)', block(name))]
def natlists(s): return [[int(x) for x in t.split(',') if x.strip()] for t in re.findall(r'\[([0-9, ]*)\]', s)]
upSets = natlists(block('upSets'))
specs = [(natlists(a)[0], natlists(b)[0]) for a, b in re.findall(r'\((\[[0-9, ]*\]), (\[[0-9, ]*\])\)', block('caseSpecs'))]
upCubes = packed('upPacked'); caseCubes = packed('casePacked')
print(len(upSets), len(upCubes), len(specs), len(caseCubes))
raw = open('/opt/work/F.cnf', 'rb').read(); hdr, Fb = raw.split(b'\n', 1); nv, nc = int(hdr.split()[2]), int(hdr.split()[3])
def emit(extra):
    return hashlib.sha256(f"p cnf {nv} {nc+len(extra)}\n".encode() + Fb + "".join(" ".join(map(str, c)) + " 0\n" for c in extra).encode()).hexdigest()
neg = lambda c: [-z for z in c]
rec = {json.loads(l)['obligation']: json.loads(l)['cnf_sha256'] for l in open(R + '/Mii-S/cover_lrat.jsonl')}
table = list(zip(specs, caseCubes))
ok = emit([neg(c) for c in upCubes]) == rec['root']
print('rootCnf sha == cover_lrat root:', ok)
bad = 0
for U, u in zip(upSets, upCubes):
    cs = [c for (s, c) in table if s[0] == U]
    if emit([[z] for z in u] + [neg(c) for c in cs]) != rec['up:' + ','.join(map(str, U))]: bad += 1
print('upCnf mismatches:', bad, 'of', len(upSets))
cases = [json.loads(l) for l in open(R + '/Mii-S/cases.jsonl')]
bad = sum(emit([[z] for z in c]) != k['cnf_sha256'] or (k['U'], k['L']) != tuple(s) and [k['U'], k['L']] != list(s) for (s, c), k in zip(table, cases))
print('caseCnf mismatches:', bad, 'of', len(cases))
print('zero literals:', sum(z == 0 for c in upCubes + caseCubes for z in c))
