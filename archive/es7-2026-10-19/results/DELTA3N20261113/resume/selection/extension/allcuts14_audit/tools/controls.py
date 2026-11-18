#!/usr/bin/env python3
"""Independent constructions and predicates, reusing only our frozen exact geometry."""
import importlib.util,itertools as it,json,resource,time
from fractions import Fraction
from pathlib import Path
import check_rows as C
R=C.R;E=R.parent
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
helper=E/'highsplit_audit/tools/controls.py'
oldmanifest=dict(line.split('  ',1)[::-1] for line in (E/'highsplit_audit/SHA256SUMS').read_text().splitlines())
assert C.sha(helper)==oldmanifest['tools/controls.py']
H=load('own_frozen_high_geometry',helper);Geometry=H.Geometry;mask=H.mask;verts=H.verts
def sec(a,b,x):return Fraction(a[1]*(b[0]-a[0])+(b[1]-a[1])*(x-a[0]),b[0]-a[0])
def above_left(P):
 x=P[0][0]-1;q=max(sec(a,b,x) for a,b in it.combinations(P,2));return (x,q.numerator//q.denominator+1)
def join(P,Q,kind):
 shift=P[-1][0]+4-Q[0][0];Q=[(x+shift,y) for x,y in Q]
 if kind=='low':
  thresholds=[y-sec(a,b,x) for x,y in Q for a,b in it.combinations(P,2)]
  thresholds += [sec(a,b,x)-y for x,y in P for a,b in it.combinations(Q,2)]
  h=max(thresholds);h=h.numerator//h.denominator+1;Q=[(x,y-h) for x,y in Q]
 else:
  boundary=Fraction(P[-1][0]+Q[0][0],2)
  thresholds=[(sec(a,b,x)-y)/(x-boundary) for x,y in Q for a,b in it.combinations(P,2)]
  thresholds += [(sec(a,b,x)-y)/(boundary-x) for x,y in P for a,b in it.combinations(Q,2)]
  h=max([Fraction(0)]+thresholds);h=h.numerator//h.denominator+1
  # Clear the possible half-unit denominator by doubling every coordinate.
  P=[(2*x,2*y) for x,y in P];Q=[(2*x,int(2*(y+h*(x-boundary)))) for x,y in Q]
 return P+Q
def top(G):return mask(i for i,b in enumerate(G.beta) if b==max(G.beta))
def mixed_check(G,k,kind):
 left=(1<<k)-1;full=(1<<G.m)-1;count=0
 for s in range(1,full+1):
  if not(s&left and s&~left):continue
  lp=verts(s&left);rp=verts(s&~left)
  want=G.chain(lp,-1 if kind=='low' else 1) and G.chain(rp,-1 if kind=='high' else 1)
  assert G.convex(verts(s))==want;count+=1
 return count
def check_case(name,P,n,k,kind):
 G=Geometry(P,n);L=Geometry(P[:k],n);Q=Geometry(P[k:],n)
 assert not G.cap5 and not G.ngons
 signs={t:d>0 for t,d in G.orient.items()};assert C.direct(signs,kind,k,G.m)
 # Brute endpoint ranks cross-check the inherited independent endpoint DP.
 for sub in (L,Q):
  beta=[1]*sub.m
  for s in range(1,1<<sub.m):
   vv=verts(s)
   if sub.chain(vv,1):beta[vv[-1]]=max(beta[vv[-1]],len(vv))
  assert beta==sub.beta
 mixed=mixed_check(G,k,kind);selections=[];cL=max(L.beta);cR=max(Q.beta)
 if kind in ('all_cup','high') and ((kind=='high' and cL==n-2) or (kind=='all_cup' and max(cL,cR)==n-2)):
  assert k==1 or G.m-k==1
  sub=Q if k==1 else L
  for b in range(1<<sub.m):
   if sub.valid(b):selections.append(G.selector((b<<1)|1 if k==1 else b|(1<<k)))
  branch='singleton_lift'
 elif kind=='all_cup':
  selections=[G.selector(top(L)|(top(Q)<<k))];branch='two_local_rank_levels'
 elif kind=='low' and cR==n-2:
  assert k==1
  for b in range(1<<Q.m):
   if Q.valid(b):selections.append(G.selector((b<<1)|1))
  branch='left_singleton_lift'
 elif kind=='low' and cR==n-3:
  assert L.chain(tuple(range(k)),1)
  selections=[G.selector((1<<a)|(top(Q)<<k)) for a in range(k)];branch='right_rank_four'
 elif kind=='low':
  assert cR<=n-4 and not L.cap4
  end3={t[-1] for t,d in L.orient.items() if d<0};option1=option2=0
  for b in range(1<<k):
   vv=verts(b);blue=verts(((1<<k)-1)^b)
   if not L.chain(vv,1):continue
   if all(b&s for s in L.targets) and all(v in end3 for v in vv[1:]):
    selections.append(G.selector(b|(top(Q)<<k)));option1+=1
   if len(blue)<=n-2 and L.chain(blue,1):selections.append(G.selector(b));option2+=1
  branch=f'T_option1={option1}_option2={option2}'
 else:raise AssertionError('unexpected case')
 assert selections
 tt,rs=C.rows(G.m);values={i:signs[t] for i,t in enumerate(tt,1)};false=[]
 for (family,cut),row in rs.items():
  split=C.direct(signs,family,cut,G.m)
  assert C.satisfied(row,values)==(not split)
  if split:false.append([family,cut])
 return {'name':name,'P':P,'n':n,'cut':k,'kind':kind,'geometry':G.summary(),'cup_left':cL,'cup_right':cR,
  'branch':branch,'selections':selections,'mixed_subset_checks':mixed,'cut_predicates_checked':len(rs),'false_cut_predicates':false}
def main():
 start=time.monotonic();resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20))
 inputs=[helper,E/'structure2/data/cup_join_controls.json',E/'highsplit_audit/data/controls-m14.json']
 inputs += [E/f'low_split_audit/data/control-left{k}.json' for k in (11,12,13)]
 before={str(p):C.sha(p) for p in inputs};cases=[]
 supplied=json.loads(inputs[1].read_text())['cases'];skipped=[]
 for name,item in supplied.items():
  if len(item['P'])>14:skipped.append(name);continue
  cases.append(check_case(name,item['P'],item['n'],item['cut'],'all_cup'))
 strong=[(0,0),(1,-1),(2,-3),(3,-6),(10,500),(11,600),(12,699),(13,797)]
 cases.append(check_case('user_two_fourcaps',strong,5,4,'all_cup'))
 right=json.loads(inputs[2].read_text())['P'];old=right[:13]
 cases.append(check_case('m14_right_singleton',right,7,13,'all_cup'))
 left=[above_left(old)]+old
 cases.append(check_case('m14_left_singleton',left,7,1,'all_cup'))
 cases.append(check_case('m14_low_d5',left,7,1,'low'))
 block=[(0,0),(1,-1),(2,-3),(3,-6),(4,1000),(5,999),(6,997)]
 cases.append(check_case('m14_cup_interior',join(block,block,'all_cup'),7,7,'all_cup'))
 r8=[(0,0),(1,-1),(2,-3),(3,-6),(4,1000),(5,1001),(6,1004),(7,1009)]
 cases.append(check_case('m14_low_d4',join([(i,i*i) for i in range(6)],r8,'low'),7,6,'low'))
 for k in (11,12,13):
  P=json.loads((E/f'low_split_audit/data/control-left{k}.json').read_text())['P_left']
  cases.append(check_case(f'm14_low_left{k}',join(P,[(i,i*i) for i in range(14-k)],'low'),7,k,'low'))
 after={str(p):C.sha(p) for p in inputs};assert before==after
 result={'status':'PASS','label':'COMPUTED','cases':cases,'cases_count':len(cases),
  'selections_checked':sum(len(c['selections']) for c in cases),'mixed_subset_checks':sum(c['mixed_subset_checks'] for c in cases),
  'actual_cut_predicates_checked':sum(c['cut_predicates_checked'] for c in cases),
  'm14_cases':sum(c['geometry']['m']==14 for c in cases),'skipped_parent_large_fixtures':skipped,
  'inputs_before':before,'inputs_after':after,'parent_expected_ranks_and_selectors_ignored':True,
  'seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 C.save('real-controls.json',result)
 print(json.dumps({k:v for k,v in result.items() if k not in ('cases','inputs_before','inputs_after')}))
if __name__=='__main__':
 try:main()
 except BaseException as e:
  C.save('controls-failure.json',{'error':repr(e)});raise
