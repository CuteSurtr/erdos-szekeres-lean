/-
Reviewer's audit for res118-rowblocks (slot lrv3), 22 Nov 2026. ONE compile, no `-o` (no olean written), read-only
on every olean store (the worker's tools/env_geo.sh LEAN_PATH). Sections:
  1 axioms of every theorem in the worker result and of their main inputs;
  2 statements and definitions as stored in the oleans (pp.fullNames);
  3 data dumps from the oleans (interpreter; compared with `rowprint list` outside Lean, COMPUTED);
  4 my own reading, kernel-checked against the worker's theorems (definitional unfolding, short derivations);
  5 kernel checksums of Res118.rowsP/Q/U/A (values computed outside Lean from `rowprint list`);
  6 the interpreter's `RowEnc.rowText` of row U 0, written to review/data (compared with the exe's bytes outside Lean).
Nothing here evaluates `rowCnf` in the kernel.
-/
import RowGeo.Blocks

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission

/-! ## 1. Axioms -/
#print axioms RowGeo.missing_of_unsat
#print axioms RowGeo.blockValid_P
#print axioms RowGeo.blockValid_Q
#print axioms RowGeo.blockValid_U
#print axioms RowGeo.blockValid_A
#print axioms RowGeo.residual_bound_118_of_rows
#print axioms RowGeo.residual_bound_118_of_texts
#print axioms RowGeo.parseDimacsBytes_rowText
#print axioms RowGeo.parseDimacs_rowText
#print axioms RowGeo.rowsUnsat_of_texts
#print axioms RowGeo.rowUnsat_of_bytes
#print axioms RowGeo.validUnitRow_of_unsat
#print axioms RowGeo.blockValid_of_unsat
#print axioms RowGeo.wf_P
#print axioms RowGeo.wf_Q
#print axioms RowGeo.wf_U
#print axioms RowGeo.wf_A
#print axioms RowGeo.litsOk_of_wf
#print axioms RowGeo.stateTable_eq
#print axioms RowGeo.cup_label_le_h1
#print axioms RowGeo.positive_of_ttB
#print axioms RowGeo.bbox_valid
#print axioms RowGeo.bad4_invalid
#print axioms RowGeo.raw_holds
#print axioms RowGeo.rowCnf_sat
#print axioms RowGeo.finish_sat
#print axioms RowGeo.decodeWith_numWith
#print axioms RowGeo.clause_source
#print axioms RowGeo.clause_fixed_pos
#print axioms RowGeo.clause_fixed_neg
#print axioms RowGeo.clause_thresh
#print axioms RowGeo.statesOf_injective
#print axioms EncB.parseDimacs_render
#print axioms EncB.render_ascii
#print axioms EncB.renderCube_bytes
#print axioms EncB.ofNat_toUInt8_ascii
#print axioms Res118.residual_bound_118_of_slices
#print axioms Res118.rows_lengths

