#!/usr/bin/env python3
"""Bounded small-orbit search in the rational fivefold linear relaxation."""
import argparse, hashlib, itertools, json, time, warnings
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def main():
    p=argparse.ArgumentParser();p.add_argument('--model',required=True,type=Path);p.add_argument('--out',required=True,type=Path);p.add_argument('--t',type=int,default=12)
    p.add_argument('--max-layers',type=int,default=4);p.add_argument('--seconds',type=float,default=60);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();raw=a.model.read_bytes();pos=set(json.loads(raw));mh=hashlib.sha256(raw).hexdigest()
    G=load('encoder',HERE.parent/'C7UPPER/gen.py');E=G.Enc(5,8,a.t);L=load('lift5',HERE/'m5_linear_lift.py');exact=load('recover',HERE/'math_linear.py').exact_weights
    variables=[(kind,i,j,part) for kind in ('D','E') for i in range(a.t) for j in range(i+(kind=='E'),a.t) for part in (0,1)]
    ix={x:j for j,x in enumerate(variables)}
    allreps=[(q,v,frozenset(x//5 for x in q),{j:c*(1 if v in pos else -1) for j,c in L.form(q,ix).items()}) for q,v in E.tvar.items()]
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix,vstack
    count=0;found=False
    with (a.out/'scan.jsonl').open('w',buffering=1) as log:
        for size in range(2,a.max_layers+1):
            for layers in itertools.combinations(range(a.t),size):
                if time.monotonic()-start>a.seconds: break
                reps=[(q,v,row) for q,v,s,row in allreps if s<=set(layers)]
                used=sorted({j for q,v,row in reps for j in row});ci={j:i for i,j in enumerate(used)}
                rr=[];cc=[];dd=[]
                for k,(q,v,row) in enumerate(reps):
                    for j,c in row.items():rr.append(ci[j]);cc.append(k);dd.append(c)
                A=coo_matrix((dd,(rr,cc)),shape=(len(used),len(reps))).tocsr();eq=vstack((A,coo_matrix(np.ones((1,len(reps)))))).tocsr()
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore');sol=linprog(np.arange(len(reps))/max(1,len(reps))+1,A_eq=eq,b_eq=np.r_[np.zeros(len(used)),1.0],bounds=(0,None),method='highs',options={'time_limit':2,'threads':1})
                count+=1;rec={'layers':layers,'status':int(sol.status),'rows':len(reps),'columns':len(used)}
                if sol.success:
                    support=np.flatnonzero(sol.x>1e-9).tolist()
                    weights=exact([{ci[j]:c for j,c in reps[k][2].items()} for k in support],[sol.x[k] for k in support],len(used))
                    records=[]
                    for k,wgt in zip(support,weights):
                        q,v,row=reps[k];records.append({'triple':q,'variable':v,'required_sign':1 if v in pos else -1,'weight':wgt,'signed_coefficients':[[variables[j],c] for j,c in sorted(row.items())]})
                    clause=sorted([-r['variable']*r['required_sign'] for r in records],key=abs)
                    w={'m':5,'t':a.t,'scope':'realizations carrying the specified geometric fivefold rotation','model_sha256':mh,'method':'positive exact dependency cancelling rational and sqrt5 coefficient blocks','records':records,'source_layers':layers,'candidate_clause':clause,'exact_residual_zero':True}
                    data=(json.dumps(w,indent=2)+'\n').encode();(a.out/'linear_witness.json').write_bytes(data)
                    rec.update({'support':len(records),'maximum_weight':max(weights),'witness_sha256':hashlib.sha256(data).hexdigest(),'candidate_clause':clause});found=True
                log.write(json.dumps(rec)+'\n')
                if found:break
            if found or time.monotonic()-start>a.seconds:break
    result={'model_sha256':mh,'restrictions_checked':count,'found_exact_block_dependency':found,'elapsed_seconds':round(time.monotonic()-start,3),'interpretation':'positive dependencies require independent symbolic and exact56 verification before use; negative searches do not establish realizability'}
    (a.out/'scan_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
