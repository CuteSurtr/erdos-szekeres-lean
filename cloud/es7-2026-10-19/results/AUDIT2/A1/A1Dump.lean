import V2L
-- AUDIT2 A1: dump the Lean data as the interpreter evaluates it, for comparison with my
-- Python decoding of the source files. Run: lake env lean --run A1Dump.lean OUT
open V2L
def cube (l : List Int) : String := " ".intercalate (l.map toString)
def main (args : List String) : IO Unit := do
  let h ← IO.FS.Handle.mk args.head! IO.FS.Mode.write
  for (s, c) in caseTable do
    h.putStrLn s!"C {s.1} {s.2} : {cube c}"
    for l in (treeOf s).leaves do
      h.putStrLn s!"L {cube l}"
  for (u, c) in upTable do
    h.putStrLn s!"U {u} : {cube c}"
  for c in V1L.hullLeaves do
    h.putStrLn s!"H {cube c}"
  h.flush
