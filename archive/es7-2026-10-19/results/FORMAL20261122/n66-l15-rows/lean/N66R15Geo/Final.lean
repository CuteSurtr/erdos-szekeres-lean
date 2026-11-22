import N66R15Geo.End
import N66R15Geo.Bound
import N66R15Enc.Bridge

/-!
# N66R15.Final: `N66Bound 54` (and 55) modulo cake_lpr verdicts only

* `N66R15Enc.CubesUnsat105R`: for each of the 105 leaf cubes of the level-15 split tree, the relaxation
  `fullCnf R1_15 c` is unsatisfiable. Discharged outside the kernel by the 105 cake_lpr verdicts on the certified
  `trim.cnf` files: `N66R15Enc.fullUnsat_of_text` (each printed clause is in `fullCnf R1_15 c`; ENCBLEAN's proved
  DIMACS round trip) and the hash binding M9 (105/105), under trust items E1-E6.
* `N66R15Geo.RowCertsUnsat`: the 629 row-certificate CNFs (421 templates, 208 cores; `N66R15Enc.certCnf`) are
  unsatisfiable. Discharged by `certUnsat_of_text` (628 full CNFs) and `subUnsat_of_text` (template 208, whose
  certified file is a trimmed sub-CNF), the hash binding of the 629 printed texts and VB's cake_lpr verdicts.
* `R1_15` is the concatenation of the chunk constants the kernel checks; there is no parse hypothesis and no
  `RowsValid` hypothesis: `rowsValid_R15` proves `RowsValid R1_15` from `RowCertsUnsat`.
-/

namespace N66R15
open N66R15Enc N66R15Geo

/-- **`N66Bound 54`, Lean-checked modulo the 105 cube verdicts (`CubesUnsat105R`) and the 629 row-certificate
verdicts (`RowCertsUnsat`).** -/
theorem n66_bound_54 (hc : CubesUnsat105R) (hr : RowCertsUnsat) : OmissionZRow.N66Bound 54 :=
  n66_bound_54_of_rows hc (rowsValid_R15 hr)

/-- **`N66Bound 55`** (the hypothesis of the 304/303 chains and of Res118), from `N66Bound 54`. -/
theorem n66_bound_55 (hc : CubesUnsat105R) (hr : RowCertsUnsat) : OmissionZRow.N66Bound 55 :=
  fun n c h1 h2 h3 => Nat.le_succ_of_le (n66_bound_54 hc hr n c h1 h2 h3)


/-! ## The two hypotheses from exactly the verdict shapes that E1-E3 deliver -/

/-- `CubesUnsat105R` from one printed text per leaf: the exe printed `render nvHeader L` for some descriptor list
(`printClauses c ds = some L`, literals in range, both checked by the exe before writing), and every DIMACS parse of
that text is unsatisfiable (cake_lpr's verdict on the certified file whose bytes are this text, E1-E3). -/
theorem cubesUnsat105R_of_texts
    (h : ∀ c ∈ N66E15.leaves105, ∃ (ds : List Desc) (L : List (List Int)), printClauses c ds = some L ∧
      litsBounded N66E15.nvHeader L = true ∧
      ∀ nv F, EncB.parseDimacs (EncB.render N66E15.nvHeader L) = some (nv, F) → ¬ EncB.DimacsSatisfiable F) :
    CubesUnsat105R := by
  intro c hc
  obtain ⟨ds, L, hp, hb, hv⟩ := h c hc
  exact fullUnsat_of_text hp hb hv

/-- `RowCertsUnsat` from the verdicts on the printed texts: the full text of every template except T208 and of every
core, and a printed sub-list (any index list) of T208 (VB certified the `lrattrim` sub-CNF of the n = 29 template). -/
theorem rowCertsUnsat_of_texts
    (hT : ∀ t ∈ templates, t = tmpl208 ∨
      ∀ nv F, EncB.parseDimacs (certText t) = some (nv, F) → ¬ EncB.DimacsSatisfiable F)
    (h208 : ∃ (idx : List ℕ) (F : List (List Int)), subCnfChecked tmpl208 idx = some F ∧
      ∀ nv G, EncB.parseDimacs (EncB.render (nvOf tmpl208.n) F) = some (nv, G) → ¬ EncB.DimacsSatisfiable G)
    (hC : ∀ k ∈ cores, ∀ nv F, EncB.parseDimacs (certText k) = some (nv, F) → ¬ EncB.DimacsSatisfiable F) :
    RowCertsUnsat := by
  refine ⟨fun t ht => ?_, fun k hk => ?_⟩
  · have hok : certOk t = true := List.all_eq_true.1 N66R15Chk.certsOkT t ht
    rcases hT t ht with h | h
    · subst h
      obtain ⟨idx, F, hs, hv⟩ := h208
      exact subUnsat_of_text hok hs hv
    · exact certUnsat_of_text hok h
  · have hk' : N66R15Chk.coreOk k = true := List.all_eq_true.1 N66R15Chk.certsOkC k hk
    have hok : certOk k = true := by
      simp only [N66R15Chk.coreOk, Bool.and_eq_true] at hk'
      exact hk'.1
    exact certUnsat_of_text hok (hC k hk)

end N66R15

/-- info: 'N66R15.n66_bound_54' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms N66R15.n66_bound_54

/-- info: 'N66R15.n66_bound_55' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms N66R15.n66_bound_55

/-- info: 'N66R15.cubesUnsat105R_of_texts' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms N66R15.cubesUnsat105R_of_texts

#print axioms N66R15.rowCertsUnsat_of_texts
