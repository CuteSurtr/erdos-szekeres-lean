#!/usr/bin/env python3
"""Independent exact audit; no encoder or existing checker imports.

Checks the emitted clauses, the chosen old copy, every geometric premise,
and all Delta subsets. An abstract model is never called a real realization.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def orientations(points):
    if any(type(c) is not int for p in points for c in p):
        raise ValueError('integer coordinates required')
    if any(points[i][0] >= points[i+1][0] for i in range(len(points)-1)):
        raise ValueError('points not in strict x order')
    ds = []
    for a, b, c in combinations(points, 3):
        d = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
        if d == 0:
            raise ValueError('collinear triple')
        ds.append(d)
    return ''.join('+' if d > 0 else '-' for d in ds), min(map(abs, ds))


def load_source(path):
    data = json.loads(Path(path).read_text())
    signs, margin = orientations(data['P'])
    if 'signs' in data and signs != data['signs']:
        raise ValueError('source signs disagree with exact determinants')
    return data['P'], signs, margin


def read_model(path, nv):
    values = bytearray(nv+1)  # 0 absent, 1 false, 2 true
    verdicts = []
    with Path(path).open() as f:
        for line in f:
            if line.startswith('s '):
                verdicts.append(line.strip())
            if not line.startswith('v '):
                continue
            for lit in map(int, line.split()[1:]):
                if lit == 0:
                    continue
                v = abs(lit)
                if v > nv:
                    raise ValueError('model variable outside header')
                val = 2 if lit > 0 else 1
                if values[v] not in (0, val):
                    raise ValueError('inconsistent model')
                values[v] = val
    if verdicts != ['s SATISFIABLE']:
        raise ValueError('expected exactly one SAT verdict')
    if any(v == 0 for v in values[1:]):
        raise ValueError('incomplete model')
    return values


def check_clauses(path, values):
    clauses = literals = 0
    header = None
    with Path(path).open() as f:
        for line in f:
            if not line.strip() or line.startswith('c'):
                continue
            if line.startswith('p '):
                if header is not None:
                    raise ValueError('duplicate header')
                _, kind, nv, nc = line.split()
                if kind != 'cnf' or int(nv) != len(values)-1:
                    raise ValueError('wrong CNF header')
                header = int(nc)
                continue
            row = list(map(int, line.split()))
            if not row or row[-1] != 0 or 0 in row[:-1]:
                raise ValueError('expected exactly one complete clause per line')
            clauses += 1
            literals += len(row)-1
            if any(abs(x) >= len(values) for x in row[:-1]):
                raise ValueError('out of range literal')
            if not any(values[abs(x)] == (2 if x > 0 else 1) for x in row[:-1]):
                raise ValueError(f'unsatisfied clause {clauses}')
    if header != clauses:
        raise ValueError('clause count mismatch')
    return {'clauses': clauses, 'literals': literals}


def upward(m, seeds):
    out = bytearray(1 << m)
    for s in seeds:
        out[s] = 1
    # Full Boolean-lattice transform, independent of the bounded-deletion DAG.
    for v in range(m):
        b = 1 << v
        for base in range(0, 1 << m, 2*b):
            for d in range(b):
                out[base+b+d] |= out[base+d]
    return out


def geometry(signs, m, n, mode, points=None):
    triples = list(combinations(range(m), 3))
    if len(signs) != len(triples) or set(signs)-set('+-'):
        raise ValueError('invalid signs')
    t = dict(zip(triples, (s == '+' for s in signs)))
    if points is not None and orientations(points)[0] != signs:
        raise ValueError('realization has wrong signs')
    for a, b, c, d in combinations(range(m), 4):
        row = [t[a,b,c], t[a,b,d], t[a,c,d], t[b,c,d]]
        if sum(x != y for x, y in zip(row, row[1:])) > 1:
            raise ValueError('not a signotope')

    def lower_hull(s):
        h = []
        for v in s:
            while len(h) >= 2 and not t[h[-2],h[-1],v]:
                h.pop()
            h.append(v)
        return h

    def convex(s):
        if points is not None:
            # Monotone hull, separately from the all-quadruple sign criterion.
            lo = lower_hull(s)
            hi = []
            for v in s:
                while len(hi) >= 2 and t[hi[-2],hi[-1],v]:
                    hi.pop()
                hi.append(v)
            return len(lo)+len(hi)-2 == len(s)
        return all(t[a,b,c] == t[a,b,d] and t[a,c,d] == t[b,c,d]
                   for a,b,c,d in combinations(s,4))

    def cap(s):
        return all(not t[q] for q in combinations(s,3))

    def mask(s):
        return sum(1 << v for v in s)

    caps = [mask(s) for s in combinations(range(m),4) if cap(s)]
    cap5 = sum(cap(s) for s in combinations(range(m),5))
    ngons = sum(convex(s) for s in combinations(range(m),n))
    targets, polygons = set(), 0
    for g in combinations(range(m),n-1):
        if convex(g):
            polygons += 1
            if mode == 'weak':
                target = g
            elif points is not None:
                target = lower_hull(g)
            else:
                target = [g[0], g[-1]] + [v for v in g[1:-1] if t[g[0],v,g[-1]]]
            targets.add(mask(target))
    a, b = upward(m, caps), upward(m, targets)
    full = (1 << m)-1
    count, first = 0, None
    for d in range(full+1):
        if not a[d] and not b[full ^ d]:
            count += 1
            if first is None:
                first = [v for v in range(m) if d >> v & 1]
    return {'fourcaps': len(caps), 'fivecaps': cap5, 'convex_ngons': ngons,
            'target_polygons': polygons, 'targets': len(targets),
            'working_deltas': count, 'first_delta': first,
            'valid': cap5 == ngons == 0}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--meta', type=Path, required=True)
    p.add_argument('--model', type=Path, required=True)
    p.add_argument('--cnf', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    old_points, old_signs, margin = load_source(a.source)
    meta = json.loads(a.meta.read_text())
    values = read_model(a.model, meta['variables'])
    checked = check_clauses(a.cnf, values)
    positions = []
    for i, row in enumerate(meta['selector_ids']):
        active = [d for d, v in enumerate(row) if values[v] == 2]
        if len(active) != 1:
            raise ValueError('selector row is not exactly one')
        positions.append(i+active[0])
    if len(positions) != len(old_points) or any(x >= y for x,y in zip(positions,positions[1:])):
        raise ValueError('bad old embedding')
    m, n = meta['m'], meta['n']
    triples = list(combinations(range(m),3))
    signs = ''.join('+' if values[i+1] == 2 else '-' for i in range(len(triples)))
    ts = dict(zip(triples, signs))
    extracted = ''.join(ts[tuple(positions[i] for i in q)]
                        for q in combinations(range(len(old_points)),3))
    if extracted != old_signs:
        raise ValueError('old orientation not preserved')
    report = {'label': 'COMPUTED', 'scope': meta['scope'], 'm': m, 'n': n,
              'mode': meta['mode'], 'old_positions': positions, 'signs': signs,
              'source_minimum_abs_determinant': margin, 'source_sha256': digest(a.source),
              'cnf_sha256': digest(a.cnf), 'clause_check': checked,
              'realizability': 'NOT CHECKED'}
    if meta['scope'] != 'embedding_only':
        report['geometry'] = geometry(signs, m, n, meta['mode'])
        if not report['geometry']['valid']:
            raise ValueError('invalid orientation model')
        if meta['scope'] == 'counterexample' and report['geometry']['working_deltas'] != 0:
            raise ValueError('model has a working Delta')
    a.out.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'label': 'COMPUTED', 'status': 'SAT_CHECKED_ABSTRACT', 'out': str(a.out)}))


if __name__ == '__main__':
    main()
