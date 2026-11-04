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
