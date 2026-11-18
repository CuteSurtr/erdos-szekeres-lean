"""Independent exact replay; imports no finder, generator or prior checker.

Ranks are checked by direct cup enumeration. Polygon maxima use reachable
cup/cap chains with prescribed common endpoints, validated on small sets
by triangle containment. This differs from the finder's monotone hulls.
"""
from fractions import Fraction as F
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import random
import resource
import time
import traceback


def determinant(p,a,b,c):
    x,y=p[a];u,v=p[b];s,t=p[c]
    return x*v+u*t+s*y-y*u-v*s-t*x


def signs_of(p):
    assert all(p[i][0]<p[i+1][0] for i in range(len(p)-1))
    result={t:determinant(p,*t) for t in combinations(range(len(p)),3)}
    assert all(result.values())
    return result


def convex(p,ids):
    for v in ids:
        for a,b,c in combinations([i for i in ids if i!=v],3):
            ds=(determinant(p,a,b,v),determinant(p,b,c,v),determinant(p,c,a,v))
            if all(x>0 for x in ds) or all(x<0 for x in ds):return False
    return True


def maxgon(signs,vertices):
    vertices=sorted(vertices);best=min(2,len(vertices))
    for start in range(len(vertices)-1):
        left=vertices[start];up={};down={}
        for j in range(start+1,len(vertices)):
            b=vertices[j];up[left,b]=down[left,b]=2
            for i in range(start+1,j):
                a=vertices[i]
                up[a,b]=max([0]+[up[k,a]+1 for k in vertices[start:i]
                    if up.get((k,a),0)>0 and signs[k,a,b]>0])
                down[a,b]=max([0]+[down[k,a]+1 for k in vertices[start:i]
                    if down.get((k,a),0)>0 and signs[k,a,b]<0])
            cup=max(up[a,b] for a in vertices[start:j])
            cap=max(down[a,b] for a in vertices[start:j])
            best=max(best,cup+cap-2)
    return best


def ranks_by_subsets(signs,vertices):
    beta={i:1 for i in vertices};six=0
    for k in range(2,7):
        for t in combinations(vertices,k):
            if all(signs[s]>0 for s in combinations(t,3)):
                beta[t[-1]]=max(beta[t[-1]],k)
                if k==6:six+=1
    assert six==0
    return beta


def four_caps(signs,vertices):
    assert not any(all(signs[s]<0 for s in combinations(t,3)) for t in combinations(vertices,5))
    return [t for t in combinations(vertices,4) if all(signs[s]<0 for s in combinations(t,3))]


def line(p,a,b):
    s=F(p[b][1]-p[a][1],p[b][0]-p[a][0])
    return s,p[b][1]+s*(p[-1][0]-p[b][0])


def certificate(q,ambient):
    for ab,l in ambient.items():
        if l[0]>=q[0] and l[1]>=q[1]:return [(ab,F(1))]
    for ab,l in ambient.items():
        if l[0]>=q[0]:continue
        for cd,r in ambient.items():
            if r[0]<=q[0]:continue
            w=(r[0]-q[0])/(r[0]-l[0])
            if w*l[1]+(1-w)*r[1]>=q[1]:return [(ab,w),(cd,1-w)]
    return None


def split_cuts(p,sgn):
    return [cut for cut in range(1,len(p)) if all(
        value>0 if b<cut<=c else value<0 if a<cut<=b else True
        for (a,b,c),value in sgn.items())]


