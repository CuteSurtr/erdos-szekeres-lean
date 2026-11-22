import EncB.Render
import N66Enc.States

/-!
# RowEnc.Gen: the coupled owner CNF of the N66 row certificates (Std-only)

Port of VB's own generator `vfy15/bin/cnfgen.cpp` (U1 row check, 20 Nov 2026), which re-generated and
re-certified the 629 template / core CNFs behind the 11,884 rows of `N66Enc.R0` (DESIGN.md F3). The text printed
from these definitions is compared byte for byte (SHA-256) with VB's certified files (M9).

Positions `0..n-1` are the owners of distinct states. Atoms: `bef i j` (i < j: owner i left of owner j),
`ge cup i j k` (i < j, k = 2..4: the label of the x-sorted pair has cap (cup = false) / cup coordinate ≥ k),
`ori i j k` (i < j < k: the owners, in position order, are positively oriented), `cvx i j k l` (the four owners
are in convex position). Literals are built 3-valued (`L3`: constants for `ge` with k ≤ 1 / k ≥ 5, as cnfgen's
`TRUE_`/`FALSE_`), then folded by `finClause` (a clause with a true constant is dropped, false constants are
removed), exactly as cnfgen's `Out::add`.
-/

namespace RowEnc
open N66Enc

inductive Atom where
  | bef (i j : Nat)
  | ge (cup : Bool) (i j k : Nat)
  | ori (i j k : Nat)
  | cvx (i j k l : Nat)
  deriving DecidableEq, Repr

/-- A literal before constant folding. -/
inductive L3 where
  | t
  | f
  | lit (pos : Bool) (a : Atom)
  deriving DecidableEq, Repr

def L3.neg : L3 → L3
  | .t => .f
  | .f => .t
  | .lit p a => .lit (!p) a

/-- `G.bef(u, v)`. -/
def befL (u v : Nat) : L3 := if u < v then .lit true (.bef u v) else .lit false (.bef v u)

/-- `G.ge(typ, i, j, k)` (`cup = (typ == 1)`). -/
def geL (cup : Bool) (i j k : Nat) : L3 :=
  if k ≤ 1 then .t else if 4 < k then .f else .lit true (.ge cup (min i j) (max i j) k)

/-- Sort three numbers (ascending) and the parity of the sorting permutation (`inv & 1`). -/
def sort3 (a b c : Nat) : Nat × Nat × Nat :=
  if a ≤ b then
    if b ≤ c then (a, b, c) else if a ≤ c then (a, c, b) else (c, a, b)
  else
    if a ≤ c then (b, a, c) else if b ≤ c then (b, c, a) else (c, b, a)

def inv3 (a b c : Nat) : Nat := (if b < a then 1 else 0) + (if c < a then 1 else 0) + (if c < b then 1 else 0)

/-- `G.ori(a, b, c)`. -/
def oriL (a b c : Nat) : L3 :=
  let s := sort3 a b c
  .lit (inv3 a b c % 2 == 0) (.ori s.1 s.2.1 s.2.2)

/-- Insertion of `x` into an ascending list. -/
def insAsc (x : Nat) : List Nat → List Nat
  | [] => [x]
  | y :: ys => if x ≤ y then x :: y :: ys else y :: insAsc x ys

def sortAsc (l : List Nat) : List Nat := l.foldr insAsc []

/-- `G.cvx(a, b, c, d)` (sorts its arguments). -/
def cvxL (a b c d : Nat) : L3 :=
  match sortAsc [a, b, c, d] with
  | [w, x, y, z] => .lit true (.cvx w x y z)
  | _ => .f

/-- cnfgen's `Out::add`: drop the clause on a true constant, drop false constants. -/
def finClause : List L3 → Option (List (Bool × Atom))
  | [] => some []
  | .t :: _ => none
  | .f :: ls => finClause ls
  | .lit p a :: ls => (finClause ls).map ((p, a) :: ·)

/-- `k`-subsets of a list, in lexicographic order of positions. -/
def combs : Nat → List Nat → List (List Nat)
  | 0, _ => [[]]
  | _ + 1, [] => []
  | k + 1, x :: xs => (combs k xs).map (x :: ·) ++ combs (k + 1) xs

/-- The 24 permutations of 4 positions in `next_permutation` order (lexicographic). -/
def perm4Idx : List (List Nat) :=
  [[0,1,2,3],[0,1,3,2],[0,2,1,3],[0,2,3,1],[0,3,1,2],[0,3,2,1],
   [1,0,2,3],[1,0,3,2],[1,2,0,3],[1,2,3,0],[1,3,0,2],[1,3,2,0],
   [2,0,1,3],[2,0,3,1],[2,1,0,3],[2,1,3,0],[2,3,0,1],[2,3,1,0],
   [3,0,1,2],[3,0,2,1],[3,1,0,2],[3,1,2,0],[3,2,0,1],[3,2,1,0]]

