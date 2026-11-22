import N66G15.Facts

/-!
# N66G15.Owners: every point has one of the 70 states, and distinct points have distinct states

* `column_le_four`, `column_four_eq_zero`: with no 6-cap and no 6-cup the incoming state lies in the 4 × 4 box.
* `profOf_mem`: the profile of a point is in `stateList`; `idxOf_lt`: its index is below 70.
* `idxOf_injective`: distinct points have distinct states (the library's `balancedState_injective`, through
  Avoids 6 ⇒ Avoids 7).
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks N66E15

theorem avoids_seven {n : ℕ} {cup : ℕ → ℕ → ℕ → Bool} {color : Bool} (h : Avoids n cup color 6) :
    Avoids n cup color 7 := by
  intro u v hv path
  obtain ⟨a, b, hb, hp⟩ := shorter_path path 6 (by omega) (by omega)
  exact h a b (by omega) hp

theorem label_bounds6 (M : Model) {u v : ℕ} (huv : u < v) (hv : v < M.n) :
    1 ≤ (labels M.cup u v).1 ∧ (labels M.cup u v).1 ≤ 4 ∧ 1 ≤ (labels M.cup u v).2 ∧ (labels M.cup u v).2 ≤ 4 := by
  have c := rank_lt_of_avoids M.n M.cup false 6 (by omega) M.noCap6 u v huv hv
  have q := rank_lt_of_avoids M.n M.cup true 6 (by omega) M.noCup6 u v huv hv
  have cl := (length_bounds (rank_attained M.cup false u v huv)).1
  have ql := (length_bounds (rank_attained M.cup true u v huv)).1
  simp only [labels]
  omega

theorem column_le_four (M : Model) {v : ℕ} (hv : v < M.n) (i : ℕ) : column M.cup v i ≤ 4 := by
  unfold column
  apply Finset.sup_le
  intro u hu
  have bd := label_bounds6 M (Finset.mem_range.mp hu) hv
  split_ifs <;> omega

theorem column_four_eq_zero (M : Model) {v : ℕ} (hv : v < M.n) : column M.cup v 4 = 0 := by
  apply Nat.eq_zero_of_le_zero
  unfold column
  apply Finset.sup_le
  intro u hu
  have bd := label_bounds6 M (Finset.mem_range.mp hu) hv
  split_ifs <;> omega

/-- Every nonincreasing tuple over `0..4` is a state (a Bool check, kernel-evaluated: 625 cases). -/
def boxCheck : Bool :=
  (List.range 5).all fun a => (List.range 5).all fun b => (List.range 5).all fun c => (List.range 5).all fun d =>
    !(decide (b ≤ a) && decide (c ≤ b) && decide (d ≤ c)) || stateList.any (fun p => decide (p = ((a, b, c, d) : Prof)))

theorem boxCheck_true : boxCheck = true := by decide +kernel

theorem stateList_length : stateList.length = 70 := by decide +kernel

theorem mem_stateList_of_bounds (a : ℕ) (ha : a < 5) (b : ℕ) (hb : b < 5) (c : ℕ) (hc : c < 5) (d : ℕ)
    (hd : d < 5) (h1 : b ≤ a) (h2 : c ≤ b) (h3 : d ≤ c) : ((a, b, c, d) : Prof) ∈ stateList := by
  have h := boxCheck_true
  unfold boxCheck at h
  have h := List.all_eq_true.1 h a (List.mem_range.2 ha)
  have h := List.all_eq_true.1 h b (List.mem_range.2 hb)
  have h := List.all_eq_true.1 h c (List.mem_range.2 hc)
  have h := List.all_eq_true.1 h d (List.mem_range.2 hd)
  simp only [h1, h2, h3, decide_true, Bool.and_self, Bool.not_true, Bool.false_or] at h
  obtain ⟨p, hp, he⟩ := List.any_eq_true.1 h
  rw [← of_decide_eq_true he]
  exact hp

theorem profOf_mem (M : Model) {v : ℕ} (hv : v < M.n) : profOf M.cup v ∈ stateList := by
  have anti := column_antitone M.cup v
  apply mem_stateList_of_bounds _ (by have := column_le_four M hv 0; omega) _
    (by have := column_le_four M hv 1; omega) _ (by have := column_le_four M hv 2; omega) _
    (by have := column_le_four M hv 3; omega)
  · exact anti (show 0 ≤ 1 by omega)
  · exact anti (show 1 ≤ 2 by omega)
  · exact anti (show 2 ≤ 3 by omega)

theorem idxOf_lt (M : Model) {v : ℕ} (hv : v < M.n) : idxOf M.cup v < 70 := by
  rw [← stateList_length]
  exact List.idxOf_lt_length_of_mem (profOf_mem M hv)

theorem profOf_of_idxOf (M : Model) {v : ℕ} (hv : v < M.n) :
    stateList[idxOf M.cup v]'(by rw [stateList_length]; exact idxOf_lt M hv) = profOf M.cup v :=
  EncB.getElem_idxOf _

/-- **Distinct points have distinct states.** -/
theorem idxOf_injective (M : Model) {u v : ℕ} (hu : u < M.n) (hv : v < M.n)
    (h : idxOf M.cup u = idxOf M.cup v) : u = v := by
  have hp : profOf M.cup u = profOf M.cup v := by
    rw [← profOf_of_idxOf M hu, ← profOf_of_idxOf M hv]
    simp only [h]
  simp only [profOf, Prod.mk.injEq] at hp
  obtain ⟨h0, h1, h2, h3⟩ := hp
  have h4 : column M.cup u 4 = column M.cup v 4 := by
    rw [column_four_eq_zero M hu, column_four_eq_zero M hv]
  have hinj := balancedState_injective M.n M.cup (avoids_seven M.noCap6) (avoids_seven M.noCup6)
  have := @hinj ⟨u, hu⟩ ⟨v, hv⟩ (by
    apply Subtype.ext
    funext i
    apply Fin.ext
    simp only [balancedState]
    fin_cases i
    · exact h0
    · exact h1
    · exact h2
    · exact h3
    · exact h4)
  exact congrArg Fin.val this

end N66G15

#print axioms N66G15.profOf_mem
#print axioms N66G15.idxOf_injective
