"""Exhaustive small-set geometry/hitting check; no finder/checker imports."""
import argparse
from fractions import Fraction as Q
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time


def turn(p, a, b, c):
    ax, ay = p[a]
    bx, by = p[b]
    cx, cy = p[c]
    return (bx-ax)*(cy-by)-(by-ay)*(cx-bx)


def hull(p, ids):
    lower=[]
    upper=[]
    for i in ids:
        while len(lower)>1 and turn(p,lower[-2],lower[-1],i)<=0:
            lower.pop()
        lower.append(i)
    for i in reversed(ids):
        while len(upper)>1 and turn(p,upper[-2],upper[-1],i)<=0:
            upper.pop()
        upper.append(i)
    return lower[:-1]+upper[:-1]


def stats(p, selected):
    assert all(turn(p,*t)!=0 for t in combinations(range(len(p)),3))
    best_cap=best_cup=best_gon=2
    blue_gon=selected_cap=0
    convex6=[]
    cap4_selected=[]
    selected=set(selected)
    for k in range(1,len(p)+1):
        for ids in combinations(range(len(p)),k):
            cap=all(turn(p,ids[i],ids[i+1],ids[i+2])<0 for i in range(k-2))
            cup=all(turn(p,ids[i],ids[i+1],ids[i+2])>0 for i in range(k-2))
            convex=k<3 or len(hull(p,ids))==k
            if cap:
                best_cap=max(best_cap,k)
            if cup:
                best_cup=max(best_cup,k)
            if convex:
                best_gon=max(best_gon,k)
            if convex and selected.isdisjoint(ids):
                blue_gon=max(blue_gon,k)
            if cap and set(ids)<=selected:
                selected_cap=max(selected_cap,k)
            if k==6 and convex:
                convex6.append(ids)
            if k==4 and cap and set(ids)<=selected:
                cap4_selected.append(ids)
    missed=[ids for ids in convex6 if selected.isdisjoint(ids)]
    return dict(max_cap=best_cap,max_cup=best_cup,max_gon=best_gon,
                selected=sorted(selected),selected_max_cap=selected_cap,
                complement_max_gon=blue_gon,targets6=convex6,
                missed_targets6=missed,selected_four_caps=cap4_selected,
                weak_delta=not cap4_selected and not missed)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('input',type=Path)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    assert not args.out.exists(), 'refuse to overwrite output'
    start=time.monotonic()
    data=json.loads(args.input.read_text())
    selected=data['target_cap_triple']
    safe=data['safe_two_supports']
    exposed=data['same_orientations_exposed']
    r=[Q(x) for x in data['exposed_insertion']]
    augmented=exposed+[r]
    results={
        'h5_old_A':stats(safe,selected),
        'h3_old_A':stats(exposed,selected),
        'h3_plus_r_A_unchanged':stats(augmented,selected),
        'h3_plus_r_A_plus_r':stats(augmented,selected+[8])}
    for result in results.values():
        assert (result['max_cap'],result['max_cup'],result['max_gon'])==(4,4,6)
        assert not result['missed_targets6']
        assert result['complement_max_gon']==4
    assert all(results[name]['weak_delta'] for name in ('h5_old_A','h3_old_A','h3_plus_r_A_unchanged'))
    assert not results['h3_plus_r_A_plus_r']['weak_delta']
    assert results['h3_plus_r_A_plus_r']['selected_four_caps']==[(0,3,6,8)]
    new_targets=[t for t in results['h3_plus_r_A_unchanged']['targets6'] if 8 in t]
    assert new_targets and all(set(t)&set(selected) for t in new_targets)
    output=dict(status='PASS',label='COMPUTED exact exhaustive subset/hull replay',
                input_sha256=hashlib.sha256(args.input.read_bytes()).hexdigest(),
                checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                results=results,new_targets6=new_targets,
                claim='A+r fails for this valid (5,7) insertion, but unchanged A remains a weak Delta; no monotone failure',
                elapsed_seconds=time.monotonic()-start,
                peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    args.out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='results'}))
    print(json.dumps({name:{k:v for k,v in result.items() if k!='targets6'} for name,result in results.items()}))


if __name__=='__main__':
    main()
