import Final312.Bridge62
import BalancedCover62Proof.Root
import Final313.Final

/-!
ES(8) ≤ 312. The exported certificate `OmissionBalancedCover62.excludes_budget` excludes
every 0/1 hole vector satisfying the 3,131 balanced rows with at most 62 holes, so the
balanced population is at most 189. With the residual bound 121 of the 313 proof, every
octagon-free set has at most 189 + 121 + 1 = 311 points.
-/

open ErdosSzekeres

namespace ErdosSzekeres.Omission

theorem balanced_population_189 : Partition.BalancedBound 189 :=
  OmissionBalanced.balanced_bound_of_hole_budget (budget := 62)
    (OmissionBalancedCover62.exclusion_transfer OmissionBalancedCover62.excludes_budget)

theorem residual_population_121 : Partition.ResidualBound 121 :=
  OmissionResidual32Bridge2650.residual_bound_121_of_excludes residual_excludes_2650_zero

/-- Every set of at least 312 points in general position contains a convex octagon. -/
theorem forces_convex_octagon_312 : ForcesConvexNGon 312 8 :=
  Partition.forces_of_population_bounds (by omega) balanced_population_189 residual_population_121

theorem convex_octagon_of_card_ge_312 (S : Finset (Fin 2 → ℝ))
    (gp : GeneralPosition S) (size : 312 ≤ S.card) :
    ∃ T : Finset (Fin 2 → ℝ), T ⊆ S ∧ T.card = 8 ∧
      ConvexIndependent ℝ (fun p : (T : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  forces_convex_octagon_312 S gp size

#print axioms balanced_population_189
#print axioms forces_convex_octagon_312
#print axioms convex_octagon_of_card_ge_312

end ErdosSzekeres.Omission
