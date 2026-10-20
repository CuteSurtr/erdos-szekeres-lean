import V1L.Main

/-! Axiom audit: `lake build` fails if any of these theorems uses an axiom other than
`propext`, `Classical.choice` and `Quot.sound` (or uses fewer than recorded here). -/

/-- info: 'V1L.hullLeaves_coverCheck' does not depend on any axioms -/
#guard_msgs in
#print axioms V1L.hullLeaves_coverCheck

/-- info: 'V1L.hullLeaves_length' does not depend on any axioms -/
#guard_msgs in
#print axioms V1L.hullLeaves_length

/-- info: 'V1L.hullCnf_unsat_of_leaves' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V1L.hullCnf_unsat_of_leaves

/-- info: 'V1L.hullVertexY_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V1L.hullVertexY_of_unsat

/-- info: 'V1L.hasConvexNGon_of_image_affine' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V1L.hasConvexNGon_of_image_affine

/-- info: 'V1L.hullVertexLine_of_hullVertexY' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V1L.hullVertexLine_of_hullVertexY

/-- info: 'V1L.hullVertexY_of_leaves' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V1L.hullVertexY_of_leaves

/-- info: 'V1L.hullVertexLine_of_leaves' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms V1L.hullVertexLine_of_leaves
