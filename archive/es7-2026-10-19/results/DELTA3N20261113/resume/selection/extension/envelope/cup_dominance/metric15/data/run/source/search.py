"""Bounded, sequential pool search; every failure and coordinate CNF retained."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import time
import traceback
from exact import build,certificate,vary
from verify import replay


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):h.update(part)
    return h.hexdigest()


def dump(path,obj):
    with Path(path).open('x') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n')


def atomic(path,obj):
    temp=Path(str(path)+'.tmp')
    temp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');temp.replace(path)


def release_cache(path):
    """Keep retained output from accumulating in the unit's file-cache charge.

    This does not delete or rewrite any file. Call only on closed outputs.
    Added after full-v1: its anonymous RSS was small but its many retained
    CNFs accumulated about a gigabyte of page cache.
    """
    files=[path] if path.is_file() else [p for p in path.iterdir() if p.is_file()]
    for file in files:
        fd=os.open(file,os.O_RDONLY)
        try:
            os.fsync(fd)
            os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED)
        finally:os.close(fd)


def pool(path,n):
    words=path.read_text().split();assert words[:2]==['D3POOL','1'];idx=3;result=[]
    for j in range(int(words[2])):
        m=int(words[idx]);idx+=1;p=[list(map(int,words[idx+2*i:idx+2*i+2])) for i in range(m)];idx+=2*m
        result.append({'name':f'n{n}-i{j:03d}','n':n,'pool_index':j,'P':p,'source':str(path.resolve()),'source_sha256':sha(path)})
    assert idx==len(words)
    return result


def run_case(r,path,binary,solver_seconds=5):
    path.mkdir();start=time.monotonic();dump(path/'input.json',r)
    p=r['P'];m=len(p)
    (path/'points.txt').write_text(f'{m} {r["n"]}\n'+''.join(f'{x} {y}\n' for x,y in p))
    result={'name':r['name'],'n':r['n'],'m':m,'label':'COMPUTED','outcome':'IN_PROGRESS'}
    def finish(**changes):
        result.update(changes);result['seconds']=time.monotonic()-start
        result['files']={f.name:{'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(path.iterdir()) if f.is_file() and f.name!='result.json'}
        dump(path/'result.json',result);release_cache(path);return result
    try:
        with (path/'geometry.json').open('x') as out,(path/'geometry.stderr').open('x') as err:
            proc=subprocess.run([str(binary),str(path/'points.txt')],stdout=out,stderr=err,timeout=20)
        if proc.returncode!=0:
            return finish(outcome='INVALID_PREMISE' if proc.returncode==4 else 'GEOMETRY_FAILURE',geometry_exit=proc.returncode)
        geo=json.loads((path/'geometry.json').read_text());assert geo['valid']
        result['geometry']={k:geo[k] for k in ('maxcap','maxcup','maxgon','chains')}
        envelope,states=build(p,geo);dump(path/'envelope.json',envelope)
        bad=envelope['exposed_triples'];targets=geo['targets'];caps=geo['caps4']
        count=len(targets)+len(caps)+len(bad);literals=sum(map(len,targets))+4*len(caps)+3*len(bad)
        result.update(targets=len(targets),fourcaps=len(caps),exposed_triples=len(bad),exposed_pairs=sum(not s['safe'] for s in states.values()),ambient_pairs=len(envelope['ambient']),variables=m,clauses=count,literals=literals)
        cnf=path/'envelope.cnf'
        with cnf.open('x') as f:
            f.write('c membership variable i+1 for point i; target, fourcap, exposure rows\n')
            f.write(f'p cnf {m} {count}\n')
            for family,sgn in ((targets,1),(caps,-1),(bad,-1)):
                for row in family:f.write(' '.join(str(sgn*(i+1)) for i in row)+' 0\n')
        ambient_pairs={tuple(z['pair']) for z in envelope['ambient']}
        rank3=[t for t in geo['caps3'] if tuple(t[-2:]) not in ambient_pairs]
        result['terminal_rank3_triples']=len(rank3)
        with (path/'terminalsafe.cnf').open('x') as f:
            f.write('c optional terminal-safe membership formula; NOT SOLVED by this track\n')
            f.write(f'p cnf {m} {len(targets)+len(caps)+len(rank3)}\n')
            for family,sgn in ((targets,1),(caps,-1),(rank3,-1)):
                for row in family:f.write(' '.join(str(sgn*(i+1)) for i in row)+' 0\n')
        # Conservative solver estimate at 250 bytes/literal is <=500MB.
        # Driver observed <60MiB on the largest-m profile; allow 128MiB
        # driver plus 100MiB solver overhead, still below 80% of 1000MiB.
        if literals>2000000:return finish(outcome='UNKNOWN_SOLVER_MEMORY_ESTIMATE',solver_memory_estimate_bytes=250*literals)
        with (path/'finder.log').open('x') as out:
            try:proc=subprocess.run(['/usr/bin/cadical','-q',str(cnf)],stdout=out,stderr=subprocess.STDOUT,timeout=solver_seconds)
            except subprocess.TimeoutExpired:return finish(outcome='UNKNOWN_SOLVER_TIMEOUT')
        result['solver_exit']=proc.returncode
        if proc.returncode==20:
            return finish(outcome='UNSAT_UNCERTIFIED_FROZEN',frozen_input=True)
        if proc.returncode!=10:return finish(outcome='UNKNOWN_SOLVER_EXIT')
        log=(path/'finder.log').read_text();assert 's SATISFIABLE' in log
        lits=[int(v) for line in log.splitlines() if line.startswith('v ') for v in line[2:].split() if v!='0']
        assert len(lits)==m and {abs(v) for v in lits}==set(range(1,m+1))
        model={v for v in lits if v>0};A=sorted(v-1 for v in model)
        with cnf.open() as f:
            for line in f:
                if line.startswith(('c','p')):continue
                clause=list(map(int,line.split()));assert clause[-1]==0 and any((v>0)==(abs(v) in model) for v in clause[:-1])
        cert=certificate(p,geo,states,A);dump(path/'certificates.json',cert);dump(path/'model.json',{'literals':lits,'A':A})
        check=replay(p,r['n'],A,cert);dump(path/'positive_replay.json',check)
        return finish(outcome='SAT_EXACT_MODEL_CHECKED',A=A,replay=check)
    except subprocess.TimeoutExpired:
        return finish(outcome='UNKNOWN_GEOMETRY_TIMEOUT')
    except Exception as e:
        (path/'failure.txt').write_text(traceback.format_exc())
        return finish(outcome='CHECK_OR_DRIVER_FAILURE',exception=str(e))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pool-dir',type=Path,required=True);ap.add_argument('--binary',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--seconds',type=int,default=2200);ap.add_argument('--variations',type=int,default=0);ap.add_argument('--first',type=int,default=0);ap.add_argument('--last',type=int,default=315)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    (args.out/'source').mkdir();(args.out/'inputs').mkdir();(args.out/'cases').mkdir()
    for file in Path(__file__).parent.iterdir():
        if file.is_file():shutil.copy2(file,args.out/'source'/file.name)
    shutil.copy2(args.binary,args.out/'source'/'geometry')
    rows=[]
    for n in (7,8):
        src=args.pool_dir/f'full-n{n}.pool';dst=args.out/'inputs'/src.name;shutil.copy2(src,dst)
        new=pool(dst,n)
        for r in new:r['original_source']=str(src.resolve())
        rows.extend(new)
    dump(args.out/'inputs.json',rows)
    dump(args.out/'plan.json',{'args':{k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},'source_hashes':{p.name:sha(p) for p in (args.out/'source').iterdir()},'pool_counts':dict(Counter(r['n'] for r in rows)),'start_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'as_limit':resource.getrlimit(resource.RLIMIT_AS),'solver':'/usr/bin/cadical','solver_sha256':sha('/usr/bin/cadical')})
    results=[];stop='COMPLETE';selected=rows[args.first:args.last]
    def status(current=None):
        atomic(args.out/'status.json',{'current':current,'completed':len(results),'planned_baseline':len(selected),'outcomes':dict(Counter(r['outcome'] for r in results)),'elapsed_seconds':time.monotonic()-start,'stop':stop})
    def sigterm(signum,frame):
        nonlocal stop
        stop='INTERRUPTED_SIGNAL_'+str(signum);status();raise SystemExit(128+signum)
    signal.signal(signal.SIGTERM,sigterm);status()
    for variation in range(args.variations+1):
        for base in selected:
            if time.monotonic()-start>=args.seconds:
                stop='DEADLINE';break
            r=dict(base)
            if variation:
                r['name']+=f'-v{variation:02d}'
                r['P'],r['variation']=vary(base['P'],base['pool_index']*97+variation*31)
                r['variation']['base_name']=base['name']
            status(r['name'])
            out=run_case(r,args.out/'cases'/r['name'],args.binary)
            if variation:
                original=next(z for z in results if z['name']==base['name'])
                if 'exposed_triples' in out and 'exposed_triples' in original:
                    out['baseline_exposed_triples']=original['exposed_triples']
                    a=json.loads((args.out/'cases'/base['name']/'envelope.json').read_text())['exposed_triples']
                    b=json.loads((args.out/'cases'/r['name']/'envelope.json').read_text())['exposed_triples']
                    out['exposure_family_changed']=a!=b
                    release_cache(args.out/'cases'/base['name']/'envelope.json')
                    release_cache(args.out/'cases'/r['name']/'envelope.json')
            results.append(out)
            with (args.out/'results.jsonl').open('a') as f:f.write(json.dumps(out,sort_keys=True)+'\n')
            print(json.dumps({k:out[k] for k in ('name','m','outcome','seconds')},sort_keys=True),flush=True)
            status()
            if out['outcome']=='UNSAT_UNCERTIFIED_FROZEN':
                stop='NEGATIVE_FROZEN';dump(args.out/'FROZEN_NEGATIVE.json',out);break
        if stop!='COMPLETE':break
    status()
    dump(args.out/'summary.json',{'label':'COMPUTED','stop':stop,'cases':results,'counts':dict(Counter(r['outcome'] for r in results)),'elapsed_seconds':time.monotonic()-start,'peak_self_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'scope':'Fixed coordinates and explicitly listed orientation-preserving variations; no universal theorem or certification.'})

if __name__=='__main__':main()
