"""Bounded finder only. Outer invocation must enforce CPU/AS/wall limits."""
import argparse
import json
import subprocess
import time
from pathlib import Path

WORK = Path('/home/jay/research/data/delta3-codex-20261113/selection/terminal')

def solve(path, timeout=2):
    try:
        p=subprocess.run(['/usr/bin/cadical','-q',str(path)], capture_output=True,
                         text=True, timeout=timeout)
        text=p.stdout+p.stderr
        path.with_suffix('.finder.log').write_text(text)
        if p.returncode==10:
            lits=[int(i) for line in p.stdout.splitlines() if line.startswith('v ')
                  for i in line[2:].split() if i!='0']
            positive={i for i in lits if i>0}
            clauses=[[int(i) for i in line.split()[:-1]] for line in path.read_text().splitlines()
                     if line and line[0] not in 'cp']
            assert all(any((l>0)==(abs(l) in positive) for l in c) for c in clauses)
            return dict(outcome='SAT',A=sorted(i-1 for i in positive),exit=p.returncode)
        return dict(outcome='UNSAT_UNCERTIFIED' if p.returncode==20 else 'UNKNOWN',exit=p.returncode)
    except subprocess.TimeoutExpired as e:
        path.with_suffix('.finder.log').write_bytes((e.stdout or b'')+(e.stderr or b'')+b'\nTIMEOUT\n')
        return dict(outcome='UNKNOWN_TIMEOUT')

def encode_solve(stem):
    prefix=WORK/stem
    result=dict(stem=stem)
    start=time.monotonic()
    try:
        p=subprocess.run([str(WORK/'encode'),str(prefix)+'.points',str(prefix)],
                         capture_output=True,text=True,timeout=4)
        (WORK/(stem+'.encode.log')).write_text(p.stdout+p.stderr)
        result['encode_exit']=p.returncode
        if p.returncode==0:
            g=json.loads(Path(str(prefix)+'.geometry.json').read_text())
            result.update(m=g['m'],n=g['n'],maxcap=g['maxcap'],maxgon=g['maxgon'],
                          cap4=len(g['fourcaps']),bad3=len(g['rank3_triples']),polygons=len(g['polygons']))
            result['terminal']=solve(Path(str(prefix)+'.terminal.cnf'))
            result['weak']=solve(Path(str(prefix)+'.weak.cnf'))
        else: result['outcome']='INVALID' if p.returncode in (3,4) else 'ERROR'
    except subprocess.TimeoutExpired as e:
        (WORK/(stem+'.encode.log')).write_bytes((e.stdout or b'')+(e.stderr or b'')+b'\nTIMEOUT\n')
        result['outcome']='UNKNOWN_ENCODER_TIMEOUT'
    result['seconds']=time.monotonic()-start
    (WORK/(stem+'.result.json')).write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--first',type=int,default=0);ap.add_argument('--last',type=int,default=30)
    args=ap.parse_args()
    inputs=json.loads((WORK/'inputs.json').read_text())
    start=time.monotonic()
    for r in inputs[args.first:args.last]:
        if time.monotonic()-start>8: break
        print(json.dumps(encode_solve(r['stem'])),flush=True)
