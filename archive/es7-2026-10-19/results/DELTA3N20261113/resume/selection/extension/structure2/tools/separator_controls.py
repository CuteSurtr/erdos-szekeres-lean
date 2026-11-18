"""Small exact controls for the written separated-subclass theorem."""
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time


def turn(p,a,b,c):
    return (p[b][0]-p[a][0])*(p[c][1]-p[a][1])-(p[b][1]-p[a][1])*(p[c][0]-p[a][0])


def high_split(left,right):
    n=len(left)+len(right)
    left=[(x,y-min(p[1] for p in left)) for x,y in left]
    right=[(x,y-min(p[1] for p in right)) for x,y in right]
    bound=max(y for x,y in left+right)
    offset=n*(bound+1)
    return left+[(x+len(left),y+offset) for x,y in right]


def extremal(cup,cap):
    assert cup>=2 and cap>=2
    if cup==2:return [(i,-i*i) for i in range(cap)]
    if cap==2:return [(i,i*i) for i in range(cup)]
    return high_split(extremal(cup-1,cap),extremal(cup,cap-1))


def ranks(signs,vertices,sign):
    beta={i:1 for i in vertices};edges={}
    for j,b in enumerate(vertices):
        for i,a in enumerate(vertices[:j]):
            edges[a,b]=max([2]+[edges[z,a]+1 for z in vertices[:i] if signs[z,a,b]*sign>0])
            beta[b]=max(beta[b],edges[a,b])
    return beta,edges


def hull(p,ids):
    lo=[];hi=[]
    for seq,order in ((lo,ids),(hi,reversed(ids))):
        for i in order:
            while len(seq)>1 and turn(p,seq[-2],seq[-1],i)<=0:seq.pop()
            seq.append(i)
    return lo[:-1]+hi[:-1]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['c2','c3','c4'],required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();start=time.monotonic()
    shapes={'c2':((2,4),(5,3)),'c3':((3,4),(5,3)),'c4':((4,4),(5,2))}
    shapeL,shapeR=shapes[args.case];left=extremal(*shapeL);right=extremal(*shapeR)
    p=high_split(left,right);cut=len(left);n=len(p);L=list(range(cut));R=list(range(cut,n));idx=list(range(n))
    signs={t:turn(p,*t) for t in combinations(idx,3)}
    assert all(signs.values()) and all(p[i][0]<p[i+1][0] for i in range(n-1))
    assert all(signs[a,b,c]>0 for a,b in combinations(L,2) for c in R)
    assert all(signs[a,b,c]<0 for a in L for b,c in combinations(R,2))
    beta,_=ranks(signs,idx,1);alpha,_=ranks(signs,idx,-1)
    betaL,_=ranks(signs,L,1);betaR,_=ranks(signs,R,1);capR,_=ranks(signs,R,-1)
    c=max(betaL.values());selected_level=5 if c<=2 else 4
    selected=[i for i in idx if beta[i]==selected_level];aset=set(selected)
    assert max(beta.values())==5 and max(alpha.values())==4
    assert all(beta[i]==max(c+1,betaR[i]) for i in R)
    c4=[t for t in combinations(idx,4) if all(signs[s]<0 for s in combinations(t,3))]
    pair_witness={t[-2:]:t for t in c4}
    selected_cap_triples=[t for t in combinations(selected,3) if signs[t]<0]
    assert all(t[-2:] in pair_witness for t in selected_cap_triples)
    assert not any(aset.issuperset(t) for t in c4)
    targets=[t for t in combinations(idx,6) if len(hull(p,t))==6]
    assert targets and all(aset.intersection(t) for t in targets)
    seven_witness=next((t for t in combinations(idx,7) if len(hull(p,t))==7),None)
    assert seven_witness is None
    kinds={'left':0,'right':0,'mixed':0}
    for t in targets:
        kind='left' if t[-1]<cut else 'right' if t[0]>=cut else 'mixed';kinds[kind]+=1
    result=dict(status='PASS',label='COMPUTED exact exhaustive target/premise control',case=args.case,
                P=p,cut=cut,m=n,left_shape=shapeL,right_shape=shapeR,
                maxima=dict(cap=max(alpha.values()),cup=max(beta.values()),gon=6),
                beta=[beta[i] for i in idx],beta_left=[betaL[i] for i in L],beta_right=[betaR[i] for i in R],
                maxcup_left=c,maxcap_right=max(capR.values()),selected_level=selected_level,A=selected,
                hexagons=len(targets),hexagon_types=kinds,one_hexagon=targets[0],
                min_target_hits=min(len(aset.intersection(t)) for t in targets),
                targets_sha256=hashlib.sha256(json.dumps(targets,separators=(',',':')).encode()).hexdigest(),
                four_caps=len(c4),selected_cap_triples=selected_cap_triples,
                terminal_witnesses={str(t):pair_witness[t[-2:]] for t in selected_cap_triples},
                seven_gon=None,minimum_absolute_determinant=min(map(abs,signs.values())),
                elapsed_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('P','terminal_witnesses','selected_cap_triples','beta_left','beta_right')}))


if __name__=='__main__':main()
