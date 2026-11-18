#!/usr/bin/env python3
import datetime
import hashlib
import json
from pathlib import Path
import resource
import shutil

resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
E=Path(__file__).resolve().parents[2]
R=E/'terminal12_audit'
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1 << 20),b''):h.update(b)
    return h.hexdigest()

def save(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')

prior={}
for name in ('audit','subset_audit','exact_audit','exact_audit/replay13','protection_audit','highsplit_audit','terminal5_audit'):
    p=E/name/'SHA256SUMS';lines=p.read_text().splitlines()
    for line in lines:
        expected,rel=line.split('  ',1);assert sha(p.parent/rel)==expected,(name,rel)
    prior[name]={'manifest_sha256':sha(p),'files_unchanged':len(lines)}
save(R/'data/prior-packets-unchanged.json',prior)
paths=[E/'terminal_general.cpp',E.parents[1]/'compact/compact_cnf.cpp',
       E/'audit/check.py',E/'audit/VERIFY_EXTENSION.md',E/'terminal15/data/balanced.json']
boundary=E.parent/'boundary/audit'
paths.extend(boundary/p for p in ('VERIFY_BOUNDARY.md','data/replay-n6.json','data/replay-n6.log'))
for case in range(4):paths.extend(W/'descend15-a'/str(case)/p for p in ('points.txt','result.json','terminal.cnf'))
paths.extend(W/'descend15-a/3/certificate'/p for p in ('result.json','proof.blrat','proof.blrat.zst'))
for m in (10,11):paths.extend([W/f'n6m{m}-terminal.cnf',W/f'n6m{m}-terminal.cnf.map',W/f'terminal6m{m}-a/result.json'])
snapshots={}
for p in paths:
    isrepo=p.is_relative_to(E.parents[1]);rel=p.relative_to(E.parents[1]) if isrepo else p.relative_to(W)
    dest=R/'data/snapshots'/('repo' if isrepo else 'scratch')/rel
    dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists()
    shutil.copyfile(p,dest);assert sha(p)==sha(dest)
    snapshots[str(p)]={'snapshot':str(dest.relative_to(R)),'sha256':sha(dest)}
check=json.loads((R/'data/check-result.json').read_text());assert check['status']=='PASS'
replays={str(m):json.loads((R/'data'/f'replay-m{m}.json').read_text()) for m in (10,11,12)}
assert all(v['status']=='PASS' and v['label']=='CERTIFIED' and v['exact_verdict_line'] and v['stable_inputs'] for v in replays.values())
result={'status':'PASS','label':'CERTIFIED components; PROVED minimum deduction',
        'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'statement':'The global minimum cardinality of a terminal-safe n6 counterexample among real x-ordered GP sets with no five-cap and no convex hexagon is exactly12.',
        'global_minimum':12,'property':'terminal-safe weak Delta','n':6,
        'ordinary_weak_deltas_in_witness':945,'ordinary_weak_minimum_size':4,
        'lower_bound_dependencies':{'through9':check['through9'],'exact10':replays['10'],'exact11':replays['11']},
        'upper_bound':{'fixed_geometry_membership':check['fixed']['3'],'certificate':replays['12']},
        'checks':check,'replays':replays,'snapshots':snapshots,'prior_packets':prior,
        'selection_monotonicity_used':False,'weak_delta_or_ES_refutation_claimed':False,
        'jobs_active':False,'extra_heap_reserved':False,'unresolved_obligations':[],
        'limits':{'AS_MiB':300,'CPUs':1,'wall_seconds_per_job':20,'heap_MiB':64,'stack_MiB':32}}
save(R/'data/result.json',result)
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
    for p in files:f.write(sha(p)+'  '+str(p.relative_to(R))+'\n')
print(json.dumps({'status':'PASS','global_terminal_n6_minimum':12,'files':len(files),
                  'bytes':sum(p.stat().st_size for p in files),'manifest_sha256':sha(R/'SHA256SUMS'),
                  'prior_packets_unchanged':list(prior)}))
