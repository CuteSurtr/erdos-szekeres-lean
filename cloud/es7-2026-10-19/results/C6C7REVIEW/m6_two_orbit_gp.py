#!/usr/bin/env python3
"""Complete GP sign family on every two-orbit restriction, with exact tests.

In [abc][ade]-[abd][ace]+[abe][acd]=0, three nonzero summands
cannot share a sign. Enumerate the sixteen forbidden bracket-sign patterns;
negating each gives a sound clause. Orbit canonicalization only substitutes
orientation literals. Tautologies are discarded, duplicate literals merged.
"""
import argparse,hashlib,importlib.util,itertools,json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    results=Path(__file__).resolve().parent.parent
    spec=importlib.util.spec_from_file_location('reference',results/'C7UPPER/gen.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    e=mod.Enc(6,8,10);clauses=set();identities=0;forbidden=0;tautologies=0
    def lits(q):
        p,b,c,d,f=q
        return [e.o(p,b,c),e.o(p,d,f),e.o(p,b,d),e.o(p,c,f),e.o(p,b,f),e.o(p,c,d)]
    for layers in itertools.combinations(range(10),2):
        pts=[6*i+k for i in layers for k in range(6)]
        for layer in layers:
            pivot=6*layer
            for rest in itertools.combinations([x for x in pts if x!=pivot],4):
                ll=lits((pivot,)+rest);identities+=1
                for s in (-1,1):
                    for b1,b2,b3 in itertools.product((-1,1),repeat=3):
                        vals=(b1,b1*s,b2,-b2*s,b3,b3*s)
                        assert vals[0]*vals[1]==-vals[2]*vals[3]==vals[4]*vals[5]
                        cl=set(-l if v>0 else l for l,v in zip(ll,vals));forbidden+=1
                        if any(-l in cl for l in cl):tautologies+=1;continue
                        clauses.add(tuple(sorted(cl,key=lambda x:(abs(x),x))))
    ordered=sorted(clauses);dest=a.out/'two_orbit_gp.clauses'
    dest.write_text(''.join(' '.join(map(str,c))+' 0\n' for c in ordered))
    raw=(results/'ES8SYM/sets/c6_54pts_9layers.pts').read_bytes();pts=[]
    for line in raw.decode().splitlines():
        if not line.strip() or line.startswith('#'):continue
        x,y,z,u,v,w=map(int,line.split());pts.append((2*x+y-z-2*u-v+w,y+z-v-w))
    det=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    reps={v:q for q,v in e.tvar.items()}
    checks=0
    # Each emitted clause is tested exactly on six concrete embeddings of its
    # source orbit set. The full identity test below separately covers all
    # 5-subsets of every pair of actual orbits.
    for cl in ordered:
        layers=sorted({x//6 for v in cl for x in reps[abs(v)]});assert 1<=len(layers)<=2
        for target in ((0,1),(3,4),(7,8)):
            mapping=dict(zip(layers,target))
            for flip in (-1,1):
                def val(v):
                    q=reps[abs(v)]
                    d=det(*(pts[6*mapping[x//6]+x%6] for x in q));assert d
                    return (d*flip>0)==(v>0)
                assert any(val(v) for v in cl)
                checks+=1
    exact_identities=0
    for i,j in itertools.combinations(range(9),2):
        pp=[6*i+k for k in range(6)]+[6*j+k for k in range(6)]
        for q5 in itertools.combinations(pp,5):
            for p in q5:
                b,c,d,f=[x for x in q5 if x!=p]
                br=lambda a,b,c:det(pts[a],pts[b],pts[c])
                vals=(br(p,b,c)*br(p,d,f),-br(p,b,d)*br(p,c,f),br(p,b,f)*br(p,c,d))
                assert sum(vals)==0 and all(vals) and len({v>0 for v in vals})==2
                exact_identities+=1
    summary={'rotation_representative_gp_identities':identities,'forbidden_assignments':forbidden,
             'tautologies':tautologies,'unique_clauses':len(ordered),'direct_exact54_clause_tests':checks,
             'exact54_full_two_orbit_gp_identities':exact_identities,
             'exact54_sha256':hashlib.sha256(raw).hexdigest(),'family_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
             'proof':'GP determinant identity; uniform brackets; exact literal substitution'}
    (a.out/'two_orbit_gp_verified.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
