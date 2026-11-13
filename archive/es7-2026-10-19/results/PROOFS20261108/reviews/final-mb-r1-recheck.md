# Final pass, round 1, section mb: independent re-check

Verdict: **pass**. All five findings are resolved correctly. The edit introduces no blocker and no major finding, and
none remains. Two minor items follow; neither is a defect of `sections/mb.tex` or `sections/mb.map.tsv`.

Paths of records are relative to RES (`cloud/es7-2026-10-19/results`). Other paths are relative to the repository root
or to STAGE, as indicated. I read the sources myself and did not rely on the fix log.

## 1. The five findings

### Finding 1 (minor): "the eight parallelogram hull cases"

**Resolved.** The text now reads "the listed subcases of the eight canonical parallelogram hull cases $P_1,\dots,P_8$
(to which reduction~A reduces the others) meet every orbit of second-layer subcases" (mb.tex ll. 1108-1110).

Checked against the records:
- `C2C34/README.md` §2 has 16 quadrilateral cases `P<a>` and 120 hexagonal ones. Under rotation and reversal of the
  gap sequence, 8 quadrilaterals are canonical (`canonical.txt`). The same README (l. 172) calls them "the other seven
  canonical parallelogram cases".
- `C2FINAL/README.md` §1 item 4: "Case P_a and P_(17−a) are equivalent (reduction A ...), so P1..P8 suffice". So the
  others, $P_9,\dots,P_{16}$, reduce to $P_8,\dots,P_1$.
- `C2FINAL/Central34Orbits.lean` quantifies over `List.range 8` with `a = k + 1` (ll. 273, 284, 291). Its docstring
  says `1 ≤ a ≤ 8`.
- The reading "meet every orbit" is the set form of `all_cases_closed`, through `uncovered` (l. 46). This is
  Corollary cb:cor:c2, and Remark cb:rem:c2-scope uses the same words.

"reduction~A" is not defined in mb. It has an antecedent earlier in the document: sr.tex ll. 266-267, "the reductions
A and B, which pair equivalent parallelogram cases and subcases". The parenthesis also states its role. That is
acceptable for a remark.

### Finding 2 (major, rigor label): closure of the central orbits called plainly "Lean-checked"

**Resolved.** The text now reads "is Lean-checked according to the record (\dirn{C2FINAL/README.md}, \S6), by kernel
evaluation, so computer-assisted (Theorem~\ref{cb:thm:c2})" (mb.tex ll. 1110-1111).

Own checks:
- `find C2FINAL -type f`: 27 files. No compile log, build log or axioms log is among them. The only `.out` files are
  the CaDiCaL, lrat-check and cake_lpr outputs of the hull cover.
- I grepped the whole repository, outside `.git` and `.lake`, for `Central34`, `all_cases_closed`,
  `closed_are_subcases` and `subcases_reflection`. Six files match: the `.lean` file, `C2FINAL/README.md`,
  `C2FINAL/gen_lean.py`, `C2ENC/class_table.md`, `AUDIT3/reports/A5_central_geometry.md` (row 12) and
  `WRITEUP/SYMMETRIC.md` (ll. 127, 207). None of them is Lean output.
- The four `.log`/`.out`/`.txt` files that mention "central34" are SAT and hash records, not Lean output.
- Git history (read-only `git log --all`): no log or axioms file was ever committed under `C2FINAL`.
- `lakefile.toml` builds only the `ErdosSzekeres` library, so no lake build log covers the file.
- The file ends with three `#print axioms` commands (ll. 296-298) whose output is nowhere in the repository. The only
  statement of the check is `C2FINAL/README.md` §6: "Core Lean 4.24.0, `decide +kernel`, axioms `propext` only, about
  6 s".
- By fd.tex ll. 76-78, the label is therefore "Lean-checked according to the record".
- All three proofs are `decide +kernel` (ll. 281, 288, 292), so "by kernel evaluation, so computer-assisted" stays
  right.
- The wording agrees with cb.tex (paragraph "Axioms", ll. 78-83; ll. 1327, 1376, 1390), sr.tex ll. 268-269 and
  ar.tex ll. 744-745.

Other places in mb:
- "Lean-check" occurs at mb.tex ll. 110, 112, 846, 886, 931, 1017, 1052, 1079, 1110, 1115, 1123 and 1129. Only
  l. 1110 concerns C2FINAL.
