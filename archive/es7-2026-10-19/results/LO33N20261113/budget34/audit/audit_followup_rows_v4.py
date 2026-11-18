"""Generic appended-row audit; candidate proximity is not proof of a new exclusion."""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import resource
import re
import subprocess
import time

from residual_encoder import Geometry
from pool_audit import ROOT,RECORD,WORK,SRC,CAKE,sha,dump,child_limits,SOURCE_RAW_SHA


def audit(version):
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',version)
    soft,hard=resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS,(300*1048576,hard))
    base=WORK.parent/f'cuts-{version}';accepted=base/'accepted.json'
    candidates=WORK.parent/f'candidates-{version}.json'
    recdir=RECORD/f'cuts-{version}';outdir=WORK/f'cuts-{version}'
    recdir.mkdir(exist_ok=True);outdir.mkdir(exist_ok=True)
    assert not (recdir/'replay.jsonl').exists(),'exclusive new attempt required'
    a=json.loads(accepted.read_text()); c=json.loads(candidates.read_text())
    assert len(a)>0 and len({tuple(r['support']) for r in a})==len(a)
    eligible={tuple(r['support']):i for i,r in enumerate(c['candidates'])}
    oldpool=json.loads((WORK.parent/'inputs/pool812.json').read_text())
    oldsupports={tuple(r['support']) for r in oldpool}
    raw=gzip.decompress(SRC.read_bytes());assert hashlib.sha256(raw).hexdigest()==SOURCE_RAW_SHA
    cat=json.loads(raw);G=Geometry(cat['states'])
    matching_witnesses=[p for p in (WORK.parent/'runs').glob('*/bb*/WITNESS.json*')  # v4: runs/b35s<T> too  # v3: every slice; v2: successor packets
                        if p.is_file() and sha(p)==c['witness_sha256']]
    assert matching_witnesses,'no actual witness packet matches the candidate provenance'
    witness_path=sorted(matching_witnesses,key=lambda p: ('snapshot' not in p.name,p.name))[0]
    witness_bytes=witness_path.read_bytes()
    assert hashlib.sha256(witness_bytes).hexdigest()==c['witness_sha256']
    if 'snapshot' not in witness_path.name:
        witness_path=outdir/'witness-frozen.json'
        witness_path.write_bytes(witness_bytes)
    witness=json.loads(witness_bytes)
    H=set(witness['holes'])
    assert len(H)==len(witness['holes']) and len(H) in (34,35) and 0 not in H  # v4: budget 35
    F={i for i,s in enumerate(cat['states']) if s[0]>=5}
    assert len(F)==84 and len(H&F) in (18,19,20,21) and len(H&F)+len(H-F)==len(H)  # v3: slice from the witness, tied below
    extra_path=Path(c['input_folder'])/'extra.json' if c.get('input_folder') else WORK.parent/'inputs/s20/extra.json'
    assert extra_path.parent.parent==WORK.parent/'inputs'
    if c.get('input_extra_sha256'):assert sha(extra_path)==c['input_extra_sha256']
    initial_extra=json.loads(extra_path.read_text())
    assert initial_extra[0]['rhs']==len(H&F) and initial_extra[1]['rhs']==len(H-F)  # v3: witness slice = input slice
    assert all(len(set(r['support'])&H)>=r['rhs'] for r in cat['constraints']+initial_extra)
    pins={str(p):sha(p) for p in [accepted,candidates,SRC,witness_path,extra_path,Path(__file__),Path(__file__).with_name('residual_encoder.py'),CAKE]}
    results=[];started=time.monotonic()
    with (recdir/'replay.jsonl').open('x') as out:
        for r in a:
            support=r['support'];key=tuple(support)
            assert support==sorted(set(support)) and all(type(i)is int and 0<=i<154 for i in support)
            assert r['rhs']==1 and type(r['rhs'])is int and key in eligible and key not in oldsupports
            overlap=len(set(support)&H)
            if version=='near9':assert len(support)==9 and overlap==1
            k=eligible[key];folder=base/f'{k:04d}';rp=folder/'receipt.json'
            assert json.loads(rp.read_text())==r
            assert json.loads((folder/'support.json').read_text())==support
            for filename,info in r['files'].items():
                q=Path(filename);assert q.parent==folder
                assert q.stat().st_size==info['bytes'] and sha(q)==info['sha256']
            cnf=folder/'system.cnf';proof=folder/'system.lrat';cake=folder/'cake.log'
            assert 's VERIFIED UNSAT' in cake.read_text().splitlines()
            h=hashlib.sha256()
            for b in G.chunks(key):h.update(b)
            assert h.hexdigest()==sha(cnf)==r['generation']['cnf_sha256']
            ch,ph=sha(cnf),sha(proof)
            fresh=outdir/f'{k:04d}.cake.out';err=outdir/f'{k:04d}.cake.err'
            command=[str(CAKE),'--CML_HEAP_SIZE=400','--CML_STACK_SIZE=32',str(cnf),str(proof)]
            with fresh.open('wb') as f,err.open('wb') as e:
                rc=subprocess.run(command,stdout=f,stderr=e,timeout=45,preexec_fn=child_limits).returncode
            assert 's VERIFIED UNSAT' in fresh.read_text().splitlines()
            assert sha(cnf)==ch and sha(proof)==ph
            rr={'candidate_index':k,'support':support,'rhs':1,'label':'CERTIFIED',
                'independent_encoder_sha256':h.hexdigest(),'cnf_sha256':ch,'lrat_sha256':ph,
                'cnf':str(cnf),'lrat':str(proof),'parent_receipt':str(rp),'parent_receipt_sha256':sha(rp),
                'parent_cake_log':str(cake),'parent_cake_sha256':sha(cake),'fresh_cake_stdout':str(fresh),
                'fresh_cake_sha256':sha(fresh),'fresh_cake_stderr':str(err),'cake_exit':rc,
                'command':command,'acceptance':'s VERIFIED UNSAT','cuts_stated_witness':overlap==0,'old_witness_intersection':overlap}
            out.write(json.dumps(rr)+'\n');out.flush();results.append(rr)
            print(json.dumps({'candidate':k,'label':'CERTIFIED','cnf_sha256':ch}),flush=True)
    assert all(sha(p)==h for p,h in pins.items())
    summary={'label':'CERTIFIED','version':version,'rows':len(results),'own_encoder_matches':len(results),
             'fresh_cake_acceptances':len(results),'old_witness_exact_row_check':f'PASS ({2650+len(initial_extra)} rows, {len(H)} holes, F{len(H&F)},Lo{len(H-F)},state0 occupied)',
             'rows_cutting_old_witness':sum(r['cuts_stated_witness'] for r in results),'old_witness_intersection_counts':{str(k):sum(r['old_witness_intersection']==k for r in results) for k in sorted({r['old_witness_intersection'] for r in results})},'accepted_sha256':sha(accepted),
             'replay_sha256':sha(recdir/'replay.jsonl'),'input_sha256':pins,
             'seconds':round(time.monotonic()-started,3),'finished_local':dt.datetime.now().astimezone().isoformat(),
             'scope':'Additional rows only; no finite exclusion or ES bound follows from these rows alone',
             'parent_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'child_maxrss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    dump(recdir/'summary.json',summary);print(json.dumps(summary),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('versions',nargs='+');args=p.parse_args()
    for version in args.versions:audit(version)
