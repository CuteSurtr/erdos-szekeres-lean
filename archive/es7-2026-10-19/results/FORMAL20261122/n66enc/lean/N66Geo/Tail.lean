import N66Geo.Model

/-!
# N66Geo.Tail: soundness of the counter and of the lex-leader clauses (families 4.14, 4.15 of DESIGN.md)

* `holds_card`: if at most 14 of the states 2..69 are unoccupied, every clause of `cardClauses` (the pysat
  seqcounter port, byte-identical to the certificates) holds under `Model.meaning` (aux `s(a, j)` = "at least `j`
  holes among states `2..a+1`").
* `holds_sb`: if the occupancy satisfies `Lex` (p2_sb.py: at the first listed pair where occupancy differs, the
  first state is a hole), every clause of `sbClauses` holds (aux `e_j` = "the first `j + 1` pairs agree").
-/

namespace N66Geo
open N66Enc

namespace Model
variable (M : Model)

/-- The listed pairs below index `j` agree. -/
def AgreeBelow (j : ℕ) : Prop := ∀ t < j, ∀ p ∈ sbPairs[t]?, (M.occ p.1 ↔ M.occ p.2)

/-- **LEX** (p2_sb.py): at the first listed pair where occupancy differs, the first state is a hole. -/
def Lex : Prop := ∀ j, ∀ p ∈ sbPairs[j]?, M.AgreeBelow j → M.occ p.1 → M.occ p.2

/-- Number of unoccupied states among 2..69. -/
noncomputable def holes : ℕ := M.holesUpTo 68

end Model

/-! ## The counter -/

open Classical in
theorem meaning_sel (M : Model) (s : Fin 70) : M.meaning (.sel s) = decide (M.occ s) := rfl

open Classical in
theorem meaning_cnt (M : Model) (a : Fin 68) (j : Fin 15) :
    M.meaning (.cnt a j) = decide (j.val ≤ M.holesUpTo a.val) := rfl

theorem holeLit_succ (i : ℕ) : holeLit (i + 1) = (false, Atom.sel ⟨(i + 2) % 70, Nat.mod_lt _ (by decide)⟩) := rfl

theorem sAux_eq {a j : ℕ} (ha : a < 68) (hj : j < 15) : sAux a j = (true, Atom.cnt ⟨a, ha⟩ ⟨j, hj⟩) := by
  simp only [sAux, Nat.mod_eq_of_lt ha, Nat.mod_eq_of_lt hj]

open Classical in
theorem holesUpTo_succ (M : Model) (a : ℕ) :
    M.holesUpTo (a + 1) = M.holesUpTo a +
      (if M.occ ⟨(a + 2) % 70, Nat.mod_lt _ (by decide)⟩ then 0 else 1) := by
  unfold Model.holesUpTo
  rw [List.range_succ, List.filter_append, List.length_append]
  congr 1
  by_cases h : M.occ ⟨(a + 2) % 70, Nat.mod_lt _ (by decide)⟩ <;> simp [h]

theorem holesUpTo_mono (M : Model) {a b : ℕ} (h : a ≤ b) : M.holesUpTo a ≤ M.holesUpTo b := by
  classical
  induction b with
  | zero =>
    have : a = 0 := by omega
    subst this; exact Nat.le_refl _
  | succ b ih =>
    rcases Nat.lt_or_ge a (b + 1) with h' | h'
    · have h1 := ih (by omega)
      have h2 := holesUpTo_succ M b
      split at h2 <;> omega
    · have : a = b + 1 := by omega
      subst this; exact Nat.le_refl _

/-- The shapes of the walk's clauses (structural). -/
theorem diag_shape : ∀ (fuel a j : ℕ), ∀ cl ∈ diagClauses fuel a j, ∃ a' j', 1 ≤ a' ∧ a' ≤ 67 ∧ 1 ≤ j' ∧ j' ≤ 14 ∧
    ((cl = [(sAux a' j').neg, sAux (a' + 1) j'] ∧ a' + 1 ≤ 67) ∨
     (cl = [(holeLit (a' + 1)).neg, (sAux a' j').neg, sAux (a' + 1) (j' + 1)] ∧ a' + 1 ≤ 67 ∧ j' < 14) ∨
     (cl = [(holeLit (a' + 1)).neg, (sAux a' j').neg] ∧ j' = 14))
  | 0, _, _, cl, h => by simp [diagClauses] at h
  | fuel + 1, a, j, cl, h => by
    unfold diagClauses at h
    split at h
    · rename_i hc
      obtain ⟨ha, hj, hn⟩ := hc
      simp only [needAux, nLits, kBound, decide_eq_true_eq] at hn
      simp only [List.mem_append] at h
      rcases h with (h | h) | h
      · split at h
        · rename_i h2
          simp only [needAux, nLits, kBound, decide_eq_true_eq] at h2
          simp only [List.mem_singleton] at h
          exact ⟨a, j, by omega, by omega, by omega, by omega, Or.inl ⟨h, by omega⟩⟩
        · simp at h
      · split at h
        · split at h
          · rename_i hk h2
            simp only [needAux, nLits, kBound, decide_eq_true_eq] at h2
            simp only [List.mem_singleton] at h
            exact ⟨a, j, by omega, by omega, by omega, by omega, Or.inr (Or.inl ⟨h, by omega, hk⟩)⟩
          · simp at h
        · rename_i hk
          simp only [List.mem_singleton] at h
          simp only [kBound] at hk
          exact ⟨a, j, by omega, by omega, by omega, by omega, Or.inr (Or.inr ⟨h, by omega⟩)⟩
      · exact diag_shape fuel (a + 1) (j + 1) cl h
    · simp at h

/-- **The counter holds when at most 14 states are unoccupied.** -/
theorem holds_card (M : Model) (hh : M.holes ≤ 14) : M.Holds cardClauses := by
  classical
  have h68 : M.holesUpTo 68 ≤ 14 := hh
  intro cl hcl
  unfold cardClauses at hcl
  obtain ⟨i', hi', hcl⟩ := List.mem_flatMap.1 hcl
  rw [List.mem_range] at hi'
  simp only [nLits] at hi'
  rcases List.mem_append.1 hcl with hb | hd
  · -- base clause [-x_i, s(i, 1)], i = i' + 1
    split at hb
    · simp only [List.mem_singleton] at hb
      subst hb
      rw [holeLit_succ, sAux_eq (show i' + 1 < 68 by omega) (show 1 < 15 by decide)]
      have h1 := holesUpTo_succ M i'
      by_cases ho : M.occ ⟨(i' + 2) % 70, Nat.mod_lt _ (by decide)⟩
      · exact ⟨_, List.mem_cons_self, by simp only [SLit.neg, Bool.not_false, meaning_sel, ho, decide_true]⟩
      · refine ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, ?_⟩
        simp only [ho, if_false] at h1
        simp only [meaning_cnt, decide_eq_true_eq]
        omega
    · simp at hb
  · obtain ⟨a, j, ha1, ha2, hj1, hj2, hshape⟩ := diag_shape _ _ _ cl hd
    obtain ⟨a0, rfl⟩ : ∃ a0, a = a0 + 1 := ⟨a - 1, by omega⟩
    rcases hshape with ⟨rfl, hA⟩ | ⟨rfl, hA, hJ⟩ | ⟨rfl, hJ⟩
    · -- transfer
      rw [sAux_eq (show a0 + 1 < 68 by omega) (show j < 15 by omega),
        sAux_eq (show a0 + 1 + 1 < 68 by omega) (show j < 15 by omega)]
      have hm := holesUpTo_mono M (Nat.le_add_right (a0 + 1) 1)
      by_cases hx : j ≤ M.holesUpTo (a0 + 1)
      · refine ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, ?_⟩
        simp only [meaning_cnt, decide_eq_true_eq]
        omega
      · refine ⟨_, List.mem_cons_self, ?_⟩
        simp only [SLit.neg, Bool.not_true, meaning_cnt, decide_eq_false_iff_not]
        exact hx
    · -- increment
      rw [holeLit_succ, sAux_eq (show a0 + 1 < 68 by omega) (show j < 15 by omega),
        sAux_eq (show a0 + 1 + 1 < 68 by omega) (show j + 1 < 15 by omega)]
      have h1 := holesUpTo_succ M (a0 + 1)
      by_cases ho : M.occ ⟨(a0 + 1 + 2) % 70, Nat.mod_lt _ (by decide)⟩
      · exact ⟨_, List.mem_cons_self, by simp only [SLit.neg, Bool.not_false, meaning_sel, ho, decide_true]⟩
      · simp only [ho, if_false] at h1
        by_cases hx : j ≤ M.holesUpTo (a0 + 1)
        · refine ⟨_, List.mem_cons_of_mem _ (List.mem_cons_of_mem _ List.mem_cons_self), ?_⟩
          simp only [meaning_cnt, decide_eq_true_eq]
          omega
        · refine ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, ?_⟩
          simp only [SLit.neg, Bool.not_true, meaning_cnt, decide_eq_false_iff_not]
          exact hx
    · -- overflow: a hole at a+2 and 14 holes before it would be 15 holes
      subst hJ
      rw [holeLit_succ, sAux_eq (show a0 + 1 < 68 by omega) (show 14 < 15 by decide)]
      have h1 := holesUpTo_succ M (a0 + 1)
      by_cases ho : M.occ ⟨(a0 + 1 + 2) % 70, Nat.mod_lt _ (by decide)⟩
      · exact ⟨_, List.mem_cons_self, by simp only [SLit.neg, Bool.not_false, meaning_sel, ho, decide_true]⟩
      · simp only [ho, if_false] at h1
        refine ⟨_, List.mem_cons_of_mem _ List.mem_cons_self, ?_⟩
        have h3 := holesUpTo_mono M (show a0 + 1 + 1 ≤ 68 by omega)
        simp only [SLit.neg, Bool.not_true, meaning_cnt, decide_eq_false_iff_not]
        omega

/-! ## The lex-leader clauses -/

open Classical in
theorem meaning_sbeAt (M : Model) {i : ℕ} (hi : i < 27) : M.meaning (sbeAt i) = decide (M.PairsAgree i) := by
  simp only [sbeAt, Model.meaning, Nat.mod_eq_of_lt hi]

/-- The shapes of the clauses of `sbFrom j l` (structural). -/
theorem sbFrom_shape : ∀ (l : List (Fin 70 × Fin 70)) (j : ℕ), ∀ cl ∈ sbFrom j l, ∃ i p, j ≤ i ∧
    l[i - j]? = some p ∧
    ((cl = (if i = 0 then [] else [(false, sbeAt (i - 1))]) ++ [(false, Atom.sel p.1), (true, Atom.sel p.2)]) ∨
     (i + 1 < j + l.length ∧
      (cl = (if i = 0 then [] else [(false, sbeAt (i - 1))]) ++
        [(false, Atom.sel p.1), (false, Atom.sel p.2), (true, sbeAt i)] ∨
       cl = (if i = 0 then [] else [(false, sbeAt (i - 1))]) ++
        [(true, Atom.sel p.1), (true, Atom.sel p.2), (true, sbeAt i)])))
  | [], _, cl, h => by simp [sbFrom] at h
  | (s, t) :: rest, j, cl, h => by
    simp only [sbFrom, List.mem_append, List.mem_singleton] at h
    rcases h with (h | h) | h
    · exact ⟨j, (s, t), Nat.le_refl _, by simp, Or.inl h⟩
    · split at h
      · simp at h
      · rename_i hne
        have hlen : 0 < rest.length := by
          cases rest with
          | nil => simp at hne
          | cons _ _ => simp
        simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at h
        refine ⟨j, (s, t), Nat.le_refl _, by simp, Or.inr ⟨by simp; omega, ?_⟩⟩
        exact h
    · obtain ⟨i, p, hij, hp, hc⟩ := sbFrom_shape rest (j + 1) cl h
      refine ⟨i, p, by omega, ?_, ?_⟩
      · have : i - j = (i - (j + 1)) + 1 := by omega
        rw [this, List.getElem?_cons_succ]
        exact hp
      · rcases hc with hc | ⟨hl, hc⟩
        · exact Or.inl hc
        · exact Or.inr ⟨by simp only [List.length_cons]; omega, hc⟩

theorem agreeBelow_of_pairsAgree (M : Model) {i : ℕ} (hi : 0 < i) (h : M.PairsAgree (i - 1)) :
    M.AgreeBelow i := fun t ht p hp => h t (by omega) p hp

/-- **The lex-leader clauses hold for an occupancy that satisfies `Lex`.** -/
theorem holds_sb (M : Model) (hlex : M.Lex) : M.Holds sbClauses := by
  classical
  intro cl hcl
  unfold sbClauses at hcl
  obtain ⟨i, p, -, hp, hc⟩ := sbFrom_shape sbPairs 0 cl hcl
  simp only [Nat.sub_zero] at hp
  have hi : i < 27 := by
    by_contra hge
    have : sbPairs[i]? = none := List.getElem?_eq_none (by simp [sbPairs]; omega)
    rw [this] at hp; simp at hp
  -- the guard literal `-e_{i-1}` holds unless the earlier pairs agree
  have hguard : ∀ rest : List SLit, (¬ (i = 0 ∨ M.AgreeBelow i)) →
      ∃ l ∈ (if i = 0 then [] else [(false, sbeAt (i - 1))]) ++ rest, M.meaning l.2 = l.1 := by
    intro rest hn
    have hi0 : i ≠ 0 := fun h => hn (Or.inl h)
    refine ⟨(false, sbeAt (i - 1)), by simp [hi0], ?_⟩
    simp only [meaning_sbeAt M (show i - 1 < 27 by omega), decide_eq_false_iff_not]
    intro hpa
    exact hn (Or.inr (agreeBelow_of_pairsAgree M (Nat.pos_of_ne_zero hi0) hpa))
  have hbelow : (i = 0 ∨ M.AgreeBelow i) → M.AgreeBelow i := by
    rintro (rfl | h)
    · intro t ht; omega
    · exact h
  have hmem : ∀ x : SLit, ∀ rest : List SLit, x ∈ rest →
      x ∈ (if i = 0 then [] else [(false, sbeAt (i - 1))]) ++ rest := fun x rest h => by
    split <;> simp [h]
  rcases hc with rfl | ⟨hl, rfl | rfl⟩
  · by_cases hg : i = 0 ∨ M.AgreeBelow i
    · by_cases h1 : M.occ p.1
      · have h2 := hlex i p hp (hbelow hg) h1
        exact ⟨(true, Atom.sel p.2), hmem _ _ (by simp), by simp [meaning_sel, h2]⟩
      · exact ⟨(false, Atom.sel p.1), hmem _ _ (by simp), by simp [meaning_sel, h1]⟩
    · exact hguard _ hg
  · by_cases hg : i = 0 ∨ M.AgreeBelow i
    · by_cases h1 : M.occ p.1
      · by_cases h2 : M.occ p.2
        · refine ⟨(true, sbeAt i), hmem _ _ (by simp), ?_⟩
          simp only [meaning_sbeAt M hi, decide_eq_true_eq]
          intro t ht q hq
          rcases Nat.lt_or_ge t i with htl | htg
          · exact hbelow hg t htl q hq
          · have : t = i := by omega
            subst this
            rw [hp] at hq; simp only [Option.mem_def, Option.some.injEq] at hq; subst hq
            exact ⟨fun _ => h2, fun _ => h1⟩
        · exact ⟨(false, Atom.sel p.2), hmem _ _ (by simp), by simp [meaning_sel, h2]⟩
      · exact ⟨(false, Atom.sel p.1), hmem _ _ (by simp), by simp [meaning_sel, h1]⟩
    · exact hguard _ hg
  · by_cases hg : i = 0 ∨ M.AgreeBelow i
    · by_cases h1 : M.occ p.1
      · exact ⟨(true, Atom.sel p.1), hmem _ _ (by simp), by simp [meaning_sel, h1]⟩
      · by_cases h2 : M.occ p.2
        · exact ⟨(true, Atom.sel p.2), hmem _ _ (by simp), by simp [meaning_sel, h2]⟩
        · refine ⟨(true, sbeAt i), hmem _ _ (by simp), ?_⟩
          simp only [meaning_sbeAt M hi, decide_eq_true_eq]
          intro t ht q hq
          rcases Nat.lt_or_ge t i with htl | htg
          · exact hbelow hg t htl q hq
          · have : t = i := by omega
            subst this
            rw [hp] at hq; simp only [Option.mem_def, Option.some.injEq] at hq; subst hq
            exact ⟨fun h => absurd h h1, fun h => absurd h h2⟩
    · exact hguard _ hg

end N66Geo

#print axioms N66Geo.holds_card
#print axioms N66Geo.holds_sb
