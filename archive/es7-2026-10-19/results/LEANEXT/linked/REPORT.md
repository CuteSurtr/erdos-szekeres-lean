# linked: rule B for layered configurations

The file is `Linked.lean` (SHA-256 `f1e18c11…`). Lines 1–1384 are identical to `merged/Merged.lean`. It then adds:
- `dist2_polar`: `dist2 c (polar c r θ) = r²`.
- `orient_pos_of_layers`, under the layer-lemma hypotheses:
  - a ∈ `peel S na`, b ∈ `hullVerts (peel S nb)` and d ∈ `peel S nd`, with nb ≤ na and nb ≤ nd, so that b is in the
    outermost layer;
  - a, b and d in polar form with positive radii;
  - 0 < β−α, 0 < δ−β and δ−α < π.

  Conclusion: `0 < orient a b d`. This is rule B stated directly on the layer indices, which is what the encoders use.

**Lean-checked.**
- **Build.** Clean, re-checked independently.
- **Axioms.** Both theorems depend only on [propext, Classical.choice, Quot.sound].
- **Mutant.** Reversing `nb ≤ nd` makes the proof fail.

**Open issues.** The polar forms are still hypotheses; `phase/exists_polar` provides them but is not merged into this
file.
