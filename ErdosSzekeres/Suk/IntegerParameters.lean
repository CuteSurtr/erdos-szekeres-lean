import ErdosSzekeres.Suk.ExponentialBound
import Mathlib.Data.Nat.Log

namespace ErdosSzekeres.Suk

/-- Bounding the antichain binomial using the smaller complementary index
keeps its exponent proportional to b, rather than n. -/
theorem spike_budget_le_power {n K b H : ℕ} (hn : 4 ≤ n) (hb : 3 ≤ b)
    (hH : n + b ≤ 2 ^ H) :
    2 ^ (n + K - 4) * (n + b - 4).choose (n - 2) ≤ 2 ^ (n + K + H * b) := by
  have hc : (n + b - 4).choose (n - 2) ≤ 2 ^ (H * b) := by
    rw [← Nat.choose_symm (show n - 2 ≤ n + b - 4 by omega),
      show n + b - 4 - (n - 2) = b - 2 by omega]
    calc
      _ ≤ (n + b - 4) ^ (b - 2) := Nat.choose_le_pow _ _
      _ ≤ (2 ^ H) ^ (b - 2) := Nat.pow_le_pow_left (by omega) _
      _ ≤ (2 ^ H) ^ b := Nat.pow_le_pow_right (Nat.one_le_pow _ _ (by decide)) (by omega)
      _ = 2 ^ (H * b) := (pow_mul _ _ _).symm
  calc
    _ ≤ 2 ^ (n + K) * 2 ^ (H * b) :=
      Nat.mul_le_mul (Nat.pow_le_pow_right (by decide) (Nat.sub_le _ _)) hc
    _ = _ := (pow_add _ _ _).symm

/-- A finite bound with a freely chosen integer logarithm upper bound. -/
theorem finite_logarithmic_bound {k n K r t b H : ℕ}
    (hn : 4 ≤ n) (hK : 3 ≤ K) (hb : 3 ≤ b)
    (hchainreach : n ≤ r * K) (hantireach : n ≤ t * b) (hregions : t * (r + 1) ≤ k)
    (hH : n + b ≤ 2 ^ H) :
    ForcesConvexNGon (2 ^ (n + K + H * b + 64 * (k + 5))) n :=
  finite_exponential_bound hn hK hb hchainreach hantireach hregions
    (spike_budget_le_power hn hb hH)

/-- Cubic parameter choice for Suk's asymptotic argument. Any integer a with
n ≤ a^3 works; H only needs to bound log₂(n+a²) from above. -/
theorem cubic_parameter_bound {n a H : ℕ} (hn : 4 ≤ n) (ha : 2 ≤ a)
    (hna : n ≤ a ^ 3) (hH : n + a ^ 2 ≤ 2 ^ H) :
    ForcesConvexNGon (2 ^ (n + a ^ 2 + H * a ^ 2 + 64 * (a * (a + 1) + 5))) n := by
  apply finite_logarithmic_bound (r := a) (t := a) hn (by nlinarith) (by nlinarith)
    (by simpa only [pow_succ, pow_zero, one_mul, mul_assoc] using hna)
    (by simpa only [pow_succ, pow_zero, one_mul, mul_assoc] using hna) (by rfl) hH

/-- A closed integer bound, ready for comparison with Suk's real exponent. -/
theorem cubic_log_bound {n a : ℕ} (hn : 4 ≤ n) (ha : 2 ≤ a) (hna : n ≤ a ^ 3) :
    ForcesConvexNGon
      (2 ^ (n + a ^ 2 + Nat.clog 2 (n + a ^ 2) * a ^ 2 + 64 * (a * (a + 1) + 5))) n :=
  cubic_parameter_bound hn ha hna (Nat.le_pow_clog (by decide) _)

end ErdosSzekeres.Suk
