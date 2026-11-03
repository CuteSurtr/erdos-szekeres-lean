#!/usr/bin/env python3
"""Complete rotation-deduplicated affine four-point sign family.

[abc]-[abd]+[acd]-[bcd]=0. Its four nonzero signed summands cannot
all have the same sign. These are standard affine-interiority constraints;
rotation is used only to identify variables and remove duplicate clauses.
"""
import argparse,hashlib,importlib.util,itertools,json,math,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--layers',type=int,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();start=time.monotonic()
    s=importlib.util.spec_from_file_location('exact_helpers',HERE/'m5_algebra.py')
    h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
    e=h.encoder(a.layers);n=5*a.layers;family=set();identities=0;tautologies=0
    for q in itertools.combinations(range(n),4):
        if q[0]%5:continue
        images=[tuple(sorted(5*(x//5)+(x%5+shift)%5 for x in q)) for shift in range(5)]
        if q!=min(images):continue
        identities+=1;a0,b,c,d=q
        ll=[e.o(a0,b,c),-e.o(a0,b,d),e.o(a0,c,d),-e.o(b,c,d)]
        for side in (-1,1):
            clause=set(side*l for l in ll)
            if any(-l in clause for l in clause):tautologies+=1;continue
            family.add(tuple(sorted(clause,key=lambda x:(abs(x),x))))
    assert identities==math.comb(n,4)//5
    ordered=sorted(family)
    a.output.write_text(''.join(' '.join(map(str,c))+' 0\n' for c in ordered))
    tab,tm=h.exact_table(a.archive);rep={v:q for q,v in e.tvar.items()};direct=0
    for cl in ordered:
        support=sorted({x//5 for l in cl for x in rep[abs(l)]});k=len(support)
        assert 1<=k<=4
        for targets in ((0,1,2,3),(3,5,7,9),(7,8,9,10)):
            for shifts in ((0,0,0,0),(0,1,2,3),(0,4,3,2)):
                mp=dict(zip(support,zip(targets,shifts)))
                for mirror in (-1,1):
                    def holds(lit):
                        q=[5*mp[x//5][0]+(x%5+mp[x//5][1])%5 for x in rep[abs(lit)]]
                        sign=tab[(q[0]*55+q[1])*55+q[2]]*mirror
                        assert sign
                        return (sign>0)==(lit>0)
                    assert any(holds(l) for l in cl)
                    direct+=1
    actual=0
    def chi(a0,b,c):return tab[(a0*55+b)*55+c]
    for a0,b,c,d in itertools.combinations(range(55),4):
        signs=(chi(a0,b,c),-chi(a0,b,d),chi(a0,c,d),-chi(b,c,d))
        assert 0 not in signs and len(set(signs))==2
        actual+=1
    meta={'kind':'standard_affine_interiority','target_layers':a.layers,'clauses':len(ordered),
          'rotation_representative_quads':identities,'all_quads':math.comb(n,4),
          'tautological_clauses_discarded':tautologies,'family_sha256':h.sha(a.output),
          'direct_exact56_clause_tests':direct,
          'complete_template_tests':{'forbidden_matches':0,'all_four_subsets_of_actual55':actual,
               'direct_orbit_selections_per_clause':3,'phase_patterns_per_selection':3,'both_mirror_signs':True},
          'arithmetic_table':tm,'proof':'The affine determinant identity [abc]-[abd]+[acd]-[bcd]=0 forbids four equal signed-term signs.',
          'elapsed_seconds':round(time.monotonic()-start,3)}
    h.save(a.output.with_suffix(a.output.suffix+'.json'),meta)
    print(json.dumps(meta),flush=True)

if __name__=='__main__':main()
