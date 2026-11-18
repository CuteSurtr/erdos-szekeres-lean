#!/usr/bin/env python3
"""High-cap side pass for a budget-35 packet, safe to run while the loop runs (track AS, 16 Nov 2026). Finder only.

One fastbb2 invocation per context (unchanged binary, run_tree_v6's search options, 1 thread, --ctx=<c>), in a SIDE
packet whose master.txt is a byte copy of the TARGET packet's. Rows: the version named by the target's master.json
(the version of the loop's newest finder), re-read before every invocation. Selection: open target contexts whose
largest record in the target's TOO_BIG.txt exceeds --above (the loop never selects these when --above equals its
largest cap), minus those recorded here above --cap, minus those whose witness found here still satisfies the rows.
- closed: with --import the ctx file is copied into the target (temporary name outside the ctx-*.json.gz pattern,
  then os.link, which never replaces a file) only if the side master.txt equals the target's, the file's header
  (context, missing, occupied) equals the target's contexts.json entry, and the body of the rows.txt it was solved
  with is a line prefix of the rows.txt of the version the target's master.json names at import time.
- WITNESS: exact row check against the invocation's rows (as run_tree), then <inbox>/w-<time>-c<ctx>.json, which
  run_tree_v7 re-checks against its round's rows before the loop may use it.
- context_too_big: a line '<c> <nodes_so_far> <tag>' in the side packet's TOO_BIG.txt (never the target's).
Nothing else is written into the target. Logs, receipts and imports.jsonl: runs/b<B>s<T>/<side>-logs/.
"""
import argparse
from datetime import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import time

p=argparse.ArgumentParser()
p.add_argument('--slice',type=int,default=20)
p.add_argument('--budget',type=int,default=35)
p.add_argument('--target',default='bb')
p.add_argument('--side',required=True)  # new folder name under runs/b<B>s<T>/, e.g. bb-hc1
p.add_argument('--above',type=int,default=300000)  # the loop's largest cap (v11: --extra-cap)
p.add_argument('--cap',type=int,default=1000000)  # fastbb2 --max-ctx-nodes here; see V12_NOTES: replay memory ~6.5 KB/node
p.add_argument('--deadline',required=True)
p.add_argument('--inbox',default=None)  # default runs/.../<side>-inbox
p.add_argument('--import',dest='do_import',action='store_true')
p.add_argument('--import-only',action='store_true')  # import the side packet's closed contexts, run nothing
p.add_argument('--part',default='0/1')  # k/m: only contexts with c % m == k (several side passes, one side packet each)
p.add_argument('--ctx',default='')  # tests: restrict to these contexts (still subject to the selection rules)
p.add_argument('--max-runs',type=int,default=0)
p.add_argument('--rss-mib',type=int,default=1000)
a=p.parse_args()
resource.setrlimit(resource.RLIMIT_AS,(300<<20,1400<<20))
W=Path('/home/jay/research/data/es308-20261114');FB=W/'bin/fastbb2';SRC=W/'inputs/source-2650.json.gz'
RUN=W/'runs'/(f's{a.slice}' if a.budget==34 else f'b{a.budget}s{a.slice}')
TGT=RUN/a.target;SIDE=RUN/a.side;LOGS=RUN/f'{a.side}-logs';IN=Path(a.inbox) if a.inbox else RUN/f'{a.side}-inbox'
assert TGT.is_dir() and (TGT/'master.txt').exists() and a.side!=a.target and SIDE.parent==RUN and a.cap>a.above
deadline=datetime.fromisoformat(a.deadline).timestamp();K,M=map(int,a.part.split('/'))
only={int(x) for x in a.ctx.split(',') if x}
def sha(q):
    h=hashlib.sha256()
    with Path(q).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def stamp():return datetime.now().astimezone().isoformat()
def write_new(q,text):  # atomic create; never replaces
    t=q.with_name('.'+q.name+'.tmp');t.write_text(text);os.link(t,q);os.unlink(t)
def record(f):
    k={}
    if f.exists():
        for line in f.read_text().split('\n')[:-1]:  # complete lines only (the loop appends while this runs)
            if line.strip():c,n=map(int,line.split()[:2]);k[c]=max(k.get(c,0),n)
    return k
def version():  # input folder of the version named by the target's master.json
    head=(TGT/'master.json').read_bytes()[:4096].decode();m=json.loads(head[:head.index(', "budget"')]+'}')
    assert Path(m['source'])==SRC;ex=Path(m['extra']);assert ex.name=='extra.json' and ex.parent.parent==W/'inputs'
    return ex.parent
