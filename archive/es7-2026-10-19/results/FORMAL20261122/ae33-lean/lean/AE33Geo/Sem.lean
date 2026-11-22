import AE33Enc.Bridge
import AE33Geo.Slot

/-!
# AE33Geo.Sem: the real assignment and the semantics of `chi` and `osgn` (DESIGN.md §2)

Points `pt 0..30` realize the base, `pt 31 = p`, `pt 32 = q`. `realAssign pt` is the intended assignment of the
961 variables (X, Y, W). `chi_spec`: a literal of `chi` is true exactly when its triple is positively oriented
(general position). `osgn_spec`: the sign of three base points transfers through the realization.
-/

namespace AE33Geo
open ErdosSzekeres AE33

/-- The 465 pairs a < b < 31 in lexicographic order (the order of the X and Y variables). -/
def pairList : List (ℕ × ℕ) :=
  (List.range 31).flatMap fun a => ((List.range 31).filter fun b => decide (a < b)).map fun b => (a, b)

def pairOf (k : ℕ) : ℕ × ℕ := pairList.getD k (0, 0)

/-- Kernel check on the 465 pairs: `pairOf` decodes `pvar 31` (DESIGN.md D7). -/
theorem pvar_spec_all : ∀ b, b < 31 → ∀ a, a < b →
    pairOf (pvar 31 a b - 1) = (a, b) ∧ 1 ≤ pvar 31 a b ∧ pvar 31 a b ≤ 465 := by
  decide +kernel

/-- The real assignment of the 961 variables. -/
noncomputable def realAssign (pt : ℕ → Point) (v : ℕ) : Bool :=
  if 1 ≤ v ∧ v ≤ 465 then decide (0 < orient (pt (pairOf (v - 1)).1) (pt (pairOf (v - 1)).2) (pt 31))
  else if 466 ≤ v ∧ v ≤ 930 then
    decide (0 < orient (pt (pairOf (v - 466)).1) (pt (pairOf (v - 466)).2) (pt 32))
  else if 931 ≤ v ∧ v ≤ 961 then decide (0 < orient (pt (v - 931)) (pt 31) (pt 32))
  else false

theorem litSat_neg {ν : ℕ → Bool} {l : ℤ} (hl : l ≠ 0) : EncB.LitSat ν (-l) ↔ ¬ EncB.LitSat ν l := by
  unfold EncB.LitSat
  rw [Int.natAbs_neg]
  rcases lt_or_gt_of_ne hl with h | h
  · have h1 : 0 < -l := by omega
    have h2 : ¬ (-l < 0) := by omega
    have h3 : ¬ (0 < l) := by omega
    simp only [h1, h2, h3, h, true_and, false_and, or_false, false_or]
    cases ν l.natAbs <;> simp
  · have h1 : ¬ (0 < -l) := by omega
    have h2 : -l < 0 := by omega
    have h3 : ¬ (l < 0) := by omega
    simp only [h1, h2, h3, h, true_and, false_and, or_false, false_or]
    cases ν l.natAbs <;> simp

theorem litSat_natCast {ν : ℕ → Bool} {v : ℕ} (hv : 0 < v) : EncB.LitSat ν (v : ℤ) ↔ ν v = true := by
  unfold EncB.LitSat
  simp only [Int.natAbs_natCast]
  constructor
  · rintro (⟨_, h⟩ | ⟨h, _⟩)
    · exact h
    · omega
  · intro h; exact Or.inl ⟨by omega, h⟩

