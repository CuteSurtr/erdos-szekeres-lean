import ErdosSzekeres.HMPT.ParameterBarrier

/-!
An endpoint obstruction for the specific entropy budget in `HMPT/Asymptotic`.
The retained finite losses make its slack eventually negative even at exactly
the published coefficient. This does not assert an extremal lower bound, a
barrier for other arguments, or a barrier for the new factorial criterion.
-/

namespace ErdosSzekeres.HMPT
open Filter
open scoped Topology

/-- The exact unnormalized entropy slack is negative at the published
coefficient once the logarithmic term is at least half of log₂ n. -/
theorem entropy_slack_negative_at_endpoint {m d n S L H : ℝ}
    (hm : 3 ≤ m) (hn : 0 ≤ n) (hS : 0 ≤ S) (hL : 0 ≤ L)
    (hH : L / 2 ≤ H) (hd : 4 * m ≤ d) (hsq : S ^ 2 = n * L) :
    (3 * m - 6) * (n + publishedCoefficient * S - 1) -
      ((d + 1) * (4 * m + 1) + 3 * m * n + 6 * m +
        (4 * n + 3 * m) * (H + 4)) < 0 := by
  have hroot : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hlead : 3 * m * publishedCoefficient * S - 16 * m ^ 2 - 2 * n * L ≤ 0 := by
    unfold publishedCoefficient
    have hsquare := sq_nonneg (4 * m - Real.sqrt 2 * S)
    have he : (Real.sqrt 2 * S) ^ 2 = 2 * (n * L) := by
      rw [mul_pow, hroot, hsq]
    nlinarith
  have hprod : 16 * m ^ 2 ≤ (d + 1) * (4 * m + 1) := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hd) (show 0 ≤ 4 * m + 1 by linarith)]
  have hlog : 2 * n * L ≤ 4 * n * H := by
    nlinarith [mul_nonneg hn (show 0 ≤ H - L / 2 by linarith)]
  have hH0 : 0 ≤ H := by linarith
  have hCS : 0 ≤ publishedCoefficient * S := by
    unfold publishedCoefficient
    positivity
  nlinarith [mul_nonneg (show 0 ≤ m by linarith) hH0]

/-- A simple explicit condition ensuring that the rounded scale has square
at least n. No asymptotic approximation to the ceiling is used. -/
theorem roundedScale_sq_ge_of_log_budget {c : ℝ} {n : ℕ}
    (hc : 0 < c) (hn : 1 ≤ n) (hlog : 1 ≤ c ^ 2 * Real.logb 2 n) :
    (n : ℝ) ≤ (roundedScale c n : ℝ) ^ 2 := by
  have hceil : c * asymptoticScale n ≤ (roundedScale c n : ℝ) := Nat.le_ceil _
  have hS : 0 ≤ asymptoticScale n := Real.sqrt_nonneg _
  have hsq := asymptoticScale_sq hn
  have hscaled : (n : ℝ) ≤ (c * asymptoticScale n) ^ 2 := by
    have he : (c * asymptoticScale n) ^ 2 = c ^ 2 * ((n : ℝ) * Real.logb 2 n) := by
      rw [mul_pow, hsq]
    rw [he]
    nlinarith [mul_nonneg (Nat.cast_nonneg n) (sub_nonneg.mpr hlog)]
  exact hscaled.trans ((sq_le_sq₀ (mul_nonneg hc.le hS) (Nat.cast_nonneg _)).mpr hceil)

/-- The exact entropy interface fails at the endpoint under an explicit
logarithmic size condition, for every fixed positive scale. -/
theorem normalizedBudget_neg_at_endpoint {c : ℝ} {n : ℕ}
    (hc : 0 < c) (hn : 9 ≤ n) (hlog : 1 ≤ c ^ 2 * Real.logb 2 n) :
    normalizedBudget c publishedCoefficient n < 0 := by
  have hnp : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
  have hL : 0 < Real.logb 2 n := Real.logb_pos (by norm_num)
    (by exact_mod_cast (show 1 < n by omega))
  have hS := asymptoticScale_pos (show 2 ≤ n by omega)
  have hsq := roundedScale_sq_ge_of_log_budget hc (by omega) hlog
  have hm : 3 ≤ roundedScale c n := by
    have hn' : (9 : ℝ) ≤ n := by exact_mod_cast hn
    by_contra! hm
    have hm' : (roundedScale c n : ℝ) ≤ 2 := by exact_mod_cast (show roundedScale c n ≤ 2 by omega)
    nlinarith [show (0 : ℝ) ≤ roundedScale c n from Nat.cast_nonneg _]
  have hH : Real.logb 2 n / 2 ≤ Real.logb 2 (roundedScale c n) := by
    have h := Real.logb_le_logb_of_le (by norm_num : (1 : ℝ) < 2) hnp hsq
    rw [Real.logb_pow] at h
    norm_num at h
    linarith
  have hd : 4 * (roundedScale c n : ℝ) ≤ scaleInputExponent c n := by
    have h := sukInputExponent_ge (show 1 ≤ 4 * roundedScale c n + 1 by omega)
    change 4 * roundedScale c n + 1 ≤ scaleInputExponent c n at h
    exact_mod_cast (show 4 * roundedScale c n ≤ scaleInputExponent c n by omega)
  have hnegative := entropy_slack_negative_at_endpoint
    (by exact_mod_cast hm) hnp.le hS.le hL.le hH hd (asymptoticScale_sq (by omega))
  have he := budgetRatio_identity (roundedScale c n) (scaleInputExponent c n) n
    (asymptoticScale n) (Real.logb 2 n) (Real.logb 2 (roundedScale c n))
    publishedCoefficient hS.ne' hL.ne' (asymptoticScale_sq (by omega))
  have hp : normalizedBudget c publishedCoefficient n * ((n : ℝ) * Real.logb 2 n) < 0 := by
    change budgetRatio _ _ _ _ _ _ _ * _ < 0
    rw [he]
    exact hnegative
  exact neg_of_mul_neg_left hp (mul_pos hnp hL).le

/-- At every fixed positive scale, the finite entropy budget is eventually
negative at exactly 8√2/3, despite its limiting leading slack being zero at the
optimal scale. This theorem concerns only `normalizedBudget`. -/
theorem budget_eventually_negative_at_published {c : ℝ} (hc : 0 < c) :
    ∀ᶠ n : ℕ in atTop, normalizedBudget c publishedCoefficient n < 0 := by
  have hlog := (log_nat_tendsto.const_mul_atTop (sq_pos_of_pos hc)).eventually_ge_atTop 1
  filter_upwards [eventually_ge_atTop 9, hlog] with n hn hlog
  exact normalizedBudget_neg_at_endpoint hc hn hlog

/-- Including the endpoint completes the obstruction for this fixed-scale
entropy interface. It does not rule out different finite counting criteria. -/
theorem budget_eventually_negative_at_or_below_published {c C : ℝ}
    (hc : 0 < c) (hC : C ≤ publishedCoefficient) :
    ∀ᶠ n : ℕ in atTop, normalizedBudget c C n < 0 := by
  rcases lt_or_eq_of_le hC with hC | rfl
  · exact budget_eventually_negative_below_published hc hC
  · exact budget_eventually_negative_at_published hc

end ErdosSzekeres.HMPT
