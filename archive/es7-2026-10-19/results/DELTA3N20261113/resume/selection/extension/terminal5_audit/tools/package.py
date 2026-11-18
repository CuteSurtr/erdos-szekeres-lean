#!/usr/bin/env python3
import datetime
import hashlib
import json
from pathlib import Path
import resource
import shutil

resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
E=Path(__file__).resolve().parents[2]
R=E/'terminal5_audit'
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1 << 20),b''):h.update(b)
    return h.hexdigest()

def save(p,v):
    with p.open('x') as f:
        json.dump(v,f,indent=2)
        f.write('\n')

prior={}
for name in ('audit','subset_audit','exact_audit','exact_audit/replay13','protection_audit','highsplit_audit'):
    p=E/name/'SHA256SUMS'
    lines=p.read_text().splitlines()
    for line in lines:
        expected,rel=line.split('  ',1)
        assert sha(p.parent/rel)==expected,(name,rel)
    prior[name]={'manifest_sha256':sha(p),'files_unchanged':len(lines)}
save(R/'data/prior-packets-unchanged.json',prior)
paths=[E/'terminal_general.cpp',E.parents[1]/'compact/compact_cnf.cpp',
       E/'audit/check.py',E/'audit/VERIFY_EXTENSION.md']
for m,tag in ((7,'terminal5m7-a'),(8,'terminal5m8-a'),(9,'base5m9-a')):
    kind='base' if m==9 else 'terminal'
    paths.extend([W/f'n5m{m}-{kind}.cnf',W/f'n5m{m}-{kind}.cnf.map',
                  W/tag/'result.json',W/tag/'proof.blrat.zst'])
snapshots={}
for p in paths:
    isrepo=p.is_relative_to(E.parents[1])
    rel=p.relative_to(E.parents[1]) if isrepo else p.relative_to(W)
    dest=R/'data/snapshots'/('repo' if isrepo else 'scratch')/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    assert not dest.exists()
    shutil.copyfile(p,dest)
    assert sha(p)==sha(dest)
    snapshots[str(p)]={'snapshot':str(dest.relative_to(R)),'sha256':sha(dest)}
formula=json.loads((R/'data/formula-result.json').read_text())
assert formula['status']=='PASS'
replays={str(m):json.loads((R/'data'/f'replay-m{m}.json').read_text()) for m in (7,8,9)}
assert all(v['status']=='PASS' and v['label']=='CERTIFIED' and v['exact_acceptance_line']
           and v['stable_inputs'] for v in replays.values())
result={'status':'PASS','label':'CERTIFIED finite components; PROVED all-size deduction',
        'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'statement':'Every finite real x-ordered GP set with no five-cap and no convex pentagon admits a terminal-safe weak Delta for n=5.',
        'deduction':{'m_le_6':'Cup A of size max(0,m-3); at m6 no-five-cap gives a cup triple.',
                     'm7':'Independently audited and replayed terminal certificate.',
                     'm8':'Separate independently audited and replayed terminal certificate.',
                     'm_ge_9':'Pure-base9 certificate plus heredity of geometric premises.'},
        'selection_monotonicity_used':False,'withdrawn_m7_shortcut_used':False,
        'formula_audit':formula,'replays':replays,'snapshots':snapshots,'prior_packets':prior,
        'resources':{'AS_MiB':300,'CPUs':1,'wall_seconds_per_job':20,'heap_MiB':128,'stack_MiB':32},
        'jobs_active':False,'extra_heap_reserved':False,'unresolved_obligations':[]}
save(R/'data/result.json',result)
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
    for p in files:f.write(sha(p)+'  '+str(p.relative_to(R))+'\n')
print(json.dumps({'status':'PASS','files':len(files),'bytes':sum(p.stat().st_size for p in files),
                  'manifest_sha256':sha(R/'SHA256SUMS'),'all_three_fresh_cake_verdicts':True,
                  'prior_packets_unchanged':list(prior)}))
