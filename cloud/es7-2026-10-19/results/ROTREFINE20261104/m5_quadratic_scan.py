#!/usr/bin/env python3
"""Bounded fivefold linear separation over the actual quadratic coefficient field."""
import argparse,hashlib,importlib.util,itertools,json,math,time,warnings
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    p=argparse.ArgumentParser();p.add_argument('--model',required=True,type=Path);p.add_argument('--out',required=True,type=Path);p.add_argument('--t',type=int,default=12)
    p.add_argument('--max-layers',type=int,default=4);p.add_argument('--seconds',type=float,default=90);p.add_argument('--full',action='store_true');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    raw=a.model.read_bytes();pos=set(json.loads(raw));mh=hashlib.sha256(raw).hexdigest();G=load('encoder',HERE.parent/'C7UPPER/gen.py');E=G.Enc(5,8,a.t)
    L=load('rational_parts',HERE/'m5_linear_lift.py');Q=load('quadratic_exact',HERE/'quadratic_recovery.py')
    parts=[(kind,i,j,k) for kind in ('D','E') for i in range(a.t) for j in range(i+(kind=='E'),a.t) for k in (0,1)];ix={x:j for j,x in enumerate(parts)}
    allreps=[]
    for q,v in E.tvar.items():
        blocks=L.form(q,ix);row={}
        for j in {j//2 for j in blocks}:
            pair=(F(blocks.get(2*j,0)),F(blocks.get(2*j+1,0)))
            if v not in pos:pair=Q.neg(pair)
            if pair!=Q.Z:row[j]=pair
        allreps.append((q,v,frozenset(x//5 for x in q),row))
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix,vstack
    choices=[tuple(range(a.t))] if a.full else itertools.chain.from_iterable(itertools.combinations(range(a.t),k) for k in range(2,a.max_layers+1))
    found=False;count=0;failed=0
    with (a.out/'scan.jsonl').open('w',buffering=1) as log:
        for layers in choices:
            if time.monotonic()-start>a.seconds:break
            subset=set(layers);reps=[(q,v,row) for q,v,s,row in allreps if s<=subset]
            used=sorted({j for q,v,row in reps for j in row});ci={j:i for i,j in enumerate(used)};rr=[];cc=[];dd=[]
            for k,(q,v,row) in enumerate(reps):
                for j,(x,y) in row.items():rr.append(ci[j]);cc.append(k);dd.append(float(x)+math.sqrt(5)*float(y))
            A=coo_matrix((dd,(rr,cc)),shape=(len(used),len(reps))).tocsr();eq=vstack((A,coo_matrix(np.ones((1,len(reps)))))).tocsr()
            with warnings.catch_warnings():
                warnings.simplefilter('ignore');sol=linprog(np.arange(len(reps))/max(1,len(reps))+1,A_eq=eq,b_eq=np.r_[np.zeros(len(used)),1.0],bounds=(0,None),method='highs',options={'time_limit':min(15,a.seconds),'threads':1})
            count+=1;rec={'layers':layers,'status':int(sol.status),'rows':len(reps),'lift_variables':len(used)}
            if sol.success:
                support=np.flatnonzero(sol.x>1e-8).tolist()
                try:weights=Q.recover([{ci[j]:c for j,c in reps[k][2].items()} for k in support],[sol.x[k] for k in support],len(used))
                except (ValueError,TimeoutError,ZeroDivisionError) as ex:
                    failed+=1;rec['unaccepted_numeric_support']=str(ex);log.write(json.dumps(rec)+'\n');continue
                records=[]
                for k,weight in zip(support,weights):
                    q,v,row=reps[k];records.append({'triple':q,'variable':v,'required_sign':1 if v in pos else -1,'weight':weight,'signed_coefficients':[[parts[2*j][:3],[str(x),str(y)]] for j,(x,y) in sorted(row.items())]})
                clause=sorted([-r['variable']*r['required_sign'] for r in records],key=abs)
                w={'m':5,'t':a.t,'model_sha256':mh,'scope':'realizations carrying the specified geometric fivefold rotation','method':'positive exact Q(sqrt5) dependency of orientation forms','records':records,'source_layers':layers,'candidate_clause':clause,'exact_residual_zero':True}
                data=(json.dumps(w,indent=2)+'\n').encode();(a.out/'linear_witness.json').write_bytes(data)
                rec.update({'support':len(records),'witness_sha256':hashlib.sha256(data).hexdigest(),'candidate_clause':clause});found=True
            log.write(json.dumps(rec)+'\n')
            if found:break
    summary={'model_sha256':mh,'restrictions_checked':count,'exact_dependency_found':found,'rejected_numeric_supports':failed,'elapsed_seconds':round(time.monotonic()-start,3),'caution':'negative or numeric-only outcomes do not prove realizability'}
    (a.out/'scan_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
if __name__=='__main__':main()
