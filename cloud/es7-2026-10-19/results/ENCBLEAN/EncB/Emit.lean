import EncB.Gen

/-!
# `lake exe encb_dimacs`

Prints `EncB.gen m K t` in the DIMACS layout of gen_b2.py (gen_b2.py:191-194), and cubes in the layout of
`C6UPPER/tools/mkcubes.py` (mkcubes.py:11-15: the header with the clause count raised by the number of
units, the exact base body, then one line `u 0` per unit).

```
encb_dimacs base  M K T                 base CNF on stdout
encb_dimacs cube  M K T U1 U2 ...       base + unit clauses U1 U2 ... on stdout (mkcubes layout)
encb_dimacs files M K T DIR NAME ...    generate once, write DIR/NAME.cnf for each NAME:
                                          base, full_Y12 (units Y12), cBBBBB (Y12 then the pattern),
                                          nBBBBB (-Y12 then the pattern); the pattern is
                                          Y13 Y14 Y23 Y24 Y34, bit 1 = positive (mkcubes.py:7,16-20)
encb_dimacs stats M K T                 only the summary line
```
The summary line `{"m": .., "K": .., "t": .., "nv": .., "ncl": .., "counts": {...}}` (gen_b2.py:200) goes to
stderr. If gen_b2.py would raise on (M, K, T), nothing is written and the exit code is 1.
Only this file's string formatting and IO lie outside the definition `EncB.gen`.
-/

namespace EncB

/-- Append `' '.join(map(str, cl)) + ' 0\n'` to `s`. -/
def pushClause (s : String) (cl : List Int) : String :=
  match cl with
  | [] => s ++ " 0\n"
  | l :: ls => (ls.foldl (fun acc x => (acc.push ' ') ++ toString x) (s ++ toString l)) ++ " 0\n"

/-- The clause lines: everything after the header line. -/
def body (cls : Array (List Int)) : String := cls.foldl pushClause ""

/-- `'p cnf %d %d\n'`. -/
def header (nv ncl : Nat) : String := s!"p cnf {nv} {ncl}\n"

/-- mkcubes.py:14-15: a newline if the body does not end with one, then `'%d 0\n'` per unit. -/
def cubeTail (bodyStr : String) (units : List Int) : String :=
  (if bodyStr.endsWith "\n" then "" else "\n") ++ String.join (units.map fun u => s!"{u} 0\n")

/-- Units of the named cube; `Yv` is read from the generator's own table. -/
def cubeUnits (r : Result) (t : Nat) (name : String) : Option (List Int) :=
  let y (i j : Nat) : Int := (r.ytab.getD (i * t + j) 0 : Nat)
  let cv := [y 1 3, y 1 4, y 2 3, y 2 4, y 3 4]
  if t < 5 then none
  else if name == "full_Y12" then some [y 1 2]
  else match name.toList with
    | s :: bits =>
      if (s == 'c' || s == 'n') && bits.length == 5 && bits.all (fun ch => ch == '0' || ch == '1') then
        some ((if s == 'c' then y 1 2 else -(y 1 2)) ::
          (cv.zip bits).map fun vb => if vb.2 == '1' then vb.1 else -vb.1)
      else none
    | [] => none

/-- The summary line of gen_b2.py:200. -/
def summary (m K t : Nat) (r : Result) : String :=
  "{\"m\": " ++ toString m ++ ", \"K\": " ++ toString K ++ ", \"t\": " ++ toString t ++
  ", \"nv\": " ++ toString r.nv ++ ", \"ncl\": " ++ toString r.clauses.size ++
  ", \"counts\": {\"unit\": " ++ toString r.nunit ++ ", \"cond\": " ++ toString r.ncond ++
  ", \"chain\": " ++ toString r.nchain ++ "}}"

end EncB

open EncB

def usage : String :=
  "usage: encb_dimacs base M K T | cube M K T U... | files M K T DIR NAME... | stats M K T"

/-- Run the generator; refuse where gen_b2.py raises. -/
def genChecked (m K t : Nat) : IO (Option Result) := do
  let r := gen m K t
  if r.bad != 0 || r.conflict then
    IO.eprintln s!"encb_dimacs: gen_b2.py raises on ({m},{K},{t}) (bad = {r.bad}, conflict = {r.conflict}); nothing written"
    return none
  IO.eprintln (summary m K t r)
  return some r

def parseMKT (ms ks ts : String) : Option (Nat × Nat × Nat) := do
  return (← ms.toNat?, ← ks.toNat?, ← ts.toNat?)

def main (args : List String) : IO UInt32 := do
  match args with
  | mode :: ms :: ks :: ts :: rest =>
    let some (m, K, t) := parseMKT ms ks ts | IO.eprintln usage; return 2
    if mode == "base" && rest.isEmpty then
      let some r ← genChecked m K t | return 1
      let out ← IO.getStdout
      out.putStr (header r.nv r.clauses.size)
      out.putStr (body r.clauses)
      out.flush
      return 0
    else if mode == "cube" then
      let some units := rest.mapM String.toInt? | IO.eprintln usage; return 2
      let some r ← genChecked m K t | return 1
      let b := body r.clauses
      let out ← IO.getStdout
      out.putStr (header r.nv (r.clauses.size + units.length))
      out.putStr b
      out.putStr (cubeTail b units)
      out.flush
      return 0
    else if mode == "files" then
      match rest with
      | dir :: names =>
        -- check every name before generating (`cubeUnits` only needs the Y table for the numbers)
        let probe : Result := { nv := 0, clauses := #[], ytab := #[], nunit := 0, ncond := 0, nchain := 0,
                                bad := 0, conflict := false }
        for n in names do
          if n != "base" && (cubeUnits probe t n).isNone then
            IO.eprintln s!"encb_dimacs: unknown cube name {n} (or T < 5)"; return 2
        let some r ← genChecked m K t | return 1
        let b := body r.clauses
        for n in names do
          let path := dir ++ "/" ++ n ++ ".cnf"
          if n == "base" then
            IO.FS.withFile path .write fun h => do
              h.putStr (header r.nv r.clauses.size); h.putStr b
          else
            let units := (cubeUnits r t n).getD []
            IO.FS.withFile path .write fun h => do
              h.putStr (header r.nv (r.clauses.size + units.length)); h.putStr b
              h.putStr (cubeTail b units)
          IO.eprintln s!"wrote {path}"
        return 0
      | [] => IO.eprintln usage; return 2
    else if mode == "stats" && rest.isEmpty then
      let some _ ← genChecked m K t | return 1
      return 0
    else
      IO.eprintln usage; return 2
  | _ => IO.eprintln usage; return 2
