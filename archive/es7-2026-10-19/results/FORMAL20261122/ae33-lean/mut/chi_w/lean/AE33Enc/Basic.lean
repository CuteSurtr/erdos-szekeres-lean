/-!
# AE33Enc.Basic: integer points, orientation signs, the variable numbering and `chi` (Std-only)

Port of l2enc.cpp (`ref/l2enc.cpp`, SHA-256 `171a3e7c…`) lines 45-77: `orient3`, `var`, `chi`.

Elements `0..n-1` are the base points, `n` is the new point p, `n+1` the new point q. Variables (l2enc.cpp:6-9):
`X(a,b) = pvar n a b`, `Y(a,b) = n2 n + pvar n a b`, `W(a) = 2·n2 n + 1 + a`; `X` true ⟺ orient(a,b,p) > 0,
`Y` true ⟺ orient(a,b,q) > 0, `W` true ⟺ orient(a,p,q) > 0.
-/

namespace AE33

abbrev Pt := Int × Int

/-- Twice the signed area (l2enc `orient3` before the sign). -/
def iorient (a b c : Pt) : Int := (b.1 - a.1) * (c.2 - a.2) - (b.2 - a.2) * (c.1 - a.1)

def isgn (x : Int) : Int := if 0 < x then 1 else if x < 0 then -1 else 0

/-- Orientation sign of three base points, by index (out of range: the point (0,0)). -/
def osgn (B : Array Pt) (i j k : Nat) : Int :=
  isgn (iorient (B.getD i (0, 0)) (B.getD j (0, 0)) (B.getD k (0, 0)))

def n2 (n : Nat) : Nat := n * (n - 1) / 2

/-- l2enc `var(a, b)` for `a < b`: one plus the lexicographic rank of the pair. -/
def pvar (n a b : Nat) : Nat := a * n - a * (a + 1) / 2 + (b - a - 1) + 1

def numVarsN (n : Nat) : Nat := 2 * n2 n + n

def numVars (B : Array Pt) : Nat := numVarsN B.size

/-- A value of l2enc's `chi`: a constant sign (three base points) or a signed DIMACS literal. -/
inductive Term where
  | const (s : Int)
  | lit (l : Int)
  deriving Inhabited, BEq, Repr, DecidableEq

def Term.neg : Term → Term
  | .const s => .const (-s)
  | .lit l => .lit (-l)

/-- l2enc's bubble sort of a triple with its permutation sign (compare-swap at (0,1), (1,2), (0,1)). -/
def sort3 (i j k : Nat) : Nat × Nat × Nat × Int :=
  let r1 : Nat × Nat × Int := if i > j then (j, i, -1) else (i, j, 1)
  let r2 : Nat × Nat × Int := if r1.2.1 > k then (k, r1.2.1, -r1.2.2) else (r1.2.1, k, r1.2.2)
  let r3 : Nat × Nat × Int := if r1.1 > r2.1 then (r2.1, r1.1, -r2.2.2) else (r1.1, r2.1, r2.2.2)
  (r3.1, r3.2.1, r2.2.1, r3.2.2)

/-- l2enc `chi(i, j, k)`: the literal of "orient(i, j, k) > 0", or its constant sign for three base points.
(l2enc dies on repeated or invalid triples; here such inputs give some value and `clauseOf` never asks for them.) -/
def chi (B : Array Pt) (i j k : Nat) : Term :=
  let n := B.size
  let s := sort3 i j k
  if s.2.2.1 < n then .const (osgn B i j k)
  else if s.2.1 < n then
    .lit (s.2.2.2 * ((pvar n s.1 s.2.1 + (if s.2.2.1 = n then 0 else n2 n) : Nat) : Int))
  else .lit (-s.2.2.2 * ((2 * n2 n + 1 + s.1 : Nat) : Int))

end AE33
