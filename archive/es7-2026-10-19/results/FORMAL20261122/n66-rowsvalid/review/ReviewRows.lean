import RowGeo.End

/-!
# Review of item n66-rowsvalid (statement fidelity; slot lrv3, 22 Nov 2026)

Loads the worker's clean-rebuild oleans (`build2/olean`) read-only and writes no olean. It prints the compiled
statements and the definitions in them, restates the deliverables with the logical wrappers unfolded by hand (each
accepted only if it is definitionally the compiled statement), checks that `RowCertsUnsat` follows from exactly the
628 full-text verdicts plus the trimmed T208 verdict (`review_discharge`), evaluates three list lengths in the
kernel, re-runs `#print axioms`, and dumps `R1` and the certificate sizes for the reviewer's own Python.
-/

open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

/-! ## 1. Statements as compiled -/
#check @RowGeo.n66_bound_55_of_cubes_rows
#check @RowGeo.rowsValid_R0
#check @RowGeo.rowsValid_R1
#check @RowGeo.certUnsat_of_text
#check @RowGeo.subUnsat_of_text
#check @RowGeo.chkRow_sound
#check @N66Geo.n66_bound_55_of_cubes

/-! ## 2. Definitions in the statements -/
#print RowGeo.RowCertsUnsat
#print RowGeo.R0Parse
#print RowGeo.R1
#print RowGeo.toFin70
#print RowChk.R1nat
#print RowEnc.certCnf
#print RowEnc.certText
#print RowEnc.subCnfChecked
#print RowEnc.Cert
#print RowEnc.nvOf
#print RowEnc.certOk
#print RowChk.coreOk
#print N66Geo.RowsValid
#print N66Geo.RowValid
#print N66Geo.InClass
#print N66Geo.n66Occ
#print N66Geo.idxOf
#print N66Geo.profOf
#print N66Enc.CubesUnsat132
#print N66Enc.R0
#print EncB.DimacsSatisfiable
#print EncB.DimacsSat
#print OmissionZRow.N66Bound

/-! ## 3. Hand-unfolded restatements (accepted iff definitionally equal to the compiled statements).
Kept as they are: the data and CNF terms `N66Enc.leaves132`, `N66Enc.fullCnf`, `N66Enc.R0`, `N66Enc.stateList`,
`RowEnc.templates`, `RowEnc.cores`, `RowEnc.certCnf`, `RowGeo.R1`, and the library's `column` / `Configuration` /
`HasCap` / `HasCup` / `HasConvexNGon`. -/

theorem review_end_unfolded :
    (∀ c ∈ N66Enc.leaves132, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66Enc.fullCnf N66Enc.R0 c, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) →
    ((∀ t ∈ RowEnc.templates, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ RowEnc.certCnf t, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) ∧
     (∀ k ∈ RowEnc.cores, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ RowEnc.certCnf k, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false))) →
    N66Enc.R0 = RowGeo.R1 →
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ 55 :=
  RowGeo.n66_bound_55_of_cubes_rows

theorem review_rowsR1_unfolded :
    ((∀ t ∈ RowEnc.templates, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ RowEnc.certCnf t, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) ∧
     (∀ k ∈ RowEnc.cores, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ RowEnc.certCnf k, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false))) →
    ∀ T ∈ RowGeo.R1, ∀ n (c : Configuration n),
      (¬ c.HasCap 6 ∧ ¬ c.HasCup 6 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point)) →
      ∃ s ∈ T, ¬ ∃ v < n, N66Enc.stateList.idxOf
        (ErdosSzekeres.Omission.ActualRanks.column c.cup v 0,
         ErdosSzekeres.Omission.ActualRanks.column c.cup v 1,
         ErdosSzekeres.Omission.ActualRanks.column c.cup v 2,
         ErdosSzekeres.Omission.ActualRanks.column c.cup v 3) = s.val :=
  RowGeo.rowsValid_R1

theorem review_rowsR0_unfolded :
    ((∀ t ∈ RowEnc.templates, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ RowEnc.certCnf t, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) ∧
     (∀ k ∈ RowEnc.cores, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ RowEnc.certCnf k, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false))) →
    N66Enc.R0 = RowGeo.R1 →
    ∀ T ∈ N66Enc.R0, ∀ n (c : Configuration n),
      (¬ c.HasCap 6 ∧ ¬ c.HasCup 6 ∧ ¬ HasConvexNGon 8 (Finset.univ.image c.point)) →
      ∃ s ∈ T, ¬ ∃ v < n, N66Enc.stateList.idxOf
        (ErdosSzekeres.Omission.ActualRanks.column c.cup v 0,
         ErdosSzekeres.Omission.ActualRanks.column c.cup v 1,
         ErdosSzekeres.Omission.ActualRanks.column c.cup v 2,
         ErdosSzekeres.Omission.ActualRanks.column c.cup v 3) = s.val :=
  RowGeo.rowsValid_R0

/-- `R1` is literally the chunk constants (checked by the kernel in `RowChk.Rows*`) read as states. -/
theorem review_R0Parse_unfolded :
    RowGeo.R0Parse ↔
      N66Enc.R0 = RowChk.R1nat.map (fun T => T.map fun x => (⟨x % 70, Nat.mod_lt _ (by decide)⟩ : Fin 70)) :=
  Iff.rfl

/-! ## 4. `RowCertsUnsat` from exactly the verdict shapes that E1-E3 deliver: the full printed text for every
template except T208 and for every core, and a printed sub-list (any index list) for T208. -/

theorem review_idx208 : RowEnc.templates[208]? = some RowEnc.tmpl208 := by rfl

