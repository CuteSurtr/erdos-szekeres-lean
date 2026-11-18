#!/usr/bin/env python3
import datetime
import hashlib
import json
from pathlib import Path
import resource
import shutil

resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
E=Path(__file__).resolve().parents[2]
R=E/'low_split_audit'
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1 << 20),b''):h.update(b)
    return h.hexdigest()

def save(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')

prior={}
for name in ('audit','subset_audit','exact_audit','exact_audit/replay13','protection_audit','highsplit_audit','terminal5_audit','terminal12_audit'):
    p=E/name/'SHA256SUMS';lines=p.read_text().splitlines()
    for line in lines:
        expected,rel=line.split('  ',1);assert sha(p.parent/rel)==expected,(name,rel)
    prior[name]={'manifest_sha256':sha(p),'files_unchanged':len(lines)}
save(R/'data/prior-packets-unchanged.json',prior)
paths=[E/'low_split_cnf.cpp',E/'low_split_compact.cpp',E.parents[1]/'compact/compact_cnf.cpp',
       E/'structure2/low_split.md',E/'structure2/data/low_split_controls.json',
       E/'structure2/data/low_classification_replay.json',E/'audit/VERIFY_EXTENSION.md',
       E/'audit/data/replay-n7m12.json',E/'exact_audit/replay13/data/result.json',
       E.parent/'boundary/audit/VERIFY_BOUNDARY.md',E.parent/'boundary/audit/data/replay-n7.json']
for m in (11,12,13,14):
    case=W/f'low{m}-n7-{"b" if m==14 else "a"}'
    paths.extend(case/p for p in ('result.json','cake.log','cake.time'))
paths.extend(W/'low14-replay-a'/p for p in ('result.json','cake.log','cake.time'))
snapshots={}
for p in paths:
    isrepo=p.is_relative_to(E.parents[1]);rel=p.relative_to(E.parents[1]) if isrepo else p.relative_to(W)
    dest=R/'data/snapshots'/('repo' if isrepo else 'scratch')/rel
    dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists()
    shutil.copyfile(p,dest);assert sha(p)==sha(dest)
    snapshots[str(p)]={'snapshot':str(dest.relative_to(R)),'sha256':sha(dest)}
parents={str(m):json.loads((R/'data'/f'parent-{"compact" if m==14 else "direct"}-{m}.json').read_text()) for m in (11,12,13,14)}
controls={name:json.loads((R/'data'/f'control-{name}.json').read_text())
          for name in ('algebra','small6','small7','small8','left11','left12','left13','left14')}
assert all(v['status']=='PASS' for v in list(parents.values())+list(controls.values()))
certs=json.loads((R/'data/parent-certificate-provenance.json').read_text());assert certs['status']=='PASS'
result={'status':'PASS','label':'PROVED encoder/projection; COMPUTED row/geometry controls; parent CERTIFIED artifacts pinned',
        'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'parent_instances':parents,'controls':controls,'certificate_provenance':certs,
        'native_instances_checked':14,'all_full_selector_assignments_compared':sum(v.get('all_selector_assignments_compared',0) for v in controls.values()),
        'n7_left_through13_supported':True,
        'left_through10_dependency':'Admissible low join to three-cup has at most13 total; separate boundary<=11, generic12, exact13 results.',
        'left11_12_13_dependency':'Individual parent accepted proofs plus this independent formula/projection audit.',
        'unrestricted_all_size_low_split_claim':False,'fresh_LRAT_replays_here':0,
        'extra_heap_reserved':False,'jobs_active':False,'snapshots':snapshots,'prior_packets':prior,
        'limits':{'AS_MiB':300,'compile_AS_MiB':500,'CPUs':1,'wall_seconds_per_job':20}}
save(R/'data/result.json',result)
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
    for p in files:f.write(sha(p)+'  '+str(p.relative_to(R))+'\n')
print(json.dumps({'status':'PASS','files':len(files),'bytes':sum(p.stat().st_size for p in files),
                  'manifest_sha256':sha(R/'SHA256SUMS'),'left_through13_supported':True,'fresh_replays':0}))
