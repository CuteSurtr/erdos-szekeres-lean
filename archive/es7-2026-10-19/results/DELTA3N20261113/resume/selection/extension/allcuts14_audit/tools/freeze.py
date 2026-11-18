#!/usr/bin/env python3
import datetime,json
from pathlib import Path
import check_rows as C
R=C.R;E=R.parent
frozen={'highsplit_audit':'dbf403074130a992c987858bb4112344099b43bcadf55e9078a394ebb9b34bef',
 'low_split_audit':'8609cc06302c622b3f37014c27334ba142bb535b86e528aa654217e9959303c3',
 'low_split_audit/replay':'159ac6c8386dbf78f2e63481bc3e4f659fe72e8c2c1456616db81729d79f298e',
 'exact_audit/replay13':'b501ec428762c70347a44de66b6bfd201fad191b82d20411e831faaeef166314'}
counts={}
for name,h in frozen.items():
 root=E/name;manifest=root/'SHA256SUMS';assert C.sha(manifest)==h
 count=0
 for line in manifest.read_text().splitlines():
  expected,p=line.split('  ',1);assert C.sha(root/p)==expected,(name,p);count+=1
 counts[name]=count
rows=json.loads((R/'data/rows.json').read_text());real=json.loads((R/'data/real-controls.json').read_text())
assert rows['status']==real['status']=='PASS'
run=Path('/home/jay/research/data/delta3-codex-20261113/extension/allcuts14-a/result.json')
receipt=json.loads(run.read_text());C.save('parent-search-snapshot.json',receipt)
assert receipt['hashes']['input.cnf']==C.EXPECTED['output']
assert C.sha(run.parent/'input.cnf')==C.EXPECTED['output']
deps=[E/'audit/VERIFY_EXTENSION.md',E/'audit/data/replay-n7m12.json',E.parent/'boundary/audit/VERIFY_BOUNDARY.md',
 E/'structure2/cup_join.md',E/'structure2/low_split.md']
C.save('completion.json',{'status':'PASS','labels':['COMPUTED rows and controls','PROVED written real-counterexample implication with explicit dependencies'],
 'frozen_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cnf_sha256':C.EXPECTED['output'],
 'frozen_manifest_hashes':frozen,'frozen_files_rechecked_unchanged':counts,'dependency_hashes':{str(p):C.sha(p) for p in deps},
 'parent_search_status':receipt['status'],'matching_combined_proof_replayed':False,'AS_MiB':300,'CPU_count':1,
 'scope':'n7/m14 combined cut formula; T7 through left14 is supplied separately by low_split_audit/replay'})
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
 for p in files:f.write(f'{C.sha(p)}  {p.relative_to(R)}\n')
print(json.dumps({'status':'PASS','files':len(files),'manifest_sha256':C.sha(R/'SHA256SUMS'),'parent_search':receipt['status']}))