def serial(obj):
    if isinstance(obj,F):return str(obj)
    if isinstance(obj,dict):return {str(k):serial(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [serial(v) for v in obj]
    return obj


def verify(root,output):
    rng=random.Random(20261114);small=0
    for n in range(3,9):
        for _ in range(4):
            while True:
                p=[(i,rng.randrange(-100,101)) for i in range(n)]
                raw={t:determinant(p,*t) for t in combinations(range(n),3)}
                if all(raw.values()):break
            expected=next(k for k in range(n,2,-1) if any(convex(p,t) for t in combinations(range(n),k)))
            assert maxgon(raw,range(n))==expected
            small+=1
    output['polygon_dp_controls']=small
    output['separator_controls']={}
    for case in ('c2','c3','c4'):
        path=root/'data'/('separator_'+case+'.json');r=json.loads(path.read_text());p=r['P']
        s=signs_of(p);idx=list(range(len(p)));cut=r['cut'];L=idx[:cut];R=idx[cut:]
        assert cut in split_cuts(p,s)
        beta=ranks_by_subsets(s,idx);betaL=ranks_by_subsets(s,L);betaR=ranks_by_subsets(s,R)
        assert [beta[i] for i in idx]==r['beta']
        assert all(beta[i]==max(max(betaL.values())+1,betaR[i]) for i in R)
        c4=four_caps(s,idx);a=set(r['A'])
        assert a=={i for i in idx if beta[i]==r['selected_level']}
        assert not any(a.issuperset(t) for t in c4)
        tails={t[-2:] for t in c4}
        selected_caps=[t for t in combinations(sorted(a),3) if s[t]<0]
        assert all(t[-2:] in tails for t in selected_caps)
        full=maxgon(s,idx);blue=maxgon(s,[i for i in idx if i not in a])
        assert full==6 and blue<6
        assert max(beta.values())==5 and c4
        output['separator_controls'][case]=dict(status='PASS',m=len(p),A=sorted(a),
            maxgon=full,complement_maxgon=blue,selected_cap_triples=len(selected_caps),
            source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    data=json.loads((root/'data/initial_profiles.json').read_text());r=data['fixtures']['terminal18'];p=r['P']
    s=signs_of(p);idx=list(range(len(p)));beta=ranks_by_subsets(s,idx);c4=four_caps(s,idx)
    assert [beta[i] for i in idx]==r['beta'] and maxgon(s,idx)==6
    L5={i for i in idx if beta[i]==5};T={i for i in idx if beta[i]>=4};region=L5|{10}
    hs=[(0,1,5,6,9,10),(0,1,2,6,7,11),(2,3,5,6,13,14),(2,3,5,6,13,16)]
    for h,v in zip(hs,(10,11,14,16)):
        assert convex(p,h) and region.intersection(h)=={v}
    assert (10,11,14,16) in c4
    graph_rows=[((0,1,5,6,9,10),{10}),((0,1,2,6,7,11),{7,11}),
                ((0,1,8,9,14,16),{8,14,16}),((2,3,5,9,11,12),{3,11,12}),
                ((2,4,5,9,11,12),{4,11,12})]
    for h,trace in graph_rows:assert convex(p,h) and T.intersection(h)==trace
    for t in ((3,4,11,12),(7,8,11,12),(10,11,14,16),(10,14,15,16)):assert t in c4
    ambient={t[-2:]:line(p,*t[-2:]) for t in c4}
    q=line(p,16,17);gaps={ab:q[0]+q[1]-u-w for ab,(u,w) in ambient.items()}
    assert s[12,16,17]<0 and min(gaps.values())>0
    chosen=[3,4,7,10,14,16];a=set(chosen)
    assert not any(a.issuperset(t) for t in c4)
    assert maxgon(s,[i for i in idx if i not in a])<6
    certificates={}
    for t in combinations(chosen,3):
        if s[t]<0:
            certificates[t]=certificate(line(p,*t[-2:]),ambient)
            assert certificates[t] is not None
    parent_negative={}
    for t in ((5,6,14,17),(5,7,14,17)):
        values=[s[tri] for tri in combinations(t,3)]
        word=''.join('+' if v>0 else '-' for v in values);assert word=='++--'
        parent_negative[t]=dict(determinants=values,signs=word)
    assert (6,7,14,17) in c4
    assert [t for t in combinations([0,5,6,7,8],3) if s[t]<0]==[(0,5,6),(0,5,7)]
    output['terminal18']=dict(status='PASS',beta=[beta[i] for i in idx],maxgon=6,
       one_representative_core=hs,first_pair_core_hexagons=[h for h,tr in graph_rows],
       exposed_triple=[12,16,17],t=1,exposure_minimum_gap=min(gaps.values()),
       positive_A=chosen,positive_certificates=certificates,split_cuts=split_cuts(p,s),
       withdrawn_parent_quadruples=parent_negative)
    assert not output['terminal18']['split_cuts']
    boundary=data['fixtures']['three_block_n7']['P'];bs=signs_of(boundary)
    output['boundary_n7_split_cuts']=split_cuts(boundary,bs)
    # Real, GP, five-cap-free positive controls for strict and shared endpoints.
    p=[(0,-8),(1,1),(2,4),(3,-10),(4,11),(5,25),(6,36)]
    s=signs_of(p);c4=four_caps(s,list(range(7)));assert (3,4,5,6) in c4
    examples=[]
    for bc in ((1,2),(1,5),(1,6)):
        assert s[0,*bc]<0
        union=sorted(set(bc+(5,6)))
        assert all(s[t]>0 for t in combinations(union,3))
        earlier=line(p,*bc);later=line(p,5,6)
        assert later[0]>=earlier[0] and later[1]>=earlier[1]
        examples.append(dict(triple=(0,*bc),ambient_cap=(3,4,5,6),cup_union=union,
                             earlier_line=earlier,later_line=later))
    output['cup_rule_positive_control']=dict(P=p,certificates=examples)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();assert not args.out.exists()
    root=Path(__file__).resolve().parents[1];start=time.monotonic();output={}
    try:
        verify(root,output);output['status']='PASS'
    except Exception:
        output['status']='FAIL';output['traceback']=traceback.format_exc();raise
    finally:
        output['elapsed_seconds']=time.monotonic()-start
        output['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        output['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        args.out.write_text(json.dumps(serial(output),indent=2)+'\n')
        print(json.dumps(serial({k:v for k,v in output.items() if k!='terminal18'})))


if __name__=='__main__':main()
