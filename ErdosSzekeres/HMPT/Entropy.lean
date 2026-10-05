import ErdosSzekeres.HMPT.TwoScale
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Log.Base

namespace ErdosSzekeres.HMPT

/-- A factorial-sensitive binomial bound. The absolute factor four is coarse
but its logarithm contributes only a lower-order term in the two-scale proof. -/
theorem choose_le_four_mul_pow {N A R : ℕ} (hN : N ≤ R * A) :
    N.choose A ≤ (4 * R) ^ A := by
  have hfac : (0 : ℝ) < A.factorial := by exact_mod_cast Nat.factorial_pos A
  have hpow : (A : ℝ) ^ A / A.factorial ≤ (Real.exp 1) ^ A := by
    have h := Real.pow_div_factorial_le_exp (A : ℝ) (Nat.cast_nonneg A) A
    simpa only [← Real.exp_nat_mul, mul_one] using h
  have hexp : Real.exp 1 ≤ 4 := by
    have h := Real.exp_one_lt_d9
    norm_num at h ⊢
    linarith
  have h : (N.choose A : ℝ) ≤ ((4 * R : ℕ) : ℝ) ^ A := by
    calc
      _ ≤ (N : ℝ) ^ A / A.factorial := Nat.choose_le_pow_div A N
      _ ≤ ((R : ℝ) * A) ^ A / A.factorial := by
        apply div_le_div_of_nonneg_right _ hfac.le
        exact pow_le_pow_left₀ (Nat.cast_nonneg N) (by exact_mod_cast hN) A
      _ = (R : ℝ) ^ A * ((A : ℝ) ^ A / A.factorial) := by rw [mul_pow]; ring
      _ ≤ (R : ℝ) ^ A * (Real.exp 1) ^ A := mul_le_mul_of_nonneg_left hpow (by positivity)
      _ ≤ (R : ℝ) ^ A * 4 ^ A :=
        mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (Real.exp_pos _).le hexp _) (by positivity)
      _ = _ := by push_cast; rw [mul_pow]; ring
  exact_mod_cast h

/-- An elementary logarithmic budget for one support product, with the leading
horizontal term (2n+r) log₂ r and explicit rounding constants. -/
def entropyExponent (r n : ℕ) : ℕ :=
  (r + 1) * (n - 1) + 2 * r +
    (2 * (n - 1) + r) * Nat.clog 2 (4 * (r + 1))

theorem supportProductBound_le_entropy (r n : ℕ) :
    supportProductBound r n ≤ 2 ^ entropyExponent r n := by
  have hN : 2 * (n - 1) + r + r * (n - 2) ≤ (r + 1) * (2 * (n - 1) + r) := by
    have h : n - 2 ≤ 2 * (n - 1) + r := by omega
    nlinarith [Nat.mul_le_mul_left r h]
  have hc := choose_le_four_mul_pow hN
  have hp : (4 * (r + 1)) ^ (2 * (n - 1) + r) ≤
      2 ^ ((2 * (n - 1) + r) * Nat.clog 2 (4 * (r + 1))) := by
    calc
      _ ≤ (2 ^ Nat.clog 2 (4 * (r + 1))) ^ (2 * (n - 1) + r) :=
        Nat.pow_le_pow_left (Nat.le_pow_clog (by decide) _) _
      _ = _ := by rw [← pow_mul, Nat.mul_comm]
  unfold supportProductBound entropyExponent
  rw [pow_add 2 ((r + 1) * (n - 1) + 2 * r)]
  exact Nat.mul_le_mul_left _ (hc.trans hp)

theorem twoScaleProduct_le_entropy (m n : ℕ) :
    twoScaleProduct m n ≤ 2 ^ (entropyExponent (m - 3) n + entropyExponent (2 * m - 3) n) := by
  rw [pow_add]
  exact Nat.mul_le_mul (supportProductBound_le_entropy _ _) (supportProductBound_le_entropy _ _)

