#!/usr/bin/env python3
"""Archive the small fixed-instance evidence and check its cross-file links."""
import csv
from fractions import Fraction as Q
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import shutil

HERE = Path(__file__).resolve().parent
WORK = Path('/home/jay/research/data/delta3-codex-20261113/extension')
resource.setrlimit(resource.RLIMIT_AS, (300 << 20, 300 << 20))
spec = importlib.util.spec_from_file_location('parent_geometry', HERE.parent / 'boundary/check_envelope.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cnf(path):
    rows = []
    for line in path.read_text().splitlines():
        if line.startswith('c') or not line.strip():
            continue
        if line.startswith('p'):
            _, _, nv, nc = line.split()
            continue
        row = [int(x) for x in line.split()]
        assert row[-1] == 0
        rows.append(row[:-1])
    assert int(nv) == 15 and len(rows) == int(nc)
    return rows


def main():
    target = HERE / 'terminal15'
    target.mkdir(exist_ok=False)
    data = target / 'data'
    data.mkdir()
    receipts = {}
    copies = {
        'original.json': WORK / 'realize15-a/witness.json',
        'balanced.json': WORK / 'balance15-a/witness.json',
        'balanced.points': WORK / 'balance15-a/witness.points',
        'membership.cnf': WORK / 'terminal15/witness.terminal.cnf',
        'membership.blrat': WORK / 'terminal15/fresh.blrat',
        'membership.cake.log': WORK / 'terminal15/cake.log',
        'membership-certificate.json': WORK / 'terminal15/certificate.json',
        'coordinate-audit.json': HERE / 'model15_audit/balanced/data/equivalence.json',
        'cup-certificates.json': HERE / 'envelope/cup_dominance/metric15/cup_minimum/data/certificates.json',
    }
    for name, source in copies.items():
        shutil.copyfile(source, data / name)
        receipts[name] = {'source': str(source), 'sha256': digest(source)}
    for folder, source in [
        ('core', WORK / 'terminal15/small-proof-a'),
        ('core-certificate', WORK / 'terminal15/core-cert-a'),
        ('figure', WORK / 'terminal15/figure-b')]:
        shutil.copytree(source, target / folder)
        for path in sorted(source.rglob('*')):
            if path.is_file():
                receipts[str(Path(folder) / path.relative_to(source))] = {
                    'source': str(path), 'sha256': digest(path)}
    P = json.loads((data / 'balanced.json').read_text())['P']
    old = json.loads((data / 'original.json').read_text())['P']
    assert len(P) == 15 and all(P[i][0] < P[i + 1][0] for i in range(14))
    determinants = [G.det(P, *t) for t in combinations(range(15), 3)]
    assert all(determinants)
    assert all((G.det(P, *t) > 0) == (G.det(old, *t) > 0)
               for t in combinations(range(15), 3))
    with (target / 'figure/plotted_points.csv').open() as stream:
        plotted = list(csv.DictReader(stream))
    assert [[int(row['x']), int(row['y'])] for row in plotted] == P
    A = [2, 3, 6, 9]
    assert G.maxima(P, range(15)) == (4, 6, 6)
    assert G.maxima(P, A)[0] < 4
    assert G.maxima(P, [i for i in range(15) if i not in A])[2] < 6
    certificates = json.loads((data / 'cup-certificates.json').read_text())
    supports = []
    for case in certificates['cases']:
        points = case['P']
        assert points == (P if case['name'] == 'balanced' else old)
        cap_triples = {t for t in combinations(A, 3) if G.det(points, *t) < 0}
        assert cap_triples == {tuple(c['selected_cap_triple']) for c in case['certificates']}
        for item in case['certificates']:
            fourcap = item['ambient_fourcap']
            assert all(G.det(points, *t) < 0 for t in combinations(fourcap, 3))
            assert all(G.det(points, *t) > 0 for t in combinations(item['cup_union'], 3))
            ell = G.line(points, item['ambient_tail_pair'])
            q = G.line(points, item['selected_tail_pair'])
            delta = [ell[i] - q[i] for i in range(2)]
            assert delta == [Q(item['slope_difference']), Q(item['intercept_difference'])]
            assert all(x > 0 for x in delta)
            supports.append({'case': case['name'], 'triple': item['selected_cap_triple'],
                             'slope_difference': str(delta[0]), 'height_difference': str(delta[1])})
    full = cnf(data / 'membership.cnf')
    core = cnf(target / 'core/core.cnf')
    core_meta = json.loads((target / 'core/DONE.json').read_text())
    ids = core_meta['original_clause_ids']
    assert core == [full[i - 1] for i in ids]
    models = json.loads((target / 'core/irredundancy_models.json').read_text())
    for omitted, row in zip(ids, core):
        model = models[str(omitted)]
        satisfies = lambda clause: any(model[str(abs(v))] == (v > 0) for v in clause)
        assert not satisfies(row)
        assert all(satisfies(other) for cid, other in zip(ids, core) if cid != omitted)
    for log in [data / 'membership.cake.log', target / 'core-certificate/cake.log']:
        assert 's VERIFIED UNSAT' in log.read_text().splitlines()
    output = {
        'label': 'COMPUTED parent cross-file replay; separate CERTIFIED and Lean proofs linked',
        'status': 'PASS', 'orientation_tests': 455, 'minimum_absolute_determinant': min(map(abs, determinants)),
        'maxima_cap_cup_gon': [4, 6, 6], 'protected_selection': A,
        'line_certificates': supports, 'full_cnf_clauses': len(full), 'core_clauses': len(core),
        'core_subset_verified': True, 'irredundancy_models_verified': len(models),
        'minimum_core_size_claimed': False, 'figure_coordinates_match': True,
        'source_sha256': digest(Path(__file__)), 'geometry_sha256': digest(HERE.parent / 'boundary/check_envelope.py'),
        'copied_inputs': receipts,
        'scope': 'Fixed geometry only. No global minimality or weak-Delta failure. Float plot carries no proof weight.'}
    (data / 'parent-cross-check.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ['status', 'orientation_tests', 'core_clauses', 'irredundancy_models_verified']}))


if __name__ == '__main__':
    main()
