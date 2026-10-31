import MirrorEncoding.CoverCore

/-! `lake exe cover_check [--timed] FILE...` reads cubes, one per line, from the files and runs
`Mir.coverCheck`. Lines are march_cu cubes `a l1 l2 … 0` (a leading `a` is dropped) or, with
`--timed`, the `time l1 l2 … 0` lines of `results/C*/logs/*/closed.txt` (the first token is
dropped). The trailing `0` ends the cube; blank lines and `c` lines are skipped.
`Mir.coverCheck` is
proved sound in `Cover.lean`: `Mir.covers_of_coverCheck`. It prints
`s COVERED` or `s NOT COVERED`. Only the parsing below is unverified. -/

open Mir

def parseCube (timed : Bool) (line : String) : Except String (Option (List Int)) := do
  let toks := (line.trim.splitOn " ").filter (· ≠ "")
  match toks with
  | [] => return none
  | "c" :: _ => return none
  | t :: rest =>
    let toks := if timed then rest else if t == "a" then rest else t :: rest
    let ints ← toks.mapM fun s => match s.toInt? with
      | some n => pure n
      | none => throw s!"bad token {s} in: {line}"
    if ints.getLast? != some 0 then throw s!"cube line not ending in 0: {line}"
    return some ints.dropLast

def main (args : List String) : IO UInt32 := do
  let (timed, args) := if args.head? == some "--timed" then (true, args.tail) else (false, args)
  if args.isEmpty then
    IO.eprintln "usage: cover_check [--timed] CUBEFILE..."; return 2
  let mut cubes : Array (List Int) := #[]
  for f in args do
    let s ← IO.FS.readFile f
    for line in s.splitOn "\n" do
      match parseCube timed line with
      | .ok (some c) => cubes := cubes.push c
      | .ok none => pure ()
      | .error e => IO.eprintln e; return 2
  IO.println s!"c cubes: {cubes.size}"
  if coverCheck cubes.toList then
    IO.println "s COVERED"; return 0
  else
    IO.println "s NOT COVERED"; return 1
