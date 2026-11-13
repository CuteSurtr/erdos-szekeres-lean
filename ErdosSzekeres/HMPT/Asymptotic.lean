import ErdosSzekeres.HMPT.ScaleLimits
import ErdosSzekeres.HMPT.Entropy
import ErdosSzekeres.HMPT.Statement

namespace ErdosSzekeres.HMPT

open Filter
open scoped Topology

/-- Normalize the exact entropy slack by n log₂ n. The subtracted terms
retain the endpoint, logarithmic, and integer-rounding losses. -/
noncomputable def budgetRatio (m d n S L H C : ℝ) : ℝ :=
  (3 * (m / S) - 6 / S) * (C - 1 / S) - 6 / L -
    (d / S + 1 / S) * (4 * (m / S) + 1 / S) -
    6 * (m / S) * (1 / S) - (4 + 3 * (m / n)) * (H / L + 4 / L)

theorem budgetRatio_identity (m d n S L H C : ℝ) (hS : S ≠ 0) (hL : L ≠ 0)
    (hsq : S ^ 2 = n * L) :
    budgetRatio m d n S L H C * (n * L) =
      (3 * m - 6) * (n + C * S - 1) -
        ((d + 1) * (4 * m + 1) + 3 * m * n + 6 * m + (4 * n + 3 * m) * (H + 4)) := by
  have hn : n = S ^ 2 / L := (eq_div_iff hL).mpr hsq.symm
  rw [hn]
  unfold budgetRatio
  field_simp
  ring

noncomputable def normalizedBudget (c C : ℝ) (n : ℕ) : ℝ :=
  budgetRatio (roundedScale c n) (scaleInputExponent c n) n
    (asymptoticScale n) (Real.logb 2 n) (Real.logb 2 (roundedScale c n)) C

/-- The two-scale leading penalty is 16c²+2 when m/sqrt(n log₂ n) tends to c. -/
theorem normalizedBudget_tendsto {c : ℝ} (hc : 0 < c) (C : ℝ) :
    Tendsto (normalizedBudget c C) atTop (𝓝 (3 * c * C - 16 * c ^ 2 - 2)) := by
  have hm := roundedScale_ratio_tendsto hc.le
  have hd := scaleInputExponent_ratio_tendsto hc
  have hmn := roundedScale_div_nat_tendsto hc.le
  have hlog := log_roundedScale_ratio_tendsto hc
  have hS := asymptoticScale_tendsto.const_div_atTop 1
  have hL := log_nat_tendsto.const_div_atTop 1
  have h₁ := ((hm.const_mul 3).sub (hS.const_mul 6)).mul
    ((tendsto_const_nhds : Tendsto (fun _ : ℕ => C) atTop (𝓝 C)).sub hS)
  have h₂ := hL.const_mul 6
  have h₃ := (hd.add hS).mul ((hm.const_mul 4).add hS)
  have h₄ := (hm.const_mul 6).mul hS
  have h₅ := ((tendsto_const_nhds : Tendsto (fun _ : ℕ => (4 : ℝ)) atTop (𝓝 4)).add
    (hmn.const_mul 3)).mul (hlog.add (hL.const_mul 4))
  have h := (((h₁.sub h₂).sub h₃).sub h₄).sub h₅
  convert h using 1
  · funext n
    unfold normalizedBudget budgetRatio
    ring
  · norm_num
    ring

