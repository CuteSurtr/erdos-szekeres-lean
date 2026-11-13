# Section `ar` (Affine symmetries), whole-document review round 1: fix log

Input: the three findings assigned to `ar` from the whole-document review, round 1:
- `reviews/doc-r1-xref-srarcbsa.md`, finding 2;
- `reviews/doc-r1-consistency.md`, m18;
- `reviews/doc-r1-claims.md`, F4.

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`) or to RES (Lean sources and records).
`ar.tex:N` refers to the edited file.

Snapshot taken before editing: `snapshots/docfix-r1-pre/ar.tex` (SHA-256 `4172a12b50ad`, 807 lines) and
`snapshots/docfix-r1-pre/ar.map.tsv` (SHA-256 `2b8e9d4786b3`). After editing: `sections/ar.tex` (`5da35be91e55`, 812
lines) and `sections/ar.map.tsv` (`af2b7f26447b`).

## Summary

| # | finding | severity | action | location (edited file) |
|---|---|---|---|---|
| 1 | xref-srarcbsa: `ar:rem:classes` does not say that the mirror theorems are about copies of the classes in a separately compiled file | minor | fixed | ar.tex:715-720 (first bullet of `ar:rem:classes`); map note of `ar:rem:classes` |
| 2 | consistency m18: `ar` writes `\paragraph{\textbf{...}}` | minor | fixed | ar.tex:25, 44, 81, 91, 109, 120, 127, 771 |
| 3 | claims F4: "The unconditional form ... is therefore computer-assisted" | major | fixed | ar.tex:753-756 (last sentence of `ar:rem:classes`); map note of `ar:rem:classes` |

3 findings, 3 fixed, 0 declined.

## 1 (fixed): the mirror classes are discharged through copies

Source check.
- `SYMLEAN/mirror/ReductionThreeClasses.lean` (SHA-256 `0cc83994fe8c`, 4322 lines) has imports only at lines 1-13. They
  are repository modules `ErdosSzekeres.*` and Mathlib modules. It does not import `SYMLEAN/AffineReduction.lean`.
- Lines 38-1559 of that file are byte-identical to lines 12-1533 of `SYMLEAN/AffineReduction.lean` (SHA-256
  `41cfc0b60aec`). Checked with `cmp` on the two `sed` extracts; both extracts have SHA-256 `f4fed1411fb9`.
- The copies of the classes are at lines 508 and 514, which is 482+26 and 488+26.
- `mirrorOneAxis33_proved : MirrorOneAxis33` is at line 4274, `mirrorNoAxis34_proved : MirrorNoAxis34` at line 4282, and
  `heptagon_of_nontrivial_affineEquiv_3` at line 4303. The line numbers in the remark are right.
- `SYMLEAN/mirror/axioms.out` lists `[propext, Classical.choice, Quot.sound]` for both mirror theorems.
- All five theorems of `ar:thm:main` (`SYMLEAN/AffineReduction.lean`, lines 1477, 1489, 1501, 1510, 1521) have the
  binders `(hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)`. These are the constants of `SYMLEAN/AffineReduction.lean`.
- `sr:rem:records` (sr.tex:286-290) and mb's paragraph "Copies of the same code" (mb.tex:89-94) state the
  identification by text. `ar:rem:classes` did not.

So the finding is correct.

Change. After "(Theorem~\ref{mb:thm:classes})." the bullet now says:
- these two theorems are about the copies of the class definitions in that file;
- the file does not import `SYMLEAN/AffineReduction.lean`;
- lines 38-1559 of `SYMLEAN/mirror/ReductionThreeClasses.lean` are byte-identical to lines 12-1533 of
  `SYMLEAN/AffineReduction.lean`;
- so the two theorems discharge the premises `hm1` and `hm0` of Theorem `ar:thm:main` only through the identity of the
  two texts.

The reviewer's suggested wording is used in substance. The two file names are written out, because a pronoun would be
ambiguous between them. The line ranges are added so that the identity can be checked, as in mb.

## 2 (fixed): bold paragraph heads

Source check.
- `ar` was the only section with `\paragraph{\textbf{...}}`: 8 of its 8 paragraph heads.
- The other eleven sections have 71 `\paragraph{...}` heads, none of them bold.
- The preamble does not redefine `\paragraph`. amsart sets its paragraph heads in normal weight.

Change. `\textbf` was removed from all eight heads: Sources, Rigor and axioms, Dependencies, Points, matrices,
iterates, Finite sets, Euclidean isometries, Affine maps (Mathlib), Coverage. The head texts are unchanged.

## 3 (fixed): the unconditional statement is the project's claim, not a result of this document

Source check.
- fd.tex:66-75 defines *computer-assisted* for a statement whose written proof, given in this document, relies on a
  finite computation.
- The unconditional statement has no such proof here. Three of its five hypotheses (`HalfTurn34`, `Threefold33`,
  `Fivefold35`) are only assumed in this document.
- `WRITEUP/SYMMETRIC.md`, §0, line 17, reads "**Theorem A (computer-assisted).** Every set of at least 33 points in
  general position that has a symmetry contains a convex 7-gon". Its bullet at lines 26-28 says that
  `heptagon_of_nontrivial_isometry` and `heptagon_of_nontrivial_affineEquiv` derive Theorem A "for isometries and for
  affine bijections" from the five case classes.

So the label "computer-assisted" belongs to the project's claim, and the old sentence gave it in this document's voice.
The finding is correct.

Change. The old sentence was "The unconditional form of Theorem~\ref{ar:thm:main} is therefore computer-assisted, and
it is not Lean-checked as a whole." It is replaced by:

> The unconditional statement, Theorem~\ref{ar:thm:main} without its five hypotheses, is claimed in the project as
> computer-assisted (Theorem~A of WRITEUP/SYMMETRIC.md, §0, in its form for affine bijections), with the evidence
> listed above; it is not Lean-checked as a whole. This document establishes it only conditionally: as
> Theorem~\ref{ar:thm:main} and, for part~(a) with three hypotheses, as Theorem~\ref{mb:thm:main3}.

This follows the reviewer's suggestion, with three additions:
- §0 is named, because that is where Theorem A is stated;
- "not Lean-checked as a whole" is kept from the old sentence;
- the three-hypothesis form `mb:thm:main3`(b) is named, so that "only conditionally" lists both conditional forms in
  the document. That form is `heptagon_of_nontrivial_affineEquiv_3`, RTC:4303, with binders `h2 h3 h5` only, already
  cited in the first bullet.

## Map

`sections/ar.map.tsv`, row `ar:rem:classes`, note column. The old note was "what supplies the five class hypotheses
and with which rigor label". The new note is the old one followed by "; the mirror theorems concern byte-identical
copies in SYMLEAN/mirror/ReductionThreeClasses.lean; the unconditional statement is a project claim
(WRITEUP/SYMMETRIC.md, Theorem A), established here only conditionally".

Checks on the map:
- The note is ASCII.
- A dry run of `note_tex` from `tools/make_appendix.py` on the new note succeeds.
- The label column is unchanged.

`appendix_map.tex` (line 329) still shows the old note. I did not regenerate it, because only the `ar` files are mine
to edit. Run `python3 tools/make_appendix.py` to pick up the new note.

No statement environment was changed, and no label was added, removed or renamed (the `\label` lists before and after
are identical). No macro was defined and no package loaded. There are no machine paths and no tool names in
`ar.tex` or `ar.map.tsv`.

## Compile check

`build/ar_wrapper.tex` was compiled twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode
-halt-on-error`.
- Both runs exit with status 0. The logs are `build/ar_docfixr1_run1.txt` and `build/ar_docfixr1_run2.txt`.
- No `!` errors, no "Missing", no undefined control sequence.
- 0 overfull boxes.
- The only undefined references are to `fd:` labels and to export labels of other sections: `sr:thm:main`,
  `sr:def:classes`, `sr:def:iso`, `sr:thm:variant`, `mb:thm:baek`, `mb:thm:classes`, `mb:thm:main3`, `cb:thm:c3` and
  `cb:thm:c2`. These are expected in the standalone check.
- The rendered text (`build/ar_docfixr1.txt`, from pdftotext) of the edited remark reads as intended.
