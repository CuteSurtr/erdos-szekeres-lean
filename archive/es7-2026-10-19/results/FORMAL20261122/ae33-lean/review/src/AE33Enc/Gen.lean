import AE33Enc.Clause
import Std.Data.HashSet

/-!
# AE33Enc.Gen: the descriptor generator (port of l2enc.cpp's loops) and the CNF (Std-only)

`gen B` lists descriptors in l2enc's order (l2enc.cpp:293-294: R2X, R2Y, ACX, ACY, RAD, GPA, GPP/GPQ interleaved,
OCTX, OCTY, JK), with l2enc's deduplication of the RAD, GP and JK families (key = clause and family, l2enc.cpp:210-214).
Nothing here is trusted: `cnf B = (gen B).toList.filterMap (clauseOf B)`, so every clause of `cnf B` is the clause
of a descriptor that `clauseOf` accepted (DESIGN.md D1). All definitions are total (no `partial`, no
`implemented_by`), so the compiled exe computes the kernel value `cnf B` (trust item E4).
-/

namespace AE33

/-- l2enc `forbid_terms` (l2enc.cpp:172-208) without shortening: the term-sign vectors of the forbidden
assignments, in increasing mask order (variables numbered by first appearance). -/
def forbidSigns (terms : List Term) (pred : List Int → Bool) : List (List Int) := Id.run do
  let mut vars : List Nat := []
  for t in terms do
    match t with
    | .lit l => if !(vars.contains l.natAbs) then vars := vars ++ [l.natAbs]
    | .const _ => pure ()
  let m := vars.length
  let mut res : Array (List Int) := #[]
  for mask in [0 : 2 ^ m] do
    let vals := terms.map fun t =>
      match t with
      | .const s => s
      | .lit l => if decide (0 < l) == ((mask >>> vars.idxOf l.natAbs) % 2 == 1) then (1 : Int) else -1
    if pred vals then res := res.push vals
  return res.toList

/-- R2 for new point `n + w` (l2enc.cpp:133-159). -/
def genR2 (B : Array Pt) (w : Nat) (out : Array Desc) : Array Desc := Id.run do
  let n := B.size
  let mut out := out
  for a in [0:n] do
    let pa := B.getD a (0, 0)
    let mut e : Array (Nat × Int × Int × Int) := #[]
    for x in [0:n] do
      if x != a then
        let px := B.getD x (0, 0)
        let dx := px.1 - pa.1
        let dy := px.2 - pa.2
        let eps : Int := if decide (0 < dy) || (dy == 0 && decide (0 < dx)) then 1 else -1
        e := e.push (x, eps, eps * dx, eps * dy)
    let cr := fun (p q : Nat × Int × Int × Int) => p.2.2.1 * q.2.2.2 - p.2.2.2 * q.2.2.1
    let es := (e.toList.mergeSort fun p q => !(decide (0 < cr q p))).toArray
    let m := es.size
    for i in [0:m] do
      for k in [i + 2:m] do
        let ei := es[i]!
        let ej := es[i + 1]!
        let ek := es[k]!
        out := out.push (.r2 w a ei.1 ej.1 ek.1 ei.2.1 ej.2.1 ek.2.1 false)
        out := out.push (.r2 w a ei.1 ej.1 ek.1 ei.2.1 ej.2.1 ek.2.1 true)
  return out

/-- AC for new point `n + w` (l2enc.cpp:160-168). -/
def genAC (B : Array Pt) (w : Nat) (out : Array Desc) : Array Desc := Id.run do
  let n := B.size
  let mut out := out
  for a in [0:n] do
    for b in [a + 1:n] do
      for c in [b + 1:n] do
        out := out.push (.ac w a b c)
  return out

/-- Append `d` unless its clause was already emitted in family `fam` (l2enc `addc_d`). -/
def addD (B : Array Pt) (d : Desc) (fam : Nat) (out : Array Desc) (seen : Std.HashSet (List Int × Nat)) :
    Array Desc × Std.HashSet (List Int × Nat) :=
  match clauseOf B d with
  | some cl => if seen.contains (cl, fam) then (out, seen) else (out.push d, seen.insert (cl, fam))
  | none => (out, seen)

