#!/usr/bin/env python3
"""Fresh kernel check of the exact case-4 Boolean witness; run under lake env.

Prerequisite: the maintained library and the separately checked
Residual32ContextsProof.Catalog must already be built. No frozen object is rebuilt.
"""
import argparse,gzip,hashlib,json,os,re,subprocess,time
from pathlib import Path
from check_witness import check,SOURCE_SHA
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--catalog',type=Path,default=ROOT/'.cache/residual32-context-certificates-2026-10-10');p.add_argument('--output',type=Path,default=ROOT/'.cache/residual32-case4-2026-10-10');p.add_argument('--preflight-only',action='store_true');a=p.parse_args()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
witness=json.loads((HERE/'witness.json').read_text());source=HERE/witness['source_reference'];raw=gzip.decompress(source.read_bytes());finite=check(raw,witness)
match=re.search(r'def missing : Finset \(Fin 154\) :=\s*\{([^}]+)\}',(HERE/'Witness.lean').read_text());assert match and [int(x.strip()) for x in match[1].split(',')]==witness['holes'],'Lean/Python witness mismatch'
context_bundle=ROOT/'experiments/omission-residual32-context-certificates-2026-10-10';manifest_path=context_bundle/'manifest.json';record_path=context_bundle/'kernel-check.json';manifest=json.loads(manifest_path.read_text());record=json.loads(record_path.read_text())
assert manifest['source_uncompressed_sha256']==SOURCE_SHA
assert sha(manifest_path)==record['manifest_sha256']
assert record['all_modules_passed']
catalog_source=context_bundle/'Residual32ContextsProof/Catalog.lean';catalog_object=a.catalog/'Residual32ContextsProof/Catalog.olean'
assert sha(catalog_source)==manifest['files']['Residual32ContextsProof/Catalog.lean']
module=next(m for m in record['modules'] if m['module']=='Residual32ContextsProof.Catalog')
assert sha(catalog_source)==module['source_sha256'] and sha(catalog_object)==module['olean_sha256'],'Catalog source/object mismatch'
inputs=[source,manifest_path,record_path,catalog_source,catalog_object,ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
inputs+=sorted((ROOT/'ErdosSzekeres').rglob('*.lean'))+sorted((ROOT/'.lake/build/lib/lean/ErdosSzekeres').rglob('*.olean'))
identities={str(x.relative_to(ROOT)) if x.is_relative_to(ROOT) else str(x):sha(x) for x in inputs}
if a.preflight_only:
 print(json.dumps({'preflight':True,'input_identities':len(identities),'witness':finite},indent=2));raise SystemExit(0)
a.output.mkdir(parents=True,exist_ok=True)
env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join([str(a.output.resolve()),str(a.catalog.resolve()),env.get('LEAN_PATH','')]);env['LEAN_NUM_THREADS']='1'
modules={'Witness':['missing_card','all_rows','fixed_context','zero_occupied','holes_boolean','sum_holes','total_holes','allows_thirty_two_holes','no_universal_thirty_three_hole_bound'],'ExistingFamilies':['all_first_variants','all_second_variants','all_third_variants','all_fourth_variants','all_fifth_variants','later_nine_rows']}
report={'scope':'Boolean witness to feasibility of the exact frozen row relaxation; geometric realizability is not claimed','lean':subprocess.check_output(['lean','--version'],text=True,env=env).strip(),'source_uncompressed_sha256':SOURCE_SHA,'checker_sha256':sha(Path(__file__)),'witness_json_sha256':sha(HERE/'witness.json'),'finite_check':finite,'inputs':identities,'modules':{},'complete':False};audits=[]
for module,names in modules.items():
 src=HERE/(module+'.lean');obj=a.output/(module+'.olean');t=time.monotonic()
 for word in ['sorry','admit','native_decide']:
  assert not re.search(r'\b'+word+r'\b',src.read_text()),word
 proc=subprocess.run(['lean','-j1','-s','32768','-M','10000',str(src),'-o',str(obj)],env=env,text=True,capture_output=True,cwd=ROOT)
 log=a.output/(module+'.log');log.write_text(proc.stdout+proc.stderr)
 item={'exit':proc.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(src),'log_sha256':sha(log),'axioms':{}}
 if proc.returncode==0:
  item['olean_sha256']=sha(obj)
  for name in names:
   fullname='OmissionResidual32Case4.'+name
   m=re.search(re.escape("'"+fullname+"'")+r' depends on axioms: \[([^]]*)\]',proc.stdout)
   if m:axioms=sorted(x.strip() for x in m[1].split(',') if x.strip())
   else:assert f"'{fullname}' does not depend on any axioms" in proc.stdout;axioms=[]
   assert set(axioms)<={'propext','Classical.choice','Quot.sound'}
   item['axioms'][fullname]=axioms
  audits.append(proc.stdout)
 report['modules'][module]=item;(HERE/'kernel-check.json').write_text(json.dumps(report,indent=2)+'\n')
 print(module,proc.returncode,item['seconds'],flush=True)
 if proc.returncode:print(proc.stdout+proc.stderr);raise SystemExit(proc.returncode)
for path,h in identities.items():assert sha(ROOT/path)==h,('Input changed during compilation',path)
(HERE/'axioms.txt').write_text('\n'.join(audits));report['axioms_sha256']=sha(HERE/'axioms.txt');report['complete']=True
(HERE/'kernel-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('Both modules passed, 15 conclusions audited, standard axioms only.',flush=True)
