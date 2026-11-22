import N66Enc.Full

/-!
# N66Enc.Print: the printer's clause selection from runtime data (Std-only)

A certified `trim.cnf` is the list of the cone clauses of a cube's `cert.cnf`, in order (p2_lrat_trim.cpp). The
printer reads, per leaf, one descriptor per clause (written by the untrusted `tools/extract_desc.py`):

| descriptor | clause |
|---|---|
| `E k` | `eagerStream ()[k]` |
| `Q a b c d j` | `(quadClauses a b c d)[j]`, only if `okQuad a b c d` |
| `U k` | `(fixedUnits ++ c.map cubeUnit)[k]` for the leaf cube `c` |
| `R k` | `rowClause R0[k]` |
| `K k` | `cardClauses[k]` |
| `S k` | `sbClauses[k]` |

Anything else makes `printClauses` return `none` (nothing is printed). By construction every clause it returns is a
member of `fullCnf R0 c` (`printClause_mem`, proved in a later milestone), whatever the runtime data are; so their
correctness is not trusted, only the text the exe writes is bound by hash (E1).
-/

namespace N66Enc

inductive Desc
  | e (k : Nat)
  | q (a b c d j : Nat)
  | u (k : Nat)
  | r (k : Nat)
  | k (k : Nat)
  | s (k : Nat)

set_option compiler.extract_closed false in
/-- The eager stream in DIMACS form (the only large constant of the printer; about 1.49M short clauses). -/
@[irreducible] def eagerArr : Array (List Int) := ((eagerStream ()).map toDimacs).toArray

@[irreducible] def cardArr : Array (List SLit) := cardClauses.toArray
@[irreducible] def sbArr : Array (List SLit) := sbClauses.toArray
@[irreducible] def R0arr : Array (List (Fin 70)) := R0.toArray

def toFin70 (n : Nat) : Option (Fin 70) := if h : n < 70 then some ⟨n, h⟩ else none

/-- The DIMACS clause of one descriptor for the leaf cube `c`. -/
def printClause (c : Cube) : Desc → Option (List Int)
  | .e k => eagerArr[k]?
  | .q a b c' d j => do
    let a ← toFin70 a
    let b ← toFin70 b
    let c' ← toFin70 c'
    let d ← toFin70 d
    if okQuad a b c' d then ((quadClauses a b c' d)[j]?).map toDimacs else none
  | .u k => ((fixedUnits ++ c.map cubeUnit)[k]?).map toDimacs
  | .r k => (R0arr[k]?).map fun T => toDimacs (rowClause T)
  | .k k => (cardArr[k]?).map toDimacs
  | .s k => (sbArr[k]?).map toDimacs

/-- The DIMACS clauses of a descriptor list (`none` if one descriptor is invalid). -/
def printClauses (c : Cube) (ds : List Desc) : Option (List (List Int)) := ds.mapM (printClause c)

/-- Every literal nonzero with `natAbs ≤ nv` (the hypothesis of `EncB.parseDimacs_render`). -/
def litsBounded (nv : Nat) (F : List (List Int)) : Bool :=
  F.all fun cl => cl.all fun l => decide (l ≠ 0) && decide (l.natAbs ≤ nv)

/-! ## Reading the descriptor text (untrusted input; its parse is irrelevant to soundness) -/

def parseDesc (line : String) : Option Desc :=
  match (line.splitOn " ").filter (· ≠ "") with
  | ["E", k] => k.toNat?.map .e
  | ["Q", a, b, c, d, j] => do
    pure (.q (← a.toNat?) (← b.toNat?) (← c.toNat?) (← d.toNat?) (← j.toNat?))
  | ["U", k] => k.toNat?.map .u
  | ["R", k] => k.toNat?.map .r
  | ["K", k] => k.toNat?.map .k
  | ["S", k] => k.toNat?.map .s
  | _ => none

def parseDescs (s : String) : Option (List Desc) :=
  ((s.splitOn "\n").filter (· ≠ "")).mapM parseDesc

end N66Enc
