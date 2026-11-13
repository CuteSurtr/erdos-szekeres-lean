import ErdosSzekeres.Suk.Asymptotic
import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics

namespace ErdosSzekeres.HMPT

open Filter
open scoped Topology

/-- Natural ceilings have vanishing relative error along a divergent positive
denominator. This includes the parameter and input-exponent rounding below. -/
theorem tendsto_natCeil_div {f g : ℕ → ℝ} {L : ℝ}
    (hg : Tendsto g atTop atTop) (hf : Tendsto (fun n => f n / g n) atTop (𝓝 L))
    (hpos : ∀ᶠ n in atTop, 0 ≤ f n) :
    Tendsto (fun n => (⌈f n⌉₊ : ℝ) / g n) atTop (𝓝 L) := by
  have hu : Tendsto (fun n => f n / g n + 1 / g n) atTop (𝓝 L) := by
    simpa using hf.add (hg.const_div_atTop 1)
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le' hf hu
  · filter_upwards [hg.eventually_gt_atTop 0] with n hn
    exact div_le_div_of_nonneg_right (Nat.le_ceil _) hn.le
  · filter_upwards [hpos, hg.eventually_gt_atTop 0] with n hf hn
    have h := div_le_div_of_nonneg_right (Nat.ceil_lt_add_one hf).le hn.le
    simpa only [add_div] using h

theorem logb_div_rpow_nat_tendsto {a : ℝ} (ha : 0 < a) :
    Tendsto (fun n : ℕ => Real.logb 2 n / (n : ℝ) ^ a) atTop (𝓝 0) := by
  have h := ((isLittleO_log_rpow_atTop ha).tendsto_div_nhds_zero).comp
    tendsto_natCast_atTop_atTop
  have h' := h.div_const (Real.log 2)
  simpa only [zero_div, Real.logb, div_right_comm] using h'

/-- Suk's proved error term is sublinear. -/
theorem suk_exponent_ratio_tendsto :
    Tendsto (fun n : ℕ => Suk.exponent 6 n / n) atTop (𝓝 1) := by
  have h := (logb_div_rpow_nat_tendsto (a := (1 : ℝ) / 3) (by norm_num)).const_mul 6
  have h' : Tendsto (fun n : ℕ => 1 + 6 * (Real.logb 2 n / (n : ℝ) ^ ((1 : ℝ) / 3)))
      atTop (𝓝 1) := by
    simpa using (tendsto_const_nhds : Tendsto (fun _ : ℕ => (1 : ℝ)) atTop (𝓝 1)).add h
  have he : (fun n : ℕ => 1 + 6 * (Real.logb 2 n / (n : ℝ) ^ ((1 : ℝ) / 3))) =ᶠ[atTop]
      (fun n : ℕ => Suk.exponent 6 n / n) := by
    filter_upwards [eventually_ge_atTop 1] with n hn
    have hp : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
    have hmul : (n : ℝ) ^ ((2 : ℝ) / 3) * (n : ℝ) ^ ((1 : ℝ) / 3) = n := by
      rw [← Real.rpow_add hp]
      norm_num
    have hroot : (n : ℝ) ^ ((1 : ℝ) / 3) ≠ 0 := (Real.rpow_pos_of_pos hp _).ne'
    unfold Suk.exponent
    field_simp
    nlinarith [congrArg (fun x : ℝ => x * Real.logb 2 n) hmul]
  exact h'.congr' he

/-- A natural exponent extracted from the complete Suk theorem. -/
noncomputable def sukInputExponent (k : ℕ) : ℕ := ⌈Suk.exponent 6 k⌉₊

theorem suk_exponent_nonneg {k : ℕ} (hk : 1 ≤ k) : 0 ≤ Suk.exponent 6 k := by
  have hl : 0 ≤ Real.logb 2 k := Real.logb_nonneg (by norm_num) (by exact_mod_cast hk)
  unfold Suk.exponent
  positivity

theorem sukInputExponent_ge {k : ℕ} (hk : 1 ≤ k) : k ≤ sukInputExponent k := by
  have hl : 0 ≤ Real.logb 2 k := Real.logb_nonneg (by norm_num) (by exact_mod_cast hk)
  have h : (k : ℝ) ≤ Suk.exponent 6 k := by
    unfold Suk.exponent
    exact le_add_of_nonneg_right (by positivity)
  exact_mod_cast h.trans (Nat.le_ceil _)

theorem sukInputExponent_ratio_tendsto :
    Tendsto (fun k : ℕ => (sukInputExponent k : ℝ) / k) atTop (𝓝 1) := by
  apply tendsto_natCeil_div tendsto_natCast_atTop_atTop suk_exponent_ratio_tendsto
  filter_upwards [eventually_ge_atTop 1] with k hk
  exact suk_exponent_nonneg hk

/-- The natural input exponent eventually forces a convex k-gon, by the
fully checked Suk theorem and monotonicity of the floor threshold. -/
theorem sukInputExponent_forces_eventually :
    ∀ᶠ k : ℕ in atTop, ForcesConvexNGon (2 ^ sukInputExponent k) k := by
  obtain ⟨k₀, _, hk₀⟩ := Suk.theorem2016
  filter_upwards [eventually_ge_atTop k₀] with k hk
  apply (hk₀ k hk).mono
  apply Nat.floor_le_of_le
  have h := Real.rpow_le_rpow_of_exponent_le (by norm_num : (1 : ℝ) ≤ 2)
    (Nat.le_ceil (Suk.exponent 6 k))
  simpa only [sukInputExponent, Real.rpow_natCast, Nat.cast_pow, Nat.cast_ofNat] using h

end ErdosSzekeres.HMPT
