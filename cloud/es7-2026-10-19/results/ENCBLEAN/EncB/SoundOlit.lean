import EncB.ModelLemmas

/-! # U0: `olit` is the orientation literal (`OlitSpec`) -/

namespace EncB

/-- Rotation by `s` sectors. `rotate m k0 tri = tri.map (rotBy m (negMod m k0))` by `rfl`. -/
def rotBy (m s : Nat) (X : Pt) : Pt := (X.1, (X.2 + s) % m)

theorem ptOk_rotBy {m t s : Nat} {X : Pt} (hX : PtOk m t X) : PtOk m t (rotBy m s X) :=
  ⟨hX.1, Nat.mod_lt _ (Nat.lt_of_le_of_lt (Nat.zero_le _) hX.2)⟩

theorem rotBy_succ (m s : Nat) (X : Pt) : rotBy m (s + 1) X = rot m (rotBy m s X) := by
  simp only [rotBy, rot, Prod.mk.injEq, true_and]
  rw [Nat.mod_add_mod, Nat.add_assoc]

theorem chi_rotBy {m K t : Nat} (M : Model m K t) {a b d : Pt} (ha : PtOk m t a) (hb : PtOk m t b)
    (hd : PtOk m t d) : ∀ s, M.chi (rotBy m s a) (rotBy m s b) (rotBy m s d) = M.chi a b d
  | 0 => by
    simp only [rotBy, Nat.add_zero, Nat.mod_eq_of_lt ha.2, Nat.mod_eq_of_lt hb.2, Nat.mod_eq_of_lt hd.2]
  | s + 1 => by
    rw [rotBy_succ, rotBy_succ, rotBy_succ,
      M.chi_rot _ _ _ (ptOk_rotBy ha) (ptOk_rotBy hb) (ptOk_rotBy hd), chi_rotBy M ha hb hd s]

theorem orbVarC_some {m t : Nat} {c : List Pt} {v : Nat} (h : orbVarC m t c = some v) :
    v = orbCode m t c ∧ ∃ a b d, c = [a, b, d] ∧ PtOk m t a ∧ PtOk m t b ∧ PtOk m t d ∧ Distinct3 a b d := by
  unfold orbVarC at h
  split at h
  · next hk =>
    refine ⟨(Option.some.inj h).symm, ?_⟩
    match c, hk with
    | [a, b, d], hk =>
      simp only [orbKeyOk, ptOkB, Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq] at hk
      exact ⟨a, b, d, rfl, ⟨hk.1.1.1.1.1.1, hk.1.1.1.1.1.2⟩, ⟨hk.1.1.1.1.2.1, hk.1.1.1.1.2.2⟩,
        ⟨hk.1.1.1.2.1, hk.1.1.1.2.2⟩, hk.1.1.2, hk.1.2, hk.2⟩
  · exact absurd h (by simp)

theorem olitSpec {m K t : Nat} (M : Model m K t) : OlitSpec M := by
  intro P Q R l hP hQ hR h
  simp only [olit] at h
  split at h
  · exact absurd h (by simp)
  · next p0 hfind =>
    split at h
    · exact absurd h (by simp)
    · next v hv =>
      obtain ⟨rfl, a, b, d, hc, ha, hb, hd, hdist⟩ := orbVarC_some hv
      have hsort := List.find?_some hfind
      simp only [beq_iff_eq] at hsort
      have hrt : rotate m p0.2 [P, Q, R] =
          [rotBy m (negMod m p0.2) P, rotBy m (negMod m p0.2) Q, rotBy m (negMod m p0.2) R] := rfl
      have hchi := (chi_rotBy M hP hQ hR (negMod m p0.2)).symm
      have hP' := ptOk_rotBy (s := negMod m p0.2) hP
      have hQ' := ptOk_rotBy (s := negMod m p0.2) hQ
      have hR' := ptOk_rotBy (s := negMod m p0.2) hR
      generalize rotBy m (negMod m p0.2) P = P' at hrt hchi hP'
      generalize rotBy m (negMod m p0.2) Q = Q' at hrt hchi hQ'
      generalize rotBy m (negMod m p0.2) R = R' at hrt hchi hR'
      rw [hrt] at hsort h
      rw [hchi]
      have hl := Option.some.inj h
      subst hl
      rw [hc] at hsort ⊢
      simp only [List.zip_cons_cons, List.zip_nil_right, insSort, List.foldr, insertBy] at hsort ⊢
      refine ⟨by split <;> simp only [orbCode, oBase] <;> omega, ?_⟩
      have key : ∀ s : List Nat, s.Perm [0, 1, 2] →
          [P', Q', R'].getD (s.getD 0 0) (0, 0) = a → [P', Q', R'].getD (s.getD 1 0) (0, 0) = b →
          [P', Q', R'].getD (s.getD 2 0) (0, 0) = d →
          (CodeLitHolds M.τc (if permSign s > 0 then (orbCode m t [a, b, d] : Int)
            else -(orbCode m t [a, b, d] : Int)) ↔ M.chi P' Q' R' = true) := by
        intro s hs e0 e1 e2
        have hd' : Distinct3 P' Q' R' := by
          rw [← e0, ← e1, ← e2] at hdist
          obtain ⟨d1, d2, d3⟩ := hdist
          rcases perm012_cases hs with rfl | rfl | rfl | rfl | rfl | rfl <;>
            simp only [List.getD, List.getElem?_cons_zero, List.getElem?_cons_succ, Option.getD_some] at d1 d2 d3 <;>
            exact ⟨by first | exact d1 | exact d2 | exact d3 | exact Ne.symm d1 | exact Ne.symm d2 | exact Ne.symm d3,
              by first | exact d1 | exact d2 | exact d3 | exact Ne.symm d1 | exact Ne.symm d2 | exact Ne.symm d3,
              by first | exact d1 | exact d2 | exact d3 | exact Ne.symm d1 | exact Ne.symm d2 | exact Ne.symm d3⟩
        have hp := chi_perm3 M hP' hQ' hR' hd' hs
        rw [e0, e1, e2] at hp
        have ho := holds_orb M ha hb hd
        split
        · next hpos => rw [ho, hp, if_pos hpos]
        · next hneg =>
          rw [codeLitHolds_neg (by simp only [orbCode, oBase]; omega), ho, hp, if_neg hneg]
          cases M.chi P' Q' R' <;> simp
      cases hA : ptLt R' Q' <;> cases hB : ptLt R' P' <;> cases hC : ptLt Q' P' <;>
        simp only [hA, hB, hC, insertBy, if_true, if_false, Bool.false_eq_true, List.cons.injEq, and_true,
          List.map_cons, List.map_nil] at hsort ⊢ <;>
        obtain ⟨e0, e1, e2⟩ := hsort <;>
        exact key _ (by decide) (by simp [e0]) (by simp [e1]) (by simp [e2])

end EncB
