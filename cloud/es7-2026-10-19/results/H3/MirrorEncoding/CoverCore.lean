/-!
# The cube-cover check (definitions only)

Kept free of Mathlib so that `cover_check` builds quickly; the soundness proof is in
`Cover.lean` (`Mir.covers_of_coverCheck`).
-/

namespace Mir

/-- Restrict the cube list to the assignments where `z` holds: drop the cubes containing
`-z`, and delete `z` from the others. -/
def restrict (z : Int) (cubes : List (List Int)) : List (List Int) :=
  cubes.filterMap fun c => if c.contains (-z) then none else some (c.filter (· != z))

/-- The cover check with fuel. -/
def coverAux : Nat → List (List Int) → Bool
  | 0, _ => false
  | fuel + 1, cubes =>
    if cubes.any List.isEmpty then true
    else match cubes with
      | [] => false
      | [] :: _ => true
      | (z :: _) :: _ =>
        z != 0 && coverAux fuel (restrict z cubes) && coverAux fuel (restrict (-z) cubes)

/-- Every split removes at least one literal occurrence, so the total length plus one is
enough fuel for tree-shaped inputs. -/
def coverCheck (cubes : List (List Int)) : Bool :=
  coverAux ((cubes.map List.length).sum + 1) cubes

end Mir
