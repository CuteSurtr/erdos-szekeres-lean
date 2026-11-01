import Std.Data.HashMap

/-!
# The ETV signotope CNF, generated on the Lean side

This file mirrors `tools/etv/gen_etv.py` (without `--hull`, `--mirror`, `--xsb`) loop by
loop, so that the clause list below, after numbering, is the DIMACS file written by

    python3 tools/etv/gen_etv.py N A U K -o out.cnf

Points are `0, …, N-1` here and `1, …, N` in Python. Only the order of variables matters for
the numbering, so this shift does not change the DIMACS output.

Conventions (as in the Python encoder): the variable `x i j k` (`i < j < k`) is true iff the
triple is counterclockwise, i.e. a *cup triple*; a *cap triple* is a false one. A chain type
`t : Bool` is `false` for caps and `true` for cups, so a triple of type `t` is one with
`x i j k = t`.
-/

namespace ETV

/-- Variables of the ETV encoding.
* `x i j k` : orientation of the triple `i < j < k` (true = counterclockwise = cup triple);
* `v t x a b r` : Python's `V[(x,a,b,r)]` for chains of type `t` (false = cap, true = cup):
  some `r`-point chain of type `t` starts at `x` and ends with `a, b`;
* `e t x b r` : Python's `E[(x,b,r)]`: some `r`-point chain of type `t` runs from `x` to `b`. -/
inductive Var where
  | x (i j k : Nat)
  | v (t : Bool) (x a b r : Nat)
  | e (t : Bool) (x b r : Nat)
  deriving DecidableEq, Hashable, Repr, Inhabited

/-- A literal: the variable together with its polarity (`true` = positive). -/
structure Lit where
  var : Var
  pos : Bool
  deriving DecidableEq, Repr

abbrev Clause := List Lit

def Lit.pos' (v : Var) : Lit := ⟨v, true⟩
def Lit.neg' (v : Var) : Lit := ⟨v, false⟩

open Lit

/-! ### `itertools.combinations` in lexicographic order -/

