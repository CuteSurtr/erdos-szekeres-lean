import BalancedRows
import ErdosSzekeres.Omission.PopulationBounds

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission

namespace OmissionBalanced

def ExcludesHoleBudget (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
    (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget

theorem feasible_holes {n} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) + n = 252 := by
  classical
  let occupied := c.occupied noCap noCup
  refine ⟨fun i => if i ∈ occupied then 0 else 1, ?_, ?_, ?_⟩
  · intro i
    dsimp only
    split_ifs <;> omega
  · intro r
    simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      all_geometric_rows c noCap noCup noOctagon r
  · have hc := Finset.card_add_card_compl occupied
    have hn : occupied.card = n := c.occupied_card noCap noCup
    have hh : (∑ i : Fin 252, if i ∈ occupied then 0 else 1) = occupiedᶜ.card := by
      simp [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, Finset.compl_eq_univ_sdiff]
    rw [hh]
    simp only [Fintype.card_fin] at hc
    omega

theorem balanced_bound_of_hole_budget {budget : ℕ}
    (verified : ExcludesHoleBudget budget) : Partition.BalancedBound (251 - budget) := by
  intro n c noCap noCup noOctagon
  obtain ⟨holes, hb, hr, hc⟩ := feasible_holes c noCap noCup noOctagon
  by_contra h
  exact verified ⟨holes, hb, hr, by omega⟩

#print axioms feasible_holes
#print axioms balanced_bound_of_hole_budget

end OmissionBalanced
