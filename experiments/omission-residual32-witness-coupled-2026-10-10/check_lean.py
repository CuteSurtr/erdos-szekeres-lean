#!/usr/bin/env python3
"""Check the new coupled row, old-template row, and exact witness separation.

Run under lake env after the case-4 witness bundle has passed its own checker.
All generated objects stay in a fresh ignored directory.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,re,subprocess,time
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'.cache/residual32-witness-coupled-2026-10-10');p.add_argument('--witness',type=Path,default=ROOT/'.cache/residual32-case4-2026-10-10');p.add_argument('--catalog',type=Path,default=ROOT/'.cache/residual32-context-certificates-2026-10-10');p.add_argument('--preflight-only',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bundle=ROOT/'experiments/omission-residual32-case4-2026-10-10';wr_path=bundle/'kernel-check.json';wr=json.loads(wr_path.read_text());assert wr['complete']
assert sha(bundle/'check_lean.py')==wr['checker_sha256']
assert sha(bundle/'Witness.lean')==wr['modules']['Witness']['source_sha256'];assert sha(a.witness/'Witness.olean')==wr['modules']['Witness']['olean_sha256']
for path,h in wr['inputs'].items():assert sha(ROOT/path)==h,('Witness input changed',path)
cat=a.catalog/'Residual32ContextsProof/Catalog.olean';expected=wr['inputs']['.cache/residual32-context-certificates-2026-10-10/Residual32ContextsProof/Catalog.olean'];assert sha(cat)==expected
exporter=ROOT/'scripts/export_omission_coupled_sized.py';spec=importlib.util.spec_from_file_location('core_export',exporter);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
regenerated=a.output/'LeanCore-regenerated.lean';mod.export(HERE/'core13.json',regenerated,'CoupledCoreSixth',HERE.name,'core13');generated=regenerated.read_text().replace('../../experiments/'+HERE.name+'/','');assert generated==(HERE/'LeanCore.lean').read_text(),'Core differs from exact regenerated semantics'
inputs=dict(wr['inputs'])
for path in [wr_path,bundle/'Witness.lean',a.witness/'Witness.olean',cat,exporter,HERE/'core13.json',HERE/'core13.cnf',HERE/'core13.lrat']:
 inputs[str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)]=sha(path)
if a.preflight_only:print(json.dumps({'preflight':True,'inputs':len(inputs),'core_regenerated':True}));raise SystemExit(0)
env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join([str(a.output.resolve()),str(a.witness.resolve()),str(a.catalog.resolve()),env.get('LEAN_PATH','')]);env['LEAN_NUM_THREADS']='1'
modules={'LeanCore':('ErdosSzekeres.Omission.CoupledCoreSixth',['context_impossible']),'Geometry':('ErdosSzekeres.Omission.CoupledCoreSixth',['states_injective','exists_missing_state','hole_bound','witness_violates_coupled','strict_strengthening','countermodel_not_realizable']),'TemplateRow':('ErdosSzekeres.Omission.CoupledFourthWitnessVariant',['checked','hole_bound','witness_violates_row','strict_strengthening'])}
report={'scope':'Geometric omission rows and exact separation from the frozen2469-row relaxation; no new global ES(8) bound','lean':subprocess.check_output(['lean','--version'],text=True,env=env).strip(),'checker_sha256':sha(Path(__file__)),'inputs':inputs,'modules':{},'complete':False};audits=[]
for module,(namespace,names) in modules.items():
 src=HERE/(module+'.lean');obj=a.output/(module+'.olean');t=time.monotonic()
 assert not re.search(r'\b(sorry|admit|native_decide)\b',src.read_text())
 proc=subprocess.run(['lean','-j1','-s','32768','-M','10000',str(src),'-o',str(obj)],env=env,text=True,capture_output=True,cwd=ROOT)
 log=a.output/(module+'.log');log.write_text(proc.stdout+proc.stderr)
 item={'exit':proc.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(src),'log_sha256':sha(log),'axioms':{}}
 if proc.returncode==0:
  item['olean_sha256']=sha(obj)
  for name in names:
   fullname=namespace+'.'+name;m=re.search(re.escape("'"+fullname+"'")+r' depends on axioms: \[([^]]*)\]',proc.stdout)
   if m:axioms=sorted(x.strip() for x in m[1].split(',') if x.strip())
   else:assert f"'{fullname}' does not depend on any axioms" in proc.stdout;axioms=[]
   assert set(axioms)<={'propext','Classical.choice','Quot.sound'};item['axioms'][fullname]=axioms
  audits.append(proc.stdout)
 report['modules'][module]=item;(HERE/'kernel-check.json').write_text(json.dumps(report,indent=2)+'\n');print(module,proc.returncode,item['seconds'],flush=True)
 if proc.returncode:print(proc.stdout+proc.stderr);raise SystemExit(proc.returncode)
for path,h in inputs.items():assert sha(ROOT/path)==h,('Input changed during compilation',path)
(HERE/'axioms.txt').write_text('\n'.join(audits));report['axioms_sha256']=sha(HERE/'axioms.txt');report['complete']=True
(HERE/'kernel-check.json').write_text(json.dumps(report,indent=2)+'\n');print('All three modules passed; 11 conclusions use only standard axioms.',flush=True)
