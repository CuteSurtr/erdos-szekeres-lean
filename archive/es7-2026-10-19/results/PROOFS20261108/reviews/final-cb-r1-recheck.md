# Final pass, round 1, section cb: independent re-check

**Verdict: pass.** No blocker or major finding remains, and the edit introduces none. Both findings are fixed
correctly. Three minor, optional observations follow at the end; none needs a change in the final pass.

Paths: STAGE-relative for the document files, RES-relative for the records (RES at commit `7e32ee259`). Line numbers
refer to the current `sections/cb.tex` (1527 lines; the snapshot `snapshots/final-r1-pre/cb.tex` has 1519).

## Finding 1 (major, rigor label): fixed

### The premise, checked in RES (I did not rely on the fix log)

- `C2FINAL` has 27 files: `git ls-files` and `find` give the same list. The only output files are the three in
  `C2FINAL/evidence/central34-cover/`: `cad_hc34_coverL.out` (a SAT solver run, `exit 20`),
  `chk_hc34_cover_cake_lpr.out` (`s VERIFIED UNSAT`) and `chk_hc34_cover_lrat-check.out`. All three are SAT tool
  output on the hull-cover CNF. None of them is Lean output. No file in `C2FINAL` contains "depends on axioms",
  "does not depend on any axioms" or a build line, and `README.md` is the only file there that mentions `propext`.
- Repository-wide search (`git grep` at HEAD, and `grep -r` of the working tree without `.git` and `.lake`):
  `Central34`, `Central34Orbits`, `subcases_reflection`, `closed_are_subcases` and `all_cases_closed` occur only in
  `C2FINAL/{Central34Orbits.lean, README.md, gen_lean.py}`, `C2ENC/class_table.md`, `WRITEUP/SYMMETRIC.md` and
  `AUDIT3/reports/A5_central_geometry.md`, all of them source or prose. Other non-prose files that mention `C2FINAL`
  (logs and TSVs under `AUDIT3`, the manifests under `REPLAY`, the JSON files in `C2FINAL/review`) are document scans,
  hash records or SAT-log comparisons. None contains Lean output. No build script compiles the file.
- `C2FINAL/Central34Orbits.lean` (298 lines, SHA-256 `b396a26b2430`...) has no `import`, `sorry`, `admit`, `axiom`,
  `native_decide`, `+native`, `ofReduceBool`, `ofReduceNat`, `skipKernelTC`, `#guard_msgs` or `set_option`. Its only
  theorems are `subcases_reflection` (l. 273), `closed_are_subcases` (l. 284) and `all_cases_closed` (l. 291). Each is
  a Boolean `List.all` over `List.range 8` set equal to `true` and proved by `decide +kernel`. The three
  `#print axioms` commands are at ll. 296-298.
- `C2FINAL/README.md` §6 (l. 153): "Core Lean 4.24.0, `decide +kernel`, axioms `propext` only, about 6 s". §8 (l. 204)
  records the reviewer's Lean check, again in prose only. The quotation at cb.tex:80 is accurate.
- So no saved Lean output exists for a build that includes the file. By the rule of Section fd (now fd.tex:84-86;
  fd.tex was edited by its own fixer at 21:53, but only the text search of kind (a) changed and this rule is
  unchanged), the three theorems are *Lean-checked according to the record*. By contrast,
  `C3LEAN/logs/compile.log` contains the axiom lines (for example l. 18: `all_roots_covered` depends on
  `[propext, Quot.sound]`), so the plain label for C3LEAN stays. That is right.

### The current text, place by place

- **Axioms paragraph (cb.tex:78-83).** It now says that no Lean output of any kind is saved for the file and gives the
  qualified label. The pointer "the qualified label defined with the rigor labels at the beginning of this document"
  is correct: the label is defined in fd's paragraph "Rigor labels", in the first numbered section after the front
  matter. The same wording appears at sa.tex:116. "rests on that record alone" is also accurate: the other records
  that call the bookkeeping Lean-checked (`WRITEUP/SYMMETRIC.md`, `AUDIT3/reports/A5_central_geometry.md`) repeat
  the claim and add no Lean output.
- **Rigor labels and dependencies (cb.tex:85-88).** The theorems of `C3LEAN/C3Cover.lean` keep *Lean-checked*. The
  three C2FINAL theorems, cited by their labels cb:thm:c2-refl, cb:fact:c2-sub and cb:thm:c2, carry *Lean-checked
  according to the record*. Correct. The C3LEAN label is not rounded down, and the sentence still reads well.
- **After the three statements (cb.tex:1327-1329, 1376-1379, 1390-1391).** Each now gives the qualified label and
  points to the Axioms paragraph through the section's own label `cb:sec:overview` (the paragraph lies in that
  subsection, ll. 3-104). The heads ("Computer-assisted in Lean ...; written proof below" and "Computer-assisted"),
  the statements and the rest of each sentence are byte-identical to the snapshot.
- **cb:cor:c2, cb:rem:c2-scope and the Coverage paragraph (ll. 1400-1405, 1418-1432, 1459-1464).** None of them gives
  the C2FINAL theorems a Lean rigor label, so nothing there needed to change. I agree with the fixer.
