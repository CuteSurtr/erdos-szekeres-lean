import N66E15.States
import N66E15.Atoms

/-!
# N66E15.Clauses: the clause families of the level-15 relaxation, structured (Std-only)

Every list below is in the generator's exact order; literals are structured (`SLit`) and numbered only in
`N66E15.Alloc`. The large lists are functions of `Unit` (Lean evaluates every closed top-level constant when the
exe starts; the first run was stopped by the memory guard at 3.4 GB for that reason), and the theorem-only ones
are `noncomputable`. Sources (pinned copies in `ref/`, SHA-256 in DESIGN.md §1.2):

* `pairClauses`, `posClauses`: coupled5.CNF(range(70), static=False) state-dependent clauses
  (coupled5.py:72-85), each followed by the guards `-sel` of its tag's owners (lazymono.py:35-36). coupled5's `add`
  sorts literals by |lit| and drops constants; for these clauses the order below is already increasing in the
  variable number (before < cap_ge 2..4 < cup_ge 2..4 of one pair), so no sort is needed.
* `threshClauses` (lazymono.py:44-46), `tripleClauses` (:48-64), `ceueClauses` (:66-72): lazymono's own clauses,
  literals exactly as written.
* `quadClauses a b c d` = `LazyMono.quad_clauses(a, b, c, d)` (lazymono.py:75-86).
* `fixedUnits`, `cubeUnit`, `rowClause` (p2_write.py:33-41), `cardClauses` (pysat 1.9.dev20 seqcounter, fitted in
  `tools/seqcounter_fit.py`: 1,646 grid cases + the production instance equal), `sbClauses` (p2_sb.py:29-38).
-/

namespace N66E15
open Atom

/-! ## Index lists in itertools order -/

def fr70 : List (Fin 70) := List.finRange 70

/-- `itertools.combinations(range(70), 2)`. -/
def comb2 : List (Fin 70 × Fin 70) :=
  fr70.flatMap fun i => fr70.filterMap fun j => if i < j then some (i, j) else none

/-- `itertools.combinations(range(70), 3)`. -/
def comb3 : List (Fin 70 × Fin 70 × Fin 70) :=
  fr70.flatMap fun i => fr70.flatMap fun j => fr70.filterMap fun k =>
    if i < j ∧ j < k then some (i, j, k) else none

/-- `itertools.combinations(range(70), 4)`. -/
def comb4 (_ : Unit) : List (Fin 70 × Fin 70 × Fin 70 × Fin 70) :=
  fr70.flatMap fun i => fr70.flatMap fun j => fr70.flatMap fun k => fr70.filterMap fun l =>
    if i < j ∧ j < k ∧ k < l then some (i, j, k, l) else none

/-- `itertools.permutations(range(70), 3)` (lexicographic). -/
def perm3 : List (Fin 70 × Fin 70 × Fin 70) :=
  fr70.flatMap fun a => fr70.flatMap fun b => fr70.filterMap fun c =>
    if a ≠ b ∧ b ≠ c ∧ a ≠ c then some (a, b, c) else none

/-! ## Literals -/

/-- `-sel[s]` (the guard of an owner). -/
def guard (s : Fin 70) : SLit := (false, sel s)

/-- `coupled5.before(a, b)` = `±before(min, max)`. -/
def befLit (a b : Fin 70) : SLit := if a < b then (true, before a b) else (false, before b a)

/-- `coupled5.orient((a, b, c))`: the sorted triple, negated for an odd permutation. -/
def oriLit (a b c : Fin 70) : SLit :=
  if a < b then
    if b < c then (true, orient a b c)
    else if a < c then (false, orient a c b)
    else (true, orient c a b)
  else
    if a < c then (false, orient b a c)
    else if b < c then (true, orient b c a)
    else (false, orient c b a)

/-- `coupled5.ge(typ, a, b, k)` for `2 ≤ k ≤ 4` (the only values used as literals): the positive literal of
`(typ_ge, min, max, k)`. -/
def geAtom (cup : Bool) (a b : Fin 70) (k : Nat) : Atom :=
  let i := if a < b then a else b
  let j := if a < b then b else a
  if cup then cupGe i j ⟨k % 5, Nat.mod_lt _ (by decide)⟩ else capGe i j ⟨k % 5, Nat.mod_lt _ (by decide)⟩

