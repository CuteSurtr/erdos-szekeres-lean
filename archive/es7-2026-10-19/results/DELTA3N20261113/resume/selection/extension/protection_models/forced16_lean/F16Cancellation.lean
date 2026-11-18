import F16Products

namespace Delta3.Forced16Algebra

open Lean.Grind Std

variable {K : Type u} [CommRing K]

def monomial {κ : Type v} (vars : List κ) (x : κ → K) (e : κ → Nat) : K :=
  product vars (fun j => x j ^ e j)

theorem monomial_congr {κ : Type v} (vars : List κ) (x : κ → K) (e f : κ → Nat)
    (h : ∀ j ∈ vars, e j = f j) : monomial vars x e = monomial vars x f :=
  product_congr vars _ _ (fun j hj => congrArg (fun n => x j ^ n) (h j hj))

theorem monomial_zero {κ : Type v} (vars : List κ) (x : κ → K) :
    monomial vars x (fun _ => 0) = 1 := by
  exact (product_congr vars _ _ (fun j _ => Semiring.pow_zero (x j))).trans (product_one vars)

theorem monomial_add {κ : Type v} (vars : List κ) (x : κ → K) (e f : κ → Nat) :
    monomial vars x (fun j => e j + f j) = monomial vars x e * monomial vars x f :=
  (product_congr vars _ _ (fun j _ => Semiring.pow_add (x j) (e j) (f j))).trans
    (product_mul vars _ _)

theorem monomial_scale {κ : Type v} (vars : List κ) (x : κ → K) (e : κ → Nat)
    (n : Nat) : monomial vars x (fun j => e j * n) = monomial vars x e ^ n := by
  induction n with
  | zero => simp only [Nat.mul_zero, monomial_zero, Semiring.pow_zero]
  | succ n ih => simp only [Nat.mul_succ, monomial_add, ih, Semiring.pow_succ]

/-- Multiplication of weighted monomials adds their exponents, including multiplicities. -/
theorem weighted_monomials {ι : Type v} {κ : Type w} (rows : List ι) (vars : List κ)
    (x : κ → K) (e : ι → κ → Nat) (weight : ι → Nat) :
    product rows (fun i => monomial vars x (e i) ^ weight i) =
      monomial vars x (fun j => natTotal rows (fun i => e i j * weight i)) := by
  induction rows with
  | nil => simp only [product, natTotal, monomial_zero]
  | cons i rows ih => simp only [product, natTotal, monomial_add, monomial_scale, ih]

variable [LE K] [LT K] [LawfulOrderLT K] [IsLinearOrder K] [OrderedRing K]

omit [LawfulOrderLT K] in
theorem monomial_pos {κ : Type v} (vars : List κ) (x : κ → K) (e : κ → Nat)
    (hx : ∀ j ∈ vars, 0 < x j) : 0 < monomial vars x e :=
  product_pos vars _ (fun j hj => power_pos (x j) (hx j hj) (e j))

/-- A nonempty positive-weight family of strict monomial inequalities cannot
have equal weighted exponent totals for every variable. -/
theorem cancelling_certificate_contradiction {ι : Type v} {κ : Type w}
    (rows : List ι) (hne : rows ≠ []) (vars : List κ) (x : κ → K)
    (small large : ι → κ → Nat) (weight : ι → Nat)
    (hx : ∀ j ∈ vars, 0 < x j) (hw : ∀ i ∈ rows, 0 < weight i)
    (hlt : ∀ i ∈ rows, monomial vars x (small i) < monomial vars x (large i))
    (hcancel : ∀ j ∈ vars,
      natTotal rows (fun i => small i j * weight i) =
        natTotal rows (fun i => large i j * weight i)) : False := by
  apply weighted_product_contradiction rows hne
    (fun i => monomial vars x (small i)) (fun i => monomial vars x (large i)) weight
    (fun i _ => monomial_pos vars x (small i) hx) hlt hw
  rw [weighted_monomials, weighted_monomials]
  exact monomial_congr vars x _ _ hcancel

#print axioms monomial_congr
#print axioms monomial_zero
#print axioms monomial_add
#print axioms monomial_scale
#print axioms weighted_monomials
#print axioms monomial_pos
#print axioms cancelling_certificate_contradiction

end Delta3.Forced16Algebra
