#!/usr/bin/env python3
"""Parent audit: exact integer hulls, full subset scans, no finder imports."""
from collections import Counter
from fractions import Fraction
import hashlib
import itertools as it
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    cases = [('terminal', 'terminal/data/witness.json', 'terminal/data/witness.terminal.cnf'),
             ('repair7', 'repair/data/rotation-best.json', 'repair/data/rightmost-n7-one.cnf'),
             ('repair8', 'repair/data/two-clones-n8-best.json', 'repair/data/rightmost-n8-one.cnf')]
    results = []
    for kind, source, formula in cases:
        f = json.loads((HERE/source).read_text())
        P, n = f['P'], f['n']
        m, full = len(P), (1 << len(P))-1
        assert all(P[i][0] < P[i+1][0] for i in range(m-1))
        def turn(a, b, c):
            a, b, c = P[a], P[b], P[c]
            return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        dets = {t: turn(*t) for t in it.combinations(range(m), 3)}
        assert all(dets.values())
        def cap(q):
            return all(dets[t] < 0 for t in it.combinations(q, 3))
        def convex(q):
            def chain(order):
                st = []
                for v in order:
                    while len(st) >= 2 and turn(st[-2], st[-1], v) <= 0:
                        st.pop()
                    st.append(v)
                return st
            return len(chain(q))+len(chain(reversed(q)))-2 == len(q)
        caps = [q for q in it.combinations(range(m), 4) if cap(q)]
        targets = [q for q in it.combinations(range(m), n-1) if convex(q)]
        assert not any(cap(q) for q in it.combinations(range(m), 5))
        assert not any(convex(q) for q in it.combinations(range(m), n))
        mask = lambda q: sum(1 << i for i in q)
        def contains(family):
            b = bytearray(1 << m)
            for q in family:
                b[mask(q)] = 1
            for i in range(m):
                bit = 1 << i
                for s in range(1 << m):
                    if s & bit:
                        b[s] |= b[s ^ bit]
            return b
        hascap, hastarget = contains(caps), contains(targets)
        deltas = [s for s in range(1 << m) if not hascap[s] and not hastarget[full ^ s]]
        rows = [tuple(-(i+1) for i in q) for q in caps]
        extra = {}
        if kind == 'terminal':
            ends = {q[-2:] for q in caps}
            bad = [q for q in it.combinations(range(m), 3) if cap(q) and q[-2:] not in ends]
            # No-five-cap also makes every four-cap contain such a bad triple.
            assert all(q[:3] in bad for q in caps)
            rows += [tuple(-(i+1) for i in q) for q in bad]
            hasbad = contains(bad)
            assert not any(not hasbad[s] for s in deltas)
            core = HERE/'terminal/data/witness.core.cnf'
            extra.update(rank3_triples=len(bad), terminal_deltas=0,
                         core_sha256=sha(core), core_rows=[])
            A = mask(f['all_X_envelope_Delta'])
            assert A in deltas
            proof = json.loads((HERE/'terminal/data/all_X_direct_proof.json').read_text())
            q = tuple(proof['ambient_cap'])
            assert q in caps
            def line(pair, x):
                i, j = pair
                return P[i][1]+Fraction(P[j][1]-P[i][1], P[j][0]-P[i][0])*(x-P[i][0])
            def slope(pair):
                i, j = pair
                return Fraction(P[j][1]-P[i][1], P[j][0]-P[i][0])
            triples = [t for t in it.combinations(f['all_X_envelope_Delta'], 3) if cap(t)]
            for t in triples:
                assert line(q[-2:], P[-1][0]) > line(t[-2:], P[-1][0])
                assert slope(q[-2:]) > slope(t[-2:])
            assert len(triples) == 2
            extra.update(all_X_envelope_witness=f['all_X_envelope_Delta'], cap_triples=len(triples))
        else:
            r, A = f['r'], mask(f['A'])
            assert r == m-1 and not (A >> r & 1) and not hascap[A]
            assert all(A & mask(q) for q in targets if r not in q)
            oldblue = full ^ (A | (1 << r))
            rows += [(-(i+1), -(j+1)) for i, j in it.combinations(range(m), 2)
                     if oldblue >> i & 1 and oldblue >> j & 1]
            costs = Counter((s & oldblue).bit_count() for s in deltas)
            assert min(costs) == 2
            best = min((s for s in deltas if (s & oldblue).bit_count() == 2),
                       key=lambda s: (s.bit_count(), s))
            extra.update(root=r, old_Delta=f['A'], minimum_old_blue_cost=2,
                         repair_cost_histogram=dict(costs),
                         positive_Delta=[i for i in range(m) if best >> i & 1],
                         rooted_working_deltas=sum(bool(s >> r & 1) for s in deltas))
        rows += [tuple(i+1 for i in q) for q in targets]
        def readcnf(path):
            out = []
            for line in path.read_text().splitlines():
                if line.startswith('c'):
                    continue
                if line.startswith('p'):
                    _, _, nv, nc = line.split()
                    assert int(nv) == m
                    continue
                row = tuple(map(int, line.split()))
                assert row[-1] == 0
                out.append(row[:-1])
            assert len(out) == int(nc)
            return out
        normalize = lambda rs: Counter(tuple(sorted(r)) for r in rs)
        assert normalize(rows) == normalize(readcnf(HERE/formula))
        if kind == 'terminal':
            actual = normalize(rows)
            core_rows = readcnf(core)
            assert all(actual[tuple(sorted(row))] >= amount
                       for row, amount in normalize(core_rows).items())
            extra['core_rows'] = len(core_rows)
        results.append(dict(label='COMPUTED', status='INDEPENDENTLY CONFIRMED', kind=kind,
                            m=m, n=n, fourcaps=len(caps), target_polygons=len(targets),
                            fivecaps=0, ngons=0, working_weak_deltas=len(deltas),
                            minimum_absolute_determinant=min(map(abs, dets.values())),
                            source=source, source_sha256=sha(HERE/source),
                            cnf=formula, cnf_sha256=sha(HERE/formula), clauses=len(rows),
                            **extra))
    (HERE/'data').mkdir(exist_ok=True)
    (HERE/'data/parent_obstructions.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ('kind','m','n','status','working_weak_deltas')} for r in results]))


if __name__ == '__main__':
    main()
