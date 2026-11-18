"""Direct full-set terminal counts vs the two-option low-split classification.

Imports no finder, generator, prior checker or SAT code. Uses integer
determinants, monotone hulls, and upward mask propagation of the actual
terminal membership constraints.
"""
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback


def det(p,a,b,c):
    x,y=p[a];u,v=p[b];s,t=p[c]
    return x*(v-t)+u*(t-y)+s*(y-v)


def hull(p,vertices):
    lower=[];upper=[]
    for chain,order in ((lower,vertices),(upper,reversed(vertices))):
        for v in order:
            while len(chain)>1 and det(p,chain[-2],chain[-1],v)<=0:chain.pop()
            chain.append(v)
    return lower[:-1]+upper[:-1]


def bm(vertices):return sum(1<<v for v in vertices)


def upward(family,m):
    result=bytearray(1<<m)
    for bits in family:result[bits]=1
    for j in range(m):
        step=1<<j
        for base in range(0,1<<m,2*step):
            for i in range(base,base+step):result[i+step]|=result[i]
    return result


def canonical_join(left,d):
    first=left[-1][0]+1;cut=len(left)
    p=list(left)+[(first+j,j*j) for j in range(d)];height=0
    for a,b in combinations(range(cut),2):
        for c in range(cut,len(p)):
            height=max(height,det(p,a,b,c)//(p[b][0]-p[a][0])+1)
    for a in range(cut):
        for b,c in combinations(range(cut,len(p)),2):
            height=max(height,(-det(p,a,b,c))//(p[c][0]-p[b][0])+1)
    return list(left)+[(first+j,j*j-height) for j in range(d)]


def check(left,n):
    p=canonical_join(left,n-4);cut=len(left);m=len(p);ids=list(range(m));L=ids[:cut]
    signs={t:det(p,*t) for t in combinations(ids,3)};assert all(signs.values())
    assert all(v<0 if b<cut<=c else v>0 if a<cut<=b else True for (a,b,c),v in signs.items())
    caps=[t for t in combinations(ids,4) if all(signs[u]<0 for u in combinations(t,3))]
    assert all(t[-1]>=cut for t in caps)
    assert not any(all(signs[u]<0 for u in combinations(t,3)) for t in combinations(ids,5))
    assert not any(len(hull(p,t))==n for t in combinations(ids,n))
    targets=[t for t in combinations(ids,n-1) if len(hull(p,t))==n-1]
    tails={t[-2:] for t in caps}
    bad=[t for t,v in signs.items() if v<0 and t[-2:] not in tails]
    contains_bad=upward([bm(t) for t in bad+caps],m)
    contains_target=upward([bm(t) for t in targets],m);full=(1<<m)-1
    direct_count=sum(not contains_bad[a] and not contains_target[full^a] for a in range(1<<m))
    leftcaps=[t for t,v in signs.items() if v<0 and t[-1]<cut]
    lefttargets=[t for t in targets if t[-1]<cut]
    ends3={t[-1] for t in leftcaps};allL=(1<<cut)-1
    capm=[bm(t) for t in leftcaps];hm=[bm(t) for t in lefttargets]
    option1=[];option2=[]
    for a in range(1<<cut):
        if any(a&c==c for c in capm):continue
        selected=[v for v in L if a>>v&1]
        if all(a&h for h in hm) and all(v in ends3 for v in selected[1:]):option1.append(a)
        blue=allL^a
        if blue.bit_count()<=n-2 and not any(blue&c==c for c in capm):option2.append(a)
    predicted=((1<<(n-4))-1)*len(option1)+len(option2)
    assert predicted==direct_count
    # Check each full model against its classified alternative as well as counts.
    one=set(option1);two=set(option2);rightmask=full^allL
    for a in range(1<<m):
        direct=not contains_bad[a] and not contains_target[full^a]
        classified=(a&allL in one) if a&rightmask else (a&allL in two)
        assert direct==classified
    return dict(status='PASS',n=n,m_left=cut,m_full=m,P=p,
       actual_fourcaps=len(caps),actual_unprotected_cap_triples=len(bad),actual_targets=len(targets),
       option1_count=len(option1),option2_count=len(option2),direct_terminal_count=direct_count,
       predicted_terminal_count=predicted,assignments_compared=1<<m,
       no_fivecap=True,no_n_gon=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();root=Path(__file__).resolve().parents[1]
    start=time.monotonic();result=dict(cases={},inputs={})
    try:
        setups=[('n5_rank_counter',5,[(0,0),(1,0),(2,-3),(3,-3),(4,1),(5,2)])]
        n6=root.parents[4]/'DELTA2N20261113/data/cex/restr_QQ_weak_a4_n6_m11_real.json'
        n7=root/'data/low_n7_fixed_1.json'
        setups.append(('n6_old_real11',6,json.loads(n6.read_text())['P']))
        setups.append(('n7_fixed_left16',7,json.loads(n7.read_text())['result']['P']))
        for path in (n6,n7):result['inputs'][str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for name,n,left in setups:
            r=check(left,n);result['cases'][name]=r
            print(json.dumps(dict(name=name,**{k:v for k,v in r.items() if k!='P'})),flush=True)
        result['status']='PASS'
    except Exception:result.update(status='FAIL',traceback=traceback.format_exc());raise
    finally:
        result['elapsed_seconds']=time.monotonic()-start
        result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        args.out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('cases','inputs')}))


if __name__=='__main__':main()
