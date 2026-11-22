/-!
# N66Enc.States: the 70 states of the 4 × 4 box and their tables (Std-only)

Port of `etv_common.py` (SHA-256 `12f00cc6…2542725`) for `ETV_A = ETV_B = 4`:

* `stateList` = `etv_common.STATES`: the nonincreasing column-height tuples `(f₁, f₂, f₃, f₄)` with entries in
  `0..4`, sorted by `(sum f, f)` (`profiles()`, etv_common.py:23-27). The literal is checked against that
  definition by `stateList_eq_sorted` (kernel, 70 entries).
* cells: `(a, y)` with `1 ≤ a ≤ 4`, `1 ≤ y ≤ f_a` (column `a` = cap coordinate `a`, height = cup coordinate).
* `capH s` = number of nonempty columns, `cupH s = f₁` (etv_common.py:33-34).
* `domPlain s t z` = `z ∈ cells t \ cells s`; `domRef s t z` additionally `z.1 ≤ capH s + 1`, `z.2 ≤ cupH s + 1`
  (etv_common.py:36-40).
* `can u v` = `domRef u v` is nonempty (`lazymono.py:32`; W = range(70), so state = index).
* `tt a b c` = `etv_common.TT[a, b, c]`, the six-order test computed from the **plain** domains
  (`coupled5.TT = ec.TT`; etv_common.py:45-68).
* `tau` = the transposition of states (conjugate partition), `p2_sb.TAU`.

Nothing here is evaluated by the kernel on the CNF instance; the tables are small (70 states).
-/

namespace N66Enc

/-- A state: the column heights `(f₁, f₂, f₃, f₄)`. -/
abbrev Prof := Nat × Nat × Nat × Nat

def Prof.sum (p : Prof) : Nat := p.1 + p.2.1 + p.2.2.1 + p.2.2.2

/-- Column `a` (1-based) of a profile; 0 outside `1..4`. -/
def Prof.col (p : Prof) (a : Nat) : Nat :=
  if a = 1 then p.1 else if a = 2 then p.2.1 else if a = 3 then p.2.2.1 else if a = 4 then p.2.2.2 else 0

/-- `etv_common.STATES` for A = B = 4 (printed by the pinned copy `ref/etv_common.py`). -/
def stateList : List Prof :=
  [(0,0,0,0), (1,0,0,0), (1,1,0,0), (2,0,0,0), (1,1,1,0), (2,1,0,0), (3,0,0,0), (1,1,1,1), (2,1,1,0),
   (2,2,0,0), (3,1,0,0), (4,0,0,0), (2,1,1,1), (2,2,1,0), (3,1,1,0), (3,2,0,0), (4,1,0,0), (2,2,1,1),
   (2,2,2,0), (3,1,1,1), (3,2,1,0), (3,3,0,0), (4,1,1,0), (4,2,0,0), (2,2,2,1), (3,2,1,1), (3,2,2,0),
   (3,3,1,0), (4,1,1,1), (4,2,1,0), (4,3,0,0), (2,2,2,2), (3,2,2,1), (3,3,1,1), (3,3,2,0), (4,2,1,1),
   (4,2,2,0), (4,3,1,0), (4,4,0,0), (3,2,2,2), (3,3,2,1), (3,3,3,0), (4,2,2,1), (4,3,1,1), (4,3,2,0),
   (4,4,1,0), (3,3,2,2), (3,3,3,1), (4,2,2,2), (4,3,2,1), (4,3,3,0), (4,4,1,1), (4,4,2,0), (3,3,3,2),
   (4,3,2,2), (4,3,3,1), (4,4,2,1), (4,4,3,0), (3,3,3,3), (4,3,3,2), (4,4,2,2), (4,4,3,1), (4,4,4,0),
   (4,3,3,3), (4,4,3,2), (4,4,4,1), (4,4,3,3), (4,4,4,2), (4,4,4,3), (4,4,4,4)]