/-- RAD (l2enc.cpp:221-227), family code 4. -/
def genRAD (B : Array Pt) (out : Array Desc) (seen : Std.HashSet (List Int × Nat)) :
    Array Desc × Std.HashSet (List Int × Nat) := Id.run do
  let n := B.size
  let mut out := out
  let mut seen := seen
  for a in [0:n] do
    for b in [a + 1:n] do
      let terms := [chi B b n (n + 1), chi B a n (n + 1), chi B a b (n + 1), chi B a b n]
      for sg in forbidSigns terms radPred do
        let r := addD B (.rad a b sg) 4 out seen
        out := r.1
        seen := r.2
  return (out, seen)

/-- One `emit_gp(e, f, g, h, i, fam)` (l2enc.cpp:215-220). -/
def emitGP (B : Array Pt) (e f g h i fam : Nat) (out : Array Desc) (seen : Std.HashSet (List Int × Nat)) :
    Array Desc × Std.HashSet (List Int × Nat) := Id.run do
  let terms := [chi B e f g, chi B e h i, chi B e f h, chi B e g i, chi B e f i, chi B e g h]
  let mut out := out
  let mut seen := seen
  for sg in forbidSigns terms gpPred do
    let r := addD B (.gp e f g h i sg) fam out seen
    out := r.1
    seen := r.2
  return (out, seen)

/-- GPA (code 5), then GPP (6) and GPQ (7) interleaved per triple (l2enc.cpp:228-238). -/
def genGP (B : Array Pt) (out : Array Desc) (seen : Std.HashSet (List Int × Nat)) :
    Array Desc × Std.HashSet (List Int × Nat) := Id.run do
  let n := B.size
  let mut out := out
  let mut seen := seen
  for a in [0:n] do
    for x in [0:n] do
      for y in [x + 1:n] do
        if x != a && y != a then
          let r := emitGP B a x y n (n + 1) 5 out seen
          out := r.1
          seen := r.2
  for x in [0:n] do
    for y in [x + 1:n] do
      for z in [y + 1:n] do
        let r := emitGP B n x y z (n + 1) 6 out seen
        out := r.1
        seen := r.2
        let r := emitGP B (n + 1) x y z n 7 out seen
        out := r.1
        seen := r.2
  return (out, seen)

/-- Mark the six cyclic 4-chains of the ccw hexagon `ch` (l2enc.cpp:87-93); the first hexagon found for a chain
key is kept, rotated so that the chain (a, b, c, d) becomes (q4, q5, q0, q1). -/
def markChains (n : Nat) (ch : Array Nat) (octw : Array (Option (List Nat))) : Array (Option (List Nat)) :=
  Id.run do
  let mut octw := octw
  for i in [0:6] do
    let a := ch[(i + 5) % 6]!
    let b := ch[i]!
    let c := ch[(i + 1) % 6]!
    let d := ch[(i + 2) % 6]!
    let key := ((a * n + b) * n + c) * n + d
    if (octw[key]!).isNone then
      octw := octw.set! key (some ((List.range 6).map fun j => ch[(i + 1 + j) % 6]!))
  return octw

/-- l2enc `dfs` (l2enc.cpp:94-107) with k = 7: counts convex m-gons, marks hexagon chains, lists pentagons. -/
def dfs (B : Array Pt) (n : Nat) (cand : Array Nat) :
    Nat → Array Nat → Nat → Array Nat → Array (Option (List Nat)) → Array (List Nat) →
      Array Nat × Array (Option (List Nat)) × Array (List Nat)
  | 0, _, _, cnt, octw, pents => (cnt, octw, pents)
  | fuel + 1, chain, lastidx, cnt, octw, pents => Id.run do
    let v := chain[0]!
    let w := chain[chain.size - 1]!
    let u := chain[chain.size - 2]!
    let mut cnt := cnt
    let mut octw := octw
    let mut pents := pents
    for t in [lastidx + 1 : cand.size] do
      let x := cand[t]!
      if osgn B u w x ≤ 0 || osgn B w x v ≤ 0 then continue
      let ch := chain.push x
      let m := ch.size
      cnt := cnt.modify m (· + 1)
      if m == 6 then octw := markChains n ch octw
      if m == 5 then pents := pents.push ch.toList
      if m < 7 then
        let r := dfs B n cand fuel ch t cnt octw pents
        cnt := r.1
        octw := r.2.1
        pents := r.2.2
    return (cnt, octw, pents)

