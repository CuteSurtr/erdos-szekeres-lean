"""Full exact low-split controls: prescribed endpoint and conditional cup selectors."""
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback
from highsplit_controls import join, chain_ranks, caps4, verify_selection
from separator_controls import extremal
from verify_structure2 import signs_of, convex, maxgon


def low_join(left,right):
    return [(x,-y) for x,y in join([(x,-y) for x,y in left],[(x,-y) for x,y in right])]


def cup(k):return [(i,i*i) for i in range(k)]


def check(left,right,n,B=None):
    p=low_join(left,right);cut=len(left);L=list(range(cut));R=list(range(cut,len(p)));ids=L+R
    s=signs_of(p)
    assert all(v<0 if b<cut<=c else v>0 if a<cut<=b else True for (a,b,c),v in s.items())
    alpha=chain_ranks(s,ids,False);beta=chain_ranks(s,ids,True)
    assert max(alpha.values())<=4 and maxgon(s,ids)<n
    al=chain_ranks(s,L,False);bl=chain_ranks(s,L,True);br=chain_ranks(s,R,True)
    d=max(br.values());assert d<=n-4 and max(al.values())<=3
    H=[h for h in combinations(L,n-1) if convex(p,h)]
    conditional=B is not None
    if B is None:
        assert max(bl.values())<=n-2
        B=sorted({h[-1] for h in H})
        assert all(al[v]==3 for v in B)
        assert len(B)<=n-3
    assert all(s[t]>0 for t in combinations(B,3))
    assert all(set(B).intersection(h) for h in H)
    assert all(al[v]==3 for v in B[1:])
    C=[v for v in R if br[v]==d] if d==n-4 else []
    A=B+C;ambient=caps4(s,ids)
    selection=verify_selection(s,ids,A,n,ambient)
    mixed=[t for t in selection['selected_cap_triples'] if t[0]<cut<=t[-1]]
    assert all(t[1]<cut and al[t[1]]==3 for t in mixed)
    if len(p)<=10:
        assert all(set(A).intersection(h) for h in combinations(ids,n-1) if convex(p,h))
        assert not any(convex(p,h) for h in combinations(ids,n))
    return dict(status='PASS',P=p,n=n,m=len(p),cut=cut,d=d,maxcup_left=max(bl.values()),
         maxima=dict(cap=max(alpha.values()),cup=max(beta.values()),gon=maxgon(s,ids)),
         B=B,C=C,selection=selection,internal_left_targets=len(H),
         mixed_selected_cap_triples=mixed,conditional_left_cup=conditional)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();root=Path(__file__).resolve().parents[1]
    start=time.monotonic();out=dict(cases={})
    try:
        for n in (5,6,7,8):
            # Small nonvacuous no-(n-1)-cup left target, upper cap three.
            k=n-2;left=[(i,(k+3)**3 if i==k//2 else i*i) for i in range(k+1)]
            right=cup(n-4)
            out['cases'][f'n{n}_endpoint_small']=check(left,right,n)
        left=extremal(5,3)
        out['cases']['n7_endpoint_R3cup']=check(left,cup(3),7)
        out['cases']['n7_endpoint_R_with_caps']=check(left,extremal(3,4),7)
        out['cases']['n7_no_mixed_targets']=check(left,extremal(2,4),7)
        for i in range(1,5):
            row=json.loads((root/f'data/low_n7_fixed_{i}.json').read_text())['result']
            assert row['kindII_count']>0
            out['cases'][f'n7_longcup_fixed_{i}']=check(row['P'],cup(3),7,B=row['kindII_witness'])
        out['status']='PASS'
    except Exception:out.update(status='FAIL',traceback=traceback.format_exc());raise
    finally:
        out['elapsed_seconds']=time.monotonic()-start
        out['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        out['helper_sha256']={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                              for name in ('highsplit_controls.py','separator_controls.py','verify_structure2.py')}
        args.out.write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps({name:dict(n=r['n'],m=r['m'],d=r['d'],maxcup_left=r['maxcup_left'],
              maxima=r['maxima'],B=r['B'],C=r['C'],left_targets=r['internal_left_targets'],
              cap_triples=len(r['selection']['selected_cap_triples']),
              mixed_cap_triples=len(r['mixed_selected_cap_triples'])) for name,r in out['cases'].items()}))
        print(json.dumps({k:v for k,v in out.items() if k not in ('cases','helper_sha256')}))


if __name__=='__main__':main()
