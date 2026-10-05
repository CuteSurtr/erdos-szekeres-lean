import ErdosSzekeres.HMPT.ConvexCounting
import ErdosSzekeres.HMPT.ExponentialBound
import ErdosSzekeres.Suk.IntegerParameters

namespace ErdosSzekeres.HMPT

open Suk

/-- Bootstrap any verified convex-polygon bound through the geometric product
method. The counting family consists of general convex subsets, not cups/caps. -/
theorem bootstrap_product_bound {N M r n : ℕ} (hn : 4 ≤ n)
    (hKM : 2 * (r + 3) + 1 ≤ M) (hMN : M ≤ N)
    (hforce : ForcesConvexNGon M (2 * (r + 3) + 1))
    (hsize : N * productThreshold N r n * M.choose (2 * (r + 3) + 1) <
      N.choose (2 * (r + 3) + 1)) : ForcesConvexNGon N n := by
  classical
  apply (forcesConvexNGon_iff_exact N n).mpr
  intro S hgp hcard
  obtain ⟨e, hgpT, hxT⟩ := exists_horizontal_image S hgp
  let T := S.image e
  have hTcard : T.card = N := by
    simpa only [T, Finset.card_image_of_injective S e.injective] using hcard
  by_contra havoid
  have havoidT : ¬ HasConvexNGon n T := by
    intro h
    have hback := h.linearEquiv e.symm
    exact havoid (by simpa [T, Finset.image_image, Function.comp_def] using hback)
  have hcount := convex_subsets_density T (2 * (r + 3) + 1) M hKM
    (by simpa only [hTcard] using hMN) hgpT hforce
  have hbound := convex_family_bound (r := r) T hn hgpT hxT havoidT
  have h := hcount.trans (Nat.mul_le_mul_right _ hbound)
  rw [hTcard] at h
  exact (not_lt_of_ge h) hsize

/-- A power-budget form of the bootstrap theorem, retaining the arbitrary
verified input exponent `d`. -/
theorem bootstrap_exponential_bound {r n d E V : ℕ} (hn : 4 ≤ n)
    (hforce : ForcesConvexNGon (2 ^ d) (2 * (r + 3) + 1))
    (hK : 2 * (r + 3) + 1 ≤ 2 ^ d) (hdE : d ≤ E)
    (hE : 2 * (2 * (r + 3) + 1) ≤ E)
    (hV : supportProductBound r n ≤ 2 ^ V)
    (hbudget : (d + 1) * (2 * (r + 3) + 1) + V < r * E) :
    ForcesConvexNGon (2 ^ E) n := by
  let K := 2 * (r + 3) + 1
  apply bootstrap_product_bound hn hK (Nat.pow_le_pow_right (by decide) hdE) hforce
  apply binomial_ratio_lt_of_scaled_power
  · exact hE.trans (Nat.lt_pow_self (n := E) (a := 2) (by decide)).le
  · have hD : 2 ^ E * productThreshold (2 ^ E) r n ≤ 2 ^ (E * (r + 7) + V) := by
      calc
        _ ≤ 2 ^ E * ((2 ^ E) ^ (r + 3) * ((2 ^ E) ^ 3 * 2 ^ V)) := by
          unfold productThreshold
          exact Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ hV))
        _ = _ := by
          rw [← pow_mul, ← pow_mul, ← pow_add, ← pow_add, ← pow_add]
          exact congrArg (fun j : ℕ => (2 : ℕ) ^ j) (by ring)
    have hp : (2 * 2 ^ d) ^ K = 2 ^ ((d + 1) * K) := by
      rw [show 2 * 2 ^ d = 2 ^ (d + 1) by rw [pow_succ]; omega, ← pow_mul]
    have he : E * (r + 7) + V + (d + 1) * K < E * K := by
      dsimp [K]
      nlinarith
    calc
      _ ≤ 2 ^ (E * (r + 7) + V) * (2 * 2 ^ d) ^ K := Nat.mul_le_mul_right _ hD
      _ = 2 ^ (E * (r + 7) + V + (d + 1) * K) := by rw [hp, ← pow_add]
      _ < 2 ^ (E * K) := Nat.pow_lt_pow_right (by decide) he
      _ = _ := pow_mul _ _ _

/-- A computable exponent for any verified input bound at size 2r+7. -/
def bootstrapExponent (r n d : ℕ) : ℕ :=
  max d (max (2 * (2 * (r + 3) + 1))
    (((d + 1) * (2 * (r + 3) + 1) + Nat.clog 2 (supportProductBound r n)) / r + 1))

theorem integer_bootstrap_bound {r n d : ℕ} (hn : 4 ≤ n) (hr : 1 ≤ r)
    (hK : 2 * (r + 3) + 1 ≤ 2 ^ d)
    (hforce : ForcesConvexNGon (2 ^ d) (2 * (r + 3) + 1)) :
    ForcesConvexNGon (2 ^ bootstrapExponent r n d) n := by
  apply bootstrap_exponential_bound hn hforce hK (le_max_left _ _)
    ((le_max_left _ _).trans (le_max_right _ _)) (Nat.le_pow_clog (by decide) _)
  have hlt (a : ℕ) : a < r * (a / r + 1) := by
    have hrem := Nat.mod_lt a (by omega : 0 < r)
    have he := Nat.mod_add_div a r
    nlinarith
  exact (hlt _).trans_le (Nat.mul_le_mul_left _ ((le_max_right _ _).trans (le_max_right _ _)))

/-- Plug the already proved finite Suk theorem into the new bootstrap.
Every hypothesis is an elementary integer constraint; no ES bound is assumed. -/
theorem suk_bootstrap_bound {r n a : ℕ} (hn : 4 ≤ n) (hr : 1 ≤ r)
    (ha : 2 ≤ a) (hKa : 2 * (r + 3) + 1 ≤ a ^ 3) :
    ForcesConvexNGon (2 ^ bootstrapExponent r n
      ((2 * (r + 3) + 1) + a ^ 2 + Nat.clog 2 ((2 * (r + 3) + 1) + a ^ 2) * a ^ 2 +
        64 * (a * (a + 1) + 5))) n := by
  apply integer_bootstrap_bound hn hr
  · exact (show 2 * (r + 3) + 1 ≤
      ((2 * (r + 3) + 1) + a ^ 2 + Nat.clog 2 ((2 * (r + 3) + 1) + a ^ 2) * a ^ 2 +
        64 * (a * (a + 1) + 5)) by omega).trans
      (Nat.lt_pow_self (a := 2) (by decide)).le
  · exact cubic_log_bound (by omega) ha hKa

end ErdosSzekeres.HMPT
