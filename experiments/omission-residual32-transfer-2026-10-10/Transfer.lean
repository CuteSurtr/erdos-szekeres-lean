import OriginalBinding
import OldcutsBinding
import GeometricBinding
import NewCuts
import ResidualAllGeometry
import ErdosSzekeres.Omission.Partition

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission

namespace OmissionResidual32Transfer

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

/-- The same hole vector is used in every row family. -/
def holesOf (occupied : Finset (Fin 154)) (i : Fin 154) : ℕ :=
  if i ∈ occupied then 0 else 1

theorem holesOf_boolean (occupied : Finset (Fin 154)) (i : Fin 154) :
    holesOf occupied i ≤ 1 := by
  unfold holesOf
  split_ifs <;> omega

theorem holesOf_sum (occupied support : Finset (Fin 154)) :
    (∑ i ∈ support, holesOf occupied i) = (support \ occupied).card := by
  simp [holesOf, Finset.sum_ite, Finset.filter_notMem_eq_sdiff]

/-- All 2457 rows preceding the new rounding cuts hold for one actual residual
configuration. The original, old-cut and new-geometry literal matches are checked. -/
theorem prior_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩,
        holesOf (c.residualOccupied noCap noOctagon noJunction) i := by
  let occupied := c.residualOccupied noCap noOctagon noJunction
  have original : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holesOf occupied i := by
    intro r
    rw [holesOf_sum]
    exact OmissionResidual.all_geometric_rows c noCap noOctagon noJunction r
  intro r
  by_cases h : r.val < 1187
  · let b : Fin 1187 := ⟨r.val, h⟩
    have hm := original_matches b
    have he : (⟨0 + b.val, by omega⟩ : Fin 2469) = ⟨r.val, by omega⟩ := by
      apply Fin.ext; simp [b]
    rw [he] at hm
    rw [hm.1, hm.2]
    exact original b
  by_cases h2 : r.val < 2295
  · let b : Fin 1108 := ⟨r.val - 1187, by omega⟩
    have hm := oldcuts_matches b
    have he : (⟨1187 + b.val, by omega⟩ : Fin 2469) = ⟨r.val, by omega⟩ := by
      apply Fin.ext; dsimp [b]; omega
    rw [he] at hm
    rw [hm.1, hm.2]
    exact ResidualCoverCutsV2.all_rows (holesOf occupied) (holesOf_boolean occupied) original b
  · let b : Fin 162 := ⟨r.val - 2295, by omega⟩
    have hm := geometric_matches b
    have he : (⟨2295 + b.val, by omega⟩ : Fin 2469) = ⟨r.val, by omega⟩ := by
      apply Fin.ext; dsimp [b]; omega
    rw [he] at hm
    rw [hm.1, hm.2, holesOf_sum]
    exact geometric_rows c noCap noOctagon noJunction b

/-- The entire frozen 2469-row catalog holds for the same actual hole vector. -/
theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 2469, OmissionResidual32Contexts.demand r ≤
      ∑ i ∈ OmissionResidual32Contexts.support r,
        holesOf (c.residualOccupied noCap noOctagon noJunction) i := by
  intro r
  by_cases h : r.val < 2457
  · exact prior_rows c noCap noOctagon noJunction ⟨r.val, h⟩
  · let b : Fin 12 := ⟨r.val - 2457, by omega⟩
    have hr : (⟨2457 + b.val, by omega⟩ : Fin 2469) = r := by
      apply Fin.ext; dsimp [b]; omega
    rw [← hr]
    exact new_cut_rows _ (holesOf_boolean _) (prior_rows c noCap noOctagon noJunction) b

/-- Every actual residual configuration supplies a Boolean model of every
literal research row, with its exact population complement. This does not
assert an exclusion of any hole budget. -/
theorem feasible_holes {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r : Fin 2469, OmissionResidual32Contexts.demand r ≤
        ∑ i ∈ OmissionResidual32Contexts.support r, holes i) ∧
      (∑ i, holes i) + n = 154 := by
  let occupied := c.residualOccupied noCap noOctagon noJunction
  refine ⟨holesOf occupied, holesOf_boolean occupied, all_rows c noCap noOctagon noJunction, ?_⟩
  have hc := Finset.card_add_card_compl occupied
  have hn : occupied.card = n := c.residual_occupied_card noCap noOctagon noJunction
  have hh : (∑ i : Fin 154, holesOf occupied i) = occupiedᶜ.card := by
    simpa only [Finset.compl_eq_univ_sdiff] using holesOf_sum occupied Finset.univ
  rw [hh]
  simp only [Fintype.card_fin] at hc
  omega

/-- This arithmetic exclusion is a proposition to prove, not an assumption
silently introduced into the library. -/
def ExcludesHoleBudget (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
    (∀ r : Fin 2469, OmissionResidual32Contexts.demand r ≤
      ∑ i ∈ OmissionResidual32Contexts.support r, holes i) ∧
    (∑ i, holes i) ≤ budget

theorem residual_bound_of_hole_budget {budget : ℕ}
    (verified : ExcludesHoleBudget budget) : Partition.ResidualBound (153 - budget) := by
  intro n c noCap noOctagon noJunction
  obtain ⟨holes, hb, hr, hc⟩ := feasible_holes c noCap noOctagon noJunction
  by_contra h
  exact verified ⟨holes, hb, hr, by omega⟩

#print axioms prior_rows
#print axioms all_rows
#print axioms feasible_holes
#print axioms residual_bound_of_hole_budget
end OmissionResidual32Transfer
