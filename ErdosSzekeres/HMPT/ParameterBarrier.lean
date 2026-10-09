import ErdosSzekeres.HMPT.Asymptotic

/-! Exact scope of retuning the existing HMPT two-scale entropy argument.
This is an optimization identity for this proof's limiting budget, not a lower
bound for the Erdős–Szekeres number or an obstruction to other arguments. -/

namespace ErdosSzekeres.HMPT
open Filter
open scoped Topology

/-- The limiting slack splits into improvement above the published coefficient
and a nonpositive square measuring the choice of scale. -/
theorem leading_slack_identity (c C : ℝ) :
    3 * c * C - 16 * c ^ 2 - 2 =
      3 * c * (C - publishedCoefficient) - (4 * c - Real.sqrt 2) ^ 2 := by
  unfold publishedCoefficient
  nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]

/-- Retuning the scale alone gives positive limiting slack exactly for
coefficients strictly larger than the published one. -/
theorem positive_leading_slack_iff (C : ℝ) :
    (∃ c : ℝ, 0 < c ∧ 0 < 3 * c * C - 16 * c ^ 2 - 2) ↔
      publishedCoefficient < C := by
  constructor
  · rintro ⟨c, hc, hslack⟩
    rw [leading_slack_identity] at hslack
    have hp : 0 < 3 * c * (C - publishedCoefficient) := by
      nlinarith [sq_nonneg (4 * c - Real.sqrt 2)]
    have : 0 < C - publishedCoefficient :=
      (mul_pos_iff_of_pos_left (by positivity : 0 < 3 * c)).mp hp
    linarith
  · intro hC
    refine ⟨Real.sqrt 2 / 4, by positivity, ?_⟩
    rw [leading_slack_identity]
    have he : 4 * (Real.sqrt 2 / 4) - Real.sqrt 2 = 0 := by ring
    rw [he]
    simpa using mul_pos (by positivity : 0 < 3 * (Real.sqrt 2 / 4))
      (sub_pos.mpr hC)

/-- The published coefficient has one zero-slack scale; all others lose slack. -/
theorem published_slack_nonnegative_iff (c : ℝ) :
    0 ≤ 3 * c * publishedCoefficient - 16 * c ^ 2 - 2 ↔
      c = Real.sqrt 2 / 4 := by
  rw [leading_slack_identity]
  constructor
  · intro h
    nlinarith [sq_nonneg (4 * c - Real.sqrt 2)]
  · intro h
    rw [h]
    ring_nf
    simp

/-- A smaller coefficient makes this exact normalized budget eventually
negative at every fixed positive scale. Other proofs remain possible. -/
theorem budget_eventually_negative_below_published {c C : ℝ}
    (hc : 0 < c) (hC : C < publishedCoefficient) :
    ∀ᶠ n : ℕ in atTop, normalizedBudget c C n < 0 := by
  have hlim : 3 * c * C - 16 * c ^ 2 - 2 < 0 := by
    rw [leading_slack_identity]
    have hp : 3 * c * (C - publishedCoefficient) < 0 :=
      mul_neg_of_pos_of_neg (by positivity) (sub_neg.mpr hC)
    nlinarith [sq_nonneg (4 * c - Real.sqrt 2)]
  exact (normalizedBudget_tendsto hc C).eventually (eventually_lt_nhds hlim)

end ErdosSzekeres.HMPT
