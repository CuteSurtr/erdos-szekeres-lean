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

end EncB.Chain

