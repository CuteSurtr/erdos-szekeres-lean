# Diff audit of section `sr`, round doc-r1

Compared: `snapshots/doc-r1-pre/sr.tex` (1,131 lines) and `snapshots/doc-r1-pre/sr.map.tsv` against `sections/sr.tex`
(1,134 lines) and `sections/sr.map.tsv`, with `diff -u`. The `.tex` has 2 hunks. The map has none: `diff` is empty, and
the file still has 47 lines, each with 5 columns. Fixer log: `reviews/sr-doc-r1-fix.md`. It addresses the one note of
`reviews/sr-doc-r0-audit.md` (m1). I also checked that the notes of `reviews/sr-p1-diff.md` (m1, m2) and
`reviews/sr-p1-referee.md` (m1-m4), fixed in round doc-r0, are still fixed in the current file. Paths below are relative
to the staging area, to `RES`, or to the repository root. Line numbers are those of the current `sections/sr.tex`.

**Verdict: PASS.** No blocker, no major and no minor finding.
- Both hunks are correct.
- Every new factual claim is supported by the Lean sources and the records.
- No rigor label is rounded up.
- The one note marked fixed is fixed, and no note was declined.
- No statement environment, label, `\leanref` or map row changed:
  - the list of `\label`s, the list of `\leanref`s and the set of `\ref` targets hash to the same values in the
    snapshot and in the current file;
  - there are 46 environments in both.
- My wrapper compiles with exit 0 and has no overfull box.

## 1. The `.tex` hunks

### Hunk 1: Remark `sr:rem:records`, H3/V2-L route (l. 249-254)

The new text reads:

> The cube covers in that reduction are checked by kernel evaluation (computer-assisted), with one exception: the
> cover of the top two levels of the hull-pair case split of sub-case (ii), where the point of $S$ on the mirror lies
> in the convex hull of the other points (WRITEUP/MIRROR.md §4). That cover is itself given by $1+121$ of those CNF
> facts. What remains outside Lean on this route is described in Remark sr:rem:mirror-line.

I checked each claim.

1. **"Hull-pair case split" is the project's term for this split.**
   - `V2-L/V2L/Main.lean:12`: "the certificates of the hull-pair split of `results/Mii-S`".
   - `Main.lean:40` and `V2-L/V2L/TreeMain.lean:21`: "All certificates of the hull-pair split".
   - `V2-L/V2L/Data.lean:2`: "the hull-pair split (sub-case (ii))".
   - `WRITEUP/MIRROR.md` §4 (l. 231) is titled "The case split of sub-case (ii)". Its cases (U, L) are labelled by the
     mirror pairs that are hull vertices.
2. **The gloss of sub-case (ii) matches the Lean case split exactly.**
   - `H3/MirrorEncoding/Targets.lean:55`, in `mirrorExclusion_of_unsat`, splits on
     `c ∈ convexHull ℝ (↑(S.erase c) : Set Point)`:
     - the interior branch uses `interiorCnf`, which is sub-case (ii);
     - the other branch uses `hullCnf`, which is sub-case (i).
   - `V2L.axisInteriorLine_final` (`V2-L/V2L/FinalTree.lean:18-23`) and `AxisInteriorLine` (`Main.lean:82-85`) have the
     same hypothesis.
   - The `Main.lean` docstring (l. 9-10) says "whose point on that line lies in the convex hull of the other points".
   - `MIRROR.md` §3 calls it "Sub-case (ii), axis point interior".
   - Under general position, "in the convex hull of the other points" and "interior" agree, and the text uses the Lean
     form.
3. **"The point of $S$ on the mirror" is well defined.**
   - In `MirrorOneAxis33` (`SYMLEAN/SymmetricReduction.lean:482-485`), uniqueness is the hypothesis
     `∃ x ∈ S, reflLine a u x = x ∧ ∀ y ∈ S, reflLine a u y = y → y = x`.
   - Definition `sr:def:classes` (l. 230-235) shows that, for a unit u, the fixed points are exactly the points of the
     mirror.
   - On the H3 side, uniqueness follows from |S| = 33 (`exists_mirrorSet`, `Targets.lean:70-73`; the end of Remark
     `sr:rem:mirror-line`).
