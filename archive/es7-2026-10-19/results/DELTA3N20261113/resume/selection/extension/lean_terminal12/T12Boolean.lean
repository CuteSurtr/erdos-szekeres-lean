/-! Fixed 12-variable Boolean refutation. Generated ordinary proof terms.
Original DIMACS SHA-256: 25ca75a9eee359ca03ae7f96657128ab03693c03421b1e7e83627f529841890a.
The source is a candidate until a bounded Lean check and axiom audit pass.
No geometric claim is encoded here. -/

set_option maxRecDepth 4096

namespace Delta3.T12Boolean

/-- The 192 original clauses, in exact DIMACS row order. -/
def terminalFormula (p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 : Prop) : Prop :=
  (¬p1 ∨ ¬p2 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p1 ∨ ¬p5 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p2 ∨ ¬p5 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p3 ∨ ¬p5 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p3 ∨ ¬p5 ∨ ¬p10 ∨ ¬p11) ∧
  (¬p4 ∨ ¬p5 ∨ ¬p6 ∨ ¬p7) ∧
  (¬p4 ∨ ¬p5 ∨ ¬p10 ∨ ¬p11) ∧
  (¬p6 ∨ ¬p8 ∨ ¬p9 ∨ ¬p11) ∧
  (¬p6 ∨ ¬p8 ∨ ¬p10 ∨ ¬p11) ∧
  (¬p7 ∨ ¬p8 ∨ ¬p9 ∨ ¬p11) ∧
  (¬p7 ∨ ¬p8 ∨ ¬p10 ∨ ¬p11) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p10 ∨ ¬p11) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p10 ∨ ¬p12) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p3) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p4) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p6) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p7) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p8) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p9) ∧
  (¬p1 ∨ ¬p2 ∨ ¬p11) ∧
  (¬p1 ∨ ¬p5 ∨ ¬p6) ∧
  (¬p1 ∨ ¬p5 ∨ ¬p7) ∧
  (¬p1 ∨ ¬p5 ∨ ¬p8) ∧
  (¬p1 ∨ ¬p5 ∨ ¬p9) ∧
  (¬p1 ∨ ¬p5 ∨ ¬p11) ∧
  (¬p2 ∨ ¬p5 ∨ ¬p6) ∧
  (¬p2 ∨ ¬p5 ∨ ¬p7) ∧
  (¬p2 ∨ ¬p5 ∨ ¬p8) ∧
  (¬p2 ∨ ¬p5 ∨ ¬p9) ∧
  (¬p2 ∨ ¬p5 ∨ ¬p11) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p6) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p7) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p8) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p9) ∧
  (¬p3 ∨ ¬p4 ∨ ¬p11) ∧
  (¬p3 ∨ ¬p5 ∨ ¬p6) ∧
  (¬p3 ∨ ¬p5 ∨ ¬p7) ∧
  (¬p3 ∨ ¬p5 ∨ ¬p8) ∧
  (¬p3 ∨ ¬p5 ∨ ¬p9) ∧
  (¬p3 ∨ ¬p5 ∨ ¬p10) ∧
  (¬p3 ∨ ¬p5 ∨ ¬p11) ∧
  (¬p4 ∨ ¬p5 ∨ ¬p6) ∧
  (¬p4 ∨ ¬p5 ∨ ¬p7) ∧
  (¬p4 ∨ ¬p5 ∨ ¬p8) ∧
  (¬p4 ∨ ¬p5 ∨ ¬p9) ∧
  (¬p4 ∨ ¬p5 ∨ ¬p10) ∧
  (¬p4 ∨ ¬p5 ∨ ¬p11) ∧
  (¬p6 ∨ ¬p8 ∨ ¬p9) ∧
  (¬p6 ∨ ¬p8 ∨ ¬p10) ∧
  (¬p6 ∨ ¬p8 ∨ ¬p11) ∧
  (¬p6 ∨ ¬p8 ∨ ¬p12) ∧
  (¬p7 ∨ ¬p8 ∨ ¬p9) ∧
  (¬p7 ∨ ¬p8 ∨ ¬p10) ∧
  (¬p7 ∨ ¬p8 ∨ ¬p11) ∧
  (¬p7 ∨ ¬p8 ∨ ¬p12) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p10) ∧
  (¬p7 ∨ ¬p9 ∨ ¬p12) ∧
  (p1 ∨ p2 ∨ p3 ∨ p6 ∨ p7) ∧
  (p1 ∨ p2 ∨ p3 ∨ p6 ∨ p8) ∧
  (p1 ∨ p2 ∨ p3 ∨ p6 ∨ p9) ∧
  (p1 ∨ p2 ∨ p3 ∨ p6 ∨ p11) ∧
  (p1 ∨ p2 ∨ p3 ∨ p7 ∨ p8) ∧
  (p1 ∨ p2 ∨ p3 ∨ p7 ∨ p9) ∧
  (p1 ∨ p2 ∨ p3 ∨ p7 ∨ p11) ∧
  (p1 ∨ p2 ∨ p3 ∨ p8 ∨ p9) ∧
  (p1 ∨ p2 ∨ p3 ∨ p8 ∨ p11) ∧
  (p1 ∨ p2 ∨ p3 ∨ p9 ∨ p11) ∧
  (p1 ∨ p2 ∨ p4 ∨ p6 ∨ p7) ∧
  (p1 ∨ p2 ∨ p4 ∨ p6 ∨ p8) ∧
  (p1 ∨ p2 ∨ p4 ∨ p6 ∨ p9) ∧
  (p1 ∨ p2 ∨ p4 ∨ p6 ∨ p11) ∧
  (p1 ∨ p2 ∨ p4 ∨ p7 ∨ p8) ∧
  (p1 ∨ p2 ∨ p4 ∨ p7 ∨ p9) ∧
  (p1 ∨ p2 ∨ p4 ∨ p7 ∨ p11) ∧
  (p1 ∨ p2 ∨ p4 ∨ p8 ∨ p9) ∧
  (p1 ∨ p2 ∨ p4 ∨ p8 ∨ p11) ∧
  (p1 ∨ p2 ∨ p4 ∨ p9 ∨ p11) ∧
  (p1 ∨ p2 ∨ p5 ∨ p10 ∨ p12) ∧
  (p1 ∨ p3 ∨ p4 ∨ p5 ∨ p12) ∧
  (p1 ∨ p3 ∨ p4 ∨ p10 ∨ p12) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p7) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p8) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p9) ∧
  (p1 ∨ p3 ∨ p5 ∨ p6 ∨ p11) ∧
  (p1 ∨ p3 ∨ p5 ∨ p7 ∨ p8) ∧
  (p1 ∨ p3 ∨ p5 ∨ p7 ∨ p9) ∧
  (p1 ∨ p3 ∨ p5 ∨ p7 ∨ p11) ∧
  (p1 ∨ p3 ∨ p5 ∨ p8 ∨ p9) ∧
  (p1 ∨ p3 ∨ p5 ∨ p8 ∨ p11) ∧
  (p1 ∨ p3 ∨ p5 ∨ p9 ∨ p11) ∧
  (p1 ∨ p3 ∨ p6 ∨ p9 ∨ p10) ∧
  (p1 ∨ p3 ∨ p6 ∨ p9 ∨ p12) ∧
  (p1 ∨ p3 ∨ p6 ∨ p10 ∨ p11) ∧
  (p1 ∨ p3 ∨ p6 ∨ p11 ∨ p12) ∧
  (p1 ∨ p3 ∨ p7 ∨ p10 ∨ p11) ∧
  (p1 ∨ p3 ∨ p7 ∨ p11 ∨ p12) ∧
  (p1 ∨ p3 ∨ p8 ∨ p9 ∨ p10) ∧
  (p1 ∨ p3 ∨ p8 ∨ p9 ∨ p12) ∧
  (p1 ∨ p3 ∨ p8 ∨ p10 ∨ p11) ∧
  (p1 ∨ p3 ∨ p8 ∨ p10 ∨ p12) ∧
  (p1 ∨ p3 ∨ p8 ∨ p11 ∨ p12) ∧
  (p1 ∨ p3 ∨ p9 ∨ p10 ∨ p11) ∧
  (p1 ∨ p3 ∨ p9 ∨ p11 ∨ p12) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p7) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p8) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p9) ∧
  (p1 ∨ p4 ∨ p5 ∨ p6 ∨ p11) ∧
  (p1 ∨ p4 ∨ p5 ∨ p7 ∨ p8) ∧
  (p1 ∨ p4 ∨ p5 ∨ p7 ∨ p9) ∧
  (p1 ∨ p4 ∨ p5 ∨ p7 ∨ p11) ∧
  (p1 ∨ p4 ∨ p5 ∨ p8 ∨ p9) ∧
  (p1 ∨ p4 ∨ p5 ∨ p8 ∨ p11) ∧
  (p1 ∨ p4 ∨ p5 ∨ p9 ∨ p11) ∧
  (p1 ∨ p4 ∨ p6 ∨ p9 ∨ p10) ∧
  (p1 ∨ p4 ∨ p6 ∨ p9 ∨ p12) ∧
  (p1 ∨ p4 ∨ p6 ∨ p10 ∨ p11) ∧
  (p1 ∨ p4 ∨ p6 ∨ p11 ∨ p12) ∧
  (p1 ∨ p4 ∨ p7 ∨ p10 ∨ p11) ∧
  (p1 ∨ p4 ∨ p7 ∨ p11 ∨ p12) ∧
  (p1 ∨ p4 ∨ p8 ∨ p9 ∨ p10) ∧
  (p1 ∨ p4 ∨ p8 ∨ p9 ∨ p12) ∧
  (p1 ∨ p4 ∨ p8 ∨ p10 ∨ p11) ∧
  (p1 ∨ p4 ∨ p8 ∨ p10 ∨ p12) ∧
  (p1 ∨ p4 ∨ p8 ∨ p11 ∨ p12) ∧
  (p1 ∨ p4 ∨ p9 ∨ p10 ∨ p11) ∧
  (p1 ∨ p4 ∨ p9 ∨ p11 ∨ p12) ∧
  (p2 ∨ p3 ∨ p4 ∨ p5 ∨ p12) ∧
  (p2 ∨ p3 ∨ p4 ∨ p10 ∨ p12) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p7) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p8) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p9) ∧
  (p2 ∨ p3 ∨ p5 ∨ p6 ∨ p11) ∧
  (p2 ∨ p3 ∨ p5 ∨ p7 ∨ p8) ∧
  (p2 ∨ p3 ∨ p5 ∨ p7 ∨ p9) ∧
  (p2 ∨ p3 ∨ p5 ∨ p7 ∨ p11) ∧
  (p2 ∨ p3 ∨ p5 ∨ p8 ∨ p9) ∧
  (p2 ∨ p3 ∨ p5 ∨ p8 ∨ p11) ∧
  (p2 ∨ p3 ∨ p5 ∨ p9 ∨ p11) ∧
  (p2 ∨ p3 ∨ p6 ∨ p9 ∨ p10) ∧
  (p2 ∨ p3 ∨ p6 ∨ p9 ∨ p12) ∧
  (p2 ∨ p3 ∨ p6 ∨ p10 ∨ p11) ∧
  (p2 ∨ p3 ∨ p6 ∨ p11 ∨ p12) ∧
  (p2 ∨ p3 ∨ p7 ∨ p10 ∨ p11) ∧
  (p2 ∨ p3 ∨ p7 ∨ p11 ∨ p12) ∧
  (p2 ∨ p3 ∨ p8 ∨ p9 ∨ p10) ∧
  (p2 ∨ p3 ∨ p8 ∨ p9 ∨ p12) ∧
  (p2 ∨ p3 ∨ p8 ∨ p10 ∨ p11) ∧
  (p2 ∨ p3 ∨ p8 ∨ p10 ∨ p12) ∧
  (p2 ∨ p3 ∨ p8 ∨ p11 ∨ p12) ∧
  (p2 ∨ p3 ∨ p9 ∨ p10 ∨ p11) ∧
  (p2 ∨ p3 ∨ p9 ∨ p11 ∨ p12) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p7) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p8) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p9) ∧
  (p2 ∨ p4 ∨ p5 ∨ p6 ∨ p11) ∧
  (p2 ∨ p4 ∨ p5 ∨ p7 ∨ p8) ∧
  (p2 ∨ p4 ∨ p5 ∨ p7 ∨ p9) ∧
  (p2 ∨ p4 ∨ p5 ∨ p7 ∨ p11) ∧
  (p2 ∨ p4 ∨ p5 ∨ p8 ∨ p9) ∧
  (p2 ∨ p4 ∨ p5 ∨ p8 ∨ p11) ∧
  (p2 ∨ p4 ∨ p5 ∨ p9 ∨ p11) ∧
  (p2 ∨ p4 ∨ p6 ∨ p9 ∨ p10) ∧
  (p2 ∨ p4 ∨ p6 ∨ p9 ∨ p12) ∧
  (p2 ∨ p4 ∨ p6 ∨ p10 ∨ p11) ∧
  (p2 ∨ p4 ∨ p6 ∨ p11 ∨ p12) ∧
  (p2 ∨ p4 ∨ p7 ∨ p10 ∨ p11) ∧
  (p2 ∨ p4 ∨ p7 ∨ p11 ∨ p12) ∧
  (p2 ∨ p4 ∨ p8 ∨ p9 ∨ p10) ∧
  (p2 ∨ p4 ∨ p8 ∨ p9 ∨ p12) ∧
  (p2 ∨ p4 ∨ p8 ∨ p10 ∨ p11) ∧
  (p2 ∨ p4 ∨ p8 ∨ p10 ∨ p12) ∧
  (p2 ∨ p4 ∨ p8 ∨ p11 ∨ p12) ∧
  (p2 ∨ p4 ∨ p9 ∨ p10 ∨ p11) ∧
  (p2 ∨ p4 ∨ p9 ∨ p11 ∨ p12) ∧
  (p3 ∨ p5 ∨ p6 ∨ p9 ∨ p10) ∧
  (p3 ∨ p5 ∨ p6 ∨ p10 ∨ p11) ∧
  (p3 ∨ p5 ∨ p7 ∨ p10 ∨ p11) ∧
  (p3 ∨ p5 ∨ p8 ∨ p9 ∨ p10) ∧
  (p3 ∨ p5 ∨ p8 ∨ p10 ∨ p11) ∧
  (p3 ∨ p5 ∨ p9 ∨ p10 ∨ p11) ∧
  (p4 ∨ p5 ∨ p6 ∨ p9 ∨ p10) ∧
  (p4 ∨ p5 ∨ p6 ∨ p10 ∨ p11) ∧
  (p4 ∨ p5 ∨ p7 ∨ p10 ∨ p11) ∧
  (p4 ∨ p5 ∨ p8 ∨ p9 ∨ p10) ∧
  (p4 ∨ p5 ∨ p8 ∨ p10 ∨ p11) ∧
  (p4 ∨ p5 ∨ p9 ∨ p10 ∨ p11) ∧
  (p6 ∨ p7 ∨ p8 ∨ p9 ∨ p11) ∧
  (p6 ∨ p7 ∨ p8 ∨ p10 ∨ p11) ∧
  (p6 ∨ p7 ∨ p8 ∨ p11 ∨ p12) ∧
  (p6 ∨ p7 ∨ p10 ∨ p11 ∨ p12) ∧
  (p7 ∨ p9 ∨ p10 ∨ p11 ∨ p12)

