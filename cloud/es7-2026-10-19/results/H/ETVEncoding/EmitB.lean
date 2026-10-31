import ETVEncoding.ClausesB

/-! `lake exe trackb_dimacs N K OUT [--hull] [--mirror] [--flip] [--no-mono]` writes
`ETV.dimacsB` in the layout of `tools/trackB/gen_cnf.py N K [options] -o OUT`, including its
two comment lines. -/

open ETV

def pyBool (b : Bool) : String := if b then "True" else "False"

def main (args : List String) : IO UInt32 := do
  let flags := args.filter (·.startsWith "--")
  let pos := args.filter (fun a => !a.startsWith "--")
  let hull := flags.contains "--hull"
  let mirror := flags.contains "--mirror"
  let flip := flags.contains "--flip"
  let mono := !flags.contains "--no-mono"
  match pos with
  | [n, k, out] =>
    match n.toNat?, k.toNat? with
    | some N, some K =>
      let cls := dimacsB N K hull mirror flip mono
      let h ← IO.FS.Handle.mk out IO.FS.Mode.write
      h.putStrLn s!"c ES signotope CNF N={N} K={K} hull={pyBool hull} mirror={pyBool mirror} flip={pyBool flip} mono={pyBool mono}"
      h.putStrLn s!"c X(i,j,k) for i<j<k are variables 1..{(triples N).length} in lexicographic order"
      h.putStrLn s!"p cnf {numVars N K K} {cls.length}"
      for c in cls do
        h.putStrLn (" ".intercalate (c.map toString ++ ["0"]))
      h.flush
      return 0
    | _, _ => IO.eprintln "N K must be natural numbers"; return 1
  | _ => IO.eprintln "usage: trackb_dimacs N K OUT [--hull] [--mirror] [--flip] [--no-mono]"
         return 1