/-! ## F1: state-dependent clauses of coupled5 (empty, domain; positive) -/

/-- The cap/cup part of a domain clause: `neg(ge(typ,i,j,a)), ge(typ,i,j,a+1)` with constants dropped. -/
def gePart (cup : Bool) (i j : Fin 70) (a : Nat) : List SLit :=
  (if 2 ≤ a then [(false, geAtom cup i j a)] else []) ++ (if a + 1 ≤ 4 then [(true, geAtom cup i j (a + 1))] else [])

/-- coupled5.py:72-81 for one directed pair (u, v) of the unordered pair (i, j), i < j. -/
def dirPairClauses (i j u v : Fin 70) : List (List SLit) :=
  if !can u v then [[(befLit u v).neg, guard u, guard v]]
  else (List.range 4).flatMap fun a' => (List.range 4).filterMap fun b' =>
    if domRef (prof u) (prof v) (a' + 1, b' + 1) then none
    else some ([(befLit u v).neg] ++ gePart false i j (a' + 1) ++ gePart true i j (b' + 1) ++ [guard u, guard v])

@[irreducible] def pairClauses (_ : Unit) : List (List SLit) :=
  comb2.flatMap fun p => dirPairClauses p.1 p.2 p.1 p.2 ++ dirPairClauses p.1 p.2 p.2 p.1

/-- coupled5.py:82-85. -/
@[irreducible] def posClauses (_ : Unit) : List (List SLit) :=
  comb3.filterMap fun t =>
    let i := t.1; let j := t.2.1; let k := t.2.2
    if tt i j k then some [(true, orient i j k), guard i, guard j, guard k]
    else if tt i k j then some [(false, orient i j k), guard i, guard k, guard j]
    else none

/-! ## F2-F5, F7: lazymono's eager clauses -/

/-- lazymono.py:44-46. -/
@[irreducible] def threshClauses (_ : Unit) : List (List SLit) :=
  comb2.flatMap fun p => [false, true].flatMap fun cup => [2, 3].map fun k =>
    [(false, geAtom cup p.1 p.2 (k + 1)), (true, geAtom cup p.1 p.2 k), guard p.1, guard p.2]

def canTriple (a b c : Fin 70) : Bool := can a b && can b c && can a c

/-- lazymono.py:48-64 for one permutation (a, b, c). -/
def tripleClausesAt (a b c : Fin 70) : List (List SLit) :=
  if !(can a b && can b c) then [] else
  let g3 := [guard a, guard b, guard c]
  let ab := befLit a b
  let bc := befLit b c
  let trans := [ab.neg, bc.neg, befLit a c] ++ g3
  if !can a c then [trans] else
  let o := oriLit a b c
  let growth := [false, true].flatMap fun cup =>
    let gate := [ab.neg, bc.neg, if cup then o.neg else o]
    [1, 2, 3, 4].map fun k =>
      gate ++ (if k = 1 then [] else [(false, geAtom cup a b k)]) ++
        (if k = 4 then [] else [(true, geAtom cup b c (k + 1))]) ++ g3
  [trans] ++ growth ++
    [[ab.neg, bc.neg, o, (true, chC 3 a b c)] ++ g3, [ab.neg, bc.neg, o.neg, (true, chU 3 a b c)] ++ g3]

@[irreducible] def tripleClauses (_ : Unit) : List (List SLit) := perm3.flatMap fun t => tripleClausesAt t.1 t.2.1 t.2.2

/-- `(p, u, q)` is the first can-triple with ends `(p, q)` in permutation order (`(p, q) not in CE`). -/
def firstMid (p u q : Fin 70) : Bool :=
  fr70.all fun u' => !(decide (u'.val < u.val) && decide (u' ≠ p) && decide (u' ≠ q) && canTriple p u' q)

