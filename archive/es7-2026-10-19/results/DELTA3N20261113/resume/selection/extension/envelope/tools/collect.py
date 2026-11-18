"""Freeze the completed full-pool batch index and verify every retained hash."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil


def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    full=json.loads((args.run/'summary.json').read_text());rows=full['cases'];assert full['stop']=='COMPLETE' and len(rows)==945
    manifest={};coverage=[];groups=[];byte_count=0
    for r in rows:
        case=args.run/'cases'/r['name']
        for name,expected in r['files'].items():
            file=case/name;assert file.stat().st_size==expected['bytes'] and sha(file)==expected['sha256']
            manifest[str(file)]={**expected};byte_count+=expected['bytes']
        f=case/'result.json';manifest[str(f)]={'sha256':sha(f),'bytes':f.stat().st_size};byte_count+=f.stat().st_size
        assert r['outcome']=='SAT_EXACT_MODEL_CHECKED'
        coverage.append({k:r[k] for k in ('name','n','m','A','targets','fourcaps','exposed_triples','exposed_pairs','ambient_pairs','terminal_rank3_triples','literals','clauses','seconds','replay')})
        coverage[-1]['exposure_family_changed']=r.get('exposure_family_changed',False)
        coverage[-1]['case_directory']=str(case)
    for n in (7,8):
        for variation in (False,True):
            selected=[r for r in rows if r['n']==n and ('-v' in r['name'])==variation]
            groups.append({'n':n,'kind':'variations' if variation else 'baseline','cases':len(selected),'size_range':[min(r['m'] for r in selected),max(r['m'] for r in selected)],'selected_cap_triples_checked':sum(r['replay']['cap_triples_checked'] for r in selected),'two_line_certificates':sum(r['replay']['two_line_certificates'] for r in selected),'exposure_family_changed':sum(r.get('exposure_family_changed',False) for r in selected),'max_literals':max(r['literals'] for r in selected),'exposed_triple_range':[min(r['exposed_triples'] for r in selected),max(r['exposed_triples'] for r in selected)]})
    for folder in ('source','inputs'):
        for f in (args.run/folder).iterdir():
            if f.is_file():manifest[str(f)]={'sha256':sha(f),'bytes':f.stat().st_size}
    for name in ('summary.json','plan.json','status.json','inputs.json','results.jsonl'):
        f=args.run/name;manifest[str(f)]={'sha256':sha(f),'bytes':f.stat().st_size}
    summary={k:v for k,v in full.items() if k!='cases'}
    summary.update(groups=groups,case_packet_bytes=byte_count,case_packets=945,verified_external_files=len(manifest),changed_exposure_cases=[r['name'] for r in rows if r.get('exposure_family_changed')],two_line_cases=[r['name'] for r in rows if r['replay']['two_line_certificates']],limitations=['No uniform failure or universal existence theorem.','Two variations per baseline: not independent order types.','Seven variations change the actual exposure family.','Full-v1 had a file-cache resource-estimate deviation; see resource_receipt.json.','Initial 1M-literal preflight UNKNOWN is preserved separately.','Parent independent replay is separate from the within-track checker.'])
    for name,obj in [('summary.json',summary),('coverage.json',coverage),('external_manifest.json',manifest)]:
        with (args.out/name).open('x') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n')
    shutil.copy2(args.run/'plan.json',args.out/'run_plan.json');shutil.copy2(args.run/'inputs.json',args.out/'inputs.json')
    print(json.dumps({'cases':len(rows),'external_files':len(manifest),'case_packet_bytes':byte_count,'groups':groups},sort_keys=True))
if __name__=='__main__':main()
