import V182Geo.End

/-! Reviewer non-vacuity checks (v182-lean, slot lrv3). Kept apart from Audit.lean so that a slip here cannot hide the
axiom audit. -/

open V182Geo V182Enc

/-- Rainbowness is a real constraint: `G` has a 4-cycle subgraph, so no rainbow colouring with 3 colours exists. -/
theorem sanity_not_three : ¬ RainbowColorable 3 := by
  rintro ⟨col, h⟩
  have h4 := h _ _ _ _ cycXY
  have hl := h4.length_le_card
  simp only [Fintype.card_fin, List.length_cons, List.length_nil] at hl <;> omega

/-- The antecedent `parseDimacs (pieceText q) = some (nv, F)` of `PieceVerdicts` holds for every piece, so the
hypothesis says exactly: every listed piece CNF is unsatisfiable. -/
theorem sanity_pv_iff : PieceVerdicts ↔
    ∀ q ∈ pieces, ¬ EncB.DimacsSatisfiable (EncB.cubeCnf baseCnf (pieceCube q)) := by
  constructor
  · intro h q hq
    exact piece_unsat h hq
  · intro h q hq nv F hp
    have e : EncB.parseDimacs (pieceText q) = some (nVars, EncB.cubeCnf baseCnf (pieceCube q)) :=
      EncB.parseDimacs_renderCube nVars baseCnf (pieceCube q) baseCnf_wf (pieceCube_wf q)
    rw [e] at hp
    simp only [Option.some.injEq, Prod.mk.injEq] at hp
    obtain ⟨-, rfl⟩ := hp
    exact h q hq

/-- `chiRainbow_eq_six'`'s hypothesis is `PieceVerdicts` verbatim. -/
theorem sanity_pv_unfold : PieceVerdicts = (∀ q ∈ pieces, ∀ (nv : ℕ) (F : List (List ℤ)),
    EncB.parseDimacs (pieceText q) = some (nv, F) → ¬ EncB.DimacsSatisfiable F) := rfl

#print axioms sanity_not_three
#print axioms sanity_pv_iff
#print axioms sanity_pv_unfold
