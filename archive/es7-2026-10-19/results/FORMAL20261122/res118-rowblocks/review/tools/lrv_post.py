#!/usr/bin/env python3
"""Post-processing (COMPUTED): my binding table data/lrv_bind.tsv against the worker's logs/m9_binding.tsv (same
(block, index) -> same support and same printed sha256), and the support multiset per block. Prints JSON."""
import csv, json
V = '/home/jay/research/data/formalize-20261122/res118-rowblocks/review'
W = '/home/jay/research/data/formalize-20261122/res118-rowblocks/logs/m9_binding.tsv'
mine = {(r['block'], r['index']): r for r in csv.DictReader(open(V + '/data/lrv_bind.tsv'), delimiter='\t')}
theirs = {(r['block'], r['index']): r for r in csv.DictReader(open(W), delimiter='\t')}
rep = {'mine': len(mine), 'theirs': len(theirs), 'same_keys': set(mine) == set(theirs)}
rep['support_mismatch'] = [k for k in mine if k in theirs and mine[k]['support'] != theirs[k]['support']]
rep['hash_mismatch'] = [k for k in mine if k in theirs and mine[k]['printed_sha256'] != theirs[k]['printed_sha256']]
sup = {}
for (b, i), r in mine.items():
    sup.setdefault(r['support'], []).append(b + i)
rep['duplicate_supports'] = {s: v for s, v in sup.items() if len(v) > 1}
rep['tables_used'] = {}
for r in mine.values():
    rep['tables_used'][r['tables']] = rep['tables_used'].get(r['tables'], 0) + 1
print(json.dumps(rep, indent=1))
