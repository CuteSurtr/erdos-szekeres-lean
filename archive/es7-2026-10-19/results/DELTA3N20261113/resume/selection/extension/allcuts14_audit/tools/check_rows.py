#!/usr/bin/env python3
"""Own cut reconstruction; no producer or previous checker import."""
import hashlib,itertools as it,json,os,resource,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R.parent
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
S=W/'allcuts14-audit';DATA=R/'data'
FILES={'base':W/'n7m14-exact.cnf','map':W/'terminal7-a/m14/input.cnf.map',
 'output':W/'n7m14-allcuts.cnf','source':E/'augment_allcuts14.py'}
EXPECTED={'base':'5dc0c1719cce7bda188abad8489534413ecbbcbe5f43e1b714244ec045a129c4',
 'map':'b81223d78761ab200ef5931cc33ab10821a3e3a2054c5e550d0d8da7cf0fa55e',
 'output':'01de4ba0c9831690f5e64a3592fd335ef701c100224060733e9734d55ac65554',
 'source':'d8979afcc2b2793f810f314821b4bb2d369c471d0771962f195140b56bd02c24'}
KINDS=('high','low','all_cup')
def save(name,obj):
 with (DATA/name).open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def sha(p):
 old=p.stat();h=hashlib.sha256();off=last=0
 with p.open('rb',buffering=0) as f:
  for b in iter(lambda:f.read(1<<20),b''):
   h.update(b);off+=len(b)
   if off-last>=64<<20:
    os.posix_fadvise(f.fileno(),last,off-last,os.POSIX_FADV_DONTNEED);last=off
  os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
 new=p.stat();assert (old.st_size,old.st_mtime_ns,old.st_ino)==(new.st_size,new.st_mtime_ns,new.st_ino)
 return h.hexdigest()
def rows(m):
 triples=list(it.combinations(range(m),3));out={}
 for kind in KINDS:
  for k in range(1,m):
   clause=[]
   for v,t in enumerate(triples,1):
    left=sum(a in range(k) for a in t)
    if left not in (1,2):continue
    positive={('high',1):True,('high',2):False,('low',1):False,('low',2):True,
              ('all_cup',1):False,('all_cup',2):False}[kind,left]
    clause.append(v if positive else -v)
   out[kind,k]=tuple(clause)
 return triples,out
def direct(signs,kind,k,m):
 # Quantify over the two Cartesian products; no left-count row builder.
 llr=[signs[a,b,c] for a,b in it.combinations(range(k),2) for c in range(k,m)]
 lrr=[signs[a,b,c] for a in range(k) for b,c in it.combinations(range(k,m),2)]
 if kind=='high':return all(llr) and not any(lrr)
 if kind=='low':return not any(llr) and all(lrr)
 return all(llr) and all(lrr)
def satisfied(clause,values):return any(values[abs(v)]==(v>0) for v in clause)
def truth_controls():
 counts={'canonical':0,'mixed_single_flips':0,'pure_single_flips':0,'exhaustive_small':0,'omission_mutants':0,'sign_mutants':0}
 triples,rr=rows(14);counter=[]
 for (kind,k),clause in rr.items():
  val={v:False for v in range(1,len(triples)+1)}
  val.update({abs(v):v<0 for v in clause})
  assert not satisfied(clause,val)
  assert direct({t:val[v] for v,t in enumerate(triples,1)},kind,k,14)
  counts['canonical']+=1
  for v in val:
   val[v]=not val[v]
   expected=v in set(map(abs,clause))
   assert satisfied(clause,val)==expected
   assert direct({t:val[w] for w,t in enumerate(triples,1)},kind,k,14)==(not expected)
   counts['mixed_single_flips' if expected else 'pure_single_flips']+=1
   val[v]=not val[v]
  v=abs(clause[0]);val[v]=not val[v]
  assert satisfied(clause,val) and not satisfied(clause[1:],val);counts['omission_mutants']+=1
  val[v]=not val[v]
  assert satisfied((-clause[0],)+clause[1:],val);counts['sign_mutants']+=1
  counter.append({'kind':kind,'cut':k,'first_literal':clause[0],'omitted_literal_counterexample_flips':v})
 for m in (4,5):
  tt,rs=rows(m)
  for bits in range(1<<len(tt)):
   val={v:bool(bits>>(v-1)&1) for v in range(1,len(tt)+1)}
   signs={t:val[v] for v,t in enumerate(tt,1)}
   for (kind,k),clause in rs.items():
    assert satisfied(clause,val)==(not direct(signs,kind,k,m));counts['exhaustive_small']+=1
 return {'status':'PASS','counts':counts,'countercontrols':counter}
