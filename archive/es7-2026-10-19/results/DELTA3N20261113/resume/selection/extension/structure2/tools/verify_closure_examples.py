"""Separate exact replay of the closure9 and rank-four-cap examples.

Imports the separate determinant/triangle-containment checker, not the
closure finder, graph comparison code, or profile generator.
"""
from fractions import Fraction
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback
from verify_structure2 import (signs_of, convex, ranks_by_subsets, four_caps,
                               line, serial)


def cup(s,vertices):
    return all(s[t]>0 for t in combinations(sorted(set(vertices)),3))


def replay(root,result):
    p=[(-1,-3),(0,0),(10,0),(12,-20),(16,-2),(20,13),(30,1),(40,40),(50,100)]
    idx=list(range(len(p)));s=signs_of(p)
    beta=ranks_by_subsets(s,idx);caps=four_caps(s,idx)
    expected_caps=[(0,1,2,3),(0,1,2,4),(0,1,5,6),(3,4,5,6),(3,4,5,7),(3,4,5,8)]
    assert caps==expected_caps and max(beta.values())==5
    hexagons=[t for t in combinations(idx,6) if convex(p,t)]
    assert hexagons==[(0,1,2,5,7,8),(0,1,3,6,7,8),(0,1,4,6,7,8),(3,4,5,6,7,8)]
    seven=[t for t in combinations(idx,7) if convex(p,t)]
    assert not seven
    ends=sorted({t[-2:] for t in caps});q=(1,6)
    eligible=[ab for ab in ends if ab[0]>=q[0] and ab[1]>=q[1]]
    assert eligible==[(5,6),(5,7),(5,8)] and q not in ends
    assert all(not cup(s,q+ab) for ab in eligible)
    assert s[1,5,6]==-370 and s[0,1,6]<0
    paths=[[(1,6),(2,7),(5,8)],[(1,6),(1,8),(5,8)]]
    path_data=[]
    for path in paths:
        comparisons=[]
        for a,b in zip(path,path[1:]):
            assert a[0]<=b[0] and a[1]<=b[1] and cup(s,a+b)
            l,r=line(p,*a),line(p,*b)
            assert l[0]<=r[0] and l[1]<=r[1]
            comparisons.append(dict(earlier=a,later=b,union=sorted(set(a+b)),
                                    earlier_line=l,later_line=r))
        path_data.append(comparisons)
    assert line(p,1,6)==(Fraction(1,30),Fraction(5,3))
    assert line(p,2,7)==(Fraction(4,3),Fraction(160,3))
    assert line(p,5,8)==(Fraction(29,10),Fraction(100))
    A={0,1,6};assert all(A.intersection(h) for h in hexagons)
    assert all(7 in h for h in hexagons)
    result['closure9']=dict(status='PASS',P=p,beta=[beta[i] for i in idx],
       maxcap=4,maxcup=5,maxgon=6,four_caps=caps,hexagons=hexagons,
       seven_gons=seven,eligible_direct_end_pairs=eligible,negative_det=s[1,5,6],
       paths=path_data,A=sorted(A),alternative_singleton=[7],
       scope='Specified weak Delta separates the protection criteria; global existence does not.')

    path=root/'data/initial_profiles.json';r=json.loads(path.read_text())['fixtures']['terminal18']
    p=r['P'];idx=list(range(len(p)));s=signs_of(p)
    beta=ranks_by_subsets(s,idx);caps=four_caps(s,idx);ends=sorted({t[-2:] for t in caps})
    C=(3,4,8,10);assert C in caps and [beta[v] for v in C]==[4,5,5,4]
    certs=[]
    for t in combinations(C,3):
        b,c=t[-2:]
        u,v=next(ab for ab in ends if ab[0]>=b and ab[1]>=c and cup(s,(b,c)+ab))
        cap=next(cap for cap in caps if cap[-2:]==(u,v))
        q,r=line(p,b,c),line(p,u,v)
        assert r[0]>=q[0] and r[1]>=q[1]
        union=sorted({b,c,u,v})
        certs.append(dict(cap_triple=t,ambient_cap=cap,cup_union=union,
           union_determinants={str(tri):s[tri] for tri in combinations(union,3)},
           target_line=q,ambient_line=r))
    result['protected_fourcap_in_top_two']=dict(status='PASS',cap=C,
       ranks=[beta[v] for v in C],certificates=certs,
       input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
       scope='Four-cap avoidance is not implied by cup-protection, even on L4 union L5.')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args();assert not args.out.exists()
    root=Path(__file__).resolve().parents[1];start=time.monotonic();result={}
    try:
        replay(root,result);result['status']='PASS'
    except Exception:
        result['status']='FAIL';result['traceback']=traceback.format_exc();raise
    finally:
        result['elapsed_seconds']=time.monotonic()-start
        result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        helper=Path(__file__).with_name('verify_structure2.py')
        result['helper_sha256']=hashlib.sha256(helper.read_bytes()).hexdigest()
        args.out.write_text(json.dumps(serial(result),indent=2)+'\n')
        print(json.dumps(serial(result)))


if __name__=='__main__':main()
