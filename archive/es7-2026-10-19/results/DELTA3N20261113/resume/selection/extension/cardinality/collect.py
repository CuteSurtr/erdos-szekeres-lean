#!/usr/bin/env python3
"""Freeze this task's small evidence and verify the previous audit is untouched."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource

HERE=Path(__file__).resolve().parent
DATA=HERE/'data'
SCRATCH=Path('/home/jay/research/data/delta3-codex-20261113/extension/cardinality')


def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f:json.dump(value,f,indent=2);f.write('\n')


def copy(source,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f:f.write(source.read_bytes())
    assert digest(source)==digest(target)


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    audit=HERE.parent/'audit';manifest=audit/'SHA256SUMS'
    files=0
    for line in manifest.read_text().splitlines():
        expected,relative=line.split('  ',1)
        assert digest(audit/relative)==expected,(relative,'previous audit changed')
        files+=1
    audit_check={'manifest_sha256':digest(manifest),'files_checked':files,'unchanged':True}
    external=set();searches=[]
    for name in ('terminal18','compact16','star12'):
        report=json.loads((DATA/f'{name}.search.json').read_text());searches.append(report)
        source=Path(report['source']['path']);trace=Path(report['trace'])
        assert digest(source)==report['source']['sha256'] and digest(trace)==report['trace_sha256']
        copy(source,DATA/f'source/{name}.json');copy(trace,DATA/f'failed_tries/{name}.tries.tsv')
        external.update((source,trace))
    discovery=json.loads((DATA/'realize.json').read_text());source=Path(discovery['source'])
    assert digest(source)==discovery['source_sha256']
    copy(source,DATA/'source/n7m11k2-cadical.log');external.add(source)
    controls=json.loads((DATA/'controls.json').read_text());p=Path(controls['boundary_control_source'])
    assert digest(p)==controls['boundary_control_sha256']
    copy(p,DATA/'source/boundary-control.json');external.add(p)
    final=DATA/'simple11.candidate.json';copy(final,DATA/'witness.json')
    raw=json.loads(final.read_text());P=raw['P']
    with (DATA/'witness.points').open('x') as f:
        f.write('11 7\n');f.writelines(f'{x} {y}\n' for x,y in P)
    for name in ('sat11','simple11','family-low','family-high'):
        report=json.loads((DATA/f'{name}.verify.json').read_text())
        assert report['status']=='PASS'
        assert digest(Path(report['input']))==report['input_sha256']
        assert digest(HERE/'verify.py')==report['checker_sha256']
    endpoint=json.loads((DATA/'family-endpoints.verify.json').read_text());assert endpoint['status']=='PASS'
    write(DATA/'inputs.json',{'external_files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)}
                                               for p in sorted(external)],'previous_audit':audit_check})
    write(DATA/'failures.json',{
        'unsuccessful_coordinate_subsets':sum(r['subsets_examined'] for r in searches),
        'interpretation':'Every listed trial had a pair hitting its convex six-targets; not an all-set obstruction.',
        'numeric_proposals_without_candidate':sum(not a['candidate_available'] for a in discovery['attempts']),
        'numeric_statuses_are_not_evidence':True,
        'failed_rounding_amplitudes':len(json.loads((DATA/'simplify.json').read_text())['failed_roundings']),
        'expected_invalid_controls':controls['controls'],'resource_failures':[],'mathematical_replay_failures':[],
        'path_probe':'An exploratory read of extension/envelope/prepare.py and a root *.py glob found no files; actual tools/ paths were subsequently listed. No computation relied on the missing path.'})
    write(DATA/'summary.json',{
        'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'COMPLETE',
        'label':'COMPUTED exact independent coordinate/hull verification',
        'P':P,'m':11,'n':7,'terminal_delta':[0,1,3],
        'minimum_weak_delta_size':3,'minimum_terminal_safe_delta_size':3,
        'convex_six_subsets':22,'five_caps':0,'seven_gons':0,
        'minimum_absolute_determinant':1,'maximum_cap_cup_convex':[4,5,6],
        'parameter_family':{'p5':'(48,1+t)','open_interval':['-1','8/61'],'others_fixed':True},
        'source_model_realized':True,'ambient_size_minimality':'NOT CLAIMED','all_n_family':'NOT ESTABLISHED',
        'independent_replays':4,'negative_controls':7,'previous_audit':audit_check,
        'running_jobs':False,'shared_manifests_changed':False})
    files=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
    with (HERE/'SHA256SUMS').open('x') as f:
        for p in files:f.write(f'{digest(p)}  {p.relative_to(HERE)}\n')
    print(json.dumps({'status':'SEALED','local_files':len(files),'external_files':len(external),
                      'previous_audit_unchanged':True}))


if __name__=='__main__':main()
