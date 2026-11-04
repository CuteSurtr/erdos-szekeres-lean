#!/usr/bin/env python3
"""Bounded GP-sign refinement after the retained product and linear families.

All accepted batches are exact-tested before the next SAT call. A complete GP
check is a necessary sign condition, never a geometric realization certificate.
"""
import argparse,datetime,json,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--bin',type=Path,required=True);p.add_argument('--checker',type=Path,required=True)
    p.add_argument('--model',type=Path,required=True);p.add_argument('--rounds',type=int,default=6)
    p.add_argument('--start',type=int,default=1);p.add_argument('--seconds',type=int,default=180)
    p.add_argument('--linear-through',type=int)
    a=p.parse_args();start=time.monotonic();journal=HERE/'logs/m5_gp_cegar.jsonl'
    deadline=datetime.datetime(2026,11,3,18,35,tzinfo=datetime.timezone.utc).timestamp()
    def emit(d):
        d['elapsed_seconds']=round(time.monotonic()-start,3)
        with journal.open('a') as f:f.write(json.dumps(d,sort_keys=True)+'\n')
        print(json.dumps(d,sort_keys=True),flush=True)
    def run(script,args,log):
        if time.time()>=deadline:raise TimeoutError('refinement deadline')
        with (HERE/'logs'/log).open('w') as f:
            subprocess.run([sys.executable,'-B','-I',str(HERE/script),*map(str,args)],stdout=f,stderr=subprocess.STDOUT,check=True)
    products=sorted(a.archive.glob('m5_family*_t12.clauses'))
    linears=sorted(a.archive.glob('m5_linear*_t12.clauses'))
    index=lambda f:int(f.stem.split('_')[1].removeprefix('linear'))
    if a.linear_through is not None:linears=[f for f in linears if index(f)<=a.linear_through]
    assert len(products)==6 and len(linears)>=2,'expected six product and at least two verified linear families'
    linear_label=f'linear{max(map(index,linears)):02d}'
    templates=sorted(a.archive.glob('m5_gp_template*_t12.clauses'))
    fixed=products+[a.archive/'m5_interiority_t12.clauses']+linears+templates
    batches=[a.archive/f'm5_gp{i:02d}_t12.clauses' for i in range(1,a.start)]
    model=a.model
    for i in range(a.start,a.start+a.rounds):
        if time.time()+a.seconds+60>deadline:emit({'event':'stop','reason':'deadline_before_round'});break
        gp=a.archive/f'm5_gp_round{i:02d}_{linear_label}'
        run('m5_full_gp.py',['--model',model,'--checker',a.checker,'--out',gp,'--layers','12'],f'm5_gp_check{i:02d}_{linear_label}.jsonl')
        record=json.loads((gp/'full_gp_check.json').read_text());emit({'event':'full_gp','round':i,**record})
        run('m5_archive.py',['--archive',a.archive,gp/'full_gp_check.json',gp/'full_gp_violations.txt'],f'm5_gp_archive_check{i:02d}_{linear_label}.jsonl')
        if not record['violations']:
            emit({'event':'gp_survivor','round':i,'model':model.name,'model_sha256':record['model_sha256']});break
        artifacts=[]
        for t in (12,13):
            family=a.archive/f'm5_gp{i:02d}_t{t}.clauses'
            run('m5_gp_refine.py',['--model',model,'--violations',gp/'full_gp_violations.txt',
                '--archive',a.archive,'--target-layers',t,'--output',family],f'm5_gp_family{i:02d}_t{t}.jsonl')
            metadata=json.loads(family.with_suffix('.clauses.json').read_text())
            assert metadata['direct_exact56_clause_tests']==6*metadata['clauses']
            assert metadata['complete_template_tests']['forbidden_matches']==0
            artifacts.extend([family,family.with_suffix('.clauses.json')])
            emit({'event':'accepted_gp_family','round':i,'target_layers':t,'clauses':metadata['clauses'],
                  'family_sha256':metadata['family_sha256'],'direct_exact56_clause_tests':metadata['direct_exact56_clause_tests']})
        run('m5_archive.py',['--archive',a.archive,*artifacts],f'm5_gp_archive_family{i:02d}.jsonl')
        batches.append(a.archive/f'm5_gp{i:02d}_t12.clauses')
        cnf=a.archive/f't12_gp{i:02d}_{linear_label}_families06.cnf'
        args=['--base',a.archive/'m5K8t12.cnf','--out',cnf]
        for f in fixed+batches:args+=['--family',f]
        run('m5_assemble.py',args,f'm5_gp_assembly{i:02d}.jsonl')
        job=f't12_gp{i:02d}_{linear_label}_families06_{a.seconds}'
        run('m5_lane.py',['--archive',a.archive,'--bin',a.bin,'--file',cnf.name,'--name',job,'--seconds',a.seconds],
            f'm5_gp_solve{i:02d}.jsonl')
        result=json.loads((a.archive/(job+'.run.json')).read_text());emit({'event':'solve','round':i,'result':result})
        if result['verdict']!='SAT_ABSTRACT':emit({'event':'stop','reason':result['verdict'],'cnf':cnf.name});break
        model=a.archive/result['positive_model']
    else:
        gp=a.archive/f'm5_gp_round{a.start+a.rounds:02d}_{linear_label}'
        run('m5_full_gp.py',['--model',model,'--checker',a.checker,'--out',gp,'--layers','12'],f'm5_gp_check{a.start+a.rounds:02d}_{linear_label}.jsonl')
        record=json.loads((gp/'full_gp_check.json').read_text());emit({'event':'full_gp_at_limit',**record})
        run('m5_archive.py',['--archive',a.archive,gp/'full_gp_check.json',gp/'full_gp_violations.txt'],f'm5_gp_archive_check{a.start+a.rounds:02d}_{linear_label}.jsonl')
    emit({'event':'finish','last_model':model.name,'gp_batches':len(batches),'all_lane_children_stopped':True})

if __name__=='__main__':main()
