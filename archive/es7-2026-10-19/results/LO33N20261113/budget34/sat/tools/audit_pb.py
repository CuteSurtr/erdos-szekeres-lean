#!/usr/bin/env python3
"""Strict independent audit of exported CP-SAT linear PB constraints.

No OR-Tools import. Accept only the explicit text grammar actually emitted,
compare every coefficient/domain/support to the frozen integer specification,
and reject any extra field/constraint. Also compare the parent's rows.txt.
"""
import collections
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

directory, model_file, parent_rows = map(Path, sys.argv[1:4])
provisional_path = Path(sys.argv[4]) if len(sys.argv) > 4 else None
meta = json.loads((directory/'encoding.json').read_text())
with gzip.open(meta['base'], 'rt') as f:
    source = json.load(f)
pool = json.loads(Path(meta['pool']).read_text())
F = [i for i, s in enumerate(source['states']) if s[0] >= 5]
Lo = [i for i, s in enumerate(source['states']) if s[0] <= 4]
t = meta['slice']
extra_provisional = json.loads(provisional_path.read_text()) if provisional_path else []
assert all(r['rhs'] == 1 and len(r['support']) == 9 for r in extra_provisional)
rows = source['constraints'] + pool + extra_provisional + [
    {'support': F, 'rhs': t or 19},
    {'support': Lo, 'rhs': 34-t if t else 14}]
lo64, hi64 = -(2**63), 2**63-1
expected = [([0], [1], [0, 0])] + [
    (r['support'], [1]*len(r['support']), [r['rhs'], hi64]) for r in rows] + [
    (list(range(154)), [1]*154, [lo64, 34])]
text = model_file.read_text()
pos, variables, constraints, hints = 0, [], [], []


def ints(s):
    assert re.fullmatch(r'\s*-?\d+(?:\s*,\s*-?\d+)*\s*', s)
    return [int(v.strip()) for v in s.split(',')]


while text[pos:].strip():
    head = re.match(r'\s*(variables|constraints|solution_hint)\s*\{', text[pos:])
    assert head, ('unknown top-level field', text[pos:pos+80])
    kind = head[1]
    start = pos+head.end()
    end, depth = start, 1
    while depth:
        assert end < len(text)
        depth += int(text[end] == '{')-int(text[end] == '}')
        end += 1
    body, pos = text[start:end-1], end
    if kind == 'variables':
        m = re.fullmatch(r'\s*name:\s*"h(\d+)"\s*domain:\s*\[([^]]+)\]\s*', body)
        assert m and ints(m[2]) == [0, 1]
        variables.append(int(m[1]))
    elif kind == 'constraints':
        m = re.fullmatch(r'\s*linear\s*\{\s*vars:\s*\[([^]]+)\]\s*'
                         r'coeffs:\s*\[([^]]+)\]\s*domain:\s*\[([^]]+)\]\s*\}\s*', body)
        assert m, ('unexpected non-linear or extra field', body[:160])
        constraints.append(tuple(ints(m[i]) for i in range(1, 4)))
    else:
        m = re.fullmatch(r'\s*vars:\s*\[([^]]+)\]\s*values:\s*\[([^]]+)\]\s*', body)
        assert m
        hints.append((ints(m[1]), ints(m[2])))
assert variables == list(range(154))
assert len(constraints) == len(expected)
for actual, wanted in zip(constraints, expected):
    S, coefficients, domain = actual
    assert len(S) == len(coefficients) == len(set(S))
    assert all(0 <= v < 154 for v in S)
    # OR-Tools sorts terms even when the source support is a cycle order.
    assert sorted(zip(S, coefficients)) == sorted(zip(wanted[0], wanted[1]))
    assert domain == wanted[2], 'PB domain differs from frozen specification'
assert len(hints) <= 1
if hints:
    assert hints[0][0] == list(range(154)) and len(hints[0][1]) == 154
    assert all(v in (0, 1) for v in hints[0][1])

lines = parent_rows.read_text().splitlines()
assert lines[0] == 'FASTBB-ROWS 1'
headers = dict(line.split(' ', 1) for line in lines[1:8])
assert int(headers['states']) == 154 and int(headers['base_rows']) == 2650
assert int(headers['rows']) == len(rows)-len(extra_provisional)
assert headers['source_sha256'] == meta['base_sha256']
parent_constraints = []
for line in lines[8:]:
    d, n, *S = map(int, line.split())
    assert n == len(S) == len(set(S)) and all(0 <= v < 154 for v in S)
    assert 1 <= d <= n
    parent_constraints.append((d, tuple(sorted(S))))
certified_rows = source['constraints'] + pool + rows[-2:]
want = [(r['rhs'], tuple(sorted(r['support']))) for r in certified_rows]
assert collections.Counter(parent_constraints) == collections.Counter(want)
result = {'label': 'COMPUTED exact independent PB and parent-row audit PASS',
          'Boolean_variables': len(variables), 'PB_constraints': len(constraints),
          'row_constraints': len(rows), 'capacity_F': t or 19,
          'capacity_Lo': 34-t if t else 14, 'budget': 34, 'h0': 0,
          'hint_is_separate_not_a_constraint': bool(hints),
          'parent_rows_sha256': hashlib.sha256(parent_rows.read_bytes()).hexdigest(),
          'exported_model_sha256': hashlib.sha256(model_file.read_bytes()).hexdigest(),
          'base_sha256': meta['base_sha256'], 'pool_sha256': meta['pool_sha256']}
if provisional_path:
    result['provisional_rows'] = len(extra_provisional)
    result['provisional_sha256'] = hashlib.sha256(provisional_path.read_bytes()).hexdigest()
    result['label'] = 'HEURISTIC model; exact independent PB audit PASS; uncertified extra rows'
(model_file.parent/'pb-audit.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
