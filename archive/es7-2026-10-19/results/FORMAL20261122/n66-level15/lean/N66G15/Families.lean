import N66G15.Final

/-!
# N66G15.Families: soundness of the threshold (4.4) and CE/UE (4.8) families for every `Model`

* `holds_thresh`: `cap_ge(k+1) → cap_ge(k)` (and cup) hold for the intended assignment.
* `holds_ceue`: `C5(p,u,q) → CE(p,q)`, `U5(p,u,q) → UE(p,q)` hold by definition, and `¬CE(p,q) ∨ ¬UE(p,q)` holds
  by `Model.noCapCup55` and owner uniqueness.
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks N66E15

/-! ## Threshold monotonicity (4.4) -/

open Classical in
theorem meaning_geAtom (M : Model) (cup : Bool) (a b : Fin 70) {k : ℕ} (hk : k < 5) :
    M.meaning (geAtom cup a b k) =
      decide (M.LabGe cup (if a < b then a else b) (if a < b then b else a) k) := by
  unfold geAtom
  cases cup <;> simp only [Bool.false_eq_true, if_true, if_false, Model.meaning, Nat.mod_eq_of_lt hk]

theorem labGe_mono (M : Model) {cup : Bool} {i j : Fin 70} {k : ℕ} (h : M.LabGe cup i j (k + 1)) :
    M.LabGe cup i j k := by
  obtain ⟨u, v, huv, hv, hidx, hk⟩ := h
  exact ⟨u, v, huv, hv, hidx, by split at hk <;> split <;> simp_all <;> omega⟩

/-- **4.4.** -/
theorem holds_thresh (M : Model) : M.Holds (threshClauses ()) := by
  classical
  intro cl hcl
  unfold threshClauses at hcl
  simp only [List.mem_flatMap, List.mem_map, List.mem_cons, List.mem_singleton, List.not_mem_nil,
    or_false] at hcl
  obtain ⟨p, -, cup, hcup, k, hk, rfl⟩ := hcl
  have hk5 : k < 4 := by rcases hk with rfl | rfl <;> omega
  by_cases h : M.LabGe cup (if p.1 < p.2 then p.1 else p.2) (if p.1 < p.2 then p.2 else p.1) (k + 1)
  · refine ⟨(true, geAtom cup p.1 p.2 k), by simp, ?_⟩
    rw [meaning_geAtom M cup p.1 p.2 (by omega)]
    simpa using labGe_mono M h
  · refine ⟨(false, geAtom cup p.1 p.2 (k + 1)), by simp, ?_⟩
    rw [meaning_geAtom M cup p.1 p.2 (by omega)]
    simpa using h

/-! ## CE/UE (4.8) -/

theorem SEPath.start_lt {cup : ℕ → ℕ → ℕ → Bool} {color : Bool} {p u v k : ℕ}
    (h : SEPath cup color p u v k) : p < v := by
  induction h with
  | two hv => exact hv
  | step _ huv _ ih => omega

open Classical in
theorem meaning_ce (M : Model) (p q : Fin 70) : M.meaning (.ce p q) = decide (M.End5 false p q) := rfl
open Classical in
theorem meaning_ue (M : Model) (p q : Fin 70) : M.meaning (.ue p q) = decide (M.End5 true p q) := rfl
open Classical in
theorem meaning_chC (M : Model) (k : Fin 6) (a b c : Fin 70) :
    M.meaning (.chC k a b c) = decide (M.Chain false k.val a b c) := rfl
open Classical in
theorem meaning_chU (M : Model) (k : Fin 6) (a b c : Fin 70) :
    M.meaning (.chU k a b c) = decide (M.Chain true k.val a b c) := rfl

theorem not_ce_and_ue (M : Model) (p q : Fin 70) : ¬ (M.End5 false p q ∧ M.End5 true p q) := by
  rintro ⟨⟨x, u, y, hy, hx, hyq, hpath⟩, ⟨x', u', y', hy', hx', hyq', hpath'⟩⟩
  have hxn : x < M.n := lt_trans hpath.start_lt hy
  have hxn' : x' < M.n := lt_trans hpath'.start_lt hy'
  have e1 : x = x' := idxOf_injective M hxn hxn' (hx.trans hx'.symm)
  have e2 : y = y' := idxOf_injective M hy hy' (hyq.trans hyq'.symm)
  subst e1; subst e2
  exact M.noCapCup55 x u u' y hy hpath hpath'

theorem end5_of_chain (M : Model) {color : Bool} {p u q : Fin 70} (h : M.Chain color 5 p u q) :
    M.End5 color p q := by
  obtain ⟨x, w, y, hy, hx, -, hyq, hpath⟩ := h
  exact ⟨x, w, y, hy, hx, hyq, hpath⟩

/-- **4.8.** -/
theorem holds_ceue (M : Model) : M.Holds (ceueClauses ()) := by
  classical
  intro cl hcl
  unfold ceueClauses at hcl
  obtain ⟨t, -, hcl⟩ := List.mem_flatMap.1 hcl
  unfold ceueClausesAt at hcl
  split at hcl
  · simp at hcl
  · simp only [List.mem_append, List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hcl
    rcases hcl with hex | rfl | rfl
    · split at hex
      · simp only [List.mem_singleton] at hex
        subst hex
        by_cases hce : M.End5 false t.1 t.2.2
        · refine ⟨(false, Atom.ue t.1 t.2.2), by simp, ?_⟩
          rw [meaning_ue]
          simpa using fun hue => not_ce_and_ue M _ _ ⟨hce, hue⟩
        · refine ⟨(false, Atom.ce t.1 t.2.2), by simp, ?_⟩
          rw [meaning_ce]
          simpa using hce
      · simp at hex
    · by_cases hc : M.Chain false 5 t.1 t.2.1 t.2.2
      · refine ⟨(true, Atom.ce t.1 t.2.2), by simp, ?_⟩
        rw [meaning_ce]
        simpa using end5_of_chain M hc
      · refine ⟨(false, Atom.chC 5 t.1 t.2.1 t.2.2), by simp, ?_⟩
        rw [meaning_chC]
        simpa using hc
    · by_cases hc : M.Chain true 5 t.1 t.2.1 t.2.2
      · refine ⟨(true, Atom.ue t.1 t.2.2), by simp, ?_⟩
        rw [meaning_ue]
        simpa using end5_of_chain M hc
      · refine ⟨(false, Atom.chU 5 t.1 t.2.1 t.2.2), by simp, ?_⟩
        rw [meaning_chU]
        simpa using hc

end N66G15

#print axioms N66G15.holds_thresh
#print axioms N66G15.holds_ceue
