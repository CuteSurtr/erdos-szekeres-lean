# Section `ar` (Affine symmetries), final pass round 1: fix log

Input: the two findings assigned to `ar` in the final pass, round 1.

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`) or to RES (Lean sources and records).
`ar.tex:N` refers to the edited file.

Snapshot taken before editing: `snapshots/final-r1-pre/ar.tex` (SHA-256 `5da35be91e55`, 812 lines) and
`snapshots/final-r1-pre/ar.map.tsv` (SHA-256 `af2b7f26447b`, 31 lines). After editing: `sections/ar.tex`
(`e235b9c61817`, 814 lines) and `sections/ar.map.tsv` (unchanged, `af2b7f26447b`).

`diff` of the snapshot and the edited file: two hunks only (ar.tex:743-746 and ar.tex:792-798). No label was added,
removed or renamed. No statement environment was touched.

## Summary

| # | finding | severity | action | location (edited file) |
|---|---|---|---|---|
| 1 | Coverage names the conditional theorems without saying they are conditional | minor | fixed | ar.tex:792, 794, 797-798 (Coverage list) |
| 2 | "Two bookkeeping steps are Lean-checked": the central parallelogram closure (C2FINAL) has no saved Lean output | major | fixed | ar.tex:742-746 (third sub-bullet of the second bullet of `ar:rem:classes`) |

2 findings, 2 fixed, 0 declined.

## 1 (fixed): the Coverage list marks the conditional theorems

Source check (`SYMLEAN/AffineReduction.lean`, SHA-256 `41cfc0b60aec`).
- `hasConvexNGon_of_affine_symmetry` (line 1330) has the binders
  `(hE : ∀ (S : Finset Point) (g : Point → Point), GeneralPosition S → N ≤ S.card → IsEucIsometry g → g ≠ id →
  Invariant g S → HasConvexNGon n S)` and `(hN : 3 ≤ N)`. The three forms `hasConvexNGon_of_affineMap_symmetry`
  (line 1423), `hasConvexNGon_of_affineEquiv_symmetry` (line 1433) and `hasConvexNGon_of_affine_coords_symmetry`
  (line 1444) have the same `hE` and `hN` binders.
- In the section this hypothesis is called (hE): it is the item `\item[\textup{(hE)}]` of Theorem `ar:thm:transfer`,
  Corollary `ar:cor:transfer-forms` says "Assume (hE), exactly as in Theorem ...", and Definition `ar:def:E` names
  it as the statement E(N,n). So "(hE)" is the section's name for it.
- All five theorems of `ar:thm:main` (`heptagon_of_nontrivial_affine` line 1477, `..._affineMap` 1489,
  `..._affineEquiv` 1501, `..._affineEquiv_image` 1510, `..._affine_coords` 1521) have the binders
  `(h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35) (hm1 : MirrorOneAxis33) (hm0 : MirrorNoAxis34)`.
  These are exactly the five classes named in the head and statement of `ar:thm:main` (all classes of
  `sr:def:classes` except `Fourfold32`).
- Sections `ll` (ll.tex:800-801, "conditional on \lean{Sixfold66}") and `mb` (mb.tex:1175, "conditional") mark their
  conditional theorems in Coverage; `ar` did not.

Old wording (ar.tex:791-796 of the snapshot):
```
\item \lean{hasConvexNGon_of_affine_symmetry} (Theorem~\ref{ar:thm:transfer});
\lean{hasConvexNGon_of_affineMap_symmetry}, \lean{hasConvexNGon_of_affineEquiv_symmetry} and
\lean{hasConvexNGon_of_affine_coords_symmetry} (Corollary~\ref{ar:cor:transfer-forms});
\item \lean{heptagon_of_nontrivial_affineEquiv}, \lean{heptagon_of_nontrivial_affineEquiv_image},
\lean{heptagon_of_nontrivial_affineMap}, \lean{heptagon_of_nontrivial_affine} and
\lean{heptagon_of_nontrivial_affine_coords} (Theorem~\ref{ar:thm:main}).
```

New wording (ar.tex:792-798):
```
\item \lean{hasConvexNGon_of_affine_symmetry} (Theorem~\ref{ar:thm:transfer}, conditional on (hE));
\lean{hasConvexNGon_of_affineMap_symmetry}, \lean{hasConvexNGon_of_affineEquiv_symmetry} and
\lean{hasConvexNGon_of_affine_coords_symmetry} (Corollary~\ref{ar:cor:transfer-forms}, conditional on (hE));
\item \lean{heptagon_of_nontrivial_affineEquiv}, \lean{heptagon_of_nontrivial_affineEquiv_image},
\lean{heptagon_of_nontrivial_affineMap}, \lean{heptagon_of_nontrivial_affine} and
\lean{heptagon_of_nontrivial_affine_coords} (Theorem~\ref{ar:thm:main}, conditional on the case classes
\lean{HalfTurn34}, \lean{Threefold33}, \lean{Fivefold35}, \lean{MirrorOneAxis33} and \lean{MirrorNoAxis34}).
```

`3 ≤ N` is a numerical side condition, not a proposition supplied from elsewhere, so it is not named in Coverage (as in
`ll`, whose Coverage names only `Sixfold66`/`Sevenfold70`). The statements themselves already state (hE), `3 ≤ N` and the
five classes as hypotheses and were not touched.

Map: no change needed. The map has one row per statement environment, not per Coverage line, and its notes already
say "takes hypothesis hE (...) and 3 <= N" (`ar:thm:transfer`, `ar:cor:transfer-forms`) and "takes hypotheses:
HalfTurn34, Threefold33, Fivefold35, MirrorOneAxis33, MirrorNoAxis34" (`ar:thm:main`).

## 2 (fixed): the closure of the central parallelogram orbits is Lean-checked according to the record

Source check.
- `find RES/C2FINAL -type f`: 27 files (the Lean file, `README.md`, `gen_lean.py`, `hashmatch.*`, `recount.*`,
  `closure_split.py`, and the directories `evidence/central34-cover` (three SAT checker outputs), `pilot/`,
  `sample/`, `review/`). None is a compile, build or axioms log of a Lean run.
- `C2FINAL/Central34Orbits.lean` (SHA-256 `b396a26b2430`) ends with three `#print axioms` lines (296-298) whose
  output is not saved anywhere. No `.lean` file of the repository imports or mentions `Central34`.
