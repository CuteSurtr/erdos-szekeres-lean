"""mk_trivial_lrat.py BASE.cnf META.json CUBEDIR : for each transitivity-inconsistent cube, write CUBEDIR/<name>.triv.lrat,
a one-step LRAT refutation: hints = the 6 unit clauses of the cube, then a base clause they falsify."""
import sys, json, itertools, os
base, meta, d = sys.argv[1:4]
Y = json.load(open(meta))['Y']
keys = ('1,2', '1,3', '1,4', '2,3', '2,4', '3,4'); vs = {Y[k] for k in keys}
small = []
with open(base) as f:
    nc = int(next(f).split()[3])
    for i, l in enumerate(f, 1):
        lits = [int(x) for x in l.split()[:-1]]
        if lits and all(abs(x) in vs for x in lits): small.append((i, lits))
cv = [Y[k] for k in keys[1:]]
n = 0
for bits in itertools.product((1, 0), repeat=5):
    units = [Y['1,2']] + [v if b else -v for v, b in zip(cv, bits)]
    tv = {abs(u): u > 0 for u in units}
    fals = [(i, c) for i, c in small if all(tv[abs(x)] != (x > 0) for x in c)]
    if not fals: continue
    name = 'c' + ''.join(map(str, bits))
    uid = list(range(nc + 1, nc + 7))           # ids of the 6 appended unit clauses
    with open(os.path.join(d, name + '.triv.lrat'), 'w') as g:
        g.write('%d 0 %s %d 0\n' % (nc + 7, ' '.join(map(str, uid)), fals[0][0]))
    n += 1
print('wrote', n, 'trivial proofs')
