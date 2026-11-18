#!/usr/bin/env python3
import datetime,hashlib,json,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R.parents[1]
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
  os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
 return h.hexdigest()
old={'low_split_audit':'8609cc06302c622b3f37014c27334ba142bb535b86e528aa654217e9959303c3',
 'low_split_audit/replay':'159ac6c8386dbf78f2e63481bc3e4f659fe72e8c2c1456616db81729d79f298e',
 'low_split_audit/n6':'6017645ab590b7e8faea0af5cbd51f53184a4c35d7c8f2dc173f8e63407dcf53'}
counts={}
for name,h in old.items():
 root=E/name;assert sha(root/'SHA256SUMS')==h;count=0
 for line in (root/'SHA256SUMS').read_text().splitlines():
  expected,p=line.split('  ',1);assert sha(root/p)==expected,(name,p);count+=1
 counts[name]=count
formula=json.loads((R/'data/formula.json').read_text())
for p,h in formula['hashes'].items():assert sha(Path(p))==h
assert sha(E/'low_split_compact.cpp')=='1fb043a5d29fa86047ba05cae86fdfb248e6069bc6731c4ee39c181737319303'
replay=json.loads((R/'data/replay/result.json').read_text());assert replay['status']=='PASS' and replay['stable_inputs']
assert replay['before']==replay['after']
assert (R/'data/replay/cake.stdout').read_text().splitlines()==['s VERIFIED UNSAT']
assert 'ActiveState=inactive' in (R/'data/unit-final.txt').read_text()
for directory,name,expected in [('low15-n7-a','parent-heap550-cake.log','CakeML heap space exhausted.'),
 ('low15-replay-a','parent-heap900-cake.log','CakeML heap space exhausted.'),
 ('low15-replay-b','parent-heap1400-cake.log','s VERIFIED UNSAT')]:
 src=W/directory/'cake.log';data=src.read_bytes();assert expected in data.decode().splitlines()
 with (R/'data'/name).open('xb') as f:f.write(data)
result={'status':'PASS','label':'CERTIFIED','statement':'T7 through left15 with explicit lower-size dependencies',
 'frozen_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'old_manifest_hashes':old,
 'old_files_rechecked_unchanged':counts,'formula':formula,'replay':{k:v for k,v in replay.items() if k not in ('before','after')},
 'unit_inactive':True,'temporary_reservation_MiB_released':1650,'capacity_and_left16_not_claimed':True}
with (R/'data/completion.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
 for p in files:f.write(f'{sha(p)}  {p.relative_to(R)}\n')
print(json.dumps({'status':'PASS','files':len(files),'manifest_sha256':sha(R/'SHA256SUMS'),'old_files_unchanged':counts}))
