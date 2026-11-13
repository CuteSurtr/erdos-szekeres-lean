# Section `sr`, round doc-r1: fixer log

Input: `reviews/sr-doc-r0-audit.md` (verdict PASS; no blocker or major finding; one minor note, m1). Snapshot before
editing: `snapshots/doc-r1-pre/sr.tex`, `snapshots/doc-r1-pre/sr.map.tsv` (sha1 of `sr.tex` `a8dff211...`, equal to the
live file at snapshot time). Paths of records are relative to `RES`; line numbers are those of the edited
`sections/sr.tex` (1,134 lines; 1,131 before).

The note was checked against the cited sources and found correct; it is fixed. Only two remarks changed. No statement
environment, label, `\leanref` or map row changed, so no Lean-faithfulness question arises. The Lean declarations that
the changed sentences describe were re-read (below).

## Note

| # | lens | summary | action | location | evidence checked / reason |
|---|---|---|---|---|---|
| 1 | diff m1 | "the top two levels of the case split" has no antecedent: the H3/V2-L route has two cube splits, the 1,198-leaf binary partition of sub-case (i) and the hull-pair split of sub-case (ii); only the second is meant | fixed | Remark `sr:rem:records`, l. 250-254; Remark `sr:rem:mirror-line`, l. 1051-1053 | See "Sources re-read". New text in `sr:rem:records` (first use): "The cube covers in that reduction are checked by kernel evaluation (computer-assisted), with one exception: the cover of the top two levels of the hull-pair case split of sub-case (ii), where the point of $S$ on the mirror lies in the convex hull of the other points (WRITEUP/MIRROR.md §4). That cover is itself given by $1+121$ of those CNF facts. What remains outside Lean on this route is described in Remark sr:rem:mirror-line." New text in `sr:rem:mirror-line`: "the $1+121$ facts of hroot and hup are the cover obligations of the top two levels of the hull-pair case split of sub-case (ii) (Remark sr:rem:records; WRITEUP/MIRROR.md §4)." |

### Differences from the suggested wording

1. **Gloss of "sub-case (ii)".** The section never defined "sub-case (ii)" (grep of the snapshot for `sub-case`, `axis
   point`, `hull vertex`: no hit). Adding the auditor's phrase alone would have moved the missing antecedent from "the
   case split" to "sub-case (ii)". So the first use adds "where the point of $S$ on the mirror lies in the convex hull
   of the other points". This is the hypothesis `c ∈ convexHull ℝ (↑(S.erase c) : Set Point)` of
   `V2L.axisInteriorLine_final` (`V2-L/V2L/FinalTree.lean:18-23`, the sub-case (ii) theorem), the wording of the
   `V2-L/V2L/Main.lean` docstring (l. 9-10: "whose point on that line lies in the convex hull of the other points"),
   and "Sub-case (ii), axis point interior" of `WRITEUP/MIRROR.md` §3. The point is unique: for 33 points exactly one
   lies on the mirror, as the end of Remark `sr:rem:mirror-line` shows; in `MirrorOneAxis33` this is a hypothesis.
2. **Sentence split.** The old sentence ended "..., which is itself given by $1+121$ of those CNF facts". With the gloss
   that "which" could attach to the wrong noun, so the sentence now reads "with one exception: ... . That cover is
   itself given by ...". "What remains outside Lean there" became "... on this route", because "there" was now two
   sentences away from "On the route through H3 and V2-L".