/-! ## 2. Stored statements and definitions -/
set_option pp.fullNames true in
#check @RowGeo.missing_of_unsat
set_option pp.fullNames true in
#check @RowGeo.blockValid_P
set_option pp.fullNames true in
#check @RowGeo.blockValid_Q
set_option pp.fullNames true in
#check @RowGeo.blockValid_U
set_option pp.fullNames true in
#check @RowGeo.blockValid_A
set_option pp.fullNames true in
#check @RowGeo.residual_bound_118_of_rows
set_option pp.fullNames true in
#check @RowGeo.residual_bound_118_of_texts
set_option pp.fullNames true in
#check @RowGeo.parseDimacsBytes_rowText
set_option pp.fullNames true in
#check @RowGeo.rowsUnsat_of_texts
set_option pp.fullNames true in
#check @RowGeo.rowUnsat_of_bytes
set_option pp.fullNames true in
#print RowGeo.RowsUnsat
set_option pp.fullNames true in
#print RowGeo.RowsTextUnsat
set_option pp.fullNames true in
#print RowGeo.WF
set_option pp.fullNames true in
#print RowGeo.statesOf
set_option pp.fullNames true in
#print EncB.DimacsSat
set_option pp.fullNames true in
#print EncB.DimacsSatisfiable
set_option pp.fullNames true in
#print EncB.parseDimacsBytes
set_option pp.fullNames true in
#print EncB.parseDimacsChars
set_option pp.fullNames true in
#print EncB.render
set_option pp.fullNames true in
#print RowEnc.rowText
set_option pp.fullNames true in
#print RowEnc.rowCnf
set_option pp.fullNames true in
#print RowEnc.rowNv
set_option pp.fullNames true in
#print Res118.ValidUnitRow
set_option pp.fullNames true in
#print Res118.BlockValid
set_option pp.fullNames true in
#print Res118.lsupp
set_option pp.fullNames true in
#print Res118.ResSliceExcludes
set_option pp.fullNames true in
#print OmissionResidual32Transfer.holesOf
set_option pp.fullNames true in
#print ErdosSzekeres.Omission.Partition.ResidualBound
set_option pp.fullNames true in
#print OmissionZRow.N66Bound
set_option pp.fullNames true in
#print ErdosSzekeres.Omission.Configuration.residualOccupied

/-! ## 3. Data dumps from the oleans (interpreter; COMPUTED) -/
#eval IO.println s!"LRV_LENGTHS {Res118.rowsP.length} {Res118.rowsQ.length} {Res118.rowsU.length} {Res118.rowsA.length}"
#eval IO.println s!"LRV_ROWSP {Res118.rowsP}"
#eval IO.println s!"LRV_ROWSQ {Res118.rowsQ}"
#eval IO.println s!"LRV_ROWSU {Res118.rowsU}"
#eval IO.println s!"LRV_ROWSA {Res118.rowsA}"

/-! ## 4. My own reading, kernel-checked -/
namespace Lrv

/-- What cake_lpr's `s VERIFIED UNSAT` asserts of the clause list `F` it read: no Boolean assignment of the variables
makes some literal of every clause true (DIMACS: `l > 0` is variable `l`, `l < 0` its negation). -/
def NoModel (F : List (List Int)) : Prop :=
  ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ F, ∃ l ∈ cl, (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)

theorem noModel_iff (F : List (List Int)) : NoModel F ↔ ¬ EncB.DimacsSatisfiable F := Iff.rfl

/-- The verdict on the bytes that `rowprint row B I` writes for `s = rows[I]` (`IO.FS.Stream.putStr` of `rowText s`
writes its UTF-8 bytes), read as `parseDimacsBytes` reads them. -/
def TextVerdict (s : List ℕ) : Prop :=
  ∀ nv F, EncB.parseDimacsBytes (RowEnc.rowText s).toUTF8.data.toList = some (nv, F) → NoModel F

theorem rowsTextUnsat_iff (rows : List (List ℕ)) :
    RowGeo.RowsTextUnsat rows ↔ ∀ s ∈ rows, TextVerdict s := Iff.rfl

theorem rowsUnsat_iff (rows : List (List ℕ)) :
    RowGeo.RowsUnsat rows ↔ ∀ s ∈ rows, NoModel (RowEnc.rowCnf s) := Iff.rfl

/-- The parse premise is never vacuous: the text form is exactly the CNF form. -/
theorem text_iff_rows (rows : List (List ℕ)) : RowGeo.RowsTextUnsat rows ↔ RowGeo.RowsUnsat rows := by
  refine ⟨RowGeo.rowsUnsat_of_texts, fun h s hs nv F hp => ?_⟩
  rw [RowGeo.parseDimacsBytes_rowText] at hp
  first
  | (cases hp; exact h s hs)
  | (simp only [Option.some.injEq, Prod.mk.injEq] at hp; obtain ⟨rfl, rfl⟩ := hp; exact h s hs)

