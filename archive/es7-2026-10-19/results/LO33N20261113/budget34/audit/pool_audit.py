"""Independent pool inventory, full encoder identity, and retained cake replay.

Writes exclusively to this audit record and es308 scratch/audit. Source packets
are only opened for reading. No SAT search or original verifier is imported.
"""
import argparse
import collections
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

from residual_encoder import Geometry

ROOT = Path('/home/jay/research/lean/erdos-szekeres-lean')
RESULTS = ROOT/'cloud/es7-2026-10-19/results'
RECORD = RESULTS/'LO33N20261113/budget34/audit'
WORK = Path('/home/jay/research/data/es308-20261114/audit')
PARENT = WORK.parent
FAST = Path('/home/jay/research/data/fastbb-20261113')
SRC = ROOT/'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
CAKE = Path('/home/jay/.local/bin/cake_lpr')
POOL_SHA = '91a4e36f31712231ed1386576d6dcbe846ddf6c1b0d4de41e225bbdb4a18bcf8'
SOURCE_RAW_SHA = 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'


def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h.update(b)
    return h.hexdigest()


def dump(p,x):
    p.write_text(json.dumps(x,indent=2)+'\n')


def canonical(r):
    s = r['support']
    if (not isinstance(s,list) or any(type(i) is not int or not 0<=i<154 for i in s)
            or s != sorted(set(s))):
        raise ValueError('noncanonical support')
    return tuple(s)


def lines(p):
    with p.open() as f:
        return [json.loads(x) for x in f if x.strip()]


def inventory():
    poolp = PARENT/'inputs/pool812.json'
    assert sha(poolp) == POOL_SHA
    pool = json.loads(poolp.read_text())
    oldp = FAST/'p2/runs/s23/extra.json'
    old = json.loads(oldp.read_text())[2:]
    assert pool == old and len(pool) == 812
    assert len({canonical(r) for r in pool}) == 812
    assert all(r['rhs'] == 1 and type(r['rhs']) is int for r in pool)
    paths = {
        'killtools': FAST/'killtools/certified.jsonl',
        'p2_recert': FAST/'p2/proofs/recert.jsonl',
        'pool_v1': FAST/'p2/pool/pool_v1.json',
        'VERIFY309': RESULTS/'VERIFY309N20261113/logs/residual-row-certificates.jsonl',
        'VERIFY_LO': Path('/home/jay/research/data/verify-LO-20261113/recert.jsonl'),
        'VERIFY_G_570': Path('/home/jay/research/data/verify-G-20261113/kill/all570_recert.jsonl'),
        'VERIFY_G_2': Path('/home/jay/research/data/verify-G-20261113/kill/recert.jsonl'),
    }
    indexed = {}
    for name,p in paths.items():
        rows = json.loads(p.read_text()) if p.suffix == '.json' else lines(p)
        d = collections.defaultdict(list)
        for i,r in enumerate(rows,1):
            d[canonical(r)].append((i,r))
        indexed[name] = d
    rows = []
    counts = collections.Counter()
    for i,r in enumerate(pool):
        s = canonical(r)
        candidates = indexed['p2_recert'][s] or indexed['killtools'][s]
        assert candidates, (i,'no identity record')
        pairs = {(z['cnf_sha256'],z['lrat_sha256']) for _,z in candidates}
        assert len(pairs) == 1, (i,'ambiguous identity')
        cnf,lrat = pairs.pop()
        found=[]
        for folder in ('p2/proofs','killtools/proofs'):
            cp=FAST/folder/(cnf[:16]+'.cnf.zst')
            lp=FAST/folder/(cnf[:16]+'.lrat.zst')
            if cp.is_file() and lp.is_file():
                found.append((cp,lp))
        assert len(found)==1, (i,'missing or ambiguous retained pair')
        cp,lp=found[0]
        refs={}
        for name,index in indexed.items():
            matching=[]
            for line,z in index[s]:
                assert z['cnf_sha256']==cnf, (i,name,'CNF identity mismatch')
                if z.get('lrat_sha256'):
                    assert z['lrat_sha256']==lrat, (i,name,'LRAT identity mismatch')
                matching.append(line)
            if matching:
                refs[name]={'file':str(paths[name]),'entries_1_based':matching}
                counts[name]+=1
        earlier_logs=[]
        oldlog=Path('/home/jay/research/data/verify309-codex-20261113/residual')/(cnf+'.cake.log')
        if oldlog.exists():
            earlier_logs.append({'path':str(oldlog),'sha256':sha(oldlog),
                                 'exact_acceptance_line':'s VERIFIED UNSAT' in oldlog.read_text().splitlines()})
            counts['prior_cake_stdout_available']+=1
        rec={'pool_index':i,'support':list(s),'rhs':1,'cnf_sha256':cnf,'lrat_sha256':lrat,
             'cnf_zst':str(cp),'lrat_zst':str(lp),'cnf_zst_bytes':cp.stat().st_size,
             'lrat_zst_bytes':lp.stat().st_size,'prior_audits_and_ledgers':refs,
             'prior_cake_logs':earlier_logs,'status':'RETAINED; fresh audit pending'}
        rows.append(rec)
        counts['retained_pairs']+=1
        counts['p2_retained' if 'p2/proofs' in str(cp) else 'killtools_retained']+=1
        counts['compressed_bytes']+=cp.stat().st_size+lp.stat().st_size
    sources={str(p):sha(p) for p in [poolp,oldp,SRC,*paths.values(),CAKE,Path(__file__),Path(__file__).with_name('residual_encoder.py')]}
    result={'created_utc':stamp(),'status':'IDENTITIES INVENTORIED; acceptance pending fresh replay',
            'counts':dict(counts),'pool_sha256':POOL_SHA,'input_sha256':sources,'rows':rows,
            'killtools_missing_pool_indices':[r['pool_index'] for r in rows if 'killtools' not in r['prior_audits_and_ledgers']]}
    dump(RECORD/'pool_inventory.json',result)
    return result


