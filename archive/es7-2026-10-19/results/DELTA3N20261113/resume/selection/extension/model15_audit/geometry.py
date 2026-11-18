#!/usr/bin/env python3
"""Independent integer-coordinate/hull replay, including every selection."""
import argparse
from collections import Counter
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback

HERE=Path(__file__).resolve().parent


def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def bits(S):return sum(1<<i for i in S)


def vertices(s):return tuple(i for i in range(s.bit_length()) if s>>i&1)


def orientation(P,a,b,c):
    x,y=P[a];u,v=P[b];w,z=P[c]
    return x*v+u*z+w*y-y*u-v*w-z*x


def hull(P,S):
    S=tuple(S)
    if len(S)<3:return S
    lower,upper=[],[]
    for seq,stack in ((S,lower),(S[::-1],upper)):
        for i in seq:
            while len(stack)>1 and orientation(P,stack[-2],stack[-1],i)<=0:stack.pop()
            stack.append(i)
    return tuple(lower[:-1]+upper[:-1])


def upwards(m,seeds):
    table=bytearray(1<<m)
    for s in seeds:table[s]=1
    for i in range(m):
        b=1<<i
        for base in range(0,1<<m,2*b):
            for j in range(b):table[base+b+j]|=table[base+j]
    return table


def geometry(P,n=7):
    m=len(P);V=tuple(range(m));full=(1<<m)-1
    assert m==15 and n==7
    assert all(len(p)==2 and all(type(z)is int for z in p) for p in P)
    assert all(P[i][0]<P[i+1][0] for i in range(m-1))
    dets={t:orientation(P,*t) for t in combinations(V,3)};assert all(dets.values())
    cap4=[q for q in combinations(V,4) if all(dets[t]<0 for t in combinations(q,3))]
    cap5=[q for q in combinations(V,5) if all(dets[t]<0 for t in combinations(q,3))]
    targets=[q for q in combinations(V,n-1) if len(hull(P,q))==n-1]
    ngons=[q for q in combinations(V,n) if len(hull(P,q))==n]
    assert not cap5 and not ngons
    ends={q[-2:] for q in cap4}
    bad=[t for t,d in dets.items() if d<0 and t[-2:] not in ends]
    nonconvex4=[q for q in combinations(V,4) if len(hull(P,q))<4]
    D=upwards(m,map(bits,bad));F=upwards(m,map(bits,cap4));T=upwards(m,map(bits,targets))
    nonconvex=upwards(m,map(bits,nonconvex4))
    for size in (6,7):
        for q in combinations(V,size):
            assert bool(not nonconvex[bits(q)])==(len(hull(P,q))==size)
    weak=[];terminal=[];failure_counts=Counter();by_size={}
    for s in range(full+1):
        assert D[s] or not F[s], 'no5cap implication failed'
        target_failure=T[full^s]
        if not F[s] and not target_failure:weak.append(s)
        if not D[s] and not target_failure:terminal.append(s)
        why='both' if D[s] and target_failure else 'bad_triple' if D[s] else 'missed_target' if target_failure else 'works'
        failure_counts[why]+=1
    assert not terminal
    rooted=[]
    for root in V:
        choices=[s for s in weak if s>>root&1]
        witness=min(choices,key=lambda s:(s.bit_count(),s)) if choices else None
        rooted.append({'root':root,'weak_delta':vertices(witness) if witness is not None else None,
                       'minimum_size':witness.bit_count() if witness is not None else None})
    maxcup=max(k for k in range(3,8) if any(all(dets[t]>0 for t in combinations(q,3)) for q in combinations(V,k)))
    report={'m':m,'n':n,'P':P,'minimum_absolute_determinant':min(map(abs,dets.values())),
            'four_caps':len(cap4),'five_caps':len(cap5),'bad_triples':len(bad),
            'convex_six_subsets':len(targets),'convex_seven_subsets':len(ngons),
            'maximum_cap_cup_convex':[4 if cap4 else 3,maxcup,6 if targets else None],
            'all_subsets_checked':full+1,'terminal_safe_deltas':len(terminal),
            'failure_reasons':dict(failure_counts),'weak_deltas':len(weak),
            'weak_delta_size_counts':dict(sorted(Counter(s.bit_count() for s in weak).items())),
            'rooted_weak_deltas':rooted,
            'signs':''.join('+' if d>0 else '-' for d in dets.values())}
    return report,{'signs':{bits(t):d>0 for t,d in dets.items()},'caps4':set(map(bits,cap4)),
                   'bad':set(map(bits,bad)),'targets':set(map(bits,targets)),
                   'D':D,'F':F,'T':T,'nonconvex':nonconvex}


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    parser=argparse.ArgumentParser();parser.add_argument('coordinates',type=Path);parser.add_argument('tag')
    a=parser.parse_args();start=time.monotonic()
    out={'label':'COMPUTED independent exact real-point replay','status':'IN_PROGRESS',
         'input':str(a.coordinates),'input_sha256':digest(a.coordinates),'script_sha256':digest(__file__)}
    try:
        raw=json.loads(a.coordinates.read_text());P=raw['P']
        result,_=geometry(P)
        abstract=json.loads((HERE/'data/gp.json').read_text())
        assert result['signs']==abstract['signs'],'coordinate signs differ from audited model'
        assert digest(a.coordinates)==out['input_sha256']
        out.update(status='PASS',result=result)
        with (HERE/f'data/{a.tag}.coordinates.json').open('x') as f:json.dump(raw,f,indent=2);f.write('\n')
    except BaseException:
        out.update(status='FAIL',error=traceback.format_exc());raise
    finally:
        out.update(seconds=time.monotonic()-start,max_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        with (HERE/f'data/{a.tag}.geometry.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
        short={k:v for k,v in out.items() if k!='result'}
        if 'result' in out:short['result']={k:v for k,v in out['result'].items() if k not in ('P','signs','rooted_weak_deltas')}
        print(json.dumps(short))


if __name__=='__main__':main()
