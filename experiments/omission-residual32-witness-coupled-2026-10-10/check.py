#!/usr/bin/env python3
"""Independently replay the frozen RUP proof and deletion witnesses.

This standard-library checker supplements the Lean proofs. It does not replace
Lean's geometric necessity proof or assert realizability of a SAT assignment.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path


def check_rup(root):
    meta = json.loads((root / 'core13.json').read_text())
    cnf = root / 'core13.cnf'
    lrat = root / 'core13.lrat'
    for path, key in [(cnf, 'cnf_sha256'), (lrat, 'lrat_sha256')]:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == meta[key]
    lines = cnf.read_text().splitlines()
    header = lines.pop(0).split()
    assert header[:2] == ['p', 'cnf']
    assert int(header[2]) == len(meta['variables']) == 337
    clauses = [list(map(int, line.split())) for line in lines]
    assert all(c[-1] == 0 for c in clauses)
    clauses = [c[:-1] for c in clauses]
    assert clauses == [c['literals'] for c in meta['clauses']]
    assert len(clauses) == int(header[3]) == 376
    db = dict(enumerate(clauses, 1))
    steps = 0
    for line in lrat.read_text().splitlines():
        nums = list(map(int, line.split()))
        zero = nums.index(0)
        index, clause, hints = nums[0], nums[1:zero], nums[zero + 1:-1]
        assert nums[-1] == 0 and index not in db and all(h > 0 for h in hints)
        values, conflict = {}, False
        for literal in clause:
            var, truth = abs(literal), literal < 0
            assert 1 <= var <= 337
            if var in values and values[var] != truth:
                conflict = True
                break
            values[var] = truth
        if not conflict:
            for hint in hints:
                unknown = []
                for literal in db[hint]:
                    value = values.get(abs(literal))
                    if value is None:
                        unknown.append(literal)
                    else:
                        assert value != (literal > 0), ('satisfied hint', index, hint)
                assert len(unknown) <= 1
                if not unknown:
                    conflict = True
                    break
                literal = unknown[0]
                values[abs(literal)] = literal > 0
        assert conflict, ('failed RUP', index)
        db[index] = clause
        steps += 1
    assert clause == [] and steps == 258
    return steps


def check_deletions(root):
    data = json.loads(gzip.decompress((root / 'deletion-witnesses.json.gz').read_bytes()))
    meta = json.loads((root / 'core13.json').read_text())
    source = Path(__file__).resolve().parents[2] / 'experiments/omission-residual32-research-2026-10-10/source.json.gz'
    source_bytes = gzip.decompress(source.read_bytes())
    assert hashlib.sha256(source_bytes).hexdigest() == data['source_sha256'], 'Deletion source identity mismatch'
    states = json.loads(source_bytes)['states']
    assert data['core'] == meta['support'], 'Deletion core identity mismatch'
    profiles = data['profiles']
    assert profiles == {str(s): states[s] for s in meta['support']}, 'Deletion profile identity mismatch'
    checked = set()
    for row in data['witnesses']:
        support, assignment = row['support'], row['assignment']
        assert set(support) == set(data['core']) - {row['removed']}
        checked.add(row['removed'])
        n = len(support)
        positions = assignment['positions']
        assert sorted(positions) == list(range(n))
        labels = {(i, j): (a, b) for i, j, a, b in assignment['labels']}
        signs = {tuple(q[:3]): q[3] for q in assignment['orientations']}
        cells = [{(a + 1, b) for a, h in enumerate(profiles[str(s)][:4])
                  for b in range(1, h + 1)} for s in support]
        differences = {(i, j): cells[j] - cells[i]
                       for i, j in itertools.permutations(range(n), 2)}

        def orient(q):
            odd = sum(q[i] > q[j] for i in range(3) for j in range(i + 1, 3)) % 2
            result = signs[tuple(sorted(q))]
            assert isinstance(result, bool)
            return not result if odd else result

        def fixed_positive(q):
            for perm in itertools.permutations(range(3)):
                a, b, c = [q[i] for i in perm]
                ab, bc, ac = differences[a, b], differences[b, c], differences[a, c]
                if not ab or not bc or not ac:
                    continue
                coord = sum(perm[i] > perm[j] for i in range(3)
                            for j in range(i + 1, 3)) % 2
                if max(z[coord] for z in bc) > min(z[coord] for z in ab):
                    return False
            return True

        for i, j in itertools.combinations(range(n), 2):
            a, b = labels[i, j]
            assert 1 <= a <= 4 and 1 <= b <= 6 and (a, b) != (1, 6)
            u, v = (i, j) if positions[i] < positions[j] else (j, i)
            assert (a, b) in differences[u, v]
        order = sorted(range(n), key=positions.__getitem__)
        for a, b, c in itertools.combinations(order, 3):
            coord = 1 if orient((a, b, c)) else 0
            assert labels[tuple(sorted((a, b)))][coord] < labels[tuple(sorted((b, c)))][coord]
        for a, b, c in itertools.combinations(range(n), 3):
            if fixed_positive((a, b, c)):
                assert orient((a, b, c))
            if fixed_positive((a, c, b)):
                assert orient((a, c, b))
        for quad in itertools.combinations(order, 4):
            bits = [orient(q) for q in itertools.combinations(quad, 3)]
            assert sum(x != y for x, y in zip(bits, bits[1:])) <= 1
        convex = {}
        for a, b, c, d in itertools.combinations(range(n), 4):
            x, y, z, w = [orient(q) for q in [(a, b, c), (a, b, d), (a, c, d), (b, c, d)]]
            convex[a, b, c, d] = sum([not w, z, not y, x]) == 2
        for eight in itertools.combinations(range(n), 8):
            assert any(not convex[q] for q in itertools.combinations(eight, 4))
    assert checked == set(data['core']) and len(data['witnesses']) == 13
    return len(checked)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path,
                        default=Path('experiments/omission-residual32-witness-coupled-2026-10-10'))
    args = parser.parse_args()
    print(json.dumps({'rup_steps': check_rup(args.root),
                      'complete_deletion_models': check_deletions(args.root),
                      'status': 'passed'}))


if __name__ == '__main__':
    main()
