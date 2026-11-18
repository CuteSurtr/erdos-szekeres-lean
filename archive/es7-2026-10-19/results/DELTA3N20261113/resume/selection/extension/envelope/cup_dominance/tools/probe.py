"""Fixed-coordinate membership CNFs for the orientation-only cup criterion."""
import argparse
from collections import Counter
from itertools import combinations as C
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

HERE=Path(__file__).resolve().parents[1];E=HERE.parent
sys.path.insert(0,str(E/'tools'))
from exact import determinant,line
from search import dump,atomic,sha,release_cache
from verify import maxima,replay


def protection(p,g):
    ambient={}
    for cap in g['caps4']:ambient.setdefault(tuple(cap[-2:]),cap)
    rows={}
    for b,c in sorted({tuple(t[-2:]) for t in g['caps3']}):
        for (u,v),cap in ambient.items():
            union=sorted({b,c,u,v})
            if (u,v)==(b,c) or (u>=b and v>=c and all(determinant(p,*t)>0 for t in C(union,3))):
                q,ell=line(p,(b,c)),line(p,(u,v))
                assert ell[0]*q[2]>=q[0]*ell[2] and ell[1]*q[2]>=q[1]*ell[2]
                rows[b,c]={'pair':[b,c],'protected':True,'ambient_fourcap':cap,'ambient_pair':[u,v],'cup_union':union,'same_pair':(u,v)==(b,c)}
                break
        else:rows[b,c]={'pair':[b,c],'protected':False}
    return rows