/-- `sort3` sorts a triple of distinct numbers and returns its permutation sign. -/
theorem sort3_spec (i j k : ℕ) (hij : i ≠ j) (hjk : j ≠ k) (hik : i ≠ k) :
    (sort3 i j k).1 < (sort3 i j k).2.1 ∧ (sort3 i j k).2.1 < (sort3 i j k).2.2.1 ∧
    (i = (sort3 i j k).1 ∨ i = (sort3 i j k).2.1 ∨ i = (sort3 i j k).2.2.1) ∧
    (j = (sort3 i j k).1 ∨ j = (sort3 i j k).2.1 ∨ j = (sort3 i j k).2.2.1) ∧
    (k = (sort3 i j k).1 ∨ k = (sort3 i j k).2.1 ∨ k = (sort3 i j k).2.2.1) ∧
    ((sort3 i j k).2.2.2 = 1 ∨ (sort3 i j k).2.2.2 = -1) ∧
    ∀ f : ℕ → Point, orient (f i) (f j) (f k) =
      ((sort3 i j k).2.2.2 : ℝ) * orient (f (sort3 i j k).1) (f (sort3 i j k).2.1) (f (sort3 i j k).2.2.1) := by
  have key : ∃ a0 a1 a2 : ℕ, ∃ s : ℤ, sort3 i j k = (a0, a1, a2, s) ∧ a0 < a1 ∧ a1 < a2 ∧
      (i = a0 ∨ i = a1 ∨ i = a2) ∧ (j = a0 ∨ j = a1 ∨ j = a2) ∧ (k = a0 ∨ k = a1 ∨ k = a2) ∧
      (s = 1 ∨ s = -1) ∧
      ∀ f : ℕ → Point, orient (f i) (f j) (f k) = (s : ℝ) * orient (f a0) (f a1) (f a2) := by
    rcases Nat.lt_or_gt_of_ne hij with h1 | h1 <;> rcases Nat.lt_or_gt_of_ne hjk with h2 | h2 <;>
      rcases Nat.lt_or_gt_of_ne hik with h3 | h3
    · exact ⟨i, j, k, 1, by simp [sort3, h1, h2, h3, Nat.lt_asymm h1, Nat.lt_asymm h2, Nat.lt_asymm h3],
        h1, h2, by omega, by omega, by omega, by norm_num, fun f => by push_cast; ring⟩
    · exfalso; omega
    · exact ⟨i, k, j, -1, by simp [sort3, h1, h2, h3, Nat.lt_asymm h1, Nat.lt_asymm h2, Nat.lt_asymm h3],
        h3, h2, by omega, by omega, by omega, by norm_num, fun f => by push_cast; simp only [orient]; ring⟩
    · exact ⟨k, i, j, 1, by simp [sort3, h1, h2, h3, Nat.lt_asymm h1, Nat.lt_asymm h2, Nat.lt_asymm h3],
        h3, h1, by omega, by omega, by omega, by norm_num, fun f => by push_cast; simp only [orient]; ring⟩
    · exact ⟨j, i, k, -1, by simp [sort3, h1, h2, h3, Nat.lt_asymm h1, Nat.lt_asymm h2, Nat.lt_asymm h3],
        h1, h3, by omega, by omega, by omega, by norm_num, fun f => by push_cast; simp only [orient]; ring⟩
    · exact ⟨j, k, i, 1, by simp [sort3, h1, h2, h3, Nat.lt_asymm h1, Nat.lt_asymm h2, Nat.lt_asymm h3],
        h2, h3, by omega, by omega, by omega, by norm_num, fun f => by push_cast; simp only [orient]; ring⟩
    · exfalso; omega
    · exact ⟨k, j, i, -1, by simp [sort3, h1, h2, h3, Nat.lt_asymm h1, Nat.lt_asymm h2, Nat.lt_asymm h3],
        h2, h1, by omega, by omega, by omega, by norm_num, fun f => by push_cast; simp only [orient]; ring⟩
  obtain ⟨a0, a1, a2, s, e, h01, h12, hi, hj, hk, hs, ho⟩ := key
  rw [e]
  exact ⟨h01, h12, hi, hj, hk, hs, ho⟩

