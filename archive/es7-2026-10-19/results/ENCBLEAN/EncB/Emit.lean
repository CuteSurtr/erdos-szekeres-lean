import EncB.Gen
import EncB.Coded
import EncB.Cover
import EncB.Render

/-!
# `lake exe encb_dimacs`

Prints `EncB.gen m K t` (M1's port) or `EncB.encB m K t` (M2's functional twin, the object of the theorems) in the
DIMACS layout of gen_b2.py (gen_b2.py:191-194), and cubes in the layout of `C6UPPER/tools/mkcubes.py`
(mkcubes.py:11-15: the header with the clause count raised by the number of units, the exact base body, then one
line `u 0` per unit).

```
encb_dimacs base  M K T                 gen: base CNF on stdout
encb_dimacs cube  M K T U1 U2 ...       gen: base + unit clauses U1 U2 ... on stdout (mkcubes layout)
encb_dimacs files M K T DIR NAME ...    gen: generate once, write DIR/NAME.cnf for each NAME:
                                          base, full_Y12 (units Y12), cBBBBB (Y12 then the pattern),
                                          nBBBBB (-Y12 then the pattern); the pattern is
                                          Y13 Y14 Y23 Y24 Y34, bit 1 = positive (mkcubes.py:7,16-20)
encb_dimacs stats M K T                 gen: only the summary line
encb_dimacs twin-base  M K T            encB: `encB M K T` on stdout, header `numVars`, `length`
encb_dimacs twin-cube  M K T U1 ...     encB: `cubeCnf (encB M K T) [U1, ...]` on stdout
encb_dimacs twin-stats M K T            encB: only the summary line
encb_dimacs twin-check M K T            encB = gen as Lean values (clauses, nv, refusal), compiled, no printing
encb_dimacs twin-ymap  M K T            encB: DIMACS numbers of Y(i,j), i < j < min(T, 5), both directions
encb_dimacs twin-profile M K T          encB: time the phases of `encode` (and `diagCoded`, `bodyR`) separately
encb_dimacs twin-cubes64 M K T DIR [NAME ...]
                                        encB: check that `cubeVars64` numbers Y12 Y13 Y14 Y23 Y24 Y34 (true iff
                                          T = 11), write DIR/base.cnf and DIR/NAME.cnf for the cubes of the Lean
                                          list `cubes64` (in its order; all 64 if no NAME is given), each file
                                          = `renderCube` of `cubeCnf (encB M K T) c` (Render.lean); the trust
                                          path is M K T = 6 8 11
encb_dimacs twin-cube64 M K T I         encB: `cubeCnf (encB M K T) (cubes64.get I)` on stdout, 0 ≤ I < 64, the
                                          I-th cube of the Lean list `cubes64` itself (not a name lookup); writes
                                          no file; stderr gets the cube's name (`cubeName`, as in twin-cubes64)
                                          and its units (M9 hash binding: `scripts/hash_binding.sh`)
```
Every twin mode that prints a CNF (`twin-base`, `twin-cube`, `twin-cubes64`, `twin-cube64`) prints the one string
`renderCube nv F bodyF cube` of `EncB/Render.lean` with a single `putStr`; `twin-base`, `twin-cube` and
`twin-cube64` print `cnfText e cube` (`= renderCube e.nv e.clauses (bodyR e.clauses) cube`) for `e = encode M K T`,
the base being `cube = []`. `Render.lean` proves that this text parses back to `(numVars M K T, cubeCnf (encB M K T)
cube)` under the reference parser `parseDimacs` (`parseDimacs_cnfText`; for (6,8,11) `parseDimacs_cube64_get` and
`parseDimacs_base6811`). The twin printer uses Render's own decimal printer (`pushNat`/`pushInt`), not core's
`toString`. The gen modes (`base`, `cube`, `files`) keep M1's printer `pushClause`/`body`/`header`/`cubeTail` below,
unchanged.
The summary line `{"m": .., "K": .., "t": .., "nv": .., "ncl": .., ...}` (gen_b2.py:200) goes to stderr. If
gen_b2.py would raise on (M, K, T), nothing is written and the exit code is 1 (for the twin modes the refusal uses
`diagCoded`).
Outside the definitions `EncB.gen` / `EncB.encB` and the proved renderer, only this file's IO (and, for the gen
modes, M1's printer) remains.
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

/-- The file name of a cube: `c` (first unit positive) or `n`, then one bit per further unit (1 = positive),
as mkcubes.py:19 and noty12.py:80 name them. -/
def cubeName (cube : List Int) : String :=
  match cube with
  | [] => "empty"
  | u :: us => (if u > 0 then "c" else "n") ++ String.mk (us.map fun z => if z > 0 then '1' else '0')

/-- The summary line of gen_b2.py:200. -/
def summary (m K t : Nat) (r : Result) : String :=
  "{\"m\": " ++ toString m ++ ", \"K\": " ++ toString K ++ ", \"t\": " ++ toString t ++
  ", \"nv\": " ++ toString r.nv ++ ", \"ncl\": " ++ toString r.clauses.size ++
  ", \"counts\": {\"unit\": " ++ toString r.nunit ++ ", \"cond\": " ++ toString r.ncond ++
  ", \"chain\": " ++ toString r.nchain ++ "}}"

