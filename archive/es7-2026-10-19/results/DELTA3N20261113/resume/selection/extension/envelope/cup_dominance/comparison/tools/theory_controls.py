"""Check the 48-row predicate, canonical two-step paths and backward support."""
import argparse
from itertools import combinations as C
import json
from pathlib import Path
from verify import setup,orientation

ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--table',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False)
inputs=json.loads((args.run/'inputs.json').read_text());records=[json.loads(s) for s in (args.run/'results.jsonl').read_text().splitlines()]
counts={'classes':0,'forced':0,'direct_cup':0,'forced_extra':0,'forbidden_late_query_by_no5':0};rows=json.loads(args.table.read_text())['rows']
for r in rows:
 z=r['d_endpoint_signs'];pred=z[-1]>=0 and any(t<=0 and (t<0 or z[-1]>0) for t in z[:-1]);assert pred==(r['classification']=='forced_dominance_after_R')
 p,q=r['query_positions'],r['ambient_positions'];direct=r['orientations_012_013_023_123']=='++++' and q[0]>=p[0] and q[1]>=p[1]
 assert not direct or pred;counts['classes']+=1;counts['forced']+=pred;counts['direct_cup']+=direct;counts['forced_extra']+=pred and not direct;counts['forbidden_late_query_by_no5']+=pred and q[1]<p[1]
canonical=0;chosen=None
for inp,r in zip(inputs,records):
 p=inp['P']
 def cup(pair,target):return all(orientation(p,*t)>0 for t in C(sorted(set(pair+target)),3))
 for row in r['closure_added']:
  query=tuple(row['pair']);target=tuple(row['path'][-1]);mid=(query[0],target[1]);assert target[0]>=query[0] and target[1]>=query[1]
  assert cup(query,mid) and cup(mid,target);canonical+=1
 if chosen is None:
  closed={tuple(z['pair']) for z in r['closure_added']}
  extra=[z for z in r['forced_added'] if tuple(z['pair']) not in closed and z['cap_terminal']]
  if extra:chosen=(inp,extra[0])
assert chosen is not None
inp,z=chosen;p=inp['P'];query=tuple(z['pair']);support=tuple(z['support']);cap=tuple(z['ambient_fourcap'])
triple=next(t for t in C(range(len(p)),3) if t[-2:]==query and orientation(p,*t)<0)
ids=sorted(set(triple+cap));small=[p[i] for i in ids];ix={v:i for i,v in enumerate(ids)};q=tuple(ix[v] for v in query);e=tuple(ix[v] for v in support);K=tuple(ix[v] for v in cap);T=tuple(ix[v] for v in triple)
sgn,c3,c4,ambient,edge,one=setup(small);assert T in c3 and K in c4 and K[-2:]==e and e[0]<q[0] and e[1]>=q[1]
pairs=list(C(range(len(small)),2));closed=set(ambient)
while True:
 new={a for a in pairs if a not in closed and any(edge(a,b) for b in closed)}
 if not new:break
 closed|=new
assert q not in closed
diff=[]
for v in sorted(set(q+e)):
 d=0 if v in q and v in e else -orientation(small,*e,v) if v in q else orientation(small,*q,v)
 diff.append(1 if d>0 else -1 if d<0 else 0)
assert diff[-1]>=0 and any(a<=0 and (a<0 or diff[-1]>0) for a in diff[:-1])
fixture={'label':'COMPUTED exact strict endpoint-rule gain','source_case':inp['name'],'source_indices':ids,'P':small,'cap_triple':T,'query_pair':q,'support_pair':e,'ambient_fourcap':K,'all_fourcaps':c4,'all_cup_closure_pairs':sorted(closed),'endpoint_difference_signs':diff,'no_fivecap':True,'cup_closure_protected':False,'endpoint_forced_protected':True}
(args.out/'backward_left_gain.json').write_text(json.dumps(fixture,indent=2)+'\n')
summary={'label':'COMPUTED exact theory controls','predicate_comparison':counts,'canonical_two_step_gains_checked':canonical,'backward_left_fixture_points':len(small),'all_passed':True}
(args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
