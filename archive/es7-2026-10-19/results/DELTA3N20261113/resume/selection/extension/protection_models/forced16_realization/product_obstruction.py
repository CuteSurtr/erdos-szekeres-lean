#!/usr/bin/env python3
"""Look for a biquadratic product contradiction. LP output is only a hint.

For each Grassmann--Pluecker identity with one common label, the unique
term of one sign has absolute value equal to the sum of the other two.
It is strictly larger than either. A positive combination of the resulting
log-product inequalities with zero exponent vector is an explicit
algebraic contradiction, accepted only after integer reconstruction.
"""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
import argparse
from datetime import datetime,timezone
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import resource
import time


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build(signs):
    triples=list(combinations(range(16),3));lookup={t:i for i,t in enumerate(triples)}
    def oriented(t):
        inv=sum(t[i]>t[j] for i in range(3) for j in range(i+1,3))
        ix=lookup[tuple(sorted(t))]
        return ix,(1 if signs[ix]=='+' else -1)*(-1 if inv%2 else 1)
    rows=[];seen=set();identities=0
    for a in range(16):
        for b,c,d,e in combinations([v for v in range(16) if v!=a],4):
            pairs=[((a,b,c),(a,d,e)),((a,b,d),(a,c,e)),((a,b,e),(a,c,d))]
            terms=[];sg=[]
            for term,(u,v) in enumerate(pairs):
                iu,su=oriented(u);iv,sv=oriented(v)
                terms.append((iu,iv));sg.append(su*sv*(-1 if term==1 else 1))
            assert len(set(sg))==2,('GP sign failure',a,b,c,d,e,sg)
            large=next(i for i,s in enumerate(sg) if sg.count(s)==1)
            identities+=1
            for small in range(3):
                if small==large:continue
                coefficients={}
                for v in terms[large]:coefficients[v]=coefficients.get(v,0)+1
                for v in terms[small]:coefficients[v]=coefficients.get(v,0)-1
                key=tuple(sorted((v,c) for v,c in coefficients.items() if c))
                if key in seen:continue
                seen.add(key)
                rows.append({'root':a,'other':[b,c,d,e],'large':large,'small':small,
                             'positive_brackets':list(terms[large]),'negative_brackets':list(terms[small]),
                             'coefficients':key})
    return triples,rows,identities


def control():
    P=[(i,i*i) for i in range(16)]
    triples,rows,identities=build('+'*560)
    ds=[(P[j][0]-P[i][0])*(P[k][1]-P[i][1])-(P[j][1]-P[i][1])*(P[k][0]-P[i][0]) for i,j,k in triples]
    for row in rows:
        a,b=row['positive_brackets'];c,d=row['negative_brackets']
        assert abs(ds[a]*ds[b])>abs(ds[c]*ds[d])
    return {'point_set':'16-point parabola','GP_identities':identities,'exact_product_inequalities':len(rows),'PASS':True}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--signs',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seconds',type=float,default=120)
    ap.add_argument('--seed',type=int,default=20261114);args=ap.parse_args()
    resource.setrlimit(resource.RLIMIT_AS,(600<<20,600<<20))
    args.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    (args.out/'source.py').write_bytes(Path(__file__).read_bytes())
    signs=args.signs.read_text().strip();assert len(signs)==560 and set(signs)<={'+','-'}
    (args.out/'orientation.signs').write_bytes(args.signs.read_bytes())
    (args.out/'controls.json').write_text(json.dumps(control(),indent=2)+'\n')
    import numpy as np
    from scipy.sparse import coo_matrix,vstack
    from scipy.optimize import linprog
    triples,rows,identities=build(signs)
    ii=[];jj=[];vv=[]
    for r,row in enumerate(rows):
        for c,v in row['coefficients']:ii.append(c);jj.append(r);vv.append(v)
    mat=coo_matrix((vv,(ii,jj)),shape=(560,len(rows))).tocsr()
    eq=vstack([mat,np.ones((1,len(rows)))],format='csc');rhs=np.r_[np.zeros(560),1.]
    rng=np.random.default_rng(args.seed)
    # Distinct costs encourage a sparse basic certificate, rather than a dense average.
    costs=rng.uniform(1.,2.,len(rows))
    metadata={'started_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':sha(__file__),
              'signs_sha256':sha(args.signs),'GP_identities':identities,'unique_strict_product_rows':len(rows),
              'seed':args.seed,'time_limit':args.seconds,'evidence':'LP status alone is not evidence'}
    (args.out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    answer=linprog(costs,A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs-ds',
                   options={'threads':1,'parallel':False,'time_limit':args.seconds})
    hints={'status':int(answer.status),'message':str(answer.message),'iterations':int(answer.nit),'certificate':False}
    cert=None
    if answer.x is not None:
        support=[(int(i),float(answer.x[i])) for i in np.flatnonzero(answer.x>1e-10)]
        (args.out/'numeric_hint.json').write_text(json.dumps({'support':support},indent=2)+'\n')
        hints['support_size']=len(support)
        for denominator in (100,1000,10000,100000,1000000,10000000):
            fractions=[Fraction(v).limit_denominator(denominator) for i,v in support]
            scale=math.lcm(*(v.denominator for v in fractions))
            weights=[int(v*scale) for v in fractions]
            common=math.gcd(*weights);weights=[v//max(1,common) for v in weights]
            total=[0]*560
            for (idx,_),w in zip(support,weights):
                for j,v in rows[idx]['coefficients']:total[j]+=w*v
            if weights and min(weights)>0 and all(v==0 for v in total):
                cert={'label':'EXACT INTEGER PRODUCT CONTRADICTION; independent replay pending',
                      'signs_sha256':sha(args.signs),'source_sha256':sha(__file__),
                      'rows':[dict(rows[i],weight=w) for (i,_),w in zip(support,weights)],
                      'row_count':len(support),'weight_sum':sum(weights),'exponent_sum':total,
                      'meaning':'Multiplying strict product inequalities to positive integer powers gives X > X.'}
                break
    if cert:
        (args.out/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
        print('EXACT_INTEGER_PRODUCT_CONTRADICTION_FOUND',flush=True);hints['certificate']=True
    done={'status':'EXACT_PRODUCT_CERTIFICATE' if cert else 'NO_VERIFIED_OBSTRUCTION',
          'seconds':time.monotonic()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'numerical_hint':hints,'scope':'No failed numeric run implies realizability or nonrealizability.'}
    (args.out/'DONE.json').write_text(json.dumps(done,indent=2)+'\n');print(json.dumps(done),flush=True)


if __name__=='__main__':main()
