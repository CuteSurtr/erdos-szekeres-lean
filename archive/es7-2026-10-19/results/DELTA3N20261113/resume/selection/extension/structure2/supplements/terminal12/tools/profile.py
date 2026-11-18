"""Profile fixed structural candidates; deliberately no membership enumeration."""
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

HERE=Path(__file__).resolve().parents[1]
TRACK=HERE.parents[1]
sys.path.insert(0,str(TRACK/'tools'))
from verify_structure2 import signs_of, convex, maxgon, four_caps
from highsplit_controls import chain_ranks


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args();assert not args.out.exists();start=time.monotonic()
    source=TRACK.parent/'terminal12/data/3/points.txt'
    rows=[tuple(map(int,row.split())) for row in source.read_text().splitlines()]
    m,n=rows[0];p=rows[1:];assert m==len(p)==12 and n==6
    s=signs_of(p);ids=list(range(m));c4=four_caps(s,ids)
    beta=chain_ranks(s,ids,True);alpha=chain_ranks(s,ids,False)
    tails={t[-2:] for t in c4}
    bad=[t for t,v in s.items() if v<0 and t[-2:] not in tails]
    targets=[t for t in combinations(ids,n-1) if convex(p,t)]
    gon=maxgon(s,ids)
    assert (len(c4),len(bad),len(targets),max(alpha.values()),max(beta.values()),gon)==(14,44,134,4,5,5)
    cuts=[]
    for cut in range(1,m):
        mixed=[(t,v) for t,v in s.items() if t[0]<cut<=t[-1]]
        failures={}
        for name in ('high','low','all_cup'):
            def expected(t):
                if name=='all_cup':return 1
                high=1 if t[1]<cut else -1
                return high if name=='high' else -high
            failures[name]=next((dict(triple=t,determinant=v,expected_sign=expected(t))
                for t,v in mixed if (v>0)!=(expected(t)>0)),None)
        cuts.append(dict(cut=cut,left_maxcup=max(chain_ranks(s,ids[:cut],True).values()),
            right_maxcup=max(chain_ranks(s,ids[cut:],True).values()),failures=failures))
    candidates={}
    for k in (3,4,5):candidates[f'level_{k}']=[v for v in ids if beta[v]==k]
    candidates['levels_4_5']=[v for v in ids if beta[v]>=4]
    candidates['levels_3_4_5']=[v for v in ids if beta[v]>=3]
    profiles={}
    for name,A in candidates.items():
        aset=set(A);missed=[t for t in targets if not aset.intersection(t)]
        contained4=[t for t in c4 if aset.issuperset(t)]
        unprotected=[t for t in bad if aset.issuperset(t)]
        profiles[name]=dict(A=A,missed_target_count=len(missed),one_missed_target=missed[0] if missed else None,
             selected_fourcaps=contained4,selected_unprotected_cap_triples=unprotected,
             complement_maxgon=maxgon(s,[v for v in ids if v not in aset]),
             terminal_safe_delta=not(missed or contained4 or unprotected))
    out=dict(status='PASS',label='COMPUTED exact structural diagnostic',P=p,n=n,m=m,
        maxima=dict(cap=max(alpha.values()),cup=max(beta.values()),gon=gon),
        counts=dict(fourcaps=len(c4),terminal_bad_triples=len(bad),pentagons=len(targets)),
        beta=[beta[v] for v in ids],cuts=cuts,
        admitted_cuts={name:[r['cut'] for r in cuts if r['failures'][name] is None] for name in ('high','low','all_cup')},
        prescribed_rank_profiles=profiles,
        source_path=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        helpers={name:hashlib.sha256((TRACK/'tools'/name).read_bytes()).hexdigest()
                 for name in ('verify_structure2.py','highsplit_controls.py')},
        elapsed_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='No membership-model enumeration, fresh certificate replay, global minimality claim, or uniform-selection test.')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('P','cuts','helpers')}))


if __name__=='__main__':main()
