#!/usr/bin/env python3
"""Search for Baek block supports: S such that some 2-valued compression of the
labels strictly increases along every possible cap triple (no 4-cap among owners,
capacity 22) or along every cup triple (mirror Baek: no 4-cup, capacity 22).
For a fixed S the compression exists iff the labels forced low and forced high
are disjoint (forced low: an incoming label at a middle state that can be followed
by a larger-coordinate outgoing label; forced high: symmetric).  Conservative:
ignores the third domain of the triple, so it only under-reports supports.
Candidate supports: all upper sets, lower sets and two-sided intervals of profiles."""
import gzip, itertools, json, sys
ROOT = '/home/jay/research/lean/erdos-szekeres-lean/'
def load(kind):
    if kind == 'res':
        d = json.load(gzip.open(ROOT + 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz')); A = 4
    else:
        d = json.load(open(ROOT + 'experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json')); A = 5
    return d['states'], d['constraints'], A
def run(kind):
    S, C, A = load(kind)
    cells = [{(a + 1, y) for a in range(A) for y in range(1, s[a] + 1)} for s in S]
    n = len(S)
    D = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                d = cells[j] - cells[i]
                if kind == 'res': d.discard((1, 6))
                D[i, j] = d
    def compressible(X, coord):
        low = set(); high = set()
        for y in X:
            inn = set().union(*[D[x, y] for x in X if x != y]) if len(X) > 1 else set()
            out = set().union(*[D[y, z] for z in X if z != y]) if len(X) > 1 else set()
            for l1 in inn:
                for l2 in out:
                    if l2[coord] > l1[coord]:
                        low.add(l1); high.add(l2)
            if low & high:
                return False
        return not (low & high)
    hmax = 6 if kind == 'res' else 5
    fams = {}
    for lo in itertools.product(range(hmax + 1), repeat=A):
        if any(lo[i] < lo[i + 1] for i in range(A - 1)): continue
        his = [None] + ([lo2 for lo2 in itertools.product(range(hmax + 1), repeat=A)] if all(v == 0 for v in lo) else [])
        for hi in his:
            if hi is not None and (any(hi[i] < hi[i + 1] for i in range(A - 1)) or any(hi[i] < lo[i] for i in range(A))):
                continue
            X = tuple(i for i, s in enumerate(S) if all(s[a] >= lo[a] for a in range(A))
                      and (hi is None or all(s[a] <= hi[a] for a in range(A))))
            if len(X) > 22:
                fams[X] = (lo, hi)
    print(kind, 'candidate supports >22:', len(fams), flush=True)
    found = []
    for X, (lo, hi) in sorted(fams.items(), key=lambda kv: -len(kv[0])):
        for coord, name in ((0, 'cap'), (1, 'cup')):
            if compressible(list(X), coord):
                inside = any(set(X) <= set(r['support']) and r['rhs'] >= len(X) - 22 for r in C)
                found.append({'lo': lo, 'hi': hi, 'size': len(X), 'kind': name, 'demand': len(X) - 22, 'implied_by_row': inside})
    found.sort(key=lambda f: -f['size'])
    for f in found[:20]: print('  ', f)
    print(kind, 'compressible supports >22:', len(found))
    json.dump(found, open(f'block_search_{kind}.json', 'w'), indent=1)
if __name__ == '__main__':
    run(sys.argv[1])
