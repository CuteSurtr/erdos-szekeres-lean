import ErdosSzekeres.Definitions
import ErdosSzekeres.OrientationGeometry
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

end ErdosSzekeres.LayerLemma
