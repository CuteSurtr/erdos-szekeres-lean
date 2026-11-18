"""Direct witness replay, importing neither finder nor envelope implementation.

Uses consecutive slopes for caps, triangle containment for convexity, and
the saved convex-combination certificates instead of the envelope algorithm.
This is a second implementation within this track, not a separate reviewer.
"""
import argparse
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path


def det(p,a,b,c):
    return ((p[b][0]-p[a][0])*(p[c][1]-p[a][1])
            -(p[c][0]-p[a][0])*(p[b][1]-p[a][1]))


def iscap(p,ids):
    return all(det(p,*ids[i:i+3])<0 for i in range(len(ids)-2))


def nonconvex4(p,ids):
    for v in ids:
        a,b,c=[i for i in ids if i!=v]
        d=(det(p,a,b,v),det(p,b,c,v),det(p,c,a,v))
        if all(x>0 for x in d) or all(x<0 for x in d):
            return True
    return False


def lin(p,pair):
    a,b=pair
    s=Q(p[b][1]-p[a][1],p[b][0]-p[a][0])
    return s,Q(p[b][1])+s*(p[-1][0]-p[b][0])


def verify(p,n,A,certs):
    assert all(p[i][0]<p[i+1][0] for i in range(len(p)-1))
    assert all(det(p,*t)!=0 for t in combinations(range(len(p)),3))
    assert not any(iscap(p,c) for c in combinations(A,4))
    blue=[i for i in range(len(p)) if i not in A]
    interior={c for c in combinations(blue,4) if nonconvex4(p,c)}
    checked=0
    for h in combinations(blue,n-1):
        # In general position, a set is convex iff all its four-subsets are.
        assert any(c in interior for c in combinations(h,4)), ('missed target',h)
        checked+=1
    triples={c for c in combinations(A,3) if iscap(p,c)}
    assert triples=={tuple(row['triple']) for row in certs}
    for row in certs:
        q=lin(p,row['triple'][-2:])
        weights=[]; ls=[]
        for r in row['supports']:
            c=r['ambient_fourcap']; pair=r['pair']; w=Q(r['weight'])
            assert c==sorted(c) and len(c)==len(set(c))==4
            assert iscap(p,c) and pair==c[-2:]
            l=lin(p,pair)
            assert l==tuple(map(Q,r['line']))
            assert w>=0
            weights.append(w); ls.append(l)
        assert 1<=len(weights)<=2 and sum(weights)==1
        assert sum(w*l[0] for w,l in zip(weights,ls))>=q[0]
        assert sum(w*l[1] for w,l in zip(weights,ls))>=q[1]
    return dict(A=A,threecaps_checked=len(triples),blue_subsets_checked=checked)


ap=argparse.ArgumentParser()
ap.add_argument('inputs',type=Path)
ap.add_argument('cases',type=Path)
ap.add_argument('--out',required=True,type=Path)
args=ap.parse_args()
rows=[]
for r in json.loads(args.inputs.read_text()):
    result=json.loads((args.cases/(r['name']+'.json')).read_text())
    assert result['result']['outcome']=='SAT_EXACT_MODEL_CHECKED'
    row=verify(r['P'],r['n'],result['result']['A'],result['all_X_certificates'])
    row['name']=r['name']
    if 'known_A' in r:
        row['prior_known_A']=verify(r['P'],r['n'],r['known_A'],result['known_A_certificates'])
    rows.append(row)
packet=dict(label='COMPUTED',scope='Positive witnesses only; no UNSAT certification or fresh full-premise audit.',
            second_implementation_same_track=True,results=rows)
args.out.write_text(json.dumps(packet,indent=2)+'\n')
print(json.dumps(dict(positive_models=len(rows),threecaps=sum(r['threecaps_checked'] for r in rows),
                     blue_subsets=sum(r['blue_subsets_checked'] for r in rows))))
