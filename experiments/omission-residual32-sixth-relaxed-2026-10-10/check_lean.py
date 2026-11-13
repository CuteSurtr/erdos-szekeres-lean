#!/usr/bin/env python3
"""Serial kernel replay and axiom audit; all saved paths are repository relative."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));from check_axioms import audit_output
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'.cache/residual32-sixth-relaxed-2026-10-10');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((HERE/'manifest.json').read_text())
for name,h in manifest['files'].items():assert sha(HERE/name)==h,('Changed bundle input',name)
for name,h in manifest['external_inputs'].items():assert sha(ROOT/name)==h,('Changed external input',name)
inputs=dict(manifest['external_inputs'])
for pattern in ['ErdosSzekeres/**/*.lean','.lake/build/lib/lean/ErdosSzekeres/**/*.olean']:
 for path in sorted(ROOT.glob(pattern)):inputs[str(path.relative_to(ROOT))]=sha(path)
for name in ['lean-toolchain','lake-manifest.json']:inputs[name]=sha(ROOT/name)
env=dict(os.environ);env['LEAN_PATH']=str(a.output.resolve())+os.pathsep+env.get('LEAN_PATH','');env['LEAN_NUM_THREADS']='1'
mods=[('SixthRelaxedCore',['ErdosSzekeres.Omission.CoupledCoreSixthRelaxed.cnf_refutation']),('SixthRelaxedTemplate',['ErdosSzekeres.Omission.CoupledTemplateSixthRelaxed.context_impossible']),('SixthRelaxedTemplateCheck',['ErdosSzekeres.Omission.CoupledTemplateSixthRelaxed.check_sound']),('SixthRelaxedTemplateGeometry',['ErdosSzekeres.Omission.CoupledTemplateSixthRelaxed.exists_missing_index','ErdosSzekeres.Omission.CoupledTemplateSixthRelaxed.hole_bound']),('SixthRelaxedProof.Data',[])]+[(f'SixthRelaxedProof.Part{i:02d}',[f'ErdosSzekeres.Omission.CoupledSixthRelaxedVariants.Part{i:02d}.checked']) for i in range(3)]+[('SixthRelaxedProof.Root',['ErdosSzekeres.Omission.CoupledSixthRelaxedVariants.checked','ErdosSzekeres.Omission.CoupledSixthRelaxedVariants.all_rows'])]
report={'scope':'Reusable41-test geometric obstruction and48actual-configuration omission rows; no global313 theorem or full logical independence claimed','lean':subprocess.check_output(['lean','--version'],text=True).strip(),'checker_sha256':sha(Path(__file__)),'manifest_sha256':sha(HERE/'manifest.json'),'inputs':inputs,'modules':{},'complete':False};audits=[]
def save():(HERE/'kernel-check.json').write_text(json.dumps(report,indent=2)+'\n')
save()
for name,theorems in mods:
 relative=Path(*name.split('.'));src=HERE/relative.with_suffix('.lean');obj=a.output/relative.with_suffix('.olean');obj.parent.mkdir(parents=True,exist_ok=True)
 assert not re.search(r'\b(sorry|admit|native_decide|sorryAx|axiom)\b',src.read_text()),('Forbidden proof token',name)
 t=time.monotonic();proc=subprocess.run(['lean','-j1','-s32768','-M10000','--root='+str(HERE),str(src.relative_to(ROOT)),'-o',str(obj)],env=env,text=True,capture_output=True,cwd=ROOT)
 log=a.output/(name+'.log');output=(proc.stdout+proc.stderr).replace(str(ROOT)+os.sep,'');log.write_text(output)
 item={'exit':proc.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(src),'log_sha256':sha(log),'axioms':{}}
 if proc.returncode==0:
  item['olean_sha256']=sha(obj)
  for theorem in theorems:item['axioms'][theorem]=audit_output(output,theorem)
  audits.append(output)
 report['modules'][name]=item;save();print(name,proc.returncode,item['seconds'],flush=True)
 if proc.returncode:print(output);raise SystemExit(proc.returncode)
for name,h in inputs.items():assert sha(ROOT/name)==h,('Input changed during build',name)
(HERE/'axioms.txt').write_text('\n'.join(audits));report['axioms_sha256']=sha(HERE/'axioms.txt');report['complete']=True;save();print('All9modules checked;10audited declarations.',flush=True)
