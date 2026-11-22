import RowEnc.DataT
import RowEnc.DataC
import RowChk.Look
import RowGeo.Basic

/-!
# RowChk.Check: the per-row certificate checker (Std-only; evaluated by the kernel in `RowChk.Rows*`)

A row is a list of state numbers (sorted, as in `N66Enc.R0`). Its certificate (`RC`, R0 order, generated from the
record's justifications by tools/gen_rows.py, untrusted) is one of:
* `tr t σ`: transported by template `templates[t]` with the map `σ` (position ↦ state);
* `mt t σ`: mirror image of a row transported by `templates[t]` with `σ`;
* `co c`: core `cores[c]` (its own states);
* `mc c`: mirror image of core `cores[c]`;
* `cy L`: cycle order `L` of eight states.

`chkRow T rc` checks the combinatorial side conditions (tests good for `σ` through the verified tables, `σ` a
duplicate-free list of states of the right length, the row contains the states of `σ` / their mirror images, the
cycle triples pass the six-order test). The CNF verdicts enter only through `RowCertsUnsat` (RowGeo.Assembly).
`certsOk` checks the data of all 629 certificates (`certOk`, and cores without repeated states).
-/

namespace RowChk
open RowEnc

inductive RC where
  | tr (t : Nat) (sig : List Nat)
  | mt (t : Nat) (sig : List Nat)
  | co (c : Nat)
  | mc (c : Nat)
  | cy (ord : List Nat)

def nodupB : List Nat → Bool
  | [] => true
  | x :: xs => !xs.contains x && nodupB xs

def goodN (σ : List Nat) : Test → Bool
  | .E u v => !canB (σ.getD u 0) (σ.getD v 0)
  | .D u v a b => decide (1 ≤ a ∧ a ≤ 4 ∧ 1 ≤ b ∧ b ≤ 4) && !drB (σ.getD u 0) (σ.getD v 0) a b
  | .P p q r => ttB (σ.getD p 0) (σ.getD q 0) (σ.getD r 0)

def sigOk (t : Cert) (σ : List Nat) : Bool :=
  σ.length == t.n && σ.all (· < 70) && nodupB σ && t.tests.all (goodN σ)

def tauN (x : Nat) : Nat := N66Enc.tauList.getD x 0

/-- The 56 index triples `i < j < k < 8`. -/
def tri8 : List (Nat × Nat × Nat) :=
  (List.range 8).flatMap fun i => (List.range 8).flatMap fun j => (List.range 8).filterMap fun k =>
    if i < j ∧ j < k then some (i, j, k) else none

def cycOk (L : List Nat) : Bool :=
  L.length == 8 && L.all (· < 70) && nodupB L && tri8.all fun t => ttB (L.getD t.1 0) (L.getD t.2.1 0) (L.getD t.2.2 0)

def coreStates : Cert → List Nat
  | .core S _ => S.map Fin.val
  | .tmpl _ _ _ => [70]

def chkRow (T : List Nat) : RC → Bool
  | .tr t σ => match templates[t]? with
    | some c => sigOk c σ && σ.all (fun x => T.contains x)
    | none => false
  | .mt t σ => match templates[t]? with
    | some c => sigOk c σ && σ.all (fun x => T.contains (tauN x))
    | none => false
  | .co c => match cores[c]? with
    | some k => (coreStates k).all (fun x => T.contains x)
    | none => false
  | .mc c => match cores[c]? with
    | some k => (coreStates k).all (fun x => T.contains (tauN x))
    | none => false
  | .cy L => cycOk L && L.all (fun x => T.contains x)

def chkRows : List (List Nat) → List RC → Bool
  | T :: Ts, r :: rs => T.all (· < 70) && chkRow T r && chkRows Ts rs
  | [], [] => true
  | _, _ => false

/-- Data validity of a core: `certOk` and no repeated state (`strictUp` of the sorted support). -/
def coreOk (k : Cert) : Bool := certOk k && strictUp (coreStates k)

end RowChk
