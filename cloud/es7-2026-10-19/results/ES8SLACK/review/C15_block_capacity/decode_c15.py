"""Decode a CaDiCaL model of an enc_c15.py CNF into a witness JSON (same format as probes/p11_witness_*.json),
after checking every clause of the CNF against the model.
Usage: decode_c15.py file.cnf file.out witness_out.json"""
import sys, json, itertools
cnf, outf, wout = sys.argv[1:4]
val = {}
status = None
for line in open(outf):
    if line.startswith('s '):
        status = line.split()[1]
    if line.startswith('v '):
        for t in line.split()[1:]:
            v = int(t)
            if v:
                val[abs(v)] = v > 0
assert status == 'SATISFIABLE', status
bad = total = 0
for line in open(cnf):
    if line[0] in 'pc':
        continue
    lits = list(map(int, line.split()))[:-1]
    total += 1
    if not any(val.get(abs(l), False) == (l > 0) for l in lits):
        bad += 1
mp = json.load(open(cnf + '.map.json'))
n, S, cells = mp['n'], [tuple(s) for s in mp['S']], [tuple(c) for c in mp['cells']]
states, labels, pos = [], {}, []
for p in range(n):
    ss = [s for s in range(len(S)) if val[mp['x'][f'{p},{s}']]]
    assert len(ss) == 1
    states.append(list(S[ss[0]]))
for p, q in itertools.combinations(range(n), 2):
    cs = [c for c in range(len(cells)) if val[mp['L'][f'{p},{q},{c}']]]
    assert len(cs) == 1
    labels[f'{p},{q}'] = list(cells[cs[0]])
for t in itertools.combinations(range(n), 3):
    if val[mp['o'][f'{t[0]},{t[1]},{t[2]}']]:
        pos.append(list(t))
json.dump({'row': mp['K'], 'n': n, 'states': states, 'labels': labels, 'orientation_positive': pos}, open(wout, 'w'))
print(json.dumps({'clauses': total, 'violated': bad, 'witness': wout}))
