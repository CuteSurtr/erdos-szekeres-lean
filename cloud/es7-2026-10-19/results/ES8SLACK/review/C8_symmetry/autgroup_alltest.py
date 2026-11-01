"""Exact automorphism group of a colored hypergraph on the 252 balanced states,
by canonical colour refinement + exhaustive individualization-refinement
(all leaves of the search tree are enumerated, no pruning, so the result is
complete as long as refinement is equivariant, which it is: colours are
relabelled by sorting isomorphism-invariant signatures).

Every automorphism reported is verified directly on the hyperedge set.
Standard library only.

Modes (argv[2]):
  base     : hyperedges = supports of the 2,685 base rows, coloured by rhs
  all      : hyperedges = supports of all 3,131 rows, coloured by (rhs, kind)
  k8       : hyperedges = all 8-subsets of base supports (minimal non-faces of
             the occupied-set complex = exact symmetry group of the Boolean
             feasible set of the base rows)
  base_p1  : base + early-vertex constraints {0}:'occ', {1}:'occ', {2,3}:'atleast1occ'
  k8_p1    : k8 + the same early-vertex hyperedges
"""
import json, sys, itertools, time
from collections import Counter

SRC, MODE = sys.argv[1], sys.argv[2]
NODE_LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
d = json.load(open(SRC))
cons = d['constraints']
NS = 252

edges = []   # list of (frozenset(states), colour)
if MODE in ('base', 'base_p1'):
    for c in cons:
        edges.append((frozenset(c['support']), ('row', c['rhs'])))
elif MODE == 'all':
    for c in cons:
        edges.append((frozenset(c['support']), ('row', c['rhs'], c.get('kind', 'base'))))
elif MODE in ('k8', 'k8_p1'):
    K = set()
    for c in cons:
        S = sorted(c['support'])
        assert len(S) - c['rhs'] == 7
        for sub in itertools.combinations(S, 8):
            K.add(frozenset(sub))
    for s in K:
        edges.append((s, ('k8',)))
else:
    raise SystemExit('bad mode')
if MODE.endswith('_p1'):
    edges.append((frozenset([0]), ('occ',)))
    edges.append((frozenset([1]), ('occ',)))
    edges.append((frozenset([2, 3]), ('atleast1occ',)))

# sanity: no duplicate (set, colour)
assert len(set(edges)) == len(edges)
M = len(edges)
n = NS + M
adj = [[] for _ in range(n)]
for j, (s, col) in enumerate(edges):
    for i in s:
        adj[i].append(NS + j)
        adj[NS + j].append(i)
ecol_names = sorted(set(col for _, col in edges), key=repr)
init = [0] * NS + [1 + ecol_names.index(col) for _, col in edges]
cov = Counter(len(adj[i]) for i in range(NS))
print(MODE, ': states', NS, 'hyperedges', M, 'incidences', sum(len(s) for s, _ in edges),
      '| states in no hyperedge:', sum(1 for i in range(NS) if not adj[i]))


def relabel(sigs):
    keys = sorted(set(sigs))
    m = {k: t for t, k in enumerate(keys)}
    return [m[s] for s in sigs], len(keys)


def refine(colors):
    colors, k = relabel(colors)
    while True:
        sigs = [(colors[v], tuple(sorted(colors[u] for u in adj[v]))) for v in range(n)]
        new, k2 = relabel(sigs)
        if k2 == k:
            return new, k
        colors, k = new, k2


def individualize(colors, v):
    return [(colors[x], 1 if x == v else 0) for x in range(n)]


def cells_of(colors):
    cl = {}
    for v in range(NS):
        cl.setdefault(colors[v], []).append(v)
    return cl


edge_set = set(edges)


def is_aut(sig):  # sig: list of length NS
    for s, col in edges:
        if (frozenset(sig[i] for i in s), col) not in edge_set:
            return False
    return True


t0 = time.time()
c0, k0 = refine(init)
cl0 = cells_of(c0)
print('equitable partition on states: %d cells, size histogram %s' % (
    len(cl0), dict(sorted(Counter(len(v) for v in cl0.values()).items()))))

leaves = []
nodes = [0]


def search(colors, depth, path):
    nodes[0] += 1
    if nodes[0] > NODE_LIMIT:
        raise RuntimeError('node limit')
    cl = cells_of(colors)
    nonsing = [c for c in sorted(cl) if len(cl[c]) > 1]
    # hyperedge vertices: once states are discrete, hyperedges (distinct sets) are discrete too
    if not nonsing:
        leaves.append((list(path), colors))
        return
    target = cl[nonsing[0]]
    for v in target:
        nc, _ = refine(individualize(colors, v))
        search(nc, depth + 1, path + [v])


search(c0, 0, [])
print('search nodes:', nodes[0], 'leaves:', len(leaves), 'max depth:', max(len(p) for p, _ in leaves),
      'time %.1fs' % (time.time() - t0))
p0, L0 = leaves[0]
inv0 = {L0[v]: v for v in range(NS)}
auts = set()
for p, L in leaves:
    inv = {L[v]: v for v in range(NS)}
    # sigma maps the vertex with colour c in leaf 0 to the vertex with colour c in leaf L
    sig = [inv[L0[v]] for v in range(NS)]
    if sorted(sig) == list(range(NS)) and is_aut(sig):
        auts.add(tuple(sig))
print('|Aut| =', len(auts))
out = {'mode': MODE, 'order': len(auts), 'automorphisms': sorted(auts),
       'equitable_cells': len(cl0), 'leaves': len(leaves)}
# orbits of Aut on states
orb = {}
for v in range(NS):
    o = frozenset(a[v] for a in auts)
    orb[o] = 1
print('Aut-orbits on states:', len(orb), 'sizes', dict(Counter(len(o) for o in orb)))
if len(sys.argv) > 4:
    json.dump(out, open(sys.argv[4], 'w'))
