#!/usr/bin/env python3
"""Bounded finder only. Exact replay and geometric row audit are separate.

v6 (skip list): fastbb2 gets --ctx=<open contexts minus those recorded too big above this cap> instead of every open
context, so known too-big contexts are not re-walked at every start. Record: <packet>/TOO_BIG.txt, one line
'<context> <nodes_so_far> <tag>' per context_too_big event (appended here after each run; initial list from
init_too_big_v1.py). --extra-cap: one extra fastbb2 (same rows, packet, slice) on the recorded too-big contexts with
the higher cap; its witnesses join the receipt. Selection only: ctx files, witnesses and checks are those of v5.

v7 (inbox): --inbox=DIR adds the witnesses a side pass (highcap_v1.py) left in DIR/w-*.json to the receipt, after this
run's own, in file-name order, up to --stop-witnesses in all: only those whose context is still open in the packet and
that pass the same exact row check against THIS run's rows (a witness cut by a later row is skipped). The loop then
batches them like its own. Nothing is written into DIR.
"""
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
p.add_argument('--budget',type=int,default=34,choices=[34,35,36])  # v8: budget 36 allowed (only change);  # v4: budget; runs/b<B>s<T> when B != 34  # v2: fastbb --split-open=L on resume (rewrites that packet's master)
p.add_argument('--skip-file',default='TOO_BIG.txt')  # v6: per-packet too-big record
p.add_argument('--too-big-only',action='store_true')  # v6: standalone pass: only open contexts recorded too big, none of them above --max-ctx-nodes
p.add_argument('--extra-cap',type=int,default=0)  # v6: > --max-ctx-nodes: extra fastbb2 on contexts recorded too big, none of them above this cap
p.add_argument('--extra-threads',type=int,default=1)
p.add_argument('--inbox',default=None)  # v7: side-pass witnesses (highcap_v1.py), re-checked against this run's rows
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
skipf=bb/args.skip_file;known={};xcmd=None;xlog=run/f'{args.tag}.x.log';sel={}  # v6: known = context -> largest nodes_so_far of its too-big attempts
use_skip=not args.split_open and (bb/'master.txt').exists() and (bb/'contexts.json').exists()  # v6: needs the packet's existing master; split-open renumbers
assert use_skip or not (args.too_big_only or args.extra_cap)
assert not args.extra_cap or args.extra_cap>args.max_ctx_nodes
if use_skip:
    assert not xlog.exists()
    if skipf.exists():
        for line in skipf.read_text().splitlines():
            if line.strip():c,n=map(int,line.split()[:2]);known[c]=max(known.get(c,0),n)
    opn=[c['context'] for c in json.loads((bb/'contexts.json').read_text()) if not (bb/f"ctx-{c['context']}.json.gz").exists()]
    lst=[c for c in opn if (0<known.get(c,0)<=args.max_ctx_nodes if args.too_big_only else known.get(c,0)<=args.max_ctx_nodes)]
    xl=[c for c in opn if args.max_ctx_nodes<known.get(c,0)<=args.extra_cap]
    cmd.append('--ctx='+(','.join(map(str,lst)) or '-1'))  # '--ctx=' (empty) would mean all contexts; -1 matches none
    sel={'skip_file':str(skipf),'skip_file_sha256_before':sha(skipf) if skipf.exists() else None,'mode':'too-big-only' if args.too_big_only else 'frontier',
         'open_at_start':len(opn),'selected':len(lst),'skipped_known_too_big':len(opn)-len(lst)}
    if args.extra_cap and xl:
        xcmd=cmd[:4]+[str(args.extra_threads)]+cmd[5:-1]+['--ctx='+','.join(map(str,xl))]
        xcmd=[x if not x.startswith('--max-ctx-nodes=') else f'--max-ctx-nodes={args.extra_cap}' for x in xcmd]
        assert '--on-witness=continue' in xcmd  # stop mode would end the extra worker at its first witness
def child_limit():
    resource.setrlimit(resource.RLIMIT_AS,(1400<<20,1400<<20))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def halt(ch):  # v6: the v5 stop sequence, for either worker
    if ch and ch.poll() is None:
        ch.terminate()
        try:ch.wait(timeout=5)
        except subprocess.TimeoutExpired:ch.kill();ch.wait()
