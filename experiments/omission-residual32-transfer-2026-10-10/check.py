#!/usr/bin/env python3
"""Compile the standalone transfer with pinned imports; run under lake env."""
from pathlib import Path
import argparse,gzip,hashlib,json,os,re,subprocess,time
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
for name,default in [('contexts','.cache/residual32-context-certificates-2026-10-10'),('arithmetic','.cache/omission-lean-full/residual'),('cycles','.cache/omission-residual-geometry'),('blocks','.cache/omission-residual-blocks'),('old-cuts','.cache/omission-cover-transfer-residual-v2'),('output','.cache/residual32-transfer-2026-10-10')]:
 parser.add_argument('--'+name,type=Path,default=ROOT/default)
args=parser.parse_args()
CACHE=args.output.resolve();CACHE.mkdir(parents=True,exist_ok=True)
paths=[CACHE,args.contexts.resolve(),args.arithmetic.resolve(),args.cycles.resolve(),args.blocks.resolve(),args.old_cuts.resolve()]
env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(map(str,paths))+os.pathsep+env.get('LEAN_PATH','');env['LEAN_NUM_THREADS']='1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Verify external source identities before loading their compiled objects.
context_bundle=ROOT/'experiments/omission-residual32-context-certificates-2026-10-10'
manifest=json.loads((HERE/'mapping.json').read_text())
for name,expected in manifest['files'].items():
 assert sha(HERE/name)==expected, ('changed transfer source',name)
context_manifest=json.loads((context_bundle/'manifest.json').read_text())
assert context_manifest['source_uncompressed_sha256']==manifest['source_sha256']
source=ROOT/'experiments/omission-residual32-research-2026-10-10/source.json.gz'
assert hashlib.sha256(gzip.decompress(source.read_bytes())).hexdigest()==manifest['source_sha256']
external_sources={}
def bind_source(path,expected):
 assert path.exists(), f'Missing prerequisite source: {path}'
 assert sha(path)==expected, f'Changed prerequisite source: {path}'
 external_sources[str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)]=expected
geo_bundle=ROOT/'experiments/omission-residual-geometry-2026-10-09'
original_raw=gzip.decompress((geo_bundle/'Catalog.lean.gz').read_bytes())
bind_source(paths[2]/'Catalog.lean',hashlib.sha256(original_raw).hexdigest())
for folder,key in [(paths[3],'cycles'),(paths[4],'blocks')]:
 original_manifest=json.loads((geo_bundle/(key+'-export.json')).read_text())
 for name,expected in original_manifest['files'].items():bind_source(folder/name,expected)
cut_source=ROOT/'experiments/omission-cover-certificates-2026-10-10/ResidualCoverCutsV2.lean'
bind_source(paths[5]/'ResidualCoverCutsV2.lean',sha(cut_source))
for name,expected in context_manifest['files'].items():bind_source(context_bundle/name,expected)
modules={'OriginalBinding' :['original_matches'],'OldcutsBinding':['oldcuts_matches'],'GeometricBinding':['geometric_matches','geometric_rows'],'NewCuts':['new_cut_rows'],'Transfer':['prior_rows','all_rows','feasible_holes','residual_bound_of_hole_budget'],'ContextGeometry':['context_impossible_of_exclusion','geometric_node492360','geometric_node492359','geometric_node485523','geometric_node485522','geometric_node30','geometric_parent492360','geometric_parent485523']}
report={'scope':'Literal binding of all2469 research rows to actual residual geometry; no arithmetic exclusion asserted','lean':subprocess.check_output(['lean','--version'],text=True,env=env).strip(),'source_sha256':'f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909','modules':{},'complete':False,'checker_sha256':sha(Path(__file__)),'mapping_sha256':sha(HERE/'mapping.json'),'external_sources':external_sources}
# Hash the imported object closure, along with its available sources. These are
# built outputs of existing checked source packages, not additional axioms.
inputs=[ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
for p in paths[1:]:inputs+=sorted(p.rglob('*.olean'))
inputs+=sorted((ROOT/'.lake/build/lib/lean/ErdosSzekeres').rglob('*.olean'))
report['imports']={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):sha(p) for p in inputs}
for module,theorems in modules.items():
 src=HERE/(module+'.lean');obj=CACHE/(module+'.olean');t=time.monotonic()
 p=subprocess.run(['lean','-j1','-s','32768','-M','14000',str(src),'-o',str(obj)],text=True,capture_output=True,env=env,cwd=ROOT)
 log=CACHE/(module+'.log');log.write_text(p.stdout+p.stderr)
 item={'exit':p.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(src),'log_sha256':sha(log),'stdout':p.stdout,'stderr':p.stderr}
 if p.returncode==0:
  item['olean_sha256']=sha(obj);item['axioms']={}
  for theorem in theorems:
   name='OmissionResidual32Transfer.'+theorem
   m=re.search(re.escape("'"+name+"'")+r' depends on axioms: \[([^]]*)\]',p.stdout)
   if m:
    axioms=sorted(x.strip() for x in m[1].split(',') if x.strip());assert set(axioms)<=set(['propext','Classical.choice','Quot.sound']),(name,axioms)
   else:
    assert f"'{name}' does not depend on any axioms" in p.stdout,(name,p.stdout)
    axioms=[]
   item['axioms'][name]=axioms
 report['modules'][module]=item
 (HERE/'kernel-check.json').write_text(json.dumps(report,indent=2)+'\n')
 print(module,p.returncode,item['seconds'],flush=True)
 if p.returncode:print((p.stdout+p.stderr)[-10000:],flush=True);raise SystemExit(p.returncode)
report['complete']=True
(HERE/'kernel-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('All2469 rows bound to actual geometry; no hole-budget exclusion asserted.',flush=True)
