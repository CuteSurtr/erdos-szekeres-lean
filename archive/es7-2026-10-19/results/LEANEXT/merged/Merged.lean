import ErdosSzekeres.Definitions
import ErdosSzekeres.OrientationGeometry
import ErdosSzekeres.Suk.OrientationClique
import Mathlib.Analysis.Convex.Independent
import Mathlib.Analysis.Convex.KreinMilman
import Mathlib.Analysis.Convex.Topology
import Mathlib.Analysis.SpecialFunctions.Complex.Circle
import Mathlib.RingTheory.RootsOfUnity.Complex
import Mathlib.Dynamics.PeriodicPts.Defs

/-!
# The layer lemma for rotationally symmetric point sets

Let `S` be a finite set of points that is mapped into itself by the rotation `ρ` by `2π/m` about a
point `c ∉ S`, and suppose `S` has no `K` points in convex position for some `K ≤ 2m`.  Then the
vertex set of the convex hull of `S` is a single `ρ`-orbit, i.e. a regular `m`-gon about `c`
(`hullVerts_eq_orbitFS_rotAbout`).  Removing it leaves a set with the same properties, so every
convex layer of `S` is one orbit, and each layer lies in the convex hull of the layer before it
(`layers_are_orbits`); the layers exhaust `S` (`exists_layer`).  If `S` is moreover in general
position and `m ≥ 2`, every point of a later layer lies strictly to the left of every edge
`x → ρ x` of an earlier layer (`strict_nesting`), which is the form of the nesting clauses of the
layered encoders.

This is the layer lemma of `SYM5/README.md` §2 (all four steps).

The vertices of the hull of a finite set are its points that are not in the convex hull of the
other points (`hullVerts`); `extreme_mem_hullVerts` and `subset_convexHull_hullVerts` relate this to
`Set.extremePoints` (Krein–Milman).

Definitions `orbitFS`, `Invariant`, `toC`, `ofC`, `crot`, `rotAbout` and their basic lemmas are
copied verbatim from `SYMLEAN/SymmetricReduction.lean` (a file that is not an importable module).

