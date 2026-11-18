#!/usr/bin/env python3
"""Freeze small parent evidence and hash retained large artifacts."""
import datetime,hashlib,json,resource,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/jay/research/data/delta3-codex-20261113/boundary')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
 out=HERE/'data';out.mkdir(exist_ok=True);archive=[]
 for name in ('sweep','realization','refined','terminal'):
  base=ROOT/name;assert (base/'DONE.json').exists()
  for p in sorted(base.rglob('*')):
   if not p.is_file() or '__pycache__' in p.parts:continue
   item={'source':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'copy':None}
   if p.suffix in ('.json','.log','.time','.py','.cpp') or (p.name.endswith('.lrat.zst') and p.stat().st_size<2_000_000):
    target=out/'archive'/name/p.relative_to(base);target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(p,target);item['copy']=str(target.relative_to(HERE))
   archive.append(item)
 terminal=[]
 for n in (6,7,8):
  r=json.loads((ROOT/f'terminal/n{n}/solve/result.json').read_text())
  assert r['status']=='UNSAT_CERTIFIED' and r['compressed_roundtrip_verified']
  assert 's VERIFIED UNSAT' in (ROOT/f'terminal/n{n}/solve/cake.log').read_text().splitlines()
  terminal.append({'n':n,'old_size':2*n-3,'status':r['status'],'hashes':r['hashes'],'seconds':r['seconds']})
 unitlog=subprocess.check_output(['journalctl','--user','-u','nov13c-vfy-delta5-*','--since','2026-11-14 03:50:00','--no-pager'],text=True)
 (out/'units.log').write_text(unitlog)
 guard=Path('/home/jay/research/data/memguard-20261113/memguard.log').read_text()
 lines=[s for s in guard.splitlines() if 'nov13c-vfy-delta5-' in s]
 assert not any(' STOP ' in s for s in lines)
 (out/'memory_guard.log').write_text('\n'.join(lines)+'\n')
 live=subprocess.check_output(['systemctl','--user','list-units','--state=running','nov13c-*','memguard*','p2-*','--no-pager'],text=True)
 assert 'nov13c-vfy-delta5-' not in live
 (out/'live_final.txt').write_text(live)
 (out/'archive_manifest.json').write_text(json.dumps(archive,indent=2)+'\n')
 summary={'label':'COMPUTED inventory','time':datetime.datetime.now().astimezone().isoformat(),
          'raw_boundary_sat':6,'raw_root_realized':3,'refined_boundary_sat_realized':3,
          'terminal_boundary_certificates':terminal,'independent_audit':'see audit/VERIFY_BOUNDARY.md',
          'all_parent_jobs_finished':True,'guard_stops':0,'weak_D57':'OPEN','weak_D58':'OPEN'}
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({'archived_items':len(archive),'certified':len(terminal),'all_parent_jobs_finished':True}))
if __name__=='__main__':main()
