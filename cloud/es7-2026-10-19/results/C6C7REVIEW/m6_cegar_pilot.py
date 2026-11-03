#!/usr/bin/env python3
"""Bounded sixfold CEGAR pilot with exact GP/product-cycle cuts.

Retains formulas, models, witnesses and checked compression round trips in the
specified archive. Adds only independently verified two-orbit cuts passing
exact tests on the certified 54-point set. The initial GP file is partial.
No claim of realizability follows if a model survives the restricted search.
"""
import argparse, datetime, hashlib, json, os, re, shutil, signal, subprocess, sys, time
from pathlib import Path


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-archive',type=Path,required=True)
    ap.add_argument('--archive',type=Path,required=True)
    ap.add_argument('--cadical',type=Path,required=True)
    ap.add_argument('--seconds',type=int,default=1500)
    ap.add_argument('--solve-seconds',type=int,default=120)
    ap.add_argument('--rounds',type=int,default=12)
    a=ap.parse_args()
    here=Path(__file__).resolve().parent
    results=here.parent
    dest=a.archive.resolve();dest.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();deadline=start+a.seconds
    log=(dest/'pilot.jsonl').open('w',buffering=1)
    def emit(event,**kw):
        row={'event':event,'seconds':round(time.monotonic()-start,3),**kw}
        text=json.dumps(row,sort_keys=True);print(text,flush=True);log.write(text+'\n')
    emit('start',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
         deadline_utc=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=a.seconds)).isoformat(),
         max_seconds=a.seconds,solve_seconds=a.solve_seconds,rounds=a.rounds)
    manifests=[]
    def archive(path):
        z=path.with_name(path.name+'.zst')
        subprocess.run(['zstd','-q','-3','-T1','-f',str(path),'-o',str(z)],check=True)
        h=hashlib.sha256()
        p=subprocess.Popen(['zstd','-q','-dc',str(z)],stdout=subprocess.PIPE)
        for b in iter(lambda:p.stdout.read(1<<20),b''):h.update(b)
        p.stdout.close();assert p.wait()==0 and h.hexdigest()==digest(path)
        row={'file':str(path.relative_to(dest)),'raw_sha256':digest(path),'zstd_sha256':digest(z),'roundtrip':True}
        manifests.append(row)
        (dest/'archive_manifest.json').write_text(json.dumps(manifests,indent=2)+'\n')
        return row['raw_sha256']
    def used_gb():
        s=subprocess.check_output(['vm_stat'],text=True)
        page=int(re.search(r'page size of (\d+) bytes',s).group(1))
        names=('Pages active','Pages wired down','Pages occupied by compressor')
        return sum(int(re.search(re.escape(n)+r':\s*(\d+)',s).group(1)) for n in names)*page/1e9
    def run(cmd,path,limit):
        """At most one child command; terminate this child on limit/memory guard."""
        launch=time.monotonic();last_mem=0;peak=0;reason=None
        with path.open('w') as f:
            p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
            try:
                while p.poll() is None:
                    now=time.monotonic()
                    if now-launch>limit or now>deadline:
                        reason='time';p.terminate();break
                    if now-last_mem>3:
                        last_mem=now;mem=used_gb();peak=max(peak,mem)
                        if mem>29:
                            reason='total_memory';p.terminate();break
                    time.sleep(.25)
                try:rc=p.wait(timeout=5)
                except subprocess.TimeoutExpired:p.kill();rc=p.wait()
            finally:
                if p.poll() is None:p.kill();p.wait()
        emit('command_done',log=str(path.relative_to(dest)),returncode=rc,
             elapsed=round(time.monotonic()-launch,3),peak_total_gb=round(peak,3),stop_reason=reason)
        return rc,reason
    hashes={line.split()[1]:line.split()[0] for line in (a.source_archive/'SHA256SUMS').read_text().splitlines()}
    for name in ('gp_m6K8t10.cnf.zst','gp_m6K8t10.cnf.model.json.zst','m6K8t10.cnf.json'):
        assert digest(a.source_archive/name)==hashes[name],name
    emit('source_hashes',hashes={n:hashes[n] for n in ('gp_m6K8t10.cnf.zst','gp_m6K8t10.cnf.model.json.zst','m6K8t10.cnf.json')})
    for src,name in (('gp_m6K8t10.cnf.zst','initial_gp.clauses'),('gp_m6K8t10.cnf.model.json.zst','initial.model.json')):
        with (dest/name).open('wb') as out:subprocess.run(['zstd','-q','-dc',str(a.source_archive/src)],stdout=out,check=True)
        archive(dest/name)
    base=dest/'base.cnf'
    rc,reason=run([sys.executable,'-I',str(results/'C7UPPER/gen.py'),'6','8','10',str(base)],dest/'generate.log',90)
    assert rc==0 and reason is None
    basehash=archive(base);maphash=archive(dest/'base.cnf.json')
    assert maphash==hashes['m6K8t10.cnf.json']
    meta=json.loads((dest/'base.cnf.json').read_text())
    gp=dest/'initial_gp.clauses';ngp=sum(1 for l in gp.open() if l.strip())
    emit('base',sha256=basehash,variables=meta['nv'],clauses=meta['ncl'],initial_gp_clauses=ngp)
    shutil.copy2(here/'m6_product_cycles.py',dest/'m6_product_cycles.py')
    shutil.copy2(here/'m6_cegar_pilot.py',dest/'m6_cegar_pilot.py')
    cuts=[];model=dest/'initial.model.json';seen=set()
    for it in range(a.rounds):
        if time.monotonic()+20>deadline:emit('stop',reason='budget_before_round');break
        rd=dest/f'round{it:03d}';rd.mkdir(exist_ok=True)
        rc,reason=run([sys.executable,'-I',str(here/'m6_product_cycles.py'),'--model',str(model),'--map',str(dest/'base.cnf.json'),
                      '--out',str(rd),'--max-layers','2','--max-seconds','40'],rd/'search.log',50)
        if reason or rc:emit('stop',reason='search_incomplete',round=it);break
        wp=rd/'m6_cycle_witness.json';kind='rotation_cycle';verifier='verify_m6_cycle.py'
        if not wp.exists():wp=rd/'gp_sign_violation.json';kind='gp_sign';verifier='verify_m6_gp.py'
        if not wp.exists():emit('stop',reason='no_two_orbit_cut',round=it,model=model.name);break
        vr=rd/'verified.json'
        rc,reason=run([sys.executable,'-I',str(here/'tests'/verifier),'--model',str(model),'--witness',str(wp),'--output',str(vr)],rd/'verify.log',90)
        assert rc==0 and reason is None
        verified=json.loads(vr.read_text());cl=verified['candidate_clause']
        assert tuple(cl) not in seen;seen.add(tuple(cl));cuts.append({'kind':kind,'clause':cl,'witness':str(wp.relative_to(dest)),
               'model_sha256':digest(model),'verified_sha256':digest(vr)})
        (dest/'cuts.json').write_text(json.dumps(cuts,indent=2)+'\n')
        prefix=rd/'cuts_prefix.json';prefix.write_text(json.dumps(cuts,indent=2)+'\n')
        archive(wp);archive(vr);archive(prefix)
        emit('cut',round=it,kind=kind,literals=len(cl),clause=cl,exact54_tests=verified['exact54_labelled_pair_tests'])
        cnf=rd/'instance.cnf'
        with cnf.open('wb') as out,base.open('rb') as inp:
            inp.readline();out.write(f"p cnf {meta['nv']} {meta['ncl']+ngp+len(cuts)}\n".encode())
            shutil.copyfileobj(inp,out)
            with gp.open('rb') as g:shutil.copyfileobj(g,out)
            for cut in cuts:out.write((' '.join(map(str,cut['clause']))+' 0\n').encode())
        archive(cnf)
        tl=min(a.solve_seconds,int(deadline-time.monotonic()-10))
        if tl<=0:emit('stop',reason='budget_before_solve',round=it);break
        rc,reason=run([str(a.cadical),'-q','-t',str(tl),str(cnf)],rd/'solve.log',tl+5)
        txt=(rd/'solve.log').read_text()
        if rc==20 and 's UNSATISFIABLE' in txt:
            proof=rd/'proof.lrat'
            tl=min(a.solve_seconds,int(deadline-time.monotonic()-10))
            if tl<=0:emit('unsat_without_proof',round=it,reason='budget');break
            rc,reason=run([str(a.cadical),'-q','-t',str(tl),'--lrat','--binary=false',str(cnf),str(proof)],rd/'proof_solve.log',tl+5)
            if proof.exists():archive(proof)
            emit('unsat_replay',round=it,returncode=rc,complete=rc==20 and reason is None,
                 cnf=str(cnf.relative_to(dest)),proof=str(proof.relative_to(dest)))
            break
        if rc!=10 or reason or 's SATISFIABLE' not in txt:
            emit('stop',reason='solve_unknown',round=it,returncode=rc);break
        positive=[]
        for line in txt.splitlines():
            if line.startswith('v '):positive.extend(x for x in map(int,line[2:].split()) if x>0)
        assert positive
        model=rd/'model.json';model.write_text(json.dumps(sorted(positive))+'\n');archive(model)
        emit('sat',round=it,model=str(model.relative_to(dest)),positive_variables=len(positive),
             all_gp_relations_checked=False)
    emit('finish',cuts=len(cuts),elapsed=round(time.monotonic()-start,3))
    log.close()
if __name__=='__main__':main()
