# Section `lg`, whole-document review round 1: re-check of the fixes (lens: recheck)

**Verdict: pass.** All five findings are resolved correctly; the fixer declined none. The four hunks of the diff
introduce no blocker, major or minor finding. The compile is clean.

Inputs:
- the fix log `reviews/docfix-lg-r1-fix.md`;
- the pre-edit snapshot `snapshots/docfix-r1-pre/lg.tex` (SHA-256 `bd3334147037`..., 945 lines) and
  `snapshots/docfix-r1-pre/lg.map.tsv` (`d7c6131c5b54`..., 32 lines);
- the current `sections/lg.tex` (`7b314e52fe64`..., 966 lines) and `sections/lg.map.tsv`, which is byte-identical
  to the snapshot (same SHA-256).

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`) or, for Lean sources and records, to
RES. Nothing under REPO was modified. No Lean, lake or solver was run, and git was not run.

## 1. The five findings

| # | finding | status | evidence |
|---|---|---|---|
| 1 | [xref-fdlllg, minor] Dependencies says all listed results are recalled in §3.1, which does not recall `fd:lem:pos-triples` | **resolved** | `lg.tex:112-114` now reads "These, except Lemma `fd:lem:pos-triples`, which is used only in Step 3 of the proof of Theorem `lg:thm:fan`, are recalled in §`lg:ssec:notation`". grep: `fd:lem:pos-triples` occurs only at :111 (the list), :113 (the new clause) and :700 ("Step 3: convex position" in the proof of `lg:thm:fan`). The Lean name at :48 is in the Sources paragraph, which is about the Lean proofs. Every other listed result is recalled in §3.1: point at :118, orient at :133, (O2) = `fd:lem:orient` at :136, rot at :146, inv/cp/ngon/mono(c)/gp/collinear at :172-177, hv/peel at :183-184, and (L1)-(L4) = `ll:lem:hv`, `ll:lem:antitone`, `ll:lem:inv-peel`, `ll:thm:core-rot` at :188-194. |
| 2 | [consistency, minor] `\subsection*{Coverage}` puts an unnumbered contents line between 3.6 and 4 | **resolved** (lg part) | `lg.tex:895` is `\paragraph{Coverage.}`, the form used by ar, ec, fd, ll, mb, mm, pc, sa and sr (grep). amsart sets `tocdepth` to 2 (`amsart.cls:1142`), and `\@tocline` omits levels above it (:1196). So the level-4 entry that amsart writes to the aux file (`\tocparagraph{}{}{Coverage.}`) is not printed in the contents. The suggestion to change oc and cb too concerns files outside lg; leaving them is right (see Notes). |
| 3 | [consistency, minor] the build.log sentence still reads as a record of the present file | **resolved** | see 1.1 |
| 4 | [completeness, major] the 19 declarations of `LEANEXT/review/tests_tail.lean` (= `VacuityTest.lean` 1149-1297) are neither covered nor listed | **resolved** | see 1.2 |
| 5 | [typesetting, minor] the same heading gives an unnumbered contents line and a level-2 bookmark | **resolved** | the change of finding 2. The bookmarks file `build/lg_recheck_r1_wrapper.out` now has exactly 7 entries: the section and subsections 1.1-1.6. There is no Coverage bookmark (hyperref's bookmark depth follows `tocdepth` = 2). |

### 1.1 Finding 3: checked against the records

The new text is at `lg.tex:54-64`.

**build.log.** `LAYERLEAN/logs/build.log` has 3 lines: the command, "exit code: 0" and "messages: 0 lines". It names
no hash. Its SHA-256 is `168d2407390b`....

**Commit history.** I confirmed the history independently, without git. A small read-only Python script decompressed
the loose commit, tree and blob objects of the repository's object store with zlib. All the commits involved are loose
objects.
- `6429e9a70` adds both `LAYERLEAN/LayerLemma.lean` and `LAYERLEAN/logs/build.log`. Its parent `44530b46f` has
  neither file. The added LayerLemma.lean has 454 lines and SHA-256 `804b1d25f79a`.... The added build.log is blob
  `513769abb6c1`, whose content SHA-256 is `168d2407390b`..., the same as the current file.
- LayerLemma.lean then changes in `b997a2970` (576 lines), `6a7ecacef` (617), `6e3d1feb9` (929), `88fe40ccc` (1034)
  and `393619a57` (1148 lines, `afb8542dceb0`..., the current file).
- The intermediate parents `22bc91964` and `c0517eb63` hold the same blob as the version before them.
- The build.log blob is identical in all six commits.

So these phrases are accurate: "committed with the first version of the file (454 lines, commit `6429e9a70`)", "not
updated by the five later commits that changed the file" and "not a record of the present file". They also agree
with `reviews/fd-r2-rigor.md` m1 (which lists the five commits from `git log`), `reviews/doc-r1-consistency.md` M3,
`ll.tex:35-38` and `fd.tex:204-206`.

**REPORT.md.** `LEANEXT/review/REPORT.md` identifies the reviewed file at lines 3-4 (`afb8542d`..., 1148 lines). Item 1
reads "Build. Exit 0, no messages." This matches the new text.

**Re-check of 6 November.** `LAYERLEAN/logs/axioms_recheck_20261106/out.txt` ends with "Exit status: 0" and "exit 0".
The first 1148 lines of its `LayerLemmaAxioms.lean` match LayerLemma.lean byte for byte (cmp OK).

**Toolchain sentence.** In that directory, `README.txt` records Lean 4.24.0, Mathlib `f897ebcf`, a run "from the
repository root" and the date 6 November 2026, 04:59 KST. `run.sh` records `lake env lean` after a `cd` to the
repository placeholder. So "the files README.txt and run.sh of that directory record the toolchain and the command
given above" is accurate. The toolchain sentence at `:54` now rests on a record of the present file.

**Other claims.** "No sorry, admit, axiom or native_decide" still holds: `grep -c -w` gives 0. No other line of lg
mentions build.log.

### 1.2 Finding 4: checked against the Lean text

The new item is at `lg.tex:944-960`. The copies-list entry at `:941` is new as well.

**The 19 declarations.** `tests_tail.lean` has 149 lines and the namespace `ErdosSzekeres.LayerLemma.Review`.
- Definitions: `L4` (12), `S4` (15) and `H6` (124).
- Theorems: `mem_S4` (17), `card_S4` (21), `angle4` (23), `rot4` (25), `hc4` (30), `inv4` (35), `gp4` (41),
  `inner4` (54), `hno4` (69), `hv4` (77), `peel1_4` (91), `nest4` (96), `orbit4` (102), `layers4` (106),
  `chain4` (117) and `inv6` (128).

That makes 3 definitions and 16 theorems, 19 in all. A grep for other declaration keywords (abbrev, instance,
structure, inductive, example, axiom, opaque) finds none. The item names exactly these 19.

**What the item says the tests state.** I checked each claim against the Lean text.
- `L4`/`S4` are the 8 distinct points (±2,0), (0,±2), (±1/2,±1/2). The centre is `0 : Point`.
- `hc4` is `(0 : Point) ∉ S4`.
- `inv4` is `Invariant (rotAbout 0 (2 * Real.pi / ((4 : ℕ) : ℝ))) S4`, which is maps-into, as the text says.
- `gp4` is `GeneralPosition S4`.
- `hno4` is `¬ HasConvexNGon 8 S4`, which is "8-free" in the convention of `lg.tex:174`.
- `hv4` is `![2, 0] ∈ hullVerts S4`.
- `peel1_4` is `![1/2, 1/2] ∈ peel S4 1`.
- `nest4`, `orbit4`, `layers4` and `chain4` apply `strict_nesting`, `hullVerts_eq_orbitFS_rotAbout`,
  `layers_are_orbits` and `chain_clauses_sound`, in that order, each with `(m := 4) (K := 8)`.
- `H6` lists (1,0), (1/2,√3/2), (-1/2,√3/2), (-1,0), (-1/2,-√3/2) and (1/2,-√3/2). These are
  (cos(kπ/3), sin(kπ/3)) for 0 ≤ k < 6.
- `inv6` is `Invariant (rotAbout 0 (2 * Real.pi / ((6 : ℕ) : ℝ))) H6`.
- The file ends with five `#print axioms`, two `#check` and two `#print` commands at lines 141-149.

