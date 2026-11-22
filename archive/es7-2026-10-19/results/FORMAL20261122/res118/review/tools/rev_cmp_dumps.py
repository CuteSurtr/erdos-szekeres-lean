#!/usr/bin/env python3
"""Compare the data the audit compile printed from the oleans (REV_* lines of logs/audit.log) with the JSON inputs.
COMPUTED binding olean -> JSON, independent of the Lean sources. Writes argv[1]."""
import gzip, json, re, sys
from pathlib import Path

V = Path('/home/jay/research/data/formalize-20261122/res118/review')
W = Path('/home/jay/research/data/es308-20261114')
log = (V / 'logs/audit.log').read_text()
def grab(tag):
    m = re.search(rf'{tag} (.*)$', log, re.M)
    return m.group(1) if m else None
def lists(s):  # [[a, b], [c]] -> list of lists
    return [[int(x) for x in re.findall(r'\d+', g)] for g in re.findall(r'\[([^\[\]]*)\]', s[1:-1])]
def flat(s):
    return [int(x) for x in re.findall(r'\d+', s)]
src = json.loads(gzip.decompress((W / 'inputs/source-2650.json.gz').read_bytes()))
F = [i for i, s in enumerate(src['states']) if s[0] >= 5]
LO = [i for i, s in enumerate(src['states']) if s[0] <= 4]
rep = {}
rep['fIndices'] = flat(grab('REV_FIDX')) == F
rep['loIndices'] = flat(grab('REV_LOIDX')) == LO
rep['F_finset'] = flat(grab('REV_FSET')) == F
rep['Lo_finset'] = flat(grab('REV_LOSET')) == LO
rep['catalog_eq_states'] = lists(grab('REV_CATALOG')) == src['states']
base = grab('REV_BASE')
pairs = re.findall(r'\(\[([0-9, ]*)\], (\d+)\)', base)
rep['base_rows'] = len(pairs)
rep['base_eq_constraints'] = [([int(x) for x in re.findall(r'\d+', a)], int(d)) for a, d in pairs] == \
    [(sorted(c['support']), c['rhs']) for c in src['constraints']]
ex = {k: json.loads((W / f'inputs/{k}/extra.json').read_text()) for k in ['s19', 's18-v13', 'b35s19-v16', 'b35s20-v169']}
P, Q, U, A = (lists(grab(t)) for t in ['REV_ROWSP', 'REV_ROWSQ', 'REV_ROWSU', 'REV_ROWSA'])
rep['sizes'] = [len(P), len(Q), len(U), len(A)]
u = lambda k: [r['support'] for r in ex[k][2:]]
rep['s19_eq_P'] = u('s19') == P
rep['s18v13_eq_PQ'] = u('s18-v13') == P + Q
rep['b35s19v16_eq_PQU'] = u('b35s19-v16') == P + Q + U
rep['b35s20v169_eq_PQA'] = u('b35s20-v169') == P + Q + A
rep['end_marker'] = 'REV_END' in log
rep['ok'] = all(v is True for k, v in rep.items() if isinstance(v, bool))
print(json.dumps(rep, indent=1))
Path(sys.argv[1]).write_text(json.dumps(rep, indent=1) + '\n')
