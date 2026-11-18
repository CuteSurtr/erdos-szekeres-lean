#!/usr/bin/env python3
"""Exact sparse nullspace reconstruction of a retained numerical hint.

This is a finder step. verify_product.py independently checks any result.
No execution is authorized while the parent's resource hold remains active.
"""
import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def normalize(row):
    row={k:v for k,v in row.items() if v}
    if not row:return row
    g=math.gcd(*row.values())
    if row[min(row)]<0:g=-g
    return {k:v//g for k,v in row.items()}


def nullvector(equations,hint,deadline):
    n=len(hint);pivots=[];ranks=[]
    todo=[normalize(r) for r in equations if r]
    while todo:
        if time.monotonic()>deadline:raise TimeoutError('exact-elimination deadline')
        # Sparse integer elimination; every row operation preserves the kernel.
        occurrence={}
        for row in todo:
            for k in row:occurrence[k]=occurrence.get(k,0)+1
        best=min(range(len(todo)),key=lambda i:(len(todo[i]),max(abs(v).bit_length() for v in todo[i].values())))
        pivotrow=todo.pop(best)
        p=min(pivotrow,key=lambda k:(occurrence[k],abs(pivotrow[k]).bit_length(),k))
        a=pivotrow[p];pivots.append((p,pivotrow))
        reduced=[];seen=set()
        for row in todo:
            if p in row:
                b=row[p];new={k:a*v for k,v in row.items()}
                for k,v in pivotrow.items():new[k]=new.get(k,0)-b*v
                row=normalize(new)
            if row:
                key=tuple(sorted(row.items()))
                if key not in seen:seen.add(key);reduced.append(row)
        todo=reduced
        if len(pivots)%25==0:
            ranks.append({'rank':len(pivots),'remaining_rows':len(todo),
                          'largest_integer_bits':max((abs(v).bit_length() for r in todo for v in r.values()),default=0)})
    used={p for p,row in pivots};free=[k for k in range(n) if k not in used]
    if not free:return None,{'rank':len(pivots),'nullity':0,'progress':ranks}
    values={k:Fraction(hint[k]).limit_denominator(10**8) for k in free}
    if len(free)==1:values[free[0]]=Fraction(1)
    for p,row in reversed(pivots):
        values[p]=-sum((Fraction(v)*values[k] for k,v in row.items() if k!=p),Fraction(0))/row[p]
    vector=[values[k] for k in range(n)]
    if all(v<=0 for v in vector):vector=[-v for v in vector]
    if any(v<0 for v in vector) or not any(vector):
        return None,{'rank':len(pivots),'nullity':len(free),'progress':ranks,'nonnegative':False}
    scale=math.lcm(*(v.denominator for v in vector));weights=[int(v*scale) for v in vector]
    g=math.gcd(*weights);weights=[v//g for v in weights]
    assert all(sum(c*weights[k] for k,c in r.items())==0 for r in equations)
    return weights,{'rank':len(pivots),'nullity':len(free),'progress':ranks,'nonnegative':True,
                    'largest_weight_bits':max(v.bit_length() for v in weights)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--hint-run',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seconds',type=float,default=14)
    args=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(600<<20,600<<20))
    args.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    (args.out/'source.py').write_bytes(Path(__file__).read_bytes())
    signs_path=args.hint_run/'orientation.signs';signs=signs_path.read_text().strip()
    (args.out/'orientation.signs').write_bytes(signs_path.read_bytes())
    # Reconstruct row indexing using the exact retained finder source, not a
    # mutable file from a different run. This step is not the independent checker.
    spec=importlib.util.spec_from_file_location('retained_product_finder',args.hint_run/'source.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    triples,rows,identity_count=module.build(signs)
    hints=json.loads((args.hint_run/'numeric_hint.json').read_text())['support']
    equations=[{} for i in range(560)]
    for j,(idx,approx) in enumerate(hints):
        for k,v in rows[idx]['coefficients']:equations[k][j]=v
    weights=None;error=None;info={}
    try:weights,info=nullvector(equations,[v for i,v in hints],start+args.seconds)
    except TimeoutError as e:error=str(e)
    if weights:
        selected=[dict(rows[idx],weight=w) for (idx,_),w in zip(hints,weights) if w]
        balance=[0]*560
        for row in selected:
            for j,v in row['coefficients']:balance[j]+=row['weight']*v
        assert selected and all(v==0 for v in balance)
        certificate={'label':'EXACT INTEGER PRODUCT CONTRADICTION; independent replay pending',
                     'signs_sha256':sha(signs_path),'source_sha256':sha(__file__),
                     'hint_source_sha256':sha(args.hint_run/'source.py'),
                     'hint_sha256':sha(args.hint_run/'numeric_hint.json'),
                     'rows':selected,'row_count':len(selected),'weight_sum':sum(r['weight'] for r in selected),
                     'exponent_sum':balance,'meaning':'Strict bracket-product inequalities multiply to X > X.'}
        (args.out/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
        print('EXACT_INTEGER_PRODUCT_CONTRADICTION_FOUND',flush=True)
    done={'status':'EXACT_PRODUCT_CERTIFICATE' if weights else 'NO_VERIFIED_OBSTRUCTION',
          'seconds':time.monotonic()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'elimination':info,'error':error,'scope':'Independent exact certificate replay is required.'}
    (args.out/'DONE.json').write_text(json.dumps(done,indent=2)+'\n');print(json.dumps(done),flush=True)


if __name__=='__main__':main()
