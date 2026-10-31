import V2L.Main
import V2L.Tree

/-!
# Sub-case (ii) and the mirror class with tree-shaped case certificates

As `V2L/Main.lean`, with each case closed by a cube tree (`CTree`) instead of a flat leaf list:
the tree passes `CTree.check` (small `coverCheck`s, one per sibling list), and every leaf CNF
`cubeCnf (cubeCnf F cube(U, L)) l`, `l ∈ (tree (U, L)).leaves`, is UNSAT.
-/

namespace V2L

open ETV ErdosSzekeres Mir

/-- Every case is closed by its cube tree. -/
def CaseCertificatesT (tree : List Nat × List Nat → CTree) : Prop :=
  ∀ p ∈ caseTable, (tree p.1).check = true ∧
    ∀ l ∈ (tree p.1).leaves, ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)

/-- All certificates of the hull-pair split, with cube trees `tree (U, L)`. -/
def InteriorCertificatesT (tree : List Nat × List Nat → CTree) : Prop :=
  RootCertificate ∧ UpCertificates ∧ CaseCertificatesT tree

/-- **The certificates refute `m33k7int.sub.cnf`** (tree form). -/
theorem interiorCnf_unsat_of_certificatesT {tree : List Nat × List Nat → CTree}
    (h : InteriorCertificatesT tree) : ¬DimacsSatisfiable (interiorCnf 33 7) := by
  obtain ⟨hroot, hup, hcase⟩ := h
  refine not_dimacsSatisfiable_of_clauseCover₂ (Us := upTable) (up := Prod.snd)
    (casesOf := fun p => casesOf p.1) upTable_nonzero (fun p _ => casesOf_nonzero p.1)
    (by rw [upTable_snd]; exact hroot) hup ?_
  intro p _ c hc
  obtain ⟨s, hs⟩ := mem_caseCubes_of_casesOf hc
  obtain ⟨hcov, hleaf⟩ := hcase _ hs
  exact not_dimacsSatisfiable_of_tree hcov hleaf

/-- **Sub-case (ii), any mirror line**, from the certificates with cube trees. -/
theorem axisInteriorLine_of_certificatesT {tree : List Nat × List Nat → CTree}
    (h : InteriorCertificatesT tree) :
    ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
      S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
      c ∈ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S :=
  axisInteriorLine_of_axisInteriorY (axisInteriorY_of_unsat (interiorCnf_unsat_of_certificatesT h))

/-- **The mirror class**, from V1-L's 1,198 leaf facts (sub-case (i)) and the certificates
with cube trees (sub-case (ii)). -/
theorem mirrorExclusionLine_of_certificatesT {tree : List Nat × List Nat → CTree}
    (h1 : ∀ c ∈ V1L.hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (h2 : InteriorCertificatesT tree) : MirrorExclusionLine :=
  mirrorExclusionLine_of_unsat (V1L.hullCnf_unsat_of_leaves h1)
    (interiorCnf_unsat_of_certificatesT h2)

end V2L
