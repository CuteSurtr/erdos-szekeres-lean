# Section sr, polish round 1: fix log

Inputs: `reviews/sr-r1-fidelity.md` (F1-F8), `reviews/sr-r1-rigor.md` (m1-m6), `reviews/sr-r1-adversarial.md` (F1-F7 and
the notes under "Points examined"), `reviews/sr-r1-claims.md` (M1-M7), `reviews/sr-writer-concerns.md` (concerns and
the 6 overfull boxes of the full-document build). Snapshot of the starting version:
`snapshots/polish-r1-pre/sr.tex`, `snapshots/polish-r1-pre/sr.map.tsv`. Line numbers below refer to
`sections/sr.tex` after the fix (1116 lines). Records were re-read for every change (paths relative to RES):
`C2ENC/class_table.md`, `SYMLEAN/README.md` §1-§9, `WRITEUP/SYMMETRIC.md` (Corollary 3, Theorems 1-5, §3),
`WRITEUP/MIRROR.md` §1 and §6, `H3/README.md`, `H3/MirrorEncoding/Line.lean`, `V2-L/README.md` §9.1 and §9.6,
`V2-L/V2L/FinalTree.lean`, `C2FINAL/README.md`, `C2RECHECK/README.md`, `C3FINAL/README.md`, `C3PIECES/README.md`,
`C3AUDIT2/REPORT.md`, `C4CUT/README.md`, `SYM5/README.md`, `LRATCHECK20261105/README.md`,
`WRITEUP/note/symmetric_es7.tex` (lines 88-104), `SYMLEAN/review/VariantChecks.lean` (group_form, line 1168),
`SYMLEAN/review/ReviewSanity.lean` (lines 1073, 1593, 1629), `SYMLEAN/mirror/ReductionThreeClasses.lean` (header and
namespaces), and the pinned Mathlib (rev f897ebcf) for the names of the written steps.

## Findings

