import ErdosSzekeres.Omission.PopulationBounds

/-!
DRAFT (track P307V, 18 Nov 2026; NOT compiled here -- the track's 1.5 GB memory budget does not fit a Lean run).
The last composition step of an ES(8) ≤ 307 statement, written exactly as
`archive/es7-2026-10-19/results/ES8SLACK/review/C1_certificates/Composition311.lean` does it for 311
(188 + 121 + 2 = 311 there; 187 + 118 + 2 = 307 here).  Both population bounds stay explicit hypotheses:
`BalancedBound 187` is `Compact310.balanced_population_187` (Final310Compact.lean); `ResidualBound 118` is what the
budget-35 chain of ROUTE307_1116 §1.3 supplies (h(C) ≥ 36 for every nonempty residual configuration, with
`holes_sum_add_population`: n + h(C) = 154), and it is NOT a Lean theorem.
Compile from the repository root, e.g. `lake env lean <this file>`; expect no errors and, for both theorems,
`#print axioms` listing only propext, Classical.choice, Quot.sound.
-/

open ErdosSzekeres ErdosSzekeres.Omission

theorem composition_307 (hB : Partition.BalancedBound 187)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 307 8 :=
  Partition.forces_of_population_bounds (by omega) hB hR

theorem avoiding_306 (hB : Partition.BalancedBound 187)
    (hR : Partition.ResidualBound 118) (S : Finset Point) (gp : GeneralPosition S)
    (avoid : ¬ HasConvexNGon 8 S) : S.card ≤ 306 :=
  Partition.avoiding_card_le_of_population_bounds (by omega) hB hR S gp avoid

#print axioms composition_307
#print axioms avoiding_306
