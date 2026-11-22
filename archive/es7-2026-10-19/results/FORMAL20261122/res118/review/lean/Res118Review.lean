/-
Reviewer's audit for res118-lean (slot lrev), 22 Nov 2026. ONE compile, read-only on every olean store, no olean
written. Sections: 1 axioms; 2 statements and definitions as stored in the oleans; 3 an independent restatement
(my own reading of what the trees and the row certificates state, F/Lo literals generated from the JSON states),
derived by the kernel from the worker's theorems; 4 data dumps from the oleans (compared with the JSON by
tools/rev_cmp_dumps.py; COMPUTED).
-/
import Res118.Final
import Res118.Compose304
import Res118.Adapter

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission

/-! ## 1. Axioms -/
#print axioms Res118.residual_bound_118_of_slices
#print axioms Res118.forces_304_of_slices
#print axioms Res118.residual_bound_118_of_blocks
#print axioms Res118.slice_false
#print axioms Res118.slice_of_root
#print axioms Res118.lo_row
#print axioms Res118.hLo
#print axioms Res118.hF18
#print axioms Res118.three_hF
#print axioms Res118.nine_mult
#print axioms Res118.nine_demands
#print axioms Res118.loOwners_no_cup
#print axioms Res118.loOwners_no_cap
#print axioms Res118.loOwners_card_le
#print axioms Res118.five_le_column_of_cup
#print axioms Res118.Lo_eq
#print axioms Res118.F_eq
#print axioms Res118.Lo_card
#print axioms Res118.F_card
#print axioms Res118.sum_Lo_add_sum_F
#print axioms Res118.rows_lengths
#print axioms Res118.BlockValid.append
#print axioms OmissionBalancedZ.composition_304_z
#print axioms OmissionResidual32Bridge2650.all_rows_2650
#print axioms OmissionResidual32Bridge2650.holes_sum_add_population
#print axioms OmissionResidualZeroState.zero_mem_residualOccupied
#print axioms ErdosSzekeres.Omission.Partition.forces_of_population_bounds

/-! ## 2. Stored statements and definitions -/
set_option pp.fullNames true in
#check @Res118.residual_bound_118_of_slices
set_option pp.fullNames true in
#check @Res118.forces_304_of_slices
set_option pp.fullNames true in
#check @Res118.slice_of_root
set_option pp.fullNames true in
#check @Res118.hF18
set_option pp.fullNames true in
#check @Res118.lo_row
set_option pp.fullNames true in
#print Res118.ResSliceExcludes
set_option pp.fullNames true in
#print Res118.ValidUnitRow
set_option pp.fullNames true in
#print Res118.BlockValid
set_option pp.fullNames true in
#print Res118.lsupp
set_option pp.fullNames true in
#print Res118.F
set_option pp.fullNames true in
#print Res118.Lo
set_option pp.fullNames true in
#print Res118.InLo
set_option pp.fullNames true in
#print Res118.loProfile
set_option pp.fullNames true in
#print Res118.SliceCatalog
set_option pp.fullNames true in
#print OmissionZRow.N66Bound
set_option pp.fullNames true in
#print ErdosSzekeres.Omission.Partition.ResidualBound
set_option pp.fullNames true in
#print OmissionBalancedZ.ExcludesHoleBudgetZ
set_option pp.fullNames true in
#print ErdosSzekeres.ForcesConvexNGon
set_option pp.fullNames true in
#print ErdosSzekeres.Omission.Configuration
set_option pp.fullNames true in
#print OmissionResidual32Transfer.holesOf
set_option pp.fullNames true in
#print ErdosSzekeres.Omission.Configuration.residualOccupied

/-! ## 3. Independent restatement -/
namespace Rev

/-- F = states with f1 >= 5, generated from source-2650.json.gz `states` (raw sha256 e800d5f8...). -/
def fIdx : List ℕ := [17, 25, 33, 34, 43, 44, 45, 53, 54, 55, 56, 64, 65, 66, 67, 68, 74, 75, 76, 77, 78, 79, 85, 86, 87, 88, 89, 90, 91, 95, 96, 97, 98, 99, 100, 101, 104, 105, 106, 107, 108, 109, 110, 111, 113, 114, 115, 116, 117, 118, 119, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153]
/-- Lo = states with f1 <= 4, generated from the same file. -/
def loIdx : List ℕ := [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 35, 36, 37, 38, 39, 40, 41, 42, 46, 47, 48, 49, 50, 51, 52, 57, 58, 59, 60, 61, 62, 63, 69, 70, 71, 72, 73, 80, 81, 82, 83, 84, 92, 93, 94, 102, 103, 112, 120]

