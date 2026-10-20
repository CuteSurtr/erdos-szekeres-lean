import Std.Data.HashMap

/-!
# The D3 clause generator (`results/E/tools/d3cnf.py`, default `--kgon layered`)

This file mirrors `d3cnf.py N K` (on top of `tools/symmetric/symcnf.py`) loop for loop, so
that `lake exe d3_dimacs N K OUT` prints the same file. Nothing here is a proof; it is the
object about which `Semantics.lean` states the soundness target.

Conventions (as in Python): `m = 3`, `t = N / 3` rotation orbits, orbit point `(o, r)` has
index `3 o + r`, the auxiliary centre has index `c = 3 t`, and there are `P = 3 t + 1`
chirotope points. The set points are `0, …, 3 t - 1`.
-/

namespace D3

/-- `itertools.combinations(l, k)`, in the same (lexicographic) order. -/
def combs : List Nat → Nat → List (List Nat)
  | _, 0 => [[]]
  | [], _ + 1 => []
  | x :: xs, k + 1 => (combs xs k).map (x :: ·) ++ combs xs (k + 1)

/-- Python's `divmod`-based rotation `pi(i, k)`. -/
def rot (c : Nat) (k i : Nat) : Nat :=
  if i = c then i else (i / 3) * 3 + (i % 3 + k) % 3

/-- `D3Encoding.sigma`, the reflection in the mirror axis through `(0,0)`. -/
def sigma (t c : Nat) (i : Nat) : Nat :=
  if i = c then i
  else if i / 3 = 0 then (3 - i % 3) % 3
  else (t - i / 3) * 3 + (3 - (i % 3 + 1) % 3) % 3

/-- The six group elements in Python's order: `R^0, R^1, R^2` (sign `+1`), then
`R^k ∘ S` for `k = 0, 1, 2` (sign `-1`). -/
def group (t : Nat) : List ((Nat → Nat) × Int) :=
  let c := 3 * t
  [(rot c 0, 1), (rot c 1, 1), (rot c 2, 1),
   (fun i => rot c 0 (sigma t c i), -1), (fun i => rot c 1 (sigma t c i), -1),
   (fun i => rot c 2 (sigma t c i), -1)]

/-- Sort ascending (Python `sorted`). -/
def sortL (l : List Nat) : List Nat := l.mergeSort (· ≤ ·)

/-- Python tuple comparison `T < best` on equal-length tuples. -/
def lexLt : List Nat → List Nat → Bool
  | [], _ => false
  | _ :: _, [] => false
  | a :: as, b :: bs => a < b || (a == b && lexLt as bs)

/-- `D3Encoding.canon`: the lexicographically least image under `G[1:]`. -/
def canon (t : Nat) (S : List Nat) : List Nat :=
  ((group t).drop 1).foldl (fun best g =>
    let T := sortL (S.map g.1)
    if lexLt T best then T else best) S

/-- `parity_sort` on a triple: the sorted triple and the sign of the sorting permutation. -/
def paritySort (a b c : Nat) : (Nat × Nat × Nat) × Int :=
  let inv := (if a > b then 1 else 0) + (if a > c then 1 else 0) + (if b > c then 1 else 0)
  match sortL [a, b, c] with
  | [x, y, z] => ((x, y, z), if inv % 2 = 1 then -1 else 1)
  | _ => ((0, 0, 0), 1)

abbrev TV := Std.HashMap (Nat × Nat × Nat) (Nat × Int)

/-- One step of `D3Encoding._triples`: allocate the next variable for an unseen orbit and
record `chi(S) = s · sg · v` for every image `S`. -/
def tripleStep (t : Nat) (st : TV × Nat) (T : List Nat) : TV × Nat :=
  match T with
  | [a, b, c] =>
    if st.1.contains (a, b, c) then st
    else
      let v := st.2 + 1
      let tv := (group t).foldl (fun tv g =>
        let (S, s) := paritySort (g.1 a) (g.1 b) (g.1 c)
        tv.insertIfNew S (v, s * g.2)) st.1
      (tv, v)
  | _ => st

/-- The triple table and the number `nX` of triple variables. -/
def triples (t : Nat) : TV × Nat :=
  (combs (List.range (3 * t + 1)) 3).foldl (tripleStep t) ({}, 0)

/-- `SymEncoding.lit`: the literal that is true iff `chi(a,b,c) = +1`. -/
def lit (tv : TV) (a b c : Nat) : Int :=
  let (S, s) := paritySort a b c
  let (v, sg) := tv.getD S (0, 1)
  s * sg * v

/-- The A4 (interiority) clauses of one 4-set. -/
def a4Clauses (L : Nat → Nat → Nat → Int) (S : List Nat) : List (List Int) :=
  S.flatMap fun x =>
    match S.filter (· != x) with
    | [p, q, r] =>
      [1, -1].map fun (s : Int) => [-s * L x q r, -s * L p x r, -s * L p q x, s * L p q r]
    | _ => []

def signs3 : List (Int × Int × Int) :=
  [(1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1), (-1, 1, 1), (-1, 1, -1), (-1, -1, 1),
   (-1, -1, -1)]

