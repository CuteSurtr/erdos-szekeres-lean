import C3Encoding.Case

/-! `lake exe c3_dimacs base m k OUT` writes `C3.baseClauses m k` (= `gen_case.py m k none`)
with header `p cnf (numVars m k) (#clauses)`. `lake exe c3_dimacs node m k DIR NAME...` writes,
for each node name, `DIR/NAME.cnf` = the base CNF followed by the units `C3.layerUnits` (the
node CNF of `close_node.py`). Only this string formatting is unverified. -/

open C3

def clauseLine (c : List Int) : String := " ".intercalate (c.map toString ++ ["0"]) ++ "\n"

/-- The clause lines, concatenated in chunks. -/
def body (cls : Array (List Int)) : Array String := Id.run do
  let mut out : Array String := #[]
  let mut cur := ""
  let mut cnt := 0
  for c in cls do
    cur := cur ++ clauseLine c
    cnt := cnt + 1
    if cnt % 65536 == 0 then
      out := out.push cur
      cur := ""
  return out.push cur

def writeCnf (path : String) (nv nc : Nat) (chunks : Array String) (units : List Int) :
    IO Unit := do
  let h ← IO.FS.Handle.mk path IO.FS.Mode.write
  h.putStr s!"p cnf {nv} {nc + units.length}\n"
  for s in chunks do h.putStr s
  h.putStr (String.join (units.map fun u => s!"{u} 0\n"))
  h.flush

def main (args : List String) : IO UInt32 := do
  match args with
  | "base" :: m :: k :: [out] =>
    match m.toNat?, k.toNat? with
    | some m, some k =>
      let cls := baseClauses m k
      writeCnf out (numVars m k) cls.size (body cls) []
      return 0
    | _, _ => IO.eprintln "m k must be natural numbers"; return 1
  | "node" :: m :: k :: dir :: names =>
    match m.toNat?, k.toNat? with
    | some m, some k =>
      let cls := baseClauses m k
      let chunks := body cls
      let nv := numVars m k
      let E := mkTables m
      for nm in names do
        writeCnf s!"{dir}/{nm}.cnf" nv cls.size chunks (layerUnits E (parseLayers nm))
      return 0
    | _, _ => IO.eprintln "m k must be natural numbers"; return 1
  | _ => IO.eprintln "usage: c3_dimacs base m k OUT | c3_dimacs node m k DIR NAME..."; return 1
