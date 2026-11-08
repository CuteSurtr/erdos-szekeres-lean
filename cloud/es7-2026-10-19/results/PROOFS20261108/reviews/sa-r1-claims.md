# Review of section `sa` (Size arithmetic of the symmetric k = 7 reduction), round 1, lens: claims, labels and LaTeX

**Verdict: pass.** I found no blocker and no major finding. There are five minor findings, F1 to F5.

Files reviewed: `sections/sa.tex` (567 lines) and `sections/sa.map.tsv` (9 rows plus a header). Paths below are
relative to STAGE (`sections/`, `build/`), to RES (`AUDIT3/...`, `ES7SPLIT/...`, `WRITEUP/...`, `MIRRORETV/...`) or to
the repository root (`ErdosSzekeres/...`, `lean-toolchain`, `lake-manifest.json`).

## Checks performed, with evidence

1. **Compilation.** I created `build/sa_claims_r1_wrapper.tex` as in the contract. I ran
   `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error sa_claims_r1_wrapper.tex` twice from `build/`.
   - Both passes exit 0 and produce 7 pages.
   - The log has no `!` error, no "Missing $", no overfull box and no multiply-defined label.
   - It has 3 underfull hboxes, all in the Coverage paragraph (see F5), and 1 underfull vbox at the page break of
     page 1.
   - After pass 2 the only undefined references are 18 labels, each an `fd:` label or an export label of the contract
     table: `fd:def:{rot,inv,gp,ngon}`, `fd:lem:mono`, `ll:lem:minperiod`, `lg:lem:centre`,
     `sr:def:classes`, `sr:thm:{main,structure,variant}`, `sr:lem:concyclic`, `ar:thm:{main,transfer}` and
     `mb:thm:{baek,seven,classes,main3}`. All 18 are defined in the current `sections/{fd,ll,lg,sr,ar,mb}.tex`.
   - I also ran a full-document test on a copy, in `build/sa_claims_r1_app/`. The copy holds the sections, the
     preamble, the bibliography and `proofs.tex`, and I ran `tools/make_appendix.py` inside it. STAGE's own
     `appendix_map.tex` was not touched.
     - Three pdflatex passes exit 0.
     - The log has no undefined reference and no multiply-defined label, and the aux file has all 19 `sa:` labels.
     - The one overfull box is in an appendix row of another section (`ENCBLEAN/logs/...`).

2. **Labels and references.**
   - The section defines 19 labels, each once, all with the prefix `sa:`. All 15 own labels that are referenced
     resolve.
   - No `\ref` goes to a non-export label of another section.
   - There is no `\cite`, `\eqref`, `\newcommand`, `\def`, `\usepackage` or `\input`. The only environments are
     theorem, lemma, proposition, remark and proof, plus enumerate, itemize, center and tabular.
   - No argument of `\lean{}`, `\dirn{}` or `\leanref{}` contains a space. Lean expressions with spaces are set in
     `\texttt`.

3. **Map.**
   - The section has 9 non-remark statement environments (5 propositions, 3 lemmas, 1 theorem) and 4 remarks. The map
     has 9 rows, one per non-remark statement.
   - The header is exact, every row has 5 tab-separated fields, there are no CR characters and the file ends with a
     newline.
   - A script (`build/sa_claims_r1_chk/mapcheck.py`) compared label, kind, `lean_name` and `file_line` of every row
     with the `\leanref` pairs of its statement head, and checked that each `file_line` is the line carrying
     `theorem <name>` in the record file. All 9 rows match (`ALL_OK`).
   - `sa:lem:model` has `-` and `-` (written step).
   - The appendix generator accepted the file on the copy, including its ASCII check. The note `mb:thm:baek` becomes
     `Theorem~\ref{mb:thm:baek}`.

