import RowGeo.Assembly

/-!
# RowGeo.End: the bridge from the certified texts, and `N66Bound 55`

* `certCnf_bounded`, `certUnsat_of_text`, `subUnsat_of_text`: what cake_lpr's verdict on the printed text (trust
  items E1-E6, M9 hash binding) gives: `¬ DimacsSatisfiable (certCnf t)` (for the trimmed certificate of the n = 29
  template: through the printed sub-list, whatever the index list).
* `R0Parse : N66Enc.R0 = R1` — **a named hypothesis** (DESIGN.md F4: the kernel cannot evaluate n66enc's
  `include_str`-parsed `R0` under the memory cap); evidence: compiled Lean evaluates `R0 == R1` to `true`
  (`Audit/R0Parse.lean`, trust item E4).
* **`rowsValid_R0 : RowCertsUnsat → R0Parse → RowsValid N66Enc.R0`** and
  **`n66_bound_55_of_cubes_rows : CubesUnsat132 → RowCertsUnsat → R0Parse → N66Bound 55`**.
-/

namespace RowGeo
open RowEnc RowChk N66Geo

/-! ## From the printed text to the verdict -/

theorem certCnf_bounded {t : Cert} (hok : certOk t = true) :
    ∀ cl ∈ certCnf t, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ nvOf t.n := by
  obtain ⟨hn, htok, hoct⟩ := certOk_parts hok
  intro cl hcl l hl
  unfold certCnf at hcl
  obtain ⟨cl', hcl', rfl⟩ := List.mem_map.1 hcl
  obtain ⟨x, hx, rfl⟩ := List.mem_map.1 hl
  have hxok : x.2.Ok t.n := by
    unfold clsS at hcl'
    obtain ⟨L, hL, hfin⟩ := List.mem_filterMap.1 hcl'
    exact cls3_ok htok hoct L hL _ (finClause_mem hfin x hx) x.1 x.2 rfl
  have hmem : code x.2 ∈ allocCodes t.n := List.mem_map_of_mem (mem_alloc hxok)
  have hle := EncB.numberMap_getD_le hmem
  have hlen : (allocCodes t.n).length = nvOf t.n := by unfold allocCodes nvOf; exact List.length_map _
  have h1 := hle.1
  have h2 := hle.2
  rw [hlen] at h2
  obtain ⟨p, a⟩ := x
  simp only at h1 h2
  cases p
  · show -(((EncB.numberMap (allocCodes t.n)).getD (code a) 0 : Nat) : Int) ≠ 0 ∧
      (-(((EncB.numberMap (allocCodes t.n)).getD (code a) 0 : Nat) : Int)).natAbs ≤ nvOf t.n
    rw [Int.natAbs_neg, Int.natAbs_natCast]
    exact ⟨by omega, h2⟩
  · show (((EncB.numberMap (allocCodes t.n)).getD (code a) 0 : Nat) : Int) ≠ 0 ∧
      ((((EncB.numberMap (allocCodes t.n)).getD (code a) 0 : Nat) : Int)).natAbs ≤ nvOf t.n
    rw [Int.natAbs_natCast]
    exact ⟨by omega, h2⟩

/-- **The verdict on the printed text refutes the certificate's CNF** (E1: the text is the certified file; E2:
cake_lpr printed `s VERIFIED UNSAT`; E3: cake_lpr's parse is `parseDimacs`). -/
theorem certUnsat_of_text {t : Cert} (hok : certOk t = true)
    (hv : ∀ nv F, EncB.parseDimacs (certText t) = some (nv, F) → ¬ EncB.DimacsSatisfiable F) :
    ¬ EncB.DimacsSatisfiable (certCnf t) :=
  hv _ _ (EncB.parseDimacs_render (nvOf t.n) (certCnf t) (certCnf_bounded hok))

theorem subCnf_mem {t : Cert} {idx : List ℕ} {F : List (List Int)} (h : subCnfChecked t idx = some F) :
    ∀ cl ∈ F, cl ∈ certCnf t := by
  unfold subCnfChecked at h
  induction idx generalizing F with
  | nil => simp at h; subst h; simp
  | cons i is ih =>
    simp only [List.mapM_cons, Option.bind_eq_bind, Option.bind_eq_some_iff, Option.pure_def,
      Option.some.injEq] at h
    obtain ⟨x, hx, xs, hxs, rfl⟩ := h
    intro cl hcl
    rcases List.mem_cons.1 hcl with rfl | hcl
    · rw [List.getElem?_toArray] at hx
      exact List.mem_of_getElem? hx
    · exact ih hxs cl hcl

/-- The same for a trimmed certificate: the printed sub-list (any index list) is refuted. -/
theorem subUnsat_of_text {t : Cert} (hok : certOk t = true) {idx : List ℕ} {F : List (List Int)}
    (hs : subCnfChecked t idx = some F)
    (hv : ∀ nv G, EncB.parseDimacs (EncB.render (nvOf t.n) F) = some (nv, G) → ¬ EncB.DimacsSatisfiable G) :
    ¬ EncB.DimacsSatisfiable (certCnf t) := by
  have hb := certCnf_bounded hok
  have hF : ∀ cl ∈ F, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ nvOf t.n := fun cl hcl => hb cl (subCnf_mem hs cl hcl)
  have hu := hv _ _ (EncB.parseDimacs_render (nvOf t.n) F hF)
  rintro ⟨ν, hν⟩
  exact hu ⟨ν, fun cl hcl => hν cl (subCnf_mem hs cl hcl)⟩

/-! ## The end statements -/

/-- **Named hypothesis** (not an axiom): n66enc's `R0` (parse of `data/rows_used.txt`) is the kernel-friendly `R1`. -/
def R0Parse : Prop := N66Enc.R0 = R1

/-- **`RowsValid R0`, Lean-checked modulo `RowCertsUnsat` and `R0Parse`.** -/
theorem rowsValid_R0 (hU : RowCertsUnsat) (hp : R0Parse) : RowsValid N66Enc.R0 := by
  unfold R0Parse at hp
  rw [hp]
  exact rowsValid_R1 hU

/-- **`N66Bound 55`, Lean-checked modulo `CubesUnsat132` (132 verdicts), `RowCertsUnsat` (629 verdicts) and the
named hypothesis `R0Parse`.** -/
theorem n66_bound_55_of_cubes_rows (hc : N66Enc.CubesUnsat132) (hU : RowCertsUnsat) (hp : R0Parse) :
    OmissionZRow.N66Bound 55 :=
  N66Geo.n66_bound_55_of_cubes hc (rowsValid_R0 hU hp)

end RowGeo

/-- info: 'RowGeo.rowsValid_R1' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms RowGeo.rowsValid_R1

/-- info: 'RowGeo.n66_bound_55_of_cubes_rows' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms RowGeo.n66_bound_55_of_cubes_rows

/-- info: 'RowGeo.certUnsat_of_text' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms RowGeo.certUnsat_of_text

/-- info: 'RowGeo.subUnsat_of_text' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms RowGeo.subUnsat_of_text
