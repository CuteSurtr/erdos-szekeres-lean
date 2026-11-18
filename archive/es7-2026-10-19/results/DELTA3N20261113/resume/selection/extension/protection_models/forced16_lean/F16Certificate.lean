import F16Cancellation
import F16GPMagnitude

namespace Delta3.Forced16Algebra

open Lean.Grind Std

variable {K : Type u} [CommRing K] [LE K] [LT K] [LawfulOrderLT K]
  [IsLinearOrder K] [OrderedRing K]

/-- Direct geometric-algebra specialization: a uniquely signed first GP term
dominates the second product in magnitude. No finite sign model is assumed here. -/
theorem coordinate_gp_inequality (a b c d e : K × K)
    (hsign :
      (0 < orient a b c * orient a d e ∧ -(orient a b d * orient a c e) < 0 ∧
        orient a b e * orient a c d < 0) ∨
      (orient a b c * orient a d e < 0 ∧ 0 < -(orient a b d * orient a c e) ∧
        0 < orient a b e * orient a c d)) :
    0 < magnitude (orient a b d) * magnitude (orient a c e) ∧
      magnitude (orient a b d) * magnitude (orient a c e) <
        magnitude (orient a b c) * magnitude (orient a d e) :=
  gp_product_inequality _ _ _ _ _ _ (orient_gp a b c d e) hsign

/-- Conditional finite GP certificate theorem. Row-term identities, unique signs,
and the bindings to monomial factors are explicit hypotheses; no fixed certificate
is silently imported by this theorem. -/
theorem gp_certificate_contradiction {ι : Type v} {κ : Type w}
    (rows : List ι) (hne : rows ≠ []) (vars : List κ) (x : κ → K)
    (small large : ι → κ → Nat) (weight : ι → Nat)
    (bigTerm smallTerm otherTerm : ι → K)
    (hx : ∀ j ∈ vars, 0 < x j) (hw : ∀ i ∈ rows, 0 < weight i)
    (hsum : ∀ i ∈ rows, bigTerm i + smallTerm i + otherTerm i = 0)
    (hsign : ∀ i ∈ rows,
      (0 < bigTerm i ∧ smallTerm i < 0 ∧ otherTerm i < 0) ∨
      (bigTerm i < 0 ∧ 0 < smallTerm i ∧ 0 < otherTerm i))
    (hsmall : ∀ i ∈ rows, monomial vars x (small i) = magnitude (smallTerm i))
    (hlarge : ∀ i ∈ rows, monomial vars x (large i) = magnitude (bigTerm i))
    (hcancel : ∀ j ∈ vars,
      natTotal rows (fun i => small i j * weight i) =
        natTotal rows (fun i => large i j * weight i)) : False := by
  apply cancelling_certificate_contradiction rows hne vars x small large weight hx hw
    (fun i hi => ?_) hcancel
  rw [hsmall i hi, hlarge i hi]
  exact (unique_sign_magnitude (bigTerm i) (smallTerm i) (otherTerm i)
    (hsum i hi) (hsign i hi)).2.2.2

#print axioms coordinate_gp_inequality
#print axioms gp_certificate_contradiction

end Delta3.Forced16Algebra
