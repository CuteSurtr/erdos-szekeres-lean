"""Exact fixed controls for all-mixed-cup cuts; no selection search."""
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import time
import traceback
from verify_structure2 import determinant, signs_of, maxgon, convex
from highsplit_controls import chain_ranks, caps4, verify_selection


def cup_join(left,right):
    first=left[-1][0]+1;dx=first-right[0][0];cut=len(left)
    p=list(left)+[(x+dx,y) for x,y in right];height=0
    for a,b in combinations(range(cut),2):
        for c in range(cut,len(p)):
            height=max(height,(-determinant(p,a,b,c))//(p[b][0]-p[a][0])+1)
    p=list(left)+[(x+dx,y+height) for x,y in right];tilt=0
    for a in range(cut):
        for b,c in combinations(range(cut,len(p)),2):
            coefficient=(p[c][0]-p[b][0])*(first-p[a][0])
            tilt=max(tilt,(-determinant(p,a,b,c))//coefficient+1)
    return p[:cut]+[(x,y+tilt*(x-first)) for x,y in p[cut:]]


def cup(k):return [(i,i*i) for i in range(k)]
def cap(k):return [(i,-i*i) for i in range(k)]


def check(left,right,n,conditional_A=None):
    p=cup_join(left,right);cut=len(left);ids=list(range(len(p)));L=ids[:cut];R=ids[cut:]
    s=signs_of(p);assert all(value>0 for (a,b,c),value in s.items() if a<cut<=c)
    bl=chain_ranks(s,L,True);br=chain_ranks(s,R,True);beta=chain_ranks(s,ids,True)
    cL=max(bl.values());cR=max(br.values());assert max(beta.values())==cL+cR<=n-1
    assert max(chain_ranks(s,ids,False).values())<=4 and maxgon(s,ids)<n
    if conditional_A is None:
        assert max(cL,cR)<=n-3
        A=[v for v in L if bl[v]==cL]+[v for v in R if br[v]==cR]
    else:A=conditional_A
    selection=verify_selection(s,ids,A,n,caps4(s,ids))
    if len(p)<=12:
        assert all(set(A).intersection(t) for t in combinations(ids,n-1) if convex(p,t))
        assert not any(convex(p,t) for t in combinations(ids,n))
    return dict(status='PASS',P=p,n=n,m=len(p),cut=cut,cup_left=cL,cup_right=cR,
                maxgon=maxgon(s,ids),selection=selection)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();root=Path(__file__).resolve().parents[1]
    start=time.monotonic();out=dict(cases={})
    try:
        out['cases']['n5_two_fourcaps']=check(cap(4),cap(4),5)
        out['cases']['n6_interior']=check(cap(4),cup(3),6)
        out['cases']['n8_interior']=check(cap(4),cup(5),8)
        old=json.loads((root/'data/separator_c3.json').read_text());p=old['P'];A=old['A']
        out['cases']['n7_right_singleton']=check(p,[(0,0)],7,A+[len(p)])
        out['cases']['n7_left_singleton']=check([(0,0)],p,7,[0]+[a+1 for a in A])
        out['status']='PASS'
    except Exception:out.update(status='FAIL',traceback=traceback.format_exc());raise
    finally:
        out['elapsed_seconds']=time.monotonic()-start
        out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        out['helper_sha256']={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                              for name in ('highsplit_controls.py','verify_structure2.py')}
        args.out.write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps({name:dict(n=r['n'],m=r['m'],cut=r['cut'],cL=r['cup_left'],cR=r['cup_right'],
              A=r['selection']['A'],cap_triples=len(r['selection']['selected_cap_triples']))
              for name,r in out['cases'].items()}))
        print(json.dumps({k:v for k,v in out.items() if k not in ('cases','helper_sha256')}))


if __name__=='__main__':main()
