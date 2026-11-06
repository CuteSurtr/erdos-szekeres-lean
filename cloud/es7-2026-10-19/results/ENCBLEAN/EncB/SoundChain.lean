import EncB.SoundOlit

/-! U2 (`EncB/SoundChain.lean`) starting point (compiled by the M3 judge): the fold over levels and the shape of an `extItems` clause (from plan A's probe),
and the shape of an `okList` entry. -/

namespace EncB.Chain

/-- U2: the fold over levels: every clause of the level fold is an `extItems` clause of some level. -/
theorem mem_levels {m K t i : Nat} {Q : List Pt} {isF : Int → Bool} {okL : List (Pt × Pt × Int)} :
    ∀ (levs : List Nat) (st : Array Bool × List (List Int)) (cl : List Int),
      cl ∈ (levs.foldl (levelStep m K t i Q isF okL) st).2 →
      cl ∈ st.2 ∨ ∃ lev ∈ levs, ∃ keys, cl ∈ (extItems m K t i lev Q isF keys okL).map (·.2.2)
  | [], st, cl, h => Or.inl h
  | lev :: levs, st, cl, h => by
    rcases mem_levels levs _ cl h with h | ⟨lev', hlev', keys, hk⟩
    · simp only [levelStep, List.mem_append] at h
      rcases h with h | h
      · exact Or.inl h
      · exact Or.inr ⟨lev, List.mem_cons_self, st.1, h⟩
    · exact Or.inr ⟨lev', List.mem_cons_of_mem _ hlev', keys, hk⟩

/-- U2: what an `extItems` clause is. -/
theorem mem_extItems {m K t i lev : Nat} {Q : List Pt} {isF : Int → Bool} {keys : Array Bool}
    {okL : List (Pt × Pt × Int)} {cl : List Int}
    (h : cl ∈ (extItems m K t i lev Q isF keys okL).map (·.2.2)) :
    ∃ e ∈ okL, ∃ a ∈ Q, ∃ lab lt, a ≠ e.1 ∧ a ≠ e.2.1 ∧
      olit m (orbVarC m t) (i, 0) a e.1 = some lab ∧ olit m (orbVarC m t) a e.1 e.2.1 = some lt ∧
      cl = (if lev + 1 < K - 1 then [-(fCode m K t i lev e.1 e.2.1 : Int), -lab, -lt,
                (fCode m K t i (lev + 1) a e.1 : Int)]
            else [-(fCode m K t i lev e.1 e.2.1 : Int), -lab, -lt]) := by
  simp only [extItems, List.mem_map, List.mem_flatMap] at h
  obtain ⟨it, ⟨e, he, hit⟩, rfl⟩ := h
  split at hit
  · simp only [List.mem_filterMap] at hit
    obtain ⟨a, ha, hsome⟩ := hit
    split at hsome
    · exact absurd hsome (by simp)
    · rename_i hab
      simp only [Bool.or_eq_true, beq_iff_eq, not_or] at hab
      split at hsome
      · exact absurd hsome (by simp)
      · rename_i lab hlab
        split at hsome
        · exact absurd hsome (by simp)
        · split at hsome
          · exact absurd hsome (by simp)
          · rename_i lt hlt
            split at hsome
            · exact absurd hsome (by simp)
            · refine ⟨e, he, a, ha, lab, lt, hab.1, hab.2, hlab, hlt, ?_⟩
              split at hsome
              · rename_i hlev
                simp only [Option.some.injEq] at hsome
                rw [if_pos hlev, ← hsome]
              · rename_i hlev
                simp only [Option.some.injEq] at hsome
                rw [if_neg hlev, ← hsome]
  · exact absurd hit (by simp)

theorem mem_okList {m t i : Nat} {Q : List Pt} {isF : Int → Bool} {e : Pt × Pt × Int}
    (h : e ∈ okList m t i Q isF) :
    e.1 ∈ Q ∧ e.2.1 ∈ Q ∧ e.1 ≠ e.2.1 ∧ olit m (orbVarC m t) (i, 0) e.1 e.2.1 = some e.2.2 := by
  simp only [okList, List.mem_flatMap, List.mem_filterMap] at h
  obtain ⟨a, ha, b, hb, hsome⟩ := h
  split at hsome
  · next hab =>
    split at hsome
    · exact absurd hsome (by simp)
    · next l hl =>
      split at hsome
      · exact absurd hsome (by simp)
      · cases hsome
        exact ⟨ha, hb, by simpa using hab, hl⟩
  · exact absurd hsome (by simp)

/-! ### Chains: the two constructions behind the base and extension clauses -/

/-- A two-label chain `a, b` (base clause): one pivot triangle, no consecutive triple. -/
theorem chainFrom_two {m t : Nat} {chi : Pt → Pt → Pt → Bool} {i : Nat} {a b : Pt}
    (ha : InQ m t i a) (hb : InQ m t i b) (h : chi (i, 0) a b = true) : ChainFrom m t chi i 2 a b := by
  refine ⟨fun s => match s with | 0 => a | _ + 1 => b, rfl, rfl, ?_, ?_, ?_⟩
  · intro s _
    cases s with
    | zero => exact ha
    | succ s => exact hb
  · intro s hs
    cases s with
    | zero => exact h
    | succ s => exact absurd hs (by omega)
  · intro s hs
    exact absurd hs (by omega)

/-- Prepending `a` to a chain `b, c, …` of length `lev` (extension clause). -/
theorem chainFrom_cons {m t : Nat} {chi : Pt → Pt → Pt → Bool} {i lev : Nat} {a b c : Pt}
    (hch : ChainFrom m t chi i lev b c) (ha : InQ m t i a) (hab : chi (i, 0) a b = true)
    (habc : chi a b c = true) : ChainFrom m t chi i (lev + 1) a b := by
  obtain ⟨q, hq0, hq1, hQ, hP, hT⟩ := hch
  refine ⟨fun s => match s with | 0 => a | s + 1 => q s, rfl, hq0, ?_, ?_, ?_⟩
  · intro s hs
    cases s with
    | zero => exact ha
    | succ s => exact hQ s (by omega)
  · intro s hs
    cases s with
    | zero => show chi (i, 0) a (q 0) = true; rw [hq0]; exact hab
    | succ s => exact hP s (by omega)
  · intro s hs
    cases s with
    | zero => show chi a (q 0) (q 1) = true; rw [hq0, hq1]; exact habc
    | succ s => exact hT s (by omega)

/-! ### Bounds and literals -/

theorem lt_chainFL {K l : Nat} (h : l < K - 1 ∨ l < 3) : l < chainFL K := by
  unfold chainFL
  rcases h with h | h
  · exact Nat.lt_of_lt_of_le h (Nat.le_max_left _ _)
  · exact Nat.lt_of_lt_of_le h (Nat.le_max_right _ _)

theorem fCode_ne_zero {m K t i l : Nat} {a b : Pt} : (fCode m K t i l a b : Int) ≠ 0 := by
  have h : 0 < fCode m K t i l a b := by simp only [fCode, fBase, oBase]; omega
  omega

theorem ptOk_of_inQ {m t i : Nat} {a : Pt} (h : InQ m t i a) : PtOk m t a := ⟨h.2.1, h.2.2.1⟩

theorem ptOk_pivot {m t i : Nat} {a : Pt} (hi : i < t) (h : InQ m t i a) : PtOk m t (i, 0) :=
  ⟨hi, Nat.lt_of_le_of_lt (Nat.zero_le _) h.2.2.1⟩

theorem mem_ite3 {c : Prop} [Decidable c] {x1 x2 x3 x4 y : Int} (hy : y = x1 ∨ y = x2 ∨ y = x3) :
    y ∈ (if c then [x1, x2, x3, x4] else [x1, x2, x3]) := by
  split <;> rcases hy with rfl | rfl | rfl <;> simp

/-! ### The two clause shapes -/

/-- Base clause `[F₂(a,b), -l]` with `l = olit (i,0) a b`. -/
theorem base_sound {m K t : Nat} (M : Model m K t) {isF : Int → Bool} {i : Nat} (hi : i < t)
    {e : Pt × Pt × Int} (he : e ∈ okList m t i (chainQ m t i) isF) :
    ∃ x ∈ [(fCode m K t i 2 e.1 e.2.1 : Int), -e.2.2], CodeLitHolds M.τc x := by
  obtain ⟨ha, hb, _, hl⟩ := mem_okList he
  have ha' := mem_chainQ.1 ha
  have hb' := mem_chainQ.1 hb
  obtain ⟨hl0, hlh⟩ :=
    olitSpec M _ _ _ _ (ptOk_pivot hi ha') (ptOk_of_inQ ha') (ptOk_of_inQ hb') hl
  by_cases hc : M.chi (i, 0) e.1 e.2.1 = true
  · refine ⟨_, List.mem_cons_self, ?_⟩
    rw [holds_f M hi (lt_chainFL (Or.inr (by omega))) (ptOk_of_inQ ha') (ptOk_of_inQ hb')]
    exact chainFrom_two ha' hb' hc
  · refine ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, ?_⟩
    rw [codeLitHolds_neg hl0, hlh]
    exact hc

/-- Extension clause `[-F_lev(b,c), -lab, -lt, F_{lev+1}(a,b)]` (`lev + 1 < K - 1`) and closing clause
`[-F_lev(b,c), -lab, -lt]` (`lev + 1 = K - 1`, by `noChain`). -/
theorem ext_sound {m K t : Nat} (M : Model m K t) {isF : Int → Bool} {i lev : Nat} (hi : i < t)
    (hlev : lev ∈ rng 2 (K - 1)) {e : Pt × Pt × Int} (he : e ∈ okList m t i (chainQ m t i) isF)
    {a : Pt} (ha : a ∈ chainQ m t i) {lab lt : Int}
    (hlab : olit m (orbVarC m t) (i, 0) a e.1 = some lab)
    (hlt : olit m (orbVarC m t) a e.1 e.2.1 = some lt) :
    ∃ x ∈ (if lev + 1 < K - 1 then [-(fCode m K t i lev e.1 e.2.1 : Int), -lab, -lt,
                (fCode m K t i (lev + 1) a e.1 : Int)]
            else [-(fCode m K t i lev e.1 e.2.1 : Int), -lab, -lt]), CodeLitHolds M.τc x := by
  obtain ⟨hb, hc, -, -⟩ := mem_okList he
  have ha' := mem_chainQ.1 ha
  have hb' := mem_chainQ.1 hb
  have hc' := mem_chainQ.1 hc
  have hpa := ptOk_of_inQ ha'
  have hpb := ptOk_of_inQ hb'
  have hpc := ptOk_of_inQ hc'
  obtain ⟨hlab0, hlabh⟩ := olitSpec M _ _ _ _ (ptOk_pivot hi ha') hpa hpb hlab
  obtain ⟨hlt0, hlth⟩ := olitSpec M _ _ _ _ hpa hpb hpc hlt
  have hlevb := mem_rng.1 hlev
  by_cases h1 : ChainFrom m t M.chi i lev e.1 e.2.1
  · by_cases h2 : M.chi (i, 0) a e.1 = true
    · by_cases h3 : M.chi a e.1 e.2.1 = true
      · have hext := chainFrom_cons h1 ha' h2 h3
        split
        · next hlt' =>
          refine ⟨_, List.mem_cons_of_mem _ (List.mem_cons_of_mem _ (List.mem_cons_of_mem _
            List.mem_cons_self)), ?_⟩
          rw [holds_f M hi (lt_chainFL (Or.inl hlt')) hpa hpb]
          exact hext
        · next hge =>
          exfalso
          obtain ⟨q, -, -, hQ, hP, hT⟩ := hext
          exact M.noChain i hi q (fun s hs => hQ s (by omega)) (fun s hs => hP s (by omega))
            (fun s hs => hT s (by omega))
      · refine ⟨_, mem_ite3 (Or.inr (Or.inr rfl)), ?_⟩
        rw [codeLitHolds_neg hlt0, hlth]
        exact h3
    · refine ⟨_, mem_ite3 (Or.inr (Or.inl rfl)), ?_⟩
      rw [codeLitHolds_neg hlab0, hlabh]
      exact h2
  · refine ⟨_, mem_ite3 (Or.inl rfl), ?_⟩
    rw [codeLitHolds_neg fCode_ne_zero, holds_f M hi (lt_chainFL (Or.inl hlevb.2)) hpb hpc]
    exact h1

end EncB.Chain

namespace EncB

/-- **U2**: every chain clause (base, extension, closing) of every pivot holds under `M.τc`, for any `isF`. -/
theorem chainCl_sound {m K t : Nat} (M : Model m K t) (isF : Int → Bool) :
    ∀ i ∈ rng 0 t, ∀ cl ∈ chainCl m K t isF i, ∃ x ∈ cl, CodeLitHolds M.τc x := by
  intro i hi cl hcl
  have hit : i < t := (mem_rng.1 hi).2
  simp only [chainCl, List.mem_append, List.mem_map] at hcl
  rcases hcl with ⟨e, he, rfl⟩ | hcl
  · exact Chain.base_sound M hit he
  · rcases Chain.mem_levels _ _ cl hcl with h | ⟨lev, hlev, keys, hk⟩
    · exact absurd h List.not_mem_nil
    · obtain ⟨e, he, a, ha, lab, lt, -, -, hlab, hlt, rfl⟩ := Chain.mem_extItems hk
      exact Chain.ext_sound M hit hlev he ha hlab hlt

/-- info: 'EncB.chainCl_sound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms chainCl_sound

end EncB

