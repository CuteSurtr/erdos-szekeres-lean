#!/usr/bin/env python3
"""Find and replay a small propositional refutation; not itself cake/Lean."""
import argparse,hashlib,json,resource,time
from pathlib import Path
def solve(rows,assigned=None,tree=False):
 assigned={} if assigned is None else assigned.copy();units=[]
 while True:
  changed=False;remaining=[]
  for cid,C in rows:
   if any(abs(x) in assigned and assigned[abs(x)]==(x>0) for x in C):continue
   U=[x for x in C if abs(x) not in assigned]
   if not U:return False,{'units':units,'conflict':cid}
   if len(U)==1:
    x=U[0];assigned[abs(x)]=x>0;units.append({'literal':x,'reason':cid});changed=True
   remaining.append(U)
  if not changed:break
 if not remaining:return True,assigned
 clause=min(remaining,key=len);v=max((abs(x) for x in clause),key=lambda v:sum(any(abs(x)==v for x in C) for C in remaining))
 assigned[v]=True;sat,pos=solve(rows,assigned,tree)
 if sat:return True,pos
 assigned[v]=False;sat,neg=solve(rows,assigned,tree)
 if sat:return True,neg
 return False,{'units':units,'branch':v,'true':pos,'false':neg}
def replay(tree,rows,assigned=None):
 A={} if assigned is None else assigned.copy();nodes=1
 for unit in tree['units']:
  x=unit['literal'];C=rows[unit['reason']];assert abs(x) not in A and x in C
  assert all(abs(y) in A and A[abs(y)]!=(y>0) for y in C if y!=x)
  A[abs(x)]=x>0
 if 'conflict' in tree:
  assert all(abs(y) in A and A[abs(y)]!=(y>0) for y in rows[tree['conflict']]);return nodes,1
 v=tree['branch'];assert v not in A
 A[v]=True;nt,lt=replay(tree['true'],rows,A);A[v]=False;nf,lf=replay(tree['false'],rows,A);return nodes+nt+nf,lt+lf
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cnf',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20));a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic();rows=[];nv=nc=0
 for line in a.cnf.read_text().splitlines():
  if line.startswith('c') or not line.strip():continue
  if line.startswith('p'):
   _,_,v,c=line.split();nv,nc=int(v),int(c);continue
  row=list(map(int,line.split()));assert row[-1]==0;rows.append((len(rows)+1,row[:-1]))
 assert len(rows)==nc;table=dict(rows);current=[(i,C) for i,C in rows if not(len(C)==4 and all(x<0 for x in C))];sat,_=solve(current);assert not sat
 steps=[];witnesses={}
 for i,C in list(current):
  candidate=[row for row in current if row[0]!=i];sat,value=solve(candidate)
  if sat:
   witness={v:value.get(v,False) for v in range(1,nv+1)};assert all(any(witness[abs(x)]==(x>0) for x in R) for _,R in candidate);witnesses[i]=witness
  else:current=candidate
  steps.append({'removed_original_clause':i,'removed':not sat,'remaining':len(current)})
 sat,tree=solve(current,tree=True);assert not sat;nodes,leaves=replay(tree,dict(current))
 for i,C in current:
  witness=witnesses[i];assert all(any(witness[abs(x)]==(x>0) for x in R) for j,R in current if i!=j)
 core=a.out/'core.cnf';core.write_text(f'p cnf {nv} {len(current)}\n'+''.join(' '.join(map(str,C))+' 0\n' for _,C in current))
 (a.out/'tree.json').write_text(json.dumps(tree,indent=2)+'\n');(a.out/'deletion_trials.json').write_text(json.dumps(steps,indent=2)+'\n');(a.out/'irredundancy_models.json').write_text(json.dumps({str(i):witnesses[i] for i,C in current},indent=2)+'\n')
 out={'label':'COMPUTED exhaustive propositional tree and independent-style replay','variables':nv,'original_clauses':nc,'core_clauses':len(current),'original_clause_ids':[i for i,C in current],'tree_nodes':nodes,'leaves':leaves,'irredundant':True,'minimum_core_size_claimed':False,'seconds':round(time.monotonic()-start,3),'hashes':{'original_cnf':hashlib.sha256(a.cnf.read_bytes()).hexdigest(),'core.cnf':hashlib.sha256(core.read_bytes()).hexdigest(),'tree.json':hashlib.sha256((a.out/'tree.json').read_bytes()).hexdigest(),'script':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'scope':'Tree covers all Boolean assignments to the fixed core. Geometry remains a separate exact audit. No SAT status or solver trust substitutes for later cake/Lean replay.'}
 (a.out/'DONE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
