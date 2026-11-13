import V2L.TreeMain
import V2L.Trees.Checks

/-!
# Sub-case (ii) and the mirror class, with the final cube trees

`treeOf` (generated, `V2L/Trees/`) gives every case its cube tree from the wave runs, and
`treeOf_check` (kernel-checked, one `decide +kernel` per sibling list) proves that every tree
passes `CTree.check`. So only the cake_lpr facts remain as hypotheses.
-/

namespace V2L

open ETV ErdosSzekeres Mir

/-- **Sub-case (ii), any mirror line**, from the 122 cover-obligation facts and the facts of
the tree leaves of the 450 cases. -/
theorem axisInteriorLine_final (hroot : RootCertificate) (hup : UpCertificates)
    (hleaves : ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves,
      ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)) :
    ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
      S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
      c ∈ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S :=
  axisInteriorLine_of_certificatesT ⟨hroot, hup, fun p hp => ⟨treeOf_check p hp, hleaves p hp⟩⟩

/-- **The mirror class**, from V1-L's 1,198 leaf facts (sub-case (i)), the 122 cover-obligation
facts and the facts of the tree leaves of the 450 cases (sub-case (ii)). -/
theorem mirrorExclusionLine_final
    (h1 : ∀ c ∈ V1L.hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (hroot : RootCertificate) (hup : UpCertificates)
    (hleaves : ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves,
      ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)) :
    MirrorExclusionLine :=
  mirrorExclusionLine_of_certificatesT h1 ⟨hroot, hup, fun p hp => ⟨treeOf_check p hp, hleaves p hp⟩⟩

end V2L
