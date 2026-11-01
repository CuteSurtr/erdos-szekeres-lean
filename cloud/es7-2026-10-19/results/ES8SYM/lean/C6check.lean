import Mathlib.Analysis.InnerProductSpace.Convex
import Mathlib.Analysis.Convex.Independent
import Mathlib.Analysis.Convex.StrictConvexSpace
import Mathlib.RingTheory.RootsOfUnity.Complex

/-!
# Check of `ES8SYM/proofs/layers.md`, Lemma 2

* `part_a`: if `S ⊆ ℂ` is invariant under multiplication by `ζ = exp(2πi/m)` with `m ≥ 8` and `S`
  contains no 8 distinct points in convex position (no injective, convex-independent family
  `Fin 8 → ℂ` with values in `S`), then `S ⊆ {0}`.
  No general-position hypothesis is needed for this part.
* `thr_m4` … `thr_m7`: the arithmetic of part (b), `|S| = m t + c` with `c ≤ 1`
  (`c = 0` for even `m`). The geometric input of part (b), the layer lemma (every convex layer is one
  rotation orbit when `K ≤ 2m`, and the centre is excluded for even `m` by general position), is NOT
  formalised here.
-/

open Complex Metric Set

namespace RefuteC6

/-- Points of the sphere `‖x‖ = r` are extreme points of the closed ball (ℂ is strictly convex). -/
theorem sphere_subset_extremePoints (r : ℝ) :
    sphere (0 : ℂ) r ⊆ (closedBall (0 : ℂ) r).extremePoints ℝ := by
  intro x hx
  rw [mem_sphere_zero_iff_norm] at hx
  rw [mem_extremePoints]
  refine ⟨mem_closedBall_zero_iff.2 hx.le, ?_⟩
  intro x₁ hx₁ x₂ hx₂ hseg
  rw [mem_closedBall_zero_iff] at hx₁ hx₂
  by_cases hne : x₁ = x₂
  · subst hne
    rw [openSegment_same, mem_singleton_iff] at hseg
    exact ⟨hseg.symm, hseg.symm⟩
  · exfalso
    obtain ⟨a, b, ha, hb, hab, hx'⟩ := hseg
    have hlt := norm_combo_lt_of_ne hx₁ hx₂ hne ha hb hab
    rw [hx', hx] at hlt
    exact lt_irrefl _ hlt

/-- An injective family of points on a circle centred at 0 is convex independent. -/
theorem convexIndependent_of_norm_eq {ι : Type*} (f : ι → ℂ) (hf : Function.Injective f) (r : ℝ)
    (hr : ∀ i, ‖f i‖ = r) : ConvexIndependent ℝ f := by
  rw [convexIndependent_iff_notMem_convexHull_diff]
  intro i s hmem
  have hext : f i ∈ (closedBall (0 : ℂ) r).extremePoints ℝ :=
    sphere_subset_extremePoints r (mem_sphere_zero_iff_norm.2 (hr i))
  have hconv : Convex ℝ (closedBall (0 : ℂ) r \ {f i}) :=
    ((convex_closedBall (0 : ℂ) r).mem_extremePoints_iff_convex_diff.1 hext).2
  have hsub : f '' (s \ {i}) ⊆ closedBall (0 : ℂ) r \ {f i} := by
    rintro _ ⟨j, hj, rfl⟩
    refine ⟨mem_closedBall_zero_iff.2 (hr j).le, ?_⟩
    intro hji
    rw [mem_singleton_iff] at hji
    exact hj.2 (mem_singleton_iff.2 (hf hji))
  exact (convexHull_min hsub hconv hmem).2 (mem_singleton _)

/-- `ζ_m = exp(2πi/m)`, the generator of the rotation by `2π/m`. -/
noncomputable def zeta (m : ℕ) : ℂ := Complex.exp (2 * Real.pi * Complex.I / m)

theorem zeta_prim (m : ℕ) (hm0 : m ≠ 0) : IsPrimitiveRoot (zeta m) m :=
  Complex.isPrimitiveRoot_exp m hm0

/-- The first 8 points `p ζ^k` (k < 8) of the orbit of `p ≠ 0` are distinct when `m ≥ 8`. -/
theorem orbit_injective (m : ℕ) (hm : 8 ≤ m) (p : ℂ) (hp : p ≠ 0) :
    Function.Injective (fun k : Fin 8 => p * zeta m ^ (k : ℕ)) := by
  have hprim := zeta_prim m (by omega)
  intro j k hjk
  dsimp only at hjk
  have h2 : zeta m ^ (j : ℕ) = zeta m ^ (k : ℕ) := mul_left_cancel₀ hp hjk
  exact Fin.ext (hprim.pow_inj (lt_of_lt_of_le j.isLt hm) (lt_of_lt_of_le k.isLt hm) h2)

/-- ... and they are in convex position (they lie on the circle of radius `‖p‖`). -/
theorem orbit_convexIndependent (m : ℕ) (hm : 8 ≤ m) (p : ℂ) (hp : p ≠ 0) :
    ConvexIndependent ℝ (fun k : Fin 8 => p * zeta m ^ (k : ℕ)) := by
  have hm0 : m ≠ 0 := by omega
  have hprim := zeta_prim m hm0
  refine convexIndependent_of_norm_eq _ (orbit_injective m hm p hp) ‖p‖ ?_
  intro k
  simp only [norm_mul, norm_pow, hprim.norm'_eq_one hm0, one_pow, mul_one]

/-- **C6 (a).** An `m`-fold symmetric set (`m ≥ 8`, centre 0) without 8 points in convex position
is contained in `{0}`. -/
theorem part_a (m : ℕ) (hm : 8 ≤ m) (S : Set ℂ)
    (hS : ∀ z ∈ S, Complex.exp (2 * Real.pi * Complex.I / m) * z ∈ S)
    (hfree : ∀ f : Fin 8 → ℂ, Function.Injective f → (∀ i, f i ∈ S) → ¬ ConvexIndependent ℝ f) :
    S ⊆ {0} := by
  intro p hpS
  rw [mem_singleton_iff]
  by_contra hp
  have horb : ∀ k : ℕ, p * zeta m ^ k ∈ S := by
    intro k
    induction k with
    | zero => simpa using hpS
    | succ k ih =>
      have h := hS _ ih
      have heq : Complex.exp (2 * Real.pi * Complex.I / m) * (p * zeta m ^ k)
          = p * zeta m ^ (k + 1) := by
        unfold zeta
        ring
      rw [heq] at h
      exact h
  exact hfree _ (orbit_injective m hm p hp) (fun i => horb i) (orbit_convexIndependent m hm p hp)

/-! ## C6 (b): arithmetic only (`|S| = m t + c`, `c ≤ 1`, `c = 0` for even `m`). -/

theorem thr_m4 (t : ℕ) : 65 ≤ 4 * t ↔ 17 ≤ t := by omega
theorem thr_m5 (t c : ℕ) (hc : c ≤ 1) : 65 ≤ 5 * t + c ↔ 13 ≤ t := by omega
theorem thr_m6 (t : ℕ) : 65 ≤ 6 * t ↔ 11 ≤ t := by omega
theorem thr_m7 (t c : ℕ) (hc : c ≤ 1) : 65 ≤ 7 * t + c ↔ 10 ≤ t := by omega

/-- Without general position the even-`m` centre exclusion fails; then `4 t + 1` points are possible
and the `m = 4` threshold would be wrong: `t = 16` already gives 65. -/
theorem m4_with_centre_counter : 65 ≤ 4 * 16 + 1 ∧ ¬ (17 ≤ 16) := by omega

end RefuteC6

#print axioms RefuteC6.part_a
#print axioms RefuteC6.thr_m4
#print axioms RefuteC6.thr_m5
#print axioms RefuteC6.thr_m6
#print axioms RefuteC6.thr_m7
