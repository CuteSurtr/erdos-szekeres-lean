import BalancedPopulation
import Residual124.Root
import Residual124Bridge

/-!
Closed fallback assembly, pending its complete prerequisite checks. The
original 29-hole exclusion gives population 124; the improved balanced
population 192 then gives the ordinary global octagon threshold 318.
-/

namespace ErdosSzekeres.Omission

theorem residual_population_124 : Partition.ResidualBound 124 :=
  OmissionResidual.residual_bound_of_hole_budget (budget := 29)
    (OmissionResidual124.exclusion_transfer OmissionResidual124.excludes_budget)

theorem forces_convex_octagon_318 : ForcesConvexNGon 318 8 :=
  Partition.forces_318_of_population_bounds balanced_population_192 residual_population_124

theorem convex_octagon_of_card_ge_318 (S : Finset (Fin 2 → ℝ))
    (gp : GeneralPosition S) (size : 318 ≤ S.card) :
    ∃ T : Finset (Fin 2 → ℝ), T ⊆ S ∧ T.card = 8 ∧
      ConvexIndependent ℝ (fun p : (T : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  forces_convex_octagon_318 S gp size

#print axioms balanced_population_192
#print axioms residual_population_124
#print axioms forces_convex_octagon_318
#print axioms convex_octagon_of_card_ge_318
#check @forces_convex_octagon_318
#check @convex_octagon_of_card_ge_318

end ErdosSzekeres.Omission
