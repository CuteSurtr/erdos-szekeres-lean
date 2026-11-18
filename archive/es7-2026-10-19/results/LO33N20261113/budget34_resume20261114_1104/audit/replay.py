import sys,json,hashlib,time,datetime as dt,os
from pathlib import Path
ROOT=Path('/home/jay/research/lean/erdos-szekeres-lean');O=ROOT/'cloud/es7-2026-10-19/results/LO33N20261113/budget34/audit';R=O.parent.parent/'budget34_resume20261114_1104/audit';W=Path('/home/jay/research/data/es308-resume-20261114-1104');P=Path('/home/jay/research/data/es308-20261114');B=W/'bb'
sys.path.insert(0,str(O));import replay34 as a
END=dt.datetime(2026,11,14,11,13,25,tzinfo=dt.timezone(dt.timedelta(hours=9))).timestamp()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
  if str(p).endswith('.gz'):os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
 return h.hexdigest()
def dump(n,x): (R/n).write_text(json.dumps(x,indent=2)+'\n')
def paths(m):
 stack=[(m['root'],((0,0),))];seen=set();cs={};ns={}
 while stack:
  i,path=stack.pop();assert type(i)is int and 0<=i<len(m['nodes']) and i not in seen;seen.add(i);n=m['nodes'][i];ns[i]=path
  if n['type']=='branch':
   v=n['vertex'];assert type(v)is int and 0<=v<154 and v not in dict(path)
   stack.extend([(n['zero'],path+((v,0),)),(n['one'],path+((v,1),))])
  elif n['type']=='context':
   c=n['context'];assert type(c)is int and c>=0 and c not in cs;cs[c]=(i,path)
  else:assert n['type'] in ('weighted','over_budget')
 assert len(seen)==len(m['nodes']) and len(cs)==m['contexts'];return cs,ns
old=a.read_json(P/'runs/s20/bb/master.json');m=a.read_json(B/'master.json');oc,on=paths(old);nc,nn=paths(m)
fin=a.read_json(O/'incremental/finished-by-control.json');assert sha(P/'runs/s20/bb/master.json')==fin['master_sha256'];assert m['budget']==old['budget']==34
assert m['source']==old['source'] and m['extra']==old['extra'];s=a.read_json(Path(m['source']));ex=a.read_json(Path(m['extra']));rows=[(r['support'],r['rhs']) for r in s['constraints']+ex];assert len(rows)==3623
F=[i for i,z in enumerate(s['states']) if z[0]>=5];Lo=[i for i,z in enumerate(s['states']) if z[0]<=4];assert ex[:2]==[{'support':F,'rhs':20},{'support':Lo,'rhs':14}]
prior=a.read_json(O/'incremental/latest-summary.json');assert sha(Path(m['source']))==prior['input_sha256'][m['source']] and sha(Path(m['extra']))==prior['input_sha256'][m['extra']]
closed={int(k[4:-8]) for k in fin['context_hashes']};assert len(closed)==1222
mapping={};stack=[(old['root'],m['root'])]
while stack:
 i,j=stack.pop();x,y=old['nodes'][i],m['nodes'][j]
 if x['type']=='branch':
  assert y['type']=='branch' and x['vertex']==y['vertex'];stack.extend([(x['zero'],y['zero']),(x['one'],y['one'])])
 elif x['type']=='context':
  c=x['context']
  if c in closed:assert y['type']=='context' and y['context']==c and oc[c][1]==nc[c][1]
  else:
   todo=[(j,0)];desc=[]
   while todo:
    k,d=todo.pop();z=m['nodes'][k]
    if z['type']=='branch':assert d<1;todo.extend([(z['zero'],d+1),(z['one'],d+1)])
    elif z['type']=='context':assert z['context'] not in oc;desc.append(z['context'])
    else:assert z['type'] in ('weighted','over_budget')
   mapping[c]=desc
 else:assert x==y
