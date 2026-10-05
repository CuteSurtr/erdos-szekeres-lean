import hashlib,importlib.util,json,sys,time
from pathlib import Path
root=Path('.cache/schroeder-release/es7_es8_bounds_81_319_v1')
module=root/'tools/check_octagon_arithmetic.py'
spec=importlib.util.spec_from_file_location('author_omission_arithmetic',module)
author=importlib.util.module_from_spec(spec);spec.loader.exec_module(author)
name=sys.argv[1];source=root/'certificates'/f'{name}.json'
data=json.loads(source.read_text())
tree_path=Path(f'.cache/omission-tree/{name}-plus1-compact.json')
tree=json.loads(tree_path.read_text());budget=tree['hole_budget']
assert tree['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
rows=[(set(s),len(s)-7) for s in data['cuts']] if 'cuts' in data else [(set(r['support']),r['rhs']) for r in data['constraints']]
nodes=[];dropped=0;zero_capacity=0
# Renumber children before parents, as required by the unmodified author checker.
# Remove zero-residual rows so its signed residual convention equals clipping.
def visit(i,M,Z):
 global dropped,zero_capacity
 x=tree['nodes'][i]
 if x['type']=='branch':
  v=x['vertex'];a=visit(x['zero'],M,Z|{v});b=visit(x['one'],M|{v},Z)
  y={'type':'branch','vertex':v,'zero':a,'one':b}
 elif x['type']=='weighted':
  w=[[r,v] for r,v in x['weights'] if rows[r][1]>len(rows[r][0]&M)]
  dropped+=len(x['weights'])-len(w)
  L=x['capacity']
  if L==0:
   zero_capacity+=1;L=1;w=[[r,v*(budget+1)] for r,v in w]
  y={'type':'weighted','capacity':L,'weights':w}
 elif x['type']=='over_budget':y={'type':'weighted','capacity':1,'weights':[]}
 else:raise ValueError('Unfinished tree')
 nodes.append(y);return len(nodes)-1
started=time.monotonic();new_root=visit(tree['root'],set(),set())
normalized={'states':data['states'],'hole_budget':budget,'nodes':nodes,'root':new_root}
field='cuts' if 'cuts' in data else 'constraints';normalized[field]=data[field]
p=Path(f'.cache/omission-tree/{name}-author-compatible.json');assert not p.exists()
p.write_text(json.dumps(normalized,separators=(',',':'))+'\n')
result={'scope':'Same finite row system checked by the unmodified source author arithmetic checker; no Lean evaluation or geometric transfer', 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'original_compact_tree_sha256':hashlib.sha256(tree_path.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(module.read_bytes()).hexdigest(),'normalizer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'zero_residual_weights_removed':dropped,'zero_capacity_leaves_rescaled':zero_capacity,'report':author.check(p),'seconds':time.monotonic()-started}
Path(f'.cache/omission-tree/{name}-author-replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
