#!/usr/bin/env python3
"""Independent linear-cut check using integer cyclotomic complex polynomials.

Expand conj(q-p)*(r-p) - (q-p)*conj(r-p), equal to 2i times the
Euclidean bracket. This uses Z[zeta_5], not the LP's Q(sqrt5) coefficient
table or its seed determinant expansion. sqrt5 = 1+2*zeta+2*zeta^4.
"""
import argparse,importlib.util,itertools,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
    p=argparse.ArgumentParser();p.add_argument('--witness',type=Path,required=True)
    p.add_argument('--model',type=Path,required=True);p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    h=load(ROOT/'C6C7REVIEW/m5_pilot.py','integer_cyclotomic');v=load(HERE/'m5_algebra.py','family_tests')
    w=json.loads(a.witness.read_text());positive=set(json.loads(a.model.read_text()))
    assert w['m']==5 and w['model_sha256']==v.sha(a.model)
    zero=h.ZERO;one=h.ONE;zeta=h.ZETA
    def plus(x,y):return h.norm([a+b for a,b in zip(x,y)])
    def minus(x,y):return h.norm([a-b for a,b in zip(x,y)])
    def neg(x):return tuple(-a for a in x)
    def field(pair):
        aa,bb=pair;assert type(aa) is int and type(bb) is int
        return h.norm((aa+bb,2*bb,0,0,2*bb))
    def padd(x,y,scale=one):
        out=dict(x)
        for m,c in y.items():out[m]=plus(out.get(m,zero),h.mul(scale,c))
        return {m:c for m,c in out.items() if c!=zero}
    def pmul(x,y):
        out={}
        for i,c in x.items():
            for j,d in y.items():
                key=tuple(sorted(i+j));out[key]=plus(out.get(key,zero),h.mul(c,d))
        return {m:c for m,c in out.items() if c!=zero}
    def pc(x):return {m:h.conj(c) for m,c in x.items()}
    powers=[one]
    for _ in range(5):powers.append(h.mul(powers[-1],zeta))
    assert powers[5]==one
    def point(x):
        orbit,k=divmod(x,5)
        return {(2*orbit,):powers[k],(2*orbit+1,):powers[(k+1)%5]}
    def bracket(q):
        p0,p1,p2=map(point,q);u=padd(p1,p0,neg(one));z=padd(p2,p0,neg(one))
        return padd(pmul(pc(u),z),pmul(u,pc(z)),neg(one))
    e=v.encoder(w['t']);residual={};pattern=[];clause=[];coefficients=[]
    for row in w['records']:
        q=tuple(row['triple']);sg=row['required_sign'];weight=tuple(row['weight'])
        assert sg in (-1,1) and h.sign5(*weight)>0
        c=field(weight);assert c==h.conj(c)
        lit=e.o(*q);assert lit>0 and lit==row['variable']
        assert sg==(1 if lit in positive else -1)
        signed=c if sg>0 else neg(c)
        residual=padd(residual,bracket(q),signed)
        pattern.append((q,sg));clause.append(-sg*lit);coefficients.append((q,signed))
    assert not residual and clause==w['candidate_clause']
    tests=v.template_test(pattern,a.archive)
    source=ROOT/'ES8SYM/sets3/c5_56pts_11layers_centre.pts'
    raw=[h.norm([int(x) for x in l.split()]) for l in source.read_text().splitlines() if l.strip() and not l.startswith('#')]
    P,_,_=h.normalized_layers(raw);layers=sorted({x//5 for q,sg in pattern for x in q})
    assert 1<=len(layers)<=4
    identities=0
    target_choices=(itertools.permutations(range(11),len(layers)) if len(layers)<=2 else
                    (((0,1,2),(4,5,6),(8,9,10)) if len(layers)==3 else
                     ((0,1,2,3),(3,4,5,6),(7,8,9,10))))
    for targets in target_choices:
        for shifts in itertools.product(range(5),repeat=len(layers)):
            for direction,mirror in itertools.product((-1,1),repeat=2):
                mp=dict(zip(layers,zip(targets,shifts)))
                def actual(x):
                    o,s=mp[x//5];z=P[5*o+(direction*(x%5)+s)%5]
                    return z if mirror>0 else h.conj(z)
                total=zero
                for q,c in coefficients:
                    aa,bb,cc=map(actual,q);u=h.sub(bb,aa);z=h.sub(cc,aa)
                    cross=minus(h.mul(h.conj(u),z),h.mul(u,h.conj(z)))
                    assert cross!=zero
                    total=plus(total,h.mul(c,cross))
                assert total==zero;identities+=1
    out={'kind':'rotation_linear_identity','m':5,'t':w['t'],'pattern':pattern,'candidate_clause':clause,
         'model_sha256':v.sha(a.model),'witness_sha256':v.sha(a.witness),'source_layers':layers,
         'independent_method':'Formal degree-two complex polynomials over integer Z[zeta_5]',
         'polynomial_residual':{},'positive_weights_verified':True,'exact56':tests,
         'exact56_weighted_identities':identities,
         'weighted_identity_scope':('all orbit injections and all shifts' if len(layers)<=2 else
                                    'three orbit selections, all shifts, both directions and mirrors'),
         'scope':w['scope']}
    v.save(a.output,out);print(json.dumps(out),flush=True)

if __name__=='__main__':main()
