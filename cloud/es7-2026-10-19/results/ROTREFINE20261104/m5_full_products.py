#!/usr/bin/env python3
"""Prepare, cross-check, and run the compact directed product-vertex checker.

Acyclicity exhausts this graph-cycle class only, not arbitrary positive
dependencies of logarithmic bracket inequalities or realizability.
"""
import argparse,hashlib,importlib.util,itertools,json,math,signal,sys,ctypes,datetime,os,subprocess,time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def triples(q):
 a,b,c,d,e=q
 return (((a,b,c),(a,d,e),1),((a,b,d),(a,c,e),-1),((a,b,e),(a,c,d),1))

class Guard:
 def __init__(self,deadline):
  self.child=None;self.deadline=datetime.datetime.fromisoformat(deadline).timestamp()
  here=Path(__file__).resolve().parent
  self.h=load(here.parent/'C6C7REVIEW/m5_pilot.py','memory_helpers')
  self.r=load(here/'m5_proof_lane.py','native_resource')
  self.lib=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True)
  self.lib.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p]
  self.lib.proc_pid_rusage.restype=ctypes.c_int
 def stopchild(self):
  if self.child and self.child.returncode is None:
   os.killpg(self.child.pid,signal.SIGKILL);self.child.wait()
  self.child=None
 def run(self,args,log,limit):
  start=time.monotonic();peak=0;reason=None;usage=None
  with log.open('w') as output:
   self.child=subprocess.Popen(args,stdout=output,stderr=subprocess.STDOUT,start_new_session=True)
   try:
    while True:
     pid,status,usage=os.wait4(self.child.pid,os.WNOHANG)
     if pid:self.child.returncode=os.waitstatus_to_exitcode(status);break
     used=self.h.memory_bytes();peak=max(peak,used)
     info=self.r.RUsageInfo();rc=self.lib.proc_pid_rusage(self.child.pid,0,ctypes.byref(info))
     if rc and ctypes.get_errno()!=3:reason='resource_monitor_error'
     if used>=29000000000 or info.resident_size>=3000000000:reason='memory_guard'
     if time.time()>=self.deadline or time.monotonic()-start>limit:reason='time_guard'
     if reason:self.stopchild();raise RuntimeError(reason)
     time.sleep(.1)
    code=self.child.returncode
   finally:self.stopchild()
  self.event('checker_process',log=log.name,returncode=code,wall_seconds=round(time.monotonic()-start,3),
             peak_rss_bytes=usage.ru_maxrss,system_peak_bytes=peak,child_stopped=True)
  if code:raise RuntimeError('product checker rejected input')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--model',type=Path,required=True);ap.add_argument('--known-cycle-model',type=Path)
 ap.add_argument('--full-only',action='store_true')
 ap.add_argument('--binary',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--deadline',required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 here=Path(__file__).resolve().parent;ref=load(here.parent/'C7UPPER/gen.py','reference');e=ref.Enc(5,8,12)
 assert all(e.tvar[q]==i+1 for i,q in enumerate(sorted(e.tvar)))
 search=load(here/'m5_product_cycles.py','python_search')
 guard=Guard(a.deadline)
 def event(kind,**kw):
  row={'event':kind,**kw};print(json.dumps(row),flush=True)
  with (a.out/'guard.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 guard.event=event;width=len(e.tvar)+1
 def case(label,model,layers,crosscheck):
  out=a.out/label;out.mkdir(exist_ok=True);pos=set(json.loads(model.read_text()))
  points=[5*o+k for o in layers for k in range(5)];anchors=[5*o for o in layers]
  def lit(q):
   v=e.o(*q);sg=(1 if v>0 else -1)*(1 if abs(v) in pos else -1);return sg*abs(v)
  table=[]
  for x in range(60):
   for y in range(60):
    for z in range(60):table.append(0 if len({x,y,z})<3 else lit((x,y,z)))
  inp=out/'input.txt';inp.write_text(f'60 {width} {len(points)} {len(anchors)}\n'+' '.join(map(str,points))+'\n'+' '.join(map(str,anchors))+'\n'+' '.join(map(str,table))+'\n')
  args=[a.binary.resolve(),inp.resolve()]+(['--dump'] if crosscheck else [])
  guard.run(args,out/'checker.log',120)
  lines=(out/'checker.log').read_text().splitlines();result=json.loads(lines[-1]);expected=len(anchors)*math.comb(len(points)-1,4)
  assert result['identities']==result['expected_identities']==expected and result['edges_with_multiplicity']==2*expected and result['all_identities_covered']
  result.update({'model_sha256':sha(model),'input_sha256':sha(inp),'binary_sha256':sha(a.binary),'source_sha256':sha(here/'m6_full_products.c'),'layers':layers,'rigor':'exact integer computation; no arbitrary final-polynomial or realizability conclusion'})
  if crosscheck:
   direct=[];graph={}
   for p in anchors:
    for rest in itertools.combinations([x for x in points if x!=p],4):
     q=(p,*rest);tt=triples(q);ll=[(lit(x),lit(y),co) for x,y,co in tt]
     signs=[co*(1 if x*y>0 else -1) for x,y,co in ll];assert len(set(signs))==2
     mi=next(j for j in range(3) if signs.count(signs[j])==1)
     pp=[min(abs(x),abs(y))*width+max(abs(x),abs(y)) for x,y,_ in ll]
     for j in range(3):
      if j!=mi:
       row=(*q,mi,j,pp[mi],pp[j]);direct.append(row);graph.setdefault(pp[mi],{})[pp[j]]=0
   dumped=[tuple(map(int,line.split()[1:])) for line in lines[:-1]]
   assert dumped==direct
   found=search.cycle(graph);assert bool(found)==(not result['acyclic'])
   result['direct_python_edges_compared']=len(direct);result['independent_python_dfs_agrees']=True
  comparisons=[];expo=Counter();products=[]
  for raw in reversed(result['cycle_backward']):
   q=tuple(raw['q']);tt=triples(q);ss=[co*(1 if lit(x)*lit(y)>0 else -1) for x,y,co in tt]
   mi=next(j for j in range(3) if ss.count(ss[j])==1);j=raw['other'];assert mi!=j
   def orbit(t):return e.canon[tuple(sorted(t))][0]
   pp=[min(abs(lit(x)),abs(lit(y)))*width+max(abs(lit(x)),abs(lit(y))) for x,y,_ in tt]
   assert raw['from']==pp[mi] and raw['to']==pp[j]
   greater=[orbit(t) for t in tt[mi][:2]];lesser=[orbit(t) for t in tt[j][:2]]
   for t in greater:expo[t]+=1
   for t in lesser:expo[t]-=1
   products.append((raw['from'],raw['to']))
   comparisons.append({'anchor_quintuple':q,'minority_term':mi,'other_term':j,'term_signs':ss,'greater_orbits':greater,'lesser_orbits':lesser,'weight':1})
  if comparisons:
   assert all(products[i][1]==products[(i+1)%len(products)][0] for i in range(len(products))) and all(v==0 for v in expo.values())
   witness={'m':5,'t':12,'model_sha256':sha(model),'scope':'realizations invariant under the specified Euclidean rotation','verified_exponent_cancellation':True,'comparisons':comparisons}
   (out/'m5_cycle_witness.json').write_text(json.dumps(witness,indent=2)+'\n');result['cycle_exactly_reverified']=True
  result['cycle_length']=len(comparisons)
  (out/'verified.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'case':label,'identities':expected,'acyclic':result['acyclic'],'cycle_length':len(comparisons)}),flush=True)
  return result
 def terminate(signum,frame):raise KeyboardInterrupt
 signal.signal(signal.SIGTERM,terminate)
 try:
  if not a.full_only:
   tests=[case('small_pair',a.model,[0,1],True),case('small_triple',a.model,[1,5,9],True)]
   (a.out/'selftests.json').write_text(json.dumps({'status':'PASS','direct_python_cases':2,'edges_compared':sum(t['direct_python_edges_compared'] for t in tests),'independent_python_dfs_agrees':True},indent=2)+'\n')
  case('full',a.model,list(range(12)),False)
 finally:guard.stopchild()
if __name__=='__main__':main()
