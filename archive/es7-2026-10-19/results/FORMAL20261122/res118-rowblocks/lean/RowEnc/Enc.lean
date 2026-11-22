import EncB.Render
import RowEnc.States

/-!
# RowEnc.Enc: the coupled-row CNF of RES33N `coupled.py` as a Lean function (Std-only)

`rowCnf S` is `coupled.CNF(S, octagon='full', static=True).clauses` for a sorted support `S`, and
`rowText S = EncB.render (rowNv S) (rowCnf S)` is the file the certifying scripts wrote
(`p cnf {nv} {len(clauses)}\n` + `' '.join(map(str, clause)) + ' 0\n'`; cut34*.py `build`, killtools certify.py).
Line numbers refer to `fastbb-20261113/killtools/coupled.py` (sha256 959072b1, the receipts' encoder pin).

* Atoms `Atm` are the generator's variable keys with owner indices into `S`; literals `Lit` are atoms with a
  polarity or Boolean constants. The helpers `befL`, `geL`, `posL`, `disagreeL` and the clause builders mirror
  `Coupled.before/ge/positive/disagree/domainClause/growthClause/packetClause/convexClause` of the library
  (CoupledSemantics.lean) with ℕ indices; `threshClause`, `sourceClause`, `octClause` are the remaining families.
* The clause list `rawClauses S` follows the generator's loops in order (DESIGN.md §2, families F1-F10).
* `finish` is the generator's `add`: a true constant drops the clause, false constants are removed, a tautology is
  dropped, literals are sorted by absolute value, repetitions removed.
* Numbering (lines 49-53, 104-117): `allocCodes n` lists the atom codes in allocation order (per pair `before,
  cap_ge 2..4, cup_ge 2..6`; per triple `orientation`; per 4-set `convex_four`); `num` is `1 +` the first position,
  through `EncB.numberMap` (ENCBLEAN/n66enc). Soundness never depends on the numbers being Python's; byte identity
  checks them (E1).
-/

namespace RowEnc

/-- The generator's variable keys (owner indices into the support). -/
inductive Atm where
  | bef (i j : Nat)
  | cap (i j t : Nat)
  | cup (i j t : Nat)
  | ori (i j l : Nat)
  | cvx (i j l m : Nat)
  deriving DecidableEq, Repr

/-- A literal: a Boolean constant or an atom with a polarity (`true` = positive). -/
inductive Lit where
  | const (b : Bool)
  | atom (a : Atm) (pos : Bool)
  deriving DecidableEq, Repr

def Lit.neg : Lit → Lit
  | .const b => .const (!b)
  | .atom a b => .atom a (!b)

/-- `self.before(i, j)` (line 125): the key of the sorted pair, negated for `i > j` (= `Coupled.before`). -/
def befL (i j : Nat) : Lit := if i < j then .atom (.bef i j) true else .atom (.bef j i) false

/-- `self.ge(typ, i, j, k)` (lines 127-131) (= `Coupled.ge`). -/
def geL (cup : Bool) (i j t : Nat) : Lit :=
  if t ≤ 1 then .const true else
  if (if cup then 6 else 4) < t then .const false else
  .atom (if cup then .cup (min i j) (max i j) t else .cap (min i j) (max i j) t) true

/-- `self.orient(q)` (lines 133-135): canonical triple order, sign reversed for odd permutations
(= `Coupled.positive`). -/
def posL (i j l : Nat) : Lit :=
  if i < j then
    if j < l then .atom (.ori i j l) true
    else if i < l then .atom (.ori i l j) false
    else .atom (.ori l i j) true
  else
    if i < l then .atom (.ori j i l) false
    else if j < l then .atom (.ori j l i) true
    else .atom (.ori l j i) false

/-- `-x if bit else x` (= `Coupled.disagree`). -/
def disagreeL (e : Lit) (b : Bool) : Lit := if b then e.neg else e

/-! ## Clause builders -/

/-- F1 (lines 60-62). -/
def threshClause (cup : Bool) (i j k : Nat) : List Lit := [(geL cup i j (k + 1)).neg, geL cup i j k]

/-- F2 (line 64), `h = STATES[S[u]][0]`. -/
def sourceClause (u v h : Nat) : List Lit := [(befL u v).neg, (geL true u v (h + 2)).neg]

/-- F3 (line 66). -/
def emptyClause (u v : Nat) : List Lit := [(befL u v).neg]

/-- F4 (lines 71-72) (= `Coupled.domainClause`). -/
def domainClause (i j a b : Nat) : List Lit :=
  [(befL i j).neg, (geL false i j a).neg, geL false i j (a + 1), (geL true i j b).neg, geL true i j (b + 1)]

/-- F5 (line 74). -/
def transClause (a b c : Nat) : List Lit := [(befL a b).neg, (befL b c).neg, befL a c]

/-- F6 (lines 75-79) (= `Coupled.growthClause`). -/
def growthClause (cup : Bool) (i j l t : Nat) : List Lit :=
  [(befL i j).neg, (befL j l).neg, if cup then (posL i j l).neg else posL i j l,
    (geL cup i j t).neg, geL cup j l (t + 1)]

/-- F8 (lines 86-89) (= `Coupled.packetClause`). -/
def packetClause (i j l m : Nat) (x y z w : Bool) : List Lit :=
  [(befL i j).neg, (befL j l).neg, (befL l m).neg,
    disagreeL (posL i j l) x, disagreeL (posL i j m) y, disagreeL (posL i l m) z, disagreeL (posL j l m) w]

/-- F9 (lines 90-96) (= `Coupled.convexClause`). -/
def convexClause (i j l m : Nat) (x y z w : Bool) : List Lit :=
  [disagreeL (posL i j l) x, disagreeL (posL i j m) y, disagreeL (posL i l m) z, disagreeL (posL j l m) w,
    .atom (.cvx i j l m) (decide ([!w, z, !y, x].count true = 2))]

/-! ## Enumerations in itertools order -/

/-- `itertools.combinations(l, k)` (lexicographic). -/
def combs : Nat → List Nat → List (List Nat)
  | 0, _ => [[]]
  | _ + 1, [] => []
  | k + 1, x :: xs => (combs k xs).map (x :: ·) ++ combs (k + 1) xs

/-- `itertools.permutations(range(n), 3)`. -/
def perm3 (n : Nat) : List (Nat × Nat × Nat) :=
  (List.range n).flatMap fun a => ((List.range n).filter (· != a)).flatMap fun b =>
    ((List.range n).filter (fun c => c != a && c != b)).map fun c => (a, b, c)

/-- `itertools.permutations((a, b, c, d))`. -/
def perm4 (a b c d : Nat) : List (Nat × Nat × Nat × Nat) :=
  [(a,b,c,d),(a,b,d,c),(a,c,b,d),(a,c,d,b),(a,d,b,c),(a,d,c,b),
   (b,a,c,d),(b,a,d,c),(b,c,a,d),(b,c,d,a),(b,d,a,c),(b,d,c,a),
   (c,a,b,d),(c,a,d,b),(c,b,a,d),(c,b,d,a),(c,d,a,b),(c,d,b,a),
   (d,a,b,c),(d,a,c,b),(d,b,a,c),(d,b,c,a),(d,c,a,b),(d,c,b,a)]

/-- `itertools.product([False, True], repeat=4)`. -/
def bits16 : List (Bool × Bool × Bool × Bool) :=
  [false, true].flatMap fun x => [false, true].flatMap fun y => [false, true].flatMap fun z =>
    [false, true].map fun w => (x, y, z, w)

/-- `BAD4` (lines 39-40): patterns with more than one change. -/
def bad4 : List (Bool × Bool × Bool × Bool) :=
  bits16.filter fun b => decide (1 < [b.1 != b.2.1, b.2.1 != b.2.2.1, b.2.2.1 != b.2.2.2].count true)

/-! ## The clause list, family by family, in generator order -/

/-- F2-F4 for the ordered pair (u, v) (lines 63-72). -/
def dirPart (S : List Nat) (u v : Nat) : List (List Lit) :=
  sourceClause u v (h1 (S.getD u 0)) ::
    (if emptyB (S.getD u 0) (S.getD v 0) then [emptyClause u v]
     else (grid46.filter (fun z => !allowedB (S.getD u 0) (S.getD v 0) z)).map
       (fun z => domainClause u v z.1 z.2))

/-- One iteration of the pair loop (lines 58-72). -/
def pairClauses (S : List Nat) (i j : Nat) : List (List Lit) :=
  [threshClause false i j 2, threshClause false i j 3,
   threshClause true i j 2, threshClause true i j 3, threshClause true i j 4, threshClause true i j 5] ++
  dirPart S i j ++ dirPart S j i

def pairPart (S : List Nat) : List (List Lit) :=
  (combs 2 (List.range S.length)).flatMap fun p => match p with
    | [i, j] => pairClauses S i j
    | _ => []

/-- One iteration of the triple loop (lines 73-79). -/
def tripleClauses (a b c : Nat) : List (List Lit) :=
  transClause a b c :: (([1, 2, 3, 4].map fun k => growthClause false a b c k) ++
    ([1, 2, 3, 4, 5, 6].map fun k => growthClause true a b c k))

def triplePart (n : Nat) : List (List Lit) := (perm3 n).flatMap fun t => tripleClauses t.1 t.2.1 t.2.2

/-- F7 (lines 80-83). -/
def fixedClauses (S : List Nat) (i j l : Nat) : List (List Lit) :=
  if ttB (S.getD i 0) (S.getD j 0) (S.getD l 0) then [[posL i j l]]
  else if ttB (S.getD i 0) (S.getD l 0) (S.getD j 0) then [[(posL i j l).neg]] else []

def fixedPart (S : List Nat) : List (List Lit) :=
  (combs 3 (List.range S.length)).flatMap fun q => match q with
    | [i, j, l] => fixedClauses S i j l
    | _ => []

/-- One iteration of the 4-set loop (lines 84-96). -/
def quadClauses (a b c d : Nat) : List (List Lit) :=
  ((perm4 a b c d).flatMap fun q =>
      bad4.map fun x => packetClause q.1 q.2.1 q.2.2.1 q.2.2.2 x.1 x.2.1 x.2.2.1 x.2.2.2) ++
    (bits16.map fun x => convexClause a b c d x.1 x.2.1 x.2.2.1 x.2.2.2)

def quadPart (n : Nat) : List (List Lit) :=
  (combs 4 (List.range n)).flatMap fun q => match q with
    | [a, b, c, d] => quadClauses a b c d
    | _ => []

def cvxLit (q : List Nat) : Lit :=
  match q with
  | [i, j, l, m] => .atom (.cvx i j l m) false
  | _ => .const false

/-- F10 (lines 97-99). -/
def octClause (eight : List Nat) : List Lit := (combs 4 eight).map cvxLit

def octPart (n : Nat) : List (List Lit) := (combs 8 (List.range n)).map octClause

/-- All clauses, before `add`, in generator order. -/
def rawClauses (S : List Nat) : List (List Lit) :=
  pairPart S ++ triplePart S.length ++ fixedPart S ++ quadPart S.length ++ octPart S.length

/-! ## Numbering -/

/-- Injective codes of the atoms with indices below 16 and thresholds below 8 (indices are reduced mod 16, so
every code is below 73984). -/
def Atm.code : Atm → Nat
  | .bef i j => (i % 16) * 16 + j % 16
  | .cap i j t => 256 + ((i % 16) * 16 + j % 16) * 8 + t % 8
  | .cup i j t => 2304 + ((i % 16) * 16 + j % 16) * 8 + t % 8
  | .ori i j l => 4352 + ((i % 16) * 16 + j % 16) * 16 + l % 16
  | .cvx i j l m => 8448 + (((i % 16) * 16 + j % 16) * 16 + l % 16) * 16 + m % 16

def pairAtoms (n : Nat) : List Atm :=
  (combs 2 (List.range n)).flatMap fun p => match p with
    | [i, j] => [.bef i j, .cap i j 2, .cap i j 3, .cap i j 4, .cup i j 2, .cup i j 3, .cup i j 4,
        .cup i j 5, .cup i j 6]
    | _ => []

def oriAtoms (n : Nat) : List Atm :=
  (combs 3 (List.range n)).filterMap fun q => match q with
    | [i, j, l] => some (.ori i j l)
    | _ => none

def cvxAtoms (n : Nat) : List Atm :=
  (combs 4 (List.range n)).filterMap fun q => match q with
    | [i, j, l, m] => some (.cvx i j l m)
    | _ => none

/-- The codes in allocation order (lines 49-53). -/
def allocCodes (n : Nat) : List Nat := (pairAtoms n ++ oriAtoms n ++ cvxAtoms n).map Atm.code

/-- The number of an atom through a code table `M` (0 = none) and allocation length `N` (n66enc `numWith`). -/
def numWith (M : Array Nat) (N : Nat) (a : Atm) : Nat :=
  let m := M.getD a.code 0
  if m = 0 then N + 1 + a.code else m

def Lit.toInt (M : Array Nat) (N : Nat) : Lit → Option Int
  | .const _ => none
  | .atom a b => some (if b then (numWith M N a : Int) else -(numWith M N a : Int))

def Lit.isTrue : Lit → Bool
  | .const b => b
  | .atom _ _ => false

/-- Remove adjacent repetitions. -/
def dedupAdj : List Int → List Int
  | a :: b :: t => if a = b then dedupAdj (b :: t) else a :: dedupAdj (b :: t)
  | l => l

/-- The generator's `add` (lines 141-149). -/
def finish (M : Array Nat) (N : Nat) (cl : List Lit) : Option (List Int) :=
  if cl.any Lit.isTrue then none else
  let xs := cl.filterMap (Lit.toInt M N)
  if xs.any (fun x => xs.contains (-x)) then none else
  some (dedupAdj (xs.mergeSort (fun a b => decide (a.natAbs ≤ b.natAbs))))

/-! ## The CNF and its text -/

/-- The header variable count `self.nv`. -/
def rowNv (S : List Nat) : Nat := (allocCodes S.length).length

/-- **The coupled-row CNF of the support `S`** (`coupled.CNF(S).clauses`). -/
def rowCnf (S : List Nat) : List (List Int) :=
  let L := allocCodes S.length
  let M := EncB.numberMap L
  (rawClauses S).filterMap (finish M L.length)

/-- **The text the exe prints for `S`** (`p cnf nv nc` + clause lines). -/
def rowText (S : List Nat) : String := EncB.render (rowNv S) (rowCnf S)

end RowEnc
