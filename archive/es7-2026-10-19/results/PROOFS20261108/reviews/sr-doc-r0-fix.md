# Section `sr`, round doc-r0: fixer log

Input: the six minor notes under key `sr` of `build/open_minors.json` (from `reviews/sr-p1-diff.md` m1, m2 and
`reviews/sr-p1-referee.md` m1-m4). Snapshot before editing: `snapshots/doc-r0-pre/sr.tex`, `snapshots/doc-r0-pre/sr.map.tsv`.
Paths of records are relative to `RES`; line numbers are those of the edited `sections/sr.tex`.

All six notes were checked against the cited sources and found correct; all six are fixed. No statement environment, no
label and no Lean reference was changed. No statement text changed, so no Lean-faithfulness question arises; the
statement of Theorem `sr:thm:structure` (whose proof was edited) was re-read against
`SYMLEAN/SymmetricReduction.lean:321` and `:869` before and after the edit and is unchanged (diff empty).

## Notes

| # | lens | summary | action | location | evidence checked / reason |
|---|---|---|---|---|---|
| 1 | diff m1 | `Isometry.affineIsometryOfStrictConvexSpace` is called a "theorem"; it is a `noncomputable def` (a construction) whose underlying map is the given isometry | fixed | proof of Thm `sr:thm:structure`(a), l. 565-569; Coverage l. 1120-1122; map note of `sr:thm:structure` | Pinned Mathlib (rev `f897ebcf72cd`) `Mathlib/Analysis/Convex/StrictConvexBetween.lean:138` is `noncomputable def affineIsometryOfStrictConvexSpace`, `coe_affineIsometryOfStrictConvexSpace` (l. 149) is `rfl`; the docstring says only the codomain is strictly convex and surjectivity is not needed. `linear_isometry_complex` (`Mathlib/Analysis/Complex/Isometry.lean:130`) is a theorem. Proof text now: "Mathlib's construction of an affine isometry from an isometry between real normed affine spaces with strictly convex codomain (..., a definition whose underlying map is the given isometry; it is a result of Mazur-Ulam type that does not need surjectivity), and then Mathlib's theorem describing the real-linear isometric equivalences of C". Coverage: "the Mathlib results on isometries that the Lean proof uses (the construction ... and the theorem ...)". Map note: "written proof of part (a) by an elementary argument instead of the Mathlib results used in Lean (a construction and a theorem)". |
| 2 | diff m2 | "the classes of that file" in the mirror bullet reads as `SymmetricReduction.lean` | fixed | Remark `sr:rem:records`, mirror bullet, l. 285-288 | Re-checked: `diff` of `SYMLEAN/mirror/ReductionThreeClasses.lean` l. 38-1084 against `SYMLEAN/SymmetricReduction.lean` l. 12-1058 is empty; the imports of the former (l. 1-13) exclude the latter; `namespace ErdosSzekeres.SymReduction` (l. 80) is inside the copied range. Both files are now named in full: "Its lines 38--1084 are byte-identical to lines 12--1058 of SYMLEAN/SymmetricReduction.lean, so the classes defined in SYMLEAN/mirror/ReductionThreeClasses.lean are copies ...". |
| 3 | referee m1 | H3/V2-L route: "the case split [is] Lean-checked" is imprecise (the top two levels of the split are covered by CNF hypotheses); the count "1+121+1,198+74,000 hypotheses" counts instances, not the four Lean hypotheses | fixed | Remark `sr:rem:records`, l. 249-253; Remark `sr:rem:mirror-line`, l. 1045-1052 | `V2-L/V2L/FinalTree.lean:28-33`: hypotheses `h1`, `hroot : RootCertificate`, `hup : UpCertificates`, `hleaves`; docstring and `V2-L/README.md` 9.6 call `hroot`, `hup` "the 122 cover-obligation facts"; `WRITEUP/MIRROR.md` 4 ("Completeness, certified without geometry (the 122 obligations)") and 6 (`RootCertificate`, `UpCertificates`; `coverCheck hullLeaves` and `treeOf_check` by `decide +kernel`). New text in `sr:rem:records`: the soundness of the encodings and the reduction of `Mir.MirrorExclusionLine` to CNF facts are Lean-checked; the cube covers in that reduction are checked by kernel evaluation (computer-assisted), except the cover of the top two levels of the case split, which is itself given by 1+121 of those CNF facts. New text in `sr:rem:mirror-line`: "Lean-checked with four hypotheses, h1, hroot, hup and hleaves, which together assert 1,198+1+121+74,000 facts ...; the 1+121 facts of hroot and hup are the cover obligations of the top two levels of the case split. Each fact has a recorded cake_lpr verdict ...". |
| 4 | referee m2 | Threefold33 bullet omits the written exhaustiveness of the layer and sigma-splits; "Lemma H6M (C3AUDIT2)" points to the check, not the written lemma | fixed | Remark `sr:rem:records`, Threefold33 bullet, l. 271-275 | `C3LEAN/README.md` status paragraph ("That the splits are exhaustive ... are written proofs, reviewed, not Lean-checked") and 6 (Lemmas 1-4 and the cover theorem of `C3-S/soundness.md`, its version for the reduced cut in `C3H6M/soundness_h6m.md`, rules 2 and 3 of `C3U2/sigma_split.md`); `C3H6M/soundness_h6m.md` l. 1-26 (the written Lemma H6M, following `C3AUDIT2/REPORT.md` 1); `C3AUDIT2/REPORT.md` title "adversarial check of Lemma H6M". New text: "the written Lemma H6M (C3H6M/soundness_h6m.md, checked adversarially in C3AUDIT2); on the written exhaustiveness of the layer splits and sigma-splits (Lemmas 1--4 and the cover theorem of C3-S/soundness.md, its version for the reduced cut in C3H6M/soundness_h6m.md, and rules 2 and 3 of C3U2/sigma_split.md)". Now consistent with Remark `mb:rem:main3`. |
| 5 | referee m3 | `cb:thm:c2`, `cb:thm:c3` called "Lean-checked bookkeeping/cover" while section cb labels them computer-assisted | fixed | Dependencies l. 79-80; HalfTurn34 bullet l. 263-264; Threefold33 bullet l. 269-270 | `sections/cb.tex` heads: `cb:thm:c3` "(Computer-assisted: ...)", `cb:thm:c2` "(Computer-assisted.)"; Lean: `C2FINAL/Central34Orbits.lean:291` `all_cases_closed ... := by decide +kernel`; `C3LEAN/C3Cover.lean` "proves, by kernel evaluation (`decide +kernel`, no `native_decide`)". All three places now say "Lean-checked by kernel evaluation and so computer-assisted". |
| 6 | referee m4 | Remark cites `SYMLEAN/README.md` 9, which still lists lrat-check and cake_lpr as trusted, while it follows the 6 Nov revision of `WRITEUP/SYMMETRIC.md` 3 | fixed | Remark `sr:rem:records`, l. 253-256 | `SYMLEAN/README.md:316` "the checkers lrat-check and cake_lpr are (`WRITEUP/SYMMETRIC.md` 3)"; `WRITEUP/SYMMETRIC.md:231` "Revised 6 November 2026: lrat-check ... is a secondary check only and not part of the trust base"; the README was last changed on 2 November, `SYMMETRIC.md` on 6 November. New text: "(WRITEUP/SYMMETRIC.md 3, revised on 6 November 2026). The trust statement in 9 of SYMLEAN/README.md, which this remark follows on other points, predates that revision and still lists both checkers as trusted." |

