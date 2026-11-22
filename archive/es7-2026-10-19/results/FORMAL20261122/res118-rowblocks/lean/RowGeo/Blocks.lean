import RowGeo.Sound
import RowGeo.Text
import Res118.Final

/-!
# RowGeo.Blocks: the four row blocks of Res118 from per-row cake_lpr verdicts

* `RowsUnsat rows`: every row's coupled-row CNF `RowEnc.rowCnf s` is unsatisfiable. For the blocks this is one
  cake_lpr verdict per row (`s VERIFIED UNSAT` on the certified file whose bytes are `RowEnc.rowText s`, trust items
  E1-E6; hash binding `tools/hash_binding.py`, `logs/m9_binding.*`).
* `validUnitRow_of_unsat`, `blockValid_of_unsat`: Res118's `ValidUnitRow`/`BlockValid` from `missing_of_unsat`.
* `wf_P` … `wf_A`: every block row is a well-formed support (kernel check of the literal rows).
* `blockValid_P` … `blockValid_A` and `residual_bound_118_of_rows`: `Res118.residual_bound_118_of_slices` with
  the four `BlockValid` hypotheses replaced by `RowsUnsat`.
* `RowsTextUnsat rows`: every `parseDimacsBytes` parse of the UTF-8 bytes of `rowText s` (what `rowprint row B I`
  writes) is unsatisfiable: the meaning of the cake_lpr verdict on the certified file (E1-E3).
  `rowsUnsat_of_texts` (`RowGeo.Text.parseDimacsBytes_rowText`) and **`residual_bound_118_of_texts`**.
-/

namespace RowGeo
open RowEnc ErdosSzekeres ErdosSzekeres.Omission OmissionResidual32Transfer

/-- Every row of `rows` has an unsatisfiable coupled-row CNF (one cake_lpr verdict per row). -/
def RowsUnsat (rows : List (List ℕ)) : Prop := ∀ s ∈ rows, ¬ EncB.DimacsSatisfiable (rowCnf s)

theorem validUnitRow_of_unsat (s : List ℕ) (hs : WF s) (hU : ¬ EncB.DimacsSatisfiable (rowCnf s)) :
    Res118.ValidUnitRow s := by
  intro n c noCap noOctagon noJunction _
  obtain ⟨i, hi⟩ := missing_of_unsat s hs hU c noCap noOctagon noJunction
  have hmem : statesOf s hs.2.1 i ∈ Res118.lsupp s := by
    simp only [Res118.lsupp, Finset.mem_filter, Finset.mem_univ, true_and, statesOf]
    exact List.getElem_mem _
  have h1 : holesOf (c.residualOccupied noCap noOctagon noJunction) (statesOf s hs.2.1 i) = 1 := by
    simp only [holesOf, if_neg hi]
  calc 1 = holesOf (c.residualOccupied noCap noOctagon noJunction) (statesOf s hs.2.1 i) := h1.symm
    _ ≤ ∑ x ∈ Res118.lsupp s, holesOf (c.residualOccupied noCap noOctagon noJunction) x :=
      Finset.single_le_sum (fun _ _ => Nat.zero_le _) hmem

theorem blockValid_of_unsat (rows : List (List ℕ)) (hwf : ∀ s ∈ rows, WF s) (h : RowsUnsat rows) :
    Res118.BlockValid rows :=
  fun s hs => validUnitRow_of_unsat s (hwf s hs) (h s hs)

set_option maxRecDepth 100000 in
theorem wf_P : ∀ s ∈ Res118.rowsP, WF s := by decide +kernel
set_option maxRecDepth 100000 in
theorem wf_Q : ∀ s ∈ Res118.rowsQ, WF s := by decide +kernel
set_option maxRecDepth 100000 in
theorem wf_U : ∀ s ∈ Res118.rowsU, WF s := by decide +kernel
set_option maxRecDepth 100000 in
theorem wf_A : ∀ s ∈ Res118.rowsA, WF s := by decide +kernel

