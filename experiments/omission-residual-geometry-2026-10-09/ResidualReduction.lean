import ResidualAllGeometry
import ErdosSzekeres.Omission.Partition

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission

namespace OmissionResidual

/-- The exact arithmetic statement still awaiting a complete kernel check.
This is a proposition definition, not an axiom or an assumed theorem. -/
def ExcludesThirtyHoles : Prop :=
  ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
    (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ 30

/-- Every actual residual configuration supplies a Boolean hole vector for
all 1187 literal rows, with the exact population complement. -/
theorem feasible_holes {n} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) + n = 154 := by
  classical
  let occupied := c.residualOccupied noCap noOctagon noJunction
  refine ⟨fun i => if i ∈ occupied then 0 else 1, ?_, ?_, ?_⟩
  · intro i
    dsimp only
    split_ifs <;> omega
  · intro r
    simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      all_geometric_rows c noCap noOctagon noJunction r
  · have hc := Finset.card_add_card_compl occupied
    have hn : occupied.card = n := c.residual_occupied_card noCap noOctagon noJunction
    have hh : (∑ i : Fin 154, if i ∈ occupied then 0 else 1) = occupiedᶜ.card := by
      simp [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, Finset.compl_eq_univ_sdiff]
    rw [hh]
    simp only [Fintype.card_fin] at hc
    omega

theorem residual_bound_of_arithmetic (verified : ExcludesThirtyHoles) :
    Partition.ResidualBound 123 := by
  intro n c noCap noOctagon noJunction
  obtain ⟨holes, hb, hr, hc⟩ := feasible_holes c noCap noOctagon noJunction
  by_contra h
  exact verified ⟨holes, hb, hr, by omega⟩

/-- End-to-end conditional composition. The balanced premise has a separate
completed certificate. The residual arithmetic premise remains unproved. -/
theorem forces_317_of_arithmetic (balanced : Partition.BalancedBound 192)
    (verified : ExcludesThirtyHoles) : ForcesConvexNGon 317 8 :=
  forces_317_of_asymmetric_315
    (Partition.asymmetric_of_population_bounds balanced (residual_bound_of_arithmetic verified))

#print axioms feasible_holes
#print axioms residual_bound_of_arithmetic
#print axioms forces_317_of_arithmetic

end OmissionResidual
