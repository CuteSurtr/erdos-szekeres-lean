#!/usr/bin/env python3
"""Independent new instances, using only frozen own geometry/row helpers read-only."""
import datetime,hashlib,importlib.util,itertools as it,json,os,resource,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R.parents[1]
W=Path('/home/jay/research/data/delta3-codex-20261113/extension');S=W/'low-split-audit/n6'
M=int(sys.argv[1]);assert M in (10,11);D=R/'data'/f'left{M}';CASE=W/f'low{M}-n6-a'
CNF=W/f'low{M}-n6.cnf';MAP=Path(str(CNF)+'.map');CAKE=Path('/home/jay/.local/bin/cake_lpr')
EXPECTED={10:('2aac28f4cfbe8b9f99e2ee4959d2efe81f6b4f0ad26805b09f395cd17f24f026',
 'f8ac66d7eba2c854d31a3cb8bc8a390b11de28aeb136faf27e341b8c368338bd',
 '88af4259a7fd793ca30925b2cea6f129ad072f9778deb41e84a6c389089abd7e'),
 11:('1dcd40d44ed07b7f94d99c450636e0e15fa6eea57f5902cad519177c2f251d37',
 'a90cd99d30b32066f97b0312b8dcbc28c7ffd3c6bd99d1275e724daba0c682e0',
 'bbbdf07f9c2ba372f308ea07bbd974b3b43a02a254c1ac1a567a468c6a50f89e')}
def save(name,obj):
 with (D/name).open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def hashed(p):
 old=p.stat();h=hashlib.sha256();off=last=0
 with p.open('rb',buffering=0) as f:
  for b in iter(lambda:f.read(1<<20),b''):
   h.update(b);off+=len(b)
   if off-last>=64<<20:
    os.posix_fadvise(f.fileno(),last,off-last,os.POSIX_FADV_DONTNEED);last=off
  os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
 new=p.stat();assert (old.st_size,old.st_mtime_ns,old.st_ino)==(new.st_size,new.st_mtime_ns,new.st_ino)
 return dict(sha256=h.hexdigest(),bytes=old.st_size,mtime_ns=old.st_mtime_ns,inode=old.st_ino)
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);mod=importlib.util.module_from_spec(spec)
 sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
def geometry(rows,C,fixture):
 item=json.loads(fixture.read_text())['cases']['n6_old_real11'];assert item['m_left']==11
 P=item['P'][:M];G=C.Geometry(P,6);U=C.Geometry(C.low_join(P,6),6)
 assert not G.cap4 and not G.ngons and not U.cap5 and not U.ngons
 right=U.full^G.full;assert right.bit_count()==2 and not U.has_cap3[right]
 for s,d in U.turn.items():
  a=(s&G.full).bit_count();b=(s&right).bit_count()
  if (a,b)==(2,1):assert d<0
  if (a,b)==(1,2):assert d>0
 assert U.end4=={(b,r) for b in G.end3 for r in range(M,U.m)}
 assert set(U.targets)==set(G.targets)|{s|right for s in G.cap3}
 assert set(U.bad3)==set(G.cap3)|{rows.mask((a,b,r)) for a,b in it.combinations(range(M),2)
                                if b not in G.end3 for r in range(M,U.m)}
 op1=bytearray(1<<M);op2=bytearray(1<<M);thinnings=0
 for b in range(1<<M):
  vs=rows.verts(b);blue=G.full^b
  op1[b]=not G.has_cap3[b] and not G.T[blue] and all(v in G.end3 for v in vs[1:])
  op2[b]=not G.has_cap3[b] and not G.has_cap3[blue] and blue.bit_count()<=4
  if op1[b] and b.bit_count()>M-4:
   smaller=rows.mask(vs[:M-4]);assert not G.has_cap3[smaller] and not G.T[G.full^smaller]
   assert all(v in G.end3 for v in rows.verts(smaller)[1:]);thinnings+=1
 assert any(op1) and not any(op2) # At n6, two cups have total at most5+4.
 terminal=0
 for a in range(1<<U.m):
  actual=not U.forbidden[a] and not U.T[U.full^a]
  predicted=bool(op1[a&G.full] if a&right else op2[a&G.full])
  assert actual==predicted;terminal+=actual
 assert terminal==3*sum(op1)+sum(op2)
 values=[False]
 with MAP.open() as f:
  assert f.readline().startswith('#')
  for line in f:
   v,kind,sm=line.split();assert int(v)==len(values);values.append(G.value(kind,int(sm)))
 counts={};false={};phase=None
 with CNF.open() as f:
  f.readline()
  for line in f:
   if line.startswith('c phase '):phase=line.split()[2];continue
   row=list(map(int,line.split()));assert row.pop()==0;counts[phase]=counts.get(phase,0)+1
   if not any(values[abs(v)]==(v>0) for v in row):false[phase]=false.get(phase,0)+1
 assert not(set(false)-{'no_covered_cup_transversal','no_small_blue_two_cup_partition'})
 bounded=sum(op1[b] for b in range(1<<M) if b.bit_count()<=M-4)
 assert false.get('no_covered_cup_transversal',0)==bounded
 assert false.get('no_small_blue_two_cup_partition',0)==sum(op2)
 return dict(status='PASS',P_left=P,P_full=U.P,left=G.report(),full=U.report(),
  all_memberships_checked=1<<U.m,terminal_selectors=terminal,option1_all=sum(op1),option1_bounded=bounded,
  option2=sum(op2),thinnings=thinnings,canonical_rows_checked=sum(counts.values()),
  canonical_false_failure_rows=false,canonical_nonfailure_all_true=True,
  first_option1=rows.verts(next(b for b in range(1<<M) if op1[b])),
  exact_target_bad3_End4_families_checked=True,parent_expected_geometry_ignored=True)
