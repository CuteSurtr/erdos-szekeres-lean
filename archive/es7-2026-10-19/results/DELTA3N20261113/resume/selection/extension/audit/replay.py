#!/usr/bin/env python3
"""Independent bounded replay. No imports from parent or former checkers.

Only the parent-authorized one CPU, AS1100MiB, heap800/stack32 allocation
is used. A timeout is NOT CONFIRMED and is retained for coordination.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
CAKE = Path('/home/jay/.local/bin/cake_lpr')


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for data in iter(lambda:f.read(1<<20), b''):
            h.update(data)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case', type=Path)
    parser.add_argument('tag')
    a = parser.parse_args()
    cnf, proof = a.case/'input.cnf', a.case/'solve/proof.lrat'
    paths = [cnf, proof, CAKE]
    before = {str(p):digest(p) for p in paths}
    log, timing = HERE/f'data/{a.tag}.log', HERE/f'data/{a.tag}.time'
    assert not timing.exists()
    cmd = ['/usr/bin/timeout','20s','/usr/bin/prlimit','--as=1153433600','--cpu=18',
           str(CAKE),'--CML_HEAP_SIZE=800','--CML_STACK_SIZE=32',str(cnf),str(proof)]
    start = time.monotonic()
    with log.open('x') as f:
        p = subprocess.run(['/usr/bin/time','-v','-o',str(timing)]+cmd,
                           stdout=f,stderr=subprocess.STDOUT)
    after = {str(p):digest(p) for p in paths}
    lines = log.read_text().splitlines()
    accepted = 's VERIFIED UNSAT' in lines and before==after
    receipt = {'label':'CERTIFIED' if accepted else 'NOT CONFIRMED',
               'command':cmd,'returncode':p.returncode,'exact_acceptance_line':'s VERIFIED UNSAT' in lines,
               'stable_inputs':before==after,'before':before,'after':after,
               'proof_bytes':proof.stat().st_size,'log_sha256':digest(log),
               'seconds':time.monotonic()-start,'script_sha256':digest(Path(__file__))}
    with (HERE/f'data/{a.tag}.json').open('x') as f:
        json.dump(receipt,f,indent=2);f.write('\n')
    print(json.dumps({'label':receipt['label'],'seconds':round(receipt['seconds'],3),
                      'returncode':p.returncode,'receipt':a.tag+'.json'}))
    assert accepted, 'Not confirmed: exact acceptance line and stable inputs required.'


if __name__=='__main__':
    main()
