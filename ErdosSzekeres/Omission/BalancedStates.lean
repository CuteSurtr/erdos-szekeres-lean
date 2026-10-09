/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, formal/sources/ES8BalancedStates.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Catalog data: CC BY 4.0; see docs/THIRD_PARTY.md.
Changes: local namespaces/imports, Lean/Mathlib 4.24 compatibility, kernel-only checks.
-/
import ErdosSzekeres.Omission.ActualRanks
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Data.Fintype.Pi

namespace ErdosSzekeres.Omission.ActualRanks

/-- The actual incoming state's column height, using every earlier owner. -/
noncomputable def column (cup : Nat → Nat → Nat → Bool) (v i : Nat) : Nat :=
  (Finset.range v).sup (fun u => if i+1 ≤ (labels cup u v).1 then (labels cup u v).2 else 0)

theorem column_antitone (cup : Nat → Nat → Nat → Bool) (v : Nat) :
    Antitone (column cup v) := by
  intro i j ij
  unfold column
  apply Finset.sup_le
  intro u hu
  by_cases big : j+1 ≤ (labels cup u v).1
  · have small : i+1 ≤ (labels cup u v).1 := by omega
    rw [if_pos big]
    exact Finset.le_sup_of_le hu (by rw [if_pos small])
  · rw [if_neg big]
    exact Nat.zero_le _

theorem column_le_five (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7)
    (v i : Nat) (hvn : v < n) : column cup v i ≤ 5 := by
  unfold column
  apply Finset.sup_le
  intro u hu
  have bd := balanced_label_bounds n cup caps cups u v (Finset.mem_range.mp hu) hvn
  split_ifs <;> omega

/-- Positive cell membership is exactly the column-height test. -/
theorem incoming_iff_column (cup : Nat → Nat → Nat → Bool) (v i b : Nat) (hb : 0 < b) :
    ErdosSzekeres.Omission.StateInterface.Incoming (labels cup) v (i+1,b) ↔ b ≤ column cup v i := by
  classical
  unfold ErdosSzekeres.Omission.StateInterface.Incoming column
  constructor
  · rintro ⟨u,hu,hcap,hcup⟩
    exact Finset.le_sup_of_le (Finset.mem_range.mpr hu) (by simpa [hcap] using hcup)
  · intro h
    obtain ⟨u,hu,high⟩ := (Finset.le_sup_iff hb).mp h
    by_cases hc : i+1 ≤ (labels cup u v).1
    · exact ⟨u,Finset.mem_range.mp hu,hc,by simpa [hc] using high⟩
    · simp only [if_neg hc] at high
      omega

abbrev FerrersState := {f : Fin 5 → Fin 6 // Antitone f}

noncomputable def balancedState (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (v : Fin n) : FerrersState :=
  ⟨fun i => ⟨column cup v i,by have := column_le_five n cup caps cups v i v.isLt; omega⟩,
   by intro i j h; exact column_antitone cup v h⟩

/-- Distinct actual owners have distinct finite Ferrers states. The separating
cell is their attained pair label; incomparable states receive no imposed order. -/
theorem balancedState_injective (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) :
    Function.Injective (balancedState n cup caps cups) := by
  have separate (u v : Fin n) (huv : u < v) :
      balancedState n cup caps cups u ≠ balancedState n cup caps cups v := by
    intro equal
    have adm := actual_incoming_admissible n cup u v huv v.isLt
    have bd := balanced_label_bounds n cup caps cups u v huv v.isLt
    let d := labels cup u v
    let i : Fin 5 := ⟨d.1-1,by dsimp [d]; omega⟩
    have cell : i.val+1=d.1 := by dsimp [i,d]; omega
    have colEqual : column cup u i = column cup v i := by
      have fEq := congrArg Subtype.val equal
      have e := congrFun fEq i
      exact congrArg Fin.val e
    have atV : d.2 ≤ column cup v i := by
      apply (incoming_iff_column cup v i d.2 (by dsimp [d]; omega)).mp
      simpa only [cell] using adm.1
    have atU : ErdosSzekeres.Omission.StateInterface.Incoming (labels cup) u (i.val+1,d.2) :=
      (incoming_iff_column cup u i d.2 (by dsimp [d]; omega)).mpr (colEqual ▸ atV)
    apply adm.2
    simpa only [cell] using atU
  intro u v equal
  by_contra ne
  rcases lt_or_gt_of_ne ne with h | h
  · exact separate u v h equal
  · exact separate v u h equal.symm

#print axioms balancedState_injective
end ErdosSzekeres.Omission.ActualRanks
