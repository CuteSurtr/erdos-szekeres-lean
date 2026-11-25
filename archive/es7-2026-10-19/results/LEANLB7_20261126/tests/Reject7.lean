import LeanLB.Check.C2N32
import LeanLB.Check.C5N31

/-! Rejection tests (not part of the build; run with `lake env lean tests/Reject7.lean`). Each
`decide +kernel` below must fail: the checks are not vacuous. Expected: four errors. -/

namespace LeanLB

set_option maxRecDepth 100000

/-- Every set of 17 points in general position has a convex hexagon (ES(6) = 17), so the bound
`B = 4` (no 6-gon) must fail on the 32-point half-turn set. -/
example : checkAll 4 c2N32Nat = true := by decide +kernel

/-- Three collinear points put in front of the list must break general position. -/
example : gpOK ((0, 0) :: (1, 1) :: (2, 2) :: c2N32Nat) = true := by decide +kernel

/-- A wrong approximation (first coordinate off by 2) must fail its certificate. -/
example : ((c5N31L.take 1).map (fun p => (p.1, (p.2.1 + 2, p.2.2)))).all
    (G.certOK G.lo5 G.D5 c5N31Sc c5N31Shift.1 c5N31Shift.2 c5N31Mx) = true := by decide +kernel

/-- The 5-fold set has convex hexagons, so `B = 4` must fail there too. -/
example : G.checkAll (G.opA (8 * c5N31Mx + 8)) (G.abA 1 (2 + 2 * 1)) 4 c5N31L = true := by
  decide +kernel

end LeanLB