4. **Lean names and line numbers.**
   - All 28 (name, file:line) pairs are exact:
     - `SizeArith.lean` :16 to :79;
     - `AssembledSizes.lean` :6, :9, :12, :15, :18, :21 and :24;
     - `BaekSeven.lean:6`.
   - The other cited lines are also exact:
     - `SizeArith.lean`: header comment 1–9, modelling 4–8, part headings at 13 and 58, `#print axioms` at 84–103
       in declaration order;
     - `AssembledSizes.lean`: proof of `big_order_orbit` at 25–27, comment "prime order p >= 7" at 23, `example` at
       30, `#print axioms` at 33–39;
     - `BaekSeven.lean`: `#check @main` at 11, `#print axioms baek_seven` at 12;
     - `ErdosSzekeres/Vendor/ETV/Main/Main.lean`: `theorem main` at :87, the `variable {γ : Type _} [LinearOrder γ]`
       line at :26;
     - `ErdosSzekeres/Vendor/ETV/Config/Defs.lean`: lines 20–67 (`Config` … `HasNGon`).
   - The recalled notions (cap, cup, `HasNCap`, `HasNGon` with `l1.length + l2.length = n + 2`, `List.In`,
     `Chain3'`) agree with these definitions and with Definition `mb:def:config`.

5. **Hashes, line counts, commit.** I recomputed `shasum -a 256` and `wc -l` for the six files of the table. All six
   hashes and line counts equal the table:
   - `SizeArith.lean` 103, `170384d8…`;
   - `SizeArith.lean.log` 20, `b4bca1cd…`;
   - `AssembledSizes.lean` 39, `c08bdf20…`;
   - `AssembledSizes.lean.log` 11, `1db4174c…`;
   - `BaekSeven.lean` 12, `d6d6636c…`;
   - `BaekSeven.out` 3, `53dced1c…`.

   The checkout HEAD is `7e32ee259` on branch `es7-night-2026-11-01`. The `git hash-object` of each of the six files
   equals its blob at HEAD, so the files are those of commit `7e32ee259`. The SHA-256 of `Main.lean` begins with
   `83dd0a214204`, as the section states, and the file equals its HEAD blob.

6. **Logs and axioms.**
   - `SizeArith.lean.log`:
     - 20 lines, no error and no warning;
     - `[propext, Classical.choice, Quot.sound]` exactly for `c5_reduce`, `c4_reduce`, `c6_reduce`, `c2_reduce`,
       `c5_gap` and `table_mirror`;
     - `[propext, Quot.sound]` for the other 14.
   - `AssembledSizes.lean.log`:
     - the warning `AssembledSizes.lean:24:41: warning: unused variable hp` and the linter note;
     - `halfturn_pairs` with `Classical.choice`, and the other six with `[propext, Quot.sound]`;
     - a timing line, and no error.
   - `BaekSeven.out`: lines 1–2 are the `#check @main` output, quoted correctly in Remark `sa:rem:baek-seven`(1),
     and line 3 gives `baek_seven` the axioms `[propext, Classical.choice, Quot.sound]`.
   - A scan of the three files for `sorry`, `admit`, `native_decide`, `axiom`, `implemented_by`, `extern` and
     `unsafe` (word-bounded) finds nothing.
   - The checkout has 1064 `.lean` files, the same number as `git ls-files`. A word-bounded search for the 27 names
     of `SizeArith.lean` and `AssembledSizes.lean` finds them only in those two files, and `baek_seven` only in
     `BaekSeven.lean`. So the claim "no other Lean file uses them" holds.

7. **Claims about the records.** Each cited passage says what the section says.
   - `AUDIT3/README.md`:
     - lines 1–13: 1 November 2026, against 9cf4949a5, the audited statement verbatim, "This directory records an
       audit; it claims no theorem";
     - §4: A1-F1 is minor/minor;
     - Reproduction: `lean AUDIT3/A1_reduction/SizeArith.lean  # Lean 4.24.0, no Mathlib needed`;
     - §7 (line 282): `SizeArith.lean` "was recompiled and reproduced its log".
   - `AUDIT3/reports/A1_reduction.md`:
     - line 3 gives the date and commit;
     - Summary at lines 11–24;
     - trust rows 2–9 at lines 50–57; rows 4, 8 and 9 have the basis "Lean-checked" and "(arithmetic only)";
     - line 68: A1-F1 is minor;
     - lines 103–106: the verifier's directory and `AssembledSizes.lean`, "Lean 4.24.0 core", with the control at
       32;
     - line 262: "core Lean 4.24.0".
   - ES7SPLIT:
     - `ES7SPLIT/README.md` lines 10–15: Theorems 5 and 6 and Corollary 7 use Baek's theorem as a black box; their
       abstract form at n = 7 is Lean-checked;
     - `ES7SPLIT/README.md` lines 71–79: the §2 "Rigor" paragraph;
     - `ES7SPLIT/proofs/split_theorem.md` lines 6–16: the status paragraph;
     - `ES7SPLIT/review/README.md` lines 71–73 and Reproduction: `lake env lean` from the repository root, "with the
       repository's Lean build".
   - Toolchain: `lean-toolchain` is v4.24.0 and `lake-manifest.json` pins Mathlib at `f897ebcf72cd…`. Neither file has
     changed since 07c94a2ac (2026-10-04), which predates BaekSeven (9793c06e0, 2026-11-02). So "the repository's
     Lean 4.24.0 and Mathlib f897ebcf" is right.
   - `WRITEUP/SYMMETRIC.md` §2 (line 160) holds the size table. Its credits (C2 Theorem 4, C3 Theorem 1, C4 via
     C4CUT, C5 Theorem 5, C6 via 36 ⊇ threefold 33, mirror Theorem 2) match Remark `sa:rem:use`(5).

