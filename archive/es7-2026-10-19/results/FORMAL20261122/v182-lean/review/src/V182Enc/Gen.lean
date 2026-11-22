import EncB.Render

/-!
# V182Enc.Gen: the CNF of the rainbow 5-colouring question on the 182-vertex graph (Std-only)

Re-implementation, as Lean clause lists, of wave 1's generator (pinned copies `ref/rainbow.py`, `ref/cubes.py`,
sha256 in `ref/SHA256SUMS.ref`):

* `baseCnf`: `rainbow.py cnf g182.json 5 OUT --strong` plus the 10 symmetry units, i.e. the file
  `a2/g182_k5_st_sb2.cnf` (sha256 c3ae5224…7074); families in file order:
  ALO (rainbow.py:110), `sorted(cls)` (rainbow.py:98-101,111), AMO (rainbow.py:115-117), star clauses
  (rainbow.py:118-124), units (wave-1 README 3.3).
* `pieceCube`: the units of the cube pieces (cubes.py:24-27): a Y1 cube puts the `n`-th lexicographic permutation
  of the colours on the star of mask 47; a Y2 sub-cube appends the `m`-th permutation on the star of mask 55.
* `pieceText`: the text of a piece file, `EncB.renderCube nVars baseCnf (EncB.bodyR baseCnf) (pieceCube pc)`
  (header with the clause count raised, B's clause lines, one line per unit; cubes.py:27).

Nothing here is trusted for byte identity: the printed texts are hashed against the certified files (M1, M9).
Numbering (rainbow.py `graph182`): vertices are the masks `m < 256` with 3, 4 or 5 bits, in increasing order; edge
`e = 8 r + x` joins the `r`-th 4-set mask `T` and `T ^^^ 2^x`; variable `lit e c = 5 e + c + 1`.
-/

namespace V182Enc

/-- The number of elements of the subset of `{0..7}` with mask `m`. -/
def pc (m : Nat) : Nat := ((List.range 8).filter fun i => m.testBit i).length

/-- The 4-set masks in increasing order. -/
def fourMasks : List Nat := (List.range 256).filter fun m => pc m == 4

/-- The 3-set masks in increasing order. -/
def threeMasks : List Nat := (List.range 256).filter fun m => pc m == 3

/-- The vertex masks (3, 4 or 5 elements) in increasing order. -/
def vtxMasks : List Nat := (List.range 256).filter fun m => 3 ≤ pc m && pc m ≤ 5

/-- The number of edges. -/
def numE : Nat := 560

/-- The 4-set end of edge `e`. -/
def eT (e : Nat) : Nat := fourMasks.getD (e / 8) 0

/-- The other end of edge `e` (a 3-set if bit `e % 8` is in `eT e`, else a 5-set). -/
def eO (e : Nat) : Nat := eT e ^^^ (1 <<< (e % 8))

/-- The index of the edge between the 4-set `T` and `T ^^^ 2^x`. -/
def eidx (T x : Nat) : Nat := 8 * fourMasks.idxOf T + x

/-- The structural 4-cycle `(X, X+p, X+p+q, X+q)` (`X` a 3-set, `p, q ∉ X`): its four edges in cyclic order. -/
def cyc (X p q : Nat) : List Nat :=
  [eidx (X ||| 1 <<< p) p, eidx (X ||| 1 <<< p) q, eidx (X ||| 1 <<< q) p, eidx (X ||| 1 <<< q) q]

/-- The pairs `p < q` of bits outside `X`. -/
def bitPairs (X : Nat) : List (Nat × Nat) :=
  ((List.range 8).flatMap fun p => (List.range 8).map fun q => (p, q)).filter fun pq =>
    pq.1 < pq.2 && !X.testBit pq.1 && !X.testBit pq.2

/-- The 560 structural 4-cycles. -/
def cycles : List (List Nat) := threeMasks.flatMap fun X => (bitPairs X).map fun pq => cyc X pq.1 pq.2

/-- Two edges conflict: they are distinct and lie in a common structural 4-cycle. -/
def conflict (e f : Nat) : Bool := e != f && cycles.any fun z => z.contains e && z.contains f

/-- The DIMACS variable "edge `e` has colour `c`" (rainbow.py: `x(e, c) = e k + c + 1`, `k = 5`). -/
def lit (e c : Nat) : Int := ((5 * e + c + 1 : Nat) : Int)

/-- (1) at least one colour per edge (rainbow.py:110). -/
def aloCls : List (List Int) := (List.range numE).map fun e => (List.range 5).map (lit e)

/-- The conflict partners `f > e` of `e`, decreasing. -/
def partnersDesc (e : Nat) : List Nat := ((List.range numE).filter fun f => e < f && conflict e f).reverse

/-- (2) `sorted(cls)` (rainbow.py:98-101,111): the clauses `(-x(e,c), -x(f,c))` for conflicting `e < f`; Python
sorts these tuples of negative numbers increasingly, i.e. by `e` decreasing, then `c` decreasing, then `f`
decreasing. -/
def confCls : List (List Int) :=
  (List.range numE).reverse.flatMap fun e =>
    (List.range 5).reverse.flatMap fun c => (partnersDesc e).map fun f => [-lit e c, -lit f c]

/-- `--strong`: at most one colour per edge, colour pairs in `itertools.combinations` order (rainbow.py:115-117). -/
def amoCls : List (List Int) :=
  (List.range numE).flatMap fun e =>
    (List.range 5).flatMap fun c1 => ((List.range 5).filter (c1 < ·)).map fun c2 => [-lit e c1, -lit e c2]

/-- The edges at the vertex with mask `v`, increasing (rainbow.py `inc`). -/
def star (v : Nat) : List Nat := (List.range numE).filter fun e => eT e == v || eO e == v

/-- Every two distinct edges of `L` conflict. -/
def allConf (L : List Nat) : Bool := L.all fun e => L.all fun f => e == f || conflict e f

/-- `--strong`: every colour on a star of 5 pairwise conflicting edges (rainbow.py:118-124). -/
def surjCls : List (List Int) :=
  vtxMasks.flatMap fun v =>
    if (star v).length == 5 && allConf (star v) then (List.range 5).map fun c => (star v).map fun e => lit e c
    else []

/-- The 10 symmetry units as (edge, colour) (wave-1 README 3.3): `σ_X0(x) = x - 3` on the edges
`{0,1,2}`-`{0,1,2,x}`, `x = 3..7`, and `τ_Y0 = (0,1,4,2,3)` on the edges `{0..4}`-(`{0..4}` minus `y`), `y = 0..4`. -/
def unitPairs : List (Nat × Nat) :=
  [(3, 0), (12, 1), (45, 2), (126, 3), (287, 4), (32, 0), (25, 1), (18, 4), (11, 2), (4, 3)]

def unitCls : List (List Int) := unitPairs.map fun ec => [lit ec.1 ec.2]

/-- **The base CNF B** (`a2/g182_k5_st_sb2.cnf`). -/
def baseCnf : List (List Int) := aloCls ++ confCls ++ amoCls ++ surjCls ++ unitCls

/-- The header variable count of every file. -/
def nVars : Nat := 2800

/-! ## The cube pieces -/

/-- The permutations of `l` in the order of `itertools.permutations` (lexicographic for increasing `l`). -/
def permsOf : Nat → List Nat → List (List Nat)
  | 0, _ => [[]]
  | k + 1, l => l.flatMap fun a => (permsOf k (l.erase a)).map (a :: ·)

/-- The 120 permutations of `0..4`, lexicographic. -/
def perms5 : List (List Nat) := permsOf 5 (List.range 5)

/-- The star of mask 47 = `{0,1,2,3,5}` (Y1). -/
def y1Star : List Nat := [5, 43, 50, 57, 64]

/-- The star of mask 55 = `{0,1,2,4,5}` (Y2). -/
def y2Star : List Nat := [13, 44, 74, 81, 88]

/-- The units of cube `n` on the star `S`: `x(S_i, π_n(i))` (cubes.py:25). -/
def starUnits (S : List Nat) (n : Nat) : List Int := List.zipWith lit S (perms5.getD n [])

/-- The 36 Y1 cubes that are split into 120 Y2 sub-cubes; the other 84 are refuted directly. -/
def splitSet : List Nat :=
  [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 78, 79, 80, 81, 82, 83, 90, 91, 92, 93, 94, 95,
   102, 103, 104, 105, 106, 107, 114, 115, 116, 117, 118, 119]

/-- **The 4,404 pieces**: `(n, none)` = Y1 cube `n` (direct), `(n, some m)` = its Y2 sub-cube `m`. -/
def pieces : List (Nat × Option Nat) :=
  (List.range 120).flatMap fun n =>
    if splitSet.contains n then (List.range 120).map fun m => (n, some m) else [(n, none)]

/-- The units of a piece. -/
def pieceCube : Nat × Option Nat → List Int
  | (n, none) => starUnits y1Star n
  | (n, some m) => starUnits y1Star n ++ starUnits y2Star m

/-- **The text of a piece file** (what `v182print` writes; hash-bound in M9). -/
def pieceText (q : Nat × Option Nat) : String :=
  EncB.renderCube nVars baseCnf (EncB.bodyR baseCnf) (pieceCube q)

/-- The text of B itself. -/
def baseText : String := EncB.render nVars baseCnf

end V182Enc