/-- Refutation of the supplied 65-clause subset by explicit case analysis. -/
theorem core_unsat (p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 : Prop)
    (c017 : ¬p1 ∨ ¬p2 ∨ ¬p6)
    (c018 : ¬p1 ∨ ¬p2 ∨ ¬p7)
    (c019 : ¬p1 ∨ ¬p2 ∨ ¬p8)
    (c020 : ¬p1 ∨ ¬p2 ∨ ¬p9)
    (c021 : ¬p1 ∨ ¬p2 ∨ ¬p11)
    (c022 : ¬p1 ∨ ¬p5 ∨ ¬p6)
    (c023 : ¬p1 ∨ ¬p5 ∨ ¬p7)
    (c024 : ¬p1 ∨ ¬p5 ∨ ¬p8)
    (c025 : ¬p1 ∨ ¬p5 ∨ ¬p9)
    (c026 : ¬p1 ∨ ¬p5 ∨ ¬p11)
    (c027 : ¬p2 ∨ ¬p5 ∨ ¬p6)
    (c028 : ¬p2 ∨ ¬p5 ∨ ¬p7)
    (c029 : ¬p2 ∨ ¬p5 ∨ ¬p8)
    (c030 : ¬p2 ∨ ¬p5 ∨ ¬p9)
    (c031 : ¬p2 ∨ ¬p5 ∨ ¬p11)
    (c032 : ¬p3 ∨ ¬p4 ∨ ¬p6)
    (c033 : ¬p3 ∨ ¬p4 ∨ ¬p7)
    (c034 : ¬p3 ∨ ¬p4 ∨ ¬p8)
    (c035 : ¬p3 ∨ ¬p4 ∨ ¬p9)
    (c036 : ¬p3 ∨ ¬p4 ∨ ¬p11)
    (c051 : ¬p6 ∨ ¬p8 ∨ ¬p11)
    (c053 : ¬p7 ∨ ¬p8 ∨ ¬p9)
    (c057 : ¬p7 ∨ ¬p9 ∨ ¬p10)
    (c058 : ¬p7 ∨ ¬p9 ∨ ¬p12)
    (c059 : p1 ∨ p2 ∨ p3 ∨ p6 ∨ p7)
    (c061 : p1 ∨ p2 ∨ p3 ∨ p6 ∨ p9)
    (c063 : p1 ∨ p2 ∨ p3 ∨ p7 ∨ p8)
    (c065 : p1 ∨ p2 ∨ p3 ∨ p7 ∨ p11)
    (c066 : p1 ∨ p2 ∨ p3 ∨ p8 ∨ p9)
    (c068 : p1 ∨ p2 ∨ p3 ∨ p9 ∨ p11)
    (c069 : p1 ∨ p2 ∨ p4 ∨ p6 ∨ p7)
    (c071 : p1 ∨ p2 ∨ p4 ∨ p6 ∨ p9)
    (c073 : p1 ∨ p2 ∨ p4 ∨ p7 ∨ p8)
    (c075 : p1 ∨ p2 ∨ p4 ∨ p7 ∨ p11)
    (c076 : p1 ∨ p2 ∨ p4 ∨ p8 ∨ p9)
    (c078 : p1 ∨ p2 ∨ p4 ∨ p9 ∨ p11)
    (c082 : p1 ∨ p3 ∨ p5 ∨ p6 ∨ p7)
    (c084 : p1 ∨ p3 ∨ p5 ∨ p6 ∨ p9)
    (c086 : p1 ∨ p3 ∨ p5 ∨ p7 ∨ p8)
    (c088 : p1 ∨ p3 ∨ p5 ∨ p7 ∨ p11)
    (c089 : p1 ∨ p3 ∨ p5 ∨ p8 ∨ p9)
    (c091 : p1 ∨ p3 ∨ p5 ∨ p9 ∨ p11)
    (c101 : p1 ∨ p3 ∨ p8 ∨ p10 ∨ p12)
    (c105 : p1 ∨ p4 ∨ p5 ∨ p6 ∨ p7)
    (c107 : p1 ∨ p4 ∨ p5 ∨ p6 ∨ p9)
    (c109 : p1 ∨ p4 ∨ p5 ∨ p7 ∨ p8)
    (c111 : p1 ∨ p4 ∨ p5 ∨ p7 ∨ p11)
    (c112 : p1 ∨ p4 ∨ p5 ∨ p8 ∨ p9)
    (c114 : p1 ∨ p4 ∨ p5 ∨ p9 ∨ p11)
    (c124 : p1 ∨ p4 ∨ p8 ∨ p10 ∨ p12)
    (c130 : p2 ∨ p3 ∨ p5 ∨ p6 ∨ p7)
    (c132 : p2 ∨ p3 ∨ p5 ∨ p6 ∨ p9)
    (c134 : p2 ∨ p3 ∨ p5 ∨ p7 ∨ p8)
    (c136 : p2 ∨ p3 ∨ p5 ∨ p7 ∨ p11)
    (c137 : p2 ∨ p3 ∨ p5 ∨ p8 ∨ p9)
    (c139 : p2 ∨ p3 ∨ p5 ∨ p9 ∨ p11)
    (c149 : p2 ∨ p3 ∨ p8 ∨ p10 ∨ p12)
    (c153 : p2 ∨ p4 ∨ p5 ∨ p6 ∨ p7)
    (c155 : p2 ∨ p4 ∨ p5 ∨ p6 ∨ p9)
    (c157 : p2 ∨ p4 ∨ p5 ∨ p7 ∨ p8)
    (c159 : p2 ∨ p4 ∨ p5 ∨ p7 ∨ p11)
    (c160 : p2 ∨ p4 ∨ p5 ∨ p8 ∨ p9)
    (c162 : p2 ∨ p4 ∨ p5 ∨ p9 ∨ p11)
    (c172 : p2 ∨ p4 ∨ p8 ∨ p10 ∨ p12)
    (c188 : p6 ∨ p7 ∨ p8 ∨ p9 ∨ p11)
    : False := by
  exact (Classical.em p1).elim
    (fun h1 => by
      exact (Classical.em p2).elim
        (fun h2 => by
          have h6 : ¬p6 := (Or.elim c017 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          have h7 : ¬p7 := (Or.elim c018 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          have h8 : ¬p8 := (Or.elim c019 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          have h9 : ¬p9 := (Or.elim c020 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          have h11 : ¬p11 := (Or.elim c021 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h2))) (fun r1 => r1))))
          exact (Or.elim c188 (fun x0 => (h6 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h7 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (h11 r3)))))))))
        )
        (fun h2 => by
          exact (Classical.em p5).elim
            (fun h5 => by
              have h6 : ¬p6 := (Or.elim c022 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              have h7 : ¬p7 := (Or.elim c023 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              have h8 : ¬p8 := (Or.elim c024 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              have h9 : ¬p9 := (Or.elim c025 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              have h11 : ¬p11 := (Or.elim c026 (fun x0 => (False.elim (x0 h1))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              exact (Or.elim c188 (fun x0 => (h6 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h7 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (h11 r3)))))))))
            )
            (fun h5 => by
              exact (Classical.em p3).elim
                (fun h3 => by
                  exact (Classical.em p4).elim
                    (fun h4 => by
                      have h6 : ¬p6 := (Or.elim c032 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h7 : ¬p7 := (Or.elim c033 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h8 : ¬p8 := (Or.elim c034 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h9 : ¬p9 := (Or.elim c035 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h11 : ¬p11 := (Or.elim c036 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      exact (Or.elim c188 (fun x0 => (h6 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h7 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (h11 r3)))))))))
                    )
                    (fun h4 => by
                      exact (Classical.em p7).elim
                        (fun h7 => by
                          exact (Classical.em p9).elim
                            (fun h9 => by
                              have h8 : ¬p8 := (Or.elim c053 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h9))))))
                              have h10 : ¬p10 := (Or.elim c057 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              have h12 : ¬p12 := (Or.elim c058 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              exact (Or.elim c172 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (h12 r3)))))))))
                            )
                            (fun h9 => by
                              have h6 : p6 := (Or.elim c155 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                              have h8 : p8 := (Or.elim c160 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                              have h11 : p11 := (Or.elim c162 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => r3))))))))
                              exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                            )
                        )
                        (fun h7 => by
                          have h6 : p6 := (Or.elim c153 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h7 r3))))))))))
                          have h8 : p8 := (Or.elim c157 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                          have h11 : p11 := (Or.elim c159 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                          exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                        )
                    )
                )
                (fun h3 => by
                  exact (Classical.em p7).elim
                    (fun h7 => by
                      exact (Classical.em p9).elim
                        (fun h9 => by
                          have h8 : ¬p8 := (Or.elim c053 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h9))))))
                          have h10 : ¬p10 := (Or.elim c057 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                          have h12 : ¬p12 := (Or.elim c058 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                          exact (Or.elim c149 (fun x0 => (h2 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (h12 r3)))))))))
                        )
                        (fun h9 => by
                          have h6 : p6 := (Or.elim c132 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                          have h8 : p8 := (Or.elim c137 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                          have h11 : p11 := (Or.elim c139 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => r3))))))))
                          exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                        )
                    )
                    (fun h7 => by
                      have h6 : p6 := (Or.elim c130 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h7 r3))))))))))
                      have h8 : p8 := (Or.elim c134 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                      have h11 : p11 := (Or.elim c136 (fun x0 => (False.elim (h2 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                      exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                    )
                )
            )
        )
    )
    (fun h1 => by
      exact (Classical.em p2).elim
        (fun h2 => by
          exact (Classical.em p5).elim
            (fun h5 => by
              have h6 : ¬p6 := (Or.elim c027 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              have h7 : ¬p7 := (Or.elim c028 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              have h8 : ¬p8 := (Or.elim c029 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              have h9 : ¬p9 := (Or.elim c030 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              have h11 : ¬p11 := (Or.elim c031 (fun x0 => (False.elim (x0 h2))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h5))) (fun r1 => r1))))
              exact (Or.elim c188 (fun x0 => (h6 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h7 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (h11 r3)))))))))
            )
            (fun h5 => by
              exact (Classical.em p3).elim
                (fun h3 => by
                  exact (Classical.em p4).elim
                    (fun h4 => by
                      have h6 : ¬p6 := (Or.elim c032 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h7 : ¬p7 := (Or.elim c033 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h8 : ¬p8 := (Or.elim c034 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h9 : ¬p9 := (Or.elim c035 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      have h11 : ¬p11 := (Or.elim c036 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                      exact (Or.elim c188 (fun x0 => (h6 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h7 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (h11 r3)))))))))
                    )
                    (fun h4 => by
                      exact (Classical.em p7).elim
                        (fun h7 => by
                          exact (Classical.em p9).elim
                            (fun h9 => by
                              have h8 : ¬p8 := (Or.elim c053 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h9))))))
                              have h10 : ¬p10 := (Or.elim c057 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              have h12 : ¬p12 := (Or.elim c058 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                              exact (Or.elim c124 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (h12 r3)))))))))
                            )
                            (fun h9 => by
                              have h6 : p6 := (Or.elim c107 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                              have h8 : p8 := (Or.elim c112 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                              have h11 : p11 := (Or.elim c114 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => r3))))))))
                              exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                            )
                        )
                        (fun h7 => by
                          have h6 : p6 := (Or.elim c105 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h7 r3))))))))))
                          have h8 : p8 := (Or.elim c109 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                          have h11 : p11 := (Or.elim c111 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h4 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                          exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                        )
                    )
                )
                (fun h3 => by
                  exact (Classical.em p7).elim
                    (fun h7 => by
                      exact (Classical.em p9).elim
                        (fun h9 => by
                          have h8 : ¬p8 := (Or.elim c053 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h9))))))
                          have h10 : ¬p10 := (Or.elim c057 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                          have h12 : ¬p12 := (Or.elim c058 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                          exact (Or.elim c101 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (h12 r3)))))))))
                        )
                        (fun h9 => by
                          have h6 : p6 := (Or.elim c084 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                          have h8 : p8 := (Or.elim c089 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                          have h11 : p11 := (Or.elim c091 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => r3))))))))
                          exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                        )
                    )
                    (fun h7 => by
                      have h6 : p6 := (Or.elim c082 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h7 r3))))))))))
                      have h8 : p8 := (Or.elim c086 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                      have h11 : p11 := (Or.elim c088 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h3 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h5 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                      exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                    )
                )
            )
        )
        (fun h2 => by
          exact (Classical.em p3).elim
            (fun h3 => by
              exact (Classical.em p4).elim
                (fun h4 => by
                  have h6 : ¬p6 := (Or.elim c032 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h7 : ¬p7 := (Or.elim c033 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h8 : ¬p8 := (Or.elim c034 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h9 : ¬p9 := (Or.elim c035 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  have h11 : ¬p11 := (Or.elim c036 (fun x0 => (False.elim (x0 h3))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h4))) (fun r1 => r1))))
                  exact (Or.elim c188 (fun x0 => (h6 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h7 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h9 x3)) (fun r3 => (h11 r3)))))))))
                )
                (fun h4 => by
                  exact (Classical.em p7).elim
                    (fun h7 => by
                      exact (Classical.em p9).elim
                        (fun h9 => by
                          have h8 : ¬p8 := (Or.elim c053 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h9))))))
                          have h10 : ¬p10 := (Or.elim c057 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                          have h12 : ¬p12 := (Or.elim c058 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                          exact (Or.elim c124 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h4 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (h12 r3)))))))))
                        )
                        (fun h9 => by
                          have h6 : p6 := (Or.elim c071 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                          have h8 : p8 := (Or.elim c076 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                          have h11 : p11 := (Or.elim c078 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => r3))))))))
                          exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                        )
                    )
                    (fun h7 => by
                      have h6 : p6 := (Or.elim c069 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h7 r3))))))))))
                      have h8 : p8 := (Or.elim c073 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                      have h11 : p11 := (Or.elim c075 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h4 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                      exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                    )
                )
            )
            (fun h3 => by
              exact (Classical.em p7).elim
                (fun h7 => by
                  exact (Classical.em p9).elim
                    (fun h9 => by
                      have h8 : ¬p8 := (Or.elim c053 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => x1) (fun r1 => (False.elim (r1 h9))))))
                      have h10 : ¬p10 := (Or.elim c057 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                      have h12 : ¬p12 := (Or.elim c058 (fun x0 => (False.elim (x0 h7))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (x1 h9))) (fun r1 => r1))))
                      exact (Or.elim c101 (fun x0 => (h1 x0)) (fun r0 => (Or.elim r0 (fun x1 => (h3 x1)) (fun r1 => (Or.elim r1 (fun x2 => (h8 x2)) (fun r2 => (Or.elim r2 (fun x3 => (h10 x3)) (fun r3 => (h12 r3)))))))))
                    )
                    (fun h9 => by
                      have h6 : p6 := (Or.elim c061 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                      have h8 : p8 := (Or.elim c066 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h9 r3))))))))))
                      have h11 : p11 := (Or.elim c068 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h9 x3))) (fun r3 => r3))))))))
                      exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                    )
                )
                (fun h7 => by
                  have h6 : p6 := (Or.elim c059 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => x3) (fun r3 => (False.elim (h7 r3))))))))))
                  have h8 : p8 := (Or.elim c063 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                  have h11 : p11 := (Or.elim c065 (fun x0 => (False.elim (h1 x0))) (fun r0 => (Or.elim r0 (fun x1 => (False.elim (h2 x1))) (fun r1 => (Or.elim r1 (fun x2 => (False.elim (h3 x2))) (fun r2 => (Or.elim r2 (fun x3 => (False.elim (h7 x3))) (fun r3 => r3))))))))
                  exact (Or.elim c051 (fun x0 => (x0 h6)) (fun r0 => (Or.elim r0 (fun x1 => (x1 h8)) (fun r1 => (r1 h11)))))
                )
            )
        )
    )

