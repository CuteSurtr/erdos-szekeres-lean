#!/usr/bin/env python3
"""Freeze this audit without writing either completed neighboring scope."""
from datetime import datetime, timezone
import json
from pathlib import Path
import resource

from geometry import digest

HERE=Path(__file__).resolve().parent
DATA=HERE/'data'
ROOT=Path('/home/jay/research/data/delta3-codex-20261113/extension')


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f:json.dump(value,f,indent=2);f.write('\n')


def copy(source,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f:f.write(source.read_bytes())
    assert digest(source)==digest(target)


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    previous={}
    for scope in ('audit','cardinality'):
        directory=HERE.parent/scope;manifest=directory/'SHA256SUMS';count=0
        for line in manifest.read_text().splitlines():
            expected,relative=line.split('  ',1)
            assert digest(directory/relative)==expected,(scope,relative)
            count+=1
        previous[scope]={'manifest_sha256':digest(manifest),'files_checked':count,'unchanged':True}
    model=json.loads((DATA/'model.json').read_text());assert model['status']=='PASS'
    real=json.loads((DATA/'real15.geometry.json').read_text());assert real['status']=='PASS'
    certificate=json.loads((DATA/'membership.json').read_text());assert certificate['label']=='CERTIFIED'
    assert all(r['minimum_size'] is not None and r['minimum_size']<=4 for r in real['result']['rooted_weak_deltas'])
    triples={tuple(r['weak_delta']) for r in real['result']['rooted_weak_deltas'] if r['minimum_size']==3}
    assert len(triples)==real['result']['weak_delta_size_counts']['3']==4
    external={Path(p) for p in model['input_hashes']}
    external.update(Path(p) for p in certificate['before'])
    external.add(Path(real['input']))
    for paths in (model['input_hashes'],certificate['before']):
        for p,sha in paths.items():assert digest(p)==sha
    assert digest(real['input'])==real['input_sha256']
    for relative in ('witness.terminal.cnf','fresh.blrat','fresh.blrat.zst','certificate.json'):
        p=ROOT/'terminal15'/relative;copy(p,DATA/'certificate'/relative);external.add(p)
    copy(ROOT/'terminal7-a/m15/solve/cadical.log',DATA/'model15.cadical.log')
    for relative in ('encode.json','solve/result.json'):
        p=ROOT/'terminal7-a/m15'/relative;copy(p,DATA/'source'/relative);external.add(p)
    # Pin reviewed encoders as provenance, without importing them.
    for source,target in ((HERE.parent/'terminal_general.cpp',DATA/'source/terminal_general.cpp'),
                          (HERE.parent.parent.parent/'compact/compact_cnf.cpp',DATA/'source/compact_cnf.cpp')):
        copy(source,target);external.add(source)
    with (DATA/'orientation.signs').open('x') as f:f.write(real['result']['signs']+'\n')
    save(DATA/'weak-witnesses.json',{'label':'COMPUTED exact positive witnesses',
         'ordinary_triples':sorted(triples),'rooted':real['result']['rooted_weak_deltas'],
         'coordinate_sha256':digest(DATA/'real15.coordinates.json')})
    save(DATA/'inputs.json',{'external_files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(external)],
                            'frozen_neighbor_checks':previous,
                            'generic_partial_LRAT':'Not read or used; a SAT solver trace is not an UNSAT certificate.'})
    save(DATA/'failures.json',{'mathematical_failures':[],'resource_failures':[],'rejected_replays':[],
         'preserved_preliminary_unknown':'GP_PASS did not establish real realizability; retained in gp.json before the exact coordinate replay.',
         'scope':'Parent subset and uniform/cup tasks not duplicated.'})
    save(DATA/'summary.json',{'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'COMPLETE',
         'generic_model':'COMPUTED all variables, clauses, auxiliary semantics and subsets checked',
         'realization':'COMPUTED independent exact integer/hull replay',
         'membership':'CERTIFIED by fresh independent cake_lpr replay',
         'm':15,'n':7,'five_caps':0,'convex_seven_subsets':0,'terminal_safe_deltas':0,
         'four_caps':48,'bad_triples':78,'convex_six_subsets':187,'subsets_checked':32768,
         'weak_deltas':4805,'weak_triples':sorted(triples),'every_root_weak_size_at_most':4,
         'membership_variables':15,'membership_clauses':313,'global_minimality':'NOT CLAIMED',
         'uniform_envelope_scope':'NOT CHECKED HERE','frozen_neighbor_checks':previous,
         'running_jobs':False,'shared_manifests_changed':False})
    files=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
    with (HERE/'SHA256SUMS').open('x') as f:
        for p in files:f.write(f'{digest(p)}  {p.relative_to(HERE)}\n')
    print(json.dumps({'status':'SEALED','local_files':len(files),'external_files':len(external),'previous_scopes_unchanged':True}))


if __name__=='__main__':main()
