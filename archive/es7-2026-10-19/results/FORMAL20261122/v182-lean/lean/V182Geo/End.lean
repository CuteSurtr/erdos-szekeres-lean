import V182Geo.Norm
import V182Geo.Six

/-!
# V182Geo.End: χ'_rainbow(G) = 6 modulo the 4,404 piece verdicts (M6)

* `rainbowColorable_six` (V182Geo.Six): a rainbow 6-colouring exists — no hypothesis.
* `not_rainbowColorable_five` (V182Geo.Norm): no rainbow colouring with at most 5 colours, given `PieceVerdicts`.
* `chiRainbow_eq_six`: the least number of colours is 6, given `PieceVerdicts`.

`PieceVerdicts` (V182Geo.Sound) says: for each of the 4,404 pieces `q ∈ V182Enc.pieces`, the text
`V182Enc.pieceText q` (what `v182print` writes; M9 binds its SHA-256 to the certified CNF of that piece) parses
(`EncB.parseDimacs`) to an unsatisfiable clause list. Label: Lean-checked modulo PieceVerdicts (4,404 cake_lpr
verdicts via trust items E1-E6, DESIGN.md §4).
-/

namespace V182Geo
open V182Enc

/-- **χ'_rainbow(G) = 6**, modulo the 4,404 piece verdicts. -/
theorem chiRainbow_eq_six (h : PieceVerdicts) : chiRainbow = 6 :=
  chiRainbow_eq_six_of rainbowColorable_six (not_rainbowColorable_five h)

/-- The same with the hypothesis unfolded. -/
theorem chiRainbow_eq_six' (h : ∀ q ∈ pieces, ∀ (nv : ℕ) (F : List (List ℤ)),
    EncB.parseDimacs (pieceText q) = some (nv, F) → ¬ EncB.DimacsSatisfiable F) : chiRainbow = 6 :=
  chiRainbow_eq_six h

/-- The cover's shape (kernel check): 4,404 pieces, of which 84 direct Y1 cubes; 36 split Y1 cubes. -/
theorem pieces_shape : pieces.length = 4404 ∧ (pieces.filter fun q => q.2.isNone).length = 84 ∧
    splitSet.length = 36 ∧ splitSet.Nodup ∧ (∀ n ∈ splitSet, n < 120) := by
  decide +kernel

/-- info: 'V182Geo.rainbowColorable_six' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms rainbowColorable_six

/-- info: 'V182Geo.not_rainbowColorable_five' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms not_rainbowColorable_five

/-- info: 'V182Geo.chiRainbow_eq_six' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms chiRainbow_eq_six

/-- info: 'V182Geo.chiRainbow_eq_six'' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms chiRainbow_eq_six'

/-- info: 'V182Geo.pieces_shape' does not depend on any axioms -/
#guard_msgs in #print axioms pieces_shape

#check @chiRainbow_eq_six'
#print PieceVerdicts
#print RainbowColorable
#print IsRainbow
#print IsFourCycle
#print G
#print Adj
#print V

end V182Geo
