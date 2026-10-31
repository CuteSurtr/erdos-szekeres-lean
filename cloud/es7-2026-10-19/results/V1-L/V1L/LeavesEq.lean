import V1L.Leaves

/-! `lake exe leaves_eq FILE` parses a march_cu cube file (`a l1 … lk 0` per line, blank
lines skipped) and checks that it is exactly `V1L.hullLeaves`, cube for cube and literal for
literal. It prints `s EQUAL` or `s DIFFERENT`. This is an unverified cross-check of the
generated data in `Leaves.lean`, not part of any proof. -/

def parseLine (line : String) : Except String (Option (List Int)) := do
  let toks := (line.trim.splitOn " ").filter (· ≠ "")
  match toks with
  | [] => return none
  | "a" :: rest =>
    let ints ← rest.mapM fun s => match s.toInt? with
      | some n => pure n
      | none => throw s!"bad token {s} in: {line}"
    if ints.getLast? != some 0 then throw s!"cube line not ending in 0: {line}"
    return some ints.dropLast
  | _ => throw s!"not a cube line: {line}"

def main (args : List String) : IO UInt32 := do
  let [f] := args | IO.eprintln "usage: leaves_eq CUBEFILE"; return 2
  let s ← IO.FS.readFile f
  let mut cubes : Array (List Int) := #[]
  for line in s.splitOn "\n" do
    match parseLine line with
    | .ok (some c) => cubes := cubes.push c
    | .ok none => pure ()
    | .error e => IO.eprintln e; return 2
  IO.println s!"c file cubes: {cubes.size}, hullLeaves: {V1L.hullLeaves.length}"
  if cubes.toList == V1L.hullLeaves then
    IO.println "s EQUAL"; return 0
  else
    IO.println "s DIFFERENT"; return 1