assert set(nc)==closed|set(c for v in mapping.values() for c in v)
des=a.read_json(B/'contexts.json');assert len(des)==len(nc) and {d['context'] for d in des}==set(nc)
for d in des:a.descriptor(d,d['context'],nc[d['context']][1])
wrapped,_=a.envelope(m['nodes'],m['root'],((0,0),),True);top=a.check_tree(154,rows,34,wrapped,0,allow_pending=True);assert top['pending']==len(nc)+1;del wrapped
pins={str(p):sha(p) for p in [B/'master.json',B/'contexts.json',Path(m['source']),Path(m['extra']),O/'final-manifest.json',O/'final-audit.json',O/'incremental/finished-by-control.json',ROOT/'scripts/omission_tree.py',Path(__file__)]}
done={}
for p in [O/'incremental/carried.jsonl',O/'incremental/new-contexts.jsonl']:
 for line in p.open():
  r=json.loads(line);c=r['context'];assert c not in done and c in closed
  assert r['path']==[list(z) for z in nc[c][1]] and r['context_sha256']==fin['context_hashes'][f'ctx-{c}.json.gz']==sha(B/f'ctx-{c}.json.gz')
  assert r['internal_pending']==0 and r['max_used_row']<r['original_row_count']<=len(rows)
  h=hashlib.sha256()
  for support,demand in rows[:r['original_row_count']]:h.update((str(demand)+':'+','.join(map(str,support))+'\n').encode())
  assert h.hexdigest()==r['original_rows_sha256'];done[c]=r
assert set(done)==closed
initial={'label':'REFINEMENT AND CARRY CHECKED; NEW LEAVES PENDING','old_contexts':len(oc),'old_closed_carried':len(done),'old_open_roots':len(mapping),'old_roots_closed_in_master':sum(not v for v in mapping.values()),'new_contexts':len(nc),'new_open_contexts':len(nc)-len(done),'master_check':top,'pins':pins}
dump('refinement.json',initial);dump('old-open-descendants.json',mapping);print(json.dumps(initial),flush=True)
with (R/'new-contexts.jsonl').open('x') as out:
 while time.time()<END and not (W/'audit/STOP').exists():
  added=0
  for p in sorted(B.glob('ctx-*.json.gz'),key=lambda p:int(p.name[4:-8])):
   c=int(p.name[4:-8]);assert c in nc
   if c in done:continue
   if time.time()>=END:break
   if p.stat().st_size*40+80*1048576>900*1048576:continue
   h=sha(p);x=a.read_json(p);a.descriptor(x,c,nc[c][1]);wrapped,u=a.envelope(x['nodes'],x['root'],nc[c][1]);rr=a.check_tree(154,rows,34,wrapped,0,allow_pending=True)
   assert rr['pending']==len(nc[c][1]) and sha(p)==h
   r={'context':c,'context_sha256':h,'path':[list(z) for z in nc[c][1]],'nodes':len(x['nodes']),'leaves':rr['leaves']-len(nc[c][1]),'minimum_margin':rr['minimum_margin'],'internal_pending':0,'used_rows':sorted(u)}
   out.write(json.dumps(r)+'\n');out.flush();done[c]=r;added+=1;del x,wrapped,rr
  present={int(p.name[4:-8]) for p in B.glob('ctx-*.json.gz')};assert present<=set(nc)
  margins=[r['minimum_margin'] for r in done.values() if r['minimum_margin']is not None]+([top['minimum_margin']] if top['minimum_margin']is not None else [])
  result={'label':'PARTIAL EXACT REPLAY; NO EXCLUSION','contexts_total':len(nc),'inherited_checked':1222,'new_checked':len(done)-1222,'present_contexts':len(present),'present_unchecked':sorted(present-set(done)),'frontier_pending':len(nc)-len(done),'global_pending':len(nc)-len(done)+1,'original_open_roots':len(mapping),'original_roots_now_closed':sum(set(v)<=set(done) for v in mapping.values()),'original_roots_still_open':sum(not set(v)<=set(done) for v in mapping.values()),'nodes':len(m['nodes'])+2-len(done)+sum(r['nodes'] for r in done.values()),'leaves':top['leaves']-len(done)+sum(r['leaves'] for r in done.values()),'minimum_margin':min(margins,default=None),'updated_local':dt.datetime.now().astimezone().isoformat(),'pins':pins}
  dump('summary.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('pins','present_unchecked')}),flush=True)
  if not added:time.sleep(min(3,max(0,END-time.time())))
assert all(sha(p)==h for p,h in pins.items());assert all(sha(B/f'ctx-{c}.json.gz')==r['context_sha256'] for c,r in done.items())
dump('finished.json',{'label':'FINAL PARTIAL','time':dt.datetime.now().astimezone().isoformat(),'summary_sha256':sha(R/'summary.json'),'old_closed_carried':1222,'all_input_hashes_stable':True,'checked_context_hashes':{str(c):r['context_sha256'] for c,r in done.items()}})