## Other changes

1. Remark `sr:rem:mirror-line`, l. 1044-1045: `Mir.mirrorExclusionLine_of_cubes` (`H3/MirrorEncoding/Line.lean:147`) also
   takes two hypotheses `coverCheck C1 = true`, `coverCheck C2 = true`; the sentence "derive ... from hypotheses saying
   that certain CNF formulas are unsatisfiable" now adds "(the second also from two hypotheses that the Boolean cover
   check `coverCheck` of a cube list returns `true`)". This was noted, but not reported, in `reviews/sr-p1-diff.md`
   section 6; it sits in the sentence next to the note-3 fix.
2. Three source lines re-wrapped to the file's line width (no change of text).

## Checks

- Compile: `build/sr_wrapper.tex`, two runs of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` from
  `build/`: exit 0 both times; no `!` error, no "Missing $", no multiply defined label; overfull boxes: 0; underfull
  lines 64 (65 before; none new in the changed text); 15 pages. Undefined references only to
  `fd:def:{point,orient,gp,cp,ngon,inv,rot}`, `fd:lem:{collinear,cp-hull,mono}`, `ar:thm:main`, `cb:thm:c2`,
  `cb:thm:c3`, `mb:thm:classes`, `mb:thm:main3` (all allowed).
- Labels: the list of `\label`s is identical to the snapshot. Map: 46 rows for 46 environments, labels and kinds in the
  same order; only the note of `sr:thm:structure` changed; every row has 5 columns.
- Hygiene: no machine path and no tool name in `sr.tex` or `sr.map.tsv`; no `\newcommand`, `\def`,
  `\usepackage`, `\makeatletter` or `\sloppy`; no "verified" or "certified"; "proved" occurs only for this section's
  written proofs, in "none is proved in this section", and in the Lean names `mirrorOneAxis33_proved`,
  `mirrorNoAxis34_proved`.