/-- `bad4()`: the bit patterns `(m & 8, m & 4, m & 2, m & 1)`, m = 0..15, with more than one sign change. -/
def bits4 (m : Nat) : Bool × Bool × Bool × Bool :=
  (m / 8 % 2 == 1, m / 4 % 2 == 1, m / 2 % 2 == 1, m % 2 == 1)

def changes4 (b : Bool × Bool × Bool × Bool) : Nat :=
  (if b.1 != b.2.1 then 1 else 0) + (if b.2.1 != b.2.2.1 then 1 else 0) + (if b.2.2.1 != b.2.2.2 then 1 else 0)

def bad4 : List (Bool × Bool × Bool × Bool) := ((List.range 16).map bits4).filter fun b => 1 < changes4 b

/-- `convex_from(x, y, z, w)`: exactly two of `x, ¬y, z, ¬w`. -/
def convexFrom (x y z w : Bool) : Bool :=
  (if x then 1 else 0) + (if !y then 1 else 0) + (if z then 1 else 0) + (if !w then 1 else 0) == 2

def flipIf (b : Bool) (l : L3) : L3 := if b then l.neg else l

/-! ## The static families (cnfgen `statics`, in its order) -/

def threshCls (n : Nat) : List (List L3) :=
  (combs 2 (List.range n)).flatMap fun p =>
    match p with
    | [i, j] => [false, true].flatMap fun cup => [2, 3].map fun k => [(geL cup i j (k + 1)).neg, geL cup i j k]
    | _ => []

/-- Transitivity and growth for one ordered triple of distinct positions. -/
def tripleCls (a b c : Nat) : List (List L3) :=
  let o := oriL a b c
  [(befL a b).neg, (befL b c).neg, befL a c] ::
    ([false, true].flatMap fun cup => [1, 2, 3, 4].map fun k =>
      [(befL a b).neg, (befL b c).neg, if cup then o.neg else o, (geL cup a b k).neg, geL cup b c (k + 1)])

def tripCls (n : Nat) : List (List L3) :=
  (List.range n).flatMap fun a => (List.range n).flatMap fun b => (List.range n).flatMap fun c =>
    if a = b ∨ b = c ∨ a = c then [] else tripleCls a b c

/-- Signotope packets for one order `q` of four positions. -/
def packetCls (q : List Nat) : List (List L3) :=
  match q with
  | [q0, q1, q2, q3] =>
    let t0 := oriL q0 q1 q2; let t1 := oriL q0 q1 q3; let t2 := oriL q0 q2 q3; let t3 := oriL q1 q2 q3
    bad4.map fun bb =>
      [(befL q0 q1).neg, (befL q1 q2).neg, (befL q2 q3).neg,
        flipIf bb.1 t0, flipIf bb.2.1 t1, flipIf bb.2.2.1 t2, flipIf bb.2.2.2 t3]
  | _ => []

/-- The 16 clauses defining `cvx` for a sorted quadruple. -/
def cvxDefCls (a b c d : Nat) : List (List L3) :=
  let t0 := oriL a b c; let t1 := oriL a b d; let t2 := oriL a c d; let t3 := oriL b c d
  let cv := cvxL a b c d
  (List.range 16).map fun m =>
    let bb := bits4 m
    [flipIf bb.1 t0, flipIf bb.2.1 t1, flipIf bb.2.2.1 t2, flipIf bb.2.2.2 t3,
      if convexFrom bb.1 bb.2.1 bb.2.2.1 bb.2.2.2 then cv else cv.neg]

def quadCls (n : Nat) : List (List L3) :=
  (combs 4 (List.range n)).flatMap fun s =>
    match s with
    | [a, b, c, d] =>
      (perm4Idx.flatMap fun ix => packetCls (ix.map fun x => s.getD x 0)) ++ cvxDefCls a b c d
    | _ => []

/-- The no-octagon clause of an 8-set `e` (its 4-subsets in index order). -/
def octClause (e : List Nat) : List L3 :=
  (combs 4 e).map fun s =>
    match s with
    | [a, b, c, d] => (cvxL a b c d).neg
    | _ => .f

def octCls (n : Nat) (octs : Option (List (List Nat))) : List (List L3) :=
  match octs with
  | some es => es.map octClause
  | none => (combs 8 (List.range n)).map octClause

/-! ## Tests -/

inductive Test where
  | E (u v : Nat)
  | D (u v a b : Nat)
  | P (p q r : Nat)
  deriving DecidableEq, Repr