3. **Second use.** In `sr:rem:mirror-line` the same phrase is used (the audit's optional suggestion), with a pointer back
   to Remark `sr:rem:records` for the gloss and to `WRITEUP/MIRROR.md` §4 for the split. The gloss is not repeated.

### Sources re-read

- `WRITEUP/MIRROR.md` §4 is titled "The case split of sub-case (ii)". Its "122 obligations" are `root` (F + {¬UP(U)} is
  UNSAT; one fact) and `up:U` for each of the 121 values of U (F + UP(U) + {¬cube(U, L)} is UNSAT). These are the two
  top levels: every model of F satisfies some UP(U), and then some cube(U, L).
- `V2-L/V2L/Main.lean`:
  - l. 12 and 40 call this split "the hull-pair split"; `V2-L/V2L/Data.lean:2` says "the hull-pair split
    (sub-case (ii))". So "hull-pair case split" is the project's own term.
  - l. 27-28: `RootCertificate := ¬DimacsSatisfiable (interiorCnf 33 7 ++ upCubes.map negClause)`.
  - l. 31-33: `UpCertificates := ∀ p ∈ upTable, ¬DimacsSatisfiable (cubeCnf (interiorCnf 33 7) p.2 ++ (casesOf p.1).map negClause)`.
- `V2-L/V2L/Facts.lean:19,47,49`: `upTable := upSets.zip upCubes`, both of length 121 (`decide +kernel`). So
  1+121 is correct.
- `V2-L/V2L/FinalTree.lean:28-34`: `mirrorExclusionLine_final` has exactly the hypotheses `h1` (sub-case (i) leaves),
  `hroot`, `hup`, `hleaves`. Its proof is `mirrorExclusionLine_of_certificatesT` applied to `treeOf_check`. The
  docstring (l. 26-27) attributes `h1` to sub-case (i) and the 122 cover-obligation facts and the tree leaves to
  sub-case (ii).
- The covers below the top two levels are kernel-checked:
  - `V1-L/V1L/Cover.lean:17` `hullLeaves_coverCheck : coverCheck hullLeaves = true := by decide +kernel` and `:19`
    `hullLeaves_length : ... = 1198`: sub-case (i);
  - `V2-L/V2L/Trees/Checks.lean:608` `treeOf_check`, and `V2-L/README.md` §9.1 and §9.5: the case trees of
    sub-case (ii).
  So the "one exception" is exactly the two-level cover given by `hroot` and `hup`.
- The unchanged anchors in the touched remark still hold:
  - `H3/MirrorEncoding/Line.lean:94` `def MirrorExclusionLine`;
  - `:139` `theorem mirrorExclusionLine_of_unsat`;
  - `:147` `theorem mirrorExclusionLine_of_cubes`, with `hc1`, `hc2` on l. 148;
  - `V2-L/V2L/FinalTree.lean:28` `theorem mirrorExclusionLine_final`.

No claim of the remarks changed in substance. The rigor wording stays as it was: kernel evaluation is
"computer-assisted", and the 1+121 facts are "CNF facts" given as hypotheses, not presented as proved.

## Checks

- **Compile.** `build/sr_wrapper.tex`, two runs of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` from
  `build/`:
  - exit 0 both times; 15 pages;
  - no `!` error, no "Missing $", no multiply defined label, no warning other than undefined references;
  - **overfull boxes: 0**; underfull lines: 64, the same as in round doc-r0.
  - Undefined references, all allowed: `fd:def:{point,orient,gp,cp,ngon,inv,rot}`, `fd:lem:{collinear,cp-hull,mono}`,
    `ar:thm:main`, `cb:thm:c2`, `cb:thm:c3`, `mb:thm:classes`, `mb:thm:main3`. The new `\ref{sr:rem:records}`
    resolves (Remark 1.8).
- **Rendering.** `pdftotext`: both passages render as intended. `WRITEUP/MIRROR.md §4` is set by `\dirn`, and "the
  point of S on the mirror" is in math italics.
- **Invariants against the snapshot.** These hash to the same values in `snapshots/doc-r1-pre/sr.tex` and
  `sections/sr.tex`:
  - the list of `\label`s;
  - the list of `\leanref`s;
  - the set of `\ref` targets.
  The environment count is 46 in both. The only new `\ref` (194 against 193) points to `sr:rem:records`, which was
  already a target. `sr.map.tsv` is unchanged (`diff` empty; 47 lines, all with 5 columns).
- **Hygiene** (grep of `sr.tex` and `sr.map.tsv`):
  - no machine path and no tool name;
  - no `\newcommand`, `\def`, `\usepackage`, `\makeatletter` or `\sloppy`;
  - no "verified" or "certified"; the added text contains no "proved";
  - no changed source line is longer than 120 characters.
