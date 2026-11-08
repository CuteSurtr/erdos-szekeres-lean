# Section `lg`, whole-document review round 1 (docfix-r1): fix log

Inputs: five findings for `lg` from the whole-document review, round 1:
`reviews/doc-r1-xref-fdlllg.md` F3 (finding 1), `reviews/doc-r1-consistency.md` m17 (finding 2) and m19 (finding 3),
`reviews/doc-r1-completeness.md` M1 (finding 4), and `reviews/doc-r1-typesetting.md` F13 (finding 5). Findings 2 and 5
are the same issue. Pre-edit snapshot: `snapshots/docfix-r1-pre/lg.tex` (SHA-256 `bd3334147037`, 945 lines) and
`snapshots/docfix-r1-pre/lg.map.tsv` (SHA-256 `d7c6131c5b54`, 32 lines). Paths are relative to STAGE (`sections/`,
`build/`, `reviews/`, `snapshots/`) or, for Lean sources and records, to the results directory. `lg.tex:N` refers to
the file after the fix (SHA-256 `7b314e52fe64`, 966 lines).

All five findings resolved: 5 fixed, 0 declined.

## Summary

| # | finding | severity | action | location after the fix |
|---|---|---|---|---|
| 1 | [xref-fdlllg F3] the Dependencies paragraph lists Lemma `fd:lem:pos-triples` and says all listed results are recalled in §3.1, which does not recall that lemma | minor | fixed with the reviewer's first option: "These, except Lemma `fd:lem:pos-triples`, which is used only in Step 3 of the proof of Theorem `lg:thm:fan`, are recalled in §`lg:ssec:notation`." | `lg.tex:112-114` |
| 2 | [consistency m17] `\subsection*{Coverage}` puts an unnumbered "Coverage" line in the contents between 3.6 and 4 | minor | fixed: `\paragraph{Coverage.}`, followed directly by the text, as in ll, fd, ec, mb, mm, pc, sa and sr. The second part of the suggestion (the same change in oc and cb) is outside this fixer's files | `lg.tex:895` |
| 3 | [consistency m19] "The log LAYERLEAN/logs/build.log records exit code 0 and no messages. That log names no file hash" still reads as a record of the present file | minor | fixed, in line with the ll fix (`ll.tex:35-38`): the log (exit code 0, no messages) names no file hash; it was committed with the first version of the file (454 lines, commit `6429e9a70`) and was not updated by the five later commits that changed the file, so it is not a record of the present file and is not used. The two records of the present file (REPORT.md item 1; the 6 November re-check) are now named as such, and the toolchain sentence now points to the re-check's `README.txt` and `run.sh` | `lg.tex:54-64` |
| 4 | [completeness M1, major] the 19 declarations of `LEANEXT/review/tests_tail.lean` (= `VacuityTest.lean` lines 1149-1297) are neither covered nor listed; VacuityTest.lean is described only as one of eight copies of lines 11-1147 | major | fixed: a new item in "Deliberately not covered" names the 19 declarations (3 definitions, 16 theorems), says that they are non-vacuity tests, not results (REPORT.md item 6), and says what they state and which theorems they apply. The VacuityTest.lean entry in the copies list now says "(all 1148 lines, followed by the tests of the next item)", and the new item describes the file as LayerLemma.lean 1-1148 followed by tests_tail.lean | `lg.tex:941` (copies list), `lg.tex:944-960` (new item) |
| 5 | [typesetting F13] the same `\subsection*{Coverage}`: unnumbered contents line and unnumbered level-2 bookmark | minor | fixed by the change of finding 2 | `lg.tex:895` |

No statement environment, label or Lean head was added, removed or changed, so `lg.map.tsv` needed no edit. It is
unchanged (31 rows, which match the 31 labelled statement environments one to one; heads and map agree on every Lean
name and file:line, checked with a script).

## Check against the sources

- **Finding 1.** In `lg.tex`, `fd:lem:pos-triples` occurs only in the Dependencies list and in Step 3 of the proof of
  Theorem `lg:thm:fan` (`lg.tex:700` after the fix). §3.1 (Notation and the results used) recalls all the other listed
  results: `fd:def:point`, `fd:def:orient`, `fd:def:gp`, `fd:def:cp`, `fd:def:ngon`, `fd:def:inv`, `fd:def:rot`,
  `fd:lem:orient`, `fd:lem:collinear`, `fd:lem:mono`, `ll:def:hv`, `ll:def:peel`, and (L1)-(L4) for `ll:lem:hv`,
  `ll:lem:antitone`, `ll:lem:inv-peel` and `ll:thm:core-rot`. The finding is correct.
- **Findings 2 and 5.** Before the fix `lg.tex:890` was `\subsection*{Coverage}`. ll, fd, ec, mb, mm, pc, sa and sr use
  `\paragraph{Coverage.}`; ar uses `\paragraph{\textbf{Coverage.}}`; oc and cb use numbered `\subsection`s. The
  findings are correct. lg defines no label on its Coverage heading, so nothing refers to it.