def pairs (N : Nat) : List (Nat × Nat) :=
  (List.range N).flatMap fun x => (List.range' (x + 1) (N - (x + 1))).map fun b => (x, b)

def triples (N : Nat) : List (Nat × Nat × Nat) :=
  (List.range N).flatMap fun i =>
    (List.range' (i + 1) (N - (i + 1))).flatMap fun j =>
      (List.range' (j + 1) (N - (j + 1))).map fun k => (i, j, k)

def quads (N : Nat) : List (Nat × Nat × Nat × Nat) :=
  (List.range N).flatMap fun i =>
    (List.range' (i + 1) (N - (i + 1))).flatMap fun j =>
      (List.range' (j + 1) (N - (j + 1))).flatMap fun k =>
        (List.range' (k + 1) (N - (k + 1))).map fun l => (i, j, k, l)

/-! ### Signotope clauses -/

/-- Forbid the patterns `+-+` and `-+-` on three of the four triples of a quadruple. -/
def tri3 (a b c : Var) : List Clause :=
  [[neg' a, pos' b, neg' c], [pos' a, neg' b, pos' c]]

/-- The eight clauses of a quadruple `i<j<k<l`, with `s = [ijk, ijl, ikl, jkl]` and the
position triples `(0,1,2), (0,1,3), (0,2,3), (1,2,3)` in Python's order. -/
def sig4 (a b c d : Var) : List Clause :=
  tri3 a b c ++ tri3 a b d ++ tri3 a c d ++ tri3 b c d

def signotopeClauses (N : Nat) : List Clause :=
  (quads N).flatMap fun (i, j, k, l) => sig4 (.x i j k) (.x i j l) (.x i k l) (.x j k l)

/-! ### Cap and cup clauses (`kind`, `sgn`, `B`) = (`cap`, -1, A) and (`cup`, +1, U) -/

/-- The triple literal `lit = sgn * X[(i,j,k)]` of the Python encoder: true iff the triple
has type `t`. -/
def tlit (t : Bool) (i j k : Nat) : Lit := ⟨.x i j k, t⟩

/-- Python's `-lit`. -/
def ntlit (t : Bool) (i j k : Nat) : Lit := ⟨.x i j k, !t⟩

/-- Keys of the dictionary `V`, in insertion order. -/
def vKeys (B N : Nat) : List (Nat × Nat × Nat × Nat) :=
  (triples N).flatMap fun (x, a, b) =>
    (List.range' 3 (B - 3)).filterMap fun r =>
      if r ≤ a - x + 2 then some (x, a, b, r) else none

/-- Keys of the dictionary `E`, in insertion order. -/
def eKeys (B N : Nat) : List (Nat × Nat × Nat) :=
  (pairs N).flatMap fun (x, b) =>
    (List.range' 3 (B - 3)).filterMap fun r =>
      if r ≤ b - x + 1 then some (x, b, r) else none

/-- `-lit ∨ V[(x,a,b,3)]` (or `-lit` alone when `B ≤ 3`). -/
def baseClauses (t : Bool) (B N : Nat) : List Clause :=
  (triples N).map fun (x, a, b) =>
    if 3 < B then [ntlit t x a b, pos' (.v t x a b 3)] else [ntlit t x a b]

/-- Extension clauses `V[(x,w,a,r-1)] ∧ lit(w,a,b) → V[(x,a,b,r)]`, and the forbidden
`B`-chain clauses for `r = B`. -/
def extClauses (t : Bool) (B N : Nat) : List Clause :=
  (quads N).flatMap fun (x, w, a, b) =>
    (List.range' 4 (B + 1 - 4)).filterMap fun r =>
      if r ≤ w - x + 3 then
        some (if r < B then [neg' (.v t x w a (r - 1)), ntlit t w a b, pos' (.v t x a b r)]
          else [neg' (.v t x w a (r - 1)), ntlit t w a b])
      else none

/-- End flags and monotonicity of `V`. -/
def vClauses (t : Bool) (B N : Nat) : List Clause :=
  (vKeys B N).flatMap fun (x, a, b, r) =>
    [neg' (.v t x a b r), pos' (.e t x b r)] ::
      (if 4 ≤ r then [[neg' (.v t x a b r), pos' (.v t x a b (r - 1))]] else [])

/-- Monotonicity of `E`. -/
def eClauses (t : Bool) (B N : Nat) : List Clause :=
  (eKeys B N).filterMap fun (x, b, r) =>
    if 4 ≤ r then some [neg' (.e t x b r), pos' (.e t x b (r - 1))] else none

def chainClauses (t : Bool) (B N : Nat) : List Clause :=
  baseClauses t B N ++ extClauses t B N ++ vClauses t B N ++ eClauses t B N

/-- The K-gon clauses `-CapE(x,b,r) ∨ -CupE(x,b,s)` with `r + s = K + 2`. -/
def gonClauses (N A U K : Nat) : List Clause :=
  (pairs N).flatMap fun (x, b) =>
    (List.range' 3 (A - 3)).filterMap fun r =>
      if 3 ≤ K + 2 - r ∧ K + 2 - r < U ∧ r ≤ b - x + 1 ∧ K + 2 - r ≤ b - x + 1 then
        some [neg' (.e false x b r), neg' (.e true x b (K + 2 - r))]
      else none

/-- The whole clause list of `gen_etv.py N A U K`, in the Python order. -/
def etvClauses (N A U K : Nat) : List Clause :=
  signotopeClauses N ++ chainClauses false A N ++ chainClauses true U N ++ gonClauses N A U K

/-! ### Numbering: the order in which Python calls `new()` -/

def allVars (N A U : Nat) : List Var :=
  (triples N).map (fun (i, j, k) => Var.x i j k) ++
  (vKeys A N).map (fun (x, a, b, r) => Var.v false x a b r) ++
  (eKeys A N).map (fun (x, b, r) => Var.e false x b r) ++
  (vKeys U N).map (fun (x, a, b, r) => Var.v true x a b r) ++
  (eKeys U N).map (fun (x, b, r) => Var.e true x b r)

/-- One step of `new()`: give `v` the next number unless it already has one. -/
def numberStep (p : Std.HashMap Var Nat × Nat) (v : Var) : Std.HashMap Var Nat × Nat :=
  (p.1.insertIfNew v p.2, p.2 + 1)

/-- Map each variable to `1 + ` its first position in the list. -/
def numberMap (l : List Var) : Std.HashMap Var Nat :=
  (l.foldl numberStep (∅, 1)).1

def litToInt (m : Std.HashMap Var Nat) (l : Lit) : Int :=
  if l.pos then (m.getD l.var 0 : Int) else -(m.getD l.var 0 : Int)

/-- The DIMACS clauses (without the header and the trailing zeros). -/
def dimacs (N A U K : Nat) : List (List Int) :=
  let m := numberMap (allVars N A U)
  (etvClauses N A U K).map fun c => c.map (litToInt m)

/-- The clauses of `gen_etv.py N A U K --xsb`: the base clauses followed by the x-reflection
lex-leader clause `-X(1,2,3) ∨ X(N-2,N-1,N)` (variables numbered as in `dimacs`). -/
def dimacsXsb (N A U K : Nat) : List (List Int) :=
  let m := numberMap (allVars N A U)
  dimacs N A U K ++ [[-(m.getD (.x 0 1 2) 0 : Int), (m.getD (.x (N - 3) (N - 2) (N - 1)) 0 : Int)]]

/-- Number of variables in the header `p cnf nv nc`. -/
def numVars (N A U : Nat) : Nat := (allVars N A U).length

end ETV
