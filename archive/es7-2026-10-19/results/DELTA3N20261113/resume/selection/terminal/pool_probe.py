"""Test a frozen prefix of a real pool; retain every model and failed probe."""
import argparse
import hashlib
import json
import time
from pathlib import Path
from probe import WORK, encode_solve

ap=argparse.ArgumentParser()
ap.add_argument('input',type=Path);ap.add_argument('--n',type=int,required=True)
ap.add_argument('--tag',required=True);ap.add_argument('--first',type=int,default=0)
ap.add_argument('--last',type=int,default=100000)
args=ap.parse_args()
blob=args.input.read_bytes(); digest=hashlib.sha256(blob).hexdigest()
lines=blob.decode().splitlines();start=time.monotonic()
for idx in range(args.first,min(args.last,len(lines))):
    if time.monotonic()-start>8: break
    data=json.loads(lines[idx]);p=sorted(data['P']);stem=f'{args.tag}-{idx:04d}-n{args.n}'
    if any(abs(c)>10**15 for q in p for c in q):
        print(json.dumps(dict(stem=stem,outcome='OUTSIDE_ENCODER_COORDINATE_BOUND')),flush=True);continue
    text=f'{len(p)} {args.n}\n'+''.join(f'{x} {y}\n' for x,y in p)
    (WORK/(stem+'.points')).write_text(text)
    (WORK/(stem+'.input.json')).write_text(json.dumps(dict(P=p,source=str(args.input),
        source_sha256=digest,line=idx+1,n=args.n,points_sha256=hashlib.sha256(text.encode()).hexdigest()),indent=2)+'\n')
    result=encode_solve(stem)
    print(json.dumps(result),flush=True)
    if result.get('terminal',{}).get('outcome')=='UNSAT_UNCERTIFIED': break
