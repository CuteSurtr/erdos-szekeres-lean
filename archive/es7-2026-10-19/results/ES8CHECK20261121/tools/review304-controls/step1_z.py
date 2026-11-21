import json, re, sys
from itertools import product

ESB = '<repo>'
SRC = ESB + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
ZS = ESB + '/archive/es7-2026-10-19/results/ES303N20261120/data/zstar.json'
LZ = ESB + '/archive/es7-2026-10-19/results/ES305N20261119/LemmaZ.lean'
LZS = ESB + '/archive/es7-2026-10-19/results/ES303N20261120/LemmaZStar.lean'
CAT = ESB + '/ErdosSzekeres/Omission/BalancedCatalogData.lean'

d = json.load(open(SRC))
states = [tuple(s) for s in d['states']]
print('states', len(states), 'distinct', len(set(states)))
# all antitone f:{0..4}->{0..5}
allf = [f for f in product(range(6), repeat=5) if all(f[i] >= f[i + 1] for i in range(4))]
print('antitone maps {0..4}->{0..5}:', len(allf), 'equal as sets to JSON states:', set(allf) == set(states))

# Lean catalog order
txt = open(CAT).read()
m = re.search(r'def catalog : List \(List Nat\) := (\[\[.*?\]\])', txt, re.S)
cat = [tuple(x) for x in json.loads(m.group(1))]
print('Lean catalog len', len(cat), 'same order as JSON states:', cat == states)

Z = [i for i, f in enumerate(states) if f[0] <= 4 and f[4] == 0]
Zs = [i for i, f in enumerate(states) if f[0] == 5 and f[4] >= 1]
print('|Z| =', len(Z), ' |Z*| =', len(Zs), ' disjoint:', not (set(Z) & set(Zs)))

zj = json.load(open(ZS))
print('zstar.json: len', len(zj['zstar']), 'rhs', zj['rhs'], 'equal to own Z*:', sorted(zj['zstar']) == Zs,
      'sorted/no dup:', zj['zstar'] == sorted(set(zj['zstar'])))


def lean_list(path, name):
    t = open(path).read()
    mm = re.search(r'def ' + name + r' : List ℕ := (\[[0-9,\s]*\])', t)
    return json.loads(mm.group(1))


lz = lean_list(LZ, 'zIndices')
lzs = lean_list(LZS, 'zsIndices')
print('LemmaZ.zIndices: len', len(lz), 'equal to own Z:', lz == Z)
print('LemmaZStar.zsIndices: len', len(lzs), 'equal to own Z*:', lzs == Zs)
# Lean-side profile predicates (re-read from the files, compared textually)
print('zProfile text:', re.search(r'def zProfile.*', open(LZ).read()).group(0))
print('zsProfile text:', re.search(r'def zsProfile.*', open(LZS).read()).group(0))
# other derived facts
print('0 in Z:', 0 in Z, ' state(1,0,0,0,0) index', states.index((1, 0, 0, 0, 0)), 'in Z:', states.index((1, 0, 0, 0, 0)) in Z)
print('Z counts by f0:', {k: sum(1 for i in Z if states[i][0] == k) for k in range(6)})
print('Z* counts by f4:', {k: sum(1 for i in Zs if states[i][4] == k) for k in range(6)})
# complement symmetry: f -> conjugate/complement map?  f -> (5 - f(4-i)) maps Z to Z*?
comp = {i: states.index(tuple(5 - states[i][4 - j] for j in range(5))) for i in range(252)}
print('complement map f(i) -> 5 - f(4-i) sends Z onto Z*:', sorted(comp[i] for i in Z) == Zs)
# rows: Z or Z* already among the 3,131 rows?
rows = d['constraints']
print('rows', len(rows), 'max support', max(len(r['support']) for r in rows), 'rhs values', sorted(set(r['rhs'] for r in rows)))
print('a JSON row with support Z:', any(sorted(r['support']) == Z for r in rows),
      ' with support Z*:', any(sorted(r['support']) == Zs for r in rows))
json.dump({'Z': Z, 'Zs': Zs}, open(sys.argv[1], 'w'))
