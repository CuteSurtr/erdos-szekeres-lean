import D3Encoding.Sound

/-!
# The main soundness theorem for `d3cnf.py`
-/

namespace D3

open Std

section
variable {t K : Nat} {χ : Nat → Nat → Nat → Int}

theorem pattern_entries : ∀ pat ∈ convexPatterns, ∃ p1 p2 p3 p4 : Int,
    pat = [p1, p2, p3, p4] ∧ (p1 = 1 ∨ p1 = -1) ∧ (p2 = 1 ∨ p2 = -1) ∧ (p3 = 1 ∨ p3 = -1) ∧
      (p4 = 1 ∨ p4 = -1) := by
  intro pat h
  simp only [convexPatterns, List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl <;> exact ⟨_, _, _, _, rfl, by simp⟩

theorem clauseSat_append_left {ν : Nat → Bool} {c d : List Int} (h : ClauseSat ν c) :
    ClauseSat ν (c ++ d) := by
  obtain ⟨l, hl, h⟩ := h; exact ⟨l, List.mem_append_left _ hl, h⟩

theorem neg_sign {s : Int} (h : s = 1 ∨ s = -1) : -s = 1 ∨ -s = -1 := by
  rcases h with rfl | rfl <;> simp

/-- The key `R ∈ A` precedes `S` when it is shorter. -/
theorem mem_done {A done rest : List (List Nat)} {S R : List Nat} (hA : A = done ++ S :: rest)
    (hP : A.Pairwise (fun X Y => X.length ≤ Y.length)) (hR : R ∈ A)
    (hlen : R.length < S.length) : R ∈ done := by
  subst hA
  rw [List.mem_append] at hR
  rcases hR with h | h
  · exact h
  · exfalso
    rw [List.pairwise_append, List.pairwise_cons] at hP
    rcases List.mem_cons.1 h with rfl | h
    · omega
    · have := hP.2.1.1 R h; omega

variable (M : Model t K χ)
include M

/-- The clauses of one conv key are satisfied. -/
theorem convClauses_sat {tv : TV} {nX : Nat}
    (TM : TableModel t χ tv nX (nuD3 χ tv nX (convKeys t K)))
    {done rest : List (List Nat)} {S : List Nat} (hA : convKeys t K = done ++ S :: rest)
    {cv : CV} (hcv : CVForm nX done cv) :
    ∀ c ∈ convClauses t (lit tv) cv (nX + done.length + 1) S,
      ClauseSat (nuD3 χ tv nX (convKeys t K)) c := by
  have hSA : S ∈ convKeys t K := by rw [hA]; simp
  obtain ⟨hS4, hSK, hScomb, -⟩ := mem_convKeys.1 hSA
  obtain ⟨hSs, hSP, -⟩ := mem_combs_range.1 hScomb
  have hνS : nuD3 χ tv nX (convKeys t K) (nX + 1 + done.length) = true ↔ ConvAll χ S :=
    nuD3_conv (getElem?_of_prefix hA)
  have hv : (nX + done.length + 1 : Nat) = nX + 1 + done.length := by omega
  intro c hc
  unfold convClauses at hc
  split at hc
  · rename_i a b c' d
    rw [List.mem_map] at hc
    obtain ⟨pat, hpat, rfl⟩ := hc
    simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false,
      forall_eq_or_imp, forall_eq, List.Pairwise.nil] at hSs hSP
    by_cases hconv : ConvAll χ [a, b, c', d]
    · refine ⟨_, List.mem_append_right _ (List.mem_singleton_self _), ?_⟩
      rw [hv]
      exact lit_pos (hνS.2 hconv) (by omega)
    · have hne : [χ a b c', χ a b d, χ a c' d, χ b c' d] ≠ pat := fun h =>
        hconv (convAll_of_pattern TM.chi hSs.1.1 hSs.2.1.1 hSs.2.2.1 pat hpat h)
      obtain ⟨p1, p2, p3, p4, rfl, s1, s2, s3, s4⟩ := pattern_entries pat hpat
      apply clauseSat_append_left
      have := clauseSat_template TM [(-p1, a, b, c'), (-p2, a, b, d), (-p3, a, c', d),
          (-p4, b, c', d)]
        (by
          intro e he
          simp only [List.mem_cons, List.not_mem_nil, or_false] at he
          rcases he with rfl | rfl | rfl | rfl <;>
            exact ⟨neg_sign (by assumption), by simp only; omega, by simp only; omega,
              by simp only; omega, by simp only; omega, by simp only; omega,
              by simp only; omega⟩)
        (by
          have hsg := TM.chi.sign
          have w1 := hsg a b c' (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
          have w2 := hsg a b d (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
          have w3 := hsg a c' d (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
          have w4 := hsg b c' d (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
          simp only [List.mem_cons, List.not_mem_nil, or_false, exists_eq_or_imp,
            exists_eq_left]
          simp only [ne_eq, List.cons.injEq, and_true, not_and] at hne
          rcases s1 with rfl | rfl <;> rcases s2 with rfl | rfl <;> rcases s3 with rfl | rfl <;>
            rcases s4 with rfl | rfl <;> rcases w1 with h1 | h1 <;> rcases w2 with h2 | h2 <;>
            rcases w3 with h3 | h3 <;> rcases w4 with h4 | h4 <;> simp only [h1, h2, h3, h4] at hne ⊢ <;>
            first | omega | (simp at hne) | exact absurd trivial (hne trivial trivial trivial))
      simpa [List.zipWith] using this
  · rename_i hnot
    have h5 : 5 ≤ S.length := by
      match S, hnot with
      | [_, _, _, _], hnot => exact absurd rfl (hnot _ _ _ _)
      | [], _ | [_], _ | [_, _], _ | [_, _, _], _ => simp at hS4
      | _ :: _ :: _ :: _ :: _ :: _, _ => simp
    rw [List.mem_singleton] at hc
    subst hc
    by_cases hconv : ConvAll χ S
    · refine ⟨_, List.mem_append_right _ (List.mem_singleton_self _), ?_⟩
      rw [hv]
      exact lit_pos (hνS.2 hconv) (by omega)
    · have : ∃ i, i < S.length ∧ ¬ConvAll χ (S.eraseIdx i) :=
        Classical.byContradiction fun hn => hconv (convAll_of_erase
          (hSs.imp fun h => Nat.ne_of_lt h) h5 fun i hi =>
            Classical.byContradiction fun h => hn ⟨i, hi, h⟩)
      obtain ⟨i, hi, hci⟩ := this
      have hY : (S.eraseIdx i).Pairwise (· < ·) := hSs.sublist (List.eraseIdx_sublist S i)
      have hYP : ∀ y ∈ S.eraseIdx i, y < 3 * t + 1 := fun y hy => by
        have := hSP y ((List.eraseIdx_sublist S i).subset hy); omega
      have hcR : ¬ConvAll χ (canon t (S.eraseIdx i)) := fun h =>
        hci (convAll_of_canon TM.chi hY hYP h)
      obtain ⟨hlen, hcomb, hcan⟩ := canon_erase_spec M.hG hSs hSP i
      rw [List.length_eraseIdx_of_lt hi] at hlen
      have hRA : canon t (S.eraseIdx i) ∈ convKeys t K :=
        mem_convKeys.2 ⟨by omega, by omega, hcomb, hcan⟩
      have hRd := mem_done hA convKeys_lengths hRA (by omega)
      refine ⟨_, List.mem_append_left _ (List.mem_map.2 ⟨i, List.mem_range.2 hi, rfl⟩), ?_⟩
      have hget : cv.getD (canon t (S.eraseIdx i)) 0 =
          nX + 1 + (convKeys t K).idxOf (canon t (S.eraseIdx i)) := by
        rw [HashMap.getD_eq_getD_getElem?, hcv, if_pos hRd, Option.getD_some, hA,
          List.idxOf_append, if_pos hRd]
      rw [hget]
      apply lit_neg _ (by omega)
      cases hb : nuD3 χ tv nX (convKeys t K) (nX + 1 + (convKeys t K).idxOf (canon t (S.eraseIdx i)))
      · rfl
      · exact absurd ((nuD3_conv (χ := χ) (tv := tv) (nX := nX) (idx_of_mem hRA)).1 hb) hcR

theorem fold_sat {tv : TV} {nX : Nat}
    (TM : TableModel t χ tv nX (nuD3 χ tv nX (convKeys t K))) :
    ∀ (l done : List (List Nat)) (cls : List (List (List Int))) (cv : CV),
      convKeys t K = done ++ l → CVForm nX done cv →
      (∀ cs ∈ cls, ∀ c ∈ cs, ClauseSat (nuD3 χ tv nX (convKeys t K)) c) →
      (∀ cs ∈ (l.foldl (convStep t (lit tv)) (cls, cv, nX + done.length)).1, ∀ c ∈ cs,
        ClauseSat (nuD3 χ tv nX (convKeys t K)) c) ∧
      CVForm nX (convKeys t K) (l.foldl (convStep t (lit tv)) (cls, cv, nX + done.length)).2.1
  | [], done, cls, cv, hA, hcv, hcls => by
    simp only [List.foldl_nil]
    rw [List.append_nil] at hA
    exact ⟨hcls, hA ▸ hcv⟩
  | S :: l, done, cls, cv, hA, hcv, hcls => by
    simp only [List.foldl_cons]
    have e : convStep t (lit tv) (cls, cv, nX + done.length) S =
        (convClauses t (lit tv) cv (nX + done.length + 1) S :: cls,
          cv.insertIfNew S (nX + done.length + 1), nX + (done ++ [S]).length) := by
      simp only [convStep, List.length_append, List.length_singleton]
      congr 2
    rw [e]
    apply fold_sat TM l (done ++ [S])
    · rw [hA]; simp
    · exact cvForm_step hcv S
    · intro cs hcs c hc
      rcases List.mem_cons.1 hcs with rfl | hcs
      · exact convClauses_sat M TM hA hcv c hc
      · exact hcls cs hcs c hc

/-- All clauses of the `K`-gon part hold. -/
theorem kgon_sat {tv : TV} {nX : Nat}
    (TM : TableModel t χ tv nX (nuD3 χ tv nX (convKeys t K))) :
    ∀ c ∈ (kgonLayered t K (lit tv) nX).1, ClauseSat (nuD3 χ tv nX (convKeys t K)) c := by
  obtain ⟨h1, h2⟩ := fold_sat M TM (convKeys t K) [] [] {} (by simp)
    (by intro R; simp) (by simp)
  simp only [List.length_nil, Nat.add_zero] at h1 h2
  intro c hc
  unfold kgonLayered at hc
  simp only [List.mem_append, List.mem_flatten, List.mem_reverse] at hc
  rcases hc with ⟨cs, hcs, hc⟩ | hc
  · exact h1 cs hcs c hc
  · rw [List.mem_map] at hc
    obtain ⟨S, hS, rfl⟩ := hc
    rw [List.mem_filter] at hS
    obtain ⟨hScomb, -⟩ := hS
    obtain ⟨hSs, hSP, hSlen⟩ := mem_combs_range.1 hScomb
    have : ∃ i, i < S.length ∧ ¬ConvAll χ (S.eraseIdx i) :=
      Classical.byContradiction fun hn => M.hNo S hSs hSlen hSP (convAll_of_erase
        (hSs.imp fun h => Nat.ne_of_lt h) (by have := M.hK; omega) fun i hi =>
          Classical.byContradiction fun h => hn ⟨i, hi, h⟩)
    obtain ⟨i, hi, hci⟩ := this
    have hY : (S.eraseIdx i).Pairwise (· < ·) := hSs.sublist (List.eraseIdx_sublist S i)
    have hYP : ∀ y ∈ S.eraseIdx i, y < 3 * t + 1 := fun y hy => by
      have := hSP y ((List.eraseIdx_sublist S i).subset hy); omega
    have hcR : ¬ConvAll χ (canon t (S.eraseIdx i)) := fun h =>
      hci (convAll_of_canon TM.chi hY hYP h)
    obtain ⟨hlen, hcomb, hcan⟩ := canon_erase_spec M.hG hSs hSP i
    rw [List.length_eraseIdx_of_lt hi] at hlen
    have hRA : canon t (S.eraseIdx i) ∈ convKeys t K :=
      mem_convKeys.2 ⟨by have := M.hK; omega, by omega, hcomb, hcan⟩
    refine ⟨_, List.mem_map.2 ⟨i, List.mem_range.2 (by omega), rfl⟩, ?_⟩
    rw [HashMap.getD_eq_getD_getElem?, h2, if_pos hRA, Option.getD_some]
    apply lit_neg _ (by omega)
    cases hb : nuD3 χ tv nX (convKeys t K) (nX + 1 + (convKeys t K).idxOf (canon t (S.eraseIdx i)))
    · rfl
    · exact absurd ((nuD3_conv (χ := χ) (tv := tv) (nX := nX) (idx_of_mem hRA)).1 hb) hcR

end

open Classical in
/-- **Soundness of the D3 encoding, chirotope level.** -/
theorem d3Cnf_sat {t K : Nat} {χ : Nat → Nat → Nat → Int} (M : Model t K χ)
    (hA4 : A4 (3 * t + 1) χ) (hGP : GP3 (3 * t + 1) χ) (hC : CenterFacts t χ)
    (hSB : SectorOrder t χ) :
    ∃ ν : Nat → Bool, ∀ c ∈ (d3Cnf (3 * t) K).2.2, ClauseSat ν c := by
  obtain ⟨hinv, hcov⟩ := triples_spec M.hχ
  have TM : TableModel t χ (triples t).1 (triples t).2
      (nuD3 χ (triples t).1 (triples t).2 (convKeys t K)) :=
    ⟨M.hχ, hinv, hcov, fun v _ hv => by
      unfold nuD3; rw [if_pos hv]; exact decide_eq_true_iff⟩
  refine ⟨nuD3 χ (triples t).1 (triples t).2 (convKeys t K), ?_⟩
  have ht : 3 * t / 3 = t := by omega
  intro c hc
  simp only [d3Cnf, ht, List.mem_append] at hc
  rcases hc with ((hc | hc) | hc) | hc
  · unfold axiomClauses at hc
    rw [List.mem_append, List.mem_flatMap, List.mem_flatMap] at hc
    rcases hc with ⟨S, hS, hc⟩ | ⟨S, hS, hc⟩
    · exact a4_sat TM hA4 (List.mem_filter.1 hS).1 hc
    · exact gp_sat TM hGP (List.mem_filter.1 hS).1 hc
  · exact center_sat TM hC hc
  · exact kgon_sat M TM c hc
  · exact sb_sat TM hSB hc

end D3
