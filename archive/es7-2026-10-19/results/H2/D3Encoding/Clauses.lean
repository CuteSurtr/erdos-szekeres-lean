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

/-- `parity_sort` on a triple of distinct numbers: the sorted triple and the sign of the
sorting permutation (Python counts inversions; for distinct entries this is the same). -/
def paritySort (a b c : Nat) : (Nat × Nat × Nat) × Int :=
  if a < b then
    if b < c then ((a, b, c), 1) else if a < c then ((a, c, b), -1) else ((c, a, b), 1)
  else
    if a < c then ((b, a, c), -1) else if b < c then ((b, c, a), 1) else ((c, b, a), -1)

abbrev TV := Std.HashMap (Nat × Nat × Nat) (Nat × Int)

/-- Record `chi(S) = s · sg · v` for every image `S = sorted(g T)` of `T = (a, b, c)`; the
first entry for `S` wins, as with Python's `seen` dictionary. -/
def orbitStep (a b c v : Nat) (tv : TV) (g : (Nat → Nat) × Int) : TV :=
  tv.insertIfNew (paritySort (g.1 a) (g.1 b) (g.1 c)).1
    (v, (paritySort (g.1 a) (g.1 b) (g.1 c)).2 * g.2)

def insertOrbit (t a b c v : Nat) (tv : TV) : TV :=
  (group t).foldl (orbitStep a b c v) tv

/-- One step of `D3Encoding._triples`: allocate the next variable for an unseen orbit. -/
def tripleStep (t : Nat) (st : TV × Nat) (T : List Nat) : TV × Nat :=
  match T with
  | [a, b, c] =>
    if st.1.contains (a, b, c) then st else (insertOrbit t a b c (st.2 + 1) st.1, st.2 + 1)
  | _ => st

/-- The triple table and the number `nX` of triple variables. -/
def triples (t : Nat) : TV × Nat :=
  (combs (List.range (3 * t + 1)) 3).foldl (tripleStep t) ({}, 0)

/-- `SymEncoding.lit`: the literal that is true iff `chi(a,b,c) = +1`. -/
def lit (tv : TV) (a b c : Nat) : Int :=
  (paritySort a b c).2 * (tv.getD (paritySort a b c).1 (0, 1)).2 *
    ((tv.getD (paritySort a b c).1 (0, 1)).1 : Int)

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

/-- Drop adjacent repeats (on a sorted list: all repeats). -/
def uniq : List Int → List Int
  | a :: b :: l => if a = b then uniq (b :: l) else a :: uniq (b :: l)
  | l => l

/-- `sorted(units)` for the centre facts, as unit clauses. -/
def centerClauses (t : Nat) (L : Nat → Nat → Nat → Int) : List (List Int) :=
  let c := 3 * t
  let units := (List.range (3 * t)).flatMap fun a =>
    [L c a (rot c 1 a), -L c a (rot c 2 a)]
  (uniq (units.mergeSort (· ≤ ·))).map ([·])

/-- The six labelled convex sign patterns `(abc, abd, acd, bcd)` of `a<b<c<d`, in the
order of `itertools.product((1,-1), repeat=4)`. -/
def convexPatterns : List (List Int) :=
  [[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, -1, 1], [-1, 1, 1, -1], [-1, -1, 1, 1],
   [-1, -1, -1, -1]]

abbrev CV := Std.HashMap (List Nat) Nat

/-- The canonical `r`-subsets of the set points, `4 ≤ r ≤ K - 1`, in Python's allocation
order (level by level, `combinations` order inside a level). -/
def convKeys (t K : Nat) : List (List Nat) :=
  (List.range' 4 (K - 4)).flatMap fun r => (combs (List.range (3 * t)) r).filter (isCanon t)

/-- The clauses that define the conv variable `v` of the key `S`: the six pattern clauses
for `|S| = 4`, the layered clause `∧ᵢ conv(canon(S∖Sᵢ)) → conv(S)` otherwise. -/
def convClauses (t : Nat) (L : Nat → Nat → Nat → Int) (cv : CV) (v : Nat) (S : List Nat) :
    List (List Int) :=
  match S with
  | [a, b, c, d] =>
    let lits := [L a b c, L a b d, L a c d, L b c d]
    convexPatterns.map fun pat => (List.zipWith (fun p l => -p * l) pat lits) ++ [(v : Int)]
  | _ =>
    [((List.range S.length).map fun i => -((cv.getD (canon t (S.eraseIdx i)) 0 : Nat) : Int)) ++
      [(v : Int)]]

def convStep (t : Nat) (L : Nat → Nat → Nat → Int) (acc : List (List (List Int)) × CV × Nat)
    (S : List Nat) : List (List (List Int)) × CV × Nat :=
  (convClauses t L acc.2.1 (acc.2.2 + 1) S :: acc.1, acc.2.1.insertIfNew S (acc.2.2 + 1),
    acc.2.2 + 1)

/-- The `K`-gon part, `--kgon layered`: conv variables from `nX + 1` on, their clauses, then
one clause per canonical `K`-set. Returns the clauses and the final variable count. -/
def kgonLayered (t K : Nat) (L : Nat → Nat → Nat → Int) (nX : Nat) : List (List Int) × Nat :=
  let st := (convKeys t K).foldl (convStep t L) ([], {}, nX)
  let clK := ((combs (List.range (3 * t)) K).filter (isCanon t)).map fun S =>
    (List.range K).map fun i => -((st.2.1.getD (canon t (S.eraseIdx i)) 0 : Nat) : Int)
  (st.1.reverse.flatten ++ clK, st.2.2)

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
  let tr := triples t
  let L := lit tr.1
  let kg := kgonLayered t K L tr.2
  (kg.2, tr.2, axiomClauses t L ++ centerClauses t L ++ kg.1 ++ sbClauses t L)

end D3
