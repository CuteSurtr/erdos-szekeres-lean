#!/usr/bin/env python3
import datetime,hashlib,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R.parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def save(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n')
rep=json.loads((R/'data/retryB/result.json').read_text())
assert rep['status']=='PASS' and rep['stable_inputs'] and rep['before']==rep['after']
assert rep['cake']['returncode']==0 and rep['cake']['exact_acceptance_line']
assert (R/'data/retryB/cake.stdout').read_text().splitlines()==['s VERIFIED UNSAT']
assert rep['cake']['final_memory']['swap']==0
unit=(R/'data/retryB-unit-final.txt').read_text()
assert all(s in unit for s in ['ActiveState=inactive','MainPID=0','Result=success','ExecMainStatus=0'])
old={'low_split_audit':'8609cc06302c622b3f37014c27334ba142bb535b86e528aa654217e9959303c3',
'low_split_audit/replay':'159ac6c8386dbf78f2e63481bc3e4f659fe72e8c2c1456616db81729d79f298e',
'low_split_audit/left15':'1ac9e0133d42a02c2b423d3dda39b5ce985d1f95486c6599449fa31c99cab0ca',
'low_split_audit/left16_longcup':'d68a01f9195b965372eefae14d4f5e358067ce017e9d51745ecb889b3282c892',
'exact_audit/replay13':'b501ec428762c70347a44de66b6bfd201fad191b82d20411e831faaeef166314'}
counts={}
for name,h in old.items():
 root=E/name;assert sha(root/'SHA256SUMS')==h;count=0
 for line in (root/'SHA256SUMS').read_text().splitlines():
  expected,p=line.split('  ',1);assert sha(root/p)==expected,(name,p);count+=1
 counts[name]=count
cap=E/'low_split/capacity_checks/pass';c=json.loads((cap/'Capacity16.json').read_text())
assert c['exit_code']==0 and c['stop_reason'] is None
assert len(c['axiom_reports'])==3 and all(set(v)=={'propext','Classical.choice','Quot.sound'} for v in c['axiom_reports'].values())
assert sha(E/'low_split/Capacity16.lean')==c['source_sha256']=='8d5ced5ab84da9ba9347bc4fd1f99952dfa876302c35a712e9e8fec284a003d3'
assert json.loads((cap/'result.json').read_text())['status']=='PASS'
assert sha(cap/'result.json')==sha(R/'data/capacity-pass-result.json')
cap_hashes={str(p):sha(p) for p in [E/'low_split/Capacity16.lean',cap/'Capacity16.json',cap/'Capacity16.log',cap/'result.json']}
for name in ['Capacity16.json','Capacity16.log']:shutil.copyfile(cap/name,R/'data'/name)
save(R/'data/completion.json',dict(status='PASS',label='CERTIFIED original16; PROVED written all-left T7 closure with dependencies',frozen_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),clean_retry='data/retryB/result.json',original16_formula_audit='../left16_longcup',old_manifests=old,old_files_rechecked_unchanged=counts,capacity_parent_evidence=cap_hashes,capacity_fresh_own_Lean_replay=False,explicit_sizes='<=10 via full<=13; individual11,12,13,14,15,16; capacity excludes>=17',attemptA='accepted checker line with failed telemetry wrapper, preserved',unit_inactive=True,released_MiB=3100,limits=dict(packaging_AS_MiB=150,CPU_count=1,wall_seconds=20,cpu_seconds=19)))
files=sorted(p for p in R.rglob('*') if p.is_file() and p!=R/'SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
 for p in files:f.write(sha(p)+'  '+str(p.relative_to(R))+'\n')
print(json.dumps(dict(status='PASS',files=len(files),manifest_sha256=sha(R/'SHA256SUMS'),old_files_unchanged=counts,active_own_large_unit=False)))
