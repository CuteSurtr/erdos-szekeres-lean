import json,sys
from pathlib import Path
sys.path.insert(0,'experiments/omission-residual32-rank-search-2026-10-10');import cnf_export as c
R=Path('.cache/rank313');e=json.loads((R/'core-four-input.json').read_text());c.occupied=set(range(154))-set(e['strict_row_witness_holes']);encoded=c.CNF(e['support']);present={tuple(d) for k,d in zip(encoded.kinds,encoded.details) if k=='no_octagon'}
for eight in e['rank_model']['cuts_list']:
 if tuple(eight) not in present:encoded.add([c.neg(encoded.convex(q)) for q in c.itertools.combinations(eight,4)],'no_octagon',eight)
encoded.export(R/'core-four-raw');print(len(encoded.S),len(encoded.variables),len(encoded.clauses))
