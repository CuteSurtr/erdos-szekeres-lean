# Recompute cnf_sha256 of V3 leaf records from F (regenerated here) + case cube + leaf units.
import json, hashlib, sys, glob, random
F=open(sys.argv[1],'rb').read(); hdr,body=F.split(b"\n",1); nv,nc=map(int,hdr.split()[2:4])
cases=[json.loads(l) for l in open('results/Mii-S/cases.jsonl')]
cubes=[l for l in open('results/Mii-S/cases.icnf') if l.startswith('a ')]
cube_of={c['case']:sorted(map(int,l.split()[1:-1]),key=abs) for c,l in zip(cases,cubes)}
recs=[]
for f in sorted(glob.glob('results/V3[A-E]/*/out*.jsonl')+glob.glob('results/V3T/**/*.jsonl',recursive=True)):
    for l in open(f):
        try: o=json.loads(l)
        except: continue
        if o.get('kind')=='leaf' and 'cnf_sha256' in o and o.get('verdict')=='VERIFIED': recs.append(o)
print('leaf records with sha',len(recs))
rnd=random.Random(5); s=rnd.sample(recs,min(int(sys.argv[2]),len(recs))); ok=0
for o in s:
    cube=cube_of[o['case']]; cs=set(cube)
    units=cube+sorted((x for x in o['lits'] if x not in cs),key=abs)
    d=f"p cnf {nv} {nc+len(units)}\n".encode()+body+"".join(f"{x} 0\n" for x in units).encode()
    ok+= hashlib.sha256(d).hexdigest()==o['cnf_sha256']
print('sampled',len(s),'sha match',ok)
