# Final pass, round 1, section sr: fixes

Files edited: `sections/sr.tex` only (snapshot before editing: `snapshots/final-r1-pre/`). `sections/sr.map.tsv` is
unchanged: both edits are in prose (the Dependencies paragraph and an item of Remark sr:rem:records). The map row of
sr:rem:records describes the remark in general terms and says nothing about the label of cb:thm:c2, so it stays
accurate. Line numbers refer to the edited `sections/sr.tex` (1171 lines; the edits add one source line).

## Finding 1 (major, rigor label): the C2FINAL bookkeeping was called plainly "Lean-checked"

- Action: fixed (two places).
- Check against the sources (RES = `REPO/cloud/es7-2026-10-19/results`, commit `7e32ee259`):
  - `git ls-files` of `RES/C2FINAL` lists 27 tracked files. None is Lean output: the only outputs are the three files
    in `C2FINAL/evidence/central34-cover/`, which are a CaDiCaL run, a cake_lpr run (`s VERIFIED UNSAT`) and an
    lrat-check run on the hull cover. They contain no `depends on axioms` line and do not mention Lean.
  - `grep -r` over RES for `Central34Orbits`, `all_cases_closed`, `closed_are_subcases` and `subcases_reflection` finds
    only `C2FINAL/Central34Orbits.lean`, `C2FINAL/gen_lean.py`, `C2FINAL/README.md`, `C2ENC/class_table.md`,
    `WRITEUP/SYMMETRIC.md` and `AUDIT3/reports/A5_central_geometry.md`. All are prose or source, and none is a saved
    build, compile or axioms log. A search of the rest of REPO finds no other file either.
  - `C2FINAL/Central34Orbits.lean` (298 lines, SHA-256 `b396a26b2430...`) ends with three `#print axioms` commands
    (ll. 296-298), and their output is not in the repository. The only statement of the check is `C2FINAL/README.md`
    §6: "Core Lean 4.24.0, `decide +kernel`, axioms `propext` only, about 6 s".
  - By fd.tex ll. 76-78, the label of `Central34.subcases_reflection` (l. 273), `Central34.closed_are_subcases`
    (l. 284) and `Central34.all_cases_closed` (l. 291) is therefore "Lean-checked according to the record". The
    finding is right.
  - By contrast, `C3LEAN/logs/compile.log` has the axiom lines of `C3Cover.all_roots_covered` (`[propext,
    Quot.sound]`), so Theorem cb:thm:c3 keeps "Lean-checked". `H3/logs/print_axioms.log` and
    `V2-L/logs/print_axioms.log` exist as well, so the "Lean-checked" of the H3/V2-L route in sr:rem:records (l. 252) is
    not affected.
- Lean declaration re-read: `Central34.all_cases_closed` (C2FINAL/Central34Orbits.lean:291) is `(List.range 8).all
  (fun k ↦ (uncovered (k + 1) (closed (k + 1))).isEmpty) = true`, proved by `decide +kernel`. Its proof is a kernel
  evaluation, so "computer-assisted" stays. No statement environment of sr was touched. The sr text only refers to the
  theorem as "the bookkeeping of the subcase orbits", which still describes it correctly.

### 1a. Dependencies paragraph (ll. 80-85, was ll. 80-84)

- Old wording:
  "Remarks~\ref{sr:rem:records} and~\ref{sr:rem:main} refer to Theorems~\ref{cb:thm:c2} and~\ref{cb:thm:c3}
  (bookkeeping of two case splits, Lean-checked by kernel evaluation and so computer-assisted), to
  Theorem~\ref{mb:thm:classes}, ..."
- New wording:
  "Remarks~\ref{sr:rem:records} and~\ref{sr:rem:main} refer to Theorems~\ref{cb:thm:c2} and~\ref{cb:thm:c3}
  (bookkeeping of two case splits; both theorems are computer-assisted, as their Lean proofs rest on kernel evaluation,
  and Theorem~\ref{cb:thm:c2} is Lean-checked according to the record, Theorem~\ref{cb:thm:c3} Lean-checked), to
  Theorem~\ref{mb:thm:classes}, ..."
- Reason: the old text gave both theorems the same plain label. The new text separates the two labels. "Rest on kernel
  evaluation" is accurate for both theorems. The proof of cb:thm:c2 is `decide +kernel` itself, and the proof of
  cb:thm:c3 combines a soundness lemma with kernel-evaluated facts, as cb.tex says. The phrase describes what the
  proofs are, as the source shows, and does not claim that Lean accepted the C2FINAL file. The rest of the sentence was
  only re-wrapped.

### 1b. Remark sr:rem:records, item HalfTurn34 (ll. 268-270, was ll. 267-269)

- Old wording:
  "... and on the bookkeeping of the subcase orbits, Lean-checked by kernel evaluation and so computer-assisted
  (Theorem~\ref{cb:thm:c2}; that the listed subcases are refuted rests on the records). A table of the evidence is in
  \dirn{C2ENC/class_table.md} \S1."
- New wording:
  "... and on the bookkeeping of the subcase orbits, Lean-checked according to the record (\dirn{C2FINAL/README.md}
  \S6), by kernel evaluation, and so computer-assisted (Theorem~\ref{cb:thm:c2}; that the listed subcases are refuted
  rests on the records). A table of the evidence is in \dirn{C2ENC/class_table.md} \S1."
- Reason: this is the wording the finding proposes. The parenthesis names the record the label rests on, so that
  "the record" is not confused with "the records" later in the same sentence (the run records of the subcases). The
  Threefold33 item (ll. 275-276, "Lean-checked by kernel evaluation and so computer-assisted (Theorem~\ref{cb:thm:c3};
  ...)") is unchanged, as the finding requires.

### Other places checked

`grep` of sr.tex for `cb:`, `Lean-checked`, `C2FINAL`, `Central34`, `subcase`, `parallelogram`, `bookkeeping` and
`kernel evaluation` finds only these two references to cb:thm:c2 or to the central orbit bookkeeping. Remark
sr:rem:main (ll. 975-987) cites only sr:rem:records, mb:thm:main3 and ar:thm:main. The Coverage paragraph does not
mention C2FINAL. The phrase "the closure of the central parallelogram orbits" does not occur in sr. References to
cb:thm:c2 in other sections (ar, mb, cb) are outside this fixer's scope and were not edited. The sr wording matches the
qualified label "Lean-checked according to the record" that fd.tex l. 78 defines.

## Checks

- Diff against the snapshot: only the two passages above changed (7 old source lines became 8). Everything else is
  byte-identical. The 55 `\label`s are unchanged. `sr.map.tsv` is byte-identical to the snapshot (same SHA-256).
- No machine path and no tool name in `sr.tex` or `sr.map.tsv`. The new source lines are at most 120
  characters long.
- Compile (from `build/`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error sr_wrapper.tex`, twice): exit 0
  both times, 0 errors, no "Missing $", 0 overfull boxes (so 0 above 1pt), no multiply defined labels, no rerun
  request. Undefined references only to `fd:` labels and to the export labels ar:thm:main, cb:thm:c2, cb:thm:c3,
  mb:thm:classes and mb:thm:main3, which is expected in the standalone check. 16 pages. pdftotext shows both new
  passages as intended.
