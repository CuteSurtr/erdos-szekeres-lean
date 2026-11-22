import RowEnc.StatesData

/-!
# RowEnc.States: cell tests and the bounding-box triple test of coupled.py (Std-only)

Python (killtools/coupled.py, sha256 959072b1, and common.py): `CELLS[s] = {(i+1, y) : i < 4, 1 ≤ y ≤ STATES[s][i]}`;
`DIFF[a][b] = CELLS[b] − CELLS[a] − {(1,6)}` (empty-direction and domain clauses); the triple table `TT` uses the
plain difference `CELLS[b] − CELLS[a]` (its bounding box `mn`/`mx`, `nonempty`) and the six-order test.

Lean: `cont sh a b` is the library's `Domains.Contains sh (a, b)`; on the 4 × 6 grid `grid46` (the library's
`ResidualDomains.grid`, same order as Python's `for a in range(1,5): for b in range(1,7)`) it is `(a,b) ∈ CELLS`,
since every height is at most 6. `bbox` is the bounding box of the plain difference, `ttB` the six-order test with
the conjunct order of `CycleSigns.CheckTriple`. Soundness never assumes that these equal Python's tables: the
printed CNFs are hash-compared with the certified files (E1), and `RowGeo` proves what the clauses need.
-/

namespace RowEnc

/-- The shape (column heights, then 0) of residual state `s`. -/
def st (s : Nat) : List Nat := stateTable.getD s []

/-- First column height `STATES[s][0]` (coupled.py line 64). -/
def h1 (s : Nat) : Nat := (st s).getD 0 0

/-- `Domains.Contains sh (a, b)`. -/
def cont (sh : List Nat) (a b : Nat) : Bool := decide (b ≤ sh.getD (a - 1) 0)

/-- The labels (a, b), 1 ≤ a ≤ 4, 1 ≤ b ≤ 6, in Python's loop order (= `ResidualDomains.grid`). -/
def grid46 : List (Nat × Nat) := (List.range 4).flatMap (fun x => (List.range 6).map (fun y => (x + 1, y + 1)))

/-- `(a,b) ∈ DIFF[su][sv]` = `CELLS[sv] − CELLS[su] − {(1,6)}` (the library's `Coupled.Allowed`). -/
def allowedB (su sv : Nat) (z : Nat × Nat) : Bool :=
  cont (st sv) z.1 z.2 && !cont (st su) z.1 z.2 && !(z.1 == 1 && z.2 == 6)

/-- `not DIFF[su][sv]` (the library's `Coupled.emptyCheck`). -/
def emptyB (su sv : Nat) : Bool := grid46.all (fun z => !allowedB su sv z)

/-- A box (the fields of the library's `Domains.Box`). -/
structure BoxS where
  present : Bool
  xmin : Nat
  xmax : Nat
  ymin : Nat
  ymax : Nat

/-- The plain difference `CELLS[sb] − CELLS[sa]`, as grid labels. -/
def diffCells (sa sb : Nat) : List (Nat × Nat) :=
  grid46.filter (fun z => cont (st sb) z.1 z.2 && !cont (st sa) z.1 z.2)

/-- Its bounding box (`nonempty`, `mn`, `mx` of coupled.py lines 13-21). -/
def bbox (sa sb : Nat) : BoxS :=
  match diffCells sa sb with
  | [] => ⟨false, 0, 0, 0, 0⟩
  | z :: zs => ⟨true, zs.foldl (fun m w => min m w.1) z.1, zs.foldl (fun m w => max m w.1) z.1,
      zs.foldl (fun m w => min m w.2) z.2, zs.foldl (fun m w => max m w.2) z.2⟩

/-- `CycleSigns.Safe` as a Boolean. -/
def safeB (ab bc ac : BoxS) (want : Bool) : Bool :=
  !ab.present || !bc.present || !ac.present ||
    (if want then decide (bc.xmax ≤ ab.xmin) else decide (bc.ymax ≤ ab.ymin))

/-- The six-order test `TT[a,b,c]` (coupled.py lines 22-30; conjunct order of `CycleSigns.CheckTriple`). -/
def ttB (a b c : Nat) : Bool :=
  safeB (bbox a b) (bbox b c) (bbox a c) true && safeB (bbox a c) (bbox c b) (bbox a b) false &&
  safeB (bbox b a) (bbox a c) (bbox b c) false && safeB (bbox b c) (bbox c a) (bbox b a) true &&
  safeB (bbox c a) (bbox a b) (bbox c b) true && safeB (bbox c b) (bbox b a) (bbox c a) false

end RowEnc