- `grep -rl Central34Orbits` over the repository finds only `C2FINAL/README.md`, `C2FINAL/gen_lean.py`,
  `C2ENC/class_table.md`, `AUDIT3/reports/A5_central_geometry.md` and `WRITEUP/SYMMETRIC.md` (prose and generator,
  no Lean output). No `.out`, `.log`, `.tsv` or `.txt` file of the repository mentions `Central34`.
- `C2FINAL/README.md` (SHA-256 `caf5cfec4071`), §6 "Lean check of the bookkeeping": "Core Lean 4.24.0,
  `decide +kernel`, axioms `propext` only, about 6 s", for `subcases_reflection`, `closed_are_subcases` and
  `all_cases_closed`. This record is the only evidence.
- By fd.tex:76-78 the label is therefore "Lean-checked according to the record". Section `cb` now uses this label
  for `cb:thm:c2-refl`, `cb:fact:c2-sub` and `cb:thm:c2` (cb.tex:78-87, 1327, 1376, 1390).
- The threefold cover keeps "Lean-checked": `C3LEAN/logs/compile.log`, line 18, and
  `C3LEAN/review/logs/main_compile.log`, line 18, both read
  `'C3Cover.all_roots_covered' depends on axioms: [propext, Quot.sound]`.
- `grep` over ar.tex for `C2FINAL`, `Central34`, `cb:`, `parallelogram`, `bookkeeping` and `Lean-checked`: the
  sentence below is the only place in `ar` that gives a Lean label to the C2 bookkeeping.

Old wording (ar.tex:742-745 of the snapshot):
```
Two bookkeeping steps are
Lean-checked, and computer-assisted because their finite checks are kernel evaluations (\texttt{decide +kernel}): the
cover of the $910$ threefold roots and the closure of the central parallelogram orbits
(Theorems~\ref{cb:thm:c3} and~\ref{cb:thm:c2}). Lean does not see the records: ...
```

New wording (ar.tex:742-746):
```
Two bookkeeping steps are
computer-assisted because their finite checks are kernel evaluations (\texttt{decide +kernel}): the cover of the $910$
threefold roots, which is Lean-checked (Theorem~\ref{cb:thm:c3}), and the closure of the central parallelogram orbits,
which is Lean-checked according to the record (\dirn{C2FINAL/README.md}, \S6; Theorem~\ref{cb:thm:c2}). Lean does not
see the records: ...
```

The rest of the sentence ("computer-assisted because ... kernel evaluations (decide +kernel)") and the following
sentence are unchanged. The two theorem references now follow the step they belong to, and the record that carries
the qualified label is named. The reference to `cb:thm:c2` still comes right before "every piece named there", so
"there" still points to the two Lean statements.

Map: no change needed. No row of `ar.map.tsv` concerns the C2 or C3 bookkeeping; the note of `ar:rem:classes` ("what
supplies the five class hypotheses and with which rigor label") stays accurate.

## Compile check

From `build/`: `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error ar_wrapper.tex`, twice. Both runs exit 0,
no line starting with `!`, no Overfull box (so 0 boxes > 1pt). Undefined references: only `fd:` labels and the export
labels `cb:thm:c2`, `cb:thm:c3`, `mb:thm:baek`, `mb:thm:classes`, `mb:thm:main3`, `sr:def:classes`, `sr:def:iso`,
`sr:thm:main`, `sr:thm:variant` (expected in the standalone check). Underfull warnings: 32 (the snapshot gives 34;
the ones left in the Coverage list come from long Lean names and were there before).
Rendered text checked with `pdftotext`. No machine path, tool name, "verified", "certified" or "proved" (other than
inside the Lean name `mirrorOneAxis33_proved`) in `ar.tex` or `ar.map.tsv`.
