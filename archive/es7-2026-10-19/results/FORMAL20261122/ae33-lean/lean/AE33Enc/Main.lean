import AE33Enc.Data

/-!
# AE33Enc.Main: the printer exe `ae33print` (Std-only)

* `ae33print cnf <i>` (0 ≤ i < 203) writes exactly the string `cnfText i` to stdout (trust path, E1/E4).
* `ae33print pts` writes `ae33` in the format of `ae33.txt` ("x y\n" per point) with ENCBLEAN's decimal printer.
* `ae33print name <i>` writes `ae_d<u>_<v>`; `ae33print stats <i>` writes block and convex counts (not trust path).
-/

open AE33

def ptsText : String :=
  ae33.foldl (fun s p => ((EncB.pushInt ((EncB.pushInt s p.1).push ' ') p.2).push '\n')) ""

def famIdx : Desc → Nat
  | .r2 w .. => w
  | .ac w .. => 2 + w
  | .rad .. => 4
  | .gp e .. => 5   -- split below by pivot
  | .oct w _ => 8 + w
  | .jk .. => 10

def statsText (i : Nat) : String := Id.run do
  let B := baseOf i
  let n := B.size
  let mut c : Array Nat := Array.replicate 11 0
  for d in gen B do
    if (clauseOf B d).isSome then
      let f := match d with
        | .gp e .. => if e < n then 5 else if e == n then 6 else 7
        | d => famIdx d
      c := c.modify f (· + 1)
  let e := enumConvex B
  let names := ["r2x", "r2y", "acx", "acy", "rad", "gpa", "gpp", "gpq", "octx", "octy", "jk"]
  let mut s := s!"\{\"n\":{n},\"vars\":{numVars B},\"clauses\":{c.foldl (· + ·) 0}"
  for k in [0:11] do
    s := s ++ s!",\"{names[k]!}\":{c[k]!}"
  for m in [3:8] do
    s := s ++ s!",\"convex{m}\":{e.1[m]!}"
  return s ++ "}\n"

def usage : IO UInt32 := do
  IO.eprintln "usage: ae33print cnf <i> | pts | name <i> | stats <i>   (0 <= i < 203)"
  return 1

def main (args : List String) : IO UInt32 := do
  let out ← IO.getStdout
  match args with
  | ["cnf", s] =>
    match s.toNat? with
    | some i =>
      if i < 203 then
        out.putStr (cnfText i)
        return 0
      else usage
    | none => usage
  | ["pts"] =>
    out.putStr ptsText
    return 0
  | ["name", s] =>
    match s.toNat? with
    | some i =>
      if i < 203 then
        out.putStr s!"ae_d{(pairOfIdx i).1}_{(pairOfIdx i).2}\n"
        return 0
      else usage
    | none => usage
  | ["stats", s] =>
    match s.toNat? with
    | some i =>
      if i < 203 then
        out.putStr (statsText i)
        return 0
      else usage
    | none => usage
  | _ => usage
