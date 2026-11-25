import LeanLB.G.Cyclo
import LeanLB.G.Approx
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# Seven-fold sets: coordinates in `ℤ[t]`, `t = 2cos(2π/7)`, `t³ + t² - 2t - 1 = 0`

`Σ_j w_j ζ^j = (X(t)/2, s·Y(t))` with `s = sin(2π/7)` and `X, Y ∈ ℤ[t]` of degree at most 2
(`lat7`, `cycPoint_seven`), and rational bounds `lo/2⁶⁴ < t < (lo + 1)/2⁶⁴` (`t7_bounds`) for the
certified approximations of `LeanLB/G/Approx.lean`.
-/

namespace LeanLB.G

open ErdosSzekeres Real

/-- `t = 2cos(2π/7)`. -/
noncomputable def t7 : ℝ := 2 * Real.cos (2 * π / 7)
/-- `s = sin(2π/7)`. -/
noncomputable def s7 : ℝ := Real.sin (2 * π / 7)

theorem cos27_lt_one : Real.cos (2 * π / 7) < 1 := by
  have := Real.cos_lt_cos_of_nonneg_of_le_pi (le_refl 0) (by linarith [Real.pi_pos] : 2 * π / 7 ≤ π)
    (by positivity : (0 : ℝ) < 2 * π / 7)
  rwa [Real.cos_zero] at this

theorem half_lt_cos27 : 1 / 2 < Real.cos (2 * π / 7) := by
  have := Real.cos_lt_cos_of_nonneg_of_le_pi (by positivity : (0 : ℝ) ≤ 2 * π / 7)
    (by linarith [Real.pi_pos] : π / 3 ≤ π) (by linarith [Real.pi_pos] : 2 * π / 7 < π / 3)
  rwa [Real.cos_pi_div_three] at this

/-- `cos 4x = cos 3x` for `x = 2π/7`, hence `(c - 1)(8c³ + 4c² - 4c - 1) = 0`. -/
theorem t7_cubic : t7 ^ 3 + t7 ^ 2 - 2 * t7 - 1 = 0 := by
  set x := 2 * π / 7 with hx
  set c := Real.cos x with hc
  have h43 : Real.cos (2 * (2 * x)) = Real.cos (3 * x) := by
    rw [show 2 * (2 * x) = 2 * π - 3 * x by rw [hx]; ring, Real.cos_two_pi_sub]
  rw [Real.cos_two_mul, Real.cos_two_mul, Real.cos_three_mul] at h43
  have hne : c - 1 ≠ 0 := by linarith [cos27_lt_one]
  have hprod : (c - 1) * (8 * c ^ 3 + 4 * c ^ 2 - 4 * c - 1) = 0 := by
    rw [← hc] at h43; linear_combination h43
  have hq := (mul_eq_zero.mp hprod).resolve_left hne
  unfold t7; rw [← hx, ← hc]
  linear_combination hq

theorem t7_mono {x y : ℝ} (hx : 1 ≤ x) (hxy : x ≤ y) :
    x ^ 3 + x ^ 2 - 2 * x - 1 ≤ y ^ 3 + y ^ 2 - 2 * y - 1 := by
  nlinarith [mul_nonneg (sub_nonneg.mpr hxy) (sub_nonneg.mpr hx), sq_nonneg (y - x), sq_nonneg x,
    mul_nonneg (sub_nonneg.mpr hxy) (sq_nonneg (x + y))]

theorem t7_gt_one : 1 < t7 := by unfold t7; linarith [half_lt_cos27]

/-- `lo` with `lo/2⁶⁴ < t < (lo + 1)/2⁶⁴`. -/
def lo7 : ℤ := 23002713614911870667
/-- `2⁶⁴`. -/
def D7 : ℤ := 18446744073709551616

theorem t7_bounds : (lo7 : ℝ) / D7 < t7 ∧ t7 < ((lo7 + 1 : ℤ) : ℝ) / D7 := by
  have hc := t7_cubic
  have h1 := t7_gt_one
  constructor
  · by_contra h
    push_neg at h
    have hm := t7_mono h1.le h
    have : ((lo7 : ℝ) / D7) ^ 3 + ((lo7 : ℝ) / D7) ^ 2 - 2 * ((lo7 : ℝ) / D7) - 1 < 0 := by
      unfold lo7 D7; norm_num
    linarith
  · by_contra h
    push_neg at h
    have hlo : (1 : ℝ) ≤ ((lo7 + 1 : ℤ) : ℝ) / D7 := by unfold lo7 D7; norm_num
    have hm := t7_mono hlo h
    have : 0 < (((lo7 + 1 : ℤ) : ℝ) / D7) ^ 3 + (((lo7 + 1 : ℤ) : ℝ) / D7) ^ 2 -
        2 * (((lo7 + 1 : ℤ) : ℝ) / D7) - 1 := by
      unfold lo7 D7; norm_num
    linarith

theorem s7_pos : 0 < s7 := by
  unfold s7
  apply Real.sin_pos_of_pos_of_lt_pi
  · positivity
  · linarith [Real.pi_pos]

/-! ## The rows of a `.pts` file with `m = 7` -/

