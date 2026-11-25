import LeanLB.G.Cyclo
import LeanLB.G.Approx
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# Five-fold sets: coordinates in `ℤ[t]`, `t = 2cos(2π/5) = (√5 - 1)/2`

`Σ_j w_j ζ^j = (X(t)/2, s·Y(t))` with `s = sin(2π/5)` and `X, Y ∈ ℤ[t]` (`lat5`, `cycPoint_five`),
and rational bounds `lo/2⁸⁰ < t < (lo + 1)/2⁸⁰` (`t5_bounds`) for the certified approximations of
`LeanLB/G/Approx.lean`.
-/

namespace LeanLB.G

open ErdosSzekeres Real

/-- `t = 2cos(2π/5)`. -/
noncomputable def t5 : ℝ := 2 * Real.cos (2 * π / 5)
/-- `s = sin(2π/5)`. -/
noncomputable def s5 : ℝ := Real.sin (2 * π / 5)

theorem sqrt5_sq : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)

theorem t5_eq : t5 = (Real.sqrt 5 - 1) / 2 := by
  have h : 2 * π / 5 = 2 * (π / 5) := by ring
  unfold t5
  rw [h, Real.cos_two_mul, Real.cos_pi_div_five]
  nlinarith [sqrt5_sq]

theorem t5_sq : t5 ^ 2 = 1 - t5 := by
  rw [t5_eq]; nlinarith [sqrt5_sq]

theorem s5_pos : 0 < s5 := by
  unfold s5
  apply Real.sin_pos_of_pos_of_lt_pi
  · positivity
  · linarith [Real.pi_pos]

theorem s5_sq : s5 ^ 2 = 1 - (t5 / 2) ^ 2 := by
  unfold s5 t5
  have := Real.sin_sq_add_cos_sq (2 * π / 5)
  linarith

/-- `lo` with `lo/2⁸⁰ < t < (lo + 1)/2⁸⁰`. -/
def lo5 : ℤ := 747157246399165135975324
/-- `2⁸⁰`. -/
def D5 : ℤ := 1208925819614629174706176

theorem t5_bounds : (lo5 : ℝ) / D5 < t5 ∧ t5 < ((lo5 + 1 : ℤ) : ℝ) / D5 := by
  rw [t5_eq]
  have hs := Real.sqrt_nonneg 5
  constructor
  · have : (2 * ((lo5 : ℝ) / D5) + 1) < Real.sqrt 5 := by
      rw [Real.lt_sqrt (by unfold lo5 D5; norm_num)]
      unfold lo5 D5; norm_num
    linarith
  · have : Real.sqrt 5 < 2 * (((lo5 + 1 : ℤ) : ℝ) / D5) + 1 := by
      rw [Real.sqrt_lt' (by unfold lo5 D5; norm_num)]
      unfold lo5 D5; norm_num
    linarith

/-! ## The rows of a `.pts` file with `m = 5` -/

/-- `Σ w_j ζ^j = (X(t)/2, s·Y(t))`. -/
def lat5 (w : List ℤ) : Q :=
  ((2 * w.getD 0 0 - w.getD 2 0 - w.getD 3 0, w.getD 1 0 + w.getD 4 0 - w.getD 2 0 - w.getD 3 0, 0),
   (w.getD 1 0 - w.getD 4 0, w.getD 2 0 - w.getD 3 0, 0))

theorem cos_sin_five :
    Real.cos (2 * π * ((1 : ℕ) : ℝ) / ((5 : ℕ) : ℝ)) = t5 / 2 ∧
    Real.sin (2 * π * ((1 : ℕ) : ℝ) / ((5 : ℕ) : ℝ)) = s5 ∧
    Real.cos (2 * π * ((2 : ℕ) : ℝ) / ((5 : ℕ) : ℝ)) = (-1 - t5) / 2 ∧
    Real.sin (2 * π * ((2 : ℕ) : ℝ) / ((5 : ℕ) : ℝ)) = s5 * t5 ∧
    Real.cos (2 * π * ((3 : ℕ) : ℝ) / ((5 : ℕ) : ℝ)) = (-1 - t5) / 2 ∧
    Real.sin (2 * π * ((3 : ℕ) : ℝ) / ((5 : ℕ) : ℝ)) = -(s5 * t5) ∧
    Real.cos (2 * π * ((4 : ℕ) : ℝ) / ((5 : ℕ) : ℝ)) = t5 / 2 ∧
    Real.sin (2 * π * ((4 : ℕ) : ℝ) / ((5 : ℕ) : ℝ)) = -s5 := by
  have e1 : 2 * π * ((1 : ℕ) : ℝ) / ((5 : ℕ) : ℝ) = 2 * π / 5 := by push_cast; ring
  have e2 : 2 * π * ((2 : ℕ) : ℝ) / ((5 : ℕ) : ℝ) = 2 * (2 * π / 5) := by push_cast; ring
  have e3 : 2 * π * ((3 : ℕ) : ℝ) / ((5 : ℕ) : ℝ) = 2 * π - 2 * (2 * π / 5) := by push_cast; ring
  have e4 : 2 * π * ((4 : ℕ) : ℝ) / ((5 : ℕ) : ℝ) = 2 * π - 2 * π / 5 := by push_cast; ring
  have hc : Real.cos (2 * π / 5) = t5 / 2 := by unfold t5; ring
  have hc2 : Real.cos (2 * (2 * π / 5)) = (-1 - t5) / 2 := by
    rw [Real.cos_two_mul, hc]; linear_combination (1 / 2) * t5_sq
  have hs2 : Real.sin (2 * (2 * π / 5)) = s5 * t5 := by
    rw [Real.sin_two_mul, hc]; unfold s5; ring
  refine ⟨by rw [e1, hc], by rw [e1]; rfl, by rw [e2, hc2], by rw [e2, hs2], ?_, ?_, ?_, ?_⟩
  · rw [e3, Real.cos_two_pi_sub, hc2]
  · rw [e3, Real.sin_two_pi_sub, hs2]
  · rw [e4, Real.cos_two_pi_sub, hc]
  · rw [e4, Real.sin_two_pi_sub]; rfl

theorem cycPoint_five (w : List ℤ) : cycPoint 5 w = embT t5 s5 (lat5 w) := by
  obtain ⟨c1, s1, c2, s2, c3, s3, c4, s4⟩ := cos_sin_five
  simp only [cycPoint, unitRoot, Finset.sum_range_succ, Finset.sum_range_zero, zero_add]
  rw [c1, s1, c2, s2, c3, s3, c4, s4]
  funext i
  fin_cases i <;> simp [embT, lat5, evT] <;> ring

end LeanLB.G
