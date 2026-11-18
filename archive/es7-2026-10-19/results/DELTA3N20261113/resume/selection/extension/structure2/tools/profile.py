"""Exact, bounded rank and polygon profiles of fixed fixtures only."""
from fractions import Fraction as Q
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import time


def det(p,a,b,c):
    return (p[b][0]-p[a][0])*(p[c][1]-p[a][1])-(p[b][1]-p[a][1])*(p[c][0]-p[a][0])


def hull(p,ids):
    lo=[];hi=[]
    for seq,order in ((lo,ids),(hi,reversed(ids))):
        for i in order:
            while len(seq)>1 and det(p,seq[-2],seq[-1],i)<=0:
                seq.pop()
            seq.append(i)
    return lo[:-1]+hi[:-1],lo,hi


def profile(p):
    n=len(p);idx=range(n)
    assert all(p[i][0]<p[i+1][0] for i in range(n-1))
    signs={t:det(p,*t) for t in combinations(idx,3)}
    assert all(signs.values())
    c3=[t for t,v in signs.items() if v<0]
    c4=[t for t in combinations(idx,4) if all(signs[s]<0 for s in combinations(t,3))]
    assert not any(all(signs[a,b,d]<0 for a,b in combinations(c,2)) for c in c4 for d in range(c[-1]+1,n))
    edges={};beta=[1]*n
    for b in idx:
        for a in range(b):
            edges[a,b]=max([2]+[edges[t,a]+1 for t in range(a) if signs[t,a,b]>0])
            beta[b]=max(beta[b],edges[a,b])
    targets=[];types={}
    for t in combinations(idx,6):
        h,lo,hi=hull(p,t)
        if len(h)==6:
            targets.append(t);types[t]=(len(hi),len(lo))
    assert not any(len(hull(p,t)[0])==7 for t in combinations(idx,7))
    end=sorted({t[-1] for t in targets});endset=set(end)
    pairs={c[-2:] for c in c4}
    m=p[-1][0]
    def line(ab):
        a,b=ab;s=Q(p[b][1]-p[a][1],p[b][0]-p[a][0]);return s,p[b][1]+s*(m-p[b][0])
    ambient={ab:line(ab) for ab in pairs}
    exp_pairs={}
    for ab in {t[-2:] for t in c3}:
        s,z=line(ab);low=Q(0);high=None;empty=False
        for u,w in ambient.values():
            if u==s and w>=z: empty=True;break
            if u<s:low=max(low,(w-z)/(s-u))
            if u>s:
                v=(z-w)/(u-s);high=v if high is None else min(v,high)
        if not empty and (high is None or low<high):exp_pairs[ab]=(str(low),None if high is None else str(high))
    bad=[t for t in c3 if t[-2:] in exp_pairs]
    top={i for i in idx if beta[i]>=4}
    selected={
        'endpoints':endset,
        'top_two_levels':top,
        'level4':{i for i in idx if beta[i]==4},
        'level5':{i for i in idx if beta[i]==5}}
    profiles={}
    for name,a in selected.items():
        profiles[name]=dict(A=sorted(a),missed=[list(t) for t in targets if not a.intersection(t)],
                            cap4=[list(t) for t in c4 if a.issuperset(t)],
                            exposed=[list(t) for t in bad if a.issuperset(t)],
                            min_hits=min((len(a.intersection(t)) for t in targets),default=0))
    return dict(P=p,m=n,beta=beta,maxcup=max(beta),targets=targets,
                target_types={str(k):v for k,v in types.items()},
                caps4=c4,exposed=bad,exposed_pairs={str(k):v for k,v in exp_pairs.items()},
                profiles=profiles,rank3_triples=[t for t in c3 if t[-2:] not in pairs])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    assert not args.out.exists()
    parent=Path('cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection')
    sources=[parent/'terminal/data/witness.json',parent/'boundary/theory/data/controls.json']
    raw=[json.loads(p.read_text()) for p in sources]
    points={'terminal18':raw[0]['P'],'three_block_n7':next(c['points'] for c in raw[1]['controls'] if c['n']==7)}
    start=time.monotonic();output={}
    for name,p in points.items():
        r=profile(p);output[name]=r
        print(json.dumps(dict(name=name,m=r['m'],beta=r['beta'],maxcup=r['maxcup'],targets=len(r['targets']),
                             profiles={key:{k:(len(v) if k in ('missed','cap4','exposed') else v) for k,v in value.items()} for key,value in r['profiles'].items()})),flush=True)
    result=dict(status='COMPUTED profiles only',fixtures=output,elapsed=time.monotonic()-start,
                sources={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
