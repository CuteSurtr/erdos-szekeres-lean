import C3Encoding.Gen

/-!
# The layer units of `results/C3-S/tools/hullcase.py` (`layer_clauses`)

A node of the C3-S layer tree is named by layers joined by `_`, residues of a layer by `-`,
and an optional suffix `s0`/`s1` giving `sigma` (`parse_layers`). The node CNF
(`close_node.py`, `compose.py`) is the base CNF with the literals of `layer_clauses` appended as
unit clauses, unnormalised, and the header clause count increased accordingly.
-/

namespace C3

/-- A layer: residues `r < m`, each with an optional `sigma_r`. -/
abbrev Layer := List (Nat × Option Nat)

/-- `parse_layers` (malformed tokens give residue `0`; the names used are well formed). -/
def parseLayers (name : String) : List Layer :=
  (name.splitOn "_").map fun lay => (lay.splitOn "-").map fun tok =>
    match tok.splitOn "s" with
    | [r, s] => (r.toNat?.getD 0, some (s.toNat?.getD 0))
    | _ => (tok.toNat?.getD 0, none)

/-- `layer_order`: the counter-clockwise order of the layer's points. -/
def layerOrder (m : Nat) (L : Layer) : List Nat :=
  match L with
  | [(r, _)] => [r, r + 2 * m, r + m]
  | _ =>
    let key := L.flatMap fun (r, s) =>
      let s := s.getD 0
      [(s, r), (1 - s, r + m), (s, r + 2 * m)]
    (key.mergeSort fun a b => a.1 < b.1 || (a.1 == b.1 && a.2 ≤ b.2)).map (·.2)

/-- `layer_clauses`, as the list of unit literals. -/
def layerUnits (E : Tables) (layers : List Layer) : List Int := Id.run do
  let mut used : List Nat := []
  let mut out : Array Int := #[]
  for L in layers do
    for (r, s) in L do
      match s with
      | some s => if r != 0 then out := out.push (if s == 1 then E.sig r else -E.sig r)
      | none => pure ()
    let H := layerOrder E.m L
    let rest := (List.range E.n).filter fun w => !used.contains w
    for t in List.range H.length do
      let u := H[t]!
      let v := H[(t + 1) % H.length]!
      for w in rest do
        if w != u && w != v then out := out.push (E.ccw u v w)
    used := used ++ H
  return out.toList

end C3
