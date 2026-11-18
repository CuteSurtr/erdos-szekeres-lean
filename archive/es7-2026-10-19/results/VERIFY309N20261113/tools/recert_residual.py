"""Link all 578 residual rows to the audited encoder and independent LRAT evidence.
130 identical CNFs were independently replayed by VERIFY_LO; replay the other 448.
"""
import collections, gzip, hashlib, json, pathlib, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parents[5]
R=ROOT/'cloud/es7-2026-10-19/results'
sys.path.insert(0,str(R/'RES33N20261113/tools'))
import coupled
V=pathlib.Path('/home/jay/research/data/verify309-codex-20261113/residual'); V.mkdir(parents=True,exist_ok=True)
cert=collections.defaultdict(list)
for l in (R/'LO33N20261113/data/certified.jsonl').open():
    r=json.loads(l); assert r['verdict']=='s VERIFIED UNSAT'; cert[tuple(r['support'])].append(r)
assert len(cert)==578
prior={}
for l in pathlib.Path('/home/jay/research/data/verify-LO-20261113/recert.jsonl').open():
    r=json.loads(l); assert r['cnf_matches_record'] and r['cadical_exit']==20 and r['cake']=='s VERIFIED UNSAT'
    prior[tuple(r['support'])]=r['cnf_sha256']
assert len(prior)==130
out=V/'certificates.jsonl'; done={tuple(json.loads(l)['support']) for l in out.open()} if out.exists() else set()
for support,records in sorted(cert.items(),key=lambda p:(len(p[0]),p[0])):
    if support in done: continue
    t=time.time(); txt=coupled.CNF(list(support)).dimacs(); raw=txt.encode(); del txt
    h=hashlib.sha256(raw).hexdigest(); assert any(r['cnf_sha256']==h for r in records)
    rec={'support':support,'cnf_sha256':h,'cnf_matches_record':True}
    if prior.get(support)==h:
        rec.update(result='INHERITED independently verified identical CNF',evidence='LO33N20261113/VERIFY_LO.md')
    else:
        cnf=V/'current.cnf'; proof=V/(h+'.lrat'); cnf.write_bytes(raw)
        with gzip.open(V/(h+'.cnf.gz'),'wb',compresslevel=1) as f: f.write(raw)
        del raw
        with (V/(h+'.cadical.log')).open('w') as f:
            rc=subprocess.run(['/usr/bin/cadical','-q','--lrat=true','--binary=false',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT).returncode
        assert rc==20
        cake=V/(h+'.cake.log')
        with cake.open('w') as f:
            subprocess.run(['/home/jay/.local/bin/cake_lpr','--CML_HEAP_SIZE=700','--CML_STACK_SIZE=100',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT)
        assert 's VERIFIED UNSAT' in cake.read_text().splitlines(),cake.read_text()[-300:]
        digest=hashlib.sha256()
        with proof.open('rb') as f:
            for b in iter(lambda:f.read(1<<20),b''): digest.update(b)
        rec.update(result='CERTIFIED',lrat_sha256=digest.hexdigest(),lrat_matches_record=any(r['lrat_sha256']==digest.hexdigest() for r in records))
    rec['seconds']=round(time.time()-t,2)
    with out.open('a') as f: f.write(json.dumps(rec)+'\n')
    print(json.dumps(rec),flush=True); done.add(support)
print(json.dumps({'result':'ALL RESIDUAL ROWS COVERED','rows':len(done)}),flush=True)
