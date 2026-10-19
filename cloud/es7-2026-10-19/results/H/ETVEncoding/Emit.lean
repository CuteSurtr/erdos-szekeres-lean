import ETVEncoding.Clauses

/-! `lake exe etv_dimacs N A U K OUT [--xsb]` writes `ETV.dimacs N A U K` (or
`ETV.dimacsXsb N A U K`) in DIMACS format, in the same layout as
`gen_etv.py N A U K [--xsb] -o OUT` (header `p cnf nv nc`, one clause per line). -/

open ETV

def writeDimacs (out : String) (nv : Nat) (cls : List (List Int)) : IO Unit := do
  let h ← IO.FS.Handle.mk out IO.FS.Mode.write
  h.putStrLn s!"p cnf {nv} {cls.length}"
  for c in cls do
    h.putStrLn (" ".intercalate (c.map toString ++ ["0"]))
  h.flush

def main (args : List String) : IO UInt32 := do
  let (args, xsb) := if args.getLast? == some "--xsb" then (args.dropLast, true)
    else (args, false)
  match args with
  | [n, a, u, k, out] =>
    match n.toNat?, a.toNat?, u.toNat?, k.toNat? with
    | some N, some A, some U, some K =>
      writeDimacs out (numVars N A U) (if xsb then dimacsXsb N A U K else dimacs N A U K)
      return 0
    | _, _, _, _ => IO.eprintln "N A U K must be natural numbers"; return 1
  | _ => IO.eprintln "usage: etv_dimacs N A U K OUT [--xsb]"; return 1