**Labels.** The cited labels are `lg:thm:nesting` (strict_nesting), `lg:thm:chain` (chain_clauses_sound),
`ll:thm:core-rot` (`ll.tex:473`, hullVerts_eq_orbitFS_rotAbout) and `ll:thm:layers` (`ll.tex:532`,
layers_are_orbits). All four sit on the right statements, and the two ll labels are export labels.

**VacuityTest.lean.** It has 1297 lines. `head -n 1148` matches LayerLemma.lean (cmp OK), and `tail -n +1149`
matches tests_tail.lean (cmp OK). So the file is exactly LayerLemma.lean followed by tests_tail.lean, and the 19
declarations stand at lines 1160-1276 (grep). The copies-list entry "(all 1148 lines, followed by the tests of the next
item)" is accurate, and the list's lead claim (lines 11-1147 verbatim) still holds for it.

**"Which no section covers".** A grep of all twelve section files, sa included, for `tests_tail`, `VacuityTest`,
`LayerLemma.Review`, `hno4`, `peel1_4`, `inv6` and `nest4` finds hits only in lg.tex.

**REPORT.md item 6.** It is "Vacuity test (tests_tail.lean, run inside VacuityTest.lean; Lean-checked)", and its
bullets match the item.

**Rigor.** The item gives the tests no label. It says only what they state and which theorems they apply, so no rigor
label is rounded up. The reason "non-vacuity tests, not results" is a test-file reason of the kind contract rule 9
allows.

