# Section `ll`, polish round 1: fix log

Input: `sections/ll.tex` and `sections/ll.map.tsv` as snapshotted in `snapshots/polish-r1-pre/` (761 lines before, 792 after).
Reports read: `ll-r1-fidelity.md` (F), `ll-r1-rigor.md` (R), `ll-r1-adversarial.md` (A), `ll-r1-claims.md` (C),
`ll-writer-concerns.md` (W). There is only one review round for `ll`. Line numbers in "location" refer to the new `ll.tex`.

Sources re-read for this round: `LAYERLEAN/LayerLemma.lean` lines 1-470 and 1030-1148 (SHA-256 afb8542d..., unchanged),
the three axiom logs, `LEANEXT/review/REPORT.md` and the file list of `LEANEXT/review/`, Mathlib at the pin f897ebcf72
(`Set.extremePoints`, `Convex.mem_extremePoints_iff_convex_diff`, `extremePoints_convexHull_subset`,
`IsCompact.extremePoints_nonempty` ("Krein-Milman lemma"), `closure_convexHull_extremePoints` ("Krein-Milman theorem"),
`Nat.iterate`, `Function.iterate_succ'`, `Function.iterate_add`), `C6UPPER/README.md`, `C7UPPER/README.md`,
`WRITEUP/note/k8_soundness.tex` (head, Section "cube cover and passage to geometry", trust table, gaps (G1)-(G4) and
trust items (E1)-(E6)), `ENCBLEAN/geo/ES8Geo/Main.lean`, `ENCBLEAN/EncB/Cover.lean:101-121`,
`ENCBLEAN/geo/ES8Geo/Capstone2.lean` (lines 45-1155 are byte-identical to `LayerLemma.lean` lines 37-1147, checked with
diff; `def Sixfold66` at line 1110 is its only definition in `ENCBLEAN/geo`; import chain Main -> ModelOfLabelling ->
Labelling -> Interface -> Capstone2), `ENCBLEAN/geo/ErdosSzekeres/Definitions.lean` (same SHA-256 2425500e... as the
repository's), and a grep of all `.lean` files of the repository for `Sixfold66`/`Sevenfold70`.

## Findings

| report + id | summary | action | location after the fix | reason (if declined) |
|---|---|---|---|---|
| F M1 | "no Lean theorem proves (H) for any m,t" is overbroad | fixed: now "no theorem of `LAYERLEAN/LayerLemma.lean` proves it; in the two applications below it is supplied by Sixfold66 and Sevenfold70, which are themselves hypotheses (Remark ll:rem:hyp)" | ll.tex 622-625 | |
| F M2 | "seven @[simp] lemmas ... used inside printed theorems" unverified (ofC_zero, ofC_one) | fixed: usage claim removed; the text now says they are printed in none of the three logs and describes their proofs (rfl; Complex.ext / funext; toC_crot via toC_ofC, lines 236-255); the conclusion about sorryAx/ofReduceBool/project axioms now follows the file scan | ll.tex 35-46 | |
| F M3 | Coverage/map say Lean proofs of (b)-(d) "use Krein-Milman"; (b) does not | fixed: Coverage now "two Mathlib facts on extreme points for (b), the Krein-Milman theorem for (c) and the Krein-Milman lemma for (d)"; proof paragraph names the Krein-Milman lemma for (d); map note of ll:lem:hv updated | ll.tex 199-203, 763-766; map row ll:lem:hv | |
| F M4 | intro: "hull vertices form a single f-orbit" false for S empty | fixed: "for every hull vertex x of S the hull vertices of S are exactly x, f(x), ..., f^{m-1}(x), so that, if S is nonempty, they form a single f-orbit" | ll.tex 8-12 | |
| F M5 | "review ... of the same file": axioms printed from an unkept copy | fixed: the sentence now says the report `LEANEXT/review/REPORT.md` names the file by SHA-256 afb8542d..., that the check file from which the axioms were printed is not kept in the record, and that the identification rests on the report (checked: the kept `tests_tail.lean` and `VacuityTest.lean` contain only 5 `#print axioms` lines each, for `Review.*` tests) | ll.tex 38-41 | |
| F M6 | overfull boxes (up to 149pt) in multi-reference heads | fixed: the preamble's new statement tolerance removed all but 3; those 3 heads were shortened (see "other changes" 1). Standalone build: 0 overfull boxes of any size; full-document build: 0 overfull boxes in the log range of `sections/ll.tex` | heads at ll.tex 303, 430, 464 | |
| R M1 | heads run off the page (35 overfull hboxes) | duplicate of F M6 | as F M6 | |
| R M2 (first part) | Coverage and map note: Lean's (b) does not use Krein-Milman | duplicate of F M3 | as F M3 | |
| R M2 (second part) | Mathlib criterion quoted without "x in C" | fixed: "x is an extreme point of a convex set C iff x in C and C minus {x} is convex" (matches `Convex.mem_extremePoints_iff_convex_diff` at the pin); also names the second fact used (extreme points of conv(S) lie in S) | ll.tex 199-201 | |
| R M3 | (C2) gives f^{i+1}=f o f^i as Lean's definition; Lean's `Nat.iterate` uses f^{i+1}=f^i o f | fixed: (C2) now states Lean's defining recursion, that both recursions give the same maps (Mathlib `Function.iterate_succ'`), and f^{i+j}=f^i o f^j (`Function.iterate_add`) | ll.tex 68-72 | |
| R M4 | Remark ll:rem:hyp omits gaps (G1)-(G4) of k8_soundness and the H(1) unit of encoder A | fixed: the remark now lists (G1)-(G4) in one clause each, says one C7UPPER encoding carries an added symmetry-breaking unit clause, and that the written soundness proof also covers the symmetry breaking and the cube cover | ll.tex 719-729 | |
| R M5 | (H) sentence unverified and too strong | duplicate of F M1 | as F M1 | |
| R M6 | intro S empty | duplicate of F M4 | as F M4 | |
| R M7 | "review of the same file" rests on REPORT.md | duplicate of F M5 | as F M5 | |
| R M8 | "every statement whose head names a Lean declaration is Lean-checked" also covers definitions | fixed: restricted to lemmas and theorems; Lemma ll:lem:rot(b) (def `rotAff`) explained; definitions "restate Lean definitions, which the same build type-checks; being definitions, they are not Lean-checked claims"; Definition ll:def:66-70 only introduces Sixfold66/Sevenfold70, which are not proved | ll.tex 46-52 | |
| A m1 | heads run off the page | duplicate of F M6 | as F M6 | |
| A m2 | typo in (C7): "For m in N the subtraction t-1" | fixed: "For t in N" | ll.tex 105 | |
| A m3 | Krein-Milman summary inconsistent | duplicate of F M3 | as F M3 | |
| A m4 | (H) overgeneralisation | duplicate of F M1 | as F M1 | |
| A m5 | Remark ll:rem:hyp: (i) gaps (G1)-(G4); (ii) ENCBLEAN's hypothesis CubesUnsat64 concerns the Lean definition EncB.encB 6 8 11, linked to the files and verdicts only by (E1)-(E6); its Sixfold66 is the verbatim copy in Capstone2.lean:1110 | (i) duplicate of R M4; (ii) fixed: the remark names `EncB.Geo.sixfold66_of_cubes64`, says its Sixfold66 is that of `ENCBLEAN/geo/ES8Geo/Capstone2.lean` (verbatim copy of this file's declarations, over a byte-identical `ErdosSzekeres/Definitions.lean`), that `EncB.CubesUnsat64` is the unsatisfiability of the 64 cube formulas built from the Lean definition `EncB.encB`, and that the identity of their printed texts with the cube files carrying the cake_lpr verdicts, and the reading of those verdicts, are not Lean-checked but rest on (E1)-(E6) under gap (G2) | ll.tex 729-737 | |
| A m6 | intro S empty | duplicate of F M4 | as F M4 | |
| A m7 | (C4) asks only x1 = x while "Mathlib asks x1 = x and x2 = x" | fixed (clarification): at the pinned Mathlib f897ebcf the definition asks only x1 = x, so (C4) is literally Mathlib's; added "This is Mathlib's definition at the pinned revision (with x in the open segment between x1 and x2); exchanging the roles of x1 and x2 shows that then also x2 = x" | ll.tex 88-91 | |
| A m8 | blanket "Lean-checked" sentence covers Definition ll:def:66-70 | duplicate of R M8 | as R M8 | |
| A section 5 (not settled) | identity of the file behind `LEANEXT/review/axioms.log` rests on REPORT.md | duplicate of F M5 | as F M5 | |
| C m1 | heads clipped in the PDF | duplicate of F M6 | as F M6 | |
| C m2 | @[simp] lemmas "used inside printed theorems" unverified; nit: "each depends only on these three axioms" ambiguous | duplicate of F M2; nit fixed: now "it reports the same three axioms for each printed theorem, except that iterate_mem depends only on propext and Quot.sound" | ll.tex 37-38 | |
| C m3 | Remark ll:rem:hyp: gaps (G1)-(G4) and the ENCBLEAN qualification | duplicate of R M4 (gaps) and A m5 (ENCBLEAN) | as R M4, A m5 | |
| C m4 | Krein-Milman in Coverage and map note | duplicate of F M3 | as F M3 | |
| C m5 (claim 1) | blanket rigor sentence covers definitions | duplicate of R M8 | as R M8 | |
| C m5 (claim 2) | "for each we say whether it follows the Lean proof" not true for ll:lem:hv-basic, ll:lem:peel-basic | fixed: both proofs now start "As in Lean:" (checked: `mem_hullVerts` unfolds the filter, `hullVerts_subset` uses it, `peel_succ` is `rfl`, `peel_subset` is the same induction); the sentence now reads "for each statement that corresponds to a Lean declaration" (the written step ll:cor:decomp has no Lean proof) | ll.tex 52-54, 182, 495 | |
| C m6 | `$mt$` in section title gives hyperref "Token not allowed" warnings | fixed: `\texorpdfstring{$mt$}{mt}` (hyperref command, no new macro) in the section title and the subsection title; no such warning remains | ll.tex 1, 609 | |
| W concern 1 | 35 overfull boxes in heads, preamble fix proposed | duplicate of F M6 | as F M6 | |
| W concern 2 | `\lean{}` ignores spaces; `\texttt{}` used for expressions with spaces | declined | - | no inaccuracy; the section already sets such expressions with `\texttt` (checked in the PDF) |
| W concern 3 | rotAbout_iterate covered here though not named in the scope list | declined | - | coverage is correct and in range; the Coverage wording about where it is used was made precise (other change 3) |
| W concern 4 | ll:cor:decomp is not an export label | declined | - | no inaccuracy; the export list is fixed by the contract and the corollary is labelled as a written step |
| W concern 5 | sixfold proof cites lg:lem:centre and includes the argument | declined | - | no inaccuracy (the hypotheses supplied match lg's statement and Lean line 582) |
| W concern 6 | proofs of (b)-(d) differ from "Lean's Krein-Milman route" | duplicate of F M3 | as F M3 | |
| W concern 7 | Remark ll:rem:hyp summarised from READMEs, not re-derived | fixed together with R M4 and A m5: every claim of the remark was checked against C6UPPER/README.md, C7UPPER/README.md, k8_soundness.tex and ENCBLEAN (see "Sources re-read") | ll.tex 708-744 | |
| W overfull list | 15.5pt (417-419), 18.7pt (451-453), 50.3pt (290-292) in the full-document build | duplicate of F M6 (these are the three heads shortened) | ll.tex 303, 430, 464 | |

## Other changes

1. Short names of three statement heads (layout only; statements, labels and Lean references unchanged):
   Lemma ll:lem:inv-sdiff "removing the hull vertices keeps invariance" -> "invariance of $S\setminus\hv(S)$";
   Lemma ll:lem:erase "removing the centre keeps invariance" -> "invariance of $S\setminus\{c\}$";
   Theorem ll:thm:core-rot "layer lemma, rotation form" -> "layer lemma, rotations".
2. Sources paragraph (line 22): the treated line range was "1--465 and 1037--1147"; `rotAbout_iterate` occupies lines
   465-469 and the part with `card_peel` starts at line 1034 (section header) and ends at 1148, so it is now
   "1--469 and 1034--1148" (consistent with "lines 471--1032" for the other sections).
3. Coverage (lines 791-792): "is used in Theorem ll:thm:sixfold" -> "Step 2 of our proof of Theorem ll:thm:sixfold uses
   it" (the Lean proof of `sixfold_octagon` calls `centre_not_mem_of_even`, not `rotAbout_iterate`).
4. Remark ll:rem:hyp, first paragraph: "they do not appear in the axiom lists, since ..." reworded to "Theorems ... take
   them as explicit hypotheses, so they do not enter the axiom lists of these theorems"; added, to support the phrase
   "not proved in Lean" used in the introduction, Definition ll:def:66-70 and Theorems ll:thm:sixfold/ll:thm:sevenfold:
   "Among the Lean files of the repository, the only theorems whose conclusion is Sixfold66 are in
   `ENCBLEAN/geo/ES8Geo/Main.lean` and take further hypotheses (see below), and no theorem has the conclusion
   Sevenfold70" (checked by grep over all `.lean` files: `sixfold66_of_no_model`, `sixfold66_of_unsat`,
   `sixfold66_of_cubes64`, each with a hypothesis; no theorem concludes Sevenfold70).
5. Remark ll:rem:hyp, second paragraph: "SAT encodings of eleven nested regular hexagons" made precise as "SAT encodings
   of octagon-free configurations of eleven nested regular hexagons in general position" (likewise for C7UPPER, "of the
   same kind for ten nested regular heptagons"), matching the statements of C6UPPER/C7UPPER; "supplied" -> "supported";
   the rigor label `certificate` is attached to the unsatisfiability results only, and the written proof keeps its
   label "written proof, not refereed".
6. Lean-evidence paragraph reordered so that "So no statement of this section depends on sorryAx, ..." follows all its
   premises (the logs, the proofs of the unprinted @[simp] lemmas, the source scan); the `rotAff` clause says "a proof
   obligation discharged inside the definition" (rigor vocabulary: no "proved" for anything beyond Lean-checked).
7. Map TSV: notes of `ll:lem:hv` (which Mathlib results the Lean proofs of (b), (c), (d) use) and `ll:rem:hyp` (not
   proved in Lean; certificate + written soundness proof, not refereed, gaps G1-G4; ENCBLEAN route assumes
   EncB.CubesUnsat64, trust items E1-E6) updated. No row added or removed (31 rows, 5 columns); labels, kinds, Lean
   names and file:line unchanged.

No statement body, hypothesis or conclusion was changed; no label was added, removed or renamed (label sets of old
and new file identical); every export label is still defined on its statement.

## Compile check

`build/ll_wrapper.tex` (contract wrapper), `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice from
`build`: both passes exit 0; no `!` error, no "Missing", no undefined control sequence, no "Label(s) may have changed",
no hyperref token warning. Undefined references: only `fd:def:cp`, `fd:def:gp`, `fd:def:inv`, `fd:def:ngon`,
`fd:def:point`, `fd:def:rot`, `fd:lem:affine-cp`, `fd:lem:collinear`, `fd:lem:cp-hull`, `fd:lem:mono`,
`lg:lem:centre`, `lg:thm:nesting` (all allowed). Overfull boxes > 1pt: 0 (0 of any size; 3 before this round).
A full-document build of `proofs.tex` into a private output directory also shows 0 overfull boxes in the log range of
`sections/ll.tex`. Mechanical checks: no machine path, tool name, `\newcommand` or `\usepackage` in
`ll.tex` or `ll.map.tsv`; 31 statement environments = 31 map rows; 21 proofs.
