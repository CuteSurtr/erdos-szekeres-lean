"""Necessary geometric model; numerical UNSAT is not a Lean proof.

Adapted from the repository's frozen fifth-core discovery archive. The state
catalog originates from Schroeder DOI10.5281/zenodo.22842891 (CC BY4.0).
See docs/THIRD_PARTY.md. All discoveries require separate kernel checking.
"""
import gc, hashlib, itertools, json, random, time
from itertools import permutations
from pathlib import Path
import numpy as np
import z3
z3.set_param(memory_max_size=768)

def cells(s):
    return {(i+1,y) for i,h in enumerate(s) for y in range(1,h+1)}

def pair_boxes(states):
    n = len(states)
    sets = [cells(s) for s in states]
    nonempty = np.zeros((n, n), bool)
    mn = np.zeros((2, n, n), np.int16)
    mx = np.zeros((2, n, n), np.int16)
    for a in range(n):
        for b in range(n):
            d = sets[b] - sets[a]
            if d:
                nonempty[a, b] = True
                mn[0, a, b] = min(z[0] for z in d)
                mx[0, a, b] = max(z[0] for z in d)
                mn[1, a, b] = min(z[1] for z in d)
                mx[1, a, b] = max(z[1] for z in d)
    return nonempty, mn, mx


def triple_table(nonempty, mn, mx):
    """T[a, b, c] is true iff the cyclic triple (a, b, c) passes all six orders."""
    n = nonempty.shape[0]
    idx = np.arange(n, dtype=np.int16)
    A, B, C = np.meshgrid(idx, idx, idx, indexing='ij')
    T = (A != B) & (B != C) & (A != C)
    grids = (A, B, C)
    for perm in permutations(range(3)):
        odd = sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3)) % 2
        coord = 1 if odd else 0
        p, q, r = (grids[perm[k]] for k in range(3))
        present = nonempty[p, q] & nonempty[q, r] & nonempty[p, r]
        forced = mx[coord][q, r] <= mn[coord][p, q]
        T &= (~present) | forced
    return T


def parity(q):return sum(q[i]>q[j] for i in range(len(q)) for j in range(i+1,len(q)))%2

def find_octagons(n,convex,limit=64):
 masks={t:0 for t in itertools.combinations(range(n),3)}
 for (a,b,c,d),v in convex.items():
  if v:masks[a,b,c]|=1<<d
 result=[];calls=0
 def dfs(selected,candidates):
  nonlocal calls
  calls+=1
  if len(selected)==8:
   result.append(tuple(selected));return len(result)>=limit
  need=8-len(selected)
  while candidates.bit_count()>=need:
   bit=candidates&-candidates;v=bit.bit_length()-1;candidates^=bit;nexts=candidates
   for a,b in itertools.combinations(selected,2):nexts&=masks[a,b,v]
   if dfs(selected+[v],nexts):return True
  return False
 dfs([], (1<<n)-1)
 return result,calls

