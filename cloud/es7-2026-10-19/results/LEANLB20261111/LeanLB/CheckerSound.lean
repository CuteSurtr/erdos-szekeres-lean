import LeanLB.Checker
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Max
import Mathlib.Data.List.Pairwise
import Mathlib.Data.List.Basic
import Mathlib.Data.Prod.Lex
import Mathlib.Order.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# Soundness of the checker (combinatorial part)

`card_le_of_check`: if `checkAll B L = true`, then every finite set `U` of points of `L` whose
orientation signs satisfy the four-point condition `ConvexSigns` has at most `B + 1` elements.
`gpOK_sound`: if `gpOK L = true`, the list has no repeated point and no three distinct points of it
have orientation determinant `0`.
-/

namespace LeanLB

open List

/-! ## Integer orientation -/

/-- The orientation determinant of three lattice points, over `ℤ`. -/
def oz (a b c : NP) : ℤ :=
  ((b.1 : ℤ) - a.1) * ((c.2 : ℤ) - a.2) - ((b.2 : ℤ) - a.2) * ((c.1 : ℤ) - a.1)

theorem oz_eq (a b c : NP) :
    oz a b c = ((a.1 * b.2 + b.1 * c.2 + c.1 * a.2 : ℕ) : ℤ) -
      ((a.2 * b.1 + b.2 * c.1 + c.2 * a.1 : ℕ) : ℤ) := by
  unfold oz; push_cast; ring

theorem opos_iff (a b c : NP) : opos a b c = true ↔ 0 < oz a b c := by
  rw [oz_eq]; unfold opos; rw [Nat.blt_eq]; omega

