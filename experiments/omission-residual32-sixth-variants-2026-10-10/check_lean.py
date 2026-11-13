#!/usr/bin/env python3
"""Kernel-check the reusable Sixth template only, using the frozen core proof."""
import argparse,hashlib,json,os,re,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--core',type=Path,default=ROOT/'.cache/residual32-witness-coupled-2026-10-10');p.add_argument('--output',type=Path,default=ROOT/'.cache/residual32-sixth-variants-2026-10-10');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cb=ROOT/'experiments/omission-residual32-witness-coupled-2026-10-10';cr=json.loads((cb/'kernel-check.json').read_text());assert cr['complete'];assert sha(cb/'LeanCore.lean')==cr['modules']['LeanCore']['source_sha256'];assert sha(a.core/'LeanCore.olean')==cr['modules']['LeanCore']['olean_sha256']
inputs={k:v for k,v in cr['inputs'].items() if k.startswith('ErdosSzekeres/') or k.startswith('.lake/build/lib/lean/ErdosSzekeres/') or k in ['lean-toolchain','lake-manifest.json']}
for path in [cb/'kernel-check.json',cb/'LeanCore.lean',cb/'core13.json',cb/'core13.cnf',cb/'core13.lrat',a.core/'LeanCore.olean',ROOT/'scripts/export_omission_coupled_template_sized.py',ROOT/'ErdosSzekeres/Omission/CoupledTemplateFifthCheck.lean',ROOT/'ErdosSzekeres/Omission/CoupledTemplateFifthGeometry.lean']:
 inputs[str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)]=sha(path)
for path,h in inputs.items():assert sha(ROOT/path)==h,('Changed input',path)
env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join([str(a.output.resolve()),str(a.core.resolve()),env.get('LEAN_PATH','')]);env['LEAN_NUM_THREADS']='1'
mods={'SixthTemplate':['context_impossible'],'SixthTemplateCheck':['check_sound'],'SixthTemplateGeometry':['exists_missing_index','hole_bound']}
report={'scope':'Generic compatible-map geometry for the sixth core; no literal variant proofs or global population bound','lean':subprocess.check_output(['lean','--version'],text=True,env=env).strip(),'checker_sha256':sha(Path(__file__)),'inputs':inputs,'modules':{},'complete':False};audits=[]
for name,ths in mods.items():
 src=HERE/(name+'.lean');obj=a.output/(name+'.olean');t=time.monotonic();assert not re.search(r'\b(sorry|admit|native_decide)\b',src.read_text())
 proc=subprocess.run(['lean','-j1','-s','32768','-M','10000',str(src),'-o',str(obj)],env=env,text=True,capture_output=True,cwd=ROOT);log=a.output/(name+'.log');log.write_text(proc.stdout+proc.stderr)
 item={'exit':proc.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(src),'log_sha256':sha(log),'axioms':{}}
 if proc.returncode==0:
  item['olean_sha256']=sha(obj)
  for th in ths:
   fullname='ErdosSzekeres.Omission.CoupledTemplateSixth.'+th;m=re.search(re.escape("'"+fullname+"'")+r' depends on axioms: \[([^]]*)\]',proc.stdout)
   if m:axs=sorted(x.strip() for x in m[1].split(',') if x.strip())
   else:assert f"'{fullname}' does not depend on any axioms" in proc.stdout;axs=[]
   assert set(axs)<={'propext','Classical.choice','Quot.sound'};item['axioms'][fullname]=axs
  audits.append(proc.stdout)
 report['modules'][name]=item;(HERE/'kernel-check.json').write_text(json.dumps(report,indent=2)+'\n');print(name,proc.returncode,item['seconds'],flush=True)
 if proc.returncode:print(proc.stdout+proc.stderr);raise SystemExit(proc.returncode)
for path,h in inputs.items():assert sha(ROOT/path)==h,('Input changed',path)
(HERE/'axioms.txt').write_text('\n'.join(audits));report['axioms_sha256']=sha(HERE/'axioms.txt');report['complete']=True;(HERE/'kernel-check.json').write_text(json.dumps(report,indent=2)+'\n');print('Three generic modules passed; four standard-axiom roots.',flush=True)
