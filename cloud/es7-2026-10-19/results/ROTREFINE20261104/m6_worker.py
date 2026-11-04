#!/usr/bin/env python3
"""Bounded one-process CEGAR campaign with reconstructible durable inputs.

Every input is base.cnf followed by the explicitly recorded ordered cut blocks.
Only mathematically verified, exact54-tested blocks enter the incoming queue.
All command paths are supplied at runtime, never recorded in public metadata.
"""
import argparse, ctypes, datetime, hashlib, json, os, re, resource, shutil
import signal, sqlite3, struct, subprocess, sys, time
from pathlib import Path
sys.dont_write_bytecode = True

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

class DiskHashes:
 """Disposable exact SHA-256 membership index with a bounded page cache."""
 def __init__(self,path):
  if path.exists():path.unlink()
  self.db=sqlite3.connect(path)
  self.db.execute('PRAGMA journal_mode=OFF');self.db.execute('PRAGMA synchronous=OFF')
  self.db.execute('PRAGMA cache_size=-8192')
  self.db.execute('CREATE TABLE hashes (digest BLOB PRIMARY KEY) WITHOUT ROWID')
 def add(self,value):self.db.execute('INSERT OR IGNORE INTO hashes VALUES (?)',(value,))
 def __contains__(self,value):return self.db.execute('SELECT 1 FROM hashes WHERE digest=?',(value,)).fetchone() is not None
 def __len__(self):return self.db.execute('SELECT count(*) FROM hashes').fetchone()[0]
 def close(self):self.db.close()

