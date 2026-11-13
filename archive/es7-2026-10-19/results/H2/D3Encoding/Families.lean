import D3Encoding.TripleTable

/-!
# Soundness of the orientation-only clause families

Axioms (A4, Grassmann–Plücker), centre facts and the labelling normal form. Each family is
stated for a literal function `lit tv` whose truth is described by `lit_spec`.
-/

namespace D3

open Std

def ClauseSat (ν : Nat → Bool) (c : List Int) : Prop := ∃ l ∈ c, LitSat ν l

/-- The standing assumptions of this file: a consistent and complete triple table and an
assignment `ν` that agrees with it on the triple variables. -/
structure TableModel (t : Nat) (χ : Nat → Nat → Nat → Int) (tv : TV) (n : Nat)
    (ν : Nat → Bool) : Prop where
  chi : Chirotope t χ
  inv : TInv χ (3 * t + 1) tv n
  cov : ∀ a b c, a < b → b < c → c < 3 * t + 1 → (tv[(a, b, c)]?).isSome
  nu : ∀ v, 1 ≤ v → v ≤ n → (ν v = true ↔ NuT χ tv v)

/-- A template entry `(σ, a, b, c)` stands for the literal `σ · lit(a, b, c)`. -/
def GoodEntry (P : Nat) (e : Int × Nat × Nat × Nat) : Prop :=
  (e.1 = 1 ∨ e.1 = -1) ∧ e.2.1 < P ∧ e.2.2.1 < P ∧ e.2.2.2 < P ∧ e.2.1 ≠ e.2.2.1 ∧
    e.2.1 ≠ e.2.2.2 ∧ e.2.2.1 ≠ e.2.2.2

theorem clauseSat_template {t : Nat} {χ : Nat → Nat → Nat → Int} {tv : TV} {n : Nat}
    {ν : Nat → Bool} (M : TableModel t χ tv n ν) (cl : List (Int × Nat × Nat × Nat))
    (hcl : ∀ e ∈ cl, GoodEntry (3 * t + 1) e)
    (h : ∃ e ∈ cl, e.1 * χ e.2.1 e.2.2.1 e.2.2.2 = 1) :
    ClauseSat ν (cl.map fun e => e.1 * lit tv e.2.1 e.2.2.1 e.2.2.2) := by
  obtain ⟨e, he, h1⟩ := h
  obtain ⟨hs, ha, hb, hc, hab, hac, hbc⟩ := hcl e he
  exact ⟨_, List.mem_map_of_mem he,
    (lit_spec M.chi M.inv M.cov M.nu ha hb hc hab hac hbc hs).2 h1⟩

/-! ### Semantic hypotheses on `χ` -/

/-- Knuth's interiority axiom (A4) on all ordered quadruples of distinct points. -/
def A4 (P : Nat) (χ : Nat → Nat → Nat → Int) : Prop :=
  ∀ p q r x, p < P → q < P → r < P → x < P → p ≠ q → p ≠ r → p ≠ x → q ≠ r → q ≠ x →
    r ≠ x → ∀ s : Int, (s = 1 ∨ s = -1) →
      χ x q r = s → χ p x r = s → χ p q x = s → χ p q r = s

/-- The 3-term Grassmann–Plücker relations: the three products are neither all positive
nor all negative. -/
def GP3 (P : Nat) (χ : Nat → Nat → Nat → Int) : Prop :=
  ∀ x y1 y2 y3 y4, x < P → y1 < P → y2 < P → y3 < P → y4 < P → x ≠ y1 → x ≠ y2 → x ≠ y3 →
    x ≠ y4 → y1 ≠ y2 → y1 ≠ y3 → y1 ≠ y4 → y2 ≠ y3 → y2 ≠ y4 → y3 ≠ y4 →
    ¬(0 < χ x y1 y2 * χ x y3 y4 ∧ 0 < -(χ x y1 y3 * χ x y2 y4) ∧ 0 < χ x y1 y4 * χ x y2 y3) ∧
    ¬(χ x y1 y2 * χ x y3 y4 < 0 ∧ -(χ x y1 y3 * χ x y2 y4) < 0 ∧ χ x y1 y4 * χ x y2 y3 < 0)

