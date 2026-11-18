#!/usr/bin/env python3
import datetime,json
import audit as A
R=A.R;E=A.E
manifest=E/'highsplit_audit/SHA256SUMS'
assert A.sha(manifest)=='dbf403074130a992c987858bb4112344099b43bcadf55e9078a394ebb9b34bef'
count=0
for line in manifest.read_text().splitlines():
 h,name=line.split('  ',1);assert A.sha(manifest.parent/name)==h;count+=1
result=json.loads((R/'data/result.json').read_text());assert result['status']=='PASS'
assert {k:A.sha(p) for k,p in A.FILES.items()}==A.EXPECTED
A.save('completion.json',{'status':'PASS','label':'COMPUTED with written exact restricted projection',
 'frozen_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'old_highsplit_files_unchanged':count,
 'old_manifest_sha256':A.sha(manifest),'CNF_sha256':A.EXPECTED['output'],'proof_replayed':False,
 'extra_hypothesis':'no six-cup','unrestricted_m14_claim':False,'AS_MiB':300,'CPU_count':1,'no_job_remaining':True})
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
 for p in files:f.write(f'{A.sha(p)}  {p.relative_to(R)}\n')
print(json.dumps({'status':'PASS','files':len(files),'manifest_sha256':A.sha(R/'SHA256SUMS')}))