/-- Nonincreasing tuples over `0..4`, in `itertools.product(range(5), repeat=4)` order. -/
def rawProfiles : List Prof :=
  ((List.range 5).flatMap fun a => (List.range 5).flatMap fun b =>
    (List.range 5).flatMap fun c => (List.range 5).map fun d => ((a, b, c, d) : Prof)).filter
    fun p => decide (p.2.1 ≤ p.1 ∧ p.2.2.1 ≤ p.2.1 ∧ p.2.2.2 ≤ p.2.2.1)

/-- Lexicographic `≤` on 4-tuples (Python tuple order). -/
def lexLe (p q : Prof) : Bool :=
  decide (p.1 < q.1) || (decide (p.1 = q.1) && (decide (p.2.1 < q.2.1) || (decide (p.2.1 = q.2.1) &&
    (decide (p.2.2.1 < q.2.2.1) || (decide (p.2.2.1 = q.2.2.1) && decide (p.2.2.2 ≤ q.2.2.2))))))

/-- Python's sort key `(sum(f), f)`. -/
def profLe (p q : Prof) : Bool :=
  decide (p.sum < q.sum) || (decide (p.sum = q.sum) && lexLe p q)

/-- Consecutive entries strictly increasing for `profLe`. -/
def chainLt : List Prof → Bool
  | p :: q :: rest => (profLe p q && p != q) && chainLt (q :: rest)
  | _ => true

/-- The literal is `profiles()` of etv_common.py: its entries are nonincreasing tuples over `0..4`, there are as
many as such tuples (70), and they are strictly increasing in the key `(sum, tuple)`; so it is the sorted list. -/
def stateListOk : Bool :=
  stateList.all (rawProfiles.contains ·) && stateList.length == rawProfiles.length && chainLt stateList

theorem stateListOk_true : stateListOk = true := by decide +kernel

/-- The state table as an array (closed term, computed once by the printer). -/
def stateArr : Array Prof := stateList.toArray

/-- The profile of state `s < 70`. -/
def prof (s : Fin 70) : Prof := stateArr.getD s.val (0, 0, 0, 0)

/-- `(x, y)` is a cell of `p`: `1 ≤ x ≤ 4` and `1 ≤ y ≤ f_x`. -/
def cellIn (p : Prof) (x y : Nat) : Bool := decide (1 ≤ x ∧ x ≤ 4 ∧ 1 ≤ y ∧ y ≤ p.col x)

def capH (p : Prof) : Nat :=
  (if 0 < p.1 then 1 else 0) + (if 0 < p.2.1 then 1 else 0) + (if 0 < p.2.2.1 then 1 else 0) +
    (if 0 < p.2.2.2 then 1 else 0)

def cupH (p : Prof) : Nat := p.1

/-- The grid `[1..4] × [1..4]` (coordinates (cap, cup)). -/
def grid : List (Nat × Nat) := (List.range 4).flatMap fun x => (List.range 4).map fun y => (x + 1, y + 1)

/-- Plain directed domain `D(s → t) = cells t \ cells s`. -/
def domPlain (s t : Prof) (z : Nat × Nat) : Bool := cellIn t z.1 z.2 && !cellIn s z.1 z.2

/-- Refined directed domain `D'(s → t)` (rank attainment). -/
def domRef (s t : Prof) (z : Nat × Nat) : Bool :=
  domPlain s t z && decide (z.1 ≤ capH s + 1) && decide (z.2 ≤ cupH s + 1)

/-- `can[u][v]` of lazymono.py:32: the refined domain is nonempty. -/
def canF (u v : Fin 70) : Bool := grid.any (domRef (prof u) (prof v))

/-- Plain domain nonempty. -/
def nePlain (u v : Fin 70) : Bool := grid.any (domPlain (prof u) (prof v))

