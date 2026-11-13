import ErdosSzekeres.Omission.CoupledSecondObstruction
import SecondResidualCountermodel

/-! The already checked abstract 32-hole witness satisfies all 1,187 original
rows, all 45 earlier geometric rows and all 42 first-template rows, but violates the new coupled
row. This does not claim a real-point realization or a new population bound. -/
namespace ErdosSzekeres.Omission.CoupledCoreSecond
open scoped BigOperators
set_option maxHeartbeats 10000000

theorem support_eq_candidate : support.toFinset = SecondResidualCountermodel.coupledCandidate := by
  decide +kernel

theorem witness_violates_coupled :
    ¬ 1 ≤ (support.toFinset ∩ SecondResidualCountermodel.missing).card := by
  rw [support_eq_candidate, SecondResidualCountermodel.candidate_occupied]
  decide

/-- Finite independence from the original rows, the forty-five earlier geometric rows,
and all forty-two first-template rows, witnessed by the same exact Boolean hole assignment. -/
theorem strict_strengthening :
    ∃ h : Fin 154 → ℕ, (∀ i, h i ≤ 1) ∧
      (∀ r : Fin 1187, OmissionResidual.demand r ≤
        ∑ i ∈ OmissionResidual.support r, h i) ∧
      (∀ r : Fin 21, AdditionalResidualRows.demand r ≤
        ∑ i ∈ AdditionalResidualRows.support r, h i) ∧
      (∀ r : Fin 24, GeneralResidualBlocks.demand r ≤
        ∑ i ∈ GeneralResidualBlocks.support r, h i) ∧
      (∀ r : Fin 42, 1 ≤ ∑ i ∈ CoupledVariants.support r, h i) ∧
      (∑ i, h i) = 32 ∧ ¬1 ≤ ∑ i ∈ support.toFinset, h i := by
  refine ⟨SecondResidualCountermodel.holes, SecondResidualCountermodel.holes_bool, ?_, ?_, ?_, ?_,
    SecondResidualCountermodel.total_holes, ?_⟩
  · intro r
    rw [SecondResidualCountermodel.sum_holes]
    exact SecondResidualCountermodel.original_rows r
  · intro r
    rw [SecondResidualCountermodel.sum_holes]
    exact SecondResidualCountermodel.prior_additional_rows r
  · intro r
    rw [SecondResidualCountermodel.sum_holes]
    exact SecondResidualCountermodel.general_block_rows r
  · intro r
    rw [SecondResidualCountermodel.sum_holes]
    exact SecondResidualCountermodel.prior_coupled_rows r
  · rw [SecondResidualCountermodel.sum_holes]
    exact witness_violates_coupled

/-- In particular, the abstract witness cannot be the missing-state set of
an actual configuration with the residual hypotheses. -/
theorem countermodel_not_realizable {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    c.residualOccupied noCap noOctagon noJunction ≠
      Finset.univ \ SecondResidualCountermodel.missing := by
  intro he
  have bound := hole_bound c noCap noOctagon noJunction
  rw [he] at bound
  have eq : support.toFinset \ (Finset.univ \ SecondResidualCountermodel.missing) =
      support.toFinset ∩ SecondResidualCountermodel.missing := by ext i; simp
  exact witness_violates_coupled (eq ▸ bound)

#print axioms strict_strengthening
#print axioms countermodel_not_realizable
end ErdosSzekeres.Omission.CoupledCoreSecond