- l. 110 ("Every Lean declaration stated below is Lean-checked") is about the declarations stated in this section.
  cb:thm:c2 is cited, not stated, so the fixer was right to leave it.
- l. 1115 (C3LEAN) keeps "Lean-checks": `C3LEAN/logs/compile.log` l. 18 prints the axioms of `all_roots_covered`.
- l. 1123 keeps "Lean-checked": `LAYERLEAN/logs/axioms.log` ll. 3 and 5 print `layers_are_orbits` and
  `strict_nesting`.

The map row `mb:rem:main3` (note) was changed to match the text. Rendered with the generator's own functions, it
gives "... is Lean-checked according to the record (Theorem~\ref{cb:thm:c2}) or Lean-checked
(Theorem~\ref{cb:thm:c3}), in both cases by kernel evaluation, so computer-assisted". This is correct. No other row of
mb.map.tsv mentions Lean-checked.

### Finding 3 (minor): mm:thm:even in the main "We use" list

**Resolved.** I classified every cross-section `\ref` of mb.tex by its enclosing environment with my own script:
- `mm:thm:even` occurs only in Remark mb:rem:eight (l. 907), in the Dependencies paragraph and in Coverage (l. 1196).
  No proof uses it.
- Exactly three remarks cite results that no proof uses:
  - mb:rem:generated cites fd:lem:pos-cycle;
  - mb:rem:eight cites mm:thm:even;
  - mb:rem:main3 cites ll:thm:layers, lg:thm:nesting, cb:thm:c2 and cb:thm:c3.
- Remark mb:rem:seven cites only results that proofs also use. mm:thm:odd is used in the proof of Theorem
  mb:thm:nine(b),(c), l. 977. mm:thm:mirror-polygon and mm:thm:axis-polygon are used at ll. 656 and 659.
- Every item left in the main list occurs in a proof, in a statement, or in Conventions.

The parenthesis "on the second Lean proof `mirror_eight'` of Theorem mb:thm:eight(a)" is correct:
- `MirrorOdd.mirror_eight'` (MirrorMain.lean:2636) has exactly the signature of `mirror_eight` (l. 1820).
- It is proved by `mirror_even_general 4 22 ... capacity22g ...`.

The Coverage mention of mm:thm:even (results that are the subject of another section) is unchanged and consistent.

### Finding 4 (minor): [n] used both generically and as the codomain

**Resolved**, with the requested wording verbatim (mb.tex ll. 119-121).
- `mb:ssec:bridge` is the subsection "From configurations to points of the plane" (l. 255), where
  $f\colon[k]\to[n]$ is introduced.
- Lean (`ErdosSzekeres/Omission/Realization.lean`): `Configuration (n : ℕ)` has `point : Fin n → Point` (l. 9).
  `HasCap` takes `f : Fin k → Fin n` (l. 64).
- So the domain is `Fin k` and the codomain is `Fin n`, as the new sentence says.
- The generic "$[m]$ ... `Fin m`" matches mm.tex ll. 95-97.

### Finding 5 (minor): Schroeder's archive without a pointer to the References

**Resolved.** The text now reads "M.~Schroeder's archive~\cite{Sch26}" (mb.tex l. 47).
- `bibliography.tex` has `\bibitem{Sch26}`: the version-1 archive of 19 September 2026, doi:10.5281/zenodo.22842891.
- `docs/THIRD_PARTY.md` names the same archive and DOI (ll. 46-48). Its ll. 111-119 say that the connections of
  `Realization.lean` were "added here, using the archive's balanced-state/cycle strategy". The adaptation header of
  `ErdosSzekeres/Omission/Baek.lean` (ll. 2-3) carries the same DOI.
- With a scratch wrapper that also inputs the bibliography (`build/mb_final_recheck_r1_bib.tex`, two passes, exit 0,
  no citation warning), the citation resolves as "[9] M. Schroeder, ...".

## 2. Diff review (snapshot `snapshots/final-r1-pre/` against `sections/`)

`diff -u` of mb.tex shows four hunks:
- Sources (finding 5);
- Dependencies and rigour (finding 3);
- Conventions (finding 4);
- Remark mb:rem:main3, item HalfTurn34 (findings 1 and 2).

`diff -u` of mb.map.tsv shows one hunk, the note of row mb:rem:main3 (finding 2).

