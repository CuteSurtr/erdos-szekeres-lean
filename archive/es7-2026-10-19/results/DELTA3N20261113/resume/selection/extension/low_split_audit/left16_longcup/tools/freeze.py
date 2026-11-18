#!/usr/bin/env python3
import datetime,json
import audit as A
R=A.R;E=A.E
old={'low_split_audit':'8609cc06302c622b3f37014c27334ba142bb535b86e528aa654217e9959303c3',
 'highsplit_audit':'dbf403074130a992c987858bb4112344099b43bcadf55e9078a394ebb9b34bef',
 'low_split_audit/left15':'1ac9e0133d42a02c2b423d3dda39b5ce985d1f95486c6599449fa31c99cab0ca',
 'cup_bound14_audit':'36a3f3debf6dcc0ba27a528007a6aa639a220d4526690ac2fc3177996b4c6c5a'}
counts={}
for name,h in old.items():
 root=E/name;assert A.sha(root/'SHA256SUMS')==h;count=0
 for line in (root/'SHA256SUMS').read_text().splitlines():
  expected,p=line.split('  ',1);assert A.sha(root/p)==expected,(name,p);count+=1
 counts[name]=count
result=json.loads((R/'data/result.json').read_text());assert result['status']=='PASS'
assert {k:A.sha(p) for k,p in A.FILES.items()}==A.EXPECTED
A.save('completion.json',{'status':'PASS','labels':['COMPUTED complete base/append rebuild and controls','PROVED written real-failure projection'],
 'frozen_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'old_manifest_hashes':old,'old_files_unchanged':counts,
 'CNF_sha256':A.EXPECTED['output'],'base_CNF_sha256':A.EXPECTED['base'],'base_full_instance_audited':True,
 'proof_replayed':False,'finite_left16_theorem_claimed':False,'all_left_sizes_claimed':False,
 'audit_AS_MiB':300,'packaging_AS_MiB':150,'CPU_count':1,'no_job_remaining':True,
 'lemma_uses_capacity_or_earlier_finite_terminal_result':False})
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
 for p in files:f.write(f'{A.sha(p)}  {p.relative_to(R)}\n')
print(json.dumps({'status':'PASS','files':len(files),'manifest_sha256':A.sha(R/'SHA256SUMS')}))
