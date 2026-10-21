import V2L2.Defs
import V2L.FinalTree

/-!
# The mirror class from the leaf files that cake_lpr checked

`mirrorExclusionLine_v3` is `V2L.mirrorExclusionLine_final` with the tree-leaf hypothesis
stated on `v3LeafCnf`, the clause lists of the files written by `v3_check.py`, and only for
the leaves that contain no negation of a case-cube literal (the others are unsatisfiable by
`not_dimacsSatisfiable_of_neg_mem`, as V3 recorded without a solver call).
-/

namespace V2L2

open ETV ErdosSzekeres Mir V2L

/-- The tree-leaf facts in the form of V2-L follow from the V3 facts. -/
theorem hleaves_of_v3
    (hv3 : ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves, (∀ x ∈ l, -x ∉ p.2) →
      ¬DimacsSatisfiable (v3LeafCnf (interiorCnf 33 7) p.2 l)) :
    ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves,
      ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l) := by
  intro p hp l hl
  by_cases h : ∀ x ∈ l, -x ∉ p.2
  · rw [← v3LeafCnf_iff]
    exact hv3 p hp l hl h
  · simp only [not_forall, not_not] at h
    obtain ⟨x, hx, hnx⟩ := h
    have hc : p.2 ∈ caseCubes := (List.of_mem_zip hp).2
    exact not_dimacsSatisfiable_of_neg_mem hx hnx (caseCubes_nonzero _ hc _ hnx)

/-- **The mirror class**, from V1-L's 1,198 leaf facts (sub-case (i)), the 122 cover-obligation
facts and, for the tree leaves of the 450 cases that do not contradict their case cube, the
facts about the exact clause lists that `v3_check.py` gave cake_lpr. -/
theorem mirrorExclusionLine_v3
    (h1 : ∀ c ∈ V1L.hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (hroot : RootCertificate) (hup : UpCertificates)
    (hleaves : ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves, (∀ x ∈ l, -x ∉ p.2) →
      ¬DimacsSatisfiable (v3LeafCnf (interiorCnf 33 7) p.2 l)) :
    MirrorExclusionLine :=
  mirrorExclusionLine_final h1 hroot hup (hleaves_of_v3 hleaves)

end V2L2
