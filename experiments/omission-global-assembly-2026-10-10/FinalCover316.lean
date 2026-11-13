import BalancedCover60Proof.Root
import ResidualCoverProof.Root
import BalancedCover60Bridge
import ResidualCoverBridge

/-!
Closed assembly through the two rounded-cover certificates. Its status is
established only by a complete successful final assembly and axiom audit.
-/

namespace ErdosSzekeres.Omission

theorem balanced_population_191 : Partition.BalancedBound 191 :=
  OmissionBalanced.balanced_bound_of_hole_budget (budget := 60)
    (OmissionBalancedCover60.exclusion_transfer OmissionBalancedCover60.excludes_budget)

theorem residual_population_123 : Partition.ResidualBound 123 :=
  OmissionResidual.residual_bound_of_hole_budget (budget := 30)
    (OmissionResidualCover.exclusion_transfer OmissionResidualCover.excludes_budget)

theorem forces_convex_octagon_316 : ForcesConvexNGon 316 8 :=
  Partition.forces_of_population_bounds (by omega) balanced_population_191 residual_population_123

theorem convex_octagon_of_card_ge_316 (S : Finset (Fin 2 → ℝ))
    (gp : GeneralPosition S) (size : 316 ≤ S.card) :
    ∃ T : Finset (Fin 2 → ℝ), T ⊆ S ∧ T.card = 8 ∧
      ConvexIndependent ℝ (fun p : (T : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  forces_convex_octagon_316 S gp size

#print axioms balanced_population_191
#print axioms residual_population_123
#print axioms forces_convex_octagon_316
#print axioms convex_octagon_of_card_ge_316
#check @forces_convex_octagon_316
#check @convex_octagon_of_card_ge_316

end ErdosSzekeres.Omission
