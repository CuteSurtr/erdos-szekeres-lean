import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.IntervalCases
import Mathlib.Tactic.Positivity

/-!
A model of repeated doubling in convex-subset counting. This is an arithmetic
model only: geometric counting estimates and asymptotic error terms are NOT
assumed as axioms and are NOT formalized here.
-/
namespace ErdosSzekeres.DyadicModel

/-- Sum lower bounds on successive increments over t doublings. -/
theorem telescope (f : ℕ → ℝ) (C x : ℝ) (t : ℕ)
    (hstep : ∀ i < t, C * x * 2 ^ i - 1 ≤ f (i + 1) - f i) :
    f 0 + C * x * (2 ^ t - 1) - t ≤ f t := by
  induction t with
  | zero => simp
  | succ t ih =>
      have hp := ih (fun i hi => hstep i (Nat.lt_trans hi (Nat.lt_succ_self t)))
      have hs := hstep t (Nat.lt_succ_self t)
      push_cast
      rw [pow_succ]
      nlinarith

/-- Explicit endpoint hypotheses expose exactly what the model uses. -/
theorem endpoint_constraint (f : ℕ → ℝ) (C x : ℝ) (t : ℕ)
    (hzero : 0 ≤ f 0)
    (hstep : ∀ i < t, C * x * 2 ^ i - 1 ≤ f (i + 1) - f i)
    (hend : f t ≤ (2 ^ t * x) ^ 2) :
    C * x * (2 ^ t - 1) ≤ (2 ^ t * x) ^ 2 + t := by
  have h := telescope f C x t hstep
  linarith

/-- The optimized squared coefficient in the endpoint model is
`4 * 4^t * t / (2^t - 1)^2`. Its minimum for integer t >= 1 is 128/9,
attained at t = 2. Stated with cleared denominators for exact arithmetic.
This does not assert an obstruction to other proof strategies. -/
theorem two_scales_optimal (t : ℕ) (ht : 1 ≤ t) :
    128 * (2 ^ t - 1) ^ 2 ≤ 36 * 4 ^ t * t := by
  by_cases hsmall : t < 4
  · interval_cases t <;> norm_num at *
  · have hfour : 4 ≤ t := by omega
    have hp : (2 ^ t - 1) ^ 2 ≤ (2 ^ t) ^ 2 :=
      Nat.pow_le_pow_left (Nat.sub_le _ _) 2
    have heq : (2 ^ t) ^ 2 = 4 ^ t := by
      rw [← pow_mul, Nat.mul_comm t 2, pow_mul]
      norm_num
    rw [heq] at hp
    calc
      128 * (2 ^ t - 1) ^ 2 ≤ 128 * 4 ^ t := Nat.mul_le_mul_left _ hp
      _ ≤ 36 * 4 ^ t * t := by nlinarith

theorem two_scales_equality :
    128 * (2 ^ (2 : ℕ) - 1) ^ 2 = 36 * 4 ^ (2 : ℕ) * 2 := by norm_num

end ErdosSzekeres.DyadicModel
