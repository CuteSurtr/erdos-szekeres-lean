# Final inline edits, round 3: independent check (lens: inline3)

Verdict: **pass**. Both edits in `build/final-inline3.diff` are correct when checked against the Lean files in RES
(commit `7e32ee259`). They carry out the two optional suggestions of `reviews/final-inline2-check.md` (findings 1
and 2). Every Lean name is right, every `\ref` follows the label rule, and the edited pages render cleanly. There is no
blocker, no major and no minor finding.

Paths: section files are relative to STAGE, Lean files to RES. Line numbers are those of the current files. Statement
and page numbers come from `build/inline-check3/proofs.pdf` (188 pages). Under STAGE I wrote only this report and the
files in `build/inline3-verify/`: an independent rebuild, the pdftotext output and three page images. I edited nothing
under REPO or STAGE. I did not run Lean, lake or any solver. Two scratch text files were kept outside STAGE.

## Findings

None.

## The diff itself

I recomputed `diff -u snapshots/final-inline3-pre/sa.tex sections/sa.tex`. Apart from the header lines it matches
`build/final-inline3.diff` exactly: two hunks, 2 lines removed and 6 added, and nothing else in sa.tex changed. The
build in `build/inline-check3/` (23:06:21-26) is newer than the edit (23:06:14), and its text contains both new
passages.

## Edit 1: naming sentence, sa.tex:430-433 (end of the first paragraph of Subsection 12.5, `sa:ssec:use`)

Text: "The names \lean{HalfTurn34}, \lean{Threefold33}, \lean{Fivefold35}, \lean{MirrorOneAxis33}, \lean{MirrorNoAxis34}
and \lean{Fourfold32} denote the case classes of Definition~\ref{sr:def:classes}, in the namespace
\lean{ErdosSzekeres.SymReduction}."

(a) **Namespace.** `SYMLEAN/SymmetricReduction.lean` opens `namespace ErdosSzekeres.SymReduction` at :54 and closes it
at :1059. The only block in between is `section Orbits` (:60-:260), which does not change the namespace. The six
classes are `def ... : Prop` at :467 (`HalfTurn34`), :472 (`Threefold33`), :477 (`Fivefold35`), :482
(`MirrorOneAxis33`), :488 (`MirrorNoAxis34`) and :496 (`Fourfold32`), so their full names are
`ErdosSzekeres.SymReduction.<name>`. Row 8 of `sections/sr.map.tsv` (`sr:def:classes`, kind `definition`) gives the
same six full names with the same six lines. So does the head of Definition 7.7 (sr.tex:212).

(b) **Bare uses.** Outside the new sentence, sa.tex writes the six names bare 26 times, on lines 449–597. I read each
one in context. Every one means the class of Definition 7.7:
- 449 (two uses): Lemma 12.12(b), "the map of the classes ... of Definition~\ref{sr:def:classes}", which names the
  definition explicitly.
- 510, 513, 515: item (1), cases s = 2, 3, 5 of Remark 12.13. The text describes the hypotheses of `HalfTurn34`
  (with "(Definition 7.7)"), `Threefold33` and `Fivefold35`. Each matches the SymReduction definition: exactly 34, 33
  or 35 points, `c ∉ S`, and `halfTurn c` or `rotAbout c (2π/3)` or `rotAbout c (2π/5)`.
- 524: item s = 4, "the class `Fourfold32`". The next sentence names `SymReduction.case_fourfold` (:763,
  `(h4 : Fourfold32)`) and Theorem 7.41 (`halfTurn_of_symmetric_counterexample`, :1024-1025, `(h4 : Fourfold32)`).
  It sets this class against "a same-text copy, `LayerLemma.Fourfold32`".
- 551, 554: item (2), the hypotheses of `MirrorNoAxis34` and `MirrorOneAxis33`. These match :482-:493: unit `u`,
  general position, 33 or 34 points, `reflLine a u` invariance, and exactly one fixed point or none.
- 566-567 (five uses) and 575-576 (three uses): item (4), Status.
- 588-597 (ten uses): item (5), the size table. Lines 596-597 contrast the bare `Fourfold32` and `Fivefold35` with
  "the same-text copy `LayerLemma.Fourfold32`" (599) and "`LayerLemma.Fivefold35`" (602).

The copies in `LEANEXT/es7corr/ES7Corollaries.lean` (namespace `ErdosSzekeres.LayerLemma`, :37-:1233; `Fivefold35` at
:1157, `Fourfold32` at :1164) appear in sa.tex only with their prefix, at 528, 599 and 602. Under fd.tex:40-42 these
read as `ErdosSzekeres.LayerLemma.<name>`. Neither name occurs in LAYERLEAN, so this reading is unambiguous.

Item (4) says that Theorem 10.40 is conditional on `HalfTurn34`, `Threefold33` and `Fivefold35`, and that the two
mirror classes are Lean-checked (Theorem 10.39). Those Lean theorems use the classes of
`SYMLEAN/mirror/ReductionThreeClasses.lean`. I checked that these classes have the same full names as the ones in
Definition 7.7:
- Lines 38–1084 of that file are byte-identical to lines 12–1058 of `SymmetricReduction.lean` (`diff` gives no
  output).
