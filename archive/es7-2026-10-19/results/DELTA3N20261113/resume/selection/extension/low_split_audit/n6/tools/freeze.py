#!/usr/bin/env python3
import datetime,hashlib,json,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R.parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
  os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
 return h.hexdigest()
frozen={'low_split_audit':'8609cc06302c622b3f37014c27334ba142bb535b86e528aa654217e9959303c3',
 'low_split_audit/replay':'159ac6c8386dbf78f2e63481bc3e4f659fe72e8c2c1456616db81729d79f298e',
 'terminal12_audit':'329176f456fb210accad89ea1721cee4dedf8aea6e867a16458d8991d6d48d23'}
counts={}
for name,h in frozen.items():
 root=E/name;assert sha(root/'SHA256SUMS')==h;count=0
 for line in (root/'SHA256SUMS').read_text().splitlines():
  expected,p=line.split('  ',1);assert sha(root/p)==expected,(name,p);count+=1
 counts[name]=count
cases={str(m):json.loads((R/f'data/left{m}/result.json').read_text()) for m in (10,11)}
for m,x in cases.items():
 assert x['status']=='PASS' and x['label']=='CERTIFIED' and x['stable_inputs']
 assert (R/f'data/left{m}/cake.stdout').read_text().splitlines()==['s VERIFIED UNSAT']
source=E/'low_split_cnf.cpp'
with (R/'data/source-direct.cpp.txt').open('xb') as f:f.write(source.read_bytes())
dependencies=[E/'terminal12_audit/VERIFY_TERMINAL12.md',E.parent/'boundary/audit/VERIFY_BOUNDARY.md',R.parent/'VERIFY_LOW_SPLIT.md']
result={'status':'PASS','label':'CERTIFIED','statement':'T6 through left11 with separate lower coverage',
 'cases':{k:{a:v[a] for a in ('cnf_sha256','proof_sha256','cake','AS_MiB','total_seconds')} for k,v in cases.items()},
 'capacity_specialization_checked_here':False,'all_left_conclusion_conditional_on_capacity':True,
 'singleton_left_d4_exception_retained':True,'old_manifest_hashes':frozen,'old_files_rechecked_unchanged':counts,
 'dependency_hashes':{str(p):sha(p) for p in dependencies},'no_job_remaining':True,'extra_allocation_MiB':0,
 'frozen_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with (R/'data/completion.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
 for p in files:f.write(f'{sha(p)}  {p.relative_to(R)}\n')
print(json.dumps({'status':'PASS','files':len(files),'manifest_sha256':sha(R/'SHA256SUMS'),'old_files_unchanged':counts}))
