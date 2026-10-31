import sys, json, hashlib, collections, os
root, fpath, man = sys.argv[1:4]; files = sys.argv[4:]
raw = open(fpath,'rb').read(); hdr, body = raw.split(b"\n",1); nv, nc = map(int, hdr.split()[2:4])
cases = [json.loads(l) for l in open(os.path.join(root,"results/Mii-S/cases.jsonl"))]
cubes = [l for l in open(os.path.join(root,"results/Mii-S/cases.icnf")) if l.startswith("a ")]
cube_of = {}
for c,l in zip(cases,cubes):
    cb = sorted((int(x) for x in l.split()[1:-1]), key=abs)
    d = f"p cnf {nv} {nc+len(cb)}\n".encode()+body+"".join(f"{x} 0\n" for x in cb).encode()
    assert hashlib.sha256(d).hexdigest()==c["cnf_sha256"], c["case"]
    cube_of[c["case"]] = cb
print("cases.icnf cubes match cases.jsonl cnf_sha256:", len(cube_of))
recs=[json.loads(l) for l in open(man)]
by_case=collections.defaultdict(list)
for r in recs: by_case[r["case"]].append(r["lits"])
cnt=collections.Counter(); fieldsets=collections.Counter(); perfile=collections.Counter()
leafv=collections.defaultdict(list); covv=collections.defaultdict(list)
for f in files:
    for l in open(os.path.join(root,f)):
        try: o=json.loads(l)
        except ValueError: cnt['badjson']+=1; continue
        fieldsets[(o.get('kind'), o.get('verdict'), tuple(sorted(o)))]+=1
        if o.get('verdict')=='VERIFIED':
            if o.get('kind')=='leaf' and 'note' not in o:
                ok = o.get('rc')==20 and o.get('cake_lpr')=='s VERIFIED UNSAT' and o.get('proof_bytes',0)>0
                if not ok: cnt['leaf_VERIFIED_inconsistent']+=1; print("INCONS", f, o)
            if o.get('kind')=='leaf' and 'lits' in o: leafv[(o['case'],json.dumps(o['lits']))].append((f,o))
            if o.get('kind')=='cover' and 'leaves_sha256' in o: covv[(o['key'],o['leaves_sha256'])].append((f,o))
        if o.get('kind')=='leaf' and o.get('verdict')=='VERIFIED' and 'note' in o: cnt['leaf_trivial_note']+=1
for k,v in sorted(fieldsets.items(), key=lambda x:-x[1]): print(v,k)
# covers used
emptyleaf=0; nocov=0
for case,lv in sorted(by_case.items()):
    lsha=hashlib.sha256(json.dumps(lv).encode()).hexdigest()
    cv=covv.get((case,lsha),[])
    if not cv: nocov+=1; print("NO COVER", case); continue
    clauses=[[x] for x in cube_of[case]]+[[-x for x in l] for l in lv]
    mv=max([nv]+[abs(x) for c in clauses for x in c])
    d=(f"p cnf {mv} {len(clauses)}\n"+"".join(" ".join(map(str,c))+" 0\n" for c in clauses)).encode()
    sha=hashlib.sha256(d).hexdigest()
    for f,o in cv:
        if 'note' in o:
            emptyleaf+=1
            if [] not in lv: print("TRIVIAL COVER WITHOUT EMPTY LEAF", case)
            continue
        if o.get('cnf_sha256')!=sha or o.get('rc')!=20 or o.get('cake_lpr')!='s VERIFIED UNSAT':
            print("COVER RECORD BAD", case, f, o.get('cnf_sha256')==sha, o.get('rc'), o.get('cake_lpr'))
        else: cnt['cover_ok']+=1
print("trivial covers", emptyleaf, "missing", nocov)
# leaves used: by file
for case,lv in by_case.items():
    for l in lv:
        for f,o in leafv.get((case,json.dumps(l)),[]): perfile[f.split('/')[1]]+=1
print(dict(cnt)); print(dict(perfile))
n_empty=sum(1 for lv in by_case.values() if [] in lv); print("cases with empty leaf", n_empty, "of which single-leaf", sum(1 for lv in by_case.values() if lv==[[]]))
