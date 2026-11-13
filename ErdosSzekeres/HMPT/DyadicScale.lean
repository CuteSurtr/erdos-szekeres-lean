import ErdosSzekeres.HMPT.ParameterBarrier

/-!
Repeated dyadic telescoping of the existing convex-family estimate, together
with an exact optimization of its idealized leading expression. The algebraic
barrier does not assert an asymptotic limit theorem for the new finite formula,
and it does not rule out different geometric or entropy arguments.
-/

namespace ErdosSzekeres.HMPT
open Suk

/-- The exact support factors from a finite number of repeated doubling steps. -/
def dyadicScaleProduct (m n : ℕ) : ℕ → ℕ
  | 0 => 1
  | s + 1 => dyadicScaleProduct m n s * supportProductBound (2 ^ s * m - 3) n

/-- Telescope any number of the already proved real-point convex-subset ratios.
All three endpoint choices at every stage remain in the displayed bound. -/
theorem convex_dyadic_scale_ratio_bound {m n : ℕ} (P : Finset Point)
    (hm : 3 ≤ m) (hn : 4 ≤ n) (hgp : GeneralPosition P)
    (hdist : ∀ p ∈ P, ∀ q ∈ P, p 0 = q 0 → p = q)
    (havoid : ¬ HasConvexNGon n P) (s : ℕ) :
    (convexSubsets P (2 ^ s * m + 1)).card ≤
      (convexSubsets P (m + 1)).card *
        (P.card ^ (3 * s) * dyadicScaleProduct m n s) := by
  induction s with
  | zero => simp [dyadicScaleProduct]
  | succ s ih =>
    have hpow : 1 ≤ (2 : ℕ) ^ s := Nat.one_le_pow s 2 (by omega)
    have hsize : 3 ≤ 2 ^ s * m := hm.trans (by nlinarith)
    have hstep := convex_family_ratio_bound (r := 2 ^ s * m - 3)
      P hn hgp hdist havoid
    rw [show 2 * (2 ^ s * m - 3 + 3) + 1 = 2 ^ (s + 1) * m + 1 by
        rw [Nat.sub_add_cancel hsize, pow_succ]; ring,
      show 2 ^ s * m - 3 + 4 = 2 ^ s * m + 1 by omega] at hstep
    calc
      _ ≤ ((convexSubsets P (m + 1)).card *
          (P.card ^ (3 * s) * dyadicScaleProduct m n s)) *
            (P.card ^ 3 * supportProductBound (2 ^ s * m - 3) n) :=
        hstep.trans (Nat.mul_le_mul_right _ ih)
      _ = _ := by
        simp only [dyadicScaleProduct, Nat.mul_add, Nat.mul_one, pow_add]
        ring

/-- A corresponding explicit upper bound retaining every endpoint loss. -/
theorem convex_dyadic_scale_bound {m n : ℕ} (P : Finset Point)
    (hm : 3 ≤ m) (hn : 4 ≤ n) (hgp : GeneralPosition P)
    (hdist : ∀ p ∈ P, ∀ q ∈ P, p 0 = q 0 → p = q)
    (havoid : ¬ HasConvexNGon n P) (s : ℕ) :
    (convexSubsets P (2 ^ s * m + 1)).card ≤
      P.card ^ (m + 1 + 3 * s) * dyadicScaleProduct m n s := by
  calc
    _ ≤ P.card ^ (m + 1) * (P.card ^ (3 * s) * dyadicScaleProduct m n s) :=
      (convex_dyadic_scale_ratio_bound P hm hn hgp hdist havoid s).trans
        (Nat.mul_le_mul_right _ (convexSubsets_card_le_pow P (m + 1)))
    _ = _ := by rw [← mul_assoc, ← pow_add]


/-- The repeated ratio estimate gives a finite forcing theorem whenever its
explicit integer density inequality holds. The endpoint losses are retained. -/
theorem dyadic_scale_bound {N M m n s : ℕ} (hm : 3 ≤ m) (hn : 4 ≤ n)
    (hKM : 2 ^ s * m + 1 ≤ M) (hMN : M ≤ N)
    (hforce : ForcesConvexNGon M (2 ^ s * m + 1))
    (hsize : (N ^ (m + 1 + 3 * s) * dyadicScaleProduct m n s) *
      M.choose (2 ^ s * m + 1) < N.choose (2 ^ s * m + 1)) :
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
  have hcount := convex_subsets_density T (2 ^ s * m + 1) M hKM
    (by simpa only [hTcard] using hMN) hgpT hforce
  have hbound := convex_dyadic_scale_bound T hm hn hgpT hxT havoidT s
  have h := hcount.trans (Nat.mul_le_mul_right _ hbound)
  rw [hTcard] at h
  exact (not_lt_of_ge h) hsize

