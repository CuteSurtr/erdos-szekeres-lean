#!/usr/bin/env python3
"""Export kernel proofs for the 1164 cycle rows of the residual system.

Michael Schroeder's version-1 cycle data (DOI 10.5281/zenodo.22842891)
is CC BY 4.0. The 23 noncycle rows are explicitly excluded. This exporter
is untrusted: Lean checks signs, support equality and demand for every row.
"""
import argparse
import json
from pathlib import Path
import re

from omission_geometry_export import cycles_from_source, digest


def export(archive, output, chunk=32, catalog_module="Catalog"):
    if re.fullmatch(r"(?:[A-Za-z][A-Za-z0-9_]*\.)?Catalog", catalog_module) is None:
        raise ValueError("Invalid arithmetic catalog module")
    if output.exists():
        raise FileExistsError(output)
    if type(chunk) is not int or chunk < 1:
        raise ValueError('Positive chunk size required')
    row_source = archive / 'certificates/residual.json'
    cycle_source = archive / 'formal/sources/ES8ResidualCycleData.lean'
    data = json.loads(row_source.read_text())
    cycles = cycles_from_source(cycle_source)
    match = re.search(r'def cycleRows[^\n]*:= \[([0-9, ]+)\]', cycle_source.read_text())
    if not match:
        raise ValueError('Missing canonical cycle-row indices')
    rows = [int(x) for x in match[1].split(',')]
    expected_rows = [i if i < 973 else i + 1 for i in range(1164)]
    if (len(data['states']) != 154 or len(data['constraints']) != 1187
            or len(cycles) != 1164 or rows != expected_rows):
        raise ValueError('Unexpected residual system dimensions or row ordering')
    for ids, r in zip(cycles, rows):
        row = data['constraints'][r]
        if (len(ids) != len(set(ids)) or set(ids) != set(row['support'])
                or len(ids) - 7 != row['rhs']):
            raise ValueError('Cycle/support/demand mismatch')
        if not 8 <= len(ids) <= 10 or not all(0 <= i < 154 for i in ids):
            raise ValueError('Invalid cycle indices or length')
    output.mkdir(parents=True)
    preamble = [f'import {catalog_module}', 'import ErdosSzekeres.Omission.ResidualCycleGeometry',
                'open ErdosSzekeres ErdosSzekeres.Omission',
                'namespace OmissionResidual',
                'set_option maxRecDepth 100000', 'set_option maxHeartbeats 10000000']
    base = preamble + [
        '/-- Cycle rows omit row 973 and the final 22 block rows. -/',
        'def cycleRow (i : Fin 1164) : Fin 1187 :=',
        '  ⟨if i.val < 973 then i.val else i.val + 1, by split <;> have := i.isLt <;> omega⟩',
        'theorem cycleRow_coverage (r : Fin 1187) (hi : r.val < 1165)',
        '    (skip : r.val ≠ 973) : ∃ i : Fin 1164, cycleRow i = r := by',
        '  by_cases h : r.val < 973',
        '  · refine ⟨⟨r.val, by omega⟩, ?_⟩',
        '    apply Fin.ext; simp [cycleRow, h]',
        '  · refine ⟨⟨r.val - 1, by omega⟩, ?_⟩',
        '    apply Fin.ext; simp only [cycleRow]; split <;> omega',
        'end OmissionResidual']
    (output / 'ResidualCycleIndex.lean').write_text('\n'.join(base) + '\n')
    hypotheses = [
        '    (noCap : ¬ c.HasCap 6)',
        '    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))',
        '    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))']
    modules = []
    for start in range(0, len(cycles), chunk):
        end = min(start + chunk, len(cycles))
        name = f'ResidualGeometry{start:05d}'
        modules.append({'module': name, 'start': start, 'end': end})
        lines = ['import ResidualCycleIndex', *preamble[2:], f'namespace {name}',
                 'def cycles : Array (List (Fin 154)) := #[']
        lines += ['  [' + ', '.join(map(str, ids)) + ']' + (',' if j + 1 < end else '')
                  for j, ids in enumerate(cycles[start:end], start)]
        lines += [']', f'def cycle (i : Fin 1164) := cycles[i.val - {start}]!',
                  'theorem checked : ∀ i : Fin 1164,',
                  f'    {start} ≤ i.val → i.val < {end} →',
                  '    ResidualCycleValid (cycle i) ∧ (cycle i).toFinset = support (cycleRow i) ∧',
                  '      (cycle i).length - 7 = demand (cycleRow i) := by',
                  '  decide +kernel',
                  'theorem row_bound {n : ℕ} (c : Configuration n)', *hypotheses,
                  f'    (i : Fin 1164) (hlo : {start} ≤ i.val) (hhi : i.val < {end}) :',
                  '    demand (cycleRow i) ≤ (support (cycleRow i) \\ c.residualOccupied noCap noOctagon noJunction).card := by',
                  '  obtain ⟨valid, hs, hd⟩ := checked i hlo hhi',
                  '  simpa only [hs, hd] using',
                  '    c.residual_list_cycle_hole_bound noCap noOctagon noJunction (cycle i) valid',
                  '#print axioms row_bound', f'end {name}', 'end OmissionResidual']
        (output / f'{name}.lean').write_text('\n'.join(lines) + '\n')
    lines = [*(f"import {m['module']}" for m in modules), *preamble[2:],
             'theorem all_cycle_rows {n : ℕ} (c : Configuration n)', *hypotheses,
             '    (i : Fin 1164) :',
             '    demand (cycleRow i) ≤ (support (cycleRow i) \\ c.residualOccupied noCap noOctagon noJunction).card := by',
             f'  have hb : i.val / {chunk} < {len(modules)} := by have := i.isLt; omega',
             f'  generalize he : i.val / {chunk} = block at hb', '  interval_cases block']
    lines += [f"  · exact {m['module']}.row_bound c noCap noOctagon noJunction i (by omega) (by have := i.isLt; omega)"
              for m in modules]
    lines += ['theorem all_nonblock_rows {n : ℕ} (c : Configuration n)', *hypotheses,
              '    (r : Fin 1187) (hi : r.val < 1165) (skip : r.val ≠ 973) :',
              '    demand r ≤ (support r \\ c.residualOccupied noCap noOctagon noJunction).card := by',
              '  obtain ⟨i, rfl⟩ := cycleRow_coverage r hi skip',
              '  exact all_cycle_rows c noCap noOctagon noJunction i',
              '#print axioms all_cycle_rows', '#print axioms all_nonblock_rows',
              'end OmissionResidual']
    (output / 'ResidualGeometry.lean').write_text('\n'.join(lines) + '\n')
    report = {'scope': '1164 residual cycle rows only; 23 block rows excluded; no population bound',
              'source_sha256': digest(row_source), 'cycle_source_sha256': digest(cycle_source),
              'exporter_sha256': digest(Path(__file__)), 'catalog_module': catalog_module, 'rows': 1164, 'total_rows': 1187,
              'excluded_rows': sorted(set(range(1187)) - set(rows)), 'chunk_size': chunk,
              'modules': modules, 'lean_checked': False,
              'files': {p.name: digest(p) for p in sorted(output.glob('*.lean'))}}
    (output / 'export.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--chunk', type=int, default=32)
    parser.add_argument('--catalog-module', default='Catalog')
    args = parser.parse_args()
    result = export(args.archive, args.output, args.chunk, args.catalog_module)
    print(json.dumps({'rows': result['rows'], 'blocks': len(result['modules']), 'lean_checked': False}))
