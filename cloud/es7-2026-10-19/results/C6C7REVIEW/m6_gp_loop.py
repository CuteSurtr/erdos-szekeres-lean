#!/usr/bin/env python3
"""Bounded full-GP refinement after the verified rotation-cycle families."""
import argparse,datetime,hashlib,json,re,subprocess,sys,time
from pathlib import Path


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True,type=Path);ap.add_argument('--checker',required=True,type=Path);ap.add_argument('--cadical',required=True,type=Path);ap.add_argument('--deadline-utc',required=True);ap.add_argument('--rounds',type=int,default=8);ap.add_argument('--start-index',type=int,default=0);ap.add_argument('--model',type=Path);ap.add_argument('--family',type=Path);a=ap.parse_args()
 root=a.archive;here=Path(__file__).resolve().parent;start=time.monotonic();deadline=datetime.datetime.fromisoformat(a.deadline_utc)
 model=a.model or root/'family_run2/model.json';family=a.family or root/'combined_families01_gp2.clauses';manifest=[]
 suffix=f'_{a.start_index:02d}' if a.start_index else ''
 log=(root/f'gp_loop{suffix}.jsonl').open('w',buffering=1)
 def emit(event,**kw):
  row={'event':event,'seconds':round(time.monotonic()-start,3),**kw};s=json.dumps(row,sort_keys=True);print(s,flush=True);log.write(s+'\n')
 def archive(p):
  z=Path(str(p)+'.zst');subprocess.run(['zstd','-q','-3','-T1','-f',str(p),'-o',str(z)],check=True)
  raw=p.read_bytes();assert subprocess.check_output(['zstd','-q','-dc',str(z)])==raw
  manifest.append({'file':str(p.relative_to(root)),'raw_sha256':hashlib.sha256(raw).hexdigest(),'zstd_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'roundtrip':True})
  (root/f'gp_loop{suffix}_archive_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 def call(script,args,out):
  with out.open('w') as f:subprocess.run([sys.executable,'-I',str(here/script),*map(str,args)],stdout=f,stderr=subprocess.STDOUT,check=True)
 for it in range(a.start_index,a.start_index+a.rounds):
  if (deadline-datetime.datetime.now(datetime.timezone.utc)).total_seconds()<30:emit('stop',reason='budget');break
  rd=root/f'gp_refine{it:02d}';rd.mkdir(exist_ok=True)
  call('m6_full_gp.py',['--model',model,'--checker',a.checker,'--out',rd,'--max-output',100000],rd/'check_console.log')
  check=json.loads((rd/'full_gp_check.json').read_text());viol=int(re.search(r'violated (\d+)',check['verdict']).group(1));emit('full_gp',round=it,model=str(model.relative_to(root)),violations=viol)
  archive(rd/'full_gp_check.json');archive(rd/'full_gp_violations.txt')
  if not viol:emit('gp_consistent',model=str(model.relative_to(root)),sha256=hashlib.sha256(model.read_bytes()).hexdigest());break
  assert len((rd/'full_gp_violations.txt').read_text().splitlines())==viol
  call('m6_gp_refine.py',['--model',model,'--violations',rd/'full_gp_violations.txt','--out',rd],rd/'refine_console.log')
  for p in (rd/'gp_refinement.clauses',rd/'gp_refinement_verified.json'):archive(p)
  lines=set(family.read_text().splitlines())|set((rd/'gp_refinement.clauses').read_text().splitlines())
  family=rd/'combined.clauses';family.write_text('\n'.join(sorted(lines))+'\n');archive(family)
  label=f'gp_run{it:02d}'
  call('m6_family_run.py',['--archive',root,'--cadical',a.cadical,'--label',label,'--family',family,'--deadline-utc',a.deadline_utc,'--seconds',120],rd/'solve_console.log')
  events=[json.loads(x) for x in (root/label/'run.jsonl').read_text().splitlines()];result=next((x for x in events if x['event']=='result'),{})
  emit('solve',round=it,status=result.get('status','UNKNOWN'),family_clauses=len(lines))
  if result.get('status')!='SAT':break
  model=root/label/'model.json'
 emit('finish',last_model=str(model.relative_to(root)),last_family=str(family.relative_to(root)))
 log.close()
if __name__=='__main__':main()
