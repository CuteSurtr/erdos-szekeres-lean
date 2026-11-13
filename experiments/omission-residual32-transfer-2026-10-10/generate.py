#!/usr/bin/env python3
"""Generate kernel-checked literal bindings; discovery metadata is not trusted.

Frozen original data follows Schroeder DOI10.5281/zenodo.22842891 (CC BY4.0),
with the attribution and code licenses recorded in docs/THIRD_PARTY.md.
This script only proposes matches. Lean checks every equality and implication.
"""
from pathlib import Path
import gzip,hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SOURCE=ROOT/'experiments/omission-residual32-research-2026-10-10/source.json.gz'
raw=gzip.decompress(SOURCE.read_bytes())
assert hashlib.sha256(raw).hexdigest()=='f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909'
data=json.loads(raw); rows=data['constraints']; assert len(rows)==2469
NS='OmissionResidual32Contexts'
PRE='open scoped BigOperators\nopen ErdosSzekeres\nnamespace OmissionResidual32Transfer\nset_option maxRecDepth 100000\nset_option maxHeartbeats 100000000\n'
geo=[]; mapping=[]
def add(row,support,demand,theorem):
 geo.append((support,demand,theorem));mapping.append({'row':row,'support_expression':support,'demand_expression':demand,'theorem':theorem.split(' c ')[0]})
for r in range(2295,2316):
 i=r-2295;add(r,f'AdditionalResidualRows.support {i}',f'AdditionalResidualRows.demand {i}',f'AdditionalResidualRows.all_rows c noCap noOctagon noJunction {i}')
for r in range(2316,2340):
 i=r-2316;add(r,f'GeneralResidualBlocks.support {i}',f'GeneralResidualBlocks.demand {i}',f'GeneralResidualBlocks.all_rows c noCap noOctagon noJunction {i}')
families={}
for name in ['CoupledVariants','CoupledSecondVariants','CoupledThirdVariants','CoupledFourthVariants','CoupledFifthVariants']:
 text=(ROOT/f'ErdosSzekeres/Omission/{name}.lean').read_text()
 maps=re.findall(r'(?:private )?def state\d+ : Fin \d+ → Fin 154 := !\[([^]]+)\]',text)
 families[name]=[sorted(map(int,s.split(','))) for s in maps]
singletons={2397:'CoupledCoreThird',2398:'CoupledDemandTwo',2426:'CoupledCoreFifth',2455:'CoupledCoreEleven',2456:'CoupledCoreNine'}
for r in range(2340,2457):
 if r in singletons:
  name=singletons[r]; sup=f'{name}.support'+('' if r==2398 else '.toFinset')
  add(r,sup,str(rows[r]['rhs']),f'{name}.hole_bound c noCap noOctagon noJunction')
 else:
  hits=[(name,i) for name,ss in families.items() for i,s in enumerate(ss) if s==sorted(rows[r]['support'])]
  assert hits,(r,rows[r]);name,i=hits[0]
  add(r,f'{name}.support {i}','1',f'{name}.all_rows c noCap noOctagon noJunction {i}')
assert len(geo)==162

def vec(xs):return '!['+', '.join(xs)+']'
def cases(xs):
 s='(fun i => Fin.elim0 i)'
 for x in reversed(xs):s=f'(Fin.cases ({x}) {s})'
 return s

def bindings(name,count,offset,oldns,oldmodule):
 lines=['import Residual32ContextsProof.Catalog',f'import {oldmodule}',PRE]
 for start in range(0,count,128):
  size=min(128,count-start)
  lines += [f'theorem {name}_chunk_{start} : ∀ r : Fin {size},',f'    {NS}.support ⟨{offset+start} + r.val, by omega⟩ = {oldns}.support ⟨{start} + r.val, by omega⟩ ∧',f'    {NS}.demand ⟨{offset+start} + r.val, by omega⟩ = {oldns}.demand ⟨{start} + r.val, by omega⟩ := by', '  decide +kernel','']
 lines += [f'theorem {name}_matches (r : Fin {count}) :',f'    {NS}.support ⟨{offset} + r.val, by omega⟩ = {oldns}.support r ∧',f'    {NS}.demand ⟨{offset} + r.val, by omega⟩ = {oldns}.demand r := by']
 for start in range(0,count,128):
  size=min(128,count-start)
  lines += [f'  by_cases h{start} : r.val < {start+size}',f'  · let k : Fin {size} := ⟨r.val - {start}, by omega⟩',f'    have hk : {start} + k.val = r.val := by dsimp [k]; omega',f'    have he : ({offset+start} + k.val) = {offset} + r.val := by omega',f'    have hi : (⟨{start} + k.val, by omega⟩ : Fin {count}) = r := Fin.ext hk',f'    have hchunk := {name}_chunk_{start} k', '    rw [hi] at hchunk', '    simpa only [he] using hchunk']
 lines+=['  omega',f'#print axioms {name}_matches','end OmissionResidual32Transfer']
 (OUT/f'{name.title()}Binding.lean').write_text('\n'.join(lines)+'\n')
