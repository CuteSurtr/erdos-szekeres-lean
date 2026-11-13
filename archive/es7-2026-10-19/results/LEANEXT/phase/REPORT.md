# lean_phase: phase patterns of three directions, and the two angular rules

4 November 2026 (KST). The file is `PhaseClassification.lean` (540 lines, 32 theorems, SHA-256 `490efcd0…`).
- **Imports.** It is self-contained apart from the repository imports and Mathlib. `polar`, `orient_polar`, both rules
  and `sin_add_lt` are copied verbatim from `LAYERLEAN/LayerLemma.lean`.
- **Checks.** The coordinator re-checked the build (exit 0, no messages), the scan (no `sorry`, `admit` or `axiom`), the
  hash, and the 16 standard-axiom lines independently.

## Lean-checked

All 16 main theorems depend only on [propext, Classical.choice, Quot.sound]. Eight mutants all fail to compile.

**Setting.** The directions are in ccw order, α < β < δ < α + 2π, with gaps g₁ = β−α, g₂ = δ−β and g₃ = α+2π−δ.
- `inArc` means "lies in the open arc".
- `Alternating` is the pattern PAPAPA: every arc contains an antipode.
- `RunMidB` is a cyclic PPP run with middle β; `RunMidA` and `RunMidD` are its two shifts.
- Genericity means all gaps ≠ π.

**(b) Alternation.**
- `alternating_iff_gaps_lt_pi`: the pattern alternates iff all three gaps are < π. No genericity is needed.
- `alternating_exactly_one`: in that case each arc contains exactly one antipode.

**Runs.**
- `runMidB_iff`: given g₃ ≠ π, a run with middle β is equivalent to δ − α < π, i.e. an open half-plane.

**(a) Classification.**
- `gap_classification`: under genericity, all gaps are < π, or one pair of adjacent gaps sums to < π.
- `phase_trichotomy`: under genericity, the pattern alternates or has a run with middle α, β or δ, and not both.

**Geometry.**
- `centre_inside_of_alternating`: an alternating pattern puts the centre strictly inside the triangle.
- `halfplane_of_runMidB`: a run puts the three points in an open half-plane through c.

**Rules, with the right sign.**
- `orient_pos_of_alternating` (rule A).
- `orient_pos_of_runMidA`, `orient_pos_of_runMidB` and `orient_pos_of_runMidD` (rule B, middle point of largest radius).
- `orient_pos_of_phase`: the combined statement.
- `orient_sign_of_phase`: for arbitrary real angles, the sign is + for the ccw order a, b, d and − for a, d, b. This is
  the encoder's `lit = v if sg > 0 else -v`.

**Arbitrary points.** `exists_polar` (every p ≠ c is `polar c r θ` with r > 0) and `polar_toIcoMod` (reducing θ
modulo 2π does not move the point).

**Discrete word** (`word_dichotomy`, by `decide`). All 64 words of length 6 with antipodal positions (s(i+3) = ¬s(i))
are alternating or contain a cyclic PPP, and not both. This is exactly the encoders' case split.

## Not in Lean

1. **Integer keys.** That sorting the integer keys (J, rank) gives the true circular order. This needs the cell
   decomposition θ = J·unit + ψ.
2. **Sorted word.** That the sorted P/A string is the cyclic word of `word_dichotomy`, with PPP read as `RunMid*` of the
   middle point.
3. **Layers.** Joining layer index to radius (`dist2_le_of_later`) in one theorem. The files cannot import each other.
4. **Genericity.** Phase perturbation, and that the integer keys are tie-free.
5. **Encoder A.** Its float sampling is not covered.

Logs are in `logs/`; `scratch/mutants.py` regenerates the 8 mutants.
