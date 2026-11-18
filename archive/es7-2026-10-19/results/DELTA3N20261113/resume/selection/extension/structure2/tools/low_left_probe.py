"""Bounded exact low-split left-block test; no generic selector CNF."""
from collections import Counter
from itertools import combinations, product
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback
from verify_structure2 import determinant, convex, maxgon, serial


def mask(ids):return sum(1<<v for v in ids)


def analyze(p,n):
    ids=list(range(len(p)));s={t:determinant(p,*t) for t in combinations(ids,3)}
    if not all(s.values()):return None
    caps=[t for t in combinations(ids,3) if s[t]<0]
    if any(all(s[t]<0 for t in combinations(q,3)) for q in combinations(ids,4)):return None
    if maxgon(s,ids)>=n:return None
    beta=[1]*len(p);alpha=[1 if i==0 else 2 for i in ids]
    for t in caps:alpha[t[-1]]=3
    cup_masks=[]
    for bits in range(1<<len(p)):
        a=[v for v in ids if bits>>v&1]
        if any(bits&mask(t)==mask(t) for t in caps):continue
        cup_masks.append(bits)
        if a:beta[a[-1]]=max(beta[a[-1]],len(a))
    if max(beta)!=n-1:return None
    H=[t for t in combinations(ids,n-1) if convex(p,t)];hm=[mask(t) for t in H];cm=[mask(t) for t in caps]
    hit=lambda a:all(a&h for h in hm)
    kindI=[];kindII=[]
    for bits in cup_masks:
        if not hit(bits):continue
        a=[v for v in ids if bits>>v&1]
        if all(bits&c for c in cm):kindI.append(a)
        if all(alpha[v]==3 for v in a[1:]):kindII.append(a)
    previous=[v for v in ids if beta[v]==n-2];top=[v for v in ids if beta[v]==n-1]
    union=sorted(previous+top);um=mask(union)
    return dict(P=p,n=n,m=len(p),maxcup=n-1,beta=beta,alpha=alpha,
        cap_triples=caps,targets=H,kindI_count=len(kindI),kindII_count=len(kindII),
        kindI_witness=min(kindI,key=lambda a:(len(a),a)) if kindI else None,
        kindII_witness=min(kindII,key=lambda a:(len(a),a)) if kindII else None,
        level_previous=previous,level_top=top,previous_hits=hit(mask(previous)),top_hits=hit(mask(top)),
        union_cap=next((t for t in caps if um&mask(t)==mask(t)),None),
        neither_level_hits=not hit(mask(previous)) and not hit(mask(top)))


def grid():
    counts=Counter();examples={};start=time.monotonic()
    # The explicit six-point cup-join control is outside the small-height grid.
    p=[(0,0),(1,-1),(2,-4),(3,0),(4,9),(5,16)]
    control=analyze(p,5);assert control and not control['previous_hits'] and control['union_cap']
    for m in range(2,8):
        for ys in product(range(-3,4),repeat=m-2):
            if time.monotonic()-start>15:
                return dict(status='PARTIAL_TIME_BOUND',counts=dict(counts),examples=examples,explicit_control=control)
            counts['attempted']+=1;p=list(enumerate((0,0)+ys));r=analyze(p,5)
            if r is None:continue
            counts['remaining_branch_sets']+=1
            for key in ('previous_hits','top_hits','neither_level_hits'):
                if r[key]:counts[key]+=1
            if r['union_cap']:counts['top_two_union_has_cap']+=1
            if not r['kindI_count']:counts['kindI_failures']+=1;examples.setdefault('kindI_failure',r)
            if not r['kindII_count']:counts['kindII_failures']+=1;examples.setdefault('kindII_failure',r)
            if not r['kindI_count'] and not r['kindII_count']:
                counts['terminal_obstructions']+=1;examples.setdefault('terminal_obstruction',r)
            if r['neither_level_hits']:examples.setdefault('neither_level_hits',r)
    return dict(status='PASS_COMPLETE_GRID',counts=dict(counts),examples=examples,explicit_control=control,
        scope='n5 left blocks only; x_i=i,y0=y1=0,other y_i in [-3,3],m2..7; positive controls are not a theorem')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();start=time.monotonic();r={}
    try:r=grid()
    except Exception:r.update(status='FAIL',traceback=traceback.format_exc());raise
    finally:
        r['elapsed_seconds']=time.monotonic()-start
        r['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        r['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        r['helper_sha256']=hashlib.sha256(Path(__file__).with_name('verify_structure2.py').read_bytes()).hexdigest()
        args.out.write_text(json.dumps(serial(r),indent=2)+'\n')
        print(json.dumps(serial(r)))


if __name__=='__main__':main()
