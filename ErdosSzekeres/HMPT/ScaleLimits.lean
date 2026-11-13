import ErdosSzekeres.HMPT.AsymptoticInput
import Mathlib.Analysis.SpecialFunctions.Sqrt

namespace ErdosSzekeres.HMPT

open Filter
open scoped Topology

noncomputable def asymptoticScale (n : ℕ) : ℝ := Real.sqrt ((n : ℝ) * Real.logb 2 n)

theorem log_nat_tendsto : Tendsto (fun n : ℕ => Real.logb 2 n) atTop atTop :=
  (Real.tendsto_logb_atTop (by norm_num : (1 : ℝ) < 2)).comp tendsto_natCast_atTop_atTop

theorem asymptoticScale_pos {n : ℕ} (hn : 2 ≤ n) : 0 < asymptoticScale n := by
  have hp : (1 : ℝ) < n := by exact_mod_cast (show 1 < n by omega)
  exact Real.sqrt_pos.mpr (mul_pos (by linarith) (Real.logb_pos (by norm_num) hp))

theorem asymptoticScale_sq {n : ℕ} (hn : 1 ≤ n) :
    asymptoticScale n ^ 2 = (n : ℝ) * Real.logb 2 n := by
  apply Real.sq_sqrt
  exact mul_nonneg (Nat.cast_nonneg _) (Real.logb_nonneg (by norm_num) (by exact_mod_cast hn))

theorem asymptoticScale_tendsto : Tendsto asymptoticScale atTop atTop := by
  have h := (tendsto_natCast_atTop_atTop : Tendsto (fun n : ℕ => (n : ℝ)) atTop atTop).atTop_mul_atTop₀
    log_nat_tendsto
  change Tendsto (fun n : ℕ => Real.sqrt ((n : ℝ) * Real.logb 2 n)) atTop atTop
  simpa only [Real.sqrt_eq_rpow, Function.comp_def] using
    (tendsto_rpow_atTop (by norm_num : (0 : ℝ) < 1 / 2)).comp h

theorem asymptoticScale_div_nat_tendsto :
    Tendsto (fun n : ℕ => asymptoticScale n / n) atTop (𝓝 0) := by
  have h : Tendsto (fun n : ℕ => Real.sqrt (Real.logb 2 n / n)) atTop (𝓝 0) := by
    simpa using (logb_div_rpow_nat_tendsto (a := 1) (by norm_num)).sqrt
  apply h.congr'
  filter_upwards [eventually_ge_atTop 2] with n hn
  have hp : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
  have hnonneg : 0 ≤ (n : ℝ) * Real.logb 2 n :=
    mul_nonneg hp.le (Real.logb_nonneg (by norm_num) (by exact_mod_cast (show 1 ≤ n by omega)))
  symm
  calc
    asymptoticScale n / n = Real.sqrt (((n : ℝ) * Real.logb 2 n) / (n : ℝ) ^ 2) := by
      rw [Real.sqrt_div hnonneg, Real.sqrt_sq hp.le]
      rfl
    _ = Real.sqrt (Real.logb 2 n / n) := by congr 1; field_simp

