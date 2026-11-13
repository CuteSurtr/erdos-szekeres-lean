# Section `pc`, round doc-r0: fix log

Inputs: the five minor notes for `pc` in `build/open_minors.json`, which come from `reviews/pc-p1-diff.md` (m1, m2)
and `reviews/pc-p1-referee.md` (F1, F2, F3). The pre-edit snapshot is in `snapshots/doc-r0-pre/` (`pc.tex`,
`pc.map.tsv`). Paths below are relative to STAGE, to RES (Lean sources and records) or to the repository root.

Result: all 5 notes fixed, 0 declined. I checked every note against RES before editing. No statement of a Lean
declaration changed, and no label was removed or renamed (34 labels, the same as before). The map stays in sync:
32 rows, the same labels, kinds, Lean names and file:line columns, and two notes extended.

## Notes

| # | Note (lens) | Action | Location (current pc.tex) | What was checked / done |
|---|---|---|---|---|
| 1 | Mutant M7: the replacement by `True` is credited to the log, but it is defined in `mutants.py` (diff m1) | fixed | "How Lean checks it", lines 788-792 | `LEANEXT/phase/logs/mutants.log:7` only names M7 ("drop antipodal premise in word_dichotomy") and gives its first error. The replacement `(∀ i : Fin 6, s (i + 3) = !s i) →` ↦ `True →` is defined in `LEANEXT/phase/mutants.py:23-24`. New text: "Mutant M7 of the mutation script `LEANEXT/phase/mutants.py` replaces the premise by `True`; the mutation log …, which calls this mutant 'drop antipodal premise in `word_dichotomy`', records that it fails to compile with the error …". The script prints only the first line of the first error (`errs[0]`), which the new parenthesis now says. |
| 2 | Remark pc:rem:word-scope calls `EncB.wordSpec`, `arcFrame` and `labelling_ruleB` Lean-checked without citing evidence (diff m2) | fixed | Remark pc:rem:word-scope, lines 836-842 | Added one sentence: the three depend only on propext, Classical.choice and Quot.sound. For `wordSpec` the evidence is the `#guard_msgs` pin after it (`ENCBLEAN/EncB/SoundWord.lean:228-229`), the build `ENCBLEAN/logs/m3_build.log:9` (Built EncB.SoundWord) and `ENCBLEAN/logs/axioms.log:446`. For `arcFrame` and `labelling_ruleB` it is the `#print axioms` output in `ENCBLEAN/logs/m8_fix_build.log:35` and `:29`, and the pin of `EncB.Geo.modelOfLabelling` (`Audit.lean:45-46`), which uses `labelling_ruleB` (`ModelOfLabelling.lean:30`; `labelling_ruleB` uses `arcFrame`, `ArcBridge.lean:480`). Every line was re-read before and after the edit. The current `SoundWord.lean` hash `c1bdb4175ee5…` is the one in `ENCBLEAN/logs/env.txt` (M3 step) and in `m9_review_lean_soundness.log:61`. |
| 3 | The blanket rigor sentence also covers remarks that name Lean declarations (referee F1) | fixed | "Rigor and axioms", lines 63-66 | New text: "Every definition, lemma, proposition, theorem and corollary below whose head or one of whose parts carries a Lean reference is Lean-checked; … Remarks are commentary and, even when they name Lean declarations, are not Lean-checked as a whole; the mathematical claims they add to the Lean statements are written observations." This agrees with the local labels in pc:rem:gaps(2) and pc:rem:runs ("written observation") and with the Coverage paragraph. The written step pc:lem:shift has no Lean reference, so it stays outside the sentence. I did not adopt the suggested "labelled as such": pc:rem:alt-boundary and pc:rem:runB-example carry that label only in the Coverage paragraph, not in their own text. |
| 4 | The opening sentence asserts six distinct points unconditionally (referee F2) | fixed | opening paragraph, lines 4-10 | The six directions are "distinct unless one of the gaps β−α, δ−β, α+2π−δ equals π, in which case a direction and an antipode coincide (Remark pc:rem:reading)". "Of these six points" became "of these points, expressed by the arc predicates of Definition pc:def:arc (which are defined in every case)". An exact grid check (angles in units of π/24, α ∈ {0, π/7, −5π/3}, 3243 ordered triples) gives 0 mismatches for both claims: "distinct ⇔ no gap = π" and "some gap = π ⇔ a direction equals an antipode mod 2π". |
| 5 | The axiom transfer from the ENCBLEAN pins does not mention the vendored repository modules (referee F3) | fixed | "Rigor and axioms", lines 86-93 | Checked first: `Capstone2.lean` imports the repository modules `ErdosSzekeres.{Definitions, OrientationGeometry, Suk.OrientationClique, Orientation}`. Their import closure is exactly the 10 modules in `ENCBLEAN/geo/VENDOR.sha256`, and the vendored set imports no other repository module. `shasum -a 256` of the 10 vendored files equals the list and equals `ErdosSzekeres/*.lean` of the repository checkout. `ENCBLEAN/geo/lakefile.toml:5-8` states that the copies keep the repository names. Both packages pin Lean v4.24.0 and Mathlib `f897ebcf72cd…`, and neither lakefile sets Lean options besides `-j1`. New text: the package compiles the copy from the same sources, against the same imports, as the original file: the byte-identical copy, the common pins, and "the ten repository modules that Capstone2.lean needs (its imports …, with the repository modules they import) are compiled there from verbatim copies, whose SHA-256 hashes are listed in `ENCBLEAN/geo/VENDOR.sha256` and agree with those of the repository files". The conclusion sentence is unchanged. |

