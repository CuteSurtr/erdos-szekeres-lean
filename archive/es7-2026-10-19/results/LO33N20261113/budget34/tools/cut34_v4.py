#!/usr/bin/env python3
"""Isolated budget-34 candidate selection and retained coupled certificates.

Selection is HEURISTIC. Only a full cake acceptance certifies a candidate.
Never calls old discovery helpers, which assume budget33 and mutate old paths.
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
import sys
import time

W = Path('/home/jay/research/data/es308-20261114')
OLD = Path('/home/jay/research/data/fastbb-20261113/killtools')
PY = '/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python'
PINS = {'coupled.py':'959072b12004eec785bdc3ace47acdd23e41221848515e5c891b431a57ac17db',
        'common.py':'4b74ae776b248cf904a7c4a5b0455aabd2ca2610cace5a3122866bbf7a765358'}

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def stamp(): return datetime.now().astimezone().isoformat()

def dump(p,x):
    p.write_text(json.dumps(x,indent=2)+'\n')

def canonical(s):
    assert isinstance(s,list) and s==sorted(set(s))
    assert all(type(i) is int and 0<=i<154 for i in s)
    return tuple(s)

def select(args):
    resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20))
    data=json.loads(args.witness.read_text())
    h=data if isinstance(data,list) else data['holes']
    H=set(h)
    assert len(h)==len(H) and len(h) in (34,35) and 0 not in H;B=len(h)  # v4: budget = witness size (slice rows sum to it)
    assert all(type(i) is int and 0<=i<154 for i in h)
    raw=gzip.decompress((W/'inputs/source-2650.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()=='e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
    base=json.loads(raw)
    t=sum(i in H for i,s in enumerate(base['states']) if s[0]>=5)
    assert t in (18,19,20,21)  # v4: budget-35 slices; v3: slice 18
    inp=W/'inputs'/(args.input_folder or f's{t}')
    assert inp.resolve().is_relative_to(W/'inputs')
    extra=json.loads((inp/'extra.json').read_text())
    assert extra[0]['rhs']==t and extra[1]['rhs']==B-t
    rows=base['constraints']+extra
    assert all(len(H.intersection(r['support']))>=r['rhs'] for r in rows)
    have={canonical(sorted(r['support'])) for r in rows if r['rhs']==1}
    cand={};sources={}
    for name in ['newrows.json','fnewrows.json','newrows_g2.json']:
        path=OLD/name;sources[str(path)]=sha(path)
        for i,r in enumerate(json.loads(path.read_text())):
            s=canonical(sorted(r['support']))
            if s in have or H.intersection(s) or not 8<=len(s)<=17:continue
            cand.setdefault(s,[]).append({'path':str(path),'index':i})
    chosen=sorted(cand,key=lambda s:(len(s),s))[:args.limit]
    result={'label':'HEURISTIC candidates, not accepted rows','created':stamp(),
            'witness_sha256':sha(args.witness),'holes':sorted(H),'slice':t,
            'exact_row_check':'PASS','rows_checked':len(rows),'input_extra_sha256':sha(inp/'extra.json'),
            'input_folder':str(inp),'candidate_sources':sources,
            'available_candidates':len(cand),
            'candidates':[{'support':list(s),'rhs':1,'discovery_references':cand[s]} for s in chosen]}
    assert not args.out.exists();dump(args.out,result)
    print(json.dumps({'slice':t,'available':len(cand),'selected':len(chosen)}))

def build(args):
    # Caller runs this one child at a time under its aggregate reservation.
    for n,h in PINS.items():assert sha(OLD/n)==h
    for n in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        os.environ[n]='1'
    s=json.loads(args.support.read_text());canonical(s)
    assert 8<=len(s)<=17
    sys.path.insert(0,str(OLD))
    import coupled
    c=coupled.CNF(s,octagon='full',static=True)
    with args.out.open('x') as f:
        f.write(f'p cnf {c.nv} {len(c.clauses)}\n')
        for clause in c.clauses:f.write(' '.join(map(str,clause))+' 0\n')
        f.flush();os.fsync(f.fileno())
    proc=dict(x.split(':',1) for x in Path('/proc/self/status').read_text().splitlines() if ':' in x)
    dump(args.out.with_suffix('.generation.json'),{'support':s,'variables':c.nv,
         'clauses':len(c.clauses),'cnf_sha256':sha(args.out),'encoder_pins':PINS,
         'label':'COMPUTED full coupled encoding; independent audit required',
         'proc_vmhwm_kib':int(proc['VmHWM'].split()[0]),
         'reported_ru_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'resource_note':'ru_maxrss can include a launcher high-water mark; AS and /proc observations govern this job',
         'finished':stamp()})

def certify(args):
    # Aggregate AS is at most 100+1000MiB. Reserve this slot before launching.
    resource.setrlimit(resource.RLIMIT_AS,(100<<20,1100<<20))
    data=json.loads(args.candidates.read_text())
    assert args.out.is_relative_to(W)
    args.out.mkdir(parents=True,exist_ok=False)
    events=[];accepted=[];start=time.monotonic()
    def limits():
        resource.setrlimit(resource.RLIMIT_AS,(1000<<20,1000<<20))
        resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    def run(cmd,path,seconds):
        ts=time.monotonic();peak=0;reason=None
        with path.open('x') as out:
            child=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,preexec_fn=limits)
            while child.poll() is None:
                try:
                    st=dict(x.split(':',1) for x in Path(f'/proc/{child.pid}/status').read_text().splitlines() if ':' in x)
                    rss=int(st.get('VmRSS','0 kB').split()[0]);swap=int(st.get('VmSwap','0 kB').split()[0]);peak=max(peak,rss)
                    if rss>900*1024 or swap:reason='clean memory/swap stop'
                except (FileNotFoundError,ProcessLookupError):pass
                if time.monotonic()-ts>seconds:reason='clean stage deadline'
                if time.monotonic()-start>args.seconds:reason='clean overall deadline'
                if reason:
                    child.terminate()
                    try:child.wait(timeout=3)
                    except subprocess.TimeoutExpired:child.kill();child.wait()
                    break
                time.sleep(.1)
        return {'command':cmd,'exit':child.wait(),'seconds':time.monotonic()-ts,
                'peak_rss_kib':peak,'stop_reason':reason,'log':str(path),'log_sha256':sha(path)}
    for k,r in enumerate(data['candidates']):
        if time.monotonic()-start>args.seconds-15 or len(accepted)>=args.accept:break
        s=list(canonical(r['support']))
        d=args.out/f'{k:04d}';d.mkdir();dump(d/'support.json',s)
        e={'support':s,'rhs':1,'started':stamp(),'stages':[],'label':'COMPUTED attempt'}
        b=run([PY,'-B',str(Path(__file__).resolve()),'build',str(d/'support.json'),str(d/'system.cnf')],d/'build.log',30)
        e['stages'].append(b)
        if b['exit']==0:
            e['generation']=json.loads((d/'system.generation.json').read_text())
            c=run(['/usr/bin/cadical','-q','--lrat=true','--binary=false','-t',str(args.solve_seconds),str(d/'system.cnf'),str(d/'system.lrat')],d/'cadical.log',args.solve_seconds+5)
            e['stages'].append(c)
            if c['exit']==20:
                v=run(['/home/jay/.local/bin/cake_lpr','--CML_HEAP_SIZE=600','--CML_STACK_SIZE=32',str(d/'system.cnf'),str(d/'system.lrat')],d/'cake.log',60)
                e['stages'].append(v)
                if 's VERIFIED UNSAT' in (d/'cake.log').read_text().splitlines():
                    e['label']='CERTIFIED';e['verdict']='s VERIFIED UNSAT';accepted.append(e)
        e['files']={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in d.iterdir() if p.is_file()}
        e['finished']=stamp();dump(d/'receipt.json',e);events.append(e)
        dump(args.out/'status.json',{'attempted':len(events),'certified':len(accepted),'seconds':time.monotonic()-start})
        for p in d.iterdir():
            if p.is_file():
                fd=os.open(p,os.O_RDONLY)
                try:os.fdatasync(fd);os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED)
                finally:os.close(fd)
        print(json.dumps({'index':k,'support':s,'label':e['label'],'seconds':time.monotonic()-start}),flush=True)
    dump(args.out/'accepted.json',accepted)
    dump(args.out/'result.json',{'finished':stamp(),'attempted':len(events),'certified':len(accepted),'seconds':time.monotonic()-start,
         'scope':'Additional coupled rows only; no bound claim','candidate_sha256':sha(args.candidates),'script_sha256':sha(__file__)})

if __name__=='__main__':
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest='mode',required=True)
    q=sp.add_parser('select');q.add_argument('witness',type=Path);q.add_argument('out',type=Path);q.add_argument('--limit',type=int,default=50);q.add_argument('--input-folder',default=None)
    q=sp.add_parser('build');q.add_argument('support',type=Path);q.add_argument('out',type=Path)
    q=sp.add_parser('certify');q.add_argument('candidates',type=Path);q.add_argument('out',type=Path);q.add_argument('--seconds',type=int,default=300);q.add_argument('--solve-seconds',type=int,default=20);q.add_argument('--accept',type=int,default=8)
    a=p.parse_args();globals()[a.mode](a)
