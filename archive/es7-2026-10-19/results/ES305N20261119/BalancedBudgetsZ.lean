/-
ES305N20261119: the balanced hole budget with the Z-row, and the ES(8) ≤ 305 composition in Lean.

Compiled against the chain311 oleans of the ES(8) ≤ 310/311 compact pipeline:
- `BalancedRows` (`OmissionBalanced.all_geometric_rows`: 2,685 geometric rows) and `BalancedCoverCutsV2`
  (`all_rows`: 446 cover cuts) are together the 3,131 rows of balanced-v2-source.json, in the same order
  (checked by `leanz/rows_match.py`);
- `LemmaZ` (this record) gives the Z-row from `N66Bound 55`.
The only hypotheses left are the three non-Lean inputs:
- `ExcludesHoleBudgetZ 66`: the budget-66 EXACT TREE (check_tree + balcheck, README §4);
- `N66Bound 55`: N66 ≤ 55, CERTIFIED by SAT/cake_lpr (N66N20261113);
- `ResidualBound 118`: the residual half of ES(8) ≤ 307 (ES307N20261118).
-/
import BalancedRows
import BalancedCoverCutsV2
import LemmaZ
import ErdosSzekeres.Omission.PopulationBounds

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission

namespace OmissionBalancedZ

/-- No 0/1 hole vector with at most `budget` holes satisfies the 3,131 catalog rows and the Z-row. -/
def ExcludesHoleBudgetZ (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
    (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
    (∀ r, BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, holes i) ∧
    15 ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ (∑ i, holes i) ≤ budget

/-- `OmissionBalanced.feasible_holes` with the cover cuts and the Z-row added. -/
theorem feasible_holes_z (n66 : OmissionZRow.N66Bound 55) {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
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
  refine ⟨fun i => if i ∈ occupied then 0 else 1, hb, hr, BalancedCoverCutsV2.all_rows _ hb hr, ?_, ?_⟩
  · simpa [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, occupied] using
      OmissionZRow.z_row n66 c noCap noCup noOctagon
  · have hc := Finset.card_add_card_compl occupied
    have hn : occupied.card = n := c.occupied_card noCap noCup
    have hh : (∑ i : Fin 252, if i ∈ occupied then 0 else 1) = occupiedᶜ.card := by
      simp [Finset.sum_ite, Finset.filter_notMem_eq_sdiff, Finset.compl_eq_univ_sdiff]
    rw [hh]
    simp only [Fintype.card_fin] at hc
    omega

theorem balanced_bound_of_hole_budget_z {budget : ℕ} (n66 : OmissionZRow.N66Bound 55)
    (verified : ExcludesHoleBudgetZ budget) : Partition.BalancedBound (251 - budget) := by
  intro n c noCap noCup noOctagon
  obtain ⟨holes, hb, hr, hcut, hz, hc⟩ := feasible_holes_z n66 c noCap noCup noOctagon
  by_contra h
  exact verified ⟨holes, hb, hr, hcut, hz, by omega⟩

/-- ES(8) ≤ 305 from its three non-Lean inputs. -/
theorem composition_305_z (trees : ExcludesHoleBudgetZ 66) (n66 : OmissionZRow.N66Bound 55)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 305 8 :=
  Partition.forces_of_population_bounds (by omega) (balanced_bound_of_hole_budget_z n66 trees) hR

/-- The same with budget 67 (gives 304). A theorem about the inputs, not a claim that they hold. -/
theorem composition_304_z (trees : ExcludesHoleBudgetZ 67) (n66 : OmissionZRow.N66Bound 55)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 304 8 :=
  Partition.forces_of_population_bounds (by omega) (balanced_bound_of_hole_budget_z n66 trees) hR

end OmissionBalancedZ

#print axioms OmissionBalancedZ.feasible_holes_z
#print axioms OmissionBalancedZ.composition_305_z
#print axioms OmissionBalancedZ.composition_304_z