/-- **Semantics of a literal of `chi`.** -/
theorem chi_spec {B : Array Pt} (hB : B.size = 31) (pt : ℕ → Point) {i j k : ℕ}
    (hi : i < 33) (hj : j < 33) (hk : k < 33) (hij : i ≠ j) (hjk : j ≠ k) (hik : i ≠ k)
    (hnew : 31 ≤ i ∨ 31 ≤ j ∨ 31 ≤ k) (hgp : orient (pt i) (pt j) (pt k) ≠ 0) :
    ∃ l, chi B i j k = .lit l ∧ l ≠ 0 ∧
      (EncB.LitSat (realAssign pt) l ↔ 0 < orient (pt i) (pt j) (pt k)) := by
  obtain ⟨h01, h12, hmi, hmj, hmk, hs, hor⟩ := sort3_spec i j k hij hjk hik
  set a0 := (sort3 i j k).1 with ha0
  set a1 := (sort3 i j k).2.1 with ha1
  set a2 := (sort3 i j k).2.2.1 with ha2
  set s := (sort3 i j k).2.2.2 with hsdef
  have ho := hor pt
  have h2 : 31 ≤ a2 := by omega
  have h2' : a2 < 33 := by omega
  -- the variable and its value under `realAssign`
  obtain ⟨v, hv, hvpos, hval⟩ : ∃ v : ℕ, chi B i j k = .lit (s * (v : ℤ)) ∧ 0 < v ∧
      (realAssign pt v = decide (0 < orient (pt a0) (pt a1) (pt a2))) := by
    simp only [chi, hB]
    rw [← ha0, ← ha1, ← ha2, ← hsdef, if_neg (by omega)]
    by_cases ha1' : a1 < 31
    · rw [if_pos ha1']
      obtain ⟨hpo, hp1, hp2⟩ := pvar_spec_all a1 ha1' a0 h01
      by_cases hq : a2 = 31
      · refine ⟨pvar 31 a0 a1, by rw [if_pos hq]; simp, by omega, ?_⟩
        simp only [realAssign, if_pos (And.intro hp1 hp2), hpo, hq]
      · have hq' : a2 = 32 := by omega
        refine ⟨pvar 31 a0 a1 + 465, by rw [if_neg hq]; simp [n2], by omega, ?_⟩
        have hx : ¬ (1 ≤ pvar 31 a0 a1 + 465 ∧ pvar 31 a0 a1 + 465 ≤ 465) := by omega
        have hy : 466 ≤ pvar 31 a0 a1 + 465 ∧ pvar 31 a0 a1 + 465 ≤ 930 := by omega
        have hz : pvar 31 a0 a1 + 465 - 466 = pvar 31 a0 a1 - 1 := by omega
        simp only [realAssign, if_neg hx, if_pos hy, hz, hpo, hq']
    · rw [if_neg ha1']
      have e1 : a1 = 31 := by omega
      have e2 : a2 = 32 := by omega
      refine ⟨931 + a0, by simp [n2], by omega, ?_⟩
      have hx : ¬ (1 ≤ 931 + a0 ∧ 931 + a0 ≤ 465) := by omega
      have hy : ¬ (466 ≤ 931 + a0 ∧ 931 + a0 ≤ 930) := by omega
      have hz : 931 ≤ 931 + a0 ∧ 931 + a0 ≤ 961 := by omega
      simp only [realAssign, if_neg hx, if_neg hy, if_pos hz, e1, e2, Nat.add_sub_cancel_left]
  refine ⟨s * (v : ℤ), hv, ?_, ?_⟩
  · rcases hs with h | h <;> rw [h] <;> omega
  · have hne : orient (pt a0) (pt a1) (pt a2) ≠ 0 := by
      intro h0; apply hgp; rw [ho, h0, mul_zero]
    rcases hs with h | h
    · rw [h, one_mul, litSat_natCast hvpos, hval, ho, h]
      simp
    · rw [h, neg_one_mul, litSat_neg (by omega), litSat_natCast hvpos, hval, ho, h]
      simp only [decide_eq_true_eq, Int.reduceNeg, Int.cast_neg, Int.cast_one, neg_one_mul, neg_pos]
      constructor
      · intro h1; exact lt_of_le_of_ne (not_lt.1 h1) hne
      · intro h1; exact not_lt.2 h1.le

theorem isgn_eq_one {x : ℤ} : isgn x = 1 ↔ 0 < x := by
  unfold isgn
  by_cases h1 : 0 < x
  · simp [h1]
  · by_cases h2 : x < 0
    · simp [h1, h2]
    · simp [h1, h2]

theorem isgn_eq_neg_one {x : ℤ} : isgn x = -1 ↔ x < 0 := by
  unfold isgn
  by_cases h1 : 0 < x
  · simp [h1]; omega
  · by_cases h2 : x < 0
    · simp [h1, h2]
    · simp [h1, h2]

theorem iorient_swap23 (a b c : Pt) : iorient a c b = -iorient a b c := by
  simp only [iorient]; ring

/-- The realization hypothesis. -/
def Realizes31 (B : Array Pt) (pt : ℕ → Point) : Prop :=
  ∀ i j k, i < 31 → j < 31 → k < 31 →
    (0 < orient (pt i) (pt j) (pt k) ↔ 0 < iorient (B.getD i (0, 0)) (B.getD j (0, 0)) (B.getD k (0, 0)))

/-- **Base orientation signs transfer through the realization.** -/
theorem osgn_spec {B : Array Pt} {pt : ℕ → Point} (hreal : Realizes31 B pt) {i j k : ℕ}
    (hi : i < 31) (hj : j < 31) (hk : k < 31) :
    (osgn B i j k = 1 ↔ 0 < orient (pt i) (pt j) (pt k)) ∧
      (osgn B i j k = -1 ↔ 0 < orient (pt i) (pt k) (pt j)) := by
  unfold osgn
  refine ⟨by rw [isgn_eq_one, hreal i j k hi hj hk], ?_⟩
  rw [isgn_eq_neg_one, hreal i k j hi hk hj, iorient_swap23]
  omega

end AE33Geo