/-- A common logarithm for both scales, keeping all lower-order losses explicit. -/
theorem twoScaleProduct_le_common_entropy {m : ℕ} (hm : 3 ≤ m) (n : ℕ) :
    twoScaleProduct m n ≤ 2 ^ (3 * m * n + 6 * m +
      (4 * n + 3 * m) * Nat.clog 2 (8 * m)) := by
  apply (twoScaleProduct_le_entropy m n).trans
  apply Nat.pow_le_pow_right (by decide)
  have h₁ := Nat.clog_mono_right 2 (show 4 * (m - 3 + 1) ≤ 8 * m by omega)
  have h₂ := Nat.clog_mono_right 2 (show 4 * (2 * m - 3 + 1) ≤ 8 * m by omega)
  unfold entropyExponent
  have h₃ : m - 3 + 3 = m := by omega
  have h₄ : 2 * m - 3 + 3 = 2 * m := by omega
  have h₅ : n - 1 ≤ n := Nat.sub_le _ _
  have hp₁ := Nat.mul_le_mul_left (2 * (n - 1) + (m - 3)) h₁
  have hp₂ := Nat.mul_le_mul_left (2 * (n - 1) + (2 * m - 3)) h₂
  have hp₃ := Nat.mul_le_mul_left (3 * m) h₅
  have hp₄ := Nat.mul_le_mul_right (Nat.clog 2 (8 * m)) h₅
  nlinarith [Nat.zero_le (Nat.clog 2 (8 * m)), Nat.zero_le (n - 1)]

/-- The elementary two-scale criterion with no binomial coefficient left to
estimate. It is a consequence of the complete geometric argument. -/
theorem entropy_two_scale_bound {m n d E : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hforce : ForcesConvexNGon (2 ^ d) (4 * m + 1))
    (hK : 4 * m + 1 ≤ 2 ^ d) (hdE : d ≤ E) (hE : 2 * (4 * m + 1) ≤ E)
    (hbudget : (d + 1) * (4 * m + 1) + 3 * m * n + 6 * m +
      (4 * n + 3 * m) * Nat.clog 2 (8 * m) < (3 * m - 6) * E) :
    ForcesConvexNGon (2 ^ E) n := by
  apply two_scale_exponential_bound hm hn hforce hK hdE hE
    (twoScaleProduct_le_common_entropy hm n)
  simpa only [Nat.add_assoc] using hbudget