## Other changes

- `sections/pc.map.tsv`, note column only:
  - row `pc:lem:helpers`: appended "the copy is compiled against verbatim copies of the ten repository modules it
    needs (ENCBLEAN/geo/VENDOR.sha256, hashes equal to the repository files)" (note 5);
  - row `pc:rem:word-scope`: appended the axiom records of note 2.
- Layout: the first wording of note 3 added one underfull line (badness 1132) to the Rigor paragraph. I reordered the
  sentence ("…and, even when they name Lean declarations, are not Lean-checked as a whole"), and the count is back to
  51, the same as the snapshot built with the same preamble (`build/docr0_snapcheck/`).
- One long source line in the M7 paragraph was rewrapped. The output is unchanged.
- No other text changed. `diff` against the snapshot shows exactly five hunks: lines 6-10, 63-66, 86-93, 788-794 and
  836-843.

## Checks

- Compile: `build/pc_wrapper.tex`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice from `build/`:
  - both passes exit 0, 13 pages;
  - 0 errors, 0 "Missing", 0 multiply defined labels;
  - **overfull boxes: 0**;
  - 51 underfull boxes, as in the snapshot.
  - The undefined references are exactly the 14 allowed labels of other sections: fd:def:inv, fd:def:ngon,
    fd:def:orient, fd:def:point, fd:def:rot, fd:lem:orient, lg:def:polar, lg:lem:polar, lg:lem:ruleA, lg:lem:ruleB,
    lg:lem:sinadd, lg:thm:radius, ll:def:hv, ll:def:peel.
- Hygiene of `pc.tex` and `pc.map.tsv`: no machine path; no tool name; no `\newcommand`, `\def`,
  `\usepackage` or `\begin{document}`; no `\lean`/`\dirn` argument with a space; every `\ref` targets a pc:, fd:, ll:
  or lg: label.
- Rigor vocabulary: the only occurrences of "verif"/"proved" are the three accepted before: the mathematical "verify
  the two inequalities", the quoted Lean message "Tactic decide proved that the proposition", and "is not proved in
  LEANEXT". The edits add none.
- Map against environments: 32 environments and 32 rows, with the same labels and kinds in the same order. Every row
  has 5 fields, and the trailing newline is preserved.
