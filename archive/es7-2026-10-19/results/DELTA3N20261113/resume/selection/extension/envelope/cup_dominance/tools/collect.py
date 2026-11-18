"""Freeze cup-protection packets without touching earlier manifests."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil


def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scratch',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=False);w=args.scratch
    s=json.loads((w/'pool-v1/summary.json').read_text());assert s['stop']=='COMPLETE' and len(s['cases'])==316
    baseline=[r for r in s['cases'] if r['name']!='known18'];assert len(baseline)==315
    groups=[]
    for n in (7,8):
        rows=[r for r in baseline if r['n']==n]
        groups.append({'n':n,'cases':len(rows),'selected_cap_triples_checked':sum(r['replay']['cap_triples_checked'] for r in rows),'max_literals':max(r['literals'] for r in rows),'max_clauses':max(r['clauses'] for r in rows)})
    summary={k:v for k,v in s.items() if k!='cases'};summary.update(baseline_groups=groups,baseline_cases=315,known18_repeated_in_batch=True)
    (args.out/'pool_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (args.out/'coverage.json').write_text(json.dumps([{k:r[k] for k in ('name','m','n','A','bad_triples','protected_pairs','cup_protected_nonterminal_pairs','clauses','literals','replay','outcome')} for r in s['cases']],indent=2)+'\n')
    copies=[('known-v1/summary.json','controls_and_known_summary.json'),('known-v1/proper_cup_control.json','proper_cup_control.json'),('pool-v1/plan.json','run_plan.json'),('real15-v1/summary.json','real15_summary.json'),('structure-v1/known18_exact_counts.json','known18_minimum.json'),('structure-v1/real15_exact_counts.json','real15_minimum.json'),('structure-v1/old_known_A.json','old_known_A.json'),('structure-v1/four_point_classes.json','four_point_classes.json')]
    for a,b in copies:shutil.copy2(w/a,args.out/b)
    manifest={}
    for run in ('known-v1','pool-v1','real15-v1','structure-v1'):
        for p in sorted((w/run).rglob('*')):
            if p.is_file():manifest[str(p)]={'sha256':digest(p),'bytes':p.stat().st_size}
    (args.out/'external_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'groups':groups,'external_files':len(manifest),'retained_bytes':sum(v['bytes'] for v in manifest.values())}))
if __name__=='__main__':main()