/-- lazymono.py:66-72 for one permutation (p, u, q). -/
def ceueClausesAt (p u q : Fin 70) : List (List SLit) :=
  if !canTriple p u q then [] else
  (if firstMid p u q then [[(false, ce p q), (false, ue p q), guard p, guard q]] else []) ++
    [[(false, chC 5 p u q), (true, ce p q), guard p, guard u, guard q],
     [(false, chU 5 p u q), (true, ue p q), guard p, guard u, guard q]]

@[irreducible] def ceueClauses (_ : Unit) : List (List SLit) := perm3.flatMap fun t => ceueClausesAt t.1 t.2.1 t.2.2

/-- **The eager stream** (`LazyMono(range(70))` with `emit`; p2_write.py:26), in order. -/
@[irreducible] def eagerStream (_ : Unit) : List (List SLit) :=
  pairClauses () ++ posClauses () ++ threshClauses () ++ tripleClauses () ++ ceueClauses ()

/-! ## F6, F8: the 12 clauses of an ordered quadruple -/

/-- `coupled5.BAD4`: the 8 orientation patterns with at least two sign changes, in product order. -/
def bad4 : List (Bool × Bool × Bool × Bool) :=
  [(false, false, true, false), (false, true, false, false), (false, true, false, true),
   (false, true, true, false), (true, false, false, true), (true, false, true, false),
   (true, false, true, true), (true, true, false, true)]

/-- `-t if bit else t`. -/
def flipIf (bit : Bool) (t : SLit) : SLit := if bit then t.neg else t

/-- `LazyMono.quad_clauses(a, b, c, d)` (lazymono.py:75-86). -/
def quadClauses (a b c d : Fin 70) : List (List SLit) :=
  let g := [guard a, guard b, guard c, guard d]
  let order := [(befLit a b).neg, (befLit b c).neg, (befLit c d).neg]
  let t0 := oriLit a b c
  let t1 := oriLit a b d
  let t2 := oriLit a c d
  let t3 := oriLit b c d
  (bad4.map fun bits =>
    order ++ [flipIf bits.1 t0, flipIf bits.2.1 t1, flipIf bits.2.2.1 t2, flipIf bits.2.2.2 t3] ++ g) ++
  [[(false, chC 3 a b c), (befLit c d).neg, t3, (true, chC 4 a c d)] ++ g,
   [(false, chU 3 a b c), (befLit c d).neg, t3.neg, (true, chU 4 a c d)] ++ g,
   [(false, chC 4 a b c), (befLit c d).neg, t3, (true, chC 5 a c d)] ++ g,
   [(false, chU 4 a b c), (befLit c d).neg, t3.neg, (true, chU 5 a c d)] ++ g]

/-- The quadruples p2_batch_cube.py accepts (`okquad`): distinct, and every pair `can` in that order. -/
def okQuad (a b c d : Fin 70) : Bool :=
  decide (a ≠ b ∧ a ≠ c ∧ a ≠ d ∧ b ≠ c ∧ b ≠ d ∧ c ≠ d) &&
    can a b && can a c && can a d && can b c && can b d && can c d

/-- The ordered quadruples with `okQuad` (permutations order). Theorem-only (`noncomputable`: no code is
generated, so the printer never builds it). -/
@[irreducible] noncomputable def perm4 : List (Fin 70 × Fin 70 × Fin 70 × Fin 70) :=
  fr70.flatMap fun a => fr70.flatMap fun b => fr70.flatMap fun c => fr70.filterMap fun d =>
    if okQuad a b c d then some (a, b, c, d) else none

/-- mono66's complete F6 + F8 (every activated set is a subset). Theorem-only, never evaluated. -/
@[irreducible] noncomputable def quadStream : List (List SLit) := perm4.flatMap fun q => quadClauses q.1 q.2.1 q.2.2.1 q.2.2.2

/-! ## The tail -/

def fixedUnits : List (List SLit) := [[(true, sel 0)], [(true, sel 1)]]

/-- A cube literal: `(s, true)` = occupied = `+sel s`, `(s, false)` = hole = `-sel s`. -/
def cubeUnit (z : Fin 70 × Bool) : List SLit := [(z.2, sel z.1)]

