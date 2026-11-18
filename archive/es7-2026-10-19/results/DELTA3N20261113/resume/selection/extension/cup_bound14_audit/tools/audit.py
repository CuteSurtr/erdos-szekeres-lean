#!/usr/bin/env python3
"""Own no-six-cup append audit; no producer execution/import."""
import hashlib,importlib.util,itertools as it,json,os,resource,time
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=R.parent;D=R/'data'
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
FILES={'base':W/'n7m14-exact.cnf','map':W/'terminal7-a/m14/input.cnf.map',
 'output':W/'n7m14-nosixcup.cnf','source':E/'augment_nosixcup14.py'}
EXPECTED={'base':'5dc0c1719cce7bda188abad8489534413ecbbcbe5f43e1b714244ec045a129c4',
 'map':'b81223d78761ab200ef5931cc33ab10821a3e3a2054c5e550d0d8da7cf0fa55e',
 'output':'614a810468d31b194293128c0c56fcf79d92230d7712fbfcd5fb610eb4c81a34',
 'source':'0f0b8ccae3c12ab43533b7bf2fcedb6396639fa882ef6cd9b1dd961ef90276fd'}
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
def verts(s):return tuple(v for v in range(14) if s>>v&1)
def sat(row,val):return any(val[abs(v)]==(v>0) for v in row)
def sec(a,b,x):return Fraction(a[1]*(b[0]-a[0])+(b[1]-a[1])*(x-a[0]),b[0]-a[0])
def high_join(P,Q):
 shift=P[-1][0]+4-Q[0][0];Q=[(x+shift,y) for x,y in Q]
 thresholds=[sec(a,b,x)-y for x,y in Q for a,b in it.combinations(P,2)]
 thresholds += [y-sec(a,b,x) for x,y in P for a,b in it.combinations(Q,2)]
 top=max([Fraction(0)]+thresholds);h=top.numerator//top.denominator+1
 return P+[(x,y+h) for x,y in Q]
def real_controls(triples,rows,masks):
 helper=E/'highsplit_audit/tools/controls.py';manifest=dict(line.split('  ',1)[::-1] for line in (E/'highsplit_audit/SHA256SUMS').read_text().splitlines())
 assert sha(helper)==manifest['tools/controls.py']
 spec=importlib.util.spec_from_file_location('own_high_geometry',helper);H=importlib.util.module_from_spec(spec);spec.loader.exec_module(H)
 cap3=[(i,-i*i) for i in range(3)];cup3=[(i,i*i) for i in range(3)];cup4=[(i,i*i) for i in range(4)]
 six=high_join(cap3,cup3);ten=high_join(six,cup4);positive=high_join(ten,cup4)
 negative_file=E/'highsplit_audit/data/controls-m14.json';old_hash=sha(negative_file)
 negative=json.loads(negative_file.read_text())['P'];out=[]
 for name,P,want in [('inside_no_six_cup',positive,True),('excluded_six_cup_present',negative,False)]:
  G=H.Geometry(P,7);assert G.m==14 and not G.cap5 and not G.ngons and G.targets
  vals={v:G.orient[t]>0 for v,t in enumerate(triples,1)}
  sixcups=[s for s in masks if G.chain(verts(s),1)]
  false=[s for s,row in zip(masks,rows) if not sat(row,vals)]
  assert false==sixcups and (not false)==want
  # Independently verify full terminal selection for both controls.
  A=H.mask(range(10,14)) if want else H.mask((0,2,3,13));assert G.valid(A)
  assert (max(G.beta)<=5)==want
  out.append({'name':name,'P':P,'geometry':G.summary(),'sixcups':len(sixcups),
   'false_appended_rows':len(false),'first_sixcup':list(verts(sixcups[0])) if sixcups else None,
   'terminal_selector_checked':list(H.verts(A)),'new_hypothesis_satisfied':want,'actual_rows_checked':len(rows)})
 assert sha(negative_file)==old_hash
 return {'status':'PASS','cases':out,'geometry_helper_sha256':sha(helper),'negative_fixture_sha256':old_hash}
