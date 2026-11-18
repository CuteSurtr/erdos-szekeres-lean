#!/usr/bin/env python3
"""Bounded coordinate-subset finder; no parent checker imports."""
import argparse
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback

HERE=Path(__file__).resolve().parent
DATA=HERE/'data'
SCRATCH=Path('/home/jay/research/data/delta3-codex-20261113/extension/cardinality')


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def det(P,a,b,c):
    x,y=P[a];u,v=P[b];w,z=P[c]
    return (u-x)*(z-y)-(v-y)*(w-x)


def bitmask(S):
    return sum(1<<i for i in S)


def convex(P,S):
    # Four-subset convexity criterion, independent of the replay's hull code.
    for a,b,c,d in combinations(S,4):
        x,y,z,w=(det(P,*t)>0 for t in ((a,b,c),(a,b,d),(a,c,d),(b,c,d)))
        if x!=y or z!=w:
            return False
    return True


def contains_table(m,witnesses):
    out=bytearray(1<<m)
    for s in witnesses:out[s]=1
    for i in range(m):
        b=1<<i
        for base in range(0,1<<m,b*2):
            for off in range(b):out[base+b+off]|=out[base+off]
    return out


def search(P,name,source,seconds):
    P=sorted(P);m=len(P)
    assert 11<=m<=20 and all(type(z)is int for p in P for z in p)
    assert all(P[i][0]<P[i+1][0] for i in range(m-1))
    assert all(det(P,*t) for t in combinations(range(m),3))
    start=time.monotonic()
    targets=[bitmask(t) for t in combinations(range(m),6) if convex(P,t)]
    forbidden5=[bitmask(t) for t in combinations(range(m),5)
                if all(det(P,*r)<0 for r in combinations(t,3))]
    forbidden7=[bitmask(t) for t in combinations(range(m),7) if convex(P,t)]
    caps4=[t for t in combinations(range(m),4) if all(det(P,*r)<0 for r in combinations(t,3))]
    target_inside=contains_table(m,targets)
    invalid_inside=contains_table(m,forbidden5+forbidden7)
    trace=SCRATCH/f'{name}.tries.tsv'
    count=valid=pairfail=triplefail=0
    candidate=None;exhausted=True
    with trace.open('x') as log:
        log.write('# subset_mask disposition witness_pair_mask\n')
        for S in combinations(range(m),11):
            if time.monotonic()-start>seconds:
                exhausted=False;break
            s=bitmask(S);count+=1
            if invalid_inside[s]:
                log.write(f'{s} invalid 0\n');continue
            valid+=1
            for pair in combinations(S,2):
                q=bitmask(pair)
                if not target_inside[s^q]:
                    pairfail+=1;log.write(f'{s} pair-hits {q}\n');break
            else:
                ends={q[-2:] for q in caps4 if bitmask(q)&s==bitmask(q)}
                for A in combinations(S,3):
                    a=bitmask(A)
                    if target_inside[s^a]:continue
                    if det(P,*A)<0 and A[-2:] not in ends:continue
                    candidate={'P':[P[i] for i in S],'n':7,'m':11,
                               'terminal_delta':[S.index(i) for i in A],
                               'source':source,'source_indices':list(S),
                               'source_point_count':m,'finder_source_sha256':digest(__file__)}
                    log.write(f'{s} FOUND {a}\n');break
                if candidate:break
                triplefail+=1;log.write(f'{s} no-terminal-triple 0\n')
    report={'status':'FOUND' if candidate else ('EXHAUSTED' if exhausted else 'BOUNDED_STOP'),
            'name':name,'input_m':m,'subsets_examined':count,'valid_subsets':valid,
            'pair_hitting_obstructions':pairfail,'no_terminal_triple':triplefail,
            'source':source,'seconds':time.monotonic()-start,'trace':str(trace),
            'trace_sha256':digest(trace),'targets_in_source':len(targets),
            'fivecaps_in_source':len(forbidden5),'sevengons_in_source':len(forbidden7)}
    if candidate:
        with (DATA/f'{name}.candidate.json').open('x') as f:
            json.dump(candidate,f,indent=2);f.write('\n')
    return report


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    ap=argparse.ArgumentParser()
    ap.add_argument('source',type=Path);ap.add_argument('name')
    ap.add_argument('--index',type=int);ap.add_argument('--seconds',type=float,default=12)
    args=ap.parse_args()
    DATA.mkdir(exist_ok=True);SCRATCH.mkdir(parents=True,exist_ok=True)
    source={'path':str(args.source),'sha256':digest(args.source),'index':args.index}
    out={'label':'COMPUTED','finder_sha256':digest(__file__),'status':'IN_PROGRESS'}
    try:
        raw=json.loads(args.source.read_text())
        if args.index is not None:raw=raw[args.index]
        P=raw.get('P',raw.get('points'))
        out.update(search(P,args.name,source,args.seconds))
    except BaseException:
        out.update(status='FAILED',error=traceback.format_exc());raise
    finally:
        out['max_rss_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        with (DATA/f'{args.name}.search.json').open('x') as f:
            json.dump(out,f,indent=2);f.write('\n')
        print(json.dumps(out))


if __name__=='__main__':main()