- **Remaining plain uses.** Every other plain "Lean-checked" in cb.tex (ll. 747, 809, 824, 844, 1132, 1188, and
  "Lean checks" at l. 1003) is in the C3 subsections (ll. 162-1193) and refers to C3LEAN theorems. l. 1512 refers to
  the files of Section sa, whose logs are saved.
- **Map rows 97-99 (cb.map.tsv).** Only the note column changed. Each note now starts with "Lean-checked according to
  the record (no saved Lean output; C2FINAL/README.md section 6 records propext only)", and the computer-assisted
  parts of the notes are kept. The file has 5 tab-separated fields per row, is ASCII, and still has 100 rows with the
  same labels in the same order.
- **Consistency with the other sections.** ar.tex:745, mb.tex:1110, sr.tex:83 and sr.tex:268 already use the
  qualified label for cb:thm:c2, and mb.map.tsv (row mb:rem:main3) was updated in this round as well. cb now agrees
  with all of them. mb.tex:109 ("Every Lean declaration stated below is Lean-checked") refers to mb's own
  declarations, not to cb:thm:c2.
- **Fidelity.** I re-read the Lean source of the three touched statements. Theorem cb:thm:c2-refl, Fact cb:fact:c2-sub
  and Theorem cb:thm:c2 still match it exactly (the conjuncts, the `let` bindings, `k + 1`, `testBit`, `mask`,
  `refl`, `uncovered`, `closed`, `isEmpty`). They were not edited.

## Finding 2 (minor): fixed

cb.tex:1512-1516 now reads "the size arithmetic of the reduction of the symmetric $k=7$ statement to its case
classes", in the same words as sa.tex:4. "Theorem A" is not used (mm.tex:10 reserves that name for the mirror
reduction). The second "theorem" in the sentence ("an instance of Baek's theorem") names Baek's published theorem and
is correctly left unchanged.

## Diff review (`diff -u` against `snapshots/final-r1-pre/`)

- cb.tex has five hunks: the Axioms and Rigor paragraphs, the three sentences after the statements, and the paragraph
  "Treated in another section". cb.map.tsv has three changed rows (97-99, note column only). Nothing else changed.
- Labels: 112 before and after, the identical list. There are 100 statement environments, and their labels and kinds
  match the 100 map rows. The new `\ref`s point only to the section's own labels (`cb:thm:c2-refl`, `cb:fact:c2-sub`,
  `cb:thm:c2`, `cb:sec:overview`), and the set of referenced labels has not grown. The external references are still
  only `sa:sec` and `sr:def:classes`.
- No machine path, no tool name, and no `\newcommand`, `\def` or `\usepackage` in cb.tex or cb.map.tsv.
  None of "verified", "certified", "proved" or "proven" appears in any added line.
- The LaTeX is sound: `\emph` for the label where the paragraph defines or assigns it (as fd does), plain text in the
  running sentences (as the earlier "Lean-checked by kernel evaluation" was), and `\S\ref{...}` as at l. 1509.

## Compile check

- `build/cb_final_recheck_r1_wrapper.tex` is identical to the contract wrapper (and to `build/cb_wrapper.tex`). I
  compiled it twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
- Both runs exit 0, with no `!` error, no "Missing $" and no overfull box (so none above 1pt). The output has 18 pages.
- Undefined references: only `sa:sec` (1) and `sr:def:classes` (2), labels of other sections, as expected
  standalone.
- On this fresh wrapper the second run warned "Label(s) may have changed". A third run was stable: the `.aux` did not
  change between runs 2 and 3, and the warning went away. This is the normal settling of a new `.aux` file, not a
  defect.
- In the text extracted from the PDF, the new passages read as intended ("Theorem 1.96, Fact 1.97 and Theorem 1.98",
  "§1.1" in the standalone numbering).

## Remaining observations (minor, optional; not required in the final pass)

1. **appendix_map.tex is stale.** This is a pipeline step, not a defect in cb's files. Rows 498-500 still carry the old
   notes, and the first of them still reads plainly "Lean-checked (no committed axioms log; ...)". Row 399, from mb's
   map, is also out of date. I ran `tools/make_appendix.py` on a copy of `sections/` inside `build/`; the real appendix
   was not touched and the copy has been removed. It produced 470 rows without error. The cb rows differ from the
   current appendix exactly in these three rows, and the new notes typeset as clean LaTeX. Run
   `python3 tools/make_appendix.py` before the final build.
2. **cb.tex:62, "Both files are checked with Lean~4.24.0."** For C2FINAL this fact is known only from the README.
   The sentence names the toolchain (fd.tex:46 makes the same unqualified statement for the whole document), and the
   Axioms paragraph a few lines later says that the C2FINAL check rests on the record alone, so a reader is not misled.
   If wanted, the fixer's suggested wording would work: "(for \dirn{C2FINAL/Central34Orbits.lean} according to its
   README; see the next paragraph)".
3. **The definitions of C2FINAL (cb:def:inner to cb:def:closed).** fd.tex:84-86 applies the qualified label to "the
   label of its declarations". For a definition, the label records only that Lean accepted it (fd.tex:116-118), and
   for this file that acceptance also rests on the README. The Axioms paragraph names only "its three theorems". A
   definition asserts nothing, so no claim is overstated. Optional wording: "the label of its declarations rests on
   that record alone: its three theorems are *Lean-checked according to the record*, ...".
