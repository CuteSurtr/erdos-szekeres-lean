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
import ErdosSzekeres.Omission.BaekGeometry
import ErdosSzekeres.ConvexCycleCuts

/-!
# Corollary 3 with the two mirror classes discharged (`ReductionThreeClasses.lean`)

This file is the concatenation of two developments (sibling files cannot be imported with
`lake env lean`), followed by a short integration section:

* Part A: `symlean/affine/AffineReduction.lean` (namespace `ErdosSzekeres.SymReduction`;
  sha256 `41cfc0b60aec15c7f60728b48492dc5f40d1a1c866ffad08947efc744ef21d61`), verbatim apart
  from its import lines, which are merged into the import block above;
* Part B: `mirrorM/odd/lean/MirrorMain.lean` (namespace `MirrorOdd`;
  sha256 `ca623e55a1b93a87bebe30535aa5a70bde2995109874a46a69f658e29292376f`), verbatim apart
  from its import lines, which are merged into the import block above;
* Part C (§ 11 below): `reflLine a u = MirrorOdd.lineRefl (-u 1) (u 0) (-u 1 * a 0 + u 0 * a 1)`
  for `u 0 ^ 2 + u 1 ^ 2 = 1`, hence `MirrorOdd.mirror_seven_line` proves the classes
  `MirrorOneAxis33` and `MirrorNoAxis34`, and the reductions
  `heptagon_of_nontrivial_isometry_3` and `heptagon_of_nontrivial_affineEquiv_3` assume only
  `HalfTurn34`, `Threefold33` and `Fivefold35`.

No statement of Part A or Part B is changed.  The two parts live in disjoint namespaces, so no
declaration had to be renamed.
-/

/-! # Part A: `symlean/affine/AffineReduction.lean` (verbatim after its imports) -/

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

/-! # Part B: `mirrorM/odd/lean/MirrorMain.lean` (verbatim after its imports) -/

/-! Mirror polygons (odd-k mirror reduction, `mirrorM/odd`).
For a cap c0 < c1 < c2 < c3 strictly above the x-axis, the points together with their mirror images
`mir p = (p 0, -p 1)` contain a convex heptagon (and form a convex octagon); if one end of a 4-cap lies on the
x-axis, the cap and the mirror images of its other three points form a convex heptagon.
Every orientation inequality is closed by `linarith` with an exact certificate found offline (gen_certs.py).
Assembled from MirrorPolygons.lean and small_polygons.lean (generated by gen_lean.py), MirrorReduction.lean,
general_section.lean, smallk_section.lean, generalk_section.lean and generalk_line.lean. -/

namespace MirrorOdd
open ErdosSzekeres

/-- Reflection in the x-axis. -/
def mir (p : Point) : Point := ![p 0, -p 1]

@[simp] theorem mir_zero (p : Point) : mir p 0 = p 0 := by simp [mir]
@[simp] theorem mir_one (p : Point) : mir p 1 = -p 1 := by simp [mir]


theorem cyc7 (q0 q1 q2 q3 q4 q5 q6 : Point) {P : Finset Point}
    (m0 : q0 ∈ P)
    (m1 : q1 ∈ P)
    (m2 : q2 ∈ P)
    (m3 : q3 ∈ P)
    (m4 : q4 ∈ P)
    (m5 : q5 ∈ P)
    (m6 : q6 ∈ P)
    (d01 : q0 ≠ q1)
    (d02 : q0 ≠ q2)
    (d03 : q0 ≠ q3)
    (d04 : q0 ≠ q4)
    (d05 : q0 ≠ q5)
    (d06 : q0 ≠ q6)
    (d12 : q1 ≠ q2)
    (d13 : q1 ≠ q3)
    (d14 : q1 ≠ q4)
    (d15 : q1 ≠ q5)
    (d16 : q1 ≠ q6)
    (d23 : q2 ≠ q3)
    (d24 : q2 ≠ q4)
    (d25 : q2 ≠ q5)
    (d26 : q2 ≠ q6)
    (d34 : q3 ≠ q4)
    (d35 : q3 ≠ q5)
    (d36 : q3 ≠ q6)
    (d45 : q4 ≠ q5)
    (d46 : q4 ≠ q6)
    (d56 : q5 ≠ q6)
    (h012 : 0 < orient q0 q1 q2)
    (h013 : 0 < orient q0 q1 q3)
    (h014 : 0 < orient q0 q1 q4)
    (h015 : 0 < orient q0 q1 q5)
    (h016 : 0 < orient q0 q1 q6)
    (h023 : 0 < orient q0 q2 q3)
    (h024 : 0 < orient q0 q2 q4)
    (h025 : 0 < orient q0 q2 q5)
    (h026 : 0 < orient q0 q2 q6)
    (h034 : 0 < orient q0 q3 q4)
    (h035 : 0 < orient q0 q3 q5)
    (h036 : 0 < orient q0 q3 q6)
    (h045 : 0 < orient q0 q4 q5)
    (h046 : 0 < orient q0 q4 q6)
    (h056 : 0 < orient q0 q5 q6)
    (h123 : 0 < orient q1 q2 q3)
    (h124 : 0 < orient q1 q2 q4)
    (h125 : 0 < orient q1 q2 q5)
    (h126 : 0 < orient q1 q2 q6)
    (h134 : 0 < orient q1 q3 q4)
    (h135 : 0 < orient q1 q3 q5)
    (h136 : 0 < orient q1 q3 q6)
    (h145 : 0 < orient q1 q4 q5)
    (h146 : 0 < orient q1 q4 q6)
    (h156 : 0 < orient q1 q5 q6)
    (h234 : 0 < orient q2 q3 q4)
    (h235 : 0 < orient q2 q3 q5)
    (h236 : 0 < orient q2 q3 q6)
    (h245 : 0 < orient q2 q4 q5)
    (h246 : 0 < orient q2 q4 q6)
    (h256 : 0 < orient q2 q5 q6)
    (h345 : 0 < orient q3 q4 q5)
    (h346 : 0 < orient q3 q4 q6)
    (h356 : 0 < orient q3 q5 q6)
    (h456 : 0 < orient q4 q5 q6)
    : HasConvexNGon 7 P := by
  have hinj : Function.Injective (![q0, q1, q2, q3, q4, q5, q6] : Fin 7 → Point) := by
    intro i j hij
    fin_cases i <;> fin_cases j
    all_goals first | rfl | skip
    exacts [absurd hij d01, absurd hij d02, absurd hij d03, absurd hij d04, absurd hij d05, absurd hij d06, absurd hij.symm d01, absurd hij d12, absurd hij d13, absurd hij d14, absurd hij d15, absurd hij d16, absurd hij.symm d02, absurd hij.symm d12, absurd hij d23, absurd hij d24, absurd hij d25, absurd hij d26, absurd hij.symm d03, absurd hij.symm d13, absurd hij.symm d23, absurd hij d34, absurd hij d35, absurd hij d36, absurd hij.symm d04, absurd hij.symm d14, absurd hij.symm d24, absurd hij.symm d34, absurd hij d45, absurd hij d46, absurd hij.symm d05, absurd hij.symm d15, absurd hij.symm d25, absurd hij.symm d35, absurd hij.symm d45, absurd hij d56, absurd hij.symm d06, absurd hij.symm d16, absurd hij.symm d26, absurd hij.symm d36, absurd hij.symm d46, absurd hij.symm d56]
  refine hasConvexNGon_of_positive_cycle (by norm_num) (![q0, q1, q2, q3, q4, q5, q6] : Fin 7 → Point) hinj
    (Function.Embedding.refl _) ?_ ?_
  · intro i
    fin_cases i
    exacts [m0, m1, m2, m3, m4, m5, m6]
  · intro i j l hij hjl
    fin_cases i <;> fin_cases j <;> fin_cases l
    all_goals first | exact absurd hij (by decide) | exact absurd hjl (by decide) | skip
    exacts [h012, h013, h014, h015, h016, h023, h024, h025, h026, h034, h035, h036, h045, h046, h056, h123, h124, h125, h126, h134, h135, h136, h145, h146, h156, h234, h235, h236, h245, h246, h256, h345, h346, h356, h456]

set_option maxHeartbeats 1000000 in
theorem cyc8 (q0 q1 q2 q3 q4 q5 q6 q7 : Point) {P : Finset Point}
    (m0 : q0 ∈ P)
    (m1 : q1 ∈ P)
    (m2 : q2 ∈ P)
    (m3 : q3 ∈ P)
    (m4 : q4 ∈ P)
    (m5 : q5 ∈ P)
    (m6 : q6 ∈ P)
    (m7 : q7 ∈ P)
    (d01 : q0 ≠ q1)
    (d02 : q0 ≠ q2)
    (d03 : q0 ≠ q3)
    (d04 : q0 ≠ q4)
    (d05 : q0 ≠ q5)
    (d06 : q0 ≠ q6)
    (d07 : q0 ≠ q7)
    (d12 : q1 ≠ q2)
    (d13 : q1 ≠ q3)
    (d14 : q1 ≠ q4)
    (d15 : q1 ≠ q5)
    (d16 : q1 ≠ q6)
    (d17 : q1 ≠ q7)
    (d23 : q2 ≠ q3)
    (d24 : q2 ≠ q4)
    (d25 : q2 ≠ q5)
    (d26 : q2 ≠ q6)
    (d27 : q2 ≠ q7)
    (d34 : q3 ≠ q4)
    (d35 : q3 ≠ q5)
    (d36 : q3 ≠ q6)
    (d37 : q3 ≠ q7)
    (d45 : q4 ≠ q5)
    (d46 : q4 ≠ q6)
    (d47 : q4 ≠ q7)
    (d56 : q5 ≠ q6)
    (d57 : q5 ≠ q7)
    (d67 : q6 ≠ q7)
    (h012 : 0 < orient q0 q1 q2)
    (h013 : 0 < orient q0 q1 q3)
    (h014 : 0 < orient q0 q1 q4)
    (h015 : 0 < orient q0 q1 q5)
    (h016 : 0 < orient q0 q1 q6)
    (h017 : 0 < orient q0 q1 q7)
    (h023 : 0 < orient q0 q2 q3)
    (h024 : 0 < orient q0 q2 q4)
    (h025 : 0 < orient q0 q2 q5)
    (h026 : 0 < orient q0 q2 q6)
    (h027 : 0 < orient q0 q2 q7)
    (h034 : 0 < orient q0 q3 q4)
    (h035 : 0 < orient q0 q3 q5)
    (h036 : 0 < orient q0 q3 q6)
    (h037 : 0 < orient q0 q3 q7)
    (h045 : 0 < orient q0 q4 q5)
    (h046 : 0 < orient q0 q4 q6)
    (h047 : 0 < orient q0 q4 q7)
    (h056 : 0 < orient q0 q5 q6)
    (h057 : 0 < orient q0 q5 q7)
    (h067 : 0 < orient q0 q6 q7)
    (h123 : 0 < orient q1 q2 q3)
    (h124 : 0 < orient q1 q2 q4)
    (h125 : 0 < orient q1 q2 q5)
    (h126 : 0 < orient q1 q2 q6)
    (h127 : 0 < orient q1 q2 q7)
    (h134 : 0 < orient q1 q3 q4)
    (h135 : 0 < orient q1 q3 q5)
    (h136 : 0 < orient q1 q3 q6)
    (h137 : 0 < orient q1 q3 q7)
    (h145 : 0 < orient q1 q4 q5)
    (h146 : 0 < orient q1 q4 q6)
    (h147 : 0 < orient q1 q4 q7)
    (h156 : 0 < orient q1 q5 q6)
    (h157 : 0 < orient q1 q5 q7)
    (h167 : 0 < orient q1 q6 q7)
    (h234 : 0 < orient q2 q3 q4)
    (h235 : 0 < orient q2 q3 q5)
    (h236 : 0 < orient q2 q3 q6)
    (h237 : 0 < orient q2 q3 q7)
    (h245 : 0 < orient q2 q4 q5)
    (h246 : 0 < orient q2 q4 q6)
    (h247 : 0 < orient q2 q4 q7)
    (h256 : 0 < orient q2 q5 q6)
    (h257 : 0 < orient q2 q5 q7)
    (h267 : 0 < orient q2 q6 q7)
    (h345 : 0 < orient q3 q4 q5)
    (h346 : 0 < orient q3 q4 q6)
    (h347 : 0 < orient q3 q4 q7)
    (h356 : 0 < orient q3 q5 q6)
    (h357 : 0 < orient q3 q5 q7)
    (h367 : 0 < orient q3 q6 q7)
    (h456 : 0 < orient q4 q5 q6)
    (h457 : 0 < orient q4 q5 q7)
    (h467 : 0 < orient q4 q6 q7)
    (h567 : 0 < orient q5 q6 q7)
    : HasConvexNGon 8 P := by
  have hinj : Function.Injective (![q0, q1, q2, q3, q4, q5, q6, q7] : Fin 8 → Point) := by
    intro i j hij
    fin_cases i <;> fin_cases j
    all_goals first | rfl | skip
    exacts [absurd hij d01, absurd hij d02, absurd hij d03, absurd hij d04, absurd hij d05, absurd hij d06, absurd hij d07, absurd hij.symm d01, absurd hij d12, absurd hij d13, absurd hij d14, absurd hij d15, absurd hij d16, absurd hij d17, absurd hij.symm d02, absurd hij.symm d12, absurd hij d23, absurd hij d24, absurd hij d25, absurd hij d26, absurd hij d27, absurd hij.symm d03, absurd hij.symm d13, absurd hij.symm d23, absurd hij d34, absurd hij d35, absurd hij d36, absurd hij d37, absurd hij.symm d04, absurd hij.symm d14, absurd hij.symm d24, absurd hij.symm d34, absurd hij d45, absurd hij d46, absurd hij d47, absurd hij.symm d05, absurd hij.symm d15, absurd hij.symm d25, absurd hij.symm d35, absurd hij.symm d45, absurd hij d56, absurd hij d57, absurd hij.symm d06, absurd hij.symm d16, absurd hij.symm d26, absurd hij.symm d36, absurd hij.symm d46, absurd hij.symm d56, absurd hij d67, absurd hij.symm d07, absurd hij.symm d17, absurd hij.symm d27, absurd hij.symm d37, absurd hij.symm d47, absurd hij.symm d57, absurd hij.symm d67]
  refine hasConvexNGon_of_positive_cycle (by norm_num) (![q0, q1, q2, q3, q4, q5, q6, q7] : Fin 8 → Point) hinj
    (Function.Embedding.refl _) ?_ ?_
  · intro i
    fin_cases i
    exacts [m0, m1, m2, m3, m4, m5, m6, m7]
  · intro i j l hij hjl
    fin_cases i <;> fin_cases j <;> fin_cases l
    all_goals first | exact absurd hij (by decide) | exact absurd hjl (by decide) | skip
    exacts [h012, h013, h014, h015, h016, h017, h023, h024, h025, h026, h027, h034, h035, h036, h037, h045, h046, h047, h056, h057, h067, h123, h124, h125, h126, h127, h134, h135, h136, h137, h145, h146, h147, h156, h157, h167, h234, h235, h236, h237, h245, h246, h247, h256, h257, h267, h345, h346, h347, h356, h357, h367, h456, h457, h467, h567]

