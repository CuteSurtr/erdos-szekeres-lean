import BalancedCover61FusedProof.Root
import BalancedCover61FusedBridge
import Residual32Bridge2650.Rows

/-!
CONDITIONAL assembly: ES(8) ≤ 313 from the single arithmetic statement
`Excludes2650Zero 32`. This file does NOT prove ES(8) ≤ 313; the hypothesis is
an explicit argument of each final theorem and is not proved anywhere here.

The balanced side is the same as in the completed 314-point assembly
(`FinalCover314B61FusedR31Fused.lean`): the 61-hole balanced cover certificate
and its literal catalog bridge give population at most 251 - 61 = 190.
The residual side is `residual_bound_121_of_excludes`.
-/

open ErdosSzekeres ErdosSzekeres.Omission

namespace OmissionResidual32Bridge2650

/-- The balanced population bound of the completed 314 assembly, derived here
from the same imported certificate and bridge. -/
theorem balanced_population_190 : Partition.BalancedBound 190 :=
  OmissionBalanced.balanced_bound_of_hole_budget (budget := 61)
    (OmissionBalancedCover61Fused.exclusion_transfer OmissionBalancedCover61Fused.excludes_budget)

/-- CONDITIONAL: 313 points in general position force a convex octagon, provided
the 2,650-row catalog admits no 32-hole Boolean model with state zero occupied. -/
theorem forces_convex_octagon_313_of_excludes (h : Excludes2650Zero 32) :
    ForcesConvexNGon 313 8 :=
  Partition.forces_of_population_bounds (by omega) balanced_population_190
    (residual_bound_121_of_excludes h)

/-- CONDITIONAL: the same statement for an arbitrary finite real point set. -/
theorem convex_octagon_of_card_ge_313_of_excludes (h : Excludes2650Zero 32)
    (S : Finset (Fin 2 → ℝ)) (gp : GeneralPosition S) (size : 313 ≤ S.card) :
    ∃ T : Finset (Fin 2 → ℝ), T ⊆ S ∧ T.card = 8 ∧
      ConvexIndependent ℝ (fun p : (T : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  forces_convex_octagon_313_of_excludes h S gp size

/-- CONDITIONAL, in the exact root-node shape of the context exporter: a 32-hole
certificate for a catalog `support'`/`demand'` equal row by row to this one. -/
theorem forces_convex_octagon_313_of_node {support' : Fin 2650 → Finset (Fin 154)}
    {demand' : Fin 2650 → ℕ} (hs : ∀ r, support' r = support2650 r)
    (hd : ∀ r, demand' r = demand2650 r)
    (h : ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand' r ≤ ∑ i ∈ support' r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ (∅ : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 0 ∅) : Finset (Fin 154)), holes i = 0)) :
    ForcesConvexNGon 313 8 :=
  forces_convex_octagon_313_of_excludes (excludes2650Zero_of_node hs hd h)

#print axioms balanced_population_190
#print axioms all_rows_2650
#print axioms residual_bound_121_of_excludes
#print axioms forces_convex_octagon_313_of_excludes
#print axioms convex_octagon_of_card_ge_313_of_excludes
#print axioms forces_convex_octagon_313_of_node
#check @Excludes2650Zero
#check @all_rows_2650
#check @residual_bound_121_of_excludes
#check @forces_convex_octagon_313_of_excludes
#check @convex_octagon_of_card_ge_313_of_excludes
#check @excludes2650Zero_of_node
#check @forces_convex_octagon_313_of_node

-- Fully qualified statements, pinned by `check.py`.
set_option pp.fullNames true in
#check @Excludes2650Zero
set_option pp.fullNames true in
#check @residual_bound_121_of_excludes
set_option pp.fullNames true in
#check @forces_convex_octagon_313_of_excludes

end OmissionResidual32Bridge2650