def body(inp):  # rows.txt without its 8-line header (the header names the version's own extra.json)
    lines=(inp/'rows.txt').read_text().splitlines();assert lines[0]=='FASTBB-ROWS 1' and lines[1]==f'source {SRC}' and lines[7].startswith('rows ')
    return lines[8:]
BASE=json.loads(gzip.decompress(SRC.read_bytes()))['constraints']
def rows_of(inp):return BASE+json.loads((inp/'extra.json').read_text())
def satisfies(h,rows):hs=set(h);return len(h)==len(hs)==a.budget and 0 not in hs and all(len(hs&set(r['support']))>=r['rhs'] for r in rows)
def ctx_header(q):
    with gzip.open(q,'rt') as f:s=f.read(8192)
    j=s.index(',"root":');return json.loads(s[:j]+'}')
def import_ctx(c,inp):
    src=SIDE/f'ctx-{c}.json.gz';dst=TGT/f'ctx-{c}.json.gz'
    if dst.exists():return 'target already has the context'
    if sha(SIDE/'master.txt')!=sha(TGT/'master.txt'):return 'refused: side master.txt differs from the target'
    d={x['context']:x for x in json.loads((TGT/'contexts.json').read_text())}.get(c)
    if d is None or ctx_header(src)!={'context':c,'missing':d['missing'],'occupied':d['occupied']}:return 'refused: header differs from the target context'
    tv=version();bv,bt=body(inp),body(tv)
    if bt[:len(bv)]!=bv:return f'refused: rows of {inp.name} are not a prefix of {tv.name}'
    tmp=TGT/f'.import-ctx-{c}.{os.getpid()}.tmp';shutil.copyfile(src,tmp)
    fd=os.open(tmp,os.O_RDONLY);os.fdatasync(fd);os.close(fd)
    h=sha(src)
    if sha(tmp)!=h:os.unlink(tmp);return 'refused: copy differs'
    try:os.link(tmp,dst)
    except FileExistsError:os.unlink(tmp);return 'target closed it meanwhile'
    os.unlink(tmp)
    with (LOGS/'imports.jsonl').open('a') as f:f.write(json.dumps({'context':c,'sha256':h,'bytes':src.stat().st_size,'solved_with':inp.name,'target_version_at_import':tv.name,'time':stamp()})+'\n')
    return 'imported'
def selected(inp,rows):
    tk=record(TGT/'TOO_BIG.txt');sk=record(SIDE/'TOO_BIG.txt');out=[];stuck=[]
    for x in json.loads((TGT/'contexts.json').read_text()):
        c=x['context']
        if (TGT/f'ctx-{c}.json.gz').exists() or tk.get(c,0)<=a.above or sk.get(c,0)>a.cap or c%M!=K or (only and c not in only):continue
        if (SIDE/f'ctx-{c}.json.gz').exists():continue  # closed here; import off or refused (see imports/receipts)
        wf=SIDE/f'witness-ctx-{c}.json'
        if wf.exists() and satisfies(json.loads(wf.read_text())['holes'],rows):stuck.append(c);continue  # its witness still stands
        out.append(c)
    return out,stuck
def child_limit():
    resource.setrlimit(resource.RLIMIT_AS,(1400<<20,1400<<20));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def events(q):
    ev=[]
    for line in q.read_text().splitlines():
        try:e=json.loads(line)
        except ValueError:continue
        if isinstance(e,dict) and 'event' in e:ev.append(e)
    return ev

if not SIDE.exists():  # setup: master files copied from the target (opened read-only)
    SIDE.mkdir()
    for n in ['master.txt','master.json','contexts.json']:shutil.copyfile(TGT/n,SIDE/n)
LOGS.mkdir(exist_ok=True);IN.mkdir(exist_ok=True)
assert sha(SIDE/'master.txt')==sha(TGT/'master.txt'),'side master differs from target master'
status={'started':stamp(),'args':vars(a),'runs':0,'closed':0,'imported':0,'too_big':0,'witnesses':0,'refused':[]}
if a.import_only:
    inp=version()
    for q in sorted(SIDE.glob('ctx-*.json.gz')):
        c=int(q.name[4:-8]);rc=json.loads((LOGS/'solved_with.json').read_text()).get(str(c)) if (LOGS/'solved_with.json').exists() else None
        r=import_ctx(c,W/'inputs'/rc) if rc else 'refused: no solved_with entry'
        print(c,r);status['imported']+=r=='imported'
    raise SystemExit(0)
