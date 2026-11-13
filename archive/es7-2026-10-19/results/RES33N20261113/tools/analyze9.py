import sys, itertools, json
sys.path.insert(0, '.')
from common import STATES, ROWS
from coupled import TT, DIFF
S = [42, 56, 62, 68, 72, 83, 94, 106, 108]
for s in S: print(s, STATES[s][:4])
# forced orientation counts: for each unordered triple, is some cyclic order forced positive?
forced = 0
for a, b, c in itertools.combinations(S, 3):
    f = [p for p in itertools.permutations((a, b, c)) if TT[p]]
    forced += bool(f)
print('triples with forced sign:', forced, 'of', len(list(itertools.combinations(S, 3))))
# empty directions (forced chronological order)
for u, v in itertools.permutations(S, 2):
    if not DIFF[u][v]: print('cannot precede:', u, '->', v)
# rows of catalog with support inside S or overlapping heavily
for k, (sup, d) in enumerate(ROWS):
    inter = len(set(sup) & set(S))
    if inter >= 7: print('row', k, 'size', len(sup), 'demand', d, 'overlap', inter, sorted(set(sup) - set(S)))
