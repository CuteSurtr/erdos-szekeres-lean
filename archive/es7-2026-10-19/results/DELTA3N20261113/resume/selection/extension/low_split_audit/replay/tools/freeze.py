#!/usr/bin/env python3
import datetime,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
old=R.parent/'SHA256SUMS'
assert sha(old)=='8609cc06302c622b3f37014c27334ba142bb535b86e528aa654217e9959303c3'
checked=0
for line in old.read_text().splitlines():
 expected,name=line.split('  ',1);assert sha(R.parent/name)==expected,name;checked+=1
cases={str(m):json.loads((R/'data'/f'm{m}'/'result.json').read_text()) for m in range(11,15)}
for m,x in cases.items():
 assert x['status']=='PASS' and x['label']=='CERTIFIED' and x['stable_inputs']
 assert (R/'data'/f'm{m}'/'cake.stdout').read_text().splitlines()==['s VERIFIED UNSAT']
 assert x['before']==x['after']
assert 'ActiveState=inactive' in (R/'data/unit-final.txt').read_text()
result={'status':'PASS','label':'CERTIFIED','claim':'T7(L) through left size14 with explicit separate lower coverage',
 'individual_sizes':[11,12,13,14],'old_frozen_manifest_sha256':sha(old),'old_files_unchanged':checked,
 'temporary_extra_MiB_released':400,'unit_inactive':True,'frozen_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'cases':{k:{a:v[a] for a in ('cnf_sha256','proof_sha256','AS_MiB','heap_MiB','total_seconds','cake')} for k,v in cases.items()}}
with (R/'data/completion.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
 for p in files:f.write(f'{sha(p)}  {p.relative_to(R)}\n')
print(json.dumps({'status':'PASS','files':len(files),'old_files_unchanged':checked,'manifest_sha256':sha(R/'SHA256SUMS')}))
