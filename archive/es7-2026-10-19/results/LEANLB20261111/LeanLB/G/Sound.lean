import LeanLB.G.Checker
import LeanLB.CheckerSound
import LeanLB.Bridge

/-!
# Soundness of the abstract checker

`LeanLB.G.lowerBound`: let `φ : P → Point`, let `op a b c = true` imply that
`orient (φ a) (φ b) (φ c) > 0`, let `op` be invariant under cyclic rotation of its arguments, and let
`ab p q = true` imply `hgt p < hgt q` for some map `hgt` to a linear order. If `gpOK op ab L` and
`checkAll op ab B L` evaluate to `true`, then the image of `L` has `L.length` points, is in general
position and has no `B + 2` points in convex position.
-/

namespace LeanLB.G

open ErdosSzekeres List

variable {P : Type}

/-! ## The programme -/

theorem bestIn_ge_init (op : P → P → P → Bool) (b c : P) :
    ∀ (r : List (P × ℕ)) (d : ℕ), d ≤ bestIn op b c d r
  | [], d => le_refl d
  | e :: r, d => by
    unfold bestIn
    refine le_trans ?_ (bestIn_ge_init op b c r _)
    cases op e.1 b c
    · exact le_refl d
    · exact le_nmax_left d e.2

theorem bestIn_ge_mem (op : P → P → P → Bool) (b c : P) :
    ∀ (r : List (P × ℕ)) (d : ℕ) (e : P × ℕ), e ∈ r →
    op e.1 b c = true → e.2 ≤ bestIn op b c d r
  | [], _, _, he, _ => by simp at he
  | f :: r, d, e, he, ho => by
    unfold bestIn
    rcases List.mem_cons.mp he with rfl | he
    · rw [ho]
      exact le_trans (le_nmax_right d e.2) (bestIn_ge_init op b c r _)
    · exact bestIn_ge_mem op b c r _ e he ho

theorem mem_newRow (op : P → P → P → Bool) (c : P) :
    ∀ (rows : List (P × List (P × ℕ))) (e : P × List (P × ℕ)),
    e ∈ rows → (e.1, bestIn op e.1 c 1 e.2 + 1) ∈ newRow op c rows
  | [], _, he => by simp at he
  | f :: rs, e, he => by
    unfold newRow
    rcases List.mem_cons.mp he with rfl | he
    · exact List.mem_cons_self
    · exact List.mem_cons_of_mem _ (mem_newRow op c rs e he)

theorem rowLe_sound (B : ℕ) : ∀ (r : List (P × ℕ)), rowLe B r = true → ∀ e ∈ r, e.2 ≤ B
  | [], _, e, he => by simp at he
  | f :: r, h, e, he => by
    unfold rowLe at h
    rw [Bool.and_eq_true, Nat.ble_eq] at h
    rcases List.mem_cons.mp he with rfl | he
    · exact h.1
    · exact rowLe_sound B r h.2 e he

theorem ins_perm (op : P → P → P → Bool) (p a : P) : ∀ l : List P, (ins op p a l).Perm (a :: l)
  | [] => List.Perm.refl _
  | b :: l => by
    unfold ins
    cases op p a b
    · exact ((ins_perm op p a l).cons b).trans (List.Perm.swap a b l)
    · exact List.Perm.refl _

theorem isort_perm (op : P → P → P → Bool) (p : P) : ∀ l : List P, (isort op p l).Perm l
  | [] => List.Perm.refl _
  | a :: l => (ins_perm op p a (isort op p l)).trans ((isort_perm op p l).cons a)

theorem pwOK_sound (op : P → P → P → Bool) (p : P) : ∀ l : List P, pwOK op p l = true →
    l.Pairwise (fun a b => op p a b = true)
  | [], _ => List.Pairwise.nil
  | a :: l, h => by
    unfold pwOK at h
    rw [Bool.and_eq_true, List.all_eq_true] at h
    exact List.Pairwise.cons h.1 (pwOK_sound op p l h.2)

/-- Every three consecutive points of the list turn left (in the sense of `op`). -/
def Good (op : P → P → P → Bool) (l : List P) : Prop :=
  ∀ a b c : P, [a, b, c] <:+: l → op a b c = true