class CompactModel:
 def __init__(self,S,deadline):
  self.S=S;self.n=n=len(S);self.s=z3.Solver();self.s.set(threads=1)
  self.pos=[z3.Int(f'p{i}') for i in range(n)];self.cap={e:z3.Int(f'a{e[0]}_{e[1]}') for e in itertools.combinations(range(n),2)};self.cup={e:z3.Int(f'b{e[0]}_{e[1]}') for e in self.cap};self.ori={e:z3.Bool('o'+'_'.join(map(str,e))) for e in itertools.combinations(range(n),3)}
  self.s.add(z3.Distinct(self.pos),*[z3.And(p>=0,p<n) for p in self.pos]);self.s.add(*[z3.And(a>=1,a<=4) for a in self.cap.values()]);self.s.add(*[z3.And(b>=1,b<=6) for b in self.cup.values()])
  self.fixed={};self.before={};self.differences={}
  for i,j in itertools.permutations(range(n),2):
   diff=cells[S[j]]-cells[S[i]]-{(1,6)};self.differences[i,j]=diff
  for i,j in self.cap:
   a=self.cap[i,j];b=self.cup[i,j];self.s.add(z3.Not(z3.And(a==1,b==6)))
   for u,v in [(i,j),(j,i)]:
    if not self.differences[u,v]:self.fixed[u,v]=False;self.fixed[v,u]=True
  for i,j in itertools.permutations(range(n),2):
   self.before[i,j]=z3.BoolVal(self.fixed[i,j]) if (i,j) in self.fixed else self.pos[i]<self.pos[j]
   if self.fixed.get((i,j)) is True:self.s.add(self.pos[i]<self.pos[j])
   if self.fixed.get((i,j)) is False:continue
   a=self.cap[tuple(sorted((i,j)))];b=self.cup[tuple(sorted((i,j)))];domain=z3.Or(*[z3.And(a==x,b==y) for x,y in sorted(self.differences[i,j])])
   self.s.add(domain if self.fixed.get((i,j)) is True else z3.Implies(self.before[i,j],domain))
  self.known={};self.oriented={}
  for t,o in self.ori.items():
   a,b,c=[S[i] for i in t]
   if TT[a,b,c]:self.known[t]=True;self.s.add(o)
   elif TT[a,c,b]:self.known[t]=False;self.s.add(z3.Not(o))
  for q in itertools.permutations(range(n),3):
   t=tuple(sorted(q));v=z3.BoolVal(self.known[t]) if t in self.known else self.ori[t]
   self.oriented[q]=z3.Not(v) if parity(q) else v
   cond=self.condition(q)
   if cond is None:continue
   a,b,c=q;ab=tuple(sorted((a,b)));bc=tuple(sorted((b,c)))
   self.s.add(z3.Implies(cond,z3.If(self.oriented[q],self.cup[ab]<self.cup[bc],self.cap[ab]<self.cap[bc])))
  self.convex={};packets=0
  for index,quad in enumerate(itertools.combinations(range(n),4)):
   if index%64==0 and time.monotonic()>deadline:raise TimeoutError('model construction deadline')
   for q in itertools.permutations(quad):
    cond=self.condition(q)
    if cond is None:continue
    a,b,c,d=q;x,y,z,w=[self.oriented[t] for t in [(a,b,c),(a,b,d),(a,c,d),(b,c,d)]]
    packet=z3.And(z3.Implies(x==z,x==y),z3.Implies(x==w,z3.And(x==y,x==z)),z3.Implies(y==w,y==z));self.s.add(z3.Implies(cond,packet));packets+=1
   a,b,c,d=quad;x,y,z,w=[self.ori[t] for t in [(a,b,c),(a,b,d),(a,c,d),(b,c,d)]];q=z3.Bool('q'+'_'.join(map(str,quad)));self.convex[quad]=q;self.s.add(q==z3.PbEq([(z3.Not(w),1),(z,1),(z3.Not(y),1),(x,1)],2))
  self.packet_count=packets;self.cuts=set()
  local_index={state:i for i,state in enumerate(S)}
  faces={frozenset(set(row['support'])&occupied) for row in D['constraints'] if len(row['support']) in [8,9] and len(set(row['support'])&occupied)==7}
  for face in faces:
   if not face<=set(S):continue
   for state in set(S)-face:
    eight=tuple(sorted(local_index[v] for v in face|{state}))
    if eight in self.cuts:continue
    self.cuts.add(eight);self.s.add(z3.Or(*[z3.Not(self.convex[q]) for q in itertools.combinations(eight,4)]))
 def condition(self,q):
  if any(self.fixed.get((a,b)) is False for a,b in itertools.combinations(q,2)):return None
  conditions=[self.before[a,b] for a,b in zip(q,q[1:]) if (a,b) not in self.fixed]
  return z3.And(*conditions)
 def assignment(self,m):
  val=lambda x:m.eval(x,model_completion=True)
  return {'positions':[val(p).as_long() for p in self.pos], 'labels':[[i,j,val(a).as_long(),val(self.cup[i,j]).as_long()] for (i,j),a in self.cap.items()], 'orientations':[[*q,z3.is_true(val(o))] for q,o in self.ori.items()]}
 def replay(self,a):
  n=self.n;p=a['positions'];assert sorted(p)==list(range(n));labels={(i,j):(x,y) for i,j,x,y in a['labels']};orientations={tuple(q[:3]):q[3] for q in a['orientations']}
  def o(q):return orientations[tuple(sorted(q))]^(parity(q)==1)
  order=sorted(range(n),key=lambda i:p[i])
  for i,j in itertools.combinations(order,2):assert labels[tuple(sorted((i,j)))] in self.differences[i,j]
  for i,j,k in itertools.combinations(order,3):
   l=labels[tuple(sorted((i,j)))];r=labels[tuple(sorted((j,k)))];coordinate=1 if o((i,j,k)) else 0;assert l[coordinate]<r[coordinate]
  for q in itertools.combinations(order,4):
   vals=[o(t) for t in itertools.combinations(q,3)];assert sum(x!=y for x,y in zip(vals,vals[1:]))<=1
  for t,v in self.known.items():assert orientations[t]==v
  convex={}
  for a,b,c,d in itertools.combinations(range(n),4):
   x,y,z,w=[orientations[t] for t in [(a,b,c),(a,b,d),(a,c,d),(b,c,d)]];convex[a,b,c,d]=sum([not w,z,not y,x])==2
  return find_octagons(n,convex)
 def probe(self,deadline):
  r={'support':self.S,'size':self.n,'packet_constraints':self.packet_count};iterations=0;solve_seconds=0
  while time.monotonic()<deadline:
   iterations+=1;remaining=max(1,int(1000*(deadline-time.monotonic())));self.s.set(timeout=min(25000,remaining));start=time.monotonic();status=self.s.check();solve_seconds+=time.monotonic()-start
   if status==z3.unsat:
    name='coupled-large-unsat-'+hashlib.sha256(bytes(self.S)).hexdigest()[:12]+'.smt2';(ROOT/name).write_text(self.s.to_smt2());return dict(r,status='unsat',smt2=name,iterations=iterations,cuts=len(self.cuts),solve_seconds=solve_seconds)
   if status==z3.unknown:
    return dict(r,status='unknown',reason=self.s.reason_unknown(),iterations=iterations,cuts=len(self.cuts),solve_seconds=solve_seconds)
   model=self.s.model();assignment=self.assignment(model);violations,calls=self.replay(assignment)
   if not violations:
    name='coupled-large-sat-'+hashlib.sha256(bytes(self.S)).hexdigest()[:12]+'.json';(ROOT/name).write_text(json.dumps({'support':self.S,'assignment':assignment,'replay':'All domains, shared-label growth, chronological packets, fixed signs, and exhaustive convex-eight clique search passed.'},indent=1));return dict(r,status='sat',assignment=name,iterations=iterations,cuts=len(self.cuts),solve_seconds=solve_seconds,final_clique_calls=calls)
   for eight in violations:
    assert eight not in self.cuts
    self.cuts.add(eight);self.s.add(z3.Or(*[z3.Not(self.convex[q]) for q in itertools.combinations(eight,4)]))
  return dict(r,status='unknown',reason='per-support total deadline',iterations=iterations,cuts=len(self.cuts),solve_seconds=solve_seconds)
