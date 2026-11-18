#!/usr/bin/env python3
"""Exclude high-split cuts, conditional on the smaller-size selection theorem.

These rows are NOT unconditional propositional consequences of the base. Their
research use requires the written reduction; the singleton-right cut additionally
requires the positive selection theorem at the preceding size. The receipt
records these dependencies explicitly.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import resource


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cnf', type=Path, required=True)
    parser.add_argument('--map', type=Path, required=True)
    parser.add_argument('--m', type=int, required=True)
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (300 << 20, 300 << 20))
    assert 5 <= args.n <= 8 and args.m >= args.n - 1
    orientations = {}
    nv = 0
    for line in args.map.read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        raw, kind, mask = line.split()
        v, mask = int(raw), int(mask)
        assert v == nv + 1
        nv = v
        if kind == 'orientation':
            triple = tuple(i for i in range(args.m) if mask >> i & 1)
            assert len(triple) == 3 and triple not in orientations
            orientations[triple] = v
    assert set(orientations) == set(itertools.combinations(range(args.m), 3))
    rows = []
    for cut in range(1, args.m):
        row = []
        for (a, b, c), v in orientations.items():
            if b < cut <= c:       # LLR must be a cup in a high split.
                row.append(-v)
            elif a < cut <= b:     # LRR must be a cap in a high split.
                row.append(v)
        assert len(row) == cut * (args.m - cut) * (args.m - 2) // 2
        rows.append(row)
    with args.cnf.open() as source, args.out.open('x') as output:
        header = source.readline().split()
        assert header[:2] == ['p', 'cnf'] and int(header[2]) == nv
        old = int(header[3])
        output.write(f'p cnf {nv} {old + len(rows)}\n')
        for line in source:
            output.write(line)
        output.write('c conditional minimal-counterexample high-split exclusions\n')
        for row in rows:
            output.write(' '.join(map(str, row)) + ' 0\n')
    record = {
        'label': 'COMPUTED conditional formula construction',
        'm': args.m, 'n': args.n, 'variables': nv,
        'base_clauses': old, 'added_clauses': len(rows),
        'clauses': old + len(rows),
        'cuts': [{'cut': k, 'literals': len(row)}
                 for k, row in enumerate(rows, 1)],
        'required_dependencies': [
            'written high-split minimal-counterexample reduction',
            f'terminal-safe existence at old-set size {args.m - 1} for the singleton-right cut',
            'semantic audit of the base CNF and its map',
            'independent audit of these added rows',
            'cake_lpr exact s VERIFIED UNSAT verdict for any UNSAT claim'],
        'hashes': {'base': sha(args.cnf), 'map': sha(args.map),
                   'output': sha(args.out), 'augmenter': sha(Path(__file__))}}
    Path(str(args.out) + '.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
