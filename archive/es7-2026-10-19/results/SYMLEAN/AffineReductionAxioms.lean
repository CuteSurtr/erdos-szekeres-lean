import ErdosSzekeres.Basic
import ErdosSzekeres.OrientationGeometry
import ErdosSzekeres.Suk.SupportingLines
import Mathlib.Analysis.Complex.Isometry
import Mathlib.Analysis.Convex.StrictConvexBetween
import Mathlib.Analysis.InnerProductSpace.Convex
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.LinearAlgebra.Complex.FiniteDimensional
import Mathlib.Analysis.SpecialFunctions.Pow.Complex
import Mathlib.RingTheory.RootsOfUnity.Complex
import Mathlib.Dynamics.PeriodicPts.Defs

/-!
# The symmetry reduction for convex heptagons (Corollary 3 of `WRITEUP/SYMMETRIC.md`)

Five case classes are stated as `Prop`s (they are *hypotheses*, never axioms):

* `HalfTurn34`      — 34 points, invariant under the half-turn about `c`, `c ∉ S`;
* `Threefold33`     — 33 points, invariant under the rotation by `2π/3` about `c`, `c ∉ S`;
* `Fivefold35`      — 35 points, invariant under the rotation by `2π/5` about `c`, `c ∉ S`;
* `MirrorOneAxis33` — 33 points, invariant under the reflection `reflLine a u`, exactly one
  point of `S` on the mirror;
* `MirrorNoAxis34`  — 34 points, invariant under `reflLine a u`, no point of `S` on the mirror.

`heptagon_of_nontrivial_isometry` derives from them: every finite `S` in general position with
`33 ≤ |S|` that is mapped into itself by a non-identity Euclidean isometry `g` contains 7 points
in convex position.

`halfTurn_of_symmetric_counterexample` is Corollary 3 exactly as written in `SYMMETRIC.md`: it
replaces `HalfTurn34` by `Fourfold32` and concludes that every non-identity symmetry of a
heptagon-free set (≥ 33 points, general position) is a half-turn about a point outside the set,
and that the set has even size ≥ 34.  `mirrorOneAxis33_of_exclusionLine` shows that the existing
Lean theorem `Mir.MirrorExclusionLine` (results/H3, copied verbatim here) supplies
`MirrorOneAxis33`.

`Point = Fin 2 → ℝ` carries the sup metric in Mathlib, so Euclidean isometries are stated with the
explicit squared distance `eDist2`: a Mathlib `Isometry` of `Fin 2 → ℝ` is a sup-norm isometry
(only the eight symmetries of the square, with translations), which would give a weaker theorem.

Proof outline: an isometry of `ℂ` is `z ↦ a z + b` or `z ↦ a z̄ + b` (Mathlib:
`Isometry.affineIsometryOfStrictConvexSpace`, `linear_isometry_complex`).  Finiteness of `S`
(pigeonhole on iterates) rules out translations and glide reflections, makes `a` a root of unity
in the rotation case, and makes `g` an involution, hence `reflLine`, in the reflecting case.
Even order: a power of `g` is the half-turn.  Odd order: a power has prime order `p`; `p = 3, 5`
use the classes after selecting whole orbits (`orbit_select`), `p ≥ 7` gives a regular `p`-gon
orbit, which is concyclic, hence in convex position (`convexPosition_of_concyclic`).  Mirror: at
most two points on the axis (general position), the rest in pairs.

