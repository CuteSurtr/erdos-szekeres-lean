#!/usr/bin/env python3
"""Exact RUP and complete deletion replay for the fifth frozen core."""
import hashlib
import json
from pathlib import Path
from check_omission_coupled_core import check_deletions


def check_rup(root):
    meta = json.loads((root / 'core13.json').read_text())
    for suffix in ['cnf', 'lrat']:
        assert hashlib.sha256((root / ('core13.' + suffix)).read_bytes()).hexdigest() == meta[suffix + '_sha256']
    lines = (root / 'core13.cnf').read_text().splitlines()
    assert lines.pop(0).split() == ['p', 'cnf', '383', '425']
    clauses = [list(map(int, line.split())) for line in lines]
    assert all(c[-1] == 0 for c in clauses)
    clauses = [c[:-1] for c in clauses]
    assert clauses == [c['literals'] for c in meta['clauses']]
    assert len(meta['variables']) == 383 and len(clauses) == 425
    db, steps = dict(enumerate(clauses, 1)), 0
    for line in (root / 'core13.lrat').read_text().splitlines():
        nums = list(map(int, line.split()))
        zero = nums.index(0)
        index, clause, hints = nums[0], nums[1:zero], nums[zero + 1:-1]
        assert nums[-1] == 0 and index not in db and all(h > 0 for h in hints)
        values, conflict = {}, False
        for literal in clause:
            var, truth = abs(literal), literal < 0
            assert 1 <= var <= 383
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
                        assert value != (literal > 0)
                assert len(unknown) <= 1
                if not unknown:
                    conflict = True
                    break
                values[abs(unknown[0])] = unknown[0] > 0
        assert conflict
        db[index] = clause
        steps += 1
    assert clause == [] and steps == 339
    return steps


if __name__ == '__main__':
    root = Path('experiments/omission-coupled-fifth-2026-10-10')
    print(json.dumps({'rup_steps': check_rup(root),
                      'complete_deletion_models': check_deletions(root),
                      'status': 'passed'}))