| # | finding | summary | action | location after the fix | reason (declined) |
|---|---|---|---|---|---|
| 1 | fidelity F1 | "over the same reflLine": `Mir.reflLine` and `reflLine` (and the two exclusion props) are distinct constants identified only by text | fixed (one action with adversarial F2 part iii) | Remark sr:rem:mirror-line, l. 1028-1032 (same text; different constants; no Lean theorem in SYMLEAN identifies them; the `rfl` check of SYMLEAN/README.md §5 is not kept) and l. 1039-1041 ("conditionally on those CNF facts and on the identification of the two texts"); paragraph after Def. sr:def:maps, l. 205-206 ("has the same text as") | |
| 2 | fidelity F2 | first sentence of Remark sr:rem:records ("rests on written soundness proofs of the encoders") is wrong for the H3 route | fixed (one action with claims M4 and adversarial F2 part ii) | Remark sr:rem:records, l. 242-251: "written proofs" restricted to the certificate routes of HalfTurn34, Threefold33, Fivefold35, Fourfold32 and to the SYMZ certificates; for the H3/V2-L route the encodings and case split are Lean-checked, and what stays outside Lean is in Remark sr:rem:mirror-line | |
| 3 | fidelity F3 | review names (`mirrorOneAxis33_iff_exclusionLine`, `exclusionLine_of_mirrorOneAxis33`, `group_form`) do not exist under the stated namespace convention | fixed (one action with claims M3 part a) | convention rewritten, l. 110-115 (a name n is the first of ErdosSzekeres.SymReduction.n, ErdosSzekeres.n, n that exists; Review./VariantChecks. are sub-namespaces, Suk. is ErdosSzekeres.Suk, Mathlib/Mir./V2L. names are full); names now `Review.mirrorOneAxis33_iff_exclusionLine` (l. 60), `Review.exclusionLine_of_mirrorOneAxis33` (l. 1043), `VariantChecks.group_form` (l. 1004) | |
| 4 | fidelity F4 | Coverage says the review files are mentioned "only in Remarks ..."; ReviewSanity.lean is also cited in "Axioms and rigor" | fixed (one action with rigor m5, adversarial F5, claims M6) | Coverage, l. 1114-1116 ("cited only in the paragraph on axioms and rigor and in Remarks ...") | |
| 5 | fidelity F5 | Lemma sr:lem:prim (P1): the fixed n is also used as a definition (n = ord(zeta)) | fixed (one action with adversarial F4) | (P1) now speaks of ord(zeta) only, l. 693-695; its proof uses a fresh letter s and states where the hypothesis is used, l. 708-711. Written step; uses in Lemmas sr:lem:root-cases and sr:lem:root-cases2 unchanged and consistent | |
| 6 | fidelity F6 | "That g has the form ... is proved in Theorem sr:thm:structure(a)" omits Lemma sr:lem:toC-iso(b) | fixed | l. 126-127 ("g, read in complex coordinates, ... with abs a = 1 follows from Lemma sr:lem:toC-iso(b) and Theorem sr:thm:structure(a)") | |
| 7 | fidelity F7 | the mirror classes and the `_3` theorem in SYMLEAN/mirror are byte-identical copies (that file cannot import this one) | fixed | Remark sr:rem:records, mirror bullet, l. 276-279 (RTC lines 38-1084 = SymmetricReduction.lean lines 12-1058, checked with `diff` via AffineReduction.lean; same full names and text); Remark sr:rem:main, l. 962-964 | |
| 8 | fidelity F8 | Mathlib's `Isometry.affineIsometryOfStrictConvexSpace` needs only the codomain strictly convex | fixed | proof of Thm sr:thm:structure(a), l. 556-559 ("an isometry from a real normed affine space into a strictly convex one is affine ... does not need surjectivity"; also "isometric equivalences" for `linear_isometry_complex`, whose argument is `ℂ ≃ₗᵢ[ℝ] ℂ`) | |
| 9 | rigor m1 | Remark sr:rem:variant mischaracterizes Corollary 3 of WRITEUP/SYMMETRIC.md (it is per-symmetry; the group form is the note's cor:only) | fixed (one action with adversarial F1, adversarial F7, claims M2) | Remark sr:rem:variant, l. 999-1007: Corollary 3 has the same per-symmetry form with the case theorems and C4CUT as assumptions, but its symmetries include affine bijections; the group form (note, `cor:only`) is Lean-checked for Euclidean isometries as `VariantChecks.group_form` with the same five classes as hypotheses; its content is stated | |
| 10 | rigor m2 | last sentence of Remark sr:rem:redundant: implied hypotheses leave a class equivalent, not weaker | fixed | l. 1066-1067 ("Dropping one of the implied hypotheses above gives an equivalent class. In general, adding a hypothesis ... can only make it weaker ..."); no claim that the hypothesis of MirrorNoAxis34 is not implied (not proved here) | |
| 11 | rigor m3 | overfull boxes in statement heads (39 before the preamble update; 6 after it) | fixed (one action with adversarial F6, claims M1 and the writer's list) | heads retitled or reordered: l. 354 (sr:lem:orbitFS: `card_orbitFS_of_minimalPeriod` listed first; map row reordered), l. 517 (sr:lem:toC-iso), l. 637 (sr:lem:concyclic), l. 932 (sr:thm:main), l. 969 (sr:thm:variant), l. 1016 (sr:lem:mirror-line). Standalone build: 0 overfull boxes; full-document build (private output directory): 0 overfull boxes in sr, all references resolved | |
| 12 | rigor m4 | two informal claims cite lemmas that do not state them: (i) reflLine is the reflection in a+Ru; (ii) fixed points lie on the mirror | fixed | (i) paragraph after Def. sr:def:maps, l. 199-204: complex form from Lemma sr:lem:refl(a), fixes a+tu and sends a+itu to a-itu; the side claim "for other u it is not a reflection" is now proved (u = 0: half-turn; otherwise eDist2 of a+u from a changes from s to (2s-1)^2 s, s = u0^2+u1^2 not in {0,1}); (ii) Def. sr:def:classes note, l. 230-234: fixed points derived directly from Def. sr:def:maps(d). All identities checked with sympy (`build/sr_polish/sr_polish_sympy.py`, all OK) | |
| 13 | rigor m5 | Coverage understates where ReviewSanity.lean is used | duplicate of fidelity F4 (fixed) | l. 1114-1116 | |
| 14 | rigor m6 | the "no axiom, no decide" claim covers three Suk modules whose hashes are not pinned | fixed | Sources, l. 36-48: all eight modules of the import closure listed with SHA-256 prefixes (Suk/BaseOrder `d21becd29e84`, Suk/BaseChart `08d0e856f005`, Suk/TriangleOrder `6447cd4833d4` added; closure recomputed from the import lines); Axioms and rigor, l. 63-67: the scan claim (no axiom, sorry, decide, native_decide; re-run with grep) now names these eight modules | |
| 15 | adversarial F1 | Remark sr:rem:variant and Corollary 3 | duplicate of rigor m1 (fixed) | l. 999-1007 | |
| 16 | adversarial F2 | provenance of the H3 chain: (i) the theorem whose hypotheses carry recorded verdicts is `V2L.mirrorExclusionLine_final`; (ii) "written soundness proofs" wrong for H3/V2-L; (iii) distinct `reflLine` constants | fixed | (i) Remark sr:rem:mirror-line, l. 1032-1038: H3's `Mir.mirrorExclusionLine_of_unsat`/`_of_cubes` (Line.lean:139, :147) derive it from unsatisfiability hypotheses; `V2L.mirrorExclusionLine_final` (V2-L/V2L/FinalTree.lean:28) with 1+121+1,198+74,000 CNF facts, recorded cake_lpr verdicts, proofs not retained, file-to-hypothesis step outside Lean (WRITEUP/MIRROR.md §6); (ii) duplicate of fidelity F2; (iii) duplicate of fidelity F1; mirror bullet of sr:rem:records now says "the Lean chain of H3 and V2-L", l. 281 | |
| 17 | adversarial F3 | Remark sr:rem:records omits Lemma H6M (Threefold33), reductions A and B (HalfTurn34), and "two encodings" may suggest independence | fixed | HalfTurn34 bullet l. 253-260 (reductions A and B: written, reviewed in C2P/review, checked at CNF level in AUDIT3; also the Lean-checked orbit bookkeeping, Thm cb:thm:c2, with what stays outside Lean); Threefold33 bullet l. 261-268 (Lemma H6M, C3AUDIT2; also C3PIECES and the Lean-checked cover, Thm cb:thm:c3); Fivefold35 bullet l. 269-273 ("two normal forms of one encoder ... not independent encodings") | |
| 18 | adversarial F4 | notation clash in (P1) | duplicate of fidelity F5 (fixed) | l. 693-695, 708-711 | |
| 19 | adversarial F5 | Coverage "mentioned only in Remarks" | duplicate of fidelity F4 (fixed) | l. 1114-1116 | |
| 20 | adversarial F6 | overfull boxes | duplicate of rigor m3 (fixed) | see row 11 | |
| 21 | adversarial F7 | "A group form is proved in the review file" should say Lean-checked | fixed (same edit as rigor m1) | l. 1002-1004 ("is Lean-checked for Euclidean isometries, with the same five classes as hypotheses") | |
| 22 | adversarial, note under "Points examined" | "accepted by both checkers": lrat-check builds are unsound on the empty-clause path; a caveat would be harmless | fixed (applied) | Remark sr:rem:records, l. 249-251: the project trusts only cake_lpr; where a certificate is said to be accepted by both checkers, cake_lpr accepted it and lrat-check is a secondary check (WRITEUP/SYMMETRIC.md §3, revised 6 Nov); "accepted by two proof checkers" (C4CUT) and "both of the project's proof checkers" (SYM5) reworded accordingly, l. 270, 284 | |
| 23 | claims M1 | statement heads run off the page | duplicate of rigor m3 (fixed); the suggested section-local `\begingroup\sloppy` group was not added, since the preamble now sets a high tolerance in every statement and the 6 remaining boxes were removed by retitling/reordering | see row 11 | |
| 24 | claims M2 | Remark sr:rem:variant: "proved" and Corollary 3 inexact | duplicate of rigor m1 and adversarial F7 (fixed) | l. 999-1007 | |
| 25 | claims M3 | (a) review names under the namespace convention; (b) Mathlib names in Lemma sr:lem:minper lack `Function.` | (a) duplicate of fidelity F3 (fixed); (b) fixed | (b) l. 327-330: `Function.IsPeriodicPt.minimalPeriod_dvd`, `Function.minimalPeriod_eq_one_iff_isFixedPt`, `Function.iterate_minimalPeriod`, `Function.iterate_injOn_Iio_minimalPeriod` (namespace checked in the pinned Mathlib, Mathlib/Dynamics/PeriodicPts/Defs.lean) | |
| 26 | claims M4 | first sentence of sr:rem:records does not fit the H3 route | duplicate of fidelity F2 (fixed) | l. 242-251 | |
| 27 | claims M5 | Fivefold35 "two encodings" can be read as independent; optionally mention that the layer lemma is Lean-checked in LAYERLEAN | main point fixed (with adversarial F3); optional addition declined | l. 269-273 | declined part: the encoder's use of the layer lemma remains a written step, and this section does not check that the LAYERLEAN statement is the form the encoder needs, so the pointer would add an unchecked claim without changing the class's label |
| 28 | claims M6 | Coverage "mentioned only in Remarks" | duplicate of fidelity F4 (fixed) | l. 1114-1116 | |
| 29 | claims M7 | "the Mathlib facts used are restated and proved in Lemmas sr:lem:minper and sr:lem:prim" overclaims | fixed | Coverage, l. 1105-1110 (only the minimal-period and root-of-unity facts are restated there; the isometry theorems are replaced by the proof of Thm sr:thm:structure(a); pigeonhole, least prime factors, square roots and finite-set facts are stated where used) | |
| 30 | writer concerns, overfull list | 6 boxes > 1pt in the full build (lines 319-320, 482-483, 602-604, 894-898, 929-935, 972-973 of the old version) | duplicate of rigor m3 (fixed) | see row 11 | |
| 31 | writer concerns, records | Remark sr:rem:records was not re-verified against the records | fixed | the remark was re-read against the records listed at the top and corrected (rows 2, 7, 16, 17, 22) | |
| 32 | writer concerns, preamble and formatting traps | heads cannot break; `\lean` drops spaces; statement bodies must start with a sentence | no action needed | preamble updated by the orchestrator; no `\lean{...}` with spaces; every statement body starts with a sentence (checked) | |

## Other changes

1. Five statement titles shortened so the unbreakable Lean names fit the line (contract head format kept, Lean
   references unchanged): sr:lem:toC-iso "Isometries in complex coordinates" -> "Isometries in coordinates";
   sr:lem:concyclic "Concyclic points are in convex position" -> "Concyclic points"; sr:thm:main "Reduction to five
   case classes" -> "Main reduction"; sr:thm:variant "Variant without HalfTurn34" -> "Variant"; sr:lem:mirror-line
   "Bridge to MirrorOneAxis33" -> "Bridge". The map has no title column, so only the reordered row of sr:lem:orbitFS
   changed there.
2. `sections/sr.map.tsv`: row sr:lem:orbitFS reordered to match the head (lean_name and file_line columns); note of
   sr:rem:mirror-line updated (conditional on CNF facts via V2L.mirrorExclusionLine_final; identified by text). 46 rows,
   5 columns each; a script check confirms labels, kinds, Lean names and file:line columns equal the heads, in order.
3. Conventions: "(Lean \lean{starRingEnd})" -> "(Mathlib \lean{starRingEnd})", consistent with the new name rule.
4. Dependencies paragraph: now names Theorems cb:thm:c2 and cb:thm:c3 (newly cited in Remark sr:rem:records; both are
   export labels of section cb); "where the two mirror classes are proved" -> "which gives written proofs of the two
   mirror classes".
5. Axioms and rigor: the scan sentence now also states "no sorry" in the eight modules (grep), says the word "axiom"
   occurs there only in comments (case-insensitive grep: Definitions.lean:30 docstring and the main file's module
   docstring), and that an unused declaration is covered by the empty compile log and this scan ("neither the file nor
   these modules add an axiom").
6. Remark sr:rem:records: now says which records it follows; HalfTurn34 bullet notes that the C2P verdicts are those of
   both checkers; Threefold33 bullet adds the 204 indispensable sigma-cube pieces re-solved with retained proofs in
   C3PIECES; Fivefold35 bullet adds the priority of B. C. Dumitru's reported computation (as recorded in SYM5/README.md
   and SYMLEAN/README.md §5); mirror bullet adds the citation of Baek (arXiv:2206.04260) and the label
   "computer-assisted" for the SYMZ confirmations; the phrase "certified record" was replaced by "record with recorded
   checker verdicts".
7. Remark sr:rem:mirror-line: "the unconditional Lean proof" -> "the Lean proof without SAT input"; the unkept `rfl`
   check is reported as "a separate check of both identities by rfl" (no "proved").

## Compile check

`build/sr_wrapper.tex`, two runs of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error sr_wrapper.tex` from
`build/`: exit 0 both times, no error, no "Missing $", no multiply defined label, 0 overfull boxes (target 0).
Undefined references only to other sections' labels: fd:def:{point,orient,gp,cp,ngon,inv,rot},
fd:lem:{collinear,cp-hull,mono}, ar:thm:main, cb:thm:c2, cb:thm:c3, mb:thm:classes, mb:thm:main3 (all contract export
labels). Extra check: the full document (`proofs.tex`, two passes into `build/sr_polish/full/`) has 0 overfull boxes in
the sr part (0 in the whole document), and every reference resolves. Labels: the same 55 labels as the snapshot; all 8
export labels on their statements.
