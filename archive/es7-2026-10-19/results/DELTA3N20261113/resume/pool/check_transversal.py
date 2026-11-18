#!/usr/bin/env python3
"""Exact audit of a signotope transversal witness; imports no encoder.

This does not establish realizability or refute weak Delta.  The SAT model
and a separately reconstructed canonical assignment are both checked.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dir', type=Path, required=True)
    a = ap.parse_args()
    f = json.loads((a.dir / 'geometry.json').read_text())
    m = f['m']
    triples = list(it.combinations(range(m), 3))
    assert len(f['signs']) == len(triples)
    assert set(f['signs']) <= {'+', '-'}
    signs = {sum(1 << i for i in t): c == '+'
             for t, c in zip(triples, f['signs'])}
    mask = lambda v: sum(1 << i for i in v)
    vertices = lambda s: [i for i in range(m) if s >> i & 1]
    cv4, caps4 = {}, []
    for q in it.combinations(range(m), 4):
        p = [signs[mask(t)] for t in it.combinations(q, 3)]
        assert sum(x != y for x, y in zip(p, p[1:])) <= 1
        cv4[mask(q)] = p[0] == p[1] and p[2] == p[3]
        if not any(p):
            caps4.append(mask(q))
    convex = {}
    for k in range(4, 9):
        for q in it.combinations(range(m), k):
            convex[mask(q)] = all(cv4[mask(t)] for t in it.combinations(q, 4))
    assert not any(all(not signs[mask(t)] for t in it.combinations(q, 3))
                   for q in it.combinations(range(m), 5))
    assert not any(convex[mask(q)] for q in it.combinations(range(m), 8))
    hexagons = [s for s, c in convex.items() if c and s.bit_count() == 6]
    heptagons = [s for s, c in convex.items() if c and s.bit_count() == 7]

    def contains(seeds):
        b = bytearray(1 << m)
        for s in seeds:
            b[s] = 1
        # Unrestricted subset zeta transform, unlike the encoded deletion DAG.
        for i in range(m):
            bit = 1 << i
            for s in range(1 << m):
                if s & bit:
                    b[s] |= b[s ^ bit]
        return b

    has6, has7, hascap = map(contains, (hexagons, heptagons, caps4))
    full = (1 << m) - 1
    transversal = min((s for s in range(1 << m) if not has6[full ^ s]),
                      key=lambda s: (s.bit_count(), s))
    assert transversal.bit_count() > 5
    five_complements = sum(s.bit_count() == 5 for s in range(1 << m))
    assert all(has6[full ^ s] for s in range(1 << m) if s.bit_count() == 5)
    deltas = [s for s in range(1 << m) if not hascap[s] and not has7[full ^ s]]
    assert len(deltas) == f['modes']['weak']['working_deltas']

    canonical, model = {}, {}
    for line in (a.dir / 'mapped.cnf.map').read_text().splitlines():
        if line.startswith('#'):
            continue
        var, kind, s = line.split()
        var, s = int(var), int(s)
        canonical[var] = {'orientation': signs, 'convex': convex,
                          'contains_hexagon': has6}[kind][s]
    for line in (a.dir / 'probe.out').read_text().splitlines():
        if line.startswith('v '):
            for lit in map(int, line.split()[1:]):
                if lit:
                    assert abs(lit) not in model or model[abs(lit)] == (lit > 0)
                    model[abs(lit)] = lit > 0
    assert len(model) == len(canonical)
    clauses = literals = 0
    with (a.dir / 'mapped.cnf').open() as file:
        for line in file:
            if line.startswith('c'):
                continue
            if line.startswith('p'):
                _, _, nv, nc = line.split()
                continue
            row = list(map(int, line.split()))
            assert row[-1] == 0 and all(row[:-1])
            for values in (canonical, model):
                assert any(values[abs(lit)] == (lit > 0) for lit in row[:-1])
            clauses += 1
            literals += len(row) - 1
    assert len(canonical) == int(nv) and clauses == int(nc)
    hashes = {name: hashlib.sha256((a.dir / name).read_bytes()).hexdigest()
              for name in ('mapped.cnf', 'mapped.cnf.map', 'n8m16.cnf',
                           'geometry.json', 'probe.out')}
    assert hashes['mapped.cnf'] == hashes['n8m16.cnf']
    result = dict(label='COMPUTED', status='EXACT ABSTRACT WITNESS CONFIRMED',
                  m=m, n=8, fourcaps=len(caps4), fivecaps=0, octagons=0,
                  hexagons=len(hexagons), heptagons=len(heptagons),
                  minimum_hexagon_transversal_size=transversal.bit_count(),
                  first_minimum_transversal=vertices(transversal),
                  five_point_deletions_checked=five_complements,
                  working_weak_deltas=len(deltas), first_weak_delta=vertices(deltas[0]),
                  canonical_and_solver_model_clauses_checked=clauses,
                  variables=int(nv), literals=literals, hashes=hashes,
                  realizability='UNRESOLVED; optimizer failure is not evidence',
                  weak_delta_refuted=False)
    (a.dir / 'exact_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
