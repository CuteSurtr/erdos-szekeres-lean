"""Independent exact re-check of claim C8 (basic finite facts).

Re-implements transposition T and complementation C on the 252 balanced states
directly from the down-set definition (as sets of cells in [1..5]^2), NOT from the
profile formulas of probes/sym.py, and checks:
  * T, C are permutations of the state list;
  * T^2 = C^2 = id, TC = CT, and id, T, C, TC pairwise distinct (so <T,C> = Z2 x Z2, order 4);
  * each of T, C, TC maps the set of 2,685 base rows onto itself (support AND rhs);
  * orbit structure of <T,C> (computed by closure, not by assuming the group is {id,T,C,TC});
  * fixed points;
  * behaviour on the 3,131-row V2 catalog and on the early-vertex constraints
    h0 = 0, h1 = 0, h2 + h3 <= 1.
Standard library only, exact integer/set arithmetic.
"""
import json, hashlib, sys, itertools

SRC = sys.argv[1]
raw = open(SRC, 'rb').read()
print('sha256', hashlib.sha256(raw).hexdigest())
d = json.loads(raw)
states = [tuple(s) for s in d['states']]
cons = d['constraints']
N = len(states)
assert N == 252

K = 5
# down-set as a set of cells (col, row), 1-based; profile f = column heights
def cells(f):
    return frozenset((c + 1, r) for c in range(K) for r in range(1, f[c] + 1))

def is_downset(S):
    return all(((a - 1, b) in S or a == 1) and ((a, b - 1) in S or b == 1) for (a, b) in S)

def profile(S):
    # column heights, must be nonincreasing for a down-set in the product order
    return tuple(max([r for (c, r) in S if c == col] + [0]) for col in range(1, K + 1))

cellsets = [cells(f) for f in states]
assert all(is_downset(S) for S in cellsets)
assert all(profile(S) == f for S, f in zip(cellsets, states))
# all 252 down-sets of [5]^2 present exactly once?
all_profiles = [p for p in itertools.product(range(K + 1), repeat=K) if all(p[i] >= p[i + 1] for i in range(K - 1))]
assert sorted(all_profiles) == sorted(states) and len(all_profiles) == 252
idx = {S: i for i, S in enumerate(cellsets)}

def T_cells(S):  # transpose
    return frozenset((r, c) for (c, r) in S)

def C_cells(S):  # complement inside the box, rotated by 180 degrees
    box = {(a, b) for a in range(1, K + 1) for b in range(1, K + 1)}
    comp = box - S
    return frozenset((K + 1 - a, K + 1 - b) for (a, b) in comp)

T = [idx[T_cells(S)] for S in cellsets]
C = [idx[C_cells(S)] for S in cellsets]
assert sorted(T) == list(range(N)) and sorted(C) == list(range(N))

def compose(p, q):  # (p o q)(i) = p[q[i]]
    return [p[q[i]] for i in range(N)]

ID = list(range(N))
TC = compose(T, C)
CT = compose(C, T)
print('T^2 = id:', compose(T, T) == ID, '| C^2 = id:', compose(C, C) == ID, '| TC = CT:', TC == CT)
print('distinct id,T,C,TC:', len({tuple(ID), tuple(T), tuple(C), tuple(TC)}) == 4)

# compare with the permutations of probes/sym_perms.json
ref = json.load(open(sys.argv[2]))
print('T equals probes T:', ref['T'] == T, '| C equals probes C:', ref['C'] == C)

# group closure (generic, does not assume commutativity)
G = {tuple(ID)}
frontier = [tuple(ID)]
while frontier:
    new = []
    for g in frontier:
        for s in (T, C):
            h = tuple(s[g[i]] for i in range(N))
            if h not in G:
                G.add(h); new.append(h)
    frontier = new
print('|<T,C>| by closure:', len(G))

# orbits by closure under generators
orb_id = [-1] * N; orbits = []
for i in range(N):
    if orb_id[i] >= 0: continue
    o = {i}; st = [i]
    while st:
        x = st.pop()
        for s in (T, C):
            y = s[x]
            if y not in o:
                o.add(y); st.append(y)
    for x in o: orb_id[x] = len(orbits)
    orbits.append(sorted(o))
from collections import Counter
print('orbits:', len(orbits), 'sizes:', dict(Counter(len(o) for o in orbits)))
print('fixed points: T', sum(T[i] == i for i in range(N)), 'C', sum(C[i] == i for i in range(N)), 'TC', sum(TC[i] == i for i in range(N)))
# self-conjugate partitions in 5x5 box should be 2^5 = 32
print('Burnside count (|Fix(id)|+|Fix(T)|+|Fix(C)|+|Fix(TC)|)/4 =',
      (N + sum(T[i] == i for i in range(N)) + sum(C[i] == i for i in range(N)) + sum(TC[i] == i for i in range(N))) / 4)

base = [(frozenset(c['support']), c['rhs']) for c in cons[:2685]]
assert all('kind' not in c for c in cons[:2685]) and all(c.get('kind') == 'exact_arithmetic_cover_cut' for c in cons[2685:])
allrows = [(frozenset(c['support']), c['rhs']) for c in cons]
Bset = set(base); Aset = set(allrows)
print('base rows distinct:', len(Bset), '| all rows distinct:', len(Aset))
for name, p in (('T', T), ('C', C), ('TC', TC)):
    img = {(frozenset(p[i] for i in S), r) for S, r in base}
    imgA = [(frozenset(p[i] for i in S), r) for S, r in allrows]
    print(name, ': base image == base set:', img == Bset,
          '| all3131 rows whose image is in all3131:', sum(1 for x in imgA if x in Aset),
          '| cut rows whose image is a cut/base row:', sum(1 for x in imgA[2685:] if x in Aset),
          '| new distinct images of cuts:', len({x for x in imgA[2685:] if x not in Aset}))
# union of new images over all three nontrivial elements
newimgs = set()
for p in (T, C, TC):
    for S, r in allrows[2685:]:
        x = (frozenset(p[i] for i in S), r)
        if x not in Aset: newimgs.add(x)
print('distinct new rows from images of the 446 cuts under T,C,TC:', len(newimgs))

# early-vertex constraints
print('T fixes 0:', T[0] == 0, 'fixes 1:', T[1] == 1, 'swaps 2,3:', T[2] == 3 and T[3] == 2)
print('C(0) =', C[0], 'C(1) =', C[1], 'TC(0) =', TC[0], '| states 0..3 =', states[:4])
# which elements of <T,C> preserve {h0=0, h1=0, h2+h3<=1} as a constraint set
def p1_preserved(p):
    return {p[0], p[1]} == {0, 1} and {p[2], p[3]} == {2, 3}
print('elements of <T,C> preserving P1:', [nm for nm, p in (('id', ID), ('T', T), ('C', C), ('TC', TC)) if p1_preserved(p)])
json.dump({'T': T, 'C': C, 'orbits': orbits}, open(sys.argv[3], 'w'))