/-- The centre facts: seen from the centre `3 t`, `R a` is to the left of `a`, `R² a` to
the right. -/
def CenterFacts (t : Nat) (χ : Nat → Nat → Nat → Int) : Prop :=
  ∀ a, a < 3 * t → χ (3 * t) a (rot (3 * t) 1 a) = 1 ∧ χ (3 * t) a (rot (3 * t) 2 a) = -1

/-- The labelling normal form: each representative `(o, 0)`, `o ≥ 1`, lies in the open
sector from `(0, 0)` to `(0, 1)` seen from the centre, and they are sorted by angle. -/
def SectorOrder (t : Nat) (χ : Nat → Nat → Nat → Int) : Prop :=
  (∀ o, 1 ≤ o → o < t → χ (3 * t) 0 (3 * o) = 1 ∧ χ (3 * t) 1 (3 * o) = -1) ∧
  ∀ o o2, 1 ≤ o → o < o2 → o2 < t → χ (3 * t) (3 * o) (3 * o2) = 1

/-! ### Families -/

section
variable {t : Nat} {χ : Nat → Nat → Nat → Int} {tv : TV} {n : Nat} {ν : Nat → Bool}

theorem pairwise_lt_nodup {l : List Nat} (h : l.Pairwise (· < ·)) : l.Nodup :=
  h.imp fun hab => Nat.ne_of_lt hab

theorem filter_ne_spec {S : List Nat} {x : Nat} {l : List Nat} (hS : S.Pairwise (· < ·))
    (h : S.filter (· != x) = l) : l.Pairwise (· < ·) ∧ ∀ y ∈ l, y ∈ S ∧ y ≠ x := by
  subst h
  refine ⟨hS.filter _, fun y hy => ?_⟩
  rw [List.mem_filter] at hy
  exact ⟨hy.1, by simpa using hy.2⟩

theorem sign_cases {s : Int} (hs : s = 1 ∨ s = -1) {w : Int} (hw : w = 1 ∨ w = -1) :
    s * w = 1 ↔ w = s := by
  rcases hs with rfl | rfl <;> rcases hw with rfl | rfl <;> decide