/-- The common integer logarithm is within four of log₂ m. -/
theorem common_clog_le_logb {m : ℕ} (hm : 1 ≤ m) :
    (Nat.clog 2 (8 * m) : ℝ) ≤ Real.logb 2 m + 4 := by
  have hmpos : (0 : ℝ) < m := by exact_mod_cast (show 0 < m by omega)
  have hlog : 0 ≤ Real.logb 2 (8 * m : ℕ) :=
    Real.logb_nonneg (by norm_num) (by exact_mod_cast (show 1 ≤ 8 * m by omega))
  have hceil := (Nat.ceil_lt_add_one hlog).le
  have hceil_eq : ⌈Real.logb 2 (8 * m : ℕ)⌉₊ = Nat.clog 2 (8 * m) := by
    simpa only [Nat.cast_ofNat] using Real.natCeil_logb_natCast 2 (8 * m)
  rw [hceil_eq] at hceil
  have h8 : Real.logb 2 8 = 3 := by
    have h := Real.logb_pow (2 : ℝ) (2 : ℝ) 3
    norm_num [Real.logb_self_eq_one (by norm_num : (1 : ℝ) < 2)] at h
    exact h
  have he : Real.logb 2 (8 * m : ℕ) = 3 + Real.logb 2 m := by
    push_cast
    rw [Real.logb_mul (by norm_num : (8 : ℝ) ≠ 0) hmpos.ne', h8]
  rw [he] at hceil
  linarith

/-- A closed integer exponent with the main term n separated from the error. -/
def twoScaleEntropyExponent (m n d : ℕ) : ℕ :=
  max d (max (2 * (4 * m + 1))
    (n + ((d + 1) * (4 * m + 1) + 6 * n + 6 * m +
      (4 * n + 3 * m) * Nat.clog 2 (8 * m)) / (3 * m - 6) + 1))

theorem integer_entropy_two_scale_bound {m n d : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hK : 4 * m + 1 ≤ 2 ^ d) (hforce : ForcesConvexNGon (2 ^ d) (4 * m + 1)) :
    ForcesConvexNGon (2 ^ twoScaleEntropyExponent m n d) n := by
  apply entropy_two_scale_bound hm hn hforce hK (le_max_left _ _)
    ((le_max_left _ _).trans (le_max_right _ _))
  let A := (d + 1) * (4 * m + 1) + 6 * n + 6 * m +
    (4 * n + 3 * m) * Nat.clog 2 (8 * m)
  have hrem := Nat.mod_lt A (by omega : 0 < 3 * m - 6)
  have he := Nat.mod_add_div A (3 * m - 6)
  have hlt : A < (3 * m - 6) * (A / (3 * m - 6) + 1) := by nlinarith
  have hsub : 3 * m - 6 + 6 = 3 * m := by omega
  have hlow : n + A / (3 * m - 6) + 1 ≤ twoScaleEntropyExponent m n d :=
    (le_max_right _ _).trans (le_max_right _ _)
  have hmul := Nat.mul_le_mul_left (3 * m - 6) hlow
  dsimp [A] at hlt
  dsimp [A, twoScaleEntropyExponent] at hmul
  nlinarith

/-- A binomial-free theorem using the fully proved finite Suk input. -/
theorem suk_entropy_two_scale_bound {m n a : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (ha : 2 ≤ a) (hKa : 4 * m + 1 ≤ a ^ 3) :
    ForcesConvexNGon (2 ^ twoScaleEntropyExponent m n
      ((4 * m + 1) + a ^ 2 + Nat.clog 2 ((4 * m + 1) + a ^ 2) * a ^ 2 +
        64 * (a * (a + 1) + 5))) n := by
  apply integer_entropy_two_scale_bound hm hn
  · exact (show 4 * m + 1 ≤
      ((4 * m + 1) + a ^ 2 + Nat.clog 2 ((4 * m + 1) + a ^ 2) * a ^ 2 +
        64 * (a * (a + 1) + 5)) by omega).trans
      (Nat.lt_pow_self (a := 2) (by decide)).le
  · exact Suk.cubic_log_bound (by omega) ha hKa

/-- Transfer a real exponent budget to the exact natural-floor convention in
the target theorem. The unit slack absorbs the exponent's integer rounding. -/
theorem real_entropy_two_scale_bound {m n d : ℕ} {X : ℝ}
    (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hforce : ForcesConvexNGon (2 ^ d) (4 * m + 1)) (hK : 4 * m + 1 ≤ 2 ^ d)
    (hd : (d : ℝ) + 1 ≤ X) (hsize : 2 * (4 * (m : ℝ) + 1) + 1 ≤ X)
    (hbudget : ((d : ℝ) + 1) * (4 * (m : ℝ) + 1) + 3 * m * n + 6 * m +
      (4 * (n : ℝ) + 3 * m) * (Real.logb 2 m + 4) <
        (3 * (m : ℝ) - 6) * (X - 1)) :
    ForcesConvexNGon ⌊(2 : ℝ) ^ X⌋₊ n := by
  let E := ⌊X⌋₊
  have hfloor : X - 1 ≤ (E : ℝ) := (Nat.sub_one_lt_floor X).le
  have hdE : d ≤ E := by exact_mod_cast (show (d : ℝ) ≤ E by linarith)
  have hE : 2 * (4 * m + 1) ≤ E := by
    exact_mod_cast (show 2 * (4 * (m : ℝ) + 1) ≤ E by linarith)
  have hsub : ((3 * m - 6 : ℕ) : ℝ) = 3 * (m : ℝ) - 6 := by
    rw [Nat.cast_sub (by omega : 6 ≤ 3 * m)]
    push_cast
    rfl
  have hlog := common_clog_le_logb (show 1 ≤ m by omega)
  have hmul := mul_le_mul_of_nonneg_left hlog (show 0 ≤ 4 * (n : ℝ) + 3 * m by positivity)
  have hfloor' := mul_le_mul_of_nonneg_left hfloor (show 0 ≤ 3 * (m : ℝ) - 6 by
    have : (3 : ℝ) ≤ m := by exact_mod_cast hm
    linarith)
  have hbudgetE : (d + 1) * (4 * m + 1) + 3 * m * n + 6 * m +
      (4 * n + 3 * m) * Nat.clog 2 (8 * m) < (3 * m - 6) * E := by
    apply (Nat.cast_lt (α := ℝ)).mp
    push_cast
    rw [hsub]
    linarith
  apply (entropy_two_scale_bound hm hn hforce hK hdE hE hbudgetE).mono
  apply (Nat.le_floor_iff (by positivity)).mpr
  have hX : 0 ≤ X := le_trans (by positivity : 0 ≤ (d : ℝ) + 1) hd
  have hp := Real.rpow_le_rpow_of_exponent_le (by norm_num : (1 : ℝ) ≤ 2) (Nat.floor_le hX)
  simpa only [E, Real.rpow_natCast, Nat.cast_pow, Nat.cast_ofNat] using hp

end ErdosSzekeres.HMPT