end EncB

open EncB

def usage : String :=
  "usage: encb_dimacs base M K T | cube M K T U... | files M K T DIR NAME... | stats M K T\n" ++
  "       encb_dimacs twin-base M K T | twin-cube M K T U... | twin-stats M K T | twin-check M K T\n" ++
  "       encb_dimacs twin-ymap M K T | twin-profile M K T | twin-cubes64 M K T DIR [NAME...]\n" ++
  "       encb_dimacs twin-cube64 M K T I   (0 <= I < 64)"

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

/-- The twin's summary line (no per-family counts). -/
def twinSummary (m K t : Nat) (e : Enc) : String :=
  "{\"m\": " ++ toString m ++ ", \"K\": " ++ toString K ++ ", \"t\": " ++ toString t ++
  ", \"nv\": " ++ toString e.nv ++ ", \"ncl\": " ++ toString e.clauses.length ++ ", \"encoder\": \"encB\"" ++
  ", \"codesDecode\": " ++ toString (codesDecode m K t e.codes) ++ "}"

/-- Run the twin; refuse where gen_b2.py raises (by `diagCoded`). -/
def encodeChecked (m K t : Nat) : IO (Option Enc) := do
  let (bad, conflict) := diagCoded m K t
  if bad != 0 || conflict then
    IO.eprintln s!"encb_dimacs: gen_b2.py raises on ({m},{K},{t}) (twin: bad = {bad}, conflict = {conflict}); nothing written"
    return none
  let e := encode m K t
  IO.eprintln (twinSummary m K t e)
  return some e

/-- The DIMACS number of `Y(i,j)` in the twin's numbering, and the variable that number decodes to. -/
def yNumbers (m K t : Nat) (e : Enc) (ij : Nat × Nat) : Nat × Var :=
  let n := e.nmap.getD (yCode t ij.1 ij.2) 0
  (n, decodeCode m K t (decode e.codes n))

