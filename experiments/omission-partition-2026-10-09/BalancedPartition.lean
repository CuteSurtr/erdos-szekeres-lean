import BalancedGeometry
import ErdosSzekeres.Omission.Partition

open ErdosSzekeres ErdosSzekeres.Omission
open ErdosSzekeres.Omission.Partition ErdosSzekeres.Omission.Subsets

namespace OmissionBalanced

/-- The independently checked large balanced certificate supplies the first
population bound with no geometric row assumptions. -/
theorem balanced_bound_192 : BalancedBound 192 :=
  fun _ c noCap noCup noOct => real_configuration_bound c noCap noCup noOct

/-- Only the residual population theorem remains in the asymmetric bound. -/
theorem asymmetric_315_of_residual_123 (residual : ResidualBound 123) :
    AsymmetricBound 315 := asymmetric_of_population_bounds balanced_bound_192 residual

/-- Conditional global reduction with every partition and projective step
proved. The residual population hypothesis is still unproved. -/
theorem forces_317_of_residual_123 (residual : ResidualBound 123) :
    ForcesConvexNGon 317 8 :=
  forces_317_of_asymmetric_315 (asymmetric_315_of_residual_123 residual)

/-- A putative counterexample to the 317 bound supplies at least 124 actual
residual chart points. Both coordinate maps and the residual index set are
retained, together with every avoidance and no-junction restriction. -/
theorem large_avoiding_set_has_residual (S : Finset Point) (gp : GeneralPosition S)
    (size : 317 ≤ S.card) (avoid : ¬ HasConvexNGon 8 S) :
    ∃ n : ℕ, ∃ c : Configuration n, ∃ R : Finset (Fin n),
      S.card = n + 1 ∧ IsRootDeletionChart S c ∧ 124 ≤ R.card ∧
      ¬ (restrict c R).HasCap 6 ∧
      ¬ HasConvexNGon 8 (Finset.univ.image (restrict c R).point) ∧
      NoJunctionOn (restrict c R).cup (Finset.range R.card) := by
  obtain ⟨n, c, count, chart, noCap, noOct⟩ := exists_cap_free_chart S gp
    (Finset.card_pos.mp (by omega)) avoid
  obtain ⟨H, R, _, _, split, hcap, hcup, hoct, rcap, roct, junction⟩ :=
    exists_partition c (by omega) noCap noOct
  have balanced := real_configuration_bound (restrict c H) hcap hcup hoct
  exact ⟨n, c, R, count, chart, by omega, rcap, roct, junction⟩

#print axioms balanced_bound_192
#print axioms asymmetric_315_of_residual_123
#print axioms forces_317_of_residual_123
#print axioms large_avoiding_set_has_residual

end OmissionBalanced
