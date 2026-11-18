#!/usr/bin/env python3
"""Independent compact16 anchor and exact long-cup append; own frozen helpers only."""
import hashlib,importlib.util,itertools as it,json,os,resource,sys,time
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R.parents[1];D=R/'data'
W=Path('/home/jay/research/data/delta3-codex-20261113/extension');S=W/'low-split-audit/left16-longcup'
FILES={'base':W/'low16-n7-compact.cnf','base_map':W/'low16-n7-compact.cnf.map',
 'output':W/'low16-n7-longcup.cnf','output_map':W/'low16-n7-longcup.cnf.map','source':E/'augment_left16_longcup.py'}
EXPECTED={'base':'2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8',
 'base_map':'46dfc8217a63d6c4a34ed65316443aff990702e3505f0791c540e67ed52cc220',
 'output':'f23af9d7113dac3f9e4414298b20fb08d8181c279804d36b79e98a66755622b4',
 'output_map':'c4e2ec5444906df0e7dbe80e2cb2846d6e38a52ed4c7af6e3c746dcef93049bb',
 'source':'168c016a00338dfa2ae0f40129c6af31ce81f13b21a4a82d40d61fd990ecb3f0'}
def save(name,o):
 with (D/name).open('x') as f:json.dump(o,f,indent=2);f.write('\n')
def sha(p):
 old=p.stat();h=hashlib.sha256();off=last=0
 with p.open('rb',buffering=0) as f:
  for b in iter(lambda:f.read(1<<20),b''):
   h.update(b);off+=len(b)
   if off-last>=64<<20:os.posix_fadvise(f.fileno(),last,off-last,os.POSIX_FADV_DONTNEED);last=off
  os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
 new=p.stat();assert (old.st_size,old.st_mtime_ns,old.st_ino)==(new.st_size,new.st_mtime_ns,new.st_ino)
 return h.hexdigest()
