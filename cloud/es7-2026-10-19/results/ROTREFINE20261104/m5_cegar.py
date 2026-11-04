#!/usr/bin/env python3
"""Bounded fivefold cycle-family CEGAR with an independent symbolic checker.

Only cycle witnesses passing both symbolic verifiers and every exact-set
test are lifted. All SAT assignments are abstract; GP-invalid identities
are skipped by the search and never used as product comparisons.
"""
import argparse,datetime,hashlib,json,shutil,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--bin',type=Path,required=True);p.add_argument('--rounds',type=int,default=8)
    p.add_argument('--seconds',type=int,default=120);p.add_argument('--start',type=int,default=1)
    a=p.parse_args();start=time.monotonic()
    hard=datetime.datetime(2026,11,3,18,50,tzinfo=datetime.timezone.utc).timestamp()
    journal=HERE/'logs/m5_cegar.jsonl'
    def emit(d):
        d['elapsed_seconds']=round(time.monotonic()-start,3)
        with journal.open('a') as f:f.write(json.dumps(d,sort_keys=True)+'\n')
        print(json.dumps(d,sort_keys=True),flush=True)
    def run(script,args,log,limit=180):
        remaining=hard-time.time()
        if remaining<10:raise TimeoutError('campaign deadline')
        with log.open('w') as f:
            r=subprocess.run([sys.executable,'-I',str(HERE/script),*map(str,args)],stdout=f,stderr=subprocess.STDOUT,
                             timeout=min(limit,remaining),check=False)
        if r.returncode:raise RuntimeError(f'{script} failed; inspect {log.name}')
    families=[a.archive/f'm5_family{i:02d}_t12.clauses' for i in range(a.start)]
    assert all(f.exists() for f in families)
    for i in range(a.start,a.start+a.rounds):
        if time.time()+a.seconds+60>hard:emit({'event':'stop','reason':'deadline_before_round'});break
        cnf=a.archive/f't12_families{i:02d}.cnf'
        args=['--base',a.archive/'m5K8t12.cnf','--out',cnf]
        for f in families:args+=['--family',f]
        run('m5_assemble.py',args,HERE/f'logs/m5_assemble_round{i:02d}.jsonl')
        job=f't12_families{i:02d}'
        run('m5_lane.py',['--archive',a.archive,'--bin',a.bin,'--file',cnf.name,'--name',job,'--seconds',a.seconds],
            HERE/f'logs/m5_solve_round{i:02d}.jsonl',a.seconds+90)
        result=json.loads((a.archive/(job+'.run.json')).read_text())
        emit({'event':'solve','round':i,'result':result,'family_count':len(families)})
        if result['verdict']!='SAT_ABSTRACT':
            emit({'event':'stop','reason':result['verdict'],'cnf':cnf.name});break
        model=a.archive/result['positive_model'];scan=a.archive/f'm5_scan_round{i:02d}'
        run('m5_product_cycles.py',['--model',model,'--map',a.archive/'m5K8t12.cnf.json','--out',scan,
            '--max-layers','3','--max-seconds','60','--max-edges','500000','--skip-invalid-gp'],
            HERE/f'logs/m5_scan_round{i:02d}.jsonl',90)
        source=scan/'m5_cycle_witness.json'
        if not source.exists():emit({'event':'stop','reason':'no_three_orbit_cycle','model':model.name});break
        witness=HERE/f'm5_cycle{i:02d}.json';shutil.copyfile(source,witness)
        independent=HERE/f'logs/m5_independent{i:02d}.json'
        run('tests/check_product_symbolic.py',['--model',model,'--witness',witness],independent)
        independent_result=json.loads(independent.read_text());assert independent_result['verified']
        verified=HERE/f'm5_cycle{i:02d}_verified.json'
        run('m5_algebra.py',['verify','--archive',a.archive,'--model',model,'--witness',witness,'--output',verified],
            HERE/f'logs/m5_verify{i:02d}.jsonl')
        vr=json.loads(verified.read_text());assert vr['candidate_clause']==independent_result['candidate_clause']
        for target in (12,13):
            family=a.archive/f'm5_family{i:02d}_t{target}.clauses'
            run('m5_algebra.py',['lift','--archive',a.archive,'--verified',verified,'--layers',target,'--output',family],
                HERE/f'logs/m5_family{i:02d}_t{target}.jsonl',240)
        artifacts=[witness,verified,independent]
        for target in (12,13):
            family=a.archive/f'm5_family{i:02d}_t{target}.clauses'
            artifacts.extend([family,family.with_suffix(family.suffix+'.json')])
        run('m5_archive.py',['--archive',a.archive,*artifacts],HERE/f'logs/m5_archive{i:02d}.jsonl',120)
        families.append(a.archive/f'm5_family{i:02d}_t12.clauses')
        emit({'event':'accepted_cycle','round':i,'witness':witness.name,'witness_sha256':sha(witness),
              'verified_sha256':sha(verified),'comparisons':vr['comparisons'],'pattern_literals':len(vr['candidate_clause']),
              'exact56':vr['exact56'],'family_count':len(families)})
    emit({'event':'finish','family_count':len(families),'all_lane_children_stopped':True})

if __name__=='__main__':main()
