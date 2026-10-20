import MirrorEncoding
import V1L.Cover

/-!
# Mirror sub-case (i): the axis point is a hull vertex

The statement: every set of 33 points in general position that is symmetric in a line, and
whose point on that line is a vertex of the convex hull, contains a convex 7-gon.

The only hypotheses of `hullVertexLine_of_leaves` are the per-cube facts
`¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)` for the 1,198 cubes `c` of `hullLeaves`.
They are established outside Lean (CaDiCaL + cake_lpr on each cube CNF, runs V1-0..V1-3).
The cover fact `coverCheck hullLeaves = true` is proved in `V1L.Cover` by kernel evaluation.
-/

namespace V1L

open ETV ErdosSzekeres Mir

/-- Sub-case (i), mirror line = y-axis: `c` is the point of `S` on the axis and a vertex of
`conv S` (equivalently, `c ∉ conv (S ∖ {c})`). -/
def HullVertexY : Prop :=
  ∀ (S : Finset Point) (c : Point), GeneralPosition S → S.card = 33 →
    (∀ q ∈ S, reflX q ∈ S) → c ∈ S → c 0 = 0 →
    c ∉ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S

/-- Sub-case (i) for an arbitrary mirror line, the line through `a` with unit direction `u`:
`c` is the point of `S` on the line and a vertex of `conv S`. -/
def HullVertexLine : Prop :=
  ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
    S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
    c ∉ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S

/-- The external facts: every leaf cube CNF is unsatisfiable. -/
def LeavesRefuted : Prop :=
  ∀ c ∈ hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)

/-- The leaf facts refute the whole sub-case (i) CNF `hm33k7.sub.cnf`. -/
theorem hullCnf_unsat_of_leaves (h : LeavesRefuted) : ¬DimacsSatisfiable (hullCnf 33 7) :=
  not_dimacsSatisfiable_of_coverCheck hullLeaves_coverCheck h

/-- Sub-case (i), y-axis form, from UNSAT of `hullCnf 33 7`. -/
theorem hullVertexY_of_unsat (h : ¬DimacsSatisfiable (hullCnf 33 7)) : HullVertexY := by
  intro S c hgp hcard hsym hc hc0 hext
  obtain ⟨c', hM⟩ := exists_mirrorSet hgp hsym (by rw [hcard]; decide)
  have hcc' : c = c' := by
    by_contra hne
    exact hM.off c hc hne hc0
  subst hcc'
  exact hasConvexNGon_of_unsat_hull h hgp hcard hM hext

/-- A convex `n`-gon in the image of `S` under an injective affine map pulls back to `S`. -/
theorem hasConvexNGon_of_image_affine {S : Finset Point} {n : ℕ} (g : Point →ᵃ[ℝ] Point)
    (hg : Function.Injective g) (h : HasConvexNGon n (S.image g)) : HasConvexNGon n S := by
  classical
  obtain ⟨T', hT', hT'card, hconv⟩ := h
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

/-- The y-axis form gives the form for an arbitrary line, by the rigid motion `toAxis a u`. -/
theorem hullVertexLine_of_hullVertexY (h : HullVertexY) : HullVertexLine := by
  classical
  intro S a u c hu hgp hcard hsym hc hcfix hext
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
  have hc' : g c ∈ S.image g := Finset.mem_image_of_mem _ hc
  have hc0 : g c 0 = 0 := by
    have e := congrFun (toAxis_reflLine (a := a) hu c) 0
    rw [hcfix, reflX_zero] at e
    change g c 0 = -g c 0 at e
    linarith
  have hext' : g c ∉ convexHull ℝ (↑((S.image g).erase (g c)) : Set Point) := by
    rw [← Finset.image_erase hg, Finset.coe_image, ← AffineMap.image_convexHull]
    rintro ⟨p, hp, hpc⟩
    rw [hg hpc] at hp
    exact hext hp
  exact hasConvexNGon_of_image_affine g hg (h _ (g c) hgp' hcard' hsym' hc' hc0 hext')

/-- **Sub-case (i), y-axis form**, from the per-cube facts alone. -/
theorem hullVertexY_of_leaves (h : LeavesRefuted) : HullVertexY :=
  hullVertexY_of_unsat (hullCnf_unsat_of_leaves h)

/-- **Sub-case (i), any mirror line**, from the per-cube facts alone: if
`¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)` for every cube `c` of `hullLeaves`, then every
33-point set in general position that is symmetric in a line, and whose point on the line is
a vertex of its convex hull, has a convex 7-gon. -/
theorem hullVertexLine_of_leaves
    (h : ∀ c ∈ hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)) :
    ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
      S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
      c ∉ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S :=
  hullVertexLine_of_hullVertexY (hullVertexY_of_leaves h)

end V1L
