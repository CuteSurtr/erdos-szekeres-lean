import N66R15Geo.Final

/-!
# Statement check (not part of the chain; compiled without -o)

Prints the compiled end statements and the definitions in them, restates the end theorem with the logical wrappers
unfolded by hand (accepted only if definitionally the compiled statement), evaluates list lengths in the kernel, and
re-prints the axioms of the key declarations.
-/

open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

/-! ## 1. Statements as compiled -/
#check @N66R15.n66_bound_54
#check @N66R15.n66_bound_55
#check @N66R15.cubesUnsat105R_of_texts
#check @N66R15.rowCertsUnsat_of_texts
#check @N66R15Geo.rowsValid_R15
#check @N66R15Geo.n66_bound_54_of_rows
#check @N66R15Enc.fullUnsat_of_text
#check @N66R15Geo.certUnsat_of_text
#check @N66R15Geo.subUnsat_of_text
#check @N66R15Chk.rowChunks_fst

/-! ## 2. Definitions in the statements -/
#print OmissionZRow.N66Bound
#print N66R15Enc.CubesUnsat105R
#print N66R15Geo.RowCertsUnsat
#print N66R15Enc.R1_15
#print N66R15Enc.R1nat15
#print N66R15Enc.toFin70
#print N66E15.fullCnf
#print N66E15.fullS
#print N66G15.RowsValid
#print N66G15.RowValid
#print N66G15.InClass
#print EncB.DimacsSatisfiable
#print EncB.DimacsSat

/-! ## 3. Hand-unfolded restatement (data and CNF terms kept: `leaves105`, `fullCnf`, `R1_15`, `templates`, `cores`,
`certCnf`, and the library's `Configuration`/`HasCap`/`HasCup`/`HasConvexNGon`). -/
theorem check_end_unfolded :
    (∀ c ∈ N66E15.leaves105, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66E15.fullCnf N66R15Enc.R1_15 c, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) →
    ((∀ t ∈ N66R15Enc.templates, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66R15Enc.certCnf t, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)) ∧
     (∀ k ∈ N66R15Enc.cores, ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ N66R15Enc.certCnf k, ∃ l ∈ cl,
        (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false))) →
    ∀ n (c : Configuration n), ¬ c.HasCap 6 → ¬ c.HasCup 6 →
      ¬ HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ 54 :=
  N66R15.n66_bound_54

/-- `R1_15` is literally the chunk constants read as states. -/
theorem check_R1_15_unfolded :
    N66R15Enc.R1_15 = N66R15Enc.rowsAll.flatten.map
      (fun T => T.map fun x => (⟨x % 70, Nat.mod_lt _ (by decide)⟩ : Fin 70)) := rfl

/-! ## 4. Sizes, evaluated by the kernel -/
theorem check_chunks : N66R15Enc.rowsAll.length = 109 := by decide +kernel
theorem check_rows : N66R15Enc.R1nat15.length = 10859 := by decide +kernel
theorem check_templates : N66R15Enc.templates.length = 421 := by decide +kernel
theorem check_cores : N66R15Enc.cores.length = 208 := by decide +kernel
theorem check_idx208 : N66R15Enc.templates[208]? = some N66R15Enc.tmpl208 := by rfl
theorem check_n208 : N66R15Enc.tmpl208.n = 29 := by rfl

/-! ## 5. Axioms -/
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
#print axioms N66R15Geo.rowValid_of_cert
#print axioms N66R15Geo.rowValid_tau
#print axioms N66R15Geo.rowValid_cycle
#print axioms N66R15Geo.ttB_sound
#print axioms N66R15Enc.printClause_mem
#print axioms N66R15Enc.fullUnsat_of_text
#print axioms N66R15Chk.rowChunks_fst
#print axioms N66R15Chk.chkAll
#print axioms N66R15Chk.chk0
#print axioms N66R15Chk.chk108
#print axioms N66R15Chk.certsOkT
#print axioms N66R15Chk.certsOkC
#print axioms N66R15Chk.cores_isCore
#print axioms N66R15Chk.tt_all
#print axioms N66R15Chk.ps_all
#print axioms N66R15Chk.dr_all
#print axioms N66R15Chk.can_all
#print axioms check_end_unfolded
#print axioms check_R1_15_unfolded
#print axioms check_chunks
#print axioms check_rows
#print axioms check_templates
#print axioms check_cores
