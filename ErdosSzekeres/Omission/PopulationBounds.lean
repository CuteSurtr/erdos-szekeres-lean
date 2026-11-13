import ErdosSzekeres.Omission.Partition

/-!
Population-bound composition for ordinary finite real point sets.

The geometric partition and the projective change of coordinates are imported
from `Partition`; this file only makes the population parameters explicit.
The two extra points in the forcing threshold account for the deleted root
and the strict inequality in the cardinality bound.
-/

namespace ErdosSzekeres.Omission.Partition

/-- Combine any two proved population bounds. The positivity assumption only
handles configurations with at most one point, where no partition is needed. -/
theorem asymmetric_of_bounds {B R : ℕ} (positive : 1 ≤ B + R)
    (balanced : BalancedBound B) (residual : ResidualBound R) :
    AsymmetricBound (B + R) := by
  intro n c noCap noOct
  by_cases hn : 2 ≤ n
  · obtain ⟨H, T, _, _, count, hcap, hcup, hoct, rcap, roct, junction⟩ :=
      exists_partition c hn noCap noOct
    have h := balanced _ (Subsets.restrict c H) hcap hcup hoct
    have r := residual _ (Subsets.restrict c T) rcap roct junction
    omega
  · omega

/-- A completely geometric, parameterized global octagon reduction. -/
theorem forces_of_population_bounds {B R : ℕ} (positive : 1 ≤ B + R)
    (balanced : BalancedBound B) (residual : ResidualBound R) :
    ForcesConvexNGon (B + R + 2) 8 :=
  forces_of_asymmetric_bound (asymmetric_of_bounds positive balanced residual)

/-- The corresponding bound on every octagon-avoiding real point set. -/
theorem avoiding_card_le_of_population_bounds {B R : ℕ} (positive : 1 ≤ B + R)
    (balanced : BalancedBound B) (residual : ResidualBound R)
    (S : Finset Point) (gp : GeneralPosition S) (avoid : ¬ HasConvexNGon 8 S) :
    S.card ≤ B + R + 1 :=
  avoiding_card_le_of_asymmetric_bound
    (asymmetric_of_bounds positive balanced residual) S gp avoid

/-- The weaker residual population 124 would already improve the published
source archive's finite bound 319 by combining with the balanced bound 192.
Both population statements remain explicit hypotheses here. -/
theorem forces_318_of_population_bounds (balanced : BalancedBound 192)
    (residual : ResidualBound 124) : ForcesConvexNGon 318 8 :=
  forces_of_population_bounds (by omega) balanced residual

/-- The stronger residual population 123 gives the target threshold 317. -/
theorem forces_317_of_population_bounds (balanced : BalancedBound 192)
    (residual : ResidualBound 123) : ForcesConvexNGon 317 8 :=
  forces_of_population_bounds (by omega) balanced residual

end ErdosSzekeres.Omission.Partition
