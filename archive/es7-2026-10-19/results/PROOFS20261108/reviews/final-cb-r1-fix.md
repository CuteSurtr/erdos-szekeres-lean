# Final pass, round 1, section cb: fixes

Files edited: `sections/cb.tex` and `sections/cb.map.tsv` (snapshot before editing: `snapshots/final-r1-pre/`).
Line numbers refer to the edited `sections/cb.tex` (1527 lines, was 1519; the edits add eight source lines). No label
was added, removed or renamed (112 labels, identical list), no statement environment was changed, and the map still has
one row per statement environment (100 rows, same labels).

## Finding 1 (major, rigor label): the three C2FINAL theorems were called plainly "Lean-checked"

- Action: fixed (five places in `cb.tex`, three rows of `cb.map.tsv`).
- Check against the sources (RES = `REPO/cloud/es7-2026-10-19/results`, commit `7e32ee259`):
  - `git ls-files` lists 27 tracked files under `RES/C2FINAL`. None is Lean output. The only output files are the three
    in `C2FINAL/evidence/central34-cover/`: a CaDiCaL run (`exit 20`), a cake_lpr run (`s VERIFIED UNSAT`) and an
    lrat-check run, all on the hull cover CNF.
  - A search of the whole repository (`git grep` at HEAD, and `grep -r` of the working tree) for `Central34`,
    `subcases_reflection`, `closed_are_subcases` and `all_cases_closed` finds only `C2FINAL/Central34Orbits.lean`,
    `C2FINAL/gen_lean.py`, `C2FINAL/README.md`, `C2ENC/class_table.md`, `WRITEUP/SYMMETRIC.md` and
    `AUDIT3/reports/A5_central_geometry.md`. All of them are source or prose. None is a compile, build or axioms log.
    The five log-like files under `AUDIT3` that mention `C2FINAL` are document scans and SAT log comparisons, with no
    Lean output.
  - `C2FINAL/Central34Orbits.lean` has no `import`, no `sorry`, `admit`, `axiom` or `native_decide`, and no
    `#guard_msgs`. It ends with three `#print axioms` commands (ll. 296-298), and their output is not in the
    repository. The only statement of the check is `C2FINAL/README.md` §6: "Core Lean 4.24.0, `decide +kernel`, axioms
    `propext` only, about 6 s".
  - So no Lean output of any kind is saved for a build that includes the file. By fd.tex ll. 76-78 the label of its
    three theorems is "Lean-checked according to the record". The finding is right.
  - By contrast, `C3LEAN/logs/compile.log` (with `C3LEAN/review/logs/main_compile.log`) has the axiom lines of all
    printed C3Cover theorems, so every use of plain "Lean-checked" for C3LEAN stays (ll. 747, 809, 824, 844, 1132,
    1188).
- Lean declarations re-read (`C2FINAL/Central34Orbits.lean`): `Central34.subcases_reflection` (l. 273),
  `Central34.closed_are_subcases` (l. 284) and `Central34.all_cases_closed` (l. 291). Each is a Boolean `List.all` over
  `List.range 8` equal to `true`, proved by `decide +kernel`. The statements of Theorem cb:thm:c2-refl, Fact cb:fact:c2-sub
  and Theorem cb:thm:c2 still match them exactly (conjuncts, the `let` bindings, `k + 1`, `testBit`, `mask`, `refl`,
  `uncovered`, `closed`, `isEmpty`) and were not edited. The heads' "Computer-assisted in Lean" and "Computer-assisted"
  are unchanged, as the finding asks.

### 1a. Paragraph "Axioms" (ll. 78-83, was ll. 78-81)

- Old: "\dirn{C2FINAL/README.md} (\S6) records ``axioms \texttt{propext} only, about 6 s''. The label
  \emph{Lean-checked} for its three theorems rests on that record."
- New: "\dirn{C2FINAL/README.md} (\S6) records ``axioms \texttt{propext} only, about 6 s''. As no Lean output of any
  kind (compile or build log, axiom output, pinned message) is saved for this file, the label of its three theorems
  rests on that record alone: they are \emph{Lean-checked according to the record}, the qualified label defined with
  the rigor labels at the beginning of this document."
- The earlier sentences of the paragraph, which say that no compile or axioms log is committed and that the output of
  the `#print axioms` lines is not in the repository, are unchanged. The pointer to the definition is in words, as in
  sa.tex:114, because no section refers to `fd:sec`, which is not among the listed foundations labels.

### 1b. Paragraph "Rigor labels and dependencies" (ll. 85-89, was ll. 83-84)

- Old: "The Lean theorems keep the label \emph{Lean-checked}; the proofs written here are \emph{written proofs (not
  refereed)}."
- New: "The Lean theorems of \dirn{C3LEAN/C3Cover.lean} keep the label \emph{Lean-checked}, and the three theorems of
  \dirn{C2FINAL/Central34Orbits.lean} (Theorem~\ref{cb:thm:c2-refl}, Fact~\ref{cb:fact:c2-sub} and
  Theorem~\ref{cb:thm:c2}) carry the label \emph{Lean-checked according to the record} (paragraph ``Axioms'' above);
  the proofs written here are \emph{written proofs (not refereed)}."
- The rest of the paragraph is unchanged.

### 1c. After Theorem cb:thm:c2-refl (ll. 1327-1328, was l. 1322)

- Old: "The theorem is Lean-checked by kernel evaluation of the definitions."
- New: "The theorem is Lean-checked according to the record (paragraph ``Axioms'' in \S\ref{cb:sec:overview}), by
  kernel evaluation of the definitions."
- The next sentence ("The following written proof does not use the evaluation.") is unchanged.

