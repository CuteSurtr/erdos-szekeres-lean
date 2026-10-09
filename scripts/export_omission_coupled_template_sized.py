#!/usr/bin/env python3
"""Generalize a checked sized core to compatible supports of the same size.

Only state-dependent tests vary; every chronological/rank/packet/convex clause
and the same literal LRAT proof are retained. The exporter is untrusted.
"""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, default=Path('experiments/omission-coupled-core-2026-10-10/core13.json'))
parser.add_argument('--core', type=Path, default=Path('ErdosSzekeres/Omission/CoupledCore13.lean'))
parser.add_argument('--namespace', default='CoupledTemplate')
parser.add_argument('--output', type=Path, default=Path('ErdosSzekeres/Omission/CoupledTemplate.lean'))
args = parser.parse_args()
data = json.loads(args.source.read_text())
original = args.core.read_text()
count = len(data['clauses'])
size = len(data['support'])
if not 3 <= size <= 154 or len(set(data['support'])) != size:
    raise ValueError('Expected 3–154 distinct residual states')
empty, domain, positive = [], [], []
for c in data['clauses']:
    q = c['detail']
    if c['kind'] == 'empty_direction':
        empty.append(tuple(q))
    elif c['kind'] == 'domain':
        domain.append(tuple(q))
    elif c['kind'] == 'fixed_sign':
        positive.append(tuple(q[:3] if q[3] else [q[0], q[2], q[1]]))

def literal(xs):
    return '[' + ', '.join('(' + ', '.join(map(str, q)) + ')' for q in xs) + ']'

text = '''import ErdosSzekeres.Omission.CoupledCore13

/-! The frozen 407-clause proof applies to any literal support satisfying
its finite state-dependent prerequisites. No fresh SAT result is assumed. -/
namespace ErdosSzekeres.Omission.CoupledTemplate
open Coupled CoupledCore13
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

'''
text += 'def emptyTests : List (Fin 13 × Fin 13) := ' + literal(empty) + '\n\n'
text += 'def domainTests : List (Fin 13 × Fin 13 × ℕ × ℕ) := ' + literal(domain) + '\n\n'
text += 'def positiveTests : List (Fin 13 × Fin 13 × Fin 13) := ' + literal(positive) + '\n\n'
text += '''def Compatible (σ : Fin 13 → Fin 154) : Prop :=
  (∀ t ∈ emptyTests, emptyCheck σ t.1 t.2 = true) ∧
  (∀ t ∈ domainTests, ¬Allowed σ t.1 t.2.1 (t.2.2.1, t.2.2.2)) ∧
  (∀ t ∈ positiveTests, CycleSigns.CheckTriple ResidualDomains.computedTable
    (σ t.1) (σ t.2.1) (σ t.2.2) = true)

instance (σ : Fin 13 → Fin 154) : Decidable (Compatible σ) := by
  unfold Compatible
  infer_instance

'''
start = original.index('private def clause000')
end = original.index('variable {n : ℕ}')
text += original[start:end]
text += 'variable {n : ℕ} {σ : Fin 13 → Fin 154} (C : Context 13 n σ) (compatible : Compatible σ)\ninclude compatible\n\n'
for i, c in enumerate(data['clauses']):
    begin = original.index(f'-- Clause {i + 1}:')
    end = original.index('\n\n', begin) + 2
    proof = original[begin:end]
    kind, q = c['kind'], c['detail']
    if kind in ['empty_direction', 'domain', 'fixed_sign']:
        if kind == 'empty_direction':
            term = 'compatible.1 (' + ', '.join(map(str, q)) + ') (by decide +kernel)'
        elif kind == 'domain':
            term = 'compatible.2.1 (' + ', '.join(map(str, q)) + ') (by decide +kernel)'
        else:
            t = q[:3] if q[3] else [q[0], q[2], q[1]]
            term = 'compatible.2.2 (' + ', '.join(map(str, t)) + ') (by decide +kernel)'
        proof = proof.replace('(by decide +kernel)) (by decide +kernel)', '(' + term + ')) (by decide +kernel)')
    if kind not in ['empty_direction', 'domain', 'fixed_sign']:
        proof = proof.replace('private theorem', 'omit compatible in\nprivate theorem')
    text += proof
text += 'private theorem all_sound : List.Forall (fun cl => C.clause (decodeClause atoms cl)) clauses := by\n  exact '
text += ''.join(f'And.intro (sound{i:03d} C' + (' compatible' if data['clauses'][i]['kind'] in ['empty_direction', 'domain', 'fixed_sign'] else '') + ') (' for i in range(count - 1))
text += f'sound{count - 1:03d} C' + (' compatible' if data['clauses'][-1]['kind'] in ['empty_direction', 'domain', 'fixed_sign'] else '') + ')' * (count - 1) + '\n\n'
text += '''theorem context_impossible : False := by
  have h : (C.valuation atoms).satisfies_fmla CoupledCore13.cnf_refutation.formula := by
    rw [formula_eq]
    constructor
    intro cl hc
    exact C.satisfies_of_clause atoms cl ((List.forall_iff_forall_mem.mp (all_sound C compatible)) cl hc)
  exact CoupledCore13.cnf_refutation (C.valuation atoms) h

#print axioms context_impossible
end ErdosSzekeres.Omission.CoupledTemplate
'''
# Context itself does not occur in the proposition False; include it explicitly.
text = text.replace('theorem context_impossible : False', 'theorem context_impossible (C : Context 13 n σ) : False')
text = text.replace('CoupledCore13', args.core.stem).replace('CoupledTemplate', args.namespace)
text = text.replace('frozen 407-clause', f'frozen {count}-clause')
text = text.replace('Fin 13', f'Fin {size}').replace('Context 13', f'Context {size}')
args.output.write_text(text)