8. **Claims about other sections.** Each matches the current section files.
   - `sr:def:classes` requires c ∉ S in HalfTurn34, Threefold33, Fivefold35 and Fourfold32, exactly one fixed point
     in MirrorOneAxis33 and none in MirrorNoAxis34. This matches the subsets built in Remark `sa:rem:use`(1),(2).
   - `sr:thm:main` and `ar:thm:main` take the five classes as hypotheses.
   - The proof of `sr:thm:main` passes, via `root_cases`, to a power that is the half-turn or has odd prime order,
     as stated in (4).
   - The remark that follows `sr:def:classes` is `sr:rem:records`. It says Fourfold32 is used only by
     `sr:thm:variant`.
   - `mb:thm:classes` is Lean-checked with no SAT input, and `mb:thm:main3` is conditional on the three classes.
   - `mb:thm:baek` is the `#check @main` statement.
   - `mb:thm:seven` uses `main` at n = 4 through Proposition `mb:prop:cap16` and the bridge `mb:prop:gon`.
   - The hypotheses of `ll:lem:minperiod` (0 < m, y ≠ c), `lg:lem:centre` (0 < m, m even, invariant, general
     position, p ∈ S, p ≠ c) and `sr:thm:structure`(b) (1 < |S|) are met where the section uses them.

9. **Rigor vocabulary and hygiene.**
   - Neither file contains "verified" or "certified".
   - "Proved" occurs only in negations and in "proved here as a written step". Other sections use the same phrase
     (`fd`, `lg`, `mb`, `sr`). "Verifier" is the audit role.
   - The claim "not computer-assisted" for the three uses of `decide` agrees with the convention in `fd.tex`, lines
     65–75 ("A Lean proof that uses decide only for facts that the written proof … establishes by hand … does not make
     a statement computer-assisted"). The written proofs do check 2∣2, 3∣3, 2∣4, 5∣5, 2∣6 and C(6,2) = 15 by hand.
   - No case class is presented as proved: Remark (4) and (5) say "used as hypotheses" and "conditional on the
     classes". Baek's theorem is cited, and the modelling is a written step (Lemma `sa:lem:model`, Remark
     `sa:rem:use`).
   - No SAT certificate or checker is mentioned, so the cake_lpr anchor rule does not arise.
   - No machine path and no tool name occurs in `sa.tex` or `sa.map.tsv`.

10. **Sanity check of the statements** (beyond this lens). A brute-force script (`build/sa_claims_r1_chk/arith.py`)
    checked all 27 arithmetic statements for k, t < 120, p < 60 and e ∈ {0, 1}, `order_split` for s < 2000, and
    C(6,2) + 2 = 17: `ALL_OK`.

11. **Coverage paragraph.**
    - It lists all 20 + 7 + 1 = 28 theorems and the anonymous example, each with its label.
    - It names the `#print axioms` and `#check` lines it leaves out (84–103, 33–39, BaekSeven 11 and 12) and the
      header modelling.
    - The scripts and logs are correctly out of scope. `find` shows no other `.lean` file under `AUDIT3/` or
      `ES7SPLIT/`. The subdirectories `verify_A1-F2` and `verify_A1-F3` and the rest of
      `ES7SPLIT/review/equivalence` hold only `.py`, `.log` and `.txt` files.
    - `cb.tex` (lines 1482–1486) points to this section for these three files, and no other section covers them.

## Findings

