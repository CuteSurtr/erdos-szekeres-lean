# Writer report for section `ll` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- 35 overfull hboxes (up to ~150pt), all in statement heads with long \leanref lists. They come from the shared preamble: the amsthm head plus long unbreakable \nolinkurl chunks; \allowbreak does not help. Tested fix: add \sloppy (or raise \tolerance) in preamble.tex, which removed all of them in a test. This affects every section.
- The preamble's \lean{} is built on \nolinkurl, which ignores spaces, so Lean expressions with spaces (e.g. rotAbout c (2 * Real.pi / m)) print run together. I used \texttt{} for those; other writers may hit the same pitfall.
- rotAbout_iterate (LayerLemma.lean:465) is covered here (Lemma ll:lem:rot(d)) although the task's scope list did not name it; it lies in the given line range and the self-contained centre argument in the sixfold proof uses it. The lg writer may duplicate it, which is harmless.
- Added Corollary ll:cor:decomp (written step) for the decomposition into t nested orbits. It is not an export label, so other sections cannot \ref it; promote it to an export if others need it.
- Theorem ll:thm:sixfold cites Lemma lg:lem:centre (centre_not_mem_of_even) and also includes the short self-contained argument for m = 6, so it does not depend on the lg section's text.
- The proofs of extreme_mem_hullVerts, subset_convexHull_hullVerts and hullVerts_nonempty are elementary (convex combinations, an exchange-argument induction) and differ from Lean's Krein-Milman route; this is stated in the text. The convex hull = convex combinations fact is cited as Rockafellar, Convex Analysis, Thm 2.3.
- Remark ll:rem:hyp describes how Sixfold66/Sevenfold70 are supplied: C6UPPER/C7UPPER cake_lpr verdicts (rigor label certificate), the written unrefereed soundness proof WRITEUP/note/k8_soundness.tex, and further written steps recorded in C6UPPER; for m = 6 the ENCBLEAN Lean route takes the SAT verdicts as a hypothesis. This summary is from the C6UPPER/C7UPPER READMEs and the inventory, not re-derived.

## contract_discrepancies

## not_covered

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/ll.tex as of the snapshot)
- 15.5pt in paragraph at lines 417--419
- 18.7pt in paragraph at lines 451--453
- 50.3pt in paragraph at lines 290--292
