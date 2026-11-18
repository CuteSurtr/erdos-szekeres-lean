#!/usr/bin/env python3
"""Adapt our frozen successful replay driver; never import a producer checker."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R.parents[1]
old=R.parent/'left15';source=old/'tools/replay.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(old/'SHA256SUMS')=='1ac9e0133d42a02c2b423d3dda39b5ce985d1f95486c6599449fa31c99cab0ca'
manifest=dict(line.split('  ',1)[::-1] for line in (old/'SHA256SUMS').read_text().splitlines())
assert sha(source)==manifest['tools/replay.py']
text=source.read_text()
replacements=[('Own fresh low15','Own fresh original low16'),("'low15-n7-a'","'low16-n7-a'"),
 ('LIMIT=1650<<20','LIMIT=3100<<20'),('2026-11-14T07:43:40+09:00','2026-11-14T08:22:30+09:00'),
 ('absolute07:43:40 deadline','absolute08:22:30 deadline'),('own1650MiB/no-swap guard','own3100MiB/no-swap guard'),
 ('nov13c-vfy-delta6-low15-independent','nov13c-vfy-delta6-low16-independent'),
 ("assert json.loads((R/'data/instance-result.json').read_text())['status']=='PASS'",
  "base=json.loads((R.parent/'left16_longcup/data/base-instance.json').read_text());assert base['status']=='PASS' and base['variables']==128297 and base['clauses']==903593\n assert '2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8' in base['hashes'].values()"),
 ("'AS_MiB':1650","'AS_MiB':3100"),("'heap_MiB':1400","'heap_MiB':2800"),('--CML_HEAP_SIZE=1400','--CML_HEAP_SIZE=2800'),
 ('793063f5c7c5208c16ce038c63659878adee4eb049546d775d65c5a18ed60418','2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8'),
 ('f86789033376814b7a36ea4bbc26e5a6007e66168a1fef4e38d09a5f6cca2f7c','247f64c822609e878be490e059fb7e0c96e5e71fde0e265de74c7be36cd8dd42'),
 ('86a3a187245ba67f0f44f00e6f24901008adddcd7edc67cab348d02e26c8366c','9b34ae9a407ce304f0ed82b9dbc6947a0219419a46145a326cfa189dd772b206'),
 ("'left_m':15","'left_m':16")]
counts=[]
for a,b in replacements:
 assert a in text,a;counts.append([a,b,text.count(a)]);text=text.replace(a,b)
compile(text,str(R/'tools/replay.py'),'exec')
with (R/'tools/replay.py').open('x') as f:f.write(text)
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
snapshots=[(W/'low16-n7-a/result.json','original-heap550-result.json'),(W/'low16-n7-a/cake.log','original-heap550-cake.log'),
 (W/'low16-replay-a/result.json','parent-heap2800-result.json'),(W/'low16-replay-a/cake.log','parent-heap2800-cake.log'),
 (E/'low_split/Capacity16.lean','Capacity16.lean.txt'),(E/'low_split/capacity_checks/pass/result.json','capacity-pass-result.json'),
 (R.parent/'left16_longcup/data/base-instance.json','base-instance.json')]
for src,name in snapshots:
 with (R/'data'/name).open('xb') as f:f.write(src.read_bytes())
result={'status':'PASS','basis':str(source),'basis_sha256':sha(source),'driver_sha256':sha(R/'tools/replay.py'),
 'replacements':counts,'snapshots':{name:{'source':str(src),'sha256':sha(src)} for src,name in snapshots}}
with (R/'data/preparation.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','driver_sha256':result['driver_sha256']}))
