import N66R15Geo.Final
import N66G15.Facts

/-!
# Reviewer rv5: statement-fidelity compile for n66-l15-rows

Not part of the chain. Compiled once (unit `esr-ag-rv5-axioms`), bare v4.24.0 `lean -j1`, no `-o`, read-only
LEAN_PATH = the worker's `tools/env.sh` (review/env.sh). Sections:
1. statements as compiled (`#check`);
2. the definitions in the statements (`#print`);
3. reviewer's own hand-unfolded restatements (accepted only if definitionally equal to the compiled statements);
4. sizes evaluated by the kernel;
5. reviewer's own kernel negative controls in positive form (two corrupted copies of chunk 108);
6. COMPUTED cross-checks (`#eval`, interpreter; evidence only): dumps of `R1_15` and `leaves105`;
7. `#print axioms`.
-/

open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

/-! ## 1. Statements as compiled -/
#check @N66R15.n66_bound_54
#check @N66R15.n66_bound_55
#check @N66R15.cubesUnsat105R_of_texts
#check @N66R15.rowCertsUnsat_of_texts
#check @N66R15Geo.rowsValid_R15
#check @N66R15Geo.n66_bound_54_of_rows
#check @N66R15Geo.gaps_proved
#check @N66R15Enc.fullUnsat_of_text
#check @N66R15Enc.printClause_mem
#check @N66R15Geo.certUnsat_of_text
#check @N66R15Geo.subUnsat_of_text
#check @N66R15Chk.rowChunks_fst
#check @N66R15Chk.chkAll
#check @N66R15Chk.chk0
#check @N66R15Chk.chk108
#check @N66G15.leaves105_length
#check @N66E15.no_base_model

/-! ## 2. Definitions in the statements -/
#print OmissionZRow.N66Bound
#print N66R15Enc.CubesUnsat105R
#print N66R15Geo.RowCertsUnsat
#print N66R15Enc.R1_15
#print N66R15Enc.R1nat15
#print N66R15Enc.toFin70
#print N66R15Enc.R1arr
#print N66R15Enc.printClauses
#print N66R15Enc.certText
#print N66R15Enc.certCnf
#print N66R15Enc.subCnfChecked
#print N66E15.fullCnf
#print N66E15.fullS
#print N66E15.leaves105
#print N66E15.rowClause
#print N66E15.toDimacs
#print N66G15.RowsValid
#print N66G15.RowValid
#print N66G15.InClass
#print N66G15.n66Occ
#print EncB.DimacsSatisfiable
#print EncB.DimacsSat
#print N66R15Chk.chkRows
#print N66R15.n66_bound_55
set_option maxRecDepth 8000 in
#print N66R15Enc.rowsAll
set_option maxRecDepth 8000 in
#print N66R15Chk.rowChunks

/-! ## 3. Own hand-unfolded restatements -/

/-- The end theorem with `CubesUnsat105R`, `fullCnf`, `fullS`, `leaves105`, `R1_15`, `R1nat15`, `toFin70`,
`RowCertsUnsat`, `DimacsSatisfiable`, `DimacsSat` and `N66Bound` unfolded by hand. Accepted only if this type is
definitionally the compiled type of `N66R15.n66_bound_54`. -/
theorem rv5_end54_unfolded :
    (∀ c ∈ N66E15.tree15.leaves, ¬ ∃ ν : ℕ → Bool,
        ∀ cl ∈ (N66E15.eagerStream () ++ N66E15.quadStream ++ N66E15.fixedUnits ++ c.map N66E15.cubeUnit ++
            (N66R15Enc.rowsAll.flatten.map
              (fun T => T.map fun x => (⟨x % 70, Nat.mod_lt _ (by decide)⟩ : Fin 70))).map N66E15.rowClause ++
            N66E15.cardClauses ++ N66E15.sbClauses).map N66E15.toDimacs,
          ∃ l ∈ cl, (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) →
    ((∀ t ∈ N66R15Enc.templates, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66R15Enc.certCnf t, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) ∧
     (∀ k ∈ N66R15Enc.cores, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66R15Enc.certCnf k, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false))) →
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ 54 :=
  N66R15.n66_bound_54

