#!/usr/bin/env python3
"""Exact hull/subset audit of the three boundary realizations."""
import hashlib,itertools,json,resource
from pathlib import Path
ROOT=Path('/home/jay/research/data/delta3-codex-20261113/boundary')
HERE=Path(__file__).resolve().parent
C=itertools.combinations
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bits(t):return sum(1<<i for i in t)
def det(P,t):
 a,b,c=(P[i] for i in t)
 return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def hull(P,t):
 def half(seq):
  st=[]
  for i in seq:
   while len(st)>1 and det(P,(st[-2],st[-1],i))<=0:st.pop()
   st.append(i)
  return st
 return set(half(t)+half(reversed(t)))
def contains(m,edges):
 z=bytearray(1<<m)
 for edge in edges:z[bits(edge)]=1
 for i in range(m):
  b=1<<i
  for s in range(1<<m):
   if s&b:z[s]|=z[s^b]
 return z
def inspect(P,n):
 m=len(P);v=range(m);full=(1<<m)-1
 assert all(type(z)is int for p in P for z in p)
 assert all(P[i][0]<P[i+1][0] for i in range(m-1))
 d={t:det(P,t) for t in C(v,3)};assert all(d.values())
 def cap(t):return all(d[x]<0 for x in C(t,3))
 def cup(t):return all(d[x]>0 for x in C(t,3))
 caps=[t for t in C(v,4) if cap(t)]
 cap5=[t for t in C(v,5) if cap(t)]
 targets=[t for t in C(v,n-1) if len(hull(P,t))==n-1]
 forbidden=[t for t in C(v,n) if len(hull(P,t))==n]
 end4={t[-2:] for t in caps}
 bad=[t for t in C(v,3) if cap(t) and t[-2:] not in end4]
 cap_cont=contains(m,caps);target_cont=contains(m,targets);bad_cont=contains(m,bad)
 deltas=[s for s in range(1<<m) if not cap_cont[s] and not target_cont[full^s]]
 safe=[s for s in deltas if not bad_cont[s]]
 rooted=[s for s in deltas if s&(1<<(m-1))]
 def least(ss):
  if not ss:return None
  s=min(ss,key=lambda s:(s.bit_count(),s))
  return [i for i in v if s>>i&1]
 cups=[t for t in C(v,n-2) if cup(t)]
 longer=[t for t in C(v,n-1) if cup(t)]
 complements=[]
 for t in cups:
  b=tuple(i for i in v if i not in t)
  complements.append({'cup':t,'complement':b,'convex':len(hull(P,b))==len(b)})
 return {'m':m,'n':n,'no_fivecap':not cap5,'no_ngon':not forbidden,
         'min_abs_det':min(abs(x) for x in d.values()),'fourcaps':len(caps),
         'target_polygons':len(targets),'long_cups':cups,'longer_cups':longer,
         'cup_complements':complements,'delta_count':len(deltas),'rooted_count':len(rooted),
         'terminal_safe_count':len(safe),'minimum_delta':least(deltas),
         'minimum_rooted_delta':least(rooted),'minimum_terminal_safe_delta':least(safe)}
def main():
 resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20));resource.setrlimit(resource.RLIMIT_CPU,(18,18))
 out=HERE/'data';out.mkdir(exist_ok=True);records=[]
 for n in (6,7,8):
  path=ROOT/f'realization/n{n}-root/realized.json';r=json.loads(path.read_text());P=r['P']
  signs=''.join('+' if det(P,t)>0 else '-' for t in C(range(len(P)),3))
  assert signs==r['signs']
  full=inspect(P,n);old=inspect(P[:-1],n)
  assert full['no_fivecap'] and full['no_ngon'] and old['no_fivecap'] and old['no_ngon']
  assert old['long_cups'] and not old['longer_cups']
  assert all(x['convex'] for x in old['cup_complements'])
  A=old['minimum_terminal_safe_delta'];assert A is not None
  D=A+[len(P)-1]
  assert not any(all(det(P,t)<0 for t in C(q,3)) for q in C(D,4))
  B=tuple(i for i in range(len(P)) if i not in D)
  assert not any(len(hull(P,t))==n-1 for t in C(B,n-1))
  result={'label':'COMPUTED exact integer exhaustive check','P':P,'n':n,
          'source':str(path),'source_sha256':sha(path),'full':full,'old':old,
          'terminal_safe_extension':D,'source_signs_match':True}
  (out/f'n{n}-boundary.json').write_text(json.dumps(result,indent=2)+'\n');records.append(result)
 print(json.dumps([{'n':r['n'],'old_cups':len(r['old']['long_cups']),
                    'terminal_safe_count':r['old']['terminal_safe_count'],
                    'terminal_safe_extension':r['terminal_safe_extension']} for r in records]))
 (out/'parent_checks.json').write_text(json.dumps({'script_sha256':sha(Path(__file__)),
    'outcomes':[{'n':r['n'],'file':f'n{r["n"]}-boundary.json','sha256':sha(out/f'n{r["n"]}-boundary.json')} for r in records]},indent=2)+'\n')
if __name__=='__main__':main()
