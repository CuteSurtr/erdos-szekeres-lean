# Final pass, round 1, section sr: independent re-check

Verdict: **pass**. No blocker, no major and no minor finding. The fix of finding 1 is correct. The edit changed only the
two passages that the finding names, and it introduced nothing new.

Paths: `STAGE` = the staging area, `RES` = `REPO/cloud/es7-2026-10-19/results` (commit `7e32ee259`), as in CONTRACT.md.

## Finding 1 (major, rigor label): resolved

I checked the sources myself and did not rely on the fix log.

- **No Lean output for C2FINAL.** `git ls-files` lists 27 tracked files under `RES/C2FINAL`. None of them is Lean
  output. The three files in `C2FINAL/evidence/central34-cover/` are a CaDiCaL run, a cake_lpr run
  (`s VERIFIED UNSAT`) and an lrat-check run. None of them mentions Lean or axioms.
- **Search of the whole worktree.** I searched for `Central34Orbits`, `all_cases_closed`, `closed_are_subcases`,
  `subcases_reflection` and `Central34.`. The search finds only these files:
  `C2FINAL/Central34Orbits.lean`, `C2FINAL/gen_lean.py`, `C2FINAL/README.md`, `C2ENC/class_table.md`,
  `WRITEUP/SYMMETRIC.md` (ll. 127, 207) and `AUDIT3/reports/A5_central_geometry.md` (l. 45). All of them are source
  or prose. None is a compile log, a build log, axiom output or a pinned message.
- **The Lean file.** `C2FINAL/Central34Orbits.lean` has 298 lines and SHA-256 `b396a26b2430…`. It imports nothing
  (core Lean). Its three theorems are `subcases_reflection` (l. 273), `closed_are_subcases` (l. 284) and
  `all_cases_closed` (l. 291), and each is proved by `decide +kernel`. The three `#print axioms` commands at
  ll. 296–298 have no saved output.
- **The record.** `C2FINAL/README.md` §6 is headed "Lean check of the bookkeeping". It records "Core Lean 4.24.0,
  `decide +kernel`, axioms `propext` only, about 6 s". Under `fd.tex` ll. 76–78, the right label is therefore
  "Lean-checked according to the record", and the finding is right.
- **Consistency with other sections.** `cb.tex` (ll. 78–88, 1327, 1376, 1390) uses the same qualified label for all
  three theorems. `ar.tex` ll. 744–745 and `mb.tex` ll. 1110–1111 use the same wording ("Lean-checked according to the
  record (C2FINAL/README.md, §6), by kernel evaluation, so computer-assisted"). The sr text now agrees with all three.
- **cb:thm:c3 correctly stays "Lean-checked".**
  - `C3LEAN/logs/compile.log` l. 18 reads `'C3Cover.all_roots_covered' depends on axioms: [propext, Quot.sound]`.
  - Its kernel-evaluated inputs (`batch0`… at l. 1740, `roots_codes_match` at l. 1725) are proved by
    `decide +kernel`.
  - The only occurrence of `native_decide` in `C3Cover.lean` is in a comment (l. 13).
  - So "Lean-checked" and "rest on kernel evaluation" are both true for cb:thm:c3, and cb.tex labels it
    computer-assisted.
- **Other places in sr.** I searched sr.tex for `cb:`, `C2FINAL`, `Central34`, `central`, `subcase`, `parallelogram`,
  `bookkeeping`, `kernel`, `closure` and `according to the record`.
  - Only the two edited passages (ll. 80–85 and 268–270) refer to cb:thm:c2 or to the central orbit bookkeeping.
  - The Threefold33 item (ll. 275–276) still gives plain "Lean-checked" to cb:thm:c3. That is correct.
  - Remark sr:rem:main (ll. 975–987) says nothing about cb:thm:c2.
  - The Coverage paragraph does not mention C2FINAL.
  - The phrase "the closure of the central parallelogram orbits" does not occur in sr.
  - The other occurrences of "Lean-checked" in sr (ll. 70, 248, 253, 289, 976, 980, 1023, 1066, 1075) concern the
    SYMLEAN declarations and the H3/V2-L route. `H3/logs/print_axioms.log` and `V2-L/logs/print_axioms.log` exist, so
    the finding does not affect them.
- **Map.** `sections/sr.map.tsv` is byte-identical to the snapshot (SHA-256 `104dc98d…`). The row for sr:rem:records
  ("with the rigor labels that the records claim") is still accurate, so the map needs no change.

## Diff review (snapshot `snapshots/final-r1-pre/` against `sections/`)

- **Scope of the change.**
  - `diff -u` of sr.tex shows two hunks. A word-level diff shows exactly the intended insertions and nothing else.
  - The line count went from 1170 to 1171, and the 55 `\label`s are identical.
  - `diff -u` of sr.map.tsv is empty.
- **Hunk 1 (Dependencies, ll. 80–85).**
  - The new text says that both cb:thm:c2 and cb:thm:c3 are computer-assisted. That matches cb.tex: cb:thm:c2 is
    marked "(Computer-assisted.)" and cb:thm:c3 "(Computer-assisted: the proof uses Facts …)".
  - It says that their Lean proofs rest on kernel evaluation, which is true (see above).
  - It gives cb:thm:c2 the label "Lean-checked according to the record" and cb:thm:c3 the label "Lean-checked".
  - The rest of the sentence is unchanged and still true: `\ref{cb:…}` occurs only at ll. 81–83, 269 and 276, all of
    them in prose and none inside a proof.
- **Hunk 2 (Remark sr:rem:records, HalfTurn34 item, ll. 268–270).**
  - The record it cites exists under that number (README §6) and states the check.
  - The parenthesis separates "the record" from "the records" that come later in the same sentence.
  - "computer-assisted" is kept.
- **Rigor labels.** No label was rounded up. The only label that changed is cb:thm:c2's plain "Lean-checked", which
  became the qualified form the finding asked for.
- **Statements.** No statement environment changed. I re-read `Central34.all_cases_closed` (l. 291:
  `(List.range 8).all (fun k ↦ (uncovered (k + 1) (closed (k + 1))).isEmpty) = true := by decide +kernel`). The prose
  "bookkeeping of the subcase orbits" still describes it correctly.
- **Hygiene.**
  - No machine path and no tool name appears in sr.tex or sr.map.tsv.
  - The edit adds no macro and no package.
  - Paths use `\dirn` and contain no spaces.
  - `\S6` renders as "§6".

## Compile

- **Runs.** I compiled `build/sr_final_recheck_r1_wrapper.tex`, which has the same content as the contract wrapper,
  twice from `build/`. Both runs exited with 0. The log has no `!` lines and no "Missing $".
- **Boxes.** There are no overfull boxes, so none above 1pt. None of the 49 underfull warnings falls in the paragraphs
  of the two edits.
- **References and labels.**
  - The only undefined references are to `fd:` labels and to the export labels ar:thm:main, cb:thm:c2, cb:thm:c3,
    mb:thm:classes and mb:thm:main3. These are expected in the standalone check.
  - No label is defined twice.
- **Output.** The PDF has 16 pages. pdftotext shows both new passages as intended.

## Findings

None.
