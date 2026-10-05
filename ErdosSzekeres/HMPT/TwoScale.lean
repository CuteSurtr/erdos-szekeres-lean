import ErdosSzekeres.HMPT.FanCounting
import ErdosSzekeres.HMPT.BootstrapBound

namespace ErdosSzekeres.HMPT

open Suk

/-- The two successive support-product factors at sizes m+1, 2m+1, 4m+1. -/
def twoScaleProduct (m n : ℕ) : ℕ :=
  supportProductBound (m - 3) n * supportProductBound (2 * m - 3) n

/-- Telescope the two genuine convex-subset ratios. -/
theorem convex_two_scale_ratio_bound {m n : ℕ} (P : Finset Point)
    (hm : 3 ≤ m) (hn : 4 ≤ n) (hgp : GeneralPosition P)
    (hdist : ∀ p ∈ P, ∀ q ∈ P, p 0 = q 0 → p = q)
    (havoid : ¬ HasConvexNGon n P) :
    (convexSubsets P (4 * m + 1)).card ≤
      (convexSubsets P (m + 1)).card * (P.card ^ 6 * twoScaleProduct m n) := by
  have h₁ := convex_family_ratio_bound (r := m - 3) P hn hgp hdist havoid
  have h₂ := convex_family_ratio_bound (r := 2 * m - 3) P hn hgp hdist havoid
  rw [show 2 * (m - 3 + 3) + 1 = 2 * m + 1 by omega,
    show m - 3 + 4 = m + 1 by omega] at h₁
  rw [show 2 * (2 * m - 3 + 3) + 1 = 4 * m + 1 by omega,
    show 2 * m - 3 + 4 = 2 * m + 1 by omega] at h₂
  calc
    _ ≤ ((convexSubsets P (m + 1)).card *
        (P.card ^ 3 * supportProductBound (m - 3) n)) *
        (P.card ^ 3 * supportProductBound (2 * m - 3) n) :=
      h₂.trans (Nat.mul_le_mul_right _ h₁)
    _ = _ := by unfold twoScaleProduct; ring

theorem convexSubsets_card_le_pow (P : Finset Point) (k : ℕ) :
    (convexSubsets P k).card ≤ P.card ^ k := by
  classical
  calc
    _ ≤ (P.powersetCard k).card := Finset.card_le_card (Finset.filter_subset _ _)
    _ = P.card.choose k := Finset.card_powersetCard _ _
    _ ≤ P.card ^ k := Nat.choose_le_pow _ _

/-- The six endpoint choices from the two ratios are retained explicitly. -/
def twoScaleThreshold (N m n : ℕ) : ℕ := N ^ (m + 7) * twoScaleProduct m n

theorem convex_two_scale_bound {m n : ℕ} (P : Finset Point)
    (hm : 3 ≤ m) (hn : 4 ≤ n) (hgp : GeneralPosition P)
    (hdist : ∀ p ∈ P, ∀ q ∈ P, p 0 = q 0 → p = q)
    (havoid : ¬ HasConvexNGon n P) :
    (convexSubsets P (4 * m + 1)).card ≤ twoScaleThreshold P.card m n := by
  calc
    _ ≤ P.card ^ (m + 1) * (P.card ^ 6 * twoScaleProduct m n) :=
      (convex_two_scale_ratio_bound P hm hn hgp hdist havoid).trans
        (Nat.mul_le_mul_right _ (convexSubsets_card_le_pow P (m + 1)))
    _ = _ := by unfold twoScaleThreshold; rw [← mul_assoc, ← pow_add]

/-- A finite real-plane bound from the two-scale count and any verified input
bound for a convex (4m+1)-gon. No incidence or extraction hypothesis is assumed. -/
theorem two_scale_bound {N M m n : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hKM : 4 * m + 1 ≤ M) (hMN : M ≤ N)
    (hforce : ForcesConvexNGon M (4 * m + 1))
    (hsize : twoScaleThreshold N m n * M.choose (4 * m + 1) < N.choose (4 * m + 1)) :
    ForcesConvexNGon N n := by
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
  have hcount := convex_subsets_density T (4 * m + 1) M hKM
    (by simpa only [hTcard] using hMN) hgpT hforce
  have hbound := convex_two_scale_bound T hm hn hgpT hxT havoidT
  have h := hcount.trans (Nat.mul_le_mul_right _ hbound)
  rw [hTcard] at h
  exact (not_lt_of_ge h) hsize

