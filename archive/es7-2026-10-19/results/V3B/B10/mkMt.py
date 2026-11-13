import json, glob, hashlib
ROOT='/opt/in/cloud/es7-2026-10-19'
files = sorted(glob.glob(ROOT+'/results/V3T/**/*.jsonl', recursive=True)) + sorted(glob.glob(ROOT+'/results/V3A/*/out.jsonl')) + sorted(glob.glob(ROOT+'/results/V3B/*/out.jsonl'))
keys=set(); recs=0
for f in files:
    for line in open(f):
        line=line.strip()
        if not line: continue
        try: r=json.loads(line)
        except Exception: continue
        if isinstance(r,dict) and r.get('kind')=='leaf' and r.get('verdict')=='VERIFIED' and 'lits' in r:
            keys.add((r['case'], json.dumps(r['lits']))); recs+=1
out=[]
for line in open('/opt/work/M.jsonl'):
    r=json.loads(line)
    if (r['case'], json.dumps(r['lits'])) in keys: continue
    out.append(r)
with open('/opt/work/Mt.jsonl','w') as fo:
    for i,r in enumerate(out):
        r['idx']=i; fo.write(json.dumps(r)+'\n')
print('files scanned', len(files)); print('VERIFIED leaf records', recs, 'distinct VERIFIED keys', len(keys)); print('n (Mt records)', len(out))
