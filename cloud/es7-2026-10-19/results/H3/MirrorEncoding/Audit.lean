import MirrorEncoding.Targets

/-! Axiom audit: `lake build` fails if any of these theorems uses an axiom other than
 `propext`, `Classical.choice` and `Quot.sound` (or uses fewer than recorded here). -/

/-- info: 'Mir.dimacsSat_mirgen' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms Mir.dimacsSat_mirgen

/-- info: 'Mir.hullCnf_satisfiable' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.hullCnf_satisfiable

/-- info: 'Mir.interiorCnf_satisfiable' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.interiorCnf_satisfiable

/-- info: 'Mir.exists_hullFrame_at' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.exists_hullFrame_at

/-- info: 'Mir.HullFrame.eq_of_ptSet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.HullFrame.eq_of_ptSet

/-- info: 'Mir.hullCnf_satisfiable_of_frame' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.hullCnf_satisfiable_of_frame

/-- info: 'Mir.extreme_axis_split' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.extreme_axis_split

/-- info: 'Mir.hullCnf_satisfiable_of_mirrorSet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.hullCnf_satisfiable_of_mirrorSet

/-- info: 'Mir.hasConvexNGon_of_unsat_hull' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.hasConvexNGon_of_unsat_hull

/-- info: 'Mir.XSorted.eq_of_ptSet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.XSorted.eq_of_ptSet

/-- info: 'Mir.axis_above_below' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.axis_above_below

/-- info: 'Mir.exists_mirror_xsorted' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.exists_mirror_xsorted

/-- info: 'Mir.interior_signotope_of_enum' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.interior_signotope_of_enum

/-- info: 'Mir.interiorCnf_satisfiable_of_distinctX' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.interiorCnf_satisfiable_of_distinctX

/-- info: 'Mir.exists_eps' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.exists_eps

/-- info: 'Mir.interiorTieBreak' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.interiorTieBreak

/-- info: 'Mir.interiorTieBreak_holds' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.interiorTieBreak_holds

/-- info: 'Mir.hasConvexNGon_of_unsat_interior' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.hasConvexNGon_of_unsat_interior

/-- info: 'Mir.mirrorExclusion_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.mirrorExclusion_of_unsat

/-- info: 'Mir.mirrorExclusion_of_cubes' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.mirrorExclusion_of_cubes

/-- info: 'Mir.exists_mirrorSet' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.exists_mirrorSet

/-- info: 'Mir.mirrorExclusionY_of_mirrorExclusion' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.mirrorExclusionY_of_mirrorExclusion

/-- info: 'Mir.covers_of_coverCheck' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.covers_of_coverCheck

/-- info: 'Mir.not_dimacsSatisfiable_of_cover' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms Mir.not_dimacsSatisfiable_of_cover

/-- info: 'Mir.not_dimacsSatisfiable_of_coverCheck' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms Mir.not_dimacsSatisfiable_of_coverCheck
