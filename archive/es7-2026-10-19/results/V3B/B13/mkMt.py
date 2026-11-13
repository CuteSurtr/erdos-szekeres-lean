import json, glob, os, sys
ROOT='/opt/in/cloud/es7-2026-10-19'
files=[]
for dp,dn,fn in os.walk(ROOT+'/results/V3T'):
    files+= [os.path.join(dp,f) for f in fn if f.endswith('.jsonl')]
files+=glob.glob(ROOT+'/results/V3A/*/out.jsonl')+glob.glob(ROOT+'/results/V3B/*/out.jsonl')
keys=set()
for f in sorted(files):
    for line in open(f):
        line=line.strip()
        if not line: continue
        try: r=json.loads(line)
        except Exception: continue
        if isinstance(r,dict) and r.get('kind')=='leaf' and r.get('verdict')=='VERIFIED' and 'lits' in r:
            keys.add((r['case'],json.dumps(r['lits'])))
out=[]
for line in open('/opt/work/M.jsonl'):
    r=json.loads(line)
    if (r['case'],json.dumps(r['lits'])) in keys: continue
    out.append(r)
with open('/opt/work/Mt.jsonl','w') as g:
    for i,r in enumerate(out):
        r['idx']=i; g.write(json.dumps(r)+'\n')
print('files',len(files),'verified keys',len(keys),'n',len(out))