/-- Elementary optimization of the formal expression obtained by repeating
same-ratio telescoping. This theorem alone asserts no geometric extension. -/
theorem dyadic_stage_discriminant (s : ℕ) (hs : 1 ≤ s) :
    32 * ((2 : ℝ) ^ s - 1) ^ 2 ≤ 9 * (s : ℝ) * ((2 : ℝ) ^ s) ^ 2 := by
  by_cases hsmall : s ≤ 3
  · interval_cases s <;> norm_num at *
  · have hfour : (4 : ℝ) ≤ s := by exact_mod_cast (show 4 ≤ s by omega)
    have hpow : 1 ≤ (2 : ℝ) ^ s := one_le_pow₀ (by norm_num)
    have hsq : ((2 : ℝ) ^ s - 1) ^ 2 ≤ ((2 : ℝ) ^ s) ^ 2 := by nlinarith
    calc
      _ ≤ 32 * ((2 : ℝ) ^ s) ^ 2 := mul_le_mul_of_nonneg_left hsq (by norm_num)
      _ ≤ _ := mul_le_mul_of_nonneg_right (by linarith) (sq_nonneg _)

private theorem quadratic_nonpositive (a b d x : ℝ) (ha : 0 < a)
    (hd : b ^ 2 ≤ 4 * a * d) : b * x - a * x ^ 2 - d ≤ 0 := by
  have hi : 4 * a * (b * x - a * x ^ 2 - d) =
      b ^ 2 - 4 * a * d - (2 * a * x - b) ^ 2 := by ring
  have hh : 4 * a * (b * x - a * x ^ 2 - d) ≤ 0 := by
    rw [hi]
    nlinarith [sq_nonneg (2 * a * x - b)]
  by_contra! hz
  have hp := mul_pos (show 0 < 4 * a by positivity) hz
  linarith

/-- No number of repeated doubling stages makes this idealized leading budget
positive at or below the HMPT coefficient. Two stages attain zero slack. -/
theorem dyadic_leading_budget_nonpositive (s : ℕ) (hs : 1 ≤ s)
    (c C : ℝ) (hc : 0 ≤ c) (hC : C ≤ publishedCoefficient) :
    ((2 : ℝ) ^ s - 1) * c * C - ((2 : ℝ) ^ s) ^ 2 * c ^ 2 - s ≤ 0 := by
  have hpow : 1 ≤ (2 : ℝ) ^ s := one_le_pow₀ (by norm_num)
  have hdisc : (((2 : ℝ) ^ s - 1) * publishedCoefficient) ^ 2 ≤
      4 * ((2 : ℝ) ^ s) ^ 2 * s := by
    have hd := dyadic_stage_discriminant s hs
    have he : publishedCoefficient ^ 2 = (128 : ℝ) / 9 := by
      unfold publishedCoefficient
      nlinarith [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    rw [mul_pow, he]
    nlinarith
  have hq := quadratic_nonpositive (((2 : ℝ) ^ s) ^ 2)
    (((2 : ℝ) ^ s - 1) * publishedCoefficient) (s : ℝ) c
    (by positivity) hdisc
  have hm := mul_le_mul_of_nonneg_left hC
    (mul_nonneg (sub_nonneg.mpr hpow) hc)
  nlinarith

/-- The best coefficient in this explicit budget family is attained with two
stages. This is an algebraic statement about the family, not an ES lower bound. -/
theorem positive_dyadic_leading_budget_iff (C : ℝ) :
    (∃ s : ℕ, 1 ≤ s ∧ ∃ c : ℝ, 0 < c ∧
      0 < ((2 : ℝ) ^ s - 1) * c * C - ((2 : ℝ) ^ s) ^ 2 * c ^ 2 - s) ↔
      publishedCoefficient < C := by
  constructor
  · rintro ⟨s, hs, c, hc, hp⟩
    by_contra! hC
    exact (not_lt_of_ge (dyadic_leading_budget_nonpositive s hs c C hc.le hC)) hp
  · intro hC
    obtain ⟨c, hc, hp⟩ := (positive_leading_slack_iff C).mpr hC
    refine ⟨2, by omega, c, hc, ?_⟩
    norm_num
    norm_num at hp
    exact hp

end ErdosSzekeres.HMPT
