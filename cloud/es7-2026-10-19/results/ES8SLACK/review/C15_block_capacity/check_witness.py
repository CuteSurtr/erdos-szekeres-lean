"""Independent checker for the C15 witnesses (does NOT import the probes' code).

For a witness JSON (owners 0..n-1 in x-order, a state per owner, a label per pair p<q,
and the set of positively oriented triples) and residual row K of source-2650, check:
  1. states: 4-tuples, each (f1..f4,0) is a catalog profile whose index lies in row K's support,
     pairwise distinct (injective owner map);
  2. orientation: every increasing triple gets a sign; signotope axiom: for all i<j<k<l the
     sequence s(ijk), s(ijl), s(ikl), s(jkl) has at most one sign change;
  3. labels: (a,b) in [1..4]x[1..6], (a,b) != (1,6), (a,b) in I(state q) \\ I(state p),
     with I(f) = {(a,b) : b <= f[a-1]}  (Lean: Domains.Contains s z := z.2 <= s.getD (z.1-1) 0);
  4. growth: cup (positive) triple p<q<r => b(p,q) < b(q,r); cap triple => a(p,q) < a(q,r);
  5. no 6-cap, no 8-cup, no cap and cup with common endpoints and >= 8 vertices in total.
     Chains are found by exhaustive DFS that tests ALL triples (not only consecutive ones);
  6. extra: brute-force all 8-subsets for convex position in the chirotope sense (every 4-subset
     in convex position, i.e. no point in the triangle of three others), max convex subset size;
     no 4-cap (consequence of the block compression); no junction among owners;
     compression certificate of block-data.json holds on the witness labels.
Usage: check_witness.py witness.json K
"""
import sys, json, gzip, itertools

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
REPO = ROOT + '/experiments'
SRC = REPO + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
BLK = REPO + '/omission-residual-geometry-2026-10-09/block-data.json'

wpath, K = sys.argv[1], int(sys.argv[2])
w = json.load(open(wpath))
src = json.load(gzip.open(SRC))
catalog = [tuple(s) for s in src['states']]
row = src['constraints'][K]
support = set(row['support'])
res = {'witness': wpath, 'row': K, 'support_size': len(support), 'rhs': row['rhs']}

n = w['n']
assert w['row'] == K
states = [tuple(s) for s in w['states']]
assert len(states) == n
# 1. states
idx = []
for s in states:
    assert len(s) == 4 and all(isinstance(x, int) for x in s)
    full = s + (0,)
    assert full in catalog, ('state not in catalog', s)
    idx.append(catalog.index(full))
res['states_in_support'] = all(i in support for i in idx)
res['states_distinct'] = len(set(idx)) == n
res['catalog_indices'] = idx

# 2. orientation
pos = set()
for t in w['orientation_positive']:
    t = tuple(t)
    assert len(t) == 3 and 0 <= t[0] < t[1] < t[2] < n, t
    assert t not in pos
    pos.add(t)
def s3(i, j, k):
    return (i, j, k) in pos          # True = positive = cup turn
sign_ok = True
for i, j, k, l in itertools.combinations(range(n), 4):
    seq = [s3(i, j, k), s3(i, j, l), s3(i, k, l), s3(j, k, l)]
    changes = sum(1 for x, y in zip(seq, seq[1:]) if x != y)
    if changes > 1:
        sign_ok = False
res['signotope_ok'] = sign_ok

# 3. labels
lab = {}
for key, v in w['labels'].items():
    p, q = map(int, key.split(','))
    assert 0 <= p < q < n
    lab[(p, q)] = (int(v[0]), int(v[1]))
assert len(lab) == n * (n - 1) // 2
def inI(f, z):
    a, b = z
    return b <= f[a - 1]
lab_ok = True
for (p, q), (a, b) in lab.items():
    if not (1 <= a <= 4 and 1 <= b <= 6) or (a, b) == (1, 6):
        lab_ok = False
    if not (inI(states[q], (a, b)) and not inI(states[p], (a, b))):
        lab_ok = False
res['labels_ok'] = lab_ok

# 4. growth
gr_ok = True
for p, q, r in itertools.combinations(range(n), 3):
    if s3(p, q, r):
        gr_ok &= lab[(p, q)][1] < lab[(q, r)][1]
    else:
        gr_ok &= lab[(p, q)][0] < lab[(q, r)][0]
res['growth_ok'] = gr_ok

