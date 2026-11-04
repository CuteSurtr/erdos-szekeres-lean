# merged: distinct layers have distinct phases (even m), in one Lean file

The file is `Merged.lean` (SHA-256 `245b7d65…`). Lines 1–1147 are byte-identical to `LAYERLEAN/LayerLemma.lean`. Section
13 adds the even-m phase results of `orbit/OrbitConsistency.lean`, de-duplicated onto LayerLemma's definitions.
- **Checks.** The build is clean (exit 0, no messages) and there is no `sorry`, `admit` or `axiom`. The coordinator
  re-checked both independently.
- **Axioms.** Both new theorems depend only on [propext, Classical.choice, Quot.sound].

## Lean-checked

Both theorems assume m ≥ 2 and even, K ≤ 2m, c ∉ S, S invariant and in general position, no convex K-gon, and i ≠ j.
- **`phase_ne_of_distinct_layers`.** For `polar c r α ∈ hullVerts (peel S i)` and `polar c r' β ∈ hullVerts (peel S j)`
  with r, r' > 0, β − α is never an integer multiple of 2π/m.
- **`not_same_ray_of_distinct_layers`.** Points x and y of different layers never satisfy y − c = l·(ρ^k x − c) with
  l > 0.
- **Helpers.** `not_mem_hullVerts_peel_of_ne` (layers are disjoint) and `iterate_mem_hullVerts_peel` (layers are closed
  under ρ).

## Mutants

All three fail to compile:
- `i ≠ j` replaced by `i ≤ j`;
- `Even m` replaced by `0 < m`;
- the conclusion strengthened to multiples of π/m. This last statement is false in general.

## Open issues

`c ∉ S` is a hypothesis; it could be derived with `centre_not_mem_of_even`. No lemma here produces the polar form
from an arbitrary point (see `phase/exists_polar`).