4. **"Top two levels" and "1+121".**
   - `V2-L/V2L/ClauseCover.lean:69-78`, `not_dimacsSatisfiable_of_clauseCover₂`, has the docstring "Two-level clause
     cover: the first level blocks the cubes `up u` (`u ∈ Us`); below `up u`, the second level blocks the cubes
     `casesOf u`".
   - `TreeMain.lean:29-31` applies it with `hroot` and `hup`.
   - `RootCertificate` (`Main.lean:27-28`) is one CNF fact.
   - `UpCertificates` (`Main.lean:31-33`) ranges over `upTable = upSets.zip upCubes` (`Facts.lean:19`). Both lists have
     length 121 (`Facts.lean:47, 49`, `decide +kernel`).
   - `MIRROR.md` §4 describes the same structure: `root`, then `up:U` for the 121 values of U.
   - So 1+121 is correct, and these two levels are covered by CNF hypotheses, not by kernel evaluation.
5. **"With one exception": every other cube cover on this route is checked by kernel evaluation.**
   - Sub-case (i):
     - `V1-L/V1L/Cover.lean:17`: `hullLeaves_coverCheck : coverCheck hullLeaves = true := by decide +kernel`;
     - it is used in `V1L.hullCnf_unsat_of_leaves` (`V1-L/V1L/Main.lean:39-40`), which
       `mirrorExclusionLine_of_certificatesT` calls (`TreeMain.lean:50`).
   - Sub-case (ii), the case trees:
     - `treeOf_check` (`V2-L/V2L/Trees/Checks.lean:608`);
     - 1,050 per-sibling-list theorems `coverCheck (...) = true := by decide +kernel` in `Trees/N*.lean`;
     - the leaf cases are `decide +kernel` in `Trees/CheckLeaf.lean`;
     - `V2-L/README.md` §9.5 records the same.
   - `native_decide` occurs in `V2-L/V2L`, `V1-L/V1L` and `H3/MirrorEncoding` only in comments that say it is not used.
   - So the only cover that is not kernel-checked is the two-level cover. "(computer-assisted)" for kernel evaluation
     follows contract rule 6, and nothing is rounded up.
6. **Wording and structure.**
   - The old relative clause ("..., which is itself given by ...") became a new sentence. That avoids attaching "which"
     to the glossed noun.
   - "there" became "on this route".
   - The content is unchanged apart from the gloss.
   - "Those CNF facts" still refers back to "the reduction of `Mir.MirrorExclusionLine` to CNF facts" in the preceding
     sentence.

### Hunk 2: Remark `sr:rem:mirror-line` (l. 1051-1053)

"the $1+121$ facts of `hroot` and `hup` are the cover obligations of the top two levels of the hull-pair case split of
sub-case (ii) (Remark sr:rem:records; WRITEUP/MIRROR.md §4)".

- `FinalTree.lean:28-34`: `mirrorExclusionLine_final` has exactly `h1`, `hroot : RootCertificate`,
  `hup : UpCertificates` and `hleaves`. The docstrings (l. 16, 26-27) call `hroot` and `hup` "the 122 cover-obligation
  facts" of sub-case (ii).
- `V2-L/README.md` §9.6 gives the counts: `hroot` 1 CNF, `hup` 121 CNFs.
- The back-reference to `sr:rem:records` points to an earlier remark that holds the gloss (Remark 1.8 against Remark
  1.45 in the PDF). It is a section-internal label, so the Dependencies paragraph (l. 76-82), which lists cross-section
  references, needs no change.
- Correct.

### Lean declarations of the touched remarks, re-read

The anchors are unchanged and still correct:
- `H3/MirrorEncoding/Line.lean`:
  - `:94` `def MirrorExclusionLine`;
  - `:139` `theorem mirrorExclusionLine_of_unsat`;
  - `:147` `theorem mirrorExclusionLine_of_cubes`, with `hc1`, `hc2`;
- `V2-L/V2L/FinalTree.lean:28` `mirrorExclusionLine_final`;
- `SYMLEAN/SymmetricReduction.lean`:
  - `:1052` `MirrorExclusionLineCopy`;
  - `:1056` `mirrorOneAxis33_of_exclusionLine`;
- `SYMLEAN/review/ReviewSanity.lean:1593` `exclusionLine_of_mirrorOneAxis33`.

The neighbouring Definition `sr:def:exclusion-line` and Lemma `sr:lem:mirror-line` were not touched, and they still match
the Lean text. The body of `MirrorExclusionLineCopy` (l. 1053-1054) is byte-identical to `Line.lean:95-96` (`diff`).

