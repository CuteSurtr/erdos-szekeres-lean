#!/usr/bin/env python3
"""Verify a two-layer GP sign contradiction and its exact 54-point tests."""
import argparse, hashlib, importlib.util, itertools, json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model',type=Path,required=True)
    ap.add_argument('--witness',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    results=Path(__file__).resolve().parents[2]
    spec=importlib.util.spec_from_file_location('reference',results/'C7UPPER/gen.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    e=mod.Enc(6,8,10)
    pos=set(json.loads(a.model.read_text()));w=json.loads(a.witness.read_text())
    assert w['model_sha256']==hashlib.sha256(a.model.read_bytes()).hexdigest()
    a0,b,c,d,f=w['anchor_quintuple']
    triples=(((a0,b,c),(a0,d,f),1),((a0,b,d),(a0,c,f),-1),((a0,b,f),(a0,c,d),1))
    lits=[e.o(*x) for z in triples for x in z[:2]]
    signs=[(1 if l>0 else -1)*(1 if abs(l) in pos else -1) for l in lits]
    gp=[signs[0]*signs[1],-signs[2]*signs[3],signs[4]*signs[5]]
    assert gp==w['term_signs'] and len(set(gp))==1
    used=sorted(set(map(abs,lits)))
    clause=[-v if v in pos else v for v in used]
    assert clause==w['candidate_clause']
    expected={q:1 if v in pos else -1 for q,v in e.tvar.items() if v in used}
    layers=sorted({x//6 for q in expected for x in q});assert len(layers)==2
    raw=(results/'ES8SYM/sets/c6_54pts_9layers.pts').read_bytes()
    pts=[]
    for line in raw.decode().splitlines():
        if not line.strip() or line.startswith('#'):continue
        x,y,z,u,v,w0=map(int,line.split());pts.append((2*x+y-z-2*u-v+w0,y+z-v-w0))
    det=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    checks=0;matches=0
    for reflect in (False,True):
        pp=[(x,-y if reflect else y) for x,y in pts]
        for i,j in itertools.permutations(range(9),2):
            for si,sj in itertools.product(range(6),repeat=2):
                def p(v):
                    layer,k=divmod(v,6)
                    orbit,shift=(i,si) if layer==layers[0] else (j,sj)
                    return pp[6*orbit+(k+shift)%6]
                vals=[co*det(*(p(v) for v in x))*det(*(p(v) for v in y)) for x,y,co in triples]
                assert sum(vals)==0 and all(vals)
                matches+=all((1 if det(*(p(v) for v in q))>0 else -1)==sg for q,sg in expected.items())
                checks+=1
    assert matches==0
    out={'model_sha256':hashlib.sha256(a.model.read_bytes()).hexdigest(),
         'witness_sha256':hashlib.sha256(a.witness.read_bytes()).hexdigest(),
         'source_layers':layers,'gp_signs':gp,'candidate_clause':clause,
         'exact54_labelled_pair_tests':checks,'exact54_forbidden_pattern_matches':matches,
         'exact54_sha256':hashlib.sha256(raw).hexdigest(),'candidate_added_to_cnf':False}
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
