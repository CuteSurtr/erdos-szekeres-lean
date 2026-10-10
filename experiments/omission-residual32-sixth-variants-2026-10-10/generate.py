#!/usr/bin/env python3
"""Generate the reusable Sixth compatible template; Lean checks output."""
from pathlib import Path
import gzip,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
core=ROOT/'experiments/omission-residual32-witness-coupled-2026-10-10'
subprocess.run([sys.executable,str(ROOT/'scripts/export_omission_coupled_template_sized.py'),'--source',str(core/'core13.json'),'--core',str(core/'LeanCore.lean'),'--namespace','CoupledTemplateSixth','--output',str(HERE/'SixthTemplate.lean')],check=True)
p=HERE/'SixthTemplate.lean';p.write_text(p.read_text().replace('LeanCore','CoupledCoreSixth').replace('import ErdosSzekeres.Omission.CoupledCoreSixth','import LeanCore'))
for suffix in ['Check','Geometry']:
 src=ROOT/('ErdosSzekeres/Omission/CoupledTemplateFifth'+suffix+'.lean');p=HERE/('SixthTemplate'+suffix+'.lean')
 p.write_text(src.read_text().replace('import ErdosSzekeres.Omission.CoupledTemplateFifth','import SixthTemplate').replace('CoupledTemplateFifth','CoupledTemplateSixth'))
p=HERE/'SixthTemplateCheck.lean';s=p.read_text();p.write_text(s.replace('end ErdosSzekeres.Omission.CoupledTemplateSixth','#print axioms check_sound\nend ErdosSzekeres.Omission.CoupledTemplateSixth'))
p=HERE/'SixthTemplateGeometry.lean';s=p.read_text();p.write_text(s.replace('#print axioms hole_bound','#print axioms exists_missing_index\n#print axioms hole_bound'))
print('Generated three generic template modules; literal variants remain computational diagnostics.')
