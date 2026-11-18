"""Deletion finder with recomputed ambient ranks. No certification claim."""
import argparse
import json
import random
import time
from pathlib import Path
from probe import WORK, encode_solve

ap=argparse.ArgumentParser();ap.add_argument('stem');ap.add_argument('--seed',type=int,default=0)
ap.add_argument('--tag',default='minimum');args=ap.parse_args()
raw=(WORK/(args.stem+'.points')).read_text().split();m,n=map(int,raw[:2])
original=[list(map(int,raw[2+2*i:4+2*i])) for i in range(m)]
indices=list(range(m));rng=random.Random(args.seed);history=[];start=time.monotonic();serial=0
while True:
    changed=False
    order=indices.copy();rng.shuffle(order)
    for removed in order:
        if time.monotonic()-start>10:
            outcome='UNKNOWN_BUDGET';break
        kept=[i for i in indices if i!=removed];p=[original[i] for i in kept]
        stem=f'{args.tag}-s{args.seed}-trial{serial:04d}';serial+=1
        (WORK/(stem+'.points')).write_text(f'{len(p)} {n}\n'+''.join(f'{x} {y}\n' for x,y in p))
        result=encode_solve(stem)
        history.append(dict(stem=stem,removed=removed,indices=kept,result=result))
        if result.get('terminal',{}).get('outcome')=='UNSAT_UNCERTIFIED':
            indices=kept;changed=True
            print(json.dumps(dict(retained=len(kept),indices=kept,stem=stem)),flush=True)
            break
    else:
        if changed: continue
        outcome='SINGLE_DELETION_IRREDUCIBLE';break
    if not changed: break
stem=f'{args.tag}-s{args.seed}-final'
p=[original[i] for i in indices]
(WORK/(stem+'.points')).write_text(f'{len(p)} {n}\n'+''.join(f'{x} {y}\n' for x,y in p))
result=encode_solve(stem)
(WORK/(stem+'.minimize.json')).write_text(json.dumps(dict(source=args.stem,seed=args.seed,
    outcome=outcome,indices=indices,P=p,history=history,result=result),indent=2)+'\n')
print(json.dumps(dict(stem=stem,indices=indices,P=p,outcome=outcome,result=result)),flush=True)
