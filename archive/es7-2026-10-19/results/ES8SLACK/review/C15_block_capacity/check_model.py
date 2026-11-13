"""Check a CaDiCaL model of a probes/p11_blockcap.py CNF against that CNF (own parser) and decode the
first three variable blocks of p11_blockcap.py's numbering (sig, st, lab) independently; compare with
the witness JSON written by probes/p11_verify.py.
Usage: check_model.py file.cnf file.out witness.json K n"""
import sys, json, gzip, itertools
cnf, outf, wjs, K, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
SRC = (ROOT + '/experiments/'
       'omission-residual32-rank-global-2026-10-10/source-2650.json.gz')
val = {}
st = None
for line in open(outf):
    if line.startswith('s '):
        st = line.split()[1]
    elif line.startswith('v '):
        for t in line.split()[1:]:
            v = int(t)
            if v:
                val[abs(v)] = v > 0
hdr = None; total = bad = 0; maxvar = 0
for line in open(cnf):
    if line.startswith('p '):
        hdr = line.split(); continue
    if line[0] == 'c':
        continue
    lits = list(map(int, line.split()))
    assert lits[-1] == 0
    lits = lits[:-1]
    total += 1
    maxvar = max([maxvar] + [abs(l) for l in lits])
    if not any(val.get(abs(l)) == (l > 0) for l in lits):
        bad += 1
complete = all(v in val for v in range(1, int(hdr[2]) + 1))
src = json.load(gzip.open(SRC))
S = [tuple(src['states'][i][:4]) for i in src['constraints'][K]['support']]
cells = [(a, b) for a in range(1, 5) for b in range(1, 7) if (a, b) != (1, 6)]
v = 0
pos = []
for t in itertools.combinations(range(n), 3):
    v += 1
    if val[v]:
        pos.append(list(t))
states = []
for p in range(n):
    hit = []
    for s in range(len(S)):
        v += 1
        if val[v]:
            hit.append(S[s])
    assert len(hit) == 1
    states.append(list(hit[0]))
labels = {}
for p, q in itertools.combinations(range(n), 2):
    hit = []
    for c in range(len(cells)):
        v += 1
        if val[v]:
            hit.append(cells[c])
    assert len(hit) == 1
    labels[f'{p},{q}'] = list(hit[0])
w = json.load(open(wjs))
same = (w['states'] == states and w['labels'] == labels and
        sorted(map(tuple, w['orientation_positive'])) == sorted(map(tuple, pos)))
print(json.dumps({'cnf': cnf.split('/')[-1], 'status': st, 'header': hdr[2:], 'clauses_read': total,
                  'max_var_used': maxvar, 'model_complete': complete, 'violated': bad,
                  'witness_json_matches_model': same}))
