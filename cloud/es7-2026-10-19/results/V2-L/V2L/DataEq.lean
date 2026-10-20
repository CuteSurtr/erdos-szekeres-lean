import V2L.Main

/-! `lake exe v2l_data` writes, from the Lean terms of `V2L.Main`, the files that the solver
runs used, so that they can be compared byte for byte (`cmp`, sha256). OUT = `-` is stdout.

* `cases OUT`: `caseCubes` as a cube file (`a l1 … lk 0`), to compare with `cases.icnf`;
* `ups OUT`: `upCubes` as a cube file, to compare with `cover.py`'s `up(U)`;
* `obligation root OUT`: `interiorCnf 33 7 ++ upCubes.map negClause`;
* `obligation up:U OUT` (`U` = `a,b`, `a` or empty): `cubeCnf (interiorCnf 33 7) UP(U) ++
  (casesOf U).map negClause`, the CNF of `RootCertificate` / `UpCertificates`;
* `case I OUT` (`0 ≤ I < 450`): `cubeCnf (interiorCnf 33 7) cube(U, L)` for line `I` of
  `cases.icnf`.

The header is `p cnf nv nc` with `nv` the variable count of `interiorCnf 33 7` (as in H3's
`mir_dimacs`). Unverified string formatting; not part of any proof. -/

open ETV Mir V2L

def withOut (out : String) (k : IO.FS.Handle → IO Unit) : IO Unit := do
  if out == "-" then
    let h ← IO.getStdout
    k h; h.flush
  else
    let h ← IO.FS.Handle.mk out IO.FS.Mode.write
    k h; h.flush

def writeDimacs (out : String) (nv : Nat) (cls : List (List Int)) : IO Unit :=
  withOut out fun h => do
    h.putStrLn s!"p cnf {nv} {cls.length}"
    for c in cls do
      h.putStrLn (" ".intercalate (c.map toString ++ ["0"]))

def writeCubes (out : String) (cubes : List (List Int)) : IO Unit :=
  withOut out fun h => do
    for c in cubes do
      h.putStrLn (" ".intercalate ("a" :: c.map toString ++ ["0"]))

def parseU (s : String) : Option (List Nat) :=
  ((s.splitOn ",").filter (· ≠ "")).mapM String.toNat?

def main (args : List String) : IO UInt32 := do
  let nv := numVars 33 7 7
  match args with
  | ["cases", out] => writeCubes out caseCubes; return 0
  | ["ups", out] => writeCubes out upCubes; return 0
  | ["obligation", "root", out] =>
    writeDimacs out nv (interiorCnf 33 7 ++ upCubes.map negClause); return 0
  | ["obligation", ob, out] =>
    if ob.startsWith "up:" then
      match parseU (ob.drop 3) with
      | some U =>
        match upTable.find? (·.1 == U) with
        | some p =>
          writeDimacs out nv (cubeCnf (interiorCnf 33 7) p.2 ++ (casesOf p.1).map negClause)
          return 0
        | none => IO.eprintln s!"no upper chain {U}"; return 1
      | none => IO.eprintln "bad U"; return 1
    else IO.eprintln "obligation must be root or up:U"; return 1
  | ["case", i, out] =>
    match i.toNat? with
    | some n =>
      match caseCubes[n]? with
      | some c => writeDimacs out nv (cubeCnf (interiorCnf 33 7) c); return 0
      | none => IO.eprintln "index out of range"; return 1
    | none => IO.eprintln "bad index"; return 1
  | _ =>
    IO.eprintln "usage: v2l_data (cases|ups) OUT | obligation (root|up:U) OUT | case I OUT"
    return 2