def probe(r,path,binary,geometry_source=None):
    path.mkdir();start=time.monotonic();dump(path/'input.json',r);p=r['P'];m=len(p);n=r['n']
    (path/'points.txt').write_text(f'{m} {n}\n'+''.join(f'{x} {y}\n' for x,y in p))
    result={'name':r['name'],'n':n,'m':m,'label':'COMPUTED'}
    def finish(**extra):
        result.update(extra);result['seconds']=time.monotonic()-start
        result['files']={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in path.iterdir() if p.is_file()}
        dump(path/'result.json',result);release_cache(path);return result
    try:
        assert all(p[i][0]<p[i+1][0] for i in range(m-1)) and all(determinant(p,*t)!=0 for t in C(range(m),3))
        premise=maxima(p,range(m));assert premise['maxcap']<5 and premise['maxgon']<n
        result['premises']=premise
        if geometry_source:
            shutil.copy2(geometry_source,path/'geometry.json');result['geometry_source']=str(geometry_source);result['geometry_source_sha256']=sha(geometry_source)
        else:
            with (path/'geometry.json').open('x') as out,(path/'geometry.stderr').open('x') as err:
                proc=subprocess.run([str(binary),str(path/'points.txt')],stdout=out,stderr=err,timeout=10)
            assert proc.returncode==0
        g=json.loads((path/'geometry.json').read_text());assert g['m']==m and g['n']==n and g['valid']
        supports=protection(p,g);dump(path/'protection.json',list(supports.values()))
        bad=[t for t in g['caps3'] if not supports[tuple(t[-2:])]['protected']]
        targets,caps=g['targets'],g['caps4'];clauses=len(targets)+len(caps)+len(bad)
        literals=sum(map(len,targets))+4*len(caps)+3*len(bad)
        result.update(targets=len(targets),fourcaps=len(caps),bad_triples=len(bad),protected_pairs=sum(r['protected'] for r in supports.values()),cup_protected_nonterminal_pairs=sum(r['protected'] and not r['same_pair'] for r in supports.values()),clauses=clauses,literals=literals)
        cnf=path/'cup.cnf'
        with cnf.open('x') as f:
            f.write('c cup-protected membership: targets, fourcaps, unprotected cap triples\n');f.write(f'p cnf {m} {clauses}\n')
            for family,sign in ((targets,1),(caps,-1),(bad,-1)):
                for row in family:f.write(' '.join(str(sign*(i+1)) for i in row)+' 0\n')
        if literals>2000000:return finish(outcome='UNKNOWN_SOLVER_MEMORY_ESTIMATE')
        with (path/'finder.log').open('x') as out:
            try:proc=subprocess.run(['/usr/bin/cadical','-q',str(cnf)],stdout=out,stderr=subprocess.STDOUT,timeout=5)
            except subprocess.TimeoutExpired:return finish(outcome='UNKNOWN_TIMEOUT')
        result['solver_exit']=proc.returncode
        if proc.returncode==20:return finish(outcome='UNSAT_UNCERTIFIED_FROZEN')
        if proc.returncode!=10:return finish(outcome='UNKNOWN_SOLVER_EXIT')
        lits=[int(v) for row in (path/'finder.log').read_text().splitlines() if row.startswith('v ') for v in row[2:].split() if v!='0']
        assert len(lits)==m and {abs(v) for v in lits}==set(range(1,m+1));positive={v for v in lits if v>0};A=sorted(v-1 for v in positive)
        with cnf.open() as f:
            for row in f:
                if row.startswith(('c','p')):continue
                c=list(map(int,row.split()));assert c[-1]==0 and any((v>0)==(abs(v) in positive) for v in c[:-1])
        cert=[];aset=set(A)
        for t in g['caps3']:
            if set(t)<=aset:
                s=supports[tuple(t[-2:])];assert s['protected'];cap=s['ambient_fourcap']
                assert all(determinant(p,*z)<0 for z in C(cap,3))
                cert.append({'triple':t,'supports':[{'fourcap':cap,'weight':'1'}]})
        dump(path/'model.json',{'A':A,'literals':lits});dump(path/'certificates.json',cert)
        checked=replay(p,n,A,cert);dump(path/'positive_replay.json',checked)
        return finish(outcome='SAT_EXACT_MODEL_CHECKED',A=A,replay=checked)
    except Exception as exc:
        (path/'failure.txt').write_text(traceback.format_exc());return finish(outcome='CHECK_OR_DRIVER_FAILURE',exception=str(exc))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--binary',type=Path,required=True);ap.add_argument('--known',type=Path,required=True);ap.add_argument('--full-run',type=Path);ap.add_argument('--controls',action='store_true');ap.add_argument('--seconds',type=int,default=500)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False);(args.out/'cases').mkdir();(args.out/'source').mkdir();start=time.monotonic()
    for p in Path(__file__).parent.iterdir():
        if p.is_file():shutil.copy2(p,args.out/'source'/p.name)
    for name in ('exact.py','search.py','verify.py'):shutil.copy2(E/'tools'/name,args.out/'source'/name)
    dump(args.out/'plan.json',{'args':{k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},'source_hashes':{p.name:sha(p) for p in (args.out/'source').iterdir()}})
    cases=[]
    if args.controls:
        for n in (6,7,8):
            source=E.parents[1]/'boundary'/'data'/f'n{n}-boundary.json';r=json.loads(source.read_text())
            cases.append(({'name':f'control-boundary-n{n}','P':r['P'][:-1],'n':n,'source':str(source),'source_sha256':sha(source)},None))
        cases.append(({'name':'control-proper-cup','P':[[0,0],[1,0],[2,-1],[3,-14],[4,-4],[5,2],[6,5]],'n':6,'control_A':[0,1,2]},None))
    original=json.loads(args.known.read_text());cases.append(({'name':'known18','P':original['P'],'n':7,'source':str(args.known),'source_sha256':sha(args.known)},None))
    if args.full_run:
        for r in json.loads((args.full_run/'inputs.json').read_text()):
            cases.append((r,args.full_run/'cases'/r['name']/'geometry.json'))
    results=[];stop='COMPLETE'
    for r,gsource in cases:
        if time.monotonic()-start>=args.seconds:stop='DEADLINE';break
        atomic(args.out/'status.json',{'current':r['name'],'completed':len(results),'stop':'RUNNING'})
        result=probe(r,args.out/'cases'/r['name'],args.binary,gsource);results.append(result)
        print(json.dumps({k:result[k] for k in ('name','outcome','seconds')}),flush=True)
        if r['name'].startswith('control-'):
            assert result['outcome']=='SAT_EXACT_MODEL_CHECKED'
            if r['name']=='control-proper-cup':
                supports=json.loads((args.out/'cases'/r['name']/'protection.json').read_text())
                support=next(z for z in supports if z['pair']==[1,2]);assert support['protected'] and not support['same_pair']
                dump(args.out/'proper_cup_control.json',support)
        if result['outcome']=='UNSAT_UNCERTIFIED_FROZEN':
            stop='NEGATIVE_FROZEN';dump(args.out/'FROZEN_NEGATIVE.json',result);break
        if result['outcome']=='CHECK_OR_DRIVER_FAILURE':stop='CHECK_OR_DRIVER_FAILURE';break
    summary={'label':'COMPUTED','stop':stop,'cases':results,'outcomes':dict(Counter(r['outcome'] for r in results)),'planned_cases':len(cases),'completed_cases':len(results),'seconds':time.monotonic()-start,'scope':'Cup-protected selector only; a negative is not a uniform-envelope or ordinary weak Delta failure.'}
    dump(args.out/'summary.json',summary);atomic(args.out/'status.json',{k:v for k,v in summary.items() if k!='cases'});release_cache(args.out/'summary.json')
if __name__=='__main__':main()