**F1 (minor; files cited by bare name before their full path).**
- *Location:* the table of "Sources and evidence", lines 54–59.
- *Issue:* the table names `SizeArith.lean.log`, `AssembledSizes.lean.log` and `BaekSeven.out` by bare file name. Their
  full paths appear only in the bullets below the table (lines 66, 73 and 79). The convention in `fd` allows a bare
  name only after the file has been cited with its full path.
- *Fix:* put the table after the bullet list, or add "(full paths in the list below)" to the sentence that introduces
  the table.

**F2 (minor; summary sentences of Remark `sa:rem:use`(4) slightly overstate).**
- *Location:* lines 518–523.
- *Issue 1:* "each item exhibits a subset T that satisfies the hypotheses of one class" is not true of the case s ≥ 7
  of item (1). That case needs no class, as item (1) itself says (line 498).
- *Issue 2:* "The Lean-checked form of this implication is Theorem `sr:thm:main`" covers Euclidean isometries only.
  Item (3) also derives the affine case, whose Lean-checked form is Theorem `ar:thm:main`.
- *Fix:* write "each item, except the case s ≥ 7 of item (1), exhibits …" and "… is Theorem `sr:thm:main`, with
  Theorem `ar:thm:main` for affine symmetries; …".

**F3 (minor; a reported status of the records is out of date and not flagged).**
- *Location:* Remark `sa:rem:baek-seven`(3), lines 381–386.
- *Issue:* the section correctly reports that the ES7SPLIT records call the step to real point sets "not Lean-checked
  for n = 7", adding that "the repository's bridge covers the octagon case only" (`ES7SPLIT/README.md:78-79`). That
  record was committed in 9793c06e0 (2026-11-02 01:03 +0900).
- Since 83c80f38f (2026-11-02 03:41 +0900), `MirrorOdd.capacity16` (`MIRRORETV/lean/MirrorMain.lean:1529`, docstring
  "Baek's theorem at n = 7 in geometric form") is Lean-checked. It is the geometric 7-gon form for x-sorted point sets
  in general position, and it is Proposition `mb:prop:cap16`, which this document uses in Theorem `mb:thm:seven`.
- The section's next sentence points to `mb:thm:seven`. Still, "for their use at n = 7" can be read as the current
  status of the project.
- *Fix:* add one clause: the records' remark predates `MirrorOdd.capacity16`, the Lean-checked geometric form at
  7-gons used in the proof of Theorem `mb:thm:seven`. Do not claim that the ES7SPLIT theorems themselves become
  Lean-checked.

**F4 (minor; a paraphrase of a file comment adds content).**
- *Location:* Remark `sa:rem:control`, lines 321–323.
- *Issue:* the file's comment (AssembledSizes.lean:29) reads "control: the half-turn line is false below 33 (32 points
  = 16 pairs; the central 32-point example exists)". The section renders it as "a 32-point half-turn-symmetric set
  without a convex 7-gon". The comment itself does not mention 7-gons.
- *Fix:* quote the comment verbatim. If the description of the set is wanted, attribute it to the A1 report, line 93
  (`SYM2/sym7_32points.txt`: half-turn symmetric, centre not in the set, largest convex subset 6).

**F5 (minor; typesetting).**
- *Location:* the Coverage paragraph, lines 545–559.
- *Issue:* the paragraph produces 3 underfull lines (badness 3601, 1383 and 4739). On page 7 there is a visibly wide
  gap after "AssembledSizes.lean:".
- *Fix:* set the paragraph ragged right with a local group, `{\raggedright … \par}`, which needs no new macro.

## Outputs of this review

- `build/sa_claims_r1_wrapper.{tex,log,pdf,txt}` and `build/sa_claims_r1_pass{1,2}.txt`: the compile check.
- `build/sa_claims_r1_png/`: page renders.
- `build/sa_claims_r1_app/`: the full-document test on a copy, with its own generated `appendix_map.tex`.
- `build/sa_claims_r1_chk/mapcheck.py` and `arith.py`: the map and arithmetic checks.

## Outside the scope of this review

`cb.tex:1486` uses `\ref{sa:sec}`. `sa:sec` is not in the contract's export table, because the table predates this
section. The label exists and resolves in the full document. If the contract table is updated for `sa`, adding `sa:sec`
(and any other labels other sections may use) would make that reference conform.