Checked with Lean 4.24.0 and Mathlib `f897ebcf` (the repository's pins), from the repository root:
`lake env lean <this file>`; every declaration is fully proved, axioms
`[propext, Classical.choice, Quot.sound]`.
-/

namespace ErdosSzekeres.SymReduction

open Function Complex

/-! ## 1. Orbits of a map with a fixed period on a finite set -/

section Orbits

variable {α : Type*} [DecidableEq α]

/-- The forward orbit `{x, f x, …, f^[p-1] x}` as a finset. -/
def orbitFS (f : α → α) (p : ℕ) (x : α) : Finset α :=
  (Finset.range p).image (fun i => f^[i] x)

omit [DecidableEq α] in
theorem iterate_mem {f : α → α} {S : Finset α} (hinv : ∀ y ∈ S, f y ∈ S) {x : α}
    (hx : x ∈ S) : ∀ i, f^[i] x ∈ S
  | 0 => hx
  | i + 1 => by
    rw [iterate_succ_apply']
    exact hinv _ (iterate_mem hinv hx i)

theorem card_orbitFS {f : α → α} {p : ℕ} (hp : p.Prime) {x : α} (hper : f^[p] x = x)
    (hfix : f x ≠ x) : (orbitFS f p x).card = p := by
  have hmin : minimalPeriod f x = p := by
    have hdvd : minimalPeriod f x ∣ p := IsPeriodicPt.minimalPeriod_dvd hper
    rcases (Nat.dvd_prime hp).1 hdvd with h | h
    · exact absurd (minimalPeriod_eq_one_iff_isFixedPt.1 h) hfix
    · exact h
  unfold orbitFS
  rw [Finset.card_image_of_injOn, Finset.card_range]
  intro i hi j hj hij
  have hinj := iterate_injOn_Iio_minimalPeriod (f := f) (x := x)
  rw [hmin] at hinj
  exact hinj (by simpa using hi) (by simpa using hj) hij

theorem mem_orbitFS_self {f : α → α} {p : ℕ} (hp : 0 < p) (x : α) : x ∈ orbitFS f p x :=
  Finset.mem_image.2 ⟨0, Finset.mem_range.2 hp, rfl⟩

theorem orbitFS_subset {f : α → α} {p : ℕ} {S : Finset α} (hinv : ∀ y ∈ S, f y ∈ S) {x : α}
    (hx : x ∈ S) : orbitFS f p x ⊆ S := by
  intro y hy
  obtain ⟨i, -, rfl⟩ := Finset.mem_image.1 hy
  exact iterate_mem hinv hx i

theorem orbitFS_invariant {f : α → α} {p : ℕ} (hp : 0 < p) {x : α} (hper : f^[p] x = x) :
    ∀ y ∈ orbitFS f p x, f y ∈ orbitFS f p x := by
  intro y hy
  obtain ⟨i, hi, rfl⟩ := Finset.mem_image.1 hy
  rw [Finset.mem_range] at hi
  rw [← iterate_succ_apply' f i x]
  by_cases h : i + 1 < p
  · exact Finset.mem_image.2 ⟨i + 1, Finset.mem_range.2 h, rfl⟩
  · have hip : i.succ = p := by omega
    rw [hip, hper]
    exact mem_orbitFS_self hp x

theorem card_orbitFS_of_minimalPeriod {f : α → α} {p : ℕ} {x : α}
    (hmin : minimalPeriod f x = p) : (orbitFS f p x).card = p := by
  unfold orbitFS
  rw [Finset.card_image_of_injOn, Finset.card_range]
  intro i hi j hj hij
  have hinj := iterate_injOn_Iio_minimalPeriod (f := f) (x := x)
  rw [hmin] at hinj
  exact hinj (by simpa using hi) (by simpa using hj) hij

/-- **Orbit selection, minimal-period form.** If `f` maps the finite set `S` injectively into
itself and every point of `S` has minimal period `p > 0`, then `p ∣ |S|`, and for every `k` with
`k p ≤ |S|` some `f`-invariant `T ⊆ S` has exactly `k p` points. -/
theorem orbit_select_minimalPeriod {f : α → α} {p : ℕ} (hp : 0 < p) :
    ∀ S : Finset α, (∀ y ∈ S, f y ∈ S) → Set.InjOn f S → (∀ y ∈ S, minimalPeriod f y = p) →
      p ∣ S.card ∧ ∀ k, k * p ≤ S.card → ∃ T ⊆ S, (∀ y ∈ T, f y ∈ T) ∧ T.card = k * p := by
  intro S
  induction S using Finset.strongInduction with
  | H S ih =>
    intro hinv hinj hmin
    have hper : ∀ y ∈ S, f^[p] y = y := fun y hy => by
      rw [← hmin y hy]
      exact iterate_minimalPeriod
    rcases S.eq_empty_or_nonempty with rfl | ⟨x, hx⟩
    · refine ⟨by simp, fun k hk => ⟨∅, Finset.empty_subset _, by simp, ?_⟩⟩
      simp only [Finset.card_empty, nonpos_iff_eq_zero] at hk
      simp [hk]
    · set O := orbitFS f p x with hO
      have hOS : O ⊆ S := orbitFS_subset hinv hx
      have hOcard : O.card = p := card_orbitFS_of_minimalPeriod (hmin x hx)
      have hOinv := orbitFS_invariant hp (hper x hx)
      have hxO : x ∈ O := mem_orbitFS_self hp x
      have hlt : S \ O ⊂ S := Finset.sdiff_ssubset hOS ⟨x, hxO⟩
      have hinv' : ∀ y ∈ S \ O, f y ∈ S \ O := by
        intro y hy
        rw [Finset.mem_sdiff] at hy ⊢
        refine ⟨hinv y hy.1, fun hfy => hy.2 ?_⟩
        obtain ⟨i, hi, hfi⟩ := Finset.mem_image.1 hfy
        rw [Finset.mem_range] at hi
        cases i with
        | zero =>
          have hx' : f (f^[p - 1] x) = x := by
            have hp1 : (p - 1).succ = p := by omega
            rw [← iterate_succ_apply' f (p - 1) x, hp1]
            exact hper x hx
          have hyeq : y = f^[p - 1] x :=
            hinj hy.1 (iterate_mem hinv hx _) (by rw [hx']; exact hfi.symm)
          rw [hyeq]
          exact Finset.mem_image.2 ⟨p - 1, Finset.mem_range.2 (by omega), rfl⟩
        | succ i =>
          have hyeq : y = f^[i] x :=
            hinj hy.1 (iterate_mem hinv hx _) (by rw [← hfi]; exact iterate_succ_apply' f i x)
          rw [hyeq]
          exact Finset.mem_image.2 ⟨i, Finset.mem_range.2 (by omega), rfl⟩
      have hsub : ((S \ O : Finset α) : Set α) ⊆ (S : Set α) := by
        intro y hy
        exact (Finset.mem_sdiff.1 hy).1
      obtain ⟨hdvd', hsel'⟩ := ih (S \ O) hlt hinv' (hinj.mono hsub)
        (fun y hy => hmin y (Finset.mem_sdiff.1 hy).1)
      have hcard : S.card = (S \ O).card + p := by
        have h1 := Finset.card_sdiff_add_card_eq_card hOS
        omega
      refine ⟨?_, ?_⟩
      · rw [hcard]
        exact Nat.dvd_add hdvd' (Nat.dvd_refl p)
      · intro k hk
        rcases k with _ | k
        · exact ⟨∅, Finset.empty_subset _, by simp, by simp⟩
        · obtain ⟨T', hT'S', hT'inv, hT'card⟩ := hsel' k (by
            rw [hcard, add_mul, one_mul] at hk
            omega)
          refine ⟨T' ∪ O, Finset.union_subset (hT'S'.trans Finset.sdiff_subset) hOS, ?_, ?_⟩
          · intro y hy
            rcases Finset.mem_union.1 hy with h | h
            · exact Finset.mem_union_left _ (hT'inv y h)
            · exact Finset.mem_union_right _ (hOinv y h)
          · rw [Finset.card_union_of_disjoint
              (Finset.disjoint_of_subset_left hT'S' Finset.sdiff_disjoint), hT'card, hOcard]
            ring

/-- **Orbit selection.** Let `f` map the finite set `S` injectively into itself, with
`f^[p] = id` on `S` for a prime `p` and no fixed point in `S`. Then `p ∣ |S|`, and for every
`k` with `k p ≤ |S|` there is an `f`-invariant `T ⊆ S` with exactly `k p` points
(a union of `k` orbits). -/
theorem orbit_select {f : α → α} {p : ℕ} (hp : p.Prime) :
    ∀ S : Finset α, (∀ y ∈ S, f y ∈ S) → Set.InjOn f S → (∀ y ∈ S, f^[p] y = y) →
      (∀ y ∈ S, f y ≠ y) →
      p ∣ S.card ∧ ∀ k, k * p ≤ S.card → ∃ T ⊆ S, (∀ y ∈ T, f y ∈ T) ∧ T.card = k * p := by
  intro S
  induction S using Finset.strongInduction with
  | H S ih =>
    intro hinv hinj hper hfree
    rcases S.eq_empty_or_nonempty with rfl | ⟨x, hx⟩
    · refine ⟨by simp, fun k hk => ⟨∅, Finset.empty_subset _, by simp, ?_⟩⟩
      simp only [Finset.card_empty, nonpos_iff_eq_zero] at hk
      simp [hk]
    · set O := orbitFS f p x with hO
      have hOS : O ⊆ S := orbitFS_subset hinv hx
      have hOcard : O.card = p := card_orbitFS hp (hper x hx) (hfree x hx)
      have hOinv := orbitFS_invariant hp.pos (hper x hx)
      have hxO : x ∈ O := mem_orbitFS_self hp.pos x
      have hlt : S \ O ⊂ S := Finset.sdiff_ssubset hOS ⟨x, hxO⟩
      have hinv' : ∀ y ∈ S \ O, f y ∈ S \ O := by
        intro y hy
        rw [Finset.mem_sdiff] at hy ⊢
        refine ⟨hinv y hy.1, fun hfy => hy.2 ?_⟩
        obtain ⟨i, hi, hfi⟩ := Finset.mem_image.1 hfy
        rw [Finset.mem_range] at hi
        cases i with
        | zero =>
          have hx' : f (f^[p - 1] x) = x := by
            have hp1 : (p - 1).succ = p := by have := hp.one_le; omega
            rw [← iterate_succ_apply' f (p - 1) x, hp1]
            exact hper x hx
          have hyeq : y = f^[p - 1] x :=
            hinj hy.1 (iterate_mem hinv hx _) (by rw [hx']; exact hfi.symm)
          rw [hyeq]
          exact Finset.mem_image.2 ⟨p - 1, Finset.mem_range.2 (by have := hp.one_le; omega), rfl⟩
        | succ i =>
          have hyeq : y = f^[i] x :=
            hinj hy.1 (iterate_mem hinv hx _) (by rw [← hfi]; exact iterate_succ_apply' f i x)
          rw [hyeq]
          exact Finset.mem_image.2 ⟨i, Finset.mem_range.2 (by omega), rfl⟩
      have hsub : ((S \ O : Finset α) : Set α) ⊆ (S : Set α) := by
        intro y hy
        exact (Finset.mem_sdiff.1 hy).1
      obtain ⟨hdvd', hsel'⟩ := ih (S \ O) hlt hinv' (hinj.mono hsub)
        (fun y hy => hper y (Finset.mem_sdiff.1 hy).1)
        (fun y hy => hfree y (Finset.mem_sdiff.1 hy).1)
      have hcard : S.card = (S \ O).card + p := by
        have h1 := Finset.card_sdiff_add_card_eq_card hOS
        omega
      refine ⟨?_, ?_⟩
      · rw [hcard]
        exact Nat.dvd_add hdvd' (Nat.dvd_refl p)
      · intro k hk
        rcases k with _ | k
        · exact ⟨∅, Finset.empty_subset _, by simp, by simp⟩
        · obtain ⟨T', hT'S', hT'inv, hT'card⟩ := hsel' k (by
            rw [hcard, add_mul, one_mul] at hk
            omega)
          refine ⟨T' ∪ O, Finset.union_subset (hT'S'.trans Finset.sdiff_subset) hOS, ?_, ?_⟩
          · intro y hy
            rcases Finset.mem_union.1 hy with h | h
            · exact Finset.mem_union_left _ (hT'inv y h)
            · exact Finset.mem_union_right _ (hOinv y h)
          · rw [Finset.card_union_of_disjoint
              (Finset.disjoint_of_subset_left hT'S' Finset.sdiff_disjoint), hT'card, hOcard]
            ring

end Orbits

/-! ## 2. Euclidean structure and complex coordinates -/

/-- Squared Euclidean distance.  (The ambient `dist` on `Point = Fin 2 → ℝ` is the sup metric.) -/
def eDist2 (p q : Point) : ℝ := (p 0 - q 0) ^ 2 + (p 1 - q 1) ^ 2

/-- `g` preserves Euclidean distances. -/
def IsEucIsometry (g : Point → Point) : Prop := ∀ p q, eDist2 (g p) (g q) = eDist2 p q

/-- `f` maps `S` into itself. -/
def Invariant (f : Point → Point) (S : Finset Point) : Prop := ∀ p ∈ S, f p ∈ S

/-- Complex coordinate of a point. -/
def toC (p : Point) : ℂ := ⟨p 0, p 1⟩

/-- The point with complex coordinate `z`. -/
def ofC (z : ℂ) : Point := ![z.re, z.im]

@[simp] theorem toC_re (p : Point) : (toC p).re = p 0 := rfl
@[simp] theorem toC_im (p : Point) : (toC p).im = p 1 := rfl
@[simp] theorem ofC_zero (z : ℂ) : ofC z 0 = z.re := rfl
@[simp] theorem ofC_one (z : ℂ) : ofC z 1 = z.im := rfl

@[simp] theorem toC_ofC (z : ℂ) : toC (ofC z) = z := by
  apply Complex.ext <;> rfl

@[simp] theorem ofC_toC (p : Point) : ofC (toC p) = p := by
  funext i
  fin_cases i <;> rfl

theorem toC_injective : Function.Injective toC := fun p q h => by
  rw [← ofC_toC p, h, ofC_toC]

theorem eDist2_eq_normSq (p q : Point) : eDist2 p q = Complex.normSq (toC p - toC q) := by
  simp [eDist2, Complex.normSq_apply, pow_two]

theorem eDist2_pos_of_ne {p q : Point} (h : p ≠ q) : 0 < eDist2 p q := by
  rw [eDist2_eq_normSq]
  exact Complex.normSq_pos.2 (sub_ne_zero.2 (fun e => h (toC_injective e)))

theorem IsEucIsometry.injective {g : Point → Point} (hg : IsEucIsometry g) :
    Function.Injective g := by
  intro p q h
  by_contra hne
  have := eDist2_pos_of_ne hne
  rw [← hg p q, h] at this
  simp [eDist2] at this

theorem Invariant.iterate {f : Point → Point} {S : Finset Point} (h : Invariant f S) (k : ℕ) :
    Invariant f^[k] S := fun _ hp => iterate_mem h hp k

/-- A Euclidean isometry of `Point`, read in complex coordinates, is an isometry of `ℂ`. -/
theorem isometry_toC_conj {g : Point → Point} (hg : IsEucIsometry g) :
    Isometry (fun z => toC (g (ofC z))) := by
  refine Isometry.of_dist_eq fun z w => ?_
  rw [Complex.dist_eq, Complex.dist_eq, Complex.norm_def, Complex.norm_def,
    ← eDist2_eq_normSq, hg, eDist2_eq_normSq, toC_ofC, toC_ofC]

/-- **Isometries of `ℂ`.** Every isometry is `z ↦ a z + b` or `z ↦ a z̄ + b` with `|a| = 1`.
(Mathlib: `Isometry.affineIsometryOfStrictConvexSpace` and `linear_isometry_complex`.) -/
theorem isometry_complex_cases {G : ℂ → ℂ} (hG : Isometry G) :
    ∃ a b : ℂ, ‖a‖ = 1 ∧ ((∀ z, G z = a * z + b) ∨ (∀ z, G z = a * (starRingEnd ℂ) z + b)) := by
  set F : ℂ →ᵃⁱ[ℝ] ℂ :=
    Isometry.affineIsometryOfStrictConvexSpace (E := ℂ) (F := ℂ) (PE := ℂ) (PF := ℂ) hG with hF
  set L : ℂ ≃ₗᵢ[ℝ] ℂ := F.linearIsometry.toLinearIsometryEquiv rfl with hL
  have hdecomp : ∀ z, G z = L z + G 0 := by
    intro z
    have h := F.map_vadd 0 z
    simp only [vadd_eq_add, add_zero] at h
    have h2 : F z = G z := rfl
    have h3 : F 0 = G 0 := rfl
    rw [h2, h3] at h
    rw [h]
    rfl
  obtain ⟨a, ha⟩ := linear_isometry_complex L
  refine ⟨(a : ℂ), G 0, Circle.norm_coe a, ?_⟩
  rcases ha with ha | ha
  · left
    intro z
    rw [hdecomp z, ha, rotation_apply]
  · right
    intro z
    rw [hdecomp z, ha]
    simp [rotation_apply]

/-! ## 3. Rotations, the half-turn and reflections -/

/-- Rotation about `c` by the complex factor `w` (a rotation when `|w| = 1`). -/
def crot (c w : ℂ) (p : Point) : Point := ofC (c + w * (toC p - c))

@[simp] theorem toC_crot (c w : ℂ) (p : Point) : toC (crot c w p) = c + w * (toC p - c) :=
  toC_ofC _

theorem crot_one (c : ℂ) : crot c 1 = id := by
  funext p
  apply toC_injective
  simp

theorem crot_comp (c w v : ℂ) (p : Point) : crot c w (crot c v p) = crot c (w * v) p := by
  apply toC_injective
  simp only [toC_crot]
  ring

theorem crot_iterate (c w : ℂ) : ∀ k : ℕ, (crot c w)^[k] = crot c (w ^ k)
  | 0 => by simp [crot_one]
  | k + 1 => by
    funext p
    rw [iterate_succ_apply', crot_iterate c w k, crot_comp, pow_succ']

theorem crot_eq_self_iff {c w : ℂ} (hw : w ≠ 1) (p : Point) : crot c w p = p ↔ toC p = c := by
  constructor
  · intro h
    have h' := congrArg toC h
    rw [toC_crot] at h'
    have h2 : (w - 1) * (toC p - c) = 0 := by linear_combination h'
    rcases mul_eq_zero.1 h2 with h1 | h1
    · exact absurd (sub_eq_zero.1 h1) hw
    · exact sub_eq_zero.1 h1
  · intro h
    apply toC_injective
    rw [toC_crot, h]
    ring

theorem crot_injective {c w : ℂ} (hw : w ≠ 0) : Function.Injective (crot c w) := by
  intro p q h
  have h' := congrArg toC h
  simp only [toC_crot] at h'
  apply toC_injective
  have h2 : w * (toC p - toC q) = 0 := by linear_combination h'
  rcases mul_eq_zero.1 h2 with h1 | h1
  · exact absurd h1 hw
  · exact sub_eq_zero.1 h1

theorem eDist2_crot_center {c w : ℂ} (hw : Complex.normSq w = 1) (p : Point) :
    eDist2 (crot c w p) (ofC c) = eDist2 p (ofC c) := by
  rw [eDist2_eq_normSq, eDist2_eq_normSq, toC_crot, toC_ofC]
  rw [show c + w * (toC p - c) - c = w * (toC p - c) by ring, Complex.normSq_mul, hw, one_mul]

/-- Rotation about `c` by the angle `θ`, in coordinates. -/
noncomputable def rotAbout (c : Point) (θ : ℝ) (p : Point) : Point :=
  ![c 0 + Real.cos θ * (p 0 - c 0) - Real.sin θ * (p 1 - c 1),
    c 1 + Real.sin θ * (p 0 - c 0) + Real.cos θ * (p 1 - c 1)]

theorem rotAbout_eq_crot (c : Point) (θ : ℝ) :
    rotAbout c θ = crot (toC c) (Complex.exp (θ * Complex.I)) := by
  funext p
  apply toC_injective
  rw [toC_crot]
  apply Complex.ext <;>
    simp [rotAbout, Complex.exp_ofReal_mul_I_re, Complex.exp_ofReal_mul_I_im] <;> ring

/-- The half-turn (point reflection) about `c`. -/
def halfTurn (c p : Point) : Point := ![2 * c 0 - p 0, 2 * c 1 - p 1]

theorem halfTurn_eq_crot (c : Point) : halfTurn c = crot (toC c) (-1) := by
  funext p
  apply toC_injective
  rw [toC_crot]
  apply Complex.ext <;> simp [halfTurn] <;> ring

/-- The reflection in the line through `a` with direction `u` (`u₀² + u₁² = 1`); the same
definition as `Mir.reflLine` in `results/H3/MirrorEncoding/Line.lean`. -/
def reflLine (a u : Point) (p : Point) : Point :=
  let d := (p 0 - a 0) * u 0 + (p 1 - a 1) * u 1
  ![a 0 + 2 * d * u 0 - (p 0 - a 0), a 1 + 2 * d * u 1 - (p 1 - a 1)]

theorem toC_reflLine {a u : Point} (hu : u 0 ^ 2 + u 1 ^ 2 = 1) (p : Point) :
    toC (reflLine a u p) = toC a + toC u ^ 2 * (starRingEnd ℂ) (toC p - toC a) := by
  apply Complex.ext
  · simp [reflLine, pow_two]
    linear_combination (p 0 - a 0) * hu
  · simp [reflLine, pow_two]
    linear_combination (p 1 - a 1) * hu

theorem reflLine_involutive {a u : Point} (hu : u 0 ^ 2 + u 1 ^ 2 = 1) (p : Point) :
    reflLine a u (reflLine a u p) = p := by
  have hn : Complex.normSq (toC u) = 1 := by
    rw [Complex.normSq_apply]; simpa [pow_two] using hu
  have hc : toC u * (starRingEnd ℂ) (toC u) = 1 := by
    rw [Complex.mul_conj, hn]; simp
  apply toC_injective
  rw [toC_reflLine hu, toC_reflLine hu]
  simp only [map_sub, map_add, map_mul, map_pow, Complex.conj_conj]
  linear_combination (toC p - toC a) * (toC u * (starRingEnd ℂ) (toC u) + 1) * hc

/-- A fixed point of `reflLine a u` lies on the mirror: `(p - a) × u = 0`. -/
theorem cross_of_reflLine_fixed {a u p : Point} (h : reflLine a u p = p) :
    (p 0 - a 0) * u 1 - (p 1 - a 1) * u 0 = 0 := by
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  simp only [reflLine, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
  linear_combination (-(u 1) / 2) * h0 + (u 0 / 2) * h1

/-- Three points on one line `a + ℝ u` (`|u| = 1`) have zero orientation. -/
theorem orient_eq_zero_of_cross {a u p q r : Point} (hu : u 0 ^ 2 + u 1 ^ 2 = 1)
    (hp : (p 0 - a 0) * u 1 - (p 1 - a 1) * u 0 = 0)
    (hq : (q 0 - a 0) * u 1 - (q 1 - a 1) * u 0 = 0)
    (hr : (r 0 - a 0) * u 1 - (r 1 - a 1) * u 0 = 0) : orient p q r = 0 := by
  unfold orient
  linear_combination ((r 0 - p 0) * u 0 + (r 1 - p 1) * u 1) * (hq - hp)
    - ((q 0 - p 0) * u 0 + (q 1 - p 1) * u 1) * (hr - hp)
    - ((q 0 - p 0) * (r 1 - p 1) - (q 1 - p 1) * (r 0 - p 0)) * hu

/-! ## 4. The case classes -/

/-- Half-turn symmetric, 34 points, centre not in the set. -/
def HalfTurn34 : Prop :=
  ∀ (S : Finset Point) (c : Point), GeneralPosition S → S.card = 34 → c ∉ S →
    Invariant (halfTurn c) S → HasConvexNGon 7 S

/-- Threefold symmetric, 33 points, centre not in the set. -/
def Threefold33 : Prop :=
  ∀ (S : Finset Point) (c : Point), GeneralPosition S → S.card = 33 → c ∉ S →
    Invariant (rotAbout c (2 * Real.pi / 3)) S → HasConvexNGon 7 S

/-- Fivefold symmetric, 35 points, centre not in the set. -/
def Fivefold35 : Prop :=
  ∀ (S : Finset Point) (c : Point), GeneralPosition S → S.card = 35 → c ∉ S →
    Invariant (rotAbout c (2 * Real.pi / 5)) S → HasConvexNGon 7 S

/-- Mirror symmetric, 33 points, exactly one point on the mirror. -/
def MirrorOneAxis33 : Prop :=
  ∀ (S : Finset Point) (a u : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
    S.card = 33 → Invariant (reflLine a u) S →
    (∃ x ∈ S, reflLine a u x = x ∧ ∀ y ∈ S, reflLine a u y = y → y = x) → HasConvexNGon 7 S

/-- Mirror symmetric, 34 points, no point on the mirror. -/
def MirrorNoAxis34 : Prop :=
  ∀ (S : Finset Point) (a u : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
    S.card = 34 → Invariant (reflLine a u) S → (∀ p ∈ S, reflLine a u p ≠ p) →
    HasConvexNGon 7 S

/-- Fourfold symmetric, 32 points, centre not in the set (only used by the variant
`halfTurn_of_symmetric_counterexample`; credited to arXiv:2506.00224 §6.2, certified in
`results/C4CUT`). -/
def Fourfold32 : Prop :=
  ∀ (S : Finset Point) (c : Point), GeneralPosition S → S.card = 32 → c ∉ S →
    Invariant (rotAbout c (2 * Real.pi / 4)) S → HasConvexNGon 7 S

/-! ## 5. Elementary geometric lemmas -/

theorem point_ext {p q : Point} (h0 : p 0 = q 0) (h1 : p 1 = q 1) : p = q := by
  funext i
  fin_cases i
  · exact h0
  · exact h1

/-- **Concyclic points are in convex position** (strict supporting line: the tangent). -/
theorem convexPosition_of_concyclic (s : Finset Point) (c : Point) (r : ℝ)
    (hs : ∀ p ∈ s, eDist2 p c = r) : ConvexPosition s := by
  apply Suk.convexPosition_of_strict_supports
  intro p hp
  refine ⟨![p 0 - (p 1 - c 1), p 1 + (p 0 - c 0)], ?_⟩
  intro q hq hqp
  have hp' := hs p hp
  have hq' := hs q hq
  have hpos := eDist2_pos_of_ne hqp
  unfold eDist2 at hp' hq' hpos
  simp only [orient, Matrix.cons_val_zero, Matrix.cons_val_one]
  nlinarith

theorem hasConvexNGon_of_concyclic {S T : Finset Point} (hT : T ⊆ S) (c : Point) (r : ℝ)
    (hconc : ∀ p ∈ T, eDist2 p c = r) {n : ℕ} (hn : n ≤ T.card) : HasConvexNGon n S :=
  ((convexPosition_of_concyclic T c r hconc).hasConvexNGon hn).mono hT

/-- In general position, the centre of a half-turn is not a point of an invariant set with at
least two points (it would be collinear with every antipodal pair). -/
theorem center_not_mem_of_halfTurn {S : Finset Point} {c : Point} (hgp : GeneralPosition S)
    (hS : 2 ≤ S.card) (hinv : Invariant (halfTurn c) S) : c ∉ S := by
  intro hc
  obtain ⟨q, hq, hqc⟩ := Finset.exists_mem_ne (by omega : 1 < S.card) c
  have key : halfTurn c q = q ∨ halfTurn c q = c → q = c := by
    intro h
    rcases h with h | h
    · have h0 := congrFun h 0
      have h1 := congrFun h 1
      simp only [halfTurn, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
      exact point_ext (by linarith) (by linarith)
    · have h0 := congrFun h 0
      have h1 := congrFun h 1
      simp only [halfTurn, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
      exact point_ext (by linarith) (by linarith)
  have hne1 : q ≠ halfTurn c q := fun h => hqc (key (Or.inl h.symm))
  have hne2 : c ≠ halfTurn c q := fun h => hqc (key (Or.inr h.symm))
  apply (generalPosition_iff_orient_ne_zero S).1 hgp q hq c hc (halfTurn c q) (hinv q hq)
    hqc hne1 hne2
  simp only [orient, halfTurn, Matrix.cons_val_zero, Matrix.cons_val_one]
  ring

/-! ## 6. Roots of unity -/

theorem root_cases {a : ℂ} {m : ℕ} (hm : 0 < m) (ham : a ^ m = 1) (ha1 : a ≠ 1) :
    (∃ k, a ^ k = -1) ∨ ∃ p k, p.Prime ∧ p ≠ 2 ∧ IsPrimitiveRoot (a ^ k) p := by
  have hfin : IsOfFinOrder a := isOfFinOrder_iff_pow_eq_one.2 ⟨m, hm, ham⟩
  have hnpos : 0 < orderOf a := hfin.orderOf_pos
  have hprim : IsPrimitiveRoot a (orderOf a) := IsPrimitiveRoot.orderOf a
  have hn1 : orderOf a ≠ 1 := fun h => ha1 (orderOf_eq_one_iff.1 h)
  by_cases heven : 2 ∣ orderOf a
  · left
    obtain ⟨k, hk⟩ := heven
    refine ⟨k, ?_⟩
    have h2 : IsPrimitiveRoot (a ^ k) 2 := hprim.pow hnpos (by rw [hk]; ring)
    exact h2.eq_neg_one_of_two_right
  · right
    refine ⟨(orderOf a).minFac, orderOf a / (orderOf a).minFac, Nat.minFac_prime hn1, ?_, ?_⟩
    · intro h2
      apply heven
      rw [← h2]
      exact Nat.minFac_dvd _
    · exact hprim.pow hnpos (Nat.div_mul_cancel (Nat.minFac_dvd _)).symm

theorem prime_cases {p : ℕ} (hp : p.Prime) (h2 : p ≠ 2) : p = 3 ∨ p = 5 ∨ 7 ≤ p := by
  have h2le := hp.two_le
  rcases (by omega : p = 2 ∨ p = 3 ∨ p = 4 ∨ p = 5 ∨ p = 6 ∨ 7 ≤ p) with h | h | h | h | h | h
  · exact absurd h h2
  · exact Or.inl h
  · subst h
    exact absurd hp (Nat.not_prime_mul (a := 2) (b := 2) (by norm_num) (by norm_num))
  · exact Or.inr (Or.inl h)
  · subst h
    exact absurd hp (Nat.not_prime_mul (a := 2) (b := 3) (by norm_num) (by norm_num))
  · exact Or.inr (Or.inr h)

theorem isPrimitiveRoot_rot3 :
    IsPrimitiveRoot (Complex.exp (↑(2 * Real.pi / 3) * Complex.I)) 3 := by
  have h := Complex.isPrimitiveRoot_exp 3 (by norm_num)
  convert h using 2
  push_cast
  ring

theorem isPrimitiveRoot_rot5 :
    IsPrimitiveRoot (Complex.exp (↑(2 * Real.pi / 5) * Complex.I)) 5 := by
  have h := Complex.isPrimitiveRoot_exp 5 (by norm_num)
  convert h using 2
  push_cast
  ring

theorem isPrimitiveRoot_rot4 :
    IsPrimitiveRoot (Complex.exp (↑(2 * Real.pi / 4) * Complex.I)) 4 := by
  have h := Complex.isPrimitiveRoot_exp 4 (by norm_num)
  convert h using 2
  push_cast
  ring

/-- The order of a nontrivial root of unity is `2`, divisible by `4`, or has an odd prime
factor. -/
theorem root_cases2 {a : ℂ} {m : ℕ} (hm : 0 < m) (ham : a ^ m = 1) (ha1 : a ≠ 1) :
    a = -1 ∨ (∃ k, IsPrimitiveRoot (a ^ k) 4) ∨
      ∃ p k, p.Prime ∧ p ≠ 2 ∧ IsPrimitiveRoot (a ^ k) p := by
  have hfin : IsOfFinOrder a := isOfFinOrder_iff_pow_eq_one.2 ⟨m, hm, ham⟩
  have hnpos : 0 < orderOf a := hfin.orderOf_pos
  have hprim : IsPrimitiveRoot a (orderOf a) := IsPrimitiveRoot.orderOf a
  have hn1 : orderOf a ≠ 1 := fun h => ha1 (orderOf_eq_one_iff.1 h)
  by_cases hodd : ∃ p, p.Prime ∧ p ≠ 2 ∧ p ∣ orderOf a
  · obtain ⟨p, hp, hp2, hpn⟩ := hodd
    exact Or.inr (Or.inr ⟨p, orderOf a / p, hp, hp2,
      hprim.pow hnpos (Nat.div_mul_cancel hpn).symm⟩)
  · push_neg at hodd
    by_cases h4 : 4 ∣ orderOf a
    · exact Or.inr (Or.inl ⟨orderOf a / 4, hprim.pow hnpos (Nat.div_mul_cancel h4).symm⟩)
    · left
      have h2 : 2 ∣ orderOf a := by
        by_contra h
        exact hodd _ (Nat.minFac_prime hn1) (fun e => h (e ▸ Nat.minFac_dvd _))
          (Nat.minFac_dvd _)
      obtain ⟨m', hm'⟩ := h2
      have hm'1 : m' = 1 := by
        by_contra hm1
        have hq := Nat.minFac_prime hm1
        have hqd : m'.minFac ∣ orderOf a := by
          rw [hm']
          exact Dvd.dvd.mul_left (Nat.minFac_dvd m') 2
        have hq2 : m'.minFac = 2 := by
          by_contra h
          exact hodd _ hq h hqd
        have h2m : 2 ∣ m' := hq2 ▸ Nat.minFac_dvd m'
        apply h4
        rw [hm']
        exact Nat.mul_dvd_mul_left 2 h2m
      have hn2 : orderOf a = 2 := by rw [hm', hm'1]
      exact (hn2 ▸ hprim : IsPrimitiveRoot a 2).eq_neg_one_of_two_right

/-! ## 7. The cases -/

/-- A half-turn symmetric set in general position (≥ 2 points) avoids the centre, has even
size, and contains invariant subsets of every even size up to `|S|`. -/
theorem halfTurn_facts {S : Finset Point} {c : Point} (hgp : GeneralPosition S)
    (hS : 2 ≤ S.card) (hinv : Invariant (halfTurn c) S) :
    c ∉ S ∧ 2 ∣ S.card ∧ ∀ k, k * 2 ≤ S.card →
      ∃ T ⊆ S, Invariant (halfTurn c) T ∧ T.card = k * 2 := by
  classical
  have hcS : c ∉ S := center_not_mem_of_halfTurn hgp hS hinv
  have hf : halfTurn c = crot (toC c) (-1) := halfTurn_eq_crot c
  have hper : ∀ y ∈ S, (halfTurn c)^[2] y = y := by
    intro y _
    rw [hf, crot_iterate, neg_one_sq, crot_one]
    rfl
  have hfree : ∀ y ∈ S, halfTurn c y ≠ y := by
    intro y hy h
    rw [hf, crot_eq_self_iff (by norm_num)] at h
    apply hcS
    rw [← toC_injective h]
    exact hy
  have hinj : Set.InjOn (halfTurn c) S := by
    rw [hf]
    exact (crot_injective (by norm_num)).injOn
  obtain ⟨hdvd, hsel⟩ := orbit_select Nat.prime_two S hinv hinj hper hfree
  exact ⟨hcS, hdvd, hsel⟩

theorem case_halfTurn (h2 : HalfTurn34) {S : Finset Point} {c : Point} (hgp : GeneralPosition S)
    (hcard : 33 ≤ S.card) (hinv : Invariant (halfTurn c) S) : HasConvexNGon 7 S := by
  obtain ⟨hcS, hdvd, hsel⟩ := halfTurn_facts hgp (by omega) hinv
  obtain ⟨T, hTS, hTinv, hTcard⟩ := hsel 17 (by omega)
  exact (h2 T c (hgp.mono hTS) (by omega) (fun h => hcS (hTS h)) hTinv).mono hTS

theorem rot_erase_facts {S : Finset Point} {c w : ℂ} {p : ℕ} (hp : p.Prime)
    (hw : w ^ p = 1) (hw1 : w ≠ 1) (hinv : Invariant (crot c w) S) :
    p ∣ (S.erase (ofC c)).card ∧ ∀ k, k * p ≤ (S.erase (ofC c)).card →
      ∃ T ⊆ S, ofC c ∉ T ∧ Invariant (crot c w) T ∧ T.card = k * p := by
  classical
  have hw0 : w ≠ 0 := by
    rintro rfl
    rw [zero_pow hp.ne_zero] at hw
    exact zero_ne_one hw
  have hinv₀ : ∀ y ∈ S.erase (ofC c), crot c w y ∈ S.erase (ofC c) := by
    intro y hy
    rw [Finset.mem_erase] at hy ⊢
    refine ⟨?_, hinv y hy.2⟩
    intro h
    apply hy.1
    apply crot_injective hw0
    rw [h]
    apply toC_injective
    simp
  have hper : ∀ y ∈ S.erase (ofC c), (crot c w)^[p] y = y := by
    intro y _
    rw [crot_iterate, hw, crot_one]
    rfl
  have hfree : ∀ y ∈ S.erase (ofC c), crot c w y ≠ y := by
    intro y hy h
    rw [crot_eq_self_iff hw1] at h
    exact (Finset.mem_erase.1 hy).1 (by rw [← h, ofC_toC])
  obtain ⟨hdvd, hsel⟩ := orbit_select hp _ hinv₀ (crot_injective hw0).injOn hper hfree
  refine ⟨hdvd, fun k hk => ?_⟩
  obtain ⟨T, hTS, hTinv, hTcard⟩ := hsel k hk
  exact ⟨T, hTS.trans (Finset.erase_subset _ _), fun h => (Finset.mem_erase.1 (hTS h)).1 rfl,
    hTinv, hTcard⟩

/-- A rotation of prime order `p ≥ 7`: any non-central orbit is a regular `p`-gon, hence a
convex heptagon. -/
theorem case_rot_big {S : Finset Point} {c w : ℂ} {p : ℕ} (hp : p.Prime) (h7 : 7 ≤ p)
    (hw : w ^ p = 1) (hw1 : w ≠ 1) (hinv : Invariant (crot c w) S) (hS : 2 ≤ S.card) :
    HasConvexNGon 7 S := by
  classical
  obtain ⟨q, hq, hqc⟩ := Finset.exists_mem_ne (by omega : 1 < S.card) (ofC c)
  have hnw : Complex.normSq w = 1 := by
    have h1 : Complex.normSq w ^ p = 1 := by rw [← map_pow, hw, map_one]
    exact (pow_eq_one_iff_of_nonneg (Complex.normSq_nonneg w) hp.ne_zero).1 h1
  have hOS : orbitFS (crot c w) p q ⊆ S := orbitFS_subset hinv hq
  have hper : (crot c w)^[p] q = q := by
    rw [crot_iterate, hw, crot_one]
    rfl
  have hfix : crot c w q ≠ q := by
    intro h
    rw [crot_eq_self_iff hw1] at h
    exact hqc (by rw [← h, ofC_toC])
  have hOcard : (orbitFS (crot c w) p q).card = p := card_orbitFS hp hper hfix
  have hconc : ∀ x ∈ orbitFS (crot c w) p q, eDist2 x (ofC c) = eDist2 q (ofC c) := by
    intro x hx
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.1 hx
    rw [crot_iterate]
    exact eDist2_crot_center (by rw [map_pow, hnw, one_pow]) q
  exact hasConvexNGon_of_concyclic hOS (ofC c) _ hconc (by omega)

/-- A rotation of odd prime order: threefold, fivefold, or order ≥ 7. -/
theorem case_odd_prime (h3 : Threefold33) (h5 : Fivefold35) {S : Finset Point} {c w : ℂ}
    {p : ℕ} (hgp : GeneralPosition S) (hcard : 33 ≤ S.card) (hp : p.Prime) (hp2 : p ≠ 2)
    (hprim : IsPrimitiveRoot w p) (hinvw : Invariant (crot c w) S) : HasConvexNGon 7 S := by
  have hw : w ^ p = 1 := hprim.pow_eq_one
  have hw1 : w ≠ 1 := hprim.ne_one hp.one_lt
  have hlow : S.card - 1 ≤ (S.erase (ofC c)).card := Finset.pred_card_le_card_erase
  rcases prime_cases hp hp2 with rfl | rfl | h7
  · -- threefold: keep 11 non-central orbits
    obtain ⟨hdvd, hsel⟩ := rot_erase_facts Nat.prime_three hw hw1 hinvw
    obtain ⟨T, hTS, hcT, hTinv, hTcard⟩ := hsel 11 (by omega)
    obtain ⟨e, -, he⟩ := hprim.eq_pow_of_pow_eq_one isPrimitiveRoot_rot3.pow_eq_one
    have hTinv' : Invariant (rotAbout (ofC c) (2 * Real.pi / 3)) T := by
      rw [rotAbout_eq_crot, toC_ofC, ← he, ← crot_iterate]
      exact hTinv.iterate e
    exact (h3 T (ofC c) (hgp.mono hTS) (by omega) hcT hTinv').mono hTS
  · -- fivefold: keep 7 non-central orbits
    obtain ⟨hdvd, hsel⟩ := rot_erase_facts Nat.prime_five hw hw1 hinvw
    obtain ⟨T, hTS, hcT, hTinv, hTcard⟩ := hsel 7 (by omega)
    obtain ⟨e, -, he⟩ := hprim.eq_pow_of_pow_eq_one isPrimitiveRoot_rot5.pow_eq_one
    have hTinv' : Invariant (rotAbout (ofC c) (2 * Real.pi / 5)) T := by
      rw [rotAbout_eq_crot, toC_ofC, ← he, ← crot_iterate]
      exact hTinv.iterate e
    exact (h5 T (ofC c) (hgp.mono hTS) (by omega) hcT hTinv').mono hTS
  · exact case_rot_big hp h7 hw hw1 hinvw (by omega)

/-- A rotation of order 4: the centre is excluded by general position (its square is the
half-turn); keep 8 orbits. -/
theorem case_fourfold (h4 : Fourfold32) {S : Finset Point} {c w : ℂ} (hgp : GeneralPosition S)
    (hcard : 33 ≤ S.card) (hprim : IsPrimitiveRoot w 4) (hinvw : Invariant (crot c w) S) :
    HasConvexNGon 7 S := by
  classical
  have hw4 : w ^ 4 = 1 := hprim.pow_eq_one
  have hw1 : w ≠ 1 := hprim.ne_one (by norm_num)
  have hw0 : w ≠ 0 := hprim.ne_zero (by norm_num)
  have hw2 : w ^ 2 = -1 :=
    (hprim.pow (by norm_num) (by norm_num : 4 = 2 * 2)).eq_neg_one_of_two_right
  have hinvH : Invariant (halfTurn (ofC c)) S := by
    have h := hinvw.iterate 2
    rw [crot_iterate, hw2] at h
    rw [halfTurn_eq_crot, toC_ofC]
    exact h
  have hcS : ofC c ∉ S := center_not_mem_of_halfTurn hgp (by omega) hinvH
  have hmin : ∀ y ∈ S, minimalPeriod (crot c w) y = 4 := by
    intro y hy
    have hyc : toC y ≠ c := fun h => hcS (by rw [← h, ofC_toC]; exact hy)
    have hper : IsPeriodicPt (crot c w) 4 y := by
      change (crot c w)^[4] y = y
      rw [crot_iterate, hw4, crot_one]
      rfl
    have hne1 : minimalPeriod (crot c w) y ≠ 1 := by
      intro h
      rw [minimalPeriod_eq_one_iff_isFixedPt] at h
      exact hyc ((crot_eq_self_iff hw1 y).1 h)
    have hne2 : minimalPeriod (crot c w) y ≠ 2 := by
      intro h
      have h2 : (crot c w)^[2] y = y := by
        rw [← h]
        exact iterate_minimalPeriod
      rw [crot_iterate, hw2] at h2
      exact hyc ((crot_eq_self_iff (by norm_num) y).1 h2)
    obtain ⟨i, hi, hd⟩ := (Nat.dvd_prime_pow Nat.prime_two).1
      (show minimalPeriod (crot c w) y ∣ 2 ^ 2 from hper.minimalPeriod_dvd)
    interval_cases i
    · exact absurd (by simpa using hd) hne1
    · exact absurd (by simpa using hd) hne2
    · simpa using hd
  obtain ⟨hdvd, hsel⟩ :=
    orbit_select_minimalPeriod (by norm_num) S hinvw (crot_injective hw0).injOn hmin
  obtain ⟨T, hTS, hTinv, hTcard⟩ := hsel 8 (by omega)
  obtain ⟨e, -, he⟩ := hprim.eq_pow_of_pow_eq_one isPrimitiveRoot_rot4.pow_eq_one
  have hTinv' : Invariant (rotAbout (ofC c) (2 * Real.pi / 4)) T := by
    rw [rotAbout_eq_crot, toC_ofC, ← he, ← crot_iterate]
    exact Invariant.iterate hTinv e
  exact (h4 T (ofC c) (hgp.mono hTS) (by omega) (fun h => hcS (hTS h)) hTinv').mono hTS

theorem case_mirror (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34) {S : Finset Point}
    {a u : Point} (hu : u 0 ^ 2 + u 1 ^ 2 = 1) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hinv : Invariant (reflLine a u) S) : HasConvexNGon 7 S := by
  classical
  have hFM : (S.filter (fun p => reflLine a u p = p)).card +
      (S.filter (fun p => ¬ reflLine a u p = p)).card = S.card :=
    Finset.filter_card_add_filter_neg_card_eq_card _
  have hF2 : (S.filter (fun p => reflLine a u p = p)).card ≤ 2 := by
    by_contra h
    push_neg at h
    obtain ⟨x, hx, y, hy, z, hz, hxy, hxz, hyz⟩ := Finset.two_lt_card.1 h
    rw [Finset.mem_filter] at hx hy hz
    exact (generalPosition_iff_orient_ne_zero S).1 hgp x hx.1 y hy.1 z hz.1 hxy hxz hyz
      (orient_eq_zero_of_cross hu (cross_of_reflLine_fixed hx.2) (cross_of_reflLine_fixed hy.2)
        (cross_of_reflLine_fixed hz.2))
  have hinvol : ∀ p, reflLine a u (reflLine a u p) = p := reflLine_involutive hu
  have hinjf : Function.Injective (reflLine a u) := fun p q h => by
    rw [← hinvol p, h, hinvol q]
  set M := S.filter (fun p => ¬ reflLine a u p = p) with hM
  have hMinv : ∀ y ∈ M, reflLine a u y ∈ M := by
    intro y hy
    rw [Finset.mem_filter] at hy ⊢
    refine ⟨hinv y hy.1, fun h => hy.2 ?_⟩
    rw [hinvol] at h
    exact h.symm
  have hMper : ∀ y ∈ M, (reflLine a u)^[2] y = y := fun y _ => hinvol y
  have hMfree : ∀ y ∈ M, reflLine a u y ≠ y := fun y hy => (Finset.mem_filter.1 hy).2
  obtain ⟨hdvd, hsel⟩ := orbit_select Nat.prime_two M hMinv hinjf.injOn hMper hMfree
  by_cases hF0 : (S.filter (fun p => reflLine a u p = p)).card = 0
  · obtain ⟨T, hTM, hTinv, hTcard⟩ := hsel 17 (by omega)
    have hTS : T ⊆ S := hTM.trans (Finset.filter_subset _ _)
    exact (hm0 T a u hu (hgp.mono hTS) (by omega) hTinv
      (fun p hp => (Finset.mem_filter.1 (hTM hp)).2)).mono hTS
  · obtain ⟨x, hx⟩ := Finset.card_pos.1 (Nat.pos_of_ne_zero hF0)
    rw [Finset.mem_filter] at hx
    obtain ⟨T, hTM, hTinv, hTcard⟩ := hsel 16 (by omega)
    have hxT : x ∉ T := fun h => (Finset.mem_filter.1 (hTM h)).2 hx.2
    have hT'S : insert x T ⊆ S :=
      Finset.insert_subset hx.1 (hTM.trans (Finset.filter_subset _ _))
    refine (hm1 (insert x T) a u hu (hgp.mono hT'S) ?_ ?_
      ⟨x, Finset.mem_insert_self _ _, hx.2, ?_⟩).mono hT'S
    · rw [Finset.card_insert_of_notMem hxT, hTcard]
    · intro y hy
      rcases Finset.mem_insert.1 hy with rfl | h
      · rw [hx.2]
        exact Finset.mem_insert_self _ _
      · exact Finset.mem_insert_of_mem (hTinv y h)
    · intro y hy hfy
      rcases Finset.mem_insert.1 hy with rfl | h
      · rfl
      · exact absurd hfy (Finset.mem_filter.1 (hTM h)).2

/-! ## 8. Finite-order isometries and the reduction -/

/-- **Structure of a symmetry of a finite set.** A Euclidean isometry `g ≠ id` that maps a
finite set with at least two points into itself is either a rotation `crot c a` with `a ≠ 1`
a root of unity, or a reflection `reflLine A u` with `|u| = 1`. (Translations and glide
reflections are excluded by finiteness.) -/
theorem isometry_structure {S : Finset Point} {g : Point → Point} (hS : 1 < S.card)
    (hg : IsEucIsometry g) (hne : g ≠ id) (hinv : Invariant g S) :
    (∃ c a : ℂ, g = crot c a ∧ a ≠ 1 ∧ ∃ m, 0 < m ∧ a ^ m = 1) ∨
      (∃ A u : Point, u 0 ^ 2 + u 1 ^ 2 = 1 ∧ g = reflLine A u) := by
  classical
  obtain ⟨a, b, ha, hcases⟩ := isometry_complex_cases (isometry_toC_conj hg)
  have pigeon : ∀ f : Point → Point, Invariant f S → ∀ q ∈ S,
      ∃ i j, i < j ∧ f^[i] q = f^[j] q := by
    intro f hf q hq
    exact Set.Finite.exists_lt_map_eq_of_forall_mem (t := (S : Set Point))
      (f := fun k => f^[k] q) (fun k => iterate_mem hf hq k) S.finite_toSet
  have nat_cast_ne : ∀ i j : ℕ, i < j → ((j : ℂ) - i) ≠ 0 := by
    intro i j hij h
    have h' : (j : ℂ) = i := sub_eq_zero.1 h
    exact absurd (by exact_mod_cast h' : j = i) (Nat.ne_of_gt hij)
  rcases hcases with hrot | hrefl
  · -- orientation preserving
    have hgC : ∀ p, toC (g p) = a * toC p + b := by
      intro p
      have := hrot (toC p)
      simpa using this
    by_cases ha1 : a = 1
    · -- a translation: only the identity preserves a finite nonempty set
      exfalso
      apply hne
      obtain ⟨q, hq⟩ := Finset.card_pos.1 (by omega : 0 < S.card)
      have hiter : ∀ k : ℕ, toC (g^[k] q) = toC q + k * b := by
        intro k
        induction k with
        | zero => simp
        | succ k ih =>
          rw [iterate_succ_apply', hgC, ih, ha1]
          push_cast
          ring
      obtain ⟨i, j, hij, heq⟩ := pigeon g hinv q hq
      have hb : b = 0 := by
        have h := congrArg toC heq
        rw [hiter, hiter] at h
        have h' : ((j : ℂ) - i) * b = 0 := by linear_combination -h
        exact (mul_eq_zero.1 h').resolve_left (nat_cast_ne i j hij)
      funext p
      apply toC_injective
      rw [hgC, ha1, hb]
      simp
    · -- a rotation about `c = b / (1 - a)`, of finite order
      left
      have h1a : (1 : ℂ) - a ≠ 0 := sub_ne_zero.2 (Ne.symm ha1)
      set c : ℂ := b / (1 - a) with hc
      have hgrot : g = crot c a := by
        funext p
        apply toC_injective
        rw [hgC, toC_crot, hc]
        field_simp
        ring
      have ha0 : a ≠ 0 := by
        intro h
        rw [h, norm_zero] at ha
        exact zero_ne_one ha
      rw [hgrot] at hinv
      obtain ⟨q, hq, hqc⟩ := Finset.exists_mem_ne hS (ofC c)
      obtain ⟨i, j, hij, heq⟩ := pigeon _ hinv q hq
      have ham : a ^ (j - i) = 1 := by
        rw [crot_iterate, crot_iterate] at heq
        have h := congrArg toC heq
        simp only [toC_crot] at h
        have hz : toC q - c ≠ 0 := by
          intro h0
          apply hqc
          rw [← sub_eq_zero.1 h0, ofC_toC]
        have h' : a ^ i * (toC q - c) = a ^ j * (toC q - c) := by linear_combination h
        have h'' : a ^ i = a ^ j := mul_right_cancel₀ hz h'
        have hsplit : a ^ j = a ^ i * a ^ (j - i) := by
          rw [← pow_add, Nat.add_sub_cancel' hij.le]
        rw [hsplit] at h''
        exact (mul_eq_left₀ (pow_ne_zero _ ha0)).1 h''.symm
      exact ⟨c, a, hgrot, ha1, j - i, Nat.sub_pos_of_lt hij, ham⟩
  · -- orientation reversing: `g ∘ g` is a translation, hence the identity, and `g` a reflection
    right
    have hgC : ∀ p, toC (g p) = a * (starRingEnd ℂ) (toC p) + b := by
      intro p
      have := hrefl (toC p)
      simpa using this
    have hconj : a * (starRingEnd ℂ) a = 1 := by
      rw [Complex.mul_conj, Complex.normSq_eq_norm_sq, ha]
      simp
    have hgg : ∀ p, toC (g (g p)) = toC p + (a * (starRingEnd ℂ) b + b) := by
      intro p
      rw [hgC, hgC]
      simp only [map_add, map_mul, Complex.conj_conj]
      linear_combination (toC p) * hconj
    have hiter : ∀ k : ℕ, ∀ p,
        toC ((g ∘ g)^[k] p) = toC p + k * (a * (starRingEnd ℂ) b + b) := by
      intro k
      induction k with
      | zero => intro p; simp
      | succ k ih =>
        intro p
        rw [iterate_succ_apply', comp_apply, hgg, ih]
        push_cast
        ring
    have hinv2 : Invariant (g ∘ g) S := fun p hp => hinv _ (hinv p hp)
    obtain ⟨q, hq⟩ := Finset.card_pos.1 (by omega : 0 < S.card)
    obtain ⟨i, j, hij, heq⟩ := pigeon _ hinv2 q hq
    have ht0 : a * (starRingEnd ℂ) b + b = 0 := by
      have h := congrArg toC heq
      rw [hiter, hiter] at h
      have h' : ((j : ℂ) - i) * (a * (starRingEnd ℂ) b + b) = 0 := by linear_combination -h
      exact (mul_eq_zero.1 h').resolve_left (nat_cast_ne i j hij)
    have hu2 : (a ^ ((2 : ℕ) : ℂ)⁻¹) ^ 2 = a := Complex.cpow_nat_inv_pow a two_ne_zero
    set u : ℂ := a ^ ((2 : ℕ) : ℂ)⁻¹ with hu
    have hun : ‖u‖ = 1 := by
      have h : ‖u‖ ^ 2 = 1 := by rw [← norm_pow, hu2, ha]
      exact (pow_eq_one_iff_of_nonneg (norm_nonneg u) two_ne_zero).1 h
    have hu1 : (ofC u) 0 ^ 2 + (ofC u) 1 ^ 2 = 1 := by
      simp only [ofC_zero, ofC_one]
      have h := Complex.normSq_eq_norm_sq u
      rw [hun, one_pow, Complex.normSq_apply] at h
      linarith
    refine ⟨ofC (b / 2), ofC u, hu1, ?_⟩
    funext p
    apply toC_injective
    rw [toC_reflLine hu1, hgC, toC_ofC, toC_ofC, hu2]
    simp only [map_sub, map_div₀, map_ofNat]
    linear_combination (1 / 2 : ℂ) * ht0

/-- **Corollary 3 (reduction).** Assume the five case classes. Then every finite set `S` of at
least 33 points in general position that is mapped into itself by a Euclidean isometry other
than the identity contains 7 points in convex position. -/
theorem heptagon_of_nontrivial_isometry
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (g : Point → Point) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hg : IsEucIsometry g) (hne : g ≠ id) (hinv : Invariant g S) : HasConvexNGon 7 S := by
  rcases isometry_structure (by omega) hg hne hinv with
    ⟨c, a, hgrot, ha1, m, hm, ham⟩ | ⟨A, u, hu1, hgrefl⟩
  · rw [hgrot] at hinv
    rcases root_cases hm ham ha1 with ⟨k, hk⟩ | ⟨p, k, hp, hp2, hprim⟩
    · -- some power of `g` is the half-turn about `c`
      have hinvH : Invariant (halfTurn (ofC c)) S := by
        have h := hinv.iterate k
        rw [crot_iterate, hk] at h
        rw [halfTurn_eq_crot, toC_ofC]
        exact h
      exact case_halfTurn h2 hgp hcard hinvH
    · have hinvw : Invariant (crot c (a ^ k)) S := by
        have h := hinv.iterate k
        rwa [crot_iterate] at h
      exact case_odd_prime h3 h5 hgp hcard hp hp2 hprim hinvw
  · rw [hgrefl] at hinv
    exact case_mirror hm1 hm0 hu1 hgp hcard hinv

/-- **Corollary 3 exactly as stated in `SYMMETRIC.md`** (no half-turn class; the fourfold
exclusion instead). If `S` (at least 33 points, general position) has no convex heptagon, then
every Euclidean isometry `g ≠ id` mapping `S` into itself is the half-turn about a point not in
`S`, and `|S|` is even, at least 34. -/
theorem halfTurn_of_symmetric_counterexample
    (h3 : Threefold33) (h4 : Fourfold32) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (g : Point → Point) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hg : IsEucIsometry g) (hne : g ≠ id) (hinv : Invariant g S) (hno : ¬ HasConvexNGon 7 S) :
    ∃ c : Point, g = halfTurn c ∧ c ∉ S ∧ 2 ∣ S.card ∧ 34 ≤ S.card := by
  rcases isometry_structure (by omega) hg hne hinv with
    ⟨c, a, hgrot, ha1, m, hm, ham⟩ | ⟨A, u, hu1, hgrefl⟩
  · rw [hgrot] at hinv
    rcases root_cases2 hm ham ha1 with hneg | ⟨k, hk4⟩ | ⟨p, k, hp, hp2, hprim⟩
    · have hH : crot c a = halfTurn (ofC c) := by
        rw [hneg, halfTurn_eq_crot, toC_ofC]
      rw [hH] at hinv
      obtain ⟨hcS, hdvd, -⟩ := halfTurn_facts hgp (by omega) hinv
      exact ⟨ofC c, by rw [hgrot, hH], hcS, hdvd, by omega⟩
    · have hinvw : Invariant (crot c (a ^ k)) S := by
        have h := hinv.iterate k
        rwa [crot_iterate] at h
      exact absurd (case_fourfold h4 hgp hcard hk4 hinvw) hno
    · have hinvw : Invariant (crot c (a ^ k)) S := by
        have h := hinv.iterate k
        rwa [crot_iterate] at h
      exact absurd (case_odd_prime h3 h5 hgp hcard hp hp2 hprim hinvw) hno
  · rw [hgrefl] at hinv
    exact absurd (case_mirror hm1 hm0 hu1 hgp hcard hinv) hno

/-- `Mir.MirrorExclusionLine` (results/H3/MirrorEncoding/Line.lean, Lean-verified there from
CNF facts), copied verbatim with the same `reflLine`; it gives the class `MirrorOneAxis33`. -/
def MirrorExclusionLineCopy : Prop :=
  ∀ (S : Finset Point) (a u : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
    S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → HasConvexNGon 7 S

theorem mirrorOneAxis33_of_exclusionLine (h : MirrorExclusionLineCopy) : MirrorOneAxis33 :=
  fun S a u hu hgp hcard hinv _ => h S a u hu hgp hcard hinv

/-! ## 9. Affine symmetries

Everything above this section is a verbatim copy of `SymmetricReduction.lean` (a sibling file
cannot be imported with `lake env lean`).  This section extends `heptagon_of_nontrivial_isometry`
from Euclidean isometries to affine bijections.

Route (`hasConvexNGon_of_affine_symmetry`, for any `N ≥ 3` and `n`): let `g p = L p + b` be
injective with `g '' S ⊆ S`, `S` finite in general position with `N ≤ |S|`.
1. `g` permutes `S`, so three non-collinear points `p₀, p₁, p₂ ∈ S` have a common period `m ≥ 1`
   (`exists_periodic_of_injective`); then `L^m` fixes `p₁ - p₀` and `p₂ - p₀`, hence `L^m = 1`
   (`iterate_sub_of_affine`, `matrix_eq_one_of_fix`).
2. The averaged form `q(z) = ∑_{k<m} |L^k z|²` (`avgQ`) satisfies `q(L z) = q(z)` and
   `q(z) ≥ |z|²`; with `q(z) = α z₀² + 2β z₀z₁ + γ z₁²` this gives `α > 0`, `αγ - β² > 0`.
3. The Cholesky factor `T z = (√α z₀ + (β/√α) z₁, √((αγ-β²)/α) z₁)` has `|T z|² = q(z)`, so
   `h = T ∘ g ∘ T⁻¹` preserves `eDist2`; `h ≠ id`, `h` maps `T(S)` into itself, and `T` preserves
   general position (`orient` scales by `det T > 0`) and cardinality.
4. The Euclidean hypothesis gives a convex `n`-gon in `T(S)`; its image under the linear map `T⁻¹`
   is a convex `n`-gon in `S` (`convexPosition_image_affine`: injective affine maps commute with
   convex hulls).

The invariance lemmas for the repository definitions are `generalPosition_image_of_orient`,
`orient_affine`, `generalPosition_image_affine`, `generalPosition_image_affineEquiv`,
`convexPosition_image_affine` and `hasConvexNGon_image_affine`. -/

section Affine

open Matrix

/-- Squared Euclidean norm of a vector. -/
def nsq (v : Point) : ℝ := v 0 ^ 2 + v 1 ^ 2

theorem nsq_nonneg (v : Point) : 0 ≤ nsq v := by
  unfold nsq
  positivity

theorem eDist2_eq_nsq (p q : Point) : eDist2 p q = nsq (p - q) := by
  simp [eDist2, nsq]

theorem mulVec2_fst (A : Matrix (Fin 2) (Fin 2) ℝ) (z : Point) :
    (A *ᵥ z) 0 = A 0 0 * z 0 + A 0 1 * z 1 := by
  simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]

theorem mulVec2_snd (A : Matrix (Fin 2) (Fin 2) ℝ) (z : Point) :
    (A *ᵥ z) 1 = A 1 0 * z 0 + A 1 1 * z 1 := by
  simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]

/-- Gram entries of the two columns of a `2 × 2` matrix. -/
def gA (A : Matrix (Fin 2) (Fin 2) ℝ) : ℝ := A 0 0 ^ 2 + A 1 0 ^ 2
def gB (A : Matrix (Fin 2) (Fin 2) ℝ) : ℝ := A 0 0 * A 0 1 + A 1 0 * A 1 1
def gC (A : Matrix (Fin 2) (Fin 2) ℝ) : ℝ := A 0 1 ^ 2 + A 1 1 ^ 2

theorem nsq_mulVec (A : Matrix (Fin 2) (Fin 2) ℝ) (z : Point) :
    nsq (A *ᵥ z) = gA A * z 0 ^ 2 + 2 * gB A * z 0 * z 1 + gC A * z 1 ^ 2 := by
  simp only [nsq, mulVec2_fst, mulVec2_snd, gA, gB, gC]
  ring

/-- The averaged quadratic form `z ↦ ∑_{k<n} |L^k z|²`. -/
def avgQ (L : Matrix (Fin 2) (Fin 2) ℝ) (n : ℕ) (z : Point) : ℝ :=
  ∑ k ∈ Finset.range n, nsq (L ^ k *ᵥ z)

/-- Coefficients of the averaged form. -/
def qA (L : Matrix (Fin 2) (Fin 2) ℝ) (n : ℕ) : ℝ := ∑ k ∈ Finset.range n, gA (L ^ k)
def qB (L : Matrix (Fin 2) (Fin 2) ℝ) (n : ℕ) : ℝ := ∑ k ∈ Finset.range n, gB (L ^ k)
def qC (L : Matrix (Fin 2) (Fin 2) ℝ) (n : ℕ) : ℝ := ∑ k ∈ Finset.range n, gC (L ^ k)

theorem avgQ_eq (L : Matrix (Fin 2) (Fin 2) ℝ) (n : ℕ) (z : Point) :
    avgQ L n z = qA L n * z 0 ^ 2 + 2 * qB L n * z 0 * z 1 + qC L n * z 1 ^ 2 := by
  induction n with
  | zero => simp [avgQ, qA, qB, qC]
  | succ n ih =>
    simp only [avgQ, qA, qB, qC, Finset.sum_range_succ] at ih ⊢
    rw [ih, nsq_mulVec]
    ring

theorem avgQ_ge (L : Matrix (Fin 2) (Fin 2) ℝ) {n : ℕ} (hn : 0 < n) (z : Point) :
    nsq z ≤ avgQ L n z := by
  have h := Finset.single_le_sum (f := fun k => nsq (L ^ k *ᵥ z)) (fun k _ => nsq_nonneg _)
    (Finset.mem_range.2 hn)
  simpa [avgQ] using h

theorem avgQ_mulVec (L : Matrix (Fin 2) (Fin 2) ℝ) {n : ℕ} (hL : L ^ n = 1) (z : Point) :
    avgQ L n (L *ᵥ z) = avgQ L n z := by
  unfold avgQ
  have h1 : ∀ k : ℕ, L ^ k *ᵥ (L *ᵥ z) = L ^ (k + 1) *ᵥ z := by
    intro k
    rw [Matrix.mulVec_mulVec, pow_succ]
  simp only [h1]
  have h2 := Finset.sum_range_succ (fun k => nsq (L ^ k *ᵥ z)) n
  have h3 := Finset.sum_range_succ' (fun k => nsq (L ^ k *ᵥ z)) n
  rw [hL] at h2
  simp only [pow_zero] at h2 h3
  linarith

theorem qA_pos (L : Matrix (Fin 2) (Fin 2) ℝ) {n : ℕ} (hn : 0 < n) : 0 < qA L n := by
  have h := avgQ_ge L hn ![1, 0]
  rw [avgQ_eq] at h
  simp [nsq] at h
  linarith

theorem qdisc_pos (L : Matrix (Fin 2) (Fin 2) ℝ) {n : ℕ} (hn : 0 < n) :
    0 < qA L n * qC L n - qB L n ^ 2 := by
  have hA := qA_pos L hn
  have h := avgQ_ge L hn ![-(qB L n), qA L n]
  rw [avgQ_eq] at h
  simp [nsq] at h
  nlinarith [mul_pos hA hA, sq_nonneg (qB L n)]

/-- The linear map `p ↦ (a p₀ + b p₁, c p₀ + d p₁)`. -/
def lin2 (a b c d : ℝ) : Point →ₗ[ℝ] Point where
  toFun p := ![a * p 0 + b * p 1, c * p 0 + d * p 1]
  map_add' p q := by
    apply point_ext <;> simp <;> ring
  map_smul' r p := by
    apply point_ext <;> simp <;> ring

@[simp] theorem lin2_fst (a b c d : ℝ) (p : Point) : lin2 a b c d p 0 = a * p 0 + b * p 1 := rfl
@[simp] theorem lin2_snd (a b c d : ℝ) (p : Point) : lin2 a b c d p 1 = c * p 0 + d * p 1 := rfl

theorem orient_lin2 (a b c d : ℝ) (x y z : Point) :
    orient (lin2 a b c d x) (lin2 a b c d y) (lin2 a b c d z) =
      (a * d - b * c) * orient x y z := by
  simp only [orient, lin2_fst, lin2_snd]
  ring

/-- The Cholesky factor: `|T z|² = s² z₀² + 2 β z₀ z₁ + (β²/s² + t²) z₁²`. -/
theorem nsq_lin2_chol {s t β : ℝ} (hs : s ≠ 0) (z : Point) :
    nsq (lin2 s (β / s) 0 t z) =
      s ^ 2 * z 0 ^ 2 + 2 * β * z 0 * z 1 + (β ^ 2 / s ^ 2 + t ^ 2) * z 1 ^ 2 := by
  simp only [nsq, lin2_fst, lin2_snd]
  field_simp
  ring

theorem lin2_chol_inv_left {s t β : ℝ} (hs : s ≠ 0) (ht : t ≠ 0) (x : Point) :
    lin2 (1 / s) (-β / (s ^ 2 * t)) 0 (1 / t) (lin2 s (β / s) 0 t x) = x := by
  apply point_ext <;> simp only [lin2_fst, lin2_snd] <;> field_simp <;> ring

theorem lin2_chol_inv_right {s t β : ℝ} (hs : s ≠ 0) (ht : t ≠ 0) (x : Point) :
    lin2 s (β / s) 0 t (lin2 (1 / s) (-β / (s ^ 2 * t)) 0 (1 / t) x) = x := by
  apply point_ext <;> simp only [lin2_fst, lin2_snd] <;> field_simp <;> ring

theorem iterate_sub_of_affine {g : Point → Point} {L : Matrix (Fin 2) (Fin 2) ℝ} {b : Point}
    (hg : ∀ p, g p = L *ᵥ p + b) (k : ℕ) (p q : Point) :
    g^[k] p - g^[k] q = L ^ k *ᵥ (p - q) := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [iterate_succ_apply', iterate_succ_apply', hg, hg, add_sub_add_right_eq_sub,
      ← Matrix.mulVec_sub, ih, Matrix.mulVec_mulVec, pow_succ']

theorem exists_periodic_of_injective {g : Point → Point} (hinj : Injective g) {S : Finset Point}
    (hinv : Invariant g S) {q : Point} (hq : q ∈ S) : ∃ m, 0 < m ∧ g^[m] q = q := by
  obtain ⟨i, j, hij, heq⟩ := Set.Finite.exists_lt_map_eq_of_forall_mem (t := (S : Set Point))
      (f := fun k => g^[k] q) (fun k => iterate_mem hinv hq k) S.finite_toSet
  refine ⟨j - i, Nat.sub_pos_of_lt hij, ?_⟩
  apply hinj.iterate i
  rw [← iterate_add_apply, Nat.add_sub_cancel' hij.le]
  exact heq.symm

theorem matrix_eq_one_of_fix {M : Matrix (Fin 2) (Fin 2) ℝ} {u w : Point}
    (hdet : u 0 * w 1 - u 1 * w 0 ≠ 0) (hu : M *ᵥ u = u) (hw : M *ᵥ w = w) : M = 1 := by
  have hu0 := congrFun hu 0
  have hu1 := congrFun hu 1
  have hw0 := congrFun hw 0
  have hw1 := congrFun hw 1
  rw [mulVec2_fst] at hu0 hw0
  rw [mulVec2_snd] at hu1 hw1
  have e00 : (M 0 0 - 1) * (u 0 * w 1 - u 1 * w 0) = 0 := by
    linear_combination w 1 * hu0 - u 1 * hw0
  have e01 : M 0 1 * (u 0 * w 1 - u 1 * w 0) = 0 := by
    linear_combination -(w 0) * hu0 + u 0 * hw0
  have e10 : M 1 0 * (u 0 * w 1 - u 1 * w 0) = 0 := by
    linear_combination w 1 * hu1 - u 1 * hw1
  have e11 : (M 1 1 - 1) * (u 0 * w 1 - u 1 * w 0) = 0 := by
    linear_combination -(w 0) * hu1 + u 0 * hw1
  have f00 := (mul_eq_zero.1 e00).resolve_right hdet
  have f01 := (mul_eq_zero.1 e01).resolve_right hdet
  have f10 := (mul_eq_zero.1 e10).resolve_right hdet
  have f11 := (mul_eq_zero.1 e11).resolve_right hdet
  ext i j
  fin_cases i <;> fin_cases j <;> simp <;> linarith

/-- An affine map `p ↦ L p + b` scales orientations by `det L`. -/
theorem orient_affine {g : Point → Point} {L : Matrix (Fin 2) (Fin 2) ℝ} {b : Point}
    (hg : ∀ p, g p = L *ᵥ p + b) (x y z : Point) :
    orient (g x) (g y) (g z) = L.det * orient x y z := by
  rw [hg, hg, hg, Matrix.det_fin_two]
  simp only [orient, Pi.add_apply, mulVec2_fst, mulVec2_snd]
  ring

/-- A map that scales orientations by a nonzero factor preserves general position. -/
theorem generalPosition_image_of_orient {f : Point → Point} {D : ℝ}
    (hD : D ≠ 0) (hor : ∀ x y z, orient (f x) (f y) (f z) = D * orient x y z)
    {S : Finset Point} (hgp : GeneralPosition S) : GeneralPosition (S.image f) := by
  classical
  rw [generalPosition_iff_orient_ne_zero] at hgp ⊢
  intro x hx y hy z hz hxy hxz hyz
  obtain ⟨x', hx', rfl⟩ := Finset.mem_image.1 hx
  obtain ⟨y', hy', rfl⟩ := Finset.mem_image.1 hy
  obtain ⟨z', hz', rfl⟩ := Finset.mem_image.1 hz
  rw [hor]
  exact mul_ne_zero hD (hgp x' hx' y' hy' z' hz' (fun h => hxy (congrArg f h))
    (fun h => hxz (congrArg f h)) (fun h => hyz (congrArg f h)))

/-- Injective affine maps preserve convex position. -/
theorem convexPosition_image_affine {s : Finset Point} (hs : ConvexPosition s)
    (f : Point →ᵃ[ℝ] Point) (hf : Injective f) : ConvexPosition (s.image f) := by
  classical
  rw [convexPosition_iff] at hs ⊢
  intro p hp hmem
  rw [Finset.coe_image] at hp hmem
  obtain ⟨q, hq, rfl⟩ := hp
  have hset : (f '' (s : Set Point)) \ {f q} = f '' ((s : Set Point) \ {q}) := by
    rw [Set.image_diff hf, Set.image_singleton]
  rw [hset, ← AffineMap.image_convexHull] at hmem
  obtain ⟨r, hr, hrq⟩ := hmem
  rw [hf hrq] at hr
  exact hs q hq hr

/-- Affine maps `p ↦ L p + b` with `det L ≠ 0` preserve general position. -/
theorem generalPosition_image_affine {g : Point → Point} {L : Matrix (Fin 2) (Fin 2) ℝ}
    {b : Point} (hg : ∀ p, g p = L *ᵥ p + b) (hL : L.det ≠ 0) {S : Finset Point}
    (hgp : GeneralPosition S) : GeneralPosition (S.image g) :=
  generalPosition_image_of_orient hL (orient_affine hg) hgp

/-- Matrix form of a Mathlib affine map of the plane. -/
theorem affineMap_eq_mulVec (f : Point →ᵃ[ℝ] Point) (p : Point) :
    f p = LinearMap.toMatrix' f.linear *ᵥ p + f 0 := by
  rw [LinearMap.toMatrix'_mulVec]
  exact congrFun f.decomp p

/-- Affine bijections preserve general position. -/
theorem generalPosition_image_affineEquiv {S : Finset Point} (hgp : GeneralPosition S)
    (f : Point ≃ᵃ[ℝ] Point) : GeneralPosition (S.image f) := by
  have hdet : (LinearMap.toMatrix' f.toAffineMap.linear).det ≠ 0 := by
    rw [LinearMap.det_toMatrix']
    exact (LinearEquiv.isUnit_det' f.linear).ne_zero
  exact generalPosition_image_affine (affineMap_eq_mulVec f.toAffineMap) hdet hgp

/-- Injective affine maps carry convex `n`-gons to convex `n`-gons. -/
theorem hasConvexNGon_image_affine {n : ℕ} {S : Finset Point} (h : HasConvexNGon n S)
    (f : Point →ᵃ[ℝ] Point) (hf : Injective f) : HasConvexNGon n (S.image f) := by
  classical
  obtain ⟨U, hUS, hUcard, hU⟩ := h
  exact ⟨U.image f, Finset.image_subset_image hUS,
    by rw [Finset.card_image_of_injective _ hf, hUcard], convexPosition_image_affine hU f hf⟩

theorem injective_of_affine {g : Point → Point} {L : Matrix (Fin 2) (Fin 2) ℝ} {b : Point}
    (hg : ∀ p, g p = L *ᵥ p + b) (hL : L.det ≠ 0) : Injective g := by
  intro p q hpq
  have h : L *ᵥ (p - q) = 0 := by
    rw [Matrix.mulVec_sub, ← add_sub_add_right_eq_sub (L *ᵥ p) (L *ᵥ q) b, ← hg, ← hg, hpq,
      sub_self]
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  rw [mulVec2_fst] at h0
  rw [mulVec2_snd] at h1
  rw [Matrix.det_fin_two] at hL
  simp only [Pi.sub_apply, Pi.zero_apply] at h0 h1
  have e0 : (L 0 0 * L 1 1 - L 0 1 * L 1 0) * (p 0 - q 0) = 0 := by
    linear_combination L 1 1 * h0 - L 0 1 * h1
  have e1 : (L 0 0 * L 1 1 - L 0 1 * L 1 0) * (p 1 - q 1) = 0 := by
    linear_combination L 0 0 * h1 - L 1 0 * h0
  exact point_ext (sub_eq_zero.1 ((mul_eq_zero.1 e0).resolve_left hL))
    (sub_eq_zero.1 ((mul_eq_zero.1 e1).resolve_left hL))

/-- **Affine-to-Euclidean reduction.** Suppose that every finite set in general position with at
least `N ≥ 3` points that is mapped into itself by a Euclidean isometry other than the identity
contains a convex `n`-gon. Then the same holds with any injective affine map `p ↦ L p + b` in
place of the isometry: the linear part has finite order, the averaged form
`∑_{k<m} |L^k z|²` is `L`-invariant and positive definite, and conjugating by its Cholesky
factor `T` turns the affine symmetry into a Euclidean one of `T(S)`. -/
theorem hasConvexNGon_of_affine_symmetry {N n : ℕ}
    (hE : ∀ (S : Finset Point) (g : Point → Point), GeneralPosition S → N ≤ S.card →
      IsEucIsometry g → g ≠ id → Invariant g S → HasConvexNGon n S)
    (hN : 3 ≤ N) (S : Finset Point) (g : Point → Point) (L : Matrix (Fin 2) (Fin 2) ℝ)
    (b : Point) (hg : ∀ p, g p = L *ᵥ p + b) (hinj : Injective g)
    (hgp : GeneralPosition S) (hcard : N ≤ S.card) (hne : g ≠ id) (hinv : Invariant g S) :
    HasConvexNGon n S := by
  classical
  -- three non-collinear points of `S`
  obtain ⟨p0, hp0, p1, hp1, p2, hp2, h01, h02, h12⟩ :=
    Finset.two_lt_card.1 (by omega : 2 < S.card)
  have hor : orient p0 p1 p2 ≠ 0 :=
    (generalPosition_iff_orient_ne_zero S).1 hgp p0 hp0 p1 hp1 p2 hp2 h01 h02 h12
  -- a common period `m` of the three points
  obtain ⟨m0, hm0, hq0⟩ := exists_periodic_of_injective hinj hinv hp0
  obtain ⟨m1, hm1, hq1⟩ := exists_periodic_of_injective hinj hinv hp1
  obtain ⟨m2, hm2, hq2⟩ := exists_periodic_of_injective hinj hinv hp2
  have hmpos : 0 < m0 * m1 * m2 := by positivity
  have hP0 : g^[m0 * m1 * m2] p0 = p0 :=
    IsPeriodicPt.mul_const (IsPeriodicPt.mul_const (f := g) hq0 m1) m2
  have hP1 : g^[m0 * m1 * m2] p1 = p1 :=
    IsPeriodicPt.mul_const (IsPeriodicPt.const_mul (f := g) hq1 m0) m2
  have hP2 : g^[m0 * m1 * m2] p2 = p2 :=
    IsPeriodicPt.const_mul (f := g) hq2 (m0 * m1)
  set m := m0 * m1 * m2 with hm
  -- the linear part has finite order
  have hLm : L ^ m = 1 := by
    apply matrix_eq_one_of_fix (u := p1 - p0) (w := p2 - p0)
    · simpa [orient] using hor
    · rw [← iterate_sub_of_affine hg, hP1, hP0]
    · rw [← iterate_sub_of_affine hg, hP2, hP0]
  -- the averaged form and its Cholesky factor `T`
  have hα : 0 < qA L m := qA_pos L hmpos
  have hδ : 0 < qA L m * qC L m - qB L m ^ 2 := qdisc_pos L hmpos
  set α := qA L m with hαdef
  set β := qB L m with hβdef
  set γ := qC L m with hγdef
  set s := Real.sqrt α with hsdef
  set t := Real.sqrt ((α * γ - β ^ 2) / α) with htdef
  have hs : 0 < s := Real.sqrt_pos.2 hα
  have ht : 0 < t := Real.sqrt_pos.2 (div_pos hδ hα)
  have hs2 : s ^ 2 = α := Real.sq_sqrt hα.le
  have ht2 : t ^ 2 = (α * γ - β ^ 2) / α := Real.sq_sqrt (div_pos hδ hα).le
  set T := lin2 s (β / s) 0 t with hT
  set Ti := lin2 (1 / s) (-β / (s ^ 2 * t)) 0 (1 / t) with hTi
  have hTiT : ∀ x, Ti (T x) = x := lin2_chol_inv_left hs.ne' ht.ne'
  have hTTi : ∀ x, T (Ti x) = x := lin2_chol_inv_right hs.ne' ht.ne'
  have hnT : ∀ z, nsq (T z) = avgQ L m z := by
    intro z
    have hγ' : β ^ 2 / s ^ 2 + t ^ 2 = γ := by
      rw [hs2, ht2]
      field_simp
      ring
    rw [nsq_lin2_chol hs.ne', avgQ_eq, hγ', hs2]
  -- the conjugate `h = T ∘ g ∘ T⁻¹` is a Euclidean isometry
  set h : Point → Point := fun x => T (g (Ti x)) with hh
  have hiso : IsEucIsometry h := by
    intro x y
    rw [eDist2_eq_nsq, eDist2_eq_nsq]
    simp only [hh]
    rw [← map_sub, hnT, hg, hg, add_sub_add_right_eq_sub, ← Matrix.mulVec_sub,
      avgQ_mulVec L hLm, ← hnT, map_sub, hTTi, hTTi]
  have hTinj : Injective T := Function.LeftInverse.injective hTiT
  have hTiinj : Injective Ti := Function.LeftInverse.injective hTTi
  have hne' : h ≠ id := by
    intro hid
    apply hne
    funext p
    have h1 := congrFun hid (T p)
    simp only [hh, hTiT, id] at h1
    exact hTinj h1
  have hgp' : GeneralPosition (S.image T) :=
    generalPosition_image_of_orient (D := s * t - β / s * 0)
      (by rw [mul_zero, sub_zero]; exact (mul_pos hs ht).ne') (orient_lin2 _ _ _ _) hgp
  have hcard' : N ≤ (S.image T).card := by
    rw [Finset.card_image_of_injective _ hTinj]
    exact hcard
  have hinv' : Invariant h (S.image T) := by
    intro x hx
    obtain ⟨p, hp, rfl⟩ := Finset.mem_image.1 hx
    simp only [hh, hTiT]
    exact Finset.mem_image_of_mem _ (hinv p hp)
  obtain ⟨U, hUS, hUcard, hUconv⟩ := hE (S.image T) h hgp' hcard' hiso hne' hinv'
  refine ⟨U.image Ti, ?_, ?_, ?_⟩
  · intro y hy
    obtain ⟨x, hx, rfl⟩ := Finset.mem_image.1 hy
    obtain ⟨p, hp, rfl⟩ := Finset.mem_image.1 (hUS hx)
    rw [hTiT]
    exact hp
  · rw [Finset.card_image_of_injective _ hTiinj, hUcard]
  · exact convexPosition_image_affine hUconv Ti.toAffineMap hTiinj

/-- `hasConvexNGon_of_affine_symmetry` for an injective affine map of Mathlib. -/
theorem hasConvexNGon_of_affineMap_symmetry {N n : ℕ}
    (hE : ∀ (S : Finset Point) (g : Point → Point), GeneralPosition S → N ≤ S.card →
      IsEucIsometry g → g ≠ id → Invariant g S → HasConvexNGon n S)
    (hN : 3 ≤ N) (S : Finset Point) (f : Point →ᵃ[ℝ] Point) (hf : Injective f)
    (hgp : GeneralPosition S) (hcard : N ≤ S.card) (hne : (f : Point → Point) ≠ id)
    (hinv : Invariant f S) : HasConvexNGon n S :=
  hasConvexNGon_of_affine_symmetry hE hN S f (LinearMap.toMatrix' f.linear) (f 0)
    (affineMap_eq_mulVec f) hf hgp hcard hne hinv

/-- `hasConvexNGon_of_affine_symmetry` for an affine equivalence of Mathlib. -/
theorem hasConvexNGon_of_affineEquiv_symmetry {N n : ℕ}
    (hE : ∀ (S : Finset Point) (g : Point → Point), GeneralPosition S → N ≤ S.card →
      IsEucIsometry g → g ≠ id → Invariant g S → HasConvexNGon n S)
    (hN : 3 ≤ N) (S : Finset Point) (f : Point ≃ᵃ[ℝ] Point)
    (hgp : GeneralPosition S) (hcard : N ≤ S.card) (hne : f ≠ AffineEquiv.refl ℝ Point)
    (hinv : Invariant f S) : HasConvexNGon n S := by
  refine hasConvexNGon_of_affineMap_symmetry hE hN S f.toAffineMap f.injective hgp hcard ?_ hinv
  intro hid
  exact hne (AffineEquiv.ext fun p => congrFun hid p)

/-- Coordinates: `g (x, y) = (a x + b y + e, c x + d y + f)` with `a d - b c ≠ 0`. -/
theorem hasConvexNGon_of_affine_coords_symmetry {N n : ℕ}
    (hE : ∀ (S : Finset Point) (g : Point → Point), GeneralPosition S → N ≤ S.card →
      IsEucIsometry g → g ≠ id → Invariant g S → HasConvexNGon n S)
    (hN : 3 ≤ N) (S : Finset Point) (g : Point → Point) (a b c d e f : ℝ)
    (hdet : a * d - b * c ≠ 0) (hg : ∀ p, g p = ![a * p 0 + b * p 1 + e, c * p 0 + d * p 1 + f])
    (hgp : GeneralPosition S) (hcard : N ≤ S.card) (hne : g ≠ id) (hinv : Invariant g S) :
    HasConvexNGon n S := by
  have hg' : ∀ p, g p = !![a, b; c, d] *ᵥ p + ![e, f] := by
    intro p
    rw [hg]
    apply point_ext
    · rw [Pi.add_apply, mulVec2_fst]
      simp
    · rw [Pi.add_apply, mulVec2_snd]
      simp
  have hdet' : (!![a, b; c, d] : Matrix (Fin 2) (Fin 2) ℝ).det ≠ 0 := by
    rw [Matrix.det_fin_two_of]
    exact hdet
  exact hasConvexNGon_of_affine_symmetry hE hN S g _ _ hg' (injective_of_affine hg' hdet') hgp
    hcard hne hinv

end Affine

/-! ## 10. Corollary 3 for affine symmetries -/

section AffineCorollary

open Matrix

/-- **Corollary 3, affine version (matrix form).** Assume the five case classes. Let `S` be a
finite set of at least 33 points in general position and `g : p ↦ L p + b` an injective affine
map of the plane, `g ≠ id`, mapping `S` into itself. Then `S` contains 7 points in convex
position. -/
theorem heptagon_of_nontrivial_affine
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (g : Point → Point) (L : Matrix (Fin 2) (Fin 2) ℝ) (b : Point)
    (hg : ∀ p, g p = L *ᵥ p + b) (hinj : Injective g)
    (hgp : GeneralPosition S) (hcard : 33 ≤ S.card) (hne : g ≠ id) (hinv : Invariant g S) :
    HasConvexNGon 7 S :=
  hasConvexNGon_of_affine_symmetry (heptagon_of_nontrivial_isometry h2 h3 h5 hm1 hm0)
    (by norm_num) S g L b hg hinj hgp hcard hne hinv

/-- **Corollary 3, affine version (Mathlib affine maps).** As `heptagon_of_nontrivial_affine`,
for an injective `f : Point →ᵃ[ℝ] Point` with `⇑f ≠ id`. -/
theorem heptagon_of_nontrivial_affineMap
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (f : Point →ᵃ[ℝ] Point) (hf : Injective f)
    (hgp : GeneralPosition S) (hcard : 33 ≤ S.card) (hne : (f : Point → Point) ≠ id)
    (hinv : Invariant f S) : HasConvexNGon 7 S :=
  hasConvexNGon_of_affineMap_symmetry (heptagon_of_nontrivial_isometry h2 h3 h5 hm1 hm0)
    (by norm_num) S f hf hgp hcard hne hinv

/-- **Corollary 3, affine version.** Assume the five case classes. Every finite set `S` of at
least 33 points in general position that is mapped into itself by an affine bijection of the
plane other than the identity contains 7 points in convex position. -/
theorem heptagon_of_nontrivial_affineEquiv
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (g : Point ≃ᵃ[ℝ] Point) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hne : g ≠ AffineEquiv.refl ℝ Point) (hinv : Invariant g S) : HasConvexNGon 7 S :=
  hasConvexNGon_of_affineEquiv_symmetry (heptagon_of_nontrivial_isometry h2 h3 h5 hm1 hm0)
    (by norm_num) S g hgp hcard hne hinv

/-- The same with the invariance written as `g '' S ⊆ S`. -/
theorem heptagon_of_nontrivial_affineEquiv_image
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (g : Point ≃ᵃ[ℝ] Point) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hne : g ≠ AffineEquiv.refl ℝ Point) (hinv : g '' (S : Set Point) ⊆ S) :
    HasConvexNGon 7 S :=
  heptagon_of_nontrivial_affineEquiv h2 h3 h5 hm1 hm0 S g hgp hcard hne
    (fun p hp => Finset.mem_coe.1 (hinv ⟨p, Finset.mem_coe.2 hp, rfl⟩))

/-- **Corollary 3, affine version (coordinates).** `g (x, y) = (a x + b y + e, c x + d y + f)`
with `a d - b c ≠ 0`. -/
theorem heptagon_of_nontrivial_affine_coords
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)
    (S : Finset Point) (g : Point → Point) (a b c d e f : ℝ) (hdet : a * d - b * c ≠ 0)
    (hg : ∀ p, g p = ![a * p 0 + b * p 1 + e, c * p 0 + d * p 1 + f])
    (hgp : GeneralPosition S) (hcard : 33 ≤ S.card) (hne : g ≠ id) (hinv : Invariant g S) :
    HasConvexNGon 7 S :=
  hasConvexNGon_of_affine_coords_symmetry (heptagon_of_nontrivial_isometry h2 h3 h5 hm1 hm0)
    (by norm_num) S g a b c d e f hdet hg hgp hcard hne hinv

end AffineCorollary

end ErdosSzekeres.SymReduction

#print axioms ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affineEquiv
#print axioms ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affineEquiv_image
#print axioms ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affineMap
#print axioms ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affine
#print axioms ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affine_coords
#print axioms ErdosSzekeres.SymReduction.hasConvexNGon_of_affine_symmetry
#print axioms ErdosSzekeres.SymReduction.generalPosition_image_affineEquiv
#print axioms ErdosSzekeres.SymReduction.hasConvexNGon_image_affine
#print axioms ErdosSzekeres.SymReduction.heptagon_of_nontrivial_isometry
#check @ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affineEquiv