theorem cap_mirror_heptagon (c0 c1 c2 c3 : Point)
    (x01 : c0 0 < c1 0)
    (x12 : c1 0 < c2 0)
    (x23 : c2 0 < c3 0)
    (y0 : 0 < c0 1)
    (y1 : 0 < c1 1)
    (y2 : 0 < c2 1)
    (y3 : 0 < c3 1)
    (o012 : orient c0 c1 c2 < 0)
    (o013 : orient c0 c1 c3 < 0)
    (o023 : orient c0 c2 c3 < 0)
    (o123 : orient c1 c2 c3 < 0)
    {P : Finset Point}
    (in_c0 : c0 ∈ P)
    (in_m1 : (mir c1) ∈ P)
    (in_m2 : (mir c2) ∈ P)
    (in_m3 : (mir c3) ∈ P)
    (in_c3 : c3 ∈ P)
    (in_c2 : c2 ∈ P)
    (in_c1 : c1 ∈ P)
    : HasConvexNGon 7 P := by
  simp only [orient] at o012 o013 o023 o123
  have p0_21 : 0 < c0 1 * (c2 0 - c1 0) := mul_pos y0 (by linarith)
  have p0_31 : 0 < c0 1 * (c3 0 - c1 0) := mul_pos y0 (by linarith)
  have p0_32 : 0 < c0 1 * (c3 0 - c2 0) := mul_pos y0 (by linarith)
  have p1_10 : 0 < c1 1 * (c1 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_20 : 0 < c1 1 * (c2 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_21 : 0 < c1 1 * (c2 0 - c1 0) := mul_pos y1 (by linarith)
  have p1_30 : 0 < c1 1 * (c3 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_31 : 0 < c1 1 * (c3 0 - c1 0) := mul_pos y1 (by linarith)
  have p1_32 : 0 < c1 1 * (c3 0 - c2 0) := mul_pos y1 (by linarith)
  have p2_10 : 0 < c2 1 * (c1 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_20 : 0 < c2 1 * (c2 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_21 : 0 < c2 1 * (c2 0 - c1 0) := mul_pos y2 (by linarith)
  have p2_30 : 0 < c2 1 * (c3 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_31 : 0 < c2 1 * (c3 0 - c1 0) := mul_pos y2 (by linarith)
  have p2_32 : 0 < c2 1 * (c3 0 - c2 0) := mul_pos y2 (by linarith)
  have p3_10 : 0 < c3 1 * (c1 0 - c0 0) := mul_pos y3 (by linarith)
  have p3_20 : 0 < c3 1 * (c2 0 - c0 0) := mul_pos y3 (by linarith)
  have p3_21 : 0 < c3 1 * (c2 0 - c1 0) := mul_pos y3 (by linarith)
  have p3_30 : 0 < c3 1 * (c3 0 - c0 0) := mul_pos y3 (by linarith)
  have p3_31 : 0 < c3 1 * (c3 0 - c1 0) := mul_pos y3 (by linarith)
  have p3_32 : 0 < c3 1 * (c3 0 - c2 0) := mul_pos y3 (by linarith)
  have d01 : c0 ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d02 : c0 ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d03 : c0 ≠ (mir c3) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d04 : c0 ≠ c3 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d05 : c0 ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d06 : c0 ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d12 : (mir c1) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d13 : (mir c1) ≠ (mir c3) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d14 : (mir c1) ≠ c3 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d15 : (mir c1) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d16 : (mir c1) ≠ c1 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d23 : (mir c2) ≠ (mir c3) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d24 : (mir c2) ≠ c3 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d25 : (mir c2) ≠ c2 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d26 : (mir c2) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d34 : (mir c3) ≠ c3 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d35 : (mir c3) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d36 : (mir c3) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d45 : c3 ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d46 : c3 ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d56 : c2 ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have h012 : 0 < orient c0 (mir c1) (mir c2) := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p0_21]
  have h013 : 0 < orient c0 (mir c1) (mir c3) := by
    simp only [orient, mir_zero, mir_one]; linarith [o013, p0_31]
  have h014 : 0 < orient c0 (mir c1) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_31, p1_30, p3_10]
  have h015 : 0 < orient c0 (mir c1) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_21, p1_20, p2_10]
  have h016 : 0 < orient c0 (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_10]
  have h023 : 0 < orient c0 (mir c2) (mir c3) := by
    simp only [orient, mir_zero, mir_one]; linarith [o023, p0_32]
  have h024 : 0 < orient c0 (mir c2) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_32, p2_30, p3_20]
  have h025 : 0 < orient c0 (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_20]
  have h026 : 0 < orient c0 (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p2_10]
  have h034 : 0 < orient c0 (mir c3) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_30]
  have h035 : 0 < orient c0 (mir c3) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [o023, p3_20]
  have h036 : 0 < orient c0 (mir c3) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o013, p3_10]
  have h045 : 0 < orient c0 c3 c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [o023]
  have h046 : 0 < orient c0 c3 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o013]
  have h056 : 0 < orient c0 c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012]
  have h123 : 0 < orient (mir c1) (mir c2) (mir c3) := by
    simp only [orient, mir_zero, mir_one]; linarith [o123]
  have h124 : 0 < orient (mir c1) (mir c2) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123, p3_21]
  have h125 : 0 < orient (mir c1) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_21]
  have h126 : 0 < orient (mir c1) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_21]
  have h134 : 0 < orient (mir c1) (mir c3) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_31]
  have h135 : 0 < orient (mir c1) (mir c3) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_32, p2_31, p3_21]
  have h136 : 0 < orient (mir c1) (mir c3) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_31]
  have h145 : 0 < orient (mir c1) c3 c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123, p1_32]
  have h146 : 0 < orient (mir c1) c3 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_31]
  have h156 : 0 < orient (mir c1) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_21]
  have h234 : 0 < orient (mir c2) (mir c3) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_32]
  have h235 : 0 < orient (mir c2) (mir c3) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_32]
  have h236 : 0 < orient (mir c2) (mir c3) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123, p1_32]
  have h245 : 0 < orient (mir c2) c3 c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_32]
  have h246 : 0 < orient (mir c2) c3 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_32, p2_31, p3_21]
  have h256 : 0 < orient (mir c2) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_21]
  have h345 : 0 < orient (mir c3) c3 c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_32]
  have h346 : 0 < orient (mir c3) c3 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_31]
  have h356 : 0 < orient (mir c3) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123, p3_21]
  have h456 : 0 < orient c3 c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123]
  exact cyc7 c0 (mir c1) (mir c2) (mir c3) c3 c2 c1 in_c0 in_m1 in_m2 in_m3 in_c3 in_c2 in_c1
    d01 d02 d03 d04 d05 d06 d12 d13 d14 d15 d16 d23 d24 d25 d26 d34 d35 d36 d45 d46 d56
    h012 h013 h014 h015 h016 h023 h024 h025 h026 h034 h035 h036 h045 h046 h056 h123 h124 h125 h126 h134 h135 h136 h145 h146 h156 h234 h235 h236 h245 h246 h256 h345 h346 h356 h456

theorem cap_mirror_octagon (c0 c1 c2 c3 : Point)
    (x01 : c0 0 < c1 0)
    (x12 : c1 0 < c2 0)
    (x23 : c2 0 < c3 0)
    (y0 : 0 < c0 1)
    (y1 : 0 < c1 1)
    (y2 : 0 < c2 1)
    (y3 : 0 < c3 1)
    (o012 : orient c0 c1 c2 < 0)
    (o013 : orient c0 c1 c3 < 0)
    (o023 : orient c0 c2 c3 < 0)
    (o123 : orient c1 c2 c3 < 0)
    {P : Finset Point}
    (in_m0 : (mir c0) ∈ P)
    (in_m1 : (mir c1) ∈ P)
    (in_m2 : (mir c2) ∈ P)
    (in_m3 : (mir c3) ∈ P)
    (in_c3 : c3 ∈ P)
    (in_c2 : c2 ∈ P)
    (in_c1 : c1 ∈ P)
    (in_c0 : c0 ∈ P)
    : HasConvexNGon 8 P := by
  simp only [orient] at o012 o013 o023 o123
  have p0_10 : 0 < c0 1 * (c1 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_20 : 0 < c0 1 * (c2 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_21 : 0 < c0 1 * (c2 0 - c1 0) := mul_pos y0 (by linarith)
  have p0_30 : 0 < c0 1 * (c3 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_31 : 0 < c0 1 * (c3 0 - c1 0) := mul_pos y0 (by linarith)
  have p0_32 : 0 < c0 1 * (c3 0 - c2 0) := mul_pos y0 (by linarith)
  have p1_10 : 0 < c1 1 * (c1 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_20 : 0 < c1 1 * (c2 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_21 : 0 < c1 1 * (c2 0 - c1 0) := mul_pos y1 (by linarith)
  have p1_30 : 0 < c1 1 * (c3 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_31 : 0 < c1 1 * (c3 0 - c1 0) := mul_pos y1 (by linarith)
  have p1_32 : 0 < c1 1 * (c3 0 - c2 0) := mul_pos y1 (by linarith)
  have p2_10 : 0 < c2 1 * (c1 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_20 : 0 < c2 1 * (c2 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_21 : 0 < c2 1 * (c2 0 - c1 0) := mul_pos y2 (by linarith)
  have p2_30 : 0 < c2 1 * (c3 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_31 : 0 < c2 1 * (c3 0 - c1 0) := mul_pos y2 (by linarith)
  have p2_32 : 0 < c2 1 * (c3 0 - c2 0) := mul_pos y2 (by linarith)
  have p3_10 : 0 < c3 1 * (c1 0 - c0 0) := mul_pos y3 (by linarith)
  have p3_20 : 0 < c3 1 * (c2 0 - c0 0) := mul_pos y3 (by linarith)
  have p3_21 : 0 < c3 1 * (c2 0 - c1 0) := mul_pos y3 (by linarith)
  have p3_30 : 0 < c3 1 * (c3 0 - c0 0) := mul_pos y3 (by linarith)
  have p3_31 : 0 < c3 1 * (c3 0 - c1 0) := mul_pos y3 (by linarith)
  have p3_32 : 0 < c3 1 * (c3 0 - c2 0) := mul_pos y3 (by linarith)
  have d01 : (mir c0) ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d02 : (mir c0) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d03 : (mir c0) ≠ (mir c3) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d04 : (mir c0) ≠ c3 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d05 : (mir c0) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d06 : (mir c0) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d07 : (mir c0) ≠ c0 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d12 : (mir c1) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d13 : (mir c1) ≠ (mir c3) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d14 : (mir c1) ≠ c3 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d15 : (mir c1) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d16 : (mir c1) ≠ c1 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d17 : (mir c1) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d23 : (mir c2) ≠ (mir c3) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d24 : (mir c2) ≠ c3 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d25 : (mir c2) ≠ c2 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d26 : (mir c2) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d27 : (mir c2) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d34 : (mir c3) ≠ c3 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d35 : (mir c3) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d36 : (mir c3) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d37 : (mir c3) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d45 : c3 ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d46 : c3 ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d47 : c3 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d56 : c2 ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d57 : c2 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d67 : c1 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have h012 : 0 < orient (mir c0) (mir c1) (mir c2) := by
    simp only [orient, mir_zero, mir_one]; linarith [o012]
  have h013 : 0 < orient (mir c0) (mir c1) (mir c3) := by
    simp only [orient, mir_zero, mir_one]; linarith [o013]
  have h014 : 0 < orient (mir c0) (mir c1) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [o013, p3_10]
  have h015 : 0 < orient (mir c0) (mir c1) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p2_10]
  have h016 : 0 < orient (mir c0) (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_10]
  have h017 : 0 < orient (mir c0) (mir c1) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_10]
  have h023 : 0 < orient (mir c0) (mir c2) (mir c3) := by
    simp only [orient, mir_zero, mir_one]; linarith [o023]
  have h024 : 0 < orient (mir c0) (mir c2) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [o023, p3_20]
  have h025 : 0 < orient (mir c0) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_20]
  have h026 : 0 < orient (mir c0) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_21, p1_20, p2_10]
  have h027 : 0 < orient (mir c0) (mir c2) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_20]
  have h034 : 0 < orient (mir c0) (mir c3) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_30]
  have h035 : 0 < orient (mir c0) (mir c3) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_32, p2_30, p3_20]
  have h036 : 0 < orient (mir c0) (mir c3) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_31, p1_30, p3_10]
  have h037 : 0 < orient (mir c0) (mir c3) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_30]
  have h045 : 0 < orient (mir c0) c3 c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [o023, p0_32]
  have h046 : 0 < orient (mir c0) c3 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o013, p0_31]
  have h047 : 0 < orient (mir c0) c3 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_30]
  have h056 : 0 < orient (mir c0) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p0_21]
  have h057 : 0 < orient (mir c0) c2 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_20]
  have h067 : 0 < orient (mir c0) c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_10]
  have h123 : 0 < orient (mir c1) (mir c2) (mir c3) := by
    simp only [orient, mir_zero, mir_one]; linarith [o123]
  have h124 : 0 < orient (mir c1) (mir c2) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123, p3_21]
  have h125 : 0 < orient (mir c1) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_21]
  have h126 : 0 < orient (mir c1) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_21]
  have h127 : 0 < orient (mir c1) (mir c2) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p0_21]
  have h134 : 0 < orient (mir c1) (mir c3) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_31]
  have h135 : 0 < orient (mir c1) (mir c3) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_32, p2_31, p3_21]
  have h136 : 0 < orient (mir c1) (mir c3) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_31]
  have h137 : 0 < orient (mir c1) (mir c3) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o013, p0_31]
  have h145 : 0 < orient (mir c1) c3 c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123, p1_32]
  have h146 : 0 < orient (mir c1) c3 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_31]
  have h147 : 0 < orient (mir c1) c3 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_31, p1_30, p3_10]
  have h156 : 0 < orient (mir c1) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_21]
  have h157 : 0 < orient (mir c1) c2 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_21, p1_20, p2_10]
  have h167 : 0 < orient (mir c1) c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_10]
  have h234 : 0 < orient (mir c2) (mir c3) c3 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_32]
  have h235 : 0 < orient (mir c2) (mir c3) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_32]
  have h236 : 0 < orient (mir c2) (mir c3) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123, p1_32]
  have h237 : 0 < orient (mir c2) (mir c3) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o023, p0_32]
  have h245 : 0 < orient (mir c2) c3 c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_32]
  have h246 : 0 < orient (mir c2) c3 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_32, p2_31, p3_21]
  have h247 : 0 < orient (mir c2) c3 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_32, p2_30, p3_20]
  have h256 : 0 < orient (mir c2) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_21]
  have h257 : 0 < orient (mir c2) c2 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_20]
  have h267 : 0 < orient (mir c2) c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p2_10]
  have h345 : 0 < orient (mir c3) c3 c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_32]
  have h346 : 0 < orient (mir c3) c3 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_31]
  have h347 : 0 < orient (mir c3) c3 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p3_30]
  have h356 : 0 < orient (mir c3) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123, p3_21]
  have h357 : 0 < orient (mir c3) c2 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o023, p3_20]
  have h367 : 0 < orient (mir c3) c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o013, p3_10]
  have h456 : 0 < orient c3 c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o123]
  have h457 : 0 < orient c3 c2 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o023]
  have h467 : 0 < orient c3 c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o013]
  have h567 : 0 < orient c2 c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012]
  exact cyc8 (mir c0) (mir c1) (mir c2) (mir c3) c3 c2 c1 c0 in_m0 in_m1 in_m2 in_m3 in_c3 in_c2 in_c1 in_c0
    d01 d02 d03 d04 d05 d06 d07 d12 d13 d14 d15 d16 d17 d23 d24 d25 d26 d27 d34 d35 d36 d37 d45 d46 d47 d56 d57 d67
    h012 h013 h014 h015 h016 h017 h023 h024 h025 h026 h027 h034 h035 h036 h037 h045 h046 h047 h056 h057 h067 h123 h124 h125 h126 h127 h134 h135 h136 h137 h145 h146 h147 h156 h157 h167 h234 h235 h236 h237 h245 h246 h247 h256 h257 h267 h345 h346 h347 h356 h357 h367 h456 h457 h467 h567

theorem axis_left_heptagon (a c0 c1 c2 : Point)
    (ha : a 1 = 0)
    (x01 : a 0 < c0 0)
    (x12 : c0 0 < c1 0)
    (x23 : c1 0 < c2 0)
    (y0 : 0 < c0 1)
    (y1 : 0 < c1 1)
    (y2 : 0 < c2 1)
    (o012 : orient a c0 c1 < 0)
    (o013 : orient a c0 c2 < 0)
    (o023 : orient a c1 c2 < 0)
    (o123 : orient c0 c1 c2 < 0)
    {P : Finset Point}
    (in_a : a ∈ P)
    (in_m0 : (mir c0) ∈ P)
    (in_m1 : (mir c1) ∈ P)
    (in_m2 : (mir c2) ∈ P)
    (in_c2 : c2 ∈ P)
    (in_c1 : c1 ∈ P)
    (in_c0 : c0 ∈ P)
    : HasConvexNGon 7 P := by
  simp only [orient, ha] at o012 o013 o023 o123
  have p0_10 : 0 < c0 1 * (c0 0 - a 0) := mul_pos y0 (by linarith)
  have p0_20 : 0 < c0 1 * (c1 0 - a 0) := mul_pos y0 (by linarith)
  have p0_21 : 0 < c0 1 * (c1 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_30 : 0 < c0 1 * (c2 0 - a 0) := mul_pos y0 (by linarith)
  have p0_31 : 0 < c0 1 * (c2 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_32 : 0 < c0 1 * (c2 0 - c1 0) := mul_pos y0 (by linarith)
  have p1_10 : 0 < c1 1 * (c0 0 - a 0) := mul_pos y1 (by linarith)
  have p1_20 : 0 < c1 1 * (c1 0 - a 0) := mul_pos y1 (by linarith)
  have p1_21 : 0 < c1 1 * (c1 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_30 : 0 < c1 1 * (c2 0 - a 0) := mul_pos y1 (by linarith)
  have p1_31 : 0 < c1 1 * (c2 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_32 : 0 < c1 1 * (c2 0 - c1 0) := mul_pos y1 (by linarith)
  have p2_10 : 0 < c2 1 * (c0 0 - a 0) := mul_pos y2 (by linarith)
  have p2_20 : 0 < c2 1 * (c1 0 - a 0) := mul_pos y2 (by linarith)
  have p2_21 : 0 < c2 1 * (c1 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_30 : 0 < c2 1 * (c2 0 - a 0) := mul_pos y2 (by linarith)
  have p2_31 : 0 < c2 1 * (c2 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_32 : 0 < c2 1 * (c2 0 - c1 0) := mul_pos y2 (by linarith)
  have d01 : a ≠ (mir c0) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d02 : a ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d03 : a ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d04 : a ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d05 : a ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d06 : a ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d12 : (mir c0) ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d13 : (mir c0) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d14 : (mir c0) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d15 : (mir c0) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d16 : (mir c0) ≠ c0 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d23 : (mir c1) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d24 : (mir c1) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d25 : (mir c1) ≠ c1 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d26 : (mir c1) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d34 : (mir c2) ≠ c2 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d35 : (mir c2) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d36 : (mir c2) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d45 : c2 ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d46 : c2 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d56 : c1 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have h012 : 0 < orient a (mir c0) (mir c1) := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012]
  have h013 : 0 < orient a (mir c0) (mir c2) := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o013]
  have h014 : 0 < orient a (mir c0) c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_30, p2_10]
  have h015 : 0 < orient a (mir c0) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_20, p1_10]
  have h016 : 0 < orient a (mir c0) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_10]
  have h023 : 0 < orient a (mir c1) (mir c2) := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o023]
  have h024 : 0 < orient a (mir c1) c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_30, p2_20]
  have h025 : 0 < orient a (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_20]
  have h026 : 0 < orient a (mir c1) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_20, p1_10]
  have h034 : 0 < orient a (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_30]
  have h035 : 0 < orient a (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_30, p2_20]
  have h036 : 0 < orient a (mir c2) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_30, p2_10]
  have h045 : 0 < orient a c2 c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o023]
  have h046 : 0 < orient a c2 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o013]
  have h056 : 0 < orient a c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012]
  have h123 : 0 < orient (mir c0) (mir c1) (mir c2) := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o123]
  have h124 : 0 < orient (mir c0) (mir c1) c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o123, p2_21]
  have h125 : 0 < orient (mir c0) (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_21]
  have h126 : 0 < orient (mir c0) (mir c1) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_21]
  have h134 : 0 < orient (mir c0) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_31]
  have h135 : 0 < orient (mir c0) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_32, p1_31, p2_21]
  have h136 : 0 < orient (mir c0) (mir c2) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_31]
  have h145 : 0 < orient (mir c0) c2 c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o123, p0_32]
  have h146 : 0 < orient (mir c0) c2 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_31]
  have h156 : 0 < orient (mir c0) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_21]
  have h234 : 0 < orient (mir c1) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_32]
  have h235 : 0 < orient (mir c1) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_32]
  have h236 : 0 < orient (mir c1) (mir c2) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o123, p0_32]
  have h245 : 0 < orient (mir c1) c2 c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_32]
  have h246 : 0 < orient (mir c1) c2 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_32, p1_31, p2_21]
  have h256 : 0 < orient (mir c1) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_21]
  have h345 : 0 < orient (mir c2) c2 c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_32]
  have h346 : 0 < orient (mir c2) c2 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_31]
  have h356 : 0 < orient (mir c2) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o123, p2_21]
  have h456 : 0 < orient c2 c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o123]
  exact cyc7 a (mir c0) (mir c1) (mir c2) c2 c1 c0 in_a in_m0 in_m1 in_m2 in_c2 in_c1 in_c0
    d01 d02 d03 d04 d05 d06 d12 d13 d14 d15 d16 d23 d24 d25 d26 d34 d35 d36 d45 d46 d56
    h012 h013 h014 h015 h016 h023 h024 h025 h026 h034 h035 h036 h045 h046 h056 h123 h124 h125 h126 h134 h135 h136 h145 h146 h156 h234 h235 h236 h245 h246 h256 h345 h346 h356 h456

