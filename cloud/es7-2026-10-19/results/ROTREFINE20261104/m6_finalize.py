#!/usr/bin/env python3
"""Close a stopped campaign: exact final composition, hashes, and compact report."""
import argparse, collections, hashlib, json, shutil, subprocess
from pathlib import Path

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for data in iter(lambda:f.read(1<<20),b''):h.update(data)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True);a=ap.parse_args();root=a.archive
 here=Path(__file__).resolve().parent
 events=[json.loads(x) for x in (root/'events.jsonl').read_text().splitlines()]
 assert events[-1]['event']=='finished' and events[-1]['all_children_reaped'], 'worker must be stopped'
 status=json.loads((root/'status.json').read_text());blocks=json.loads((root/'cut_prefix.json').read_text())
 with (root/'current.cnf').open('rb') as f:header=f.readline().split()
 nv,nc=int(header[2]),int(header[3]);assert nc==3381621+sum(b['clauses'] for b in blocks)
 expected=hashlib.sha256(f'p cnf {nv} {nc}\n'.encode())
 with (root/'base.cnf').open('rb') as f:
  f.readline()
  for data in iter(lambda:f.read(1<<20),b''):expected.update(data)
 for block in blocks:
  p=root/block['path'];assert digest(p)==block['sha256']
  with p.open('rb') as f:
   for data in iter(lambda:f.read(1<<20),b''):expected.update(data)
 final_sha=digest(root/'current.cnf');assert final_sha==expected.hexdigest()
 final_input={'base_sha256':digest(root/'base.cnf'),'blocks':[{'path':b['path'],'sha256':b['sha256']} for b in blocks],'variables':nv,'clauses':nc,'cnf_sha256':final_sha}
 (root/'final_input.json').write_text(json.dumps(final_input,indent=2)+'\n')
 sat=[e for e in events if e['event']=='SAT'];assess={e['model_sha256']:e for e in events if e['event']=='candidate_assessed'}
 outputs=[]
 for e in sat:
  inp=json.loads((root/e['input']).read_text());outputs.append({'model':e['path'],'model_sha256':e['sha256'],'input_record':e['input'],'cnf_sha256':inp['cnf_sha256'],'clauses':inp['clauses']})
 (root/'solver_outputs.json').write_text(json.dumps({'note':'Use this binding; same-folder assignment.json assesses the preceding candidate.','models':outputs},indent=2)+'\n')
 outcomes=json.loads((root/'survivor_outcomes.json').read_text())['survivors']
 assert {r['model_sha256'] for r in outcomes}=={e['model_sha256'] for e in events if e['event']=='gp_consistent_survivor'}
 methods=collections.Counter(s['method'] for row in outcomes for s in row['separation'])
 full=[]
 for p in [*(root/'iterations').glob('*/full_product/full/verified.json'),*root.glob('full_product_model*/full/verified.json')]:
  x=json.loads(p.read_text());full.append({'model_sha256':x['model_sha256'],'acyclic':x['acyclic'],'evidence':str(p.relative_to(root))})
 old_units=True;peak_total=0.;peak_lane=0
 for e in events:
  if e['event']=='resumed':old_units=False
  if 'peak_total_gb' in e:peak_total=max(peak_total,e['peak_total_gb']*(1024**3/1e9 if old_units else 1))
  peak_lane=max(peak_lane,e.get('peak_lane_rss_bytes',0))
 last_sha=status['last_model_sha256'];last_assessment=assess.get(last_sha)
 summary={'status':status['stop_reason'],'last_event_utc':events[-1]['utc'],'all_children_reaped':True,'SAT_models_retained':len(sat),'UNSAT_events':sum(e['event']=='UNSAT' for e in events),'UNKNOWN_events':sum(e['event']=='UNKNOWN' for e in events),'full_GP_survivors':len(outcomes),'separation_methods':dict(methods),'unseparated_survivors':[r['model'] for r in outcomes if not r['separation']],'cut_blocks':len(blocks),'cut_types':dict(collections.Counter(b['kind'] for b in blocks)),'variables':nv,'final_clauses':nc,'final_cnf_sha256':final_sha,'final_composition_reconstructed':True,'last_model':status['last_model'],'last_model_sha256':last_sha,'last_model_assessment':last_assessment,'last_model_satisfies_final_formula':bool(last_assessment and last_assessment['formula_sha256']==final_sha),'peak_observed_total_decimal_GB':round(peak_total,6),'peak_measured_lane_RSS_bytes':peak_lane,'full_product_checks':full,'proof_traces':[]}
 # Retain compressed final input and every LRAT trace; verify raw roundtrips.
 for p in [root/'current.cnf',*root.rglob('*.lrat')]:
  z=p.with_name(p.name+'.zst');subprocess.run(['zstd','-q','-f','-T1','-3',str(p),'-o',str(z)],check=True)
  child=subprocess.Popen(['zstd','-q','-d','-c',str(z)],stdout=subprocess.PIPE);h=hashlib.sha256()
  for data in iter(lambda:child.stdout.read(1<<20),b''):h.update(data)
  assert child.wait()==0 and h.hexdigest()==digest(p)
  record={'path':str(p.relative_to(root)),'sha256':h.hexdigest(),'compressed_sha256':digest(z),'decompression_roundtrip':True}
  if p.suffix=='.lrat':
   log=p.parent/('lrat_solver.log' if p.name=='unsat.lrat' else 'solver.log');txt=log.read_text() if log.exists() else ''
   record['status']='UNSAT trace; independent replay required' if 's UNSATISFIABLE' in txt else 'SAT/UNKNOWN/partial trace; not an UNSAT certificate'
   summary['proof_traces'].append(record)
  else:summary['final_cnf_archive']=record
 cache=root/'dedup_cache.sqlite'
 if cache.exists():cache.unlink()
 current=root/'sources/current';current.mkdir(parents=True,exist_ok=True)
 for p in [*here.glob('m6*.py'),*here.glob('m6*.c')]:shutil.copyfile(p,current/p.name)
 shutil.copyfile(here.parent/'ES8SYM/sets/c6_54pts_9layers.pts',current/'c6_54pts_9layers.pts')
 source_records=[{'path':str(p.relative_to(root)),'sha256':digest(p)} for p in sorted((root/'sources').rglob('*')) if p.is_file() and not p.name.startswith('source_manifest.json')]
 (root/'sources/source_manifest.json').write_text(json.dumps({'files':source_records},indent=2)+'\n')
 summary['first_event_utc']=events[0]['utc']
 segments=[]
 for p in [*sorted(root.glob('*worker_status.json')),root/'status.json']:
  x=json.loads(p.read_text());assert x['all_children_reaped'];segments.append({'record':str(p.relative_to(root)),'status':x})
 (root/'process_summary.json').write_text(json.dumps({'hard_computation_stop_utc':'2026-11-03T19:00:00Z','authorized_budget_start_utc':'2026-11-03T17:09:32Z','all_recorded_segments_reaped':True,'segments':segments},indent=2)+'\n')
 (root/'final_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (here/'m6_STATUS.json').write_text(json.dumps(summary,indent=2)+'\n')
 report=here/'m6_REPORT.md';text=report.read_text();start=text.index('Status: active.');end=text.index('\n\nThis campaign',start)
 closing=f"Status: stopped; {status['stop_reason']}. All task children were reaped.\nThe hard computation deadline was 2026-11-03 19:00 UTC\n(2026-11-04 04:00 KST)."
 text=text[:start]+closing+text[end:]
 rows=['## Final retained status','',f"The campaign retained {len(sat)} SAT models and {len(blocks)} verified cut blocks.",f"The final formula has {nv:,} variables and {nc:,} clauses.",f"There were {len(outcomes)} fully GP-consistent candidate models; their exact",'separations and any pending cases are listed in `survivor_outcomes.json`.','', '| Separation method | Candidates |','| --- | ---: |']
 rows += [f'| {method} | {count} |' for method,count in methods.items()]
 rows += [f"| Pending separation | {sum(not r['separation'] for r in outcomes)} |",'',f"Final formula SHA-256: `{final_sha}`.",f"Last retained model: `{status['last_model']}`, SHA-256 `{last_sha}`."]
 if last_assessment:rows += [f"Its full-GP scan found {last_assessment['gp_violations']} violations; its verified",f"input formula SHA-256 is `{last_assessment['formula_sha256']}`."]
 else:rows += ['Its assessment did not finish before the stop.']
 if not summary['last_model_satisfies_final_formula']:rows += ['That input differs from the final strengthened formula; this model is not','reported as a satisfying assignment of the final formula.']
 rows += ['',f"Observed total-memory peak in this lane's samples was {peak_total:.3f} decimal GB.",f"The corrected worker measured peak lane RSS of {peak_lane/1e9:.3f} decimal GB.",'Initial GiB/GB guard correction is disclosed below.','',f"Recorded UNSAT events: {summary['UNSAT_events']}. All SAT, UNKNOWN or partial",'LRAT traces are noncertificates. Any complete UNSAT trace still requires the','separately coordinated checker replays before a certified bound is claimed.','The final input was reconstructed from the durable base and exact cut prefix,','and compressed final input/proof artifacts passed decompression hash checks.','']
 pos=text.index('## Evidence and scope');text=text[:pos]+'\n'.join(rows)+'\n'+text[pos:];report.write_text(text)
 # Refresh any pre-existing compressed mutable copies after their last write.
 # Missing compressed copies are left for the independently coordinated audit.
 paired=0;refreshed=0
 for z in root.rglob('*.zst'):
  if z.name.startswith('archive_manifest.json'):continue
  raw=z.with_name(z.name[:-4])
  if not raw.exists():continue
  want=digest(raw);child=subprocess.Popen(['zstd','-q','-d','-c',str(z)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL);h=hashlib.sha256()
  for data in iter(lambda:child.stdout.read(1<<20),b''):h.update(data)
  rc=child.wait()
  if rc or h.hexdigest()!=want:
   subprocess.run(['zstd','-q','-f','-T1','-3',str(raw),'-o',str(z)],check=True);refreshed+=1
   child=subprocess.Popen(['zstd','-q','-d','-c',str(z)],stdout=subprocess.PIPE);h=hashlib.sha256()
   for data in iter(lambda:child.stdout.read(1<<20),b''):h.update(data)
   assert child.wait()==0 and h.hexdigest()==want
  paired+=1
 # Exclude both the manifest and its compressed copy to avoid self-reference.
 records=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(root.rglob('*')) if p.is_file() and not p.name.startswith('archive_manifest.json')]
 (root/'archive_manifest.json').write_text(json.dumps({'files':records},indent=2)+'\n')
 if (root/'archive_manifest.json.zst').exists():subprocess.run(['zstd','-q','-f','-T1','-3',str(root/'archive_manifest.json'),'-o',str(root/'archive_manifest.json.zst')],check=True)
 print(json.dumps({'status':'finalized','SAT_models':len(sat),'full_GP_survivors':len(outcomes),'clauses':nc,'manifest_files':len(records),'existing_pairs_checked':paired,'stale_pairs_refreshed':refreshed}))
if __name__=='__main__':main()