theorem a4_sat (M : TableModel t χ tv n ν) (hA4 : A4 (3 * t + 1) χ) {S : List Nat}
    (hS : S ∈ combs (List.range (3 * t + 1)) 4) {c : List Int}
    (hc : c ∈ a4Clauses (lit tv) S) : ClauseSat ν c := by
  rw [mem_combs_range] at hS
  obtain ⟨hp, hlt, -⟩ := hS
  unfold a4Clauses at hc
  rw [List.mem_flatMap] at hc
  obtain ⟨x, hx, hc⟩ := hc
  split at hc
  · rename_i p q r hf
    obtain ⟨hp3, hm⟩ := filter_ne_spec hp hf
    simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false,
      forall_eq_or_imp, forall_eq, List.Pairwise.nil] at hp3
    obtain ⟨hpS, hpx⟩ := hm p (by simp)
    obtain ⟨hqS, hqx⟩ := hm q (by simp)
    obtain ⟨hrS, hrx⟩ := hm r (by simp)
    have hxP := hlt x hx
    have hpP := hlt p hpS
    have hqP := hlt q hqS
    have hrP := hlt r hrS
    simp only [List.mem_map, List.mem_cons, List.not_mem_nil, or_false] at hc
    obtain ⟨s, hs, rfl⟩ := hc
    have hs' : s = 1 ∨ s = -1 := hs
    have := clauseSat_template M [(-s, x, q, r), (-s, p, x, r), (-s, p, q, x), (s, p, q, r)]
      (by
        intro e he
        simp only [List.mem_cons, List.not_mem_nil, or_false] at he
        rcases he with rfl | rfl | rfl | rfl <;>
          refine ⟨by rcases hs' with rfl | rfl <;> simp, ?_⟩ <;> simp only <;> omega)
      (by
        have hsg := M.chi.sign
        have w1 := hsg x q r hxP hqP hrP (by omega) (by omega) (by omega)
        have w2 := hsg p x r hpP hxP hrP (by omega) (by omega) (by omega)
        have w3 := hsg p q x hpP hqP hxP (by omega) (by omega) (by omega)
        have w4 := hsg p q r hpP hqP hrP (by omega) (by omega) (by omega)
        have key := hA4 p q r x hpP hqP hrP hxP (by omega) (by omega) (by omega) (by omega)
          (by omega) (by omega) s hs'
        simp only [List.mem_cons, List.not_mem_nil, or_false, exists_eq_or_imp, exists_eq_left]
        rcases hs' with rfl | rfl <;> rcases w1 with h1 | h1 <;> rcases w2 with h2 | h2 <;>
          rcases w3 with h3 | h3 <;> rcases w4 with h4 | h4 <;> simp only [h1, h2, h3, h4] <;>
          first | omega | (exfalso; have := key (by omega) (by omega) (by omega); omega))
    simpa using this
  · simp at hc

theorem eq_neg_of_ne {s w : Int} (hs : s = 1 ∨ s = -1) (hw : w = 1 ∨ w = -1) (h : ¬s * w = 1) :
    w = -s := by
  rcases hs with rfl | rfl <;> rcases hw with rfl | rfl <;> simp_all

theorem gp_sat (M : TableModel t χ tv n ν) (hGP : GP3 (3 * t + 1) χ) {S : List Nat}
    (hS : S ∈ combs (List.range (3 * t + 1)) 5) {c : List Int}
    (hc : c ∈ gpClauses (lit tv) S) : ClauseSat ν c := by
  rw [mem_combs_range] at hS
  obtain ⟨hp, hlt, -⟩ := hS
  unfold gpClauses at hc
  rw [List.mem_flatMap] at hc
  obtain ⟨x, hx, hc⟩ := hc
  split at hc
  · rename_i y1 y2 y3 y4 hf
    obtain ⟨hp4, hm⟩ := filter_ne_spec hp hf
    simp only [List.pairwise_cons, List.mem_cons, List.not_mem_nil, or_false,
      forall_eq_or_imp, forall_eq, List.Pairwise.nil] at hp4
    obtain ⟨h1S, h1x⟩ := hm y1 (by simp)
    obtain ⟨h2S, h2x⟩ := hm y2 (by simp)
    obtain ⟨h3S, h3x⟩ := hm y3 (by simp)
    obtain ⟨h4S, h4x⟩ := hm y4 (by simp)
    have hxP := hlt x hx
    have h1P := hlt y1 h1S
    have h2P := hlt y2 h2S
    have h3P := hlt y3 h3S
    have h4P := hlt y4 h4S
    clear hm hf hlt hp
    have good : ∀ (σ : Int) (a b : Nat), (σ = 1 ∨ σ = -1) → a ∈ [y1, y2, y3, y4] →
        b ∈ [y1, y2, y3, y4] → a ≠ b → GoodEntry (3 * t + 1) (σ, x, a, b) := by
      intro σ a b hσ ha hb hab
      simp only [List.mem_cons, List.not_mem_nil, or_false] at ha hb
      refine ⟨hσ, hxP, ?_, ?_, ?_, ?_, hab⟩ <;> simp only <;> omega
    have hsg := M.chi.sign
    have w12 := hsg x y1 y2 hxP h1P h2P (by omega) (by omega) (by omega)
    have w34 := hsg x y3 y4 hxP h3P h4P (by omega) (by omega) (by omega)
    have w13 := hsg x y1 y3 hxP h1P h3P (by omega) (by omega) (by omega)
    have w24 := hsg x y2 y4 hxP h2P h4P (by omega) (by omega) (by omega)
    have w14 := hsg x y1 y4 hxP h1P h4P (by omega) (by omega) (by omega)
    have w23 := hsg x y2 y3 hxP h2P h3P (by omega) (by omega) (by omega)
    have key := hGP x y1 y2 y3 y4 hxP h1P h2P h3P h4P (by omega) (by omega) (by omega)
      (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
    rw [List.mem_flatMap] at hc
    obtain ⟨⟨s1, s2, s3⟩, hs, hc⟩ := hc
    have hs' : (s1 = 1 ∨ s1 = -1) ∧ (s2 = 1 ∨ s2 = -1) ∧ (s3 = 1 ∨ s3 = -1) := by
      simp only [signs3, List.mem_cons, List.not_mem_nil, or_false, Prod.mk.injEq] at hs
      rcases hs with h | h | h | h | h | h | h | h <;> simp [h]
    obtain ⟨hs1, hs2, hs3⟩ := hs'
    have n1 : ∀ s : Int, (s = 1 ∨ s = -1) → (-s = 1 ∨ -s = -1) := by
      intro s hs; rcases hs with rfl | rfl <;> simp
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hc
    rcases hc with rfl | rfl
    · have := clauseSat_template M [(-s1, x, y1, y2), (-s1, x, y3, y4), (-s2, x, y1, y3),
          (s2, x, y2, y4), (-s3, x, y1, y4), (-s3, x, y2, y3)]
        (by
          intro e he
          simp only [List.mem_cons, List.not_mem_nil, or_false] at he
          rcases he with rfl | rfl | rfl | rfl | rfl | rfl
          · exact good _ _ _ (n1 _ hs1) (by simp) (by simp) (by omega)
          · exact good _ _ _ (n1 _ hs1) (by simp) (by simp) (by omega)
          · exact good _ _ _ (n1 _ hs2) (by simp) (by simp) (by omega)
          · exact good _ _ _ hs2 (by simp) (by simp) (by omega)
          · exact good _ _ _ (n1 _ hs3) (by simp) (by simp) (by omega)
          · exact good _ _ _ (n1 _ hs3) (by simp) (by simp) (by omega))
        (Classical.byContradiction fun hn => by
          simp only [List.mem_cons, List.not_mem_nil, or_false, exists_eq_or_imp,
            exists_eq_left, not_or] at hn
          obtain ⟨e1, e2, e3, e4, e5, e6⟩ := hn
          rw [eq_neg_of_ne (n1 _ hs1) w12 e1, eq_neg_of_ne (n1 _ hs1) w34 e2,
            eq_neg_of_ne (n1 _ hs2) w13 e3, eq_neg_of_ne hs2 w24 e4,
            eq_neg_of_ne (n1 _ hs3) w14 e5, eq_neg_of_ne (n1 _ hs3) w23 e6] at key
          rcases hs1 with rfl | rfl <;> rcases hs2 with rfl | rfl <;>
            rcases hs3 with rfl | rfl <;> simp at key)
      simpa using this
    · have := clauseSat_template M [(-s1, x, y1, y2), (s1, x, y3, y4), (-s2, x, y1, y3),
          (-s2, x, y2, y4), (-s3, x, y1, y4), (s3, x, y2, y3)]
        (by
          intro e he
          simp only [List.mem_cons, List.not_mem_nil, or_false] at he
          rcases he with rfl | rfl | rfl | rfl | rfl | rfl
          · exact good _ _ _ (n1 _ hs1) (by simp) (by simp) (by omega)
          · exact good _ _ _ hs1 (by simp) (by simp) (by omega)
          · exact good _ _ _ (n1 _ hs2) (by simp) (by simp) (by omega)
          · exact good _ _ _ (n1 _ hs2) (by simp) (by simp) (by omega)
          · exact good _ _ _ (n1 _ hs3) (by simp) (by simp) (by omega)
          · exact good _ _ _ hs3 (by simp) (by simp) (by omega))
        (Classical.byContradiction fun hn => by
          simp only [List.mem_cons, List.not_mem_nil, or_false, exists_eq_or_imp,
            exists_eq_left, not_or] at hn
          obtain ⟨e1, e2, e3, e4, e5, e6⟩ := hn
          rw [eq_neg_of_ne (n1 _ hs1) w12 e1, eq_neg_of_ne hs1 w34 e2,
            eq_neg_of_ne (n1 _ hs2) w13 e3, eq_neg_of_ne (n1 _ hs2) w24 e4,
            eq_neg_of_ne (n1 _ hs3) w14 e5, eq_neg_of_ne hs3 w23 e6] at key
          rcases hs1 with rfl | rfl <;> rcases hs2 with rfl | rfl <;>
            rcases hs3 with rfl | rfl <;> simp at key)
      simpa using this
  · simp at hc

theorem mem_uniq {x : Int} : ∀ {l : List Int}, x ∈ uniq l ↔ x ∈ l
  | [] => Iff.rfl
  | [a] => Iff.rfl
  | a :: b :: l => by
    have ih := @mem_uniq x (b :: l)
    unfold uniq
    split
    · rename_i h; subst h; rw [ih]; simp
    · rw [List.mem_cons, ih]; simp

theorem rot_ne {t a k : Nat} (ha : a < 3 * t) (hk1 : 1 ≤ k) (hk2 : k ≤ 2) :
    rot (3 * t) k a ≠ a := by
  unfold rot; split <;> omega

theorem center_sat (M : TableModel t χ tv n ν) (hC : CenterFacts t χ) {c : List Int}
    (hc : c ∈ centerClauses t (lit tv)) : ClauseSat ν c := by
  unfold centerClauses at hc
  rw [List.mem_map] at hc
  obtain ⟨u, hu, rfl⟩ := hc
  rw [mem_uniq, List.mem_mergeSort, List.mem_flatMap] at hu
  obtain ⟨a, ha, hu⟩ := hu
  rw [List.mem_range] at ha
  have r1 := rot_lt' (k := 1) ha
  have r2 := rot_lt' (k := 2) ha
  have n1 := rot_ne ha (k := 1) (by omega) (by omega)
  have n2 := rot_ne ha (k := 2) (by omega) (by omega)
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hu
  rcases hu with rfl | rfl
  · have := clauseSat_template M [(1, 3 * t, a, rot (3 * t) 1 a)]
      (by
        intro e he
        simp only [List.mem_cons, List.not_mem_nil, or_false] at he
        subst he
        refine ⟨by simp, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp only <;> omega)
      ⟨_, List.mem_cons_self .., by simp [(hC a ha).1]⟩
    simpa using this
  · have := clauseSat_template M [(-1, 3 * t, a, rot (3 * t) 2 a)]
      (by
        intro e he
        simp only [List.mem_cons, List.not_mem_nil, or_false] at he
        subst he
        refine ⟨by simp, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp only <;> omega)
      ⟨_, List.mem_cons_self .., by simp [(hC a ha).2]⟩
    simpa using this

theorem sb_sat (M : TableModel t χ tv n ν) (hSB : SectorOrder t χ) {c : List Int}
    (hc : c ∈ sbClauses t (lit tv)) : ClauseSat ν c := by
  unfold sbClauses at hc
  split at hc
  · simp at hc
  rename_i ht
  rw [List.mem_append, List.mem_flatMap, List.mem_flatMap] at hc
  rcases hc with ⟨o, ho, hc⟩ | ⟨o, ho, hc⟩
  · rw [List.mem_range'] at ho
    obtain ⟨i, hi, rfl⟩ := ho
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hc
    rcases hc with rfl | rfl
    · have := clauseSat_template M [(1, 3 * t, 0, 3 * (1 + i))]
        (by
          intro e he
          simp only [List.mem_cons, List.not_mem_nil, or_false] at he
          subst he
          refine ⟨by simp, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp only <;> omega)
        ⟨_, List.mem_cons_self .., by simp [(hSB.1 (1 + i) (by omega) (by omega)).1]⟩
      simpa using this
    · have := clauseSat_template M [(-1, 3 * t, 1, 3 * (1 + i))]
        (by
          intro e he
          simp only [List.mem_cons, List.not_mem_nil, or_false] at he
          subst he
          refine ⟨by simp, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp only <;> omega)
        ⟨_, List.mem_cons_self .., by simp [(hSB.1 (1 + i) (by omega) (by omega)).2]⟩
      simpa using this
  · rw [List.mem_range'] at ho
    obtain ⟨i, hi, rfl⟩ := ho
    rw [List.mem_map] at hc
    obtain ⟨o2, ho2, rfl⟩ := hc
    rw [List.mem_range'] at ho2
    obtain ⟨j, hj, rfl⟩ := ho2
    have := clauseSat_template M [(1, 3 * t, 3 * (1 + i), 3 * (1 + i + 1 + j))]
      (by
        intro e he
        simp only [List.mem_cons, List.not_mem_nil, or_false] at he
        subst he
        refine ⟨by simp, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> simp only <;> omega)
      ⟨_, List.mem_cons_self .., by simp [hSB.2 (1 + i) (1 + i + 1 + j) (by omega) (by omega) (by omega)]⟩
    simpa using this

end

end D3