theorem log_asymptoticScale {n : ℕ} (hn : 2 ≤ n) :
    Real.logb 2 (asymptoticScale n) = (Real.logb 2 n + Real.logb 2 (Real.logb 2 n)) / 2 := by
  have hp : (1 : ℝ) < n := by exact_mod_cast (show 1 < n by omega)
  have hl := Real.logb_pos (by norm_num : (1 : ℝ) < 2) hp
  have he : Real.log (asymptoticScale n) = (Real.log n + Real.log (Real.logb 2 n)) / 2 := by
    unfold asymptoticScale
    rw [Real.log_sqrt (mul_nonneg (by linarith) hl.le),
      Real.log_mul (by linarith : (n : ℝ) ≠ 0) hl.ne']
  change Real.log (asymptoticScale n) / Real.log 2 = _
  rw [he]
  unfold Real.logb
  ring

theorem log_asymptoticScale_ratio_tendsto :
    Tendsto (fun n : ℕ => Real.logb 2 (asymptoticScale n) / Real.logb 2 n) atTop (𝓝 (1 / 2)) := by
  have hloglog : Tendsto (fun n : ℕ => Real.logb 2 (Real.logb 2 n) / Real.logb 2 n)
      atTop (𝓝 0) := Real.isLittleO_logb_id_atTop.tendsto_div_nhds_zero.comp log_nat_tendsto
  have h : Tendsto (fun n : ℕ => (1 + Real.logb 2 (Real.logb 2 n) / Real.logb 2 n) / 2)
      atTop (𝓝 (1 / 2)) := by
    simpa using ((tendsto_const_nhds : Tendsto (fun _ : ℕ => (1 : ℝ)) atTop (𝓝 1)).add hloglog).div_const 2
  apply h.congr'
  filter_upwards [eventually_ge_atTop 2] with n hn
  have hp : (1 : ℝ) < n := by exact_mod_cast (show 1 < n by omega)
  rw [log_asymptoticScale hn]
  field_simp [(Real.logb_pos (by norm_num : (1 : ℝ) < 2) hp).ne']

noncomputable def roundedScale (c : ℝ) (n : ℕ) : ℕ := ⌈c * asymptoticScale n⌉₊

theorem roundedScale_ratio_tendsto {c : ℝ} (hc : 0 ≤ c) :
    Tendsto (fun n : ℕ => (roundedScale c n : ℝ) / asymptoticScale n) atTop (𝓝 c) := by
  apply tendsto_natCeil_div asymptoticScale_tendsto
  · apply (tendsto_const_nhds : Tendsto (fun _ : ℕ => c) atTop (𝓝 c)).congr'
    filter_upwards [eventually_ge_atTop 2] with n hn
    exact (mul_div_cancel_right₀ c (asymptoticScale_pos hn).ne').symm
  · exact Eventually.of_forall (fun n => mul_nonneg hc (Real.sqrt_nonneg _))

theorem roundedScale_tendsto {c : ℝ} (hc : 0 < c) :
    Tendsto (roundedScale c) atTop atTop := by
  exact tendsto_nat_ceil_atTop.comp (asymptoticScale_tendsto.const_mul_atTop hc)

theorem roundedScale_div_nat_tendsto {c : ℝ} (hc : 0 ≤ c) :
    Tendsto (fun n : ℕ => (roundedScale c n : ℝ) / n) atTop (𝓝 0) := by
  have h : Tendsto (fun n : ℕ => ((roundedScale c n : ℝ) / asymptoticScale n) *
      (asymptoticScale n / n)) atTop (𝓝 0) := by
    simpa using (roundedScale_ratio_tendsto hc).mul asymptoticScale_div_nat_tendsto
  apply h.congr'
  filter_upwards [eventually_ge_atTop 2] with n hn
  field_simp [(asymptoticScale_pos hn).ne']

theorem log_roundedScale_ratio_tendsto {c : ℝ} (hc : 0 < c) :
    Tendsto (fun n : ℕ => Real.logb 2 (roundedScale c n) / Real.logb 2 n)
      atTop (𝓝 (1 / 2)) := by
  have hr := (Real.continuousAt_logb (b := 2) hc.ne').tendsto.comp (roundedScale_ratio_tendsto hc.le)
  have h : Tendsto (fun n : ℕ =>
      Real.logb 2 ((roundedScale c n : ℝ) / asymptoticScale n) / Real.logb 2 n +
        Real.logb 2 (asymptoticScale n) / Real.logb 2 n) atTop (𝓝 (1 / 2)) := by
    simpa using (hr.div_atTop log_nat_tendsto).add log_asymptoticScale_ratio_tendsto
  apply h.congr'
  filter_upwards [eventually_ge_atTop 2, (roundedScale_tendsto hc).eventually_ge_atTop 1] with n hn hm
  have hmp : (0 : ℝ) < roundedScale c n := by exact_mod_cast (show 0 < roundedScale c n by omega)
  rw [Real.logb_div hmp.ne' (asymptoticScale_pos hn).ne']
  ring

noncomputable def scaleInputExponent (c : ℝ) (n : ℕ) : ℕ :=
  sukInputExponent (4 * roundedScale c n + 1)

theorem four_roundedScale_tendsto {c : ℝ} (hc : 0 < c) :
    Tendsto (fun n => 4 * roundedScale c n + 1) atTop atTop :=
  tendsto_atTop_mono (fun _ => by omega) (roundedScale_tendsto hc)

theorem scaleInputExponent_ratio_tendsto {c : ℝ} (hc : 0 < c) :
    Tendsto (fun n : ℕ => (scaleInputExponent c n : ℝ) / asymptoticScale n) atTop (𝓝 (4 * c)) := by
  have hinput := sukInputExponent_ratio_tendsto.comp (four_roundedScale_tendsto hc)
  have hK : Tendsto (fun n : ℕ => ((4 * roundedScale c n + 1 : ℕ) : ℝ) / asymptoticScale n)
      atTop (𝓝 (4 * c)) := by
    have h := ((roundedScale_ratio_tendsto hc.le).const_mul 4).add
      (asymptoticScale_tendsto.const_div_atTop 1)
    convert h using 1 <;> simp [add_div, mul_div_assoc]
  have h : Tendsto (fun n : ℕ =>
      (sukInputExponent (4 * roundedScale c n + 1) : ℝ) / (4 * roundedScale c n + 1 : ℕ) *
        (((4 * roundedScale c n + 1 : ℕ) : ℝ) / asymptoticScale n)) atTop (𝓝 (4 * c)) := by
    simpa using hinput.mul hK
  apply h.congr'
  exact Eventually.of_forall (fun n => by
    unfold scaleInputExponent
    have hp : ((4 * roundedScale c n + 1 : ℕ) : ℝ) ≠ 0 := by positivity
    field_simp)

theorem scaleInputExponent_div_nat_tendsto {c : ℝ} (hc : 0 < c) :
    Tendsto (fun n : ℕ => (scaleInputExponent c n : ℝ) / n) atTop (𝓝 0) := by
  have h : Tendsto (fun n : ℕ => (scaleInputExponent c n : ℝ) / asymptoticScale n *
      (asymptoticScale n / n)) atTop (𝓝 0) := by
    simpa using (scaleInputExponent_ratio_tendsto hc).mul asymptoticScale_div_nat_tendsto
  apply h.congr'
  filter_upwards [eventually_ge_atTop 2] with n hn
  field_simp [(asymptoticScale_pos hn).ne']

theorem scaleInputExponent_forces_eventually {c : ℝ} (hc : 0 < c) :
    ∀ᶠ n : ℕ in atTop, ForcesConvexNGon (2 ^ scaleInputExponent c n) (4 * roundedScale c n + 1) :=
  (four_roundedScale_tendsto hc).eventually sukInputExponent_forces_eventually

end ErdosSzekeres.HMPT