/-- The per-row conclusion in my words: some state of the support is the residual state of no point. -/
def Misses (s : List ℕ) : Prop :=
  ∀ n (c : Configuration n) (noCap : ¬ c.HasCap 6) (noOct : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJ : Subsets.NoJunctionOn c.cup (Finset.range n)),
    ∃ x ∈ s, ∀ v : Fin n, (c.residualOwner noCap noOct noJ v).val ≠ x

theorem misses_of_unsat (s : List ℕ) (hs : RowGeo.WF s) (hU : NoModel (RowEnc.rowCnf s)) : Misses s := by
  intro n c noCap noOct noJ
  obtain ⟨i, hi⟩ := RowGeo.missing_of_unsat s hs hU c noCap noOct noJ
  refine ⟨s[i.val]'i.isLt, List.getElem_mem _, fun v hv => hi ?_⟩
  first
  | exact Finset.mem_image.mpr ⟨v, Finset.mem_univ _, Fin.ext hv⟩
  | (simp only [Configuration.residualOccupied, Finset.mem_image, Finset.mem_univ, true_and]
     exact ⟨v, Fin.ext hv⟩)

theorem block_own (rows : List (List ℕ)) (hwf : ∀ s ∈ rows, RowGeo.WF s)
    (h : ∀ s ∈ rows, TextVerdict s) : ∀ s ∈ rows, Misses s :=
  fun s hs => misses_of_unsat s (hwf s hs) (((text_iff_rows rows).1 h) s hs)

/-- The four blocks in my words, from the verdicts on the printed bytes. -/
theorem block_P_own (h : ∀ s ∈ Res118.rowsP, TextVerdict s) : ∀ s ∈ Res118.rowsP, Misses s :=
  block_own _ RowGeo.wf_P h
theorem block_Q_own (h : ∀ s ∈ Res118.rowsQ, TextVerdict s) : ∀ s ∈ Res118.rowsQ, Misses s :=
  block_own _ RowGeo.wf_Q h
theorem block_U_own (h : ∀ s ∈ Res118.rowsU, TextVerdict s) : ∀ s ∈ Res118.rowsU, Misses s :=
  block_own _ RowGeo.wf_U h
theorem block_A_own (h : ∀ s ∈ Res118.rowsA, TextVerdict s) : ∀ s ∈ Res118.rowsA, Misses s :=
  block_own _ RowGeo.wf_A h

