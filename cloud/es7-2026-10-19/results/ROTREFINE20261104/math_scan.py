#!/usr/bin/env python3
"""Scan two-/three-orbit restrictions for short exact linear dependencies."""
import argparse
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import resource
import time
import warnings


def load(name,path):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model',required=True,type=Path);ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--sizes',default='2,3');ap.add_argument('--limit',type=int,default=1);ap.add_argument('--seconds',type=float,default=120);ap.add_argument('--seed',type=int,default=0)
    args=ap.parse_args();start=time.monotonic();args.out.mkdir(parents=True,exist_ok=True)
    M=load('linear',Path(__file__).with_name('math_linear.py'));G=load('encoder',M.ROOT/'C7UPPER/gen.py');E=G.Enc(6,8,10)
    raw=args.model.read_bytes();modelhash=hashlib.sha256(raw).hexdigest();pos=set(json.loads(raw))
    vs=M.variables(10);ix={v:j for j,v in enumerate(vs)}
    allrows=[(q,v,{x//6 for x in q},{j:c*(1 if v in pos else -1) for j,c in M.form(q,ix).items()}) for q,v in E.tvar.items()]
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix,vstack
    import numpy as np
    rng=np.random.default_rng(args.seed);found=[];tried=0
    with (args.out/'scan.jsonl').open('w') as log:
        for count in map(int,args.sizes.split(',')):
            for ls in it.combinations(range(10),count):
                if time.monotonic()-start>args.seconds:break
                rows=[(q,v,row) for q,v,lay,row in allrows if lay<=set(ls)]
                rr=[];cc=[];dd=[]
                for k,(q,v,row) in enumerate(rows):
                    for j,c in row.items():rr.append(j);cc.append(k);dd.append(c)
                A=coo_matrix((dd,(rr,cc)),shape=(len(vs),len(rows))).tocsr()
                eq=vstack((A,coo_matrix(np.ones((1,len(rows)))))).tocsr();rhs=np.r_[np.zeros(len(vs)),1.0]
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    sol=linprog(rng.uniform(0.5,1.5,len(rows)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs',
                                options={'time_limit':min(5,args.seconds-(time.monotonic()-start)),'threads':1,'presolve':True})
                tried+=1;entry={'layers':ls,'lp_status':int(sol.status),'seconds':round(time.monotonic()-start,3)}
                if sol.success:
                    support=np.flatnonzero(sol.x>1e-9).tolist()
                    weights=M.exact_weights([rows[k][2] for k in support],[sol.x[k] for k in support],len(vs))
                    records=[]
                    for k,weight in zip(support,weights):
                        q,v,row=rows[k]
                        records.append({'triple':q,'variable':v,'required_sign':1 if v in pos else -1,'weight':weight,
                                        'signed_coefficients':[[vs[j],c] for j,c in sorted(row.items())]})
                    cut=sorted([-r['variable']*r['required_sign'] for r in records],key=abs)
                    w={'m':6,'t':10,'scope':'realizations with the specified Euclidean sixfold rotation','model_sha256':modelhash,
                       'method':'positive exact linear dependency of rotation-specific determinant forms','lift_variables':vs,
                       'records':records,'candidate_clause':cut,'exact_residual_zero':True,
                       'source_layers':sorted({x//6 for r in records for x in r['triple']})}
                    dest=args.out/('layers_'+'_'.join(map(str,ls)));dest.mkdir(exist_ok=True)
                    data=(json.dumps(w,indent=2)+'\n').encode();(dest/'linear_witness.json').write_bytes(data)
                    entry.update({'exact_dependency':True,'support':len(records),'maximum_weight':max(weights),
                                  'candidate_clause':cut,'witness_sha256':hashlib.sha256(data).hexdigest(),'directory':dest.name})
                    found.append(entry)
                log.write(json.dumps(entry)+'\n');log.flush()
                if sol.success:print(json.dumps(entry),flush=True)
                if len(found)>=args.limit:break
            if len(found)>=args.limit or time.monotonic()-start>args.seconds:break
    result={'model_sha256':modelhash,'restrictions_tried':tried,'witnesses':found,'elapsed_seconds':round(time.monotonic()-start,3),
            'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (args.out/'scan_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':main()
