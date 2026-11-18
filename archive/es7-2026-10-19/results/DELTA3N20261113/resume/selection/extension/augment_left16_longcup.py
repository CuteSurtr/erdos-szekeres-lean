#!/usr/bin/env python3
"""Append the explicit long-cup consequence of a real T7(L) failure.

This is a conditional geometric reduction, not propositional equivalence
with the original compact formula. The original instance is unchanged.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while block := f.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cnf', type=Path, required=True)
    ap.add_argument('--map', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (150 << 20, 150 << 20))
    ids = {}
    oldvars = 0
    for line in a.map.read_text().splitlines():
        if line.startswith('#'):
            continue
        raw, kind, mask = line.split()
        assert int(raw) == oldvars + 1
        oldvars = int(raw)
        if kind == 'orientation':
            ids[tuple(i for i in range(16) if int(mask) >> i & 1)] = oldvars
    assert set(ids) == set(combinations(range(16), 3))
    cups = list(combinations(range(16), 6))
    assert len(cups) == 8008
    clauses = 21 * len(cups) + 1
    literals = 62 * len(cups)
    with a.cnf.open() as src, a.out.open('x') as dst:
        h = src.readline().split()
        assert h[:2] == ['p', 'cnf'] and int(h[2]) == oldvars
        oldrows = int(h[3])
        dst.write(f'p cnf {oldvars+len(cups)} {oldrows+clauses}\n')
        for line in src:
            dst.write(line)
        dst.write('c real T7 failure implies existence of a six-cup\n')
        for offset, cup in enumerate(cups, 1):
            z = oldvars + offset
            ts = [ids[t] for t in combinations(cup, 3)]
            assert len(ts) == 20
            for t in ts:
                dst.write(f'{-z} {t} 0\n')
            dst.write(' '.join(map(str, [z]+[-t for t in ts]))+' 0\n')
        dst.write(' '.join(str(oldvars+i) for i in range(1,len(cups)+1))+' 0\n')
    outmap = Path(str(a.out)+'.map')
    with outmap.open('x') as f:
        original = a.map.read_text()
        f.write(original)
        if not original.endswith('\n'):
            f.write('\n')
        for offset, cup in enumerate(cups, 1):
            mask = sum(1 << i for i in cup)
            f.write(f'{oldvars+offset} six_cup {mask}\n')
    receipt = {
        'label': 'COMPUTED conditional formula construction', 'left_m': 16, 'n': 7,
        'old_variables': oldvars, 'old_clauses': oldrows, 'new_variables': len(cups),
        'added_clauses': clauses, 'added_literals': literals,
        'hashes': {k: sha(p) for k,p in {'base':a.cnf, 'base_map':a.map,
                    'output':a.out,'output_map':outmap,'source':Path(__file__)}.items()},
        'geometric_dependency': 'structure2/low_split.md: maxcup(L)<=n-2 gives a terminal selector in the standard low join; exact T_n equivalence then implies T7(L). A real failure therefore has a six-cup.',
        'scope': 'No propositional equivalence is asserted. A real T7(L) failure canonically satisfies the new family. UNSAT still needs cake and independent audit.'}
    Path(str(a.out)+'.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
