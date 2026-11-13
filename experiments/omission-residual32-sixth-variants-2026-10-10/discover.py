#!/usr/bin/env python3
"""Complete CSP traversal up to an explicit support/time limit, not Lean proof.

Adapted from the case4 template-map search. Candidates are globally drawn from
all154 states, not just a coordinate-neighborhood of an existing support.
"""
import argparse,collections,hashlib,json,os,sys,time
from pathlib import Path
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from omission_cycle_enumeration import pair_boxes,triple_table
p=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=64);p.add_argument('--seconds',type=float,default=180);p.add_argument('--occupied-only',action='store_true');p.add_argument('--output',type=Path,default=HERE/'variants.json');a=p.parse_args()
source=ROOT/'.cache/residual32-resume-2026-10-10-b/source.json';raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()=='f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909';D=json.loads(raw)
core_path=ROOT/'experiments/omission-residual32-witness-coupled-2026-10-10/core13.json';core=json.loads(core_path.read_text());criteria=[c for c in core['clauses'] if c['kind'] in ('empty_direction','domain','fixed_sign')];k=len(core['support']);assert k==13
holes=set(json.loads((ROOT/'experiments/omission-residual32-case4-2026-10-10/witness.json').read_text())['holes']);T=sorted(set(range(154))-holes)+(sorted(holes) if not a.occupied_only else [])
cells=[{(i+1,j) for i,h in enumerate(s[:4]) for j in range(1,h+1)} for s in D['states']];P,mn,mx=pair_boxes(D['states']);TT=triple_table(P,mn,mx)
def good(c,S):
 q=c['detail'];aa,bb=S[q[0]],S[q[1]]
 if c['kind']=='fixed_sign':return TT[aa,bb,S[q[2]]] if q[3] else TT[aa,S[q[2]],bb]
 diff=cells[bb]-cells[aa]-{(1,6)}
 return not diff if c['kind']=='empty_direction' else (q[2],q[3]) not in diff
assert len(set(core['support']))==13 and all(good(c,core['support']) for c in criteria)
scopes=[set(c['detail'][:3] if c['kind']=='fixed_sign' else c['detail'][:2]) for c in criteria];checks=[[(c,sc) for c,sc in zip(criteria,scopes) if i in sc] for i in range(k)]
known={tuple(sorted(r['support'])) for r in D['constraints']}|{tuple(sorted(core['support']))};seen=set();variants=[];nodes=duplicates=old_supports=0;reason=None;start=time.monotonic();end=start+a.seconds

def save():
 out={'scope':'Finite compatibility CSP candidates; Lean verification required','source_sha256':hashlib.sha256(raw).hexdigest(),'core_sha256':hashlib.sha256(core_path.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'candidate_states':T,'constraints':len(criteria),'nodes':nodes,'seconds':time.monotonic()-start,'limit':a.limit,'stop_reason':reason,'complete_search':reason=='exhausted','duplicate_mappings':duplicates,'old_supports_skipped':old_supports,'variants':variants}
 a.output.write_text(json.dumps(out,indent=2)+'\n')

def dfs(S,used,assigned):
 global nodes,duplicates,old_supports,reason
 nodes+=1
 if time.monotonic()>end:reason='time_limit';return True
 if len(assigned)==k:
  supp=tuple(sorted(S))
  if supp in known:old_supports+=1;return False
  if supp in seen:duplicates+=1;return False
  assert all(good(c,S) for c in criteria)
  seen.add(supp);variants.append({'map':S.copy(),'support':list(supp),'rhs':1,'violates_case4_witness':not holes&set(S)})
  if len(variants)%16==0:save();print(json.dumps({'found':len(variants),'nodes':nodes,'seconds':time.monotonic()-start,'witness_separating':sum(x['violates_case4_witness'] for x in variants)}),flush=True)
  if len(variants)>=a.limit:reason='support_limit';return True
  return False
 best=None
 for i in set(range(k))-assigned:
  ready=[c for c,sc in checks[i] if sc-{i}<=assigned];opts=[]
  for v in T:
   if v in used:continue
   S[i]=v
   if all(good(c,S) for c in ready):opts.append(v)
  S[i]=None;score=(len(opts),-len(ready),-len(checks[i]))
  if best is None or score<best[0]:best=(score,i,opts)
  if not opts:return False
 _,i,opts=best
 for v in opts:
  S[i]=v
  if dfs(S,used|{v},assigned|{i}):return True
 S[i]=None
 return False

dfs([None]*k,set(),set())
if reason is None:reason='exhausted'
save();print(json.dumps({'found':len(variants),'nodes':nodes,'stop_reason':reason,'seconds':time.monotonic()-start}),flush=True)