/-- l2enc `enumerate_convex` (l2enc.cpp:108-119). -/
def enumConvex (B : Array Pt) : Array Nat × Array (Option (List Nat)) × Array (List Nat) := Id.run do
  let n := B.size
  let mut cnt : Array Nat := Array.replicate 8 0
  let mut octw : Array (Option (List Nat)) := Array.replicate (n * n * n * n) none
  let mut pents : Array (List Nat) := #[]
  for v in [0:n] do
    let pv := B.getD v (0, 0)
    let mut cand : Array Nat := #[]
    for x in [0:n] do
      let px := B.getD x (0, 0)
      if x != v && (decide (px.2 > pv.2) || (px.2 == pv.2 && decide (px.1 > pv.1))) then cand := cand.push x
    let cs := (cand.toList.mergeSort fun p1 p2 => !(decide (0 < osgn B v p2 p1))).toArray
    for t in [0:cs.size] do
      let r := dfs B n cs 7 #[v, cs[t]!] t cnt octw pents
      cnt := r.1
      octw := r.2.1
      pents := r.2.2
  return (cnt, octw, pents)

/-- OCT for new point `n + w` (l2enc.cpp:239-248), in increasing chain-key order. -/
def genOCT (octw : Array (Option (List Nat))) (w : Nat) (out : Array Desc) : Array Desc := Id.run do
  let mut out := out
  for key in [0 : octw.size] do
    match octw[key]! with
    | some q => out := out.push (.oct w q)
    | none => pure ()
  return out

/-- JK (l2enc.cpp:250-284), family code 10. -/
def genJK (B : Array Pt) (pents : Array (List Nat)) (out : Array Desc) (seen : Std.HashSet (List Int × Nat)) :
    Array Desc × Std.HashSet (List Int × Nat) := Id.run do
  let mut out := out
  let mut seen := seen
  for Q in pents do
    for i in [0:5] do
      for j in [0:6] do
        match jkClause B Q i j with
        | some cl =>
          if !(seen.contains (cl, 10)) then
            out := out.push (.jk Q i j)
            seen := seen.insert (cl, 10)
        | none => pure ()
  return (out, seen)

/-- **The descriptors of `l2enc B 7`**, in l2enc's order. -/
def gen (B : Array Pt) : Array Desc := Id.run do
  let mut out : Array Desc := #[]
  let mut seen : Std.HashSet (List Int × Nat) := {}
  out := genR2 B 0 out
  out := genR2 B 1 out
  out := genAC B 0 out
  out := genAC B 1 out
  let r := genRAD B out seen
  out := r.1
  seen := r.2
  let r := genGP B out seen
  out := r.1
  seen := r.2
  let e := enumConvex B
  out := genOCT e.2.1 0 out
  out := genOCT e.2.1 1 out
  let r := genJK B e.2.2 out seen
  out := r.1
  return out

/-- The clause of a descriptor, kept only if every literal is nonzero and `≤ numVars B` in absolute value (always
the case for `clauseOf`'s outputs; the extra test makes the round trip `EncB.parseDimacs_render` immediate). -/
def clauseB (B : Array Pt) (d : Desc) : Option (List Int) :=
  match clauseOf B d with
  | some cl => if bounded (numVars B) cl then some cl else none
  | none => none

/-- **The CNF**: the clauses of the generated descriptors that `clauseOf` accepts. -/
def cnf (B : Array Pt) : List (List Int) := (gen B).toList.filterMap (clauseB B)

end AE33