start=time.monotonic();peak=0;stop=None;released=set();pos=[0,0];nwit=0;first=None;xchild=xout=None
with log.open('x') as out:
    child=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,preexec_fn=child_limit)
    while child.poll() is None:
        if xcmd and xchild is None and b'"event": "start"' in log.read_bytes()[:8192]:  # v6: after the frontier worker has written master.json
            xout=xlog.open('x');xchild=subprocess.Popen(xcmd,stdout=xout,stderr=subprocess.STDOUT,preexec_fn=child_limit)
        for ch in [child]+[xchild]*(xchild is not None and xchild.poll() is None):  # v6: same guard for the extra worker
          try:
            status={line.split(':',1)[0]:line.split(':',1)[1].strip() for line in Path(f'/proc/{ch.pid}/status').read_text().splitlines() if ':' in line}
            rss=int(status.get('VmRSS','0 kB').split()[0]);swap=int(status.get('VmSwap','0 kB').split()[0]);peak=max(peak,rss)
            if rss>=1200*1024 or swap:stop='internal RSS/swap guard'
          except (FileNotFoundError,ProcessLookupError,PermissionError):pass
        if time.monotonic()-start>args.seconds+180:stop='outer wall guard'
        if args.witness_grace or args.stop_witnesses:  # v5: count complete continue-mode WITNESS lines of the log
          for i,lg in enumerate([log,xlog][:1+(xchild is not None)]):  # v6: of both workers' logs
            with lg.open('rb') as f:f.seek(pos[i]);chunk=f.read()
            k=chunk.rfind(b'\n')+1;pos[i]+=k
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
            halt(child);halt(xchild)
            break
        time.sleep(1)
rc=child.wait()
halt(xchild)  # v6: the slice ends with the frontier worker; the extra worker's context in progress is lost (as at every v5 stop)
xrc=xchild.wait() if xchild else None
if xout:xout.close()
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
def events(lg):  # v5: all JSON events of the log; every distinct WITNESS (continue mode: one per context) gets its own exact row check
  ev=[]
  for line in lg.read_text().splitlines():
    try:e=json.loads(line)
    except ValueError:continue
    if isinstance(e,dict) and 'event' in e:ev.append(e)
  return ev
ev=events(log);xev=events(xlog) if xchild else []  # v6: and of the extra worker's log
counts={};ws=[]
for e in ev:counts[e['event']]=counts.get(e['event'],0)+1
st=[e for e in ev if e['event']=='start']
result.update(on_witness=args.on_witness,events=counts,todo=st[0]['todo'] if st else None,
              processed=counts.get('closed',0)+counts.get('context_too_big',0)+sum('nodes_so_far' in e for e in ev if e['event']=='WITNESS'))
xcounts={}
for e in xev:xcounts[e['event']]=xcounts.get(e['event'],0)+1
result.update(sel,extra={'command':xcmd,'exit':xrc,'log':str(xlog),'events':xcounts} if xchild else None)  # v6
wev=[e for e in ev+xev if e['event']=='WITNESS']
if wev:
    base=json.loads(gzip.decompress((W/'inputs/source-2650.json.gz').read_bytes()))
    rows=base['constraints']+json.loads((inp/'extra.json').read_text())
    for e in wev:
        h=e['holes'];hs=set(h)
        if sorted(h) in [sorted(w['holes']) for w in ws]:continue
        assert len(h)==len(hs)==args.budget and 0 not in hs
        assert all(len(hs&set(r['support']))>=r['rhs'] for r in rows)
        ws.append({'holes':h,'context':e.get('context'),'nodes_so_far':e.get('nodes_so_far'),'independent_exact_row_check':'PASS','rows_checked':len(rows)})
if args.inbox:  # v7: side-pass witnesses still open and still satisfying every row of this run
    base=json.loads(gzip.decompress((W/'inputs/source-2650.json.gz').read_bytes()))
    rows=base['constraints']+json.loads((inp/'extra.json').read_text());took=[];cut=[]
    for q in sorted(Path(args.inbox).glob('w-*.json')):
        if args.stop_witnesses and len(ws)>=args.stop_witnesses:break
        e=json.loads(q.read_text());h=e['holes'];hs=set(h)
        if (bb/f"ctx-{e['context']}.json.gz").exists() or sorted(h) in [sorted(w['holes']) for w in ws]:continue
        assert len(h)==len(hs)==args.budget and 0 not in hs
        if not all(len(hs&set(r['support']))>=r['rhs'] for r in rows):cut.append(q.name);continue
        ws.append({'holes':h,'context':e['context'],'nodes_so_far':e.get('nodes_so_far'),'independent_exact_row_check':'PASS','rows_checked':len(rows),'inbox':str(q)});took.append(q.name)
    result['inbox']={'dir':args.inbox,'taken':took,'cut_by_rows':len(cut)}
result['witnesses']=ws
if use_skip:  # v6: record this run's too-big contexts: frontier at --max-ctx-nodes (tag), extra worker at --extra-cap (tag.x)
    new=[f"{e['context']} {e['nodes_so_far']} {t}\n" for t,es in ((args.tag,ev),(args.tag+'.x',xev)) for e in es if e['event']=='context_too_big']
    with skipf.open('a') as f:f.write(''.join(new))
    result['too_big_recorded']=len(new)
receipt.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
