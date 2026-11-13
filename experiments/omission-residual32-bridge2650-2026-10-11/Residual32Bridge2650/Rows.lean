import Residual32Bridge2650.Matches
import Transfer
import SixthRelaxedProof.Root
import RankGeometryOne
import RankGeometryTwo
import RankGeometryThree
import RankGeometryFour
import ZeroState

/-!
Geometric validity of all 2,650 literal rows, and the conditional residual bound.

`all_rows_2650` holds for the hole vector of every actual residual
configuration (real points in general position, no 6-cap, no convex octagon,
no incoming-6-cup/outgoing-5-cap junction). `Excludes2650Zero` is the remaining
purely arithmetic statement; it is a definition, not an assumption of any
theorem except those that take it as an explicit hypothesis.
-/

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission
open OmissionResidual32Transfer (holesOf holesOf_boolean holesOf_sum)

namespace OmissionResidual32Bridge2650

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

/-- A demand-one literal row is valid once its support has a missing state. -/
theorem row_of_missing {occupied S : Finset (Fin 154)} {r : Fin 2650}
    (hs : support2650 r = S) (hd : demand2650 r = 1) (h : 1 ≤ (S \ occupied).card) :
    demand2650 r ≤ ∑ i ∈ support2650 r, holesOf occupied i := by
  rw [hs, hd, holesOf_sum]
  exact h

/-- Every literal row of the 2,650-row catalog holds for the hole vector of an
actual residual configuration. -/
theorem all_rows_2650 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 2650, demand2650 r ≤
      ∑ i ∈ support2650 r, holesOf (c.residualOccupied noCap noOctagon noJunction) i := by
  intro r
  by_cases h1 : r.val < 2469
  · have he : prefixIndex ⟨r.val, h1⟩ = r := Fin.ext rfl
    obtain ⟨hs, hd⟩ := prefix_matches ⟨r.val, h1⟩
    rw [he] at hs hd
    rw [hs, hd]
    exact OmissionResidual32Transfer.all_rows c noCap noOctagon noJunction ⟨r.val, h1⟩
  by_cases h2 : r.val < 2598
  · let b : Fin 129 := ⟨r.val - 2469, by omega⟩
    have he : addedIndex b = r := Fin.ext (by simp only [addedIndex, b]; omega)
    obtain ⟨hs, hd⟩ := added_matches b
    rw [he] at hs hd
    exact row_of_missing hs hd (Residual32AddedRows.all_rows c noCap noOctagon noJunction b)
  by_cases h3 : r.val < 2646
  · let b : Fin 48 := ⟨r.val - 2598, by omega⟩
    have he : relaxedIndex b = r := Fin.ext (by simp only [relaxedIndex, b]; omega)
    obtain ⟨hs, hd⟩ := relaxed_matches b
    rw [he] at hs hd
    exact row_of_missing hs hd
      (CoupledSixthRelaxedVariants.all_rows c noCap noOctagon noJunction b)
  have hlt := r.isLt
  have hcases : r = ⟨2646, by decide⟩ ∨ r = ⟨2647, by decide⟩ ∨
      r = ⟨2648, by decide⟩ ∨ r = ⟨2649, by decide⟩ := by
    simp only [Fin.ext_iff]
    omega
  rcases hcases with rfl | rfl | rfl | rfl
  · exact row_of_missing rank_one_matches.1 rank_one_matches.2
      (CoupledCoreRankSearchOne.hole_bound c noCap noOctagon noJunction)
  · exact row_of_missing rank_two_matches.1 rank_two_matches.2
      (CoupledCoreRankSearchTwo.hole_bound c noCap noOctagon noJunction)
  · exact row_of_missing rank_three_matches.1 rank_three_matches.2
      (CoupledCoreRankSearchThree.hole_bound c noCap noOctagon noJunction)
  · exact row_of_missing rank_four_matches.1 rank_four_matches.2
      (CoupledCoreRankSearchFour.hole_bound c noCap noOctagon noJunction)

/-- The exact population complement of the actual hole vector. -/
theorem holes_sum_add_population {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    (∑ i, holesOf (c.residualOccupied noCap noOctagon noJunction) i) + n = 154 := by
  let occupied := c.residualOccupied noCap noOctagon noJunction
  have hc := Finset.card_add_card_compl occupied
  have hn : occupied.card = n := c.residual_occupied_card noCap noOctagon noJunction
  have hh : (∑ i : Fin 154, holesOf occupied i) = occupiedᶜ.card := by
    simpa only [Finset.compl_eq_univ_sdiff] using holesOf_sum occupied Finset.univ
  change (∑ i : Fin 154, holesOf occupied i) + n = 154
  rw [hh]
  simp only [Fintype.card_fin] at hc
  omega

/-- The remaining purely arithmetic statement: no Boolean hole vector with state
zero occupied satisfies all 2,650 literal rows within the given hole budget.
This is a proposition to be proved, not an axiom; nothing here asserts it. -/
def Excludes2650Zero (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧
    (∀ r, demand2650 r ≤ ∑ i ∈ support2650 r, holes i) ∧ (∑ i, holes i) ≤ budget

/-- An arithmetic exclusion for budget `b` bounds every actual residual
configuration by `153 - b` points. State zero is occupied whenever `n > 0`;
the empty configuration satisfies every bound. -/
theorem residual_bound_of_excludes2650 {budget : ℕ} (verified : Excludes2650Zero budget) :
    Partition.ResidualBound (153 - budget) := by
  intro n c noCap noOctagon noJunction
  by_contra hn
  have hpos : 0 < n := by omega
  have hsum := holes_sum_add_population c noCap noOctagon noJunction
  have hzero := OmissionResidualZeroState.zero_mem_residualOccupied c noCap noOctagon
    noJunction hpos
  apply verified
  refine ⟨holesOf (c.residualOccupied noCap noOctagon noJunction), holesOf_boolean _, ?_,
    all_rows_2650 c noCap noOctagon noJunction, by omega⟩
  simp only [holesOf, if_pos hzero]

/-- Conditional residual population bound 153 - 32 = 121. -/
theorem residual_bound_121_of_excludes (h : Excludes2650Zero 32) :
    Partition.ResidualBound 121 :=
  residual_bound_of_excludes2650 h

/-- Adapter for the exact root-node shape emitted by the context exporter
(`scripts/omission_context_export.py`): a certificate for any literal catalog
`support'`/`demand'` that agrees row by row with this one, with no forced
missing state and state zero forced occupied, proves `Excludes2650Zero`. -/
theorem excludes2650Zero_of_node {budget : ℕ} {support' : Fin 2650 → Finset (Fin 154)}
    {demand' : Fin 2650 → ℕ} (hs : ∀ r, support' r = support2650 r)
    (hd : ∀ r, demand' r = demand2650 r)
    (h : ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand' r ≤ ∑ i ∈ support' r, holes i) ∧
      (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ (∅ : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 0 ∅) : Finset (Fin 154)), holes i = 0)) :
    Excludes2650Zero budget := by
  rintro ⟨holes, hb, h0, hr, hc⟩
  refine h ⟨holes, hb, fun r => ?_, hc, by simp, ?_⟩
  · rw [hs r, hd r]
    exact hr r
  · intro i hi
    have hi0 : i = 0 := by simpa using hi
    rw [hi0]
    exact h0

#print axioms row_of_missing
#print axioms all_rows_2650
#print axioms holes_sum_add_population
#print axioms residual_bound_of_excludes2650
#print axioms residual_bound_121_of_excludes
#print axioms excludes2650Zero_of_node

end OmissionResidual32Bridge2650