/-- `mn[coord][u, v]` / `mx[coord][u, v]` of `triple_table` over the plain domain (0 if empty). -/
def coordOf (coord : Bool) (z : Nat × Nat) : Nat := if coord then z.2 else z.1

def mnPlain (coord : Bool) (u v : Fin 70) : Nat :=
  match (grid.filter (domPlain (prof u) (prof v))).map (coordOf coord) with
  | [] => 0
  | x :: xs => xs.foldl min x

def mxPlain (coord : Bool) (u v : Fin 70) : Nat :=
  match (grid.filter (domPlain (prof u) (prof v))).map (coordOf coord) with
  | [] => 0
  | x :: xs => xs.foldl max x

/-- The six orders `(p, q, r)` of `(a, b, c)` with their parity (`True` = odd), in
`itertools.permutations(range(3))` order. -/
def sixOrders (a b c : Fin 70) : List (Fin 70 × Fin 70 × Fin 70 × Bool) :=
  [(a, b, c, false), (a, c, b, true), (b, a, c, true), (b, c, a, false), (c, a, b, false), (c, b, a, true)]

/-- `etv_common.TT[a, b, c]` (plain domains): distinct, and for every order whose three directed domains are
nonempty, `mx[coord][q, r] ≤ mn[coord][p, q]` with `coord = 1` (cup) for odd orders, `0` (cap) for even ones. -/
def ttF (a b c : Fin 70) : Bool :=
  decide (a ≠ b ∧ b ≠ c ∧ a ≠ c) &&
    (sixOrders a b c).all fun o =>
      let p := o.1; let q := o.2.1; let r := o.2.2.1; let coord := o.2.2.2
      !(nePlain p q && nePlain q r && nePlain p r) || decide (mxPlain coord q r ≤ mnPlain coord p q)

/-- Tables for the printer (closed terms). -/
def canArr : Array Bool := Array.ofFn (n := 4900) fun i =>
  canF ⟨i.val / 70, by omega⟩ ⟨i.val % 70, Nat.mod_lt _ (by decide)⟩

def can (u v : Fin 70) : Bool := canArr.getD (u.val * 70 + v.val) false

def ttArr : Array Bool := Array.ofFn (n := 343000) fun i =>
  ttF ⟨i.val / 4900, by omega⟩ ⟨i.val / 70 % 70, Nat.mod_lt _ (by decide)⟩
    ⟨i.val % 70, Nat.mod_lt _ (by decide)⟩

def tt (a b c : Fin 70) : Bool := ttArr.getD (a.val * 4900 + b.val * 70 + c.val) false

/-- Transposed profile (conjugate partition): `h'_x = #{a : f_a ≥ x}`. -/
def Prof.transpose (p : Prof) : Prof :=
  let h (x : Nat) : Nat := (if x ≤ p.1 then 1 else 0) + (if x ≤ p.2.1 then 1 else 0) +
    (if x ≤ p.2.2.1 then 1 else 0) + (if x ≤ p.2.2.2 then 1 else 0)
  (h 1, h 2, h 3, h 4)

/-- `p2_sb.TAU` (the printed value of the pinned copy, `ref/p2_sb.py`). -/
def tauList : List Nat :=
  [0, 1, 3, 2, 6, 5, 4, 11, 10, 9, 8, 7, 16, 15, 14, 13, 12, 23, 21, 22, 20, 18, 19, 17, 30, 29, 27, 26, 28,
   25, 24, 38, 37, 36, 34, 35, 33, 32, 31, 45, 44, 41, 43, 42, 40, 39, 52, 50, 51, 49, 47, 48, 46, 57, 56, 55,
   54, 53, 62, 61, 60, 59, 58, 65, 64, 63, 67, 66, 68, 69]

/-- `tauList` is the transposition of states. -/
theorem tauList_spec : ∀ i < 70, stateList.getD (tauList.getD i 0) (0,0,0,0) =
    (stateList.getD i (0,0,0,0)).transpose := by decide +kernel

end N66Enc
