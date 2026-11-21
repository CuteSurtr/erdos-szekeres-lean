-- AUXILIARY EXCERPT (lean-rebuild, 21 Nov 2026), NOT the record file: lines 12-62 of
-- ES305N20261119/FixedStatesZ.lean verbatim, with the imports BalancedRows and BalancedCoverCutsV2 dropped.
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

end OmissionBalancedZF

#print axioms OmissionBalancedZF.zero_mem_occupied
#print axioms OmissionBalancedZF.one_mem_occupied
