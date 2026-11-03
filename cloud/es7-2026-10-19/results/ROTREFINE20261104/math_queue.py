#!/usr/bin/env python3
"""Publish a completed exact-verified family into the local immutable queue.

Approval scope is the standing authorization for exact identity and exact54
checks; independent symbolic review is batched before any final theorem claim.
Only the specified incoming folder is created. approved.json appears last.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--family',type=Path,required=True);ap.add_argument('--incoming',type=Path,required=True);ap.add_argument('--index',type=int,required=True);a=ap.parse_args()
    assert a.index>=1000
    parent=a.family.parent;w=parent/'linear_witness.json';v=parent/'verified.json';f=a.family/'family_verified.json';c=a.family/'family.clauses'
    ww=json.loads(w.read_text());vv=json.loads(v.read_text());ff=json.loads(f.read_text())
    assert vv['status']==ff['status']=='PASS' and vv['exact54_forbidden_matches']==0
    assert vv['direct_symbolic_identity'] and vv['reverse_direction_identity'] and vv['positive_integer_weights']
    assert sha(w)==vv['witness_sha256']==ff['source_witness_sha256']
    assert sha(v)==ff['source_verified_sha256'] and sha(c)==ff['family_sha256']
    assert ww['model_sha256']==vv['model_sha256']==ff['source_model_sha256']
    independent=parent/'independent_verified.json'
    if len(ww['source_layers'])>4:
        assert independent.exists() and sha(independent)==ff['independent_verification_sha256'] and ff['exact54_tests']>=2*ff['unique_clauses']
    dest=a.incoming/f'linear{a.index:04d}';dest.mkdir(exist_ok=False)
    for src in (w,v,f,c):shutil.copyfile(src,dest/src.name)
    if independent.exists():shutil.copyfile(independent,dest/independent.name)
    assert sha(dest/'family.clauses')==ff['family_sha256']
    kind='sixfold linear determinant identity '+('ordered-injection ' if ff.get('orbit_injections')=='order-preserving only' else '')+'family'
    approval={'approved':True,'kind':kind,'clauses':'family.clauses','sha256':ff['family_sha256'],
              'approval_scope':'standing approval for exact-verified and exact54-tested templates; independent symbolic review batched',
              'evidence':['linear_witness.json','verified.json','family_verified.json']}
    if independent.exists():approval['evidence'].append(independent.name)
    temp=dest/'approved.pending';temp.write_text(json.dumps(approval,indent=2)+'\n');temp.replace(dest/'approved.json')
    result={'queue_folder':dest.name,'family_sha256':ff['family_sha256'],'witness_sha256':sha(w),'source_model_sha256':ww['model_sha256'],
            'clauses':ff['unique_clauses'],'exact54_tests':vv['exact54_tests']}
    (parent/'queue_receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':main()