theorem nz_iff (a b c : NP) : nz a b c = true ↔ oz a b c ≠ 0 := by
  rw [oz_eq]; unfold nz
  rw [Bool.not_eq_true', ← Bool.not_eq_true, Nat.beq_eq]
  omega

theorem oz_swap12 (a b c : NP) : oz b a c = -oz a b c := by unfold oz; ring
theorem oz_swap23 (a b c : NP) : oz a c b = -oz a b c := by unfold oz; ring
theorem oz_cycle (a b c : NP) : oz b c a = oz a b c := by unfold oz; ring
theorem oz_self12 (a c : NP) : oz a a c = 0 := by unfold oz; ring
theorem oz_self23 (a b : NP) : oz a b b = 0 := by unfold oz; ring

theorem ne_of_opos {p a b : NP} (h : opos p a b = true) : p ≠ a ∧ p ≠ b ∧ a ≠ b := by
  rw [opos_iff] at h
  refine ⟨?_, ?_, ?_⟩
  · rintro rfl; rw [oz_self12] at h; exact lt_irrefl _ h
  · rintro rfl; rw [oz_swap23, oz_self12] at h; simp at h
  · rintro rfl; rw [oz_self23] at h; exact lt_irrefl _ h

/-! ## Small lemmas on the checker's functions -/

theorem nmax_eq (a b : ℕ) : nmax a b = max a b := by
  unfold nmax
  by_cases h : a < b
  · have h' : Nat.blt a b = true := Nat.blt_eq.mpr h
    rw [h', max_eq_right h.le]; rfl
  · have h' : Nat.blt a b = false := by
      rw [← Bool.not_eq_true, Nat.blt_eq]; exact h
    rw [h', max_eq_left (not_lt.mp h)]; rfl

theorem le_nmax_left (a b : ℕ) : a ≤ nmax a b := by rw [nmax_eq]; exact le_max_left a b

theorem le_nmax_right (a b : ℕ) : b ≤ nmax a b := by rw [nmax_eq]; exact le_max_right a b

theorem bestIn_ge_init (b c : NP) : ∀ (r : List (NP × ℕ)) (d : ℕ), d ≤ bestIn b c d r
  | [], d => le_refl d
  | e :: r, d => by
    unfold bestIn
    refine le_trans ?_ (bestIn_ge_init b c r _)
    cases opos e.1 b c
    · exact le_refl d
    · exact le_nmax_left d e.2

theorem bestIn_ge_mem (b c : NP) : ∀ (r : List (NP × ℕ)) (d : ℕ) (e : NP × ℕ), e ∈ r →
    opos e.1 b c = true → e.2 ≤ bestIn b c d r
  | [], _, _, he, _ => by simp at he
  | f :: r, d, e, he, ho => by
    unfold bestIn
    rcases List.mem_cons.mp he with rfl | he
    · rw [ho]
      exact le_trans (le_nmax_right d e.2) (bestIn_ge_init b c r _)
    · exact bestIn_ge_mem b c r _ e he ho

theorem mem_newRow (c : NP) : ∀ (rows : List (NP × List (NP × ℕ))) (e : NP × List (NP × ℕ)),
    e ∈ rows → (e.1, bestIn e.1 c 1 e.2 + 1) ∈ newRow c rows
  | [], _, he => by simp at he
  | f :: rs, e, he => by
    unfold newRow
    rcases List.mem_cons.mp he with rfl | he
    · exact List.mem_cons_self
    · exact List.mem_cons_of_mem _ (mem_newRow c rs e he)

theorem rowLe_sound (B : ℕ) : ∀ (r : List (NP × ℕ)), rowLe B r = true → ∀ e ∈ r, e.2 ≤ B
  | [], _, e, he => by simp at he
  | f :: r, h, e, he => by
    unfold rowLe at h
    rw [Bool.and_eq_true, Nat.ble_eq] at h
    rcases List.mem_cons.mp he with rfl | he
    · exact h.1
    · exact rowLe_sound B r h.2 e he

theorem ins_perm (p a : NP) : ∀ l : List NP, (ins p a l).Perm (a :: l)
  | [] => List.Perm.refl _
  | b :: l => by
    unfold ins
    cases opos p a b
    · exact ((ins_perm p a l).cons b).trans (List.Perm.swap a b l)
    · exact List.Perm.refl _

theorem isort_perm (p : NP) : ∀ l : List NP, (isort p l).Perm l
  | [] => List.Perm.refl _
  | a :: l => (ins_perm p a (isort p l)).trans ((isort_perm p l).cons a)

theorem pwOK_sound (p : NP) : ∀ l : List NP, pwOK p l = true →
    l.Pairwise (fun a b => opos p a b = true)
  | [], _ => List.Pairwise.nil
  | a :: l, h => by
    unfold pwOK at h
    rw [Bool.and_eq_true, List.all_eq_true] at h
    exact List.Pairwise.cons h.1 (pwOK_sound p l h.2)

/-! ## Chains with left turns -/

/-- Every three consecutive points of the list turn left. -/
def Good (l : List NP) : Prop :=
  ∀ a b c : NP, [a, b, c] <:+: l → opos a b c = true

theorem Good.of_snoc {d : List NP} {w x z : NP} (h : Good (d ++ [w, x, z])) :
    Good (d ++ [w, x]) ∧ opos w x z = true := by
  refine ⟨fun a b c habc => h a b c ?_, h w x z ?_⟩
  · refine habc.trans (List.IsPrefix.isInfix ?_)
    exact ⟨[z], by simp⟩
  · exact (List.suffix_append d [w, x, z]).isInfix

/-! ## The dynamic programme -/

theorem runDP_sound (B : ℕ) : ∀ (cs pre : List NP) (rows : List (NP × List (NP × ℕ))),
    (∀ x ∈ pre, ∃ r, (x, r) ∈ rows) →
    (∀ d x y, d ++ [x, y] <+ pre → Good (d ++ [x, y]) →
      ∃ r, (y, r) ∈ rows ∧ ∃ v, (x, v) ∈ r ∧ (d ++ [x, y]).length ≤ v) →
    (∀ e ∈ rows, ∀ f ∈ e.2, f.2 ≤ B) →
    runDP B cs rows = true →
    ∀ d x y, d ++ [x, y] <+ pre ++ cs → Good (d ++ [x, y]) → (d ++ [x, y]).length ≤ B
  | [], pre, rows, _, hI2, hI3, _ => by
    intro d x y hs hg
    rw [List.append_nil] at hs
    obtain ⟨r, hr, v, hv, hlen⟩ := hI2 d x y hs hg
    exact le_trans hlen (hI3 _ hr _ hv)
  | z :: cs, pre, rows, hI1, hI2, hI3, hrun => by
    unfold runDP at hrun
    rw [Bool.and_eq_true] at hrun
    have hnr := rowLe_sound B _ hrun.1
    have key := runDP_sound B cs (pre ++ [z]) ((z, newRow z rows) :: rows) ?_ ?_ ?_ hrun.2
    · intro d x y hs hg
      exact key d x y (by simpa using hs) hg
    · -- invariant 1
      intro x hx
      rcases List.mem_append.mp hx with hx | hx
      · obtain ⟨r, hr⟩ := hI1 x hx
        exact ⟨r, List.mem_cons_of_mem _ hr⟩
      · rw [List.mem_singleton] at hx
        subst hx
        exact ⟨_, List.mem_cons_self⟩
    · -- invariant 2
      intro d x y hs hg
      obtain ⟨l₁, l₂, heq, h₁, h₂⟩ := List.sublist_append_iff.mp hs
      rcases List.sublist_singleton.mp h₂ with rfl | rfl
      · rw [List.append_nil] at heq
        obtain ⟨r, hr, v, hv, hlen⟩ := hI2 d x y (by rw [heq]; exact h₁) hg
        exact ⟨r, List.mem_cons_of_mem _ hr, v, hv, hlen⟩
      · have heq' : (d ++ [x]) ++ [y] = l₁ ++ [z] := by simpa using heq
        obtain ⟨hl, hyz⟩ := List.append_inj' heq' rfl
        simp only [List.cons.injEq, and_true] at hyz
        subst hyz
        refine ⟨newRow y rows, List.mem_cons_self, ?_⟩
        have hxpre : x ∈ pre := h₁.subset (by rw [← hl]; simp)
        rcases List.eq_nil_or_concat' d with rfl | ⟨d', w, rfl⟩
        · obtain ⟨r, hr⟩ := hI1 x hxpre
          refine ⟨_, mem_newRow y rows (x, r) hr, ?_⟩
          have := bestIn_ge_init x y r 1
          simp only [List.nil_append, List.length_cons, List.length_nil]
          omega
        · have hg' : Good (d' ++ [w, x, y]) := by simpa using hg
          obtain ⟨hg2, hturn⟩ := hg'.of_snoc
          have hs2 : d' ++ [w, x] <+ pre := by
            rw [show d' ++ [w, x] = d' ++ [w] ++ [x] by simp, hl]; exact h₁
          obtain ⟨r, hr, v, hv, hlen⟩ := hI2 d' w x hs2 hg2
          refine ⟨_, mem_newRow y rows (x, r) hr, ?_⟩
          have := bestIn_ge_mem x y r 1 (w, v) hv hturn
          simp only [List.length_append, List.length_cons, List.length_nil] at hlen ⊢
          omega
    · -- invariant 3
      intro e he f hf
      rcases List.mem_cons.mp he with rfl | he
      · exact hnr f hf
      · exact hI3 e he f hf

theorem runDP_sound' {B : ℕ} {l : List NP} (h : runDP B l [] = true) (c : List NP)
    (hc : c <+ l) (hg : Good c) (h2 : 2 ≤ c.length) : c.length ≤ B := by
  rcases List.eq_nil_or_concat' c with rfl | ⟨c', y, rfl⟩
  · simp at h2
  rcases List.eq_nil_or_concat' c' with rfl | ⟨d, x, rfl⟩
  · simp at h2
  have := runDP_sound B l [] [] (by simp) (by simp) (by simp) h d x y
    (by simpa using hc) (by simpa using hg)
  simpa using this

/-! ## From sets in convex position to chains -/

/-- The four-point condition: a point `b` that lies counterclockwise between `a` and `c` around `p`
(with `a, c` counterclockwise around `p`) is not inside the triangle `p a c`, i.e. `a, b, c` turn
left. It holds for every set in convex position (`LeanLB.convexSigns_of_convexPosition`). -/
def ConvexSigns (U : Finset NP) : Prop :=
  ∀ p ∈ U, ∀ a ∈ U, ∀ b ∈ U, ∀ c ∈ U,
    opos p a b = true → opos p a c = true → opos p b c = true → opos a b c = true

theorem above_iff (p q : NP) : above p q = true ↔ p.2 < q.2 ∨ (p.2 = q.2 ∧ p.1 < q.1) := by
  unfold above
  simp [Nat.blt_eq, Nat.beq_eq]

theorem exists_bottom (U : Finset NP) (hU : U.Nonempty) :
    ∃ p ∈ U, ∀ q ∈ U, q ≠ p → above p q = true := by
  obtain ⟨p, hp, hmin⟩ := U.exists_min_image (fun q : NP => toLex (q.2, q.1)) hU
  refine ⟨p, hp, fun q hq hne => ?_⟩
  have h := hmin q hq
  rw [Prod.Lex.toLex_le_toLex] at h
  rw [above_iff]
  rcases h with h | ⟨h1, h2⟩
  · exact Or.inl h
  · refine Or.inr ⟨h1, lt_of_le_of_ne h2 ?_⟩
    intro h3
    exact hne (Prod.ext h3.symm h1.symm)

theorem card_le_of_check {B : ℕ} (hB : 1 ≤ B) {L : List NP} (h : checkAll B L = true)
    (U : Finset NP) (hU : ∀ x ∈ U, x ∈ L) (hcs : ConvexSigns U) : U.card ≤ B + 1 := by
  classical
  by_cases hsmall : U.card ≤ 2
  · omega
  have hne : U.Nonempty := Finset.card_pos.mp (by omega)
  obtain ⟨p, hp, hbot⟩ := exists_bottom U hne
  have hanchor : anchorOK B L p = true := (List.all_eq_true.mp h) p (hU p hp)
  unfold anchorOK at hanchor
  rw [Bool.and_eq_true] at hanchor
  set l := isort p (L.filter (above p)) with hl
  have hpw := pwOK_sound p l hanchor.1
  set chain := l.filter (fun x => decide (x ∈ U)) with hchain
  have hsub : chain <+ l := List.filter_sublist
  have hpwc := hpw.sublist hsub
  have hmem : ∀ x, x ∈ chain ↔ x ∈ U ∧ x ≠ p := by
    intro x
    rw [hchain, List.mem_filter, hl, (isort_perm p _).mem_iff, List.mem_filter, decide_eq_true_iff]
    constructor
    · rintro ⟨⟨_, hab⟩, hx⟩
      refine ⟨hx, ?_⟩
      rintro rfl
      rw [above_iff] at hab
      omega
    · rintro ⟨hx, hxp⟩
      exact ⟨⟨hU x hx, hbot x hx hxp⟩, hx⟩
  have hnodup : chain.Nodup := hpwc.imp (fun hab => (ne_of_opos hab).2.2)
  have hlen : chain.length = U.card - 1 := by
    rw [← List.toFinset_card_of_nodup hnodup, ← Finset.card_erase_of_mem hp]
    congr 1
    ext x
    rw [List.mem_toFinset, hmem, Finset.mem_erase]
    tauto
  have hgood : Good chain := by
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

/-! ## Splitting the check into ranges of anchors -/

theorem checkFrom_trans {B : ℕ} {L : List NP} {a b c : ℕ} (hab : a ≤ b) (hbc : b ≤ c)
    (h1 : checkFrom B L a b = true) (h2 : checkFrom B L b c = true) : checkFrom B L a c = true := by
  unfold checkFrom at *
  have e : c - a = (b - a) + (c - b) := by omega
  rw [e, List.take_add, List.drop_drop, List.all_append, Bool.and_eq_true]
  rw [show a + (b - a) = b by omega]
  exact ⟨h1, h2⟩

theorem checkAll_of_checkFrom {B : ℕ} {L : List NP} (h : checkFrom B L 0 L.length = true) :
    checkAll B L = true := by
  unfold checkFrom at h
  rw [List.drop_zero, Nat.sub_zero, List.take_length] at h
  exact h

/-! ## General position -/

theorem gpPairs_sound (a : NP) : ∀ l : List NP, gpOK.gpPairs a l = true →
    l.Pairwise (fun b c => nz a b c = true)
  | [], _ => List.Pairwise.nil
  | b :: l, h => by
    unfold gpOK.gpPairs at h
    rw [Bool.and_eq_true, List.all_eq_true] at h
    exact List.Pairwise.cons h.1 (gpPairs_sound a l h.2)

theorem nz_symm23 (a b c : NP) : nz a b c = true → nz a c b = true := by
  intro h
  rw [nz_iff] at h ⊢
  rw [oz_swap23]
  exact neg_ne_zero.mpr h

theorem gpOK_sound : ∀ l : List NP, gpOK l = true →
    l.Nodup ∧ ∀ a ∈ l, ∀ b ∈ l, ∀ c ∈ l, a ≠ b → a ≠ c → b ≠ c → oz a b c ≠ 0
  | [], _ => ⟨List.nodup_nil, by simp⟩
  | h :: t, hg => by
    unfold gpOK at hg
    simp only [Bool.and_eq_true, List.all_eq_true] at hg
    obtain ⟨⟨hd, hp⟩, ht⟩ := hg
    obtain ⟨htn, htg⟩ := gpOK_sound t ht
    have hne : ∀ x ∈ t, h ≠ x := by
      intro x hx hhx
      have := hd x hx
      subst hhx
      simp [Nat.beq_refl] at this
    have hpair := (gpPairs_sound h t hp).forall (fun b c hbc => nz_symm23 h b c hbc)
    have hh : ∀ b ∈ t, ∀ c ∈ t, b ≠ c → oz h b c ≠ 0 := fun b hb c hc hbc =>
      (nz_iff h b c).mp (hpair hb hc hbc)
    refine ⟨List.nodup_cons.mpr ⟨fun hmem => hne h hmem rfl, htn⟩, ?_⟩
    intro a ha b hb c hc hab hac hbc
    rcases List.mem_cons.mp ha with ha' | ha' <;> rcases List.mem_cons.mp hb with hb' | hb' <;>
      rcases List.mem_cons.mp hc with hc' | hc'
    · exact absurd (ha'.trans hb'.symm) hab
    · exact absurd (ha'.trans hb'.symm) hab
    · exact absurd (ha'.trans hc'.symm) hac
    · subst ha'; exact hh b hb' c hc' hbc
    · exact absurd (hb'.trans hc'.symm) hbc
    · subst hb'; rw [oz_swap12]; exact neg_ne_zero.mpr (hh a ha' c hc' hac)
    · subst hc'; rw [oz_cycle]; exact hh a ha' b hb' hab
    · exact htg a ha' b hb' c hc' hab hac hbc

end LeanLB
