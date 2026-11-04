# keys: integer (cell, rank) keys give the circular order (Lean-checked)

The file is `KeyOrder.lean` (158 lines, SHA-256 `6e34096c…`, standalone, Mathlib only). Every theorem assumes u > 0 and
phases 0 ≤ ψ < u.
- **Checks.** The build is clean, re-checked independently.
- **Axioms.** All theorems depend only on [propext, Classical.choice, Quot.sound].

**Theorems.**
- `cell_lt_iff`: J₁u + ψ₁ < J₂u + ψ₂ iff J₁ < J₂, or J₁ = J₂ and ψ₁ < ψ₂. `cell_eq_iff` is the equality version.
- `cell_lt_iff_rank` (and a Finset version): with a strictly monotone rank on the phases, the direction order equals
  the lexicographic order of (J, rank ψ).
- `reduce_mod_two_pi`: if N·u = 2π, reducing into [0, 2π) gives the cell J mod N with the same phase.
- `antipode_odd`: with units π/m, the antipode has cell (J + m) mod 2m.
- `antipode_even`: with units 2π/m and m even, the antipode has cell (J + m/2) mod m. Both match encoder B's
  conventions.
- `reduced_lt_iff_key`: the order of reduced directions equals the lexicographic key order. This is the step "sorting
  keys gives the circular order" in `gen_b2.py`.

**Mutants.** Weakening ψ < u to ψ ≤ u makes the proof fail. Weakening strict monotonicity also fails, partly for a
syntactic reason.

**Still hypotheses.**
- That the encoder's decomposition θ = J·u + ψ (via h_i and J = 2k + h_i) has ψ in [0, u).
- That the ranks are strictly monotone, i.e. phases distinct across layers. For even m this is `orbit/same_ray_false`
  and `merged/phase_ne_of_distinct_layers`.