def testCl : Test → List L3
  | .E u v => [(befL u v).neg]
  | .D u v a b =>
    [(befL u v).neg, (geL false (min u v) (max u v) a).neg, geL false (min u v) (max u v) (a + 1),
      (geL true (min u v) (max u v) b).neg, geL true (min u v) (max u v) (b + 1)]
  | .P p q r => [oriL p q r]

/-- The 16 cells `(a, b)`, `a` outer, as cnfgen enumerates them. -/
def cells16 : List (Nat × Nat) := (List.range 4).flatMap fun a => (List.range 4).map fun b => (a + 1, b + 1)

/-- cnfgen's `all_tests` for a state list `S` (refined domains for E/D, the plain six-order table for P). -/
def allTests (S : List (Fin 70)) : List Test :=
  ((combs 2 (List.range S.length)).flatMap fun p =>
    match p with
    | [i, j] => [(i, j), (j, i)].flatMap fun uv =>
        let su := S.getD uv.1 0; let sv := S.getD uv.2 0
        if !can su sv then [Test.E uv.1 uv.2]
        else cells16.filterMap fun z => if domRef (prof su) (prof sv) z then none else some (Test.D uv.1 uv.2 z.1 z.2)
    | _ => []) ++
  ((combs 3 (List.range S.length)).filterMap fun t =>
    match t with
    | [i, j, k] =>
      let si := S.getD i 0; let sj := S.getD j 0; let sk := S.getD k 0
      if tt si sj sk then some (Test.P i j k) else if tt si sk sj then some (Test.P i k j) else none
    | _ => none)

/-! ## The certificates and their CNFs -/

/-- A certified row CNF: a template (state-independent: size, kept tests, octagon list or `none` = complete) or a
core (states; all tests; octagon list or `none` = complete). -/
inductive Cert where
  | tmpl (n : Nat) (tests : List Test) (octs : Option (List (List Nat)))
  | core (S : List (Fin 70)) (octs : Option (List (List Nat)))

def Cert.n : Cert → Nat
  | .tmpl n _ _ => n
  | .core S _ => S.length

def Cert.tests : Cert → List Test
  | .tmpl _ ts _ => ts
  | .core S _ => allTests S

def Cert.octs : Cert → Option (List (List Nat))
  | .tmpl _ _ o => o
  | .core _ o => o

/-- The 3-valued clause list in cnfgen order. -/
def cls3 (n : Nat) (tests : List Test) (octs : Option (List (List Nat))) : List (List L3) :=
  threshCls n ++ tripCls n ++ quadCls n ++ octCls n octs ++ tests.map testCl

def clsS (t : Cert) : List (List (Bool × Atom)) := (cls3 t.n t.tests t.octs).filterMap finClause

/-! ## Numbering (cnfgen's allocation order) -/

def allocPair (i j : Nat) : List Atom :=
  [.bef i j, .ge false i j 2, .ge false i j 3, .ge false i j 4, .ge true i j 2, .ge true i j 3, .ge true i j 4]

def alloc (n : Nat) : List Atom :=
  ((combs 2 (List.range n)).flatMap fun p => match p with | [i, j] => allocPair i j | _ => []) ++
  ((combs 3 (List.range n)).filterMap fun p => match p with | [i, j, k] => some (.ori i j k) | _ => none) ++
  ((combs 4 (List.range n)).filterMap fun p => match p with | [i, j, k, l] => some (.cvx i j k l) | _ => none)

/-- An injective code of atoms with positions below 32. -/
def code : Atom → Nat
  | .bef i j => 4 * (i + 32 * j)
  | .ge cup i j k => 1 + 4 * (k + 8 * ((if cup then 1 else 0) + 2 * (i + 32 * j)))
  | .ori i j k => 2 + 4 * (i + 32 * (j + 32 * k))
  | .cvx i j k l => 3 + 4 * (i + 32 * (j + 32 * (k + 32 * l)))

def allocCodes (n : Nat) : List Nat := (alloc n).map code

def nvOf (n : Nat) : Nat := (alloc n).length

def toLit (m : Array Nat) (x : Bool × Atom) : Int :=
  let v : Int := m.getD (code x.2) 0
  if x.1 then v else -v

/-- **The CNF of a certificate** (DIMACS numbers = 1 + position in cnfgen's allocation order). -/
def certCnf (t : Cert) : List (List Int) :=
  let m := EncB.numberMap (allocCodes t.n)
  (clsS t).map fun cl => cl.map (toLit m)

/-- **What the printer writes for a certificate.** -/
def certText (t : Cert) : String := EncB.render (nvOf t.n) (certCnf t)

/-- The sub-list of `certCnf t` at the given positions (`none` if a position is out of range). -/
def subCnfChecked (t : Cert) (idx : List Nat) : Option (List (List Int)) :=
  let A := (certCnf t).toArray
  idx.mapM fun i => A[i]?

end RowEnc
