#!/usr/bin/env python3
"""Batch independent symbolic checks of retained sixfold linear witnesses."""
import argparse, hashlib, importlib.util, json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--archive',required=True,type=Path);p.add_argument('--old-archive',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args()
checker=Path(__file__).with_name('check_linear_symbolic.py')
s=importlib.util.spec_from_file_location('direct_polynomials',checker);v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
models=list((a.archive/'m6/models').glob('*.json'))+[a.old_archive/'m6/gp_run08/model.json',a.old_archive/'m6/family_run3/model.json']
lookup={hashlib.sha256(f.read_bytes()).hexdigest():f for f in models if f.exists()}
old=json.loads(a.out.read_text()) if a.out.exists() else {'verified':[]}
done={r['witness_sha256'] for r in old['verified']};pending=[]
for f in sorted((a.archive/'math').rglob('linear_witness.json')):
    try: w=json.loads(f.read_text())
    except json.JSONDecodeError: continue
    if w.get('m')!=6: continue
    digest=hashlib.sha256(f.read_bytes()).hexdigest()
    if digest in done: continue
    if w['model_sha256'] not in lookup:
        pending.append(f.relative_to(a.archive).as_posix());continue
    result=v.check(f,lookup[w['model_sha256']]);result['witness']=f.relative_to(a.archive).as_posix()
    old['verified'].append(result);done.add(digest)
old['pending_model_lookup']=pending;old['checker_sha256']=hashlib.sha256(checker.read_bytes()).hexdigest()
a.out.write_text(json.dumps(old,indent=2)+'\n')
print(json.dumps({'independently_verified_witnesses':len(old['verified']),'pending':pending}))