theorem Good.of_snoc {op : P → P → P → Bool} {d : List P} {w x z : P}
    (h : Good op (d ++ [w, x, z])) : Good op (d ++ [w, x]) ∧ op w x z = true := by
  refine ⟨fun a b c habc => h a b c ?_, h w x z ?_⟩
  · refine habc.trans (List.IsPrefix.isInfix ?_)
    exact ⟨[z], by simp⟩
  · exact (List.suffix_append d [w, x, z]).isInfix

theorem runDP_sound (op : P → P → P → Bool) (B : ℕ) :
    ∀ (cs pre : List P) (rows : List (P × List (P × ℕ))),
    (∀ x ∈ pre, ∃ r, (x, r) ∈ rows) →
    (∀ d x y, d ++ [x, y] <+ pre → Good op (d ++ [x, y]) →
      ∃ r, (y, r) ∈ rows ∧ ∃ v, (x, v) ∈ r ∧ (d ++ [x, y]).length ≤ v) →
    (∀ e ∈ rows, ∀ f ∈ e.2, f.2 ≤ B) →
    runDP op B cs rows = true →
    ∀ d x y, d ++ [x, y] <+ pre ++ cs → Good op (d ++ [x, y]) → (d ++ [x, y]).length ≤ B
  | [], pre, rows, _, hI2, hI3, _ => by
    intro d x y hs hg
    rw [List.append_nil] at hs
    obtain ⟨r, hr, v, hv, hlen⟩ := hI2 d x y hs hg
    exact le_trans hlen (hI3 _ hr _ hv)
  | z :: cs, pre, rows, hI1, hI2, hI3, hrun => by
    unfold runDP at hrun
    rw [Bool.and_eq_true] at hrun
    have hnr := rowLe_sound B _ hrun.1
    have key := runDP_sound op B cs (pre ++ [z]) ((z, newRow op z rows) :: rows) ?_ ?_ ?_ hrun.2
    · intro d x y hs hg
      exact key d x y (by simpa using hs) hg
    · intro x hx
      rcases List.mem_append.mp hx with hx | hx
      · obtain ⟨r, hr⟩ := hI1 x hx
        exact ⟨r, List.mem_cons_of_mem _ hr⟩
      · rw [List.mem_singleton] at hx
        subst hx
        exact ⟨_, List.mem_cons_self⟩
    · intro d x y hs hg
      obtain ⟨l₁, l₂, heq, h₁, h₂⟩ := List.sublist_append_iff.mp hs
      rcases List.sublist_singleton.mp h₂ with rfl | rfl
      · rw [List.append_nil] at heq
        obtain ⟨r, hr, v, hv, hlen⟩ := hI2 d x y (by rw [heq]; exact h₁) hg
        exact ⟨r, List.mem_cons_of_mem _ hr, v, hv, hlen⟩
      · have heq' : (d ++ [x]) ++ [y] = l₁ ++ [z] := by simpa using heq
        obtain ⟨hl, hyz⟩ := List.append_inj' heq' rfl
        simp only [List.cons.injEq, and_true] at hyz
        subst hyz
        refine ⟨newRow op y rows, List.mem_cons_self, ?_⟩
        have hxpre : x ∈ pre := h₁.subset (by rw [← hl]; simp)
        rcases List.eq_nil_or_concat' d with rfl | ⟨d', w, rfl⟩
        · obtain ⟨r, hr⟩ := hI1 x hxpre
          refine ⟨_, mem_newRow op y rows (x, r) hr, ?_⟩
          have := bestIn_ge_init op x y r 1
          simp only [List.nil_append, List.length_cons, List.length_nil]
          omega
        · have hg' : Good op (d' ++ [w, x, y]) := by simpa using hg
          obtain ⟨hg2, hturn⟩ := hg'.of_snoc
          have hs2 : d' ++ [w, x] <+ pre := by
            rw [show d' ++ [w, x] = d' ++ [w] ++ [x] by simp, hl]; exact h₁
          obtain ⟨r, hr, v, hv, hlen⟩ := hI2 d' w x hs2 hg2
          refine ⟨_, mem_newRow op y rows (x, r) hr, ?_⟩
          have := bestIn_ge_mem op x y r 1 (w, v) hv hturn
          simp only [List.length_append, List.length_cons, List.length_nil] at hlen ⊢
          omega
    · intro e he f hf
      rcases List.mem_cons.mp he with rfl | he
      · exact hnr f hf
      · exact hI3 e he f hf

