"""Minimal unrealizable state sets (circuits) from the list of maximal realizable sets."""
import sys, json, itertools
d = json.load(open(sys.argv[1])); S = d['states']; NS = len(S)
MX = [sum(1 << i for i in M) for M, m, sig in d['maximal']]
def realizable(mask): return any(mask & ~M == 0 for M in MX)
nm = lambda i: ''.join(map(str, S[i]))
circ = []
maxk = int(sys.argv[2]) if len(sys.argv) > 2 else NS
for k in range(1, maxk + 1):
    cnt = 0
    for T in itertools.combinations(range(NS), k):
        mask = sum(1 << i for i in T)
        if any(c & ~mask == 0 for c in circ): continue
        if not realizable(mask): circ.append(mask); cnt += 1
    print('size', k, 'circuits', cnt)
    if cnt and k <= 4:
        for c in circ[-cnt:][:60]: print('   ', [nm(i) for i in range(NS) if c >> i & 1])
print('total circuits', len(circ), 'max realizable size', max(bin(M).count('1') for M in MX), 'sizes of maximal sets', sorted({bin(M).count('1') for M in MX}))
json.dump({'states': S, 'circuits': [[i for i in range(NS) if c >> i & 1] for c in circ]}, open(sys.argv[1].replace('maximal', 'circuits'), 'w'))
