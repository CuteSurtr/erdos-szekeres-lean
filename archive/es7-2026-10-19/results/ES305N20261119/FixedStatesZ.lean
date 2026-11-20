/-
ES305N20261119: the balanced hole budget with the Z-row and two fixed occupied states.

The first point of a balanced configuration has state 0 (no incoming pair), the second has state 1 (its only
incoming pair has labels (1, 1)). So trees for `ExcludesHoleBudgetZF b` may assume h_0 = h_1 = 0: no "state 0
missing" or "state 1 missing" side is needed. Compiled like BalancedBudgetsZ.lean (tools/build.sh).
-/
import BalancedRows
import BalancedCoverCutsV2
import LemmaZ
import ErdosSzekeres.Omission.PopulationBounds

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks
  ErdosSzekeres.Omission.BalancedCatalog

namespace OmissionBalancedZF

theorem column_zero (cup : ℕ → ℕ → ℕ → Bool) (i : ℕ) : column cup 0 i = 0 := by
  unfold column; simp

theorem labels_zero_one (cup : ℕ → ℕ → ℕ → Bool) : labels cup 0 1 = (1, 1) := by
  have a1 := rank_ge (EndingPath.pair (cup := cup) (color := false) (show 0 < 1 by norm_num))
  have a2 := (length_bounds (rank_attained cup false 0 1 (by norm_num))).2.1
  have b1 := rank_ge (EndingPath.pair (cup := cup) (color := true) (show 0 < 1 by norm_num))
  have b2 := (length_bounds (rank_attained cup true 0 1 (by norm_num))).2.1
  simp only [labels, Prod.mk.injEq]
  omega

theorem column_one (cup : ℕ → ℕ → ℕ → Bool) (i : ℕ) : column cup 1 i = if i = 0 then 1 else 0 := by
  unfold column
  rw [Finset.range_one, Finset.sup_singleton, labels_zero_one]
  by_cases h : i = 0 <;> simp [h]

theorem catalog_zero : ∀ k, k < 252 → catalog.getD k [] = [0, 0, 0, 0, 0] → k = 0 := by
  decide +kernel

theorem catalog_one : ∀ k, k < 252 → catalog.getD k [] = [1, 0, 0, 0, 0] → k = 1 := by
  decide +kernel

theorem owner_zero {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (h0 : 0 < n) : c.balancedOwner noCap noCup ⟨0, h0⟩ = 0 := by
  apply Fin.ext
  have h := OmissionZRow.owner_profile c noCap noCup ⟨0, h0⟩
  simp only [column_zero] at h
  exact catalog_zero _ (c.balancedOwner noCap noCup ⟨0, h0⟩).isLt (by simpa [List.ofFn_succ] using h)

theorem owner_one {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (h1 : 1 < n) : c.balancedOwner noCap noCup ⟨1, h1⟩ = 1 := by
  apply Fin.ext
  have h := OmissionZRow.owner_profile c noCap noCup ⟨1, h1⟩
  simp only [column_one] at h
  exact catalog_one _ (c.balancedOwner noCap noCup ⟨1, h1⟩).isLt (by simpa [List.ofFn_succ] using h)

theorem zero_mem_occupied {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) (h0 : 0 < n) : (0 : Fin 252) ∈ c.occupied noCap noCup :=
  Finset.mem_image.mpr ⟨⟨0, h0⟩, Finset.mem_univ _, owner_zero c noCap noCup h0⟩

theorem one_mem_occupied {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 7)
    (noCup : ¬ c.HasCup 7) (h1 : 1 < n) : (1 : Fin 252) ∈ c.occupied noCap noCup :=
  Finset.mem_image.mpr ⟨⟨1, h1⟩, Finset.mem_univ _, owner_one c noCap noCup h1⟩

/-- No 0/1 vector with h_0 = h_1 = 0 and at most `budget` holes satisfies the 3,131 rows and the Z-row. -/
def ExcludesHoleBudgetZF (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 252 → ℕ, holes 0 = 0 ∧ holes 1 = 0 ∧ (∀ i, holes i ≤ 1) ∧
    (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
    (∀ r, BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, holes i) ∧
    15 ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ (∑ i, holes i) ≤ budget

theorem feasible_holes_zf (n66 : OmissionZRow.N66Bound 55) {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) (hn : 2 ≤ n) :
    ∃ holes : Fin 252 → ℕ, holes 0 = 0 ∧ holes 1 = 0 ∧ (∀ i, holes i ≤ 1) ∧
      (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
      (∀ r, BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, holes i) ∧
      15 ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ (∑ i, holes i) + n = 252 := by
  classical
  let occupied := c.occupied noCap noCup
  have hb : ∀ i, (fun i => if i ∈ occupied then 0 else 1) i ≤ 1 := by
    intro i
    dsimp only
    split_ifs <;> omega
  have hr : ∀ r, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, (fun i => if i ∈ occupied then 0 else 1) i := by
    intro r
    simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      OmissionBalanced.all_geometric_rows c noCap noCup noOctagon r
  refine ⟨fun i => if i ∈ occupied then 0 else 1, ?_, ?_, hb, hr,
    BalancedCoverCutsV2.all_rows _ hb hr, ?_, ?_⟩
  · simp [occupied, zero_mem_occupied c noCap noCup (by omega)]
  · simp [occupied, one_mem_occupied c noCap noCup (by omega)]
  · simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      OmissionZRow.z_row n66 c noCap noCup noOctagon
  · have hc := Finset.card_add_card_compl occupied
    have hn' : occupied.card = n := c.occupied_card noCap noCup
    have hh : (∑ i : Fin 252, if i ∈ occupied then 0 else 1) = occupiedᶜ.card := by
      simp [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, Finset.compl_eq_univ_sdiff]
    rw [hh]
    simp only [Fintype.card_fin] at hc
    omega

theorem balanced_bound_of_hole_budget_zf {budget : ℕ} (small : budget ≤ 249)
    (n66 : OmissionZRow.N66Bound 55) (verified : ExcludesHoleBudgetZF budget) :
    Partition.BalancedBound (251 - budget) := by
  intro n c noCap noCup noOctagon
  by_cases hn : 2 ≤ n
  · obtain ⟨holes, h0, h1, hb, hr, hcut, hz, hc⟩ := feasible_holes_zf n66 c noCap noCup noOctagon hn
    by_contra h
    exact verified ⟨holes, h0, h1, hb, hr, hcut, hz, by omega⟩
  · omega

/-- ES(8) ≤ 304 from a budget-67 tree with states 0 and 1 fixed occupied. A statement about the inputs. -/
theorem composition_304_zf (trees : ExcludesHoleBudgetZF 67) (n66 : OmissionZRow.N66Bound 55)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 304 8 :=
  Partition.forces_of_population_bounds (by omega)
    (balanced_bound_of_hole_budget_zf (by norm_num) n66 trees) hR

/-- ES(8) ≤ 303 from a budget-68 tree with states 0 and 1 fixed occupied. A statement about the inputs. -/
theorem composition_303_zf (trees : ExcludesHoleBudgetZF 68) (n66 : OmissionZRow.N66Bound 55)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 303 8 :=
  Partition.forces_of_population_bounds (by omega)
    (balanced_bound_of_hole_budget_zf (by norm_num) n66 trees) hR

end OmissionBalancedZF

#print axioms OmissionBalancedZF.feasible_holes_zf
#print axioms OmissionBalancedZF.composition_304_zf
#print axioms OmissionBalancedZF.composition_303_zf
