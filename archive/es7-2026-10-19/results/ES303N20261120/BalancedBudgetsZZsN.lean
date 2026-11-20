/-
Parametric form of BalancedBudgetsZZs.lean (ES303N20261120): the Z-row and the Z*-row from ANY N66 bound,
`N66Bound B → 70 − B ≤ (Z \ occupied).card` and the same for Z*, and the balanced hole budget with both rows at
demand r. With N66 ≤ 55 (r = 15) this is the statement of BalancedBudgetsZZs.lean; with a future N66 ≤ 54 (r = 16)
it is what a budget-69 tree on `balzs.rows` with both demands raised to 16 would certify (ES(8) ≤ 302).
N66 enters only as the hypothesis `N66Bound B` (no such bound below 55 is known yet).
-/
import FixedStatesZ
import LemmaZStar
import BalancedBudgetsZZs

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks
  ErdosSzekeres.Omission.BalancedCatalog ErdosSzekeres.Omission.Ferrers
  ErdosSzekeres.Omission.Subsets ErdosSzekeres.Omission.SlopePartition

namespace OmissionBalancedZZsN

theorem z_row_of {B n : ℕ} (n66 : OmissionZRow.N66Bound B) (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    70 - B ≤ (OmissionZRow.Z \ c.occupied noCap noCup).card := by
  have h1 := Finset.card_sdiff_add_card_inter OmissionZRow.Z (c.occupied noCap noCup)
  rw [OmissionZRow.Z_inter_occupied, Finset.card_image_of_injective _ (c.balancedOwner_injective noCap noCup),
    OmissionZRow.Z_card] at h1
  have h2 : (OmissionZRow.zOwners c noCap noCup).card ≤ B :=
    n66 _ (restrict c _) (restrict_no_cap c _ (OmissionZRow.zOwners_no_cap c noCap noCup))
      (restrict_no_cup c _ (OmissionZRow.zOwners_no_cup c noCap noCup)) (restrict_no_octagon c _ noOctagon)
  omega

theorem zs_row_of {B n : ℕ} (n66 : OmissionZRow.N66Bound B) (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    70 - B ≤ (OmissionZStarRow.Zs \ c.occupied noCap noCup).card := by
  have h1 := Finset.card_sdiff_add_card_inter OmissionZStarRow.Zs (c.occupied noCap noCup)
  rw [OmissionZStarRow.Zs_inter_occupied,
    Finset.card_image_of_injective _ (c.balancedOwner_injective noCap noCup), OmissionZStarRow.Zs_card] at h1
  have h2 : (OmissionZStarRow.zsOwners c noCap noCup).card ≤ B :=
    n66 _ (restrict c _) (restrict_no_cap c _ (OmissionZStarRow.zsOwners_no_cap c noCap noCup))
      (restrict_no_cup c _ (OmissionZStarRow.zsOwners_no_cup c noCap noCup)) (restrict_no_octagon c _ noOctagon)
  omega

/-- No 0/1 vector with h_0 = h_1 = 0 and at most `budget` holes satisfies the 3,131 rows, the Z-row and the
Z*-row, both rows with demand `r`. -/
def ExcludesHoleBudgetZZsN (r budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 252 → ℕ, holes 0 = 0 ∧ holes 1 = 0 ∧ (∀ i, holes i ≤ 1) ∧
    (∀ q, OmissionBalanced.demand q ≤ ∑ i ∈ OmissionBalanced.support q, holes i) ∧
    (∀ q, BalancedCoverCutsV2.demand q ≤ ∑ i ∈ BalancedCoverCutsV2.support q, holes i) ∧
    r ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ r ≤ ∑ i ∈ OmissionZStarRow.Zs, holes i ∧
    (∑ i, holes i) ≤ budget

theorem feasible_holes_zzsn {B : ℕ} (n66 : OmissionZRow.N66Bound B) {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) (hn : 2 ≤ n) :
    ∃ holes : Fin 252 → ℕ, holes 0 = 0 ∧ holes 1 = 0 ∧ (∀ i, holes i ≤ 1) ∧
      (∀ q, OmissionBalanced.demand q ≤ ∑ i ∈ OmissionBalanced.support q, holes i) ∧
      (∀ q, BalancedCoverCutsV2.demand q ≤ ∑ i ∈ BalancedCoverCutsV2.support q, holes i) ∧
      70 - B ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ 70 - B ≤ ∑ i ∈ OmissionZStarRow.Zs, holes i ∧
      (∑ i, holes i) + n = 252 := by
  classical
  let occupied := c.occupied noCap noCup
  have hb : ∀ i, (fun i => if i ∈ occupied then 0 else 1) i ≤ 1 := by
    intro i
    dsimp only
    split_ifs <;> omega
  have hr : ∀ q, OmissionBalanced.demand q ≤
      ∑ i ∈ OmissionBalanced.support q, (fun i => if i ∈ occupied then 0 else 1) i := by
    intro q
    simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      OmissionBalanced.all_geometric_rows c noCap noCup noOctagon q
  refine ⟨fun i => if i ∈ occupied then 0 else 1, ?_, ?_, hb, hr,
    BalancedCoverCutsV2.all_rows _ hb hr, ?_, ?_, ?_⟩
  · simp [occupied, OmissionBalancedZF.zero_mem_occupied c noCap noCup (by omega)]
  · simp [occupied, OmissionBalancedZF.one_mem_occupied c noCap noCup (by omega)]
  · simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      z_row_of n66 c noCap noCup noOctagon
  · simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      zs_row_of n66 c noCap noCup noOctagon
  · have hc := Finset.card_add_card_compl occupied
    have hn' : occupied.card = n := c.occupied_card noCap noCup
    have hh : (∑ i : Fin 252, if i ∈ occupied then 0 else 1) = occupiedᶜ.card := by
      simp [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, Finset.compl_eq_univ_sdiff]
    rw [hh]
    simp only [Fintype.card_fin] at hc
    omega

theorem balanced_bound_of_hole_budget_zzsn {B budget : ℕ} (small : budget ≤ 249)
    (n66 : OmissionZRow.N66Bound B) (verified : ExcludesHoleBudgetZZsN (70 - B) budget) :
    Partition.BalancedBound (251 - budget) := by
  intro n c noCap noCup noOctagon
  by_cases hn : 2 ≤ n
  · obtain ⟨holes, h0, h1, hb, hr, hcut, hz, hzs, hc⟩ :=
      feasible_holes_zzsn n66 c noCap noCup noOctagon hn
    by_contra h
    exact verified ⟨holes, h0, h1, hb, hr, hcut, hz, hzs, by omega⟩
  · omega

/-- Sanity link: with B = 55 the parametric statement is exactly the recorded `ExcludesHoleBudgetZZsF`. -/
theorem zzsn_55_iff (b : ℕ) :
    ExcludesHoleBudgetZZsN (70 - 55) b ↔ OmissionBalancedZZsF.ExcludesHoleBudgetZZsF b := Iff.rfl

/-- ES(8) ≤ 302 from a zero-side budget-69 tree with both rows at 16, a (not yet known) N66 ≤ 54, and the
residual half of the 307 chain. -/
theorem composition_302_n54 (trees : ExcludesHoleBudgetZZsN 16 69) (n66 : OmissionZRow.N66Bound 54)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 302 8 :=
  Partition.forces_of_population_bounds (by omega)
    (balanced_bound_of_hole_budget_zzsn (by norm_num) n66 trees) hR

/-- ES(8) ≤ 301 from a budget-70 tree with both rows at 17 and a (not yet known) N66 ≤ 53. -/
theorem composition_301_n53 (trees : ExcludesHoleBudgetZZsN 17 70) (n66 : OmissionZRow.N66Bound 53)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 301 8 :=
  Partition.forces_of_population_bounds (by omega)
    (balanced_bound_of_hole_budget_zzsn (by norm_num) n66 trees) hR

end OmissionBalancedZZsN

#print axioms OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn
#print axioms OmissionBalancedZZsN.composition_302_n54
#print axioms OmissionBalancedZZsN.composition_301_n53
