#!/usr/bin/env python3
"""Bounded finder only. Exact replay and geometric row audit are separate."""
import argparse
from datetime import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import time

p=argparse.ArgumentParser()
p.add_argument('slice',type=int,choices=[19,20])
p.add_argument('--seconds',type=int,default=900)
p.add_argument('--threads',type=int,default=3)
p.add_argument('--tag',default='a')
p.add_argument('--contexts',type=int,default=2048)
args=p.parse_args()
resource.setrlimit(resource.RLIMIT_AS,(150<<20,1400<<20))
W=Path('/home/jay/research/data/es308-20261114')
run=W/'runs'/f's{args.slice}';run.mkdir(exist_ok=True)
log=run/f'{args.tag}.log';receipt=run/f'{args.tag}.json'
assert not log.exists() and not receipt.exists()
inp=W/'inputs'/f's{args.slice}'
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
before={str(q):sha(q) for q in [inp/'rows.txt',inp/'extra.json',W/'inputs/source-2650.json.gz',W/'bin/fastbb2']}
cmd=[str(W/'bin/fastbb2'),'solve',str(inp/'rows.txt'),'34',str(args.threads),str(args.contexts),str(run/'bb'),
     '--slice=1','--on-witness=stop',f'--time-limit={args.seconds}',
     '--max-ctx-nodes=50000','--ktop=16','--dtop=8','--klow=4','--sbiter=1000']
def child_limit():
    resource.setrlimit(resource.RLIMIT_AS,(1400<<20,1400<<20))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
start=time.monotonic();peak=0;stop=None;released=set()
with log.open('x') as out:
    child=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,preexec_fn=child_limit)
    while child.poll() is None:
        try:
            status={line.split(':',1)[0]:line.split(':',1)[1].strip() for line in Path(f'/proc/{child.pid}/status').read_text().splitlines() if ':' in line}
            rss=int(status.get('VmRSS','0 kB').split()[0]);swap=int(status.get('VmSwap','0 kB').split()[0]);peak=max(peak,rss)
            if rss>=1200*1024 or swap:stop='internal RSS/swap guard'
        except (FileNotFoundError,ProcessLookupError,PermissionError):pass
        if time.monotonic()-start>args.seconds+180:stop='outer wall guard'
        for q in (run/'bb').glob('ctx-*.json.gz'):
            if q.name not in released:
                try:
                    fd=os.open(q,os.O_RDONLY)
                    try:os.fdatasync(fd);os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED)
                    finally:os.close(fd)
                    released.add(q.name)
                except OSError:pass
        if stop:
            child.terminate()
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:child.kill();child.wait()
            break
        time.sleep(1)
rc=child.wait()
after={q:sha(Path(q)) for q in before}
assert after==before,'inputs changed during finder'
result={'label':'COMPUTED finder result; not yet EXACT TREE','slice':args.slice,'budget':34,
        'command':cmd,'exit':rc,'seconds':time.monotonic()-start,'peak_sampled_rss_kib':peak,
        'stop_reason':stop,'input_hashes':before,'stable_input_hashes':True,
        'contexts_saved':len(list((run/'bb').glob('ctx-*.json.gz'))),'cache_releases':len(released),
        'finished':datetime.now().astimezone().isoformat()}
wp=run/'bb/WITNESS.json'
if wp.exists():
    h=json.loads(wp.read_text())['holes'];hs=set(h)
    base=json.loads(gzip.decompress((W/'inputs/source-2650.json.gz').read_bytes()))
    rows=base['constraints']+json.loads((inp/'extra.json').read_text())
    assert len(h)==len(hs)==34 and 0 not in hs
    assert all(len(hs&set(r['support']))>=r['rhs'] for r in rows)
    result['witness']={'holes':h,'independent_exact_row_check':'PASS','rows_checked':len(rows),
                       'scope':'abstract hole vector, not a real point set'}
receipt.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
