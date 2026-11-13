#!/usr/bin/env python3
"""Rational relaxation of fivefold linear bracket identities.

Let D_ij=dot(z_i,z_j), E_ij=det(z_i,z_j)/sin(72deg). Then
4*det(z_i,R^k z_j)/sin(72deg) has coefficients in Z[sqrt(5)].
Cancel the rational and sqrt(5) coefficient blocks separately. This is a
weaker rational relaxation, but every positive exact dependency is sound.
Numerical LP only selects support; rational elimination certifies weights.
"""
import argparse, hashlib, importlib.util, itertools, json, time, warnings
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
DCO=((0,0),(4,0),(-2,2),(2,-2),(-4,0))
ECO=((4,0),(-1,1),(-1,-1),(-1,-1),(-1,1))
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def form(triple,index):
    row=defaultdict(int)
    for a,b in zip(triple,triple[1:]+triple[:1]):
        i,ka=divmod(a,5);j,kb=divmod(b,5);k=(kb-ka)%5
        for part,c in enumerate(DCO[k]): row[index[('D',min(i,j),max(i,j),part)]]+=c
        if i!=j:
            for part,c in enumerate(ECO[k]): row[index[('E',min(i,j),max(i,j),part)]]+=c*(1 if i<j else -1)
    return {j:c for j,c in row.items() if c}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model',required=True,type=Path);ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--t',type=int,default=12);ap.add_argument('--layers',required=True);ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--seed',type=int,default=0)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    raw=a.model.read_bytes();pos=set(json.loads(raw));G=load('source_encoder',HERE.parent/'C7UPPER/gen.py');E=G.Enc(5,8,a.t)
    exact=load('rational_recovery',HERE/'math_linear.py').exact_weights
    variables=[(kind,i,j,part) for kind in ('D','E') for i in range(a.t) for j in range(i+(kind=='E'),a.t) for part in (0,1)]
    index={x:j for j,x in enumerate(variables)};layers=set(map(int,a.layers.split(','))) if a.layers!='all' else set(range(a.t))
    reps=[(q,v) for q,v in E.tvar.items() if {x//5 for x in q}<=layers]
    rows=[{j:c*(1 if v in pos else -1) for j,c in form(q,index).items()} for q,v in reps]
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix,vstack
    rr=[];cc=[];dd=[]
    for k,row in enumerate(rows):
        for j,c in row.items():rr.append(j);cc.append(k);dd.append(c)
    A=coo_matrix((dd,(rr,cc)),shape=(len(variables),len(rows))).tocsr()
    eq=vstack((A,coo_matrix(np.ones((1,len(rows)))))).tocsr();rhs=np.r_[np.zeros(len(variables)),1.0]
    objective=np.random.default_rng(a.seed).uniform(.5,1.5,len(rows))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore');sol=linprog(objective,A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs',options={'time_limit':a.seconds,'threads':1})
    result={'rigor':'numerical search only until an exact dependency is verified','model_sha256':hashlib.sha256(raw).hexdigest(),'layers':sorted(layers),'lp_status':int(sol.status),'rows':len(rows),'columns':len(variables)}
    if sol.success:
        support=np.flatnonzero(sol.x>1e-9).tolist();weights=exact([rows[k] for k in support],[sol.x[k] for k in support],len(variables))
        records=[]
        for k,weight in zip(support,weights):
            q,v=reps[k];records.append({'triple':q,'variable':v,'required_sign':1 if v in pos else -1,'weight':weight,'signed_coefficients':[[variables[j],c] for j,c in sorted(rows[k].items())]})
        cut=sorted([-r['variable']*r['required_sign'] for r in records],key=abs)
        w={'m':5,'t':a.t,'scope':'realizations carrying the specified geometric fivefold rotation','method':'positive exact linear dependency cancelling both rational and sqrt5 coefficient blocks','model_sha256':result['model_sha256'],'records':records,'source_layers':sorted({x//5 for r in records for x in r['triple']}),'candidate_clause':cut,'exact_residual_zero':True}
        data=(json.dumps(w,indent=2)+'\n').encode();(a.out/'linear_witness.json').write_bytes(data)
        result.update({'rigor':'exact coefficient-block cancellation; independent symbolic and real-set checks required','support':len(records),'candidate_clause':cut,'witness_sha256':hashlib.sha256(data).hexdigest(),'maximum_weight':max(weights)})
    result['elapsed_seconds']=round(time.monotonic()-start,3)
    (a.out/'linear_search.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
