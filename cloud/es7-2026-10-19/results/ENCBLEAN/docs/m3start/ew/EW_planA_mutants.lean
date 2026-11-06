import EncB.M3.Interface

/-!
# M3 early warning (prototype): an exact concrete `Model` and its `tau` on every clause of `genCoded`

Evidence only, evaluated by `#eval` (compiled IR), never by the kernel. For a configuration of `t` nested regular
`m`-gons (`m ∈ {4, 6}`) with exact coordinates in `ℤ[√3]`, it computes
* `chi a b d = [orient(P a, P b, P d) > 0]` exactly, `psiLt i j = [ψ_i < ψ_j]` exactly;
* the chain variables by the least fixpoint (`ChainFrom`, level by level);
then it checks (1) every `Model` field as a Boolean statement over all valid labels and (2) that every clause of
`genCoded m K t` has a literal that is true under `tau ∘ decodeCode`.
-/

namespace EncB.EW
open EncB

/-- `a + b√3`. -/
structure Z3 where
  a : Int
  b : Int
  deriving Repr, BEq, Inhabited

instance : Add Z3 := ⟨fun x y => ⟨x.a + y.a, x.b + y.b⟩⟩
instance : Sub Z3 := ⟨fun x y => ⟨x.a - y.a, x.b - y.b⟩⟩
instance : Mul Z3 := ⟨fun x y => ⟨x.a * y.a + 3 * x.b * y.b, x.a * y.b + x.b * y.a⟩⟩

def Z3.ofInt (n : Int) : Z3 := ⟨n, 0⟩

/-- The exact sign of `a + b√3` (`√3` is irrational, so `a² = 3b²` only at `0`). -/
def Z3.sign (x : Z3) : Int :=
  if x.a ≥ 0 && x.b ≥ 0 then (if x.a == 0 && x.b == 0 then 0 else 1)
  else if x.a ≤ 0 && x.b ≤ 0 then -1
  else
    let d := x.a * x.a - 3 * x.b * x.b
    if x.a > 0 then (if d > 0 then 1 else -1) else (if d > 0 then -1 else 1)

/-- `(2 cos (2πk/m), 2 sin (2πk/m))` for `m ∈ {4, 6}`. -/
def rotTab (m k : Nat) : Z3 × Z3 :=
  if m == 6 then
    match k % 6 with
    | 0 => (⟨2, 0⟩, ⟨0, 0⟩) | 1 => (⟨1, 0⟩, ⟨0, 1⟩) | 2 => (⟨-1, 0⟩, ⟨0, 1⟩)
    | 3 => (⟨-2, 0⟩, ⟨0, 0⟩) | 4 => (⟨-1, 0⟩, ⟨0, -1⟩) | _ => (⟨1, 0⟩, ⟨0, -1⟩)
  else
    match k % 4 with
    | 0 => (⟨2, 0⟩, ⟨0, 0⟩) | 1 => (⟨0, 0⟩, ⟨2, 0⟩) | 2 => (⟨-2, 0⟩, ⟨0, 0⟩) | _ => (⟨0, 0⟩, ⟨-2, 0⟩)

/-- `2 · P(i, k)`: the layer-`i` vector `vs[i]` (direction `ψ_i`) rotated by `2πk/m`. -/
def P (m : Nat) (vs : List (Int × Int)) (p : Pt) : Z3 × Z3 :=
  let v := vs.getD p.1 (0, 0)
  let cs := rotTab m p.2
  let x := Z3.ofInt v.1
  let y := Z3.ofInt v.2
  (cs.1 * x - cs.2 * y, cs.2 * x + cs.1 * y)

def orient (A B C : Z3 × Z3) : Z3 := (B.1 - A.1) * (C.2 - A.2) - (B.2 - A.2) * (C.1 - A.1)

def chiB (m : Nat) (vs : List (Int × Int)) (a b d : Pt) : Bool :=
  (orient (P m vs a) (P m vs b) (P m vs d)).sign > 0

