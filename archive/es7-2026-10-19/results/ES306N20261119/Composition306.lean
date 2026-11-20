import ErdosSzekeres.Omission.PopulationBounds

/-!
ES306N20261119: the last composition step of an ES(8) ≤ 306 statement, in the form of
`LO33N20261113/budget34/VERIFY307/tools/Composition307.lean` (187 + 118 + 2 = 307 there; 186 + 118 + 2 = 306 here).

Both population bounds stay explicit hypotheses.
- `BalancedBound 186` is what `OmissionBalanced.balanced_bound_of_hole_budget (budget := 65)`
  (experiments/omission-global-assembly-2026-10-10/BalancedBudgets.lean) gives from `ExcludesHoleBudget 65`, the
  statement the balanced budget-65 campaign of this record establishes as an EXACT TREE (two implementations; not a
  Lean theorem).
- `ResidualBound 118` is the residual half of the ES(8) ≤ 307 chain (ES307N20261118; h(C) ≥ 36); NOT a Lean theorem.

Compile from the repository root: `lake env lean <this file>`; `#print axioms` must list only propext,
Classical.choice and Quot.sound.
-/

open ErdosSzekeres ErdosSzekeres.Omission

theorem composition_306 (hB : Partition.BalancedBound 186)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 306 8 :=
  Partition.forces_of_population_bounds (by omega) hB hR

theorem avoiding_305 (hB : Partition.BalancedBound 186)
    (hR : Partition.ResidualBound 118) (S : Finset Point) (gp : GeneralPosition S)
    (avoid : ¬ HasConvexNGon 8 S) : S.card ≤ 305 :=
  Partition.avoiding_card_le_of_population_bounds (by omega) hB hR S gp avoid

#print axioms composition_306
#print axioms avoiding_305
