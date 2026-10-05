import ErdosSzekeres.HMPT.FiniteBound
import Mathlib.Data.Nat.Log

namespace ErdosSzekeres.HMPT

/-- Cancel the same factorial on both sides of the density comparison, instead
of paying a separate factorial bound. This keeps the extraction loss quadratic
with its original leading coefficient. -/
theorem density_condition_of_scaled_power {N M L D : ℕ} (hNL : 2 * L ≤ N)
    (hpow : 2 * D * (2 * M) ^ L < N ^ L) :
    2 * D * M.choose L < N.choose L := by
  have hlo : N ^ L ≤ 2 ^ L * (L.factorial * N.choose L) := by
    calc
      _ ≤ (2 * (N + 1 - L)) ^ L := Nat.pow_le_pow_left (by omega) L
      _ = 2 ^ L * (N + 1 - L) ^ L := mul_pow _ _ _
      _ ≤ 2 ^ L * N.descFactorial L := Nat.mul_le_mul_left _ (Nat.pow_sub_le_descFactorial N L)
      _ = _ := by rw [Nat.descFactorial_eq_factorial_mul_choose]
  have hhi : L.factorial * M.choose L ≤ M ^ L := by
    rw [← Nat.descFactorial_eq_factorial_mul_choose]
    exact Nat.descFactorial_le_pow _ _
  have h : (2 ^ L * L.factorial) * (2 * D * M.choose L) <
      (2 ^ L * L.factorial) * N.choose L := by
    calc
      _ = 2 ^ L * (2 * D * (L.factorial * M.choose L)) := by ring
      _ ≤ 2 ^ L * (2 * D * M ^ L) := Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ hhi)
      _ = 2 * D * (2 * M) ^ L := by rw [mul_pow]; ring
      _ < N ^ L := hpow
      _ ≤ 2 ^ L * (L.factorial * N.choose L) := hlo
      _ = _ := by ring
  exact lt_of_mul_lt_mul_left h (Nat.zero_le _)

theorem density_condition_of_power {N L D : ℕ} (hNL : 2 * L ≤ N)
    (hpow : 2 ^ (2 * (L * L) + L + 1) * D < N ^ L) :
    2 * D * (4 ^ L).choose L < N.choose L := by
  apply density_condition_of_scaled_power hNL
  have h4 : (4 : ℕ) = 2 ^ 2 := by norm_num
  have he : 2 * D * (2 * 4 ^ L) ^ L = 2 ^ (2 * (L * L) + L + 1) * D := by
    rw [mul_pow, h4, ← pow_mul, ← pow_mul,
      show 2 * (L * L) + L + 1 = (2 * L * L) + L + 1 by ring,
      pow_add, pow_add]
    ring
  rwa [he]

/-- A sufficient exponent budget for the fully geometric product theorem. -/
theorem exponential_product_bound {E V r n : ℕ} (hn : 4 ≤ n)
    (hV : supportProductBound r n ≤ 2 ^ V) (hE : 4 * (r + 3) ≤ E)
    (hbudget : 2 * ((2 * (r + 3)) * (2 * (r + 3))) + 2 * (r + 3) + 1 + V < r * E) :
    ForcesConvexNGon (2 ^ E) n := by
  let L := 2 * (r + 3)
  apply finite_product_bound (r := r) hn
  · have h4 : (4 : ℕ) = 2 ^ 2 := by norm_num
    rw [h4, ← pow_mul]
    exact Nat.pow_le_pow_right (by decide) (by omega)
  · apply density_condition_of_power
    · have hpow : E ≤ 2 ^ E := (Nat.lt_pow_self (n := E) (a := 2) (by decide)).le
      exact le_trans (by omega) hpow
    · have hD : productThreshold (2 ^ E) r n ≤ 2 ^ (E * (r + 6) + V) := by
        calc
          _ ≤ (2 ^ E) ^ (r + 3) * ((2 ^ E) ^ 3 * 2 ^ V) := by
            unfold productThreshold
            exact Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ hV)
          _ = _ := by
            rw [← pow_mul, ← pow_mul, ← pow_add, ← pow_add]
            exact congrArg (fun j : ℕ => (2 : ℕ) ^ j) (by ring)
      have he : 2 * (L * L) + L + 1 + (E * (r + 6) + V) < E * L := by
        dsimp [L]
        nlinarith
      calc
        _ ≤ 2 ^ (2 * (L * L) + L + 1) * 2 ^ (E * (r + 6) + V) := Nat.mul_le_mul_left _ hD
        _ = 2 ^ (2 * (L * L) + L + 1 + (E * (r + 6) + V)) := (pow_add _ _ _).symm
        _ < 2 ^ (E * L) := Nat.pow_lt_pow_right (by decide) he
        _ = _ := pow_mul _ _ _

/-- A closed computable exponent. The parameter `r` can be searched using
integer arithmetic; the theorem covers every positive choice, not just samples. -/
def productExponent (r n : ℕ) : ℕ :=
  max (4 * (r + 3))
    ((2 * ((2 * (r + 3)) * (2 * (r + 3))) + 2 * (r + 3) + 1 +
      Nat.clog 2 (supportProductBound r n)) / r + 1)

theorem integer_product_bound {r n : ℕ} (hn : 4 ≤ n) (hr : 1 ≤ r) :
    ForcesConvexNGon (2 ^ productExponent r n) n := by
  apply exponential_product_bound hn (Nat.le_pow_clog (by decide) _)
    (le_max_left _ _)
  have hlt (a : ℕ) : a < r * (a / r + 1) := by
    have hrem := Nat.mod_lt a (by omega : 0 < r)
    have he := Nat.mod_add_div a r
    nlinarith
  exact (hlt _).trans_le (Nat.mul_le_mul_left _ (le_max_right _ _))

end ErdosSzekeres.HMPT