theorem fIdx_eq : fIdx = Res118.fIndices := rfl
theorem loIdx_eq : loIdx = Res118.loIndices := rfl

/-- A literal support as a set of states. -/
def revSupp (l : List ℕ) : Finset (Fin 154) := Finset.univ.filter (fun i : Fin 154 => i.val ∈ l)

theorem S_f : revSupp fIdx = Res118.F := by
  ext i
  rw [Res118.F_eq, ← fIdx_eq]
  simp only [revSupp, Finset.mem_filter, Finset.mem_univ, true_and]

theorem S_lo : revSupp loIdx = Res118.Lo := by
  ext i
  rw [Res118.Lo_eq, ← loIdx_eq]
  simp only [revSupp, Finset.mem_filter, Finset.mem_univ, true_and]

/-- What a slice-tree replay checks (`check_tree` over constraints[0..2649] ++ extra rows of the slice file, budget B,
the replay envelope fixing state 0 occupied): no 0/1 vector with state 0 not a hole, all base rows, the capacity rows
(F, T) and (Lo, B - T), every unit row, and at most B holes. -/
def TreeSystem (units : List (List ℕ)) (B T : ℕ) : Prop :=
  ¬ ∃ h : Fin 154 → ℕ, (∀ i, h i ≤ 1) ∧ h 0 = 0 ∧
    (∀ r : Fin 2650, OmissionResidual32Bridge2650.demand2650 r ≤
      ∑ i ∈ OmissionResidual32Bridge2650.support2650 r, h i) ∧
    T ≤ ∑ i ∈ revSupp fIdx, h i ∧ B - T ≤ ∑ i ∈ revSupp loIdx, h i ∧
    (∀ s ∈ units, 1 ≤ ∑ i ∈ revSupp s, h i) ∧ ∑ i, h i ≤ B

/-- What an UNSAT support CNF certifies (VERIFY309N link (c)): no actual residual configuration occupies every state of
the support. No `0 < n` premise. -/
def RowHolds (s : List ℕ) : Prop :=
  ∀ n (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOct : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJ : Subsets.NoJunctionOn c.cup (Finset.range n)),
    ¬ revSupp s ⊆ c.residualOccupied noCap noOct noJ

theorem S_eq_lsupp (s : List ℕ) : revSupp s = Res118.lsupp s := rfl

theorem excl_of_tree {units : List (List ℕ)} {B T : ℕ} (h : TreeSystem units B T) :
    Res118.ResSliceExcludes units B T := by
  rintro ⟨x, hb, h0, hr, hT, hL, hu, hB⟩
  refine h ⟨x, hb, h0, hr, ?_, ?_, ?_, hB⟩
  · rw [S_f]; exact hT
  · rw [S_lo]; exact hL
  · first
    | exact hu
    | (intro s hs; rw [S_eq_lsupp]; exact hu s hs)

/-- The library definitions, unfolded (definitional). -/
theorem residualBound_unfold (B : ℕ) : Partition.ResidualBound B ↔
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ HasConvexNGon 8 (Finset.univ.image c.point) →
      Subsets.NoJunctionOn c.cup (Finset.range n) → n ≤ B := Iff.rfl

theorem n66_unfold (B : ℕ) : OmissionZRow.N66Bound B ↔
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ B := Iff.rfl

theorem forces_unfold (N k : ℕ) : ForcesConvexNGon N k ↔
    ∀ s : Finset Point, GeneralPosition s → N ≤ s.card → HasConvexNGon k s := Iff.rfl

theorem valid_of_holds {s : List ℕ} (h : RowHolds s) : Res118.ValidUnitRow s := by
  intro n c noCap noOct noJ _
  have hne := h n c noCap noOct noJ
  rw [OmissionResidual32Transfer.holesOf_sum]
  first
  | exact Finset.one_le_card.mpr (Finset.sdiff_nonempty.mpr hne)
  | exact Finset.card_pos.mpr (Finset.sdiff_nonempty.mpr hne)
  | (by_contra hc
     have h0 : (Res118.lsupp s \ c.residualOccupied noCap noOct noJ).card = 0 := by omega
     rw [Finset.card_eq_zero, Finset.sdiff_eq_empty_iff_subset] at h0
     exact hne h0)

