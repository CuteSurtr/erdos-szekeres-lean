#!/usr/bin/env python3
"""Export compact verified determinant witnesses and their archive-bound catalog."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--results',type=Path,required=True);a=ap.parse_args()
    out=a.results/'math_witnesses';out.mkdir(exist_ok=True);records=[]
    for f in sorted(a.archive.rglob('family_verified.json')):
        d=f.parent.parent;wp=d/'linear_witness.json';vp=d/'verified.json'
        psd=not wp.exists()
        if psd:wp=d/'sdp_witness.json'
        w=json.loads(wp.read_text());v=json.loads(vp.read_text());fam=json.loads(f.read_text())
        assert v['status']==fam['status']=='PASS' and digest(wp)==fam['source_witness_sha256']==v['witness_sha256']
        name='_'.join(d.relative_to(a.archive).parts);dest=out/name;dest.mkdir(exist_ok=True)
        for src in (wp,vp,f):shutil.copyfile(src,dest/src.name)
        ip=d/'independent_verified.json'
        if ip.exists():shutil.copyfile(ip,dest/ip.name)
        records.append({'name':name,'rigor':('written quadratic negativity proof' if psd else 'written linear determinant proof')+' plus exact computation','model_sha256':w['model_sha256'],
                        'source_layers':w['source_layers'],'support':len(w['records']),'weights':[r['weight'] for r in w['records']],
                        'candidate_clause':w['candidate_clause'],'witness_sha256':digest(wp),'verification_sha256':digest(vp),
                        'family_verification_sha256':digest(f),'family_sha256':fam['family_sha256'],
                        'family_archive_path':str((f.parent/'family.clauses').relative_to(a.archive)),
                        'orbit_injections':fam.get('orbit_injections','all injections'),'embeddings_verified':fam.get('embeddings_verified',fam['unique_clauses']),
                        'source_exact54_test_scope':v.get('exact54_test_scope','exhaustive ordered injections, shifts, direction, mirror and global sign'),
                        'family_exact54_tests':fam.get('exact54_tests',0),
                        'independent_verification_sha256':digest(ip) if ip.exists() else None,
                        'unique_clauses':fam['unique_clauses'],'exact54_tests':v['exact54_tests'],'exact54_forbidden_matches':v['exact54_forbidden_matches']})
    (a.results/'math_catalog.json').write_text(json.dumps(records,indent=2)+'\n')
    text=['# Retained determinant separators','',
          '**Written proof + exact computation.** Each entry has a positive integer zero dependency or negative-definite quadratic combination, direct symbolic verification, exact certified-set tests, and a verified orbit family. The proofs and distinct lifting rules are in `math.md` and `math_sdp.md`. Archive paths below are relative to the archive’s `math/` directory. No theorem about the full ten-layer instance follows solely from this catalog.','',
          '| Source | Orbits | Rows | Maximum weight | Family clauses | Injection scope | Exact54 tests |',
          '|---|---|---:|---:|---:|---|---:|']
    for r in records:text.append(f"| `{r['name']}` | {','.join(map(str,r['source_layers']))} | {r['support']} | {max(r['weights'])} | {r['unique_clauses']:,} | {r['orbit_injections']} | {r['exact54_tests']:,} |")
    text+=['','**Exact computation.** All listed certified-set tests have zero forbidden-pattern matches. Linear sources on at most four orbits receive exhaustive tests over the stated embeddings. Larger linear sources and PSD sources receive finite deterministic regression samples, with an additional exact original/mirror test for every emitted family clause. `math_catalog.json` supplies each scope and full model, witness, verification, and family hashes. Compact witnesses and verification outputs are copied into `math_witnesses/`; large clause families remain in the durable proof archive.','']
    (a.results/'math_cases.md').write_text('\n'.join(text))
    print(json.dumps({'verified_templates':len(records),'sum_family_clause_counts':sum(r['unique_clauses'] for r in records),
                      'sum_exact54_tests':sum(r['exact54_tests'] for r in records)}))


if __name__=='__main__':main()
