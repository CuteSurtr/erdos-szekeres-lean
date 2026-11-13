#!/usr/bin/env python3
"""Exact finite replay of the29 variant candidates and their redundancy.

This is a Python diagnostic, not a Lean proof of literal instances or CSP
exhaustiveness. The reusable geometric template is checked separately.
"""
from pathlib import Path
import gzip,hashlib,itertools,json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent

def check():
 data=json.loads((HERE/'variants.json').read_text());bindings=json.loads((HERE/'row-bindings.json').read_text())['rows']
 raw=gzip.decompress((ROOT/'experiments/omission-residual32-research-2026-10-10/source.json.gz').read_bytes());assert hashlib.sha256(raw).hexdigest()==data['source_sha256']=='f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909';source=json.loads(raw)
 core_path=ROOT/'experiments/omission-residual32-witness-coupled-2026-10-10/core13.json';assert hashlib.sha256(core_path.read_bytes()).hexdigest()==data['core_sha256'];core=json.loads(core_path.read_text())
 assert hashlib.sha256((HERE/'discover.py').read_bytes()).hexdigest()==data['script_sha256']
 criteria=[c for c in core['clauses'] if c['kind'] in ('empty_direction','domain','fixed_sign')];assert len(criteria)==159
 cells=[{(i+1,j) for i,h in enumerate(s[:4]) for j in range(1,h+1)} for s in source['states']]
 def positive(q):
  for perm in itertools.permutations(range(3)):
   a,b,c=[q[i] for i in perm];ab=cells[b]-cells[a];bc=cells[c]-cells[b];ac=cells[c]-cells[a]
   if not ab or not bc or not ac:continue
   parity=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2
   if max(z[parity] for z in bc)>min(z[parity] for z in ab):return False
  return True
 def valid(mapping):
  assert len(mapping)==len(set(mapping))==13 and all(type(x) is int and 0<=x<154 for x in mapping)
  for clause in criteria:
   q=clause['detail'];kind=clause['kind'];a,b=mapping[q[0]],mapping[q[1]]
   if kind=='fixed_sign':
    c=mapping[q[2]];assert positive((a,b,c) if q[3] else (a,c,b))
   else:
    diff=cells[b]-cells[a]-{(1,6)}
    assert not diff if kind=='empty_direction' else (q[2],q[3]) not in diff
 valid(core['support']);assert len(data['variants'])==len(bindings)==29
 seen={tuple(sorted(core['support']))}
 for i,(candidate,binding) in enumerate(zip(data['variants'],bindings)):
  mapping=candidate['map'];valid(mapping);support=sorted(mapping);assert support==candidate['support']==binding['support'];assert mapping==binding['map'];assert tuple(support) not in seen;seen.add(tuple(support))
  assert binding['index']==i and candidate['rhs']==binding['rhs']==1
  row=source['constraints'][binding['implied_by_single_frozen_row']]
  assert row['rhs']>len(set(row['support'])-set(support))
 return {'scope':'Exact Python compatibility and redundancy diagnostics; no literal variant Lean proof or exhaustiveness theorem','compatible_new_supports':29,'redundant_supports':29,'known_base_core_compatible':True,'criteria_per_map':159,'checked_injective_maps':30}
if __name__=='__main__':print(json.dumps(check(),indent=2))