class Campaign:
 def __init__(self,a):
  self.a=a;self.root=a.archive.resolve();self.root.mkdir(parents=True,exist_ok=True)
  self.script=Path(__file__).resolve().parent;self.child=None
  self.deadline=datetime.datetime.fromisoformat(a.deadline).timestamp()
  self.blocks=[];self.count=0;self.iteration=0
  self.seen=DiskHashes(self.root/'dedup_cache.sqlite') if a.dedup_sqlite else set()
  self.queued=set()
  self.start=time.monotonic();self.peak_gb=0.;self.peak_lane_bytes=0;self.stop_reason=None
  self.libproc=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True)
  (self.root/'worker.pid').write_text(str(os.getpid())+'\n')
  self.log=self.root/'events.jsonl'
  for d in ('models','cuts','iterations','incoming','proofs'): (self.root/d).mkdir(exist_ok=True)
 def event(self,event_type,**kw):
  row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':round(time.monotonic()-self.start,2),'event':event_type,**kw}
  line=json.dumps(row,sort_keys=True)+'\n'
  with self.log.open('a') as f:f.write(line)
  with (self.script/'logs/m6_campaign.jsonl').open('a') as f:f.write(line)
  print(line,end='',flush=True)
 def memory(self):
  out=subprocess.check_output(['vm_stat'],text=True)
  size=int(re.search(r'page size of (\d+)',out).group(1))
  names=['Pages active','Pages wired down','Pages occupied by compressor']
  pages=sum(int(re.search(re.escape(n)+r':\s+(\d+)',out).group(1)) for n in names)
  used=pages*size/1e9;self.peak_gb=max(self.peak_gb,used);return used
 def lane_memory(self):
  # SDK rusage_info_v0: UUID[16], then resident_size is uint64 field 6.
  def rss(pid):
   buffer=ctypes.create_string_buffer(96)
   rc=self.libproc.proc_pid_rusage(pid,0,ctypes.byref(buffer))
   if rc: return 0
   return struct.unpack_from('Q',buffer.raw,64)[0]
  used=rss(os.getpid())+(rss(self.child.pid) if self.child else 0)
  self.peak_lane_bytes=max(self.peak_lane_bytes,used);return used
 def stopchild(self):
  if self.child and self.child.poll() is None:
   os.killpg(self.child.pid,signal.SIGTERM)
   try:self.child.wait(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(self.child.pid,signal.SIGKILL);self.child.wait()
  self.child=None
 def run(self,args,log,limit=300,solver=False):
  if time.time()>=self.deadline:raise TimeoutError('hard deadline')
  used=self.memory()
  if used>=29:raise MemoryError('total memory guard before process')
  start=time.monotonic();reason=None
  with log.open('wb') as f:
   self.child=subprocess.Popen([str(x) for x in args],stdout=f,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'})
   while self.child.poll() is None:
    time.sleep(.5)
    if time.time()>=self.deadline:reason='hard_deadline';break
    if time.monotonic()-start>=limit:reason='time_limit';break
    if self.memory()>=29:reason='total_memory_guard';break
    if self.lane_memory()>2500000000:reason='lane_memory_guard';break
   if reason:self.stopchild();rc=None
   else:rc=self.child.returncode;self.child=None
  self.event('process_finished',role='solver' if solver else 'verification',log=str(log.relative_to(self.root)),returncode=rc,stop_reason=reason,seconds=round(time.monotonic()-start,2),peak_total_gb=round(self.peak_gb,3),peak_lane_rss_bytes=self.peak_lane_bytes,max_child_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
  if reason=='hard_deadline':raise TimeoutError(reason)
  if reason in ('total_memory_guard','lane_memory_guard'):raise MemoryError(reason)
  if not solver and (reason or rc!=0):raise RuntimeError('verification failed: '+str(log.relative_to(self.root)))
  return rc,reason
 def helper(self,name,args,log,limit=180):return self.run([sys.executable,'-I',self.script/name,*args],log,limit)
 def compress(self,path):
  dest=path.with_name(path.name+'.zst')
  self.run(['zstd','-q','-f','-T1','-3',path,'-o',dest],self.root/'compression.log',90)
  p=subprocess.Popen(['zstd','-q','-d','-c',dest],stdout=subprocess.PIPE);h=hashlib.sha256()
  for b in iter(lambda:p.stdout.read(1<<20),b''):h.update(b)
  assert p.wait()==0 and h.hexdigest()==sha(path)
  return {'path':str(path.relative_to(self.root)),'sha256':h.hexdigest(),'compressed_sha256':sha(dest),'decompression_roundtrip':True}
 def prepare(self):
  if self.a.resume:
   self.blocks=json.loads((self.root/'cut_prefix.json').read_text())
   self.base_sha=sha(self.root/'base.cnf')
   assert self.base_sha=='7889860ea9c629e9a00d8f1523ecfaaa6e02d615d88853b7695c6ab1985c50d6'
   for block in self.blocks:
    assert sha(self.root/block['path'])==block['sha256']
    if block['evidence'].startswith('incoming/'):self.queued.add(block['evidence'])
   with (self.root/'current.cnf').open('rb') as f:
    _,_,nv,nc=f.readline().split();self.nv=int(nv);self.count=int(nc)
    for line in f:self.seen.add(hashlib.sha256(line).digest())
   assert self.count==3381621+sum(b['clauses'] for b in self.blocks)
   # Independently reconstruct the entire expected prefix before resuming.
   expected=hashlib.sha256(f'p cnf {self.nv} {self.count}\n'.encode())
   with (self.root/'base.cnf').open('rb') as f:
    f.readline()
    for data in iter(lambda:f.read(1<<20),b''):expected.update(data)
   for block in self.blocks:
    with (self.root/block['path']).open('rb') as f:
     for data in iter(lambda:f.read(1<<20),b''):expected.update(data)
   assert sha(self.root/'current.cnf')==expected.hexdigest()
   self.model=max((self.root/'models').glob('model*.json'))
   self.model_index=int(self.model.stem[5:])
   self.iteration=1+max(int(p.name[4:]) for p in (self.root/'iterations').glob('step*'))
   self.event('resumed',base_sha256=self.base_sha,clauses=self.count,blocks=len(self.blocks),deadline_utc=self.a.deadline,next_step=self.iteration)
   return
  prior=self.a.previous_archive
  assert not (self.root/'base.cnf').exists(), 'existing campaign requires --resume'
  files=[('family_run3/instance.cnf','base.cnf','7889860ea9c629e9a00d8f1523ecfaaa6e02d615d88853b7695c6ab1985c50d6'),('family_run3/model.json','models/model0000.json','437144235bdaf2045f30767432d7453a2199bb608fee49257dfb51554db9789d'),('base.cnf.json','base.cnf.json','f053fbdf5682ebb444f287ef52ec323d3e5d30214f17f8e12ef1f0087c921114')]
  records=[]
  for src,dst,expected in files:
   p=self.root/dst;shutil.copyfile(prior/src,p);assert sha(p)==expected
   records.append(self.compress(p))
  (self.root/'base_manifest.json').write_text(json.dumps(records,indent=2)+'\n')
  base=self.root/'base.cnf'
  with base.open('rb') as f:
   _,_,nv,nc=f.readline().split();self.nv=int(nv);self.count=int(nc)
   for line in f:self.seen.add(hashlib.sha256(line).digest())
  shutil.copyfile(base,self.root/'current.cnf');self.base_sha=sha(base)
  self.model=self.root/'models/model0000.json';self.model_index=0
  self.event('prepared',base_sha256=self.base_sha,base_clauses=self.count,variables=self.nv,deadline_utc=self.a.deadline,initial_model_sha256=sha(self.model),base_unique_line_hashes=len(self.seen))
 def append_block(self,source,kind,evidence):
  idx=len(self.blocks)+1;target=self.root/f'cuts/block{idx:04d}.clauses';added=0
  with target.open('wb') as out,source.open('rb') as f:
   for line in f:
    ll=list(map(int,line.split()));assert ll[-1]==0 and all(0<abs(x)<=self.nv for x in ll[:-1])
    canonical=(' '.join(map(str,sorted(set(ll[:-1]),key=lambda x:(abs(x),x))))+' 0\n').encode()
    digest=hashlib.sha256(canonical).digest()
    if digest not in self.seen:self.seen.add(digest);out.write(canonical);added+=1
  if not added:target.unlink();self.event('block_redundant',kind=kind);return 0
  entry={**self.compress(target),'clauses':added,'kind':kind,'evidence':evidence};self.blocks.append(entry);self.count+=added
  # Previous formulas remain exactly reconstructible from immutable base/prefix.
  tmp=self.root/'current.next.cnf'
  with tmp.open('wb') as out:
   out.write(f'p cnf {self.nv} {self.count}\n'.encode())
   with (self.root/'base.cnf').open('rb') as f:f.readline();shutil.copyfileobj(f,out)
   for block in self.blocks:
    with (self.root/block['path']).open('rb') as f:shutil.copyfileobj(f,out)
  tmp.replace(self.root/'current.cnf')
  (self.root/'cut_prefix.json').write_text(json.dumps(self.blocks,indent=2)+'\n')
  self.event('block_added',**entry,total_clauses=self.count);return added
 def incoming(self):
  added=0
  for manifest in sorted((self.root/'incoming').glob('*/approved.json')):
   key=str(manifest.relative_to(self.root))
   if key in self.queued:continue
   spec=json.loads(manifest.read_text());source=manifest.parent/spec['clauses']
   assert spec['approved'] is True and sha(source)==spec['sha256']
   added+=self.append_block(source,spec['kind'],key);self.queued.add(key)
  return added
 def assess(self,folder):
  self.helper('m6_verify_assignment.py',['--cnf',self.root/'current.cnf','--model',self.model,'--out',folder/'assignment.json'],folder/'assignment.log')
  self.helper('m6_full_gp.py',['--model',self.model,'--checker',self.a.checker,'--out',folder/'gp','--max-output','100000'],folder/'gp.log')
  data=json.loads((folder/'gp/full_gp_check.json').read_text());n=int(re.search(r'violated (\d+)',data['verdict']).group(1))
  self.event('candidate_assessed',model=str(self.model.relative_to(self.root)),model_sha256=sha(self.model),gp_violations=n,formula_sha256=sha(self.root/'current.cnf'),clauses=self.count)
  if n:
   self.helper('m6_gp_refine.py',['--model',self.model,'--violations',folder/'gp/full_gp_violations.txt','--out',folder/'gp_cuts'],folder/'gp_cuts.log',300)
   return self.append_block(folder/'gp_cuts/gp_refinement.clauses','GP identity',str((folder/'gp_cuts/gp_refinement_verified.json').relative_to(self.root)))
  # Let independent linear separation see every GP-consistent candidate first.
  self.event('gp_consistent_survivor',model=str(self.model.relative_to(self.root)),model_sha256=sha(self.model))
  if self.incoming():return 1
  binary=self.root/'m6_full_products'
  validation=json.loads((self.root/'full_product_model0033/full/verified.json').read_text())
  assert sha(binary)==validation['binary_sha256']
  self.helper('m6_full_products.py',['--model',self.model,'--binary',binary,'--out',folder/'full_product','--deadline',self.a.deadline,'--full-only'],folder/'full_product.log',130)
  full=json.loads((folder/'full_product/full/verified.json').read_text())
  self.event('full_product_graph',model=str(self.model.relative_to(self.root)),acyclic=full['acyclic'],identities=full['identities'],edges=full['edges_with_multiplicity'],evidence=str((folder/'full_product/full/verified.json').relative_to(self.root)))
  if full['acyclic']:return 0
  # Prefer a small witness for complete family lifting when a global cycle exists.
  self.helper('m6_product_cycles.py',['--model',self.model,'--map',self.root/'base.cnf.json','--out',folder/'cycle','--max-seconds','90','--max-layers','3'],folder/'cycle.log',110)
  witness=folder/'cycle/m6_cycle_witness.json'
  if not witness.exists():
   witness=folder/'full_product/full/m6_cycle_witness.json'
   data=json.loads(witness.read_text());layers={x//6 for row in data['comparisons'] for x in row['anchor_quintuple']}
   if len(layers)>3:
    self.event('nonlocal_cycle_requires_review',model=str(self.model.relative_to(self.root)),layers=sorted(layers),witness=str(witness.relative_to(self.root)))
    return 0
  self.helper('m6_verify_cycle.py',['--model',self.model,'--witness',witness,'--output',folder/'cycle/verified.json'],folder/'cycle_verify.log',180)
  self.helper('m6_embed_cycle.py',['--model',self.model,'--witness',witness,'--out',folder/'cycle_family'],folder/'cycle_family.log',240)
  return self.append_block(folder/'cycle_family/family.clauses','rotational product cycle family',str((folder/'cycle_family/family_verified.json').relative_to(self.root)))
 def solve(self,folder):
  composition={'base_sha256':self.base_sha,'blocks':[{'path':b['path'],'sha256':b['sha256']} for b in self.blocks],'variables':self.nv,'clauses':self.count,'cnf_sha256':sha(self.root/'current.cnf')}
  record_proof=self.a.proof_always or (self.root/'RECORD_PROOFS').exists()
  attempt_proof=folder/'attempt.lrat'
  options=['--seed='+str(self.iteration)]+(['--lrat','--binary=false'] if record_proof else [])
  composition['solver_options']=options
  if record_proof:composition['proof_path']=str(attempt_proof.relative_to(self.root))
  (folder/'input.json').write_text(json.dumps(composition,indent=2)+'\n')
  solve_seconds=min(300,max(1,self.deadline-time.time()-30))
  rc,reason=self.run([self.a.cadical,*options,self.root/'current.cnf',*([attempt_proof] if record_proof else [])],folder/'solver.log',solve_seconds,True)
  txt=(folder/'solver.log').read_text()
  if rc==20 or 's UNSATISFIABLE' in txt:
   self.event('UNSAT',input=str((folder/'input.json').relative_to(self.root)),retained_proof=str(attempt_proof.relative_to(self.root)) if record_proof else None)
   final=self.root/'proofs/unsat.cnf';shutil.copyfile(self.root/'current.cnf',final);self.compress(final)
   if record_proof:
    assert attempt_proof.exists()
    self.event('proof_retained',path=str(attempt_proof.relative_to(self.root)),sha256=sha(attempt_proof),status='UNSAT trace; independent replay required')
    self.stop_reason='UNSAT; retained LRAT requires independent replay';return False
   proof=self.root/'proofs/unsat.lrat'
   remain=max(1,self.deadline-time.time()-3)
   prc,preason=self.run([self.a.cadical,'--seed='+str(self.iteration),'--lrat','--binary=false',final,proof],self.root/'proofs/lrat_solver.log',remain,True)
   if proof.exists():self.compress(proof)
   self.event('proof_attempt',returncode=prc,stop_reason=preason,proof_present=proof.exists());self.stop_reason='UNSAT; proof requires independent replay';return False
  if rc==10 or 's SATISFIABLE' in txt:
   if record_proof and attempt_proof.exists():self.event('noncertificate_trace',path=str(attempt_proof.relative_to(self.root)),sha256=sha(attempt_proof),status='SAT trace; not an UNSAT certificate')
   vals=[]
   for line in txt.splitlines():
    if line.startswith('v '):vals.extend(int(x) for x in line[2:].split() if int(x)>0)
   assert vals
   self.model_index+=1;self.model=self.root/f'models/model{self.model_index:04d}.json';self.model.write_text(json.dumps(sorted(vals))+'\n');record=self.compress(self.model)
   self.event('SAT',**record,input=str((folder/'input.json').relative_to(self.root)));return True
  if record_proof and attempt_proof.exists():self.event('noncertificate_trace',path=str(attempt_proof.relative_to(self.root)),sha256=sha(attempt_proof),status='UNKNOWN trace; not an UNSAT certificate')
  self.event('UNKNOWN',reason=reason,returncode=rc,input=str((folder/'input.json').relative_to(self.root)));return None
 def execute(self):
  try:
   self.prepare();need_assess=(not self.a.resume or self.a.resume_assess);idle_since=None
   while time.time()<self.deadline:
    folder=self.root/f'iterations/step{self.iteration:04d}';folder.mkdir(exist_ok=True)
    added=self.assess(folder) if need_assess else 0
    added+=self.incoming()
    if need_assess and not added:
     self.event('awaiting_verified_separation',model=str(self.model.relative_to(self.root)))
     idle_since=time.monotonic()
     while time.time()<self.deadline and not added:
      time.sleep(2);added=self.incoming()
      if time.monotonic()-idle_since>300:
       self.event('separation_pending',model=str(self.model.relative_to(self.root)))
       idle_since=time.monotonic()
    if self.deadline-time.time()<31:
     self.stop_reason='final assessment margin reached';return
    result=self.solve(folder)
    if result is False:return
    need_assess=result is True;self.iteration+=1
   self.stop_reason='hard deadline'
  except (TimeoutError,MemoryError,RuntimeError,AssertionError) as exc:
   self.stop_reason=type(exc).__name__+': '+str(exc);self.event('stopped',reason=self.stop_reason)
  except KeyboardInterrupt:
   self.stop_reason='interrupted for controlled continuation';self.event('stopped',reason=self.stop_reason)
  finally:
   self.stopchild()
   if isinstance(self.seen,DiskHashes):self.seen.close()
   final={'stop_reason':self.stop_reason,'last_model':str(self.model.relative_to(self.root)) if hasattr(self,'model') else None,'last_model_sha256':sha(self.model) if hasattr(self,'model') else None,'cut_blocks':len(self.blocks),'clauses':self.count,'peak_total_gb':round(self.peak_gb,3),'peak_lane_rss_bytes':self.peak_lane_bytes,'elapsed_seconds':round(time.monotonic()-self.start,2),'all_children_reaped':True}
   (self.root/'status.json').write_text(json.dumps(final,indent=2)+'\n');self.event('finished',**final)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--previous-archive',type=Path,required=True);ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--cadical',type=Path,required=True);ap.add_argument('--checker',type=Path,required=True);ap.add_argument('--deadline',required=True);ap.add_argument('--resume',action='store_true');ap.add_argument('--resume-assess',action='store_true');ap.add_argument('--dedup-sqlite',action='store_true');ap.add_argument('--proof-always',action='store_true');Campaign(ap.parse_args()).execute()
if __name__=='__main__':main()
