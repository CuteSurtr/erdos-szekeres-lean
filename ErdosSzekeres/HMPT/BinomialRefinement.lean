import ErdosSzekeres.HMPT.TwoScale

/-!
A finite refinement of the existing HMPT two-scale interface: retain the exact
number of available smaller subsets rather than bounding it by ordered tuples.
This sharpens this repository's sufficient finite criteria. It asserts no new
asymptotic coefficient and no literature-priority claim.
-/

namespace ErdosSzekeres.HMPT
open Suk

/-- There are at most as many convex subsets as subsets of the specified size. -/
theorem convexSubsets_card_le_choose (P : Finset Point) (k : ℕ) :
    (convexSubsets P k).card ≤ P.card.choose k := by
  classical
  exact (Finset.card_le_card (Finset.filter_subset _ _)).trans_eq
    (Finset.card_powersetCard _ _)

/-- The two-scale count with the exact binomial count at its initial scale. -/
def twoScaleBinomialThreshold (N m n : ℕ) : ℕ :=
  N.choose (m + 1) * (N ^ 6 * twoScaleProduct m n)

theorem convex_two_scale_binomial_bound {m n : ℕ} (P : Finset Point)
    (hm : 3 ≤ m) (hn : 4 ≤ n) (hgp : GeneralPosition P)
    (hdist : ∀ p ∈ P, ∀ q ∈ P, p 0 = q 0 → p = q)
    (havoid : ¬ HasConvexNGon n P) :
    (convexSubsets P (4 * m + 1)).card ≤ twoScaleBinomialThreshold P.card m n := by
  exact (convex_two_scale_ratio_bound P hm hn hgp hdist havoid).trans
    (Nat.mul_le_mul_right _ (convexSubsets_card_le_choose P (m + 1)))

/-- A stronger exact finite density criterion, valid for arbitrary real point
sets in general position. The only input is any already proved smaller ES bound. -/
theorem two_scale_binomial_bound {N M m n : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hKM : 4 * m + 1 ≤ M) (hMN : M ≤ N)
    (hforce : ForcesConvexNGon M (4 * m + 1))
    (hsize : twoScaleBinomialThreshold N m n * M.choose (4 * m + 1) <
      N.choose (4 * m + 1)) : ForcesConvexNGon N n := by
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
  have hbound := convex_two_scale_binomial_bound T hm hn hgpT hxT havoidT
  have h := hcount.trans (Nat.mul_le_mul_right _ hbound)
  rw [hTcard] at h
  exact (not_lt_of_ge h) hsize

/-- The refined count is never larger than the previous tuple bound. -/
theorem twoScaleBinomialThreshold_le (N m n : ℕ) :
    twoScaleBinomialThreshold N m n ≤ twoScaleThreshold N m n := by
  calc
    _ ≤ N ^ (m + 1) * (N ^ 6 * twoScaleProduct m n) :=
      Nat.mul_le_mul_right _ (Nat.choose_le_pow _ _)
    _ = _ := by unfold twoScaleThreshold; rw [← mul_assoc, ← pow_add]

/-- For positive populations and a nontrivial initial scale, the count used in
this density test is strictly smaller than the previous one. -/
theorem twoScaleBinomialThreshold_lt {N m n : ℕ} (hN : 0 < N) (hm : 1 ≤ m) :
    twoScaleBinomialThreshold N m n < twoScaleThreshold N m n := by
  have hB (r : ℕ) : 0 < supportProductBound r n := by
    unfold supportProductBound
    exact Nat.mul_pos (by positivity) (Nat.choose_pos (by omega))
  have hP : 0 < N ^ 6 * twoScaleProduct m n := by
    unfold twoScaleProduct
    exact Nat.mul_pos (by positivity) (Nat.mul_pos (hB _) (hB _))
  calc
    _ < N ^ (m + 1) * (N ^ 6 * twoScaleProduct m n) :=
      Nat.mul_lt_mul_of_pos_right (Nat.choose_lt_pow (by omega) (by omega)) hP
    _ = _ := by unfold twoScaleThreshold; rw [← mul_assoc, ← pow_add]

