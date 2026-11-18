"""Reproduce the restricted T=L4 union L5 enumeration, never all U subsets."""
import argparse
import hashlib
import json
from pathlib import Path
import time


def mask(t):return sum(1<<v for v in t)
def ids(t):return [i for i in range(t.bit_length()) if t>>i&1]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();start=time.monotonic()
    r=json.loads(args.input.read_text())['fixtures']['terminal18']
    T=r['profiles']['top_two_levels']['A'];tm=mask(T)
    H=[mask(t) for t in r['targets']]
    C=[mask(t) for t in r['caps4'] if mask(t)&tm==mask(t)]
    B=[mask(t) for t in r['exposed'] if mask(t)&tm==mask(t)]
    R=[mask(t) for t in r['rank3_triples'] if mask(t)&tm==mask(t)]
    G=sorted(set(mask(t[:2]) for t in r['caps4']+r['exposed'] if mask(t)&tm==mask(t)))
    valid=[];graph=[];ordinary=[];terminal=[]
    for b in range(1<<len(T)):
        a=mask([v for i,v in enumerate(T) if b>>i&1])
        if any(a&h==0 for h in H) or any(a&c==c for c in C):continue
        ordinary.append(ids(a))
        if any(a&c==c for c in B):continue
        valid.append(ids(a))
        if not any(a&c==c for c in G):graph.append(ids(a))
        if not any(a&c==c for c in R):terminal.append(ids(a))
    result=dict(label='COMPUTED exact restricted enumeration',region=T,assignments=1<<len(T),
       counts=dict(ordinary=len(ordinary),uniform=len(valid),prefix_graph=len(graph),terminal=len(terminal)),
       smallest_uniform=min(valid,key=lambda a:(len(a),a)) if valid else None,
       smallest_graph=min(graph,key=lambda a:(len(a),a)) if graph else None,
       prefix_edges=[ids(e) for e in G],all_uniform=valid,
       input_sha256=hashlib.sha256(args.input.read_bytes()).hexdigest(),
       source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed=time.monotonic()-start)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='all_uniform'}))


if __name__=='__main__':main()