Every hunk was checked as a referee:
- **Mathematics and fidelity.** No statement environment was touched. The Lean sources behind the edited sentences
  (`Central34Orbits.lean` ll. 1-48, 267-298; `Realization.lean` ll. 9-13, 64-66; MirrorMain.lean ll. 1820, 2636)
  match the new wording.
- **Records.** Every claim was checked in RES (§1 above).
- **Rigor labels.** C2FINAL is now correctly qualified. C3LEAN and LAYERLEAN keep "Lean-checked" and have saved logs.
  Nothing is rounded down. "computer-assisted" is kept. No hypothesis is presented as proved, and cake_lpr remains the
  anchor in the remark.
- **Paths and names.** No machine path and no tool name occurs in mb.tex or mb.map.tsv. The only grep hit
  was a substring of `smallmatrix`, a false positive.
- **LaTeX.** No `\newcommand`, `\usepackage` or "verified"/"certified" occurs. `\texttt{...\textquotesingle}` follows
  the existing usage in Remark mb:rem:seven and in Coverage.
- **Labels.** The sequence of the 57 `\label`s is identical.
- **Map.** 43 lines, 5 tab-separated fields each, ASCII only. The rows pass the checks of `tools/make_appendix.py`
  (header, field count, ASCII, kind, prefix, label defined). I rendered them with its functions and wrote nothing:
  only row mb:rem:main3 changes.
- Nothing outside the findings changed.

## 3. Compile

Wrapper `build/mb_final_recheck_r1_wrapper.tex` (same content as the contract wrapper), run twice from `build/` with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`:
- Exit 0 both times. 0 errors, 0 "Missing", 0 overfull boxes. No multiply defined labels, no rerun request. 16 pages.
- Undefined references, all expected in the standalone check:
  - `fd:` labels;
  - export labels of other sections: ar:thm:main, cb:thm:c2, cb:thm:c3, lg:thm:nesting, ll:thm:layers,
    mm:def:config, mm:lem:slope, mm:thm:axis-polygon, mm:thm:even, mm:thm:line, mm:thm:mirror-polygon, mm:thm:odd,
    mm:thm:small, sr:def:classes, sr:def:iso, sr:thm:main;
  - the citation `Sch26`, because the wrapper has no bibliography. It resolves in the full document (§1, finding 5).
- Underfull boxes: 3, against 2 for the snapshot built the same way (`build/mb_final_recheck_r1_base.tex`). The extra
  one is a page-level underfull vbox at the page-2 break of the standalone build, caused by a pagination shift. I
  rendered page 2 and it looks normal. Pages 1 and 2 typeset the new sentences as intended.

## 4. Findings

1. **minor** (process, outside mb's edit scope). `appendix_map.tex` is stale: it was generated at 21:39, before this
   fix. Its row "Rem. mb:rem:main3" (l. 399) still reads "the case-split bookkeeping (Theorem~\ref{cb:thm:c2},
   Theorem~\ref{cb:thm:c3}) is Lean-checked by kernel evaluation, so computer-assisted". Until it is regenerated, the
   full document keeps the rounded-up label in the appendix.
   - Fix: run `python3 tools/make_appendix.py` from STAGE before the final build. With the current map, that row
     becomes the corrected note and no other mb row changes.
2. **minor** (outside mb's edit scope, invisible in the PDF). The header comment of `bibliography.tex` (l. 1) says "The
   sections cite them inline, by author and title". Section mb now also cites `Sch26` by key, and the front matter's
   "Works cited" paragraph has since been reworded.
   - Fix (optional): update the comment, for example "The sections cite them inline, mostly by author (Section mb also
     by key); ...".

## 5. Observations (no finding)

- **Short Lean name.** The new parenthesis writes `mirror_eight'` without its namespace `MirrorOdd.`. fd.tex ll. 42-44
  says that names outside `ErdosSzekeres` are always written in full. Section mb, however, writes `MirrorOdd` names
  short in running text throughout: about 40 occurrences predate this edit, including this very name in Coverage.
  Remark mb:rem:eight gives the full name. The new text follows the section's practice, and changing that practice is
  outside this final pass.
- **Citation in a section.** The contract's standalone rule names only undefined references. The undefined citation is
  of the same kind, a key defined in another input file of `proofs.tex`, and it resolves there.
