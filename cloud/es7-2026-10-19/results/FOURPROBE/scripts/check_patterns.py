"""check_patterns.py BASE.cnf META.json : for each of the 32 sign patterns (with Y(1,2)=1), decide consistency with a
linear order of psi_1..psi_4 (exact enumeration), and for each inconsistent one find a clause of BASE whose literals are
all over {Y(1,2),..,Y(3,4)} and all false under the pattern (so cube = BASE + units is refuted by unit propagation)."""
import sys, json, itertools
base, meta = sys.argv[1:3]
Y = json.load(open(meta))['Y']
keys = ('1,2', '1,3', '1,4', '2,3', '2,4', '3,4'); vs = {Y[k]: k for k in keys}
small = []
with open(base) as f:
    next(f)
    for l in f:
        lits = [int(x) for x in l.split()[:-1]]
        if lits and all(abs(x) in vs for x in lits): small.append(lits)
print('clauses over the six Y vars:', len(small))
def consistent(b):
    less = lambda i, j: b['%d,%d' % (i, j)] if i < j else 1 - b['%d,%d' % (j, i)]
    return [p for p in itertools.permutations((1, 2, 3, 4)) if all(less(p[a], p[c]) for a in range(4) for c in range(a+1, 4))]
nc = 0
for bits in itertools.product((1, 0), repeat=5):
    b = dict(zip(keys[1:], bits)); b['1,2'] = 1
    name = 'c' + ''.join(map(str, bits)); ords = consistent(b)
    val = {Y[k]: b[k] for k in keys}
    fals = [c for c in small if all((val[abs(x)] == 1) != (x > 0) for x in c)]
    if ords:
        nc += 1; print(name, 'consistent order', '<'.join(map(str, ords[0])), 'falsified clauses', len(fals))
    else:
        print(name, 'inconsistent; falsified base clause', fals[0] if fals else None)
        if not fals: sys.exit('FAIL: inconsistent pattern with no falsified clause')
print('consistent:', nc, 'inconsistent:', 32 - nc)
