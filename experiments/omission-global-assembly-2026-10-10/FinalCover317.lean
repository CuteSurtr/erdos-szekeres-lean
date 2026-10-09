import BalancedCoverProof.Root
import ResidualCoverProof.Root
import BalancedCoverBridge
import ResidualCoverBridge

/-!
Closed assembly through the two rounded-cover certificates. Its status is
established only by a complete successful final assembly and axiom audit.
-/

namespace ErdosSzekeres.Omission

theorem balanced_population_192 : Partition.BalancedBound 192 :=
  OmissionBalanced.balanced_bound_of_hole_budget (budget := 59)
    (OmissionBalancedCover.exclusion_transfer OmissionBalancedCover.excludes_budget)

theorem residual_population_123 : Partition.ResidualBound 123 :=
  OmissionResidual.residual_bound_of_hole_budget (budget := 30)
    (OmissionResidualCover.exclusion_transfer OmissionResidualCover.excludes_budget)

theorem forces_convex_octagon_317 : ForcesConvexNGon 317 8 :=
  Partition.forces_317_of_population_bounds balanced_population_192 residual_population_123

theorem convex_octagon_of_card_ge_317 (S : Finset (Fin 2 → ℝ))
    (gp : GeneralPosition S) (size : 317 ≤ S.card) :
    ∃ T : Finset (Fin 2 → ℝ), T ⊆ S ∧ T.card = 8 ∧
      ConvexIndependent ℝ (fun p : (T : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  forces_convex_octagon_317 S gp size

#print axioms balanced_population_192
#print axioms residual_population_123
#print axioms forces_convex_octagon_317
#print axioms convex_octagon_of_card_ge_317
#check @forces_convex_octagon_317
#check @convex_octagon_of_card_ge_317

end ErdosSzekeres.Omission