# 5. chains by exhaustive DFS checking all triples
def chains(sign):
    """longest[i][j] = max #vertices of a chain from i to j whose every triple has the given sign."""
    longest = [[0] * n for _ in range(n)]
    def dfs(seq):
        i, j = seq[0], seq[-1]
        if len(seq) > longest[i][j]:
            longest[i][j] = len(seq)
        for x in range(j + 1, n):
            if all(s3(seq[a], seq[b], x) == sign for a, b in itertools.combinations(range(len(seq)), 2)):
                dfs(seq + [x])
    for i in range(n):
        for j in range(i + 1, n):
            dfs([i, j])
    return longest
cap = chains(False)
cup = chains(True)
max_cap = max(cap[i][j] for i in range(n) for j in range(i + 1, n))
max_cup = max(cup[i][j] for i in range(n) for j in range(i + 1, n))
max_capcup = max(cap[i][j] + cup[i][j] - 2 for i in range(n) for j in range(i + 1, n))
res.update({'max_cap': max_cap, 'max_cup': max_cup, 'max_cap_plus_cup_vertices': max_capcup,
            'no_6cap': max_cap < 6, 'no_8cup': max_cup < 8, 'no_capcup_octagon': max_capcup < 8,
            'no_4cap': max_cap < 4})

# 6a. chirotope convex position (every 4-subset convex), brute force over all subsets
def conv4(a, b, c, d):
    x = (s3(a, b, c), s3(a, b, d), s3(a, c, d), s3(b, c, d))
    # b inside acd: (-y, y, y, y); c inside abd: (y, y, y, -y); a or d inside: patterns that
    # violate the signotope axiom (checked anyway for completeness)
    b_in = (not x[0]) == x[1] == x[2] == x[3]
    c_in = x[0] == x[1] == x[2] == (not x[3])
    a_in = x[0] == x[2] == x[3] == (not x[1])     # chi(b,c,a)=chi(c,d,a)=chi(d,b,a)=chi(b,c,d)
    d_in = x[0] == x[1] == x[3] == (not x[2])     # chi(a,b,d)=chi(b,c,d)=chi(c,a,d)=chi(a,b,c)
    return not (b_in or c_in or a_in or d_in)
C4 = {q: conv4(*q) for q in itertools.combinations(range(n), 4)}
# maximum convex subset via DFS (sets in increasing order)
best = [0, None]
def grow(cur, start):
    if len(cur) > best[0]:
        best[0], best[1] = len(cur), list(cur)
    for x in range(start, n):
        if all(C4[tuple(sorted(t + (x,)))] for t in itertools.combinations(cur, 3)):
            grow(cur + [x], x + 1)
grow([], 0)
res['max_convex_subset_chirotope'] = best[0]
res['max_convex_example'] = best[1]
cnt8 = sum(1 for S8 in itertools.combinations(range(n), 8)
           if all(C4[q] for q in itertools.combinations(S8, 4)))
res['convex_8_subsets_bruteforce'] = cnt8

# 6b. junction among owners: 6-cup ending at v and 5-cap starting at v
def chain_end_at(sign, length):
    ends = set()
    for seq in itertools.combinations(range(n), length):
        if all(s3(*t) == sign for t in itertools.combinations(seq, 3)):
            ends.add(seq[-1])
    return ends
def chain_start_at(sign, length):
    starts = set()
    for seq in itertools.combinations(range(n), length):
        if all(s3(*t) == sign for t in itertools.combinations(seq, 3)):
            starts.add(seq[0])
    return starts
res['junction_free'] = not (chain_end_at(True, 6) & chain_start_at(False, 5))

# 6c. compression certificate of the block row on the witness labels
blk = {b['row']: b for b in json.load(open(BLK))}
if K in blk:
    b = blk[K]
    active = set(map(tuple, b['active']))
    def compress(z):
        return 1 if z[0] <= b['thresholds'][z[1] - 1] else 2
    res['labels_in_active'] = all(z in active for z in lab.values())
    res['compressed_cap_growth'] = all(compress(lab[(p, q)]) < compress(lab[(q, r)])
                                       for p, q, r in itertools.combinations(range(n), 3) if not s3(p, q, r))
res['all_listed_conditions_ok'] = all(res[k] for k in ['states_in_support', 'states_distinct', 'signotope_ok',
                                                       'labels_ok', 'growth_ok', 'no_6cap', 'no_8cup',
                                                       'no_capcup_octagon'])
print(json.dumps(res))