/-- A demand-one row on `T` (sorted support): `[-sel s | s ∈ T]`. -/
def rowClause (T : List (Fin 70)) : List SLit := T.map fun s => (false, sel s)

/-! ### The sequential counter (pysat seqcounter, "at most 15 of the 68 hole literals"; level 15) -/

/-- Number of hole literals (states 2..69) and the bound. -/
def nLits : Nat := 68
def kBound : Nat := 15

/-- `x_i` (i = 1..68) = `-sel[i+1]`. -/
def holeLit (i : Nat) : SLit := (false, sel ⟨(i + 1) % 70, Nat.mod_lt _ (by decide)⟩)

/-- Aux `s(a, j)` is used iff `1 ≤ j ≤ a ≤ n-1`, `j ≤ k` and `k - j ≤ n - 1 - a`. -/
def needAux (a j : Nat) : Bool :=
  decide (1 ≤ a ∧ a ≤ nLits - 1 ∧ 1 ≤ j ∧ j ≤ kBound ∧ j ≤ a ∧ kBound - j ≤ nLits - 1 - a)

def sAux (a j : Nat) : SLit := (true, cnt ⟨a % 68, Nat.mod_lt _ (by decide)⟩ ⟨j % 16, Nat.mod_lt _ (by decide)⟩)

/-- The diagonal walk from `s(a, j)` (see `tools/seqcounter_fit.py`). -/
def diagClauses : Nat → Nat → Nat → List (List SLit)
  | 0, _, _ => []
  | fuel + 1, a, j =>
    if a ≤ nLits - 1 ∧ j ≤ kBound ∧ needAux a j = true then
      (if needAux (a + 1) j then [[(sAux a j).neg, sAux (a + 1) j]] else []) ++
      (if j < kBound then
        (if needAux (a + 1) (j + 1) then [[(holeLit (a + 1)).neg, (sAux a j).neg, sAux (a + 1) (j + 1)]] else [])
       else [[(holeLit (a + 1)).neg, (sAux a j).neg]]) ++
      diagClauses fuel (a + 1) (j + 1)
    else []

/-- pysat `CardEnc.atmost(lits=[-sel[s] for s in 2..69], bound=15, encoding=seqcounter)`, clause order. -/
@[irreducible] def cardClauses : List (List SLit) :=
  (List.range (nLits - 1)).flatMap fun i' =>
    (if needAux (i' + 1) 1 then [[(holeLit (i' + 1)).neg, sAux (i' + 1) 1]] else []) ++
      diagClauses (kBound + 1) (i' + 1) 1

/-! ### The lex-leader clauses (p2_sb.py) -/

/-- The 27 pairs `(s, τ s)` of every certificate (cert.json `sb_pairs`, identical for all 105 cubes). -/
def sbPairs : List (Fin 70 × Fin 70) :=
  [(32, 37), (29, 25), (39, 45), (24, 30), (46, 52), (47, 50), (44, 40), (19, 22), (23, 17), (38, 31),
   (16, 12), (57, 53), (33, 36), (43, 42), (48, 51), (11, 7), (56, 54), (27, 26), (62, 58), (18, 21),
   (13, 15), (8, 10), (61, 59), (4, 6), (2, 3), (63, 65), (66, 67)]

def sbeAt (j : Nat) : Atom := sbe ⟨j % 27, Nat.mod_lt _ (by decide)⟩

/-- p2_sb.py:29-38 from pair index `j` on (`e_j` = aux `sbe j`). -/
def sbFrom : Nat → List (Fin 70 × Fin 70) → List (List SLit)
  | _, [] => []
  | j, (s, t) :: rest =>
    let g : List SLit := if j = 0 then [] else [(false, sbeAt (j - 1))]
    [g ++ [(false, sel s), (true, sel t)]] ++
      (if rest.isEmpty then [] else
        [g ++ [(false, sel s), (false, sel t), (true, sbeAt j)], g ++ [(true, sel s), (true, sel t), (true, sbeAt j)]]) ++
      sbFrom (j + 1) rest

@[irreducible] def sbClauses : List (List SLit) := sbFrom 0 sbPairs

end N66E15
