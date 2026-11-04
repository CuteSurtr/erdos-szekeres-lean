# capstone: the encoders' discrete rule-B case on layered configurations

The file is `Capstone.lean` (2004 lines, SHA-256 `dc382395…`): `linked/Linked.lean` and `phase/PhaseClassification.lean`
in one file, with the phase file kept in its own namespace.
- **Checks.** The build is clean (exit 0, no messages) and there is no `sorry`, `admit` or `axiom`. The coordinator
  re-checked both independently.
- **Axioms.** All three new theorems depend only on [propext, Classical.choice, Quot.sound].

**Lean-checked.**
- **`orient_pos_of_layers_runMidB`.** The hypotheses are:
  - the layer-lemma hypotheses;
  - b a hull vertex of layer nb, with nb ≤ the layers of a and d;
  - polar forms with α < β < δ < α + 2π and α + 2π − δ ≠ π;
  - the discrete pattern `RunMidB` (a PPP run with middle b).

  Conclusion: `0 < orient a b d`. This is the encoders' rule-B case in terms of its discrete pattern.
- **`orient_pos_of_alternating_polar`.** Rule A from the alternating pattern.
- **`polar_eq`.** The two copies of `polar` agree.

**Mutants.** Dropping the genericity hypothesis makes the proof fail. Flipping the conclusion also fails.

**Open issues.** The runs with middle point a or d follow in the same way (`orient_pos_of_runMidA`/`D`) but are not
combined with layers here. The polar forms are assumed (see `phase/exists_polar`).

## Capstone2.lean (all three run positions)

The file is `Capstone2.lean` (2132 lines, SHA-256 `f8c3930c…`). Lines 1–2003 are identical to `Capstone.lean`.
- **Checks.** The build is clean, re-checked independently.
- **Axioms.** All main theorems depend only on [propext, Classical.choice, Quot.sound].

**Lean-checked.**
- **`orient_pos_of_layers_runMidD` and `orient_pos_of_layers_runMidA`.** The runs with middle point d or a in the
  outermost layer.
- **`orient_pos_of_layers_runMid{B,D,A}_intrinsic`.** The same three cases with intrinsic radii: each point is
  `polar c (√(dist2 c ·)) θ`, and positivity comes from c ∉ S.
- **Helpers.** `exists_angle` (every p ≠ c has such a form, from `exists_polar`), `sqrt_dist2_pos`, `polar_zero` and
  `ne_of_mem`.

**Mutant.** Reversing the outermost-layer hypothesis makes the proof fail.

**Open issues.**
- **Sorted angles.** The angles must be given sorted (α < β < δ < α + 2π). The unsorted case
  (`orient_sign_of_phase`) is not wired in.
- **Gap conditions.** The gap conditions ≠ π are assumed rather than derived from general position.
