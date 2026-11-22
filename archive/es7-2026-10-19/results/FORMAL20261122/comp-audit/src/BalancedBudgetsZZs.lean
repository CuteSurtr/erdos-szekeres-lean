/-
The balanced hole budget with the Z-row, the Z*-row and the two fixed occupied states (states 0 and 1).
`ExcludesHoleBudgetZZsF b` is the statement a zero-side-only tree on `balzs.rows` (the 3,131 catalog rows, the
Z-row and the Z*-row) certifies. Compiled by build_zs.sh against the chain311, LemmaZ and FixedStatesZ oleans.
-/
import FixedStatesZ
import LemmaZStar

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks
  ErdosSzekeres.Omission.BalancedCatalog

namespace OmissionBalancedZZsF

/-- No 0/1 vector with h_0 = h_1 = 0 and at most `budget` holes satisfies the 3,131 rows, the Z-row and the
Z*-row. -/
def ExcludesHoleBudgetZZsF (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 252 → ℕ, holes 0 = 0 ∧ holes 1 = 0 ∧ (∀ i, holes i ≤ 1) ∧
    (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
    (∀ r, BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, holes i) ∧
    15 ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ 15 ≤ ∑ i ∈ OmissionZStarRow.Zs, holes i ∧
    (∑ i, holes i) ≤ budget

theorem feasible_holes_zzsf (n66 : OmissionZRow.N66Bound 55) {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) (hn : 2 ≤ n) :
    ∃ holes : Fin 252 → ℕ, holes 0 = 0 ∧ holes 1 = 0 ∧ (∀ i, holes i ≤ 1) ∧
      (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
      (∀ r, BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, holes i) ∧
      15 ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ 15 ≤ ∑ i ∈ OmissionZStarRow.Zs, holes i ∧
      (∑ i, holes i) + n = 252 := by
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
    BalancedCoverCutsV2.all_rows _ hb hr, ?_, ?_, ?_⟩
  · simp [occupied, OmissionBalancedZF.zero_mem_occupied c noCap noCup (by omega)]
  · simp [occupied, OmissionBalancedZF.one_mem_occupied c noCap noCup (by omega)]
  · simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      OmissionZRow.z_row n66 c noCap noCup noOctagon
  · simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      OmissionZStarRow.zs_row n66 c noCap noCup noOctagon
  · have hc := Finset.card_add_card_compl occupied
    have hn' : occupied.card = n := c.occupied_card noCap noCup
    have hh : (∑ i : Fin 252, if i ∈ occupied then 0 else 1) = occupiedᶜ.card := by
      simp [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, Finset.compl_eq_univ_sdiff]
    rw [hh]
    simp only [Fintype.card_fin] at hc
    omega

theorem balanced_bound_of_hole_budget_zzsf {budget : ℕ} (small : budget ≤ 249)
    (n66 : OmissionZRow.N66Bound 55) (verified : ExcludesHoleBudgetZZsF budget) :
    Partition.BalancedBound (251 - budget) := by
  intro n c noCap noCup noOctagon
  by_cases hn : 2 ≤ n
  · obtain ⟨holes, h0, h1, hb, hr, hcut, hz, hzs, hc⟩ :=
      feasible_holes_zzsf n66 c noCap noCup noOctagon hn
    by_contra h
    exact verified ⟨holes, h0, h1, hb, hr, hcut, hz, hzs, by omega⟩
  · omega

/-- ES(8) ≤ 371 − b from a zero-side budget-b tree on catalog + Z-row + Z*-row. Statements about the inputs. -/
theorem composition_303_zzsf (trees : ExcludesHoleBudgetZZsF 68) (n66 : OmissionZRow.N66Bound 55)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 303 8 :=
  Partition.forces_of_population_bounds (by omega)
    (balanced_bound_of_hole_budget_zzsf (by norm_num) n66 trees) hR

theorem composition_302_zzsf (trees : ExcludesHoleBudgetZZsF 69) (n66 : OmissionZRow.N66Bound 55)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 302 8 :=
  Partition.forces_of_population_bounds (by omega)
    (balanced_bound_of_hole_budget_zzsf (by norm_num) n66 trees) hR

theorem composition_301_zzsf (trees : ExcludesHoleBudgetZZsF 70) (n66 : OmissionZRow.N66Bound 55)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 301 8 :=
  Partition.forces_of_population_bounds (by omega)
    (balanced_bound_of_hole_budget_zzsf (by norm_num) n66 trees) hR

theorem composition_300_zzsf (trees : ExcludesHoleBudgetZZsF 71) (n66 : OmissionZRow.N66Bound 55)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 300 8 :=
  Partition.forces_of_population_bounds (by omega)
    (balanced_bound_of_hole_budget_zzsf (by norm_num) n66 trees) hR

end OmissionBalancedZZsF

#print axioms OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf
#print axioms OmissionBalancedZZsF.composition_301_zzsf
