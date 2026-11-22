import EncB.Render
import N66Enc.Print

/-!
# n66print: the printer exe (modes)

* `stats` — sizes of the Lean lists (eager stream, allocation, counter, SB, leaves, R0).
* `eager` — the DIMACS lines of `eagerStream` (no header), for comparison with the pinned Python generator.
* `leaves` — the 132 leaf cubes, one per line: `index s:b …` (b = 1 occupied, 0 hole).
* `trim I DESC` — **the certificate text of leaf I**: `EncB.render nvHeader L` with
  `L = printClauses leaves132[I] (parseDescs DESC)`; refuses (exit 1, nothing on stdout) if a descriptor is invalid
  or a literal is 0 or above `nvHeader`.
* `full I ACT ROWS` — control only (not on the trust path): streams the complete `cert.cnf` of leaf I in
  p2_write.py's layout from an activated-quadruple file (`a b c d` per line) and a row file (one support per line).
-/

open N66Enc

def flushAt : Nat := 1 <<< 20

/-- Stream clause lines through a buffer. -/
def streamClauses (out : IO.FS.Stream) (buf : String) (cls : List (List Int)) : IO String := do
  let mut b := buf
  for cl in cls do
    b := EncB.pushClauseR b cl
    if b.utf8ByteSize ≥ flushAt then
      out.putStr b
      b := ""
  return b

def readLines (path : String) : IO (List String) := do
  let s ← IO.FS.readFile path
  return (s.splitOn "\n").filter (· ≠ "")

def cubeName (c : Cube) : String :=
  " ".intercalate (c.map fun z => s!"{z.1.val}:{if z.2 then 1 else 0}")

def main (args : List String) : IO UInt32 := do
  let out ← IO.getStdout
  let err ← IO.getStderr
  match args with
  | ["stats"] =>
    out.putStrLn s!"eager {eagerArr.size}"
    out.putStrLn s!"pairClauses {(pairClauses ()).length} posClauses {(posClauses ()).length} thresh {(threshClauses ()).length} triple {(tripleClauses ()).length} ceue {(ceueClauses ()).length}"
    out.putStrLn s!"alloc {nAlloc} pair {(pairAtoms ()).length} orient {(orientAtoms ()).length} convex {(convexAtoms ()).length} chain {(chainAtoms ()).length} ceue {(ceueAtoms ()).length} cnt {cntAtoms.length} sbe {sbeAtoms.length}"
    out.putStrLn s!"card {cardClauses.length} sb {sbClauses.length} leaves {leaves132.length} R0 {R0.length}"
    out.putStrLn s!"num sel0 {num (.sel 0)} sel69 {num (.sel 69)} firstcnt {(cntAtoms.head?.map num)} lastsbe {num (sbeAt 25)}"
    return 0
  | ["eager"] =>
    let rest ← streamClauses out "" eagerArr.toList
    out.putStr rest
    return 0
  | ["leaves"] =>
    let mut i := 0
    for c in leaves132 do
      out.putStrLn s!"{i} {cubeName c}"
      i := i + 1
    return 0
  | ["trim", idx, descPath] =>
    let some i := idx.toNat? | err.putStrLn "bad index"; return 1
    let some c := leaves132[i]? | err.putStrLn "no such leaf"; return 1
    let txt ← IO.FS.readFile descPath
    let some ds := parseDescs txt | err.putStrLn "bad descriptor file"; return 1
    let some L := printClauses c ds | err.putStrLn "invalid descriptor"; return 1
    if !litsBounded nvHeader L then
      err.putStrLn "literal out of range"
      return 1
    out.putStr (EncB.render nvHeader L)
    err.putStrLn s!"leaf {i} [{cubeName c}] clauses {L.length}"
    return 0
  | ["full", idx, actPath, rowsPath] =>
    let some i := idx.toNat? | err.putStrLn "bad index"; return 1
    let some c := leaves132[i]? | err.putStrLn "no such leaf"; return 1
    let actL ← readLines actPath
    let rows := parseRows (← IO.FS.readFile rowsPath)
    let units := fixedUnits ++ c.map cubeUnit
    let nc := eagerArr.size + 12 * actL.length + units.length + rows.length + cardClauses.length +
      sbClauses.length
    out.putStr (EncB.headerR nvHeader nc)
    let mut b := ""
    b ← streamClauses out b eagerArr.toList
    let mut bad := 0
    for l in actL do
      match ((l.splitOn " ").filter (· ≠ "")).mapM String.toNat? with
      | some [a, b', c', d] =>
        match toFin70 a, toFin70 b', toFin70 c', toFin70 d with
        | some a, some b', some c', some d => b ← streamClauses out b ((quadClauses a b' c' d).map toDimacs)
        | _, _, _, _ => bad := bad + 1
      | _ => bad := bad + 1
    b ← streamClauses out b (units.map toDimacs)
    b ← streamClauses out b ((rows.map rowClause).map toDimacs)
    b ← streamClauses out b (cardClauses.map toDimacs)
    b ← streamClauses out b (sbClauses.map toDimacs)
    out.putStr b
    err.putStrLn s!"leaf {i} clauses {nc} act {actL.length} rows {rows.length} bad {bad}"
    return (if bad = 0 then 0 else 1)
  | _ =>
    err.putStrLn "usage: n66print stats | eager | leaves | trim I DESC | full I ACT ROWS"
    return 2
