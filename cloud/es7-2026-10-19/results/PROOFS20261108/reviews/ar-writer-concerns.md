# Writer report for section `ar` (from the writing stage; machine paths may appear here, never copy them)

## concerns
- Preamble/amsthm interplay: amsthm sets theorem heads in an hbox, where TeX inserts no automatic math penalties, so the url-based \lean/\dirn names inside \leanref heads cannot break. That caused 30-800pt overfull heads. I worked around it inside the section with \begingroup\sloppy\emergencystretch=\linewidth ... \endgroup, which gives 0 overfull boxes. A preamble-level fix would serve all sections better.
- \lean{...} (via \nolinkurl) drops spaces and breaks on non-ASCII. Lean expressions with arguments must be written as \lean{HasConvexNGon}~$n$~$S$, and Greek letters must stay out of \lean{}. Other writers should know this.
- Remark ar:rem:classes and the Coverage paragraph \ref the mb: export labels mb:thm:baek, mb:thm:classes and mb:thm:main3. The contract allows other sections' export labels, but the task text mentioned only sr: and fd:.
- Proposition ar:prop:averaging is a written step that goes beyond Lean. Lean derives only L^m = 1 and the implication g != id => h != id; the claims g^m = id, h^k = T g^k T^{-1} and equal orders are written proofs only. This is stated explicitly in the proof and in Remark ar:rem:hE. It supports the P1 Remark rem:affine, whose order-preserving form remains unformalized.
- The rigor evidence relies on recorded logs of 1 Nov 2026 (logs/AffineReduction.out empty, exit 0; logs/AffineReductionAxioms.out). Re-running Lean was not allowed. The source scan finds no decide, native_decide, sorry or admit.
- The class-status remark follows SYMLEAN/README.md sections 5 and 9. Checker trust may have changed since then (later project notes question lrat-check), so I used neutral wording: 'SAT certificates with recorded checker verdicts'.

## contract_discrepancies
- Task text: 'You may \ref sr: and fd: export labels'. Contract: any export label of other sections. I also used three mb: export labels; both documents allow this, but the task text is narrower.
- fd:lem:affine-cp is phrased for injective affine maps. The identity g(conv Y) = conv(gY) holds for every affine map (Step 1 of ar:lem:cp-affine proves it without injectivity). This does not affect correctness.

## not_covered
- SYMLEAN/AffineReduction.lean lines 1-1058: byte-identical duplicate of SYMLEAN/SymmetricReduction.lean (checked with diff), covered by section sr; iterate_mem (:69) is re-derived inline and point_ext (:502) is used tacitly
- SYMLEAN/AffineReductionAxioms.lean: same 1533 lines plus 9 #print axioms lines and 1 #check line; used only as axioms evidence
- Verbatim copy of these declarations inside SYMLEAN/mirror/ReductionThreeClasses.lean (line + 26); its own content (the _3 theorems) belongs to section mb

## Overfull boxes > 1pt in the full-document build (line numbers refer to sections/ar.tex as of the snapshot)
- none
