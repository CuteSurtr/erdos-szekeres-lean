/-! Finite products and natural powers over Lean's standard core ordered-ring API. -/

namespace Delta3.Forced16Algebra

open Lean.Grind Std

variable {K : Type u} [CommRing K]

def product {ι : Type v} (s : List ι) (f : ι → K) : K :=
  match s with
  | [] => 1
  | i :: rest => f i * product rest f

def natTotal {ι : Type v} (s : List ι) (f : ι → Nat) : Nat :=
  match s with
  | [] => 0
  | i :: rest => f i + natTotal rest f

theorem product_congr {ι : Type v} (s : List ι) (f g : ι → K)
    (h : ∀ i ∈ s, f i = g i) : product s f = product s g := by
  induction s with
  | nil => rfl
  | cons i s ih =>
    simp only [product, h i (.head s), ih (fun j hj => h j (.tail i hj))]

theorem product_one {ι : Type v} (s : List ι) : product s (fun _ => (1 : K)) = 1 := by
  induction s with
  | nil => rfl
  | cons i s ih => simp only [product, ih, Semiring.one_mul]

theorem product_mul {ι : Type v} (s : List ι) (f g : ι → K) :
    product s (fun i => f i * g i) = product s f * product s g := by
  induction s with
  | nil => exact (Semiring.one_mul 1).symm
  | cons i s ih =>
    simp only [product, ih]
    grind only

variable [LE K] [LT K] [LawfulOrderLT K] [IsLinearOrder K] [OrderedRing K]

omit [LawfulOrderLT K] in
theorem power_pos (a : K) (ha : 0 < a) (n : Nat) : 0 < a ^ n := by
  induction n with
  | zero => simpa only [Semiring.pow_zero] using (OrderedRing.zero_lt_one (R := K))
  | succ n ih =>
    simpa only [Semiring.pow_succ] using OrderedRing.mul_pos ih ha

theorem power_le (a b : K) (ha : 0 < a) (hab : a ≤ b) (n : Nat) : a ^ n ≤ b ^ n := by
  induction n with
  | zero => simp only [Semiring.pow_zero]; exact le_refl 1
  | succ n ih =>
    rw [Semiring.pow_succ, Semiring.pow_succ]
    have h1 := OrderedRing.mul_le_mul_of_nonneg_right ih (Preorder.le_of_lt ha)
    have hb := Preorder.lt_of_lt_of_le ha hab
    have h2 := OrderedRing.mul_le_mul_of_nonneg_left hab
      (Preorder.le_of_lt (power_pos b hb n))
    exact le_trans h1 h2

theorem power_lt (a b : K) (ha : 0 < a) (hab : a < b) (n : Nat) (hn : 0 < n) :
    a ^ n < b ^ n := by
  cases n with
  | zero => exact False.elim (Nat.not_lt_zero _ hn)
  | succ n =>
    rw [Semiring.pow_succ, Semiring.pow_succ]
    have h1 := OrderedRing.mul_le_mul_of_nonneg_right
      (power_le a b ha (Preorder.le_of_lt hab) n) (Preorder.le_of_lt ha)
    have h2 := OrderedRing.mul_lt_mul_of_pos_left hab
      (power_pos b (Preorder.lt_trans ha hab) n)
    exact Preorder.lt_of_le_of_lt h1 h2

omit [LawfulOrderLT K] in
theorem product_pos {ι : Type v} (s : List ι) (f : ι → K)
    (h : ∀ i ∈ s, 0 < f i) : 0 < product s f := by
  induction s with
  | nil => exact OrderedRing.zero_lt_one
  | cons i s ih =>
    exact OrderedRing.mul_pos (h i (.head s)) (ih (fun j hj => h j (.tail i hj)))

theorem product_le {ι : Type v} (s : List ι) (f g : ι → K)
    (hp : ∀ i ∈ s, 0 < f i) (h : ∀ i ∈ s, f i ≤ g i) :
    product s f ≤ product s g := by
  induction s with
  | nil => exact le_refl 1
  | cons i s ih =>
    have ht := ih (fun j hj => hp j (.tail i hj)) (fun j hj => h j (.tail i hj))
    have h1 := OrderedRing.mul_le_mul_of_nonneg_right (h i (.head s))
      (Preorder.le_of_lt (product_pos s f (fun j hj => hp j (.tail i hj))))
    have h2 := OrderedRing.mul_le_mul_of_nonneg_left ht
      (Preorder.le_of_lt (Preorder.lt_of_lt_of_le (hp i (.head s)) (h i (.head s))))
    exact le_trans h1 h2

theorem product_lt {ι : Type v} (s : List ι) (hne : s ≠ []) (f g : ι → K)
    (hp : ∀ i ∈ s, 0 < f i) (h : ∀ i ∈ s, f i < g i) :
    product s f < product s g := by
  cases s with
  | nil => exact False.elim (hne rfl)
  | cons i s =>
    have h1 := OrderedRing.mul_lt_mul_of_pos_right (h i (.head s))
      (product_pos s f (fun j hj => hp j (.tail i hj)))
    have h2 := OrderedRing.mul_le_mul_of_nonneg_left
      (product_le s f g (fun j hj => hp j (.tail i hj))
        (fun j hj => Preorder.le_of_lt (h j (.tail i hj))))
      (Preorder.le_of_lt (Preorder.lt_trans (hp i (.head s)) (h i (.head s))))
    exact Preorder.lt_of_lt_of_le h1 h2

/-- Positive strict inequalities cannot have equal weighted products. -/
theorem weighted_product_contradiction {ι : Type v} (s : List ι) (hne : s ≠ [])
    (f g : ι → K) (w : ι → Nat) (hp : ∀ i ∈ s, 0 < f i)
    (hlt : ∀ i ∈ s, f i < g i) (hw : ∀ i ∈ s, 0 < w i)
    (heq : product s (fun i => f i ^ w i) = product s (fun i => g i ^ w i)) : False := by
  have h := product_lt s hne (fun i => f i ^ w i) (fun i => g i ^ w i)
    (fun i hi => power_pos (f i) (hp i hi) (w i))
    (fun i hi => power_lt (f i) (g i) (hp i hi) (hlt i hi) (w i) (hw i hi))
  rw [heq] at h
  exact Preorder.lt_irrefl _ h

#print axioms product_congr
#print axioms product_one
#print axioms product_mul
#print axioms power_pos
#print axioms power_le
#print axioms power_lt
#print axioms product_pos
#print axioms product_le
#print axioms product_lt
#print axioms weighted_product_contradiction

end Delta3.Forced16Algebra
