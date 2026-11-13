"""Independently extract and replay conditional subtrees; frozen source remains authoritative."""
import gzip,hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,'scripts')
from omission_row_probe import read_rows
from omission_tree import check_tree,contexts
D=Path('.cache/residual32-resume-2026-10-10-b'); start=time.monotonic()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=D/'source.json';n,rows=read_rows(json.loads(src.read_text()));path=D/'resumed-tree.json.gz'
with gzip.open(path,'rt') as f:t=json.load(f)
assert t['source_sha256']==sha(src) and t['hole_budget']==32
orig=json.loads(Path('experiments/omission-residual32-research-2026-10-10/pending-contexts.json').read_text())
prior={c['node'] for c in json.loads(Path('experiments/omission-residual32-three-row-probe-2026-10-10/diagnostic.json').read_text())['cuts_for_original_source']}
records=[]; allpending=[]; newclosed=[]
for c in orig['contexts']:
 stack=[(c['node'],set(c['missing']),set(c['occupied']))];seen=set();pending=[];margins=[];closed=over=0
 while stack:
  i,M,O=stack.pop();assert i not in seen;seen.add(i);q=t['nodes'][i]
  if q['type']=='branch':
   v=q['vertex'];assert 0<=v<n and v not in M|O
   stack.extend([(q['zero'],M,O|{v}),(q['one'],M|{v},O)])
  elif q['type']=='pending':pending.append({'node':i,'missing':sorted(M),'occupied':sorted(O),'original_pending_node':c['node']})
  elif q['type']=='over_budget':assert len(M)>32;over+=1
  else:
   assert q['type']=='weighted';cap=q['capacity'];assert type(cap) is int and cap>=0
   loads=[0]*n;demand=0;seenrows=set()
   # Integer-only check written separately from omission_tree.leaf_margin.
   # Discarding already-satisfied row remainders is allowed and can strengthen the cut.
   for r,w in q['weights']:
    assert type(r) is int and 0<=r<len(rows) and r not in seenrows;seenrows.add(r)
    assert type(w) is int and w>=0
    support,rhs=rows[r];remaining=rhs-sum(v in M for v in support)
    if remaining>0:demand+=w*remaining
    for v in support:loads[v]+=w
   upper=cap*(32-len(M))+sum(max(loads[v]-cap,0) for v in range(n) if v not in M|O)
   assert demand>upper,(i,demand,upper);margins.append(demand-upper);closed+=1
 rec={'original_node':c['node'],'initial_missing':c['missing'],'initial_occupied':c['occupied'],'nodes':len(seen),'weighted_leaves':closed,'over_budget_leaves':over,'pending_leaves':len(pending),'complete_under_context':not pending,'previously_cut_closed':c['node'] in prior,'minimum_margin':min(margins,default=None)}
 records.append(rec);allpending+=pending
 if not pending and c['node'] not in prior:
  newclosed.append(c['node']); ordered=sorted(seen);index={old:j for j,old in enumerate(ordered)};new=[]
  for old in ordered:
   q=dict(t['nodes'][old])
   if q['type']=='branch':q['zero']=index[q['zero']];q['one']=index[q['one']]
   new.append(q)
  pack={'scope':'Conditional exact integer Boolean row obstruction, not Lean checked or geometric transfer','source_sha256':sha(src),'hole_budget':32,'original_node':c['node'],'missing':c['missing'],'occupied':c['occupied'],'root':index[c['node']],'nodes':new,'independent_check':rec}
  with gzip.open(D/f'closed-context-{c["node"]}.json.gz','wt',compresslevel=9) as f:json.dump(pack,f,separators=(',',':'))
report={'scope':'Independent exact integer replay of every resumed original pending context; no Lean or planar-bound claim','source_sha256':sha(src),'resumed_tree_sha256':sha(path),'original_tree_sha256':orig['tree_sha256'],'newly_closed_original_contexts':newclosed,'original_contexts':records,'pending_count':len(allpending),'complete':not allpending,'seconds':time.monotonic()-start,'script_sha256':sha(Path(__file__))}
(D/'conditional-replay.json').write_text(json.dumps(report,indent=2)+'\n');(D/'pending-contexts.json').write_text(json.dumps({'source_sha256':sha(src),'tree_sha256':sha(path),'contexts':allpending},indent=2)+'\n');print(json.dumps(report),flush=True)
