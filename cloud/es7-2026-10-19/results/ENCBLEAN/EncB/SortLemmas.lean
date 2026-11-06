import EncB.ModelLemmas

/-! # U0: insertion sort, `perms`, `Obj.lt`, and positions in strictly sorted lists (Std-only) -/

namespace EncB

/-- Completeness of `perms` (U5's existence step). -/
theorem mem_permsAux : ∀ (n : Nat) (l p : List Nat), l.Nodup → l.length = n → p.Perm l → p ∈ permsAux n l
  | 0, l, p, _, hl, hp => by
    have : l = [] := List.eq_nil_of_length_eq_zero hl
    subst this
    rw [List.perm_nil] at hp
    subst hp
    simp [permsAux]
  | n + 1, l, p, hnd, hl, hp => by
    match p, hp with
    | [], hp => exact absurd hp.length_eq (by simp [hl])
    | x :: p', hp =>
      have hx : x ∈ l := hp.mem_iff.1 List.mem_cons_self
      have hp' : p'.Perm (l.erase x) := by
        have := hp.erase x
        rwa [List.erase_cons_head] at this
      have hlen : (l.erase x).length = n := by rw [List.length_erase_of_mem hx]; omega
      have ih := mem_permsAux n (l.erase x) p' (hnd.erase x) hlen hp'
      simp only [permsAux, List.mem_flatMap, List.mem_map]
      exact ⟨x, hx, p', ih, rfl⟩

theorem mem_perms {l p : List Nat} (hnd : l.Nodup) (hp : p.Perm l) : p ∈ perms l :=
  mem_permsAux _ l p hnd rfl hp

/-! ### Insertion sort (U6a) -/

theorem insertBy_perm {α : Type} (lt : α → α → Bool) (x : α) : ∀ l : List α, (insertBy lt x l).Perm (x :: l)
  | [] => List.Perm.refl _
  | y :: ys => by
    unfold insertBy
    split
    · exact ((insertBy_perm lt x ys).cons y).trans (List.Perm.swap x y ys)
    · exact List.Perm.refl _

theorem insSort_perm {α : Type} (lt : α → α → Bool) : ∀ l : List α, (insSort lt l).Perm l
  | [] => List.Perm.refl _
  | x :: l => by
    show (insertBy lt x (insSort lt l)).Perm (x :: l)
    exact (insertBy_perm lt x _).trans ((insSort_perm lt l).cons x)

theorem insertBy_pairwise {α : Type} (lt : α → α → Bool) (U : α → Prop)
    (htr : ∀ a b c, U a → U b → U c → lt a b = true → lt b c = true → lt a c = true)
    (x : α) (hx : U x) :
    ∀ S : List α, (∀ y ∈ S, lt y x = false → lt x y = true) → (∀ y ∈ S, U y) →
      S.Pairwise (fun a b => lt a b = true) → (insertBy lt x S).Pairwise (fun a b => lt a b = true)
  | [], _, _, _ => by simp [insertBy]
  | y :: ys, htot, hU, hS => by
    unfold insertBy
    rw [List.pairwise_cons] at hS
    split
    · next hyx =>
      rw [List.pairwise_cons]
      refine ⟨fun z hz => ?_, insertBy_pairwise lt U htr x hx ys (fun z hz => htot z (by simp [hz]))
        (fun z hz => hU z (by simp [hz])) hS.2⟩
      rcases List.mem_cons.1 ((insertBy_perm lt x ys).mem_iff.1 hz) with rfl | hz'
      · exact hyx
      · exact hS.1 z hz'
    · next hyx =>
      have hxy : lt x y = true := htot y List.mem_cons_self (by simpa using hyx)
      rw [List.pairwise_cons, List.pairwise_cons]
      refine ⟨fun z hz => ?_, hS.1, hS.2⟩
      rcases List.mem_cons.1 hz with rfl | hz'
      · exact hxy
      · exact htr _ _ _ hx (hU y List.mem_cons_self) (hU z (by simp [hz'])) hxy (hS.1 z hz')

/-- U6a's sortedness half, for a strict total order on the entries. -/
theorem insSort_pairwise {α : Type} (lt : α → α → Bool) : ∀ l : List α, l.Nodup →
    (∀ x ∈ l, ∀ y ∈ l, ∀ z ∈ l, lt x y = true → lt y z = true → lt x z = true) →
    (∀ x ∈ l, ∀ y ∈ l, x ≠ y → lt x y = true ∨ lt y x = true) →
    (insSort lt l).Pairwise (fun x y => lt x y = true)
  | [], _, _, _ => List.Pairwise.nil
  | x :: l, hnd, htr, htot => by
    show (insertBy lt x (insSort lt l)).Pairwise _
    have hnd' := List.nodup_cons.1 hnd
    refine insertBy_pairwise lt (· ∈ x :: l) (fun a b c ha hb hc => htr a ha b hb c hc) x List.mem_cons_self
      _ (fun y hy hyx => ?_) (fun y hy => List.mem_cons_of_mem _ ((insSort_perm lt l).mem_iff.1 hy))
      (insSort_pairwise lt l hnd'.2 (fun a ha b hb c hc => htr a (by simp [ha]) b (by simp [hb]) c (by simp [hc]))
        (fun a ha b hb => htot a (by simp [ha]) b (by simp [hb])))
    have hy' : y ∈ l := (insSort_perm lt l).mem_iff.1 hy
    have hne : x ≠ y := by rintro rfl; exact hnd'.1 hy'
    rcases htot x List.mem_cons_self y (List.mem_cons_of_mem _ hy') hne with h | h
    · exact h
    · rw [hyx] at h; exact absurd h (by simp)

theorem Obj.lt_iff : ObjLtSpec := by
  intro a b
  simp only [Obj.lt, lexLt, Bool.or_eq_true, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq,
    Bool.false_eq_true, or_false, and_false]

theorem Obj.lt_irrefl (a : Obj) : Obj.lt a a = false := by
  cases h : Obj.lt a a
  · rfl
  · have := (Obj.lt_iff a a).1 h; omega

variable {α : Type} {R : α → α → Prop}

/-- In a strictly sorted list (Pairwise `R`, `R` irreflexive and asymmetric), `R` between entries is the order of
positions. -/
theorem rel_getElem_iff {L : List α} (hp : L.Pairwise R) (hirr : ∀ x, ¬R x x)
    (hasy : ∀ x y, R x y → ¬R y x) {i j : Nat} (hi : i < L.length) (hj : j < L.length) :
    R L[i] L[j] ↔ i < j := by
  rw [List.pairwise_iff_getElem] at hp
  constructor
  · intro h
    rcases Nat.lt_trichotomy i j with hij | rfl | hij
    · exact hij
    · exact absurd h (hirr _)
    · exact absurd h (hasy _ _ (hp j i hj hi hij))
  · exact hp i j hi hj

/-- `ccwIn` between entries is cyclic betweenness of positions. -/
theorem ccwIn_getElem_iff {L : List α} (hp : L.Pairwise R) (hirr : ∀ x, ¬R x x)
    (hasy : ∀ x y, R x y → ¬R y x) {i j k : Nat} (hi : i < L.length) (hj : j < L.length) (hk : k < L.length) :
    ccwIn R L[i] L[j] L[k] ↔ (i < j ∧ j < k) ∨ (k < i ∧ i < j) ∨ (j < k ∧ k < i) := by
  simp only [ccwIn, rel_getElem_iff hp hirr hasy]

/-- Rule B: three cyclically consecutive positions are in ccw order, and nothing lies strictly between two
cyclically consecutive positions. -/
theorem ccwIn_consecutive {L : List α} (hp : L.Pairwise R) (hirr : ∀ x, ¬R x x)
    (hasy : ∀ x y, R x y → ¬R y x) (h6 : L.length = 6) {st : Nat} :
    ccwIn R (L[st % 6]'(by omega)) (L[(st + 1) % 6]'(by omega)) (L[(st + 2) % 6]'(by omega)) := by
  rw [ccwIn_getElem_iff hp hirr hasy]
  omega

theorem not_ccwIn_adjacent {L : List α} (hp : L.Pairwise R) (hirr : ∀ x, ¬R x x)
    (hasy : ∀ x y, R x y → ¬R y x) (h6 : L.length = 6) {st q : Nat} (hq : q < 6) :
    ¬ ccwIn R (L[st % 6]'(by omega)) (L[q]'(by omega)) (L[(st + 1) % 6]'(by omega)) := by
  rw [ccwIn_getElem_iff hp hirr hasy]
  omega

/-- `ccwIn` forces three distinct entries (used for `Distinct3` in rules A and B). -/
theorem ccwIn_distinct (hirr : ∀ x, ¬R x x) (hasy : ∀ x y, R x y → ¬R y x) {x z y : α}
    (h : ccwIn R x z y) : x ≠ z ∧ x ≠ y ∧ z ≠ y := by
  refine ⟨?_, ?_, ?_⟩ <;> rintro rfl <;>
    rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩ <;>
    first | exact hirr _ h1 | exact hirr _ h2 | exact hasy _ _ h1 h2 | exact hasy _ _ h2 h1

/-- `objLt` is a strict order once `psiLt` is. -/
theorem objLt_irrefl {m : Nat} {psiLt : Nat → Nat → Bool} (h : ∀ i, psiLt i i = false) (o : Pt × Bool) :
    ¬ objLt m psiLt o o := by
  rintro (h1 | ⟨_, h2⟩)
  · exact Nat.lt_irrefl _ h1
  · rw [h] at h2; exact Bool.false_ne_true h2

theorem objLt_asymm {m : Nat} {psiLt : Nat → Nat → Bool} (hirr : ∀ i, psiLt i i = false)
    (htr : ∀ i j k, psiLt i j = true → psiLt j k = true → psiLt i k = true) (o o' : Pt × Bool) :
    objLt m psiLt o o' → ¬ objLt m psiLt o' o := by
  rintro (h1 | ⟨e1, h1⟩) (h2 | ⟨e2, h2⟩)
  · omega
  · omega
  · omega
  · have := htr _ _ _ h1 h2; rw [hirr] at this; exact Bool.false_ne_true this

/-- U0 discharges the sort spec. -/
theorem sortSpec : SortSpec := fun _ lt l =>
  ⟨insSort_perm lt l, fun hnd _ htr htot => insSort_pairwise lt l hnd htr htot⟩

end EncB