/-- ResidualBound 118 from my reading of the evidence (unfolded form: `residualBound_unfold`). -/
theorem rev_residual_118
    (n66 : OmissionZRow.N66Bound 55)
    (rowsOK : ∀ s ∈ Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU ++ Res118.rowsA, RowHolds s)
    (t33_18 : TreeSystem [] 33 18)
    (t34_18 : TreeSystem (Res118.rowsP ++ Res118.rowsQ) 34 18)
    (t34_19 : TreeSystem Res118.rowsP 34 19)
    (t35_18 : TreeSystem (Res118.rowsP ++ Res118.rowsQ) 35 18)
    (t35_19 : TreeSystem (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t35_20 : TreeSystem (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    Partition.ResidualBound 118 :=
  Res118.residual_bound_118_of_slices n66
    (fun s hs => valid_of_holds (rowsOK s
      (List.mem_append_left _ (List.mem_append_left _ (List.mem_append_left _ hs)))))
    (fun s hs => valid_of_holds (rowsOK s
      (List.mem_append_left _ (List.mem_append_left _ (List.mem_append_right _ hs)))))
    (fun s hs => valid_of_holds (rowsOK s (List.mem_append_left _ (List.mem_append_right _ hs))))
    (fun s hs => valid_of_holds (rowsOK s (List.mem_append_right _ hs)))
    (excl_of_tree t33_18) (excl_of_tree t34_18) (excl_of_tree t34_19)
    (excl_of_tree t35_18) (excl_of_tree t35_19) (excl_of_tree t35_20)

/-- ES(8) <= 304 from the same readings plus the two hypotheses of composition_304_z, through the worker's corollary. -/
theorem rev_304
    (trees : OmissionBalancedZ.ExcludesHoleBudgetZ 67)
    (n66 : OmissionZRow.N66Bound 55)
    (rowsOK : ∀ s ∈ Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU ++ Res118.rowsA, RowHolds s)
    (t33_18 : TreeSystem [] 33 18)
    (t34_18 : TreeSystem (Res118.rowsP ++ Res118.rowsQ) 34 18)
    (t34_19 : TreeSystem Res118.rowsP 34 19)
    (t35_18 : TreeSystem (Res118.rowsP ++ Res118.rowsQ) 35 18)
    (t35_19 : TreeSystem (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t35_20 : TreeSystem (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  Res118.forces_304_of_slices trees n66
    (fun s hs => valid_of_holds (rowsOK s
      (List.mem_append_left _ (List.mem_append_left _ (List.mem_append_left _ hs)))))
    (fun s hs => valid_of_holds (rowsOK s
      (List.mem_append_left _ (List.mem_append_left _ (List.mem_append_right _ hs)))))
    (fun s hs => valid_of_holds (rowsOK s (List.mem_append_left _ (List.mem_append_right _ hs))))
    (fun s hs => valid_of_holds (rowsOK s (List.mem_append_right _ hs)))
    (excl_of_tree t33_18) (excl_of_tree t34_18) (excl_of_tree t34_19)
    (excl_of_tree t35_18) (excl_of_tree t35_19) (excl_of_tree t35_20)

end Rev

#print axioms Rev.fIdx_eq
#print axioms Rev.loIdx_eq
#print axioms Rev.S_f
#print axioms Rev.S_lo
#print axioms Rev.excl_of_tree
#print axioms Rev.valid_of_holds
#print axioms Rev.rev_residual_118
#print axioms Rev.rev_304
#print axioms Rev.S_eq_lsupp
#print axioms Rev.residualBound_unfold
#print axioms Rev.n66_unfold
#print axioms Rev.forces_unfold

/-! ## 4. Data dumps from the oleans (COMPUTED; compared with the JSON outside Lean) -/
#eval IO.println s!"REV_FIDX {Res118.fIndices}"
#eval IO.println s!"REV_LOIDX {Res118.loIndices}"
#eval IO.println s!"REV_FSET {((List.finRange 154).filter (fun i => decide (i ∈ Res118.F))).map (fun i => i.val)}"
#eval IO.println s!"REV_LOSET {((List.finRange 154).filter (fun i => decide (i ∈ Res118.Lo))).map (fun i => i.val)}"
#eval IO.println s!"REV_ROWSP {Res118.rowsP}"
#eval IO.println s!"REV_ROWSQ {Res118.rowsQ}"
#eval IO.println s!"REV_ROWSU {Res118.rowsU}"
#eval IO.println s!"REV_ROWSA {Res118.rowsA}"
#eval IO.println s!"REV_CATALOG {ErdosSzekeres.Omission.ResidualCatalog.catalog}"
#eval IO.println s!"REV_BASE {(List.finRange 2650).map (fun r => (((List.finRange 154).filter (fun i => decide (i ∈ OmissionResidual32Bridge2650.support2650 r))).map (fun i => i.val), OmissionResidual32Bridge2650.demand2650 r))}"
#eval IO.println "REV_END"