theorem review_n208 : RowEnc.tmpl208.n = 29 := by rfl

theorem review_discharge
    (hT : ∀ t ∈ RowEnc.templates, t = RowEnc.tmpl208 ∨
      ∀ nv F, EncB.parseDimacs (RowEnc.certText t) = some (nv, F) → ¬ EncB.DimacsSatisfiable F)
    (h208 : ∃ (idx : List ℕ) (F : List (List Int)), RowEnc.subCnfChecked RowEnc.tmpl208 idx = some F ∧
      ∀ nv G, EncB.parseDimacs (EncB.render (RowEnc.nvOf RowEnc.tmpl208.n) F) = some (nv, G) →
        ¬ EncB.DimacsSatisfiable G)
    (hC : ∀ k ∈ RowEnc.cores,
      ∀ nv F, EncB.parseDimacs (RowEnc.certText k) = some (nv, F) → ¬ EncB.DimacsSatisfiable F) :
    RowGeo.RowCertsUnsat := by
  refine ⟨fun t ht => ?_, fun k hk => ?_⟩
  · have hok : RowEnc.certOk t = true := List.all_eq_true.1 RowChk.certsOkT t ht
    rcases hT t ht with h | h
    · subst h
      obtain ⟨idx, F, hs, hv⟩ := h208
      exact RowGeo.subUnsat_of_text hok hs hv
    · exact RowGeo.certUnsat_of_text hok h
  · have hk' : RowChk.coreOk k = true := List.all_eq_true.1 RowChk.certsOkC k hk
    have hok : RowEnc.certOk k = true := by
      first
        | exact ((Bool.and_eq_true _ _).1 hk').1
        | (simp only [RowChk.coreOk, Bool.and_eq_true] at hk'; exact hk'.1)
    exact RowGeo.certUnsat_of_text hok (hC k hk)

/-! ## 5. List lengths, evaluated by the kernel (M9 printed indices 0..420 and 0..207). -/
theorem review_templates_length : RowEnc.templates.length = 421 := by decide +kernel
theorem review_cores_length : RowEnc.cores.length = 208 := by decide +kernel
theorem review_chunks_length : RowChk.rowChunks.length = 119 := by decide +kernel

/-! ## 6. Axioms -/
#print axioms RowGeo.n66_bound_55_of_cubes_rows
#print axioms RowGeo.rowsValid_R0
#print axioms RowGeo.rowsValid_R1
#print axioms RowGeo.certUnsat_of_text
#print axioms RowGeo.subUnsat_of_text
#print axioms RowGeo.certCnf_bounded
#print axioms RowGeo.chkRow_sound
#print axioms RowGeo.chkRows_mem
#print axioms RowGeo.rowValid_sig
#print axioms RowGeo.rowValid_core
#print axioms RowGeo.rowValid_of_cert
#print axioms RowGeo.certCnf_sat
#print axioms RowGeo.rowValid_tau
#print axioms RowGeo.rowValid_cycle
#print axioms RowGeo.allTests_good
#print axioms RowGeo.sat_oct
#print axioms RowGeo.no_eight
#print axioms RowGeo.ttQ_eq
#print axioms RowGeo.ttB_sound
#print axioms RowGeo.drB_sound
#print axioms RowGeo.canB_sound
#print axioms RowGeo.goodN_sound
#print axioms RowChk.chkAll
#print axioms RowChk.chk0
#print axioms RowChk.chk118
#print axioms RowChk.certsOkT
#print axioms RowChk.certsOkC
#print axioms RowChk.cores_isCore
#print axioms RowChk.tt_all
#print axioms RowChk.ps_all
#print axioms RowChk.dr_all
#print axioms RowChk.can_all
#print axioms N66Geo.n66_bound_55_of_cubes
#print axioms N66Geo.mirror_holds
#print axioms review_end_unfolded
#print axioms review_rowsR1_unfolded
#print axioms review_rowsR0_unfolded
#print axioms review_R0Parse_unfolded
#print axioms review_idx208
#print axioms review_n208
#print axioms review_discharge
#print axioms review_templates_length
#print axioms review_cores_length
#print axioms review_chunks_length

/-! ## 7. Data dumps (interpreter; not evidence by themselves; compared with n66enc's rows file and the M9
manifest by the reviewer's own Python). -/
def reviewOut : String := "/home/jay/research/data/formalize-20261122/n66-rowsvalid/review/"

#eval show IO Unit from do
  IO.FS.writeFile (reviewOut ++ "dump_R1.txt") <|
    String.intercalate "\n" (RowGeo.R1.map fun T => " ".intercalate (T.map fun s => toString s.val)) ++ "\n"
  IO.FS.writeFile (reviewOut ++ "dump_templates.txt") <|
    String.intercalate "\n" (RowEnc.templates.map fun t =>
      s!"{t.n} {t.tests.length} {(t.octs.map List.length).getD 0} {t.octs.isNone}") ++ "\n"
  IO.FS.writeFile (reviewOut ++ "dump_cores.txt") <|
    String.intercalate "\n" (RowEnc.cores.map fun k =>
      match k with
      | .core S o => s!"{S.length} {(o.map List.length).getD 0} {o.isNone} {" ".intercalate (S.map fun s => toString s.val)}"
      | .tmpl _ _ _ => "TEMPLATE-IN-CORES") ++ "\n"
  IO.println s!"R1 {RowGeo.R1.length} templates {RowEnc.templates.length} cores {RowEnc.cores.length} chunks {RowChk.rowChunks.length}"
