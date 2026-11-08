# Review of section `sa` (Size arithmetic of the symmetric k = 7 reduction), round 2, lens: claims

**Verdict: pass.** No blocker and no major finding. Three minor findings (F1 to F3), all wording-level.

Files reviewed:
- `sections/sa.tex` (611 lines);
- `sections/sa.map.tsv` (header plus 13 rows).

Path conventions in this report:
- `sections/`, `build/`, `reviews/`, `snapshots/` are relative to STAGE;
- `AUDIT3/...`, `ES7SPLIT/...`, `WRITEUP/...`, `MIRRORETV/...`, `LEANEXT/...`, `LAYERLEAN/...`, `SYMLEAN/...`,
  `SYM2/...` are relative to RES;
- `ErdosSzekeres/...`, `lean-toolchain`, `lake-manifest.json` are relative to the repository root.

Round-1 inputs: `reviews/sa-r1-claims.md`, `reviews/sa-r1-math.md`, `reviews/sa-r2-fix.md`. A diff against
`snapshots/sa-r2-pre/sa.tex` shows that all 15 round-1 findings were applied. I checked the new text claim by claim.

## Checks performed, with evidence

### 1. Compile check

I created `build/sa_claims_r2_wrapper.tex` exactly as in the contract. From `build/` I ran
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error sa_claims_r2_wrapper.tex` twice.
- Both passes exit 0 and produce 8 pages.
- The log has no `!` error, no "Missing", no overfull box, no underfull hbox and no multiply defined label. It has two
  underfull vboxes during page output.
- After pass 2 there are 51 undefined-reference warnings, for 26 distinct labels:
  - `ar:thm:{main,transfer}`;
  - `ec:thm:{compat,fivefold,fourfold}`;
  - `fd:def:{gp,inv,ngon,rot}`, `fd:lem:mono`;
  - `lg:lem:centre`;
  - `ll:lem:minperiod`, `ll:thm:{card-peel,layers}`;
  - `mb:thm:{baek,classes,main3,refl32,seven}`;
  - `mm:def:config`;
  - `sr:def:classes`, `sr:lem:{concyclic,orbit}`, `sr:thm:{main,structure,variant}`.

  Each is an `fd:` label or a contract export label, and none is an `sa:` label. This is the expected outcome.
- Page renders (`build/sa_claims_r2_png/`) show no layout defect. The source table, the multi-name statement heads and
  the ragged-right Coverage block all set cleanly.

### 2. Full-document test, on a copy

In `build/sa_claims_r2_app/` I copied the sections, maps, preamble, bibliography and `proofs.tex`, and ran
`python3 -I tools/make_appendix.py` there. STAGE's own `appendix_map.tex` was not touched.
- The generator accepts the 13 `sa` rows: ASCII check, kinds, label prefix, and the labels named in the notes. It
  writes 470 rows in all.
- Three passes of `proofs.tex` exit 0 and give 187 pages.
- There is no undefined reference and no multiply defined label.
- The aux file holds all 19 `sa:` labels.
- The only overfull box (49.4pt) is in an appendix row of another section (`ENCBLEAN/logs/m8_fix_build.log`).
- I viewed the appendix rows of `sa` (page 186) and the table of contents. Both are fine.

### 3. Labels and `\ref` targets

- The section defines 19 labels, each once, all with the prefix `sa:`, starting with `\section{...}\label{sa:sec}`.
- There are 122 `\ref`s to 41 distinct targets: 15 own labels and the 26 external labels listed above.
- A script compared every external target with the export labels of `CONTRACT.md`: all 26 are allowed.
- All 41 targets are defined in the current `sections/*.tex`.
- Non-export labels are cited only in words, never with `\ref`. Examples: the remark after `sr:def:classes`
  (`sr:rem:records`), `mb:prop:cap16`, `ll:thm:reduction`.
- There is no `\cite`, `\newcommand`, `\def`, `\usepackage`, `\input`, `\eqref`, `\url` or `\href`. No other section
  uses `\cite` either.
- Environments used: theorem, lemma, proposition, remark, proof, enumerate, itemize, center, tabular.
- None of the 128 `\lean` arguments, 68 `\dirn` arguments or 28 `\leanref` pairs contains a space or a special
  character. Lean expressions with spaces are in `\texttt`, with `\_` and `\#` escaped.
- The file is ASCII only and has no trailing whitespace.

### 4. Map TSV

I checked the map with `build/sa_claims_r2_chk/mapcheck.py`, which reads the section, the map and the Lean
sources. Result: `ALL_OK`.
- **Format.** The header is exact. Every row has 5 tab-separated fields. The file is ASCII, has no CR and ends with
  a newline.
- **Rows.** There are 9 non-remark statements (5 propositions, 3 lemmas, 1 theorem), and each has a row. The 4
  remarks also have rows; the generator explicitly allows remark rows. The rows are in document order.
- **Kinds.** Each row's kind equals its environment.
- **Names and lines.** For every statement whose head names Lean declarations, `lean_name` and `file_line` equal the
  `\leanref` pairs of the head, in order. Each `file_line` is the line that carries `theorem <name>` in the record
  file, and namespace `A1` is open there.
- **`sa:lem:model`.** It is a written step, with `-` and `-`.
- **`sa:rem:control`.** It has `-` and `AssembledSizes.lean:30`, which is the line of the anonymous `example`.

### 5. Lean names, line numbers and file structure

I re-read all three files and checked each claim about them.
- **`AUDIT3/A1_reduction/SizeArith.lean`.**
  - Lines 1–9 are the header comment, and the modelling is at 4–8.
  - The quote "audited by hand in the report, not formalised here" is verbatim (line 4).
  - Namespace `A1` (line 11) contains exactly 20 theorems, at lines 16–80.
  - The part headings are at 13 ("Reduction ...") and 58 ("Upper bounds of the table, given the case theorems",
    verbatim).
  - Lines 84–103 hold one `#print axioms` per theorem, in declaration order.
  - There is no `import`.
- **`AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean`.**
  - The 7 theorems are at lines 6, 9, 12, 15, 18, 21 and 24, with the proof of `big_order_orbit` on 25–27.
  - The anonymous `example` is at line 30, with its proof `intro h; have := h 32 16 rfl (by decide); omega` quoted
    exactly.
  - Lines 33–39 hold the `#print axioms` commands.
  - The file has no `import` and declares no namespace.
  - The comment at line 29 is quoted verbatim, and the comment at line 23 matches.
- **`ES7SPLIT/review/equivalence/BaekSeven.lean`.**
  - It imports `ErdosSzekeres.Vendor.ETV.Main.Main`.
  - `baek_seven` is at line 6, and its statement and its two proof lines are quoted exactly.
  - `#check @main` is at line 11 and `#print axioms baek_seven` at line 12.
- **Vendored ETV definitions.**
  - `ErdosSzekeres/Vendor/ETV/Config/Defs.lean` lines 20–67 run from `structure Config` to `HasNGon`. The recalled
    notions match the source: Cap = `IsChain (· < ·)` plus `Chain3' Cap3`; Gon with lengths ≥ 2, equal `head?` and
    `getLast?`; `NGon` with length sum `n + 2`.
  - `ErdosSzekeres/Vendor/ETV/Lib/List/Defs.lean` has `List.In` at :22, the inductive `Chain3` at :42 and `Chain3'`
    at :46.
  - `ErdosSzekeres/Vendor/ETV/Main/Main.lean` has `theorem main` at :87 and the `variable {γ : Type _} [LinearOrder γ]`
    line at :26.
  - I located `List.IsChain` read-only in the local package sources. It is defined in Batteries at the pinned revision
    `8da40b72` (`Batteries/Data/List/Basic.lean:562`, inside `namespace List`). It is not in Lean core v4.24.0;
    Mathlib's `IsChain` is a different, set-based notion. So "which Mathlib takes from its dependency Batteries" is
    correct.
- **`MIRRORETV/lean/MirrorMain.lean`.**
  - `capacity16` is at :1529, in `section Baek17` of namespace `MirrorOdd`, so the full name `MirrorOdd.capacity16`
    is correct.
  - Its statement is `Configuration n`, `¬ c.HasCap 4`, no convex heptagon, `n ≤ 16`, as described.
  - It is used at :1701 in `mirror_seven_of`, which `mirror_seven` (:1803) calls.
  - `MirrorMain.out` lines 848 and 850 print the axioms of `mirror_seven` and `mirror_seven_line`.

### 6. Hashes, line counts and commit (recomputed)

I recomputed `shasum -a 256` and `wc -l` for the six files of the table. A script compared them with the `.tex` table
character by character. All six line counts and all six hashes match:

| file | lines | SHA-256 prefix |
|---|---|---|
| `SizeArith.lean` | 103 | `170384d81db7` |
| `SizeArith.lean.log` | 20 | `b4bca1cd8542` |
| `AssembledSizes.lean` | 39 | `c08bdf200fb5` |
| `AssembledSizes.lean.log` | 11 | `1db4174c7c04` |
| `BaekSeven.lean` | 12 | `d6d6636c78dd` |
| `BaekSeven.out` | 3 | `53dced1cd76f` |

- The SHA-256 of `ErdosSzekeres/Vendor/ETV/Main/Main.lean` starts with `83dd0a214204`, as stated.
- The checkout is at HEAD `7e32ee259` on branch `es7-night-2026-11-01`, with a clean worktree. `git hash-object` of
  all seven files equals their HEAD blobs.
- `lean-toolchain` is `v4.24.0` and `lake-manifest.json` pins Mathlib `f897ebcf72cd…`. Neither file has changed since
  `07c94a2ac` (2026-10-04).
- `ErdosSzekeres/Vendor/ETV` was last changed on 2026-10-09. So `BaekSeven.out` (committed in `9793c06e0`) refers to
  the same `main` and toolchain as HEAD.

### 7. Logs and axioms

- **`SizeArith.lean.log`.** It has 20 lines and no error or warning.
  - `[propext, Classical.choice, Quot.sound]` appears exactly for `A1.c5_reduce`, `A1.c4_reduce`, `A1.c6_reduce`,
    `A1.c2_reduce`, `A1.c5_gap` and `A1.table_mirror`.
  - `[propext, Quot.sound]` appears for the other 14.
- **`AssembledSizes.lean.log`.**
  - Line 1 is the warning ``AssembledSizes.lean:24:41: warning: unused variable `hp` ``, followed by the linter note.
  - `halfturn_pairs` uses `Classical.choice`; the other six use `[propext, Quot.sound]`.
  - Line 11 is a timing line. There is no error.
  - Column 41 is Lean's 0-based column of `hp`.
- **`BaekSeven.out`.** Lines 1–2 give the type of `@main` and match Remark `sa:rem:baek-seven`(1) term by term:
  `Type u_1`, the instance, `n`, `C`, `S`, `(n + 2).choose 2 + 2 ≤ S.card`, and the disjunction. Line 3 gives
  `baek_seven` the axioms `[propext, Classical.choice, Quot.sound]`.
- **Token scan.** A word-bounded scan of the three files for `sorry`, `admit`, `native_decide`, `axiom`,
  `implemented_by`, `extern` and `unsafe` finds nothing beyond the `#print axioms` lines.
- **Name search.** I searched all 1,064 tracked `.lean` files (the checkout has no `.lake`) for the 27 names of the
  two `AUDIT3` files and for `baek_seven`, word-bounded. Each name occurs only in its own file. This confirms "no other
  Lean file uses them".

### 8. Claims about the records

Every cited passage says what the section says.
- **`AUDIT3/README.md`.**
  - Line 3: 1 November 2026 (UTC), against `9cf4949a5`.
  - Lines 6–7: the audited statement, matching the section's quote.
  - Line 12: "This directory records an audit; it claims no theorem."
  - §4 line 83: A1-F1 is rated minor by both the auditor and the verifier.
  - Reproduction, line 304: `lean AUDIT3/A1_reduction/SizeArith.lean # Lean 4.24.0, no Mathlib needed`.
- **`AUDIT3/reports/A1_reduction.md`.**
  - The auditor's own proof (Summary, lines 11–24) and the outputs list (lines 36–42, which includes `SizeArith.lean`).
  - Trust rows 2–9 are at lines 50–57. Rows 4, 8 and 9 are the ones labelled "Lean-checked", rows 8 and 9 with
    "(arithmetic only)".
  - Line 68: A1-F1 is minor.
  - Lines 103–106: the verifier's directory, and `AssembledSizes.lean` described as "Lean 4.24.0 core" with the
    control at 32. Line 106 does not mention `big_order_orbit`, as the section says.
  - Lines 93 and 107: the description of the 32-point example and the file name `SYM2/sym7_32points.txt`. The file
    exists.
  - Line 262: "core Lean 4.24.0".
- **`ES7SPLIT/README.md`.**
  - Lines 11–14: Theorems 5 and 6 and Corollary 7 use Baek's theorem as a black box, and its abstract form at n = 7
    is Lean-checked.
  - Lines 78–79 are quoted verbatim, in the "Rigor" paragraph of §2 (section headings at lines 22 and 85).
- **`ES7SPLIT/proofs/split_theorem.md`.** Lines 13–15, in the status paragraph that starts at line 6, say the same.
- **`ES7SPLIT/review/README.md`.** Line 210 says "compiled from the repository root with the repository's Lean
  build", and line 229 is the `lake env lean` command.
- **Commits.** Checked with `git show -s`, `git blame` and `git log -S`; all three commits are ancestors of HEAD.
  - The cited lines of both ES7SPLIT files were committed in `9793c06e0` (2026-11-02 01:03:29 +0900) and have not
    changed since.
  - `capacity16` first appears in `83c80f38f` (2026-11-02 03:41:47 +0900).
  - `9cf4949a5` is in the history.
- **`WRITEUP/SYMMETRIC.md`.** §2 "Sizes and constructions" (line 160) holds the size table that item (5) of Remark
  `sa:rem:use` refers to. Its rows 32/31/28/31/30/32 match the bounds of `sa:prop:table`.

### 9. Claims about other sections

Each claim matches the current section files.
- **`sr:def:classes`.**
  - `HalfTurn34`, `Threefold33`, `Fivefold35` and `Fourfold32` require `c ∉ S`.
  - `MirrorOneAxis33` requires exactly one fixed point and `MirrorNoAxis34` none.
  - The `reflLine` formula equals `sr:def:maps`(d).
  - Only `sr:thm:variant` uses `Fourfold32` among the reduction theorems: sr.tex:238–239, and mb.tex:1117–1121 for
    the `RTC` variants. `ar:thm:main` excludes it (ar.tex:14–15).
- **`sr:thm:main`.**
  - It assumes the five classes.
  - Its proof uses `root_cases`: a power of the rotation is the half-turn or has odd prime order.
  - It selects whole orbits with `sr:lem:orbit`.
- **`sr:thm:structure`(b).** The hypothesis `1 < |S|` holds, since n ≥ 33.
- **`sr:lem:concyclic`.** It needs equal `eDist2` only.
- **`ar:thm:main` and `ar:thm:transfer`.** They play the role stated.
- **`ec:thm:compat`(a),(b).** Under (O), "ζ has exact order m", every finite ζ-invariant set T with 0 ∉ T has
  m dividing |T|, and |S| mod m = [0 ∈ S] mod m. "An abstract form of the count" is a fair description.
- **`ec:thm:fourfold` and `ec:thm:fivefold`.** They need at least 29 and 32 points, with `rotAbout c (2π/4)` and
  `(2π/5)`.
  - `LayerLemma.Fourfold32` and `LayerLemma.Fivefold35` (`LEANEXT/es7corr/ES7Corollaries.lean:1157`, `:1164`) have the
    same text as `SYMLEAN/SymmetricReduction.lean:477` and `:496`. I compared them.
- **`ll:lem:minperiod` and `lg:lem:centre`.** Their hypotheses are met where they are used.
- **`fd:lem:mono`(a),(b),(c).** The parts are as cited.
- **`mm:def:config`.** It is the `Configuration` of `capacity16`.
- **`mb` theorems.**
  - `mb:thm:baek` is the `#check @main` statement.
  - `mb:thm:seven`(b) is about `lineRefl`, and `mb:thm:refl32`(b) about `reflLine`, derived from it.
  - `mb:thm:classes` is Lean-checked with no SAT input or hypothesis.
  - `mb:thm:main3` is conditional on the three classes.
- **The convention invoked for `decide`.** It is the "Computer-assisted" item of fd's "Rigor labels" paragraph
  (fd.tex:73–75): "A Lean proof that uses decide only for facts that the written proof ... establishes by
  hand ... does not make a statement computer-assisted."

### 10. Rigor labels and overclaiming

- **Rigor words.** Neither file contains "verified" or "certified".
  - "proved" occurs only in negations ("not proved in Lean or in this document", "cited and not proved") and in "proved
    here as a written step". "We prove" also refers to the written step.
  - "Lean proves" and "`rfl` proves" describe Lean tactics; other sections (ec, fd, lg, cb) use the same wording.
  - "verifier" is the audit role and `verify_A1-F1` a directory name.
- **Lean-checked.** The label is attached only to the 28 declarations. Each has `#print axioms` evidence in the three
  logs, and all axioms are within the standard three.
- **The anonymous `example`.** It is not called Lean-checked. The section says that no `#print axioms` covers it and
  names the evidence: the error-free compile log.
- **"Not computer-assisted".** The claim agrees with the fd convention. `decide` occurs only at `SizeArith.lean:55`,
  `AssembledSizes.lean:31` and `BaekSeven.lean:8`, each on a closed fact that the written proof checks by hand: 2∣2,
  3∣3, 2∣4, 5∣5, 2∣6, C(6,2) = 15 and 32 ≤ 32. `omega` produces a kernel-checked proof term, not a kernel evaluation.
- **Modelling.** Lemma `sa:lem:model` is tagged "written step". The Rigor paragraph and the Coverage paragraph say that
  it is not Lean-checked and not a declaration of the files.
- **Case classes.** None is presented as proved.
  - `HalfTurn34`, `Threefold33` and `Fivefold35` are stated to be hypotheses, not proved in Lean or here.
  - `Fourfold32` is used only inside conditional statements.
  - The mirror classes are Lean-checked theorems, which matches mb.
- **Baek's theorem.** It is cited (`mb:thm:baek`). The ES7SPLIT theorems are said to "remain written proofs".
  Whether `capacity16` covers their z-split use is explicitly "not examined here".
- **SAT.** No SAT certificate, CNF or checker verdict is mentioned, so the cake_lpr anchor rule does not apply.
- **Forbidden content.** `sa.tex` and `sa.map.tsv` contain no machine path, no forbidden name and no internal
  directory name.

### 11. Coverage paragraph

- **Covered.** A script listed every declaration of the three files: 20, plus 7 and 1 `example`, plus 1. All 28 named
  declarations appear in the Coverage paragraph with their labels, and the example appears too. The total "28 theorems
  and one example" is right.
- **Not covered.** The paragraph excludes the `#print axioms` lines (84–103, 33–39 and line 12), the `#check` (line
  11) and the comments, including the modelling, with reasons.
- **Out of scope.** `find` shows that `AUDIT3/A1_reduction/` and its three `verify_*` subdirectories, and
  `ES7SPLIT/review/equivalence/`, hold no other `.lean` file, only `.py`, `.log`, `.txt` and `.out`. So "none of them
  contains a Lean declaration" holds.
- **No other section covers these files.** `cb.tex:1482–1486` points to this section.

## Findings

**F1 (minor; the introduction of §1.2 overstates what the statements assume).**
- *Location:* `sa.tex:225–227`.
- *Issue:* the text says "each statement assumes the bound on k as a hypothesis". That is not true of `A1.c3_no32` and
  `A1.c5_gap`. Their only hypothesis is `e ≤ 1`; they are unconditional facts about the sizes 3k+e and 5k+e. In
  `A1.table_c5` the hypothesis bounds `5k+e`, not k. The statements printed just below are correct, so this is
  wording only.
- *Fix:* "each statement that uses a case theorem assumes the bound it gives (on k; for `A1.table_c5`, `5k+e<35`) as a
  hypothesis; `A1.c3_no32` and `A1.c5_gap` assume no such bound."

**F2 (minor; two loose paraphrases of the file contents).**
- (a) *Location:* `sa.tex:273–274`.
  - *Issue:* "restates six of the statements above with the size n as an explicit variable". `fivefold_size` restates
    only the first conclusion of `A1.c5_reduce`, and `fourfold_via_halfturn` only the third conclusion of
    `A1.c4_reduce`. The proof of Proposition `sa:prop:assembled` shows this correctly.
  - *Fix:* "restates six of the statements above, or parts of them, ...".
- (b) *Location:* `sa.tex:23–24`.
  - *Issue:* "an order of at least 7 gives one orbit". The lemma concludes `1 ≤ k`, which means at least one orbit
    other than {c}.
  - *Fix:* "gives at least one orbit other than {c}".

**F3 (minor; two cross-references are slightly imprecise).**
- (a) *Location:* `sa.tex:468`.
  - *Issue:* "(This is also shown after Definition sr:def:classes.)" The fixed-point argument for `reflLine` is the last
    part of Definition `sr:def:classes` itself (sr.tex:231–235, inside the definition environment, which ends at
    :236), not text after it.
  - *Fix:* "at the end of Definition ...".
- (b) *Location:* `sa.tex:43–46`.
  - *Issue:* "the layer results (Theorems ll:thm:layers and ll:thm:card-peel), through which the Lean proofs of
    Theorems ec:thm:fourfold and ec:thm:fivefold pass". Those Lean proofs live in `LEANEXT/es7corr/ES7Corollaries.lean`.
    That file does not import `LAYERLEAN`; its lines 1–1147 are a verbatim copy of `LAYERLEAN/LayerLemma.lean` lines
    1–1147 (checked with `cmp`; ec.tex:902–904 says so). So the proofs use copies of these theorems, which are
    different Lean constants. Also, the step to exactly 32 or 35 points is `convexNGon_of_layers` (`ll:thm:reduction`,
    an export label). Item (5) of Remark `sa:rem:use` already says "same-text copy" for `Fourfold32` and `Fivefold35`.
  - *Fix:* "through verbatim copies of which (with Theorem ll:thm:reduction) ...".

## Observations that are not findings

- In the generated appendix the four remark rows show "written step" in the Lean-declaration column. This is how
  `make_appendix.py` renders `-`, and other sections' remark rows look the same. For `sa:rem:control` this sits next to
  the file line `AssembledSizes.lean:30`; the note explains the case ("anonymous example ... accepted by Lean ...
  not covered by #print axioms").
- In the `sa:rem:use` note, the generator's identifier heuristic sets `HalfTurn34` in typewriter but `Threefold33` and
  `Fivefold35` in roman. This is cosmetic, and the cause is the generator, not the map.
- The fd definition of *Lean-checked* names "Lean 4.24.0 with Mathlib f897ebcf". The two `AUDIT3` files are core Lean
  with no import, checked with Lean 4.24.0 alone. The section states this explicitly, so the label is used correctly.

## Outputs of this review

- `build/sa_claims_r2_wrapper.{tex,log,pdf,txt}` and `build/sa_claims_r2_pass{1,2}.txt`: the compile check.
- `build/sa_claims_r2_png/`: page renders.
- `build/sa_claims_r2_app/`: the full-document test on a copy, with its own generated `appendix_map.tex`, three pass
  logs and renders of the contents page and of the appendix page with the `sa` rows.
- `build/sa_claims_r2_chk/mapcheck.py`: the map check. It takes STAGE, RES and the repository root as arguments.

## Outside the scope of this review

`cb.tex:1486` uses `\ref{sa:sec}`. That label exists and resolves in the full document, but `sa:sec` is not in the
contract's export table, which predates this section. Adding a row for `sa` to the table (at least `sa:sec`) would make
that reference conform. Round 1 noted the same.
