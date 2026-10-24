import json,glob,os,sys,hashlib
ROOT=sys.argv[1]
files=sorted(glob.glob(ROOT+'/results/V3T/**/*.jsonl',recursive=True))+sorted(glob.glob(ROOT+'/results/V3A/*/out.jsonl'))+sorted(glob.glob(ROOT+'/results/V3B/*/out.jsonl'))
keys=set()
for f in files:
    for line in open(f):
        line=line.strip()
        if not line: continue
        try: r=json.loads(line)
        except Exception: continue
        if isinstance(r,dict) and r.get('kind')=='leaf' and r.get('verdict')=='VERIFIED' and 'lits' in r:
            keys.add((r.get('case'),json.dumps(r['lits'])))
print('files',len(files))
print('verified keys',len(keys))
out=[]
for line in open('/opt/work/M.jsonl'):
    r=json.loads(line)
    if (r['case'],json.dumps(r['lits'])) in keys: continue
    out.append(r)
with open('/opt/work/Mt.jsonl','w') as g:
    for i,r in enumerate(out):
        r['idx']=i; g.write(json.dumps(r)+'\n')
print('n',len(out))