def child_limits():
    resource.setrlimit(resource.RLIMIT_AS,(800*1048576,800*1048576))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))


def run_child(cmd,log,seconds):
    with log.open('wb') as f:
        return subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=seconds,
                              preexec_fn=child_limits).returncode


def decompress(src,dst):
    with dst.open('wb') as f:
        subprocess.run(['/usr/bin/zstd','-q','-d','-c',str(src)],stdout=f,check=True,timeout=30,
                       preexec_fn=child_limits)


def replay(inv):
    # A 300 MiB parent plus an 800 MiB sequential child uses <=1100 MiB
    # aggregate virtual-address reservation. The unit supplies the hard ceiling.
    soft,hard=resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS,(300*1048576,hard))
    start=time.monotonic()
    raw=gzip.decompress(SRC.read_bytes())
    assert hashlib.sha256(raw).hexdigest()==SOURCE_RAW_SHA
    catalog=json.loads(raw)
    assert len(catalog['states'])==154 and len(catalog['constraints'])==2650
    geometry=Geometry(catalog['states'])
    logfile=RECORD/'pool_replay.jsonl'
    # An attempt cannot silently append to or overwrite an earlier replay.
    if logfile.exists():
        raise FileExistsError(logfile)
    with logfile.open('x') as results:
        for row in inv['rows']:
            now=dt.datetime.now().astimezone()
            if now.date()!=dt.date(2026,11,14) or now.hour>=11 or (now.hour==10 and now.minute>=54):
                raise TimeoutError('audit stops before10:55 KST')
            t=time.monotonic(); i=row['pool_index']
            h=hashlib.sha256()
            for b in geometry.chunks(tuple(row['support'])):
                h.update(b)
            assert h.hexdigest()==row['cnf_sha256'], (i,'independent encoder hash mismatch')
            cp,lp=Path(row['cnf_zst']),Path(row['lrat_zst'])
            compressed={str(p):sha(p) for p in (cp,lp)}
            cnf,proof=WORK/'current.cnf',WORK/'current.lrat'
            decompress(cp,cnf);decompress(lp,proof)
            assert sha(cnf)==row['cnf_sha256'], (i,'retained CNF mismatch')
            assert sha(proof)==row['lrat_sha256'], (i,'retained LRAT mismatch')
            out=WORK/'cake'/f'row-{i:04d}.out'; err=WORK/'cake'/f'row-{i:04d}.err'
            cmd=[str(CAKE),'--CML_HEAP_SIZE=400','--CML_STACK_SIZE=32',str(cnf),str(proof)]
            with out.open('wb') as o,err.open('wb') as e:
                rc=subprocess.run(cmd,stdout=o,stderr=e,timeout=40,preexec_fn=child_limits).returncode
            # Return code is diagnostic only. Exact stdout acceptance is required.
            assert 's VERIFIED UNSAT' in out.read_text().splitlines(), (i,'cake did not accept',rc)
            assert sha(cnf)==row['cnf_sha256'] and sha(proof)==row['lrat_sha256']
            assert all(sha(p)==v for p,v in compressed.items()), (i,'source changed during replay')
            result={'pool_index':i,'support':row['support'],'rhs':1,'status':'CERTIFIED',
                    'independent_encoder_sha256':h.hexdigest(),'cnf_sha256':sha(cnf),'lrat_sha256':sha(proof),
                    'cnf_bytes':cnf.stat().st_size,'lrat_bytes':proof.stat().st_size,
                    'compressed_inputs_sha256':compressed,'cake_command':cmd,'cake_exit':rc,
                    'cake_stdout':str(out),'cake_stdout_sha256':sha(out),'cake_stderr':str(err),
                    'cake_stderr_sha256':sha(err),'acceptance':'s VERIFIED UNSAT',
                    'seconds':round(time.monotonic()-t,4),'finished_utc':stamp()}
            results.write(json.dumps(result)+'\n');results.flush()
            if i%25==0 or i==811:
                progress={'done':i+1,'total':812,'elapsed_seconds':round(time.monotonic()-start,2),
                          'python_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                          'children_maxrss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                          'updated_utc':stamp()}
                dump(WORK/'progress.json',progress);print(json.dumps(progress),flush=True)
    assert all(sha(p)==h for p,h in inv['input_sha256'].items()),'input or executable changed'
    summary={'status':'CERTIFIED','rows':812,'independently_reconstructed_cnfs':812,
             'accepted_retained_lrats':812,'all_exact_stdout_acceptances':True,'pool_sha256':POOL_SHA,
             'inventory_sha256':sha(RECORD/'pool_inventory.json'),'replay_sha256':sha(logfile),
             'elapsed_seconds':round(time.monotonic()-start,2),'finished_utc':stamp(),
             'python_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'children_maxrss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    dump(RECORD/'pool_summary.json',summary);print(json.dumps(summary),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');args=p.parse_args()
    WORK.mkdir(exist_ok=True);(WORK/'cake').mkdir(exist_ok=True)
    inv=inventory();print(json.dumps(inv['counts']),flush=True)
    if args.replay:
        try:
            replay(inv)
        except BaseException as e:
            dump(WORK/'failure.json',{'status':'NOT CONFIRMED','exception':repr(e),'time_utc':stamp()})
            raise
