#!/usr/bin/env python3
"""Exhaust exactly three removals/additions around the frozen near-model."""
import gzip,hashlib,itertools,json,time
from pathlib import Path
D=Path('.cache/resume313-primal');P=Path('experiments/omission-residual32-2598-primal-2026-10-10');raw=gzip.decompress((P/'source-2598.json.gz').read_bytes());sh=hashlib.sha256(raw).hexdigest();assert sh=='01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b';data=json.loads(raw);rows=data['constraints'];assert len(rows)==2598
base=json.loads((P/'candidates.json').read_text())['candidates'][2]['holes'];assert len(base)==32;W=sum(1<<i for i in base);masks=[sum(1<<i for i in r['support']) for r in rows];rhs=[r['rhs'] for r in rows];violations=[i for i,m in enumerate(masks) if (m&W).bit_count()<rhs[i]];assert violations==[205]
# Most restrictive rows first, without omitting any row.
order=sorted(range(len(rows)),key=lambda i:((masks[i]&W).bit_count()-rhs[i],len(rows[i]['support'])))
missing_universe=((1<<154)-1)&~W&~1;trials=0;stage2=0;pairchecks=0;found=None;start=time.monotonic();complete=True
for add in rows[205]['support']:
 if not (missing_universe>>add)&1:continue
 available0=missing_universe&~(1<<add)
 for drops in itertools.combinations(base,3):
  trials+=1;partial=(W^sum(1<<i for i in drops))|(1<<add);allowed=available0;ones=[]
  for i in order:
   deficit=rhs[i]-(masks[i]&partial).bit_count()
   if deficit>2:allowed=0;break
   if deficit==2:
    allowed&=masks[i]
    if allowed.bit_count()<2:allowed=0;break
   elif deficit==1:ones.append(masks[i])
  if allowed.bit_count()<2:continue
  stage2+=1
  # Every demand-one row must receive at least one of the last two holes.
  choices=allowed
  if ones:choices &= min(ones,key=lambda m:(m&allowed).bit_count())
  while choices:
   a=choices&-choices;choices-=a;bset=allowed&~a;pairchecks+=1
   for m in ones:
    if not (a&m):
     bset&=m
     if not bset:break
   if bset:
    candidate=partial|a|(bset&-bset);holes=[i for i in range(154) if candidate>>i&1];S=set(holes)
    assert len(holes)==32 and 0 not in holes
    assert all(len(S.intersection(r['support']))>=r['rhs'] for r in rows)
    assert all((candidate&m).bit_count()>=d for m,d in zip(masks,rhs))
    found=holes;break
  if found:break
  if trials%2000==0:
   print(json.dumps({'trials':trials,'stage2':stage2,'pairchecks':pairchecks,'seconds':time.monotonic()-start}),flush=True)
   if time.monotonic()-start>180:complete=False;break
 if found or not complete:break
report={'scope':'Exact three-exchange Boolean neighborhood only; no global exclusion or geometric realization claim.','source':str(P/'source-2598.json.gz'),'source_sha256':sh,'base_holes':base,'occupied_fixed':[0],'exchanges':3,'trials':trials,'stage2':stage2,'pairchecks':pairchecks,'seconds':time.monotonic()-start,'complete_neighborhood':complete and found is None,'witness_found':found is not None,'holes':found,'exact_all_rows_set_and_bitset_checked':found is not None,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(D/'three-exchange-result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