theorem runDP_sound' {op : P → P → P → Bool} {B : ℕ} {l : List P} (h : runDP op B l [] = true)
    (c : List P) (hc : c <+ l) (hg : Good op c) (h2 : 2 ≤ c.length) : c.length ≤ B := by
  rcases List.eq_nil_or_concat' c with rfl | ⟨c', y, rfl⟩
  · simp at h2
  rcases List.eq_nil_or_concat' c' with rfl | ⟨d, x, rfl⟩
  · simp at h2
  have := runDP_sound op B l [] [] (by simp) (by simp) (by simp) h d x y
    (by simpa using hc) (by simpa using hg)
  simpa using this

theorem checkFrom_trans {op : P → P → P → Bool} {ab : P → P → Bool} {B : ℕ} {L : List P}
    {a b c : ℕ} (hab : a ≤ b) (hbc : b ≤ c)
    (h1 : checkFrom op ab B L a b = true) (h2 : checkFrom op ab B L b c = true) :
    checkFrom op ab B L a c = true := by
  unfold checkFrom at *
  have e : c - a = (b - a) + (c - b) := by omega
  rw [e, List.take_add, List.drop_drop, List.all_append, Bool.and_eq_true]
  rw [show a + (b - a) = b by omega]
  exact ⟨h1, h2⟩

theorem checkAll_of_checkFrom {op : P → P → P → Bool} {ab : P → P → Bool} {B : ℕ} {L : List P}
    (h : checkFrom op ab B L 0 L.length = true) : checkAll op ab B L = true := by
  unfold checkFrom at h
  rw [List.drop_zero, Nat.sub_zero, List.take_length] at h
  exact h

/-! ## Combinatorial soundness -/

/-- The four-point sign condition. -/
def ConvexSigns (op : P → P → P → Bool) (U : Finset P) : Prop :=
  ∀ p ∈ U, ∀ a ∈ U, ∀ b ∈ U, ∀ c ∈ U,
    op p a b = true → op p a c = true → op p b c = true → op a b c = true