/-- The same for `N66R15.n66_bound_55` (only the constant differs). -/
theorem rv5_end55_unfolded :
    (∀ c ∈ N66E15.tree15.leaves, ¬ ∃ ν : ℕ → Bool,
        ∀ cl ∈ (N66E15.eagerStream () ++ N66E15.quadStream ++ N66E15.fixedUnits ++ c.map N66E15.cubeUnit ++
            (N66R15Enc.rowsAll.flatten.map
              (fun T => T.map fun x => (⟨x % 70, Nat.mod_lt _ (by decide)⟩ : Fin 70))).map N66E15.rowClause ++
            N66E15.cardClauses ++ N66E15.sbClauses).map N66E15.toDimacs,
          ∃ l ∈ cl, (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) →
    ((∀ t ∈ N66R15Enc.templates, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66R15Enc.certCnf t, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) ∧
     (∀ k ∈ N66R15Enc.cores, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66R15Enc.certCnf k, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false))) →
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ 55 :=
  N66R15.n66_bound_55

/-- Contrapositive reading: under the two verdict hypotheses, 55 points force a 6-cap, a 6-cup or an octagon. -/
theorem rv5_contra (hc : N66R15Enc.CubesUnsat105R) (hr : N66R15Geo.RowCertsUnsat) :
    ∀ n (c : Configuration n), 55 ≤ n → ¬ N66G15.InClass c :=
  fun n c hn ⟨h1, h2, h3⟩ => absurd (N66R15.n66_bound_54 hc hr n c h1 h2 h3) (by omega)

/-- `RowsValid R1_15` unfolded: every row of the chunk constants is never fully occupied by the class. -/
theorem rv5_rows_unfolded (hr : N66R15Geo.RowCertsUnsat) :
    ∀ T ∈ N66R15Enc.rowsAll.flatten.map
        (fun T => T.map fun x => (⟨x % 70, Nat.mod_lt _ (by decide)⟩ : Fin 70)),
      ∀ n (c : Configuration n), (¬ c.HasCap 6 ∧ ¬ c.HasCup 6 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point)) →
        ∃ s ∈ T, ¬ ∃ v < n, N66G15.idxOf c.cup v = s.val :=
  N66R15Geo.rowsValid_R15 hr

/-! ## 4. Sizes, evaluated by the kernel -/
theorem rv5_chunks : N66R15Enc.rowsAll.length = 109 := by decide +kernel
theorem rv5_rowChunks : N66R15Chk.rowChunks.length = 109 := by decide +kernel
theorem rv5_rows : N66R15Enc.R1nat15.length = 10859 := by decide +kernel
theorem rv5_R1_15_length : N66R15Enc.R1_15.length = 10859 := by
  rw [N66R15Enc.R1_15, List.length_map]; exact rv5_rows
theorem rv5_templates : N66R15Enc.templates.length = 421 := by decide +kernel
theorem rv5_cores : N66R15Enc.cores.length = 208 := by decide +kernel
theorem rv5_idx208 : N66R15Enc.templates[208]? = some N66R15Enc.tmpl208 := rfl
theorem rv5_n208 : N66R15Enc.tmpl208.n = 29 := rfl
theorem rv5_leaves : N66E15.leaves105.length = 105 := N66G15.leaves105_length

/-! ## 5. Own kernel negative controls (positive form): corrupted copies of chunk 108 are rejected

`chk108 : chkRows rows108 just108 = true` is the chain's check. Here two copies of `rows108` with one row edited are
checked against the unchanged `just108`; the kernel evaluates the checker to `false`, so a chunk constant edited this
way could not carry `chk108` (`Bool.false_ne_true`). The `≠` facts show the edits change the data. -/

namespace N66R15Chk
open N66R15Enc

/-- Row 0 of chunk 108 (certificate `.mt 75 σ`) with its state 69 replaced by 68. -/
def rv5Bad0 : List (List Nat) := rows108.set 0 [33, 40, 41, 43, 47, 50, 51, 53, 57, 58, 61, 62, 64, 68]
/-- Row 38 of chunk 108 (certificate `.cy L`, an 8-cycle) with its state 64 replaced by 65. -/
def rv5Bad38 : List (List Nat) := rows108.set 38 [34, 40, 44, 46, 52, 53, 57, 65]

