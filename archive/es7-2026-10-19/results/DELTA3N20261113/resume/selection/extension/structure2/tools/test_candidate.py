"""Exact restricted-selection enumeration over one frozen cup-rank level."""
import argparse
from itertools import combinations
import hashlib
import json
from pathlib import Path
import time


def mask(ids): return sum(1<<i for i in ids)
def ids(m): return [i for i in range(m.bit_length()) if m>>i&1]


def analyze(r):
    beta=r['beta'];level=[i for i,b in enumerate(beta) if b==5]
    lmask=mask(level)
    targets=[mask(t) for t in r['targets']]
    missed=[h for h in targets if not h&lmask]
    common=set(range(r['m']))
    for h in missed:common.intersection_update(ids(h))
    ps=sorted(i for i in common if beta[i]==4) if missed else []
    c4=[mask(t) for t in r['caps4']]
    bad=[mask(t) for t in r['exposed']]
    rankbad=[mask(t) for t in r['rank3_triples']]
    output=dict(L5=level,missed=[ids(h) for h in missed],eligible_p=ps,tests=[])
    for p in ps:
        pmask=1<<p
        region=lmask|pmask
        required=sorted(set(h&lmask for h in targets if not h&pmask),key=lambda x:(x.bit_count(),ids(x)))
        required=[h for h in required if not any(g!=h and g&h==g for g in required)]
        forbid=sorted(set((h&lmask) for h in c4+bad if h&region==h),key=lambda x:(x.bit_count(),ids(x)))
        forbid=[h for h in forbid if not any(g!=h and g&h==g for g in forbid)]
        witnesses=[];terminal=[];ordinary=[]
        rejected=dict(target=0,cap4=0,exposure=0)
        for bits in range(1<<len(level)):
            b=sum(1<<v for j,v in enumerate(level) if bits>>j&1);a=b|pmask
            if any(a&h==0 for h in targets):rejected['target']+=1;continue
            if any(a&h==h for h in c4):rejected['cap4']+=1;continue
            ordinary.append(ids(a))
            if any(a&h==h for h in bad):rejected['exposure']+=1;continue
            witnesses.append(ids(a))
            if not any(a&h==h for h in rankbad):terminal.append(ids(a))
        key=lambda x:(len(x),x)
        output['tests'].append(dict(p=p,required_minimal=[ids(h) for h in required],
              forbidden_minimal=[ids(h) for h in forbid],enumerated=1<<len(level),
              ordinary_count=len(ordinary),uniform_count=len(witnesses),terminal_count=len(terminal),
              smallest_uniform=min(witnesses,key=key) if witnesses else None,
              all_uniform=witnesses,rejected=rejected))
    return output


def main():
    ap=argparse.ArgumentParser();ap.add_argument('profiles',type=Path);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();start=time.monotonic()
    raw=json.loads(args.profiles.read_text());results={name:analyze(r) for name,r in raw['fixtures'].items()}
    output=dict(status='COMPUTED exact finite restricted enumeration',results=results,
                input_sha256=hashlib.sha256(args.profiles.read_bytes()).hexdigest(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed=time.monotonic()-start)
    args.out.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output))


if __name__=='__main__':main()