/-- The full original formula implies the refuted subset. -/
theorem terminal_unsat_prop (p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 : Prop)
    (h : terminalFormula p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12) : False := by
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
  have c017 := tail16.1
  have tail17 := tail16.2
  have c018 := tail17.1
  have tail18 := tail17.2
  have c019 := tail18.1
  have tail19 := tail18.2
  have c020 := tail19.1
  have tail20 := tail19.2
  have c021 := tail20.1
  have tail21 := tail20.2
  have c022 := tail21.1
  have tail22 := tail21.2
  have c023 := tail22.1
  have tail23 := tail22.2
  have c024 := tail23.1
  have tail24 := tail23.2
  have c025 := tail24.1
  have tail25 := tail24.2
  have c026 := tail25.1
  have tail26 := tail25.2
  have c027 := tail26.1
  have tail27 := tail26.2
  have c028 := tail27.1
  have tail28 := tail27.2
  have c029 := tail28.1
  have tail29 := tail28.2
  have c030 := tail29.1
  have tail30 := tail29.2
  have c031 := tail30.1
  have tail31 := tail30.2
  have c032 := tail31.1
  have tail32 := tail31.2
  have c033 := tail32.1
  have tail33 := tail32.2
  have c034 := tail33.1
  have tail34 := tail33.2
  have c035 := tail34.1
  have tail35 := tail34.2
  have c036 := tail35.1
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
  have c051 := tail50.1
  have tail51 := tail50.2
  have tail52 := tail51.2
  have c053 := tail52.1
  have tail53 := tail52.2
  have tail54 := tail53.2
  have tail55 := tail54.2
  have tail56 := tail55.2
  have c057 := tail56.1
  have tail57 := tail56.2
  have c058 := tail57.1
  have tail58 := tail57.2
  have c059 := tail58.1
  have tail59 := tail58.2
  have tail60 := tail59.2
  have c061 := tail60.1
  have tail61 := tail60.2
  have tail62 := tail61.2
  have c063 := tail62.1
  have tail63 := tail62.2
  have tail64 := tail63.2
  have c065 := tail64.1
  have tail65 := tail64.2
  have c066 := tail65.1
  have tail66 := tail65.2
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
  have tail74 := tail73.2
  have c075 := tail74.1
  have tail75 := tail74.2
  have c076 := tail75.1
  have tail76 := tail75.2
  have tail77 := tail76.2
  have c078 := tail77.1
  have tail78 := tail77.2
  have tail79 := tail78.2
  have tail80 := tail79.2
  have tail81 := tail80.2
  have c082 := tail81.1
  have tail82 := tail81.2
  have tail83 := tail82.2
  have c084 := tail83.1
  have tail84 := tail83.2
  have tail85 := tail84.2
  have c086 := tail85.1
  have tail86 := tail85.2
  have tail87 := tail86.2
  have c088 := tail87.1
  have tail88 := tail87.2
  have c089 := tail88.1
  have tail89 := tail88.2
  have tail90 := tail89.2
  have c091 := tail90.1
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
  have c105 := tail104.1
  have tail105 := tail104.2
  have tail106 := tail105.2
  have c107 := tail106.1
  have tail107 := tail106.2
  have tail108 := tail107.2
  have c109 := tail108.1
  have tail109 := tail108.2
  have tail110 := tail109.2
  have c111 := tail110.1
  have tail111 := tail110.2
  have c112 := tail111.1
  have tail112 := tail111.2
  have tail113 := tail112.2
  have c114 := tail113.1
  have tail114 := tail113.2
  have tail115 := tail114.2
  have tail116 := tail115.2
  have tail117 := tail116.2
  have tail118 := tail117.2
  have tail119 := tail118.2
  have tail120 := tail119.2
  have tail121 := tail120.2
  have tail122 := tail121.2
  have tail123 := tail122.2
  have c124 := tail123.1
  have tail124 := tail123.2
  have tail125 := tail124.2
  have tail126 := tail125.2
  have tail127 := tail126.2
  have tail128 := tail127.2
  have tail129 := tail128.2
  have c130 := tail129.1
  have tail130 := tail129.2
  have tail131 := tail130.2
  have c132 := tail131.1
  have tail132 := tail131.2
  have tail133 := tail132.2
  have c134 := tail133.1
  have tail134 := tail133.2
  have tail135 := tail134.2
  have c136 := tail135.1
  have tail136 := tail135.2
  have c137 := tail136.1
  have tail137 := tail136.2
  have tail138 := tail137.2
  have c139 := tail138.1
  have tail139 := tail138.2
  have tail140 := tail139.2
  have tail141 := tail140.2
  have tail142 := tail141.2
  have tail143 := tail142.2
  have tail144 := tail143.2
  have tail145 := tail144.2
  have tail146 := tail145.2
  have tail147 := tail146.2
  have tail148 := tail147.2
  have c149 := tail148.1
  have tail149 := tail148.2
  have tail150 := tail149.2
  have tail151 := tail150.2
  have tail152 := tail151.2
  have c153 := tail152.1
  have tail153 := tail152.2
  have tail154 := tail153.2
  have c155 := tail154.1
  have tail155 := tail154.2
  have tail156 := tail155.2
  have c157 := tail156.1
  have tail157 := tail156.2
  have tail158 := tail157.2
  have c159 := tail158.1
  have tail159 := tail158.2
  have c160 := tail159.1
  have tail160 := tail159.2
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
  have c172 := tail171.1
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
  have tail184 := tail183.2
  have tail185 := tail184.2
  have tail186 := tail185.2
  have tail187 := tail186.2
  have c188 := tail187.1
  have tail188 := tail187.2
  have tail189 := tail188.2
  have tail190 := tail189.2
  have tail191 := tail190.2
  exact core_unsat p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12
    c017 c018 c019 c020 c021 c022 c023 c024 c025 c026 c027 c028 c029 c030 c031 c032 c033 c034 c035 c036 c051 c053 c057 c058 c059 c061 c063 c065 c066 c068 c069 c071 c073 c075 c076 c078 c082 c084 c086 c088 c089 c091 c101 c105 c107 c109 c111 c112 c114 c124 c130 c132 c134 c136 c137 c139 c149 c153 c155 c157 c159 c160 c162 c172 c188

/-- The fixed CNF interpreted on twelve Boolean membership values. -/
def terminalBoolFormula (b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 : Bool) : Prop :=
  terminalFormula (b1 = true) (b2 = true) (b3 = true) (b4 = true) (b5 = true) (b6 = true) (b7 = true) (b8 = true) (b9 = true) (b10 = true) (b11 = true) (b12 = true)

/-- No assignment of the twelve Boolean values satisfies the fixed CNF. -/
theorem terminal_unsat_bool (b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 : Bool) :
    ¬terminalBoolFormula b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 :=
  fun h => terminal_unsat_prop (b1 = true) (b2 = true) (b3 = true) (b4 = true) (b5 = true) (b6 = true) (b7 = true) (b8 = true) (b9 = true) (b10 = true) (b11 = true) (b12 = true) h

#print axioms core_unsat
#print axioms terminal_unsat_prop
#print axioms terminal_unsat_bool

end Delta3.T12Boolean