def main():
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));start=time.monotonic()
 before={k:sha(p) for k,p in FILES.items()};save('hashes-before.json',before);assert before==EXPECTED
 receipt_file=Path(str(FILES['output'])+'.json');receipt=json.loads(receipt_file.read_text())
 assert receipt['hashes']==EXPECTED and receipt['extra_hypothesis']=='no six-cup'
 assert (receipt['m'],receipt['n'],receipt['base_clauses'],receipt['added_clauses'],receipt['added_literals'])==(14,7,231613,3003,60060)
 triples=list(it.combinations(range(14),3));ids={};nv=0
 for line in FILES['map'].open():
  if line.startswith('#'):continue
  v,kind,s=line.split();v=int(v);assert v==nv+1;nv=v
  if kind=='orientation':ids[verts(int(s))]=v
 assert nv==32086 and ids=={t:v for v,t in enumerate(triples,1)}
 # Enumerate six-masks independently, then filter the full orientation list.
 masks=sorted((s for s in range(1<<14) if s.bit_count()==6),key=verts)
 rows=[tuple(-v for t,v in ids.items() if all(s>>a&1 for a in t)) for s in masks]
 assert len(rows)==len(set(rows))==3003 and all(len(r)==len(set(r))==20 for r in rows)
 rebuild=hashlib.sha256();bodybytes=count=baselits=0
 with FILES['base'].open('rb') as f,FILES['output'].open('rb') as g,(D/'added-rows.cnf').open('xb') as added:
  assert f.readline().split()==[b'p',b'cnf',b'32086',b'231613']
  header=b'p cnf 32086 234616\n';assert g.readline()==header;rebuild.update(header)
  for line in f:
   assert g.readline()==line;rebuild.update(line);bodybytes+=len(line)
   if not line.startswith(b'c') and line.strip():
    a=[int(x) for x in line.split()];assert a[-1]==0 and all(0<abs(v)<=nv for v in a[:-1]);count+=1;baselits+=len(a)-1
  assert count==231613
  marker=b'c additional geometric premise: no six-cup\n';assert g.readline()==marker;rebuild.update(marker)
  added.write(b'p cnf 32086 3003\n')
  for row in rows:
   line=(' '.join(map(str,row))+' 0\n').encode();assert g.readline()==line;rebuild.update(line);added.write(line)
  assert not g.read(1)
 assert rebuild.hexdigest()==EXPECTED['output']
 truth={'canonical_sixcups':0,'single_child_false':0,'outside_single_flips':0,'omission_mutants':0,'polarity_mutants':0}
 val={i:True for i in range(1,365)}
 for s,row in zip(masks,rows):
  assert not sat(row,val);truth['canonical_sixcups']+=1
  for lit in row:
   v=-lit;val[v]=False;assert sat(row,val)
   assert not all(val[ids[t]] for t in it.combinations(verts(s),3));truth['single_child_false']+=1;val[v]=True
  outside=next(v for v in val if -v not in row);val[outside]=False;assert not sat(row,val);val[outside]=True;truth['outside_single_flips']+=1
  v=-row[0];val[v]=False;assert not sat(row[1:],val) and sat(row,val);val[v]=True;truth['omission_mutants']+=1
  assert sat((-row[0],)+row[1:],val);truth['polarity_mutants']+=1
 save('truth-controls.json',truth)
 real=real_controls(triples,rows,masks);save('real-controls.json',real)
 after={k:sha(p) for k,p in FILES.items()};assert before==after;save('hashes-after.json',after)
 for src,name in [(FILES['source'],'producer.py.txt'),(receipt_file,'producer-receipt.json')]:
  with (D/name).open('xb') as f:f.write(src.read_bytes())
 result={'status':'PASS','label':'COMPUTED','m':14,'n':7,'extra_hypothesis':'no six-cup','variables':32086,
  'base_rows_unchanged':count,'base_literals':baselits,'base_body_bytes_unchanged':bodybytes,
  'added_clauses':3003,'added_literals':60060,'total_clauses':234616,'total_literals':baselits+60060,
  'hashes':after,'streamed_rebuilt_sha256':rebuild.hexdigest(),'truth_controls':truth,
  'real_control_counts':[(x['name'],x['sixcups']) for x in real['cases']],
  'seconds':time.monotonic()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
  'limits':Path('/proc/self/limits').read_text(),'affinity':sorted(os.sched_getaffinity(0)),
  'proof_replayed':False,'unrestricted_m14_claim':False}
 save('result.json',result);print(json.dumps({k:v for k,v in result.items() if k!='limits'}))
if __name__=='__main__':
 try:main()
 except BaseException as e:save('failure.json',{'error':repr(e)});raise