/-- `blockValid_P` with `RowsUnsat`, `BlockValid`, `ValidUnitRow`, `lsupp` and `holesOf` unfolded (kernel defeq). -/
theorem blockValid_P_unfolded (h : ∀ s ∈ Res118.rowsP, NoModel (RowEnc.rowCnf s)) :
    ∀ s ∈ Res118.rowsP, ∀ n (c : Configuration n) (noCap : ¬ c.HasCap 6)
      (noOct : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
      (noJ : Subsets.NoJunctionOn c.cup (Finset.range n)), 0 < n →
        1 ≤ ∑ i ∈ Finset.univ.filter (fun i : Fin 154 => i.val ∈ s),
          (if i ∈ c.residualOccupied noCap noOct noJ then 0 else 1) :=
  RowGeo.blockValid_P h

/-- The goal of the item: `BlockValid` of each block from the verdicts on the printed bytes. -/
theorem blockValid_P_of_texts (h : RowGeo.RowsTextUnsat Res118.rowsP) : Res118.BlockValid Res118.rowsP :=
  RowGeo.blockValid_P (RowGeo.rowsUnsat_of_texts h)
theorem blockValid_Q_of_texts (h : RowGeo.RowsTextUnsat Res118.rowsQ) : Res118.BlockValid Res118.rowsQ :=
  RowGeo.blockValid_Q (RowGeo.rowsUnsat_of_texts h)
theorem blockValid_U_of_texts (h : RowGeo.RowsTextUnsat Res118.rowsU) : Res118.BlockValid Res118.rowsU :=
  RowGeo.blockValid_U (RowGeo.rowsUnsat_of_texts h)
theorem blockValid_A_of_texts (h : RowGeo.RowsTextUnsat Res118.rowsA) : Res118.BlockValid Res118.rowsA :=
  RowGeo.blockValid_A (RowGeo.rowsUnsat_of_texts h)

/-- `residual_bound_118_of_texts` with `ResidualBound` and `RowsTextUnsat` unfolded (kernel defeq). -/
theorem residual_own
    (n66 : OmissionZRow.N66Bound 55)
    (hP : ∀ s ∈ Res118.rowsP, TextVerdict s) (hQ : ∀ s ∈ Res118.rowsQ, TextVerdict s)
    (hU : ∀ s ∈ Res118.rowsU, TextVerdict s) (hA : ∀ s ∈ Res118.rowsA, TextVerdict s)
    (s33_18 : Res118.ResSliceExcludes [] 33 18)
    (s34_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18)
    (s34_19 : Res118.ResSliceExcludes Res118.rowsP 34 19)
    (s35_18 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 35 18)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ HasConvexNGon 8 (Finset.univ.image c.point) →
      Subsets.NoJunctionOn c.cup (Finset.range n) → n ≤ 118 :=
  RowGeo.residual_bound_118_of_texts n66 hP hQ hU hA s33_18 s34_18 s34_19 s35_18 s35_19 s35_20

/-! ## 5. Kernel checksums of the olean row lists -/

/-- Polynomial fingerprint mod 2^61 - 1 of a row list (lengths and entries, in order); tools/lrv_ck.py computes the
same function on the output of `rowprint list B`. -/
def ck (rows : List (List ℕ)) : ℕ :=
  rows.foldl (fun a s => s.foldl (fun b x => (b * 1000003 + x + 1) % 2305843009213693951)
    ((a * 1000033 + s.length + 7) % 2305843009213693951)) 0

set_option maxRecDepth 100000 in
theorem ck_P : ck Res118.rowsP = 1344959598462246673 := by decide +kernel
set_option maxRecDepth 100000 in
theorem ck_Q : ck Res118.rowsQ = 1417387261197172680 := by decide +kernel
set_option maxRecDepth 100000 in
theorem ck_U : ck Res118.rowsU = 767129163372159809 := by decide +kernel
set_option maxRecDepth 100000 in
theorem ck_A : ck Res118.rowsA = 2077712976096827448 := by decide +kernel

end Lrv

#print axioms Lrv.noModel_iff
#print axioms Lrv.rowsTextUnsat_iff
#print axioms Lrv.rowsUnsat_iff
#print axioms Lrv.text_iff_rows
#print axioms Lrv.misses_of_unsat
#print axioms Lrv.block_own
#print axioms Lrv.block_P_own
#print axioms Lrv.block_Q_own
#print axioms Lrv.block_U_own
#print axioms Lrv.block_A_own
#print axioms Lrv.blockValid_P_unfolded
#print axioms Lrv.blockValid_P_of_texts
#print axioms Lrv.blockValid_Q_of_texts
#print axioms Lrv.blockValid_U_of_texts
#print axioms Lrv.blockValid_A_of_texts
#print axioms Lrv.residual_own
#print axioms Lrv.ck_P
#print axioms Lrv.ck_Q
#print axioms Lrv.ck_U
#print axioms Lrv.ck_A

/-! ## 6. The interpreter's text of row U 0 (compared with the exe's bytes outside Lean) -/
#eval IO.FS.writeFile "/home/jay/research/data/formalize-20261122/res118-rowblocks/review/data/interp_U0.cnf"
  (RowEnc.rowText (Res118.rowsU.headD []))
#eval IO.println s!"LRV_U0 {Res118.rowsU.headD []}"
#eval IO.println "LRV_END"
