import MirrorEncoding.CoverCore

/-!
# Splitting the kernel cover check

`decide +kernel` on `coverCheck` of one large leaf list exhausts memory (one case has about
18,000 leaves). These lemmas let a generated proof follow the recursion of `Mir.coverAux` for
its top levels, so that the kernel only evaluates the subtrees, each in its own declaration.
-/

namespace V2L

open Mir

/-- The cube list after restricting to the literals of `path`, in order. -/
def restrictPath (path : List Int) (cubes : List (List Int)) : List (List Int) :=
  path.foldl (fun cs z => restrict z cs) cubes

theorem restrictPath_append (path : List Int) (z : Int) (cubes : List (List Int)) :
    restrictPath (path ++ [z]) cubes = restrict z (restrictPath path cubes) := by
  simp [restrictPath, List.foldl_append]

/-- One step of `coverAux`: split on the first literal `z` of the first cube. -/
theorem coverAux_step {n : Nat} {cubes : List (List Int)} {z : Int}
    (hz : (cubes.head?.bind List.head?) = some z) (hz0 : z ≠ 0)
    (h1 : coverAux n (restrict z cubes) = true) (h2 : coverAux n (restrict (-z) cubes) = true) :
    coverAux (n + 1) cubes = true := by
  match cubes, hz with
  | (z' :: c) :: tl, hz =>
    simp only [List.head?_cons, Option.bind_some, Option.some.injEq] at hz
    subst hz
    simp only [coverAux]
    split
    · rfl
    · simp [hz0, h1, h2]

theorem coverAux_path {n : Nat} {path : List Int} {cubes : List (List Int)} {z : Int}
    (hz : ((restrictPath path cubes).head?.bind List.head?) = some z) (hz0 : z ≠ 0)
    (h1 : coverAux n (restrictPath (path ++ [z]) cubes) = true)
    (h2 : coverAux n (restrictPath (path ++ [-z]) cubes) = true) :
    coverAux (n + 1) (restrictPath path cubes) = true := by
  rw [restrictPath_append] at h1 h2
  exact coverAux_step hz hz0 h1 h2

theorem coverCheck_of_coverAux {cubes : List (List Int)} {n : Nat}
    (hn : (cubes.map List.length).sum + 1 = n) (h : coverAux n (restrictPath [] cubes) = true) :
    coverCheck cubes = true := by
  subst hn; exact h

end V2L
