#!/usr/bin/env python3
"""Translate the supplied DPLL tree to ordinary Lean proof terms; not a Lean checker.

All output goes to the authorized scratch directory. No solver verdict is trusted by
the resulting theorem: every unit step, conflict, and split becomes a proof term.
"""
from pathlib import Path
import hashlib
import json

SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/extension/lean')
DATA = Path(__file__).resolve().parent / 'data'
ORIGINAL = DATA / 'terminal15-original.cnf'
CORE = DATA / 'terminal15-core.cnf'
META = DATA / 'terminal15-core-DONE.json'
TREE = DATA / 'terminal15-tree.json'
EXPECTED_CNF = '7d18c713d190d893a4d3d7873e8caa7d45061326c403ee8133888382040cc22a'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_cnf(path):
    rows = []
    header = None
    for line in path.read_text().splitlines():
        words = line.split()
        if not words or words[0] == 'c':
            continue
        if words[0] == 'p':
            assert header is None and words[1] == 'cnf' and len(words) == 4
            header = tuple(map(int, words[2:]))
        else:
            row = list(map(int, words))
            assert row[-1] == 0 and 0 not in row[:-1]
            rows.append(row[:-1])
    assert header is not None and header[1] == len(rows)
    assert all(1 <= abs(lit) <= header[0] for row in rows for lit in row)
    return header, rows


assert sha(ORIGINAL) == EXPECTED_CNF
header, rows = read_cnf(ORIGINAL)
assert header == (15, 313)
info = json.loads(META.read_text())
ids = info['original_clause_ids']
assert ids == sorted(set(ids)) and len(ids) == 98
assert read_cnf(CORE) == ((15, 98), [rows[i - 1] for i in ids])
assert sha(CORE) == info['hashes']['core.cnf']
assert sha(TREE) == info['hashes']['tree.json']
tree = json.loads(TREE.read_text())
stats = {'nodes': 0, 'leaves': 0, 'unit_steps': 0}


def literal(lit):
    return f'p{lit}' if lit > 0 else f'¬p{-lit}'


def clause(row):
    assert row
    return ' ∨ '.join(literal(lit) for lit in row)


def eliminate(cid, assignment, target=None):
    """Eliminate every disjunct of the original clause to a unit literal or False."""
    assert cid in ids
    row = rows[cid - 1]
    if target is not None:
        assert target in row and abs(target) not in assignment

    def arm(lit, witness):
        if lit == target:
            return witness
        assert abs(lit) in assignment and assignment[abs(lit)] != (lit > 0)
        known = f'h{abs(lit)}'
        contradiction = f'({known} {witness})' if lit > 0 else f'({witness} {known})'
        return f'(False.elim {contradiction})' if target is not None else contradiction

    def descend(offset, witness):
        if offset == len(row) - 1:
            return arm(row[offset], witness)
        left, right = f'x{offset}', f'r{offset}'
        return f'(Or.elim {witness} (fun {left} => {arm(row[offset], left)}) ' \
               f'(fun {right} => {descend(offset + 1, right)}))'

    return descend(0, f'c{cid:03}')


def emit_tree(node, assignment, indent):
    stats['nodes'] += 1
    assignment = dict(assignment)
    lines = []
    pad = ' ' * indent
    for unit in node['units']:
        lit, cid = unit['literal'], unit['reason']
        assert abs(lit) not in assignment
        proof = eliminate(cid, assignment, lit)
        lines.append(f'{pad}have h{abs(lit)} : {literal(lit)} := {proof}')
        assignment[abs(lit)] = lit > 0
        stats['unit_steps'] += 1
    if 'conflict' in node:
        assert 'branch' not in node
        lines.append(f'{pad}exact {eliminate(node["conflict"], assignment)}')
        stats['leaves'] += 1
        return lines
    var = node['branch']
    assert 1 <= var <= 15 and var not in assignment
    lines.append(f'{pad}exact (Classical.em p{var}).elim')
    for key, value in [('true', True), ('false', False)]:
        lines.append(f'{pad}  (fun h{var} => by')
        lines.extend(emit_tree(node[key], {**assignment, var: value}, indent + 4))
        lines.append(f'{pad}  )')
    return lines


variables = ' '.join(f'p{i}' for i in range(1, 16))
bools = ' '.join(f'b{i}' for i in range(1, 16))
bool_props = ' '.join(f'(b{i} = true)' for i in range(1, 16))
lines = [
    '/-! Fixed 15-variable Boolean refutation. Generated ordinary proof terms.',
    f'Original DIMACS SHA-256: {EXPECTED_CNF}.',
    'The source is a candidate until a bounded Lean check and axiom audit pass.',
    'No geometric claim is encoded here. -/',
    '',
    'set_option maxRecDepth 4096',
    '',
    'namespace Delta3.Terminal15Boolean',
    '',
    '/-- The 313 original clauses, in exact DIMACS row order. -/',
    f'def terminalFormula ({variables} : Prop) : Prop :=',
]
for index, row in enumerate(rows):
    lines.append(f'  ({clause(row)})' + (' ∧' if index < len(rows) - 1 else ''))
lines += ['', '/-- Refutation of the supplied 98-clause subset by explicit case analysis. -/',
          f'theorem core_unsat ({variables} : Prop)']
for cid in ids:
    lines.append(f'    (c{cid:03} : {clause(rows[cid - 1])})')
lines += ['    : False := by'] + emit_tree(tree, {}, 2)
assert stats['nodes'] == 85 and stats['leaves'] == 43
lines += ['', '/-- The full original formula implies the refuted subset. -/',
          f'theorem terminal_unsat_prop ({variables} : Prop)',
          f'    (h : terminalFormula {variables}) : False := by']
tail = 'h'
for cid in range(1, 314):
    if cid in ids:
        projection = f'{tail}.1' if cid < 313 else tail
        lines.append(f'  have c{cid:03} := {projection}')
    if cid < 313:
        lines.append(f'  have tail{cid} := {tail}.2')
        tail = f'tail{cid}'
lines.append(f'  exact core_unsat {variables}')
lines.append('    ' + ' '.join(f'c{cid:03}' for cid in ids))
lines += ['', '/-- The fixed CNF interpreted on fifteen Boolean membership values. -/',
          f'def terminalBoolFormula ({bools} : Bool) : Prop :=',
          f'  terminalFormula {bool_props}',
          '', '/-- No assignment of the fifteen Boolean values satisfies the fixed CNF. -/',
          f'theorem terminal_unsat_bool ({bools} : Bool) :',
          f'    ¬terminalBoolFormula {bools} :=',
          f'  fun h => terminal_unsat_prop {bool_props} h',
          '', '#print axioms core_unsat', '#print axioms terminal_unsat_prop',
          '#print axioms terminal_unsat_bool', '', 'end Delta3.Terminal15Boolean', '']
source = SCRATCH / 'Terminal15Boolean.lean'
source.write_text('\n'.join(lines))
record = {'original_cnf_sha256': EXPECTED_CNF,
          'core_cnf_sha256': sha(CORE),
          'tree_sha256': sha(TREE),
          'source_sha256': sha(source), 'generator_sha256': sha(Path(__file__)),
          'original_clause_ids': ids, 'tree_statistics': stats,
          'status': 'generated candidate; no Lean check by this script'}
(SCRATCH / 'boolean-generation.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({k: record[k] for k in ('status', 'source_sha256', 'tree_statistics')}, indent=2))