/-- Any positive limiting slack gives a geometric bound at the exact floor
threshold. All parameter and input-bound hypotheses are discharged eventually. -/
theorem eventual_bound_of_positive_slack {c C : ℝ} (hc : 0 < c)
    (hslack : 0 < 3 * c * C - 16 * c ^ 2 - 2) :
    ∀ᶠ n : ℕ in atTop, ForcesConvexNGon (threshold C n) n := by
  have hC : 0 < C := by nlinarith [sq_nonneg c]
  have hbudget := (normalizedBudget_tendsto hc C).eventually (eventually_gt_nhds hslack)
  have hd : Tendsto (fun n : ℕ => (scaleInputExponent c n : ℝ) / n + 1 / n)
      atTop (𝓝 0) := by
    simpa using (scaleInputExponent_div_nat_tendsto hc).add
      ((tendsto_natCast_atTop_atTop : Tendsto (fun n : ℕ => (n : ℝ)) atTop atTop).const_div_atTop 1)
  have hsize : Tendsto (fun n : ℕ => 8 * ((roundedScale c n : ℝ) / n) + 3 / n)
      atTop (𝓝 0) := by
    simpa using ((roundedScale_div_nat_tendsto hc.le).const_mul 8).add
      ((tendsto_natCast_atTop_atTop : Tendsto (fun n : ℕ => (n : ℝ)) atTop atTop).const_div_atTop 3)
  filter_upwards [eventually_ge_atTop 4, (roundedScale_tendsto hc).eventually_ge_atTop 3,
    scaleInputExponent_forces_eventually hc, hbudget,
    hd.eventually (eventually_lt_nhds (by norm_num : (0 : ℝ) < 1)),
    hsize.eventually (eventually_lt_nhds (by norm_num : (0 : ℝ) < 1))]
    with n hn hm hforce hb hd hsize
  have hnp : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
  have hl : 0 < Real.logb 2 n :=
    Real.logb_pos (by norm_num) (by exact_mod_cast (show 1 < n by omega))
  have hS := asymptoticScale_pos (show 2 ≤ n by omega)
  have hK : 4 * roundedScale c n + 1 ≤ 2 ^ scaleInputExponent c n :=
    (sukInputExponent_ge (by omega)).trans (Nat.lt_pow_self (a := 2) (by decide)).le
  apply real_entropy_two_scale_bound hm hn hforce hK
  · have hd' : (scaleInputExponent c n : ℝ) + 1 < n := by
      apply (div_lt_one hnp).mp
      simpa only [add_div] using hd
    change (scaleInputExponent c n : ℝ) + 1 ≤ n + C * asymptoticScale n
    nlinarith
  · have hs' : 8 * (roundedScale c n : ℝ) + 3 < n := by
      apply (div_lt_one hnp).mp
      simpa only [add_div, mul_div_assoc] using hsize
    change 2 * (4 * (roundedScale c n : ℝ) + 1) + 1 ≤ n + C * asymptoticScale n
    nlinarith
  · have he := budgetRatio_identity (roundedScale c n) (scaleInputExponent c n) n
      (asymptoticScale n) (Real.logb 2 n) (Real.logb 2 (roundedScale c n)) C hS.ne' hl.ne'
      (asymptoticScale_sq (show 1 ≤ n by omega))
    have hp := mul_pos hb (mul_pos hnp hl)
    change 0 < budgetRatio _ _ _ _ _ _ _ * _ at hp
    rw [he] at hp
    change ((scaleInputExponent c n : ℝ) + 1) * (4 * (roundedScale c n : ℝ) + 1) +
      3 * roundedScale c n * n + 6 * roundedScale c n +
      (4 * (n : ℝ) + 3 * roundedScale c n) * (Real.logb 2 (roundedScale c n) + 4) <
      (3 * (roundedScale c n : ℝ) - 6) * (n + C * asymptoticScale n - 1)
    linarith

/-- Final HMPT 2020 leading coefficient, including arbitrary positive epsilon
and the exact natural-floor convention, for ordinary real point sets. -/
theorem theorem2020 : Theorem2020 := by
  intro ε hε
  let c : ℝ := 1 / (2 * Real.sqrt 2)
  have hs : 0 < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have hc : 0 < c := by dsimp [c]; positivity
  have heq : 3 * c * publishedCoefficient - 16 * c ^ 2 - 2 = 0 := by
    dsimp [c, publishedCoefficient]
    field_simp
    nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
  have hslack : 0 < 3 * c * (publishedCoefficient + ε) - 16 * c ^ 2 - 2 := by
    nlinarith [mul_pos hc hε]
  obtain ⟨n₀, hn₀⟩ := eventually_atTop.mp (eventual_bound_of_positive_slack hc hslack)
  refine ⟨max n₀ 3, by omega, ?_⟩
  intro n hn
  exact hn₀ n (by omega)

end ErdosSzekeres.HMPT
