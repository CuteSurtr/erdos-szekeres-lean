/-! Fixed 15-variable Boolean refutation. Generated ordinary proof terms.
Original DIMACS SHA-256: 7d18c713d190d893a4d3d7873e8caa7d45061326c403ee8133888382040cc22a.
The source is a candidate until a bounded Lean check and axiom audit pass.
No geometric claim is encoded here. -/

set_option maxRecDepth 4096

namespace Delta3.Terminal15Boolean

/-- The 313 original clauses, in exact DIMACS row order. -/
def terminalFormula (p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 : Prop) : Prop :=
  (¬p1 ∨ ¬p2 ∨ ¬p7 ∨ ¬p8) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p9 ∨ ¬p12) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p7 ∨ ¬p8) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p9 ∨ ¬p12) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p7 ∨ ¬p8) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p9 ∨ ¬p12) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p7 ∨ ¬p8) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p9 ∨ ¬p12) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p7 ∨ ¬p8) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p9 ∨ ¬p12) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p11 ∨ ¬p12) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p11 ∨ ¬p13) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p11 ∨ ¬p14) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p7 ∨ ¬p8) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p9 ∨ ¬p12) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p11 ∨ ¬p12) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p11 ∨ ¬p13) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p11 ∨ ¬p14) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p7 ∨ ¬p8) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p9 ∨ ¬p12) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p11 ∨ ¬p12) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p11 ∨ ¬p13) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p11 ∨ ¬p14) ∧
  (¬p5 ∨ ¬p8 ∨ ¬p13 ∨ ¬p14) ∧
  (¬p5 ∨ ¬p12 ∨ ¬p13 ∨ ¬p14) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p10 ∨ ¬p13) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p10 ∨ ¬p14) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p11 ∨ ¬p12) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p11 ∨ ¬p13) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p11 ∨ ¬p14) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p10 ∨ ¬p13) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p10 ∨ ¬p14) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p11 ∨ ¬p12) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p11 ∨ ¬p13) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p11 ∨ ¬p14) ∧
  (¬p8 ∨ ¬p10 ∨ ¬p11 ∨ ¬p12) ∧
  (¬p8 ∨ ¬p10 ∨ ¬p11 ∨ ¬p13) ∧
  (¬p8 ∨ ¬p10 ∨ ¬p11 ∨ ¬p14) ∧
  (¬p8 ∨ ¬p10 ∨ ¬p11 ∨ ¬p15) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p3) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p4) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p5) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p7) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p8) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p9) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p10) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p12) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p13) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p8) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p9) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p10) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p12) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p13) ∧
  (¬p1 ∨ ¬p6 ∨ ¬p14) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p8) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p9) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p10) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p12) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p13) ∧
  (¬p2 ∨ ¬p6 ∨ ¬p14) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p5) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p7) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p8) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p9) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p10) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p12) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p13) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p14) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p8) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p9) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p10) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p11) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p12) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p13) ∧
  (¬p3 ∨ ¬p6 ∨ ¬p14) ∧
  (¬p3 ∨ ¬p7 ∨ ¬p12) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p8) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p9) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p10) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p11) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p12) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p13) ∧
  (¬p4 ∨ ¬p6 ∨ ¬p14) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p8) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p9) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p10) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p11) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p12) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p13) ∧
  (¬p5 ∨ ¬p6 ∨ ¬p14) ∧
  (¬p5 ∨ ¬p7 ∨ ¬p12) ∧
  (¬p5 ∨ ¬p7 ∨ ¬p13) ∧
  (¬p5 ∨ ¬p7 ∨ ¬p14) ∧
  (¬p5 ∨ ¬p8 ∨ ¬p12) ∧
  (¬p5 ∨ ¬p8 ∨ ¬p13) ∧
  (¬p5 ∨ ¬p8 ∨ ¬p14) ∧
  (¬p5 ∨ ¬p9 ∨ ¬p13) ∧
  (¬p5 ∨ ¬p9 ∨ ¬p14) ∧
  (¬p5 ∨ ¬p12 ∨ ¬p13) ∧
  (¬p5 ∨ ¬p12 ∨ ¬p14) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p10) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p11) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p13) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p14) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p15) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p10) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p11) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p13) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p14) ∧
  (¬p8 ∨ ¬p9 ∨ ¬p15) ∧
  (¬p8 ∨ ¬p10 ∨ ¬p11) ∧
  (¬p8 ∨ ¬p10 ∨ ¬p15) ∧
  (p1 ∨ p2 ∨ p3 ∨ p5 ∨ p7 ∨ p8) ∧
  (p1 ∨ p2 ∨ p4 ∨ p5 ∨ p7 ∨ p8) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p7 ∨ p8) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p7 ∨ p8) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p7 ∨ p8) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p7 ∨ p8) ∧
  (p1 ∨ p2 ∨ p3 ∨ p5 ∨ p7 ∨ p9) ∧
  (p1 ∨ p2 ∨ p4 ∨ p5 ∨ p7 ∨ p9) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p7 ∨ p9) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p7 ∨ p9) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p7 ∨ p9) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p7 ∨ p9) ∧
  (p1 ∨ p2 ∨ p3 ∨ p5 ∨ p8 ∨ p9) ∧
  (p1 ∨ p2 ∨ p4 ∨ p5 ∨ p8 ∨ p9) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p8 ∨ p9) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p8 ∨ p9) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p8 ∨ p9) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p8 ∨ p9) ∧
  (p1 ∨ p2 ∨ p3 ∨ p5 ∨ p7 ∨ p10) ∧
  (p1 ∨ p2 ∨ p4 ∨ p5 ∨ p7 ∨ p10) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p7 ∨ p10) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p7 ∨ p10) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p7 ∨ p10) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p7 ∨ p10) ∧
  (p1 ∨ p2 ∨ p3 ∨ p5 ∨ p8 ∨ p10) ∧
  (p1 ∨ p2 ∨ p4 ∨ p5 ∨ p8 ∨ p10) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p8 ∨ p10) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p8 ∨ p10) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p8 ∨ p10) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p8 ∨ p10) ∧
  (p1 ∨ p2 ∨ p3 ∨ p5 ∨ p9 ∨ p10) ∧
  (p1 ∨ p2 ∨ p4 ∨ p5 ∨ p9 ∨ p10) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p9 ∨ p10) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p9 ∨ p10) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p9 ∨ p10) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p9 ∨ p10) ∧
  (p1 ∨ p3 ∨ p5 ∨ p7 ∨ p10 ∨ p11) ∧
  (p2 ∨ p3 ∨ p5 ∨ p7 ∨ p10 ∨ p11) ∧
  (p1 ∨ p4 ∨ p5 ∨ p7 ∨ p10 ∨ p11) ∧
  (p2 ∨ p4 ∨ p5 ∨ p7 ∨ p10 ∨ p11) ∧
  (p3 ∨ p5 ∨ p6 ∨ p7 ∨ p10 ∨ p11) ∧
  (p4 ∨ p5 ∨ p6 ∨ p7 ∨ p10 ∨ p11) ∧
  (p1 ∨ p3 ∨ p5 ∨ p9 ∨ p10 ∨ p11) ∧
  (p2 ∨ p3 ∨ p5 ∨ p9 ∨ p10 ∨ p11) ∧
  (p1 ∨ p4 ∨ p5 ∨ p9 ∨ p10 ∨ p11) ∧
  (p2 ∨ p4 ∨ p5 ∨ p9 ∨ p10 ∨ p11) ∧
  (p3 ∨ p5 ∨ p6 ∨ p9 ∨ p10 ∨ p11) ∧
  (p4 ∨ p5 ∨ p6 ∨ p9 ∨ p10 ∨ p11) ∧
  (p1 ∨ p2 ∨ p3 ∨ p5 ∨ p9 ∨ p12) ∧
  (p1 ∨ p2 ∨ p4 ∨ p5 ∨ p9 ∨ p12) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p9 ∨ p12) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p9 ∨ p12) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p9 ∨ p12) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p9 ∨ p12) ∧
  (p1 ∨ p2 ∨ p4 ∨ p7 ∨ p9 ∨ p12) ∧
  (p1 ∨ p4 ∨ p6 ∨ p7 ∨ p9 ∨ p12) ∧
  (p2 ∨ p4 ∨ p6 ∨ p7 ∨ p9 ∨ p12) ∧
  (p1 ∨ p2 ∨ p3 ∨ p8 ∨ p9 ∨ p12) ∧
  (p1 ∨ p2 ∨ p4 ∨ p8 ∨ p9 ∨ p12) ∧
  (p1 ∨ p3 ∨ p6 ∨ p8 ∨ p9 ∨ p12) ∧
  (p2 ∨ p3 ∨ p6 ∨ p8 ∨ p9 ∨ p12) ∧
  (p1 ∨ p4 ∨ p6 ∨ p8 ∨ p9 ∨ p12) ∧
  (p2 ∨ p4 ∨ p6 ∨ p8 ∨ p9 ∨ p12) ∧
  (p1 ∨ p2 ∨ p3 ∨ p5 ∨ p10 ∨ p12) ∧
  (p1 ∨ p2 ∨ p4 ∨ p5 ∨ p10 ∨ p12) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p10 ∨ p12) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p10 ∨ p12) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p10 ∨ p12) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p10 ∨ p12) ∧
  (p1 ∨ p2 ∨ p4 ∨ p7 ∨ p10 ∨ p12) ∧
  (p1 ∨ p4 ∨ p6 ∨ p7 ∨ p10 ∨ p12) ∧
  (p2 ∨ p4 ∨ p6 ∨ p7 ∨ p10 ∨ p12) ∧
  (p1 ∨ p2 ∨ p3 ∨ p8 ∨ p10 ∨ p12) ∧
  (p1 ∨ p2 ∨ p4 ∨ p8 ∨ p10 ∨ p12) ∧
  (p1 ∨ p3 ∨ p6 ∨ p8 ∨ p10 ∨ p12) ∧
  (p2 ∨ p3 ∨ p6 ∨ p8 ∨ p10 ∨ p12) ∧
  (p1 ∨ p4 ∨ p6 ∨ p8 ∨ p10 ∨ p12) ∧
  (p2 ∨ p4 ∨ p6 ∨ p8 ∨ p10 ∨ p12) ∧
  (p1 ∨ p2 ∨ p4 ∨ p7 ∨ p12 ∨ p13) ∧
  (p1 ∨ p4 ∨ p6 ∨ p7 ∨ p12 ∨ p13) ∧
  (p2 ∨ p4 ∨ p6 ∨ p7 ∨ p12 ∨ p13) ∧
  (p1 ∨ p2 ∨ p3 ∨ p8 ∨ p12 ∨ p13) ∧
  (p1 ∨ p2 ∨ p4 ∨ p8 ∨ p12 ∨ p13) ∧
  (p1 ∨ p3 ∨ p6 ∨ p8 ∨ p12 ∨ p13) ∧
  (p2 ∨ p3 ∨ p6 ∨ p8 ∨ p12 ∨ p13) ∧
  (p1 ∨ p4 ∨ p6 ∨ p8 ∨ p12 ∨ p13) ∧
  (p2 ∨ p4 ∨ p6 ∨ p8 ∨ p12 ∨ p13) ∧
  (p7 ∨ p8 ∨ p9 ∨ p10 ∨ p12 ∨ p13) ∧
  (p1 ∨ p4 ∨ p7 ∨ p11 ∨ p12 ∨ p13) ∧
  (p2 ∨ p4 ∨ p7 ∨ p11 ∨ p12 ∨ p13) ∧
  (p4 ∨ p6 ∨ p7 ∨ p11 ∨ p12 ∨ p13) ∧
  (p1 ∨ p3 ∨ p8 ∨ p11 ∨ p12 ∨ p13) ∧
  (p2 ∨ p3 ∨ p8 ∨ p11 ∨ p12 ∨ p13) ∧
  (p1 ∨ p4 ∨ p8 ∨ p11 ∨ p12 ∨ p13) ∧
  (p2 ∨ p4 ∨ p8 ∨ p11 ∨ p12 ∨ p13) ∧
  (p3 ∨ p6 ∨ p8 ∨ p11 ∨ p12 ∨ p13) ∧
  (p4 ∨ p6 ∨ p8 ∨ p11 ∨ p12 ∨ p13) ∧
  (p7 ∨ p8 ∨ p9 ∨ p11 ∨ p12 ∨ p13) ∧
  (p1 ∨ p4 ∨ p6 ∨ p7 ∨ p12 ∨ p14) ∧
  (p2 ∨ p4 ∨ p6 ∨ p7 ∨ p12 ∨ p14) ∧
  (p1 ∨ p3 ∨ p6 ∨ p8 ∨ p12 ∨ p14) ∧
  (p2 ∨ p3 ∨ p6 ∨ p8 ∨ p12 ∨ p14) ∧
  (p1 ∨ p4 ∨ p6 ∨ p8 ∨ p12 ∨ p14) ∧
  (p2 ∨ p4 ∨ p6 ∨ p8 ∨ p12 ∨ p14) ∧
  (p7 ∨ p8 ∨ p9 ∨ p10 ∨ p12 ∨ p14) ∧
  (p1 ∨ p4 ∨ p7 ∨ p11 ∨ p12 ∨ p14) ∧
  (p2 ∨ p4 ∨ p7 ∨ p11 ∨ p12 ∨ p14) ∧
  (p4 ∨ p6 ∨ p7 ∨ p11 ∨ p12 ∨ p14) ∧
  (p1 ∨ p3 ∨ p8 ∨ p11 ∨ p12 ∨ p14) ∧
  (p2 ∨ p3 ∨ p8 ∨ p11 ∨ p12 ∨ p14) ∧
  (p1 ∨ p4 ∨ p8 ∨ p11 ∨ p12 ∨ p14) ∧
  (p2 ∨ p4 ∨ p8 ∨ p11 ∨ p12 ∨ p14) ∧
  (p3 ∨ p6 ∨ p8 ∨ p11 ∨ p12 ∨ p14) ∧
  (p4 ∨ p6 ∨ p8 ∨ p11 ∨ p12 ∨ p14) ∧
  (p7 ∨ p8 ∨ p9 ∨ p11 ∨ p12 ∨ p14) ∧
  (p1 ∨ p3 ∨ p6 ∨ p7 ∨ p13 ∨ p14) ∧
  (p2 ∨ p3 ∨ p6 ∨ p7 ∨ p13 ∨ p14) ∧
  (p1 ∨ p4 ∨ p6 ∨ p7 ∨ p13 ∨ p14) ∧
  (p2 ∨ p4 ∨ p6 ∨ p7 ∨ p13 ∨ p14) ∧
  (p1 ∨ p3 ∨ p6 ∨ p9 ∨ p13 ∨ p14) ∧
  (p2 ∨ p3 ∨ p6 ∨ p9 ∨ p13 ∨ p14) ∧
  (p1 ∨ p4 ∨ p6 ∨ p9 ∨ p13 ∨ p14) ∧
  (p2 ∨ p4 ∨ p6 ∨ p9 ∨ p13 ∨ p14) ∧
  (p1 ∨ p3 ∨ p6 ∨ p10 ∨ p13 ∨ p14) ∧
  (p2 ∨ p3 ∨ p6 ∨ p10 ∨ p13 ∨ p14) ∧
  (p1 ∨ p4 ∨ p6 ∨ p10 ∨ p13 ∨ p14) ∧
  (p2 ∨ p4 ∨ p6 ∨ p10 ∨ p13 ∨ p14) ∧
  (p1 ∨ p3 ∨ p7 ∨ p11 ∨ p13 ∨ p14) ∧
  (p2 ∨ p3 ∨ p7 ∨ p11 ∨ p13 ∨ p14) ∧
  (p1 ∨ p4 ∨ p7 ∨ p11 ∨ p13 ∨ p14) ∧
  (p2 ∨ p4 ∨ p7 ∨ p11 ∨ p13 ∨ p14) ∧
  (p3 ∨ p6 ∨ p7 ∨ p11 ∨ p13 ∨ p14) ∧
  (p4 ∨ p6 ∨ p7 ∨ p11 ∨ p13 ∨ p14) ∧
  (p1 ∨ p3 ∨ p9 ∨ p11 ∨ p13 ∨ p14) ∧
  (p2 ∨ p3 ∨ p9 ∨ p11 ∨ p13 ∨ p14) ∧
  (p1 ∨ p4 ∨ p9 ∨ p11 ∨ p13 ∨ p14) ∧
  (p2 ∨ p4 ∨ p9 ∨ p11 ∨ p13 ∨ p14) ∧
  (p3 ∨ p6 ∨ p9 ∨ p11 ∨ p13 ∨ p14) ∧
  (p4 ∨ p6 ∨ p9 ∨ p11 ∨ p13 ∨ p14) ∧
  (p1 ∨ p3 ∨ p10 ∨ p11 ∨ p13 ∨ p14) ∧
  (p2 ∨ p3 ∨ p10 ∨ p11 ∨ p13 ∨ p14) ∧
  (p1 ∨ p4 ∨ p10 ∨ p11 ∨ p13 ∨ p14) ∧
  (p2 ∨ p4 ∨ p10 ∨ p11 ∨ p13 ∨ p14) ∧
  (p3 ∨ p6 ∨ p10 ∨ p11 ∨ p13 ∨ p14) ∧
  (p4 ∨ p6 ∨ p10 ∨ p11 ∨ p13 ∨ p14) ∧
  (p1 ∨ p3 ∨ p5 ∨ p7 ∨ p10 ∨ p15) ∧
  (p2 ∨ p3 ∨ p5 ∨ p7 ∨ p10 ∨ p15) ∧
  (p1 ∨ p4 ∨ p5 ∨ p7 ∨ p10 ∨ p15) ∧
  (p2 ∨ p4 ∨ p5 ∨ p7 ∨ p10 ∨ p15) ∧
  (p1 ∨ p3 ∨ p5 ∨ p9 ∨ p10 ∨ p15) ∧
  (p2 ∨ p3 ∨ p5 ∨ p9 ∨ p10 ∨ p15) ∧
  (p1 ∨ p4 ∨ p5 ∨ p9 ∨ p10 ∨ p15) ∧
  (p2 ∨ p4 ∨ p5 ∨ p9 ∨ p10 ∨ p15) ∧
  (p1 ∨ p3 ∨ p5 ∨ p9 ∨ p11 ∨ p15) ∧
  (p2 ∨ p3 ∨ p5 ∨ p9 ∨ p11 ∨ p15) ∧
  (p1 ∨ p4 ∨ p5 ∨ p9 ∨ p11 ∨ p15) ∧
  (p2 ∨ p4 ∨ p5 ∨ p9 ∨ p11 ∨ p15) ∧
  (p1 ∨ p4 ∨ p7 ∨ p12 ∨ p13 ∨ p15) ∧
  (p2 ∨ p4 ∨ p7 ∨ p12 ∨ p13 ∨ p15) ∧
  (p1 ∨ p3 ∨ p8 ∨ p12 ∨ p13 ∨ p15) ∧
  (p2 ∨ p3 ∨ p8 ∨ p12 ∨ p13 ∨ p15) ∧
  (p1 ∨ p4 ∨ p8 ∨ p12 ∨ p13 ∨ p15) ∧
  (p2 ∨ p4 ∨ p8 ∨ p12 ∨ p13 ∨ p15) ∧
  (p7 ∨ p8 ∨ p9 ∨ p12 ∨ p13 ∨ p15) ∧
  (p7 ∨ p8 ∨ p11 ∨ p12 ∨ p13 ∨ p15) ∧
  (p8 ∨ p10 ∨ p11 ∨ p12 ∨ p13 ∨ p15) ∧
  (p1 ∨ p4 ∨ p7 ∨ p12 ∨ p14 ∨ p15) ∧
  (p2 ∨ p4 ∨ p7 ∨ p12 ∨ p14 ∨ p15) ∧
  (p1 ∨ p3 ∨ p8 ∨ p12 ∨ p14 ∨ p15) ∧
  (p2 ∨ p3 ∨ p8 ∨ p12 ∨ p14 ∨ p15) ∧
  (p1 ∨ p4 ∨ p8 ∨ p12 ∨ p14 ∨ p15) ∧
  (p2 ∨ p4 ∨ p8 ∨ p12 ∨ p14 ∨ p15) ∧
  (p7 ∨ p8 ∨ p9 ∨ p12 ∨ p14 ∨ p15) ∧
  (p7 ∨ p8 ∨ p11 ∨ p12 ∨ p14 ∨ p15) ∧
  (p8 ∨ p10 ∨ p11 ∨ p12 ∨ p14 ∨ p15) ∧
  (p1 ∨ p3 ∨ p7 ∨ p13 ∨ p14 ∨ p15) ∧
  (p2 ∨ p3 ∨ p7 ∨ p13 ∨ p14 ∨ p15) ∧
  (p1 ∨ p4 ∨ p7 ∨ p13 ∨ p14 ∨ p15) ∧
  (p2 ∨ p4 ∨ p7 ∨ p13 ∨ p14 ∨ p15) ∧
  (p1 ∨ p3 ∨ p9 ∨ p13 ∨ p14 ∨ p15) ∧
  (p2 ∨ p3 ∨ p9 ∨ p13 ∨ p14 ∨ p15) ∧
  (p1 ∨ p4 ∨ p9 ∨ p13 ∨ p14 ∨ p15) ∧
  (p2 ∨ p4 ∨ p9 ∨ p13 ∨ p14 ∨ p15) ∧
  (p1 ∨ p3 ∨ p10 ∨ p13 ∨ p14 ∨ p15) ∧
  (p2 ∨ p3 ∨ p10 ∨ p13 ∨ p14 ∨ p15) ∧
  (p1 ∨ p4 ∨ p10 ∨ p13 ∨ p14 ∨ p15) ∧
  (p2 ∨ p4 ∨ p10 ∨ p13 ∨ p14 ∨ p15)

