import V1L.Main
import V2L.ClauseCover
import V2L.Facts
import V2L.Obligations

/-!
# Mirror sub-case (ii): the axis point is interior

The statement: every set of 33 points in general position that is symmetric in a line, and
whose point on that line lies in the convex hull of the other points, contains a convex 7-gon.

It is reduced to the certificates of the hull-pair split of `results/Mii-S`
(`InteriorCertificates`), with `F = interiorCnf 33 7` (`m33k7int.sub.cnf`):
* root: `F ++ {¬UP(U)}` is UNSAT;
* up:U, for each of the 121 `U`: `cubeCnf F UP(U) ++ {¬cube(U, L) : L}` is UNSAT;
* each of the 450 cases `(U, L)`: the leaves `leaves (U, L)` pass `coverCheck`, and every
  leaf CNF `cubeCnf (cubeCnf F cube(U, L)) l` is UNSAT.
These are established outside Lean (CaDiCaL + cake_lpr). The leaf lists are parameters.
Together with V1-L's sub-case (i) this gives `Mir.MirrorExclusionLine`.
-/

namespace V2L

open ETV ErdosSzekeres Mir

/-- root: every model of `interiorCnf 33 7` satisfies some `UP(U)`. -/
def RootCertificate : Prop :=
  ¬DimacsSatisfiable (interiorCnf 33 7 ++ upCubes.map negClause)

/-- up:U: every model of `interiorCnf 33 7` and `UP(U)` satisfies some `cube(U, L)`. -/
def UpCertificates : Prop :=
  ∀ p ∈ upTable,
    ¬DimacsSatisfiable (cubeCnf (interiorCnf 33 7) p.2 ++ (casesOf p.1).map negClause)

/-- Every case is closed by its leaf cubes. -/
def CaseCertificates (leaves : List Nat × List Nat → List (List Int)) : Prop :=
  ∀ p ∈ caseTable, coverCheck (leaves p.1) = true ∧
    ∀ l ∈ leaves p.1, ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)

/-- All certificates of the hull-pair split, with leaf lists `leaves (U, L)`. -/
def InteriorCertificates (leaves : List Nat × List Nat → List (List Int)) : Prop :=
  RootCertificate ∧ UpCertificates ∧ CaseCertificates leaves

theorem rootCnf_eq : rootCnf = interiorCnf 33 7 ++ upCubes.map negClause := rfl

theorem upCnf_eq (p : List Nat × List Int) :
    upCnf p = cubeCnf (interiorCnf 33 7) p.2 ++ (casesOf p.1).map negClause := rfl

theorem caseCnf_eq (c : List Int) : caseCnf c = cubeCnf (interiorCnf 33 7) c := rfl

/-- Once the cover facts of a concrete leaf table are proved (in the kernel), only the UNSAT
facts remain as hypotheses. -/
theorem interiorCertificates_of_cover {leaves : List Nat × List Nat → List (List Int)}
    (hcov : ∀ p ∈ caseTable, coverCheck (leaves p.1) = true) (hroot : RootCertificate)
    (hup : UpCertificates)
    (hleaf : ∀ p ∈ caseTable, ∀ l ∈ leaves p.1,
      ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)) :
    InteriorCertificates leaves :=
  ⟨hroot, hup, fun p hp => ⟨hcov p hp, hleaf p hp⟩⟩

/-- **The certificates refute `m33k7int.sub.cnf`.** -/
theorem interiorCnf_unsat_of_certificates {leaves : List Nat × List Nat → List (List Int)}
    (h : InteriorCertificates leaves) : ¬DimacsSatisfiable (interiorCnf 33 7) := by
  obtain ⟨hroot, hup, hcase⟩ := h
  refine not_dimacsSatisfiable_of_clauseCover₂ (Us := upTable) (up := Prod.snd)
    (casesOf := fun p => casesOf p.1) upTable_nonzero (fun p _ => casesOf_nonzero p.1)
    (by rw [upTable_snd]; exact hroot) hup ?_
  intro p _ c hc
  obtain ⟨s, hs⟩ := mem_caseCubes_of_casesOf hc
  obtain ⟨hcov, hleaf⟩ := hcase _ hs
  exact not_dimacsSatisfiable_case_of_leaves hcov hleaf

/-- Sub-case (ii), mirror line = y-axis: `c` is the point of `S` on the axis and lies in
`conv (S ∖ {c})`. -/
def AxisInteriorY : Prop :=
  ∀ (S : Finset Point) (c : Point), GeneralPosition S → S.card = 33 →
    (∀ q ∈ S, reflX q ∈ S) → c ∈ S → c 0 = 0 →
    c ∈ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S

/-- Sub-case (ii) for an arbitrary mirror line, the line through `a` with unit direction
`u`. -/
def AxisInteriorLine : Prop :=
  ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
    S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
    c ∈ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S

/-- Sub-case (ii), y-axis form, from UNSAT of `interiorCnf 33 7`. -/
theorem axisInteriorY_of_unsat (h : ¬DimacsSatisfiable (interiorCnf 33 7)) : AxisInteriorY := by
  intro S c hgp hcard hsym hc hc0 hin
  obtain ⟨c', hM⟩ := exists_mirrorSet hgp hsym (by rw [hcard]; decide)
  have hcc' : c = c' := by
    by_contra hne
    exact hM.off c hc hne hc0
  subst hcc'
  exact hasConvexNGon_of_unsat_interior interiorTieBreak_holds h hgp hcard hM hin

/-- The y-axis form gives the form for an arbitrary line, by the rigid motion `toAxis a u`
(the argument of `V1L.hullVertexLine_of_hullVertexY`). -/
theorem axisInteriorLine_of_axisInteriorY (h : AxisInteriorY) : AxisInteriorLine := by
  classical
  intro S a u c hu hgp hcard hsym hc hcfix hin
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
  have hin' : g c ∈ convexHull ℝ (↑((S.image g).erase (g c)) : Set Point) := by
    rw [← Finset.image_erase hg, Finset.coe_image, ← AffineMap.image_convexHull]
    exact Set.mem_image_of_mem _ hin
  exact V1L.hasConvexNGon_of_image_affine g hg (h _ (g c) hgp' hcard' hsym' hc' hc0 hin')

/-- **Sub-case (ii), any mirror line**, from the certificates of the hull-pair split. -/
theorem axisInteriorLine_of_certificates {leaves : List Nat × List Nat → List (List Int)}
    (h : InteriorCertificates leaves) :
    ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
      S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
      c ∈ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S :=
  axisInteriorLine_of_axisInteriorY (axisInteriorY_of_unsat (interiorCnf_unsat_of_certificates h))

/-- **The mirror class**: every 33-point set in general position that is symmetric in some
line has a convex 7-gon, from V1-L's 1,198 leaf facts (sub-case (i)) and the certificates of
the hull-pair split (sub-case (ii)). -/
theorem mirrorExclusionLine_of_certificates {leaves : List Nat × List Nat → List (List Int)}
    (h1 : ∀ c ∈ V1L.hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (h2 : InteriorCertificates leaves) : MirrorExclusionLine :=
  mirrorExclusionLine_of_unsat (V1L.hullCnf_unsat_of_leaves h1)
    (interiorCnf_unsat_of_certificates h2)

end V2L
