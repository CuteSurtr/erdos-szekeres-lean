#!/usr/bin/env python3
"""Independent cut rows/truth/real controls; never imports a parent encoder."""
import hashlib,itertools as it,json,resource,sys,time,importlib.util,shutil
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parents[2]
R=E/'fourcuts14_audit'; D=R/'data'
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
K=('high','low','all_cup','all_cap')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def save(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n')
def desired(kind,left_count):
 return {'high':{2:True,1:False},'low':{2:False,1:True},'all_cup':{2:True,1:True},'all_cap':{2:False,1:False}}[kind][left_count]
def predicate(sign,m,k,kind):
 llr=[sign[a,b,c] for a,b in it.combinations(range(k),2) for c in range(k,m)]
 lrr=[sign[a,b,c] for a in range(k) for b,c in it.combinations(range(k,m),2)]
 if kind=='high':return all(llr) and not any(lrr)
 if kind=='low':return not any(llr) and all(lrr)
 if kind=='all_cup':return all(llr+lrr)
 return not any(llr+lrr)
def row_signs(m,k,kind):
 return [(t,not desired(kind,sum(v<k for v in t))) for t in it.combinations(range(m),3) if 0<sum(v<k for v in t)<3]
def truth(row,s):return any(s[t]==v for t,v in row)
def main():
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));start=time.monotonic();D.mkdir(exist_ok=True)
 base=W/'n7m14-exact.cnf';mp=W/'terminal7-a/m14/input.cnf.map';out=W/'n7m14-fourcuts.cnf';receipt=Path(str(out)+'.json')
 source=E/'augment_fourcuts14.py';geo=E/'highsplit_audit/tools/controls.py'
 inputs=[base,mp,out,receipt,source,geo,E/'low_split_audit/data/control-left13.json',E/'low_split/consequences/all_cap.md',E/'low_split/consequences/ROOTED_LEMMA.md',E/'allcuts14_audit/SHA256SUMS',E/'highsplit_audit/SHA256SUMS']
 before={str(p):sha(p) for p in inputs}
 assert before[str(base)]=='5dc0c1719cce7bda188abad8489534413ecbbcbe5f43e1b714244ec045a129c4'
 assert before[str(mp)]=='b81223d78761ab200ef5931cc33ab10821a3e3a2054c5e550d0d8da7cf0fa55e'
 assert before[str(out)]=='3c6c1f83e2cf426ca13eb2e9ba7e363a1da42f1138cc3b9503c57601678e5788'
 assert before[str(source)]=='964b349651920e44bafd66ea478a44e77d53bd1a8e2d616375c7c1061570114b'
 assert before[str(E/'allcuts14_audit/SHA256SUMS')]=='e77056a4121e68e6ff383e6545f8fe268ee6249de3edf0f12d82ee77d1eb07db'
 assert before[str(E/'highsplit_audit/SHA256SUMS')]=='dbf403074130a992c987858bb4112344099b43bcadf55e9078a394ebb9b34bef'
 assert any(line.split()[0]==sha(geo) and line.split()[-1]=='tools/controls.py' for line in (E/'highsplit_audit/SHA256SUMS').read_text().splitlines())
 ids={};nv=0
 for line in mp.open():
  if line.startswith('#'):continue
  raw,kind,mask=line.split();v=int(raw);assert v==nv+1;nv=v
  if kind=='orientation':ids[tuple(i for i in range(14) if int(mask)&(1<<i))]=v
 assert set(ids)==set(it.combinations(range(14),3)) and nv==32086
 rows=[];prov=[]
 for kind in K:
  for k in range(1,14):
   row=tuple(ids[t] if v else -ids[t] for t,v in row_signs(14,k,kind))
   assert len(row)==6*k*(14-k)
   if row not in rows:rows.append(row)
   prov.append(dict(kind=kind,cut=k,row_index=rows.index(row),literals=len(row)))
 assert len(rows)==48 and sum(map(len,rows))==10608
 rec=json.loads(receipt.read_text());assert rec['cuts']==prov
 for key,val in [('variables',32086),('base_clauses',231613),('added_clauses',48),('added_literals',10608),('m',14),('n',7)]:assert rec[key]==val
 for key,p in [('base',base),('map',mp),('output',out),('source',source)]:assert rec['hashes'][key]==before[str(p)]
 rebuilt=hashlib.sha256();counts=[0,0,0]
 with base.open('rb') as b,out.open('rb') as f:
  assert b.readline()==b'p cnf 32086 231613\n';header=b'p cnf 32086 231661\n';assert f.readline()==header;rebuilt.update(header)
  for line in b:
   assert f.readline()==line;rebuilt.update(line);counts[2]+=len(line)
   if not line.startswith(b'c') and line.strip():
    q=list(map(int,line.split()));assert q[-1]==0;counts[0]+=1;counts[1]+=len(q)-1
  comment=b'c conditional high/low/all-cup/all-cap cut exclusions; see receipt dependencies\n';assert f.readline()==comment;rebuilt.update(comment)
  for row in rows:
   line=(' '.join(map(str,row))+' 0\n').encode();assert f.readline()==line;rebuilt.update(line)
  assert f.read(1)==b''
 assert counts==[231613,623240,4104153] and rebuilt.hexdigest()==before[str(out)]
 old=W/'n7m14-allcuts.cnf';assert sha(old)=='01de4ba0c9831690f5e64a3592fd335ef701c100224060733e9734d55ac65554'
 tail=[];phase=False
 for line in old.open():
  if line.startswith('c conditional'):phase=True;continue
  if phase:tail.append(tuple(map(int,line.split()[:-1])))
 assert tail==rows[:37]
 boolcounts=dict(canonical=0,mixed_flips=0,pure_flips=0,exhaustive_small=0,omission_mutants=0,polarity_mutants=0)
 ts=list(it.combinations(range(14),3))
 for kind in K:
  for k in range(1,14):
   row=row_signs(14,k,kind);s={t:False for t in ts}
   for t,v in row:s[t]=not v
   assert predicate(s,14,k,kind) and not truth(row,s);boolcounts['canonical']+=1
   for t in ts:
    s[t]=not s[t];mixed=0<sum(v<k for v in t)<3
    assert truth(row,s)==(not predicate(s,14,k,kind))==mixed
    boolcounts['mixed_flips' if mixed else 'pure_flips']+=1;s[t]=not s[t]
   t,v=row[0];s[t]=not s[t];assert not truth(row[1:],s) and truth(row,s);s[t]=not s[t];boolcounts['omission_mutants']+=1
   assert truth([(t,not v)]+row[1:],s);boolcounts['polarity_mutants']+=1
 for m in (4,5):
  triples=list(it.combinations(range(m),3))
  for bits in range(1<<len(triples)):
   s={t:bool(bits&(1<<i)) for i,t in enumerate(triples)}
   for kind in K:
    for k in range(1,m):
     assert truth(row_signs(m,k,kind),s)==(not predicate(s,m,k,kind));boolcounts['exhaustive_small']+=1
 spec=importlib.util.spec_from_file_location('own_frozen_geometry',geo);H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)
 cases=[]
 for n in (5,6,7):
  for a in range(2,n):
   for b in range(2,n):
    # Each block is a quadratic cup; a large negative slope applied to R
    # about a point in the gap makes both crossing triple types caps.
    P=[(2*i,2*i*i) for i in range(a)]
    P += [(2*(a+j),2*j*j-10000*(2*(a+j)-(2*a-1))) for j in range(b)]
    G=H.Geometry(P,n);s={t:d>0 for t,d in G.orient.items()}
    assert predicate(s,a+b,a,'all_cap') and not G.cap5 and not G.ngons
    assert G.chain(tuple(range(a)),1) and G.chain(tuple(range(a,a+b)),1)
    sels=[G.selector((1<<l)|(((1<<b)-1)<<a)) for l in range(a)]
    cases.append(dict(kind='two_nonsingleton_cups',cut=a,P=P,geometry=G.summary(),selections=sels))
 L=json.loads((E/'low_split_audit/data/control-left13.json').read_text())['P_left'];L=[tuple(p) for p in L]
 left=H.Geometry(L,7);assert not left.cap4 and not left.ngons
 def below(x):
  values=[Fraction(y0*(x1-x0)+(y1-y0)*(x-x0),x1-x0) for (x0,y0),(x1,y1) in it.combinations(L,2)]
  v=min(values);return (x,v.numerator//v.denominator-1)
 for side in ('left','right'):
  P=([below(L[0][0]-1)]+L) if side=='left' else (L+[below(L[-1][0]+1)])
  G=H.Geometry(P,7);k=1 if side=='left' else 13;s={t:d>0 for t,d in G.orient.items()}
  assert not G.cap5 and not G.ngons and predicate(s,14,k,'all_cap')
  if side=='left':A=((1<<13)-1)<<1
  else:
   ends={c for (a,b,c),d in left.orient.items() if d<0}
   B=next(mask for mask in range(1<<13) if left.chain(H.verts(mask),1) and all(mask&t for t in left.targets) and all(v in ends for v in H.verts(mask)[1:]))
   A=B|(1<<13)
  selector=G.selector(A);checks=[]
  for item in prov:
   row=rows[item['row_index']];vs={ids[t]:d>0 for t,d in G.orient.items()}
   actual=any(vs[abs(v)]==(v>0) for v in row);pred=predicate(s,14,item['cut'],item['kind']);assert actual==not_(pred)
   checks.append(dict(**item,predicate=pred,clause_satisfied=actual))
  cases.append(dict(kind='singleton_'+side,cut=k,P=P,geometry=G.summary(),selections=[selector],cut_checks=checks))
 after={str(p):sha(p) for p in inputs};assert before==after
 save(D/'controls.json',dict(status='PASS',label='COMPUTED',cases=cases,selections=sum(len(c['selections']) for c in cases),real_cut_comparisons=104))
 save(D/'result.json',dict(status='PASS',label='COMPUTED formula and controls; written projection separate',base=dict(variables=nv,clauses=counts[0],literals=counts[1],unchanged_body_bytes=counts[2]),added=dict(unique_rows=48,provenance_entries=52,literals=10608,new_distinct_from_prior=11,new_literals=2574),total=dict(variables=nv,clauses=231661,literals=633848),provenance=prov,boolean_controls=boolcounts,real_cases=len(cases),real_selections=sum(len(c['selections']) for c in cases),stable_inputs=True,input_sha256=before,rebuilt_sha256=rebuilt.hexdigest(),seconds=time.monotonic()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,limits=dict(AS_MiB=300,CPU_count=1,wall_seconds=20,cpu_seconds=19),proof_replay=False))
 for p,name in [(source,'producer.py.txt'),(receipt,'producer-receipt.json'),(E/'low_split/consequences/all_cap.md','all_cap.md.txt'),(E/'low_split/consequences/ROOTED_LEMMA.md','ROOTED_LEMMA.md.txt')]:shutil.copyfile(p,D/name)
 print(json.dumps(dict(status='PASS',rows=48,provenance=52,boolean=boolcounts,real_cases=len(cases),real_selections=sum(len(c['selections']) for c in cases),seconds=time.monotonic()-start)))
def not_(x):return not x
if __name__=='__main__':
 try:main()
 except Exception as e:
  D.mkdir(exist_ok=True);save(D/'failure.json',dict(status='FAIL',type=type(e).__name__,message=str(e)));raise
