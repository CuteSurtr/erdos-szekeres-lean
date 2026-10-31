import MirrorEncoding.Gen

/-! `lake exe mir_dimacs hull N K OUT` writes `Mir.hullCnf N K` (the layout of
`mirgen.py ... --hull`), and `lake exe mir_dimacs interior N K OUT` writes
`Mir.interiorCnf N K` (`mirgen.py ... --interior --yflip-unit`). The header is
`p cnf nv nc` with `nv` the variable count of `gen_etv.py N K K K`. Only this string
formatting is unverified. -/

open ETV Mir

def writeDimacs (out : String) (nv : Nat) (cls : List (List Int)) : IO Unit := do
  let h ← IO.FS.Handle.mk out IO.FS.Mode.write
  h.putStrLn s!"p cnf {nv} {cls.length}"
  for c in cls do
    h.putStrLn (" ".intercalate (c.map toString ++ ["0"]))
  h.flush

def main (args : List String) : IO UInt32 := do
  match args with
  | [mode, n, k, out] =>
    match n.toNat?, k.toNat? with
    | some N, some K =>
      if mode == "hull" then
        writeDimacs out (numVars N K K) (hullCnf N K); return 0
      else if mode == "interior" then
        writeDimacs out (numVars N K K) (interiorCnf N K); return 0
      else IO.eprintln "mode must be hull or interior"; return 1
    | _, _ => IO.eprintln "N K must be natural numbers"; return 1
  | _ => IO.eprintln "usage: mir_dimacs (hull|interior) N K OUT"; return 1
