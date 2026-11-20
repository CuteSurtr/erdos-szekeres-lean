import ErdosSzekeres.Omission.PopulationBounds

/-!
ES305N20261119: the last composition step of ES(8) ≤ 305 (185 + 118 + 2 = 305), in the form of
ES306N20261119/Composition306.lean. Both population bounds are explicit hypotheses:
- `BalancedBound 185`: the balanced budget-66 EXACT TREE on the 3,131 Lean catalog rows plus the Z-row
  (Lemma Z + N66 ≤ 55), see README §3; NOT a Lean theorem.
- `ResidualBound 118`: the residual half of the ES(8) ≤ 307 chain (ES307N20261118); NOT a Lean theorem.
-/

open ErdosSzekeres ErdosSzekeres.Omission

theorem composition_305 (hB : Partition.BalancedBound 185)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 305 8 :=
  Partition.forces_of_population_bounds (by omega) hB hR

theorem avoiding_304 (hB : Partition.BalancedBound 185)
    (hR : Partition.ResidualBound 118) (S : Finset Point) (gp : GeneralPosition S)
    (avoid : ¬ HasConvexNGon 8 S) : S.card ≤ 304 :=
  Partition.avoiding_card_le_of_population_bounds (by omega) hB hR S gp avoid

#print axioms composition_305
#print axioms avoiding_304
