#!/usr/bin/env python3
"""Emit exact-tested GP clauses for retained fivefold model violations.

The determinant identity has three nonzero summands, which cannot all have
the same sign. All sixteen impossible assignments to its six brackets are
enumerated. No layer order or geometric rotation is needed for this argument.
"""
import argparse, importlib.util, itertools, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True)
    p.add_argument('--violations',type=Path,required=True);p.add_argument('--archive',type=Path,required=True)
    p.add_argument('--source-layers',type=int,default=12);p.add_argument('--target-layers',type=int,required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    s=importlib.util.spec_from_file_location('exact',HERE/'m5_algebra.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
    source=v.encoder(a.source_layers);target=v.encoder(a.target_layers);positive=set(json.loads(a.model.read_text()))
    clauses=set();count=0;truth_tables=0
    for line in a.violations.read_text().splitlines():
        q=tuple(map(int,line.split()))
        if len(q)!=5 or len(set(q))!=5 or not all(0<=x<5*min(a.source_layers,a.target_layers) for x in q):raise ValueError('point IDs')
        p0,b,c,d,e=q;triples=((p0,b,c),(p0,d,e),(p0,b,d),(p0,c,e),(p0,b,e),(p0,c,d))
        original=[source.o(*tr) for tr in triples]
        signs=[(1 if lit>0 else -1)*(1 if abs(lit) in positive else -1) for lit in original]
        if not signs[0]*signs[1]==-signs[2]*signs[3]==signs[4]*signs[5]:raise ValueError('not a violated identity')
        literals=[target.o(*tr) for tr in triples];count+=1
        for common in (-1,1):
            for x,y,z in itertools.product((-1,1),repeat=3):
                values=(x,x*common,y,-y*common,z,z*common);truth_tables+=1
                if not values[0]*values[1]==-values[2]*values[3]==values[4]*values[5]:raise ValueError('truth table')
                clause=set(-lit if val>0 else lit for lit,val in zip(literals,values))
                if not any(-lit in clause for lit in clause):clauses.add(tuple(sorted(clause,key=lambda x:(abs(x),x))))
    ordered=sorted(clauses);a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(''.join(' '.join(map(str,cl))+' 0\n' for cl in ordered))
    table,table_meta=v.exact_table(a.archive);representatives={var:q for q,var in target.tvar.items()};tests=0
    for clause in ordered:
        support=sorted({x//5 for lit in clause for x in representatives[abs(lit)]})
        if len(support)>5:raise ValueError('support size')
        for offset in (0,3,6):
            mapping={layer:(i+offset)%11 for i,layer in enumerate(support)}
            for flip in (-1,1):
                def satisfied(lit):
                    q=[5*mapping[x//5]+x%5 for x in representatives[abs(lit)]]
                    sg=table[(q[0]*55+q[1])*55+q[2]]*flip
                    if sg==0:raise ValueError('test is not general position')
                    return (lit>0)==(sg>0)
                if not any(satisfied(lit) for lit in clause):raise ValueError('failed certified-set test')
                tests+=1
    record={'kind':'gp_sign_refinement','source_model_sha256':v.sha(a.model),'source_layers':a.source_layers,
        'target_layers':a.target_layers,'violations_sha256':v.sha(a.violations),'verified_violated_relations':count,
        'clauses':len(ordered),'family_sha256':v.sha(a.output),'direct_exact56_clause_tests':tests,
        'complete_template_tests':{'forbidden_matches':0,'mode':'all sixteen forbidden bracket assignments per retained identity',
            'truth_table_cases':truth_tables,'all_orbit_injections':False},'arithmetic_table':table_meta,
        'proof':'GP determinant identity and exact literal substitution; finite certified-set tests check implementation'}
    v.save(a.output.with_suffix(a.output.suffix+'.json'),record);print(json.dumps(record))
if __name__=='__main__':main()
