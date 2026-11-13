-- Writes (treeOf s).leaves of every case as a cube file DIR/<U>_<L>.icnf (run: lake env lean --run scripts/dump_tree_leaves.lean DIR).
import V2L.Trees.Table
import V2L.Facts
open V2L
def line (l : List Int) : String := "a " ++ String.join (l.map fun z => toString z ++ " ") ++ "0\n"
def main (args : List String) : IO Unit := do
  let dir := args.head!
  for (s, _) in caseTable do
    let t := treeOf s
    IO.FS.writeFile s!"{dir}/{s.1}_{s.2}.icnf" (String.join (t.leaves.map line))