/-- `ψ_i < ψ_j`: all `vs[i]` lie in one open half-plane sector, so the cross product orders them. Out of range
layers get the zero vector and are incomparable. -/
def psiLtB (vs : List (Int × Int)) (i j : Nat) : Bool :=
  let u := vs.getD i (0, 0)
  let w := vs.getD j (0, 0)
  decide (u.1 * w.2 - u.2 * w.1 > 0)

def labelsOf (m t : Nat) : List Pt := labels m t

def inQB (m t i : Nat) (a : Pt) : Bool := decide (i ≤ a.1) && decide (a.1 < t) && decide (a.2 < m) && a != (i, 0)

/-- Level tables of `ChainFrom` for pivot `i`: entry `l` (for `2 ≤ l ≤ L`) is the array over `pairCode` of
`ChainFrom M i l a b`, by the recursion `ChainFrom (l+1) a b ↔ InQ a ∧ chi p a b ∧ ∃ c, chi a b c ∧ ChainFrom l b c`. -/
def chainLevels (m t : Nat) (chi : Pt → Pt → Pt → Bool) (i L : Nat) : Array (Array Bool) := Id.run do
  let N := t * m
  let Q := chainQ m t i
  let p : Pt := (i, 0)
  let mut levs : Array (Array Bool) := #[Array.replicate (N * N) true, Array.replicate (N * N) true]
  -- level 2
  let mut cur : Array Bool := Array.replicate (N * N) false
  for a in Q do
    for b in Q do
      if chi p a b then cur := cur.setIfInBounds (pairCode m N a b) true
  levs := levs.push cur
  for _l in rng 3 (L + 1) do
    let prev := cur
    let mut nxt : Array Bool := Array.replicate (N * N) false
    for a in Q do
      for b in Q do
        if chi p a b then
          if Q.any (fun c => chi a b c && prev.getD (pairCode m N b c) false) then
            nxt := nxt.setIfInBounds (pairCode m N a b) true
    cur := nxt
    levs := levs.push cur
  return levs

structure Cfg where
  m : Nat
  K : Nat
  t : Nat
  vs : List (Int × Int)
  /-- mutant switch: 1 = mirror orientations, 2 = reverse the ψ order of layers ≥ 1 -/
  mutant : Nat := 0

def Cfg.chi (C : Cfg) : Pt → Pt → Pt → Bool :=
  if C.mutant == 1 then fun a b d => !chiB C.m C.vs a b d else chiB C.m C.vs
def Cfg.psi (C : Cfg) : Nat → Nat → Bool :=
  if C.mutant == 2 then fun i j => if i == 0 || j == 0 then psiLtB C.vs i j else psiLtB C.vs j i
  else psiLtB C.vs

def Cfg.tables (C : Cfg) : Array (Array (Array Bool)) :=
  ((rng 0 C.t).map fun i => chainLevels C.m C.t C.chi i (chainFL C.K)).toArray

