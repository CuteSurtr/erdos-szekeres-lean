#!/usr/bin/env python3
"""Independent rotation-orbit and GP-sign verifier for product-cycle witnesses.
The GP identity is a determinant identity; every minority signed product is
strictly larger in magnitude than either other product. Positive weighted
comparisons whose orbit-bracket exponents cancel contradict general position.
"""
import argparse, hashlib, itertools, json
from collections import Counter
from pathlib import Path

def cs(q,m):
    choices=[]
    for s in range(m):
        r=[(x//m)*m+(x%m+s)%m for x in q]
        parity=(-1)**sum(r[i]>r[j] for i in range(3) for j in range(i+1,3))
        choices.append((tuple(sorted(r)),parity))
    key=min(q for q,p in choices)
    signs={p for q,p in choices if q==key}
    if len(signs)!=1: raise ValueError('odd triple stabilizer')
    return key,signs.pop()

def check(witness,model):
    w=json.loads(witness.read_text());raw=model.read_bytes();pos=set(json.loads(raw));m,t=w['m'],w['t']
    if hashlib.sha256(raw).hexdigest()!=w['model_sha256']: raise ValueError('model hash')
    orbits={}
    for q in itertools.combinations(range(m*t),3):
        c,_=cs(q,m)
        if c not in orbits: orbits[c]=len(orbits)+1
    used=set();exponents=Counter();details=[]
    def chi(q):
        c,s=cs(q,m);v=orbits[c];used.add(v)
        return s*(1 if v in pos else -1)
    for record in w['comparisons']:
        a,b,c,d,e=record['anchor_quintuple']
        if len({a,b,c,d,e})!=5: raise ValueError('repeated point')
        terms=[((a,b,c),(a,d,e),1),((a,b,d),(a,c,e),-1),((a,b,e),(a,c,d),1)]
        signs=[s*chi(q)*chi(r) for q,r,s in terms]
        mi,other=record['minority_term'],record['other_term'];weight=record['weight']
        if type(weight) is not int or weight<=0: raise ValueError('weight')
        if signs!=record['term_signs'] or signs.count(signs[mi])!=1 or signs[other]!=-signs[mi]: raise ValueError('minority sign')
        products=[sorted([cs(q,m)[0],cs(r,m)[0]]) for q,r,s in terms]
        if products[mi]!=sorted(map(tuple,record['greater_orbits'])) or products[other]!=sorted(map(tuple,record['lesser_orbits'])): raise ValueError('orbit product')
        for q in products[mi]: exponents[q]+=weight
        for q in products[other]: exponents[q]-=weight
        details.append({'quintuple':[a,b,c,d,e],'signs':signs,'greater':products[mi],'lesser':products[other],'weight':weight})
    if not details or any(exponents.values()): raise ValueError('exponents do not cancel')
    clause=[-v if v in pos else v for v in sorted(used)]
    return {'rigor':'exact computation plus the determinant-identity and rotation argument','m':m,'t':t,
        'model_sha256':hashlib.sha256(raw).hexdigest(),'witness_sha256':hashlib.sha256(witness.read_bytes()).hexdigest(),
        'canonical_orbits':len(orbits),'comparisons':details,'candidate_clause':clause,'verified':True,
        'scope':'realizations carrying the specified geometric rotation'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--witness',required=True,type=Path);p.add_argument('--model',required=True,type=Path)
    a=p.parse_args();print(json.dumps(check(a.witness,a.model),sort_keys=True))
