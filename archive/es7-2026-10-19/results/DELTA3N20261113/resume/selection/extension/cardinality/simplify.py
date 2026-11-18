#!/usr/bin/env python3
"""Exact bounded integer-coordinate simplification preserving all signs."""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time

HERE=Path(__file__).resolve().parent
DATA=HERE/'data'


def orient(P,a,b,c):
    x,y=P[a];u,v=P[b];w,z=P[c]
    return (u-x)*(z-y)-(v-y)*(w-x)


def rounded(a,b):
    return (2*a+b)//(2*b)


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    start=time.monotonic()
    source=DATA/'sat11.candidate.json';raw=json.loads(source.read_text());original=raw['P']
    triples=list(combinations(range(11),3));signs=[1 if c=='+' else -1 for c in raw['signs']]
    bound=max(abs(y) for x,y in original);failed=[];P=None
    for amplitude in range(1,10001):
        Q=[[x,rounded(y*amplitude,bound)] for x,y in original]
        bad=next((i for i,(t,s) in enumerate(zip(triples,signs)) if s*orient(Q,*t)<=0),None)
        if bad is None:
            P=Q;break
        failed.append({'amplitude':amplitude,'first_failed_triple':triples[bad]})
    assert P is not None
    initial=[p[:] for p in P];moves=[]
    # Exact integer admissible intervals for changing one coordinate.
    def interval(index,axis):
        lo,hi=-10**12,10**12
        if axis==0:
            lo=P[index-1][0]+1 if index else 0
            hi=P[index+1][0]-1 if index<10 else P[index][0]
        old=P[index][axis]
        for t,s in zip(triples,signs):
            if index not in t:continue
            P[index][axis]=0;b=s*orient(P,*t)
            P[index][axis]=1;a=s*orient(P,*t)-b
            if a>0:lo=max(lo,-((b-1)//a))
            elif a<0:hi=min(hi,(1-b)//a)
            else:assert b>=1
        P[index][axis]=old
        assert lo<=old<=hi
        return lo,hi
    for roundno in range(200):
        changed=False
        for axis in (0,1):
            for i in range(10,-1,-1):
                lo,hi=interval(i,axis)
                target=max(lo,min(0,hi))
                old=P[i][axis]
                if abs(target)<abs(old):
                    moves.append({'round':roundno,'index':i,'axis':axis,'old':old,'new':target,'interval':[lo,hi]})
                    P[i][axis]=target;changed=True
        if not changed:break
        if time.monotonic()-start>12:break
    assert all(s*orient(P,*t)>0 for t,s in zip(triples,signs))
    candidate={**raw,'P':P,'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
               'finder':'Exact rounding and single-coordinate interval compression',
               'minimum_absolute_determinant':min(abs(orient(P,*t)) for t in triples)}
    for key in ('trial','rational_denominator_bound'):candidate.pop(key,None)
    with (DATA/'simple11.candidate.json').open('x') as f:json.dump(candidate,f,indent=2);f.write('\n')
    report={'label':'COMPUTED exact sign preservation','status':'PASS',
            'first_successful_amplitude':amplitude,'failed_roundings':failed,'rounded_points':initial,
            'moves':moves,'final_points':P,'seconds':time.monotonic()-start,
            'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with (DATA/'simplify.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps({k:report[k] for k in ('status','first_successful_amplitude','final_points','seconds','max_rss_KiB')}))


if __name__=='__main__':main()
