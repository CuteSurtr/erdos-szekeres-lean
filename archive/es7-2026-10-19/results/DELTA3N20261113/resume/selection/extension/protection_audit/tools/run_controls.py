#!/usr/bin/env python3
"""Run bounded native regeneration and the independent streamed checker."""
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT=Path('/home/jay/research/lean/erdos-szekeres-lean')
REC=ROOT/'cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/protection_audit'
SCR=Path('/home/jay/research/data/delta3-codex-20261113/extension/protection-audit')

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def run(tag,args,expected=0):
    data=REC/'data'
    cmd=['/usr/bin/time','-v','-o',str(data/(tag+'.time')),'/usr/bin/timeout','-k','1','20s',
         '/usr/bin/prlimit','--as=314572800','--cpu=19','/usr/bin/taskset','-c','5',
         '/usr/bin/nice','-n','10',*map(str,args)]
    started=time.monotonic()
    with (data/(tag+'.stdout')).open('x') as out,(data/(tag+'.stderr')).open('x') as err:
        p=subprocess.run(cmd,stdout=out,stderr=err)
    entry=dict(tag=tag,command=cmd,exit=p.returncode,expected_exit=expected,seconds=time.monotonic()-started)
    with (data/'commands.jsonl').open('a') as f:f.write(json.dumps(entry)+'\n')
    assert p.returncode==expected,entry
    return entry

def main():
    regeneration=[];cases=[];domain=[]
    for variant,m in [('cup',15),('forced',13)]:
        out=SCR/(variant+'-main-native.cnf');assert not out.exists()
        run('generate-'+variant+'-main',[SCR/variant,m,7,out])
        original=SCR.parent/('n7m15-cup.cnf' if variant=='cup' else 'n7m13-forced.cnf')
        for suffix in ('','.map'):
            actual=Path(str(out)+suffix);source=Path(str(original)+suffix)
            assert sha(actual)==sha(source)
            regeneration.append(dict(variant=variant,file=str(actual),original=str(source),sha256=sha(actual),byte_identical=True))
        for label,cm,cn,fixture in [('blocks5',8,5,'blocks'),('blocks7',8,7,'blocks'),('two7',8,7,'two'),
                                  ('edge45',4,5,'none'),('edge55',5,5,'none'),('edge78',7,8,'none'),('edge88',8,8,'two')]:
            tag=variant+'-'+label;path=SCR/(tag+'.cnf');assert not path.exists()
            run('generate-'+tag,[SCR/variant,cm,cn,path])
            run('check-'+tag,['/usr/bin/python3','-B',REC/'tools/check.py','rows','--variant',variant,
                '--m',cm,'--n',cn,'--cnf',path,'--fixture',fixture,'--tag',tag])
            receipt=json.loads((REC/'data'/(tag+'.json')).read_text())
            assert receipt['status']=='PASS'
            if label.startswith('edge'):
                # At m=n-1 or n, a retained selection has no bad witness and
                # complement below target size, so the proper contradiction is explicit.
                empty=sum(line.strip()=='0' for line in path.open())
                assert empty>0
                domain.append(dict(tag=tag,empty_clauses=empty))
            cases.append(dict(tag=tag,variables=receipt['variables'],clauses=receipt['clauses'],fixture=fixture))
        for label,cm,cn in [('bad-n',8,4),('bad-small',3,5),('bad-large',21,7)]:
            dest=SCR/(variant+'-'+label+'.cnf');assert not dest.exists()
            entry=run(variant+'-'+label,[SCR/variant,cm,cn,dest],1)
            assert 'bad_parameters' in (REC/'data'/(variant+'-'+label+'.stderr')).read_text()
            assert not dest.exists()
            domain.append(entry)
    summary=dict(status='PASS',regenerated_main_files=regeneration,checked_generated_cases=cases,domain_controls=domain)
    with (REC/'data/native-controls.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',main_files=len(regeneration),generated_cases=len(cases),domain_controls=len(domain))))

if __name__=='__main__':main()
