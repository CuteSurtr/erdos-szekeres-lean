# Section `ar` (Affine symmetries), final pass round 1: independent re-check

Lens: recheck. Verdict: **pass** (no blocker or major finding remains or is introduced; one minor, optional).

Paths are relative to STAGE (`sections/`, `build/`, `snapshots/`) or to RES (Lean sources and records).
Inputs: `snapshots/final-r1-pre/ar.tex` (SHA-256 `5da35be91e55`, 812 lines), `sections/ar.tex` (`e235b9c61817`,
814 lines), `ar.map.tsv` unchanged (`af2b7f26447b` before and after). Repository at commit `7e32ee259`.

## Diff

`diff -u` gives two hunks (ar.tex:742-746 and ar.tex:792-798), both inside the two findings. The map is byte-identical.
The `\label`s, the multiset of `\ref`s and all statement heads are identical before and after. Nothing outside the
findings changed.

## Finding 1 (minor, Coverage marks conditional theorems): resolved

- Lean source `SYMLEAN/AffineReduction.lean` (SHA-256 `41cfc0b60aec`, matches the section): the four transfer forms
  (lines 1330, 1423, 1433, 1444) take `hE` (the Euclidean statement) and `hN : 3 ≤ N`; all five theorems of
  `ar:thm:main` (lines 1477, 1489, 1501, 1510, 1521) take `(h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)
  (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)`, and no other class.
- "(hE)" is the section's own name for that hypothesis (the item `(hE)` of `ar:thm:transfer`, ar.tex:573; "Assume
  (hE)" in `ar:cor:transfer-forms`; Definition `ar:def:E`). The Coverage text now says "conditional on (hE)" for
  Theorem `ar:thm:transfer` and Corollary `ar:cor:transfer-forms`, and "conditional on the case classes HalfTurn34,
  Threefold33, Fivefold35, MirrorOneAxis33 and MirrorNoAxis34" for `ar:thm:main`. The five names are exactly the Lean
  binders. This agrees with the head of `ar:thm:main` ("conditional on the five case classes"), with the introduction
  (ar.tex:13-15) and with Remark `ar:rem:hE`(1), which presents (hE) as a parameter and not as an unproved claim, so
  "conditional on" is accurate and does not suggest an unproved premise. Leaving out `3 ≤ N` (a numerical side
  condition stated in the theorems) is right; `ll` does the same.
- Map: no change needed; its notes already list the hypotheses (rows `ar:thm:transfer`, `ar:cor:transfer-forms`,
  `ar:thm:main`).

## Finding 2 (major, rigor label of the C2 bookkeeping): resolved

- `find C2FINAL -type f`: 27 files. None is a compile, build or axioms log of a Lean run (the three files under
  `evidence/central34-cover` are SAT checker outputs). `git log --diff-filter=D` shows no file ever removed from
  `C2FINAL`.
- `C2FINAL/Central34Orbits.lean` (298 lines) ends with three `#print axioms` lines (296-298); their output is not
  saved. A search of the whole repository for `Central34`, `all_cases_closed`, `closed_are_subcases` and
  `subcases_reflection` finds only the Lean file, `gen_lean.py`, `C2FINAL/README.md`, `C2ENC/class_table.md`,
  `AUDIT3/reports/A5_central_geometry.md` and `WRITEUP/SYMMETRIC.md`: generator and prose records, no Lean output.
  The audit (A5, row 12) recomputed the closure in Python and did not run Lean; `AUDIT3/A5_central_geometry` holds no
  Lean log.
- `C2FINAL/README.md` (SHA-256 `caf5cfec4071`), §6 "Lean check of the bookkeeping" (lines 147-162): "Core Lean
  4.24.0, `decide +kernel`, axioms `propext` only, about 6 s" for the three theorems. So, by the rule of Section `fd`
  (now fd.tex:84-86), the label is "Lean-checked according to the record", and ar.tex:745 now says exactly that and
  names the record (`C2FINAL/README.md`, §6), in the same form as mb.tex:1110 and consistent with cb.tex:78-87,
  1327, 1376, 1390 and sr.tex:83.
- The threefold cover keeps "Lean-checked": `C3LEAN/logs/compile.log`:18 and `C3LEAN/review/logs/main_compile.log`:18
  read `'C3Cover.all_roots_covered' depends on axioms: [propext, Quot.sound]`; 910 roots per `C3LEAN/README.md`:5.
- "computer-assisted because their finite checks are kernel evaluations (decide +kernel)" stays and is accurate for
  both files (`decide +kernel` at Central34Orbits.lean:281, 288, 292 and throughout C3Cover.lean).
- No other place in ar.tex gives the C2 bookkeeping a Lean label (grep for `Lean-checked`, `C2FINAL`, `Central34`,
  `cb:`, `parallelogram`, `bookkeeping`).

## Remaining observation (minor, optional; introduced by the edit, no effect on correctness)

ar.tex:745-746. The next sentence keeps "that every piece named there has a record with the checker verdicts and a
CNF hash ...". Before the edit "there" followed "(Theorems cb:thm:c3 and cb:thm:c2)"; now it follows
"(C2FINAL/README.md, §6; Theorem cb:thm:c2)", so a reader may take "there" to mean the README section or only the C2
theorem, although the statement holds for both bookkeeping steps. Either reading is true, so nothing false is said.
Optional fix: "that every piece named in these two theorems has a record ...".

## Checks

- Compile: `build/ar_final_recheck_r1_wrapper.tex` (contract wrapper), `nice -n 15 pdflatex -interaction=nonstopmode
  -halt-on-error`, twice from `build/`: both runs exit 0, no line starting with `!`, no Overfull box, 32 Underfull
  warnings (pre-existing, from long Lean names). Undefined references only `fd:` labels and the export labels
  `cb:thm:c2`, `cb:thm:c3`, `mb:thm:baek`, `mb:thm:classes`, `mb:thm:main3`, `sr:def:classes`, `sr:def:iso`,
  `sr:thm:main`, `sr:thm:variant` (expected in the standalone check). Rendered text of both hunks checked with
  `pdftotext` ("§6" and the Lean names render correctly).
- No machine path, no tool name, no "verified"/"certified"/"proved" (as words) in `ar.tex` or
  `ar.map.tsv`; no `\newcommand`, `\usepackage` or preamble material.

## Summary

| # | finding | status |
|---|---|---|
| 1 | Coverage marks conditional theorems (minor) | resolved |
| 2 | C2 bookkeeping label "Lean-checked according to the record" (major) | resolved |
| new | antecedent of "there" at ar.tex:745-746 (minor, optional) | open, does not affect the verdict |
