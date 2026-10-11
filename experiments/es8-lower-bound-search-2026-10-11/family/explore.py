import sys
sys.path.insert(0, '.')
from dp import build, combine
from collections import defaultdict
count, by_n = build()
top = (64, 7, 7, 7)
# decompositions
dec = defaultdict(list)
for s in count:
    pass
states = list(count)
idx = defaultdict(list)
for s in states: idx[s[0]].append(s)
def decomps(s):
    out = []
    n = s[0]
    for na in range(1, n):
        for sa in idx[na]:
            for sb in idx[n-na]:
                for d in 'UD':
                    if combine(sa, sb, d) == s:
                        out.append((d, sa, sb, count[sa]*count[sb]))
    return out
# backward reachable
used = {top}
stack = [top]
D = {}
while stack:
    s = stack.pop()
    if s[0] == 1: continue
    D[s] = decomps(s)
    for d, sa, sb, w in D[s]:
        for t in (sa, sb):
            if t not in used:
                used.add(t); stack.append(t)
print('used states:', len(used))
for s in sorted(used, key=lambda s: (-s[0], s)):
    if s[0] >= 16:
        print(s, 'count~2^%d' % (count[s].bit_length()-1), 'decomps:', [(d, sa, sb) for d, sa, sb, w in D.get(s, [])])
