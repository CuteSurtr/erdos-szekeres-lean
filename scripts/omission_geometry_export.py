#!/usr/bin/env python3
"""Export kernel-only geometric checks for every balanced omission row.

The literal cycle orders are CC BY 4.0 data from Michael Schroeder's version-1
archive, DOI 10.5281/zenodo.22842891. No upstream native-evaluation proof or box
table is imported. Bounding-box correctness and geometric row soundness are
proved in ErdosSzekeres.Omission; the exporter is untrusted.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cycles_from_source(path):
    text = path.read_text()
    start = text.index('def cycles ')
    start = text.index('"', start) + 1
    end = text.index('"', start)
    raw = text[start:end].replace('\\n', '\n')
    if re.fullmatch(r'[0-9]+(?: [0-9]+)*(?:\n[0-9]+(?: [0-9]+)*)*', raw) is None:
        raise ValueError('Noncanonical cycle data')
    return [[int(x) for x in row.split()] for row in raw.splitlines()]


def export(archive, output, chunk=32):
    if output.exists():
        raise FileExistsError(output)
    if type(chunk) is not int or chunk < 1:
        raise ValueError('Positive chunk size required')
    row_source = archive / 'certificates/balanced.json'
    cycle_source = archive / 'formal/sources/ES8CycleData.lean'
    data = json.loads(row_source.read_text())
    cycles = cycles_from_source(cycle_source)
    if len(data['states']) != 252 or len(cycles) != 2685 or len(data['cuts']) != 2685:
        raise ValueError('Unexpected balanced system dimensions')
    for ids, support in zip(cycles, data['cuts']):
        if len(ids) != len(set(ids)) or set(ids) != set(support):
            raise ValueError('Cycle/support mismatch')
        if not 8 <= len(ids) <= 10 or not all(0 <= i < 252 for i in ids):
            raise ValueError('Invalid cycle indices or length')
    output.mkdir(parents=True)
    modules = []
    for start in range(0, len(cycles), chunk):
        end = min(start + chunk, len(cycles))
        name = f'Geometry{start:05d}'
        modules.append({'module': name, 'start': start, 'end': end})
        lines = ['import Catalog', 'import ErdosSzekeres.Omission.CycleGeometry',
                 'open ErdosSzekeres ErdosSzekeres.Omission',
                 f'namespace OmissionBalanced.{name}',
                 'set_option maxRecDepth 100000',
                 'set_option maxHeartbeats 10000000',
                 'def cycles : Array (List (Fin 252)) := #[']
        lines += ['  [' + ', '.join(map(str, ids)) + ']' + (',' if j + 1 < end else '')
                  for j, ids in enumerate(cycles[start:end], start)]
        lines += [']', f'def cycle (r : Fin 2685) := cycles[r.val - {start}]!',
                  'theorem checked : ∀ r : Fin 2685,',
                  f'    {start} ≤ r.val → r.val < {end} →',
                  '    CycleValid (cycle r) ∧ (cycle r).toFinset = support r ∧',
                  '      (cycle r).length - 7 = demand r := by',
                  '  decide +kernel',
                  'theorem row_bound {n : ℕ} (c : Configuration n)',
                  '    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)',
                  '    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))',
                  f'    (r : Fin 2685) (hlo : {start} ≤ r.val) (hhi : r.val < {end}) :',
                  '    demand r ≤ (support r \\ c.occupied noCap noCup).card := by',
                  '  obtain ⟨valid, hs, hd⟩ := checked r hlo hhi',
                  '  simpa only [hs, hd] using',
                  '    c.list_cycle_hole_bound noCap noCup noOctagon (cycle r) valid',
                  '#print axioms row_bound', f'end OmissionBalanced.{name}']
        (output / f'{name}.lean').write_text('\n'.join(lines) + '\n')
    lines = ['import Root', 'import Occupancy', *(f"import {m['module']}" for m in modules),
             'open ErdosSzekeres ErdosSzekeres.Omission', 'namespace OmissionBalanced',
             'set_option maxRecDepth 100000', 'set_option maxHeartbeats 10000000',
             'theorem all_geometric_rows {n : ℕ} (c : Configuration n)',
             '    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)',
             '    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))',
             '    (r : Fin 2685) : demand r ≤ (support r \\ c.occupied noCap noCup).card := by',
             f'  have hblocks : r.val / {chunk} < {len(modules)} := by have := r.isLt; omega',
             f'  generalize hblock : r.val / {chunk} = block at hblocks',
             '  interval_cases block']
    lines += [f"  · exact {m['module']}.row_bound c noCap noCup noOctagon r (by omega) (by have := r.isLt; omega)"
              for m in modules]
    lines += ['theorem real_configuration_bound {n : ℕ} (c : Configuration n)',
              '    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)',
              '    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) : n ≤ 192 := by',
              '  have bound := occupied_card_le (c.occupied noCap noCup)',
              '    (all_geometric_rows c noCap noCup noOctagon)',
              '  simpa only [c.occupied_card noCap noCup] using bound',
              '#print axioms all_geometric_rows', '#print axioms real_configuration_bound',
              'end OmissionBalanced']
    (output / 'BalancedGeometry.lean').write_text('\n'.join(lines) + '\n')
    report = {'scope': 'Balanced real configurations avoiding 7-cups, 7-caps and convex octagons',
              'source_sha256': digest(row_source), 'cycle_source_sha256': digest(cycle_source),
              'exporter_sha256': digest(Path(__file__)), 'rows': 2685, 'chunk_size': chunk,
              'modules': modules, 'lean_checked': False,
              'files': {p.name: digest(p) for p in sorted(output.glob('*.lean'))}}
    (output / 'export.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--chunk', type=int, default=32)
    args = parser.parse_args()
    result = export(args.archive, args.output, args.chunk)
    print(json.dumps({'rows': result['rows'], 'blocks': len(result['modules']), 'lean_checked': False}))
