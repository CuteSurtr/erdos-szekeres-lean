import N66E15.States
import N66R15Chk.Tables

/-!
# N66R15Chk.Look: table lookups and the Bool checks that tie them to n66enc's definitions (Std-only)

* `neQ`, `mnQ`, `mxQ` (plain-domain statistics from `psRow`), `ttQ` (the six-order test written with them, same
  shape as `N66E15.ttF`), `ttB` (bit of `ttRow`), `drB` (bit of `drRow`), `canB` (bit of `canRow`).
* `psChk u`, `ttChk a`, `drChk u`, `canChk u`: Bool statements "row `u` of the table agrees with n66enc's
  definition" (`nePlain`/`mnPlain`/`mxPlain`, `ttQ` on every set bit, `domRef`, `canF`), evaluated by the kernel in
  `N66R15Chk.TabChk*` (`decide +kernel`, chunks of rows).
-/

namespace N66R15Chk
open N66E15

def psCode (u v : Nat) : Nat := (psRow u >>> (16 * v)) % 65536

def neQ (u v : Fin 70) : Bool := psCode u.val v.val % 2 == 1

def mnQ (coord : Bool) (u v : Fin 70) : Nat :=
  if coord then psCode u.val v.val / 128 % 8 else psCode u.val v.val / 2 % 8

def mxQ (coord : Bool) (u v : Fin 70) : Nat :=
  if coord then psCode u.val v.val / 1024 % 8 else psCode u.val v.val / 16 % 8

def psChk (u : Fin 70) : Bool := (List.finRange 70).all fun v =>
  neQ u v == nePlain u v && mnQ false u v == mnPlain false u v && mxQ false u v == mxPlain false u v &&
    mnQ true u v == mnPlain true u v && mxQ true u v == mxPlain true u v

def psChkN (u : Nat) : Bool := if h : u < 70 then psChk ⟨u, h⟩ else true

/-- `N66E15.ttF` with the statistics read from `psRow`. -/
def ttQ (a b c : Fin 70) : Bool :=
  decide (a ≠ b ∧ b ≠ c ∧ a ≠ c) &&
    (sixOrders a b c).all fun o =>
      let p := o.1; let q := o.2.1; let r := o.2.2.1; let coord := o.2.2.2
      !(neQ p q && neQ q r && neQ p r) || decide (mxQ coord q r ≤ mnQ coord p q)

def ttQN (a b c : Nat) : Bool :=
  if h : a < 70 ∧ b < 70 ∧ c < 70 then ttQ ⟨a, h.1⟩ ⟨b, h.2.1⟩ ⟨c, h.2.2⟩ else false

def ttB (a b c : Nat) : Bool := Nat.testBit (ttRow a) (b * 70 + c)

def ttChk (a : Nat) : Bool := (List.range 4900).all fun i => !Nat.testBit (ttRow a) i || ttQN a (i / 70) (i % 70)

def drB (u v a b : Nat) : Bool :=
  if 1 ≤ a ∧ a ≤ 4 ∧ 1 ≤ b ∧ b ≤ 4 then Nat.testBit (drRow u) (16 * v + 4 * (a - 1) + (b - 1)) else false

def drChk (u : Fin 70) : Bool := (List.finRange 70).all fun v =>
  grid.all fun z => drB u.val v.val z.1 z.2 == domRef (prof u) (prof v) z

def drChkN (u : Nat) : Bool := if h : u < 70 then drChk ⟨u, h⟩ else true

def canB (u v : Nat) : Bool := Nat.testBit (canRow u) v

def canChk (u : Fin 70) : Bool := (List.finRange 70).all fun v => canB u.val v.val == canF u v

def canChkN (u : Nat) : Bool := if h : u < 70 then canChk ⟨u, h⟩ else true

end N66R15Chk
