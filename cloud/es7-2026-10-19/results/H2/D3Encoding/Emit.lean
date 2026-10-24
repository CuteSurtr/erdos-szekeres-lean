import D3Encoding.Clauses

/-!
`lake exe d3_dimacs N K OUT` writes `D3.d3Cnf N K` in the layout of `d3cnf.py N K -o OUT`.
Only this string formatting is unverified.
-/

open D3

def main (args : List String) : IO UInt32 := do
  match args with
  | [n, k, out] =>
    let N := n.toNat!
    let K := k.toNat!
    let (nv, nX, cls) := d3Cnf N K
    IO.FS.withFile out .write fun h => do
      h.putStr s!"c symmetric chirotope CNF N={N} K={K} m=3 center=aux sb=True kgon=layered\n"
      h.putStr s!"c triple-orbit variables 1..{nX}; see map file\n"
      h.putStr s!"p cnf {nv} {cls.length}\n"
      for c in cls do
        h.putStr (" ".intercalate (c.map toString) ++ " 0\n")
    return 0
  | _ =>
    IO.eprintln "usage: d3_dimacs N K OUT"
    return 1
