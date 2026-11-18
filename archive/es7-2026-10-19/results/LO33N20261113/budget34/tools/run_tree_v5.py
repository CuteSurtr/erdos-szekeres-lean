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
p.add_argument('slice',type=int,choices=[18,19,20])  # v3: slice 18
p.add_argument('--seconds',type=int,default=900)
p.add_argument('--threads',type=int,default=3)
p.add_argument('--tag',default='a')
p.add_argument('--contexts',type=int,default=2048)
p.add_argument('--input-folder',default=None)
p.add_argument('--max-ctx-nodes',type=int,default=50000)
p.add_argument('--bb',default='bb')  # v2: successor packet folder under runs/s<slice>/, prepared by prepare_successor.py
p.add_argument('--split-open',type=int,default=0)
p.add_argument('--on-witness',default='stop',choices=['stop','continue'])  # v5: continue = every context's witness is logged, that context stays open
p.add_argument('--witness-grace',type=int,default=0)  # v5: end the finder (SIGTERM; ctx files are written atomically) this many seconds after its first logged WITNESS
p.add_argument('--stop-witnesses',type=int,default=0)  # v5: ... or once this many WITNESS events were logged
p.add_argument('--budget',type=int,default=34,choices=[34,35])  # v4: budget; runs/b<B>s<T> when B != 34  # v2: fastbb --split-open=L on resume (rewrites that packet's master)
args=p.parse_args()
resource.setrlimit(resource.RLIMIT_AS,(150<<20,1400<<20))
W=Path('/home/jay/research/data/es308-20261114')
run=W/'runs'/(f's{args.slice}' if args.budget==34 else f'b{args.budget}s{args.slice}');run.mkdir(exist_ok=True)
log=run/f'{args.tag}.log';receipt=run/f'{args.tag}.json'
bb=run/args.bb;assert bb.is_dir() and bb.parent==run and (args.split_open==0 or args.bb!='bb')
assert not log.exists() and not receipt.exists()
inp=W/'inputs'/(args.input_folder or f's{args.slice}')
assert inp.resolve().is_relative_to(W/'inputs')
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
before={str(q):sha(q) for q in [inp/'rows.txt',inp/'extra.json',W/'inputs/source-2650.json.gz',W/'bin/fastbb2']}
cmd=[str(W/'bin/fastbb2'),'solve',str(inp/'rows.txt'),str(args.budget),str(args.threads),str(args.contexts),str(bb),
     '--slice=1',f'--on-witness={args.on_witness}',f'--time-limit={args.seconds}',
     f'--max-ctx-nodes={args.max_ctx_nodes}','--ktop=16','--dtop=8','--klow=4','--sbiter=1000']+([f'--split-open={args.split_open}'] if args.split_open else [])
def child_limit():
    resource.setrlimit(resource.RLIMIT_AS,(1400<<20,1400<<20))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
start=time.monotonic();peak=0;stop=None;released=set();pos=0;nwit=0;first=None
with log.open('x') as out:
    child=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,preexec_fn=child_limit)
    while child.poll() is None:
        try:
            status={line.split(':',1)[0]:line.split(':',1)[1].strip() for line in Path(f'/proc/{child.pid}/status').read_text().splitlines() if ':' in line}
            rss=int(status.get('VmRSS','0 kB').split()[0]);swap=int(status.get('VmSwap','0 kB').split()[0]);peak=max(peak,rss)
            if rss>=1200*1024 or swap:stop='internal RSS/swap guard'
        except (FileNotFoundError,ProcessLookupError,PermissionError):pass
        if time.monotonic()-start>args.seconds+180:stop='outer wall guard'
        if args.witness_grace or args.stop_witnesses:  # v5: count complete continue-mode WITNESS lines of the log
            with log.open('rb') as f:f.seek(pos);chunk=f.read()
            k=chunk.rfind(b'\n')+1;pos+=k
            nwit+=sum(b'"event": "WITNESS"' in l and b'"nodes_so_far"' in l for l in chunk[:k].split(b'\n'))
            if nwit and first is None:first=time.monotonic()  # witnesses come in clusters after the too-big prefix of the context list
            if (args.witness_grace and nwit and time.monotonic()-first>=args.witness_grace) or (args.stop_witnesses and nwit>=args.stop_witnesses):
                stop=f'witness slice complete ({nwit} witnesses logged)'
        for q in bb.glob('ctx-*.json.gz'):
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
result={'label':'COMPUTED finder result; not yet EXACT TREE','slice':args.slice,'budget':args.budget,
        'runner_sha256':sha(Path(__file__)),
        'command':cmd,'exit':rc,'seconds':time.monotonic()-start,'peak_sampled_rss_kib':peak,
        'stop_reason':stop,'input_hashes':before,'stable_input_hashes':True,
        'bb':str(bb),'contexts_saved':len(list(bb.glob('ctx-*.json.gz'))),'cache_releases':len(released),
        'finished':datetime.now().astimezone().isoformat()}
wp=bb/'WITNESS.json'
if wp.exists():
    h=json.loads(wp.read_text())['holes'];hs=set(h)
    base=json.loads(gzip.decompress((W/'inputs/source-2650.json.gz').read_bytes()))
    rows=base['constraints']+json.loads((inp/'extra.json').read_text())
    assert len(h)==len(hs)==args.budget and 0 not in hs
    assert all(len(hs&set(r['support']))>=r['rhs'] for r in rows)
    result['witness']={'holes':h,'independent_exact_row_check':'PASS','rows_checked':len(rows),
                       'scope':'abstract hole vector, not a real point set'}
ev=[]  # v5: all JSON events of the log; every distinct WITNESS (continue mode: one per context) gets its own exact row check
for line in log.read_text().splitlines():
    try:e=json.loads(line)
    except ValueError:continue
    if isinstance(e,dict) and 'event' in e:ev.append(e)
counts={};ws=[]
for e in ev:counts[e['event']]=counts.get(e['event'],0)+1
st=[e for e in ev if e['event']=='start']
result.update(on_witness=args.on_witness,events=counts,todo=st[0]['todo'] if st else None,
              processed=counts.get('closed',0)+counts.get('context_too_big',0)+sum('nodes_so_far' in e for e in ev if e['event']=='WITNESS'))
wev=[e for e in ev if e['event']=='WITNESS']
if wev:
    base=json.loads(gzip.decompress((W/'inputs/source-2650.json.gz').read_bytes()))
    rows=base['constraints']+json.loads((inp/'extra.json').read_text())
    for e in wev:
        h=e['holes'];hs=set(h)
        if sorted(h) in [sorted(w['holes']) for w in ws]:continue
        assert len(h)==len(hs)==args.budget and 0 not in hs
        assert all(len(hs&set(r['support']))>=r['rhs'] for r in rows)
        ws.append({'holes':h,'context':e.get('context'),'nodes_so_far':e.get('nodes_so_far'),'independent_exact_row_check':'PASS','rows_checked':len(rows)})
result['witnesses']=ws
receipt.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