def main():
 start=time.monotonic();resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20))
 DATA.mkdir(exist_ok=True);S.mkdir(exist_ok=False)
 before={k:sha(p) for k,p in FILES.items()};save('hashes-before.json',before);assert before==EXPECTED
 receipt=json.loads(Path(str(FILES['output'])+'.json').read_text())
 assert receipt['hashes']==EXPECTED
 triples,allrows=rows(14);nv=0;ids={}
 with FILES['map'].open() as f:
  for line in f:
   if line.startswith('#'):continue
   v,kind,mask=line.split();v=int(v);assert v==nv+1;nv=v
   if kind=='orientation':ids[tuple(i for i in range(14) if int(mask)>>i&1)]=v
 assert nv==32086 and ids=={t:i for i,t in enumerate(triples,1)}
 unique=[];provenance=[]
 for (kind,k),row in allrows.items():
  assert len(row)==len(set(map(abs,row)))==k*(14-k)*12//2
  if row not in unique:unique.append(row)
  provenance.append({'kind':kind,'cut':k,'row_index':unique.index(row),'literals':len(row)})
 assert len(unique)==37 and sum(map(len,unique))==8034
 assert provenance==receipt['cuts']
 assert {k:receipt[k] for k in ('m','n','variables','base_clauses','added_clauses','added_literals')}==dict(m=14,n=7,variables=32086,base_clauses=231613,added_clauses=37,added_literals=8034)
 count=lits=bodybytes=0;rebuilt=S/'rebuilt.cnf';marker=b'c conditional high/low/all-cup cut exclusions; see receipt dependencies\n'
 with FILES['base'].open('rb') as base,FILES['output'].open('rb') as out,rebuilt.open('xb') as dst:
  assert base.readline().split()==[b'p',b'cnf',b'32086',b'231613']
  head=b'p cnf 32086 231650\n';assert out.readline()==head;dst.write(head)
  for line in base:
   assert out.readline()==line,('base body changed',count)
   dst.write(line);bodybytes+=len(line)
   if not line.strip() or line.startswith(b'c'):continue
   numbers=[int(x) for x in line.split()];assert numbers[-1]==0 and all(0<abs(v)<=nv for v in numbers[:-1])
   count+=1;lits+=len(numbers)-1
  assert count==231613
  assert out.readline()==marker;dst.write(marker)
  for row in unique:
   line=(' '.join(map(str,row))+' 0\n').encode();assert out.readline()==line;dst.write(line)
  assert out.read(1)==b''
 assert sha(rebuilt)==EXPECTED['output']
 truth=truth_controls();save('truth-controls.json',truth)
 after={k:sha(p) for k,p in FILES.items()};assert before==after;save('hashes-after.json',after)
 for src,name in ((FILES['source'],'producer.py.txt'),(Path(str(FILES['output'])+'.json'),'producer-receipt.json')):
  with (DATA/name).open('xb') as f:f.write(src.read_bytes())
 result={'status':'PASS','label':'COMPUTED','m':14,'n':7,'variables':nv,'map_entries_pinned':nv,'orientation_entries_rebuilt':len(ids),
  'base_rows_unchanged':count,'base_literals':lits,'base_body_bytes_unchanged':bodybytes,'added_rows':37,'added_literals':8034,
  'total_rows':count+37,'provenance':provenance,'hashes':after,'rebuilt':str(rebuilt),'truth_controls':truth['counts'],
  'seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  'limits':Path('/proc/self/limits').read_text(),'affinity':sorted(os.sched_getaffinity(0))}
 save('rows.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('provenance','limits')}))
if __name__=='__main__':
 try:main()
 except BaseException as e:
  if DATA.exists() and not (DATA/'failure.json').exists():save('failure.json',{'error':repr(e)})
  raise