/-- The initial-scale factorial yields an exact integer saving in the exponent
budget. No approximation to a factorial or binomial coefficient is assumed. -/
theorem two_scale_factorial_exponential_bound {m n d E V : ℕ}
    (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hforce : ForcesConvexNGon (2 ^ d) (4 * m + 1))
    (hK : 4 * m + 1 ≤ 2 ^ d) (hdE : d ≤ E) (hE : 2 * (4 * m + 1) ≤ E)
    (hV : twoScaleProduct m n ≤ 2 ^ V)
    (hbudget : (d + 1) * (4 * m + 1) + V <
      (3 * m - 6) * E + Nat.log 2 (m + 1).factorial) :
    ForcesConvexNGon (2 ^ E) n := by
  apply two_scale_binomial_bound hm hn hK
    (Nat.pow_le_pow_right (by decide) hdE) hforce
  apply binomial_ratio_lt_of_scaled_power
  · exact hE.trans (Nat.lt_pow_self (n := E) (a := 2) (by decide)).le
  · have hchoose : (m + 1).factorial * (2 ^ E).choose (m + 1) ≤
        (2 ^ E) ^ (m + 1) := by
      rw [← Nat.descFactorial_eq_factorial_mul_choose]
      exact Nat.descFactorial_le_pow _ _
    have hbound : (m + 1).factorial * twoScaleBinomialThreshold (2 ^ E) m n ≤
        2 ^ (E * (m + 7) + V) := by
      calc
        _ = ((m + 1).factorial * (2 ^ E).choose (m + 1)) *
          ((2 ^ E) ^ 6 * twoScaleProduct m n) := by
            unfold twoScaleBinomialThreshold; ring
        _ ≤ (2 ^ E) ^ (m + 1) * ((2 ^ E) ^ 6 * 2 ^ V) :=
          Nat.mul_le_mul hchoose (Nat.mul_le_mul_left _ hV)
        _ = _ := by
          rw [← mul_assoc, ← pow_add, ← pow_mul, ← pow_add]
    have hp : (2 * 2 ^ d) ^ (4 * m + 1) = 2 ^ ((d + 1) * (4 * m + 1)) := by
      rw [show 2 * 2 ^ d = 2 ^ (d + 1) by rw [pow_succ]; omega, ← pow_mul]
    have he : E * (m + 7) + V + (d + 1) * (4 * m + 1) <
        E * (4 * m + 1) + Nat.log 2 (m + 1).factorial := by
      have hsub : 3 * m - 6 + 6 = 3 * m := by omega
      nlinarith
    have hmul : (m + 1).factorial *
        (twoScaleBinomialThreshold (2 ^ E) m n * (2 * 2 ^ d) ^ (4 * m + 1)) <
        (m + 1).factorial * (2 ^ E) ^ (4 * m + 1) := by
      calc
        _ = ((m + 1).factorial * twoScaleBinomialThreshold (2 ^ E) m n) *
            (2 * 2 ^ d) ^ (4 * m + 1) := by ring
        _ ≤ 2 ^ (E * (m + 7) + V) * (2 * 2 ^ d) ^ (4 * m + 1) :=
          Nat.mul_le_mul_right _ hbound
        _ = 2 ^ (E * (m + 7) + V + (d + 1) * (4 * m + 1)) := by rw [hp, ← pow_add]
        _ < 2 ^ (E * (4 * m + 1) + Nat.log 2 (m + 1).factorial) :=
          Nat.pow_lt_pow_right (by decide) he
        _ = (2 ^ E) ^ (4 * m + 1) * 2 ^ Nat.log 2 (m + 1).factorial := by
          rw [pow_add, ← pow_mul]
        _ ≤ (2 ^ E) ^ (4 * m + 1) * (m + 1).factorial :=
          Nat.mul_le_mul_left _ (Nat.pow_log_le_self _ (Nat.factorial_ne_zero _))
        _ = _ := Nat.mul_comm _ _
    exact lt_of_mul_lt_mul_left hmul (Nat.zero_le _)

/-- A computable closed exponent retaining the factorial saving. -/
def twoScaleFactorialExponent (m n d : ℕ) : ℕ :=
  max d (max (2 * (4 * m + 1))
    (((d + 1) * (4 * m + 1) + Nat.clog 2 (twoScaleProduct m n) -
      Nat.log 2 (m + 1).factorial) / (3 * m - 6) + 1))

theorem integer_two_scale_factorial_bound {m n d : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hK : 4 * m + 1 ≤ 2 ^ d) (hforce : ForcesConvexNGon (2 ^ d) (4 * m + 1)) :
    ForcesConvexNGon (2 ^ twoScaleFactorialExponent m n d) n := by
  apply two_scale_factorial_exponential_bound hm hn hforce hK
    (le_max_left _ _) ((le_max_left _ _).trans (le_max_right _ _))
    (Nat.le_pow_clog (by decide) _)
  let A := (d + 1) * (4 * m + 1) + Nat.clog 2 (twoScaleProduct m n)
  let F := Nat.log 2 (m + 1).factorial
  have hrem := Nat.mod_lt (A - F) (by omega : 0 < 3 * m - 6)
  have he := Nat.mod_add_div (A - F) (3 * m - 6)
  have hAF : A ≤ (A - F) + F := by omega
  have hlt : A < (3 * m - 6) * ((A - F) / (3 * m - 6) + 1) + F := by nlinarith
  exact hlt.trans_le (Nat.add_le_add_right
    (Nat.mul_le_mul_left _ ((le_max_right _ _).trans (le_max_right _ _))) _)

/-- This closed exponent is never worse than the existing exact-product one. -/
theorem twoScaleFactorialExponent_le (m n d : ℕ) :
    twoScaleFactorialExponent m n d ≤ twoScaleExponent m n d := by
  unfold twoScaleFactorialExponent twoScaleExponent
  exact max_le_max le_rfl (max_le_max le_rfl
    (Nat.add_le_add_right (Nat.div_le_div_right (Nat.sub_le _ _)) _))

/-- Instantiation by the fully proved finite Suk theorem leaves only ordinary
integer parameter constraints, with no unproved geometric input. -/
theorem suk_two_scale_factorial_bound {m n a : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (ha : 2 ≤ a) (hKa : 4 * m + 1 ≤ a ^ 3) :
    ForcesConvexNGon (2 ^ twoScaleFactorialExponent m n
      ((4 * m + 1) + a ^ 2 + Nat.clog 2 ((4 * m + 1) + a ^ 2) * a ^ 2 +
        64 * (a * (a + 1) + 5))) n := by
  apply integer_two_scale_factorial_bound hm hn
  · exact (show 4 * m + 1 ≤
      ((4 * m + 1) + a ^ 2 + Nat.clog 2 ((4 * m + 1) + a ^ 2) * a ^ 2 +
        64 * (a * (a + 1) + 5)) by omega).trans
      (Nat.lt_pow_self (a := 2) (by decide)).le
  · exact cubic_log_bound (by omega) ha hKa

end ErdosSzekeres.HMPT
