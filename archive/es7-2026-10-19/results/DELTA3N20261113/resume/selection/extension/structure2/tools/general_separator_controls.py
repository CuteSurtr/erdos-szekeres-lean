"""n=5 edge cases and small n=6/n=8 controls; no selection search."""
from collections import Counter
from itertools import combinations, product
import argparse
import hashlib
import json
from pathlib import Path
import time
import traceback
from verify_structure2 import determinant, convex, maxgon


def cup(k):return [(i,i*i) for i in range(k)]
def cap(k):return [(i,-i*i) for i in range(k)]


def target(k):
    # k lower-cup vertices and one upper vertex, on a uniform x grid.
    middle=k//2
    return [(i,(k+1)**2 if i==middle else i*i) for i in range(k+1)]


def join(left,right):
    left=[(x,y-min(v for _,v in left)) for x,y in left]
    right=[(x,y-min(v for _,v in right)) for x,y in right]
    height=(len(left)+len(right)+1)*(max(y for _,y in left+right)+1)
    return left+[(x+len(left),y+height) for x,y in right]


def all_cups(signs,vertices,n):
    beta={i:1 for i in vertices}
    for k in range(2,min(len(vertices),n-1)+1):
        for ids in combinations(vertices,k):
            if all(signs[t]>0 for t in combinations(ids,3)):
                if k==n-1:return None
                beta[ids[-1]]=max(beta[ids[-1]],k)
    return beta


def check(p,cut,n):
    assert 0<cut<len(p)
    s={t:determinant(p,*t) for t in combinations(range(len(p)),3)}
    assert all(s.values())
    assert all(v>0 if b<cut<=c else v<0 if a<cut<=b else True for (a,b,c),v in s.items())
    idx=list(range(len(p)));L=idx[:cut];R=idx[cut:]
    beta=all_cups(s,idx,n);assert beta is not None
    bl=all_cups(s,L,n);br=all_cups(s,R,n)
    c=max(bl.values());assert 1<=c<=n-3
    c4=[t for t in combinations(idx,4) if all(s[u]<0 for u in combinations(t,3))]
    assert not any(all(s[u]<0 for u in combinations(t,3)) for t in combinations(idx,5))
    assert not any(convex(p,t) for t in combinations(idx,n))
    level=n-3 if c in (n-3,n-4) else n-2
    a={i for i in idx if beta[i]==level}
    targets=[t for t in combinations(idx,n-1) if convex(p,t)]
    assert all(a.intersection(t) for t in targets)
    assert not any(a.issuperset(t) for t in c4)
    tails={t[-2:] for t in c4}
    selected_caps=[t for t in combinations(sorted(a),3) if s[t]<0]
    assert all(t[-2:] in tails for t in selected_caps)
    assert all(beta[i]==max(c+1,br[i]) for i in R)
    gon=maxgon(s,idx);blue=maxgon(s,[i for i in idx if i not in a])
    assert gon<n and blue<n-1
    return dict(n=n,m=len(p),P=p,cut=cut,c=c,level=level,A=sorted(a),
        maxcup=max(beta.values()),maxgon=gon,complement_maxgon=blue,
        beta=[beta[i] for i in idx],target_count=len(targets),selected_cap_triples=selected_caps)


def named_cases():
    out={}
    setups=[('n5_c1',5,[(0,0)],target(3)),('n5_c2',5,cap(4),cup(3)),
            ('n5_two_singletons',5,[(0,0)],[(0,0)]),('n5_three_points',5,cup(2),[(0,0)])]
    for n in (6,8):
        for c in (n-5,n-4,n-3):
            setups.append((f'n{n}_c{c}',n,cup(c),cup(n-2) if c==n-3 else target(n-2)))
    for name,n,L,R in setups:out[name]=check(join(L,R),len(L),n)
    # A required-premise negative control: the formula fails for empty L.
    p=cap(4);s={t:determinant(p,*t) for t in combinations(range(4),3)}
    beta=all_cups(s,list(range(4)),5);a=[i for i in range(4) if beta[i]==3]
    assert not a and convex(p,range(4)) and maxgon(s,range(4))==4
    return dict(status='PASS',cases=out,negative_empty_left=dict(P=p,n=5,c=0,A=a,
                outcome='EXPECTED FAILURE without nonempty L: level 3 misses the four-cap target'))


def grid():
    stats=Counter();by_case=Counter();examples={};start=time.monotonic()
    for m in range(2,8):
        for ys in product(range(-3,4),repeat=m-2):
            if time.monotonic()-start>15:
                return dict(status='PARTIAL_TIME_BOUND',stats=dict(stats),case_counts=dict(by_case),examples=examples)
            stats['attempted']+=1;p=list(enumerate((0,0)+ys));idx=list(range(m))
            s={t:determinant(p,*t) for t in combinations(idx,3)}
            if not all(s.values()):continue
            stats['general_position']+=1
            cuts=[cut for cut in range(1,m) if all(v>0 if b<cut<=c else v<0 if a<cut<=b else True for (a,b,c),v in s.items())]
            if not cuts:continue
            stats['has_split']+=1
            if all_cups(s,idx,5) is None:continue
            if any(all(s[u]<0 for u in combinations(t,3)) for t in combinations(idx,5)):continue
            if maxgon(s,idx)>=5:continue
            stats['valid_sets']+=1
            for cut in cuts:
                r=check(p,cut,5);stats['checked_valid_splits']+=1;by_case[r['c']]+=1
                examples.setdefault(str(r['c']),r)
    return dict(status='PASS_COMPLETE_GRID',stats=dict(stats),case_counts=dict(by_case),examples=examples,
                scope='x=0,...,m-1, y0=y1=0, remaining heights in [-3,3], m=2,...,7; not all real order types')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['cases','grid'],required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();start=time.monotonic();result={}
    try:result=named_cases() if args.mode=='cases' else grid()
    except Exception:result.update(status='FAIL',traceback=traceback.format_exc());raise
    finally:
        result['elapsed_seconds']=time.monotonic()-start
        result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        args.out.write_text(json.dumps(result,indent=2)+'\n')
        if args.mode=='cases' and 'cases' in result:
            print(json.dumps({k:{key:value for key,value in r.items() if key not in ('P','beta','selected_cap_triples')} for k,r in result['cases'].items()}))
        else:print(json.dumps({k:v for k,v in result.items() if k!='examples'}))


if __name__=='__main__':main()