def replay():
 cmd=[str(CAKE),'--CML_HEAP_SIZE=128','--CML_STACK_SIZE=32',str(CASE/'input.cnf'),str(CASE/'proof.blrat')]
 save('cake-command.json',cmd);fds=[os.open(CASE/x,os.O_RDONLY) for x in ('input.cnf','proof.blrat')]
 for fd in fds:os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED)
 start=time.monotonic();last=start;releases=0
 with (D/'cake.stdout').open('x') as out,(D/'cake.stderr').open('x') as err:
  p=subprocess.Popen(cmd,stdout=out,stderr=err)
  try:
   while p.poll() is None:
    now=time.monotonic();assert now-start<17,'cake deadline17sec'
    if now-last>=1:
     for fd in fds:os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED)
     last=now;releases+=1
    time.sleep(.025)
  except BaseException:
   p.terminate()
   try:p.wait(timeout=.5)
   except subprocess.TimeoutExpired:p.kill();p.wait()
   raise
  finally:
   for fd in fds:os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED);os.close(fd)
 usage=resource.getrusage(resource.RUSAGE_CHILDREN)
 result=dict(returncode=p.returncode,seconds=time.monotonic()-start,peak_RSS_KiB=usage.ru_maxrss,
  user_seconds=usage.ru_utime,system_seconds=usage.ru_stime,periodic_cache_release_rounds=releases,
  exact_acceptance_line=(D/'cake.stdout').read_text().splitlines()==['s VERIFIED UNSAT'])
 save('cake-result.json',result);assert p.returncode==0 and result['exact_acceptance_line'];return result
def main():
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));start=time.monotonic();D.mkdir(parents=True,exist_ok=False);S.mkdir(parents=True,exist_ok=True)
 source=E/'low_split_cnf.cpp';compact=E.parents[1]/'compact/compact_cnf.cpp'
 helpers=[R.parent/'tools/rows.py',R.parent/'tools/controls.py'];fixture=E/'structure2/data/low_classification_replay.json'
 inputs=[CNF,MAP,CASE/'input.cnf',CASE/'proof.blrat',CASE/'proof.blrat.zst',CASE/'result.json',CAKE,source,compact,fixture,*helpers]
 before={str(p):hashed(p) for p in inputs};save('hashes-before.json',before)
 assert before[str(CNF)]['sha256']==before[str(CASE/'input.cnf')]['sha256']==EXPECTED[M][0]
 assert before[str(CASE/'proof.blrat')]['sha256']==EXPECTED[M][1]
 assert before[str(CASE/'proof.blrat.zst')]['sha256']==EXPECTED[M][2]
 assert before[str(CAKE)]['sha256']=='c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54'
 assert before[str(source)]['sha256']=='c7793f8d8a92c5230c38091bf23366e49ec037624085f8752405609c88a335c8'
 assert before[str(compact)]['sha256']=='1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553'
 manifest=dict(line.split('  ',1)[::-1] for line in (R.parent/'SHA256SUMS').read_text().splitlines())
 for p in helpers:assert before[str(p)]['sha256']==manifest[str(p.relative_to(R.parent))]
 receipt=json.loads((CASE/'result.json').read_text());save('parent-result.json',receipt)
 assert receipt['finished'] and receipt['status']=='UNSAT_CERTIFIED'
 assert all(receipt['hashes'][name]==before[str(CASE/name)]['sha256'] for name in ('input.cnf','proof.blrat','proof.blrat.zst'))
 rows=load('rows',helpers[0]);rows.S=S
 C=load('own_low_controls',helpers[1])
 formula=rows.check(CNF,M,6,'direct',f'n6-left{M}');save('formula.json',formula)
 assert (formula['variables'],formula['clauses'])=={10:(592,6522),11:(968,11298)}[M]
 control=geometry(rows,C,fixture);save('geometry.json',control)
 # Formula/geometry work ends before cake starts; no concurrent own check.
 cake=replay()
 after={str(p):hashed(p) for p in inputs};save('hashes-after.json',after);assert before==after
 result=dict(status='PASS',label='CERTIFIED',n=6,left_m=M,fresh_independent_replay=True,
  cnf_sha256=EXPECTED[M][0],proof_sha256=EXPECTED[M][1],formula=formula,geometry=control,cake=cake,
  stable_inputs=True,AS_MiB=300,heap_MiB=128,stack_MiB=32,CPU_count=1,
  total_seconds=time.monotonic()-start,own_peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  limits=Path('/proc/self/limits').read_text(),affinity=sorted(os.sched_getaffinity(0)),
  finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
 save('result.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('formula','geometry','limits')}))
if __name__=='__main__':
 try:main()
 except BaseException as e:
  if D.exists() and not(D/'failure.json').exists():save('failure.json',{'error':repr(e)})
  raise
