#!/usr/bin/env python3
"""Generate ordinary Lean proofs from frozen augmented CNF and literal maps."""
from pathlib import Path
import importlib.util,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CACHE=ROOT/'.cache/residual32-sixth-relaxed-2026-10-10';CACHE.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('exporter',ROOT/'scripts/export_omission_coupled_sized.py');exporter=importlib.util.module_from_spec(spec);spec.loader.exec_module(exporter)
core=CACHE/'SixthRelaxedCore.lean';exporter.export(HERE/'augmented.json',core,'CoupledCoreSixthRelaxed',HERE.name,'augmented')
full=core.read_text().replace('../../experiments/'+HERE.name+'/','');core.write_text(full)
subprocess.run([sys.executable,str(ROOT/'scripts/export_omission_coupled_template_sized.py'),'--source',str(HERE/'augmented.json'),'--core',str(core),'--namespace','CoupledTemplateSixthRelaxed','--output',str(HERE/'SixthRelaxedTemplate.lean')],check=True)
p=HERE/'SixthRelaxedTemplate.lean';p.write_text(p.read_text().replace('SixthRelaxedCore','CoupledCoreSixthRelaxed').replace('import ErdosSzekeres.Omission.CoupledCoreSixthRelaxed','import SixthRelaxedCore'))
# Share only refutation and atom table. The generic module proves all geometry.
(HERE/'SixthRelaxedCore.lean').write_text(full[:full.index('private def clause000')]+'#print axioms cnf_refutation\nend ErdosSzekeres.Omission.CoupledCoreSixthRelaxed\n')
old=ROOT/'experiments/omission-residual32-sixth-variants-2026-10-10'
for suffix in ['Check','Geometry']:
 s=(old/('SixthTemplate'+suffix+'.lean')).read_text().replace('import SixthTemplate','import SixthRelaxedTemplate').replace('CoupledTemplateSixth','CoupledTemplateSixthRelaxed')
 (HERE/('SixthRelaxedTemplate'+suffix+'.lean')).write_text(s)
rows=json.loads((HERE/'rows.json').read_text())['rows'];N=len(rows);assert N==48
family=HERE/'SixthRelaxedProof';family.mkdir(exist_ok=True)
namespace='ErdosSzekeres.Omission.CoupledSixthRelaxedVariants'
head='\nnamespace '+namespace+'\nopen CoupledTemplateSixthRelaxed\nset_option maxRecDepth 100000\nset_option maxHeartbeats 100000000\n\n'
text='import SixthRelaxedTemplateGeometry\nimport SixthRelaxedTemplateCheck\n'+head
for i,r in enumerate(rows):text+=f'def state{i:03d} : Fin 13 → Fin 154 := !['+', '.join(map(str,r['map']))+']\n'
text+='\ndef maps : Fin 48 → Fin 13 → Fin 154 := !['+', '.join(f'state{i:03d}' for i in range(N))+']\n\ndef support (r : Fin 48) : Finset (Fin 154) := Finset.univ.image (maps r)\n\nend '+namespace+'\n';(family/'Data.lean').write_text(text)
for part in range(3):
 name=f'Part{part:02d}';start=part*16;text='import SixthRelaxedProof.Data\n'+head+'namespace '+name+'\n'
 for i in range(start,start+16):text+=f'private theorem checked{i:03d} : Function.Injective state{i:03d} ∧ Compatible state{i:03d} := by\n  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩\n\n'
 text+=f'theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨{start} + r.val, by omega⟩) ∧\n    Compatible (maps ⟨{start} + r.val, by omega⟩) := by\n  intro r\n  fin_cases r\n'+''.join(f'  · exact checked{i:03d}\n' for i in range(start,start+16))+'#print axioms checked\nend '+name+'\nend '+namespace+'\n';(family/(name+'.lean')).write_text(text)
text=''.join(f'import SixthRelaxedProof.Part{part:02d}\n' for part in range(3))+head
text+='theorem checked : ∀ r : Fin 48, Function.Injective (maps r) ∧ Compatible (maps r) := by\n  intro r\n  fin_cases r\n'+''.join(f'  · exact Part{i//16:02d}.checked {i%16}\n' for i in range(N))
text+='''
/-- Every literal row is valid in an actual residual configuration. -/
theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 48, 1 ≤ (support r \\ c.residualOccupied noCap noOctagon noJunction).card := by
  intro r
  exact CoupledTemplateSixthRelaxed.hole_bound (maps r) (checked r).1 (checked r).2
    c noCap noOctagon noJunction
#print axioms checked
#print axioms all_rows
end '''+namespace+'\n';(family/'Root.lean').write_text(text)
print('Generated9modules: refutation, generic template/check/geometry, literal data+3parts+root.')
