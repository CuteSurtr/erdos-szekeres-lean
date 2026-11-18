"""Weaker split variants on an abstract FL(5,5) configuration (brute force over all partitions)."""
import sys, json, itertools
d = json.load(open(sys.argv[1])); a, b, n, sig = d['a'], d['b'], d['n'], d['sig']
T = list(itertools.combinations(range(n), 3)); sg = {t: (1 if c == '+' else -1) for t, c in zip(T, sig)}
def chains(L, s): return [idx for idx in itertools.combinations(range(n), L) if all(sg[idx[q], idx[q+1], idx[q+2]] == s for q in range(L - 2))]
capsA1 = chains(a - 1, -1); cupsB1 = chains(b - 1, 1); capsA2 = chains(a - 2, -1); cupsB2 = chains(b - 2, 1)
m = lambda s: sum(1 << p for p in s)
def gons(caps, cups):
    by = {}
    for c in cups: by.setdefault((c[0], c[-1]), []).append(c)
    return [m(set(c) | set(u)) for c in caps for u in by.get((c[0], c[-1]), [])]
cap1 = [m(c) for c in capsA1]; cup1 = [m(c) for c in cupsB1]
g1 = gons(capsA2, cupsB1); g2 = gons(capsA1, cupsB2)
full = (1 << n) - 1
inside = lambda S, L: any(x & S == x for x in L)
cnt = {'strong': 0, 'S1 in FL(a-1,b), S2 no (b-1)-cup': 0, 'S1 no (a-1)-cap, S2 in FL(a,b-1)': 0, 'S1 no (a-1)-cap, S2 no (b-1)-cup': 0}
best1 = best2 = 0
for S1 in range(1 << n):
    S2 = full ^ S1
    c1 = not inside(S1, cap1); u2 = not inside(S2, cup1)
    f1 = c1 and not inside(S1, g1); f2 = u2 and not inside(S2, g2)
    if f1: best1 = max(best1, bin(S1).count('1'))
    if f2: best2 = max(best2, bin(S2).count('1'))
    cnt['strong'] += f1 and f2; cnt['S1 in FL(a-1,b), S2 no (b-1)-cup'] += f1 and u2
    cnt['S1 no (a-1)-cap, S2 in FL(a,b-1)'] += c1 and f2; cnt['S1 no (a-1)-cap, S2 no (b-1)-cup'] += c1 and u2
print('number of partitions of each kind:', cnt)
print('largest subset in FL(a-1,b):', best1, ' largest subset in FL(a,b-1):', best2)