theorem rv5_bad0_rejected : chkRows rv5Bad0 just108 = false := by decide +kernel
theorem rv5_bad38_rejected : chkRows rv5Bad38 just108 = false := by decide +kernel
theorem rv5_bad0_ne : rv5Bad0 ≠ rows108 := by decide +kernel
theorem rv5_bad38_ne : rv5Bad38 ≠ rows108 := by decide +kernel
theorem rv5_row0_was : rows108[0]? = some [33, 40, 41, 43, 47, 50, 51, 53, 57, 58, 61, 62, 64, 69] := by
  decide +kernel
theorem rv5_row38_was : rows108[38]? = some [34, 40, 44, 46, 52, 53, 57, 64] := by decide +kernel

end N66R15Chk

/-! ## 6. COMPUTED cross-checks (interpreter; evidence only, not part of any proof) -/

#eval show IO Unit from do
  IO.FS.writeFile "/home/jay/research/data/formalize-20261122/n66-l15-rows/review/dump_R1_15.txt"
    (String.join (N66R15Enc.R1_15.map fun T => " ".intercalate (T.map fun s => toString s.val) ++ "\n"))
  IO.FS.writeFile "/home/jay/research/data/formalize-20261122/n66-l15-rows/review/dump_leaves105.txt"
    (String.join (N66E15.leaves105.map fun c =>
      " ".intercalate (c.map fun z => s!"{z.1.val}:{if z.2 then 1 else 0}") ++ "\n"))
  IO.println s!"dumped R1_15 ({N66R15Enc.R1_15.length} rows) and leaves105 ({N66E15.leaves105.length} leaves)"

/-! ## 7. Axioms -/
#print axioms N66R15.n66_bound_54
#print axioms N66R15.n66_bound_55
#print axioms N66R15.cubesUnsat105R_of_texts
#print axioms N66R15.rowCertsUnsat_of_texts
#print axioms N66R15Geo.n66_bound_54_of_rows
#print axioms N66R15Geo.gaps_proved
#print axioms N66R15Geo.rowsValid_R15
#print axioms N66R15Geo.chkRow_sound
#print axioms N66R15Geo.chkRows_mem
#print axioms N66R15Geo.certUnsat_of_text
#print axioms N66R15Geo.subUnsat_of_text
#print axioms N66R15Geo.certCnf_bounded
#print axioms N66R15Geo.rowValid_of_cert
#print axioms N66R15Geo.rowValid_sig
#print axioms N66R15Geo.rowValid_core
#print axioms N66R15Geo.rowValid_tau
#print axioms N66R15Geo.rowValid_cycle
#print axioms N66R15Geo.ttB_sound
#print axioms N66R15Geo.drB_sound
#print axioms N66R15Geo.canB_sound
#print axioms N66R15Enc.printClause_mem
#print axioms N66R15Enc.printClauses_mem
#print axioms N66R15Enc.fullUnsat_of_text
#print axioms N66E15.no_base_model
#print axioms N66R15Chk.rowChunks_fst
#print axioms N66R15Chk.chkAll
#print axioms N66R15Chk.chk0
#print axioms N66R15Chk.chk54
#print axioms N66R15Chk.chk108
#print axioms N66R15Chk.certsOkT
#print axioms N66R15Chk.certsOkC
#print axioms N66R15Chk.cores_isCore
#print axioms N66R15Chk.tt_all
#print axioms N66R15Chk.ps_all
#print axioms N66R15Chk.dr_all
#print axioms N66R15Chk.can_all
#print axioms N66G15.leaves105_length
#print axioms rv5_end54_unfolded
#print axioms rv5_end55_unfolded
#print axioms rv5_contra
#print axioms rv5_rows_unfolded
#print axioms rv5_chunks
#print axioms rv5_rowChunks
#print axioms rv5_rows
#print axioms rv5_R1_15_length
#print axioms rv5_templates
#print axioms rv5_cores
#print axioms rv5_idx208
#print axioms rv5_n208
#print axioms rv5_leaves
#print axioms N66R15Chk.rv5_bad0_rejected
#print axioms N66R15Chk.rv5_bad38_rejected
#print axioms N66R15Chk.rv5_bad0_ne
#print axioms N66R15Chk.rv5_bad38_ne
#print axioms N66R15Chk.rv5_row0_was
#print axioms N66R15Chk.rv5_row38_was