theorem axis_right_heptagon (a c0 c1 c2 : Point)
    (ha : a 1 = 0)
    (x01 : c0 0 < c1 0)
    (x12 : c1 0 < c2 0)
    (x23 : c2 0 < a 0)
    (y0 : 0 < c0 1)
    (y1 : 0 < c1 1)
    (y2 : 0 < c2 1)
    (o012 : orient c0 c1 c2 < 0)
    (o013 : orient c0 c1 a < 0)
    (o023 : orient c0 c2 a < 0)
    (o123 : orient c1 c2 a < 0)
    {P : Finset Point}
    (in_m0 : (mir c0) ∈ P)
    (in_m1 : (mir c1) ∈ P)
    (in_m2 : (mir c2) ∈ P)
    (in_a : a ∈ P)
    (in_c2 : c2 ∈ P)
    (in_c1 : c1 ∈ P)
    (in_c0 : c0 ∈ P)
    : HasConvexNGon 7 P := by
  simp only [orient, ha] at o012 o013 o023 o123
  have p0_10 : 0 < c0 1 * (c1 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_20 : 0 < c0 1 * (c2 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_21 : 0 < c0 1 * (c2 0 - c1 0) := mul_pos y0 (by linarith)
  have p0_30 : 0 < c0 1 * (a 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_31 : 0 < c0 1 * (a 0 - c1 0) := mul_pos y0 (by linarith)
  have p0_32 : 0 < c0 1 * (a 0 - c2 0) := mul_pos y0 (by linarith)
  have p1_10 : 0 < c1 1 * (c1 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_20 : 0 < c1 1 * (c2 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_21 : 0 < c1 1 * (c2 0 - c1 0) := mul_pos y1 (by linarith)
  have p1_30 : 0 < c1 1 * (a 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_31 : 0 < c1 1 * (a 0 - c1 0) := mul_pos y1 (by linarith)
  have p1_32 : 0 < c1 1 * (a 0 - c2 0) := mul_pos y1 (by linarith)
  have p2_10 : 0 < c2 1 * (c1 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_20 : 0 < c2 1 * (c2 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_21 : 0 < c2 1 * (c2 0 - c1 0) := mul_pos y2 (by linarith)
  have p2_30 : 0 < c2 1 * (a 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_31 : 0 < c2 1 * (a 0 - c1 0) := mul_pos y2 (by linarith)
  have p2_32 : 0 < c2 1 * (a 0 - c2 0) := mul_pos y2 (by linarith)
  have d01 : (mir c0) ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d02 : (mir c0) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d03 : (mir c0) ≠ a := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d04 : (mir c0) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d05 : (mir c0) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d06 : (mir c0) ≠ c0 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d12 : (mir c1) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d13 : (mir c1) ≠ a := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d14 : (mir c1) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d15 : (mir c1) ≠ c1 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d16 : (mir c1) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d23 : (mir c2) ≠ a := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d24 : (mir c2) ≠ c2 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d25 : (mir c2) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d26 : (mir c2) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d34 : a ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d35 : a ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d36 : a ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d45 : c2 ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d46 : c2 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d56 : c1 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have h012 : 0 < orient (mir c0) (mir c1) (mir c2) := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012]
  have h013 : 0 < orient (mir c0) (mir c1) a := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o013]
  have h014 : 0 < orient (mir c0) (mir c1) c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012, p2_10]
  have h015 : 0 < orient (mir c0) (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_10]
  have h016 : 0 < orient (mir c0) (mir c1) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_10]
  have h023 : 0 < orient (mir c0) (mir c2) a := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o023]
  have h024 : 0 < orient (mir c0) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_20]
  have h025 : 0 < orient (mir c0) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_21, p1_20, p2_10]
  have h026 : 0 < orient (mir c0) (mir c2) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_20]
  have h034 : 0 < orient (mir c0) a c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_32, p2_30]
  have h035 : 0 < orient (mir c0) a c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_31, p1_30]
  have h036 : 0 < orient (mir c0) a c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_30]
  have h045 : 0 < orient (mir c0) c2 c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012, p0_21]
  have h046 : 0 < orient (mir c0) c2 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_20]
  have h056 : 0 < orient (mir c0) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_10]
  have h123 : 0 < orient (mir c1) (mir c2) a := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o123]
  have h124 : 0 < orient (mir c1) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_21]
  have h125 : 0 < orient (mir c1) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_21]
  have h126 : 0 < orient (mir c1) (mir c2) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012, p0_21]
  have h134 : 0 < orient (mir c1) a c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_32, p2_31]
  have h135 : 0 < orient (mir c1) a c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_31]
  have h136 : 0 < orient (mir c1) a c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_31, p1_30]
  have h145 : 0 < orient (mir c1) c2 c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_21]
  have h146 : 0 < orient (mir c1) c2 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_21, p1_20, p2_10]
  have h156 : 0 < orient (mir c1) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_10]
  have h234 : 0 < orient (mir c2) a c2 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_32]
  have h235 : 0 < orient (mir c2) a c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_32, p2_31]
  have h236 : 0 < orient (mir c2) a c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_32, p2_30]
  have h245 : 0 < orient (mir c2) c2 c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_21]
  have h246 : 0 < orient (mir c2) c2 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p2_20]
  have h256 : 0 < orient (mir c2) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012, p2_10]
  have h345 : 0 < orient a c2 c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o123]
  have h346 : 0 < orient a c2 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o023]
  have h356 : 0 < orient a c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o013]
  have h456 : 0 < orient c2 c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012]
  exact cyc7 (mir c0) (mir c1) (mir c2) a c2 c1 c0 in_m0 in_m1 in_m2 in_a in_c2 in_c1 in_c0
    d01 d02 d03 d04 d05 d06 d12 d13 d14 d15 d16 d23 d24 d25 d26 d34 d35 d36 d45 d46 d56
    h012 h013 h014 h015 h016 h023 h024 h025 h026 h034 h035 h036 h045 h046 h056 h123 h124 h125 h126 h134 h135 h136 h145 h146 h156 h234 h235 h236 h245 h246 h256 h345 h346 h356 h456

/-! ### Small k: mirror polygons for caps of length 2 and 3 (generated by gen_lean.py) -/

theorem cyc4 (q0 q1 q2 q3 : Point) {P : Finset Point}
    (m0 : q0 ∈ P)
    (m1 : q1 ∈ P)
    (m2 : q2 ∈ P)
    (m3 : q3 ∈ P)
    (d01 : q0 ≠ q1)
    (d02 : q0 ≠ q2)
    (d03 : q0 ≠ q3)
    (d12 : q1 ≠ q2)
    (d13 : q1 ≠ q3)
    (d23 : q2 ≠ q3)
    (h012 : 0 < orient q0 q1 q2)
    (h013 : 0 < orient q0 q1 q3)
    (h023 : 0 < orient q0 q2 q3)
    (h123 : 0 < orient q1 q2 q3)
    : HasConvexNGon 4 P := by
  have hinj : Function.Injective (![q0, q1, q2, q3] : Fin 4 → Point) := by
    intro i j hij
    fin_cases i <;> fin_cases j
    all_goals first | rfl | skip
    exacts [absurd hij d01, absurd hij d02, absurd hij d03, absurd hij.symm d01, absurd hij d12, absurd hij d13, absurd hij.symm d02, absurd hij.symm d12, absurd hij d23, absurd hij.symm d03, absurd hij.symm d13, absurd hij.symm d23]
  refine hasConvexNGon_of_positive_cycle (by norm_num) (![q0, q1, q2, q3] : Fin 4 → Point) hinj
    (Function.Embedding.refl _) ?_ ?_
  · intro i
    fin_cases i
    exacts [m0, m1, m2, m3]
  · intro i j l hij hjl
    fin_cases i <;> fin_cases j <;> fin_cases l
    all_goals first | exact absurd hij (by decide) | exact absurd hjl (by decide) | skip
    exacts [h012, h013, h023, h123]

theorem cyc5 (q0 q1 q2 q3 q4 : Point) {P : Finset Point}
    (m0 : q0 ∈ P)
    (m1 : q1 ∈ P)
    (m2 : q2 ∈ P)
    (m3 : q3 ∈ P)
    (m4 : q4 ∈ P)
    (d01 : q0 ≠ q1)
    (d02 : q0 ≠ q2)
    (d03 : q0 ≠ q3)
    (d04 : q0 ≠ q4)
    (d12 : q1 ≠ q2)
    (d13 : q1 ≠ q3)
    (d14 : q1 ≠ q4)
    (d23 : q2 ≠ q3)
    (d24 : q2 ≠ q4)
    (d34 : q3 ≠ q4)
    (h012 : 0 < orient q0 q1 q2)
    (h013 : 0 < orient q0 q1 q3)
    (h014 : 0 < orient q0 q1 q4)
    (h023 : 0 < orient q0 q2 q3)
    (h024 : 0 < orient q0 q2 q4)
    (h034 : 0 < orient q0 q3 q4)
    (h123 : 0 < orient q1 q2 q3)
    (h124 : 0 < orient q1 q2 q4)
    (h134 : 0 < orient q1 q3 q4)
    (h234 : 0 < orient q2 q3 q4)
    : HasConvexNGon 5 P := by
  have hinj : Function.Injective (![q0, q1, q2, q3, q4] : Fin 5 → Point) := by
    intro i j hij
    fin_cases i <;> fin_cases j
    all_goals first | rfl | skip
    exacts [absurd hij d01, absurd hij d02, absurd hij d03, absurd hij d04, absurd hij.symm d01, absurd hij d12, absurd hij d13, absurd hij d14, absurd hij.symm d02, absurd hij.symm d12, absurd hij d23, absurd hij d24, absurd hij.symm d03, absurd hij.symm d13, absurd hij.symm d23, absurd hij d34, absurd hij.symm d04, absurd hij.symm d14, absurd hij.symm d24, absurd hij.symm d34]
  refine hasConvexNGon_of_positive_cycle (by norm_num) (![q0, q1, q2, q3, q4] : Fin 5 → Point) hinj
    (Function.Embedding.refl _) ?_ ?_
  · intro i
    fin_cases i
    exacts [m0, m1, m2, m3, m4]
  · intro i j l hij hjl
    fin_cases i <;> fin_cases j <;> fin_cases l
    all_goals first | exact absurd hij (by decide) | exact absurd hjl (by decide) | skip
    exacts [h012, h013, h014, h023, h024, h034, h123, h124, h134, h234]

theorem cyc6 (q0 q1 q2 q3 q4 q5 : Point) {P : Finset Point}
    (m0 : q0 ∈ P)
    (m1 : q1 ∈ P)
    (m2 : q2 ∈ P)
    (m3 : q3 ∈ P)
    (m4 : q4 ∈ P)
    (m5 : q5 ∈ P)
    (d01 : q0 ≠ q1)
    (d02 : q0 ≠ q2)
    (d03 : q0 ≠ q3)
    (d04 : q0 ≠ q4)
    (d05 : q0 ≠ q5)
    (d12 : q1 ≠ q2)
    (d13 : q1 ≠ q3)
    (d14 : q1 ≠ q4)
    (d15 : q1 ≠ q5)
    (d23 : q2 ≠ q3)
    (d24 : q2 ≠ q4)
    (d25 : q2 ≠ q5)
    (d34 : q3 ≠ q4)
    (d35 : q3 ≠ q5)
    (d45 : q4 ≠ q5)
    (h012 : 0 < orient q0 q1 q2)
    (h013 : 0 < orient q0 q1 q3)
    (h014 : 0 < orient q0 q1 q4)
    (h015 : 0 < orient q0 q1 q5)
    (h023 : 0 < orient q0 q2 q3)
    (h024 : 0 < orient q0 q2 q4)
    (h025 : 0 < orient q0 q2 q5)
    (h034 : 0 < orient q0 q3 q4)
    (h035 : 0 < orient q0 q3 q5)
    (h045 : 0 < orient q0 q4 q5)
    (h123 : 0 < orient q1 q2 q3)
    (h124 : 0 < orient q1 q2 q4)
    (h125 : 0 < orient q1 q2 q5)
    (h134 : 0 < orient q1 q3 q4)
    (h135 : 0 < orient q1 q3 q5)
    (h145 : 0 < orient q1 q4 q5)
    (h234 : 0 < orient q2 q3 q4)
    (h235 : 0 < orient q2 q3 q5)
    (h245 : 0 < orient q2 q4 q5)
    (h345 : 0 < orient q3 q4 q5)
    : HasConvexNGon 6 P := by
  have hinj : Function.Injective (![q0, q1, q2, q3, q4, q5] : Fin 6 → Point) := by
    intro i j hij
    fin_cases i <;> fin_cases j
    all_goals first | rfl | skip
    exacts [absurd hij d01, absurd hij d02, absurd hij d03, absurd hij d04, absurd hij d05, absurd hij.symm d01, absurd hij d12, absurd hij d13, absurd hij d14, absurd hij d15, absurd hij.symm d02, absurd hij.symm d12, absurd hij d23, absurd hij d24, absurd hij d25, absurd hij.symm d03, absurd hij.symm d13, absurd hij.symm d23, absurd hij d34, absurd hij d35, absurd hij.symm d04, absurd hij.symm d14, absurd hij.symm d24, absurd hij.symm d34, absurd hij d45, absurd hij.symm d05, absurd hij.symm d15, absurd hij.symm d25, absurd hij.symm d35, absurd hij.symm d45]
  refine hasConvexNGon_of_positive_cycle (by norm_num) (![q0, q1, q2, q3, q4, q5] : Fin 6 → Point) hinj
    (Function.Embedding.refl _) ?_ ?_
  · intro i
    fin_cases i
    exacts [m0, m1, m2, m3, m4, m5]
  · intro i j l hij hjl
    fin_cases i <;> fin_cases j <;> fin_cases l
    all_goals first | exact absurd hij (by decide) | exact absurd hjl (by decide) | skip
    exacts [h012, h013, h014, h015, h023, h024, h025, h034, h035, h045, h123, h124, h125, h134, h135, h145, h234, h235, h245, h345]

theorem cap_mirror_quadrilateral (c0 c1 : Point)
    (x01 : c0 0 < c1 0)
    (y0 : 0 < c0 1)
    (y1 : 0 < c1 1)
    {P : Finset Point}
    (in_m0 : (mir c0) ∈ P)
    (in_m1 : (mir c1) ∈ P)
    (in_c1 : c1 ∈ P)
    (in_c0 : c0 ∈ P)
    : HasConvexNGon 4 P := by
  have p0_10 : 0 < c0 1 * (c1 0 - c0 0) := mul_pos y0 (by linarith)
  have p1_10 : 0 < c1 1 * (c1 0 - c0 0) := mul_pos y1 (by linarith)
  have d01 : (mir c0) ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d02 : (mir c0) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d03 : (mir c0) ≠ c0 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d12 : (mir c1) ≠ c1 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d13 : (mir c1) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d23 : c1 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have h012 : 0 < orient (mir c0) (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_10]
  have h013 : 0 < orient (mir c0) (mir c1) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_10]
  have h023 : 0 < orient (mir c0) c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_10]
  have h123 : 0 < orient (mir c1) c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_10]
  exact cyc4 (mir c0) (mir c1) c1 c0 in_m0 in_m1 in_c1 in_c0
    d01 d02 d03 d12 d13 d23
    h012 h013 h023 h123

theorem cap_mirror_hexagon (c0 c1 c2 : Point)
    (x01 : c0 0 < c1 0)
    (x12 : c1 0 < c2 0)
    (y0 : 0 < c0 1)
    (y1 : 0 < c1 1)
    (y2 : 0 < c2 1)
    (o012 : orient c0 c1 c2 < 0)
    {P : Finset Point}
    (in_m0 : (mir c0) ∈ P)
    (in_m1 : (mir c1) ∈ P)
    (in_m2 : (mir c2) ∈ P)
    (in_c2 : c2 ∈ P)
    (in_c1 : c1 ∈ P)
    (in_c0 : c0 ∈ P)
    : HasConvexNGon 6 P := by
  simp only [orient] at o012
  have p0_10 : 0 < c0 1 * (c1 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_20 : 0 < c0 1 * (c2 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_21 : 0 < c0 1 * (c2 0 - c1 0) := mul_pos y0 (by linarith)
  have p1_10 : 0 < c1 1 * (c1 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_20 : 0 < c1 1 * (c2 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_21 : 0 < c1 1 * (c2 0 - c1 0) := mul_pos y1 (by linarith)
  have p2_10 : 0 < c2 1 * (c1 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_20 : 0 < c2 1 * (c2 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_21 : 0 < c2 1 * (c2 0 - c1 0) := mul_pos y2 (by linarith)
  have d01 : (mir c0) ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d02 : (mir c0) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d03 : (mir c0) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d04 : (mir c0) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d05 : (mir c0) ≠ c0 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d12 : (mir c1) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d13 : (mir c1) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d14 : (mir c1) ≠ c1 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d15 : (mir c1) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d23 : (mir c2) ≠ c2 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d24 : (mir c2) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d25 : (mir c2) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d34 : c2 ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d35 : c2 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d45 : c1 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have h012 : 0 < orient (mir c0) (mir c1) (mir c2) := by
    simp only [orient, mir_zero, mir_one]; linarith [o012]
  have h013 : 0 < orient (mir c0) (mir c1) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p2_10]
  have h014 : 0 < orient (mir c0) (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_10]
  have h015 : 0 < orient (mir c0) (mir c1) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_10]
  have h023 : 0 < orient (mir c0) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_20]
  have h024 : 0 < orient (mir c0) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_21, p1_20, p2_10]
  have h025 : 0 < orient (mir c0) (mir c2) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_20]
  have h034 : 0 < orient (mir c0) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p0_21]
  have h035 : 0 < orient (mir c0) c2 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_20]
  have h045 : 0 < orient (mir c0) c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_10]
  have h123 : 0 < orient (mir c1) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_21]
  have h124 : 0 < orient (mir c1) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_21]
  have h125 : 0 < orient (mir c1) (mir c2) c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p0_21]
  have h134 : 0 < orient (mir c1) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_21]
  have h135 : 0 < orient (mir c1) c2 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_21, p1_20, p2_10]
  have h145 : 0 < orient (mir c1) c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_10]
  have h234 : 0 < orient (mir c2) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_21]
  have h235 : 0 < orient (mir c2) c2 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_20]
  have h245 : 0 < orient (mir c2) c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p2_10]
  have h345 : 0 < orient c2 c1 c0 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012]
  exact cyc6 (mir c0) (mir c1) (mir c2) c2 c1 c0 in_m0 in_m1 in_m2 in_c2 in_c1 in_c0
    d01 d02 d03 d04 d05 d12 d13 d14 d15 d23 d24 d25 d34 d35 d45
    h012 h013 h014 h015 h023 h024 h025 h034 h035 h045 h123 h124 h125 h134 h135 h145 h234 h235 h245 h345

