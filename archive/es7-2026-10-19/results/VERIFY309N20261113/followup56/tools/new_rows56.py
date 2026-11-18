"""Prepare/certify only four new CNF obligations, using the prior independent encoder.
Generation can run as a short bounded probe. Certification is for the parent's
centrally scheduled unit only. Every failed attempt and every proof is retained.
Usage: new_rows56.py generate INDEX | new_rows56.py certify INDEX --seconds 180 --heap 512
"""
import argparse
import hashlib
import json
import os
import pathlib
import signal
import shutil
import subprocess
import time
from model import HERE, WORK
from coupled66_independent import Model, clause, line

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h.update(b)
    return h.hexdigest()

def generate(index):
    item=json.loads((HERE/'data/new_certificates.json').read_text())[index]
    kind,r=item['kind'],item['record']; support=r['core'] if kind=='tmpl' else r['support']
    dest=WORK/'new_rows'/r['cnf_sha256']; dest.mkdir(parents=True,exist_ok=True)
    full=dest/'full.cnf'; body=dest/'full.body'
    assert not full.exists() and not body.exists(), 'preserve earlier generation'
    model=Model(len(support)); nc=0; start=time.monotonic()
    with body.open('xb') as f:
        def put(lits):
            nonlocal nc
            c=clause(lits)
            if c is not None:
                f.write(line(c)); nc+=1
        for c in model.static('octs' not in r):
            put(c)
        for q in r.get('octs',[]):
            assert q==sorted(set(q)) and len(q)==8 and all(0<=i<model.n for i in q)
            put(model.oct(q))
        keep={tuple(t) for t in r['tests']} if kind=='tmpl' else None
        seen=set()
        for c,tag in model.dynamic(support):
            if keep is None or tag in keep:
                put(c); seen.add(tag)
        assert keep is None or keep<=seen
    with full.open('xb') as f, body.open('rb') as g:
        f.write(f'p cnf {model.nv} {nc}\n'.encode()); shutil.copyfileobj(g,f,1<<20)
    actual=sha(full)
    rec={'index':index,'kind':kind,'id':r.get('id'),'support':support,'n':len(support),
         'clauses':nc,'vars':model.nv,'full_sha256':actual,'expected_sha256':r['cnf_sha256'],
         'hash_matches':actual==r['cnf_sha256'],'bytes':full.stat().st_size,
         'generation_seconds':round(time.monotonic()-start,3)}
    (dest/'generation.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec),flush=True)
    assert rec['hash_matches'], 'independent encoder hash mismatch'

def certify(index, seconds, heap):
    item=json.loads((HERE/'data/new_certificates.json').read_text())[index]
    r=item['record']; dest=WORK/'new_rows'/r['cnf_sha256']
    generation=json.loads((dest/'generation.json').read_text())
    assert generation['hash_matches'] and sha(dest/'full.cnf')==r['cnf_sha256']
    attempt=dest/('attempt-'+time.strftime('%Y%m%dT%H%M%S'))
    attempt.mkdir(exist_ok=False)
    receipts=attempt/'stages.jsonl'
    def run(stage,cmd,limit):
        start=time.monotonic()
        with (attempt/(stage+'.log')).open('w') as f:
            proc=subprocess.Popen(['/usr/bin/time','-v']+cmd,stdout=f,
                                  stderr=subprocess.STDOUT,start_new_session=True)
            try:
                code=proc.wait(timeout=limit)
                result={'stage':stage,'returncode':code}
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGTERM)
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid,signal.SIGKILL); proc.wait()
                result={'stage':stage,'result':'UNKNOWN TIMEOUT'}
        result.update(seconds=round(time.monotonic()-start,3),command=cmd)
        with receipts.open('a') as f:
            f.write(json.dumps(result)+'\n')
        print(json.dumps(result),flush=True)
        return result
    fullproof=attempt/'full.lrat'
    result=run('full-solve',['/usr/bin/cadical','-q','--lrat=true','--binary=false',str(dest/'full.cnf'),str(fullproof)],seconds)
    assert result.get('returncode')==20, 'full solve not UNSAT; see retained logs/proof'
    # This selector is not trusted as a proof checker. The selected clauses
    # are checked to be original clauses, then solved/certified again.
    used=set(); m=generation['clauses']
    with fullproof.open() as f:
        for raw in f:
            words=raw.split()
            if len(words)<2 or words[1]=='d':
                continue
            z=words.index('0',1)
            used.update(abs(int(x)) for x in words[z+1:-1] if 0<abs(int(x))<=m)
    sub=attempt/'selected.cnf'; count=0
    with (dest/'full.cnf').open('rb') as f, sub.open('xb') as g:
        next(f); g.write(f'p cnf {generation["vars"]} {len(used)}\n'.encode())
        for i,l in enumerate(f,1):
            if i in used:
                g.write(l); count+=1
    assert count==len(used) and count>0
    proof=attempt/'selected.lrat'
    result=run('sub-solve',['/usr/bin/cadical','-q','--lrat=true','--binary=false',str(sub),str(proof)],seconds)
    assert result.get('returncode')==20, 'sub solve not UNSAT'
    result=run('cake',['/home/jay/.local/bin/cake_lpr',f'--CML_HEAP_SIZE={heap}','--CML_STACK_SIZE=32',str(sub),str(proof)],120)
    assert 's VERIFIED UNSAT' in (attempt/'cake.log').read_text().splitlines(), 'cake has no literal success line'
    rec={**generation,'result':'CERTIFIED','sub_clauses':count,'sub_sha256':sha(sub),
         'lrat_sha256':sha(proof),'full_lrat_sha256':sha(fullproof),'attempt':str(attempt)}
    (attempt/'receipt.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec),flush=True)
    # Retain raw proofs too; no deletion before independent replay. zstd -k
    # makes archival copies and is explicitly one thread.
    for p in (fullproof,proof):
        result=run('compress-'+p.stem,['zstd','-q','-T1','-3','-k',str(p)],30)
        assert result.get('returncode')==0, 'certificate passed; compression incomplete'

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('mode',choices=['generate','certify'])
    ap.add_argument('index',type=int,choices=range(4)); ap.add_argument('--seconds',type=int,default=180)
    ap.add_argument('--heap',type=int,default=512)
    args=ap.parse_args()
    if args.mode=='generate': generate(args.index)
    else: certify(args.index,args.seconds,args.heap)
