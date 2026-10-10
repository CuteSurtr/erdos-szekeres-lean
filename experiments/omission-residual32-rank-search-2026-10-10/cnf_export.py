#!/usr/bin/env python3
"""Rank-aware derivative of the frozen direct CNF encoder. Discovery only."""
import collections,gzip,hashlib,itertools,json,sys
from pathlib import Path
import model
ROOT=Path('.cache/rank313')
SOURCE=Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz')
raw=gzip.decompress(SOURCE.read_bytes());assert hashlib.sha256(raw).hexdigest()=='151ea1bfb175f6507d910521eb96961c82b54add2fb7e49e13b864b87241123e';D=json.loads(raw)
P,mn,mx=model.pair_boxes(D['states']);TT=model.triple_table(P,mn,mx);cells=[{(i+1,y) for i,h in enumerate(s[:4]) for y in range(1,h+1)} for s in D['states']]
record=json.loads((ROOT/'minimal-core.json').read_text());occupied=set(range(154))-set(record['strict_row_witness_holes'])
def neg(l):return not l if isinstance(l,bool) else -l
class CNF:
 def __init__(self,S):
  self.S=S;self.n=n=len(S);self.ids={};self.variables=[];self.clauses=[];self.kinds=[];self.details=[]
  def variable(key):
   key=tuple(key)
   if key not in self.ids:self.ids[key]=len(self.variables)+1;self.variables.append(key)
   return self.ids[key]
  self.variable=variable
  for i,j in itertools.combinations(range(n),2):
   self.before(i,j)
   for k in range(2,5):self.ge('cap',i,j,k)
   for k in range(2,7):self.ge('cup',i,j,k)
  for q in itertools.combinations(range(n),3):self.orient(q)
  for q in itertools.combinations(range(n),4):self.convex(q)
  self.differences={(i,j):cells[S[j]]-cells[S[i]]-{(1,6)} for i,j in itertools.permutations(range(n),2)}
  for i,j in itertools.combinations(range(n),2):
   for typ,maximum in [('cap',4),('cup',6)]:
    for k in range(2,maximum):self.add([neg(self.ge(typ,i,j,k+1)),self.ge(typ,i,j,k)],'threshold_monotone',[typ,i,j,k])
   for u,v in [(i,j),(j,i)]:
    self.add([neg(self.before(u,v)),neg(self.ge('cup',u,v,D['states'][S[u]][0]+2))],'source_cup',[u,v])
    if not self.differences[u,v]:self.add([neg(self.before(u,v))],'empty_direction',[u,v])
    for a in range(1,5):
     for b in range(1,7):
      if (a,b) in self.differences[u,v]:continue
      self.add([neg(self.before(u,v)),neg(self.ge('cap',i,j,a)),self.ge('cap',i,j,a+1),neg(self.ge('cup',i,j,b)),self.ge('cup',i,j,b+1)],'domain',[u,v,a,b])
  for a,b,c in itertools.permutations(range(n),3):
   self.add([neg(self.before(a,b)),neg(self.before(b,c)),self.before(a,c)],'order_transitive',[a,b,c])
   for typ,maximum,color in [('cap',4,False),('cup',6,True)]:
    gate=[neg(self.before(a,b)),neg(self.before(b,c)),neg(self.orient((a,b,c))) if color else self.orient((a,b,c))]
    for k in range(1,maximum+1):self.add(gate+[neg(self.ge(typ,a,b,k)),self.ge(typ,b,c,k+1)],'growth',[typ,a,b,c,k])
  for q in itertools.combinations(range(n),3):
   a,b,c=[S[i] for i in q]
   if TT[a,b,c]:self.add([self.orient(q)],'fixed_sign',[*q,True])
   elif TT[a,c,b]:self.add([neg(self.orient(q))],'fixed_sign',[*q,False])
  for quad in itertools.combinations(range(n),4):
   for q in itertools.permutations(quad):
    order=[neg(self.before(a,b)) for a,b in zip(q,q[1:])];triples=list(itertools.combinations(q,3))
    for bits in itertools.product([False,True],repeat=4):
     if sum(a!=b for a,b in zip(bits,bits[1:]))<=1:continue
     self.add(order+[neg(self.orient(t)) if bit else self.orient(t) for t,bit in zip(triples,bits)],'packet',[*q,*bits])
   a,b,c,d=quad;triples=[(a,b,c),(a,b,d),(a,c,d),(b,c,d)]
   for bits in itertools.product([False,True],repeat=4):
    x,y,z,w=bits;convex=sum([not w,z,not y,x])==2
    self.add([neg(self.orient(t)) if bit else self.orient(t) for t,bit in zip(triples,bits)]+[self.convex(quad) if convex else neg(self.convex(quad))],'convex_four',[*quad,*bits])
  faces={frozenset(set(row['support'])&occupied) for row in D['constraints'] if len(row['support']) in [8,9] and len(set(row['support'])&occupied)==7};index={v:i for i,v in enumerate(S)};eights=set()
  for face in faces:
   if not face<=set(S):continue
   for v in set(S)-face:eights.add(tuple(sorted(index[u] for u in face|{v})))
  for eight in sorted(eights):self.add([neg(self.convex(q)) for q in itertools.combinations(eight,4)],'no_octagon',list(eight))
 def before(self,i,j):return self.variable(('before',min(i,j),max(i,j)))*(1 if i<j else -1)
 def ge(self,typ,i,j,k):
  maximum=4 if typ=='cap' else 6
  if k<=1:return True
  if k>maximum:return False
  return self.variable((typ+'_ge',min(i,j),max(i,j),k))
 def orient(self,q):
  parity=sum(q[i]>q[j] for i in range(3) for j in range(i+1,3))%2
  return self.variable(('orientation',*sorted(q)))*(1 if not parity else -1)
 def convex(self,q):return self.variable(('convex_four',*sorted(q)))
 def add(self,literals,kind,detail):
  if any(l is True for l in literals):return
  clause=set(l for l in literals if l is not False)
  if any(-l in clause for l in clause):return
  self.clauses.append(sorted(clause,key=lambda l:(abs(l),l)));self.kinds.append(kind);self.details.append(detail)
 def export(self,prefix):
  prefix=Path(prefix);cnf=prefix.with_suffix('.cnf');cnf.write_text(f'p cnf {len(self.variables)} {len(self.clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in self.clauses))
  prefix.with_suffix('.json').write_text(json.dumps({'scope':'Unverified geometry-to-CNF encoding; SAT proof only establishes this literal CNF is inconsistent','support':self.S,'variables':self.variables,'clause_kinds':self.kinds,'clause_details':self.details,'cnf_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest(),'kind_counts':dict(collections.Counter(self.kinds))},separators=(',',':'))+'\n')
 def replay(self,assignment):
  positions=assignment['positions'];labels={(i,j):(a,b) for i,j,a,b in assignment['labels']};orientations={tuple(q[:3]):q[3] for q in assignment['orientations']};values={}
  for i,key in enumerate(self.variables,1):
   if key[0]=='before':values[i]=positions[key[1]]<positions[key[2]]
   elif key[0] in ['cap_ge','cup_ge']:values[i]=labels[key[1:3]][0 if key[0]=='cap_ge' else 1]>=key[3]
   elif key[0]=='orientation':values[i]=orientations[key[1:]]
   else:
    a,b,c,d=key[1:];x,y,z,w=[orientations[t] for t in [(a,b,c),(a,b,d),(a,c,d),(b,c,d)]];values[i]=sum([not w,z,not y,x])==2
  for index,clause in enumerate(self.clauses):assert any(values[abs(l)]==(l>0) for l in clause),(index,self.kinds[index],self.details[index])
  return len(self.clauses)

if __name__ == '__main__':
 encoded=CNF(record['support']);encoded.export(ROOT/'core-raw');print('EXPORTED',len(encoded.S),len(encoded.variables),len(encoded.clauses),collections.Counter(encoded.kinds),flush=True)
