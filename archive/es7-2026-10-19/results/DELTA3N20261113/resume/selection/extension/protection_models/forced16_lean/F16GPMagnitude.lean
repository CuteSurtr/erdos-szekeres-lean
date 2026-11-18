import F16GP

namespace Delta3.Forced16Algebra

open Lean.Grind Std

variable {K : Type u} [CommRing K] [LE K] [LT K] [LawfulOrderLT K]
  [IsLinearOrder K] [OrderedRing K]

theorem magnitude_neg (a : K) : magnitude (-a) = magnitude a := by
  rcases LinearOrder.trichotomy 0 a with hp | he | hn
  · have hneg : -a < 0 := by
      apply OrderedAdd.neg_lt_iff.mpr
      simpa only [AddCommGroup.neg_zero] using hp
    rw [magnitude_of_neg hneg, magnitude_of_pos hp, AddCommGroup.neg_neg]
  · subst a
    rw [AddCommGroup.neg_zero]
  · rw [magnitude_of_pos (OrderedAdd.neg_pos_iff.mpr hn), magnitude_of_neg hn]

theorem magnitude_mul (a b : K) : magnitude (a * b) = magnitude a * magnitude b := by
  rcases LinearOrder.trichotomy 0 a with hp | he | hn
  · rcases LinearOrder.trichotomy 0 b with hq | he | hr
    · rw [magnitude_of_pos (OrderedRing.mul_pos hp hq), magnitude_of_pos hp,
        magnitude_of_pos hq]
    · subst b
      simp only [Semiring.mul_zero, magnitude_zero]
    · rw [magnitude_of_neg (OrderedRing.mul_neg_of_pos_of_neg hp hr),
        magnitude_of_pos hp, magnitude_of_neg hr, Ring.mul_neg]
  · subst a
    simp only [Semiring.zero_mul, magnitude_zero]
  · rcases LinearOrder.trichotomy 0 b with hq | he | hr
    · rw [magnitude_of_neg (OrderedRing.mul_neg_of_neg_of_pos hn hq),
        magnitude_of_neg hn, magnitude_of_pos hq, Ring.neg_mul]
    · subst b
      simp only [Semiring.mul_zero, magnitude_zero]
    · rw [magnitude_of_pos (OrderedRing.mul_pos_of_neg_of_neg hn hr),
        magnitude_of_neg hn, magnitude_of_neg hr, Ring.neg_mul, Ring.mul_neg,
        AddCommGroup.neg_neg]

/-- A GP row with its first term uniquely signed yields an inequality between
products of positive bracket magnitudes. Other selected terms can be permuted. -/
theorem gp_product_inequality (a b c d e f : K)
    (hgp : a * b - c * d + e * f = 0)
    (hsign : (0 < a * b ∧ -(c * d) < 0 ∧ e * f < 0) ∨
      (a * b < 0 ∧ 0 < -(c * d) ∧ 0 < e * f)) :
    0 < magnitude c * magnitude d ∧
      magnitude c * magnitude d < magnitude a * magnitude b := by
  have hsum : a * b + -(c * d) + e * f = 0 := by
    simpa only [Ring.sub_eq_add_neg] using hgp
  have h := unique_sign_magnitude (a * b) (-(c * d)) (e * f) hsum hsign
  simpa only [magnitude_neg, magnitude_mul] using And.intro h.2.1 h.2.2.2

#print axioms magnitude_neg
#print axioms magnitude_mul
#print axioms gp_product_inequality

end Delta3.Forced16Algebra
