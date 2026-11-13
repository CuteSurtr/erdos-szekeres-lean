import ErdosSzekeres.Suk.IntegerParameters
import ErdosSzekeres.Suk.Statement
import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics
import Mathlib.Algebra.Order.Floor.Semiring

namespace ErdosSzekeres.Suk

/-- Round the cube-root parameter and logarithm, retaining enough slack for
the explicit extraction loss. -/
theorem integer_parameters_fit_exponent (n : ℕ) (hn : 4 ≤ n)
    (hx : 4 ≤ (n : ℝ) ^ ((1 : ℝ) / 3)) (hl : 100 ≤ Real.logb 2 n) :
    ∃ a H : ℕ, 2 ≤ a ∧ n ≤ a ^ 3 ∧ n + a ^ 2 ≤ 2 ^ H ∧
      ((n + a ^ 2 + H * a ^ 2 + 64 * (a * (a + 1) + 5) : ℕ) : ℝ) ≤ exponent 6 n := by
  let x := (n : ℝ) ^ ((1 : ℝ) / 3)
  let a := ⌈x⌉₊
  let H := Nat.clog 2 (n + a ^ 2)
  have hx0 : 0 ≤ x := by dsimp [x]; positivity
  have hxa : x ≤ (a : ℝ) := Nat.le_ceil x
  have hax : (a : ℝ) ≤ x + 1 := (Nat.ceil_lt_add_one hx0).le
  have ha4 : 4 ≤ a := by exact_mod_cast (hx.trans hxa)
  have hcube : x ^ 3 = (n : ℝ) := by
    dsimp [x]
    rw [← Real.rpow_mul_natCast (Nat.cast_nonneg n)]
    norm_num
  have hsquare : x ^ 2 = (n : ℝ) ^ ((2 : ℝ) / 3) := by
    dsimp [x]
    rw [← Real.rpow_mul_natCast (Nat.cast_nonneg n)]
    norm_num
  have hna : n ≤ a ^ 3 := by
    have h := pow_le_pow_left₀ hx0 hxa 3
    rw [hcube] at h
    exact_mod_cast h
  have ha2 : (a : ℝ) ^ 2 ≤ 2 * x ^ 2 := by
    have h := pow_le_pow_left₀ (Nat.cast_nonneg a) hax 2
    nlinarith [sq_nonneg (x - 2)]
  have hbn : (a : ℝ) ^ 2 ≤ n := by
    have h := mul_nonneg (show 0 ≤ x - 2 by linarith) (sq_nonneg x)
    nlinarith [hcube]
  have hnp : (0 : ℝ) < n := by exact_mod_cast (show 0 < n by omega)
  have hlog : Real.logb 2 (n + a ^ 2 : ℕ) ≤ Real.logb 2 n + 1 := by
    have h := Real.logb_le_logb_of_le (by norm_num : (1 : ℝ) < 2)
      (show (0 : ℝ) < (n + a ^ 2 : ℕ) by exact_mod_cast (show 0 < n + a ^ 2 by omega))
      (show ((n + a ^ 2 : ℕ) : ℝ) ≤ 2 * n by push_cast; linarith)
    rw [Real.logb_mul (by norm_num : (2 : ℝ) ≠ 0) hnp.ne',
      Real.logb_self_eq_one (by norm_num : (1 : ℝ) < 2)] at h
    linarith
  have hH : (H : ℝ) ≤ Real.logb 2 n + 2 := by
    have hnonneg : 0 ≤ Real.logb 2 (n + a ^ 2 : ℕ) :=
      Real.logb_nonneg (by norm_num) (by exact_mod_cast (show 1 ≤ n + a ^ 2 by omega))
    have hceil := Nat.ceil_lt_add_one hnonneg
    have hceil_eq : ⌈Real.logb 2 (n + a ^ 2 : ℕ)⌉₊ = H := by
      simpa only [Nat.cast_ofNat] using Real.natCeil_logb_natCast 2 (n + a ^ 2)
    rw [hceil_eq] at hceil
    dsimp [H]
    linarith
  have hak : (a : ℝ) * (a + 1) + 5 ≤ 3 * (a : ℝ) ^ 2 := by
    have har : (4 : ℝ) ≤ a := by exact_mod_cast ha4
    nlinarith [sq_nonneg (a : ℝ)]
  refine ⟨a, H, by omega, hna, Nat.le_pow_clog (by decide) _, ?_⟩
  push_cast
  unfold exponent
  rw [← hsquare]
  have h₁ := mul_le_mul_of_nonneg_right hH (sq_nonneg (a : ℝ))
  have h₂ := mul_le_mul_of_nonneg_left ha2
    (show 0 ≤ Real.logb 2 n + 195 by linarith)
  have h₃ := mul_nonneg (show 0 ≤ 4 * Real.logb 2 n - 390 by linarith) (sq_nonneg x)
  nlinarith

/-- The integer bound lies below Suk's exact natural-floor threshold once
the cube root and logarithm satisfy the displayed elementary cutoffs. -/
theorem coefficient_six_bound (n : ℕ) (hn : 4 ≤ n)
    (hx : 4 ≤ (n : ℝ) ^ ((1 : ℝ) / 3)) (hl : 100 ≤ Real.logb 2 n) :
    ForcesConvexNGon (threshold 6 n) n := by
  obtain ⟨a, H, ha, hna, hH, he⟩ := integer_parameters_fit_exponent n hn hx hl
  apply (cubic_parameter_bound hn ha hna hH).mono
  unfold threshold
  apply (Nat.le_floor_iff (by positivity)).mpr
  have hp := Real.rpow_le_rpow_of_exponent_le (by norm_num : (1 : ℝ) ≤ 2) he
  simpa only [Real.rpow_natCast, Nat.cast_pow, Nat.cast_ofNat] using hp

/-- Suk's 2016 eventual upper bound, with coefficient 6 and the paper's
floor convention, for arbitrary real point sets in general position. -/
theorem theorem2016 : Theorem2016 := by
  have hroot : Filter.Tendsto (fun n : ℕ => (n : ℝ) ^ ((1 : ℝ) / 3))
      Filter.atTop Filter.atTop :=
    (tendsto_rpow_atTop (by norm_num : (0 : ℝ) < 1 / 3)).comp
      tendsto_natCast_atTop_atTop
  have hlog : Filter.Tendsto (fun n : ℕ => Real.logb 2 n)
      Filter.atTop Filter.atTop :=
    (Real.tendsto_logb_atTop (by norm_num : (1 : ℝ) < 2)).comp
      tendsto_natCast_atTop_atTop
  have hevent : ∀ᶠ n : ℕ in Filter.atTop, ForcesConvexNGon (threshold 6 n) n := by
    filter_upwards [Filter.eventually_ge_atTop 4, hroot.eventually_ge_atTop 4,
      hlog.eventually_ge_atTop 100] with n hn hx hl
    exact coefficient_six_bound n hn hx hl
  obtain ⟨n₀, h₀⟩ := Filter.eventually_atTop.mp hevent
  refine ⟨max n₀ 4, by omega, ?_⟩
  intro n hn
  exact h₀ n (by omega)

end ErdosSzekeres.Suk
