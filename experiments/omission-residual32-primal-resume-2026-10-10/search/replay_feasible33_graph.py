import collections,gzip,hashlib,json,time
from pathlib import Path
D=Path('.cache/resume313-primal');P=Path('experiments/omission-residual32-2598-primal-2026-10-10');raw=gzip.decompress((P/'source-2598.json.gz').read_bytes());sha=hashlib.sha256(raw).hexdigest();assert sha=='01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b';base=json.loads(raw)['constraints'];ep=Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/rows.json');er=ep.read_bytes();extra=json.loads(er)['rows'];seedjson=json.loads((D/'feasible33-input.json').read_text());reports=[];graphs=[]
for label,rows in [('base2598',base),('augmented2646',base+extra)]:
 start=time.monotonic();seeds=[frozenset(s) for s in seedjson['seeds']];queue=collections.deque(seeds);seen=set(seeds);edges=0;near={};removals=[];universe=set(range(1,154));members=[set(r['support']) for r in rows]
 while queue:
  holes=queue.popleft();counts=[len(holes&support) for support in members];assert all(c>=r['rhs'] for c,r in zip(counts,rows));tight=[j for j,(c,r) in enumerate(zip(counts,rows)) if c==r['rhs']]
  for drop in sorted(holes):
   blockers=[j for j in tight if drop in members[j]]
   if not blockers:removals.append(sorted(holes-{drop}))
   if len(blockers)==1:near.setdefault(blockers[0],set()).add(tuple(sorted(holes-{drop})))
   allowed=universe-holes
   for j in blockers:allowed &=members[j]
   for add in sorted(allowed):
    child=frozenset((holes-{drop})|{add});assert len(child)==33;edges+=1
    if child not in seen:seen.add(child);queue.append(child)
 assert len(seen)==306 and edges==3650 and not removals and list(near)==[205] and len(near[205])==26
 (D/f'feasible33-{label}-near-models.json').write_text(json.dumps({'rows':{str(k):sorted(map(list,v)) for k,v in near.items()},'scope':'Not witnesses; all32-hole near-models violate exactly row205.'},indent=2)+'\n'); graph=sorted(map(sorted,seen));graphs.append(graph);(D/f'feasible33-{label}-vertices.json').write_text(json.dumps(graph,separators=(',',':'))+'\n');reports.append({'catalog':label,'rows':len(rows),'vertices':len(seen),'directed_edges':edges,'exhausted':True,'removable_holes':len(removals),'single_deficit_rows':sorted(near),'single_deficit_models':sum(map(len,near.values())),'seconds':time.monotonic()-start})
assert graphs[0]==graphs[1]
report={'scope':'Independent exact integer replay of the complete feasible33 single-exchange component containing eight row205 repairs; no global32 exclusion and no geometric realization claim.','source':str(P/'source-2598.json.gz'),'source_sha256':sha,'additional_rows':str(ep),'additional_rows_sha256':hashlib.sha256(er).hexdigest(),'same_graphs':True,'reports':reports,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};(D/'feasible33-independent-replay.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
