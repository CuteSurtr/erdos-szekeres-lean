#!/usr/bin/env python3
"""Emit ordinary clause implications from the exact coordinate predicates.

The fixed Boolean source and data are read-only dependencies. All arithmetic
premises in the generated source must subsequently pass Lean kernel reduction.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'lean'
rows = []
for line in (BASE / 'data/terminal15-original.cnf').read_text().splitlines():
    fields = line.split()
    if fields and fields[0] not in ('c', 'p'):
        values = list(map(int, fields))
        assert values[-1] == 0
        rows.append(values[:-1])
ids = json.loads((BASE / 'data/terminal15-core-DONE.json').read_text())['original_clause_ids']

source = '''import FiniteModel
import Terminal15Boolean

namespace Delta3.Balanced15

theorem not_three {P Q R : Prop} (h : P → Q → R → False) : ¬P ∨ ¬Q ∨ ¬R :=
  (Classical.em P).elim
    (fun hp => (Classical.em Q).elim
      (fun hq => Or.inr (Or.inr (fun hr => h hp hq hr)))
      (fun hq => Or.inr (Or.inl hq)))
    (fun hp => Or.inl hp)

/-- No chosen index set satisfies both exact finite determinant predicates.
This statement has no unformalized real-convexity hypothesis or conclusion. -/
theorem terminal_selection_contradiction (A : Index → Prop)
    (hT : TerminalSafe A) (hH : HitsSix A) : False := by
'''
for cid in ids:
    row = rows[cid - 1]
    if all(lit < 0 for lit in row):
        assert len(row) == 3
        a, b, c = [-lit - 1 for lit in row]
        assert 0 <= a < b < c < 15
        source += f'''  have c{cid:03} : ¬A {a} ∨ ¬A {b} ∨ ¬A {c} :=
    not_three fun ha hb hc => by
      have ht := hT {a} {b} {c} (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair {b} {c} = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
'''
    else:
        assert len(row) == 6 and all(lit > 0 for lit in row)
        subset = [lit - 1 for lit in row]
        assert subset == sorted(set(subset))
        clause = ' ∨ '.join(f'A {i}' for i in subset)
        args = ' '.join(map(str, subset))
        source += f'  have c{cid:03} : {clause} :=\n'
        source += f'    hH {args}\n      ' + ' '.join('(by decide +kernel)' for _ in range(6)) + '\n'
source += '  exact Delta3.Terminal15Boolean.core_unsat\n    '
source += ' '.join(f'(A {i})' for i in range(15)) + '\n    '
source += ' '.join(f'c{i:03}' for i in ids) + '\n\n'
source += '''theorem no_terminal_selection : ¬∃ A : Index → Prop, TerminalSafe A ∧ HitsSix A :=
  fun ⟨A, hT, hH⟩ => terminal_selection_contradiction A hT hH

theorem no_boolean_terminal_selection :
    ¬∃ A : Index → Bool, TerminalSafe (fun i => A i = true) ∧ HitsSix (fun i => A i = true) :=
  fun ⟨A, hT, hH⟩ => terminal_selection_contradiction (fun i => A i = true) hT hH

#print axioms not_three
#print axioms terminal_selection_contradiction
#print axioms no_terminal_selection
#print axioms no_boolean_terminal_selection

end Delta3.Balanced15
'''
target = Path('/home/jay/research/data/delta3-codex-20261113/extension/lean/geometry-generated')
target.mkdir(exist_ok=True)
(target / 'TerminalBridge.lean').write_text(source)
assert source == (ROOT / 'TerminalBridge.lean').read_text()
print(f'Generated {len(ids)} exact-coordinate clause implications.')