Checked with Lean 4.24.0 and Mathlib `f897ebcf` (the repository's pins), from the repository root:
`lake env lean <this file>`.
-/

namespace ErdosSzekeres.LayerLemma

open Function Complex

/-! ## 1. Orbits of a map with a fixed period (from `SYMLEAN`) -/

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

/-- Two orbits of points of period `p` are equal or disjoint: a point of `orbitFS f p x` that lies
in the orbit of `y` forces `y` into the orbit of `x`. -/
theorem mem_orbitFS_of_not_disjoint {f : α → α} {p : ℕ} (hp : 0 < p) {x y : α}
    (hx : f^[p] x = x) (hy : f^[p] y = y)
    (h : ¬ Disjoint (orbitFS f p x) (orbitFS f p y)) : y ∈ orbitFS f p x := by
  obtain ⟨z, hzx, hzy⟩ := Finset.not_disjoint_iff.1 h
  obtain ⟨j, hj, rfl⟩ := Finset.mem_image.1 hzy
  rw [Finset.mem_range] at hj
  have hback : f^[p - j] (f^[j] y) = y := by
    rw [← iterate_add_apply, Nat.sub_add_cancel hj.le, hy]
  rw [← hback]
  exact iterate_mem (orbitFS_invariant hp hx) hzx (p - j)

end Orbits

/-- `f` maps `S` into itself. -/
def Invariant (f : Point → Point) (S : Finset Point) : Prop := ∀ p ∈ S, f p ∈ S

/-! ## 2. Vertices of the convex hull of a finite set -/

open scoped Classical in
/-- The vertices of `conv S`: the points of `S` that are not in the convex hull of the others. -/
noncomputable def hullVerts (S : Finset Point) : Finset Point :=
  S.filter (fun x => x ∉ convexHull ℝ ((S : Set Point) \ {x}))

theorem mem_hullVerts {S : Finset Point} {x : Point} :
    x ∈ hullVerts S ↔ x ∈ S ∧ x ∉ convexHull ℝ ((S : Set Point) \ {x}) := by
  simp only [hullVerts, Finset.mem_filter]

theorem hullVerts_subset (S : Finset Point) : hullVerts S ⊆ S := fun _ hx => (mem_hullVerts.1 hx).1

/-- The hull vertices are in convex position. -/
theorem convexPosition_hullVerts (S : Finset Point) : ConvexPosition (hullVerts S) := by
  unfold ConvexPosition
  rw [convexIndependent_set_iff_notMem_convexHull_diff]
  intro x hx hmem
  have hx' := mem_hullVerts.1 hx
  refine hx'.2 (convexHull_mono ?_ hmem)
  exact Set.diff_subset_diff_left (by exact_mod_cast hullVerts_subset S)

/-- Every extreme point of `conv S` is a hull vertex. -/
theorem extreme_mem_hullVerts {S : Finset Point} {x : Point}
    (hx : x ∈ (convexHull ℝ (S : Set Point)).extremePoints ℝ) : x ∈ hullVerts S := by
  have hxS : x ∈ (S : Set Point) := extremePoints_convexHull_subset hx
  rw [(convex_convexHull ℝ _).mem_extremePoints_iff_convex_diff] at hx
  refine mem_hullVerts.2 ⟨hxS, fun hmem => ?_⟩
  have hsub : convexHull ℝ ((S : Set Point) \ {x}) ⊆ convexHull ℝ (S : Set Point) \ {x} :=
    convexHull_min (Set.diff_subset_diff_left (subset_convexHull ℝ _)) hx.2
  exact (hsub hmem).2 rfl

theorem hullVerts_nonempty {S : Finset Point} (hS : S.Nonempty) : (hullVerts S).Nonempty := by
  have hcomp : IsCompact (convexHull ℝ (S : Set Point)) := S.finite_toSet.isCompact_convexHull
  have hne : (convexHull ℝ (S : Set Point)).Nonempty := convexHull_nonempty_iff.2 hS
  obtain ⟨e, he⟩ := hcomp.extremePoints_nonempty hne
  exact ⟨e, extreme_mem_hullVerts he⟩

/-- Every point of `S` lies in the convex hull of the hull vertices (Krein–Milman). -/
theorem subset_convexHull_hullVerts (S : Finset Point) :
    (S : Set Point) ⊆ convexHull ℝ (hullVerts S : Set Point) := by
  have hcomp : IsCompact (convexHull ℝ (S : Set Point)) := S.finite_toSet.isCompact_convexHull
  have hKM := closure_convexHull_extremePoints hcomp (convex_convexHull ℝ (S : Set Point))
  have hclosed : IsClosed (convexHull ℝ (hullVerts S : Set Point)) :=
    (hullVerts S).finite_toSet.isCompact_convexHull.isClosed
  have hext : (convexHull ℝ (S : Set Point)).extremePoints ℝ ⊆ (hullVerts S : Set Point) :=
    fun _ he => extreme_mem_hullVerts he
  calc (S : Set Point) ⊆ convexHull ℝ (S : Set Point) := subset_convexHull ℝ _
    _ = closure (convexHull ℝ ((convexHull ℝ (S : Set Point)).extremePoints ℝ)) := hKM.symm
    _ ⊆ closure (convexHull ℝ (hullVerts S : Set Point)) := closure_mono (convexHull_mono hext)
    _ = convexHull ℝ (hullVerts S : Set Point) := hclosed.closure_eq

/-! ## 3. Invariance under an injective affine map -/

/-- An injective affine map that sends `S` into itself sends hull vertices to hull vertices. -/
theorem map_mem_hullVerts {f : Point →ᵃ[ℝ] Point} (hf : Injective f) {S : Finset Point}
    (hinv : ∀ y ∈ S, f y ∈ S) {x : Point} (hx : x ∈ hullVerts S) : f x ∈ hullVerts S := by
  have hx' := mem_hullVerts.1 hx
  have himg : S.image f = S :=
    Finset.eq_of_subset_of_card_le (fun y hy => by
      obtain ⟨z, hz, rfl⟩ := Finset.mem_image.1 hy
      exact hinv z hz) (by rw [Finset.card_image_of_injective _ hf])
  refine mem_hullVerts.2 ⟨hinv x hx'.1, fun hmem => hx'.2 ?_⟩
  have hsub : (S : Set Point) \ {f x} ⊆ f '' ((S : Set Point) \ {x}) := by
    rintro y ⟨hyS, hyx⟩
    have hyS' : y ∈ S.image f := by rw [himg]; exact hyS
    obtain ⟨z, hz, rfl⟩ := Finset.mem_image.1 hyS'
    refine ⟨z, ⟨hz, fun hzx => hyx ?_⟩, rfl⟩
    rw [Set.mem_singleton_iff.1 hzx]
    rfl
  have h2 : f x ∈ f '' convexHull ℝ ((S : Set Point) \ {x}) := by
    rw [AffineMap.image_convexHull]
    exact convexHull_mono hsub hmem
  obtain ⟨y, hy, hyx⟩ := h2
  rw [hf hyx] at hy
  exact hy

/-! ## 4. The core lemma -/

/-- **Layer lemma, abstract form.** Let `f` be an injective affine map sending the finite set `S`
into itself, with every point of `S` of minimal period `m > 0`.  If `S` has no `K` points in convex
position for some `K ≤ 2m`, then the hull vertices of `S` form exactly one `f`-orbit. -/
theorem hullVerts_eq_orbitFS {f : Point →ᵃ[ℝ] Point} (hf : Injective f) {S : Finset Point}
    {m K : ℕ} (hm : 0 < m) (hK : K ≤ 2 * m) (hinv : ∀ y ∈ S, f y ∈ S)
    (hper : ∀ y ∈ S, minimalPeriod f y = m) (hno : ¬ HasConvexNGon K S)
    {x : Point} (hx : x ∈ hullVerts S) : hullVerts S = orbitFS f m x := by
  have hH : ∀ y ∈ hullVerts S, f y ∈ hullVerts S := fun y hy => map_mem_hullVerts hf hinv hy
  have hfix : ∀ y ∈ S, f^[m] y = y := fun y hy => by
    rw [← hper y hy]
    exact iterate_minimalPeriod
  have hxS := hullVerts_subset S hx
  refine (Finset.Subset.antisymm ?_ (orbitFS_subset hH hx))
  intro y hy
  by_contra hyx
  have hyS := hullVerts_subset S hy
  have hdisj : Disjoint (orbitFS f m x) (orbitFS f m y) := by
    by_contra h
    exact hyx (mem_orbitFS_of_not_disjoint hm (hfix x hxS) (hfix y hyS) h)
  have hunion : orbitFS f m x ∪ orbitFS f m y ⊆ hullVerts S :=
    Finset.union_subset (orbitFS_subset hH hx) (orbitFS_subset hH hy)
  have hcard : 2 * m ≤ (hullVerts S).card := by
    have := Finset.card_le_card hunion
    rw [Finset.card_union_of_disjoint hdisj, card_orbitFS_of_minimalPeriod (hper x hxS),
      card_orbitFS_of_minimalPeriod (hper y hyS)] at this
    omega
  obtain ⟨t, ht, htK⟩ := Finset.exists_subset_card_eq (hK.trans hcard)
  refine hno ⟨t, ht.trans (hullVerts_subset S), htK, ?_⟩
  exact (convexPosition_hullVerts S).mono (by exact_mod_cast ht)

/-- Removing the hull vertices keeps the set invariant. -/
theorem invariant_sdiff_hullVerts {f : Point →ᵃ[ℝ] Point} (hf : Injective f) {S : Finset Point}
    {m : ℕ} (hm : 0 < m) (hinv : ∀ y ∈ S, f y ∈ S) (hfix : ∀ y ∈ S, f^[m] y = y) :
    ∀ y ∈ S \ hullVerts S, f y ∈ S \ hullVerts S := by
  intro y hy
  obtain ⟨hyS, hyH⟩ := Finset.mem_sdiff.1 hy
  refine Finset.mem_sdiff.2 ⟨hinv y hyS, fun hfy => hyH ?_⟩
  have hback : f^[m - 1] (f y) = y := by
    rw [← iterate_succ_apply, Nat.succ_eq_add_one, Nat.sub_add_cancel hm, hfix y hyS]
  rw [← hback]
  exact iterate_mem (fun z hz => map_mem_hullVerts hf hinv hz) hfy (m - 1)

/-! ## 5. Rotations (definitions and basic lemmas from `SYMLEAN`) -/

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

/-- `rotAbout c θ` as an affine map (its linear part is the rotation matrix). -/
noncomputable def rotAff (c : Point) (θ : ℝ) : Point →ᵃ[ℝ] Point where
  toFun := rotAbout c θ
  linear := Matrix.toLin' !![Real.cos θ, -Real.sin θ; Real.sin θ, Real.cos θ]
  map_vadd' p v := by
    funext i
    fin_cases i <;>
      simp [rotAbout, Matrix.toLin'_apply, dotProduct, Fin.sum_univ_two] <;> ring

theorem rotAbout_injective (c : Point) (θ : ℝ) : Injective (rotAbout c θ) := by
  rw [rotAbout_eq_crot]
  exact crot_injective (Complex.exp_ne_zero _)

/-- Removing the centre keeps a rotation-invariant set invariant, so the layer lemma applies to
`S.erase c` when the centre belongs to `S`. -/
theorem invariant_erase_centre {S : Finset Point} {c : Point} {θ : ℝ}
    (hinv : Invariant (rotAbout c θ) S) : Invariant (rotAbout c θ) (S.erase c) := by
  intro p hp
  obtain ⟨hpc, hpS⟩ := Finset.mem_erase.1 hp
  refine Finset.mem_erase.2 ⟨fun h => hpc ?_, hinv p hpS⟩
  have hcc : rotAbout c θ c = c := by
    funext i
    fin_cases i <;> simp [rotAbout]
  exact rotAbout_injective c θ (h.trans hcc.symm)

/-- Every point other than the centre has minimal period `m` under the rotation by `2π/m`. -/
theorem minimalPeriod_rotAbout {c : Point} {m : ℕ} (hm : 0 < m) {y : Point} (hy : y ≠ c) :
    minimalPeriod (rotAbout c (2 * Real.pi / m)) y = m := by
  set w : ℂ := Complex.exp (((2 * Real.pi / m : ℝ) : ℂ) * Complex.I) with hwdef
  have hw : w = Complex.exp (2 * Real.pi * Complex.I / m) := by
    rw [hwdef]
    congr 1
    push_cast
    ring
  have hprim : IsPrimitiveRoot w m := by
    rw [hw]
    exact Complex.isPrimitiveRoot_exp m hm.ne'
  have hyc : toC y ≠ toC c := fun h => hy (toC_injective h)
  rw [rotAbout_eq_crot]
  have hpm : IsPeriodicPt (crot (toC c) w) m y := by
    show (crot (toC c) w)^[m] y = y
    rw [crot_iterate, hprim.pow_eq_one, crot_one]
    rfl
  have hle := hpm.minimalPeriod_le hm
  have hpos := hpm.minimalPeriod_pos hm
  by_contra hne
  have hlt : minimalPeriod (crot (toC c) w) y < m := lt_of_le_of_ne hle hne
  have hfix : (crot (toC c) w)^[minimalPeriod (crot (toC c) w) y] y = y := iterate_minimalPeriod
  rw [crot_iterate] at hfix
  exact hyc ((crot_eq_self_iff (hprim.pow_ne_one_of_pos_of_lt hpos.ne' hlt) y).1 hfix)

/-- **Layer lemma, hull form.** If `S` is mapped into itself by the rotation by `2π/m` about
`c ∉ S` (`m > 0`) and has no `K` points in convex position for some `K ≤ 2m`, then the vertices of
`conv S` form exactly one orbit of the rotation. -/
theorem hullVerts_eq_orbitFS_rotAbout {S : Finset Point} {c : Point} {m K : ℕ} (hm : 0 < m)
    (hK : K ≤ 2 * m) (hc : c ∉ S) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S)
    (hno : ¬ HasConvexNGon K S) {x : Point} (hx : x ∈ hullVerts S) :
    hullVerts S = orbitFS (rotAbout c (2 * Real.pi / m)) m x :=
  hullVerts_eq_orbitFS (f := rotAff c (2 * Real.pi / m)) (rotAbout_injective c _) hm hK hinv
    (fun _ hy => minimalPeriod_rotAbout hm (fun h => hc (h ▸ hy))) hno hx

/-! ## 6. Peeling the layers -/

/-- `peel S n` is what remains of `S` after removing the `n` outermost convex layers. -/
noncomputable def peel (S : Finset Point) : ℕ → Finset Point
  | 0 => S
  | n + 1 => peel S n \ hullVerts (peel S n)

theorem peel_succ (S : Finset Point) (n : ℕ) : peel S (n + 1) = peel S n \ hullVerts (peel S n) :=
  rfl

theorem peel_subset (S : Finset Point) : ∀ n, peel S n ⊆ S
  | 0 => Finset.Subset.refl S
  | n + 1 => (Finset.sdiff_subset).trans (peel_subset S n)

/-- The hypotheses of the layer lemma pass to every `peel S n`. -/
theorem invariant_peel {S : Finset Point} {c : Point} {m : ℕ} (hm : 0 < m) (hc : c ∉ S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) :
    ∀ n, Invariant (rotAbout c (2 * Real.pi / m)) (peel S n)
  | 0 => hinv
  | n + 1 => by
    have ih := invariant_peel hm hc hinv n
    have hfix : ∀ y ∈ peel S n, (rotAbout c (2 * Real.pi / m))^[m] y = y := fun y hy => by
      have hyc : y ≠ c := fun h => hc (h ▸ peel_subset S n hy)
      have h := iterate_minimalPeriod (f := rotAbout c (2 * Real.pi / m)) (x := y)
      rwa [minimalPeriod_rotAbout hm hyc] at h
    exact invariant_sdiff_hullVerts (f := rotAff c (2 * Real.pi / m)) (rotAbout_injective c _) hm
      ih hfix

/-- **Layer lemma.** Under the hypotheses of `hullVerts_eq_orbitFS_rotAbout`, every nonempty
`peel S n` has as its hull vertices one orbit of exactly `m` points, and the next layers lie in the
convex hull of that orbit. -/
theorem layers_are_orbits {S : Finset Point} {c : Point} {m K : ℕ} (hm : 0 < m) (hK : K ≤ 2 * m)
    (hc : c ∉ S) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S)
    (hno : ¬ HasConvexNGon K S) (n : ℕ) (hn : (peel S n).Nonempty) :
    ∃ x ∈ peel S n, hullVerts (peel S n) = orbitFS (rotAbout c (2 * Real.pi / m)) m x ∧
      (orbitFS (rotAbout c (2 * Real.pi / m)) m x).card = m ∧
      (peel S (n + 1) : Set Point) ⊆ convexHull ℝ (hullVerts (peel S n) : Set Point) := by
  obtain ⟨x, hx⟩ := hullVerts_nonempty hn
  have hxS : x ∈ peel S n := hullVerts_subset _ hx
  have hcn : c ∉ peel S n := fun h => hc (peel_subset S n h)
  have hnon : ¬ HasConvexNGon K (peel S n) := fun ⟨t, ht, htK, htc⟩ =>
    hno ⟨t, ht.trans (peel_subset S n), htK, htc⟩
  refine ⟨x, hxS, hullVerts_eq_orbitFS_rotAbout hm hK hcn (invariant_peel hm hc hinv n) hnon hx,
    card_orbitFS_of_minimalPeriod (minimalPeriod_rotAbout hm (fun h => hcn (h ▸ hxS))), ?_⟩
  rw [peel_succ]
  exact (Finset.coe_subset.2 Finset.sdiff_subset).trans (subset_convexHull_hullVerts _)

/-- The layers exhaust `S`: every point of `S` is a hull vertex of some `peel S n`. -/
theorem exists_layer (S : Finset Point) {y : Point} (hy : y ∈ S) :
    ∃ n, y ∈ hullVerts (peel S n) := by
  classical
  have hcard : ∀ n, (peel S n).card + n ≤ S.card ∨ peel S n = ∅ := by
    intro n
    induction n with
    | zero => left; simp [peel]
    | succ n ih =>
      rcases (peel S n).eq_empty_or_nonempty with h | h
      · right
        rw [peel_succ, h, Finset.empty_sdiff]
      · left
        have hlt : (peel S (n + 1)).card < (peel S n).card := by
          rw [peel_succ]
          exact Finset.card_lt_card (Finset.sdiff_ssubset (hullVerts_subset _) (hullVerts_nonempty h))
        rcases ih with ih | ih
        · omega
        · exact absurd ih h.ne_empty
  have hex : ∃ k, y ∉ peel S k := by
    refine ⟨S.card + 1, fun hmem => ?_⟩
    rcases hcard (S.card + 1) with h | h
    · have := Finset.card_pos.2 ⟨y, hmem⟩
      omega
    · rw [h] at hmem
      exact Finset.notMem_empty y hmem
  have hk := Nat.find_spec hex
  have hk0 : Nat.find hex ≠ 0 := by
    intro h0
    rw [h0] at hk
    exact hk hy
  obtain ⟨n, hn⟩ := Nat.exists_eq_succ_of_ne_zero hk0
  have hyn : y ∈ peel S n := by
    by_contra h
    exact absurd (Nat.find_min hex (by omega : n < Nat.find hex)) (not_not.2 h)
  refine ⟨n, ?_⟩
  rw [hn, peel_succ] at hk
  by_contra hH
  exact hk (Finset.mem_sdiff.2 ⟨hyn, hH⟩)

/-! ## 7. Strict nesting (step 4), in the orientation form of the encoders' nesting clauses -/

theorem peel_antitone (S : Finset Point) {n n' : ℕ} (h : n ≤ n') : peel S n' ⊆ peel S n := by
  induction h with
  | refl => exact Finset.Subset.refl _
  | step _ ih => exact (Finset.sdiff_subset).trans ih

theorem rotAbout_iterate (c : Point) (α : ℝ) (j : ℕ) :
    (rotAbout c α)^[j] = rotAbout c (j * α) := by
  rw [rotAbout_eq_crot, crot_iterate, rotAbout_eq_crot, ← Complex.exp_nat_mul]
  push_cast
  ring_nf

/-- The orientation of a regular-polygon triple, in coordinates. -/
theorem orient_rotAbout (c x : Point) (α β : ℝ) :
    orient x (rotAbout c α x) (rotAbout c β x) =
      ((x 0 - c 0) ^ 2 + (x 1 - c 1) ^ 2) *
        ((Real.cos α - 1) * Real.sin β - Real.sin α * (Real.cos β - 1)) := by
  simp only [orient, rotAbout, Matrix.cons_val_zero, Matrix.cons_val_one]
  ring

/-- `(cos 2t - 1) sin 2s - sin 2t (cos 2s - 1) = 4 sin t sin s sin (s - t)`. -/
theorem trig_layer (s t : ℝ) :
    (Real.cos (2 * t) - 1) * Real.sin (2 * s) - Real.sin (2 * t) * (Real.cos (2 * s) - 1) =
      4 * Real.sin t * Real.sin s * Real.sin (s - t) := by
  rw [Real.cos_two_mul, Real.cos_two_mul, Real.sin_two_mul, Real.sin_two_mul, Real.sin_sub]
  linear_combination (4 * Real.sin s * Real.cos s) * Real.sin_sq_add_cos_sq t -
    (4 * Real.sin t * Real.cos t) * Real.sin_sq_add_cos_sq s

/-- Every vertex of a regular `m`-gon lies weakly to the left of each of its edges. -/
theorem orient_regular_nonneg {c x : Point} {m : ℕ} (hm : 0 < m) {j : ℕ} (hj : j ≤ m) :
    0 ≤ orient x (rotAbout c (2 * Real.pi / m) x) ((rotAbout c (2 * Real.pi / m))^[j] x) := by
  rw [rotAbout_iterate, orient_rotAbout]
  refine mul_nonneg (by positivity) ?_
  rcases Nat.eq_zero_or_pos j with rfl | hj0
  · simp
  set t : ℝ := Real.pi / m with htdef
  have hmpos : (0 : ℝ) < m := by exact_mod_cast hm
  have h2t : 2 * Real.pi / m = 2 * t := by rw [htdef]; ring
  have h2s : (j : ℝ) * (2 * Real.pi / m) = 2 * (j * t) := by rw [htdef]; ring
  rw [h2s, h2t, trig_layer]
  have hjm : (j : ℝ) ≤ m := by exact_mod_cast hj
  have hj1 : (1 : ℝ) ≤ j := by exact_mod_cast hj0
  have ht0 : 0 ≤ t := by positivity
  have htpi : t ≤ Real.pi := by
    rw [htdef, div_le_iff₀ hmpos]
    nlinarith [Real.pi_pos, (show (1 : ℝ) ≤ m by exact_mod_cast hm)]
  have hjt : j * t ≤ Real.pi := by
    rw [htdef, mul_div_assoc', div_le_iff₀ hmpos]
    nlinarith [Real.pi_pos]
  have h1 : 0 ≤ Real.sin t := Real.sin_nonneg_of_nonneg_of_le_pi ht0 htpi
  have h2 : 0 ≤ Real.sin (j * t) :=
    Real.sin_nonneg_of_nonneg_of_le_pi (by positivity) hjt
  have h3 : 0 ≤ Real.sin (j * t - t) :=
    Real.sin_nonneg_of_nonneg_of_le_pi (by nlinarith) (by nlinarith)
  positivity

/-- A closed half-plane `{q | 0 ≤ orient a b q}` is convex. -/
theorem convex_orient_nonneg (a b : Point) : Convex ℝ {q : Point | 0 ≤ orient a b q} := by
  intro q₁ hq₁ q₂ hq₂ u v hu hv huv
  simp only [Set.mem_setOf_eq] at hq₁ hq₂ ⊢
  have h : orient a b (u • q₁ + v • q₂) = u * orient a b q₁ + v * orient a b q₂ := by
    simp only [orient, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    linear_combination ((b 0 - a 0) * a 1 - (b 1 - a 1) * a 0) * huv
  rw [h]
  positivity

/-- **Strict nesting.** Under the hypotheses of the layer lemma and general position, every point
of a later layer lies strictly to the left of the edge `x → ρ x` of an earlier layer, for every
vertex `x` of that layer: `orient x (ρ x) y > 0`.  This is the form of the nesting clauses of the
layered encoders. -/
theorem strict_nesting {S : Finset Point} {c : Point} {m K : ℕ} (hm : 2 ≤ m) (hK : K ≤ 2 * m)
    (hc : c ∉ S) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hno : ¬ HasConvexNGon K S)
    (hgp : GeneralPosition S) {n n' : ℕ} (hnn' : n < n') {x : Point}
    (hx : x ∈ hullVerts (peel S n)) {y : Point} (hy : y ∈ peel S n') :
    0 < orient x (rotAbout c (2 * Real.pi / m) x) y := by
  set ρ := rotAbout c (2 * Real.pi / m) with hρ
  have hm0 : 0 < m := by omega
  have hxn : x ∈ peel S n := hullVerts_subset _ hx
  have hcn : c ∉ peel S n := fun h => hc (peel_subset S n h)
  have hnon : ¬ HasConvexNGon K (peel S n) := fun ⟨t, ht, htK⟩ =>
    hno ⟨t, ht.trans (peel_subset S n), htK⟩
  have hL := hullVerts_eq_orbitFS_rotAbout hm0 hK hcn (invariant_peel hm0 hc hinv n) hnon hx
  -- `y` is in a strictly later peel, so it lies in the hull of the layer and is not a vertex
  have hy1 : y ∈ peel S (n + 1) := peel_antitone S (by omega) hy
  have hyconv : y ∈ convexHull ℝ (hullVerts (peel S n) : Set Point) := by
    have := subset_convexHull_hullVerts (peel S n)
    exact this (Finset.mem_coe.2 ((Finset.sdiff_subset) (by rw [← peel_succ]; exact hy1)))
  have hyL : y ∉ hullVerts (peel S n) := by
    rw [peel_succ] at hy1
    exact (Finset.mem_sdiff.1 hy1).2
  -- weakly left: the half-plane contains the layer, hence its hull
  have hweak : 0 ≤ orient x (ρ x) y := by
    have hsub : (hullVerts (peel S n) : Set Point) ⊆ {q : Point | 0 ≤ orient x (ρ x) q} := by
      intro q hq
      rw [Finset.mem_coe, hL] at hq
      obtain ⟨j, hj, rfl⟩ := Finset.mem_image.1 hq
      exact orient_regular_nonneg hm0 (Finset.mem_range.1 hj).le
    exact convexHull_min hsub (convex_orient_nonneg x (ρ x)) hyconv
  -- strictly: equality would make `x, ρ x, y` collinear
  have hρx : ρ x ∈ hullVerts (peel S n) := by
    rw [hL]
    exact Finset.mem_image.2 ⟨1, Finset.mem_range.2 (by omega), rfl⟩
  have hxS : x ∈ S := peel_subset S n hxn
  have hρxS : ρ x ∈ S := peel_subset S n (hullVerts_subset _ hρx)
  have hyS : y ∈ S := peel_subset S n' hy
  have hxc : x ≠ c := fun h' => hc (h' ▸ hxS)
  have hxρx : x ≠ ρ x := by
    intro h
    have hper := minimalPeriod_rotAbout hm0 hxc
    rw [← hρ] at hper
    have : Function.IsFixedPt ρ x := h.symm
    rw [Function.minimalPeriod_eq_one_iff_isFixedPt.2 this] at hper
    omega
  have hne : orient x (ρ x) y ≠ 0 :=
    (generalPosition_iff_orient_ne_zero S).1 hgp x hxS (ρ x) hρxS y hyS hxρx
      (fun h => hyL (h ▸ hx)) (fun h => hyL (h ▸ hρx))
  exact lt_of_le_of_ne hweak (Ne.symm hne)

/-! ## 8. The centre for even orders -/

/-- **Even orders exclude the centre.** If `m` is even, `S` is invariant under the rotation by
`2π/m` about `c`, in general position, and has a point other than `c`, then `c ∉ S`: the rotation by
`π` (a power of the given rotation) maps `p` to `2c - p`, and `p, c, 2c - p` are collinear. -/
theorem centre_not_mem_of_even {S : Finset Point} {c : Point} {m : ℕ} (hm : 0 < m) (heven : Even m)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    {p : Point} (hp : p ∈ S) (hpc : p ≠ c) : c ∉ S := by
  intro hc
  set q := (rotAbout c (2 * Real.pi / m))^[m / 2] p with hqdef
  have hq : q ∈ S := iterate_mem hinv hp (m / 2)
  have hhalf : ((m / 2 : ℕ) : ℝ) * (2 * Real.pi / m) = Real.pi := by
    obtain ⟨k, hk⟩ := heven
    have hk' : m / 2 = k := by omega
    have hkpos : (0 : ℝ) < k := by exact_mod_cast (show 0 < k by omega)
    rw [hk', hk]
    push_cast
    field_simp
    ring
  have hqval : q = ![2 * c 0 - p 0, 2 * c 1 - p 1] := by
    rw [hqdef, rotAbout_iterate, hhalf]
    funext i
    fin_cases i <;> simp [rotAbout] <;> ring
  have h0 : orient p c q = 0 := by
    rw [hqval]
    simp only [orient, Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  have hqc : q ≠ c := by
    intro h
    apply hpc
    funext i
    have := congrFun (hqval.symm.trans h) i
    fin_cases i <;> simp at this ⊢ <;> linarith
  have hpq : p ≠ q := by
    intro h
    apply hpc
    funext i
    have := congrFun (h.trans hqval) i
    fin_cases i <;> simp at this ⊢ <;> linarith
  exact (generalPosition_iff_orient_ne_zero S).1 hgp p hp c hc q hq hpc hpq (Ne.symm hqc) h0

/-! ## 9. Fan chains are convex polygons (the chain family of the layered encoders)

The encoders forbid `K - 1` points `q 0, …, q (K-2)` around a pivot `p` with `orient p (q s) (q (s+1)) > 0`
and `orient (q s) (q (s+1)) (q (s+2)) > 0`.  Such a chain inside an open half-plane through `p` is,
with `p`, a convex polygon (`hasConvexNGon_of_fan`). -/

/-- The linear functional `y ↦ w · (y - a)`. -/
def lin (w a y : Point) : ℝ := w 0 * (y 0 - a 0) + w 1 * (y 1 - a 1)

/-- **Half-plane transitivity.** Inside an open half-plane bounded by a line through `a`, the
angular order around `a` is transitive. -/
theorem orient_trans_halfplane {a b c e w : Point} (hb : 0 < lin w a b) (hc : 0 < lin w a c)
    (he : 0 < lin w a e) (h1 : 0 < orient a b c) (h2 : 0 < orient a c e) :
    0 < orient a b e := by
  have key : orient a b e * lin w a c = orient a b c * lin w a e + orient a c e * lin w a b := by
    simp only [orient, lin]
    ring
  have hpos : 0 < orient a b e * lin w a c := by
    rw [key]
    positivity
  exact pos_of_mul_pos_left hpos hc.le

/-- **One step along the fan.** -/
theorem fan_step {p a b c e : Point} (h1 : 0 < orient b c e) (h2 : 0 < orient p c e)
    (h3 : 0 < orient p b c) (h4 : 0 < orient a b c) (h5 : 0 < orient p a c) :
    0 < orient a c e := by
  have key : orient p b c * orient a c e = orient p c e * orient a b c + orient b c e * orient p a c := by
    simp only [orient]
    ring
  have hpos : 0 < orient p b c * orient a c e := by
    rw [key]
    positivity
  exact pos_of_mul_pos_right hpos h3.le

/-- `orient p (q i) y` as the linear functional of a half-plane bounded by the line through `q i`. -/
theorem orient_eq_lin (p x y : Point) : orient p x y = lin ![-(x 1 - p 1), x 0 - p 0] x y := by
  simp only [orient, lin, Matrix.cons_val_zero, Matrix.cons_val_one]
  ring

/-- **Fan chains have all triples positive.** -/
theorem fan_positive {p w : Point} {q : ℕ → Point} {n : ℕ}
    (hhalf : ∀ s < n, 0 < lin w p (q s))
    (hfan : ∀ s, s + 1 < n → 0 < orient p (q s) (q (s + 1)))
    (hturn : ∀ s, s + 2 < n → 0 < orient (q s) (q (s + 1)) (q (s + 2))) :
    (∀ j k, j < k → k < n → 0 < orient p (q j) (q k)) ∧
      (∀ i j k, i < j → j < k → k < n → 0 < orient (q i) (q j) (q k)) := by
  -- (a) angular order around the pivot, for all pairs
  have hP : ∀ j k, j < k → k < n → 0 < orient p (q j) (q k) := by
    intro j k hjk hkn
    induction k, hjk using Nat.le_induction with
    | base => exact hfan j hkn
    | succ k hk ih =>
      exact orient_trans_halfplane (hhalf j (by omega)) (hhalf k (by omega)) (hhalf (k + 1) hkn)
        (ih (by omega)) (hfan k hkn)
  -- (b) consecutive triples seen from an earlier chain point
  have hQ : ∀ i s, i < s → s + 1 < n → 0 < orient (q i) (q s) (q (s + 1)) := by
    intro i s his hsn
    induction s, his using Nat.le_induction with
    | base => exact hturn i (by omega)
    | succ s hs ih =>
      exact fan_step (p := p) (b := q s) (hturn s hsn) (hfan (s + 1) hsn) (hfan s (by omega))
        (ih (by omega)) (hP i (s + 1) (by omega) (by omega))
  refine ⟨hP, ?_⟩
  -- (c) all triples, by transitivity around `q i` in the half-plane left of the line `p → q i`
  intro i j k hij hjk hkn
  induction k, hjk using Nat.le_induction with
  | base => exact hQ i j hij hkn
  | succ k hk ih =>
    have hl : ∀ t, i < t → t < n → 0 < lin ![-(q i 1 - p 1), q i 0 - p 0] (q i) (q t) := by
      intro t hit htn
      rw [← orient_eq_lin]
      exact hP i t hit htn
    exact orient_trans_halfplane (hl j hij (by omega)) (hl k (by omega) (by omega))
      (hl (k + 1) (by omega) hkn) (ih (by omega)) (hQ i k (by omega) hkn)

/-- The pivot followed by the chain, indexed by `Fin (n + 1)`. -/
def fanPt (p : Point) (q : ℕ → Point) (i : Fin (n + 1)) : Point :=
  if (i : ℕ) = 0 then p else q ((i : ℕ) - 1)

/-- **A fan chain is a convex polygon.** If `p` and the chain points `q 0, …, q (n-1)` (`n ≥ 3`) of
`S` satisfy the chain conditions inside an open half-plane through `p`, then `S` contains `n + 1`
points in convex position. -/
theorem hasConvexNGon_of_fan {S : Finset Point} {p w : Point} {q : ℕ → Point} {n : ℕ}
    (hn : 3 ≤ n) (hp : p ∈ S) (hq : ∀ s < n, q s ∈ S) (hhalf : ∀ s < n, 0 < lin w p (q s))
    (hfan : ∀ s, s + 1 < n → 0 < orient p (q s) (q (s + 1)))
    (hturn : ∀ s, s + 2 < n → 0 < orient (q s) (q (s + 1)) (q (s + 2))) :
    HasConvexNGon (n + 1) S := by
  classical
  obtain ⟨hP, hT⟩ := fan_positive hhalf hfan hturn
  set x : Fin (n + 1) → Point := fanPt p q with hx
  -- every ordered triple of the polygon is positive
  have htri : ∀ i j k : Fin (n + 1), i < j → j < k → 0 < orient (x i) (x j) (x k) := by
    intro i j k hij hjk
    have hij' : (i : ℕ) < j := hij
    have hjk' : (j : ℕ) < k := hjk
    have hk : (k : ℕ) < n + 1 := k.isLt
    by_cases hi0 : (i : ℕ) = 0
    · have hj0 : (j : ℕ) ≠ 0 := by omega
      have hk0 : (k : ℕ) ≠ 0 := by omega
      simp only [hx, fanPt, hi0, hj0, hk0, if_true, if_false]
      exact hP _ _ (by omega) (by omega)
    · have hj0 : (j : ℕ) ≠ 0 := by omega
      have hk0 : (k : ℕ) ≠ 0 := by omega
      simp only [hx, fanPt, hi0, hj0, hk0, if_false]
      exact hT _ _ _ (by omega) (by omega) (by omega)
  -- injectivity: two distinct indices lie in a positive triple with a third one
  have hinj : Function.Injective x := by
    intro i j hij
    by_contra hne
    rcases lt_or_gt_of_ne hne with h | h
    · -- pick a third index
      have : ∃ k : Fin (n + 1), k ≠ i ∧ k ≠ j := by
        by_cases h0 : (i : ℕ) = 0 ∧ (j : ℕ) = 1
        · exact ⟨⟨2, by omega⟩, fun e => by simp [Fin.ext_iff] at e; omega,
            fun e => by simp [Fin.ext_iff] at e; omega⟩
        · by_cases h1 : (i : ℕ) = 0
          · exact ⟨⟨1, by omega⟩, fun e => by simp [Fin.ext_iff] at e; omega,
              fun e => by simp [Fin.ext_iff] at e; omega⟩
          · exact ⟨⟨0, by omega⟩, fun e => by simp [Fin.ext_iff] at e; omega,
              fun e => by simp [Fin.ext_iff] at e; omega⟩
      obtain ⟨k, hki, hkj⟩ := this
      have hzero : ∀ a c : Point, orient a a c = 0 := fun a c => by simp [orient]
      rcases lt_or_gt_of_ne hki with hk1 | hk1 <;> rcases lt_or_gt_of_ne hkj with hk2 | hk2
      · have := htri k i j hk1 h
        rw [hij, orient_cycle, orient_cycle] at this
        rw [hzero] at this
        exact lt_irrefl _ this
      · exact absurd (lt_trans hk1 h) (lt_asymm hk2)
      · have := htri i k j hk1 hk2
        rw [hij, orient_cycle, hzero] at this
        exact lt_irrefl _ this
      · have := htri i j k h hk2
        rw [hij, hzero] at this
        exact lt_irrefl _ this
    · -- symmetric case
      have hji : x j = x i := hij.symm
      have : ∃ k : Fin (n + 1), k ≠ i ∧ k ≠ j := by
        by_cases h0 : (j : ℕ) = 0 ∧ (i : ℕ) = 1
        · exact ⟨⟨2, by omega⟩, fun e => by simp [Fin.ext_iff] at e; omega,
            fun e => by simp [Fin.ext_iff] at e; omega⟩
        · by_cases h1 : (j : ℕ) = 0
          · exact ⟨⟨1, by omega⟩, fun e => by simp [Fin.ext_iff] at e; omega,
              fun e => by simp [Fin.ext_iff] at e; omega⟩
          · exact ⟨⟨0, by omega⟩, fun e => by simp [Fin.ext_iff] at e; omega,
              fun e => by simp [Fin.ext_iff] at e; omega⟩
      obtain ⟨k, hki, hkj⟩ := this
      have hzero : ∀ a c : Point, orient a a c = 0 := fun a c => by simp [orient]
      rcases lt_or_gt_of_ne hkj with hk1 | hk1 <;> rcases lt_or_gt_of_ne hki with hk2 | hk2
      · have := htri k j i hk1 h
        rw [hji, orient_cycle, orient_cycle] at this
        rw [hzero] at this
        exact lt_irrefl _ this
      · exact absurd (lt_trans hk1 h) (lt_asymm hk2)
      · have := htri j k i hk1 hk2
        rw [hji, orient_cycle, hzero] at this
        exact lt_irrefl _ this
      · have := htri j i k h hk2
        rw [hji, hzero] at this
        exact lt_irrefl _ this
  have hconv : ConvexPosition ((Finset.univ : Finset (Fin (n + 1))).image x) :=
    ErdosSzekeres.Suk.convexPosition_of_positive_triples x hinj Finset.univ (by simp; omega)
      (fun i _ j _ k _ hij hjk => htri i j k hij hjk)
  refine ⟨(Finset.univ : Finset (Fin (n + 1))).image x, ?_, ?_, hconv⟩
  · intro y hy
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.1 hy
    by_cases hi0 : (i : ℕ) = 0
    · simp only [hx, fanPt, hi0, if_true]
      exact hp
    · simp only [hx, fanPt, hi0, if_false]
      exact hq _ (by have := i.isLt; omega)
  · rw [Finset.card_image_of_injective _ hinj]
    simp

/-! ## 10. Soundness of the chain clauses for layered configurations -/

/-- The tangent functional at a polygon vertex, evaluated on another vertex of the same orbit. -/
theorem lin_rotAbout (c p : Point) (β : ℝ) :
    lin (c - p) p (rotAbout c β p) = ((p 0 - c 0) ^ 2 + (p 1 - c 1) ^ 2) * (1 - Real.cos β) := by
  simp only [lin, rotAbout, Pi.sub_apply, Matrix.cons_val_zero, Matrix.cons_val_one]
  ring

/-- Every other vertex of the regular `m`-gon through `p` lies strictly on the inner side of the
tangent at `p`. -/
theorem lin_orbit_pos {c p : Point} (hpc : p ≠ c) {m : ℕ} (hm : 0 < m) {j : ℕ} (hj0 : 0 < j)
    (hjm : j < m) : 0 < lin (c - p) p ((rotAbout c (2 * Real.pi / m))^[j] p) := by
  rw [rotAbout_iterate, lin_rotAbout]
  have hr : 0 < (p 0 - c 0) ^ 2 + (p 1 - c 1) ^ 2 := by
    by_contra h
    apply hpc
    have h0 : p 0 - c 0 = 0 := by nlinarith [sq_nonneg (p 0 - c 0), sq_nonneg (p 1 - c 1)]
    have h1 : p 1 - c 1 = 0 := by nlinarith [sq_nonneg (p 0 - c 0), sq_nonneg (p 1 - c 1)]
    funext i
    fin_cases i
    · simpa using sub_eq_zero.1 h0
    · simpa using sub_eq_zero.1 h1
  have hmpos : (0 : ℝ) < m := by exact_mod_cast hm
  have hβ0 : 0 < (j : ℝ) * (2 * Real.pi / m) := by
    have : (0 : ℝ) < j := by exact_mod_cast hj0
    positivity
  have hβ1 : (j : ℝ) * (2 * Real.pi / m) < 2 * Real.pi := by
    have hjm' : (j : ℝ) < m := by exact_mod_cast hjm
    rw [mul_div_assoc', div_lt_iff₀ hmpos]
    nlinarith [Real.pi_pos]
  have hcos : Real.cos ((j : ℝ) * (2 * Real.pi / m)) < 1 := by
    refine lt_of_le_of_ne (Real.cos_le_one _) ?_
    intro h
    have := (Real.cos_eq_one_iff_of_lt_of_lt (by linarith [Real.pi_pos]) hβ1).1 h
    linarith
  have : 0 < 1 - Real.cos ((j : ℝ) * (2 * Real.pi / m)) := by linarith
  positivity

/-- For `m ≥ 3` the vertex triple `p, ρ p, ρ^{m-1} p` is positively oriented. -/
theorem orient_next_prev_pos {c p : Point} (hpc : p ≠ c) {m : ℕ} (hm : 3 ≤ m) :
    0 < orient p (rotAbout c (2 * Real.pi / m) p) ((rotAbout c (2 * Real.pi / m))^[m - 1] p) := by
  rw [rotAbout_iterate, orient_rotAbout]
  have hr : 0 < (p 0 - c 0) ^ 2 + (p 1 - c 1) ^ 2 := by
    by_contra h
    apply hpc
    have h0 : p 0 - c 0 = 0 := by nlinarith [sq_nonneg (p 0 - c 0), sq_nonneg (p 1 - c 1)]
    have h1 : p 1 - c 1 = 0 := by nlinarith [sq_nonneg (p 0 - c 0), sq_nonneg (p 1 - c 1)]
    funext i
    fin_cases i
    · simpa using sub_eq_zero.1 h0
    · simpa using sub_eq_zero.1 h1
  refine mul_pos hr ?_
  set t : ℝ := Real.pi / m with htdef
  have hmpos : (0 : ℝ) < m := by exact_mod_cast (show 0 < m by omega)
  have hm3 : (3 : ℝ) ≤ m := by exact_mod_cast hm
  have hcast : ((m - 1 : ℕ) : ℝ) = (m : ℝ) - 1 := by
    rw [Nat.cast_sub (by omega)]
    simp
  have h2t : 2 * Real.pi / m = 2 * t := by rw [htdef]; ring
  have h2s : ((m - 1 : ℕ) : ℝ) * (2 * Real.pi / m) = 2 * (((m : ℝ) - 1) * t) := by
    rw [hcast, htdef]; ring
  rw [h2s, h2t, trig_layer]
  have hmt : (m : ℝ) * t = Real.pi := by rw [htdef]; field_simp
  have ht0 : 0 < t := by positivity
  have h1 : 0 < Real.sin t := Real.sin_pos_of_pos_of_lt_pi ht0 (by nlinarith [Real.pi_pos])
  have h2 : 0 < Real.sin (((m : ℝ) - 1) * t) :=
    Real.sin_pos_of_pos_of_lt_pi (by nlinarith) (by nlinarith)
  have h3 : 0 < Real.sin (((m : ℝ) - 1) * t - t) :=
    Real.sin_pos_of_pos_of_lt_pi (by nlinarith) (by nlinarith)
  positivity

/-- **The half-plane hypothesis of the chain family.** For a pivot `p` of layer `i`, every other
point of the layers `≥ i` lies strictly on the inner side of the tangent at `p`. -/
theorem lin_pos_of_peel {S : Finset Point} {c : Point} {m K : ℕ} (hm : 3 ≤ m) (hK : K ≤ 2 * m)
    (hc : c ∉ S) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hno : ¬ HasConvexNGon K S)
    (hgp : GeneralPosition S) {i : ℕ} {p : Point} (hp : p ∈ hullVerts (peel S i)) {y : Point}
    (hy : y ∈ peel S i) (hyp : y ≠ p) : 0 < lin (c - p) p y := by
  set ρ := rotAbout c (2 * Real.pi / m) with hρ
  have hm0 : 0 < m := by omega
  have hpS : p ∈ S := peel_subset S i (hullVerts_subset _ hp)
  have hpc : p ≠ c := fun h => hc (h ▸ hpS)
  have hci : c ∉ peel S i := fun h => hc (peel_subset S i h)
  have hnon : ¬ HasConvexNGon K (peel S i) := fun ⟨t, ht, htK⟩ =>
    hno ⟨t, ht.trans (peel_subset S i), htK⟩
  have hL := hullVerts_eq_orbitFS_rotAbout hm0 hK hci (invariant_peel hm0 hc hinv i) hnon hp
  by_cases hyL : y ∈ hullVerts (peel S i)
  · rw [hL] at hyL
    obtain ⟨j, hj, rfl⟩ := Finset.mem_image.1 hyL
    have hj0 : j ≠ 0 := by rintro rfl; exact hyp rfl
    exact lin_orbit_pos hpc hm0 (by omega) (Finset.mem_range.1 hj)
  · have hy1 : y ∈ peel S (i + 1) := by
      rw [peel_succ]; exact Finset.mem_sdiff.2 ⟨hy, hyL⟩
    set p' := ρ^[m - 1] p with hp'
    have hp'L : p' ∈ hullVerts (peel S i) := by
      rw [hL]; exact Finset.mem_image.2 ⟨m - 1, Finset.mem_range.2 (by omega), rfl⟩
    have hρp' : ρ p' = p := by
      rw [hp', ← Function.iterate_succ_apply' ρ (m - 1) p, Nat.succ_eq_add_one,
        Nat.sub_add_cancel (by omega : 1 ≤ m)]
      have := iterate_minimalPeriod (f := ρ) (x := p)
      rwa [hρ, minimalPeriod_rotAbout hm0 hpc] at this
    have e1 : 0 < orient p (ρ p) y :=
      strict_nesting (by omega) hK hc hinv hno hgp (by omega : i < i + 1) hp hy1
    have e2 : 0 < orient p' (ρ p') y :=
      strict_nesting (by omega) hK hc hinv hno hgp (by omega : i < i + 1) hp'L hy1
    rw [hρp'] at e2
    have hw1 : 0 < lin (c - p) p (ρ p) := by
      have := lin_orbit_pos hpc hm0 (j := 1) (by omega) (by omega)
      simpa using this
    have hw2 : 0 < lin (c - p) p p' := lin_orbit_pos hpc hm0 (by omega) (by omega)
    have hpp : 0 < orient p (ρ p) p' := orient_next_prev_pos hpc hm
    have key : orient p (ρ p) p' * lin (c - p) p y =
        orient p' p y * lin (c - p) p (ρ p) + orient p (ρ p) y * lin (c - p) p p' := by
      simp only [orient, lin, Pi.sub_apply]
      ring
    have hpos : 0 < orient p (ρ p) p' * lin (c - p) p y := by
      rw [key]; positivity
    exact pos_of_mul_pos_right hpos hpp.le

/-- **Soundness of the chain clauses.** In a configuration satisfying the hypotheses of the layer
lemma, in general position and with no `K` points in convex position (`4 ≤ K ≤ 2m`, `m ≥ 3`),
there is no chain of `K - 1` points of the layers `≥ i`, other than a pivot `p` of layer `i`, with
`orient p (q s) (q (s+1)) > 0` and `orient (q s) (q (s+1)) (q (s+2)) > 0`.  This is the statement that
the true orientations satisfy the encoders' "no convex `K`-gon" clauses. -/
theorem chain_clauses_sound {S : Finset Point} {c : Point} {m K : ℕ} (hm : 3 ≤ m) (hK4 : 4 ≤ K)
    (hK : K ≤ 2 * m) (hc : c ∉ S) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S)
    (hno : ¬ HasConvexNGon K S) (hgp : GeneralPosition S) {i : ℕ} {p : Point}
    (hp : p ∈ hullVerts (peel S i)) {q : ℕ → Point} (hq : ∀ s < K - 1, q s ∈ peel S i)
    (hqp : ∀ s < K - 1, q s ≠ p)
    (hfan : ∀ s, s + 1 < K - 1 → 0 < orient p (q s) (q (s + 1)))
    (hturn : ∀ s, s + 2 < K - 1 → 0 < orient (q s) (q (s + 1)) (q (s + 2))) : False := by
  have hpS : p ∈ peel S i := hullVerts_subset _ hp
  have hconv : HasConvexNGon (K - 1 + 1) (peel S i) :=
    hasConvexNGon_of_fan (w := c - p) (by omega) hpS hq
      (fun s hs => lin_pos_of_peel hm hK hc hinv hno hgp hp (hq s hs) (hqp s hs)) hfan hturn
  rw [Nat.sub_add_cancel (by omega)] at hconv
  obtain ⟨t, ht, htK, htc⟩ := hconv
  exact hno ⟨t, ht.trans (peel_subset S i), htK, htc⟩

/-! ## 11. The angular rules (polar form) and radius order of layers -/

/-- The point at distance `r` from `c` in direction `θ`. -/
noncomputable def polar (c : Point) (r θ : ℝ) : Point := ![c 0 + r * Real.cos θ, c 1 + r * Real.sin θ]

/-- **Polar orientation formula.** -/
theorem orient_polar (c : Point) (ra rb rd α β δ : ℝ) :
    orient (polar c ra α) (polar c rb β) (polar c rd δ) =
      ra * rb * Real.sin (β - α) + rb * rd * Real.sin (δ - β) + rd * ra * Real.sin (α - δ) := by
  simp only [orient, polar, Matrix.cons_val_zero, Matrix.cons_val_one, Real.sin_sub]
  ring

/-- **Angular rule A (centre inside the triangle).** If the three directions are in counter-clockwise
order with all three gaps in `(0, π)`, the triple is positively oriented. -/
theorem orient_polar_centre_inside {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hb : 0 < rb)
    (hd : 0 < rd) (h1 : 0 < β - α) (h1' : β - α < Real.pi) (h2 : 0 < δ - β) (h2' : δ - β < Real.pi)
    (h3 : 0 < α - δ + 2 * Real.pi) (h3' : α - δ + 2 * Real.pi < Real.pi) :
    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by
  rw [orient_polar]
  have s1 := Real.sin_pos_of_pos_of_lt_pi h1 h1'
  have s2 := Real.sin_pos_of_pos_of_lt_pi h2 h2'
  have s3 : 0 < Real.sin (α - δ) := by
    have := Real.sin_pos_of_pos_of_lt_pi h3 h3'
    rwa [Real.sin_add_two_pi] at this
  positivity

/-- `sin x + sin y > sin (x + y)` for `x, y ∈ (0, π)`. -/
theorem sin_add_lt {x y : ℝ} (hx : 0 < x) (hx' : x < Real.pi) (hy : 0 < y) (hy' : y < Real.pi) :
    Real.sin (x + y) < Real.sin x + Real.sin y := by
  rw [Real.sin_add]
  have sx := Real.sin_pos_of_pos_of_lt_pi hx hx'
  have sy := Real.sin_pos_of_pos_of_lt_pi hy hy'
  have cx : Real.cos x < 1 := by
    refine lt_of_le_of_ne (Real.cos_le_one x) fun h => ?_
    have := (Real.cos_eq_one_iff_of_lt_of_lt (by linarith) (by linarith)).1 h
    linarith
  have cy : Real.cos y < 1 := by
    refine lt_of_le_of_ne (Real.cos_le_one y) fun h => ?_
    have := (Real.cos_eq_one_iff_of_lt_of_lt (by linarith) (by linarith)).1 h
    linarith
  nlinarith [mul_pos sx (sub_pos.2 cy), mul_pos sy (sub_pos.2 cx)]

/-- **Angular rule B (open half-plane, middle point outermost).** If the directions increase by
`x, y > 0` with `x + y < π` and the angularly middle point has the largest radius, the triple turns
left. -/
theorem orient_polar_halfplane {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hd : 0 < rd)
    (hba : ra ≤ rb) (hbd : rd ≤ rb) (h1 : 0 < β - α) (h2 : 0 < δ - β) (h12 : δ - α < Real.pi) :
    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by
  rw [orient_polar]
  set x := β - α
  set y := δ - β
  have hxy : α - δ = -(x + y) := by simp only [x, y]; ring
  rw [hxy, Real.sin_neg]
  have hx' : x < Real.pi := by simp only [x, y] at h12 h2 ⊢; linarith
  have hy' : y < Real.pi := by simp only [x, y] at h12 h1 ⊢; linarith
  have sx := Real.sin_pos_of_pos_of_lt_pi h1 hx'
  have sy := Real.sin_pos_of_pos_of_lt_pi h2 hy'
  have key := sin_add_lt h1 hx' h2 hy'
  have e1 : ra * rd * Real.sin x ≤ ra * rb * Real.sin x := by
    have := mul_le_mul_of_nonneg_left hbd (mul_nonneg ha.le sx.le)
    nlinarith
  have e2 : ra * rd * Real.sin y ≤ rb * rd * Real.sin y := by
    have := mul_le_mul_of_nonneg_left hba (mul_nonneg hd.le sy.le)
    nlinarith
  have e3 : 0 < ra * rd * (Real.sin x + Real.sin y - Real.sin (x + y)) := by
    have := sub_pos.2 key
    positivity
  nlinarith

/-- Squared distance from `c`. -/
def dist2 (c y : Point) : ℝ := (y 0 - c 0) ^ 2 + (y 1 - c 1) ^ 2

/-- The closed disk `{y | dist2 c y ≤ R}` is convex. -/
theorem convex_disk (c : Point) (R : ℝ) : Convex ℝ {y : Point | dist2 c y ≤ R} := by
  intro y₁ hy₁ y₂ hy₂ u v hu hv huv
  simp only [Set.mem_setOf_eq, dist2] at hy₁ hy₂ ⊢
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  have hv' : v = 1 - u := by linarith
  subst hv'
  nlinarith [sq_nonneg (y₁ 0 - y₂ 0), sq_nonneg (y₁ 1 - y₂ 1), mul_nonneg hu hv]

/-- **Radius order of the layers.** Under the hypotheses of the layer lemma, every point of a later
layer is no farther from the centre than the points of an earlier layer. -/
theorem dist2_le_of_later {S : Finset Point} {c : Point} {m K : ℕ} (hm : 0 < m) (hK : K ≤ 2 * m)
    (hc : c ∉ S) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hno : ¬ HasConvexNGon K S)
    {n n' : ℕ} (hnn' : n ≤ n') {x : Point} (hx : x ∈ hullVerts (peel S n)) {y : Point}
    (hy : y ∈ peel S n') : dist2 c y ≤ dist2 c x := by
  have hcn : c ∉ peel S n := fun h => hc (peel_subset S n h)
  have hnon : ¬ HasConvexNGon K (peel S n) := fun ⟨t, ht, htK⟩ =>
    hno ⟨t, ht.trans (peel_subset S n), htK⟩
  have hL := hullVerts_eq_orbitFS_rotAbout hm hK hcn (invariant_peel hm hc hinv n) hnon hx
  -- every vertex of the layer has the same distance from `c`
  have hsub : (hullVerts (peel S n) : Set Point) ⊆ {z : Point | dist2 c z ≤ dist2 c x} := by
    intro z hz
    rw [Finset.mem_coe, hL] at hz
    obtain ⟨j, -, rfl⟩ := Finset.mem_image.1 hz
    simp only [Set.mem_setOf_eq, dist2]
    rw [rotAbout_iterate]
    simp only [rotAbout, Matrix.cons_val_zero, Matrix.cons_val_one]
    nlinarith [Real.sin_sq_add_cos_sq ((j : ℝ) * (2 * Real.pi / m))]
  have hyn : y ∈ peel S n := peel_antitone S hnn' hy
  have hyconv : y ∈ convexHull ℝ (hullVerts (peel S n) : Set Point) :=
    subset_convexHull_hullVerts (peel S n) (Finset.mem_coe.2 hyn)
  exact convexHull_min hsub (convex_disk c _) hyconv

/-! ## 12. Reduction to exactly `t` layers (§1 of `C6UPPER` and `C7UPPER`) -/

/-- While the remaining set is nonempty, each peel removes exactly one orbit of `m` points. -/
theorem card_peel {S : Finset Point} {c : Point} {m K : ℕ} (hm : 0 < m) (hK : K ≤ 2 * m)
    (hc : c ∉ S) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hno : ¬ HasConvexNGon K S)
    {t : ℕ} (ht : m * (t - 1) < S.card) : ∀ n ≤ t, (peel S n).card + m * n = S.card := by
  intro n hn
  induction n with
  | zero => simp [peel]
  | succ n ih =>
    have ih' := ih (by omega)
    have hne : (peel S n).Nonempty := by
      rw [← Finset.card_pos]
      have : m * n ≤ m * (t - 1) := Nat.mul_le_mul_left m (by omega)
      omega
    obtain ⟨x, hx, hL, hcard, -⟩ := layers_are_orbits hm hK hc hinv hno n hne
    have hsub : hullVerts (peel S n) ⊆ peel S n := hullVerts_subset _
    have hcardL : (hullVerts (peel S n)).card = m := by
      have hxv : x ∈ hullVerts (peel S n) := by
        rw [hL]; exact mem_orbitFS_self hm x
      rw [hullVerts_eq_orbitFS_rotAbout hm hK (fun h => hc (peel_subset S n h))
        (invariant_peel hm hc hinv n) (fun ⟨u, hu, huK⟩ => hno ⟨u, hu.trans (peel_subset S n), huK⟩) hxv]
      exact hcard
    rw [peel_succ, Finset.card_sdiff_of_subset hsub, hcardL]
    have : m ≤ (peel S n).card := hcardL ▸ Finset.card_le_card hsub
    rw [Nat.mul_succ]
    omega

/-- **Reduction to exactly `t` layers.** Suppose every set of exactly `m · t` points that is
invariant under the rotation by `2π/m` about `c ∉` the set and in general position has `K` points in
convex position (`K ≤ 2m`).  Then so does every invariant set in general position with more than
`m (t - 1)` points other than the centre. -/
theorem convexNGon_of_layers {m K t : ℕ} (hm : 0 < m) (hK : K ≤ 2 * m)
    (H : ∀ (T : Finset Point) (c : Point), GeneralPosition T → c ∉ T →
      Invariant (rotAbout c (2 * Real.pi / m)) T → T.card = m * t → HasConvexNGon K T)
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hcard : m * (t - 1) < (S.erase c).card) :
    HasConvexNGon K S := by
  classical
  by_contra hno
  set S' := S.erase c with hS'
  have hc' : c ∉ S' := Finset.notMem_erase c S
  have hinv' : Invariant (rotAbout c (2 * Real.pi / m)) S' := invariant_erase_centre hinv
  have hno' : ¬ HasConvexNGon K S' := fun ⟨u, hu, huK⟩ => hno ⟨u, hu.trans (Finset.erase_subset c S), huK⟩
  have hcp := card_peel hm hK hc' hinv' hno' hcard t le_rfl
  set T := S' \ peel S' t with hT
  have hTcard : T.card = m * t := by
    rw [hT, Finset.card_sdiff_of_subset (peel_subset S' t)]
    omega
  -- `T` is invariant: `S'` and `peel S' t` are, and the rotation has period `m` on `S'`
  have hTinv : Invariant (rotAbout c (2 * Real.pi / m)) T := by
    intro y hy
    obtain ⟨hyS, hyP⟩ := Finset.mem_sdiff.1 hy
    refine Finset.mem_sdiff.2 ⟨hinv' y hyS, fun hρy => hyP ?_⟩
    have hyc : y ≠ c := fun h => hc' (h ▸ hyS)
    have hback : (rotAbout c (2 * Real.pi / m))^[m - 1] (rotAbout c (2 * Real.pi / m) y) = y := by
      rw [← Function.iterate_succ_apply, Nat.succ_eq_add_one, Nat.sub_add_cancel (by omega : 1 ≤ m)]
      have := iterate_minimalPeriod (f := rotAbout c (2 * Real.pi / m)) (x := y)
      rwa [minimalPeriod_rotAbout hm hyc] at this
    rw [← hback]
    exact iterate_mem (invariant_peel hm hc' hinv' t) hρy (m - 1)
  have hTsub : T ⊆ S := (Finset.sdiff_subset).trans (Finset.erase_subset c S)
  have hTgp : GeneralPosition T := fun a ha b hb d hd => hgp a (hTsub ha) b (hTsub hb) d (hTsub hd)
  have hcT : c ∉ T := fun h => hc' ((Finset.sdiff_subset) h)
  obtain ⟨u, hu, huK, hconv⟩ := H T c hTgp hcT hTinv hTcard
  exact hno ⟨u, hu.trans hTsub, huK, hconv⟩

/-- The `66`-point sixfold statement certified by `C6UPPER` (11 nested regular hexagons). -/
def Sixfold66 : Prop :=
  ∀ (T : Finset Point) (c : Point), GeneralPosition T → c ∉ T →
    Invariant (rotAbout c (2 * Real.pi / 6)) T → T.card = 66 → HasConvexNGon 8 T

/-- The `70`-point sevenfold statement certified by `C7UPPER` (10 nested regular heptagons). -/
def Sevenfold70 : Prop :=
  ∀ (T : Finset Point) (c : Point), GeneralPosition T → c ∉ T →
    Invariant (rotAbout c (2 * Real.pi / 7)) T → T.card = 70 → HasConvexNGon 8 T

/-- **The sixfold case of `ES(8) = 65`, reduced to `Sixfold66`.** Every sixfold symmetric set of at
least 61 points in general position contains a convex octagon. -/
theorem sixfold_octagon (H : Sixfold66) (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 6)) S) (hcard : 61 ≤ S.card) :
    HasConvexNGon 8 S := by
  classical
  -- the centre is not in `S` (even order)
  obtain ⟨p, hpS, hpc⟩ : ∃ p ∈ S, p ≠ c := by
    by_contra h
    push_neg at h
    have : S ⊆ {c} := fun y hy => Finset.mem_singleton.2 (h y hy)
    have := Finset.card_le_card this
    simp at this
    omega
  have hcS : c ∉ S := centre_not_mem_of_even (m := 6) (by norm_num) (by decide)
    (by exact_mod_cast hinv) hgp hpS hpc
  refine convexNGon_of_layers (m := 6) (t := 11) (by norm_num) (by norm_num) ?_ S c hgp
    (by exact_mod_cast hinv) ?_
  · intro T c' h1 h2 h3 h4
    exact H T c' h1 h2 (by exact_mod_cast h3) (by simpa using h4)
  · rw [Finset.erase_eq_of_notMem hcS]
    omega

/-- **The sevenfold case of `ES(8) = 65`, reduced to `Sevenfold70`.** Every sevenfold symmetric set
of at least 65 points in general position contains a convex octagon. -/
theorem sevenfold_octagon (H : Sevenfold70) (S : Finset Point) (c : Point)
    (hgp : GeneralPosition S) (hinv : Invariant (rotAbout c (2 * Real.pi / 7)) S)
    (hcard : 65 ≤ S.card) : HasConvexNGon 8 S := by
  classical
  refine convexNGon_of_layers (m := 7) (t := 10) (by norm_num) (by norm_num) ?_ S c hgp
    (by exact_mod_cast hinv) ?_
  · intro T c' h1 h2 h3 h4
    exact H T c' h1 h2 (by exact_mod_cast h3) (by simpa using h4)
  · have := Finset.card_erase_le (s := S) (a := c)
    have h2 := Finset.pred_card_le_card_erase (s := S) (a := c)
    omega


/-! ## 13. Distinct layers have distinct phases (merged from `lean_orbit/OrbitConsistency.lean`)

The results of part (c) of `OrbitConsistency.lean` (`antipode_mem_of_even`, `same_ray_false`,
`rotAbout_polar`, `eq_iterate_of_phase_eq`, `polar_add_int`, `eq_iterate_of_phase_eq_int`,
`phase_ne_of_not_mem_orbit`), restated over the definitions of this file (`iterate_mem`,
`Invariant`, `rotAbout`, `rotAbout_iterate`, `polar`), which that file had copied verbatim.  The
proofs are unchanged.  Then the combined statement `phase_ne_of_distinct_layers`. -/

section Phases

/-- For even `m`, the antipode `2c - x` of a point of an invariant set lies in the set. -/
theorem antipode_mem_of_even {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m)
    (hm : 0 < m) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) {x : Point} (hx : x ∈ S) :
    (![2 * c 0 - x 0, 2 * c 1 - x 1] : Point) ∈ S := by
  have hq : (rotAbout c (2 * Real.pi / m))^[m / 2] x ∈ S := iterate_mem hinv hx (m / 2)
  have hhalf : ((m / 2 : ℕ) : ℝ) * (2 * Real.pi / m) = Real.pi := by
    obtain ⟨k, hk⟩ := heven
    have hk' : m / 2 = k := by omega
    have hkpos : (0 : ℝ) < k := by exact_mod_cast (show 0 < k by omega)
    rw [hk', hk]
    push_cast
    field_simp
    ring
  have hqval : (rotAbout c (2 * Real.pi / m))^[m / 2] x = ![2 * c 0 - x 0, 2 * c 1 - x 1] := by
    rw [rotAbout_iterate, hhalf]
    funext i
    fin_cases i <;> simp [rotAbout] <;> ring
  rw [← hqval]
  exact hq

/-- For even `m`, an invariant set in general position has no two distinct points `x, y` on one
open ray from `c` (`y - c = λ (x - c)`, `λ > 0`): `x`, `y` and `2c - x ∈ S` would be collinear. -/
theorem same_ray_false {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m) (hm : 0 < m)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    {x y : Point} (hx : x ∈ S) (hy : y ∈ S) (hxy : x ≠ y) {l : ℝ} (hl : 0 < l)
    (hray : y - c = l • (x - c)) : False := by
  set q : Point := ![2 * c 0 - x 0, 2 * c 1 - x 1] with hqdef
  have hq : q ∈ S := antipode_mem_of_even heven hm hinv hx
  have hy0 : y 0 = c 0 + l * (x 0 - c 0) := by
    have := congrFun hray 0
    simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at this
    linarith
  have hy1 : y 1 = c 1 + l * (x 1 - c 1) := by
    have := congrFun hray 1
    simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul] at this
    linarith
  have hxc : x ≠ c := by
    intro h
    apply hxy
    funext i
    fin_cases i
    · show x 0 = y 0
      rw [hy0, h]
      ring
    · show x 1 = y 1
      rw [hy1, h]
      ring
  have hcoord : x 0 ≠ c 0 ∨ x 1 ≠ c 1 := by
    by_contra hcon
    push_neg at hcon
    apply hxc
    funext i
    fin_cases i
    · exact hcon.1
    · exact hcon.2
  have hxq : x ≠ q := by
    intro h
    have h0 := congrFun h 0
    have h1 := congrFun h 1
    simp only [hqdef, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
    rcases hcoord with h' | h'
    · exact h' (by linarith)
    · exact h' (by linarith)
  have hyq : y ≠ q := by
    intro h
    have h0 := congrFun h 0
    have h1 := congrFun h 1
    simp only [hqdef, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
    rw [hy0] at h0
    rw [hy1] at h1
    have e0 : (l + 1) * (x 0 - c 0) = 0 := by linarith
    have e1 : (l + 1) * (x 1 - c 1) = 0 := by linarith
    have hl1 : l + 1 ≠ 0 := by linarith
    rcases hcoord with h' | h'
    · exact h' (sub_eq_zero.1 ((mul_eq_zero.1 e0).resolve_left hl1))
    · exact h' (sub_eq_zero.1 ((mul_eq_zero.1 e1).resolve_left hl1))
  have h0 : orient x y q = 0 := by
    simp only [orient, hqdef, Matrix.cons_val_zero, Matrix.cons_val_one]
    rw [hy0, hy1]
    ring
  exact (generalPosition_iff_orient_ne_zero S).1 hgp x hx y hy q hq hxy hxq hyq h0

theorem rotAbout_polar (c : Point) (r θ φ : ℝ) :
    rotAbout c φ (polar c r θ) = polar c r (θ + φ) := by
  funext i
  fin_cases i <;> simp [rotAbout, polar, Real.cos_add, Real.sin_add] <;> ring

/-- **Phases, natural form.** For even `m`, if two points `x = c + r e^{iα}` and
`y = c + r' e^{iβ}` (`r, r' > 0`) of an invariant set in general position satisfy
`β = α + k · 2π/m`, then `y = ρ^k x`. -/
theorem eq_iterate_of_phase_eq {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m)
    (hm : 0 < m) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    {r r' α β : ℝ} (hr : 0 < r) (hr' : 0 < r') (hx : polar c r α ∈ S) (hy : polar c r' β ∈ S)
    {k : ℕ} (hk : β = α + k * (2 * Real.pi / m)) :
    polar c r' β = (rotAbout c (2 * Real.pi / m))^[k] (polar c r α) := by
  have hx' : (rotAbout c (2 * Real.pi / m))^[k] (polar c r α) ∈ S := iterate_mem hinv hx k
  have hval : (rotAbout c (2 * Real.pi / m))^[k] (polar c r α) = polar c r β := by
    rw [rotAbout_iterate, rotAbout_polar, hk]
  rw [hval] at hx' ⊢
  by_contra hne
  refine same_ray_false heven hm hinv hgp hx' hy (Ne.symm hne) (l := r' / r) (by positivity) ?_
  funext i
  fin_cases i
  · show c 0 + r' * Real.cos β - c 0 = r' / r * (c 0 + r * Real.cos β - c 0)
    rw [div_mul_eq_mul_div, eq_div_iff hr.ne']
    ring
  · show c 1 + r' * Real.sin β - c 1 = r' / r * (c 1 + r * Real.sin β - c 1)
    rw [div_mul_eq_mul_div, eq_div_iff hr.ne']
    ring

theorem polar_add_int (c : Point) (r θ : ℝ) (n : ℤ) :
    polar c r (θ + n * (2 * Real.pi)) = polar c r θ := by
  simp only [polar, Real.cos_add_int_mul_two_pi, Real.sin_add_int_mul_two_pi]

/-- **Phases, integer form.** Same as `eq_iterate_of_phase_eq` with `k ∈ ℤ`: then `y = ρ^j x`
for `j = k mod m`. -/
theorem eq_iterate_of_phase_eq_int {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m)
    (hm : 0 < m) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    {r r' α β : ℝ} (hr : 0 < r) (hr' : 0 < r') (hx : polar c r α ∈ S) (hy : polar c r' β ∈ S)
    {k : ℤ} (hk : β = α + k * (2 * Real.pi / m)) :
    ∃ j : ℕ, polar c r' β = (rotAbout c (2 * Real.pi / m))^[j] (polar c r α) := by
  have hmz : (0 : ℤ) < m := by exact_mod_cast hm
  set j : ℕ := (k % (m : ℤ)).toNat with hjdef
  have hmod_nonneg : 0 ≤ k % (m : ℤ) := Int.emod_nonneg k hmz.ne'
  have hj : (j : ℤ) = k % (m : ℤ) := Int.toNat_of_nonneg hmod_nonneg
  have hdecomp : k = (j : ℤ) + (m : ℤ) * (k / (m : ℤ)) := by
    rw [hj]
    exact (Int.emod_add_mul_ediv k m).symm
  have hmR : (m : ℝ) ≠ 0 := by exact_mod_cast hm.ne'
  have hβ : β = (α + (j : ℝ) * (2 * Real.pi / m)) + ((k / (m : ℤ) : ℤ) : ℝ) * (2 * Real.pi) := by
    rw [hk]
    have hkR : (k : ℝ) = (j : ℝ) + (m : ℝ) * ((k / (m : ℤ) : ℤ) : ℝ) := by
      exact_mod_cast hdecomp
    rw [hkR]
    field_simp
    ring
  have hy' : polar c r' (α + (j : ℝ) * (2 * Real.pi / m)) ∈ S := by
    rw [hβ, polar_add_int] at hy
    exact hy
  refine ⟨j, ?_⟩
  rw [hβ, polar_add_int]
  exact eq_iterate_of_phase_eq heven hm hinv hgp hr hr' hx hy' rfl

/-- If `y` is not in the `ρ`-orbit of `x`, the directions of `x` and `y` are not congruent modulo
`2π/m` (even `m`). -/
theorem phase_ne_of_not_mem_orbit {S : Finset Point} {c : Point} {m : ℕ} (heven : Even m)
    (hm : 0 < m) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    {r r' α β : ℝ} (hr : 0 < r) (hr' : 0 < r') (hx : polar c r α ∈ S) (hy : polar c r' β ∈ S)
    (horb : ∀ j : ℕ, polar c r' β ≠ (rotAbout c (2 * Real.pi / m))^[j] (polar c r α)) :
    ∀ k : ℤ, β ≠ α + k * (2 * Real.pi / m) := by
  intro k hk
  obtain ⟨j, hj⟩ := eq_iterate_of_phase_eq_int heven hm hinv hgp hr hr' hx hy hk
  exact horb j hj

/-! ### Combining with the layer lemma -/

/-- Hull vertices of different peels are disjoint: the layers partition-by-depth. -/
theorem not_mem_hullVerts_peel_of_lt (S : Finset Point) {i j : ℕ} (hij : i < j) {y : Point}
    (hy : y ∈ hullVerts (peel S j)) : y ∉ hullVerts (peel S i) := by
  have h1 : y ∈ peel S (i + 1) := peel_antitone S hij (hullVerts_subset _ hy)
  rw [peel_succ, Finset.mem_sdiff] at h1
  exact h1.2

theorem not_mem_hullVerts_peel_of_ne (S : Finset Point) {i j : ℕ} (hij : i ≠ j) {y : Point}
    (hyi : y ∈ hullVerts (peel S i)) (hyj : y ∈ hullVerts (peel S j)) : False := by
  rcases lt_or_gt_of_ne hij with h | h
  · exact not_mem_hullVerts_peel_of_lt S h hyj hyi
  · exact not_mem_hullVerts_peel_of_lt S h hyi hyj

/-- Under the layer-lemma hypotheses, each layer `hullVerts (peel S i)` is closed under every
power of the rotation: it is one orbit (`layers_are_orbits`). -/
theorem iterate_mem_hullVerts_peel {S : Finset Point} {c : Point} {m K : ℕ} (hm : 0 < m)
    (hK : K ≤ 2 * m) (hc : c ∉ S) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S)
    (hno : ¬ HasConvexNGon K S) {i : ℕ} {x : Point} (hx : x ∈ hullVerts (peel S i)) (k : ℕ) :
    (rotAbout c (2 * Real.pi / m))^[k] x ∈ hullVerts (peel S i) := by
  have hxS : x ∈ peel S i := hullVerts_subset _ hx
  have hcn : c ∉ peel S i := fun h => hc (peel_subset S i h)
  have hnon : ¬ HasConvexNGon K (peel S i) := fun ⟨t, ht, htK, htc⟩ =>
    hno ⟨t, ht.trans (peel_subset S i), htK, htc⟩
  have horb := hullVerts_eq_orbitFS_rotAbout hm hK hcn (invariant_peel hm hc hinv i) hnon hx
  have hper : (rotAbout c (2 * Real.pi / m))^[m] x = x := by
    have hxc : x ≠ c := fun h => hcn (h ▸ hxS)
    have h := iterate_minimalPeriod (f := rotAbout c (2 * Real.pi / m)) (x := x)
    rwa [minimalPeriod_rotAbout hm hxc] at h
  rw [horb]
  exact iterate_mem (orbitFS_invariant hm hper) (mem_orbitFS_self hm x) k

/-- **Distinct layers lie on distinct rays (same-ray form).** For even `m ≥ 2`, let `S` be
invariant under `ρ = rotAbout c (2π/m)`, in general position, with `c ∉ S` and no `K` points in
convex position (`K ≤ 2m`).  If `x` is a hull vertex of `peel S i` and `y` one of `peel S j`
with `i ≠ j`, then `y` is not on the open ray from `c` through any `ρ^k x`. -/
theorem not_same_ray_of_distinct_layers {S : Finset Point} {c : Point} {m K : ℕ} (hm : 2 ≤ m)
    (heven : Even m) (hK : K ≤ 2 * m) (hc : c ∉ S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    (hno : ¬ HasConvexNGon K S) {i j : ℕ} (hij : i ≠ j) {x y : Point}
    (hx : x ∈ hullVerts (peel S i)) (hy : y ∈ hullVerts (peel S j)) (k : ℕ) {l : ℝ} (hl : 0 < l)
    (hray : y - c = l • ((rotAbout c (2 * Real.pi / m))^[k] x - c)) : False := by
  have hm0 : 0 < m := by omega
  have hxk := iterate_mem_hullVerts_peel hm0 hK hc hinv hno hx k
  have hne : (rotAbout c (2 * Real.pi / m))^[k] x ≠ y := fun h =>
    not_mem_hullVerts_peel_of_ne S hij (h ▸ hxk) hy
  exact same_ray_false heven hm0 hinv hgp (peel_subset S i (hullVerts_subset _ hxk))
    (peel_subset S j (hullVerts_subset _ hy)) hne hl hray

/-- **Distinct layers have distinct phases (polar form).** For even `m ≥ 2`, let `S` be invariant
under `ρ = rotAbout c (2π/m)`, in general position, with `c ∉ S` and no `K` points in convex
position (`K ≤ 2m`).  If `x = polar c r α` is a hull vertex of `peel S i` and `y = polar c r' β`
one of `peel S j` (`r, r' > 0`) with `i ≠ j`, then `β - α` is not an integer multiple of `2π/m`. -/
theorem phase_ne_of_distinct_layers {S : Finset Point} {c : Point} {m K : ℕ} (hm : 2 ≤ m)
    (heven : Even m) (hK : K ≤ 2 * m) (hc : c ∉ S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) S) (hgp : GeneralPosition S)
    (hno : ¬ HasConvexNGon K S) {i j : ℕ} (hij : i ≠ j) {r r' α β : ℝ} (hr : 0 < r) (hr' : 0 < r')
    (hx : polar c r α ∈ hullVerts (peel S i)) (hy : polar c r' β ∈ hullVerts (peel S j)) :
    ∀ k : ℤ, β - α ≠ k * (2 * Real.pi / m) := by
  have hm0 : 0 < m := by omega
  intro k hk
  refine phase_ne_of_not_mem_orbit heven hm0 hinv hgp hr hr'
    (peel_subset S i (hullVerts_subset _ hx)) (peel_subset S j (hullVerts_subset _ hy)) ?_ k
    (by linarith)
  intro n hn
  have hxn := iterate_mem_hullVerts_peel hm0 hK hc hinv hno hx n
  rw [← hn] at hxn
  exact not_mem_hullVerts_peel_of_ne S hij hxn hy

end Phases

end ErdosSzekeres.LayerLemma
