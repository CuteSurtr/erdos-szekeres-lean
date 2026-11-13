#!/usr/bin/env python3
"""Exact certificate replay and source identity checks; not a Lean substitute."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def preflight(manifest=None):
    if manifest is None:
        manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, digest in manifest['files'].items():
        require(sha(HERE / name) == digest, 'Changed bundle input: ' + name)
    for name, digest in manifest['external_inputs'].items():
        require(sha(ROOT / name) == digest, 'Changed external input: ' + name)
    return manifest


def check_rup(directory=HERE, stem='core-one'):
    meta = json.loads((directory / (stem + '.json')).read_text())
    for suffix in ['cnf', 'lrat']:
        require(sha(directory / (stem + '.' + suffix)) == meta[suffix + '_sha256'],
                'Changed ' + suffix.upper() + ' bytes')
    lines = (directory / (stem + '.cnf')).read_text().splitlines()
    header = lines.pop(0).split()
    require(len(header) == 4 and header[:2] == ['p', 'cnf'], 'CNF header')
    variables, count = map(int, header[2:])
    require(variables == len(meta['variables']), 'Variable count')
    clauses = [list(map(int, line.split())) for line in lines]
    require(all(c and c[-1] == 0 and all(0 < abs(x) <= variables for x in c[:-1])
                for c in clauses), 'CNF literal range or terminator')
    clauses = [c[:-1] for c in clauses]
    require(len(clauses) == count and clauses == [c['literals'] for c in meta['clauses']],
            'CNF metadata mismatch')
    database = dict(enumerate(clauses, 1))
    steps = 0
    last_clause = None
    for line in (directory / (stem + '.lrat')).read_text().splitlines():
        values = list(map(int, line.split()))
        zero = values.index(0)
        index, clause, hints = values[0], values[1:zero], values[zero + 1:-1]
        require(values[-1] == 0 and index > 0 and index not in database,
                'LRAT clause identity or terminator')
        require(all(0 < abs(x) <= variables for x in clause), 'LRAT literal range')
        require(all(h > 0 and h in database for h in hints), 'Unknown LRAT hint')
        assignment, conflict = {}, False
        for literal in clause:
            var, truth = abs(literal), literal < 0
            if var in assignment and assignment[var] != truth:
                conflict = True
                break
            assignment[var] = truth
        if not conflict:
            for hint in hints:
                unknown = []
                for literal in database[hint]:
                    if abs(literal) not in assignment:
                        unknown.append(literal)
                    else:
                        require(assignment[abs(literal)] != (literal > 0), 'Satisfied RUP hint')
                require(len(unknown) <= 1, 'Non-unit RUP hint')
                if not unknown:
                    conflict = True
                    break
                assignment[abs(unknown[0])] = unknown[0] > 0
        require(conflict, 'RUP step has no contradiction')
        database[index] = clause
        steps += 1
        last_clause = clause
    require(steps > 0 and last_clause == [], 'Missing final empty clause')
    return {'variables': variables, 'clauses': count, 'rup_steps': steps,
            'source_cup_clauses': sum(c['kind'] == 'source_cup' for c in meta['clauses'])}


def check():
    manifest = preflight()
    exporter_path = ROOT / 'scripts/export_omission_coupled_rank.py'
    spec = importlib.util.spec_from_file_location('rank_exporter', exporter_path)
    exporter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)
    proofs, previous_supports = {}, []
    for certificate in manifest['certificates']:
        stem, module = certificate['stem'], certificate['module']
        proof = check_rup(stem=stem)
        require(proof == certificate['proof_counts'], 'Certificate dimensions changed: ' + stem)
        with tempfile.TemporaryDirectory() as tmp:
            generated = Path(tmp) / (module + '.lean')
            exporter.export(HERE / (stem + '.json'), generated, certificate['namespace'],
                            HERE.name, stem)
            text = generated.read_text().replace('../../experiments/' + HERE.name + '/', '')
            require(text == (HERE / (module + '.lean')).read_text(),
                    'Generated Lean semantics changed: ' + module)
        witness = json.loads((HERE / certificate['countermodel']).read_text())
        raw = gzip.decompress((ROOT / witness['source']).read_bytes())
        require(hashlib.sha256(raw).hexdigest() == witness['source_sha256'], 'Countermodel source identity')
        catalog = json.loads(raw)
        meta = json.loads((HERE / (stem + '.json')).read_text())
        require(witness['support'] == meta['support'], 'Countermodel core identity')
        holes = set(witness['holes'])
        require(len(holes) == len(witness['holes']) == witness['holes_count'] == 33,
                'Countermodel hole count')
        require(all(type(i) is int and 0 <= i < 154 for i in holes), 'Countermodel state range')
        require(0 not in holes and not holes.intersection(meta['support']),
                'Countermodel does not violate the new row with zero occupied')
        require(len(catalog['constraints']) == witness['previous_rows'] == 2646, 'Previous row count')
        require(all(len(holes.intersection(row['support'])) >= row['rhs']
                    for row in catalog['constraints']), 'Countermodel violates a previous row')
        require(witness.get('previous_supports', []) == previous_supports,
                'Earlier support identity mismatch')
        require(all(holes.intersection(support) for support in previous_supports),
                'Countermodel violates an earlier row in this batch')
        require(proof['source_cup_clauses'] == witness['retained_source_cup_clauses'],
                'Unexpected source-cup clause count')
        if stem == 'core-one':
            require(all(catalog['states'][s][0] >= 5 for s in meta['support']),
                    'Rank-tautology scope changed')
        proofs[stem] = proof
        previous_supports.append(meta['support'])
    return {'complete': True,
            'scope': 'Exact finite proof replay and regenerated source; kernel status recorded separately.',
            'manifest_sha256': sha(HERE / 'manifest.json'),
            'countermodel_holes': 33, 'countermodel_rows': 2646,
            'proofs': proofs, 'ordered_supports': previous_supports}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
