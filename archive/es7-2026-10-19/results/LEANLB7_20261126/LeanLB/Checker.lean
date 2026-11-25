/-!
# A kernel-evaluable checker for "no `B + 2` points in convex position"

Points are pairs of natural numbers (lattice coordinates after a translation). Everything the kernel
evaluates uses only `Nat` primitives (`Nat.mul`, `Nat.add`, `Nat.blt`, `Nat.beq`), `Bool` and
structural recursion on lists.

For every anchor `p` of the list `L`:
* `above p` keeps the points that are larger than `p` in the order (second coordinate, first
  coordinate);
* `isort p` sorts them by insertion with the comparison `opos p a b` (counterclockwise order around
  `p`), and `pwOK` checks that the sorted list is pairwise counterclockwise around `p`;
* `runDP` computes, for every pair `(x, y)` of the sorted list, the length of the longest chain
  `… , x, y` of the list (in list order) whose consecutive triples all turn left; it fails as soon as
  a value exceeds the bound `B`.

The soundness theorem is `LeanLB.card_le_of_check` in `LeanLB/CheckerSound.lean`.
-/

namespace LeanLB

/-- A lattice point with natural-number coordinates. -/
abbrev NP := Nat × Nat

/-- `opos a b c` is `true` iff the orientation determinant of `a, b, c` is positive
(counterclockwise turn). Shoelace form: `a₀b₁ + b₀c₁ + c₀a₁ > a₁b₀ + b₁c₀ + c₁a₀`. -/
def opos (a b c : NP) : Bool :=
  Nat.blt (a.2 * b.1 + b.2 * c.1 + c.2 * a.1) (a.1 * b.2 + b.1 * c.2 + c.1 * a.2)

/-- Strict order by (second coordinate, first coordinate). -/
def above (p q : NP) : Bool :=
  Nat.blt p.2 q.2 || (Nat.beq p.2 q.2 && Nat.blt p.1 q.1)

/-- Maximum of two naturals, with `Nat.blt`. -/
def nmax (a b : Nat) : Nat := bif Nat.blt a b then b else a

/-- Insertion into a list sorted counterclockwise around `p`. -/
def ins (p a : NP) : List NP → List NP
  | [] => [a]
  | b :: l => bif opos p a b then a :: b :: l else b :: ins p a l

/-- Insertion sort, counterclockwise around `p`. -/
def isort (p : NP) : List NP → List NP
  | [] => []
  | a :: l => ins p a (isort p l)

/-- Every earlier element of the list is counterclockwise-before every later one, around `p`. -/
def pwOK (p : NP) : List NP → Bool
  | [] => true
  | a :: l => l.all (fun b => opos p a b) && pwOK p l

/-- `bestIn b c d r`: the maximum of `d` and of the values `v` of the entries `(x, v)` of `r` with a
left turn `x, b, c`. -/
def bestIn (b c : NP) (d : Nat) : List (NP × Nat) → Nat
  | [] => d
  | e :: r => bestIn b c (bif opos e.1 b c then nmax d e.2 else d) r

/-- The row of a new point `c`: for each earlier point `b` (with its row `rb`), the entry
`(b, 1 + bestIn b c 1 rb)`. -/
def newRow (c : NP) : List (NP × List (NP × Nat)) → List (NP × Nat)
  | [] => []
  | e :: rs => (e.1, bestIn e.1 c 1 e.2 + 1) :: newRow c rs

/-- Every value of a row is at most `B`. -/
def rowLe (B : Nat) : List (NP × Nat) → Bool
  | [] => true
  | e :: r => Nat.ble e.2 B && rowLe B r

/-- The dynamic programme over a list, processed left to right. -/
def runDP (B : Nat) : List NP → List (NP × List (NP × Nat)) → Bool
  | [], _ => true
  | c :: cs, rows => rowLe B (newRow c rows) && runDP B cs ((c, newRow c rows) :: rows)

/-- The check for one anchor. -/
def anchorOK (B : Nat) (L : List NP) (p : NP) : Bool :=
  pwOK p (isort p (L.filter (above p))) && runDP B (isort p (L.filter (above p))) []

/-- The check for all anchors. -/
def checkAll (B : Nat) (L : List NP) : Bool :=
  L.all (anchorOK B L)

/-- The check for the anchors at positions `a, …, b - 1` of `L` (to split the kernel evaluation into
declarations of bounded size). -/
def checkFrom (B : Nat) (L : List NP) (a b : Nat) : Bool :=
  ((L.drop a).take (b - a)).all (anchorOK B L)

/-- No three distinct points of the list are collinear: `oz a b c ≠ 0` for all triples of distinct
positions, in Boolean form. `nz a b c` is `true` iff the two shoelace sums differ. -/
def nz (a b c : NP) : Bool :=
  !(Nat.beq (a.2 * b.1 + b.2 * c.1 + c.2 * a.1) (a.1 * b.2 + b.1 * c.2 + c.1 * a.2))

/-- Pairwise distinct points and every triple (in list order) non-collinear. -/
def gpOK : List NP → Bool
  | [] => true
  | a :: l => l.all (fun b => !(Nat.beq a.1 b.1 && Nat.beq a.2 b.2)) &&
      gpPairs a l && gpOK l
where
  gpPairs (a : NP) : List NP → Bool
    | [] => true
    | b :: l => l.all (fun c => nz a b c) && gpPairs a l

end LeanLB
