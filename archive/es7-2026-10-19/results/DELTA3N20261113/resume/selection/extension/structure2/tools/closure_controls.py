"""Compare actual cup-union reachability with the proved two-triangle test."""
from collections import Counter
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import random
import resource
import time
import traceback


def orient(p,a,b,c):
    return ((p[b][0]-p[a][0])*(p[c][1]-p[a][1])
            -(p[b][1]-p[a][1])*(p[c][0]-p[a][0]))


def analyze(p,details=True):
    n=len(p);signs={t:orient(p,*t) for t in combinations(range(n),3)}
    assert all(signs.values())
    pairs=list(combinations(range(n),2));index={q:i for i,q in enumerate(pairs)}
    adjacent=[];two_triangles=[]
    for i,(b,c) in enumerate(pairs):
        one=flat=0
        for j,(u,v) in enumerate(pairs):
            if b>u or c>v:continue
            if (c==v or signs[b,c,v]>0) and (b==u or signs[b,u,v]>0):flat|=1<<j
            if i!=j and all(signs[t]>0 for t in combinations(sorted({b,c,u,v}),3)):one|=1<<j
        adjacent.append(one);two_triangles.append(flat)
    reachable=[1<<i for i in range(len(pairs))]
    for i in reversed(range(len(pairs))):
        edges=adjacent[i]
        while edges:
            bit=edges&-edges;j=bit.bit_length()-1;assert j>i
            reachable[i]|=reachable[j];edges-=bit
    assert reachable==two_triangles
    if not details:return dict(m=n,pairs=len(pairs),relation_tests=len(pairs)**2)
    caps=[t for t in combinations(range(n),4) if all(signs[s]<0 for s in combinations(t,3))]
    ends={t[-2:] for t in caps};endmask=sum(1<<index[q] for q in ends)
    direct={q for i,q in enumerate(pairs) if (adjacent[i]|1<<i)&endmask}
    closure={q for i,q in enumerate(pairs) if reachable[i]&endmask}
    assert direct<=closure
    for i,q in enumerate(pairs):
        if q not in closure:
            assert all(r not in closure for j,r in enumerate(pairs) if reachable[i]>>j&1)
    beta=[1]*n;edge_rank={}
    for c in range(n):
        for b in range(c):
            edge_rank[b,c]=max([2]+[edge_rank[a,b]+1 for a in range(b) if signs[a,b,c]>0])
            beta[c]=max(beta[c],edge_rank[b,c])
    triples=[t for t,v in signs.items() if v<0]
    extra=[t for t in triples if t[-2:] in closure and t[-2:] not in direct]
    unprotected=[t for t in triples if t[-2:] not in closure]
    assert all(beta[a]<beta[b] for a,b,c in unprotected)
    certificates={}
    for t in extra:
        b,c=t[-2:]
        u,v=next(r for r in sorted(ends) if two_triangles[index[b,c]]>>index[r]&1)
        certificates[str(t)]=dict(target=[b,c],middle=[b,v],ambient_pair=[u,v],
                                  ambient_cap=next(cap for cap in caps if cap[-2:]==(u,v)))
    return dict(m=n,P=p,beta=beta,maxcup=max(beta),four_caps=caps,ambient_pairs=sorted(ends),
                direct_covered_pairs=sorted(direct),closure_covered_pairs=sorted(closure),
                extra_cap_triples=extra,extra_rank_patterns=dict(Counter(str(tuple(beta[i] for i in t)) for t in extra)),
                extra_top_two_triples=[t for t in extra if all(beta[i]>=4 for i in t)],
                unprotected_cap_triples=unprotected,certificates=certificates,
                relation_tests=len(pairs)**2,closure_equals_two_triangles=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();assert not args.out.exists()
    root=Path(__file__).resolve().parents[1];start=time.monotonic();output={}
    try:
        initial=json.loads((root/'data/initial_profiles.json').read_text())['fixtures']
        fixtures={name:r['P'] for name,r in initial.items()}
        fixtures['closure9']=json.loads((root/'data/closure_first_probe.json').read_text())['P']
        for case in ('c2','c3','c4'):
            fixtures['separator_'+case]=json.loads((root/'data'/('separator_'+case+'.json')).read_text())['P']
        fixtures['user_nontransitive6']=[(0,0),(10,0),(20,13),(30,1),(40,40),(50,100)]
        frozen=root.parent/'theory/data/examples.json'
        fixtures['two_support8']=json.loads(frozen.read_text())['safe_two_supports']
        output['fixtures']={}
        for name,p in fixtures.items():
            r=analyze(p);output['fixtures'][name]=r
            print(json.dumps(dict(name=name,m=r['m'],direct_pairs=len(r['direct_covered_pairs']),
                closure_pairs=len(r['closure_covered_pairs']),extra_triples=len(r['extra_cap_triples']),
                extra_rank_patterns=r['extra_rank_patterns'],extra_top_two=r['extra_top_two_triples'])),flush=True)
        assert [3,6] not in output['fixtures']['two_support8']['closure_covered_pairs']
        # The list is tuple-valued before JSON conversion.
        assert (3,6) not in output['fixtures']['two_support8']['closure_covered_pairs']
        rng=random.Random(710526);controls=[]
        for n in range(3,9):
            for _ in range(8):
                while True:
                    p=[(i,rng.randrange(-200,201)) for i in range(n)]
                    if all(orient(p,*t)!=0 for t in combinations(range(n),3)):break
                controls.append(analyze(p,False))
        output['random_relation_controls']=controls
        output['status']='PASS'
    except Exception:
        output['status']='FAIL';output['traceback']=traceback.format_exc();raise
    finally:
        output['elapsed_seconds']=time.monotonic()-start
        output['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        output['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        args.out.write_text(json.dumps(output,indent=2)+'\n')
        print(json.dumps({k:v for k,v in output.items() if k not in ('fixtures','random_relation_controls')}))


if __name__=='__main__':main()
