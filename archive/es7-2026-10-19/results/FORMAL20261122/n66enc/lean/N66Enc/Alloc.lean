import EncB.Dimacs
import N66Enc.Clauses

/-!
# N66Enc.Alloc: the generator's variable numbering (Std-only)

`pyAlloc` lists the codes of the atoms in the order in which the generator allocates DIMACS variables:

1. coupled5.py:38-43: per pair (combinations order) `before, cap_ge 2..4, cup_ge 2..4`; per triple `orientation`;
   per 4-set `convex_four` (allocated, unused);
2. lazymono.py:30: `sel[0..69]`;
3. lazymono.py:61-62: per can-triple (permutations order) `C3, U3, C4, U4, C5, U5`;
4. lazymono.py:70: `CE, UE` at the first can-triple of each end pair;
5. pysat seqcounter aux, first reference in clause order (`top_id = E.top`);
6. p2_sb.py:36: `e_0 … e_25`.

`num a = 1 + (first position of a.code in pyAlloc)` through `EncB.numberMap` (an array indexed by code), and
`nAlloc + 1 + a.code` for an atom that is not allocated (never printed: the printer refuses literals above the header
count). Soundness never depends on these numbers being Python's (ENCBLEAN D4); byte identity checks them.
-/

namespace N66Enc
open Atom

def pairAtoms (_ : Unit) : List Atom :=
  comb2.flatMap fun p => [before p.1 p.2, capGe p.1 p.2 2, capGe p.1 p.2 3, capGe p.1 p.2 4,
    cupGe p.1 p.2 2, cupGe p.1 p.2 3, cupGe p.1 p.2 4]

def orientAtoms (_ : Unit) : List Atom := comb3.map fun t => orient t.1 t.2.1 t.2.2

def convexAtoms (_ : Unit) : List Atom := (comb4 ()).map fun q => convex q.1 q.2.1 q.2.2.1 q.2.2.2

def selAtoms : List Atom := fr70.map sel

def chainAtoms (_ : Unit) : List Atom :=
  perm3.flatMap fun t =>
    if canTriple t.1 t.2.1 t.2.2 then
      [chC 3 t.1 t.2.1 t.2.2, chU 3 t.1 t.2.1 t.2.2, chC 4 t.1 t.2.1 t.2.2, chU 4 t.1 t.2.1 t.2.2,
       chC 5 t.1 t.2.1 t.2.2, chU 5 t.1 t.2.1 t.2.2]
    else []

def ceueAtoms (_ : Unit) : List Atom :=
  perm3.flatMap fun t =>
    if canTriple t.1 t.2.1 t.2.2 && firstMid t.1 t.2.1 t.2.2 then [ce t.1 t.2.2, ue t.1 t.2.2] else []

/-- The counter aux atoms in first-reference order. -/
def cntAtoms : List Atom :=
  ((cardClauses.flatMap fun cl => cl.map (·.2)).filter fun a => match a with
    | cnt _ _ => true
    | _ => false).eraseDups

def sbeAtoms : List Atom := (List.range 26).map sbeAt

/-- The allocation order (codes). -/
@[irreducible] def pyAlloc (_ : Unit) : List Nat :=
  (pairAtoms () ++ orientAtoms () ++ convexAtoms () ++ selAtoms ++ chainAtoms () ++ ceueAtoms () ++ cntAtoms ++
    sbeAtoms).map Atom.code

/-- code ↦ number (0 = not allocated). Defined directly (not through a shared pair) so that the equation
`pyMap = EncB.numberMap (pyAlloc ())` is one delta step: through a projection the elaborator unfolded
`numberMap` first and started evaluating the 1.65M-entry list (scratch test T5, timeout at `whnf`). -/
@[irreducible] def pyMap : Array Nat := EncB.numberMap (pyAlloc ())

@[irreducible] def nAlloc : Nat := (pyAlloc ()).length

/-- The numbering through a code table `M` (0 = no number) and an allocation length `N`: allocated atoms get
their table entry, the others `N + 1 + code`. Generic in `M`, `N`, so that the lemmas of `N66Enc.DecodeB` are
proved for a variable list and only instantiated (by substitution) at `pyAlloc ()`; the kernel never has to
compare arithmetic over the 1.65M-entry list (its Nat extension would evaluate it). -/
def numWith (M : Array Nat) (N : Nat) (a : Atom) : Nat :=
  let m := M.getD a.code 0
  if m = 0 then N + 1 + a.code else m

/-- The DIMACS number of an atom. -/
def num (a : Atom) : Nat := numWith pyMap nAlloc a

def litInt (l : SLit) : Int := if l.1 then (num l.2 : Int) else -(num l.2 : Int)

/-- A structured clause as a DIMACS clause. -/
def toDimacs (cl : List SLit) : List Int := cl.map litInt

/-- The header variable count of every certificate (`p cnf 1647808 …`). -/
def nvHeader : Nat := 1647808

end N66Enc
