# SYM16FIVE20261110: at least 49 fivefold symmetric 16-point sets without a convex hexagon (SMQH Appendix B lists 46)

10 November 2026 (KST). **There are at least 49 order types of 16-point sets in general position that are invariant
under the rotation by 2π/5 and have no 6 points in convex position.** "Order type" here merges every relabelling and
the mirror image. Label: **exact computation**.

- **The sets.** The 49 sets are in `sets/`. Each is written exactly in Z[ζ₅], ζ₅ = e^{2πi/5}: three orbit
  representatives a + bζ₅ with integers a and b, plus the centre, which every such 16-point set contains (16 = 3·5 + 1).
- **Two exact checks.** Each set was checked in two ways, by programs written separately:
  - the project's GMP verifier `PRIMEFOLD/rule/sym_cvx.c` certifies every orientation sign nonzero and the largest
    convex subset equal to 5;
  - `tools/sym5_exact.py` computes every orientation sign exactly in Z[ζ₅], with integers only.
- **The 49 are pairwise distinct order types.** This was checked with an independent canonical form, in exact integer
  arithmetic, on the integer realizations of `F/data/sym16/m5/`.
- **Extremal.** By ES(6) = 17, each of these sets is an extremal hexagon-free set.

## Comparison with SMQH

Read on 10 November 2026 from arXiv:2506.00224v1 (B. Subercaseaux, E. Mackey, L. Qian, M. J. H. Heule, *Automated
symmetric constructions in discrete geometry*). The sentences below were checked against the text of the PDF.
- §6.1: "After symmetry breaking, they have 66 and 948 satisfying assignments, respectively." This is for the 4-fold
  and 5-fold formulas.
- §6.1: "Out of the 66 solutions of the 4-fold symmetry, 18 are realizable, while out of the 932 solutions of the 5-fold
  symmetry 92 are realizable."
- §6.1, footnote 2: "The realizer tool can only determine realizability, not unrealizability."
- Appendix B: "Below are the 46 non-isomorphic realizable configurations on 16 points with a 5-fold rotational
  symmetry." The appendix gives plots, not coordinates.
- Appendix A, the control: "Below are the nine non-isomorphic realizable configurations on 16 points with a 4-fold
  rotational symmetry."

**Conclusion.** The paper does not define "isomorphic".
- Any equivalence at least as fine as order type under relabelling and reflection keeps the 49 sets of this record
  pairwise distinct.
- **So the list of 46 in Appendix B is incomplete by at least 3 configurations under any such notion.** It is not
  complete under the coarsest one either.
- Footnote 2 is consistent with this: the paper's realizability test is a heuristic local search.
- Which three configurations are missing cannot be determined here, because Appendix B gives no coordinates.

**Counting solutions as the paper does.**
- **The mapping.** The record `F` (19 October 2026, "calibration (b)") enumerated the models of the 5-fold formula of
  `symcnf.py 16 6 5 --center-in-set`. It found 2,796 models in 466 classes, and 2,796 = 3 · 932. F reads the paper's
  932 as counting mirror images separately and its "up to isomorphism" as merging them, as F's classes do.
- **The count.** In that counting, the 49 classes are at least 98 realizable solutions, against the paper's 92.
- **Caveat.** This mapping is F's reading of the paper's counts; whether `symcnf.py`'s encoding is the paper's was not
  checked. The lower bound of 49 does not depend on it, since it rests only on the point sets.
- **The 4-fold control.** F realized 9 of 33 classes, matching the paper's nine. `tools/ordertypes.py` also gives 9
  distinct order types for F's 4-fold realizations.

## What is new in this record

`F/README.md` (19 October 2026) reported 49 realized 5-fold classes, against 46 in the paper, using integer
realizations found by its heuristic realizer. Those realizations match the class's orientations exactly but are only
roundings of symmetric configurations. This record adds three things:
1. **Exactly symmetric realizations.** For every one of the 49 classes there is a set in Z[ζ₅] with exactly the same
   labelled orientation pattern as F's integer set.
   - `tools/sym5_exact.py` compares all 560 orientation signs per set, with integers only:
     Im(Σ c_k ζ^k) = (c₁ − c₄) sin 72° + (c₂ − c₃) sin 144°.
   - The sign is decided via s₁² = (10 + 2√5)/16 and s₂² = (10 − 2√5)/16.
   - All signs agree and none is zero, with the orbit representatives rounded to a + bζ₅ at scale 1.
2. **An independent distinctness check.** `tools/ordertypes.py` uses a different canonical form from F's
   `chiro.canonical_form`.
   - **The form.** For every convex-hull vertex p and both orientations, label p first and the other points in
     angular order around p. Take the orientation vector of all triples in that labelling, and keep the
     lexicographic minimum.
   - **Why it is a complete invariant.** The labelling is fixed by the order type once p and the orientation are
     chosen.
   - **Self-test.** Each file passes four random relabellings or reflections with the same form (seed 20261110).
   - **Result.** 9 of 9 (4-fold) and 49 of 49 (5-fold) are distinct.
3. **The comparison with the text of the paper** (above). Earlier records quoted the counts second-hand.

## What is not claimed

- **Not the exact number.** It lies between 49 and 466 (the classes of `F`'s model enumeration). The other 417 classes
  are failures of a heuristic realizer within 4 CPU-s each, not proofs of non-realizability.
- **No check of the published version.** Whether the CICM 2025 version of SMQH differs from arXiv v1 was not checked:
  the chapter text was not accessed. Neither the CICM chapter nor Mackey's thesis was consulted for a corrected count.
- **No novelty or priority claim.** The literature was not searched for a later correction.

## Files

- `tools/run_all.sh OUT` (about 5 s) builds `sym_cvx` from `PRIMEFOLD/rule/sym_cvx.c` and runs the three tools on
  `F/data/sym16/{m4,m5}`. A rerun gave the same 49 files byte for byte.
- `tools/ordertypes.py`: canonical forms and distinct order types.
- `tools/sym5_exact.py`: exact comparison of the Z[ζ₅] sets with F's integer sets.
- `tools/make_sym5.py`: writes `sets/` from F's files.
- `logs/ordertypes.log`, `logs/sym5_exact.log`, `logs/sym_cvx.log`: the outputs. `sym_cvx.log` has 49 × `PASS (K=6)`,
  each with "zero orientations: 0" and "largest convex subset = 5".
- `sets/model<N>.pts`: one exactly 5-fold symmetric representative per realized class, named after F's model.
  - Format: that of `PRIMEFOLD/rule`. The line "5 3 1" means p = 5, three orbits and the centre included. Then come
    three rows of coefficients of ζ^0..ζ^4.
  - Example: `model239.pts` has the representatives 16384, 2022 + 2892ζ and 6 + 9394ζ.
