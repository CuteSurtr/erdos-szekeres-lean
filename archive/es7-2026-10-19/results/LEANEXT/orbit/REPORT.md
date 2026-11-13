# lean_orbit: orbit variables and even-order phase variables of the layered encoders

4 November 2026 (KST). The file is `OrbitConsistency.lean` (429 lines, SHA-256 `9b843180…`). Rigor labels follow
`RULES.md`. The coordinator re-checked the build, the `sorry` scan, the hash and the axioms independently.

## Lean-checked

All 15 main theorems depend only on [propext, Classical.choice, Quot.sound]. Five mutant copies all fail to compile.

**(a) Rotation invariance.**
- `orient_rotAbout_inv`: `orient (rotAbout c θ a) (rotAbout c θ b) (rotAbout c θ d) = orient a b d`.
- `RotComp.preservesOrient` and `rotComp_iterate`: every composition of rotations by k·2π/m preserves `orient`, and every
  power of ρ is such a composition.

**(b) Consistency of one SAT variable per orbit.**
- `orient3_perm`: `orient3 (t ∘ σ) = sign σ · orient3 t`, for all 6 permutations.
- `orient3_rot_perm`: the general consistency statement.
- `sign_eq_of_two_reps`: if orient ≠ 0, the sign does not depend on the chosen map to the representative.
- `literal_sound` and `encoder_literal_sound`: the literal rule exactly as `gen.py`'s `Enc.o` uses it (sortpar parity
  times canonicalisation parity).

**(c) Even m: no perturbation needed.**
- `antipode_mem_of_even`: for even m, x ∈ S implies 2c − x ∈ S.
- `same_ray_false`: under general position, two points of S on one ray from c are impossible.
- `eq_iterate_of_phase_eq` (ℕ and ℤ versions) and `phase_ne_of_not_mem_orbit`: equal phases mod 2π/m force the same
  orbit. With the layer lemma, distinct layers therefore have distinct, nonzero phases.

## Evidence only

`check_literals.py` runs `gen.py`'s literal code on random nested configurations: m = 6 with t = 6 and t = 11, m = 7
with t = 5, and m = 4 with t = 6. It found 0 mismatches against the real orientations over 368,814 ordered triples.

## Open issues

- **Odd m.** For odd m, the H variables and ψ mod π/m still rely on the written perturbation step.
- **Encoder B.** Its literal code was not tested here. The Lean statement does hold for any choice of representative.
- **Not yet combined.** The step "distinct layers are distinct orbits" (`layers_are_orbits`) is not joined with (c) in
  one file, because these files are not importable modules.
- **Unchanged.** The phase-pattern classification and the code-to-clause correspondence remain review and tests.

The commands, the mutant table and all file hashes are in the agent's hand-back. Logs are in `logs/`; the mutant and
axiom copies are in `scratch/`.
