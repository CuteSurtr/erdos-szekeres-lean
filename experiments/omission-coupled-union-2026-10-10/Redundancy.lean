import UnionCatalog
import Catalog

open scoped BigOperators
namespace ErdosSzekeres.Omission.CoupledUnion
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

/-- A deficient intersection forces a hole on S under any Boolean assignment. -/
theorem forced_hole_of_deficit {α : Type*} [DecidableEq α]
    (R S : Finset α) (d : ℕ) (holes : α → ℕ)
    (hbool : ∀ i, holes i ≤ 1)
    (hrow : d ≤ ∑ i ∈ R, holes i) (hdef : (R \ S).card < d) :
    1 ≤ ∑ i ∈ S, holes i := by
  by_contra h
  have hz : ∑ i ∈ S, holes i = 0 := by omega
  have hzero : ∀ i ∈ S, holes i = 0 := by
    intro i hi
    have hh := Finset.single_le_sum (fun j (_ : j ∈ S) => Nat.zero_le (holes j)) hi
    omega
  have heq : ∑ i ∈ R \ S, holes i = ∑ i ∈ R, holes i := by
    apply Finset.sum_subset Finset.sdiff_subset
    intro i hi hn
    apply hzero i
    by_contra hs
    exact hn (Finset.mem_sdiff.mpr ⟨hi, hs⟩)
  have hle : ∑ i ∈ R \ S, holes i ≤ (R \ S).card := by
    calc
      ∑ i ∈ R \ S, holes i ≤ ∑ _i ∈ R \ S, 1 :=
        Finset.sum_le_sum (fun i _ => hbool i)
      _ = (R \ S).card := by simp
  omega

theorem redundant_deficits : ∀ i : Fin 48,
    (OmissionResidual.support (redundancyRow i) \ support (redundantIndex i)).card <
      OmissionResidual.demand (redundancyRow i) := by
  simp only [matches_literal]
  decide +kernel

/-- All 48 classified redundant rows follow from single original inequalities.
The Boolean assumption is explicit; no geometric realization is assumed. -/
theorem redundant_rows_implied (holes : Fin 154 → ℕ)
    (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) (j : Fin 48) :
    1 ≤ ∑ i ∈ support (redundantIndex j), holes i := by
  exact forced_hole_of_deficit _ _ _ holes hbool (hrows (redundancyRow j))
    (redundant_deficits j)

#print axioms forced_hole_of_deficit
#print axioms redundant_deficits
#print axioms redundant_rows_implied
end ErdosSzekeres.Omission.CoupledUnion