bindings('original',1187,0,'OmissionResidual','Catalog')
bindings('oldcuts',1108,1187,'ResidualCoverCutsV2','ResidualCoverCutsV2')
imports=['AdditionalResidualRows','GeneralResidualBlocks','CoupledVariants','CoupledSecondVariants','CoupledThirdVariants','CoupledFourthVariants','CoupledFifthVariants','CoupledDemandTwo','CoupledFifthObstruction','CoupledElevenObstruction','CoupledNineObstruction']
lines=['import Residual32ContextsProof.Catalog']+[f'import ErdosSzekeres.Omission.{n}' for n in imports]+[PRE,'open ErdosSzekeres.Omission',
 f'def geometricSupport : Fin 162 → Finset (Fin 154) := {vec([x[0] for x in geo])}',f'def geometricDemand : Fin 162 → ℕ := {vec([x[1] for x in geo])}',
 'theorem geometric_matches : ∀ r : Fin 162,',f'    {NS}.support ⟨2295 + r.val, by omega⟩ = geometricSupport r ∧',f'    {NS}.demand ⟨2295 + r.val, by omega⟩ = geometricDemand r := by','  decide +kernel',
 'theorem geometric_rows {n : ℕ} (c : Configuration n)', '    (noCap : ¬ c.HasCap 6)', '    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))', '    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :', '    ∀ r : Fin 162, geometricDemand r ≤', '      (geometricSupport r \\ c.residualOccupied noCap noOctagon noJunction).card := by', '  unfold geometricSupport geometricDemand','  exact '+cases([x[2] for x in geo]), '#print axioms geometric_matches','#print axioms geometric_rows','end OmissionResidual32Transfer']
(OUT/'GeometricBinding.lean').write_text('\n'.join(lines)+'\n')
# Every final cut uses only earlier rows. We retain the exact source indices.
cuts=json.loads((SOURCE.parent/'cover-cuts.json').read_text())['proofs']
lines=['import Residual32ContextsProof.Catalog','import ErdosSzekeres.Omission.CoverCuts',PRE,'open ErdosSzekeres.OmissionCertificates']
for i,cut in enumerate(cuts):
 rid=2457+i;assert cut['row']==rid;assert cut['support']==rows[rid]['support'] and cut['rhs']==rows[rid]['rhs']
 ss=[];ds=[];ws=[];hs=[]
 for parent,w in cut['weights']:
  assert parent<rid
  ss.append(f'{NS}.support {parent}');ds.append(f'{NS}.demand {parent}');ws.append(str(w))
  hs.append(f'hrows ⟨{parent}, by omega⟩' if parent<2457 else f'cut{parent-2457} holes hbool hrows')
 lines += [f'theorem cut{i} (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)',f'    (hrows : ∀ r : Fin 2457, {NS}.demand ⟨r.val, by omega⟩ ≤',f'      ∑ i ∈ {NS}.support ⟨r.val, by omega⟩, holes i) :',f'    {NS}.demand {rid} ≤ ∑ i ∈ {NS}.support {rid}, holes i := by',f'  apply rounded_cover_cut {vec(ss)} {vec(ds)} {vec(ws)}',f'    ({NS}.support {rid}) {cut["capacity"]} ({NS}.demand {rid}) (by decide +kernel) holes hbool','  exact '+cases(hs),f'#print axioms cut{i}']
lines+=['theorem new_cut_rows (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)',f'    (hrows : ∀ r : Fin 2457, {NS}.demand ⟨r.val, by omega⟩ ≤',f'      ∑ i ∈ {NS}.support ⟨r.val, by omega⟩, holes i) :',f'    ∀ r : Fin 12, {NS}.demand ⟨2457 + r.val, by omega⟩ ≤',f'      ∑ i ∈ {NS}.support ⟨2457 + r.val, by omega⟩, holes i := by', '  exact '+cases([f'cut{i} holes hbool hrows' for i in range(12)]),'#print axioms new_cut_rows','end OmissionResidual32Transfer']
(OUT/'NewCuts.lean').write_text('\n'.join(lines)+'\n')
manifest={'source_sha256':hashlib.sha256(raw).hexdigest(),'geometric_rows':mapping,'original_range':[0,1186],'oldcuts_range':[1187,2294],'geometric_range':[2295,2456],'newcuts_range':[2457,2468],'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*.lean')},'lean_checked':False}
(OUT/'mapping.json').write_text(json.dumps(manifest,indent=2)+'\n')
print({k:len(v) if isinstance(v,list) else v for k,v in manifest.items() if k not in ('files',)})