def twinMain (mode : String) (args : List String) : IO UInt32 := do
  match mode, args with
  | "twin-cubes64", ms :: ks :: ts :: dir :: names =>
    let some (m, K, t) := parseMKT ms ks ts | IO.eprintln usage; return 2
    -- the cubes of the Lean list `cubes64`, in its order, optionally restricted to the given names
    let all := cubes64.map fun c => (cubeName c, c)
    for n in names do
      if !(all.any (·.1 == n)) then IO.eprintln s!"encb_dimacs: {n} is not the name of a cube of cubes64"; return 2
    let sel := if names.isEmpty then all else all.filter fun nc => names.contains nc.1
    let some e ← encodeChecked m K t | return 1
    -- the variables of the cubes are Y12 Y13 Y14 Y23 Y24 Y34 in this numbering (both directions)
    let ys : List (Nat × Nat) := [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
    let fwd := ys.map fun ij => ((yNumbers m K t e ij).1 : Int)
    let bwd := cubeVars64.map fun v => decodeCode m K t (decode e.codes v.natAbs)
    let want := ys.map fun ij => Var.y ij.1 ij.2
    let varsOk := cubes64.all fun c => c.map Int.natAbs == cubeVars64.map Int.natAbs
    IO.eprintln s!"cubeVars64 = {cubeVars64}; numbers of Y12 Y13 Y14 Y23 Y24 Y34 = {fwd}; decode(cubeVars64) = {repr bwd}; every cube of cubes64 on cubeVars64: {varsOk}; {cubes64.length} cubes"
    if fwd != cubeVars64 || bwd != want || !varsOk then
      IO.eprintln "encb_dimacs: the cube variables are not Y12 Y13 Y14 Y23 Y24 Y34; nothing written"; return 1
    -- the base lines are rendered once and shared; each file is `renderCube e.nv e.clauses (bodyR e.clauses) c`
    -- (= `cnfText e c`, and = `render e.nv (cubeCnf e.clauses c)` by `renderCube_eq`)
    let bodyF := bodyR e.clauses
    IO.FS.withFile (dir ++ "/base.cnf") .write fun h => h.putStr (renderCube e.nv e.clauses bodyF [])
    IO.eprintln s!"wrote {dir}/base.cnf"
    for (n, c) in sel do
      let path := dir ++ "/" ++ n ++ ".cnf"
      IO.FS.withFile path .write fun h => h.putStr (renderCube e.nv e.clauses bodyF c)
      IO.eprintln s!"wrote {path} units {c}"
    return 0
  | "twin-cube64", [ms, ks, ts, istr] =>
    let some (m, K, t) := parseMKT ms ks ts | IO.eprintln usage; return 2
    let some i := istr.toNat? | IO.eprintln usage; return 2
    -- the `i`-th entry of the Lean list `cubes64` itself (the theorem's definition), not a name lookup
    if h : i < cubes64.length then
      let c := cubes64.get ⟨i, h⟩
      let some e ← encodeChecked m K t | return 1
      IO.eprintln s!"cubes64[{i}] name {cubeName c} units {c}"
      let out ← IO.getStdout
      -- `e = encode m K t` (`encodeChecked`); the text is the one of `parseDimacs_cube64_get` for (6,8,11)
      out.putStr (cnfText e c)
      out.flush
      return 0
    else
      IO.eprintln s!"encb_dimacs: index {i} out of range (cubes64 has {cubes64.length} cubes)"; return 2
  | _, ms :: ks :: ts :: rest =>
    let some (m, K, t) := parseMKT ms ks ts | IO.eprintln usage; return 2
    if mode == "twin-base" && rest.isEmpty then
      let some e ← encodeChecked m K t | return 1
      let out ← IO.getStdout
      -- the base is the empty cube (`parseDimacs_base6811` for (6,8,11))
      out.putStr (cnfText e [])
      out.flush
      return 0
    else if mode == "twin-cube" then
      let some units := rest.mapM String.toInt? | IO.eprintln usage; return 2
      let some e ← encodeChecked m K t | return 1
      let out ← IO.getStdout
      out.putStr (cnfText e units)
      out.flush
      return 0
    else if mode == "twin-stats" && rest.isEmpty then
      let some _ ← encodeChecked m K t | return 1
      return 0
    else if mode == "twin-ymap" && rest.isEmpty then
      let some e ← encodeChecked m K t | return 1
      for i in rng 1 (min t 5) do
        for j in rng (i + 1) (min t 5) do
          let (n, v) := yNumbers m K t e (i, j)
          IO.println s!"Y({i},{j}) number {n} decodes to {repr v}"
      return 0
    else if mode == "twin-profile" && rest.isEmpty then
      -- the phases of `encode`, timed separately (the same functions, called one by one; output = summary only)
      let t0 ← IO.monoMsNow
      let d := diagCoded m K t
      IO.eprintln s!"diagCoded: bad {d.1}, conflict {d.2}"
      let t1 ← IO.monoMsNow
      let cls := genCoded m K t
      IO.eprintln s!"genCoded: {cls.length} clauses"
      let t2 ← IO.monoMsNow
      let codes := allCodesOf m K t cls
      IO.eprintln s!"allCodesOf: {codes.length} codes"
      let t3 ← IO.monoMsNow
      let nm := numberMap codes
      IO.eprintln s!"numberMap: size {nm.size}"
      let t4 ← IO.monoMsNow
      let out := cls.map (fun cl => cl.map (renumberLit nm))
      IO.eprintln s!"renumber: {out.length} clauses"
      let t5 ← IO.monoMsNow
      let b := bodyR out
      IO.eprintln s!"bodyR: {b.utf8ByteSize} bytes"
      let t6 ← IO.monoMsNow
      IO.println s!"({m},{K},{t}) profile ms: diagCoded {t1 - t0}, genCoded {t2 - t1}, allCodesOf {t3 - t2}, numberMap {t4 - t3}, renumber {t5 - t4}, bodyR {t6 - t5}"
      return 0
    else if mode == "twin-check" && rest.isEmpty then
      -- encB = gen as Lean values: the same refusal, the same nv, the same clause list
      let (bad, conflict) := diagCoded m K t
      let twinRefuses := bad != 0 || conflict
      let t0 ← IO.monoMsNow
      let r := gen m K t
      let genRefuses := r.bad != 0 || r.conflict
      IO.eprintln s!"gen: nv {r.nv}, ncl {r.clauses.size}"
      let t1 ← IO.monoMsNow
      if twinRefuses || genRefuses then
        if twinRefuses == genRefuses then
          IO.println s!"({m},{K},{t}) BOTH-REFUSE twin(bad={bad},conflict={conflict}) gen(bad={r.bad},conflict={r.conflict})"; return 0
        else
          IO.println s!"({m},{K},{t}) REFUSAL-DIFFERS twin(bad={bad},conflict={conflict}) gen(bad={r.bad},conflict={r.conflict})"; return 1
      let e := encode m K t
      IO.eprintln s!"encB: nv {e.nv}, ncl {e.clauses.length}"
      let t2 ← IO.monoMsNow
      let sameNv := e.nv == r.nv
      let sameCls := e.clauses == r.clauses.toList
      if sameNv && sameCls then
        IO.println s!"({m},{K},{t}) EQUAL nv={e.nv} ncl={e.clauses.length} gen_ms={t1 - t0} encB_ms={t2 - t1}"; return 0
      else
        IO.println s!"({m},{K},{t}) DIFFERENT nv twin={e.nv} gen={r.nv} ncl twin={e.clauses.length} gen={r.clauses.size} sameClauses={sameCls}"; return 1
    else
      IO.eprintln usage; return 2
  | _, _ => IO.eprintln usage; return 2

/-- M1's modes (the port `gen`), unchanged. -/
def mainGen (args : List String) : IO UInt32 := do
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

def main (args : List String) : IO UInt32 := do
  match args with
  | mode :: rest => if mode.startsWith "twin-" then twinMain mode rest else mainGen args
  | [] => IO.eprintln usage; return 2
