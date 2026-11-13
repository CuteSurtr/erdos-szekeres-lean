import json,glob,sys
R='/opt/in/cloud/es7-2026-10-19/results'
files=sorted(glob.glob(R+'/V3T/**/*.jsonl',recursive=True))+sorted(glob.glob(R+'/V3A/*/out.jsonl'))+sorted(glob.glob(R+'/V3B/*/out.jsonl'))
keys=set()
for f in files:
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
    for k,r in enumerate(out):
        r['idx']=k; g.write(json.dumps(r)+'\n')
print('files',len(files),'verified_keys',len(keys),'n',len(out))