theorem cap_mirror_pentagon (c0 c1 c2 : Point)
    (x01 : c0 0 < c1 0)
    (x12 : c1 0 < c2 0)
    (y0 : 0 < c0 1)
    (y1 : 0 < c1 1)
    (y2 : 0 < c2 1)
    (o012 : orient c0 c1 c2 < 0)
    {P : Finset Point}
    (in_m0 : (mir c0) ∈ P)
    (in_m1 : (mir c1) ∈ P)
    (in_m2 : (mir c2) ∈ P)
    (in_c2 : c2 ∈ P)
    (in_c1 : c1 ∈ P)
    : HasConvexNGon 5 P := by
  simp only [orient] at o012
  have p0_21 : 0 < c0 1 * (c2 0 - c1 0) := mul_pos y0 (by linarith)
  have p1_10 : 0 < c1 1 * (c1 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_20 : 0 < c1 1 * (c2 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_21 : 0 < c1 1 * (c2 0 - c1 0) := mul_pos y1 (by linarith)
  have p2_10 : 0 < c2 1 * (c1 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_20 : 0 < c2 1 * (c2 0 - c0 0) := mul_pos y2 (by linarith)
  have p2_21 : 0 < c2 1 * (c2 0 - c1 0) := mul_pos y2 (by linarith)
  have d01 : (mir c0) ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d02 : (mir c0) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d03 : (mir c0) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d04 : (mir c0) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d12 : (mir c1) ≠ (mir c2) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d13 : (mir c1) ≠ c2 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d14 : (mir c1) ≠ c1 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d23 : (mir c2) ≠ c2 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d24 : (mir c2) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d34 : c2 ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have h012 : 0 < orient (mir c0) (mir c1) (mir c2) := by
    simp only [orient, mir_zero, mir_one]; linarith [o012]
  have h013 : 0 < orient (mir c0) (mir c1) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p2_10]
  have h014 : 0 < orient (mir c0) (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_10]
  have h023 : 0 < orient (mir c0) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_20]
  have h024 : 0 < orient (mir c0) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p0_21, p1_20, p2_10]
  have h034 : 0 < orient (mir c0) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [o012, p0_21]
  have h123 : 0 < orient (mir c1) (mir c2) c2 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_21]
  have h124 : 0 < orient (mir c1) (mir c2) c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_21]
  have h134 : 0 < orient (mir c1) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p1_21]
  have h234 : 0 < orient (mir c2) c2 c1 := by
    simp only [orient, mir_zero, mir_one]; linarith [p2_21]
  exact cyc5 (mir c0) (mir c1) (mir c2) c2 c1 in_m0 in_m1 in_m2 in_c2 in_c1
    d01 d02 d03 d04 d12 d13 d14 d23 d24 d34
    h012 h013 h014 h023 h024 h034 h123 h124 h134 h234

theorem axis_left_pentagon (a c0 c1 : Point)
    (ha : a 1 = 0)
    (x01 : a 0 < c0 0)
    (x12 : c0 0 < c1 0)
    (y0 : 0 < c0 1)
    (y1 : 0 < c1 1)
    (o012 : orient a c0 c1 < 0)
    {P : Finset Point}
    (in_a : a ∈ P)
    (in_m0 : (mir c0) ∈ P)
    (in_m1 : (mir c1) ∈ P)
    (in_c1 : c1 ∈ P)
    (in_c0 : c0 ∈ P)
    : HasConvexNGon 5 P := by
  simp only [orient, ha] at o012
  have p0_10 : 0 < c0 1 * (c0 0 - a 0) := mul_pos y0 (by linarith)
  have p0_20 : 0 < c0 1 * (c1 0 - a 0) := mul_pos y0 (by linarith)
  have p0_21 : 0 < c0 1 * (c1 0 - c0 0) := mul_pos y0 (by linarith)
  have p1_10 : 0 < c1 1 * (c0 0 - a 0) := mul_pos y1 (by linarith)
  have p1_20 : 0 < c1 1 * (c1 0 - a 0) := mul_pos y1 (by linarith)
  have p1_21 : 0 < c1 1 * (c1 0 - c0 0) := mul_pos y1 (by linarith)
  have d01 : a ≠ (mir c0) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d02 : a ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d03 : a ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d04 : a ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d12 : (mir c0) ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d13 : (mir c0) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d14 : (mir c0) ≠ c0 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d23 : (mir c1) ≠ c1 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d24 : (mir c1) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d34 : c1 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have h012 : 0 < orient a (mir c0) (mir c1) := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012]
  have h013 : 0 < orient a (mir c0) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_20, p1_10]
  have h014 : 0 < orient a (mir c0) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_10]
  have h023 : 0 < orient a (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_20]
  have h024 : 0 < orient a (mir c1) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_20, p1_10]
  have h034 : 0 < orient a c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012]
  have h123 : 0 < orient (mir c0) (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_21]
  have h124 : 0 < orient (mir c0) (mir c1) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_21]
  have h134 : 0 < orient (mir c0) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_21]
  have h234 : 0 < orient (mir c1) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_21]
  exact cyc5 a (mir c0) (mir c1) c1 c0 in_a in_m0 in_m1 in_c1 in_c0
    d01 d02 d03 d04 d12 d13 d14 d23 d24 d34
    h012 h013 h014 h023 h024 h034 h123 h124 h134 h234

theorem axis_right_pentagon (a c0 c1 : Point)
    (ha : a 1 = 0)
    (x01 : c0 0 < c1 0)
    (x12 : c1 0 < a 0)
    (y0 : 0 < c0 1)
    (y1 : 0 < c1 1)
    (o012 : orient c0 c1 a < 0)
    {P : Finset Point}
    (in_m0 : (mir c0) ∈ P)
    (in_m1 : (mir c1) ∈ P)
    (in_a : a ∈ P)
    (in_c1 : c1 ∈ P)
    (in_c0 : c0 ∈ P)
    : HasConvexNGon 5 P := by
  simp only [orient, ha] at o012
  have p0_10 : 0 < c0 1 * (c1 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_20 : 0 < c0 1 * (a 0 - c0 0) := mul_pos y0 (by linarith)
  have p0_21 : 0 < c0 1 * (a 0 - c1 0) := mul_pos y0 (by linarith)
  have p1_10 : 0 < c1 1 * (c1 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_20 : 0 < c1 1 * (a 0 - c0 0) := mul_pos y1 (by linarith)
  have p1_21 : 0 < c1 1 * (a 0 - c1 0) := mul_pos y1 (by linarith)
  have d01 : (mir c0) ≠ (mir c1) := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d02 : (mir c0) ≠ a := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d03 : (mir c0) ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d04 : (mir c0) ≠ c0 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d12 : (mir c1) ≠ a := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d13 : (mir c1) ≠ c1 := fun h => by
    have e := congrFun h 1; try simp only [mir_one] at e
    linarith
  have d14 : (mir c1) ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d23 : a ≠ c1 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d24 : a ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have d34 : c1 ≠ c0 := fun h => by
    have e := congrFun h 0; try simp only [mir_zero] at e
    linarith
  have h012 : 0 < orient (mir c0) (mir c1) a := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012]
  have h013 : 0 < orient (mir c0) (mir c1) c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_10]
  have h014 : 0 < orient (mir c0) (mir c1) c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_10]
  have h023 : 0 < orient (mir c0) a c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_21, p1_20]
  have h024 : 0 < orient (mir c0) a c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_20]
  have h034 : 0 < orient (mir c0) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_10]
  have h123 : 0 < orient (mir c1) a c1 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_21]
  have h124 : 0 < orient (mir c1) a c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p0_21, p1_20]
  have h134 : 0 < orient (mir c1) c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [p1_10]
  have h234 : 0 < orient a c1 c0 := by
    simp only [orient, mir_zero, mir_one, ha]; linarith [o012]
  exact cyc5 (mir c0) (mir c1) a c1 c0 in_m0 in_m1 in_a in_c1 in_c0
    d01 d02 d03 d04 d12 d13 d14 d23 d24 d34
    h012 h013 h014 h023 h024 h034 h123 h124 h134 h234

section Baek17
open ErdosSzekeres.Omission ErdosSzekeres.Omission.BoundaryGeometry
open ErdosSzekeres.Omission.BaekGeometry ErdosSzekeres.Omission.ActualRanks

theorem hasNGon_heptagon {n} (c : Configuration n)
    (gon : (colorConfig c.cup true).HasNGon 7 (Finset.range n)) :
    HasConvexNGon 7 (Finset.univ.image c.point) := by
  obtain ⟨xs,ys,hgon,xi,yi⟩ := gon
  let k := xs.length-2
  let l := ys.length-2
  have hx : xs.length=k+2 := by have := hgon.1.1; dsimp [k]; omega
  have hy : ys.length=l+2 := by have := hgon.1.2.2.1; dsimp [l]; omega
  have seven : l+k+2=7 := by have := hgon.2; omega
  have h := boundary_polygon (boundaryOfGon c xs ys k l hx hy xi yi hgon.1)
    (Finset.univ.image c.point) (by
      simpa only [Finset.coe_image, Finset.coe_univ, Set.image_univ] using
        boundaryOfGon_inside c xs ys k l hx hy xi yi hgon.1)
  simpa only [seven] using h

/-- Baek's theorem at n = 7 in geometric form: a configuration with no geometric 4-cap and no convex
heptagon has at most 16 points. -/
theorem capacity16 {n} (c : Configuration n) (noCap : ¬ c.HasCap 4)
    (noHept : ¬ HasConvexNGon 7 (Finset.univ.image c.point)) : n ≤ 16 := by
  by_contra h
  have h15 : Nat.choose (4 + 2) 2 = 15 := by decide
  have hs : Nat.choose (4 + 2) 2 + 2 ≤ (Finset.range n).card := by
    rw [Finset.card_range, h15]; omega
  rcases main 4 (colorConfig c.cup true) (Finset.range n) hs with cap | gon
  · exact noCap (ListGeometry.hasCap_of_list c cap)
  · exact noHept (hasNGon_heptagon c gon)

end Baek17

open ErdosSzekeres.Omission

theorem mir_mir (p : Point) : mir (mir p) = p := by
  funext i; fin_cases i <;> simp [mir]

/-! ### Sorting a finite point set with distinct x-coordinates -/
section XSort

noncomputable def xset (T : Finset Point) : Finset ℝ := T.image (fun p : Point => p 0)

theorem xset_card (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) : (xset T).card = T.card := Finset.card_image_of_injOn hx

noncomputable def emb (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) : Fin T.card ↪o ℝ := (xset T).orderEmbOfFin (xset_card T hx)

theorem emb_mem (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) (i : Fin T.card) : ∃ p ∈ T, p 0 = emb T hx i :=
  Finset.mem_image.mp ((xset T).orderEmbOfFin_mem (xset_card T hx) i)

noncomputable def sortPt (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) (i : Fin T.card) : Point := Classical.choose (emb_mem T hx i)

theorem sortPt_mem (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) (i : Fin T.card) : sortPt T hx i ∈ T :=
  (Classical.choose_spec (emb_mem T hx i)).1

theorem sortPt_x (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) (i : Fin T.card) : sortPt T hx i 0 = emb T hx i :=
  (Classical.choose_spec (emb_mem T hx i)).2

theorem sortPt_strictMono (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) : StrictMono (fun i => sortPt T hx i 0) := by
  intro i j hij
  change sortPt T hx i 0 < sortPt T hx j 0
  rw [sortPt_x, sortPt_x]
  exact (emb T hx).strictMono hij

theorem sortPt_injective (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) : Function.Injective (sortPt T hx) := by
  intro i j h
  exact (sortPt_strictMono T hx).injective (congrArg (fun p : Point => p 0) h)

theorem sortPt_image (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) : Finset.univ.image (sortPt T hx) = T := by
  apply Finset.eq_of_subset_of_card_le
  · intro p hp
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.mp hp
    exact sortPt_mem T hx i
  · rw [Finset.card_image_of_injective _ (sortPt_injective T hx)]
    simp

noncomputable def cfg (T : Finset Point) (hx : Set.InjOn (fun p : Point => p 0) T) (hgp : GeneralPosition T) : Configuration T.card where
  point := sortPt T hx
  xOrder := sortPt_strictMono T hx
  generalPosition := by
    intro i j k hij hjk
    have hinj := sortPt_injective T hx
    exact (generalPosition_iff_orient_ne_zero T).mp hgp _ (sortPt_mem T hx i) _ (sortPt_mem T hx j) _
      (sortPt_mem T hx k) (hinj.ne hij.ne) (hinj.ne (hij.trans hjk).ne) (hinj.ne hjk.ne)

end XSort

/-! ### The reduction -/
section Reduction

noncomputable def Rset (S : Finset Point) : Finset Point := S.filter (fun p : Point => 0 < p 1)
noncomputable def Aset (S : Finset Point) : Finset Point := S.filter (fun p : Point => p 1 = 0)

theorem card_split (S : Finset Point) (sym : ∀ p ∈ S, mir p ∈ S) :
    S.card = 2 * (Rset S).card + (Aset S).card := by
  have h1 : (S.filter (fun p : Point => 0 < p 1)).card + (S.filter (fun p : Point => ¬ 0 < p 1)).card
      = S.card := Finset.filter_card_add_filter_neg_card_eq_card _
  have h2 : ((S.filter (fun p : Point => ¬ 0 < p 1)).filter (fun p : Point => p 1 = 0)).card
      + ((S.filter (fun p : Point => ¬ 0 < p 1)).filter (fun p : Point => ¬ p 1 = 0)).card
      = (S.filter (fun p : Point => ¬ 0 < p 1)).card := Finset.filter_card_add_filter_neg_card_eq_card _
  have eA : (S.filter (fun p : Point => ¬ 0 < p 1)).filter (fun p : Point => p 1 = 0) = Aset S := by
    ext p
    simp only [Aset, Finset.mem_filter]
    constructor
    · rintro ⟨⟨hp, -⟩, h0⟩; exact ⟨hp, h0⟩
    · rintro ⟨hp, h0⟩; exact ⟨⟨hp, by rw [h0]; exact lt_irrefl 0⟩, h0⟩
  have eL : (S.filter (fun p : Point => ¬ 0 < p 1)).filter (fun p : Point => ¬ p 1 = 0)
      = (Rset S).image mir := by
    classical
    ext p
    simp only [Rset, Finset.mem_filter, Finset.mem_image]
    constructor
    · rintro ⟨⟨hp, hle⟩, hne⟩
      have hneg : p 1 < 0 := lt_of_le_of_ne (le_of_not_gt hle) hne
      exact ⟨mir p, ⟨sym p hp, by rw [mir_one]; linarith⟩, mir_mir p⟩
    · rintro ⟨q, ⟨hq, hpos⟩, rfl⟩
      refine ⟨⟨sym q hq, ?_⟩, ?_⟩
      · rw [mir_one]; linarith
      · rw [mir_one]; intro h; linarith
  have cL : ((Rset S).image mir).card = (Rset S).card := by
    classical
    exact Finset.card_image_of_injective _ (fun a b h => by
      have := congrArg mir h
      simpa only [mir_mir] using this)
  rw [eA, eL, cL] at h2
  change (Rset S).card + _ = S.card at h1
  omega

theorem card_A_le (S : Finset Point) (gp : GeneralPosition S) : (Aset S).card ≤ 2 := by
  by_contra h
  push_neg at h
  obtain ⟨a, ha, b, hb, c, hc, hab, hac, hbc⟩ := Finset.two_lt_card.mp h
  simp only [Aset, Finset.mem_filter] at ha hb hc
  have := (generalPosition_iff_orient_ne_zero S).mp gp a ha.1 b hb.1 c hc.1 hab hac hbc
  apply this
  simp only [orient, ha.2, hb.2, hc.2]
  ring