/-- Refutation of the supplied 98-clause subset by explicit case analysis. -/
theorem core_unsat (p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 : Prop)
    (c052 : ¬p1 ∨ ¬p2 ∨ ¬p7)
    (c053 : ¬p1 ∨ ¬p2 ∨ ¬p8)
    (c054 : ¬p1 ∨ ¬p2 ∨ ¬p9)
    (c055 : ¬p1 ∨ ¬p2 ∨ ¬p10)
    (c056 : ¬p1 ∨ ¬p2 ∨ ¬p12)
    (c057 : ¬p1 ∨ ¬p2 ∨ ¬p13)
    (c058 : ¬p1 ∨ ¬p6 ∨ ¬p7)
    (c059 : ¬p1 ∨ ¬p6 ∨ ¬p8)
    (c060 : ¬p1 ∨ ¬p6 ∨ ¬p9)
    (c061 : ¬p1 ∨ ¬p6 ∨ ¬p10)
    (c062 : ¬p1 ∨ ¬p6 ∨ ¬p12)
    (c064 : ¬p1 ∨ ¬p6 ∨ ¬p14)
    (c065 : ¬p2 ∨ ¬p6 ∨ ¬p7)
    (c066 : ¬p2 ∨ ¬p6 ∨ ¬p8)
    (c067 : ¬p2 ∨ ¬p6 ∨ ¬p9)
    (c068 : ¬p2 ∨ ¬p6 ∨ ¬p10)
    (c069 : ¬p2 ∨ ¬p6 ∨ ¬p12)
    (c071 : ¬p2 ∨ ¬p6 ∨ ¬p14)
    (c073 : ¬p3 ∨ ¬p4 ∨ ¬p7)
    (c074 : ¬p3 ∨ ¬p4 ∨ ¬p8)
    (c075 : ¬p3 ∨ ¬p4 ∨ ¬p9)
    (c076 : ¬p3 ∨ ¬p4 ∨ ¬p10)
    (c077 : ¬p3 ∨ ¬p4 ∨ ¬p12)
    (c079 : ¬p3 ∨ ¬p4 ∨ ¬p14)
    (c101 : ¬p5 ∨ ¬p6 ∨ ¬p11)
    (c109 : ¬p5 ∨ ¬p8 ∨ ¬p13)
    (c110 : ¬p5 ∨ ¬p8 ∨ ¬p14)
    (c112 : ¬p5 ∨ ¬p9 ∨ ¬p14)
    (c113 : ¬p5 ∨ ¬p12 ∨ ¬p13)
    (c114 : ¬p5 ∨ ¬p12 ∨ ¬p14)
    (c115 : ¬p7 ∨ ¬p9 ∨ ¬p10)
    (c122 : ¬p8 ∨ ¬p9 ∨ ¬p13)
    (c123 : ¬p8 ∨ ¬p9 ∨ ¬p14)
    (c124 : ¬p8 ∨ ¬p9 ∨ ¬p15)
    (c125 : ¬p8 ∨ ¬p10 ∨ ¬p11)
    (c126 : ¬p8 ∨ ¬p10 ∨ ¬p15)
    (c127 : p1 ∨ p2 ∨ p3 ∨ p5 ∨ p7 ∨ p8)
    (c128 : p1 ∨ p2 ∨ p4 ∨ p5 ∨ p7 ∨ p8)
    (c129 : p1 ∨ p3 ∨ p5 ∨ p6 ∨ p7 ∨ p8)
    (c130 : p2 ∨ p3 ∨ p5 ∨ p6 ∨ p7 ∨ p8)
    (c131 : p1 ∨ p4 ∨ p5 ∨ p6 ∨ p7 ∨ p8)
    (c132 : p2 ∨ p4 ∨ p5 ∨ p6 ∨ p7 ∨ p8)
    (c139 : p1 ∨ p2 ∨ p3 ∨ p5 ∨ p8 ∨ p9)
    (c140 : p1 ∨ p2 ∨ p4 ∨ p5 ∨ p8 ∨ p9)
    (c141 : p1 ∨ p3 ∨ p5 ∨ p6 ∨ p8 ∨ p9)
    (c142 : p2 ∨ p3 ∨ p5 ∨ p6 ∨ p8 ∨ p9)
    (c143 : p1 ∨ p4 ∨ p5 ∨ p6 ∨ p8 ∨ p9)
    (c144 : p2 ∨ p4 ∨ p5 ∨ p6 ∨ p8 ∨ p9)
    (c151 : p1 ∨ p2 ∨ p3 ∨ p5 ∨ p8 ∨ p10)
    (c152 : p1 ∨ p2 ∨ p4 ∨ p5 ∨ p8 ∨ p10)
    (c153 : p1 ∨ p3 ∨ p5 ∨ p6 ∨ p8 ∨ p10)
    (c154 : p2 ∨ p3 ∨ p5 ∨ p6 ∨ p8 ∨ p10)
    (c155 : p1 ∨ p4 ∨ p5 ∨ p6 ∨ p8 ∨ p10)
    (c156 : p2 ∨ p4 ∨ p5 ∨ p6 ∨ p8 ∨ p10)
    (c157 : p1 ∨ p2 ∨ p3 ∨ p5 ∨ p9 ∨ p10)
    (c158 : p1 ∨ p2 ∨ p4 ∨ p5 ∨ p9 ∨ p10)
    (c159 : p1 ∨ p3 ∨ p5 ∨ p6 ∨ p9 ∨ p10)
    (c160 : p2 ∨ p3 ∨ p5 ∨ p6 ∨ p9 ∨ p10)
    (c161 : p1 ∨ p4 ∨ p5 ∨ p6 ∨ p9 ∨ p10)
    (c162 : p2 ∨ p4 ∨ p5 ∨ p6 ∨ p9 ∨ p10)
    (c184 : p1 ∨ p2 ∨ p3 ∨ p8 ∨ p9 ∨ p12)
    (c185 : p1 ∨ p2 ∨ p4 ∨ p8 ∨ p9 ∨ p12)
    (c186 : p1 ∨ p3 ∨ p6 ∨ p8 ∨ p9 ∨ p12)
    (c187 : p2 ∨ p3 ∨ p6 ∨ p8 ∨ p9 ∨ p12)
    (c188 : p1 ∨ p4 ∨ p6 ∨ p8 ∨ p9 ∨ p12)
    (c189 : p2 ∨ p4 ∨ p6 ∨ p8 ∨ p9 ∨ p12)
    (c214 : p7 ∨ p8 ∨ p9 ∨ p10 ∨ p12 ∨ p13)
    (c227 : p1 ∨ p3 ∨ p6 ∨ p8 ∨ p12 ∨ p14)
    (c228 : p2 ∨ p3 ∨ p6 ∨ p8 ∨ p12 ∨ p14)
    (c229 : p1 ∨ p4 ∨ p6 ∨ p8 ∨ p12 ∨ p14)
    (c230 : p2 ∨ p4 ∨ p6 ∨ p8 ∨ p12 ∨ p14)
    (c231 : p7 ∨ p8 ∨ p9 ∨ p10 ∨ p12 ∨ p14)
    (c236 : p2 ∨ p3 ∨ p8 ∨ p11 ∨ p12 ∨ p14)
    (c238 : p2 ∨ p4 ∨ p8 ∨ p11 ∨ p12 ∨ p14)
    (c242 : p1 ∨ p3 ∨ p6 ∨ p7 ∨ p13 ∨ p14)
    (c243 : p2 ∨ p3 ∨ p6 ∨ p7 ∨ p13 ∨ p14)
    (c244 : p1 ∨ p4 ∨ p6 ∨ p7 ∨ p13 ∨ p14)
    (c245 : p2 ∨ p4 ∨ p6 ∨ p7 ∨ p13 ∨ p14)
    (c246 : p1 ∨ p3 ∨ p6 ∨ p9 ∨ p13 ∨ p14)
    (c247 : p2 ∨ p3 ∨ p6 ∨ p9 ∨ p13 ∨ p14)
    (c248 : p1 ∨ p4 ∨ p6 ∨ p9 ∨ p13 ∨ p14)
    (c249 : p2 ∨ p4 ∨ p6 ∨ p9 ∨ p13 ∨ p14)
    (c250 : p1 ∨ p3 ∨ p6 ∨ p10 ∨ p13 ∨ p14)
    (c251 : p2 ∨ p3 ∨ p6 ∨ p10 ∨ p13 ∨ p14)
    (c252 : p1 ∨ p4 ∨ p6 ∨ p10 ∨ p13 ∨ p14)
    (c253 : p2 ∨ p4 ∨ p6 ∨ p10 ∨ p13 ∨ p14)
    (c255 : p2 ∨ p3 ∨ p7 ∨ p11 ∨ p13 ∨ p14)
    (c257 : p2 ∨ p4 ∨ p7 ∨ p11 ∨ p13 ∨ p14)
    (c261 : p2 ∨ p3 ∨ p9 ∨ p11 ∨ p13 ∨ p14)
    (c263 : p2 ∨ p4 ∨ p9 ∨ p11 ∨ p13 ∨ p14)
    (c267 : p2 ∨ p3 ∨ p10 ∨ p11 ∨ p13 ∨ p14)
    (c269 : p2 ∨ p4 ∨ p10 ∨ p11 ∨ p13 ∨ p14)
    (c280 : p1 ∨ p3 ∨ p5 ∨ p9 ∨ p11 ∨ p15)
    (c281 : p2 ∨ p3 ∨ p5 ∨ p9 ∨ p11 ∨ p15)
    (c282 : p1 ∨ p4 ∨ p5 ∨ p9 ∨ p11 ∨ p15)
    (c283 : p2 ∨ p4 ∨ p5 ∨ p9 ∨ p11 ∨ p15)
    (c311 : p2 ∨ p3 ∨ p10 ∨ p13 ∨ p14 ∨ p15)
    (c313 : p2 ∨ p4 ∨ p10 ∨ p13 ∨ p14 ∨ p15)
    : False := by
  exact (Classical.em p2).elim
    (fun h2 => by
      exact (Classical.em p1).elim
        (fun h1 => by
          have h7 : ¬p7 := (Or.elim c052 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          have h8 : ¬p8 := (Or.elim c053 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          have h9 : ¬p9 := (Or.elim c054 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          have h10 : ¬p10 := (Or.elim c055 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          have h12 : ¬p12 := (Or.elim c056 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          have h13 : ¬p13 := (Or.elim c057 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          exact (Or.elim c214 (fun x0 => (h7 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h8 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h9 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h12 x4)) (fun r4 => (h13 r4)))))))))))
        )
        (fun h1 => by
          exact (Classical.em p6).elim
            (fun h6 => by
              have h7 : ¬p7 := (Or.elim c065 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h8 : ¬p8 := (Or.elim c066 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h9 : ¬p9 := (Or.elim c067 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h10 : ¬p10 := (Or.elim c068 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h12 : ¬p12 := (Or.elim c069 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h14 : ¬p14 := (Or.elim c071 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h13 : p13 := (Or.elim c214 (fun x0 => (False.elim (h7 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h8 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h9 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h10 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h12 x4))) (fun r4 => r4))))))))))
              exact (Or.elim c231 (fun x0 => (h7 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h8 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h9 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h12 x4)) (fun r4 => (h14 r4)))))))))))
            )
            (fun h6 => by
              exact (Classical.em p3).elim
                (fun h3 => by
                  exact (Classical.em p4).elim
                    (fun h4 => by
                      have h7 : ¬p7 := (Or.elim c073 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h8 : ¬p8 := (Or.elim c074 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h9 : ¬p9 := (Or.elim c075 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h10 : ¬p10 := (Or.elim c076 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h12 : ¬p12 := (Or.elim c077 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h14 : ¬p14 := (Or.elim c079 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h13 : p13 := (Or.elim c214 (fun x0 => (False.elim (h7 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h8 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h9 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h10 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h12 x4))) (fun r4 => r4))))))))))
                      exact (Or.elim c231 (fun x0 => (h7 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h8 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h9 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h12 x4)) (fun r4 => (h14 r4)))))))))))
                    )
                    (fun h4 => by
                      exact (Classical.em p8).elim
                        (fun h8 => by
                          exact (Classical.em p5).elim
                            (fun h5 => by
                              have h13 : ¬p13 := (Or.elim c109 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => r1))))
                              have h14 : ¬p14 := (Or.elim c110 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => r1))))
                              have h7 : p7 := (Or.elim c244 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h9 : p9 := (Or.elim c248 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h10 : p10 := (Or.elim c252 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                            )
                            (fun h5 => by
                              exact (Classical.em p9).elim
                                (fun h9 => by
                                  have h13 : ¬p13 := (Or.elim c122 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                                  have h14 : ¬p14 := (Or.elim c123 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                                  have h15 : ¬p15 := (Or.elim c124 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                                  have h7 : p7 := (Or.elim c244 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                  have h10 : p10 := (Or.elim c252 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                  exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                                )
                                (fun h9 => by
                                  have h10 : p10 := (Or.elim c161 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => r4))))))))))
                                  have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                                  have h15 : ¬p15 := (Or.elim c126 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                                  exact (Or.elim c282 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h5 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h11 x4)) (fun r4 => (h15 r4)))))))))))
                                )
                            )
                        )
                        (fun h8 => by
                          exact (Classical.em p5).elim
                            (fun h5 => by
                              exact (Classical.em p14).elim
                                (fun h14 => by
                                  have h9 : ¬p9 := (Or.elim c112 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                                  have h12 : ¬p12 := (Or.elim c114 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                                  exact (Or.elim c188 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h6 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h8 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h9 x4)) (fun r4 => (h12 r4)))))))))))
                                )
                                (fun h14 => by
                                  have h12 : p12 := (Or.elim c229 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h8 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h14 r4))))))))))))
                                  have h13 : ¬p13 := (Or.elim c113 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h12))) (fun r1 => r1))))
                                  have h7 : p7 := (Or.elim c244 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                  have h9 : p9 := (Or.elim c248 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                  have h10 : p10 := (Or.elim c252 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                  exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                                )
                            )
                            (fun h5 => by
                              have h7 : p7 := (Or.elim c131 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h8 r4))))))))))))
                              have h9 : p9 := (Or.elim c143 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                              have h10 : p10 := (Or.elim c155 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                              exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                            )
                        )
                    )
                )
                (fun h3 => by
                  exact (Classical.em p8).elim
                    (fun h8 => by
                      exact (Classical.em p5).elim
                        (fun h5 => by
                          have h13 : ¬p13 := (Or.elim c109 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => r1))))
                          have h14 : ¬p14 := (Or.elim c110 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => r1))))
                          have h7 : p7 := (Or.elim c242 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h9 : p9 := (Or.elim c246 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h10 : p10 := (Or.elim c250 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                        )
                        (fun h5 => by
                          exact (Classical.em p9).elim
                            (fun h9 => by
                              have h13 : ¬p13 := (Or.elim c122 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              have h14 : ¬p14 := (Or.elim c123 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              have h15 : ¬p15 := (Or.elim c124 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              have h7 : p7 := (Or.elim c242 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h10 : p10 := (Or.elim c250 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                            )
                            (fun h9 => by
                              have h10 : p10 := (Or.elim c159 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => r4))))))))))
                              have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                              have h15 : ¬p15 := (Or.elim c126 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                              exact (Or.elim c280 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h5 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h11 x4)) (fun r4 => (h15 r4)))))))))))
                            )
                        )
                    )
                    (fun h8 => by
                      exact (Classical.em p5).elim
                        (fun h5 => by
                          exact (Classical.em p14).elim
                            (fun h14 => by
                              have h9 : ¬p9 := (Or.elim c112 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                              have h12 : ¬p12 := (Or.elim c114 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                              exact (Or.elim c186 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h6 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h8 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h9 x4)) (fun r4 => (h12 r4)))))))))))
                            )
                            (fun h14 => by
                              have h12 : p12 := (Or.elim c227 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h8 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h13 : ¬p13 := (Or.elim c113 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h12))) (fun r1 => r1))))
                              have h7 : p7 := (Or.elim c242 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h9 : p9 := (Or.elim c246 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h10 : p10 := (Or.elim c250 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                            )
                        )
                        (fun h5 => by
                          have h7 : p7 := (Or.elim c129 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h8 r4))))))))))))
                          have h9 : p9 := (Or.elim c141 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                          have h10 : p10 := (Or.elim c153 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                          exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                        )
                    )
                )
            )
        )
    )
    (fun h2 => by
      exact (Classical.em p6).elim
        (fun h6 => by
          exact (Classical.em p1).elim
            (fun h1 => by
              have h7 : ¬p7 := (Or.elim c058 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h8 : ¬p8 := (Or.elim c059 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h9 : ¬p9 := (Or.elim c060 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h10 : ¬p10 := (Or.elim c061 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h12 : ¬p12 := (Or.elim c062 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h14 : ¬p14 := (Or.elim c064 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
              have h13 : p13 := (Or.elim c214 (fun x0 => (False.elim (h7 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h8 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h9 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h10 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h12 x4))) (fun r4 => r4))))))))))
              exact (Or.elim c231 (fun x0 => (h7 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h8 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h9 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h12 x4)) (fun r4 => (h14 r4)))))))))))
            )
            (fun h1 => by
              exact (Classical.em p5).elim
                (fun h5 => by
                  have h11 : ¬p11 := (Or.elim c101 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h6))) (fun r1 => r1))))
                  exact (Classical.em p8).elim
                    (fun h8 => by
                      have h13 : ¬p13 := (Or.elim c109 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => r1))))
                      have h14 : ¬p14 := (Or.elim c110 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => r1))))
                      exact (Classical.em p3).elim
                        (fun h3 => by
                          have h4 : ¬p4 := (Or.elim c074 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h8))))))
                          have h7 : p7 := (Or.elim c257 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h9 : p9 := (Or.elim c263 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h10 : p10 := (Or.elim c269 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                        )
                        (fun h3 => by
                          have h7 : p7 := (Or.elim c255 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h9 : p9 := (Or.elim c261 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h10 : p10 := (Or.elim c267 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                        )
                    )
                    (fun h8 => by
                      exact (Classical.em p14).elim
                        (fun h14 => by
                          have h9 : ¬p9 := (Or.elim c112 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                          have h12 : ¬p12 := (Or.elim c114 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                          have h3 : p3 := (Or.elim c184 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h8 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => (False.elim (h12 r4))))))))))))
                          have h4 : p4 := (Or.elim c185 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h8 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => (False.elim (h12 r4))))))))))))
                          have h7 : ¬p7 := (Or.elim c073 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                          have h10 : ¬p10 := (Or.elim c076 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                          exact (Or.elim c079 (fun x0 => (x0 h3)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h4)) (fun r1 => (r1 h14)))))
                        )
                        (fun h14 => by
                          exact (Classical.em p13).elim
                            (fun h13 => by
                              have h12 : ¬p12 := (Or.elim c113 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h13))))))
                              have h3 : p3 := (Or.elim c236 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h8 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h12 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h4 : p4 := (Or.elim c238 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h8 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h12 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h7 : ¬p7 := (Or.elim c073 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                              have h9 : ¬p9 := (Or.elim c075 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                              have h10 : ¬p10 := (Or.elim c076 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                              exact (Or.elim c231 (fun x0 => (h7 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h8 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h9 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h12 x4)) (fun r4 => (h14 r4)))))))))))
                            )
                            (fun h13 => by
                              exact (Classical.em p3).elim
                                (fun h3 => by
                                  exact (Classical.em p4).elim
                                    (fun h4 => by
                                      have h7 : ¬p7 := (Or.elim c073 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                                      have h9 : ¬p9 := (Or.elim c075 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                                      have h10 : ¬p10 := (Or.elim c076 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                                      have h12 : ¬p12 := (Or.elim c077 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                                      exact (Or.elim c214 (fun x0 => (h7 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h8 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h9 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h12 x4)) (fun r4 => (h13 r4)))))))))))
                                    )
                                    (fun h4 => by
                                      have h12 : p12 := (Or.elim c238 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h8 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h14 r4))))))))))))
                                      have h7 : p7 := (Or.elim c257 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                      have h9 : p9 := (Or.elim c263 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                      have h10 : p10 := (Or.elim c269 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                      exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                                    )
                                )
                                (fun h3 => by
                                  have h12 : p12 := (Or.elim c236 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h8 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h14 r4))))))))))))
                                  have h7 : p7 := (Or.elim c255 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                  have h9 : p9 := (Or.elim c261 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                  have h10 : p10 := (Or.elim c267 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h11 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                                  exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                                )
                            )
                        )
                    )
                )
                (fun h5 => by
                  exact (Classical.em p3).elim
                    (fun h3 => by
                      exact (Classical.em p4).elim
                        (fun h4 => by
                          have h7 : ¬p7 := (Or.elim c073 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                          have h8 : ¬p8 := (Or.elim c074 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                          have h9 : ¬p9 := (Or.elim c075 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                          have h10 : ¬p10 := (Or.elim c076 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                          have h12 : ¬p12 := (Or.elim c077 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                          have h14 : ¬p14 := (Or.elim c079 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                          have h13 : p13 := (Or.elim c214 (fun x0 => (False.elim (h7 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h8 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h9 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h10 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h12 x4))) (fun r4 => r4))))))))))
                          exact (Or.elim c231 (fun x0 => (h7 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h8 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h9 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h12 x4)) (fun r4 => (h14 r4)))))))))))
                        )
                        (fun h4 => by
                          exact (Classical.em p8).elim
                            (fun h8 => by
                              exact (Classical.em p9).elim
                                (fun h9 => by
                                  have h13 : ¬p13 := (Or.elim c122 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                                  have h14 : ¬p14 := (Or.elim c123 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                                  have h15 : ¬p15 := (Or.elim c124 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                                  have h10 : p10 := (Or.elim c313 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h13 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h14 x4))) (fun r4 => (False.elim (h15 r4))))))))))))
                                  have h7 : ¬p7 := (Or.elim c115 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => (False.elim (r1 h10))))))
                                  have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                                  exact (Or.elim c257 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h7 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h11 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h13 x4)) (fun r4 => (h14 r4)))))))))))
                                )
                                (fun h9 => by
                                  have h10 : p10 := (Or.elim c158 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h5 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => r4))))))))))
                                  have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                                  have h15 : ¬p15 := (Or.elim c126 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                                  exact (Or.elim c282 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h5 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h11 x4)) (fun r4 => (h15 r4)))))))))))
                                )
                            )
                            (fun h8 => by
                              have h7 : p7 := (Or.elim c128 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h5 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h8 r4))))))))))))
                              have h9 : p9 := (Or.elim c140 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h5 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                              have h10 : p10 := (Or.elim c152 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h5 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                              exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                            )
                        )
                    )
                    (fun h3 => by
                      exact (Classical.em p8).elim
                        (fun h8 => by
                          exact (Classical.em p9).elim
                            (fun h9 => by
                              have h13 : ¬p13 := (Or.elim c122 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              have h14 : ¬p14 := (Or.elim c123 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              have h15 : ¬p15 := (Or.elim c124 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              have h10 : p10 := (Or.elim c311 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => x2) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h13 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h14 x4))) (fun r4 => (False.elim (h15 r4))))))))))))
                              have h7 : ¬p7 := (Or.elim c115 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => (False.elim (r1 h10))))))
                              have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                              exact (Or.elim c255 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h7 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h11 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h13 x4)) (fun r4 => (h14 r4)))))))))))
                            )
                            (fun h9 => by
                              have h10 : p10 := (Or.elim c157 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h5 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => r4))))))))))
                              have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                              have h15 : ¬p15 := (Or.elim c126 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                              exact (Or.elim c280 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h5 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h11 x4)) (fun r4 => (h15 r4)))))))))))
                            )
                        )
                        (fun h8 => by
                          have h7 : p7 := (Or.elim c127 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h5 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h8 r4))))))))))))
                          have h9 : p9 := (Or.elim c139 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h5 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                          have h10 : p10 := (Or.elim c151 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h5 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                          exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                        )
                    )
                )
            )
        )
        (fun h6 => by
          exact (Classical.em p3).elim
            (fun h3 => by
              exact (Classical.em p4).elim
                (fun h4 => by
                  have h7 : ¬p7 := (Or.elim c073 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h8 : ¬p8 := (Or.elim c074 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h9 : ¬p9 := (Or.elim c075 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h10 : ¬p10 := (Or.elim c076 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h12 : ¬p12 := (Or.elim c077 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h14 : ¬p14 := (Or.elim c079 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h13 : p13 := (Or.elim c214 (fun x0 => (False.elim (h7 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h8 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h9 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h10 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h12 x4))) (fun r4 => r4))))))))))
                  exact (Or.elim c231 (fun x0 => (h7 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h8 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h9 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h12 x4)) (fun r4 => (h14 r4)))))))))))
                )
                (fun h4 => by
                  exact (Classical.em p8).elim
                    (fun h8 => by
                      exact (Classical.em p13).elim
                        (fun h13 => by
                          have h5 : ¬p5 := (Or.elim c109 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => (False.elim (r1 h13))))))
                          have h9 : ¬p9 := (Or.elim c122 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h13))))))
                          have h10 : p10 := (Or.elim c162 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => r4))))))))))
                          have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                          have h15 : ¬p15 := (Or.elim c126 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                          have h1 : p1 := (Or.elim c282 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h11 x4))) (fun r4 => (False.elim (h15 r4))))))))))))
                          exact (Or.elim c283 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h5 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h11 x4)) (fun r4 => (h15 r4)))))))))))
                        )
                        (fun h13 => by
                          exact (Classical.em p14).elim
                            (fun h14 => by
                              have h5 : ¬p5 := (Or.elim c110 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => (False.elim (r1 h14))))))
                              have h9 : ¬p9 := (Or.elim c123 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                              have h10 : p10 := (Or.elim c162 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => r4))))))))))
                              have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                              have h15 : ¬p15 := (Or.elim c126 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                              have h1 : p1 := (Or.elim c282 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h11 x4))) (fun r4 => (False.elim (h15 r4))))))))))))
                              exact (Or.elim c283 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h5 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h11 x4)) (fun r4 => (h15 r4)))))))))))
                            )
                            (fun h14 => by
                              have h7 : p7 := (Or.elim c245 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h9 : p9 := (Or.elim c249 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h10 : p10 := (Or.elim c253 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                            )
                        )
                    )
                    (fun h8 => by
                      exact (Classical.em p5).elim
                        (fun h5 => by
                          exact (Classical.em p14).elim
                            (fun h14 => by
                              have h9 : ¬p9 := (Or.elim c112 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                              have h12 : ¬p12 := (Or.elim c114 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                              have h1 : p1 := (Or.elim c185 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h8 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => (False.elim (h12 r4))))))))))))
                              exact (Or.elim c189 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h6 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h8 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h9 x4)) (fun r4 => (h12 r4)))))))))))
                            )
                            (fun h14 => by
                              have h12 : p12 := (Or.elim c230 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h8 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h13 : ¬p13 := (Or.elim c113 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h12))) (fun r1 => r1))))
                              have h7 : p7 := (Or.elim c245 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h9 : p9 := (Or.elim c249 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              have h10 : p10 := (Or.elim c253 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                              exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                            )
                        )
                        (fun h5 => by
                          have h7 : p7 := (Or.elim c132 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h8 r4))))))))))))
                          have h9 : p9 := (Or.elim c144 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                          have h10 : p10 := (Or.elim c156 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                          exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                        )
                    )
                )
            )
            (fun h3 => by
              exact (Classical.em p8).elim
                (fun h8 => by
                  exact (Classical.em p13).elim
                    (fun h13 => by
                      have h5 : ¬p5 := (Or.elim c109 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => (False.elim (r1 h13))))))
                      have h9 : ¬p9 := (Or.elim c122 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h13))))))
                      have h10 : p10 := (Or.elim c160 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => r4))))))))))
                      have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                      have h15 : ¬p15 := (Or.elim c126 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                      have h1 : p1 := (Or.elim c280 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h11 x4))) (fun r4 => (False.elim (h15 r4))))))))))))
                      exact (Or.elim c281 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h5 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h11 x4)) (fun r4 => (h15 r4)))))))))))
                    )
                    (fun h13 => by
                      exact (Classical.em p14).elim
                        (fun h14 => by
                          have h5 : ¬p5 := (Or.elim c110 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h8))) (fun r1 => (False.elim (r1 h14))))))
                          have h9 : ¬p9 := (Or.elim c123 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                          have h10 : p10 := (Or.elim c160 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => r4))))))))))
                          have h11 : ¬p11 := (Or.elim c125 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                          have h15 : ¬p15 := (Or.elim c126 (fun x0 => (False.elim (x0 h8))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h10))) (fun r1 => r1))))
                          have h1 : p1 := (Or.elim c280 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h11 x4))) (fun r4 => (False.elim (h15 r4))))))))))))
                          exact (Or.elim c281 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h5 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h11 x4)) (fun r4 => (h15 r4)))))))))))
                        )
                        (fun h14 => by
                          have h7 : p7 := (Or.elim c243 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h9 : p9 := (Or.elim c247 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h10 : p10 := (Or.elim c251 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                        )
                    )
                )
                (fun h8 => by
                  exact (Classical.em p5).elim
                    (fun h5 => by
                      exact (Classical.em p14).elim
                        (fun h14 => by
                          have h9 : ¬p9 := (Or.elim c112 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                          have h12 : ¬p12 := (Or.elim c114 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h14))))))
                          have h1 : p1 := (Or.elim c184 (fun x0 => x0) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h8 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h9 x4))) (fun r4 => (False.elim (h12 r4))))))))))))
                          exact (Or.elim c187 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h6 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h8 x3)) (fun r3 => (Or.elim r3 (fun x4 => (h9 x4)) (fun r4 => (h12 r4)))))))))))
                        )
                        (fun h14 => by
                          have h12 : p12 := (Or.elim c228 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h8 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h13 : ¬p13 := (Or.elim c113 (fun x0 => (False.elim (x0 h5))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h12))) (fun r1 => r1))))
                          have h7 : p7 := (Or.elim c243 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h9 : p9 := (Or.elim c247 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          have h10 : p10 := (Or.elim c251 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h6 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h13 x4))) (fun r4 => (False.elim (h14 r4))))))))))))
                          exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                        )
                    )
                    (fun h5 => by
                      have h7 : p7 := (Or.elim c130 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => x4) (fun r4 => (False.elim (h8 r4))))))))))))
                      have h9 : p9 := (Or.elim c142 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                      have h10 : p10 := (Or.elim c154 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h6 x3))) (fun r3 => (Or.elim r3 (fun x4 => (False.elim (h8 x4))) (fun r4 => r4))))))))))
                      exact (Or.elim c115 (fun x0 => (x0 h7)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h9)) (fun r1 => (r1 h10)))))
                    )
                )
            )
        )
    )

