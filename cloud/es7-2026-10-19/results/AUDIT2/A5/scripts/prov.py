# independent provenance of sampled leaves in raw wave directories at Zf
import json,os,collections,glob
R='/opt/in/cloud/es7-2026-10-19/'
S0={json.loads(l)['case']:json.loads(l) for l in open(R+'results/Mii-S/cases.jsonl')}
M={}
for l in open('/opt/work/M.jsonl'):
    m=json.loads(l); M[m['idx']]=m
c=collections.Counter(); notes=[]
for l in open('/opt/a5/sample.jsonl'):
    s=json.loads(l); key=frozenset(s['lits']); hit=set()
    for src in M[s['idx']]['sources']:
        if not src.startswith('results/'): continue
        d=R+src
        if os.path.basename(d)!=s['case']: notes.append(('dirname',src,s['case']))
        p=d+'/leaves.icnf'
        if os.path.exists(p):
            for x in open(p):
                if x.startswith('a ') and frozenset(int(t) for t in x.split()[1:-1])==key: hit.add('icnf')
        p=d+'/leaves.jsonl'
        if os.path.exists(p):
            for x in open(p):
                try: r=json.loads(x)
                except Exception: continue
                if 'case_sha256' in r and r['case_sha256']!=S0[s['case']]['cnf_sha256']: notes.append(('case_sha',src))
                if r.get('status')=='UNSAT' and 'cube' in r and frozenset(r['cube'])==key: hit.add('jsonl_unsat')
    c[tuple(sorted(hit))]+=1
print(dict(c)); print('notes',sorted(set(map(str,notes)))[:20])