## 2. Diff review (4 hunks in lg.tex, none in lg.map.tsv)

- **@@ -52,12 +52,16 @@** (build-record paragraph). All claims are true; see 1.1. The LaTeX is sound: `\dirn` for the
  file names and `\texttt` for the hash and commit.
- **@@ -105,7 +109,8 @@** (Dependencies). This is the accurate exception clause of finding 1. The grammar is fine.
- **@@ -887,8 +892,7 @@** (`\subsection*{Coverage}` becomes `\paragraph{Coverage.}`, with the text following
  directly). It renders as a run-in head like the section's other paragraph heads (checked on the rendered page 11).
  No label was attached to the old heading, so nothing refers to it.
- **@@ -934,9 +938,26 @@** (copies-list entry and new item). All claims are true; see 1.2.
  - The mathematics is right: S4, its centre and m, K are given correctly, and the hexagon's coordinates equal
    (cos kπ/3, sin kπ/3).
  - The `\lean{...}` arguments contain no spaces, so `\nolinkurl` loses nothing. `\hv`, `\peel` and
    `\operatorname{rotAbout}` are used as elsewhere in lg.
  - The rendered text (pdftotext and page 12 as an image) shows every name and formula correctly.

**No statement touched.** No statement environment, label, Lean head or map row changed. A script check shows 31
labelled statement environments against 31 map rows, with the same labels, kinds, Lean names and file:line. So no
Lean statement fidelity is at stake in this diff.

**Scans of lg.tex and lg.map.tsv.**
- No machine path: `/private`, `/Users`, `/home`, `/tmp`, `/sandbox` and `/path/to` were all absent.
- No tool name.
- No `\newcommand`, `\def` or `\usepackage`.
- No "verified" or "certified".
- The four occurrences of "proved" (`:85`, `:97`, `:784`, `:849`) are outside the diff, and they refer to this
  document's own written proofs.

## 3. Compile

The wrapper `build/lg_recheck_r1_wrapper.tex` has the contract content. It was compiled twice from `build/` with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
- Both runs exit 0.
- There are no `!` errors and no Missing, Runaway or Emergency messages.
- There are no overfull boxes, so none above 1pt.
- There is no "multiply defined" warning and no rerun request.
- The output is 12 pages.

**Undefined references.** These are expected in the standalone check, and all are allowed export labels:
- the fd labels `fd:def:cp`, `fd:def:gp`, `fd:def:inv`, `fd:def:ngon`, `fd:def:orient`, `fd:def:point`,
  `fd:def:rot`, `fd:lem:collinear`, `fd:lem:mono`, `fd:lem:orient` and `fd:lem:pos-triples`;
- the ll labels `ll:def:hv`, `ll:def:peel`, `ll:lem:antitone`, `ll:lem:hv`, `ll:lem:inv-peel`, `ll:lem:minperiod`,
  `ll:thm:card-peel`, `ll:thm:core-rot` and `ll:thm:layers`. `ll:thm:layers` is new, used by the new item.

**Underfull vbox.** One "Underfull \vbox (badness 10000) has occurred while \output is active" occurs at the shipout of
page 1 (log line 639). The fixer's own `build/lg_wrapper.log` has it at the same line. It is not a finding category.

## Notes (no finding against lg)

- oc (`oc.tex:900`) and cb (`cb.tex:1426`) still use numbered `\subsection{Coverage}`, which gives contents lines 4.7
  and 11.11. That is the optional second half of finding 2, and it is outside lg's files. It is for the oc and cb
  fixers, if full uniformity is wanted.
- Optional readability point: the sentence at `lg.tex:58-64` chains four relative clauses. It is correct and
  parseable as it stands.
- Scratch files from this re-check:
  - `build/lg_recheck_r1_wrapper.{tex,aux,log,out,pdf}`;
  - `build/lg_recheck_r1_run2.out`;
  - `build/lg_recheck_r1.txt` (pdftotext);
  - `build/lg_recheck_r1_pg-11.png` and `build/lg_recheck_r1_pg-12.png`;
  - the read-only object-store helper `STAGE/../lg_recheck_gitpeek.py`.
