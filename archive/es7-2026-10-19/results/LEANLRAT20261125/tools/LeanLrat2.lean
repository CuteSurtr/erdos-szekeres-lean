import Std.Tactic.BVDecide.LRAT.Checker
import Std.Tactic.BVDecide.LRAT.Parser
import Std.Sat.CNF.Dimacs

/-!
# A second LRAT checker, variant 2 (header may declare unused variables): Lean core's verified `LRAT.check`

`LRAT.check proof cnf = true → cnf.Unsat` is `Std.Tactic.BVDecide.LRAT.check_sound` (proved in Lean core). This program
runs that checker natively (`lean --run`), so its trust is the Lean compiler and runtime plus core's proof, not the
kernel. The DIMACS parser below is NOT verified; it is validated per file by a byte round trip: core's own printer
`Std.Sat.CNF.dimacs` applied to the parsed `CNF Nat` must reproduce the input text exactly (DIMACS variable `i` is
`CNF Nat` variable `i - 1`, as in core's printer, which adds 1). The program prints `s VERIFIED UNSAT (...)` only when
the round trip is exact, the clause count equals the header and `check` returns `true`.

usage: lean --run LeanLrat.lean CNF LRAT
-/

open Std.Sat Std.Tactic.BVDecide

/-- DIMACS text to (declared variables, declared clauses, clauses); comment lines (`c ...`) and empty lines skipped. -/
def parseDimacs (s : String) : Except String (Nat × Nat × CNF Nat) := Id.run do
  let mut nv := 0
  let mut nc := 0
  let mut seenP := false
  let mut clauses : Array (CNF.Clause Nat) := #[]
  let mut cur : Array (Literal Nat) := #[]
  for line in s.splitOn "\n" do
    if line.isEmpty || line.startsWith "c" then continue
    if line.startsWith "p" then
      match (line.splitOn " ").filter (· ≠ "") with
      | ["p", "cnf", a, b] =>
        match a.toNat?, b.toNat? with
        | some a, some b => nv := a; nc := b; seenP := true
        | _, _ => return .error "bad p line"
      | _ => return .error "bad p line"
      continue
    for tok in (line.splitOn " ").filter (· ≠ "") do
      match tok.toInt? with
      | none => return .error s!"bad token {tok}"
      | some i =>
        if i == 0 then
          clauses := clauses.push cur.toList
          cur := #[]
        else
          cur := cur.push (i.natAbs - 1, decide (0 < i))
  if !cur.isEmpty then return .error "last clause not terminated by 0"
  if !seenP then return .error "no p line"
  return .ok (nv, nc, clauses.toList)

def main (args : List String) : IO UInt32 := do
  match args with
  | [cnfPath, lratPath] =>
    let text ← IO.FS.readFile cnfPath
    match parseDimacs text with
    | .error e => IO.eprintln s!"parse error: {e}"; return 2
    | .ok (nv, nc, cnf) =>
      -- variant 2: the clause lines must equal core's printer output byte for byte; the header must be exactly
      -- `p cnf NV NC` with NC the clause count and NV at least the largest variable used (core's printer writes the
      -- largest variable; a trimmed formula may declare more). Unsatisfiability does not depend on unused variables.
      let rt := CNF.dimacs cnf
      let body (s : String) : String := let p := s.posOf '\n'; s.extract (s.next p) s.endPos
      let maxVar := cnf.foldl (fun m c => c.foldl (fun m l => max m (l.1 + 1)) m) 0
      let head := text.extract 0 (text.posOf '\n')
      let roundTrip := body rt == body text && head == s!"p cnf {nv} {nc}" && maxVar ≤ nv
      IO.println s!"c parsed: header p cnf {nv} {nc}; clauses {cnf.length}; largest variable {maxVar}; clause lines equal core's printer and header canonical: {roundTrip}"
      if !roundTrip then IO.println "s NOT CHECKED (round trip differs)"; return 3
      if cnf.length != nc then IO.println "s NOT CHECKED (clause count differs from header)"; return 3
      let proof ← LRAT.loadLRATProof lratPath
      IO.println s!"c proof actions: {proof.size}"
      if LRAT.check proof cnf then
        IO.println "s VERIFIED UNSAT (Std.Tactic.BVDecide.LRAT.check; sound by LRAT.check_sound)"
        return 0
      else
        IO.println "s NOT VERIFIED"
        return 1
  | _ => IO.eprintln "usage: lean --run LeanLrat.lean CNF LRAT"; return 2
