"""Independent structural check of the 2-level cover (no reuse of Mii-S code).
Reads F, the 122 regenerated obligation CNFs, Mii-S/cases.icnf and cases.jsonl."""
import sys, json, hashlib, glob, os
R = sys.argv[1]  # results dir
def read(p):
    with open(p,'rb') as f: raw=f.read()
    hdr, body = raw.split(b"\n",1); t=hdr.split()
    assert t[:2]==[b"p",b"cnf"]
    return int(t[2]), int(t[3]), body
nv, nc, Fb = read('/opt/work/F.cnf')
Fcl = Fb.count(b" 0\n") + (1 if Fb.startswith(b"0\n") else 0)
def extra(p):
    v, c, b = read(p)
    assert v == nv and b.startswith(Fb), p
    rest = b[len(Fb):].decode().split("\n")
    cls = [tuple(int(x) for x in l.split()) for l in rest if l]
    assert all(c[-1]==0 for c in cls); cls=[c[:-1] for c in cls]
    assert c == nc + len(cls), (p, c, nc, len(cls))
    for cl in cls:
        assert all(0<abs(x)<=nv for x in cl)
    return cls
root = extra('/opt/work/ob/root.cnf')
assert len(root)==121 and all(len(c)>1 for c in root)
rootset = {frozenset(c) for c in root}; assert len(rootset)==121
ups = sorted(glob.glob('/opt/work/ob/up_*.cnf')); assert len(ups)==121
cubes = [l.split() for l in open(R+'/Mii-S/cases.icnf') if l.startswith('a ')]
cubes = [frozenset(int(x) for x in t[1:-1]) for t in cubes]
assert len(cubes)==450 and len(set(cubes))==450
covered = []; upsets=set()
for p in ups:
    cls = extra(p)
    units = frozenset(c[0] for c in cls if len(c)==1)
    blocks = [frozenset(-x for x in c) for c in cls if len(c)>1]
    assert len(units)+len(blocks)==len(cls)
    assert not any(-u in units for u in units)
    neg = frozenset(-u for u in units)
    assert neg in rootset, ("UP units of", p, "not blocked in root")
    upsets.add(neg)
    for b in blocks: assert b in set(cubes), ("blocked cube not a case cube", p)
    covered += blocks
assert upsets == rootset
assert len(covered)==450 and set(covered)==set(cubes), (len(covered), len(set(covered)))
# cases.jsonl sha = F + cube units (cube sorted by abs, as in cases.icnf order)
cases=[json.loads(l) for l in open(R+'/Mii-S/cases.jsonl')]
names=[c['case'] for c in cases]; assert len(set(names))==450
raw=[l.split() for l in open(R+'/Mii-S/cases.icnf') if l.startswith('a ')]
bad=0
for c,t in zip(cases,raw):
    cube=[int(x) for x in t[1:-1]]
    data=f"p cnf {nv} {nc+len(cube)}\n".encode()+Fb+"".join(f"{x} 0\n" for x in cube).encode()
    if hashlib.sha256(data).hexdigest()!=c['cnf_sha256']: bad+=1
    assert c['nlits']==len(cube)
print("root 121 distinct blocking clauses; 121 up files; UP sets == root blocks;",
      "450 blocked cubes == 450 cases.icnf cubes each once; cases.jsonl sha mismatches:", bad)