/-- The 3-term Grassmann–Plücker clauses of one 5-set. -/
def gpClauses (L : Nat → Nat → Nat → Int) (S : List Nat) : List (List Int) :=
  S.flatMap fun x =>
    match S.filter (· != x) with
    | [y1, y2, y3, y4] =>
      let l12 := L x y1 y2
      let l34 := L x y3 y4
      let l13 := L x y1 y3
      let l24 := L x y2 y4
      let l14 := L x y1 y4
      let l23 := L x y2 y3
      signs3.flatMap fun (s1, s2, s3) =>
        [[-s1 * l12, -s1 * l34, -s2 * l13, s2 * l24, -s3 * l14, -s3 * l23],
         [-s1 * l12, s1 * l34, -s2 * l13, -s2 * l24, -s3 * l14, s3 * l23]]
    | _ => []

def isCanon (t : Nat) (S : List Nat) : Bool := canon t S == S

def axiomClauses (t : Nat) (L : Nat → Nat → Nat → Int) : List (List Int) :=
  let pts := List.range (3 * t + 1)
  ((combs pts 4).filter (isCanon t)).flatMap (a4Clauses L) ++
  ((combs pts 5).filter (isCanon t)).flatMap (gpClauses L)

/-- `sorted(units)` for the centre facts, as unit clauses. -/
def centerClauses (t : Nat) (L : Nat → Nat → Nat → Int) : List (List Int) :=
  let c := 3 * t
  let units := (List.range (3 * t)).flatMap fun a =>
    [L c a (rot c 1 a), -L c a (rot c 2 a)]
  ((units.mergeSort (· ≤ ·)).eraseDups).map ([·])

/-- The six labelled convex sign patterns `(abc, abd, acd, bcd)` of `a<b<c<d`, in the
order of `itertools.product((1,-1), repeat=4)`. -/
def convexPatterns : List (List Int) :=
  [[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, -1, 1], [-1, 1, 1, -1], [-1, -1, 1, 1],
   [-1, -1, -1, -1]]

abbrev CV := Std.HashMap (List Nat) Nat

/-- The `K`-gon part, `--kgon layered`: the conv variables (from `nX + 1` on) and their
clauses. Returns the clauses, the conv map and the final variable count. -/
def kgonLayered (t K : Nat) (L : Nat → Nat → Nat → Int) (nX : Nat) : List (List Int) × Nat :=
  let pts := List.range (3 * t)
  let can := canon t
  -- conv_4
  let (cl4, cv, nv) := ((combs pts 4).filter (isCanon t)).foldl
    (fun (acc : List (List (List Int)) × CV × Nat) S =>
      let (cls, cv, nv) := acc
      let v := nv + 1
      match S with
      | [a, b, c, d] =>
        let lits := [L a b c, L a b d, L a c d, L b c d]
        let new := convexPatterns.map fun pat =>
          (List.zipWith (fun p l => -p * l) pat lits) ++ [(v : Int)]
        (new :: cls, cv.insert S v, v)
      | _ => (cls, cv.insert S v, v)) ([], {}, nX)
  -- conv_r, 5 ≤ r ≤ K-1
  let (clr, cv, nv) := (List.range' 5 (K - 5)).foldl
    (fun (acc : List (List (List Int)) × CV × Nat) r =>
      ((combs pts r).filter (isCanon t)).foldl
        (fun (acc : List (List (List Int)) × CV × Nat) S =>
          let (cls, cv, nv) := acc
          let v := nv + 1
          let cl := ((List.range r).map fun i =>
            -((cv.getD (can (S.eraseIdx i)) 0 : Nat) : Int)) ++ [(v : Int)]
          ([cl] :: cls, cv.insert S v, v)) acc) ([], cv, nv)
  -- K-sets
  let clK := ((combs pts K).filter (isCanon t)).map fun S =>
    (List.range K).map fun i => -((cv.getD (can (S.eraseIdx i)) 0 : Nat) : Int)
  (cl4.reverse.flatten ++ clr.reverse.flatten ++ clK, nv)

/-- The labelling normal form (`add_sb`, odd `m`). -/
def sbClauses (t : Nat) (L : Nat → Nat → Nat → Int) : List (List Int) :=
  if t < 2 then [] else
  let c := 3 * t
  ((List.range' 1 (t - 1)).flatMap fun o => [[L c 0 (3 * o)], [-L c 1 (3 * o)]]) ++
  ((List.range' 1 (t - 1)).flatMap fun o =>
    (List.range' (o + 1) (t - 1 - o)).map fun o2 => [L c (3 * o) (3 * o2)])

/-- The whole file `d3cnf.py N K`: number of variables, number of triple variables, and
the clauses in file order. -/
def d3Cnf (N K : Nat) : Nat × Nat × List (List Int) :=
  let t := N / 3
  let (tv, nX) := triples t
  let L := lit tv
  let (kg, nv) := kgonLayered t K L nX
  (nv, nX, axiomClauses t L ++ centerClauses t L ++ kg ++ sbClauses t L)

end D3