/-- The full original formula implies the refuted subset. -/
theorem terminal_unsat_prop (p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15 : Prop)
    (h : terminalFormula p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15) : False := by
  have tail1 := h.2
  have tail2 := tail1.2
  have tail3 := tail2.2
  have tail4 := tail3.2
  have tail5 := tail4.2
  have tail6 := tail5.2
  have tail7 := tail6.2
  have tail8 := tail7.2
  have tail9 := tail8.2
  have tail10 := tail9.2
  have tail11 := tail10.2
  have tail12 := tail11.2
  have tail13 := tail12.2
  have tail14 := tail13.2
  have tail15 := tail14.2
  have tail16 := tail15.2
  have tail17 := tail16.2
  have tail18 := tail17.2
  have tail19 := tail18.2
  have tail20 := tail19.2
  have tail21 := tail20.2
  have tail22 := tail21.2
  have tail23 := tail22.2
  have tail24 := tail23.2
  have tail25 := tail24.2
  have tail26 := tail25.2
  have tail27 := tail26.2
  have tail28 := tail27.2
  have tail29 := tail28.2
  have tail30 := tail29.2
  have tail31 := tail30.2
  have tail32 := tail31.2
  have tail33 := tail32.2
  have tail34 := tail33.2
  have tail35 := tail34.2
  have tail36 := tail35.2
  have tail37 := tail36.2
  have tail38 := tail37.2
  have tail39 := tail38.2
  have tail40 := tail39.2
  have tail41 := tail40.2
  have tail42 := tail41.2
  have tail43 := tail42.2
  have tail44 := tail43.2
  have tail45 := tail44.2
  have tail46 := tail45.2
  have tail47 := tail46.2
  have tail48 := tail47.2
  have tail49 := tail48.2
  have tail50 := tail49.2
  have tail51 := tail50.2
  have c052 := tail51.1
  have tail52 := tail51.2
  have c053 := tail52.1
  have tail53 := tail52.2
  have c054 := tail53.1
  have tail54 := tail53.2
  have c055 := tail54.1
  have tail55 := tail54.2
  have c056 := tail55.1
  have tail56 := tail55.2
  have c057 := tail56.1
  have tail57 := tail56.2
  have c058 := tail57.1
  have tail58 := tail57.2
  have c059 := tail58.1
  have tail59 := tail58.2
  have c060 := tail59.1
  have tail60 := tail59.2
  have c061 := tail60.1
  have tail61 := tail60.2
  have c062 := tail61.1
  have tail62 := tail61.2
  have tail63 := tail62.2
  have c064 := tail63.1
  have tail64 := tail63.2
  have c065 := tail64.1
  have tail65 := tail64.2
  have c066 := tail65.1
  have tail66 := tail65.2
  have c067 := tail66.1
  have tail67 := tail66.2
  have c068 := tail67.1
  have tail68 := tail67.2
  have c069 := tail68.1
  have tail69 := tail68.2
  have tail70 := tail69.2
  have c071 := tail70.1
  have tail71 := tail70.2
  have tail72 := tail71.2
  have c073 := tail72.1
  have tail73 := tail72.2
  have c074 := tail73.1
  have tail74 := tail73.2
  have c075 := tail74.1
  have tail75 := tail74.2
  have c076 := tail75.1
  have tail76 := tail75.2
  have c077 := tail76.1
  have tail77 := tail76.2
  have tail78 := tail77.2
  have c079 := tail78.1
  have tail79 := tail78.2
  have tail80 := tail79.2
  have tail81 := tail80.2
  have tail82 := tail81.2
  have tail83 := tail82.2
  have tail84 := tail83.2
  have tail85 := tail84.2
  have tail86 := tail85.2
  have tail87 := tail86.2
  have tail88 := tail87.2
  have tail89 := tail88.2
  have tail90 := tail89.2
  have tail91 := tail90.2
  have tail92 := tail91.2
  have tail93 := tail92.2
  have tail94 := tail93.2
  have tail95 := tail94.2
  have tail96 := tail95.2
  have tail97 := tail96.2
  have tail98 := tail97.2
  have tail99 := tail98.2
  have tail100 := tail99.2
  have c101 := tail100.1
  have tail101 := tail100.2
  have tail102 := tail101.2
  have tail103 := tail102.2
  have tail104 := tail103.2
  have tail105 := tail104.2
  have tail106 := tail105.2
  have tail107 := tail106.2
  have tail108 := tail107.2
  have c109 := tail108.1
  have tail109 := tail108.2
  have c110 := tail109.1
  have tail110 := tail109.2
  have tail111 := tail110.2
  have c112 := tail111.1
  have tail112 := tail111.2
  have c113 := tail112.1
  have tail113 := tail112.2
  have c114 := tail113.1
  have tail114 := tail113.2
  have c115 := tail114.1
  have tail115 := tail114.2
  have tail116 := tail115.2
  have tail117 := tail116.2
  have tail118 := tail117.2
  have tail119 := tail118.2
  have tail120 := tail119.2
  have tail121 := tail120.2
  have c122 := tail121.1
  have tail122 := tail121.2
  have c123 := tail122.1
  have tail123 := tail122.2
  have c124 := tail123.1
  have tail124 := tail123.2
  have c125 := tail124.1
  have tail125 := tail124.2
  have c126 := tail125.1
  have tail126 := tail125.2
  have c127 := tail126.1
  have tail127 := tail126.2
  have c128 := tail127.1
  have tail128 := tail127.2
  have c129 := tail128.1
  have tail129 := tail128.2
  have c130 := tail129.1
  have tail130 := tail129.2
  have c131 := tail130.1
  have tail131 := tail130.2
  have c132 := tail131.1
  have tail132 := tail131.2
  have tail133 := tail132.2
  have tail134 := tail133.2
  have tail135 := tail134.2
  have tail136 := tail135.2
  have tail137 := tail136.2
  have tail138 := tail137.2
  have c139 := tail138.1
  have tail139 := tail138.2
  have c140 := tail139.1
  have tail140 := tail139.2
  have c141 := tail140.1
  have tail141 := tail140.2
  have c142 := tail141.1
  have tail142 := tail141.2
  have c143 := tail142.1
  have tail143 := tail142.2
  have c144 := tail143.1
  have tail144 := tail143.2
  have tail145 := tail144.2
  have tail146 := tail145.2
  have tail147 := tail146.2
  have tail148 := tail147.2
  have tail149 := tail148.2
  have tail150 := tail149.2
  have c151 := tail150.1
  have tail151 := tail150.2
  have c152 := tail151.1
  have tail152 := tail151.2
  have c153 := tail152.1
  have tail153 := tail152.2
  have c154 := tail153.1
  have tail154 := tail153.2
  have c155 := tail154.1
  have tail155 := tail154.2
  have c156 := tail155.1
  have tail156 := tail155.2
  have c157 := tail156.1
  have tail157 := tail156.2
  have c158 := tail157.1
  have tail158 := tail157.2
  have c159 := tail158.1
  have tail159 := tail158.2
  have c160 := tail159.1
  have tail160 := tail159.2
  have c161 := tail160.1
  have tail161 := tail160.2
  have c162 := tail161.1
  have tail162 := tail161.2
  have tail163 := tail162.2
  have tail164 := tail163.2
  have tail165 := tail164.2
  have tail166 := tail165.2
  have tail167 := tail166.2
  have tail168 := tail167.2
  have tail169 := tail168.2
  have tail170 := tail169.2
  have tail171 := tail170.2
  have tail172 := tail171.2
  have tail173 := tail172.2
  have tail174 := tail173.2
  have tail175 := tail174.2
  have tail176 := tail175.2
  have tail177 := tail176.2
  have tail178 := tail177.2
  have tail179 := tail178.2
  have tail180 := tail179.2
  have tail181 := tail180.2
  have tail182 := tail181.2
  have tail183 := tail182.2
  have c184 := tail183.1
  have tail184 := tail183.2
  have c185 := tail184.1
  have tail185 := tail184.2
  have c186 := tail185.1
  have tail186 := tail185.2
  have c187 := tail186.1
  have tail187 := tail186.2
  have c188 := tail187.1
  have tail188 := tail187.2
  have c189 := tail188.1
  have tail189 := tail188.2
  have tail190 := tail189.2
  have tail191 := tail190.2
  have tail192 := tail191.2
  have tail193 := tail192.2
  have tail194 := tail193.2
  have tail195 := tail194.2
  have tail196 := tail195.2
  have tail197 := tail196.2
  have tail198 := tail197.2
  have tail199 := tail198.2
  have tail200 := tail199.2
  have tail201 := tail200.2
  have tail202 := tail201.2
  have tail203 := tail202.2
  have tail204 := tail203.2
  have tail205 := tail204.2
  have tail206 := tail205.2
  have tail207 := tail206.2
  have tail208 := tail207.2
  have tail209 := tail208.2
  have tail210 := tail209.2
  have tail211 := tail210.2
  have tail212 := tail211.2
  have tail213 := tail212.2
  have c214 := tail213.1
  have tail214 := tail213.2
  have tail215 := tail214.2
  have tail216 := tail215.2
  have tail217 := tail216.2
  have tail218 := tail217.2
  have tail219 := tail218.2
  have tail220 := tail219.2
  have tail221 := tail220.2
  have tail222 := tail221.2
  have tail223 := tail222.2
  have tail224 := tail223.2
  have tail225 := tail224.2
  have tail226 := tail225.2
  have c227 := tail226.1
  have tail227 := tail226.2
  have c228 := tail227.1
  have tail228 := tail227.2
  have c229 := tail228.1
  have tail229 := tail228.2
  have c230 := tail229.1
  have tail230 := tail229.2
  have c231 := tail230.1
  have tail231 := tail230.2
  have tail232 := tail231.2
  have tail233 := tail232.2
  have tail234 := tail233.2
  have tail235 := tail234.2
  have c236 := tail235.1
  have tail236 := tail235.2
  have tail237 := tail236.2
  have c238 := tail237.1
  have tail238 := tail237.2
  have tail239 := tail238.2
  have tail240 := tail239.2
  have tail241 := tail240.2
  have c242 := tail241.1
  have tail242 := tail241.2
  have c243 := tail242.1
  have tail243 := tail242.2
  have c244 := tail243.1
  have tail244 := tail243.2
  have c245 := tail244.1
  have tail245 := tail244.2
  have c246 := tail245.1
  have tail246 := tail245.2
  have c247 := tail246.1
  have tail247 := tail246.2
  have c248 := tail247.1
  have tail248 := tail247.2
  have c249 := tail248.1
  have tail249 := tail248.2
  have c250 := tail249.1
  have tail250 := tail249.2
  have c251 := tail250.1
  have tail251 := tail250.2
  have c252 := tail251.1
  have tail252 := tail251.2
  have c253 := tail252.1
  have tail253 := tail252.2
  have tail254 := tail253.2
  have c255 := tail254.1
  have tail255 := tail254.2
  have tail256 := tail255.2
  have c257 := tail256.1
  have tail257 := tail256.2
  have tail258 := tail257.2
  have tail259 := tail258.2
  have tail260 := tail259.2
  have c261 := tail260.1
  have tail261 := tail260.2
  have tail262 := tail261.2
  have c263 := tail262.1
  have tail263 := tail262.2
  have tail264 := tail263.2
  have tail265 := tail264.2
  have tail266 := tail265.2
  have c267 := tail266.1
  have tail267 := tail266.2
  have tail268 := tail267.2
  have c269 := tail268.1
  have tail269 := tail268.2
  have tail270 := tail269.2
  have tail271 := tail270.2
  have tail272 := tail271.2
  have tail273 := tail272.2
  have tail274 := tail273.2
  have tail275 := tail274.2
  have tail276 := tail275.2
  have tail277 := tail276.2
  have tail278 := tail277.2
  have tail279 := tail278.2
  have c280 := tail279.1
  have tail280 := tail279.2
  have c281 := tail280.1
  have tail281 := tail280.2
  have c282 := tail281.1
  have tail282 := tail281.2
  have c283 := tail282.1
  have tail283 := tail282.2
  have tail284 := tail283.2
  have tail285 := tail284.2
  have tail286 := tail285.2
  have tail287 := tail286.2
  have tail288 := tail287.2
  have tail289 := tail288.2
  have tail290 := tail289.2
  have tail291 := tail290.2
  have tail292 := tail291.2
  have tail293 := tail292.2
  have tail294 := tail293.2
  have tail295 := tail294.2
  have tail296 := tail295.2
  have tail297 := tail296.2
  have tail298 := tail297.2
  have tail299 := tail298.2
  have tail300 := tail299.2
  have tail301 := tail300.2
  have tail302 := tail301.2
  have tail303 := tail302.2
  have tail304 := tail303.2
  have tail305 := tail304.2
  have tail306 := tail305.2
  have tail307 := tail306.2
  have tail308 := tail307.2
  have tail309 := tail308.2
  have tail310 := tail309.2
  have c311 := tail310.1
  have tail311 := tail310.2
  have tail312 := tail311.2
  have c313 := tail312
  exact core_unsat p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 p14 p15
    c052 c053 c054 c055 c056 c057 c058 c059 c060 c061 c062 c064 c065 c066 c067 c068 c069 c071 c073 c074 c075 c076 c077 c079 c101 c109 c110 c112 c113 c114 c115 c122 c123 c124 c125 c126 c127 c128 c129 c130 c131 c132 c139 c140 c141 c142 c143 c144 c151 c152 c153 c154 c155 c156 c157 c158 c159 c160 c161 c162 c184 c185 c186 c187 c188 c189 c214 c227 c228 c229 c230 c231 c236 c238 c242 c243 c244 c245 c246 c247 c248 c249 c250 c251 c252 c253 c255 c257 c261 c263 c267 c269 c280 c281 c282 c283 c311 c313

/-- The fixed CNF interpreted on fifteen Boolean membership values. -/
def terminalBoolFormula (b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 : Bool) : Prop :=
  terminalFormula (b1 = true) (b2 = true) (b3 = true) (b4 = true) (b5 = true) (b6 = true) (b7 = true) (b8 = true) (b9 = true) (b10 = true) (b11 = true) (b12 = true) (b13 = true) (b14 = true) (b15 = true)

/-- No assignment of the fifteen Boolean values satisfies the fixed CNF. -/
theorem terminal_unsat_bool (b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 : Bool) :
    ¬terminalBoolFormula b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 :=
  fun h => terminal_unsat_prop (b1 = true) (b2 = true) (b3 = true) (b4 = true) (b5 = true) (b6 = true) (b7 = true) (b8 = true) (b9 = true) (b10 = true) (b11 = true) (b12 = true) (b13 = true) (b14 = true) (b15 = true) h

#print axioms core_unsat
#print axioms terminal_unsat_prop
#print axioms terminal_unsat_bool

end Delta3.Terminal15Boolean
