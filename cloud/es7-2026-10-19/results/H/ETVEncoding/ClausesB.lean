import ETVEncoding.Clauses

/-!
# The track-B CNF (`tools/trackB/gen_cnf.py N K`), generated on the Lean side

`gen_cnf.py N K` is the ETV CNF with `A = U = K`, with two differences: the end-flag and
monotonicity clauses come in a different order, and there are optional symmetry-breaking
clauses (`--hull`, `--mirror`, `--flip`) and an option to omit monotonicity (`--no-mono`).
The variables, and so the numbering, are those of `gen_etv.py N K K K`.

Points are `0, …, N-1` here and `1, …, N` in Python, so Python's `X(1,i,j)` is `x 0 (i-1) (j-1)`.
-/

namespace ETV

open Lit

/-- End flags `V[(x,a,b,r)] → E[(x,b,r)]`, all at once (`gen_cnf.py` order). -/
def endClauses (t : Bool) (B N : Nat) : List Clause :=
  (vKeys B N).map fun (x, a, b, r) => [neg' (.v t x a b r), pos' (.e t x b r)]

/-- Monotonicity of `V`, all at once (`gen_cnf.py` order). -/
def vMonoClauses (t : Bool) (B N : Nat) : List Clause :=
  (vKeys B N).filterMap fun (x, a, b, r) =>
    if 4 ≤ r then some [neg' (.v t x a b r), pos' (.v t x a b (r - 1))] else none

def chainClausesB (t : Bool) (K N : Nat) (mono : Bool) : List Clause :=
  baseClauses t K N ++ extClauses t K N ++ endClauses t K N ++
    (if mono then vMonoClauses t K N ++ eClauses t K N else [])

/-- `--hull`: the unit clauses `X(1,i,j)` for `2 ≤ i < j ≤ N` (Python numbering). -/
def hullClauses (N : Nat) : List Clause :=
  (pairs N).filterMap fun (i, j) => if 1 ≤ i then some [pos' (.x 0 i j)] else none

/-- `--mirror` (with `--hull`, only for `N ≥ 7`): `-X(2,3,4) ∨ X(N-2,N-1,N)`. -/
def mirrorClausesB (N : Nat) : List Clause :=
  if 7 ≤ N then [[neg' (.x 1 2 3), pos' (.x (N - 3) (N - 2) (N - 1))]] else []

/-- `--flip`: the unit clause `X(1,2,3)`. -/
def flipClauses : List Clause := [[pos' (.x 0 1 2)]]

/-- The whole clause list of `gen_cnf.py N K` with the given options, in the Python order. -/
def trackBClauses (N K : Nat) (hull mirror flip mono : Bool) : List Clause :=
  signotopeClauses N ++ chainClausesB false K N mono ++ chainClausesB true K N mono ++
    gonClauses N K K K ++
    ((if hull then hullClauses N else []) ++ (if mirror then mirrorClausesB N else []) ++
      (if flip then flipClauses else []))

/-- The DIMACS clauses of `gen_cnf.py N K` (numbering of `gen_etv.py N K K K`). -/
def dimacsB (N K : Nat) (hull mirror flip mono : Bool) : List (List Int) :=
  let m := numberMap (allVars N K K)
  (trackBClauses N K hull mirror flip mono).map fun c => c.map (litToInt m)

end ETV