/-- `ChainFrom` from the tables (levels 0 and 1 by their definition). -/
def Cfg.chainB (C : Cfg) (tabs : Array (Array (Array Bool))) (i l : Nat) (a b : Pt) : Bool :=
  if l == 0 then true
  else if l == 1 then inQB C.m C.t i a
  else inQB C.m C.t i a && inQB C.m C.t i b &&
    ((tabs.getD i #[]).getD l #[]).getD (pairCode C.m (C.t * C.m) a b) false

/-- `Model.tau`, computably. -/
def Cfg.tauB (C : Cfg) (tabs : Array (Array (Array Bool))) : Var → Bool
  | .y i j => C.psi i j
  | .h _ => false
  | .orb [a, b, d] => C.chi a b d
  | .orb _ => false
  | .f i l a b => C.chainB tabs i l a b
  | .other _ => false

def Cfg.litB (C : Cfg) (tabs : Array (Array (Array Bool))) (x : Int) : Bool :=
  let v := C.tauB tabs (decodeCode C.m C.K C.t x.natAbs)
  if x > 0 then v else if x < 0 then !v else false

def Cfg.failing (C : Cfg) (tabs : Array (Array (Array Bool))) (cls : List (List Int)) : Nat :=
  (cls.filter fun cl => !(cl.any (C.litB tabs))).length

/-! ### Boolean versions of the `Model` fields -/

def cellB (m : Nat) (o : Pt × Bool) : Nat := if o.2 then o.1.2 else (o.1.2 + m / 2) % m
def objLtB (m : Nat) (psi : Nat → Nat → Bool) (o o' : Pt × Bool) : Bool :=
  decide (cellB m o < cellB m o') || (cellB m o == cellB m o' && psi o.1.1 o'.1.1)
def ccwInB {α : Type} (lt : α → α → Bool) (x z y : α) : Bool :=
  (lt x z && lt z y) || (lt y x && lt x z) || (lt z y && lt y x)
def keysDistinctB (m : Nat) (psi : Nat → Nat → Bool) (a b d : Pt) : Bool :=
  (objs6 a b d).all fun o => (objs6 a b d).all fun o' => o == o' || objLtB m psi o o' || objLtB m psi o' o
def arcB (m : Nat) (psi : Nat → Nat → Bool) (a b d x y : Pt) : Bool :=
  [a, b, d].any fun z => ccwInB (objLtB m psi) (x, true) (z, false) (y, true)
def altB (m : Nat) (psi : Nat → Nat → Bool) (a b d : Pt) : Bool :=
  keysDistinctB m psi a b d && ccwInB (objLtB m psi) (a, true) (b, true) (d, true) &&
  arcB m psi a b d a b && arcB m psi a b d b d && arcB m psi a b d d a
def blockB (m : Nat) (psi : Nat → Nat → Bool) (a b d : Pt) : Bool :=
  keysDistinctB m psi a b d && ccwInB (objLtB m psi) (a, true) (b, true) (d, true) &&
  !arcB m psi a b d a b && !arcB m psi a b d b d

def rotB (m : Nat) (a : Pt) : Pt := (a.1, (a.2 + 1) % m)

/-- Counts of violated `Model` fields (all zero = the configuration gives a `Model`), and the counts of
`AltCCW`/`BlockCCW` triples (to see that the rules are exercised). -/
def Cfg.fieldReport (C : Cfg) (tabs : Array (Array (Array Bool))) : List (String × Nat) :=
  let m := C.m
  let t := C.t
  let L := labels m t
  let ord3 : List (Pt × Pt × Pt) := L.flatMap fun a => L.flatMap fun b => L.map fun d => (a, b, d)
  let dist := ord3.filter fun x => x.1 != x.2.1 && x.1 != x.2.2 && x.2.1 != x.2.2
  let ix := rng 0 (t + 2)
  let psi := C.psi
  let chi := C.chi
  [("collinear", (dist.filter fun x => (orient (P m C.vs x.1) (P m C.vs x.2.1) (P m C.vs x.2.2)).sign == 0).length),
   ("psi_irrefl", (ix.filter fun i => psi i i).length),
   ("psi_trans", (ix.flatMap fun i => ix.flatMap fun j => ix.filter fun k =>
      psi i j && psi j k && !psi i k).length),
   ("psi_total", ((rng 0 t).flatMap fun i => (rng 0 t).filter fun j => i != j && !psi i j && !psi j i).length),
   ("psi_zero", ((rng 1 t).filter fun i => !psi 0 i).length),
   ("chi_rot", (ord3.filter fun x => chi (rotB m x.1) (rotB m x.2.1) (rotB m x.2.2) != chi x.1 x.2.1 x.2.2).length),
   ("chi_cycle", (dist.filter fun x => chi x.2.1 x.2.2 x.1 != chi x.1 x.2.1 x.2.2).length),
   ("chi_swap", (dist.filter fun x => chi x.1 x.2.2 x.2.1 != !chi x.1 x.2.1 x.2.2).length),
   ("ruleA_viol", (dist.filter fun x => altB m psi x.1 x.2.1 x.2.2 && !chi x.1 x.2.1 x.2.2).length),
   ("ruleB_viol", (dist.filter fun x => blockB m psi x.1 x.2.1 x.2.2 && decide (x.2.1.1 ≤ x.1.1) &&
      decide (x.2.1.1 ≤ x.2.2.1) && !chi x.1 x.2.1 x.2.2).length),
   ("nest_viol", ((rng 0 t).flatMap fun i => (rng (i + 1) t).flatMap fun j => (rng 0 m).filter fun k =>
      !chi (i, 0) (i, 1) (j, k)).length),
   ("noChain_viol", ((rng 0 t).flatMap fun i => L.flatMap fun a => L.filter fun b =>
      C.chainB tabs i (C.K - 1) a b).length),
   ("alt_triples", (dist.filter fun x => altB m psi x.1 x.2.1 x.2.2).length),
   ("block_triples", (dist.filter fun x => blockB m psi x.1 x.2.1 x.2.2).length)]

/-- Clause counts and failures per family of `genCoded`. -/
def Cfg.clauseReport (C : Cfg) (tabs : Array (Array (Array Bool))) : List (String × Nat) :=
  let m := C.m
  let K := C.K
  let t := C.t
  let ad := (orbList m t).map fun c => (angOutsC m t c).1
  let nest := nestLits m t
  let isF := isFalseIn (forcedOf (fBase m t) (ad.filterMap unitOf ++ nest))
  let tr := transCl t
  let an := ad.flatMap angClOf
  let ne := nest.map (fun l => [l])
  let ch := (rng 0 t).flatMap (chainCl m K t isF)
  let all := genCoded m K t
  [("clauses", all.length), ("fail", C.failing tabs all),
   ("trans", tr.length), ("trans_fail", C.failing tabs tr),
   ("ang", an.length), ("ang_fail", C.failing tabs an),
   ("nest", ne.length), ("nest_fail", C.failing tabs ne),
   ("chain", ch.length), ("chain_fail", C.failing tabs ch),
   ("same_as_genCoded", if tr ++ an ++ ne ++ ch == all then 1 else 0)]

def Cfg.report (C : Cfg) : String :=
  let tabs := C.tables
  s!"(m,K,t)=({C.m},{C.K},{C.t}) fields={C.fieldReport tabs} clauses={C.clauseReport tabs}"

/-- Layer vectors: layer 0 at angle 0; inner layers with distinct angles in `(0, 2π/m)`, radius ratio about 1/2. -/
def vs6 : List (Int × Int) := [(4096, 0), (1700, 900), (800, 150), (330, 280)]
def vs4 : List (Int × Int) := [(1000, 0), (400, 300), (100, 160), (60, 20)]

end EncB.EW

/-- Second configurations: radius ratios close to the apothem bound, other ψ orders. -/
def vs6b : List (Int × Int) := [(10000, 0), (7000, 3000), (5500, 600), (3700, 2700), (2800, 1500)]

open EncB.EW in
#eval (do
  -- base run (fast): the target parity m = 6 at K = 8, and m = 4
  IO.println ({ m := 6, K := 8, t := 2, vs := vs6 } : Cfg).report
  IO.println ({ m := 6, K := 8, t := 3, vs := vs6 } : Cfg).report
  IO.println ({ m := 4, K := 8, t := 3, vs := vs4 } : Cfg).report
  IO.println ({ m := 6, K := 10, t := 3, vs := vs6b } : Cfg).report
  -- mutants: the test must see violations
  IO.println ({ m := 6, K := 8, t := 3, vs := vs6, mutant := 1 } : Cfg).report
  IO.println ({ m := 6, K := 8, t := 3, vs := vs6, mutant := 2 } : Cfg).report
  IO.println ({ m := 6, K := 10, t := 4, vs := vs6b, mutant := 2 } : Cfg).report
  IO.println ({ m := 4, K := 8, t := 4, vs := vs4, mutant := 2 } : Cfg).report : IO Unit)
