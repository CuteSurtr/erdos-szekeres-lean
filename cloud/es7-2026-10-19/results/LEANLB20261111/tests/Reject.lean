import LeanLB.Check.MirN46
import LeanLB.Check.C7N64

/-! Rejection tests (not part of the build; run with `lake env lean tests/Reject.lean`). Each
`decide +kernel` below must fail: the checks are not vacuous. Expected: three errors. -/

namespace LeanLB

set_option maxRecDepth 100000

/-- The mirror set has 7 points in convex position, so the bound `B = 5` (no 7-gon) must fail. -/
example : checkAll 5 mirN46Nat = true := by decide +kernel

/-- Moving one point onto the line through two others must break general position. -/
example : gpOK ((0, 0) :: (1, 1) :: (2, 2) :: mirN46Nat) = true := by decide +kernel

/-- A wrong approximation (first coordinate off by 2) must fail its certificate. -/
example : ((c7N64L.take 1).map (fun p => (p.1, (p.2.1 + 2, p.2.2)))).all
    (G.certOK G.lo7 G.D7 c7N64Sc c7N64Shift.1 c7N64Shift.2 c7N64Mx) = true := by decide +kernel

end LeanLB
