"""Separate exact replay of every reported gain, plus full small-case closure."""
import argparse
from collections import Counter
from itertools import combinations as C
import json
from pathlib import Path
import time


def orientation(p,a,b,c):
    return p[a][0]*(p[b][1]-p[c][1])+p[b][0]*(p[c][1]-p[a][1])+p[c][0]*(p[a][1]-p[b][1])


def setup(p):
    m=len(p);sgn={t:1 if orientation(p,*t)>0 else -1 if orientation(p,*t)<0 else 0 for t in C(range(m),3)};assert all(sgn.values())
    c3=[t for t,v in sgn.items() if v<0];c4=[t for t in C(range(m),4) if all(sgn[z]<0 for z in C(t,3))];ambient={c[-2:] for c in c4}
    rank={}
    for b,c in C(range(m),2):
        rank[b,c]=max([2]+[rank[a,b]+1 for a in range(b) if sgn[a,b,c]<0])
    assert max(rank.values())<5
    def edge(q,r):return q[0]<=r[0] and q[1]<=r[1] and q!=r and all(sgn[t]>0 for t in C(sorted(set(q+r)),3))
    def one(q):return q in ambient or any(edge(q,r) for r in ambient)
    return sgn,c3,c4,ambient,edge,one


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();start=time.monotonic()
    inputs=json.loads((args.run/'inputs.json').read_text());results=[json.loads(x) for x in (args.run/'results.jsonl').read_text().splitlines()];assert len(inputs)==len(results)==318
    closure_gains=force_gains=0;full_cases=[];closure_only=force_only=0;noncap_closed=0;noncap_forced=0;rows=[]
    for index,(inp,r) in enumerate(zip(inputs,results)):
        assert inp['name']==r['name'];p=inp['P'];sgn,c3,c4,ambient,edge,one=setup(p);cap_pairs={t[-2:] for t in c3};unprotected=set()
        closure_set={tuple(z['pair']) for z in r['closure_added']};force_set={tuple(z['pair']) for z in r['forced_added']}
        assert len(closure_set)==len(r['closure_added']) and len(force_set)==len(r['forced_added'])
        for pair in closure_set|force_set:
            assert not one(pair);unprotected.add(pair)
        for z in r['closure_added']:
            path=[tuple(a) for a in z['path']];q=tuple(z['pair']);assert path[0]==q and path[-1] in ambient
            assert tuple(z['ambient_fourcap']) in c4 and tuple(z['ambient_fourcap'][-2:])==path[-1]
            assert all(edge(a,b) for a,b in zip(path,path[1:]));assert z['cap_terminal']==(q in cap_pairs)
            closure_gains+=1;noncap_closed+=q not in cap_pairs
        for z in r['forced_added']:
            q=tuple(z['pair']);e=tuple(z['support']);cap=tuple(z['ambient_fourcap']);assert cap in c4 and cap[-2:]==e
            ids=sorted(set(q+e));diff=[]
            for v in ids:
                if v in q and v in e:d=0
                elif v in q:d=-orientation(p,*e,v)
                else:d=orientation(p,*q,v)
                diff.append(1 if d>0 else -1 if d<0 else 0)
            assert diff==z['endpoint_difference_signs'] and diff[-1]>=0 and any(x<=0 and (x<0 or diff[-1]>0) for x in diff[:-1])
            assert e[1]>=q[1] and z['cap_terminal']==(q in cap_pairs)
            force_gains+=1;noncap_forced+=q not in cap_pairs
        # Independent fixed-point closure on the three controls/fixtures and
        # deterministic small/large pool cases. Other cases replay every gain.
        if index in (0,1,2,3,22,67,124,125,254,265):
            pairs=list(C(range(len(p)),2));direct={q for q in pairs if one(q)};closed=set(ambient)
            changed=True
            while changed:
                changed=False
                for q in pairs:
                    if q not in closed and any(edge(q,t) for t in closed):closed.add(q);changed=True
            assert len(direct)==r['direct_cup'] and len(closed)==r['cup_closure'] and closed-direct==closure_set
            full_cases.append(r['name'])
        closure_only+=len(closure_set-force_set);force_only+=len(force_set-closure_set)
        rows.append({'name':r['name'],'closure_added_checked':len(closure_set),'force_added_checked':len(force_set),'closure_not_force':sorted(closure_set-force_set),'force_not_closure':sorted(force_set-closure_set)})
    # Six-point no-five-cap counterexample to direct cup = cup-path closure.
    old=inputs[1]['P'];ids=[0,5,6,9,12,13];p=[old[i] for i in ids];sgn,c3,c4,ambient,edge,one=setup(p)
    path=[(1,2),(2,5),(4,5)];cap=(0,3,4,5);assert (0,1,2) in c3 and cap in c4
    assert not one(path[0]) and all(edge(a,b) for a,b in zip(path,path[1:])) and cap[-2:]==path[-1]
    fixture={'P':p,'source_indices':ids,'cap_triple':[0,1,2],'path':path,'ambient_fourcap':cap,'all_fourcaps':c4,'no_fivecap':True,'direct_cup_protected':False,'cup_path_protected':True}
    args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'six_point_gain.json').write_text(json.dumps(fixture,indent=2)+'\n')
    report={'label':'COMPUTED separate exact gain replay','verdict':'PASS','cases':318,'valid_geometries':317,'raw_relation_controls':1,'closure_added_pairs_checked':closure_gains,'closure_added_cap_terminal_checked':closure_gains-noncap_closed,'forced_added_pairs_checked':force_gains,'forced_added_cap_terminal_checked':force_gains-noncap_forced,'closure_not_endpoint_forced_pairs':closure_only,'endpoint_forced_not_closure_pairs':force_only,'full_fixed_point_recomputations':full_cases,'per_case':rows,'seconds':time.monotonic()-start,'scope':'Every reported gain independently verifies its witness and absence of direct ambient cup protection; full closure recomputed on listed cases only.'}
    (args.out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('per_case','scope','full_fixed_point_recomputations')}))
if __name__=='__main__':main()