theorem blockValid_P (h : RowsUnsat Res118.rowsP) : Res118.BlockValid Res118.rowsP := blockValid_of_unsat _ wf_P h
theorem blockValid_Q (h : RowsUnsat Res118.rowsQ) : Res118.BlockValid Res118.rowsQ := blockValid_of_unsat _ wf_Q h
theorem blockValid_U (h : RowsUnsat Res118.rowsU) : Res118.BlockValid Res118.rowsU := blockValid_of_unsat _ wf_U h
theorem blockValid_A (h : RowsUnsat Res118.rowsA) : Res118.BlockValid Res118.rowsA := blockValid_of_unsat _ wf_A h

/-- **`ResidualBound 118` with the four row blocks replaced by per-row CNF verdicts.** -/
theorem residual_bound_118_of_rows
    (n66 : OmissionZRow.N66Bound 55)
    (hP : RowsUnsat Res118.rowsP) (hQ : RowsUnsat Res118.rowsQ) (hU : RowsUnsat Res118.rowsU)
    (hA : RowsUnsat Res118.rowsA)
    (s33_18 : Res118.ResSliceExcludes [] 33 18)
    (s34_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18)
    (s34_19 : Res118.ResSliceExcludes Res118.rowsP 34 19)
    (s35_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    Partition.ResidualBound 118 :=
  Res118.residual_bound_118_of_slices n66 (blockValid_P hP) (blockValid_Q hQ) (blockValid_U hU) (blockValid_A hA)
    s33_18 s34_18 s34_19 s35_18 s35_19 s35_20

/-! ## From the printed bytes -/

/-- Every `parseDimacsBytes` parse of the bytes the exe writes for a row is unsatisfiable (for the four blocks: the
cake_lpr verdicts `s VERIFIED UNSAT` on the certified files, whose bytes are these, E1-E3). -/
def RowsTextUnsat (rows : List (List ℕ)) : Prop :=
  ∀ s ∈ rows, ∀ nv F, EncB.parseDimacsBytes (rowText s).toUTF8.data.toList = some (nv, F) →
    ¬ EncB.DimacsSatisfiable F

theorem rowsUnsat_of_texts {rows : List (List ℕ)} (h : RowsTextUnsat rows) : RowsUnsat rows :=
  fun s hs => rowUnsat_of_bytes s (h s hs)

/-- **`ResidualBound 118` from the six slice exclusions, `N66Bound 55` and the verdicts on the 2,025 printed row
texts.** -/
theorem residual_bound_118_of_texts
    (n66 : OmissionZRow.N66Bound 55)
    (hP : RowsTextUnsat Res118.rowsP) (hQ : RowsTextUnsat Res118.rowsQ) (hU : RowsTextUnsat Res118.rowsU)
    (hA : RowsTextUnsat Res118.rowsA)
    (s33_18 : Res118.ResSliceExcludes [] 33 18)
    (s34_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18)
    (s34_19 : Res118.ResSliceExcludes Res118.rowsP 34 19)
    (s35_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    Partition.ResidualBound 118 :=
  residual_bound_118_of_rows n66 (rowsUnsat_of_texts hP) (rowsUnsat_of_texts hQ) (rowsUnsat_of_texts hU)
    (rowsUnsat_of_texts hA) s33_18 s34_18 s34_19 s35_18 s35_19 s35_20

end RowGeo

/-- info: 'RowGeo.missing_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms RowGeo.missing_of_unsat
/-- info: 'RowGeo.blockValid_P' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms RowGeo.blockValid_P
/-- info: 'RowGeo.blockValid_Q' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms RowGeo.blockValid_Q
/-- info: 'RowGeo.blockValid_U' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms RowGeo.blockValid_U
/-- info: 'RowGeo.blockValid_A' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms RowGeo.blockValid_A
/-- info: 'RowGeo.residual_bound_118_of_rows' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms RowGeo.residual_bound_118_of_rows
/-- info: 'RowGeo.residual_bound_118_of_texts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms RowGeo.residual_bound_118_of_texts
#print axioms RowGeo.parseDimacsBytes_rowText
#print axioms RowGeo.rowsUnsat_of_texts
