import V2L2.Main

/-! Axiom audit: `lake build` fails if any of these theorems uses an axiom other than
`propext`, `Classical.choice` and `Quot.sound` (or uses fewer than recorded here). -/

/-- info: 'V2L2.dimacsSatisfiable_congr' does not depend on any axioms -/
#guard_msgs in
#print axioms V2L2.dimacsSatisfiable_congr

/-- info: 'V2L2.v3LeafCnf_iff' depends on axioms: [propext] -/
#guard_msgs in
#print axioms V2L2.v3LeafCnf_iff

/-- info: 'V2L2.not_dimacsSatisfiable_of_units' depends on axioms: [propext] -/
#guard_msgs in
#print axioms V2L2.not_dimacsSatisfiable_of_units

/-- info: 'V2L2.not_dimacsSatisfiable_of_neg_mem' depends on axioms: [propext] -/
#guard_msgs in
#print axioms V2L2.not_dimacsSatisfiable_of_neg_mem

/-- info: 'V2L2.mirrorExclusionLine_v3' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V2L2.mirrorExclusionLine_v3
