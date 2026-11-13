import ErdosSzekeres.Suk.ExtractionEstimates

namespace ErdosSzekeres.Suk

/-- The extraction loss is linear in the number of retained support regions.
The constant is deliberately coarse; all endpoint and counting losses are included. -/
theorem exponential_density_condition (k E B : ℕ) (hB : B ≤ 2 ^ E) :
    2 * extractionThreshold (2 ^ (E + 64 * (k + 5))) (2 * k + 4) k B *
      (4 ^ (2 * (2 * k + 4 + 3))).choose (2 * (2 * k + 4 + 3)) <
        (2 ^ (E + 64 * (k + 5))).choose (2 * (2 * k + 4 + 3)) := by
  let C := 64 * (k + 5)
  let L := 2 * (2 * k + 4 + 3)
  have hL : 2 * L ≤ E + C := by dsimp [L, C]; omega
  apply density_condition_of_power
  · exact hL.trans (Nat.lt_pow_self (by decide)).le
  · have hD : extractionThreshold (2 ^ (E + C)) (2 * k + 4) k B ≤
        2 ^ ((E + C) * (3 * k + 12) + E * (k + 2)) := by
      calc
        _ ≤ extractionThreshold (2 ^ (E + C)) (2 * k + 4) k (2 ^ E) := by
          unfold extractionThreshold
          gcongr
        _ = _ := by
          unfold extractionThreshold
          rw [show 2 * k + 4 - k - 2 = k + 2 by omega]
          rw [← pow_mul, ← pow_mul, ← pow_mul, ← pow_mul]
          rw [← pow_add, ← pow_add, ← pow_add]
          exact congrArg (fun j : ℕ => (2 : ℕ) ^ j) (by ring)
    have he : 3 * (L * L) + L + 1 +
        ((E + C) * (3 * k + 12) + E * (k + 2)) < (E + C) * L := by
      dsimp [L, C]
      nlinarith [Nat.zero_le (k * k)]
    calc
      _ ≤ 2 ^ (3 * (L * L) + L + 1) *
          2 ^ ((E + C) * (3 * k + 12) + E * (k + 2)) := Nat.mul_le_mul_left _ hD
      _ = 2 ^ (3 * (L * L) + L + 1 +
          ((E + C) * (3 * k + 12) + E * (k + 2))) := (pow_add _ _ _).symm
      _ < 2 ^ ((E + C) * L) := Nat.pow_lt_pow_right (by decide) he
      _ = _ := pow_mul _ _ _

/-- An explicit exponential bound, derived from the complete finite geometric
proof. Parameter choices and the final asymptotic estimates remain separate. -/
theorem finite_exponential_bound {k n K r t b E : ℕ}
    (hn : 4 ≤ n) (hK : 3 ≤ K) (hb : 3 ≤ b)
    (hchainreach : n ≤ r * K) (hantireach : n ≤ t * b) (hregions : t * (r + 1) ≤ k)
    (hB : 2 ^ (n + K - 4) * (n + b - 4).choose (n - 2) ≤ 2 ^ E) :
    ForcesConvexNGon (2 ^ (E + 64 * (k + 5))) n := by
  apply finite_density_bound (m := 2 * k + 4) (k := k) (by omega)
    hn hK hb hchainreach hantireach hregions
  · have h4 : (4 : ℕ) = 2 ^ 2 := by norm_num
    rw [h4, ← pow_mul]
    exact Nat.pow_le_pow_right (by decide) (by omega)
  · exact exponential_density_condition k E _ hB

end ErdosSzekeres.Suk
