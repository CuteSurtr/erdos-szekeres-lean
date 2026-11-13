import ErdosSzekeres.Suk.FiniteBound

namespace ErdosSzekeres.Suk

/-- A coarse integer lower bound for binomial coefficients, convenient for
the density argument. No division or real-number rounding is involved. -/
theorem pow_le_scaled_choose (N L : ℕ) (hNL : 2 * L ≤ N) :
    N ^ L ≤ 2 ^ (L * L + L) * N.choose L := by
  have hbase : N ≤ 2 * (N + 1 - L) := by omega
  have hfac : L.factorial ≤ 2 ^ (L * L) := by
    calc
      L.factorial ≤ L ^ L := Nat.factorial_le_pow L
      _ ≤ (2 ^ L) ^ L := Nat.pow_le_pow_left (Nat.lt_pow_self (by decide)).le L
      _ = 2 ^ (L * L) := (pow_mul _ _ _).symm
  calc
    N ^ L ≤ (2 * (N + 1 - L)) ^ L := Nat.pow_le_pow_left hbase L
    _ = 2 ^ L * (N + 1 - L) ^ L := mul_pow _ _ _
    _ ≤ 2 ^ L * N.descFactorial L := Nat.mul_le_mul_left _ (Nat.pow_sub_le_descFactorial N L)
    _ = 2 ^ L * (L.factorial * N.choose L) := by rw [Nat.descFactorial_eq_factorial_mul_choose]
    _ ≤ 2 ^ L * (2 ^ (L * L) * N.choose L) :=
      Nat.mul_le_mul_left _ (Nat.mul_le_mul_right _ hfac)
    _ = 2 ^ (L * L + L) * N.choose L := by rw [pow_add]; ring

/-- A sufficient power inequality for the exact binomial density condition. -/
theorem density_condition_of_power {N L D : ℕ} (hNL : 2 * L ≤ N)
    (hpow : 2 ^ (3 * (L * L) + L + 1) * D < N ^ L) :
    2 * D * (4 ^ L).choose L < N.choose L := by
  have hlo := pow_le_scaled_choose N L hNL
  have hhi := Nat.choose_le_pow (4 ^ L) L
  have he : 2 ^ (L * L + L) * (2 * D * (4 ^ L) ^ L) =
      2 ^ (3 * (L * L) + L + 1) * D := by
    have h4 : (4 : ℕ) = 2 ^ 2 := by norm_num
    rw [h4, ← pow_mul, ← pow_mul]
    rw [show 3 * (L * L) + L + 1 = (L * L + L) + (2 * L * L) + 1 by ring,
      pow_add, pow_add]
    ring
  have h := (Nat.mul_le_mul_left (2 ^ (L * L + L))
    (Nat.mul_le_mul_left (2 * D) hhi)).trans_lt (he ▸ hpow)
  exact lt_of_mul_lt_mul_left (h.trans_le hlo) (Nat.zero_le _)

end ErdosSzekeres.Suk
