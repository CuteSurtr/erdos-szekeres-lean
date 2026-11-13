#!/usr/bin/env python3
"""Exact finite domain arithmetic only; no solver and no geometric proof claim."""
import argparse,collections,gzip,hashlib,itertools,json,os,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
os.chdir(ROOT)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path('.cache/residual-rank-attainment-assessment-replay'))
parser.add_argument('--check',action='store_true')
args=parser.parse_args()
D=args.output;D.mkdir(parents=True,exist_ok=True)
P=Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz');raw=gzip.decompress(P.read_bytes());sha=hashlib.sha256(raw).hexdigest();assert sha=='151ea1bfb175f6507d910521eb96961c82b54add2fb7e49e13b864b87241123e';states=json.loads(raw)['states'];n=len(states);assert n==154;cells=[{(i+1,y) for i,h in enumerate(s[:4]) for y in range(1,h+1)} for s in states]
rawdomains={(u,v):cells[v]-cells[u] for u in range(n) for v in range(n) if u!=v};old={uv:d-{(1,6)} for uv,d in rawdomains.items()};new={uv:{(x,y) for x,y in d if y<=states[uv[0]][0]+1} for uv,d in old.items()};lost=[{'from':u,'to':v,'source_first_column':states[u][0],'old_size':len(old[u,v]),'new_size':len(new[u,v]),'removed':sorted(old[u,v]-new[u,v])} for u,v in old if old[u,v]!=new[u,v]];newempty=[list(uv) for uv in old if old[uv] and not new[uv]];incompatible=[list((u,v)) for u in range(n) for v in range(u+1,n) if (old[u,v] or old[v,u]) and not(new[u,v] or new[v,u])]
cp=Path('experiments/omission-residual32-2598-primal-2026-10-10/candidates.json');cand0=json.loads(cp.read_text())['candidates'];candidates={c['name']:c['holes'] for c in cand0};np=Path('experiments/omission-residual32-primal-resume-2026-10-10/feasible34-checked-near-models.json');candidates.update({f"near_row{c['violations'][0]['row']}":c['holes'] for c in json.loads(np.read_text())['candidates']});profiles={}
for name,holes in candidates.items():
 occupied=set(range(n))-set(holes);pairs=[(u,v) for u in occupied for v in occupied if u!=v];profiles[name]={'holes':holes,'occupied_states':len(occupied),'directed_pairs':len(pairs),'changed_domains':sum(old[p]!=new[p] for p in pairs),'labels_removed':sum(len(old[p]-new[p]) for p in pairs),'newly_empty_directions':[list(p) for p in pairs if old[p] and not new[p]],'newly_incompatible_pairs':[p for p in incompatible if set(p)<=occupied]}
report={'scope':'Read-only exact finite arithmetic for proposed chronological cup-label bound. Geometry theorem status is separate. No search or theorem inference.','source':str(P),'source_sha256':sha,'restriction':'for u before v, cup(label(u,v)) <= states[u][0]+1','domain_baseline':'cells(v) minus cells(u) minus {(1,6)}','directed_pairs':n*(n-1),'old_nonempty_domains':sum(bool(d) for d in old.values()),'new_nonempty_domains':sum(bool(d) for d in new.values()),'changed_domains':len(lost),'old_total_labels':sum(map(len,old.values())),'new_total_labels':sum(map(len,new.values())),'labels_removed':sum(len(r['removed']) for r in lost),'newly_empty_directions':newempty,'newly_incompatible_unordered_pairs':incompatible,'removed_by_source_first_height':dict(sorted(collections.Counter({h:sum(len(r['removed']) for r in lost if r['source_first_column']==h) for h in range(7)}).items())),'candidate_domains':profiles,'changed_domain_records':lost};(D/'domains.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['candidate_domains','changed_domain_records']}),flush=True)
# Reproduce ResidualDomains.boundingBox coordinate extrema and the six cases
# of CycleSigns.CheckTriple from the maintained Lean sources; no solver.
perms=[]
for perm in itertools.permutations(range(3)):
 parity=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2;perms.append((perm,1 if parity else 0))
def boxes(domains):
 return {uv:(min(x for x,y in d),max(x for x,y in d),min(y for x,y in d),max(y for x,y in d)) if d else None for uv,d in domains.items()}
B=[boxes(ds) for ds in [rawdomains,old,new]]
def sign(t,b):
 for p,c in perms:
  u,v,w=[t[i] for i in p];a=b[u,v];z=b[v,w]
  if a is not None and z is not None and b[u,w] is not None and z[2*c+1]>a[2*c]:return False
 return True
counts=[collections.Counter() for _ in B];changes_raw=collections.Counter();changes_coupled=collections.Counter();new_both=[];occupiedsets={k:set(range(n))-set(v) for k,v in candidates.items()};cc={k:{'old':collections.Counter(),'new':collections.Counter(),'new_forced_unsigned':0,'new_both_signs':[]} for k in candidates};records=[];start=time.monotonic()
for t in itertools.combinations(range(n),3):
 rev=(t[0],t[2],t[1]);statuses=[(int(sign(t,b))+2*int(sign(rev,b))) for b in B]
 for c,s in zip(counts,statuses):c[s]+=1
 if statuses[0]!=statuses[2]:changes_raw[str(statuses[0])+'->'+str(statuses[2])]+=1
 if statuses[1]!=statuses[2]:
  changes_coupled[str(statuses[1])+'->'+str(statuses[2])]+=1
  if statuses[2]==3 and statuses[1]!=3:new_both.append(list(t))
  records.append({'states':t,'old':statuses[1],'new':statuses[2]})
 for name,occupied in occupiedsets.items():
  if set(t)<=occupied:
   cc[name]['old'][statuses[1]]+=1;cc[name]['new'][statuses[2]]+=1
   if statuses[1]==0 and statuses[2] in [1,2]:cc[name]['new_forced_unsigned']+=1
   if statuses[2]==3 and statuses[1]!=3:cc[name]['new_both_signs'].append(list(t))
tr={'scope':'Bounding-box cyclic-triple predicate changes only, using the coordinate extrema from ResidualDomains.boundingBox and the six chronological cases of CycleSigns.CheckTriple in the maintained Lean sources. Status0=neither sign forced;1=positive;2=negative;3=both predicates true. No solver and no new geometric theorem.','source_sha256':sha,'unordered_triples':n*(n-1)*(n-2)//6,'seconds':time.monotonic()-start,'raw_original_box_counts':counts[0],'old_forbidden_cell_box_counts':counts[1],'new_cup_bound_box_counts':counts[2],'raw_to_new_status_changes':changes_raw,'coupled_to_new_status_changes':changes_coupled,'new_both_predicate_triples':new_both,'candidate_triples':cc,'changed_triples':records};(D/'triples.json').write_text(json.dumps(tr,indent=2)+'\n');print(json.dumps({k:v for k,v in tr.items() if k not in ['candidate_triples','changed_triples','new_both_predicate_triples']}),flush=True)

if args.check:
 expected_domains=json.loads(gzip.decompress((HERE/'domains.json.gz').read_bytes()))
 expected_triples=json.loads((HERE/'triples.json').read_text())
 replayed_triples=json.loads((D/'triples.json').read_text())
 expected_triples.pop('seconds',None);replayed_triples.pop('seconds',None)
 if json.loads((D/'domains.json').read_text())!=expected_domains:raise ValueError('Domain assessment differs from exact replay')
 if replayed_triples!=expected_triples:raise ValueError('Triple assessment differs from exact replay')
 print('All domain records and 596,904 triple predicates replayed exactly.')
