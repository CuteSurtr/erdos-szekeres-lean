from pathlib import Path
import argparse,ast,json,hashlib,re,sys,time,os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
sys.path.insert(0,'scripts')
from omission_cycle_enumeration import pair_boxes,triple_table
p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=30);p.add_argument('--full-witness',action='store_true');a=p.parse_args()
b=Path('experiments/omission-residual32-case4-2026-10-10');raw=Path('.cache/residual32-resume-2026-10-10-b/source.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909';states=json.loads(raw)['states']
H=set(json.loads((b/'witness.json').read_text())['holes']);T=sorted(set(range(154))-H) if a.full_witness else [25,43,53,65,74,85,89,91,96,107,110,111,125];assert not H&set(T)
cells=[{(i+1,j) for i,h in enumerate(s[:4]) for j in range(1,h+1)} for s in states];P,mn,mx=pair_boxes(states);TT=triple_table(P,mn,mx)
log=[]
for family in ['Nine','', 'Second','Third','Fourth','Fifth']:
 start=time.monotonic();end=start+a.seconds;k=9 if family=='Nine' else 13
 path=Path(f'ErdosSzekeres/Omission/CoupledTemplate{family}.lean');text=path.read_text();criteria=[]
 for name,kind in [('emptyTests','empty'),('domainTests','domain'),('positiveTests','positive')]:
  match=re.search(r'def '+name+r' :[^\n]+:= (\[[^\n]*\])',text);assert match,name
  criteria.extend((kind,tuple(item)) for item in ast.literal_eval(match[1]))
 def good(c,S):
  kind,q=c;aa,bb=S[q[0]],S[q[1]]
  if kind=='positive':return TT[aa,bb,S[q[2]]]
  diff=cells[bb]-cells[aa]-{(1,6)}
  return not diff if kind=='empty' else (q[2],q[3]) not in diff
 scopes=[set(q[:3] if kind=='positive' else q[:2]) for kind,q in criteria];checks=[[(c,sc) for c,sc in zip(criteria,scopes) if i in sc] for i in range(k)]
 nodes=0;timedout=False
 def dfs(S,used,assigned):
  global nodes,timedout
  nodes+=1
  if time.monotonic()>end:timedout=True;return None
  if len(assigned)==k:return S.copy()
  best=None
  for i in set(range(k))-assigned:
   ready=[c for c,sc in checks[i] if sc-{i}<=assigned];opts=[]
   for v in T:
    if v in used:continue
    S[i]=v
    if all(good(c,S) for c in ready):opts.append(v)
   S[i]=None;score=(len(opts),-len(ready),-len(checks[i]))
   if best is None or score<best[0]:best=(score,i,opts)
   if not opts:return None
  _,i,opts=best
  for v in opts:
   S[i]=v;res=dfs(S,used|{v},assigned|{i})
   if res is not None:return res
   if timedout:return None
  S[i]=None
  return None
 res=dfs([None]*k,set(),set());r={'family':family or 'First','support':T,'mapping':res,'nodes':nodes,'timeout':timedout,'complete_search':not timedout,'seconds':time.monotonic()-start,'template_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'criteria':len(criteria)};log.append(r);print(json.dumps(r),flush=True)
 if res is not None:assert len(set(res))==k and all(good(c,res) for c in criteria);break
out=Path('.cache/residual32-case4-2026-10-10')/('full-witness-template-match.json' if a.full_witness else 'minimal-core-template-match.json');out.write_text(json.dumps({'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'results':log,'scope':'Finite CSP diagnostic; positive substitutions still require Lean check'},indent=2)+'\n')
