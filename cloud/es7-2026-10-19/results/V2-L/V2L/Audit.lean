import V2L.Main
import V2L.FinalTree

/-! Axiom audit: `lake build` fails if any of these theorems uses an axiom other than
`propext`, `Classical.choice` and `Quot.sound` (or uses fewer than recorded here). -/

/-- info: 'V2L.upSets_eq' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.upSets_eq

/-- info: 'V2L.caseSpecs_eq' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.caseSpecs_eq

/-- info: 'V2L.upSets_length' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.upSets_length

/-- info: 'V2L.upCubes_length' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.upCubes_length

/-- info: 'V2L.caseSpecs_length' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.caseSpecs_length

/-- info: 'V2L.caseCubes_length' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.caseCubes_length

/-- info: 'V2L.upSets_nodup' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.upSets_nodup

/-- info: 'V2L.caseSpecs_upper_mem' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms V2L.caseSpecs_upper_mem

/-- info: 'V2L.casesOf_length_sum' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.casesOf_length_sum

/-- info: 'V2L.upCubes_nonzero' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.upCubes_nonzero

/-- info: 'V2L.caseCubes_nonzero' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.caseCubes_nonzero

/-- info: 'V2L.upTable_snd' depends on axioms: [propext] -/
#guard_msgs in
#print axioms V2L.upTable_snd

/-- info: 'V2L.caseTable_snd' depends on axioms: [propext] -/
#guard_msgs in
#print axioms V2L.caseTable_snd

/-- info: 'V2L.casesOf_nonzero' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms V2L.casesOf_nonzero

/-- info: 'V2L.upTable_nonzero' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms V2L.upTable_nonzero

/-- info: 'V2L.withUnits_eq' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.withUnits_eq

/-- info: 'V2L.exists_cubeSat_of_block' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.exists_cubeSat_of_block

/-- info: 'V2L.not_dimacsSatisfiable_of_clauseCover' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.not_dimacsSatisfiable_of_clauseCover

/-- info: 'V2L.not_dimacsSatisfiable_of_clauseCover₂' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.not_dimacsSatisfiable_of_clauseCover₂

/-- info: 'V2L.not_dimacsSatisfiable_of_clauseCover₂'' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.not_dimacsSatisfiable_of_clauseCover₂'

/-- info: 'V2L.not_dimacsSatisfiable_case_of_leaves' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.not_dimacsSatisfiable_case_of_leaves

/-- info: 'V2L.not_dimacsSatisfiable_of_clauseCover_leaves' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.not_dimacsSatisfiable_of_clauseCover_leaves

/-- info: 'V2L.not_dimacsSatisfiable_of_clauseCover₂_leaves' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.not_dimacsSatisfiable_of_clauseCover₂_leaves

/-- info: 'V2L.rootCnf_eq' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms V2L.rootCnf_eq

/-- info: 'V2L.upCnf_eq' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms V2L.upCnf_eq

/-- info: 'V2L.caseCnf_eq' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms V2L.caseCnf_eq

/-- info: 'V2L.interiorCertificates_of_cover' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms V2L.interiorCertificates_of_cover

/-- info: 'V2L.interiorCnf_unsat_of_certificates' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.interiorCnf_unsat_of_certificates

/-- info: 'V2L.axisInteriorY_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.axisInteriorY_of_unsat

/-- info: 'V2L.axisInteriorLine_of_axisInteriorY' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.axisInteriorLine_of_axisInteriorY

/-- info: 'V2L.axisInteriorLine_of_certificates' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.axisInteriorLine_of_certificates

/-- info: 'V2L.mirrorExclusionLine_of_certificates' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.mirrorExclusionLine_of_certificates

-- Tree certificates (TREE_TASK.md, V2G)

/-- info: 'V2L.CTree.covers_of_check' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.CTree.covers_of_check

/-- info: 'V2L.CTree.check_of_sibLists' depends on axioms: [propext] -/
#guard_msgs in
#print axioms V2L.CTree.check_of_sibLists

/-- info: 'V2L.not_dimacsSatisfiable_of_tree' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.not_dimacsSatisfiable_of_tree

/-- info: 'V2L.Trees.check001' depends on axioms: [propext] -/
#guard_msgs in
#print axioms V2L.Trees.check001

/-- info: 'V2L.Trees.c001_0' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L.Trees.c001_0

/-- info: 'V2L.treeOf_check' depends on axioms: [propext] -/
#guard_msgs in
#print axioms V2L.treeOf_check

/-- info: 'V2L.interiorCnf_unsat_of_certificatesT' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.interiorCnf_unsat_of_certificatesT

/-- info: 'V2L.axisInteriorLine_of_certificatesT' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.axisInteriorLine_of_certificatesT

/-- info: 'V2L.mirrorExclusionLine_of_certificatesT' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.mirrorExclusionLine_of_certificatesT

/-- info: 'V2L.axisInteriorLine_final' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.axisInteriorLine_final

/-- info: 'V2L.mirrorExclusionLine_final' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L.mirrorExclusionLine_final
