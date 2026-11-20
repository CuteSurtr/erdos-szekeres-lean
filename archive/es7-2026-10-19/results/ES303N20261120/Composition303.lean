import ErdosSzekeres.Omission.PopulationBounds

/-!
ES303N20261120 (draft, to be filed only if budget 68 passes both checks): the last composition step of
ES(8) ≤ 303 (183 + 118 + 2 = 303), in the form of ES304N20261119/Composition304.lean. Both population bounds are
explicit hypotheses:
- `BalancedBound 183`: the balanced budget-68 EXACT TREE (zero side only) on the 3,131 Lean catalog rows plus the
  Z-row and the Z*-row; in Lean, `balanced_bound_of_hole_budget_zzsf` (BalancedBudgetsZZs.lean, this record) turns
  `ExcludesHoleBudgetZZsF 68` (the tree) and `N66Bound 55` into it, and `composition_303_zzsf` there is the whole
  chain. The tree itself is NOT a Lean theorem.
- `ResidualBound 118`: the residual half of the ES(8) ≤ 307 chain (ES307N20261118); NOT a Lean theorem.
-/

open ErdosSzekeres ErdosSzekeres.Omission

theorem composition_303 (hB : Partition.BalancedBound 183)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 303 8 :=
  Partition.forces_of_population_bounds (by omega) hB hR

theorem avoiding_302 (hB : Partition.BalancedBound 183)
    (hR : Partition.ResidualBound 118) (S : Finset Point) (gp : GeneralPosition S)
    (avoid : ¬ HasConvexNGon 8 S) : S.card ≤ 302 :=
  Partition.avoiding_card_le_of_population_bounds (by omega) hB hR S gp avoid

#print axioms composition_303
#print axioms avoiding_302
