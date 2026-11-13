#!/usr/bin/env python3
"""Bounded solve of the retained sixfold base, GP clauses and verified cuts.

The embedding family must already have been verified by m6_embed_cycle.py.
Any additional cuts must have passed their independent witness checker.
Proofs are retained and compressed, with exact decompression hash checks;
LRAT checker acceptance is intentionally a separate step.
"""
import argparse,datetime,hashlib,json,re,shutil,subprocess,time
from pathlib import Path


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--archive',type=Path,required=True)
    ap.add_argument('--cadical',type=Path,required=True)
    ap.add_argument('--label',required=True)
    ap.add_argument('--deadline-utc',required=True)
    ap.add_argument('--seconds',type=int,default=300)
    ap.add_argument('--extra-cuts',type=Path)
    ap.add_argument('--family',type=Path)
    a=ap.parse_args();root=a.archive;out=root/a.label;out.mkdir(exist_ok=True)
    start=time.monotonic()
    until=datetime.datetime.fromisoformat(a.deadline_utc)
    deadline=start+max(0,(until-datetime.datetime.now(datetime.timezone.utc)).total_seconds())
    log=(out/'run.jsonl').open('w',buffering=1);manifest=[]
    def emit(event,**kw):
        row={'event':event,'seconds':round(time.monotonic()-start,3),**kw};s=json.dumps(row,sort_keys=True)
        print(s,flush=True);log.write(s+'\n')
    def archive(p):
        z=Path(str(p)+'.zst');subprocess.run(['zstd','-q','-3','-T1','-f',str(p),'-o',str(z)],check=True)
        h=hashlib.sha256();proc=subprocess.Popen(['zstd','-q','-dc',str(z)],stdout=subprocess.PIPE)
        for b in iter(lambda:proc.stdout.read(1<<20),b''):h.update(b)
        proc.stdout.close();assert proc.wait()==0 and h.hexdigest()==digest(p)
        manifest.append({'file':str(p.relative_to(root)),'raw_sha256':digest(p),'zstd_sha256':digest(z),'roundtrip':True})
        (out/'archive_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    def used():
        s=subprocess.check_output(['vm_stat'],text=True);page=int(re.search(r'page size of (\d+)',s).group(1))
        return page*sum(int(re.search(re.escape(n)+r':\s*(\d+)',s).group(1)) for n in ('Pages active','Pages wired down','Pages occupied by compressor'))/1e9
    def solve(proof=None):
        tl=min(a.seconds,int(deadline-time.monotonic()-5));assert tl>0
        cmd=[str(a.cadical),'-q','-t',str(tl)]
        if proof:cmd+=['--lrat','--binary=false']
        cmd.append(str(cnf))
        if proof:cmd.append(str(proof))
        logfile=out/('proof_solve.log' if proof else 'solve.log')
        t0=time.monotonic();peak=0;lastmem=0;reason=None
        with logfile.open('w') as f:
            p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
            try:
                while p.poll() is None:
                    now=time.monotonic()
                    if now>deadline or now-t0>tl+3:reason='time';p.terminate();break
                    if now-lastmem>3:
                        lastmem=now;mem=used();peak=max(peak,mem)
                        if mem>29:reason='total_memory';p.terminate();break
                    time.sleep(.25)
                try:rc=p.wait(timeout=3)
                except subprocess.TimeoutExpired:p.kill();rc=p.wait()
            finally:
                if p.poll() is None:p.kill();p.wait()
        emit('solve',returncode=rc,stop_reason=reason,peak_total_gb=round(peak,3),elapsed=round(time.monotonic()-t0,3),proof=bool(proof))
        return rc,reason,logfile.read_text()
    family=a.family or root/'embedding_family/family.clauses'
    base=root/'base.cnf';meta=json.loads((root/'base.cnf.json').read_text())
    gp=root/'initial_gp.clauses';cuts=json.loads((root/'cuts.json').read_text())
    extra=json.loads(a.extra_cuts.read_text()) if a.extra_cuts else []
    if extra and isinstance(extra,dict):extra=[extra]
    cls=[x['clause'] if 'clause' in x else x['candidate_clause'] for x in cuts+extra]
    nfamily=sum(bool(x.strip()) for x in family.open());ngp=sum(bool(x.strip()) for x in gp.open())
    cnf=out/'instance.cnf'
    with cnf.open('wb') as f,base.open('rb') as b:
        b.readline();f.write(f"p cnf {meta['nv']} {meta['ncl']+ngp+nfamily+len(cls)}\n".encode());shutil.copyfileobj(b,f)
        for part in (gp,family):
            with part.open('rb') as z:shutil.copyfileobj(z,f)
        for c in cls:f.write((' '.join(map(str,c))+' 0\n').encode())
    inputs={'base_sha256':digest(base),'gp_sha256':digest(gp),'family_sha256':digest(family),
            'pilot_cuts_sha256':digest(root/'cuts.json'),'extra_cut_sha256':digest(a.extra_cuts) if a.extra_cuts else None,
            'variables':meta['nv'],'clauses':meta['ncl']+ngp+nfamily+len(cls),'family_clauses':nfamily,
            'extra_clauses':len(extra),'deadline_utc':a.deadline_utc}
    (out/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n');archive(cnf);archive(out/'inputs.json')
    for p in (family,root/'embedding_family/family_witnesses.json',root/'embedding_family/family_verified.json'):
        if not Path(str(p)+'.zst').exists():archive(p)
    emit('start',**inputs)
    rc,reason,txt=solve()
    if rc==10 and 's SATISFIABLE' in txt:
        positive=[]
        for line in txt.splitlines():
            if line.startswith('v '):positive.extend(x for x in map(int,line[2:].split()) if x>0)
        assert positive
        p=out/'model.json';p.write_text(json.dumps(sorted(positive))+'\n');archive(p)
        emit('result',status='SAT',model_sha256=digest(p),all_gp_checked=False)
    elif rc==20 and 's UNSATISFIABLE' in txt:
        emit('unsat_pending_proof')
        if deadline-time.monotonic()>15:
            p=out/'proof.lrat';rc,reason,txt=solve(p)
            if p.exists():archive(p)
            emit('result',status='UNSAT' if rc==20 and reason is None else 'UNSAT_recorded_proof_incomplete',
                 proof_complete=rc==20 and reason is None,checker_acceptance_pending=True)
    else:emit('result',status='UNKNOWN',reason=reason)
    emit('finish');log.close()
if __name__=='__main__':main()
