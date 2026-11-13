import copy,gzip,hashlib,itertools,json,os,sys,time
from pathlib import Path
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
sys.path.insert(0,'experiments/omission-residual32-rank-search-2026-10-10');import model
R=Path('.cache/rank313');C=R/'clipping';C.mkdir(exist_ok=True);raw=gzip.decompress(Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz').read_bytes());D=json.loads(raw);model.D=D;P,mn,mx=model.pair_boxes(D['states']);model.TT=model.triple_table(P,mn,mx);model.cells=[{(i+1,y) for i,h in enumerate(s[:4]) for y in range(1,h+1)} for s in D['states']];entries=json.loads((R/'candidates.json').read_text());out=[]
for e in [e for e in entries if len(e['support'])==11][:8]:
 model.ROOT=C;model.occupied=set(range(154))-set(e['strict_row_witness_holes']);S=e['support'];m=model.CompactModel(S,time.monotonic()+15,source_cup_bound=False);m.s.add(model.z3.Or(*[model.z3.And(m.before[i,j],m.cup[tuple(sorted((i,j)))]>D['states'][S[i]][0]+1) for i,j in itertools.permutations(range(len(S)),2)]));r=m.probe(time.monotonic()+10);out.append(r)
 if r['status']!='sat':continue
 old=json.loads((C/r['assignment']).read_text())['assignment'];assert not m.replay(old)[0];new=copy.deepcopy(old);p=old['positions'];changes=[]
 for row in new['labels']:
  i,j,a,b=row;source=i if p[i]<p[j] else j;cap=D['states'][S[source]][0]+1;row[3]=min(b,cap)
  if row[3]!=b:changes.append({'pair':[i,j],'chronological_source':source,'source_state':S[source],'before_cup':b,'after_cup':row[3]})
 assert changes;m.source_cup_bound=True;violations,calls=m.replay(new);assert not violations
 report={'scope':'Exact independent replay of an OLD coupled-model assignment violating source-cup bounds, after clipping. Neither assignment is a real-point realization.','source_sha256':hashlib.sha256(raw).hexdigest(),'support':S,'old_assignment':old,'clipped_assignment':new,'changes':changes,'old_all_constraints_except_new_rank_checked':True,'clipped_domains_growth_packets_fixed_signs_new_rank_checked':True,'clipped_exhaustive_octagon_search_found_none':True,'octagon_search_calls':calls,'positions_caps_orientations_unchanged':True};(C/'checked-old-assignment.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'support':S,'changed_labels':len(changes),'changes':changes,'complete':True}));break
else:print(json.dumps({'complete':False,'results':out}))
