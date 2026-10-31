import ETVEncoding.Soundness

/-!
# From structured clauses to the DIMACS clauses

`dimacs N A U K` numbers the variables in the order of Python's `new()` calls
(`numberMap (allVars N A U)`). We prove that this numbering is `1 + ` the position in
`allVars`, that every variable used by a clause is allocated, and hence that a satisfying
assignment of the structured clauses gives a satisfying Boolean assignment of the DIMACS
clauses.
-/

namespace ETV

open Lit

/-- A Boolean assignment of variable numbers satisfies a list of DIMACS clauses. -/
def DimacsSat (cls : List (List ℤ)) (ν : ℕ → Bool) : Prop :=
  ∀ c ∈ cls, ∃ l ∈ c, (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)

/-- The DIMACS formula has a model. An UNSAT certificate for the file is a proof of the
negation of this proposition. -/
def DimacsSatisfiable (cls : List (List ℤ)) : Prop := ∃ ν, DimacsSat cls ν

/-! ### The numbering -/

theorem numberStep_foldl (v : Var) : ∀ (l : List Var) (m : Std.HashMap Var ℕ) (c : ℕ),
    (v ∈ (l.foldl numberStep (m, c)).1 ↔ v ∈ m ∨ v ∈ l) ∧
    (l.foldl numberStep (m, c)).1.getD v 0 =
      if v ∈ m then m.getD v 0 else if v ∈ l then c + l.idxOf v else 0
  | [], m, c => by
      refine ⟨by simp, ?_⟩
      by_cases hvm : v ∈ m
      · simp [hvm]
      · simp [hvm, Std.HashMap.getD_eq_fallback hvm]
  | a :: l, m, c => by
      obtain ⟨ih1, ih2⟩ := numberStep_foldl v l (m.insertIfNew a c) (c + 1)
      simp only [List.foldl_cons, numberStep]
      refine ⟨?_, ?_⟩
      · rw [ih1, Std.HashMap.mem_insertIfNew, beq_iff_eq, List.mem_cons]
        constructor
        · rintro ((rfl | h) | h)
          · exact Or.inr (Or.inl rfl)
          · exact Or.inl h
          · exact Or.inr (Or.inr h)
        · rintro (h | rfl | h)
          · exact Or.inl (Or.inr h)
          · exact Or.inl (Or.inl rfl)
          · exact Or.inr h
      · rw [ih2]
        by_cases hvm : v ∈ m
        · have hv' : v ∈ m.insertIfNew a c := Std.HashMap.mem_insertIfNew.2 (Or.inr hvm)
          rw [if_pos hv', if_pos hvm, Std.HashMap.getD_insertIfNew]
          have ham : ¬((a == v) = true ∧ a ∉ m) := fun h => h.2 (by
            rw [beq_iff_eq] at h
            exact h.1 ▸ hvm)
          rw [if_neg ham]
        · by_cases hav : a = v
          · subst hav
            have hv' : a ∈ m.insertIfNew a c :=
              Std.HashMap.mem_insertIfNew.2 (Or.inl (beq_self_eq_true a))
            rw [if_pos hv', if_neg hvm, Std.HashMap.getD_insertIfNew,
              if_pos ⟨beq_self_eq_true a, hvm⟩, if_pos List.mem_cons_self,
              List.idxOf_cons_self]
            simp
          · have hv' : v ∉ m.insertIfNew a c := by
              rw [Std.HashMap.mem_insertIfNew, beq_iff_eq]
              rintro (h | h)
              · exact hav h
              · exact hvm h
            rw [if_neg hv', if_neg hvm, List.idxOf_cons_ne _ hav]
            by_cases hvl : v ∈ l
            · rw [if_pos hvl, if_pos (List.mem_cons_of_mem _ hvl)]
              omega
            · rw [if_neg hvl, if_neg (by simp [List.mem_cons, Ne.symm hav, hvl])]

theorem numberMap_getD {l : List Var} {v : Var} (h : v ∈ l) :
    (numberMap l).getD v 0 = l.idxOf v + 1 := by
  have := (numberStep_foldl v l ∅ 1).2
  simp only [numberMap, Std.HashMap.not_mem_empty, if_false, if_pos h] at this ⊢
  rw [this]
  omega

/-- Recover a variable from its number. -/
def decode (l : List Var) (n : ℕ) : Var := l.getD (n - 1) default

theorem decode_numberMap {l : List Var} {v : Var} (h : v ∈ l) :
    decode l ((numberMap l).getD v 0) = v := by
  rw [numberMap_getD h, decode, Nat.add_sub_cancel, List.getD_eq_getElem?_getD,
    List.getElem?_eq_getElem (List.idxOf_lt_length_of_mem h), Option.getD_some]
  exact List.getElem_idxOf _

/-! ### Every variable of every clause is allocated -/

theorem mem_allVars_x {N A U i j k : ℕ} :
    Var.x i j k ∈ allVars N A U ↔ i < j ∧ j < k ∧ k < N := by
  simp [allVars, List.mem_append, List.mem_map, Prod.exists]

theorem mem_allVars_v {N A U x a b r : ℕ} {t : Bool} :
    Var.v t x a b r ∈ allVars N A U ↔ (x, a, b, r) ∈ vKeys (if t then U else A) N := by
  cases t <;> simp [allVars, List.mem_append, List.mem_map, Prod.exists, -mem_vKeys]

theorem mem_allVars_e {N A U x b r : ℕ} {t : Bool} :
    Var.e t x b r ∈ allVars N A U ↔ (x, b, r) ∈ eKeys (if t then U else A) N := by
  cases t <;> simp [allVars, List.mem_append, List.mem_map, Prod.exists, -mem_eKeys]

/-- The chain clauses of type `t` only use allocated variables. -/
theorem chainClauses_vars {N A U : ℕ} (t : Bool) :
    ∀ c ∈ chainClauses t (if t then U else A) N, ∀ l ∈ c, l.var ∈ allVars N A U := by
  generalize hB : (if t then U else A) = B
  intro c hc l hl
  simp only [chainClauses, List.mem_append] at hc
  rcases hc with ((hc | hc) | hc) | hc
  · simp only [baseClauses, List.mem_map, Prod.exists, mem_triples] at hc
    obtain ⟨x, a, b, ⟨hxa, hab, hb⟩, rfl⟩ := hc
    split_ifs at hl with h3 <;> simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
    · rcases hl with rfl | rfl <;>
        simp only [pos', ntlit, mem_allVars_x, mem_allVars_v, hB, mem_vKeys] <;> omega
    · subst hl
      simp only [ntlit, mem_allVars_x]
      omega
  · simp only [extClauses, List.mem_flatMap, Prod.exists, mem_quads, List.mem_filterMap,
      List.mem_range'_1] at hc
    obtain ⟨x, w, a, b, ⟨hxw, hwa, hab, hb⟩, r, ⟨hr4, hrB⟩, hc⟩ := hc
    split_ifs at hc with hkey hlt <;> simp only [Option.some.injEq] at hc <;> subst hc <;>
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
    · rcases hl with rfl | rfl | rfl <;>
        simp only [pos', neg', ntlit, mem_allVars_x, mem_allVars_v, hB, mem_vKeys] <;> omega
    · rcases hl with rfl | rfl <;>
        simp only [neg', ntlit, mem_allVars_x, mem_allVars_v, hB, mem_vKeys] <;> omega
  · simp only [vClauses, List.mem_flatMap, Prod.exists, mem_vKeys, List.mem_cons] at hc
    obtain ⟨x, a, b, r, ⟨⟨hxa, hab, hb⟩, h3, hrB, hkey⟩, hc⟩ := hc
    rcases hc with rfl | hc
    · simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
      rcases hl with rfl | rfl <;>
        simp only [pos', neg', mem_allVars_v, mem_allVars_e, hB, mem_vKeys, mem_eKeys] <;>
        omega
    · split_ifs at hc with h4
      · simp only [List.mem_cons, List.not_mem_nil, or_false] at hc
        subst hc
        simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
        rcases hl with rfl | rfl <;>
          simp only [pos', neg', mem_allVars_v, hB, mem_vKeys] <;> omega
      · simp at hc
  · simp only [eClauses, List.mem_filterMap, Prod.exists, mem_eKeys] at hc
    obtain ⟨x, b, r, ⟨⟨hxb, hb⟩, h3, hrB, hkey⟩, hc⟩ := hc
    split_ifs at hc with h4
    simp only [Option.some.injEq] at hc
    subst hc
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
    rcases hl with rfl | rfl <;>
      simp only [pos', neg', mem_allVars_e, hB, mem_eKeys] <;> omega

theorem etvClauses_vars {N A U K : ℕ} :
    ∀ c ∈ etvClauses N A U K, ∀ l ∈ c, l.var ∈ allVars N A U := by
  intro c hc l hl
  simp only [etvClauses, List.mem_append] at hc
  rcases hc with ((hc | hc) | hc) | hc
  · simp only [signotopeClauses, List.mem_flatMap, Prod.exists, mem_quads] at hc
    obtain ⟨i, j, k, m, ⟨hij, hjk, hkm, hm⟩, hc⟩ := hc
    simp only [sig4, tri3, List.cons_append, List.nil_append, List.mem_cons,
      List.not_mem_nil, or_false] at hc
    rcases hc with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hl <;>
      rcases hl with rfl | rfl | rfl <;>
      simp only [pos', neg', mem_allVars_x] <;> omega
  · exact chainClauses_vars false c hc l hl
  · exact chainClauses_vars true c hc l hl
  · simp only [gonClauses, List.mem_flatMap, Prod.exists, mem_pairs, List.mem_filterMap,
      List.mem_range'_1] at hc
    obtain ⟨x, b, ⟨hxb, hb⟩, r, ⟨hr3, hrA⟩, hc⟩ := hc
    split_ifs at hc with hcond
    simp only [Option.some.injEq] at hc
    subst hc
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hl
    rcases hl with rfl | rfl
    · simp only [neg', mem_allVars_e, Bool.false_eq_true, if_false, mem_eKeys]
      omega
    · simp only [neg', mem_allVars_e, if_true, mem_eKeys]
      omega

/-! ### Transfer of models -/

/-- The Boolean assignment of variable numbers induced by `τ`. -/
noncomputable def nuOf (N A U : ℕ) (τ : Var → Prop) (n : ℕ) : Bool :=
  @decide (τ (decode (allVars N A U) n)) (Classical.propDecidable _)

theorem nuOf_num {N A U : ℕ} {τ : Var → Prop} {v : Var} (hv : v ∈ allVars N A U) :
    nuOf N A U τ ((numberMap (allVars N A U)).getD v 0) = true ↔ τ v := by
  simp only [nuOf, decode_numberMap hv, decide_eq_true_iff]

/-- A model of the structured clauses gives a model of the DIMACS clauses. -/
theorem dimacsSat_of_holds {N A U K : ℕ} {τ : Var → Prop}
    (h : ∀ c ∈ etvClauses N A U K, ClauseHolds τ c) : DimacsSat (dimacs N A U K) (nuOf N A U τ) := by
  classical
  intro c hc
  simp only [dimacs, List.mem_map] at hc
  obtain ⟨c', hc', rfl⟩ := hc
  obtain ⟨l, hl, hhold⟩ := h c' hc'
  have hv := etvClauses_vars c' hc' l hl
  refine ⟨litToInt (numberMap (allVars N A U)) l, List.mem_map_of_mem hl, ?_⟩
  have hdec := decode_numberMap hv
  have hnum := numberMap_getD hv
  unfold litToInt
  unfold Lit.Holds at hhold
  cases hpos : l.pos
  · simp only [hpos, Bool.false_eq_true, if_false] at hhold ⊢
    right
    refine ⟨by omega, ?_⟩
    simp only [nuOf, Int.natAbs_neg, Int.natAbs_natCast, hdec, decide_eq_false_iff_not]
    exact hhold
  · simp only [hpos, if_true] at hhold ⊢
    left
    refine ⟨by omega, ?_⟩
    simp only [nuOf, Int.natAbs_natCast, hdec, decide_eq_true_eq]
    exact hhold

/-- A model of the structured clauses gives a model of the DIMACS clauses. -/
theorem dimacsSatisfiable_of_holds {N A U K : ℕ} {τ : Var → Prop}
    (h : ∀ c ∈ etvClauses N A U K, ClauseHolds τ c) : DimacsSatisfiable (dimacs N A U K) :=
  ⟨_, dimacsSat_of_holds h⟩

/-- **Soundness of the DIMACS file.** If `σ` is a signotope on `N` points with no `A`-cap,
no `U`-cup and no `K`-gon, then `dimacs N A U K` (the clauses of `gen_etv.py N A U K`) is
satisfiable. -/
theorem dimacsSatisfiable_of_signotope {N A U K : ℕ} {σ : Sig} (hσ : IsSignotope N σ)
    (hA : ¬HasCap σ N A) (hU : ¬HasCup σ N U) (hK : ¬HasGon σ N K) :
    DimacsSatisfiable (dimacs N A U K) :=
  dimacsSatisfiable_of_holds (etvClauses_sound hσ hA hU hK)

/-- Contrapositive: an UNSAT verdict for `dimacs N A U K` means every signotope on `N`
points has an `A`-cap, a `U`-cup or a `K`-gon. -/
theorem signotope_of_unsat {N A U K : ℕ} (h : ¬DimacsSatisfiable (dimacs N A U K))
    {σ : Sig} (hσ : IsSignotope N σ) : HasCap σ N A ∨ HasCup σ N U ∨ HasGon σ N K := by
  by_contra hc
  simp only [not_or] at hc
  exact h (dimacsSatisfiable_of_signotope hσ hc.1 hc.2.1 hc.2.2)

end ETV
