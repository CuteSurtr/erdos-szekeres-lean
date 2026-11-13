import BalancedCover61Proof.Root
import ResidualCover31Proof.Root
import BalancedCover61Bridge
import ResidualCover31V2Bridge

/-!
Closed assembly through the two rounded-cover certificates. Its status is
established only by a complete successful final assembly and axiom audit.
-/

namespace ErdosSzekeres.Omission

theorem balanced_population_190 : Partition.BalancedBound 190 :=
  OmissionBalanced.balanced_bound_of_hole_budget (budget := 61)
    (OmissionBalancedCover61.exclusion_transfer OmissionBalancedCover61.excludes_budget)

theorem residual_population_122 : Partition.ResidualBound 122 :=
  OmissionResidual.residual_bound_of_hole_budget (budget := 31)
    (OmissionResidualCover31.exclusion_transfer OmissionResidualCover31.excludes_budget)

theorem forces_convex_octagon_314 : ForcesConvexNGon 314 8 :=
  Partition.forces_of_population_bounds (by omega) balanced_population_190 residual_population_122

theorem convex_octagon_of_card_ge_314 (S : Finset (Fin 2 → ℝ))
    (gp : GeneralPosition S) (size : 314 ≤ S.card) :
    ∃ T : Finset (Fin 2 → ℝ), T ⊆ S ∧ T.card = 8 ∧
      ConvexIndependent ℝ (fun p : (T : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  forces_convex_octagon_314 S gp size

#print axioms balanced_population_190
#print axioms residual_population_122
#print axioms forces_convex_octagon_314
#print axioms convex_octagon_of_card_ge_314
#check @forces_convex_octagon_314
#check @convex_octagon_of_card_ge_314

end ErdosSzekeres.Omission
