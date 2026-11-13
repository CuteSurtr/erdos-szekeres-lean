#!/usr/bin/env python3
"""Exact fivefold GP-cycle verification, certified-set tests, and cut lifting.

The verifier reconstructs literals through encoder A, independently of the
cycle search's canonicalization and table. Magnitude equalities require the
specified rotational realization, not only a sign-pattern automorphism.
"""
import argparse, collections, hashlib, importlib.util, itertools, json, sys
from array import array
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')

def terms(q):
    a,b,c,d,e=q
    return (((a,b,c),(a,d,e),1),((a,b,d),(a,c,e),-1),((a,b,e),(a,c,d),1))

def encoder(t):return load(ROOT/'C7UPPER/gen.py','encoder_for_verify').Enc(5,8,t)

def exact_table(archive):
    source=ROOT/'ES8SYM/sets3/c5_56pts_11layers_centre.pts'
    binary=archive/'m5_exact56.bin';meta=archive/'m5_exact56.json'
    if binary.exists() and meta.exists():
        d=json.loads(meta.read_text());assert d['source_sha256']==sha(source) and d['table_sha256']==sha(binary)
        table=array('b');table.frombytes(binary.read_bytes());return table,d
    h=load(ROOT/'C6C7REVIEW/m5_pilot.py','exact_fivefold')
    points=[h.norm([int(x) for x in line.split()]) for line in source.read_text().splitlines()
            if line.strip() and not line.startswith('#')]
    P,phase,halves=h.normalized_layers(points);assert len(P)==55
    tab=array('b',[0])*(55**3);count=0
    for a,b,c in itertools.combinations(range(55),3):
        sign=h.orient(P[a],P[b],P[c]);assert sign in (-1,1);count+=1
        for x,y,z in ((a,b,c),(b,c,a),(c,a,b)):tab[(x*55+y)*55+z]=sign
        for x,y,z in ((a,c,b),(c,b,a),(b,a,c)):tab[(x*55+y)*55+z]=-sign
    binary.write_bytes(tab.tobytes())
    d={'source_sha256':sha(source),'table_sha256':sha(binary),'nonzero_triples':count,
       'points_without_centre':55,'arithmetic':'integer Z[zeta_5] and A+B sqrt(5) sign comparison',
       'arithmetic_source_sha256':sha(ROOT/'C6C7REVIEW/m5_pilot.py')}
    save(meta,d);return tab,d

