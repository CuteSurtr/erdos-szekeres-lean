"""Plant extra symmetry: close the base supports under the swap (a b) for a=100, b=101
(they lie in different <T,C>-orbits), so (a b) becomes an automorphism. The search must
then report a group strictly larger than 4 containing (a b)."""
import json, sys
d = json.load(open(sys.argv[1]))
a, b = 100, 101
sw = lambda i: b if i == a else a if i == b else i
rows = {(tuple(sorted(c['support'])), c['rhs']) for c in d['constraints'][:2685]}
rows |= {(tuple(sorted(sw(i) for i in s)), r) for s, r in rows}
out = {'states': d['states'], 'constraints': [{'support': list(s), 'rhs': r} for s, r in sorted(rows)]}
# autgroup.py 'base' mode reads the first 2685 constraints; write a version with all rows first
out['constraints'] = out['constraints']
json.dump(out, open(sys.argv[2], 'w'))
print('rows after closure:', len(rows))