/-- Points on or above the x-axis, with at most one on it, have distinct abscissae. -/
theorem injOn_x (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    {T : Finset Point} (hTS : T ⊆ S) (hT0 : ∀ p ∈ T, 0 ≤ p 1)
    (hT1 : ∀ p ∈ T, ∀ q ∈ T, p 1 = 0 → q 1 = 0 → p = q) :
    Set.InjOn (fun p : Point => p 0) T := by
  -- if p is strictly above the axis and q ≠ p has the same abscissa, then p, q, mir p are collinear
  have key : ∀ p ∈ T, ∀ q ∈ T, 0 < p 1 → p 0 = q 0 → p = q := by
    intro p hp q hq hp1 hpq
    by_contra hne
    have hpm : p ≠ mir p := fun h => by
      have := congrArg (fun r : Point => r 1) h
      simp only [mir_one] at this; linarith
    have hqm : q ≠ mir p := fun h => by
      have := congrArg (fun r : Point => r 1) h
      simp only [mir_one] at this
      have := hT0 q hq; linarith
    have h3 := (generalPosition_iff_orient_ne_zero S).mp gp p (hTS hp) q (hTS hq) (mir p)
      (sym p (hTS hp)) hne hpm hqm
    apply h3
    simp only [orient, mir_zero, mir_one, hpq]
    ring
  intro p hp q hq hpq
  change p 0 = q 0 at hpq
  rcases (hT0 p hp).lt_or_eq with hp1 | hp1
  · exact key p hp q hq hp1 hpq
  · rcases (hT0 q hq).lt_or_eq with hq1 | hq1
    · exact (key q hq p hp hq1 hpq.symm).symm
    · exact hT1 p hp q hq hp1.symm hq1.symm

/-- The odd-k mirror reduction for k = 7, given the three mirror-polygon lemmas. -/
theorem mirror_seven_of
    (Hcap : ∀ (c0 c1 c2 c3 : Point), c0 0 < c1 0 → c1 0 < c2 0 → c2 0 < c3 0 →
      0 < c0 1 → 0 < c1 1 → 0 < c2 1 → 0 < c3 1 →
      orient c0 c1 c2 < 0 → orient c0 c1 c3 < 0 → orient c0 c2 c3 < 0 → orient c1 c2 c3 < 0 →
      ∀ {P : Finset Point}, c0 ∈ P → mir c1 ∈ P → mir c2 ∈ P → mir c3 ∈ P → c3 ∈ P → c2 ∈ P → c1 ∈ P →
      HasConvexNGon 7 P)
    (HL : ∀ (a c0 c1 c2 : Point), a 1 = 0 → a 0 < c0 0 → c0 0 < c1 0 → c1 0 < c2 0 →
      0 < c0 1 → 0 < c1 1 → 0 < c2 1 →
      orient a c0 c1 < 0 → orient a c0 c2 < 0 → orient a c1 c2 < 0 → orient c0 c1 c2 < 0 →
      ∀ {P : Finset Point}, a ∈ P → mir c0 ∈ P → mir c1 ∈ P → mir c2 ∈ P → c2 ∈ P → c1 ∈ P → c0 ∈ P →
      HasConvexNGon 7 P)
    (HR : ∀ (a c0 c1 c2 : Point), a 1 = 0 → c0 0 < c1 0 → c1 0 < c2 0 → c2 0 < a 0 →
      0 < c0 1 → 0 < c1 1 → 0 < c2 1 →
      orient c0 c1 c2 < 0 → orient c0 c1 a < 0 → orient c0 c2 a < 0 → orient c1 c2 a < 0 →
      ∀ {P : Finset Point}, mir c0 ∈ P → mir c1 ∈ P → mir c2 ∈ P → a ∈ P → c2 ∈ P → c1 ∈ P → c0 ∈ P →
      HasConvexNGon 7 P)
    (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noHept : ¬ HasConvexNGon 7 S) : S.card ≤ 32 := by
  classical
  -- capacity of any T ⊆ S on or above the axis with at most one axis point
  have keyT : ∀ T : Finset Point, T ⊆ S → (∀ p ∈ T, 0 ≤ p 1) →
      (∀ p ∈ T, ∀ q ∈ T, p 1 = 0 → q 1 = 0 → p = q) → T.card ≤ 16 := by
    intro T hTS hT0 hT1
    have hx := injOn_x S gp sym hTS hT0 hT1
    have hgpT : GeneralPosition T := fun a ha b hb c hc => gp a (hTS ha) b (hTS hb) c (hTS hc)
    apply capacity16 (cfg T hx hgpT)
    · -- no geometric 4-cap
      rintro ⟨f, hf, hneg⟩
      set c : Fin 4 → Point := fun m => sortPt T hx (f m) with hc
      have mem : ∀ m, c m ∈ T := fun m => sortPt_mem T hx (f m)
      have xo : ∀ m m' : Fin 4, m < m' → c m 0 < c m' 0 := fun m m' h => sortPt_strictMono T hx (hf h)
      have o : ∀ m m' m'' : Fin 4, m < m' → m' < m'' → orient (c m) (c m') (c m'') < 0 :=
        fun m m' m'' h h' => hneg m m' m'' h h'
      have x01 := xo 0 1 (by decide); have x12 := xo 1 2 (by decide); have x23 := xo 2 3 (by decide)
      have o012 := o 0 1 2 (by decide) (by decide); have o013 := o 0 1 3 (by decide) (by decide)
      have o023 := o 0 2 3 (by decide) (by decide); have o123 := o 1 2 3 (by decide) (by decide)
      have inS : ∀ m, c m ∈ S := fun m => hTS (mem m)
      have minS : ∀ m, mir (c m) ∈ S := fun m => sym _ (inS m)
      have y : ∀ m, 0 ≤ c m 1 := fun m => hT0 _ (mem m)
      -- an interior point of a cap cannot lie on the axis
      have interior : ∀ p a q : Point, p 0 < a 0 → a 0 < q 0 → 0 ≤ p 1 → 0 ≤ q 1 → a 1 = 0 →
          orient p a q < 0 → False := by
        intro p a q hpa haq hp hq ha ho
        simp only [orient, ha] at ho
        nlinarith [mul_nonneg (sub_nonneg.mpr hpa.le) hq, mul_nonneg hp (sub_nonneg.mpr haq.le)]
      rcases (y 0).lt_or_eq with y0 | y0
      · rcases (y 3).lt_or_eq with y3 | y3
        · rcases (y 1).lt_or_eq with y1 | y1
          · rcases (y 2).lt_or_eq with y2 | y2
            · exact noHept (Hcap (c 0) (c 1) (c 2) (c 3) x01 x12 x23 y0 y1 y2 y3 o012 o013 o023 o123
                (inS 0) (minS 1) (minS 2) (minS 3) (inS 3) (inS 2) (inS 1))
            · exact interior (c 1) (c 2) (c 3) x12 x23 (y 1) (y 3) y2.symm o123
          · exact interior (c 0) (c 1) (c 2) x01 x12 (y 0) (y 2) y1.symm o012
        · -- c 3 on the axis: the other three are above it
          have y1 : 0 < c 1 1 := by
            rcases (y 1).lt_or_eq with h | h
            · exact h
            · exact absurd (hT1 _ (mem 1) _ (mem 3) h.symm y3.symm) (fun e => by
                have := congrArg (fun p : Point => p 0) e; simp only at this; linarith)
          have y2 : 0 < c 2 1 := by
            rcases (y 2).lt_or_eq with h | h
            · exact h
            · exact absurd (hT1 _ (mem 2) _ (mem 3) h.symm y3.symm) (fun e => by
                have := congrArg (fun p : Point => p 0) e; simp only at this; linarith)
          exact noHept (HR (c 3) (c 0) (c 1) (c 2) y3.symm x01 x12 x23 y0 y1 y2 o012 o013 o023 o123
            (minS 0) (minS 1) (minS 2) (inS 3) (inS 2) (inS 1) (inS 0))
      · -- c 0 on the axis
        have yk : ∀ m : Fin 4, m ≠ 0 → 0 < c m 1 := by
          intro m hm
          rcases (y m).lt_or_eq with h | h
          · exact h
          · exfalso
            have e := hT1 _ (mem m) _ (mem 0) h.symm y0.symm
            have hx' := congrArg (fun p : Point => p 0) e
            simp only at hx'
            have hm' : (0 : Fin 4) < m := Fin.pos_iff_ne_zero.mpr hm
            have := xo 0 m hm'
            linarith
        exact noHept (HL (c 0) (c 1) (c 2) (c 3) y0.symm x01 x12 x23 (yk 1 (by decide)) (yk 2 (by decide))
          (yk 3 (by decide)) o012 o013 o023 o123
          (inS 0) (minS 1) (minS 2) (minS 3) (inS 3) (inS 2) (inS 1))
    · -- no convex heptagon among the points of T
      intro h
      apply noHept
      have himg : Finset.univ.image (cfg T hx hgpT).point = T := sortPt_image T hx
      rw [himg] at h
      exact h.mono hTS
  -- assemble
  have hsplit := card_split S sym
  have hA := card_A_le S gp
  have hR : (Rset S).card ≤ 16 := by
    apply keyT (Rset S) (Finset.filter_subset _ _)
    · intro p hp; exact le_of_lt (Finset.mem_filter.mp hp).2
    · intro p hp q _ hp0 _
      exact absurd hp0 (ne_of_gt (Finset.mem_filter.mp hp).2)
  by_cases hAe : Aset S = ∅
  · rw [hAe, Finset.card_empty] at hsplit
    omega
  · obtain ⟨a, ha⟩ := Finset.nonempty_iff_ne_empty.mpr hAe
    have ha' := Finset.mem_filter.mp ha
    have haR : a ∉ Rset S := fun h => by
      have := (Finset.mem_filter.mp h).2
      rw [ha'.2] at this
      exact lt_irrefl 0 this
    have hT := keyT (insert a (Rset S))
      (Finset.insert_subset ha'.1 (Finset.filter_subset _ _))
      (by
        intro p hp
        rcases Finset.mem_insert.mp hp with rfl | hp
        · exact le_of_eq ha'.2.symm
        · exact le_of_lt (Finset.mem_filter.mp hp).2)
      (by
        intro p hp q hq hp0 hq0
        rcases Finset.mem_insert.mp hp with rfl | hp
        · rcases Finset.mem_insert.mp hq with rfl | hq
          · rfl
          · exact absurd hq0 (ne_of_gt (Finset.mem_filter.mp hq).2)
        · exact absurd hp0 (ne_of_gt (Finset.mem_filter.mp hp).2))
    rw [Finset.card_insert_of_notMem haR] at hT
    omega

end Reduction

/-! ### Main theorems -/

/-- **k = 7.** A finite set in general position that is symmetric under the reflection in the x-axis and
contains no 7 points in convex position has at most 32 points. -/
theorem mirror_seven (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noHept : ¬ HasConvexNGon 7 S) : S.card ≤ 32 :=
  mirror_seven_of cap_mirror_heptagon axis_left_heptagon axis_right_heptagon S gp sym noHept

section Eight
open ErdosSzekeres.Omission.BoundaryGeometry
open ErdosSzekeres.Omission.BaekGeometry ErdosSzekeres.Omission.ActualRanks

/-- Baek's theorem at n = 8 in geometric form (cf. `geometric_capacity22`). -/
theorem capacity22g {n} (c : Configuration n) (noCap : ¬ c.HasCap 4)
    (noOct : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) : n ≤ 22 := by
  have h := geometric_capacity22 c (Finset.range n) (fun _ h => h)
    (fun cap => noCap (ListGeometry.hasCap_of_list c cap)) noOct
  simpa using h

/-- **k = 8.** A finite set in general position that is symmetric under the reflection in the x-axis and
contains no 8 points in convex position has at most 46 points. -/
theorem mirror_eight (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noOct : ¬ HasConvexNGon 8 S) : S.card ≤ 46 := by
  classical
  have hR : (Rset S).card ≤ 22 := by
    set T := Rset S with hTdef
    have hTS : T ⊆ S := Finset.filter_subset _ _
    have hT0 : ∀ p ∈ T, 0 < p 1 := fun p hp => (Finset.mem_filter.mp hp).2
    have hx := injOn_x S gp sym hTS (fun p hp => le_of_lt (hT0 p hp))
      (fun p hp q _ hp0 _ => absurd hp0 (ne_of_gt (hT0 p hp)))
    have hgpT : GeneralPosition T := fun a ha b hb c hc => gp a (hTS ha) b (hTS hb) c (hTS hc)
    apply capacity22g (cfg T hx hgpT)
    · rintro ⟨f, hf, hneg⟩
      set c : Fin 4 → Point := fun m => sortPt T hx (f m) with hc
      have mem : ∀ m, c m ∈ T := fun m => sortPt_mem T hx (f m)
      have xo : ∀ m m' : Fin 4, m < m' → c m 0 < c m' 0 := fun m m' h => sortPt_strictMono T hx (hf h)
      have o : ∀ m m' m'' : Fin 4, m < m' → m' < m'' → orient (c m) (c m') (c m'') < 0 :=
        fun m m' m'' h h' => hneg m m' m'' h h'
      have inS : ∀ m, c m ∈ S := fun m => hTS (mem m)
      have minS : ∀ m, mir (c m) ∈ S := fun m => sym _ (inS m)
      exact noOct (cap_mirror_octagon (c 0) (c 1) (c 2) (c 3) (xo 0 1 (by decide)) (xo 1 2 (by decide))
        (xo 2 3 (by decide)) (hT0 _ (mem 0)) (hT0 _ (mem 1)) (hT0 _ (mem 2)) (hT0 _ (mem 3))
        (o 0 1 2 (by decide) (by decide)) (o 0 1 3 (by decide) (by decide))
        (o 0 2 3 (by decide) (by decide)) (o 1 2 3 (by decide) (by decide))
        (minS 0) (minS 1) (minS 2) (minS 3) (inS 3) (inS 2) (inS 1) (inS 0))
    · intro h
      apply noOct
      have himg : Finset.univ.image (cfg T hx hgpT).point = T := sortPt_image T hx
      rw [himg] at h
      exact h.mono hTS
  have hsplit := card_split S sym
  have hA := card_A_le S gp
  omega

end Eight

/-! ### Arbitrary mirror lines -/
section General

/-- Convex polygons are transported by injective affine maps. -/
theorem hasConvexNGon_affineMap {S : Finset Point} {n : ℕ} (h : HasConvexNGon n S)
    (f : Point →ᵃ[ℝ] Point) (hf : Function.Injective f) : HasConvexNGon n (S.image f) := by
  classical
  obtain ⟨T, hTS, hTcard, hTconv⟩ := h
  refine ⟨T.image f, Finset.image_subset_image hTS, ?_, ?_⟩
  · rw [Finset.card_image_of_injective T hf, hTcard]
  · rw [convexPosition_iff] at hTconv ⊢
    intro q hq hmem
    rw [Finset.coe_image] at hq
    obtain ⟨p, hp, rfl⟩ := hq
    apply hTconv p hp
    have he : ((↑(T.image f) : Set Point) \ {f p}) = f '' ((T : Set Point) \ {p}) := by
      rw [Set.image_diff hf, Set.image_singleton, Finset.coe_image]
    rw [he, ← f.image_convexHull] at hmem
    obtain ⟨x, hx, hxp⟩ := hmem
    have hxp' : x = p := hf hxp
    rw [hxp'] at hx
    exact hx

/-- Euclidean reflection in the line `{p | n0 * p 0 + n1 * p 1 = c}` (for a unit normal `(n0, n1)`). -/
def lineRefl (n0 n1 c : ℝ) (p : Point) : Point :=
  ![p 0 - 2 * (n0 * p 0 + n1 * p 1 - c) * n0, p 1 - 2 * (n0 * p 0 + n1 * p 1 - c) * n1]

/-- A rigid motion taking that line to the x-axis. -/
def frame (n0 n1 c : ℝ) (p : Point) : Point :=
  ![n1 * (p 0 - c * n0) - n0 * (p 1 - c * n1), n0 * (p 0 - c * n0) + n1 * (p 1 - c * n1)]

def unframeLin (n0 n1 : ℝ) : Point →ₗ[ℝ] Point where
  toFun q := ![n1 * q 0 + n0 * q 1, -(n0 * q 0) + n1 * q 1]
  map_add' p q := by ext i; fin_cases i <;> simp <;> ring
  map_smul' r p := by ext i; fin_cases i <;> simp <;> ring

/-- The inverse rigid motion, as an affine map. -/
def unframe (n0 n1 c : ℝ) : Point →ᵃ[ℝ] Point where
  toFun q := ![n1 * q 0 + n0 * q 1 + c * n0, -(n0 * q 0) + n1 * q 1 + c * n1]
  linear := unframeLin n0 n1
  map_vadd' p v := by ext i; fin_cases i <;> simp [unframeLin] <;> ring

theorem unframe_apply (n0 n1 c : ℝ) (q : Point) :
    unframe n0 n1 c q = ![n1 * q 0 + n0 * q 1 + c * n0, -(n0 * q 0) + n1 * q 1 + c * n1] := rfl

theorem unframe_frame {n0 n1 : ℝ} (c : ℝ) (hn : n0 ^ 2 + n1 ^ 2 = 1) (p : Point) :
    unframe n0 n1 c (frame n0 n1 c p) = p := by
  rw [unframe_apply]
  ext i; fin_cases i
  · simp [frame]; linear_combination (p 0 - c * n0) * hn
  · simp [frame]; linear_combination (p 1 - c * n1) * hn

theorem frame_unframe {n0 n1 : ℝ} (c : ℝ) (hn : n0 ^ 2 + n1 ^ 2 = 1) (q : Point) :
    frame n0 n1 c (unframe n0 n1 c q) = q := by
  rw [unframe_apply]
  ext i; fin_cases i
  · simp [frame]; linear_combination (q 0) * hn
  · simp [frame]; linear_combination (q 1) * hn

theorem frame_lineRefl {n0 n1 : ℝ} (c : ℝ) (hn : n0 ^ 2 + n1 ^ 2 = 1) (p : Point) :
    frame n0 n1 c (lineRefl n0 n1 c p) = mir (frame n0 n1 c p) := by
  ext i; fin_cases i
  · simp [frame, lineRefl, mir]; ring
  · simp [frame, lineRefl, mir]; linear_combination (-2 * (n0 * p 0 + n1 * p 1)) * hn

theorem orient_frame {n0 n1 : ℝ} (c : ℝ) (hn : n0 ^ 2 + n1 ^ 2 = 1) (a b d : Point) :
    orient (frame n0 n1 c a) (frame n0 n1 c b) (frame n0 n1 c d) = orient a b d := by
  simp only [orient, frame, Matrix.cons_val_zero, Matrix.cons_val_one]
  linear_combination ((b 0 - a 0) * (d 1 - a 1) - (b 1 - a 1) * (d 0 - a 0)) * hn

theorem frame_injective {n0 n1 : ℝ} (c : ℝ) (hn : n0 ^ 2 + n1 ^ 2 = 1) :
    Function.Injective (frame n0 n1 c) := by
  intro p q h
  rw [← unframe_frame c hn p, ← unframe_frame c hn q, h]

theorem unframe_injective {n0 n1 : ℝ} (c : ℝ) (hn : n0 ^ 2 + n1 ^ 2 = 1) :
    Function.Injective (unframe n0 n1 c) := by
  intro p q h
  rw [← frame_unframe c hn p, ← frame_unframe c hn q, h]

/-- Transport to the x-axis: the image of a set symmetric in the line is symmetric in the x-axis,
in general position, of the same size, and without convex `m`-gons if the original has none. -/
theorem transport {n0 n1 c : ℝ} (hn : n0 ^ 2 + n1 ^ 2 = 1) {S : Finset Point} {m : ℕ}
    (gp : GeneralPosition S) (sym : ∀ p ∈ S, lineRefl n0 n1 c p ∈ S) (noGon : ¬ HasConvexNGon m S) :
    GeneralPosition (S.image (frame n0 n1 c)) ∧ (∀ q ∈ S.image (frame n0 n1 c), mir q ∈ S.image (frame n0 n1 c))
      ∧ ¬ HasConvexNGon m (S.image (frame n0 n1 c)) ∧ (S.image (frame n0 n1 c)).card = S.card := by
  classical
  have hinj := frame_injective c hn
  refine ⟨?_, ?_, ?_, Finset.card_image_of_injective S hinj⟩
  · rw [generalPosition_iff_orient_ne_zero] at gp ⊢
    intro a ha b hb d hd hab had hbd
    obtain ⟨a', ha', rfl⟩ := Finset.mem_image.mp ha
    obtain ⟨b', hb', rfl⟩ := Finset.mem_image.mp hb
    obtain ⟨d', hd', rfl⟩ := Finset.mem_image.mp hd
    rw [orient_frame c hn]
    exact gp a' ha' b' hb' d' hd' (fun e => hab (by rw [e])) (fun e => had (by rw [e]))
      (fun e => hbd (by rw [e]))
  · intro q hq
    obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hq
    rw [← frame_lineRefl c hn]
    exact Finset.mem_image_of_mem _ (sym p hp)
  · intro h
    apply noGon
    have h2 := hasConvexNGon_affineMap h (unframe n0 n1 c) (unframe_injective c hn)
    have himg : (S.image (frame n0 n1 c)).image (unframe n0 n1 c) = S := by
      rw [Finset.image_image]
      conv_rhs => rw [← Finset.image_id (s := S)]
      apply Finset.image_congr
      intro p _
      exact unframe_frame c hn p
    rwa [himg] at h2

/-- **k = 7, any mirror line.** A finite set in general position that is symmetric under the reflection
in some line and has no 7 points in convex position has at most 32 points. -/
theorem mirror_seven_line {n0 n1 c : ℝ} (hn : n0 ^ 2 + n1 ^ 2 = 1) (S : Finset Point)
    (gp : GeneralPosition S) (sym : ∀ p ∈ S, lineRefl n0 n1 c p ∈ S) (noHept : ¬ HasConvexNGon 7 S) :
    S.card ≤ 32 := by
  obtain ⟨gp', sym', no', card'⟩ := transport hn gp sym noHept
  rw [← card']
  exact mirror_seven _ gp' sym' no'

/-- **k = 8, any mirror line.** -/
theorem mirror_eight_line {n0 n1 c : ℝ} (hn : n0 ^ 2 + n1 ^ 2 = 1) (S : Finset Point)
    (gp : GeneralPosition S) (sym : ∀ p ∈ S, lineRefl n0 n1 c p ∈ S) (noOct : ¬ HasConvexNGon 8 S) :
    S.card ≤ 46 := by
  obtain ⟨gp', sym', no', card'⟩ := transport hn gp sym noOct
  rw [← card']
  exact mirror_eight _ gp' sym' no'

end General


/-! ### Small k: reductions for k = 4, 5, 6 -/
section SmallK

/-- Three increasing indices with negative orientation form a geometric 3-cap. -/
theorem hasCap3_of {n} (c : Configuration n) {a b d : Fin n} (hab : a < b) (hbd : b < d)
    (h : orient (c.point a) (c.point b) (c.point d) < 0) : c.HasCap 3 := by
  refine ⟨![a, b, d], ?_, ?_⟩
  · intro x y hxy
    fin_cases x <;> fin_cases y
    all_goals first | exact absurd hxy (by decide) | exact hab | exact hbd | exact hab.trans hbd
  · intro x y z hxy hyz
    fin_cases x <;> fin_cases y <;> fin_cases z
    all_goals first | exact absurd hxy (by decide) | exact absurd hyz (by decide) | exact h

/-- Without a geometric 3-cap a configuration is a cup, so any `K ≥ 4` of its points form a convex K-gon. -/
theorem capacity_cup {n K : ℕ} (hK : 4 ≤ K) (c : Configuration n) (noCap : ¬ c.HasCap 3)
    (noGon : ¬ HasConvexNGon K (Finset.univ.image c.point)) : n ≤ K - 1 := by
  by_contra h
  have hKn : K ≤ n := by omega
  apply noGon
  have hp : Function.Injective c.point :=
    fun _ _ e => c.xOrder.injective (congrArg (fun p : Point => p 0) e)
  refine hasConvexNGon_of_positive_cycle hK c.point hp (Fin.castLEEmb hKn)
    (fun i => Finset.mem_image_of_mem _ (Finset.mem_univ _)) ?_
  intro i j l hij hjl
  have hij' : (Fin.castLEEmb hKn) i < (Fin.castLEEmb hKn) j := hij
  have hjl' : (Fin.castLEEmb hKn) j < (Fin.castLEEmb hKn) l := hjl
  rcases lt_or_gt_of_ne (c.generalPosition _ _ _ hij' hjl') with hneg | hpos
  · exact absurd (hasCap3_of c hij' hjl' hneg) noCap
  · exact hpos

/-- **k = 4.** -/
theorem mirror_four (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noQuad : ¬ HasConvexNGon 4 S) : S.card ≤ 4 := by
  classical
  have hR : (Rset S).card ≤ 1 := by
    by_contra h
    push_neg at h
    obtain ⟨p, hp, q, hq, hpq⟩ := Finset.one_lt_card.mp h
    have hp' := Finset.mem_filter.mp hp
    have hq' := Finset.mem_filter.mp hq
    have hx := injOn_x S gp sym (T := Rset S) (Finset.filter_subset _ _)
      (fun r hr => le_of_lt (Finset.mem_filter.mp hr).2)
      (fun r hr s _ hr0 _ => absurd hr0 (ne_of_gt (Finset.mem_filter.mp hr).2))
    have hne : p 0 ≠ q 0 := fun e => hpq (hx hp hq e)
    rcases lt_or_gt_of_ne hne with hlt | hlt
    · exact noQuad (cap_mirror_quadrilateral p q hlt hp'.2 hq'.2 (sym p hp'.1) (sym q hq'.1) hq'.1 hp'.1)
    · exact noQuad (cap_mirror_quadrilateral q p hlt hq'.2 hp'.2 (sym q hq'.1) (sym p hp'.1) hp'.1 hq'.1)
  have hsplit := card_split S sym
  have hA := card_A_le S gp
  omega

/-- **k = 5.** Odd case: axis points are absorbed (Theorem 2(a)). -/
theorem mirror_five (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noPent : ¬ HasConvexNGon 5 S) : S.card ≤ 8 := by
  classical
  have keyT : ∀ T : Finset Point, T ⊆ S → (∀ p ∈ T, 0 ≤ p 1) →
      (∀ p ∈ T, ∀ q ∈ T, p 1 = 0 → q 1 = 0 → p = q) → T.card ≤ 4 := by
    intro T hTS hT0 hT1
    have hx := injOn_x S gp sym hTS hT0 hT1
    have hgpT : GeneralPosition T := fun a ha b hb c hc => gp a (hTS ha) b (hTS hb) c (hTS hc)
    apply le_trans (capacity_cup (K := 5) (by norm_num) (cfg T hx hgpT) ?_ ?_) (by norm_num)
    · rintro ⟨f, hf, hneg⟩
      set c : Fin 3 → Point := fun m => sortPt T hx (f m) with hc
      have mem : ∀ m, c m ∈ T := fun m => sortPt_mem T hx (f m)
      have xo : ∀ m m' : Fin 3, m < m' → c m 0 < c m' 0 :=
        fun m m' h => sortPt_strictMono T hx (hf h)
      have o012 : orient (c 0) (c 1) (c 2) < 0 := hneg 0 1 2 (by decide) (by decide)
      have x01 := xo 0 1 (by decide)
      have x12 := xo 1 2 (by decide)
      have inS : ∀ m, c m ∈ S := fun m => hTS (mem m)
      have minS : ∀ m, mir (c m) ∈ S := fun m => sym _ (inS m)
      have y : ∀ m, 0 ≤ c m 1 := fun m => hT0 _ (mem m)
      have interior : ∀ p a q : Point, p 0 < a 0 → a 0 < q 0 → 0 ≤ p 1 → 0 ≤ q 1 → a 1 = 0 →
          orient p a q < 0 → False := by
        intro p a q hpa haq hp hq ha ho
        simp only [orient, ha] at ho
        nlinarith [mul_nonneg (sub_nonneg.mpr hpa.le) hq, mul_nonneg hp (sub_nonneg.mpr haq.le)]
      rcases (y 0).lt_or_eq with y0 | y0
      · rcases (y 2).lt_or_eq with y2 | y2
        · rcases (y 1).lt_or_eq with y1 | y1
          · exact noPent (cap_mirror_pentagon (c 0) (c 1) (c 2) x01 x12 y0 y1 y2 o012
              (minS 0) (minS 1) (minS 2) (inS 2) (inS 1))
          · exact interior (c 0) (c 1) (c 2) x01 x12 (y 0) (y 2) y1.symm o012
        · have y1 : 0 < c 1 1 := by
            rcases (y 1).lt_or_eq with h | h
            · exact h
            · exact absurd (hT1 _ (mem 1) _ (mem 2) h.symm y2.symm) (fun e => by
                have := congrArg (fun p : Point => p 0) e; simp only at this; linarith)
          exact noPent (axis_right_pentagon (c 2) (c 0) (c 1) y2.symm x01 x12 y0 y1 o012
            (minS 0) (minS 1) (inS 2) (inS 1) (inS 0))
      · have y1 : 0 < c 1 1 := by
          rcases (y 1).lt_or_eq with h | h
          · exact h
          · exact absurd (hT1 _ (mem 1) _ (mem 0) h.symm y0.symm) (fun e => by
              have := congrArg (fun p : Point => p 0) e; simp only at this; linarith)
        have y2 : 0 < c 2 1 := by
          rcases (y 2).lt_or_eq with h | h
          · exact h
          · exact absurd (hT1 _ (mem 2) _ (mem 0) h.symm y0.symm) (fun e => by
              have := congrArg (fun p : Point => p 0) e; simp only at this; linarith)
        exact noPent (axis_left_pentagon (c 0) (c 1) (c 2) y0.symm x01 x12 y1 y2 o012
          (inS 0) (minS 1) (minS 2) (inS 2) (inS 1))
    · intro h
      apply noPent
      have himg : Finset.univ.image (cfg T hx hgpT).point = T := sortPt_image T hx
      rw [himg] at h
      exact h.mono hTS
  have hsplit := card_split S sym
  have hA := card_A_le S gp
  have hR : (Rset S).card ≤ 4 := by
    apply keyT (Rset S) (Finset.filter_subset _ _)
    · intro p hp; exact le_of_lt (Finset.mem_filter.mp hp).2
    · intro p hp q _ hp0 _
      exact absurd hp0 (ne_of_gt (Finset.mem_filter.mp hp).2)
  by_cases hAe : Aset S = ∅
  · rw [hAe, Finset.card_empty] at hsplit
    omega
  · obtain ⟨a, ha⟩ := Finset.nonempty_iff_ne_empty.mpr hAe
    have ha' := Finset.mem_filter.mp ha
    have haR : a ∉ Rset S := fun h => by
      have := (Finset.mem_filter.mp h).2
      rw [ha'.2] at this
      exact lt_irrefl 0 this
    have hT := keyT (insert a (Rset S))
      (Finset.insert_subset ha'.1 (Finset.filter_subset _ _))
      (by
        intro p hp
        rcases Finset.mem_insert.mp hp with rfl | hp
        · exact le_of_eq ha'.2.symm
        · exact le_of_lt (Finset.mem_filter.mp hp).2)
      (by
        intro p hp q hq hp0 hq0
        rcases Finset.mem_insert.mp hp with rfl | hp
        · rcases Finset.mem_insert.mp hq with rfl | hq
          · rfl
          · exact absurd hq0 (ne_of_gt (Finset.mem_filter.mp hq).2)
        · exact absurd hp0 (ne_of_gt (Finset.mem_filter.mp hp).2))
    rw [Finset.card_insert_of_notMem haR] at hT
    omega

/-- **k = 6.** -/
theorem mirror_six (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noHex : ¬ HasConvexNGon 6 S) : S.card ≤ 12 := by
  classical
  have hR : (Rset S).card ≤ 5 := by
    set T := Rset S with hTdef
    have hTS : T ⊆ S := Finset.filter_subset _ _
    have hT0 : ∀ p ∈ T, 0 < p 1 := fun p hp => (Finset.mem_filter.mp hp).2
    have hx := injOn_x S gp sym hTS (fun p hp => le_of_lt (hT0 p hp))
      (fun p hp q _ hp0 _ => absurd hp0 (ne_of_gt (hT0 p hp)))
    have hgpT : GeneralPosition T := fun a ha b hb c hc => gp a (hTS ha) b (hTS hb) c (hTS hc)
    apply le_trans (capacity_cup (K := 6) (by norm_num) (cfg T hx hgpT) ?_ ?_) (by norm_num)
    · rintro ⟨f, hf, hneg⟩
      set c : Fin 3 → Point := fun m => sortPt T hx (f m) with hc
      have mem : ∀ m, c m ∈ T := fun m => sortPt_mem T hx (f m)
      have xo : ∀ m m' : Fin 3, m < m' → c m 0 < c m' 0 :=
        fun m m' h => sortPt_strictMono T hx (hf h)
      have inS : ∀ m, c m ∈ S := fun m => hTS (mem m)
      have minS : ∀ m, mir (c m) ∈ S := fun m => sym _ (inS m)
      exact noHex (cap_mirror_hexagon (c 0) (c 1) (c 2) (xo 0 1 (by decide)) (xo 1 2 (by decide))
        (hT0 _ (mem 0)) (hT0 _ (mem 1)) (hT0 _ (mem 2)) (hneg 0 1 2 (by decide) (by decide))
        (minS 0) (minS 1) (minS 2) (inS 2) (inS 1) (inS 0))
    · intro h
      apply noHex
      have himg : Finset.univ.image (cfg T hx hgpT).point = T := sortPt_image T hx
      rw [himg] at h
      exact h.mono hTS
  have hsplit := card_split S sym
  have hA := card_A_le S gp
  omega

theorem mirror_four_line {n0 n1 c : ℝ} (hn : n0 ^ 2 + n1 ^ 2 = 1) (S : Finset Point)
    (gp : GeneralPosition S) (sym : ∀ p ∈ S, lineRefl n0 n1 c p ∈ S) (noGon : ¬ HasConvexNGon 4 S) :
    S.card ≤ 4 := by
  obtain ⟨gp', sym', no', card'⟩ := transport hn gp sym noGon
  rw [← card']; exact mirror_four _ gp' sym' no'

theorem mirror_five_line {n0 n1 c : ℝ} (hn : n0 ^ 2 + n1 ^ 2 = 1) (S : Finset Point)
    (gp : GeneralPosition S) (sym : ∀ p ∈ S, lineRefl n0 n1 c p ∈ S) (noGon : ¬ HasConvexNGon 5 S) :
    S.card ≤ 8 := by
  obtain ⟨gp', sym', no', card'⟩ := transport hn gp sym noGon
  rw [← card']; exact mirror_five _ gp' sym' no'

theorem mirror_six_line {n0 n1 c : ℝ} (hn : n0 ^ 2 + n1 ^ 2 = 1) (S : Finset Point)
    (gp : GeneralPosition S) (sym : ∀ p ∈ S, lineRefl n0 n1 c p ∈ S) (noGon : ¬ HasConvexNGon 6 S) :
    S.card ≤ 12 := by
  obtain ⟨gp', sym', no', card'⟩ := transport hn gp sym noGon
  rw [← card']; exact mirror_six _ gp' sym' no'

end SmallK

/-! ### General k: the mirror lemma for caps of any length and the reductions of Theorem 2 -/
section GeneralK

theorem hasConvexNGon_of_le {S : Finset Point} {m n : ℕ} (h : HasConvexNGon m S) (hnm : n ≤ m) :
    HasConvexNGon n S := by
  obtain ⟨t, hts, htc, hconv⟩ := h
  exact (hconv.hasConvexNGon (by omega)).mono hts

theorem orient_mir3 (a b d : Point) : orient (mir a) (mir b) (mir d) = -orient a b d := by
  simp only [orient, mir_zero, mir_one]; ring

theorem orient_mir2 (a b d : Point) : orient (mir a) (mir b) d = -orient a b (mir d) := by
  simp only [orient, mir_zero, mir_one]; ring

theorem orient_cycl (a b d : Point) : orient a b d = orient b d a := by
  simp only [orient]; ring

theorem orient_swap12 (a b d : Point) : orient a b d = -orient b a d := by
  simp only [orient]; ring

theorem orient_rev (a b d : Point) : orient a b d = -orient d b a := by
  simp only [orient]; ring

/-- In a cap on or above the x-axis, the mirror image of a point strictly above the axis lies strictly below
every line through two points of the cap. -/
theorem cap_below_lines {m : ℕ} (c : Fin m → Point) (hx : StrictMono (fun i => c i 0))
    (hy : ∀ i, 0 ≤ c i 1) (hcap : ∀ i j l, i < j → j < l → orient (c i) (c j) (c l) < 0)
    {i j : Fin m} (l : Fin m) (hij : i < j) (hl : 0 < c l 1) :
    orient (c i) (c j) (mir (c l)) < 0 := by
  have hxij : c i 0 < c j 0 := hx hij
  have hp : 0 < c l 1 * (c j 0 - c i 0) := mul_pos hl (sub_pos.mpr hxij)
  rcases lt_trichotomy l i with hli | hli | hli
  · have h1 := hcap l i j hli hij
    simp only [orient, mir_zero, mir_one] at h1 ⊢
    nlinarith
  · subst hli
    simp only [orient, mir_zero, mir_one]
    nlinarith
  · rcases lt_trichotomy l j with hlj | hlj | hlj
    · have hxil : c i 0 < c l 0 := hx hli
      have hxlj : c l 0 < c j 0 := hx hlj
      have q1 : 0 ≤ c i 1 * (c j 0 - c l 0) := mul_nonneg (hy i) (sub_nonneg.mpr hxlj.le)
      have q2 : 0 ≤ c j 1 * (c l 0 - c i 0) := mul_nonneg (hy j) (sub_nonneg.mpr hxil.le)
      simp only [orient, mir_zero, mir_one]
      nlinarith
    · subst hlj
      simp only [orient, mir_zero, mir_one]
      nlinarith
    · have h1 := hcap i j l hij hlj
      simp only [orient, mir_zero, mir_one] at h1 ⊢
      nlinarith

/-- **Mirror lemma (no axis point).** A cap of `m ≥ 2` points strictly above the x-axis, together with the
mirror images, is a convex `2m`-gon. -/
theorem cap_mirror_polygon {m : ℕ} (hm : 2 ≤ m) (c : Fin m → Point) (hx : StrictMono (fun i => c i 0))
    (hy : ∀ i, 0 < c i 1) (hcap : ∀ i j l, i < j → j < l → orient (c i) (c j) (c l) < 0)
    {P : Finset Point} (hP : ∀ i, c i ∈ P) (hPm : ∀ i, mir (c i) ∈ P) : HasConvexNGon (2 * m) P := by
  classical
  have hy' : ∀ i, 0 ≤ c i 1 := fun i => (hy i).le
  let q : Fin (2 * m) → Point := fun r =>
    if h : r.val < m then mir (c ⟨r.val, h⟩) else c ⟨2 * m - 1 - r.val, by omega⟩
  have hq : ∀ r : Fin (2 * m), q r =
      (if h : r.val < m then mir (c ⟨r.val, h⟩) else c ⟨2 * m - 1 - r.val, by omega⟩) := fun r => rfl
  have hmem : ∀ r, q r ∈ P := by
    intro r
    by_cases h : r.val < m
    · rw [hq, dif_pos h]; exact hPm _
    · rw [hq, dif_neg h]; exact hP _
  have hpos : ∀ r s t : Fin (2 * m), r < s → s < t → 0 < orient (q r) (q s) (q t) := by
    intro r s t hrs hst
    have hrs' : r.val < s.val := hrs
    have hst' : s.val < t.val := hst
    by_cases ht : t.val < m
    · have hr : r.val < m := by omega
      have hs : s.val < m := by omega
      rw [hq r, hq s, hq t, dif_pos hr, dif_pos hs, dif_pos ht, orient_mir3]
      have := hcap ⟨r.val, hr⟩ ⟨s.val, hs⟩ ⟨t.val, ht⟩ hrs hst
      linarith
    · by_cases hs : s.val < m
      · have hr : r.val < m := by omega
        rw [hq r, hq s, hq t, dif_pos hr, dif_pos hs, dif_neg ht, orient_mir2]
        have := cap_below_lines c hx hy' hcap (i := ⟨r.val, hr⟩) (j := ⟨s.val, hs⟩)
          ⟨2 * m - 1 - t.val, by omega⟩ hrs (hy _)
        linarith
      · by_cases hr : r.val < m
        · rw [hq r, hq s, hq t, dif_pos hr, dif_neg hs, dif_neg ht, orient_cycl, orient_swap12]
          have := cap_below_lines c hx hy' hcap (i := ⟨2 * m - 1 - t.val, by omega⟩)
            (j := ⟨2 * m - 1 - s.val, by omega⟩) ⟨r.val, hr⟩
            (show (⟨2 * m - 1 - t.val, by omega⟩ : Fin m) < ⟨2 * m - 1 - s.val, by omega⟩ from by
              show 2 * m - 1 - t.val < 2 * m - 1 - s.val; omega) (hy _)
          linarith
        · rw [hq r, hq s, hq t, dif_neg hr, dif_neg hs, dif_neg ht, orient_rev]
          have := hcap ⟨2 * m - 1 - t.val, by omega⟩ ⟨2 * m - 1 - s.val, by omega⟩
            ⟨2 * m - 1 - r.val, by omega⟩
            (show (⟨2 * m - 1 - t.val, by omega⟩ : Fin m) < ⟨2 * m - 1 - s.val, by omega⟩ from by
              show 2 * m - 1 - t.val < 2 * m - 1 - s.val; omega)
            (show (⟨2 * m - 1 - s.val, by omega⟩ : Fin m) < ⟨2 * m - 1 - r.val, by omega⟩ from by
              show 2 * m - 1 - s.val < 2 * m - 1 - r.val; omega)
          linarith
  have hinj : Function.Injective q := by
    intro r s hrs
    by_contra hne
    have hne' : r.val ≠ s.val := fun h => hne (Fin.ext h)
    have hrb : r.val < 2 * m := r.isLt
    have hsb : s.val < 2 * m := s.isLt
    by_cases hr : r.val < m <;> by_cases hs : s.val < m
    · rw [hq r, hq s, dif_pos hr, dif_pos hs] at hrs
      have e := congrArg (fun p : Point => p 0) hrs
      simp only [mir_zero] at e
      exact hne' (Fin.mk.inj (hx.injective e))
    · rw [hq r, hq s, dif_pos hr, dif_neg hs] at hrs
      have e := congrArg (fun p : Point => p 1) hrs
      simp only [mir_one] at e
      have h1 := hy ⟨r.val, hr⟩
      have h2 := hy ⟨2 * m - 1 - s.val, by omega⟩
      linarith
    · rw [hq r, hq s, dif_neg hr, dif_pos hs] at hrs
      have e := congrArg (fun p : Point => p 1) hrs
      simp only [mir_one] at e
      have h1 := hy ⟨s.val, hs⟩
      have h2 := hy ⟨2 * m - 1 - r.val, by omega⟩
      linarith
    · rw [hq r, hq s, dif_neg hr, dif_neg hs] at hrs
      have e := congrArg (fun p : Point => p 0) hrs
      have := Fin.mk.inj (hx.injective e)
      omega
  exact hasConvexNGon_of_positive_cycle (by omega) q hinj (Function.Embedding.refl _) (fun i => hmem i) hpos

/-- **Mirror lemma, axis point first.** A cap `c 0, …, c (m-1)` (`m ≥ 3`) with `c 0` on the x-axis and the others
strictly above it, together with the mirror images, is a convex `(2m-1)`-gon. -/
theorem axis_left_polygon {m : ℕ} (hm : 3 ≤ m) (c : Fin m → Point) (hx : StrictMono (fun i => c i 0))
    (h0 : c ⟨0, by omega⟩ 1 = 0) (hy : ∀ i : Fin m, 0 < i.val → 0 < c i 1)
    (hcap : ∀ i j l, i < j → j < l → orient (c i) (c j) (c l) < 0)
    {P : Finset Point} (hP : ∀ i, c i ∈ P) (hPm : ∀ i, mir (c i) ∈ P) : HasConvexNGon (2 * m - 1) P := by
  classical
  have hy' : ∀ i, 0 ≤ c i 1 := by
    intro i
    by_cases hi : 0 < i.val
    · exact (hy i hi).le
    · have : i = ⟨0, by omega⟩ := Fin.ext (by show i.val = 0; omega)
      rw [this, h0]
  let q : Fin (2 * m - 1) → Point := fun r =>
    if h : r.val < m then mir (c ⟨r.val, h⟩) else c ⟨2 * m - 1 - r.val, by omega⟩
  have hq : ∀ r : Fin (2 * m - 1), q r =
      (if h : r.val < m then mir (c ⟨r.val, h⟩) else c ⟨2 * m - 1 - r.val, by omega⟩) := fun r => rfl
  have hmem : ∀ r, q r ∈ P := by
    intro r
    by_cases h : r.val < m
    · rw [hq, dif_pos h]; exact hPm _
    · rw [hq, dif_neg h]; exact hP _
  have hpos : ∀ r s t : Fin (2 * m - 1), r < s → s < t → 0 < orient (q r) (q s) (q t) := by
    intro r s t hrs hst
    have hrs' : r.val < s.val := hrs
    have hst' : s.val < t.val := hst
    have htb : t.val < 2 * m - 1 := t.isLt
    by_cases ht : t.val < m
    · have hr : r.val < m := by omega
      have hs : s.val < m := by omega
      rw [hq r, hq s, hq t, dif_pos hr, dif_pos hs, dif_pos ht, orient_mir3]
      have := hcap ⟨r.val, hr⟩ ⟨s.val, hs⟩ ⟨t.val, ht⟩ hrs hst
      linarith
    · by_cases hs : s.val < m
      · have hr : r.val < m := by omega
        rw [hq r, hq s, hq t, dif_pos hr, dif_pos hs, dif_neg ht, orient_mir2]
        have := cap_below_lines c hx hy' hcap (i := ⟨r.val, hr⟩) (j := ⟨s.val, hs⟩)
          ⟨2 * m - 1 - t.val, by omega⟩ hrs (hy _ (by show 0 < 2 * m - 1 - t.val; omega))
        linarith
      · by_cases hr : r.val < m
        · rw [hq r, hq s, hq t, dif_pos hr, dif_neg hs, dif_neg ht]
          by_cases hr0 : r.val = 0
          · -- the axis point: mir (c 0) and c 0 have the same coordinates
            have hcap' := hcap ⟨0, by omega⟩ ⟨2 * m - 1 - t.val, by omega⟩ ⟨2 * m - 1 - s.val, by omega⟩
              (show (⟨0, by omega⟩ : Fin m) < ⟨2 * m - 1 - t.val, by omega⟩ from by
                show 0 < 2 * m - 1 - t.val; omega)
              (show (⟨2 * m - 1 - t.val, by omega⟩ : Fin m) < ⟨2 * m - 1 - s.val, by omega⟩ from by
                show 2 * m - 1 - t.val < 2 * m - 1 - s.val; omega)
            have e : (⟨r.val, hr⟩ : Fin m) = ⟨0, by omega⟩ := Fin.ext hr0
            rw [e]
            simp only [orient, mir_zero, mir_one, h0] at hcap' ⊢
            linarith
          · rw [orient_cycl, orient_swap12]
            have := cap_below_lines c hx hy' hcap (i := ⟨2 * m - 1 - t.val, by omega⟩)
              (j := ⟨2 * m - 1 - s.val, by omega⟩) ⟨r.val, hr⟩
              (show (⟨2 * m - 1 - t.val, by omega⟩ : Fin m) < ⟨2 * m - 1 - s.val, by omega⟩ from by
                show 2 * m - 1 - t.val < 2 * m - 1 - s.val; omega) (hy _ (by show 0 < r.val; omega))
            linarith
        · rw [hq r, hq s, hq t, dif_neg hr, dif_neg hs, dif_neg ht, orient_rev]
          have := hcap ⟨2 * m - 1 - t.val, by omega⟩ ⟨2 * m - 1 - s.val, by omega⟩
            ⟨2 * m - 1 - r.val, by omega⟩
            (show (⟨2 * m - 1 - t.val, by omega⟩ : Fin m) < ⟨2 * m - 1 - s.val, by omega⟩ from by
              show 2 * m - 1 - t.val < 2 * m - 1 - s.val; omega)
            (show (⟨2 * m - 1 - s.val, by omega⟩ : Fin m) < ⟨2 * m - 1 - r.val, by omega⟩ from by
              show 2 * m - 1 - s.val < 2 * m - 1 - r.val; omega)
          linarith
  have hinj : Function.Injective q := by
    intro r s hrs
    by_contra hne
    have hne' : r.val ≠ s.val := fun h => hne (Fin.ext h)
    have hrb : r.val < 2 * m - 1 := r.isLt
    have hsb : s.val < 2 * m - 1 := s.isLt
    by_cases hr : r.val < m <;> by_cases hs : s.val < m
    · rw [hq r, hq s, dif_pos hr, dif_pos hs] at hrs
      have e := congrArg (fun p : Point => p 0) hrs
      simp only [mir_zero] at e
      exact hne' (Fin.mk.inj (hx.injective e))
    · rw [hq r, hq s, dif_pos hr, dif_neg hs] at hrs
      have e := congrArg (fun p : Point => p 1) hrs
      simp only [mir_one] at e
      have h1 := hy' ⟨r.val, hr⟩
      have h2 := hy ⟨2 * m - 1 - s.val, by omega⟩ (by show 0 < 2 * m - 1 - s.val; omega)
      linarith
    · rw [hq r, hq s, dif_neg hr, dif_pos hs] at hrs
      have e := congrArg (fun p : Point => p 1) hrs
      simp only [mir_one] at e
      have h1 := hy' ⟨s.val, hs⟩
      have h2 := hy ⟨2 * m - 1 - r.val, by omega⟩ (by show 0 < 2 * m - 1 - r.val; omega)
      linarith
    · rw [hq r, hq s, dif_neg hr, dif_neg hs] at hrs
      have e := congrArg (fun p : Point => p 0) hrs
      have := Fin.mk.inj (hx.injective e)
      omega
  exact hasConvexNGon_of_positive_cycle (by omega) q hinj (Function.Embedding.refl _) (fun i => hmem i) hpos

/-- **Mirror lemma, axis point last.** -/
theorem axis_right_polygon {m : ℕ} (hm : 3 ≤ m) (c : Fin m → Point) (hx : StrictMono (fun i => c i 0))
    (hlast : c ⟨m - 1, by omega⟩ 1 = 0) (hy : ∀ i : Fin m, i.val < m - 1 → 0 < c i 1)
    (hcap : ∀ i j l, i < j → j < l → orient (c i) (c j) (c l) < 0)
    {P : Finset Point} (hP : ∀ i, c i ∈ P) (hPm : ∀ i, mir (c i) ∈ P) : HasConvexNGon (2 * m - 1) P := by
  classical
  have hy' : ∀ i, 0 ≤ c i 1 := by
    intro i
    by_cases hi : i.val < m - 1
    · exact (hy i hi).le
    · have : i = ⟨m - 1, by omega⟩ := Fin.ext (by show i.val = m - 1; have := i.isLt; omega)
      rw [this, hlast]
  let q : Fin (2 * m - 1) → Point := fun r =>
    if h : r.val < m then mir (c ⟨r.val, h⟩) else c ⟨2 * m - 2 - r.val, by omega⟩
  have hq : ∀ r : Fin (2 * m - 1), q r =
      (if h : r.val < m then mir (c ⟨r.val, h⟩) else c ⟨2 * m - 2 - r.val, by omega⟩) := fun r => rfl
  have hmem : ∀ r, q r ∈ P := by
    intro r
    by_cases h : r.val < m
    · rw [hq, dif_pos h]; exact hPm _
    · rw [hq, dif_neg h]; exact hP _
  have hpos : ∀ r s t : Fin (2 * m - 1), r < s → s < t → 0 < orient (q r) (q s) (q t) := by
    intro r s t hrs hst
    have hrs' : r.val < s.val := hrs
    have hst' : s.val < t.val := hst
    have htb : t.val < 2 * m - 1 := t.isLt
    by_cases ht : t.val < m
    · have hr : r.val < m := by omega
      have hs : s.val < m := by omega
      rw [hq r, hq s, hq t, dif_pos hr, dif_pos hs, dif_pos ht, orient_mir3]
      have := hcap ⟨r.val, hr⟩ ⟨s.val, hs⟩ ⟨t.val, ht⟩ hrs hst
      linarith
    · by_cases hs : s.val < m
      · have hr : r.val < m := by omega
        rw [hq r, hq s, hq t, dif_pos hr, dif_pos hs, dif_neg ht, orient_mir2]
        have := cap_below_lines c hx hy' hcap (i := ⟨r.val, hr⟩) (j := ⟨s.val, hs⟩)
          ⟨2 * m - 2 - t.val, by omega⟩ hrs (hy _ (by show 2 * m - 2 - t.val < m - 1; omega))
        linarith
      · by_cases hr : r.val < m
        · rw [hq r, hq s, hq t, dif_pos hr, dif_neg hs, dif_neg ht]
          by_cases hr0 : r.val = m - 1
          · have hcap' := hcap ⟨2 * m - 2 - t.val, by omega⟩ ⟨2 * m - 2 - s.val, by omega⟩ ⟨m - 1, by omega⟩
              (show (⟨2 * m - 2 - t.val, by omega⟩ : Fin m) < ⟨2 * m - 2 - s.val, by omega⟩ from by
                show 2 * m - 2 - t.val < 2 * m - 2 - s.val; omega)
              (show (⟨2 * m - 2 - s.val, by omega⟩ : Fin m) < ⟨m - 1, by omega⟩ from by
                show 2 * m - 2 - s.val < m - 1; omega)
            have e : (⟨r.val, hr⟩ : Fin m) = ⟨m - 1, by omega⟩ := Fin.ext hr0
            rw [e]
            simp only [orient, mir_zero, mir_one, hlast] at hcap' ⊢
            linarith
          · rw [orient_cycl, orient_swap12]
            have := cap_below_lines c hx hy' hcap (i := ⟨2 * m - 2 - t.val, by omega⟩)
              (j := ⟨2 * m - 2 - s.val, by omega⟩) ⟨r.val, hr⟩
              (show (⟨2 * m - 2 - t.val, by omega⟩ : Fin m) < ⟨2 * m - 2 - s.val, by omega⟩ from by
                show 2 * m - 2 - t.val < 2 * m - 2 - s.val; omega) (hy _ (by show r.val < m - 1; omega))
            linarith
        · rw [hq r, hq s, hq t, dif_neg hr, dif_neg hs, dif_neg ht, orient_rev]
          have := hcap ⟨2 * m - 2 - t.val, by omega⟩ ⟨2 * m - 2 - s.val, by omega⟩
            ⟨2 * m - 2 - r.val, by omega⟩
            (show (⟨2 * m - 2 - t.val, by omega⟩ : Fin m) < ⟨2 * m - 2 - s.val, by omega⟩ from by
              show 2 * m - 2 - t.val < 2 * m - 2 - s.val; omega)
            (show (⟨2 * m - 2 - s.val, by omega⟩ : Fin m) < ⟨2 * m - 2 - r.val, by omega⟩ from by
              show 2 * m - 2 - s.val < 2 * m - 2 - r.val; omega)
          linarith
  have hinj : Function.Injective q := by
    intro r s hrs
    by_contra hne
    have hne' : r.val ≠ s.val := fun h => hne (Fin.ext h)
    have hrb : r.val < 2 * m - 1 := r.isLt
    have hsb : s.val < 2 * m - 1 := s.isLt
    by_cases hr : r.val < m <;> by_cases hs : s.val < m
    · rw [hq r, hq s, dif_pos hr, dif_pos hs] at hrs
      have e := congrArg (fun p : Point => p 0) hrs
      simp only [mir_zero] at e
      exact hne' (Fin.mk.inj (hx.injective e))
    · rw [hq r, hq s, dif_pos hr, dif_neg hs] at hrs
      have e := congrArg (fun p : Point => p 1) hrs
      simp only [mir_one] at e
      have h1 := hy' ⟨r.val, hr⟩
      have h2 := hy ⟨2 * m - 2 - s.val, by omega⟩ (by show 2 * m - 2 - s.val < m - 1; omega)
      linarith
    · rw [hq r, hq s, dif_neg hr, dif_pos hs] at hrs
      have e := congrArg (fun p : Point => p 1) hrs
      simp only [mir_one] at e
      have h1 := hy' ⟨s.val, hs⟩
      have h2 := hy ⟨2 * m - 2 - r.val, by omega⟩ (by show 2 * m - 2 - r.val < m - 1; omega)
      linarith
    · rw [hq r, hq s, dif_neg hr, dif_neg hs] at hrs
      have e := congrArg (fun p : Point => p 0) hrs
      have := Fin.mk.inj (hx.injective e)
      omega
  exact hasConvexNGon_of_positive_cycle (by omega) q hinj (Function.Embedding.refl _) (fun i => hmem i) hpos

/-- **Theorem 2(a), Lean form.** Let `k = 2j+1` with `j ≥ 2`. If every x-sorted configuration without a
`(j+1)`-cap and without a convex `k`-gon has at most `M` points, then every finite set in general position that
is symmetric in the x-axis and has no convex `k`-gon has at most `2M` points. -/
theorem mirror_odd_general (j M : ℕ) (hj : 2 ≤ j)
    (hM : ∀ (n : ℕ) (c : Configuration n), ¬ c.HasCap (j + 1) →
      ¬ HasConvexNGon (2 * j + 1) (Finset.univ.image c.point) → n ≤ M)
    (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noGon : ¬ HasConvexNGon (2 * j + 1) S) : S.card ≤ 2 * M := by
  classical
  have keyT : ∀ T : Finset Point, T ⊆ S → (∀ p ∈ T, 0 ≤ p 1) →
      (∀ p ∈ T, ∀ q ∈ T, p 1 = 0 → q 1 = 0 → p = q) → T.card ≤ M := by
    intro T hTS hT0 hT1
    have hx := injOn_x S gp sym hTS hT0 hT1
    have hgpT : GeneralPosition T := fun a ha b hb c hc => gp a (hTS ha) b (hTS hb) c (hTS hc)
    apply hM T.card (cfg T hx hgpT)
    · rintro ⟨f, hf, hneg⟩
      let c : Fin (j + 1) → Point := fun i => sortPt T hx (f i)
      have mem : ∀ i, c i ∈ T := fun i => sortPt_mem T hx (f i)
      have xo : StrictMono (fun i => c i 0) := fun i i' h => sortPt_strictMono T hx (hf h)
      have hcap : ∀ i i' i'', i < i' → i' < i'' → orient (c i) (c i') (c i'') < 0 :=
        fun i i' i'' h h' => hneg i i' i'' h h'
      have inS : ∀ i, c i ∈ S := fun i => hTS (mem i)
      have minS : ∀ i, mir (c i) ∈ S := fun i => sym _ (inS i)
      have y : ∀ i, 0 ≤ c i 1 := fun i => hT0 _ (mem i)
      by_cases hall : ∀ i, 0 < c i 1
      · exact noGon (hasConvexNGon_of_le (cap_mirror_polygon (m := j + 1) (by omega) c xo hall hcap inS minS)
          (by omega))
      · push_neg at hall
        obtain ⟨i0, hi0⟩ := hall
        have hz : c i0 1 = 0 := le_antisymm hi0 (y i0)
        have others : ∀ i, i ≠ i0 → 0 < c i 1 := by
          intro i hi
          rcases (y i).lt_or_eq with h | h
          · exact h
          · exfalso
            have e := hT1 _ (mem i) _ (mem i0) h.symm hz
            exact hi (xo.injective (congrArg (fun p : Point => p 0) e))
        by_cases hfirst : i0.val = 0
        · have he : i0 = ⟨0, by omega⟩ := Fin.ext hfirst
          have hpoly := axis_left_polygon (m := j + 1) (by omega) c xo (by rw [← he]; exact hz)
            (fun i hi => others i (fun h => by rw [h] at hi; omega)) hcap inS minS
          exact noGon ((show 2 * (j + 1) - 1 = 2 * j + 1 by omega) ▸ hpoly)
        · by_cases hlast : i0.val = j
          · have he : i0 = ⟨j + 1 - 1, by omega⟩ := Fin.ext (by show i0.val = j + 1 - 1; omega)
            have hpoly := axis_right_polygon (m := j + 1) (by omega) c xo (by rw [← he]; exact hz)
              (fun i hi => others i (fun h => by rw [h] at hi; omega)) hcap inS minS
            exact noGon ((show 2 * (j + 1) - 1 = 2 * j + 1 by omega) ▸ hpoly)
          · -- an interior point of a cap cannot lie on the axis
            have hb : i0.val + 1 < j + 1 := by have := i0.isLt; omega
            have ha : i0.val - 1 < j + 1 := by omega
            have h1 := hcap ⟨i0.val - 1, ha⟩ i0 ⟨i0.val + 1, hb⟩
              (show (⟨i0.val - 1, ha⟩ : Fin (j + 1)) < i0 from by
                show i0.val - 1 < i0.val; omega)
              (show i0 < (⟨i0.val + 1, hb⟩ : Fin (j + 1)) from by
                show i0.val < i0.val + 1; omega)
            have hxa : c ⟨i0.val - 1, ha⟩ 0 < c i0 0 := xo (show (⟨i0.val - 1, ha⟩ : Fin (j + 1)) < i0 from by
                show i0.val - 1 < i0.val; omega)
            have hxb : c i0 0 < c ⟨i0.val + 1, hb⟩ 0 := xo (show i0 < (⟨i0.val + 1, hb⟩ : Fin (j + 1)) from by
                show i0.val < i0.val + 1; omega)
            have ya := y ⟨i0.val - 1, ha⟩
            have yb := y ⟨i0.val + 1, hb⟩
            simp only [orient, hz] at h1
            nlinarith [mul_nonneg (sub_nonneg.mpr hxa.le) yb, mul_nonneg ya (sub_nonneg.mpr hxb.le)]
    · intro h
      apply noGon
      have himg : Finset.univ.image (cfg T hx hgpT).point = T := sortPt_image T hx
      rw [himg] at h
      exact h.mono hTS
  have hsplit := card_split S sym
  have hA := card_A_le S gp
  have hR : (Rset S).card ≤ M := by
    apply keyT (Rset S) (Finset.filter_subset _ _)
    · intro p hp; exact le_of_lt (Finset.mem_filter.mp hp).2
    · intro p hp q _ hp0 _
      exact absurd hp0 (ne_of_gt (Finset.mem_filter.mp hp).2)
  by_cases hAe : Aset S = ∅
  · rw [hAe, Finset.card_empty] at hsplit
    omega
  · obtain ⟨a, ha⟩ := Finset.nonempty_iff_ne_empty.mpr hAe
    have ha' := Finset.mem_filter.mp ha
    have haR : a ∉ Rset S := fun h => by
      have := (Finset.mem_filter.mp h).2
      rw [ha'.2] at this
      exact lt_irrefl 0 this
    have hT := keyT (insert a (Rset S))
      (Finset.insert_subset ha'.1 (Finset.filter_subset _ _))
      (by
        intro p hp
        rcases Finset.mem_insert.mp hp with rfl | hp
        · exact le_of_eq ha'.2.symm
        · exact le_of_lt (Finset.mem_filter.mp hp).2)
      (by
        intro p hp q hq hp0 hq0
        rcases Finset.mem_insert.mp hp with rfl | hp
        · rcases Finset.mem_insert.mp hq with rfl | hq
          · rfl
          · exact absurd hq0 (ne_of_gt (Finset.mem_filter.mp hq).2)
        · exact absurd hp0 (ne_of_gt (Finset.mem_filter.mp hp).2))
    rw [Finset.card_insert_of_notMem haR] at hT
    omega

/-- **Theorem 2(b), Lean form.** Let `k = 2j` with `j ≥ 2`. If every x-sorted configuration without a `j`-cap and
without a convex `k`-gon has at most `M` points, then every finite set in general position that is symmetric in
the x-axis and has no convex `k`-gon has at most `2M + 2` points. -/
theorem mirror_even_general (j M : ℕ) (hj : 2 ≤ j)
    (hM : ∀ (n : ℕ) (c : Configuration n), ¬ c.HasCap j →
      ¬ HasConvexNGon (2 * j) (Finset.univ.image c.point) → n ≤ M)
    (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noGon : ¬ HasConvexNGon (2 * j) S) : S.card ≤ 2 * M + 2 := by
  classical
  have hR : (Rset S).card ≤ M := by
    set T := Rset S with hTdef
    have hTS : T ⊆ S := Finset.filter_subset _ _
    have hT0 : ∀ p ∈ T, 0 < p 1 := fun p hp => (Finset.mem_filter.mp hp).2
    have hx := injOn_x S gp sym hTS (fun p hp => le_of_lt (hT0 p hp))
      (fun p hp q _ hp0 _ => absurd hp0 (ne_of_gt (hT0 p hp)))
    have hgpT : GeneralPosition T := fun a ha b hb c hc => gp a (hTS ha) b (hTS hb) c (hTS hc)
    apply hM T.card (cfg T hx hgpT)
    · rintro ⟨f, hf, hneg⟩
      let c : Fin j → Point := fun i => sortPt T hx (f i)
      have mem : ∀ i, c i ∈ T := fun i => sortPt_mem T hx (f i)
      have xo : StrictMono (fun i => c i 0) := fun i i' h => sortPt_strictMono T hx (hf h)
      have inS : ∀ i, c i ∈ S := fun i => hTS (mem i)
      have minS : ∀ i, mir (c i) ∈ S := fun i => sym _ (inS i)
      exact noGon (cap_mirror_polygon (m := j) hj c xo (fun i => hT0 _ (mem i))
        (fun i i' i'' h h' => hneg i i' i'' h h') inS minS)
    · intro h
      apply noGon
      have himg : Finset.univ.image (cfg T hx hgpT).point = T := sortPt_image T hx
      rw [himg] at h
      exact h.mono hTS
  have hsplit := card_split S sym
  have hA := card_A_le S gp
  omega

/-- Consistency check: the general odd reduction with Baek at n = 7 gives the k = 7 bound again. -/
theorem mirror_seven' (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noHept : ¬ HasConvexNGon 7 S) : S.card ≤ 32 :=
  mirror_odd_general 3 16 (by norm_num) (fun n c h1 h2 => capacity16 c h1 h2) S gp sym noHept

/-- Consistency check: the general even reduction with Baek at n = 8 gives the k = 8 bound again. -/
theorem mirror_eight' (S : Finset Point) (gp : GeneralPosition S) (sym : ∀ p ∈ S, mir p ∈ S)
    (noOct : ¬ HasConvexNGon 8 S) : S.card ≤ 46 :=
  mirror_even_general 4 22 (by norm_num) (fun n c h1 h2 => capacity22g c h1 h2) S gp sym noOct

/-- Theorem 2(a) for an arbitrary mirror line. -/
theorem mirror_odd_general_line (j M : ℕ) (hj : 2 ≤ j)
    (hM : ∀ (n : ℕ) (c : Configuration n), ¬ c.HasCap (j + 1) →
      ¬ HasConvexNGon (2 * j + 1) (Finset.univ.image c.point) → n ≤ M)
    {n0 n1 c : ℝ} (hn : n0 ^ 2 + n1 ^ 2 = 1) (S : Finset Point) (gp : GeneralPosition S)
    (sym : ∀ p ∈ S, lineRefl n0 n1 c p ∈ S) (noGon : ¬ HasConvexNGon (2 * j + 1) S) : S.card ≤ 2 * M := by
  obtain ⟨gp', sym', no', card'⟩ := transport hn gp sym noGon
  rw [← card']; exact mirror_odd_general j M hj hM _ gp' sym' no'

/-- Theorem 2(b) for an arbitrary mirror line. -/
theorem mirror_even_general_line (j M : ℕ) (hj : 2 ≤ j)
    (hM : ∀ (n : ℕ) (c : Configuration n), ¬ c.HasCap j →
      ¬ HasConvexNGon (2 * j) (Finset.univ.image c.point) → n ≤ M)
    {n0 n1 c : ℝ} (hn : n0 ^ 2 + n1 ^ 2 = 1) (S : Finset Point) (gp : GeneralPosition S)
    (sym : ∀ p ∈ S, lineRefl n0 n1 c p ∈ S) (noGon : ¬ HasConvexNGon (2 * j) S) : S.card ≤ 2 * M + 2 := by
  obtain ⟨gp', sym', no', card'⟩ := transport hn gp sym noGon
  rw [← card']; exact mirror_even_general j M hj hM _ gp' sym' no'

end GeneralK

end MirrorOdd

#print axioms MirrorOdd.mirror_seven
#print axioms MirrorOdd.mirror_eight
#print axioms MirrorOdd.mirror_seven_line
#print axioms MirrorOdd.mirror_eight_line
#print axioms MirrorOdd.mirror_four
#print axioms MirrorOdd.mirror_five
#print axioms MirrorOdd.mirror_six
#print axioms MirrorOdd.mirror_four_line
#print axioms MirrorOdd.mirror_five_line
#print axioms MirrorOdd.mirror_six_line
#print axioms MirrorOdd.mirror_odd_general
#print axioms MirrorOdd.mirror_even_general
#print axioms MirrorOdd.mirror_seven'
#print axioms MirrorOdd.mirror_eight'
#print axioms MirrorOdd.mirror_odd_general_line
#print axioms MirrorOdd.mirror_even_general_line

/-! # Part C: integration -/

/-! ## 11. Integration: the two mirror classes from `MirrorOdd.mirror_seven_line`

`reflLine a u` (the line through `a` with direction `u`, `u 0 ^ 2 + u 1 ^ 2 = 1`) and
`MirrorOdd.lineRefl n0 n1 c` (the line `n0 x + n1 y = c`, unit normal `(n0, n1)`) are the same
map for `(n0, n1) = (-u 1, u 0)` (`u` turned by 90°) and `c = n0 * a 0 + n1 * a 1`
(`reflLine_eq_lineRefl`).  Hence a finite `reflLine`-invariant set in general position with no
convex heptagon has at most 32 points (`card_le_32_of_reflLine`); this refutes counterexamples
to both mirror classes (33 and 34 points), whatever the number of points on the mirror. -/

namespace ErdosSzekeres.SymReduction

/-- The reflection `reflLine a u` (`|u| = 1`) is `MirrorOdd.lineRefl` for the unit normal
`(-u 1, u 0)` and the offset `-u 1 * a 0 + u 0 * a 1`. -/
theorem reflLine_eq_lineRefl {a u : Point} (hu : u 0 ^ 2 + u 1 ^ 2 = 1) :
    reflLine a u = MirrorOdd.lineRefl (-u 1) (u 0) (-u 1 * a 0 + u 0 * a 1) := by
  funext p
  apply point_ext
  · simp only [reflLine, MirrorOdd.lineRefl, Matrix.cons_val_zero]
    linear_combination (2 * (p 0 - a 0)) * hu
  · simp only [reflLine, MirrorOdd.lineRefl, Matrix.cons_val_zero, Matrix.cons_val_one]
    linear_combination (2 * (p 1 - a 1)) * hu

/-- A finite set in general position that is invariant under `reflLine a u` (`|u| = 1`) and has
no convex heptagon has at most 32 points (`MirrorOdd.mirror_seven_line`). -/
theorem card_le_32_of_reflLine {S : Finset Point} {a u : Point} (hu : u 0 ^ 2 + u 1 ^ 2 = 1)
    (hgp : GeneralPosition S) (hinv : Invariant (reflLine a u) S) (hno : ¬ HasConvexNGon 7 S) :
    S.card ≤ 32 := by
  have hn : (-u 1) ^ 2 + u 0 ^ 2 = 1 := by linear_combination hu
  refine MirrorOdd.mirror_seven_line (c := -u 1 * a 0 + u 0 * a 1) hn S hgp ?_ hno
  intro p hp
  rw [← reflLine_eq_lineRefl hu]
  exact hinv p hp

/-- The class `MirrorOneAxis33` holds (the hypothesis on the axis point is not needed). -/
theorem mirrorOneAxis33_proved : MirrorOneAxis33 :=
  fun _S _a _u hu hgp hcard hinv _ => by
    by_contra hno
    have h32 := card_le_32_of_reflLine hu hgp hinv hno
    omega

/-- The class `MirrorNoAxis34` holds (the hypothesis that no point is on the axis is not
needed). -/
theorem mirrorNoAxis34_proved : MirrorNoAxis34 :=
  fun _S _a _u hu hgp hcard hinv _ => by
    by_contra hno
    have h32 := card_le_32_of_reflLine hu hgp hinv hno
    omega

/-- **Corollary 3 (reduction), three classes.** Assume `HalfTurn34`, `Threefold33` and
`Fivefold35`. Then every finite set `S` of at least 33 points in general position that is mapped
into itself by a Euclidean isometry other than the identity contains 7 points in convex
position. -/
theorem heptagon_of_nontrivial_isometry_3
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (S : Finset Point) (g : Point → Point) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hg : IsEucIsometry g) (hne : g ≠ id) (hinv : Invariant g S) : HasConvexNGon 7 S :=
  heptagon_of_nontrivial_isometry h2 h3 h5 mirrorOneAxis33_proved mirrorNoAxis34_proved
    S g hgp hcard hg hne hinv

/-- **Corollary 3, affine version, three classes.** Assume `HalfTurn34`, `Threefold33` and
`Fivefold35`. Every finite set `S` of at least 33 points in general position that is mapped into
itself by an affine bijection of the plane other than the identity contains 7 points in convex
position. -/
theorem heptagon_of_nontrivial_affineEquiv_3
    (h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
    (S : Finset Point) (g : Point ≃ᵃ[ℝ] Point) (hgp : GeneralPosition S) (hcard : 33 ≤ S.card)
    (hne : g ≠ AffineEquiv.refl ℝ Point) (hinv : Invariant g S) : HasConvexNGon 7 S :=
  heptagon_of_nontrivial_affineEquiv h2 h3 h5 mirrorOneAxis33_proved mirrorNoAxis34_proved
    S g hgp hcard hne hinv

end ErdosSzekeres.SymReduction

#check @ErdosSzekeres.SymReduction.reflLine_eq_lineRefl
#check @ErdosSzekeres.SymReduction.mirrorOneAxis33_proved
#check @ErdosSzekeres.SymReduction.mirrorNoAxis34_proved
#check @ErdosSzekeres.SymReduction.heptagon_of_nontrivial_isometry_3
#check @ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affineEquiv_3
#print axioms ErdosSzekeres.SymReduction.reflLine_eq_lineRefl
#print axioms ErdosSzekeres.SymReduction.card_le_32_of_reflLine
#print axioms ErdosSzekeres.SymReduction.mirrorOneAxis33_proved
#print axioms ErdosSzekeres.SymReduction.mirrorNoAxis34_proved
#print axioms ErdosSzekeres.SymReduction.heptagon_of_nontrivial_isometry_3
#print axioms ErdosSzekeres.SymReduction.heptagon_of_nontrivial_affineEquiv_3
