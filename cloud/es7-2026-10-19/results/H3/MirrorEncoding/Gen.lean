import ETVEncoding.Clauses
import Std.Data.HashSet

/-!
# The mirror CNFs of `results/C`, generated on the Lean side

`results/C/scripts/make_cnfs.sh` builds the two ES(7) mirror instances in two steps:

    gen_etv.py 33 7 7 7 --mirror --hull -o hm33k7.cnf
    mirgen.py hm33k7.cnf 33 --hull -o hm33k7.sub.cnf                    # sub-case (i)
    gen_etv.py 33 7 7 7 --mirror -o m33k7.cnf
    mirgen.py m33k7.cnf 33 --interior --yflip-unit -o m33k7int.sub.cnf  # sub-case (ii)

This file follows both scripts loop by loop.

* `mirClauses N A U K hull` is the clause list of `gen_etv.py N A U K --mirror [--hull]`:
  the clauses of `ETV.etvClauses` (proved to be the option-free file in `results/H`), then
  the hull units `X(0,i,j)` (`0 < i < j`), then the identification clauses
  `¬X(i,j,k) ∨ X(m-k,m-j,m-i)` and `X(i,j,k) ∨ ¬X(m-k,m-j,m-i)` for every triple with
  `lo ≤ i` whose mirror image is lexicographically larger. Points are `0, …, N-1`; `lo = 1`
  with `--hull` (point `0` is the hull point) and `lo = 0` otherwise; `m = N - 1 + lo`.
* `mirgen` is `mirgen.py`: every orientation variable is replaced by the representative of
  its orbit `{X(i,j,k), X(m-k,m-j,m-i)}` (the one with the smaller number, i.e. the
  lexicographically smaller triple), each clause becomes the sorted list of its distinct
  literals, tautologies and repeated clauses are dropped (first occurrence kept).
* `interiorClauses` are the two clauses "the axis point `c = (N-1)/2` is not extreme",
  and `yflipUnit` is the unit `X(0,1,2)`.

The output is compared byte for byte with the Python files by `scripts/compare_mir.sh`.
-/

namespace Mir

open ETV Lit

/-- `(i,j,k) < (i',j',k')` lexicographically: the order of `itertools.combinations`, hence
of the variable numbers. -/
def lexLt (i j k i' j' k' : Nat) : Prop := i < i' ∨ (i = i' ∧ (j < j' ∨ (j = j' ∧ k < k')))

instance (i j k i' j' k' : Nat) : Decidable (lexLt i j k i' j' k') := by
  unfold lexLt; infer_instance

/-- `lo` of `gen_etv.py --mirror` in 0-based indexing. -/
def lo (hull : Bool) : Nat := if hull then 1 else 0

/-- The mirror index `m` in 0-based indexing: `p ↦ m - p` pairs the points `lo, …, N-1`. -/
def mm (N : Nat) (hull : Bool) : Nat := N - 1 + lo hull

/-- The hull units of `gen_etv.py --hull`: `X(0,i,j)` for `0 < i < j < N`. -/
def hullUnits (N : Nat) : List Clause :=
  ((pairs N).filter fun (i, _) => 1 ≤ i).map fun (i, j) => [pos' (.x 0 i j)]

/-- The identification clauses of `gen_etv.py --mirror`. -/
def mirrorEqs (N : Nat) (hull : Bool) : List Clause :=
  (triples N).flatMap fun (i, j, k) =>
    let m := mm N hull
    if lo hull ≤ i ∧ lexLt i j k (m - k) (m - j) (m - i) then
      [[neg' (.x i j k), pos' (.x (m - k) (m - j) (m - i))],
       [pos' (.x i j k), neg' (.x (m - k) (m - j) (m - i))]]
    else []

/-- The clause list of `gen_etv.py N A U K --mirror [--hull]`. -/
def mirClauses (N A U K : Nat) (hull : Bool) : List Clause :=
  etvClauses N A U K ++ (if hull then hullUnits N else []) ++ mirrorEqs N hull

/-- The orbit representative of a variable (identity on chain variables and on triples
outside the range of the identification). -/
def subVar (N : Nat) (hull : Bool) : Var → Var
  | .x i j k =>
    let m := mm N hull
    if lo hull ≤ i ∧ i < j ∧ j < k ∧ k < N ∧ lexLt (m - k) (m - j) (m - i) i j k then
      .x (m - k) (m - j) (m - i)
    else .x i j k
  | v => v

def subLit (N : Nat) (hull : Bool) (l : Lit) : Lit := ⟨subVar N hull l.var, l.pos⟩

/-- The variable numbering of `gen_etv.py N A U K` (as in `ETV.dimacs`). -/
def num (N A U : Nat) : Std.HashMap Var Nat := numberMap (allVars N A U)

/-- A clause as Python's `tuple(sorted(set(c)))`. -/
def normClause (c : List Int) : List Int := c.eraseDups.mergeSort (fun a b => decide (a ≤ b))

/-- Python's `any(-l in s for l in s)`. -/
def isTaut (c : List Int) : Bool := c.any fun l => c.contains (-l)

/-- One step of the `mirgen.py` loop. -/
def mirStep (st : Std.HashSet (List Int) × Array (List Int)) (c : List Int) :
    Std.HashSet (List Int) × Array (List Int) :=
  if isTaut c then st
  else if st.1.contains (normClause c) then st
  else (st.1.insert (normClause c), st.2.push (normClause c))

/-- `mirgen.py` without the extra clauses: substituted, normalised, deduplicated. -/
def mirgen (cls : List (List Int)) : List (List Int) :=
  (cls.foldl mirStep (∅, #[])).2.toList

/-- The substituted DIMACS clauses of `gen_etv.py N A U K --mirror [--hull]`. -/
def subDimacs (N A U K : Nat) (hull : Bool) : List (List Int) :=
  let m := num N A U
  (mirClauses N A U K hull).map fun c => c.map fun l => litToInt m (subLit N hull l)

/-- The axis point of the option-free mirror instance (`N` odd): `(N-1)/2`. -/
def axisPt (N : Nat) : Nat := (N - 1) / 2

/-- The numbers of the substituted triples `X(i,c,k)`, `i < c < k`, as `sorted(set(...))`. -/
def interiorLits (N A U : Nat) : List Int :=
  let c := axisPt N
  normClause <| (List.range c).flatMap fun i =>
    (List.range' (c + 1) (N - (c + 1))).map fun k =>
      ((num N A U).getD (subVar N false (.x i c k)) 0 : Int)

/-- "The axis point is not extreme": some `X(i,c,k)` is true and some is false. -/
def interiorClauses (N A U : Nat) : List (List Int) :=
  [interiorLits N A U, (interiorLits N A U).map (fun l => -l)]

/-- The unit `X(0,1,2)` (after substitution). -/
def yflipUnit (N A U : Nat) : List (List Int) :=
  [[((num N A U).getD (subVar N false (.x 0 1 2)) 0 : Int)]]

/-- `hm33k7.sub.cnf` = `mirgen.py (gen_etv.py N K K K --mirror --hull) N --hull`. -/
def hullCnf (N K : Nat) : List (List Int) := mirgen (subDimacs N K K K true)

/-- `m33k7int.sub.cnf` = `mirgen.py (gen_etv.py N K K K --mirror) N --interior --yflip-unit`. -/
def interiorCnf (N K : Nat) : List (List Int) :=
  mirgen (subDimacs N K K K false) ++ interiorClauses N K K ++ yflipUnit N K K

end Mir
