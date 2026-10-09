import BalancedPopulation
import Root
import ResidualBudgets

/-!
Closed global assembly. This source requires both complete arithmetic roots
and every geometric row theorem. Its checked status is established only by
the corresponding complete `scripts/check_omission_global.py` output.
-/

namespace ErdosSzekeres.Omission

theorem residual_population_123 : Partition.ResidualBound 123 :=
  OmissionResidual.residual_bound_of_hole_budget (budget := 30) OmissionResidual.excludes_budget

/-- Every finite real point set in general position with at least 317 points
contains eight points in convex position. There is no emptiness requirement. -/
theorem forces_convex_octagon_317 : ForcesConvexNGon 317 8 :=
  Partition.forces_317_of_population_bounds balanced_population_192 residual_population_123

/-- The forcing theorem with its definitions exposed at the geometric boundary. -/
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
