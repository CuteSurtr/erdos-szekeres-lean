# Section `ar` (Affine symmetries), whole-document review round 1: recheck of the fix

**Verdict: pass.** All three assigned findings are resolved correctly. The fix introduces no blocker, major or minor
problem. There is one minor finding, m1. It is older than this fix and was not among the findings assigned to `ar` in
this round: claims-review F11 names ar's Coverage paragraph, and no fixer has handled it. It is reported here so that it
gets routed. It does not affect the verdict.

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`, `tools/`) or to RES (Lean sources and
records). `ar.tex:N` refers to the current file.

## Inputs

- Fix log: `reviews/docfix-ar-r1-fix.md` (3 findings, 3 fixed, 0 declined).
- Before: `snapshots/docfix-r1-pre/ar.tex` (SHA-256 `4172a12b50ad`..., 807 lines), `snapshots/docfix-r1-pre/ar.map.tsv`
  (`2b8e9d4786b3`...).
- After: `sections/ar.tex` (`5da35be91e55`..., 812 lines), `sections/ar.map.tsv` (`af2b7f26447b`...). These hashes
  match the ones in the log.

## 1. The three assigned findings

### 1. xref-srarcbsa, finding 2 (minor): the mirror theorems prove copies of the classes. Resolved.

The new text is at ar.tex:717-720 in the first bullet of `ar:rem:classes`. It says that the two theorems are about the
copies of the class definitions in `SYMLEAN/mirror/ReductionThreeClasses.lean` (RTC). It says that RTC does not import
`SYMLEAN/AffineReduction.lean` (AR), and that RTC lines 38-1559 are byte-identical to AR lines 12-1533. So the two
theorems discharge `hm1` and `hm0` of `ar:thm:main` only through the identity of the two texts.

Each claim was checked against the sources:
- **Imports.** RTC's imports are at lines 1-13. They are the eleven imports of AR plus `ErdosSzekeres.Omission.BaekGeometry`
  and `ErdosSzekeres.ConvexCycleCuts`. AR is not among them, so the claim is true.
- **Byte identity.** `sed -n 38,1559p` of RTC and `sed -n 12,1533p` of AR give identical output under `cmp`. Both
  extracts have SHA-256 `f4fed1411fb9`.... AR has exactly 1533 lines. Its `namespace ErdosSzekeres.SymReduction`
  (AR:54) and the matching `end` (AR:1533) lie inside the copied range, so the copies have the same full names. The
  copied classes are at RTC:508 and RTC:514, that is AR:482 and AR:488 shifted by 26.
- **Line numbers.** `mirrorOneAxis33_proved : MirrorOneAxis33` is at RTC:4274 and `mirrorNoAxis34_proved : MirrorNoAxis34`
  at RTC:4282. Both lie in namespace `ErdosSzekeres.SymReduction`.
- **Axioms.** `SYMLEAN/mirror/axioms.out` gives `[propext, Classical.choice, Quot.sound]` for both theorems.
- **The premises.** All five theorems of `ar:thm:main` (AR:1477, 1489, 1501, 1510, 1521) have the binders
  `(hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)`, which refer to AR's constants. The new sentence names these premises
  correctly.
- **Consistency.** The text agrees with `sr:rem:records` (sr.tex:284-290) and with mb's paragraph "Copies of the same
  code" (mb.tex:89-94), which give the same ranges and the same claim about imports.
- **Reading.** In the next sentence, "Their axioms log" now refers to "the two theorems". That reading is correct.

### 2. consistency m18 (minor): bold paragraph heads. Resolved.

- `\textbf` was removed from all eight heads. In the current file these are at ar.tex:25, 44, 81, 91, 109, 120, 127 and
  771. The head texts are unchanged.
- `grep 'paragraph{\textbf'` finds nothing in any section.
- `preamble.tex` does not redefine `\paragraph`.
- Rendered page 1 of the wrapper shows normal-weight run-in heads ("Sources.", "Rigor and axioms."), like those of the
  other sections.

### 3. claims F4 (major): the unconditional statement given this document's label. Resolved.

The old sentence was "The unconditional form of Theorem ar:thm:main is therefore computer-assisted, and it is not
Lean-checked as a whole." It is gone. The new text is at ar.tex:753-756:

> The unconditional statement, Theorem ar:thm:main without its five hypotheses, is claimed in the project as
> computer-assisted (Theorem A of WRITEUP/SYMMETRIC.md, §0, in its form for affine bijections), with the evidence
> listed above; it is not Lean-checked as a whole. This document establishes it only conditionally: as Theorem
> ar:thm:main and, for part (a) with three hypotheses, as Theorem mb:thm:main3.

Each claim was checked:
- **The project's claim.** `WRITEUP/SYMMETRIC.md` §0 ("Main theorem") states "**Theorem A (computer-assisted).** Every set
  of at least 33 points in general position that has a symmetry contains a convex 7-gon". The Setting paragraph defines
  a symmetry as "an isometry or an affine bijection of the plane, other than the identity, that maps S into itself". A
  bullet of §0 says that `heptagon_of_nontrivial_affineEquiv` derives Theorem A "for isometries and for affine
  bijections" from the five classes. So the attribution and the words "in its form for affine bijections" are
  accurate.
- **Parts (c)-(e).** These parts of `ar:thm:main` concern injective affine maps of the plane. Such maps are bijections,
  so all five parts are presentations of that form.
- **"Not Lean-checked as a whole".** This is true, because three of the five classes are only hypotheses.
- **"Only conditionally ... mb:thm:main3".** `heptagon_of_nontrivial_affineEquiv_3` (RTC:4303) has binders `h2 h3 h5`
  only. Otherwise its statement is that of `heptagon_of_nontrivial_affineEquiv`, which is part (a). It is
  `mb:thm:main3`(b), and mb itself labels it "Lean-checked as a conditional statement".
- **Rigor vocabulary.** The label is attributed to the project. None of "verified", "certified" or "proved" occurs in
  ar.tex. "Establishes ... only conditionally" is the reviewer's own wording. It is used the same way in ll.tex:725,
  mb.tex:1077-1078 and the current sr.tex:981.
- **Consistency with sr.** sr's parallel sentence in `sr:rem:main` (sr.tex:976-982, edited by a concurrent fix and
  compared as on disk at the time of this check) uses the same pattern, in its form for Euclidean isometries.
- **The rest of the remark.** No other sentence rounds up. The second bullet still reads "computer-assisted claims of
  the records", which the claims review accepted as attributed.

## 2. Diff review, hunk by hunk

`diff -u` gives ten hunks in ar.tex and one in ar.map.tsv.
- **Eight paragraph heads** (ar.tex:25, 44, 81, 91, 109, 120, 127, 771). Only `\textbf{...}` was removed. These hunks
  carry no content change.
- **ar.tex:714-720.** See finding 1 above: every factual claim is true.
  - LaTeX: the paths go in `\dirn` and contain no spaces. `\lean{hm1}` and `\lean{hm0}` are fine.
    `\ref{ar:thm:main}` is an ar label.
- **ar.tex:750-756.** See finding 3 above.
  - `\ref{mb:thm:main3}` is an export label.
  - `\S0` renders as §0.
  - The paths have no spaces.
- **No statement changed.** No statement environment, label, macro or package was changed. The 30 statement labels
  match the 30 map rows one to one.
  - So no Lean-faithful statement was touched.
  - The Lean declarations that the edited remark talks about were re-read: AR:1470-1533 (the five theorems of
    `ar:thm:main`), AR:467-492 (the five classes), and RTC:4239-4322 (the integration section, with
    `mirrorOneAxis33_proved`, `mirrorNoAxis34_proved` and the two `_3` theorems).
- **ar.map.tsv.** Only the note of `ar:rem:classes` changed.
  - The row has 5 tab-separated fields and is ASCII.
  - The note is accurate.
  - A dry run of `note_tex` from `tools/make_appendix.py`, imported without running `main`, renders it without error.
    The paths come out in typewriter type with break points.
- **Forbidden content.** `grep` finds no machine path and no tool name in ar.tex or ar.map.tsv.

## 3. Compile check

`build/ar_recheck_r1_wrapper.tex` has the same content as the contract wrapper. It was compiled from `build/` with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`, twice.
- **Exit status.** Both runs exit with status 0. The logs are `build/ar_recheck_r1_run1.txt` and
  `build/ar_recheck_r1_run2.txt`. The PDF has 11 pages.
