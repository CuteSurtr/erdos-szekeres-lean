import D3Encoding.Targets

/-! Axiom audit: `lake build` fails if any of these uses an axiom other than `propext`,
`Classical.choice` and `Quot.sound` (e.g. `sorryAx`, `Lean.ofReduceBool`, or a new axiom). -/

/-- info: 'D3.triples_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.triples_spec

/-- info: 'D3.lit_spec' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.lit_spec

/-- info: 'D3.canon_canon' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.canon_canon

/-- info: 'D3.convAll_of_pattern' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.convAll_of_pattern

/-- info: 'D3.d3Cnf_sat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.d3Cnf_sat

/-- info: 'D3.groupClosed_11' does not depend on any axioms -/
#guard_msgs in #print axioms D3.groupClosed_11

/-- info: 'D3.LabelledD3.chirotope' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.LabelledD3.chirotope

/-- info: 'D3.LabelledD3.hasConvexNGon_of_convAll' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.LabelledD3.hasConvexNGon_of_convAll

/-- info: 'D3.dimacsSatisfiable_of_labelled' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.dimacsSatisfiable_of_labelled

/-- info: 'D3.hasConvexNGon_of_unsat_d3' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.hasConvexNGon_of_unsat_d3

/-- info: 'D3.d3Exclusion_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms D3.d3Exclusion_of_unsat
