# Task 1: cases.jsonl vs cases.icnf, and case CNF sha256 rebuilt from F + icnf units (own code)
import json, hashlib, sys, collections
F, ICNF, JL = sys.argv[1:4]
raw = open(F,'rb').read()
hdr, body = raw.split(b"\n",1)
assert hdr.startswith(b"p cnf") and b"\nc" not in body[:1]
nv, nc = map(int, hdr.split()[2:4])
cubes = [list(map(int,l.split()[1:-1])) for l in open(ICNF) if l.startswith('a')]
recs = [json.loads(l) for l in open(JL)]
assert len(cubes)==450==len(recs)
names=set(); bad=0
for c, r in zip(cubes, recs):
    U, L = tuple(r['U']), tuple(r['L'])
    names.add((U,L))
    data = f"p cnf {nv} {nc+len(c)}\n".encode() + body + "".join(f"{l} 0\n" for l in c).encode()
    h = hashlib.sha256(data).hexdigest()
    ok = h == r['cnf_sha256'] and r['nlits']==len(c)
    if not ok: bad+=1; print("MISMATCH", r['case'], h)
P=range(2,17)
exp=set()
for a in P:
    for b in P:
        if a<b: exp.add(((a,b),())); exp.add(((),(a,b)))
        if a!=b: exp.add(((a,),(b,)))
    exp.add(((a,),())); exp.add(((),(a,)))
print("distinct (U,L) in jsonl:", len(names), "expected set equal:", names==exp, "sha mismatches:", bad)
print("by |U|:", collections.Counter(len(u) for u,l in names))
print("status:", collections.Counter(r['status'] for r in recs), "method:", collections.Counter(r.get('method') for r in recs))
