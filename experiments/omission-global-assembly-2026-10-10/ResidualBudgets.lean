import ResidualReduction
import ErdosSzekeres.Omission.PopulationBounds

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission

namespace OmissionResidual

/-- Finite arithmetic exclusion with an explicit hole budget. -/
def ExcludesHoleBudget (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
    (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget

/-- Excluding a larger budget also excludes every smaller budget. -/
theorem excludes_hole_budget_mono {a b : ℕ} (h : a ≤ b)
    (verified : ExcludesHoleBudget b) : ExcludesHoleBudget a := by
  rintro ⟨holes, hb, hr, hc⟩
  exact verified ⟨holes, hb, hr, by omega⟩

/-- The real geometric transfer works for every arithmetic hole budget.
The complement equation is exact, so no rounding or estimated constants enter. -/
theorem residual_bound_of_hole_budget {budget : ℕ}
    (verified : ExcludesHoleBudget budget) : Partition.ResidualBound (153 - budget) := by
  intro n c noCap noOctagon noJunction
  obtain ⟨holes, hb, hr, hc⟩ := feasible_holes c noCap noOctagon noJunction
  by_contra h
  exact verified ⟨holes, hb, hr, by omega⟩

/-- Parameterized end-to-end geometric reduction. The arithmetic exclusion
and the balanced population bound are both explicit hypotheses. -/
theorem forces_of_hole_budget {B budget : ℕ}
    (positive : 1 ≤ B + (153 - budget)) (balanced : Partition.BalancedBound B)
    (verified : ExcludesHoleBudget budget) :
    ForcesConvexNGon (B + (153 - budget) + 2) 8 :=
  Partition.forces_of_population_bounds positive balanced
    (residual_bound_of_hole_budget verified)

/-- The smaller original 29-hole certificate would suffice for threshold 318
when combined with the improved balanced population 192. -/
theorem forces_318_of_twenty_nine_holes (balanced : Partition.BalancedBound 192)
    (verified : ExcludesHoleBudget 29) : ForcesConvexNGon 318 8 :=
  forces_of_hole_budget (by omega) balanced verified

theorem forces_317_of_thirty_holes (balanced : Partition.BalancedBound 192)
    (verified : ExcludesHoleBudget 30) : ForcesConvexNGon 317 8 :=
  forces_of_hole_budget (by omega) balanced verified

#print axioms excludes_hole_budget_mono
#print axioms residual_bound_of_hole_budget
#print axioms forces_of_hole_budget
#print axioms forces_318_of_twenty_nine_holes
#print axioms forces_317_of_thirty_holes

end OmissionResidual