### 1d. After Fact cb:fact:c2-sub (ll. 1376-1377, was l. 1370)

- Old: "Lean-checked by kernel evaluation over the explicit lists: for each $a$, ..."
- New: "Lean-checked according to the record (paragraph ``Axioms'' in \S\ref{cb:sec:overview}), by kernel evaluation
  over the explicit lists: for each $a$, ..."

### 1e. After Theorem cb:thm:c2 (ll. 1390-1391, was l. 1383)

- Old: "The theorem is Lean-checked by kernel evaluation; no hand proof is given, ..."
- New: "The theorem is Lean-checked according to the record (paragraph ``Axioms'' in \S\ref{cb:sec:overview}), by
  kernel evaluation; no hand proof is given, ..."

The paragraph reference follows the style of l. 1509 ("the paragraph ``What is not established here'' in
\S\ref{cb:sec:overview}"). It uses only an own label of the section.

### 1f. Map notes (`cb.map.tsv`, rows 97-99)

- cb:thm:c2-refl. Old: "Lean-checked (no committed axioms log; C2FINAL/README.md section 6 records propext only);
  computer-assisted in Lean (decide +kernel); written proof given". New: "Lean-checked according to the record (no saved
  Lean output; C2FINAL/README.md section 6 records propext only); computer-assisted in Lean (decide +kernel); written
  proof given".
- cb:fact:c2-sub. Old: "computer-assisted (decide +kernel on generated lists); no committed axioms log; no hand proof".
  New: "Lean-checked according to the record (no saved Lean output; C2FINAL/README.md section 6 records propext only);
  computer-assisted (decide +kernel on generated lists); no hand proof".
- cb:thm:c2. Old: "export label; computer-assisted (decide +kernel on generated lists closedP1..closedP8); no committed
  axioms log (C2FINAL/README.md section 6 records propext only); no hypotheses". New: "export label; Lean-checked
  according to the record (no saved Lean output; C2FINAL/README.md section 6 records propext only); computer-assisted
  (decide +kernel on generated lists closedP1..closedP8); no hypotheses".
- The three notes were typeset with the functions of `tools/make_appendix.py` (imported, not run). They are ASCII and
  give clean LaTeX. `appendix_map.tex` was not regenerated and is unchanged; it needs `python3 tools/make_appendix.py`
  to pick up the new notes.

### Checked and left unchanged

- Corollary cb:cor:c2 ("(Computer-assisted: a consequence of Theorem~\ref{cb:thm:c2}.)"), its map row ("written step;
  computer-assisted (a consequence of cb:thm:c2)"), Remark cb:rem:c2-scope and the Coverage paragraph (ll. 1459-1464,
  which list the declarations by label) carry no Lean rigor label, so nothing in them rounds the label up.
- l. 1512 ("The Lean-checked files \dirn{AUDIT3/A1_reduction/SizeArith.lean} and ..."). This concerns the files of
  Section sa, whose logs are saved and which sa.tex:105 labels "Lean-checked". It is not about C2FINAL.
- l. 62 ("Both files are checked with Lean~4.24.0.", paragraph "Sources and toolchain"). This names the toolchain and
  is not a rigor label, and the finding does not list it. The paragraph "Axioms" right after it now says that for
  C2FINAL the check rests on `C2FINAL/README.md` §6 alone (which is also where the version 4.24.0 is stated). It is
  left byte-identical, as the final-pass rule asks. If the orchestrator wants it qualified as well, a minimal change
  would be "Both files are checked with Lean~4.24.0 (for \dirn{C2FINAL/Central34Orbits.lean} according to its
  README; see the next paragraph)."
- The phrases quoted in the finding ("the closure of the central parallelogram orbits", "the bookkeeping of the
  subcase orbits") do not occur in cb.tex. They occur in ar.tex:744, mb.tex:1105-1111 and sr.tex:267-269, which are
  outside this fixer's scope. All three already read "Lean-checked according to the record" in their current versions,
  so cb is now consistent with them.

## Finding 2 (minor): "the symmetric $k=7$ theorem" in the paragraph "Treated in another section"

- Action: fixed.
- Check: sa.tex:4 says "the size arithmetic of the reduction of the symmetric $k=7$ statement to its case classes". In
  this document the composite claim holds only conditionally on HalfTurn34, Threefold33 and Fivefold35, and
  "Theorem~A" is the mirror reduction of Section mm (mm.tex:8-11). The finding is right.
- Location: l. 1514 (was l. 1506).
- Old: "(the size arithmetic of the reduction of the symmetric $k=7$ theorem to its case classes)".
- New: "(the size arithmetic of the reduction of the symmetric $k=7$ statement to its case classes)".
- The second "theorem" in the sentence ("an instance of Baek's theorem for abstract configurations") refers to Baek's
  published theorem and is unchanged.

## Compile check

- `build/cb_wrapper.tex` was compiled twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode
  -halt-on-error`. Both runs exit 0, with no `!` errors and no "Missing $". There are 0 overfull boxes (none at all, so 0
  above 1pt). The output has 18 pages.
- Undefined references: only `sa:sec` (1) and `sr:def:classes` (2). Both are other sections' labels, expected in the
  standalone check, and both were present before the edit.
- In the rendered text (pdftotext) the new passages read as intended. In the standalone build the references show as
  "Theorem 1.96, Fact 1.97 and Theorem 1.98" and "§1.1".
- No machine path, no tool name, no `\newcommand` or `\usepackage` in `cb.tex` or `cb.map.tsv`. The only
  hit of "certified" is the pre-existing quotation of the project's term at l. 38, which is unchanged.
