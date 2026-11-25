import LeanLB.Checker

/-!
# The checker over an abstract point type

The same programme as `LeanLB/Checker.lean`, with the orientation test `op` and the order `ab` as
parameters, for points whose coordinates are not integers (5-fold and 7-fold sets: coordinates in
`ℤ[2cos(2π/m)]`). `op a b c = true` must certify a positive orientation (`LeanLB.G.lowerBound`).
-/

namespace LeanLB.G

variable {P : Type}

/-- Insertion into a list sorted counterclockwise around `p`. -/
def ins (op : P → P → P → Bool) (p a : P) : List P → List P
  | [] => [a]
  | b :: l => bif op p a b then a :: b :: l else b :: ins op p a l

/-- Insertion sort, counterclockwise around `p`. -/
def isort (op : P → P → P → Bool) (p : P) : List P → List P
  | [] => []
  | a :: l => ins op p a (isort op p l)

/-- Every earlier element of the list is counterclockwise-before every later one, around `p`. -/
def pwOK (op : P → P → P → Bool) (p : P) : List P → Bool
  | [] => true
  | a :: l => l.all (fun b => op p a b) && pwOK op p l

/-- The maximum of `d` and of the values `v` of the entries `(x, v)` of `r` with `op x b c`. -/
def bestIn (op : P → P → P → Bool) (b c : P) (d : Nat) : List (P × Nat) → Nat
  | [] => d
  | e :: r => bestIn op b c (bif op e.1 b c then nmax d e.2 else d) r

/-- The row of a new point `c`. -/
def newRow (op : P → P → P → Bool) (c : P) : List (P × List (P × Nat)) → List (P × Nat)
  | [] => []
  | e :: rs => (e.1, bestIn op e.1 c 1 e.2 + 1) :: newRow op c rs

/-- Every value of a row is at most `B`. -/
def rowLe (B : Nat) : List (P × Nat) → Bool
  | [] => true
  | e :: r => Nat.ble e.2 B && rowLe B r

/-- The dynamic programme over a list, processed left to right. -/
def runDP (op : P → P → P → Bool) (B : Nat) : List P → List (P × List (P × Nat)) → Bool
  | [], _ => true
  | c :: cs, rows => rowLe B (newRow op c rows) && runDP op B cs ((c, newRow op c rows) :: rows)

/-- The check for one anchor. -/
def anchorOK (op : P → P → P → Bool) (ab : P → P → Bool) (B : Nat) (L : List P) (p : P) : Bool :=
  pwOK op p (isort op p (L.filter (ab p))) && runDP op B (isort op p (L.filter (ab p))) []

/-- The check for all anchors. -/
def checkAll (op : P → P → P → Bool) (ab : P → P → Bool) (B : Nat) (L : List P) : Bool :=
  L.all (anchorOK op ab B L)

/-- The check for the anchors at positions `a, …, b - 1`. -/
def checkFrom (op : P → P → P → Bool) (ab : P → P → Bool) (B : Nat) (L : List P) (a b : Nat) :
    Bool :=
  ((L.drop a).take (b - a)).all (anchorOK op ab B L)

/-- Every two points (in list order) are comparable by `ab`, and every three (in list order) have a
certified orientation in one of the two orders. -/
def gpOK (op : P → P → P → Bool) (ab : P → P → Bool) : List P → Bool
  | [] => true
  | a :: l => l.all (fun b => ab a b || ab b a) && gpPairs op a l && gpOK op ab l
where
  gpPairs (op : P → P → P → Bool) (a : P) : List P → Bool
    | [] => true
    | b :: l => l.all (fun c => op a b c || op a c b) && gpPairs op a l

end LeanLB.G
