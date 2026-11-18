#!/usr/bin/env python3
"""Independent exact replay: no finder/LP/earlier checker imports."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time
import traceback

HERE=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def orientation(P,a,b,c):
    x,y=P[a];u,v=P[b];w,z=P[c]
    return x*v+u*z+w*y-y*u-v*w-z*x


def convex_hull(P,S):
    ordered=sorted(S,key=lambda i:P[i])
    if len(ordered)<3:return ordered
    lower,upper=[],[]
    for order,chain in ((ordered,lower),(ordered[::-1],upper)):
        for i in order:
            while len(chain)>=2 and orientation(P,chain[-2],chain[-1],i)<=0:
                chain.pop()
            chain.append(i)
    return lower[:-1]+upper[:-1]


def contains(S,T):return set(T).issubset(S)


def check(record):
    P=record['P'];m=len(P);A=tuple(record['terminal_delta'])
    assert m==11 and record['n']==7
    assert all(len(p)==2 and all(type(z)is int for z in p) for p in P)
    assert all(P[i][0]<P[i+1][0] for i in range(m-1))
    signs={t:orientation(P,*t) for t in combinations(range(m),3)}
    assert all(signs.values())
    if 'signs' in record:
        assert record['signs']==''.join('+' if d>0 else '-' for d in signs.values())
    cap4=[q for q in combinations(range(m),4) if all(signs[t]<0 for t in combinations(q,3))]
    cap5=[q for q in combinations(range(m),5) if all(signs[t]<0 for t in combinations(q,3))]
    targets=[q for q in combinations(range(m),6) if len(convex_hull(P,q))==6]
    ngons=[q for q in combinations(range(m),7) if len(convex_hull(P,q))==7]
    assert not cap5 and not ngons
    assert len(A)==3 and len(set(A))==3 and tuple(sorted(A))==A
    assert all(set(A)&set(q) for q in targets)
    terminal_witnesses=[]
    for t in combinations(A,3):
        if signs[t]<0:
            q=next(q for q in cap4 if q[-2:]==t[-2:])
            terminal_witnesses.append({'triple':t,'fourcap':q})
    pair_witnesses=[]
    for pair in combinations(range(m),2):
        q=next(q for q in targets if not set(pair)&set(q))
        pair_witnesses.append({'pair':pair,'disjoint_convex_six':q})
    allpairs=set(combinations(range(m),2));uncovered=allpairs.copy();cover=[]
    while uncovered:
        q=max(targets,key=lambda q:len(uncovered & set(combinations([i for i in range(m) if i not in q],2))))
        complement=[i for i in range(m) if i not in q]
        hits=uncovered & set(combinations(complement,2));assert hits
        cover.append({'convex_six':q,'complement':complement})
        uncovered-=hits
    # Remove any redundant selected certificate rows without a minimality claim.
    for i in range(len(cover)-1,-1,-1):
        rest=cover[:i]+cover[i+1:]
        if set().union(*(set(combinations(r['complement'],2)) for r in rest))==allpairs:
            cover=rest
    bad=[t for t,d in signs.items() if d<0 and not any(q[-2:]==t[-2:] for q in cap4)]
    weak_sizes,terminal_sizes=Counter(),Counter()
    for size in range(m+1):
        for S in combinations(range(m),size):
            if any(contains(S,q) for q in cap4) or any(not set(S)&set(q) for q in targets):continue
            weak_sizes[size]+=1
            if not any(contains(S,t) for t in bad):terminal_sizes[size]+=1
    assert min(weak_sizes)==3 and min(terminal_sizes)==3
    maxcap=max(k for k in range(3,6) if any(all(signs[t]<0 for t in combinations(q,3)) for q in combinations(range(m),k)))
    maxcup=max(k for k in range(3,8) if any(all(signs[t]>0 for t in combinations(q,3)) for q in combinations(range(m),k)))
    maxgon=max(k for k in range(3,8) if any(len(convex_hull(P,q))==k for q in combinations(range(m),k)))
    return {'m':m,'n':7,'P':P,'minimum_absolute_determinant':min(map(abs,signs.values())),
            'caps4':len(cap4),'caps5':len(cap5),'convex6':len(targets),'convex7':len(ngons),
            'maximum_cap_cup_convex':[maxcap,maxcup,maxgon],
            'terminal_delta':A,'terminal_delta_is_cup':signs[A]>0,'terminal_pair_witnesses':terminal_witnesses,
            'pair_obstructions':pair_witnesses,'small_cover_of_pair_obstructions':cover,
            'weak_delta_size_counts':dict(sorted(weak_sizes.items())),
            'terminal_delta_size_counts':dict(sorted(terminal_sizes.items())),
            'all_subsets_checked':2**m,'minimum_weak_size':3,'minimum_terminal_size':3,
            'all_convex_six_subsets':targets,'all_four_caps':cap4}


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('tag')
    args=ap.parse_args();start=time.monotonic()
    out={'label':'COMPUTED exact independent replay','status':'IN_PROGRESS',
         'input':str(args.candidate),'input_sha256':sha(args.candidate),'checker_sha256':sha(Path(__file__))}
    try:
        out.update(status='PASS',result=check(json.loads(args.candidate.read_text())))
    except BaseException:
        out.update(status='FAIL',error=traceback.format_exc());raise
    finally:
        out.update(seconds=time.monotonic()-start,max_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        with (HERE/f'data/{args.tag}.verify.json').open('x') as f:
            json.dump(out,f,indent=2);f.write('\n')
        print(json.dumps({k:v for k,v in out.items() if k!='result'}))


if __name__=='__main__':main()