- `mirrorOneAxis33_proved : MirrorOneAxis33` (:4274), `mirrorNoAxis34_proved` (:4282) and
  `heptagon_of_nontrivial_isometry_3` / `_affineEquiv_3` (:4292, :4303) lie in `namespace ErdosSzekeres.SymReduction`
  (:4249-:4310).

So these sentences agree with the new naming sentence. They also agree with the document's own identification of such
copies (sr.tex:291-295: "copies of those of Definition~\ref{sr:def:classes}, with the same full names and the same
text"; mb.tex:1041).

(c) **Placement.** The first of the six names anywhere in sa.tex is on line 431, in the new sentence. Lines 1–430
mention only "case classes" (lines 4, 14-15, 51-52, 134) and never a class name, in `\lean` or in any other form. The
first bare use, line 449 in Lemma 12.12(b), comes after the sentence. This is also why the sentence is better placed
here than before Remark 12.13, which the inline2 report suggested.

(d) **Label.** `sr:def:classes` is an export label in the CONTRACT table (sr row). sr.tex:212 defines it on the
definition it names (Definition 7.7 in the build). I checked every `\ref` in sa.tex, 127 in all, against the label rule
(CONTRACT.md:68-69): each one is an sa label, an fd label or an export label. The diff touches four labels:
`sr:def:classes` is the only new one; `fd:def:rot`, `sa:lem:model`, `sa:prop:rot` and `ec:thm:fourfold` were there
before.

## Edit 2: sa.tex:528-530 (Remark 12.13, item s = 4)

Before: "... is the hypothesis of Theorem~\ref{ec:thm:fourfold} and of the form
\lean{LayerLemma.fourfold_heptagon_of_erase} that its proof uses;"
After: "... is the hypothesis of Theorem~\ref{ec:thm:fourfold} and of its layer form
\lean{LayerLemma.fourfold_heptagon_of_erase}, which its proof uses;"

- **The proof uses it.** `fourfold_heptagon (H : Fourfold32) ...` is at `ES7Corollaries.lean:1216`. Its proof
  (:1219-:1231) derives `c ∉ S` from `centre_not_mem_of_even` and then ends with
  `refine fourfold_heptagon_of_erase H S c hgp hinv ?_` (:1229). `fourfold_heptagon_of_erase (H : Fourfold32) ...`
  is at :1203, so `LayerLemma.Fourfold32` is a hypothesis of both theorems. The written proof of Theorem 6.7 ends by
  applying Theorem 6.6 (ec.tex:238).
- **"Layer form".** The docstring at :1201 reads "**Fourfold, layer form.** From `Fourfold32`: ...". ec titles the
  statement "fourfold, layer form" (ec.tex:215, `ec:thm:fourfold-erase`, Theorem 6.6), and Theorem 6.7 is titled
  "fourfold" (ec.tex:227). So "its layer form" matches both. Both uses of "its" refer to Theorem 6.7: "layer form of a
  hypothesis" would make no sense.
- **No new `\ref`.** `ec:thm:fourfold-erase` is not an export label, so naming the Lean declaration is the correct
  choice. `LayerLemma.fourfold_heptagon_of_erase` is the full name minus `ErdosSzekeres.`, as fd.tex:40-42 allows.
- **Consistency.** The phrasing matches sr.tex:298-299 ("of Lemma~\ref{sr:lem:fourfold}, which its proof uses"). It
  also matches ec.tex:154-156 ("the hypothesis of Theorems 6.6 and 6.7") and ec.map.tsv:7-8 (both rows: "takes
  hypotheses: Fourfold32").

## Rendering, build, and forbidden content

- **pdftotext -layout.** Page 155 shows the naming sentence verbatim, with "Definition 7.7", at the end of the first
  paragraph of 12.5. Page 156 shows Edit 2 verbatim: "... is the hypothesis of Theorem 6.7 and of its layer form
  LayerLemma.fourfold_heptagon_of_erase, which its proof uses; item (5) uses the class for the size table.)". There
  is no "??", no broken name and no stray text. Images of pages 155-157 at 80 dpi show clean lines and no overfull
  margins.
- **Log of `build/inline-check3`.** No errors, overfull boxes, undefined references or multiply defined labels, and no
  rerun request; 188 pages.
- **Independent rebuild.** I rebuilt into `build/inline3-verify/` with `nice -n 15 pdflatex`, three passes, all exiting
  0. The counts are the same, the page count is 188, and the pdftotext output is identical to that of
  `build/inline-check3`.
- **Cosmetic note, no action.** The sa part of the log now has one more page-builder warning, `Underfull \vbox
  (badness 5119)` on page 157. It is the stretch above "Coverage." that results from the three added lines. The
  inline2 build already had the one on page 156 (badness 3049). Neither affects the text.
- **Forbidden content.** The added lines contain no machine path and no tool name. A scan of the whole of
  sa.tex for `/private`, `/Users`, `/home`, `/tmp`, the scratch directory and tool names also finds nothing. The
  edited lines are at most 117 characters long and have no trailing whitespace.