/-- `Σ w_j ζ^j = (X(t)/2, s·Y(t))`. -/
def lat7 (w : List ℤ) : Q :=
  ((2 * w.getD 0 0 - 2 * (w.getD 2 0 + w.getD 5 0) + (w.getD 3 0 + w.getD 4 0),
    (w.getD 1 0 + w.getD 6 0) - (w.getD 3 0 + w.getD 4 0),
    (w.getD 2 0 + w.getD 5 0) - (w.getD 3 0 + w.getD 4 0)),
   ((w.getD 1 0 - w.getD 6 0) - (w.getD 3 0 - w.getD 4 0), w.getD 2 0 - w.getD 5 0,
    w.getD 3 0 - w.getD 4 0))

theorem cos_sin_seven (j : ℕ) (hj : j ∈ ({1, 2, 3, 4, 5, 6} : Finset ℕ)) :
    Real.cos (2 * π * (j : ℝ) / ((7 : ℕ) : ℝ)) =
      (if j = 1 ∨ j = 6 then t7 / 2 else if j = 2 ∨ j = 5 then (t7 ^ 2 - 2) / 2
        else (-t7 ^ 2 - t7 + 1) / 2) ∧
    Real.sin (2 * π * (j : ℝ) / ((7 : ℕ) : ℝ)) =
      (if j = 1 then s7 else if j = 6 then -s7 else if j = 2 then s7 * t7
        else if j = 5 then -(s7 * t7) else if j = 3 then s7 * (t7 ^ 2 - 1)
        else -(s7 * (t7 ^ 2 - 1))) := by
  set x := 2 * π / 7 with hx
  have hc : Real.cos x = t7 / 2 := by unfold t7; ring
  have hs : Real.sin x = s7 := rfl
  have hs2 : Real.sin x ^ 2 = 1 - (t7 / 2) ^ 2 := by rw [← hc]; linarith [Real.sin_sq_add_cos_sq x]
  have c2 : Real.cos (2 * x) = (t7 ^ 2 - 2) / 2 := by rw [Real.cos_two_mul, hc]; ring
  have s2 : Real.sin (2 * x) = s7 * t7 := by rw [Real.sin_two_mul, hc, hs]; ring
  have c3 : Real.cos (3 * x) = (-t7 ^ 2 - t7 + 1) / 2 := by
    rw [Real.cos_three_mul, hc]; linear_combination (1 / 2) * t7_cubic
  have s3 : Real.sin (3 * x) = s7 * (t7 ^ 2 - 1) := by
    rw [Real.sin_three_mul, hs]
    have : s7 ^ 2 = 1 - (t7 / 2) ^ 2 := by rw [← hs]; exact hs2
    linear_combination (-4 * s7) * this
  simp only [Finset.mem_insert, Finset.mem_singleton] at hj
  rcases hj with rfl | rfl | rfl | rfl | rfl | rfl
  · rw [show 2 * π * ((1 : ℕ) : ℝ) / ((7 : ℕ) : ℝ) = x by rw [hx]; push_cast; ring]
    simp [hc, hs]
  · rw [show 2 * π * ((2 : ℕ) : ℝ) / ((7 : ℕ) : ℝ) = 2 * x by rw [hx]; push_cast; ring]
    simp [c2, s2]
  · rw [show 2 * π * ((3 : ℕ) : ℝ) / ((7 : ℕ) : ℝ) = 3 * x by rw [hx]; push_cast; ring]
    simp [c3, s3]
  · rw [show 2 * π * ((4 : ℕ) : ℝ) / ((7 : ℕ) : ℝ) = 2 * π - 3 * x by rw [hx]; push_cast; ring]
    simp [Real.cos_two_pi_sub, Real.sin_two_pi_sub, c3, s3]
  · rw [show 2 * π * ((5 : ℕ) : ℝ) / ((7 : ℕ) : ℝ) = 2 * π - 2 * x by rw [hx]; push_cast; ring]
    simp [Real.cos_two_pi_sub, Real.sin_two_pi_sub, c2, s2]
  · rw [show 2 * π * ((6 : ℕ) : ℝ) / ((7 : ℕ) : ℝ) = 2 * π - x by rw [hx]; push_cast; ring]
    simp [Real.cos_two_pi_sub, Real.sin_two_pi_sub, hc, hs]

theorem cycPoint_seven (w : List ℤ) : cycPoint 7 w = embT t7 s7 (lat7 w) := by
  obtain ⟨c1, s1⟩ := cos_sin_seven 1 (by decide)
  obtain ⟨c2, s2⟩ := cos_sin_seven 2 (by decide)
  obtain ⟨c3, s3⟩ := cos_sin_seven 3 (by decide)
  obtain ⟨c4, s4⟩ := cos_sin_seven 4 (by decide)
  obtain ⟨c5, s5⟩ := cos_sin_seven 5 (by decide)
  obtain ⟨c6, s6⟩ := cos_sin_seven 6 (by decide)
  simp only [cycPoint, unitRoot, Finset.sum_range_succ, Finset.sum_range_zero, zero_add]
  rw [c1, s1, c2, s2, c3, s3, c4, s4, c5, s5, c6, s6]
  funext i
  fin_cases i <;> simp [embT, lat7, evT] <;> ring

end LeanLB.G
