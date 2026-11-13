import ETVEncoding.Main
import ETVEncoding.Xsb
import ETVEncoding.Shear
import ETVEncoding.Hull
import ETVEncoding.EndToEnd

/-! Axiom audit: `lake build` fails if any of these theorems uses an axiom other than
`propext`, `Classical.choice` and `Quot.sound` (in particular `sorryAx`,
`Lean.ofReduceBool` from `native_decide`, or a new axiom). -/

/-- info: 'ETV.etvClauses_sound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms ETV.etvClauses_sound

/--
info: 'ETV.dimacsSatisfiable_of_signotope' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.dimacsSatisfiable_of_signotope

/-- info: 'ETV.signotope_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms ETV.signotope_of_unsat

/-- info: 'ETV.isSignotope_sigOf' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms ETV.isSignotope_sigOf

/-- info: 'ETV.HasGon.vertices' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms ETV.HasGon.vertices

/--
info: 'ETV.hasConvexNGon_of_hasGon' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.hasConvexNGon_of_hasGon

/--
info: 'ETV.hasChainPts_of_hasChain' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.hasChainPts_of_hasChain

/--
info: 'ETV.dimacsSatisfiable_of_xsorted' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.dimacsSatisfiable_of_xsorted

/-- info: 'ETV.exists_xsorted' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms ETV.exists_xsorted

/--
info: 'ETV.dimacsSatisfiable_of_pointSet' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.dimacsSatisfiable_of_pointSet

/--
info: 'ETV.cap_cup_or_gon_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.cap_cup_or_gon_of_unsat

/--
info: 'ETV.hasConvexNGon_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.hasConvexNGon_of_unsat

/-- info: 'ETV.xsbSound' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms ETV.xsbSound

/--
info: 'ETV.cap_cup_or_gon_of_unsat_xsb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.cap_cup_or_gon_of_unsat_xsb

/-- info: 'ETV.distinctXReduction' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms ETV.distinctXReduction

/--
info: 'ETV.forcesConvexNGon_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.forcesConvexNGon_of_unsat

/--
info: 'ETV.heptagonConjecture_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.heptagonConjecture_of_unsat

/--
info: 'ETV.dimacsB_satisfiable_of_signotope' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.dimacsB_satisfiable_of_signotope

/--
info: 'ETV.forcesConvexNGon_of_unsat_trackB' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.forcesConvexNGon_of_unsat_trackB

/--
info: 'ETV.forcesConvexNGon_of_unsat_hull' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.forcesConvexNGon_of_unsat_hull

/--
info: 'ETV.heptagonConjecture_of_unsat_n33k7hm' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.heptagonConjecture_of_unsat_n33k7hm

/--
info: 'ETV.Rup.not_dimacsSatisfiable_of_run' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.Rup.not_dimacsSatisfiable_of_run

/-- info: 'ETV.forces_quadrilateral_5' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms ETV.forces_quadrilateral_5

/--
info: 'ETV.forces_quadrilateral_5_hm' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in #print axioms ETV.forces_quadrilateral_5_hm
