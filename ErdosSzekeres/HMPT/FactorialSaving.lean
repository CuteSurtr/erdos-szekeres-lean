import ErdosSzekeres.HMPT.BinomialRefinement

/-! A uniform strict improvement of the finite exponent criterion when its
counting term, rather than either auxiliary lower bound, is active.
This does not change the asymptotic leading coefficient. -/
namespace ErdosSzekeres.HMPT

theorem factorial_ge_two_pow_three_mul_sub {m : ℕ} (hm : 3 ≤ m) :
    2 ^ (3 * m - 6) ≤ (m + 1).factorial := by
  by_cases hlarge : 6 ≤ m
  · induction m, hlarge using Nat.le_induction with
    | base => norm_num
    | succ m hm ih =>
      have hexp : 3 * (m + 1) - 6 = (3 * m - 6) + 3 := by omega
      rw [hexp, pow_add, Nat.factorial_succ]
      calc
        2 ^ (3 * m - 6) * 2 ^ 3 = 8 * 2 ^ (3 * m - 6) := by ring
        _ ≤ (m + 1 + 1) * (m + 1).factorial :=
          Nat.mul_le_mul (by omega) (ih (by omega))
  · interval_cases m <;> norm_num

/-- The factorial credit covers at least one full denominator for every
admissible scale, not just for an isolated numerical example. -/
theorem factorial_log_ge_scale_denominator {m : ℕ} (hm : 3 ≤ m) :
    3 * m - 6 ≤ Nat.log 2 (m + 1).factorial :=
  Nat.le_log_of_pow_le (by decide) (factorial_ge_two_pow_three_mul_sub hm)

private theorem div_sub_lt_div {A F D : ℕ} (hD : 0 < D) (hF : D ≤ F)
    (hA : D ≤ A) : (A - F) / D < A / D := by
  apply (Nat.div_lt_iff_lt_mul hD).mpr
  rw [Nat.mul_comm (A / D) D]
  have hmod := Nat.mod_lt A hD
  have heq := Nat.mod_add_div A D
  have hq : 0 < A / D := Nat.div_pos hA hD
  have hmul : 0 < D * (A / D) := Nat.mul_pos hD hq
  omega

/-- Whenever the previous exponent strictly exceeds both auxiliary floors,
retaining the factorial makes its integer value strictly smaller. -/
theorem twoScaleFactorialExponent_lt_of_counting_dominates {m n d : ℕ}
    (hm : 3 ≤ m) (hd : d < twoScaleExponent m n d)
    (hK : 2 * (4 * m + 1) < twoScaleExponent m n d) :
    twoScaleFactorialExponent m n d < twoScaleExponent m n d := by
  let A := (d + 1) * (4 * m + 1) + Nat.clog 2 (twoScaleProduct m n)
  let F := Nat.log 2 (m + 1).factorial
  let D := 3 * m - 6
  have hD : 0 < D := by dsimp [D]; omega
  have hF : D ≤ F := factorial_log_ge_scale_denominator hm
  have hcount : twoScaleExponent m n d = A / D + 1 := by
    unfold twoScaleExponent at *
    dsimp [A, D]
    omega
  have hq : 0 < A / D := by rw [hcount] at hK; omega
  have hA : D ≤ A := by
    have heq := Nat.mod_add_div A D
    have hmul : D ≤ D * (A / D) := Nat.le_mul_of_pos_right D hq
    omega
  have hdiv := div_sub_lt_div hD hF hA
  unfold twoScaleFactorialExponent
  change max d (max (2 * (4 * m + 1)) ((A - F) / D + 1)) < _
  rw [hcount] at hd hK ⊢
  omega

/-- The auxiliary input exponent cannot be the active floor. -/
theorem self_lt_twoScaleExponent {m n d : ℕ} (hm : 3 ≤ m) :
    d < twoScaleExponent m n d := by
  have hD : 0 < 3 * m - 6 := by omega
  have hKD : 3 * m - 6 ≤ 4 * m + 1 := by omega
  have hq : d ≤ ((d + 1) * (4 * m + 1) +
      Nat.clog 2 (twoScaleProduct m n)) / (3 * m - 6) := by
    apply (Nat.le_div_iff_mul_le hD).mpr
    nlinarith
  unfold twoScaleExponent
  omega

/-- A simple one-floor condition suffices for a strict integer improvement. -/
theorem twoScaleFactorialExponent_lt {m n d : ℕ} (hm : 3 ≤ m)
    (hfloor : 2 * (4 * m + 1) < twoScaleExponent m n d) :
    twoScaleFactorialExponent m n d < twoScaleExponent m n d :=
  twoScaleFactorialExponent_lt_of_counting_dominates hm
    (self_lt_twoScaleExponent hm) hfloor

/-- Under the stated finite floor condition, the same auxiliary ES input forces
the target polygon with at most half the previous power-of-two threshold. -/
theorem integer_two_scale_bound_one_bit_smaller {m n d : ℕ}
    (hm : 3 ≤ m) (hn : 4 ≤ n) (hK : 4 * m + 1 ≤ 2 ^ d)
    (hforce : ForcesConvexNGon (2 ^ d) (4 * m + 1))
    (hfloor : 2 * (4 * m + 1) < twoScaleExponent m n d) :
    ForcesConvexNGon (2 ^ (twoScaleExponent m n d - 1)) n := by
  apply (integer_two_scale_factorial_bound hm hn hK hforce).mono
  apply Nat.pow_le_pow_right (by decide)
  have h := twoScaleFactorialExponent_lt hm hfloor
  omega

#print axioms factorial_ge_two_pow_three_mul_sub
#print axioms factorial_log_ge_scale_denominator
#print axioms twoScaleFactorialExponent_lt_of_counting_dominates
#print axioms self_lt_twoScaleExponent
#print axioms twoScaleFactorialExponent_lt
#print axioms integer_two_scale_bound_one_bit_smaller
end ErdosSzekeres.HMPT
