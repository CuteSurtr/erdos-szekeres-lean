#!/usr/bin/env python3
"""Freeze this bounded audit's sources, external evidence and local manifest."""
from datetime import datetime, timezone
import json
from pathlib import Path
import resource

from check import COMPACT, DATA, EXT, HERE, SCRATCH, sha


def save(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f:
        json.dump(value,f,indent=2);f.write('\n')


def copy(source, target):
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f:
        f.write(source.read_bytes())
    assert sha(source)==sha(target)


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    sources = [(EXT/'terminal_general.cpp',HERE/'source/selection/extension/terminal_general.cpp'),
               (EXT/'SOUNDNESS.md',HERE/'source/selection/extension/SOUNDNESS.md'),
               (EXT/'small_delta.py',HERE/'source/selection/extension/small_delta.py'),
               (COMPACT,HERE/'source/compact/compact_cnf.cpp'),
               (COMPACT.with_name('SOUNDNESS.md'),HERE/'source/compact/SOUNDNESS.md')]
    external = set()
    for source,target in sources:
        copy(source,target);external.add(source)
    # Check that the reviewed implementation has not changed since generation.
    expected = json.loads((DATA/'generate-terminal18.json').read_text())['result']
    assert expected['source_sha256']==sha(EXT/'terminal_general.cpp')
    assert expected['compact_sha256']==sha(COMPACT)
    accepted = []
    for n,m in ((7,11),(7,12),(8,13)):
        case = SCRATCH.parent/f'terminal{n}-a/m{m}'
        receipt = json.loads((DATA/f'replay-n{n}m{m}.json').read_text())
        assert receipt['label']=='CERTIFIED' and receipt['exact_acceptance_line']
        for path,digest in receipt['before'].items():
            assert sha(path)==digest
            external.add(Path(path))
        for relative in ('input.cnf.map','encode.json','solve/result.json','solve/cake.log',
                         'solve/cadical.log','solve/proof.lrat.zst'):
            external.add(case/relative)
        for relative in ('encode.json','solve/result.json','solve/cake.log'):
            copy(case/relative, DATA/f'parent/n{n}m{m}'/relative)
        accepted.append({'n':n,'m':m,'label':'CERTIFIED',
                         'receipt':f'data/replay-n{n}m{m}.json',
                         'cnf_sha256':receipt['before'][str(case/'input.cnf')],
                         'proof_sha256':receipt['before'][str(case/'solve/proof.lrat')]})
    filters = json.loads((DATA/'filters.json').read_text())['result']['cases']
    for r in filters:
        case = SCRATCH.parent/f'small-delta/n{r["n"]}m{r["m"]}k{r["k"]}'
        for relative in ('input.cnf','encode.json','solve/result.json'):
            external.add(case/relative)
        copy(case/'solve/result.json',DATA/f'parent/small-n{r["n"]}m{r["m"]}k{r["k"]}.json')
    external.add(SCRATCH.parent/'small-delta/n7m11k2/solve/cadical.log')
    external.update(p for p in SCRATCH.rglob('*') if p.is_file())
    for f in json.loads((DATA/'fixtures.json').read_text()):
        p = Path(f['source']);assert sha(p)==f['source_sha256'];external.add(p)
    records = [{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(external)]
    save(DATA/'inputs.json',{'label':'COMPUTED provenance','files':records})
    save(DATA/'failures.json',{
        'mathematical_control_failures':[], 'resource_failures':[], 'rejected_replays':[],
        'compiler_warning':'Unused archived_compact_main reaches end of non-void function; retained in compile.log.',
        'initial_probe':'One ls invocation returned 2 before extension directories were created; no result used.',
        'expected_rejections':'Six out-of-domain inputs, flipped exact flags, missing-premise and too-short cover controls.',
        'parent_unknowns':[{'n':r['n'],'m':r['m'],'k':r['k']} for r in filters if r['parent_status']=='UNKNOWN']})
    save(DATA/'summary.json',{
        'completed_utc':datetime.now(timezone.utc).isoformat(),'status':'COMPLETE',
        'written_projection':'PROVED within stated signotope geometry',
        'independent_certificates':accepted,
        'consequence':'Together with previous coverage through 11, terminal-safe weak Delta exists through 12 old points at n=7.',
        'eighteen_point_fixed_real_control':'COMPUTED exact canonical model; every clause and all subsets checked.',
        'small_cardinality':'All six filters checked; n7m11k2 abstract model minimum terminal size 3; five UNKNOWNs retained.',
        'scope_exclusions':['later parent sweep outcomes','real realizability of small abstract SAT model',
                            'other extension tracks','general all-size selection','new ES bound','Lean proof'],
        'audit_jobs_running':False,'shared_manifests_changed':False})
    files = sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
    with (HERE/'SHA256SUMS').open('x') as f:
        for p in files:
            f.write(f'{sha(p)}  {p.relative_to(HERE)}\n')
    print(json.dumps({'external_inputs':len(records),'local_files':len(files),'status':'SEALED'}))


if __name__=='__main__':
    main()
