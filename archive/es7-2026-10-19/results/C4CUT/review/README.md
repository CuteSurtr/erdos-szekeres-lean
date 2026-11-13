# Independent review of C4CUT (1 November 2026)

**The review.** An adversarial review, run separately from the work it checks. It was given the code and the claims,
not the authors' reasoning, and used its own scripts (this directory). It reused no project code, except running
unmodified copies of the encoder.

**Verdict.** No blocking or major finding.

## What was checked

**Encoder `SYM5/symcnf_layers.py` with m = 4.** Checked by argument for every clause family:
- the triple-orbit identification and literal signs;
- the interiority axiom, via det(pqr) = det(tqr) + det(ptr) + det(pqt);
- the Grassmann–Plücker clauses and the convexity implications;
- the K-set clauses: a non-convex 7-set has a non-convex 4-subset, hence a non-convex 6-subset;
- the layer units and the even-m sector units, which are chi((0,0),(0,2),(o,0)) = −1 and chi((0,1),(0,3),(o,0)) = +1
  for a representative in the open quadrant counter-clockwise from (0,0).

**Clause count.** The family sizes add up to the header exactly:
72,192 + 4,027,520 + 54,144 + 50,344 + 226,688 + 841,464 + 142 = 5,272,494.

**Exact tests** (`geom.py`, `evalcnf.py`; integer and rational arithmetic). For each labelled set, the triple variables
are fixed from exact orientations, and the convexity variables are set to the least model of the remaining Horn part.
Every clause is then evaluated.
- **`SYMMAX/c4_28points.txt`.** The set and all 120 of its whole-orbit subsets with at least two orbits, each in 16
  labellings: 0 violated clauses (`test_real_28.log`).
- **Perturbed sets.** 41 distinct 7-gon-free 28-point chirotopes made by perturbing it: all satisfy the N = 28 formula.
- **Random nested 7-gon-free sets.** 52 at N = 12, 32 at N = 16 and 8 at N = 20: all satisfy their formulas.
- **Random nested sets with convex 7-gons,** at N = 12 to 28 and on the N = 32 formula itself.
  - No axiom, sector, layer or convexity clause is ever violated.
  - The violated K-set clauses always number (convex 7-sets)/4.
- **Near-degenerate sets.** Representatives within 1e-9 rad of a diameter, and nearly touching layers: no violation.
- **Negative controls.** Swapped layers, a wrong sector, clockwise labelling, and a moved (0,0) without relabelling:
  all rejected.

**Cuts.**
- The GP identity holds on 5,000 random integer quintuples, and a wrong sign pattern fails.
- The minority step and the cancellation argument were checked by hand. The global sign convention is irrelevant,
  since every term is a product of two brackets.
- `verify_cuts.py` passes, and so does the reviewer's own `my_verify_cuts.py`. The latter also checks that each clause's
  variables are exactly the 55 triple-orbit variables of labels 20..31.
- Mutations are rejected by both verifiers: a flipped literal, swapped plus/minus, a changed or zero weight, a dropped
  row, and a dropped literal.

**Final link.**
- The regenerated base CNF is `c3933d9a…` and the map is byte-identical (`f72b186e…`).
- Base plus cuts rebuilt as in `c4final.sh` is `2aa18f1e…`, as in `final.json`.
- A re-solve without proof gave UNSAT in 26 s.

**Consequence.**
- The centre cannot belong to a fourfold set in general position, so the size is a multiple of 4.
- `SYMMAX/c4_28points.txt` is fourfold and in general position, with layers that are single orbits.
- It has no convex 7-subset by two methods, the second being a hull computation over all 1,184,040 7-subsets.

## Minor findings and their resolution

1. **No guard on the floating-point sector sign.** The even-m sector sign is computed in floating point, and the
   `abs(d) > 1e-9` guard of `symcnf.py` is absent. This is harmless: d = −2 sin(π(1 − 2j)/m) is ±√2 for m = 4. The
   encoder is left unchanged so that its recorded hash stays valid.
2. **Layer-lemma hypotheses spread out.** The lemma's hypotheses (general position, no centre in the set) appear on
   different docstring lines. This is documentation only, and the lemma holds for m = 4, K = 7.
3. **Verifier gaps.** `verify_cuts.py` did not tie the map to the CNF, accepted `true` as a weight, and checked distinct
   anchors only implicitly. Fixed: weights must be of type int, repeated anchor points are rejected, and the map's
   SHA-256 is printed and recorded in `../README.md`.
4. **Verdicts rest on logs.** The checker verdicts are recorded in `final.json` and the logs; the proof is archived
   outside Git. This is unchanged by design.
5. **Wording.** The README said the six cuts "match" the six patterns of arXiv:2506.00224. It now says only that the
   counts agree. `SYM5/README.md` §4 still cites the enumeration; it will be updated with the write-up.
