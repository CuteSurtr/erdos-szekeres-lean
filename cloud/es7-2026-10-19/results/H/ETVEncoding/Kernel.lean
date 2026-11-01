import ETVEncoding.Hull

/-!
# A kernel-evaluable form of `dimacsB`

`dimacsB` numbers variables with a `HashMap`, whose hash (`mixHash`) is opaque, so the kernel
cannot evaluate it. `dimacsBSpec` writes the same numbering with `List.idxOf`, and
`dimacsB_eq_spec` proves the two are equal. Small instances can then be checked by
`decide +kernel` (kernel reduction only, no `native_decide`, no new axiom); see
`ETVEncoding.Rup` and `ETVEncoding.EndToEnd`.
-/

namespace ETV

open Lit

/-- The numbering of `dimacs`, written with `List.idxOf`. -/
def litSpec (l : List Var) (x : Lit) : ℤ :=
  if x.pos then ((l.idxOf x.var + 1 : ℕ) : ℤ) else -((l.idxOf x.var + 1 : ℕ) : ℤ)

/-- `dimacsB` with the `idxOf` numbering. -/
def dimacsBSpec (N K : ℕ) (hull mirror flip mono : Bool) : List (List ℤ) :=
  (trackBClauses N K hull mirror flip mono).map fun c => c.map (litSpec (allVars N K K))

theorem dimacsB_eq_spec {N K : ℕ} {hull mirror flip mono : Bool} (hN : 3 ≤ N) :
    dimacsB N K hull mirror flip mono = dimacsBSpec N K hull mirror flip mono := by
  unfold dimacsB dimacsBSpec
  apply List.map_congr_left
  intro c hc
  apply List.map_congr_left
  intro x hx
  have hv : x.var ∈ allVars N K K := by
    rcases mem_trackBClauses hc with hc' | hc'
    · exact etvClauses_vars c hc' x hx
    · exact sbClauses_vars hN c hc' x hx
  simp only [litToInt, litSpec, numberMap_getD hv]

end ETV