def template_test(pattern,archive):
    tab,meta=exact_table(archive)
    layers=sorted({x//5 for q,sg in pattern for x in q});k=len(layers)
    assert 1<=k<=4
    tested=0;matched=0
    for targets in itertools.permutations(range(11),k):
        for relative in itertools.product(range(5),repeat=k-1):
            shifts=(0,)+relative
            for direction,flip in itertools.product((-1,1),repeat=2):
                mp=dict(zip(layers,zip(targets,shifts)))
                def f(x):
                    o,s=mp[x//5];return 5*o+(direction*(x%5)+s)%5
                match=True
                for q,sg in pattern:
                    a,b,c=map(f,q)
                    if tab[(a*55+b)*55+c]!=sg*flip:
                        match=False;break
                matched+=match;tested+=1
    assert matched==0
    return {'all_orbit_injections':True,'relative_shifts_complete':True,'directions_and_sign_flips':True,
            'embeddings':tested,'forbidden_matches':matched,'source_layers':layers,**meta}

def verify(a):
    w=json.loads(a.witness.read_text());positive=set(json.loads(a.model.read_text()))
    assert w['model_sha256']==sha(a.model)
    t=w.get('t',a.layers);e=encoder(t);used={};expo=collections.Counter();products=[]
    def sign(q):
        l=e.o(*q);used[abs(l)]=abs(l) in positive
        return (1 if l>0 else -1)*(1 if abs(l) in positive else -1)
    def orb(q):return e.canon[tuple(sorted(q))][0]
    if 'comparisons' in w:
        kind='rotation_product_cycle'
        for row in w['comparisons']:
            tt=terms(tuple(row['anchor_quintuple']));ss=[co*sign(x)*sign(y) for x,y,co in tt]
            assert ss==row['term_signs'];i,j=row['minority_term'],row['other_term']
            assert i!=j and ss.count(ss[i])==1 and row['weight']==1
            plus=tuple(sorted((orb(tt[i][0]),orb(tt[i][1]))))
            minus=tuple(sorted((orb(tt[j][0]),orb(tt[j][1]))))
            assert plus==tuple(sorted(map(tuple,row['greater_orbits'])))
            assert minus==tuple(sorted(map(tuple,row['lesser_orbits'])))
            for q in plus:expo[q]+=1
            for q in minus:expo[q]-=1
            products.append((plus,minus))
        assert products and all(products[i][1]==products[(i+1)%len(products)][0] for i in range(len(products)))
        assert all(v==0 for v in expo.values())
    else:
        kind='gp_sign'
        tt=terms(tuple(w['anchor_quintuple']));ss=[co*sign(x)*sign(y) for x,y,co in tt]
        assert ss==w['term_signs'] and len(set(ss))==1
    clause=[-v if value else v for v,value in sorted(used.items())]
    assert all((l>0)!=(abs(l) in positive) for l in clause)
    pattern=[(q,1 if v in positive else -1) for q,v in e.tvar.items() if v in used]
    tests=template_test(pattern,a.archive)
    out={'kind':kind,'m':5,'t':t,'model_sha256':sha(a.model),'witness_sha256':sha(a.witness),
         'verified_by':'encoder A map and exact coefficient/exponent comparisons',
         'comparisons':len(products),'candidate_clause':clause,'pattern':pattern,'exact56':tests,
         'scope':'realizations invariant under the specified fivefold rotation',
         'source_search_not_imported':True}
    save(a.output,out);print(json.dumps(out),flush=True)

def lift(a):
    v=json.loads(a.verified.read_text());pattern=[(tuple(q),sg) for q,sg in v['pattern']]
    assert v['m']==5 and v['exact56']['forbidden_matches']==0
    layers=sorted({x//5 for q,sg in pattern for x in q});k=len(layers)
    assert 1<=k<=4
    ordered_injections=getattr(a,'ordered_injections',False)
    if k==4 and not ordered_injections:
        raise ValueError('four-orbit lifting requires explicit bounded ordered injections')
    e=encoder(a.layers);clauses=set();count=0;contradictory=0
    targets_iter=(itertools.combinations(range(a.layers),k) if ordered_injections else
                  itertools.permutations(range(a.layers),k))
    for targets in targets_iter:
        for rel in itertools.product(range(5),repeat=k-1):
            for direction,flip in itertools.product((-1,1),repeat=2):
                mp=dict(zip(layers,zip(targets,(0,)+rel)));required={};bad=False
                def f(x):
                    o,s=mp[x//5];return 5*o+(direction*(x%5)+s)%5
                for q,sg in pattern:
                    lit=e.o(*(f(x) for x in q));value=sg*flip*(1 if lit>0 else -1)
                    if abs(lit) in required and required[abs(lit)]!=value:bad=True;break
                    required[abs(lit)]=value
                count+=1
                if bad:contradictory+=1;continue
                clauses.add(tuple(-x if b>0 else x for x,b in sorted(required.items())))
    ordered=sorted(clauses);a.output.write_text(''.join(' '.join(map(str,c))+' 0\n' for c in ordered))
    # Directly test every emitted clause as well as the complete template test.
    tab,table_meta=exact_table(a.archive);rep={v:q for q,v in e.tvar.items()};direct=0
    for cl in ordered:
        support=sorted({x//5 for lit in cl for x in rep[abs(lit)]})
        assert len(support)==k
        test_targets=(((0,1,2),(4,5,6),(8,9,10)) if k<=3 else
                      ((0,1,2,3),(3,4,5,6),(7,8,9,10)))
        for target in test_targets:
            mp=dict(zip(support,target))
            for mirror in (-1,1):
                def tr(lit):
                    q=[5*mp[x//5]+x%5 for x in rep[abs(lit)]]
                    sign=tab[(q[0]*55+q[1])*55+q[2]]*mirror
                    assert sign
                    return (sign>0)==(lit>0)
                assert any(tr(l) for l in cl)
                direct+=1
    meta={'template_verified_sha256':sha(a.verified),'kind':v['kind'],'source_layers':layers,
          'target_layers':a.layers,'embeddings':count,'contradictory_premises':contradictory,
          'clauses':len(ordered),'family_sha256':sha(a.output),'direct_exact56_clause_tests':direct,
          'complete_template_tests':v['exact56'],'arithmetic_table':table_meta,
          'soundness':('Orbit injections and shifts substitute arbitrary seeds; inverse direction follows common conjugation; all bracket signs may be negated in a homogeneous identity with real coefficients.'
                       if v['kind']=='rotation_linear_identity' else
                       'Injective orbit maps commute with rotation or its inverse; global bracket-sign reversal preserves GP product signs.')}
    if ordered_injections:
        meta['orbit_injections']='order-preserving only; bounded partial family'
        meta['relative_shifts']='all, with the common shift fixed to zero'
    save(a.output.with_suffix(a.output.suffix+'.json'),meta);print(json.dumps(meta),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=('verify','lift'))
    p.add_argument('--archive',type=Path,required=True);p.add_argument('--model',type=Path)
    p.add_argument('--witness',type=Path);p.add_argument('--verified',type=Path)
    p.add_argument('--layers',type=int,default=12);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--ordered-injections',action='store_true')
    a=p.parse_args();a.archive.mkdir(parents=True,exist_ok=True)
    verify(a) if a.action=='verify' else lift(a)

if __name__=='__main__':main()