/-- The power-budget form isolates the analytic estimates still needed for
the final published coefficient. The denominator is 3m-6, with no hidden losses. -/
theorem two_scale_exponential_bound {m n d E V : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hforce : ForcesConvexNGon (2 ^ d) (4 * m + 1))
    (hK : 4 * m + 1 ≤ 2 ^ d) (hdE : d ≤ E) (hE : 2 * (4 * m + 1) ≤ E)
    (hV : twoScaleProduct m n ≤ 2 ^ V)
    (hbudget : (d + 1) * (4 * m + 1) + V < (3 * m - 6) * E) :
    ForcesConvexNGon (2 ^ E) n := by
  apply two_scale_bound hm hn hK (Nat.pow_le_pow_right (by decide) hdE) hforce
  apply binomial_ratio_lt_of_scaled_power
  · exact hE.trans (Nat.lt_pow_self (n := E) (a := 2) (by decide)).le
  · have hD : twoScaleThreshold (2 ^ E) m n ≤ 2 ^ (E * (m + 7) + V) := by
      calc
        _ ≤ (2 ^ E) ^ (m + 7) * 2 ^ V := Nat.mul_le_mul_left _ hV
        _ = _ := by rw [← pow_mul, ← pow_add]
    have hp : (2 * 2 ^ d) ^ (4 * m + 1) = 2 ^ ((d + 1) * (4 * m + 1)) := by
      rw [show 2 * 2 ^ d = 2 ^ (d + 1) by rw [pow_succ]; omega, ← pow_mul]
    have he : E * (m + 7) + V + (d + 1) * (4 * m + 1) < E * (4 * m + 1) := by
      have hsub : 3 * m - 6 + 6 = 3 * m := by omega
      nlinarith
    calc
      _ ≤ 2 ^ (E * (m + 7) + V) * (2 * 2 ^ d) ^ (4 * m + 1) :=
        Nat.mul_le_mul_right _ hD
      _ = 2 ^ (E * (m + 7) + V + (d + 1) * (4 * m + 1)) := by rw [hp, ← pow_add]
      _ < 2 ^ (E * (4 * m + 1)) := Nat.pow_lt_pow_right (by decide) he
      _ = _ := pow_mul _ _ _

/-- A computable exponent for the complete two-scale geometric theorem. -/
def twoScaleExponent (m n d : ℕ) : ℕ :=
  max d (max (2 * (4 * m + 1))
    (((d + 1) * (4 * m + 1) + Nat.clog 2 (twoScaleProduct m n)) / (3 * m - 6) + 1))

theorem integer_two_scale_bound {m n d : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hK : 4 * m + 1 ≤ 2 ^ d) (hforce : ForcesConvexNGon (2 ^ d) (4 * m + 1)) :
    ForcesConvexNGon (2 ^ twoScaleExponent m n d) n := by
  apply two_scale_exponential_bound hm hn hforce hK (le_max_left _ _)
    ((le_max_left _ _).trans (le_max_right _ _)) (Nat.le_pow_clog (by decide) _)
  have hlt (a : ℕ) : a < (3 * m - 6) * (a / (3 * m - 6) + 1) := by
    have hrem := Nat.mod_lt a (by omega : 0 < 3 * m - 6)
    have he := Nat.mod_add_div a (3 * m - 6)
    nlinarith
  exact (hlt _).trans_le (Nat.mul_le_mul_left _ ((le_max_right _ _).trans (le_max_right _ _)))

/-- Instantiation by the proved finite Suk bound. All hypotheses are explicit
integer constraints, so parameter searches may choose any admissible m and a. -/
theorem suk_two_scale_bound {m n a : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (ha : 2 ≤ a) (hKa : 4 * m + 1 ≤ a ^ 3) :
    ForcesConvexNGon (2 ^ twoScaleExponent m n
      ((4 * m + 1) + a ^ 2 + Nat.clog 2 ((4 * m + 1) + a ^ 2) * a ^ 2 +
        64 * (a * (a + 1) + 5))) n := by
  apply integer_two_scale_bound hm hn
  · exact (show 4 * m + 1 ≤
      ((4 * m + 1) + a ^ 2 + Nat.clog 2 ((4 * m + 1) + a ^ 2) * a ^ 2 +
        64 * (a * (a + 1) + 5)) by omega).trans
      (Nat.lt_pow_self (a := 2) (by decide)).le
  · exact cubic_log_bound (by omega) ha hKa

end ErdosSzekeres.HMPT