k=1
while True:
    while (LOGS/f'h{k}.json').exists() or (LOGS/f'h{k}.log').exists():k+=1
    left=int(deadline-time.time())-30
    if left<60 or (a.max_runs and status['runs']>=a.max_runs):break
    inp=version();rows=rows_of(inp);sel,stuck=selected(inp,rows)
    status.update(version=inp.name,selectable=len(sel),stuck_on_valid_witness=stuck,time=stamp())
    (LOGS/'status.json').write_text(json.dumps(status,indent=1)+'\n')
    if not sel:break
    c=sel[0];tag=f'h{k}';log=LOGS/f'{tag}.log'
    if (SIDE/'WITNESS.json').exists():os.rename(SIDE/'WITNESS.json',SIDE/f'WITNESS.json.before-{tag}')  # else fastbb2 stops at once on it (old_witness_still_valid)
    before={str(q):sha(q) for q in [inp/'rows.txt',inp/'extra.json',SRC,FB]}
    cmd=[str(FB),'solve',str(inp/'rows.txt'),str(a.budget),'1','2048',str(SIDE),'--slice=1','--on-witness=continue',f'--time-limit={left}',
         f'--max-ctx-nodes={a.cap}','--ktop=16','--dtop=8','--klow=4','--sbiter=1000',f'--ctx={c}']
    t0=time.monotonic();peak=0;stop=None
    with log.open('x') as out:
        ch=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,preexec_fn=child_limit)
        while ch.poll() is None:
            try:
                st={l.split(':',1)[0]:l.split(':',1)[1].strip() for l in Path(f'/proc/{ch.pid}/status').read_text().splitlines() if ':' in l}
                rss=int(st.get('VmRSS','0 kB').split()[0]);peak=max(peak,rss)
                if rss>=a.rss_mib*1024 or int(st.get('VmSwap','0 kB').split()[0]):stop='RSS/swap guard'
            except (FileNotFoundError,ProcessLookupError,PermissionError):pass
            if time.monotonic()-t0>left+120:stop='outer wall guard'
            if stop:
                ch.terminate()
                try:ch.wait(timeout=5)
                except subprocess.TimeoutExpired:ch.kill();ch.wait()
                break
            time.sleep(1)
    rc=ch.wait()
    assert {q:sha(Path(q)) for q in before}==before,'inputs changed during the invocation'
    ev=events(log);res={'label':'COMPUTED finder result (side pass); not an EXACT TREE','tool_sha256':sha(Path(__file__)),'tag':tag,'context':c,
        'command':cmd,'exit':rc,'seconds':time.monotonic()-t0,'peak_sampled_rss_kib':peak,'stop_reason':stop,'input_hashes':before,
        'events':[e for e in ev if e['event'] in ('closed','context_too_big','WITNESS','abandoned')],'finished':stamp()}
    for e in ev:
        if e['event']=='closed' and e['context']==c:
            status['closed']+=1;sw=LOGS/'solved_with.json';d=json.loads(sw.read_text()) if sw.exists() else {}
            d[str(c)]=inp.name;sw.write_text(json.dumps(d,indent=1)+'\n')
            res['import']=import_ctx(c,inp) if a.do_import else 'not requested'
            status['imported']+=res['import']=='imported'
            if res['import'].startswith('refused'):status['refused'].append([c,res['import']])
        elif e['event']=='context_too_big':
            with (SIDE/'TOO_BIG.txt').open('a') as f:f.write(f"{e['context']} {e['nodes_so_far']} {tag}\n")
            status['too_big']+=1
        elif e['event']=='WITNESS' and 'nodes_so_far' in e:
            assert satisfies(e['holes'],rows),'witness fails the exact row check'
            q=IN/f"w-{datetime.now():%Y%m%dT%H%M%S}-c{e['context']}.json"
            write_new(q,json.dumps({'holes':e['holes'],'context':e['context'],'nodes_so_far':e['nodes_so_far'],'input_folder':inp.name,
                                    'independent_exact_row_check':'PASS','rows_checked':len(rows),'log':str(log),'time':stamp()})+'\n')
            res.setdefault('inbox',[]).append(str(q));status['witnesses']+=1
    (LOGS/f'{tag}.json').write_text(json.dumps(res,indent=1)+'\n');status['runs']+=1
    if stop or not any(e['event'] in ('closed','context_too_big','WITNESS') for e in ev):status['ended_by']=stop or f'no result for context {c} (exit {rc})';break
status['finished']=stamp();(LOGS/'status.json').write_text(json.dumps(status,indent=1)+'\n')
print(json.dumps(status,indent=1))
