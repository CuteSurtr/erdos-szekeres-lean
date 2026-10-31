import json,glob,sys
ROOT=sys.argv[1]
files=glob.glob(ROOT+'/results/V3T/**/*.jsonl',recursive=True)+glob.glob(ROOT+'/results/V3A/*/out.jsonl')+glob.glob(ROOT+'/results/V3B/*/out.jsonl')
keys=set(); nrec=0
for f in sorted(files):
    for line in open(f):
        line=line.strip()
        if not line: continue
        try: r=json.loads(line)
        except Exception: continue
        if isinstance(r,dict) and r.get('kind')=='leaf' and r.get('verdict')=='VERIFIED' and 'lits' in r:
            keys.add((r['case'],json.dumps(r['lits']))); nrec+=1
out=[]
for line in open('/opt/work/M.jsonl'):
    r=json.loads(line)
    if (r['case'],json.dumps(r['lits'])) in keys: continue
    out.append(r)
with open('/opt/work/Mt.jsonl','w') as g:
    for i,r in enumerate(out):
        r['idx']=i; g.write(json.dumps(r)+'\n')
print('files',len(files),'verified records',nrec,'verified keys',len(keys),'n',len(out))
