import MirrorEncoding.Targets

/-!
# An arbitrary mirror line

`reflLine a u` is the reflection in the line through `a` with unit direction `u`. The rigid
motion `toAxis a u : p ↦ M (p - a)`, `M = [[u₁, -u₀], [u₀, u₁]]`, sends this line to the
y-axis and conjugates `reflLine a u` to `reflX`. It preserves orientations (`det M = 1`),
hence general position, and convex position pulls back along it. So `MirrorExclusionY`
(axis = y-axis) gives `MirrorExclusionLine` (any line).
-/

namespace Mir

open ETV ErdosSzekeres

/-- The reflection in the line through `a` with direction `u` (`u₀² + u₁² = 1`). -/
def reflLine (a u : Point) (p : Point) : Point :=
  let d := (p 0 - a 0) * u 0 + (p 1 - a 1) * u 1
  ![a 0 + 2 * d * u 0 - (p 0 - a 0), a 1 + 2 * d * u 1 - (p 1 - a 1)]

/-- The rigid motion sending the line through `a` with direction `u` to the y-axis. -/
def toAxisFun (a u : Point) (p : Point) : Point :=
  ![u 1 * (p 0 - a 0) - u 0 * (p 1 - a 1), u 0 * (p 0 - a 0) + u 1 * (p 1 - a 1)]

/-- The linear part of `toAxisFun`. -/
def toAxisLin (u : Point) : Point →ₗ[ℝ] Point where
  toFun v := ![u 1 * v 0 - u 0 * v 1, u 0 * v 0 + u 1 * v 1]
  map_add' p q := by
    ext i
    fin_cases i
    all_goals simp
    all_goals ring
  map_smul' c p := by
    ext i
    fin_cases i
    all_goals simp
    all_goals ring

/-- `toAxisFun` as an affine map. -/
def toAxis (a u : Point) : Point →ᵃ[ℝ] Point where
  toFun := toAxisFun a u
  linear := toAxisLin u
  map_vadd' p v := by
    ext i
    fin_cases i
    all_goals simp [toAxisFun, toAxisLin]
    all_goals ring

theorem toAxis_apply (a u p : Point) : toAxis a u p = toAxisFun a u p := rfl

theorem toAxis_injective {a u : Point} (hu : u 0 ^ 2 + u 1 ^ 2 = 1) :
    Function.Injective (toAxis a u) := by
  intro p q h
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  simp only [toAxis_apply, toAxisFun, Matrix.cons_val_zero, Matrix.cons_val_one] at h0 h1
  ext i
  fin_cases i
  · simp only [Fin.zero_eta, Fin.isValue]
    linear_combination u 1 * h0 + u 0 * h1 - (p 0 - q 0) * hu
  · simp only [Fin.mk_one, Fin.isValue]
    linear_combination -u 0 * h0 + u 1 * h1 - (p 1 - q 1) * hu

theorem orient_toAxis {a u : Point} (hu : u 0 ^ 2 + u 1 ^ 2 = 1) (p q r : Point) :
    orient (toAxis a u p) (toAxis a u q) (toAxis a u r) = 1 * orient p q r := by
  simp only [toAxis_apply, toAxisFun, orient, Matrix.cons_val_zero, Matrix.cons_val_one]
  linear_combination ((q 0 - p 0) * (r 1 - p 1) - (q 1 - p 1) * (r 0 - p 0)) * hu

