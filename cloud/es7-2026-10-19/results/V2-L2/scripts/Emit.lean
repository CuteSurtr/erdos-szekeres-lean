import V2L2.Defs
import V2L.Trees.Table
import V2L.Facts

/-! Run with `lake env lean --run scripts/Emit.lean ARGS` (interpreted; not part of any proof).

* `count`: the number of tree leaves `l ∈ (treeOf p.1).leaves`, `p ∈ caseTable`, in all, and of
  those containing the negation of a case-cube literal (`∃ x ∈ l, -x ∈ p.2`).
* `emit REQ OUTDIR`: for each line `I CASE SHA LITS ...` of REQ (tab-separated, `LITS`
  comma-separated), checks that `LITS` is a leaf of `treeOf (caseTable[I]).1`, then writes
  `v3LeafCnf (interiorCnf 33 7) (caseTable[I]).2 LITS` as DIMACS text to `OUTDIR/I.cnf`,
  with the header `p cnf nv nc` (`nv` = `numVars 33 7 7`) and the clause formatting of
  `mir_dimacs` (H3). -/

open ETV Mir V2L V2L2

def writeDimacs (out : String) (nv : Nat) (cls : List (List Int)) : IO Unit := do
  let h ← IO.FS.Handle.mk out IO.FS.Mode.write
  h.putStrLn s!"p cnf {nv} {cls.length}"
  for c in cls do
    h.putStrLn (" ".intercalate (c.map toString ++ ["0"]))
  h.flush

def parseInt (s : String) : Option Int :=
  if s.startsWith "-" then (s.drop 1).toNat?.map fun n => -(n : Int) else s.toNat?.map Int.ofNat

def main (args : List String) : IO UInt32 := do
  match args with
  | ["count"] =>
    let mut total := 0
    let mut contra := 0
    let mut cases := 0
    for p in caseTable do
      let ls := (treeOf p.1).leaves
      total := total + ls.length
      let k := (ls.filter fun l => l.any fun x => p.2.contains (-x)).length
      contra := contra + k
      if k > 0 then cases := cases + 1
    IO.println s!"cases {caseTable.length} tree_leaves {total} contradicting_case_cube {contra} in_cases {cases} needing_hypothesis {total - contra}"
    return 0
  | ["emit", req, outDir] =>
    let F := interiorCnf 33 7
    let nv := numVars 33 7 7
    let mut bad := 0
    for line in (← IO.FS.lines req) do
      match line.splitOn "\t" with
      | i :: name :: sha :: lits :: _ =>
        match i.toNat?, (lits.splitOn ",").mapM parseInt with
        | some n, some l =>
          match caseTable[n]? with
          | some p =>
            let isLeaf := (treeOf p.1).leaves.contains l
            if !isLeaf then bad := bad + 1
            writeDimacs s!"{outDir}/{n}.cnf" nv (v3LeafCnf F p.2 l)
            IO.println s!"{n}\t{name}\t{sha}\tleaf_of_tree={isLeaf}"
          | none => IO.eprintln s!"case index {n} out of range"; bad := bad + 1
        | _, _ => IO.eprintln s!"bad line {line}"; bad := bad + 1
      | _ => IO.eprintln s!"bad line {line}"; bad := bad + 1
    return (if bad == 0 then 0 else 1)
  | _ => IO.eprintln "usage: count | emit REQ OUTDIR"; return 2
