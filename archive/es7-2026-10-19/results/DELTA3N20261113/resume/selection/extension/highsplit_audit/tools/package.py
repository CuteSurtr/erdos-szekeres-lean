#!/usr/bin/env python3
"""Freeze only the owned m14 audit; verify earlier manifests read-only."""
import datetime
import hashlib
import json
from pathlib import Path
import resource
import shutil

resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
E = Path(__file__).resolve().parents[2]
R = E/'highsplit_audit'
W = Path('/home/jay/research/data/delta3-codex-20261113/extension')

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1 << 20),b''):
            h.update(b)
    return h.hexdigest()

def write(p,obj):
    with p.open('x') as f:
        json.dump(obj,f,indent=2)
        f.write('\n')

prior = {}
for name in ('subset_audit','exact_audit','exact_audit/replay13','protection_audit'):
    root = E/name
    manifest = root/'SHA256SUMS'
    entries = manifest.read_text().splitlines()
    for line in entries:
        expected,rel = line.split('  ',1)
        assert sha(root/rel)==expected,(name,rel)
    prior[name] = {'manifest_sha256':sha(manifest),'files_checked_unchanged':len(entries)}
write(R/'data/prior-packets-unchanged.json',prior)
snapshots = {}
paths = [E/'augment_exact.py',E/'augment_indecomposable.py',
         E/'structure2/highsplit_reduction.md',E/'structure2/separated_theorem.md',
         E/'structure2/data/highsplit_cases.json',E.parent/'terminal/data/witness.points',
         E/'exact_audit/replay13/data/result.json',
         *(W/(name+'.cnf.json') for name in ('n7m14-exact','n7m14-indecomp','n7m14-indecomp-v2'))]
for p in paths:
    category = 'repo' if p.is_relative_to(E.parent) else 'scratch'
    rel = p.relative_to(E.parent) if category=='repo' else p.relative_to(W)
    dest = R/'data/snapshots'/category/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    assert not dest.exists()
    shutil.copyfile(p,dest)
    assert sha(p)==sha(dest)
    snapshots[str(p)] = {'snapshot':str(dest.relative_to(R)),'sha256':sha(dest)}
state = json.loads((W/'indecomp14-a/result.json').read_text())
write(R/'data/parent-indecomp14-at-handoff.json',state)
rows = json.loads((R/'data/rows-run02/rows-result.json').read_text())
controls = {mode:json.loads((R/'data'/('controls-'+mode+'.json')).read_text())
            for mode in ('small','m14','negative19')}
assert rows['status']=='PASS' and all(v['status']=='PASS' for v in controls.values())
result = {'status':'PASS','label':'PROVED written projection/reduction; COMPUTED instance and integer controls',
          'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'rows':rows,'control_summaries':{k:{x:v for x,v in c.items() if x not in
              ('results','P','input_sha256','left_selection','lifted_selection')} for k,c in controls.items()},
          'explicit_prior_dependencies':prior,'source_snapshots':snapshots,
          'cnf_sha256':{p.name:sha(p) for p in
              (W/'n7m14-exact.cnf',W/'n7m14-indecomp.cnf',W/'n7m14-indecomp-v2.cnf')},
          'parent_conditional_status_at_handoff':state.get('status'),
          'm14_certificate_replayed':False,'new_heap_reserved':False,
          'last_cut_premise':'terminal-safe existence at exactly size13',
          'negative_control_dependency_links':['../../terminal/README.md','../subset_audit/VERIFY_SUBSETS.md'],
          'retained_failure':'First row-check attempt rejected padded DIMACS header; corrected token parser passed with all body bytes still compared literally.',
          'owned_jobs_active':False,'resources':{'AS_MiB':300,'CPUs':1,'wall_seconds_per_check':20,'CPU_seconds':19}}
write(R/'data/result.json',result)
files = sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
    for p in files:
        f.write(sha(p)+'  '+str(p.relative_to(R))+'\n')
print(json.dumps({'status':'PASS','files':len(files),'bytes':sum(p.stat().st_size for p in files),
                  'manifest_sha256':sha(R/'SHA256SUMS'),'prior_packets':prior,
                  'parent_status':state.get('status')}))