## 2. The map

- `diff` is empty.
- The notes of rows `sr:rem:records` and `sr:rem:mirror-line` remain accurate for the edited text.

## 3. The fixer's log

| note | fixer | audit |
|---|---|---|
| doc-r0 audit m1 ("the case split" has no antecedent) | fixed | confirmed (hunks 1 and 2). The gloss of "sub-case (ii)" goes beyond the suggested wording, and it is correct and needed (§1, items 2-3). |
| p1-diff m1 (`affineIsometryOfStrictConvexSpace` is a definition) | fixed in doc-r0 | still in place: l. 569, l. 1124, map note of `sr:thm:structure` |
| p1-diff m2 ("that file") | fixed in doc-r0 | still in place: l. 287-289 |
| p1-referee m1 (H3/V2-L case split; hypothesis count) | fixed in doc-r0 | still in place, now made more precise by this round (l. 249-254, 1049-1053) |
| p1-referee m2 (Threefold33: exhaustiveness of splits; H6M pointer) | fixed in doc-r0 | still in place: l. 273-276 |
| p1-referee m3 (cb theorems labelled computer-assisted) | fixed in doc-r0 | still in place: l. 79-80, 265-266, 271 |
| p1-referee m4 (README §9 against SYMMETRIC.md §3) | fixed in doc-r0 | still in place: l. 255-258 |

No note was declined.

I also checked the factual statements of the log:
- the snapshot sha1 is `a8dff211467f...`;
- the snapshot has no occurrence of "sub-case";
- there are 194 `\ref` occurrences against 193, the extra one pointing to the existing target `sr:rem:records`;
- there are 64 underfull lines;
- `sr.map.tsv` is unchanged.

All of these are true.

## 4. Compile check

- Wrapper `build/sr_docr1audit_wrapper.tex`, with the contract's content. I ran
  `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice from `build/`. Both runs exited with 0, and the
  output has 15 pages.
- No `!` error, no "Missing $", no multiply defined label, and no warning other than undefined references.
- **Overfull boxes: none.**
- 64 underfull lines, none in the changed line ranges (l. 248-258, 1049-1056).
- Undefined references, all allowed:
  - `fd:def:{point,orient,gp,cp,ngon,inv,rot}`;
  - `fd:lem:{collinear,cp-hull,mono}`;
  - `ar:thm:main`, `cb:thm:c2`, `cb:thm:c3`, `mb:thm:classes`, `mb:thm:main3`.
- `pdftotext`:
  - both passages render as intended;
  - `\ref{sr:rem:records}` prints "Remark 1.8" and `\ref{sr:rem:mirror-line}` prints "Remark 1.45";
  - `WRITEUP/MIRROR.md §4` renders correctly.
- Hygiene (grep of `sr.tex` and `sr.map.tsv`):
  - no machine path and no tool name;
  - no `\newcommand`, `\def`, `\usepackage`, `\makeatletter` or `\sloppy`;
  - no "verified" or "certified";
  - the added lines contain no "proved";
  - no added line is longer than 120 characters.

## 5. Findings

None.

## 6. Checked and not reported

- **"sub-case" and "subcase".** The section now uses "sub-case (ii)" (hyphenated, as in `MIRROR.md`) for the mirror route
  and "subcases" (as in the C2 records) for the parallelogram subcases of `HalfTurn34`. They are different objects in
  different bullets, and each follows its record. This is not a source of confusion.
- **"Sub-case (ii)" without "(i)".** The text names sub-case (ii) without naming sub-case (i). The gloss defines (ii) by
  its condition, and the complementary sub-case is implicit. The kernel-checked sub-case (i) cover is covered by "the cube
  covers in that reduction". This is adequate.
- **Remark `sr:rem:mirror-line` attributes `hroot` and `hup` but not `h1` and `hleaves`.** It now says which split
  `hroot` and `hup` belong to, but not that `h1` holds the sub-case (i) leaves and `hleaves` the sub-case (ii) tree
  leaves. The counts are listed in the same order as the hypotheses, and nothing stated is inaccurate. An optional
  parallel attribution would be a style choice, not a correction.
- **No conflict with other sections.** No other section (`mb`, `cb`, `ar`, `ec`, `sa`) describes the H3/V2-L route with
  these counts (grep for `V2-L`, `hroot`, `121`).
