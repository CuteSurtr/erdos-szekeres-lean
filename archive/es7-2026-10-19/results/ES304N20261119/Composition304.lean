import ErdosSzekeres.Omission.PopulationBounds

/-!
ES304N20261119: the last composition step of ES(8) ≤ 304 (184 + 118 + 2 = 304), in the form of
ES305N20261119/Composition305.lean. Both population bounds are explicit hypotheses:
- `BalancedBound 184`: the balanced budget-67 EXACT TREE on the 3,131 Lean catalog rows plus the Z-row; in Lean,
  `OmissionBalancedZ.balanced_bound_of_hole_budget_z` (ES305N20261119/BalancedBudgetsZ.lean) turns
  `ExcludesHoleBudgetZ 67` (the tree) and `N66Bound 55` into it. The tree itself is NOT a Lean theorem.
- `ResidualBound 118`: the residual half of the ES(8) ≤ 307 chain (ES307N20261118); NOT a Lean theorem.
-/

open ErdosSzekeres ErdosSzekeres.Omission

theorem composition_304 (hB : Partition.BalancedBound 184)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 304 8 :=
  Partition.forces_of_population_bounds (by omega) hB hR

theorem avoiding_303 (hB : Partition.BalancedBound 184)
    (hR : Partition.ResidualBound 118) (S : Finset Point) (gp : GeneralPosition S)
    (avoid : ¬ HasConvexNGon 8 S) : S.card ≤ 303 :=
  Partition.avoiding_card_le_of_population_bounds (by omega) hB hR S gp avoid

#print axioms composition_304
#print axioms avoiding_303
