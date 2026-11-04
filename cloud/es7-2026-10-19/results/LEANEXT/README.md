# LEANEXT: Lean extensions and an independent review of LAYERLEAN (4 November 2026)

**Lean-checked.**
- Every theorem below depends only on [propext, Classical.choice, Quot.sound].
- No file contains `sorry`, `admit` or `axiom`.
- Each file compiles with `lake env lean` from the repository root, with no messages.
- Each was rebuilt and its axioms and hashes re-checked independently before inclusion.

**Imports.** The files are standalone, not importable modules. `es7corr/ES7Corollaries.lean` starts with an exact copy
of `LAYERLEAN/LayerLemma.lean` (checked with `diff`).

| Directory | Content |
|---|---|
| `orbit/` | `OrbitConsistency.lean`: rotation invariance of `orient`; permutation-sign consistency of one SAT variable per triple orbit (`encoder_literal_sound`, the `gen.py` literal rule); for even m, no two points of S on one ray from c, so distinct layers have distinct, nonzero phases with no perturbation (`same_ray_false`, `phase_ne_of_not_mem_orbit`). `check_literals.py` (evidence only): `gen.py`'s literal code against real orientations, 0 mismatches. |
| `phase/` | `PhaseClassification.lean`: alternation (PAPAPA) iff all three gaps < π; under genericity, alternation or a PPP run with a given middle point (half-plane); both connected to the angular rules with the right sign, including arbitrary angles (`orient_sign_of_phase`); `word_dichotomy` (by `decide`) is the encoders' discrete case split. |
| `es7corr/` | From `Fivefold35`: every fivefold set of 32 or more points has a convex 7-gon. From `Fourfold32`: every fourfold set of 29 or more points has one. These are the ES(7) maxima 31 and 28 relative to the SAT case classes; the examples are in `SYMMAX`. |
| `merged/` | `Merged.lean`: LayerLemma plus the even-m phase results in one file; `phase_ne_of_distinct_layers` and `not_same_ray_of_distinct_layers` (distinct layers have distinct phases mod 2π/m). |
| `review/` | An adversarial review of `LAYERLEAN` with no error found, and `VacuityTest.lean`: a concrete fourfold configuration discharging every hypothesis of `strict_nesting`, `layers_are_orbits`, `hullVerts_eq_orbitFS_rotAbout` and `chain_clauses_sound`. |

**Still outside Lean.**
- Integer (sector, rank) keys versus the true circular order.
- The perturbation to generic phases (odd m).
- Encoder A's float sampling.
- The code-to-clause correspondence.
- The symmetry-breaking units and the cube cover.
