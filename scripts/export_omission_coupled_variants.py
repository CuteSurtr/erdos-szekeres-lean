#!/usr/bin/env python3
"""Emit independent kernel checks for the finite compatible-support family."""
import argparse
import json
from pathlib import Path


def export(source, output, template='CoupledTemplate', namespace='CoupledVariants'):
    supports = json.loads(source.read_text())['supports']
    count = len(supports)
    assert all(len(s) == len(set(s)) == 13 for s in supports)
    assert len({frozenset(s) for s in supports}) == count
    text = '''import ErdosSzekeres.Omission.CoupledTemplateGeometry
import ErdosSzekeres.Omission.CoupledTemplateCheck

/-! Literal support variants of the same coupled obstruction. Each variant
passes the entire frozen template in Lean; no new SAT result is assumed. -/
namespace ErdosSzekeres.Omission.CoupledVariants
open CoupledTemplate
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

'''
    for i, support in enumerate(supports):
        text += f'private def state{i:03d} : Fin 13 → Fin 154 := ![' + ', '.join(map(str, support)) + ']\n\n'
    text += f'def maps : Fin {count} → Fin 13 → Fin 154 := !['
    text += ', '.join(f'state{i:03d}' for i in range(count)) + ']\n\n'
    text += f'def support (r : Fin {count}) : Finset (Fin 154) := Finset.univ.image (maps r)\n\n'
    for i in range(count):
        text += f'private theorem checked{i:03d} : Function.Injective state{i:03d} ∧ Compatible state{i:03d} := by\n  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩\n\n'
        if i % 10 == 9 or i == count - 1:
            text += f'#check checked{i:03d}\n\n'
    text += f'theorem checked : ∀ r : Fin {count}, Function.Injective (maps r) ∧ Compatible (maps r) := by\n  intro r\n  fin_cases r\n'
    for i in range(count):
        text += f'  · exact checked{i:03d}\n'
    text += f'''
/-- All {count} rows have demand one in every actual residual configuration. -/
theorem all_rows {{n : ℕ}} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin {count}, 1 ≤ (support r \\ c.residualOccupied noCap noOctagon noJunction).card := by
  intro r
  exact CoupledTemplate.hole_bound (maps r) (checked r).1 (checked r).2
    c noCap noOctagon noJunction

#print axioms checked
#print axioms all_rows
end ErdosSzekeres.Omission.CoupledVariants
'''
    text = text.replace('CoupledTemplate', template).replace('CoupledVariants', namespace)
    output.write_text(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('experiments/omission-coupled-core-2026-10-10/template-variants.json'))
    parser.add_argument('--output', type=Path, default=Path('ErdosSzekeres/Omission/CoupledVariants.lean'))
    parser.add_argument('--template', default='CoupledTemplate')
    parser.add_argument('--namespace', default='CoupledVariants')
    args = parser.parse_args()
    export(args.source, args.output, args.template, args.namespace)
