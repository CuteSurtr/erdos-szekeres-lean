#!/usr/bin/env python3
"""Export the 23 residual block checks and composition with the cycle rows.

Block data: Michael Schroeder, DOI 10.5281/zenodo.22842891, CC BY 4.0.
The parser accepts literal data only. Every mathematical check is repeated
inside Lean's kernel; no upstream evaluation proof is imported.
"""
import argparse
import json
from pathlib import Path
import re

from omission_geometry_export import digest


def parse_blocks(source):
    pattern = (r'\{ rowId := ([0-9]+), support := (\[[0-9, ]+\]), '
               r'thresholds := (\[[0-9, ]+\]), active := (\[[0-9,() ]+\]) \}')
    result = []
    for line in source.read_text().splitlines():
        if not line.startswith('{'):
            continue
        match = re.fullmatch(pattern + ',?', line)
        if not match:
            raise ValueError('Nonliteral block data')
        row, support, thresholds, active = match.groups()
        result.append({'row': int(row), 'support': json.loads(support),
                       'thresholds': json.loads(thresholds),
                       'active': json.loads(active.replace('(', '[').replace(')', ']'))})
    if [b['row'] for b in result] != [973, *range(1165, 1187)]:
        raise ValueError('Incomplete or misordered block rows')
    return result


def export(archive, output, catalog_module="Catalog"):
    if re.fullmatch(r"(?:[A-Za-z][A-Za-z0-9_]*\.)?Catalog", catalog_module) is None:
        raise ValueError("Invalid arithmetic catalog module")
    if output.exists():
        raise FileExistsError(output)
    source = archive / 'formal/sources/ES8BlockData.lean'
    row_source = archive / 'certificates/residual.json'
    blocks = parse_blocks(source)
    rows = json.loads(row_source.read_text())['constraints']
    for b in blocks:
        if (len(set(b['support'])) != len(b['support'])
                or set(b['support']) != set(rows[b['row']]['support'])
                or len(b['support']) - 22 != rows[b['row']]['rhs']):
            raise ValueError('Block/support/demand mismatch')
    output.mkdir(parents=True)
    hypotheses = ['    (noCap : ¬ c.HasCap 6)',
                  '    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))',
                  '    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))']
    modules = []
    for b in blocks:
        name = f"ResidualBlock{b['row']:05d}"
        modules.append({'module': name, 'row': b['row']})
        literal = ('{ rowId := ' + str(b['row']) + ', support := ' + str(b['support'])
                   + ', thresholds := ' + str(b['thresholds']) + ', active := ['
                   + ', '.join(f'({x},{y})' for x, y in b['active']) + '] }')
        lines = [f'import {catalog_module}', 'import ErdosSzekeres.Omission.BlockGeometry',
                 'open ErdosSzekeres ErdosSzekeres.Omission BlockCompression',
                 f'namespace OmissionResidual.{name}',
                 'set_option maxRecDepth 100000', 'set_option maxHeartbeats 100000000',
                 f'def block : Block := {literal}', f'def row : Fin 1187 := {b["row"]}',
                 'theorem checked : pairsOK block = true ∧ growthOK block = true ∧',
                 '    block.support.toFinset = (support row).image Fin.val ∧',
                 '    demand row = (support row).card - 22 := by decide +kernel',
                 'theorem row_bound {n : ℕ} (c : Configuration n)', *hypotheses,
                 '    : demand row ≤ (support row \\ c.residualOccupied noCap noOctagon noJunction).card := by',
                 '  obtain ⟨pairs, growth, hs, hd⟩ := checked',
                 '  rw [hd]',
                 '  exact BlockGeometry.block_hole_bound c noCap noOctagon noJunction block pairs growth (support row) hs',
                 '#print axioms row_bound', f'end OmissionResidual.{name}']
        (output / f'{name}.lean').write_text('\n'.join(lines) + '\n')
    lines = ['import ResidualGeometry', *(f"import {m['module']}" for m in modules),
             'open ErdosSzekeres ErdosSzekeres.Omission', 'namespace OmissionResidual',
             '/-- Every residual row is necessary for an actual residual configuration.',
             'This theorem does not assert an arithmetic population bound. -/',
             'theorem all_geometric_rows {n : ℕ} (c : Configuration n)', *hypotheses,
             '    (r : Fin 1187) : demand r ≤ (support r \\ c.residualOccupied noCap noOctagon noJunction).card := by',
             '  by_cases h : r.val = 973',
             '  · have he : r = ResidualBlock00973.row := Fin.ext h',
             '    subst r; exact ResidualBlock00973.row_bound c noCap noOctagon noJunction',
             '  · by_cases hi : r.val < 1165',
             '    · exact all_nonblock_rows c noCap noOctagon noJunction r hi h',
             '    · have lo : 1165 ≤ r.val := by omega',
             '      have high := r.isLt',
             '      generalize he : r.val = j at lo high', '      interval_cases j']
    for m in modules[1:]:
        lines += [f"      · have hr : r = {m['module']}.row := Fin.ext he",
                  f"        subst r; exact {m['module']}.row_bound c noCap noOctagon noJunction"]
    lines += ['#print axioms all_geometric_rows', 'end OmissionResidual']
    (output / 'ResidualAllGeometry.lean').write_text('\n'.join(lines) + '\n')
    report = {'scope': 'All 1187 residual geometric rows; no arithmetic population bound',
              'source_sha256': digest(source), 'row_source_sha256': digest(row_source),
              'exporter_sha256': digest(Path(__file__)), 'catalog_module': catalog_module, 'block_rows': 23, 'total_rows': 1187,
              'modules': modules, 'lean_checked': False,
              'files': {p.name: digest(p) for p in sorted(output.glob('*.lean'))}}
    (output / 'export.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--catalog-module', default='Catalog')
    args = parser.parse_args()
    result = export(args.archive, args.output, args.catalog_module)
    print(json.dumps({'block_rows': result['block_rows'], 'lean_checked': False}))