theorem card_le_of_check [DecidableEq P] {H : Type} [LinearOrder H] {op : P → P → P → Bool}
    {ab : P → P → Bool} {hgt : P → H} {L : List P}
    (hab : ∀ p ∈ L, ∀ q ∈ L, ab p q = true → hgt p < hgt q)
    (hne : ∀ p ∈ L, ∀ a ∈ L, ∀ b ∈ L, op p a b = true → a ≠ b)
    {B : ℕ} (hB : 1 ≤ B) (h : checkAll op ab B L = true)
    (U : Finset P) (hU : ∀ x ∈ U, x ∈ L)
    (htot : ∀ p ∈ U, ∀ q ∈ U, p ≠ q → ab p q = true ∨ ab q p = true)
    (hcs : ConvexSigns op U) : U.card ≤ B + 1 := by
  by_cases hsmall : U.card ≤ 2
  · omega
  have hUne : U.Nonempty := Finset.card_pos.mp (by omega)
  obtain ⟨p, hp, hmin⟩ := U.exists_min_image hgt hUne
  have hbot : ∀ q ∈ U, q ≠ p → ab p q = true := by
    intro q hq hqp
    rcases htot p hp q hq (Ne.symm hqp) with h1 | h1
    · exact h1
    · exact absurd (hmin q hq) (not_le.mpr (hab q (hU q hq) p (hU p hp) h1))
  have hanchor : anchorOK op ab B L p = true := (List.all_eq_true.mp h) p (hU p hp)
  unfold anchorOK at hanchor
  rw [Bool.and_eq_true] at hanchor
  set l := isort op p (L.filter (ab p)) with hl
  have hpw := pwOK_sound op p l hanchor.1
  set chain := l.filter (fun x => decide (x ∈ U)) with hchain
  have hsub : chain <+ l := List.filter_sublist
  have hpwc := hpw.sublist hsub
  have hmem : ∀ x, x ∈ chain ↔ x ∈ U ∧ x ≠ p := by
    intro x
    rw [hchain, List.mem_filter, hl, (isort_perm op p _).mem_iff, List.mem_filter,
      decide_eq_true_iff]
    constructor
    · rintro ⟨⟨hxL, hx'⟩, hx⟩
      refine ⟨hx, ?_⟩
      rintro rfl
      exact lt_irrefl _ (hab x hxL x hxL hx')
    · rintro ⟨hx, hxp⟩
      exact ⟨⟨hU x hx, hbot x hx hxp⟩, hx⟩
  have hchainL : ∀ x ∈ chain, x ∈ L := fun x hx => hU x ((hmem x).mp hx).1
  have hnodup : chain.Nodup := hpwc.imp_of_mem (fun {a b} ha hb hab' =>
    hne p (hU p hp) a (hchainL a ha) b (hchainL b hb) hab')
  have hlen : chain.length = U.card - 1 := by
    rw [← List.toFinset_card_of_nodup hnodup, ← Finset.card_erase_of_mem hp]
    congr 1
    ext x
    rw [List.mem_toFinset, hmem, Finset.mem_erase]
    tauto
  have hgood : Good op chain := by
    intro a b c habc
    have hs : [a, b, c] <+ chain := habc.sublist
    have hp3 := hpwc.sublist hs
    simp only [List.pairwise_cons, List.mem_cons, forall_eq_or_imp, List.not_mem_nil,
      IsEmpty.forall_iff, implies_true, List.Pairwise.nil, and_true] at hp3
    have ha := (hmem a).mp (hs.subset (by simp))
    have hb := (hmem b).mp (hs.subset (by simp))
    have hc := (hmem c).mp (hs.subset (by simp))
    exact hcs p hp a ha.1 b hb.1 c hc.1 hp3.1.1 hp3.1.2 hp3.2
  have := runDP_sound' hanchor.2 chain hsub hgood (by omega)
  omega

/-! ## The list checks -/

theorem gpPairs_sound (op : P → P → P → Bool) (a : P) : ∀ l : List P, gpOK.gpPairs op a l = true →
    l.Pairwise (fun b c => (op a b c || op a c b) = true)
  | [], _ => List.Pairwise.nil
  | b :: l, h => by
    unfold gpOK.gpPairs at h
    rw [Bool.and_eq_true, List.all_eq_true] at h
    exact List.Pairwise.cons h.1 (gpPairs_sound op a l h.2)

theorem gpOK_sound {op : P → P → P → Bool} {ab : P → P → Bool}
    (hcyc : ∀ a b c, op b c a = op a b c) :
    ∀ l : List P, gpOK op ab l = true →
    (l.Pairwise fun a b => (ab a b || ab b a) = true) ∧
    ∀ a ∈ l, ∀ b ∈ l, ∀ c ∈ l, a ≠ b → a ≠ c → b ≠ c → (op a b c || op a c b) = true
  | [], _ => ⟨List.Pairwise.nil, by simp⟩
  | h :: t, hg => by
    unfold gpOK at hg
    simp only [Bool.and_eq_true, List.all_eq_true] at hg
    obtain ⟨⟨hd, hp⟩, ht⟩ := hg
    obtain ⟨htn, htg⟩ := gpOK_sound hcyc t ht
    have hpair := (gpPairs_sound op h t hp).forall
      (fun b c hbc => by rw [Bool.or_comm]; exact hbc)
    have hh : ∀ b ∈ t, ∀ c ∈ t, b ≠ c → (op h b c || op h c b) = true := fun b hb c hc hbc =>
      hpair hb hc hbc
    -- permutations: `op x y z || op x z y` is invariant under all permutations
    have e1 : ∀ x y z, (op y x z || op y z x) = (op x y z || op x z y) := by
      intro x y z
      rw [hcyc x y z, hcyc z y x, hcyc x z y, Bool.or_comm]
    have e2 : ∀ x y z, (op z x y || op z y x) = (op x y z || op x z y) := by
      intro x y z
      rw [hcyc y z x, hcyc x y z, hcyc x z y]
    refine ⟨List.Pairwise.cons hd htn, ?_⟩
    intro a ha b hb c hc hab hac hbc
    rcases List.mem_cons.mp ha with ha' | ha' <;> rcases List.mem_cons.mp hb with hb' | hb' <;>
      rcases List.mem_cons.mp hc with hc' | hc'
    · exact absurd (ha'.trans hb'.symm) hab
    · exact absurd (ha'.trans hb'.symm) hab
    · exact absurd (ha'.trans hc'.symm) hac
    · subst ha'; exact hh b hb' c hc' hbc
    · exact absurd (hb'.trans hc'.symm) hbc
    · subst hb'; rw [← e1]; exact hh a ha' c hc' hac
    · subst hc'; rw [← e2]; exact hh a ha' b hb' hab
    · exact htg a ha' b hb' c hc' hab hac hbc

end LeanLB.G
