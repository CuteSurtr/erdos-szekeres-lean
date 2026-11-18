#!/usr/bin/env python3
"""Fresh bounded cake replay of one tiny n5 proof; no re-solve."""
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

R=Path(__file__).resolve().parents[1]
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
CAKE=Path('/home/jay/.local/bin/cake_lpr')
CASES={'7':'terminal5m7-a','8':'terminal5m8-a','9':'base5m9-a'}

def sha(p):
    a=p.stat()
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1 << 20),b''):
            h.update(block)
    b=p.stat()
    assert (a.st_ino,a.st_size,a.st_mtime_ns)==(b.st_ino,b.st_size,b.st_mtime_ns)
    return h.hexdigest()

def save(p,v):
    with p.open('x') as f:
        json.dump(v,f,indent=2)
        f.write('\n')

def main():
    resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
    assert len(sys.argv)==2 and sys.argv[1] in CASES
    m=sys.argv[1]
    case=W/CASES[m]
    cnf,proof=case/'input.cnf',case/'proof.blrat'
    compressed=case/'proof.blrat.zst'
    assert proof.stat().st_size<100000,'not the authorized tiny proof'
    parent=json.loads((case/'result.json').read_text())
    paths=[cnf,proof,compressed,CAKE,case/'result.json',Path(__file__)]
    before={str(p):sha(p) for p in paths}
    for p in (cnf,proof,compressed):
        assert before[str(p)]==parent['hashes'][p.name]
    assert before[str(CAKE)]==parent['hashes']['cake_lpr']
    audited=json.loads((R/'data'/f'formula-m{m}.json').read_text())
    assert before[str(cnf)]==audited['original_cnf_sha256']
    prefix=R/'data'/f'replay-m{m}'
    stdout=Path(str(prefix)+'.stdout')
    stderr=Path(str(prefix)+'.stderr')
    timing=Path(str(prefix)+'.time')
    assert not timing.exists()
    command=['/usr/bin/time','-v','-o',str(timing),'/usr/bin/timeout','--kill-after=1','17s',
             '/usr/bin/prlimit','--as=314572800','--cpu=16',str(CAKE),
             '--CML_HEAP_SIZE=128','--CML_STACK_SIZE=32',str(cnf),str(proof)]
    save(Path(str(prefix)+'.command.json'),{'command':command,'before':before,
        'limits':{'AS_MiB':300,'heap_MiB':128,'stack_MiB':32,'CPUs':1,
                  'outer_wall_seconds':20,'cake_wall_seconds':17,'cake_CPU_seconds':16}})
    start=time.monotonic()
    with stdout.open('x') as out,stderr.open('x') as err:
        proc=subprocess.run(command,stdout=out,stderr=err)
    seconds=time.monotonic()-start
    after={str(p):sha(p) for p in paths}
    verdict='s VERIFIED UNSAT' in stdout.read_text().splitlines()
    accepted=verdict and before==after and proc.returncode==0
    result={'status':'PASS' if accepted else 'NOT CONFIRMED',
            'label':'CERTIFIED' if accepted else 'NOT CONFIRMED','m':int(m),'n':5,
            'scope':'pure geometric base' if m=='9' else 'generic terminal selector counterexample formula',
            'exact_acceptance_line':verdict,'returncode':proc.returncode,
            'stable_inputs':before==after,'seconds':seconds,'before':before,'after':after,
            'proof_bytes':proof.stat().st_size,'compressed_bytes':compressed.stat().st_size,
            'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),
            'proof_retained_at':str(proof),'compressed_proof_retained_at':str(compressed),
            'extra_heap_allocation':False,'limits':{'AS_MiB':300,'heap_MiB':128,'stack_MiB':32,
                                                 'CPUs':1,'outer_wall_seconds':20}}
    save(Path(str(prefix)+'.json'),result)
    print(json.dumps({k:result[k] for k in ('status','label','m','seconds','exact_acceptance_line','proof_bytes')}))
    assert accepted,'Exact acceptance line, successful process and stable hashes required'

if __name__=='__main__':
    main()
