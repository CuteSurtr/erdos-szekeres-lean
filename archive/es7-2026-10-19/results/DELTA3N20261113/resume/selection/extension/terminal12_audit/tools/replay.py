#!/usr/bin/env python3
"""Independent short heap64 replay with streamed hashes and cache release."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

R=Path(__file__).resolve().parents[1]
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
CAKE=Path('/home/jay/.local/bin/cake_lpr')
CASES={'10':W/'terminal6m10-a','11':W/'terminal6m11-a','12':W/'descend15-a/3/certificate'}

def sha(p):
    a=p.stat();h=hashlib.sha256()
    with p.open('rb') as f:
        pending=0;offset=0
        for block in iter(lambda:f.read(1 << 20),b''):
            h.update(block);pending+=len(block)
            if pending>=64 << 20:
                os.posix_fadvise(f.fileno(),offset,pending,os.POSIX_FADV_DONTNEED)
                offset+=pending;pending=0
        if pending:os.posix_fadvise(f.fileno(),offset,pending,os.POSIX_FADV_DONTNEED)
    b=p.stat()
    assert (a.st_ino,a.st_size,a.st_mtime_ns)==(b.st_ino,b.st_size,b.st_mtime_ns)
    return h.hexdigest()

def save(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')

def main():
    resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
    assert len(sys.argv)==2 and sys.argv[1] in CASES
    m=sys.argv[1];case=CASES[m]
    cnf=case/'input.cnf';proof=case/'proof.blrat';zst=case/'proof.blrat.zst'
    parent=json.loads((case/'result.json').read_text())
    paths=[cnf,proof,zst,CAKE,case/'result.json',Path(__file__)]
    before={str(p):sha(p) for p in paths}
    for p in (cnf,proof,zst):assert before[str(p)]==parent['hashes'][p.name]
    assert before[str(CAKE)]==parent['hashes']['cake_lpr']
    report=json.loads((R/'data'/('fixed-case3.json' if m=='12' else f'generic-m{m}.json')).read_text())
    assert report['cnf_sha256']==before[str(cnf)]
    prefix=R/'data'/f'replay-m{m}'
    outpath=Path(str(prefix)+'.stdout');errpath=Path(str(prefix)+'.stderr');timing=Path(str(prefix)+'.time')
    assert not timing.exists()
    cmd=['/usr/bin/time','-v','-o',str(timing),'/usr/bin/timeout','--kill-after=1','17s',
         '/usr/bin/prlimit','--as=314572800','--cpu=16',str(CAKE),
         '--CML_HEAP_SIZE=64','--CML_STACK_SIZE=32',str(cnf),str(proof)]
    save(Path(str(prefix)+'.command.json'),{'command':cmd,'before':before,
         'limits':{'AS_MiB':300,'heap_MiB':64,'stack_MiB':32,'CPUs':1,'outer_wall_seconds':20}})
    start=time.monotonic()
    with outpath.open('x') as out,errpath.open('x') as err:
        proc=subprocess.run(cmd,stdout=out,stderr=err)
    elapsed=time.monotonic()-start
    after={str(p):sha(p) for p in paths}
    accepted='s VERIFIED UNSAT' in outpath.read_text().splitlines()
    passed=accepted and before==after and proc.returncode==0
    result={'status':'PASS' if passed else 'NOT CONFIRMED',
            'label':'CERTIFIED' if passed else 'NOT CONFIRMED','m':int(m),'n':6,
            'scope':'fixed membership obstruction' if m=='12' else 'universal generic terminal counterexample formula',
            'exact_verdict_line':accepted,'returncode':proc.returncode,'seconds':elapsed,
            'stable_inputs':before==after,'before':before,'after':after,
            'proof_bytes':proof.stat().st_size,'compressed_bytes':zst.stat().st_size,
            'stdout_sha256':sha(outpath),'stderr_sha256':sha(errpath),
            'cache_release':'POSIX_FADV_DONTNEED every64MiB and remainder on every hash',
            'limits':{'AS_MiB':300,'heap_MiB':64,'stack_MiB':32,'CPUs':1,'outer_wall_seconds':20,
                      'cake_wall_seconds':17,'cake_CPU_seconds':16},
            'proofs_retained':True,'new_reservation':False}
    save(Path(str(prefix)+'.json'),result)
    print(json.dumps({k:result[k] for k in ('status','label','m','seconds','exact_verdict_line','proof_bytes')}))
    assert passed,'Exact cake acceptance and stable audited inputs are required'

if __name__=='__main__':main()