- **Errors.** There are no `!` errors and no undefined control sequence. The only "missing" line is microtype's
  information message "Character `029' is missing", which is not an error.
- **Boxes.** There are no overfull boxes. The log has only underfull boxes, which come from the high tolerance in
  statements.
- **Undefined references.** These are only to `fd:` labels and to export labels of other sections: `sr:def:iso`,
  `sr:def:classes`, `sr:thm:main`, `sr:thm:variant`, `mb:thm:baek`, `mb:thm:classes`, `mb:thm:main3`, `cb:thm:c3` and
  `cb:thm:c2`. This is expected in the standalone check.
- **Rendering.** The text extracted from page 10, which holds the edited remark, reads as intended, and pages 1 and 10
  were checked visually.

## 4. Findings

- **m1 (minor; older than this fix; not assigned to `ar` in this round). The Coverage paragraph lists conditional
  theorems without saying so.**
  - Source: claims-review F11. Its location list includes "ar.tex:787-789, and the transfer theorem in the same list";
    in the current file these lines are ar.tex:791-796.
  - Current text:
    - `hasConvexNGon_of_affine_symmetry` (Theorem `ar:thm:transfer`) and the three forms of Corollary
      `ar:cor:transfer-forms` take the hypothesis (hE).
    - The five theorems of `ar:thm:main` take the five case classes.
    - None of them is marked conditional.
  - By contrast, ll (ll.tex:800-801, "conditional on Sixfold66") and mb (mb.tex:1175, "(Theorem mb:thm:main3,
    conditional)") mark their conditional theorems.
  - Routing: F11 is not in the `ar` fix log, and `reviews/docfix-ec-r1-fix.md` says F11 was not assigned there either.
  - Fix, as F11 suggests:
    - append ", conditional on (hE)" after `Theorem~\ref{ar:thm:transfer}` and after `Corollary~\ref{ar:cor:transfer-forms}`;
    - append ", conditional on the five case classes" after `Theorem~\ref{ar:thm:main}` in the Coverage list.

## 5. Observations (no action required by this recheck)

- **O1. The import contexts of the two texts differ.** RTC compiles its copy of AR lines 12-1533 with two more imports
  than AR (`ErdosSzekeres.Omission.BaekGeometry`, `ErdosSzekeres.ConvexCycleCuts`). Identical text therefore identifies
  the classes only on the tacit assumption that these modules do not change how the copied text elaborates.
  - The remark's "only through the identity of the two texts" already marks the link as informal.
  - sr and mb describe it at the same level of detail.
  - If a later round wants this precision, all three places should change together, not ar alone.
- **O2. The appendix is stale.** `appendix_map.tex:329` still shows the old note of `ar:rem:classes`. Run
  `python3 tools/make_appendix.py`; the dry run on the new note succeeds.
- **O3. An optional precision.** "for part (a) with three hypotheses, as Theorem mb:thm:main3" refers to
  `mb:thm:main3`(b). Writing "Theorem~\ref{mb:thm:main3}(b)" would be exact. The first bullet of the remark uses the
  same pattern, and the xref review accepted it there.