- **Finding 3.**
  - `LAYERLEAN/logs/build.log` has three lines (command, exit code 0, "messages: 0 lines") and names no file or hash.
  - The present `LAYERLEAN/LayerLemma.lean` has 1148 lines and SHA-256 `afb8542dceb0...` (shasum).
  - The history (build.log last committed in `6429e9a70`, with a 454-line LayerLemma.lean; the file then changed in
    five later commits, the last `393619a57`) is taken from two independent reviews that agree:
    `reviews/doc-r1-consistency.md` M3 and `reviews/fd-r2-rigor.md` m1. It also agrees with the inventory
    (`inventory/LAYERLEAN.json`: last change of the file `393619a57`) and with the ll fix (`ll.tex:35-38`).
  - git was not run in this fix, because it is not on the allowed command list.
  - REPORT.md item 1 reads "Build. Exit 0, no messages." for the reviewed file `afb8542d...`, 1148 lines.
  - `LAYERLEAN/logs/axioms_recheck_20261106/README.txt` gives the repository root, Lean 4.24.0 and Mathlib `f897ebcf`.
    `run.sh` runs `lake env lean`. So the method sentence at `lg.tex:54` rests on a record of the present file.
  - The first 1148 lines of `LayerLemmaAxioms.lean` are byte-identical to LayerLemma.lean (checked with cmp).
  - LayerLemma.lean contains none of the words sorry, admit, axiom or native_decide (grep -w, 0 hits).
- **Finding 4.**
  - `LEANEXT/review/tests_tail.lean` has 149 lines. In namespace `ErdosSzekeres.LayerLemma.Review` it declares the
    definitions `L4` (12), `S4` (15) and `H6` (124), and the theorems `mem_S4` (17), `card_S4` (21), `angle4` (23),
    `rot4` (25), `hc4` (30), `inv4` (35), `gp4` (41), `inner4` (54), `hno4` (69), `hv4` (77), `peel1_4` (91),
    `nest4` (96), `orbit4` (102), `layers4` (106), `chain4` (117) and `inv6` (128). That is 19 declarations. The file
    ends with `#print axioms`, `#check` and `#print` commands (lines 141-149).
  - `LEANEXT/review/VacuityTest.lean` has 1297 lines. Its lines 1-1148 match `LAYERLEAN/LayerLemma.lean` byte for
    byte, and its lines 1149-1297 match `tests_tail.lean` byte for byte (both checked with cmp). The 19 declarations sit
    at lines 1160-1276 (grep).
  - The descriptions in the new item were checked against the Lean text:
    - `L4` lists (2,0), (0,2), (-2,0), (0,-2), (1/2,1/2), (-1/2,1/2), (-1/2,-1/2), (1/2,-1/2).
    - `hc4`: `(0 : Point) ∉ S4`.
    - `inv4`: `Invariant (rotAbout 0 (2 * Real.pi / ((4 : ℕ) : ℝ))) S4`.
    - `gp4`: `GeneralPosition S4`.
    - `hno4`: `¬ HasConvexNGon 8 S4`.
    - `hv4`: `![2, 0] ∈ hullVerts S4`.
    - `peel1_4`: `![1/2, 1/2] ∈ peel S4 1`.
    - `nest4` applies `strict_nesting`, `orbit4` applies `hullVerts_eq_orbitFS_rotAbout`, `layers4` applies
      `layers_are_orbits` and `chain4` applies `chain_clauses_sound`, each with m = 4 and K = 8.
    - `H6` lists (1,0), (1/2, √3/2), (-1/2, √3/2), (-1,0), (-1/2, -√3/2) and (1/2, -√3/2). These are
      (cos(kπ/3), sin(kπ/3)) for 0 ≤ k < 6.
    - `inv6`: `Invariant (rotAbout 0 (2 * Real.pi / ((6 : ℕ) : ℝ))) H6`.
  - REPORT.md item 6 is "Vacuity test (tests_tail.lean, run inside VacuityTest.lean; Lean-checked)".
  - No other section file mentions `tests_tail.lean`, `VacuityTest.lean` or the namespace (grep over `sections/*.tex`).
    So "which no section covers" is accurate.
  - The new item cites `lg:thm:nesting`, `lg:thm:chain` (lg's own labels) and `ll:thm:core-rot`, `ll:thm:layers`. The
    last two are ll export labels, defined in `ll.tex` on the theorems for `hullVerts_eq_orbitFS_rotAbout` and
    `layers_are_orbits`.
  - The new text calls the tests neither proved nor checked. It says only what their Lean statements state and which
    theorems they apply.
  - The finding is correct.

## Compile check

From `build/`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error lg_wrapper.tex` was run twice.
- Both runs exit 0.
- There are no errors, no "Missing"/"Runaway" messages and no overfull boxes (0 in all, so 0 above 1pt).
- The undefined references are only fd and ll export labels, as expected in the standalone check:
  - 11 fd labels;
  - 9 ll labels: `ll:def:hv`, `ll:def:peel`, `ll:lem:antitone`, `ll:lem:hv`, `ll:lem:inv-peel`, `ll:lem:minperiod`,
    `ll:thm:card-peel`, `ll:thm:core-rot` and `ll:thm:layers`. The last one is new.
- One underfull vbox occurs while page 1 is shipped out. It is also present when the pre-edit snapshot is compiled the
  same way (checked with a temporary wrapper, since deleted). The output is 12 pages, before and after.
- `lg.tex` contains no machine path and no tool name. It does not use "verified" or "certified".