theorem toAxis_reflLine {a u : Point} (hu : u 0 ^ 2 + u 1 ^ 2 = 1) (p : Point) :
    toAxis a u (reflLine a u p) = reflX (toAxis a u p) := by
  ext i
  fin_cases i
  · simp only [toAxis_apply, toAxisFun, reflLine, reflX_zero, Fin.zero_eta, Fin.isValue,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  · simp only [toAxis_apply, toAxisFun, reflLine, reflX_one, Fin.mk_one, Fin.isValue,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    linear_combination 2 * ((p 0 - a 0) * u 0 + (p 1 - a 1) * u 1) * hu

/-- Convex position pulls back along an injective affine map. -/
theorem convexPosition_of_image_affine {T : Finset Point} (f : Point →ᵃ[ℝ] Point)
    (hf : Function.Injective f) (h : ConvexPosition (T.image f)) : ConvexPosition T := by
  classical
  rw [convexPosition_iff] at h ⊢
  intro p hp hhull
  apply h (f p) (by rw [Finset.coe_image]; exact Set.mem_image_of_mem f hp)
  have := Set.mem_image_of_mem f hhull
  rw [AffineMap.image_convexHull] at this
  rwa [Finset.coe_image, ← Set.image_singleton, ← Set.image_diff hf]

/-- Every 33-point set in general position that is symmetric in some line has a convex
7-gon. -/
def MirrorExclusionLine : Prop :=
  ∀ (S : Finset Point) (a u : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
    S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → HasConvexNGon 7 S

theorem mirrorExclusionLine_of_mirrorExclusionY (h : MirrorExclusionY) :
    MirrorExclusionLine := by
  classical
  intro S a u hu hgp hcard hsym
  let g := toAxis a u
  have hg : Function.Injective g := toAxis_injective hu
  have hgp' : GeneralPosition (S.image g) := by
    rw [generalPosition_iff_orient_ne_zero] at hgp ⊢
    intro x hx y hy z hz hxy hxz hyz
    obtain ⟨x', hx', rfl⟩ := Finset.mem_image.1 hx
    obtain ⟨y', hy', rfl⟩ := Finset.mem_image.1 hy
    obtain ⟨z', hz', rfl⟩ := Finset.mem_image.1 hz
    rw [orient_toAxis hu, one_mul]
    exact hgp x' hx' y' hy' z' hz' (fun e => hxy (e ▸ rfl)) (fun e => hxz (e ▸ rfl))
      (fun e => hyz (e ▸ rfl))
  have hcard' : (S.image g).card = 33 := by rw [Finset.card_image_of_injective _ hg, hcard]
  have hsym' : ∀ q ∈ S.image g, reflX q ∈ S.image g := by
    intro w hw
    obtain ⟨q, hq, rfl⟩ := Finset.mem_image.1 hw
    rw [← toAxis_reflLine hu]
    exact Finset.mem_image_of_mem _ (hsym q hq)
  obtain ⟨T', hT', hT'card, hconv⟩ := h _ hgp' hcard' hsym'
  let T := S.filter fun q => g q ∈ T'
  have hTimg : T.image g = T' := by
    ext w
    simp only [T, Finset.mem_image, Finset.mem_filter]
    constructor
    · rintro ⟨q, ⟨_, hq⟩, rfl⟩
      exact hq
    · intro hw
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.1 (hT' hw)
      exact ⟨q, ⟨hq, hw⟩, rfl⟩
  refine ⟨T, Finset.filter_subset _ _, ?_, ?_⟩
  · rw [← hT'card, ← hTimg, Finset.card_image_of_injective _ hg]
  · apply convexPosition_of_image_affine g hg
    rw [hTimg]
    exact hconv

/-- **The reduction for an arbitrary mirror line**: UNSAT of `hm33k7.sub.cnf` and
`m33k7int.sub.cnf` imply that every 33-point set in general position with a mirror
symmetry has a convex 7-gon. -/
theorem mirrorExclusionLine_of_unsat
    (h1 : ¬DimacsSatisfiable (hullCnf 33 7)) (h2 : ¬DimacsSatisfiable (interiorCnf 33 7)) :
    MirrorExclusionLine :=
  mirrorExclusionLine_of_mirrorExclusionY
    (mirrorExclusionY_of_mirrorExclusion (mirrorExclusion_of_unsat h1 h2))

/-- The same from cube-and-conquer data: two cube lists accepted by `coverCheck` and a
refutation of every cube CNF. -/
theorem mirrorExclusionLine_of_cubes {C1 C2 : List (List ℤ)}
    (hc1 : coverCheck C1 = true) (hc2 : coverCheck C2 = true)
    (h1 : ∀ c ∈ C1, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (h2 : ∀ c ∈ C2, ¬DimacsSatisfiable (cubeCnf (interiorCnf 33 7) c)) : MirrorExclusionLine :=
  mirrorExclusionLine_of_unsat (not_dimacsSatisfiable_of_coverCheck hc1 h1)
    (not_dimacsSatisfiable_of_coverCheck hc2 h2)

end Mir