def load(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def verts(s):return tuple(i for i in range(s.bit_length()) if s>>i&1)
def mask(vs):return sum(1<<v for v in vs)
def gate(z,children):return [(-z,t) for t in children]+[(z,*[-t for t in children])]
def holds(row,values):return any(values[abs(v)]==(v>0) for v in row)
def sec(a,b,x):return Fraction(a[1]*(b[0]-a[0])+(b[1]-a[1])*(x-a[0]),b[0]-a[0])
def high(P,Q):
 shift=P[-1][0]+4-Q[0][0];Q=[(x+shift,y) for x,y in Q]
 thresholds=[sec(a,b,x)-y for x,y in Q for a,b in it.combinations(P,2)]
 thresholds += [y-sec(a,b,x) for x,y in P for a,b in it.combinations(Q,2)]
 h=max([Fraction(0)]+thresholds);h=h.numerator//h.denominator+1
 return P+[(x,y+h) for x,y in Q]
def controls(ids,masks,rows_helper):
 helper=E/'highsplit_audit/tools/controls.py';hm=dict(x.split('  ',1)[::-1] for x in (E/'highsplit_audit/SHA256SUMS').read_text().splitlines())
 assert sha(helper)==hm['tools/controls.py'];H=load('own_exact_high',helper)
 c3=[(i,-i*i) for i in range(3)];u3=[(i,i*i) for i in range(3)];u4=[(i,i*i) for i in range(4)];u5=[(i,i*i) for i in range(5)]
 P10=high(high(c3,u3),u4);P15=high(P10,u5);small=[]
 for name,P in [('cup_max4',P10),('cup_max5',P15)]:
  G=H.Geometry(P,7);assert not G.cap4 and not G.ngons;maximum=max(G.beta);assert maximum in (4,5)
  brute=[1]*G.m
  for s in range(1,1<<G.m):
   vv=verts(s)
   if G.chain(vv,1):brute[vv[-1]]=max(brute[vv[-1]],len(vv))
  assert brute==G.beta
  B=0 if maximum<=4 else mask(i for i,b in enumerate(G.beta) if b==5)
  end3={t[-1] for t,d in G.orient.items() if d<0}
  assert G.chain(verts(B),1) and all(B&t for t in G.targets)
  assert all(v in end3 for v in verts(B)[1:])
  assert not any(G.chain(q,1) for q in it.combinations(range(G.m),6))
  small.append({'name':name,'P':P,'geometry':G.summary(),'B':list(verts(B)),'End3':sorted(end3),'T7_option1_verified':True})
 fixture=E/'structure2/data/low_classification_replay.json';fh=sha(fixture)
 P=json.loads(fixture.read_text())['cases']['n7_fixed_left16']['P'][:16]
 G=H.Geometry(P,7);assert not G.cap4 and not G.ngons and max(G.beta)==6
 values={v:G.orient[t]>0 for t,v in ids.items()};trueflags=[];checked=0
 for offset,s in enumerate(masks,1):
  z=128297+offset;children=tuple(v for t,v in ids.items() if all(s>>a&1 for a in t))
  values[z]=G.chain(verts(s),1)
  assert all(holds(row,values) for row in gate(z,children));checked+=21
  if values[z]:trueflags.append(z)
 final=tuple(range(128298,136306));assert holds(final,values) and trueflags
 # Explicitly verify the positive T7 witness in this actual16-point control.
 end3={t[-1] for t,d in G.orient.items() if d<0};witness=None
 for s in range(1<<16):
  vv=verts(s)
  if G.chain(vv,1) and all(v in end3 for v in vv[1:]) and all(s&t for t in G.targets):witness=vv;break
 assert witness is not None
 assert fh==sha(fixture)
 return {'status':'PASS','rank_lemma_controls':small,'actual16':{'P':P,'geometry':G.summary(),
  'true_sixcup_flags':len(trueflags),'new_rows_canonical_true':checked+1,'T7_option1':list(witness),
  'first_sixcup':list(verts(masks[trueflags[0]-128298]))},'fixture_sha256':fh,'geometry_helper_sha256':sha(helper)}
def main():
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));start=time.monotonic();S.mkdir(exist_ok=False)
 before={k:sha(p) for k,p in FILES.items()};save('hashes-before.json',before);assert before==EXPECTED
 receipt_path=Path(str(FILES['output'])+'.json');receipt=json.loads(receipt_path.read_text());assert receipt['hashes']==EXPECTED
 assert (receipt['old_variables'],receipt['old_clauses'],receipt['new_variables'],receipt['added_clauses'],receipt['added_literals'])==(128297,903593,8008,168169,496496)
 manifest=dict(x.split('  ',1)[::-1] for x in (R.parent/'SHA256SUMS').read_text().splitlines())
 helper=R.parent/'tools/rows.py';assert sha(helper)==manifest['tools/rows.py'];rows=load('rows',helper);rows.S=S
 assert sha(E/'low_split_compact.cpp')=='1fb043a5d29fa86047ba05cae86fdfb248e6069bc6731c4ee39c181737319303'
 assert sha(E.parents[1]/'compact/compact_cnf.cpp')=='1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553'
 base=rows.check(FILES['base'],16,7,'compact','base16');save('base-instance.json',base)
 assert (base['variables'],base['clauses'])==(128297,903593)
 ids={};nv=0
 for line in FILES['base_map'].open():
  if line.startswith('#'):continue
  v,kind,s=line.split();v=int(v);assert v==nv+1;nv=v
  if kind=='orientation':ids[verts(int(s))]=v
 assert ids=={t:v for v,t in enumerate(it.combinations(range(16),3),1)}
 masks=sorted((s for s in range(1<<16) if s.bit_count()==6),key=verts);assert len(masks)==len(set(masks))==8008
 cnf_hash=hashlib.sha256();bodybytes=0;newrows=newlits=gate_checks=0
 with FILES['base'].open('rb') as f,FILES['output'].open('rb') as g:
  assert f.readline().split()==[b'p',b'cnf',b'128297',b'903593']
  header=b'p cnf 136305 1071762\n';assert g.readline()==header;cnf_hash.update(header)
  for line in f:assert g.readline()==line;cnf_hash.update(line);bodybytes+=len(line)
  marker=b'c real T7 failure implies existence of a six-cup\n';assert g.readline()==marker;cnf_hash.update(marker)
  for offset,s in enumerate(masks,1):
   z=nv+offset;children=tuple(v for t,v in ids.items() if all(s>>a&1 for a in t));assert len(children)==len(set(children))==20
   definition=gate(z,children)
   for row in definition:
    line=(' '.join(map(str,row))+' 0\n').encode();assert g.readline()==line;cnf_hash.update(line);newrows+=1;newlits+=len(row)
   # Gate truth controls: true, every single false child, and all false;
   # both flag values. All gates are also checked literally above.
   patterns=[(),*[(v,) for v in children],children]
   for falsechildren in patterns:
    vals={v:v not in falsechildren for v in children};expected=not falsechildren
    for value in (False,True):
     vals[z]=value;assert all(holds(r,vals) for r in definition)==(value==expected);gate_checks+=1
  final=tuple(range(nv+1,nv+8009));line=(' '.join(map(str,final))+' 0\n').encode()
  assert g.readline()==line and not g.read(1);cnf_hash.update(line);newrows+=1;newlits+=len(final)
 assert (newrows,newlits)==(168169,496496) and cnf_hash.hexdigest()==EXPECTED['output']
 mp_hash=hashlib.sha256();mapbytes=0
 with FILES['base_map'].open('rb') as f,FILES['output_map'].open('rb') as g:
  for line in f:assert g.readline()==line;mp_hash.update(line);mapbytes+=len(line)
  assert line.endswith(b'\n')
  for offset,s in enumerate(masks,1):
   line=f'{nv+offset} six_cup {s}\n'.encode();assert g.readline()==line;mp_hash.update(line)
  assert not g.read(1)
 assert mp_hash.hexdigest()==EXPECTED['output_map']
 flags={z:False for z in final};assert not holds(final,flags)
 for z in (final[0],final[-1]):flags[z]=True;assert holds(final,flags);flags[z]=False
 real=controls(ids,masks,rows);save('real-controls.json',real)
 after={k:sha(p) for k,p in FILES.items()};assert after==before;save('hashes-after.json',after)
 for src,name in ((FILES['source'],'producer.py.txt'),(receipt_path,'producer-receipt.json')):
  with (D/name).open('xb') as f:f.write(src.read_bytes())
 result={'status':'PASS','label':'COMPUTED','n':7,'left_m':16,'base_full_row_map_rebuild':True,
  'base_variables':nv,'base_rows':base['clauses'],'base_literals':base['literals'],'base_body_bytes_unchanged':bodybytes,'base_map_bytes_unchanged':mapbytes,
  'new_variables':8008,'new_rows':newrows,'new_literals':newlits,'total_variables':136305,'total_rows':1071762,
  'total_literals':base['literals']+newlits,'gate_truth_assignments':gate_checks,'final_OR_controls':3,
  'hashes':after,'CNF_reconstruction_sha256':cnf_hash.hexdigest(),'map_reconstruction_sha256':mp_hash.hexdigest(),
  'seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  'limits':Path('/proc/self/limits').read_text(),'affinity':sorted(os.sched_getaffinity(0)),
  'proof_replayed':False,'propositional_equivalence_to_base_claimed':False}
 save('result.json',result);print(json.dumps({k:v for k,v in result.items() if k!='limits'}))
if __name__=='__main__':
 try:main()
 except BaseException as e:save('failure.json',{'error':repr(e)});raise
