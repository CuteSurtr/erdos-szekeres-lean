# docfix cb, round 1 (whole-document review): re-check

Inputs: the fix log `reviews/docfix-cb-r1-fix.md`; the snapshot `snapshots/docfix-r1-pre/cb.tex` and `cb.map.tsv`; the
current `sections/cb.tex` and `sections/cb.map.tsv`; the sources under RES (read only). Paths below are relative to
STAGE or to RES.

**Verdict: pass.** All three findings are resolved correctly. The diff adds no blocker or major. Two minor points are
listed in section 4.

## 1. The three findings

### F1 [consistency, minor] "counts as certified" / "uncertified node": resolved

Changed text: cb.tex:36-40 (item (iii) of "What is not established here"), 1156-1163 (Remark `cb:rem:use`), 1272-1274
(Remark `cb:rem:c2-reading`), and the map notes of `cb:thm:c3` and `cb:rem:use`.

Checked against the sources:
- `C3U2/tools/compose.py:151`: a record is counted only if `certified` is true, lrat_check is `c VERIFIED` and
  cake_lpr is `s VERIFIED UNSAT`.
- `C3LEAN/README.md` §4 says "A record counts as certified by the criterion of `compose.py`" and "Each one records that
  both checkers accepted its proof". It also says that the collapsed leaf of `rev_uncertified_leaf_passes` "has no
  certified record".
- `C2FINAL/gen_lean.py:3-7, 16-17` (`ok`): status UNSATISFIABLE, both verdict strings, and a matched CNF hash.
- `C2FINAL/README.md:150` uses "certified record" for the same thing.

So the new phrase "a run record in which both proof checkers, cake_lpr and lrat-check, are recorded as accepting the
proof" is exact for both splits. The parenthetical "(the project's term for such a record: ``certified'')" is also
true for both splits.

The fixer departed from the suggested gloss ("a recorded cake_lpr verdict"), and that choice is right. The project's
term requires both verdicts, so the suggested gloss would define it wrongly. The cake_lpr anchor is still in place:
Remark `cb:rem:use` says that lrat-check verdicts are supporting only and that only the cake_lpr verdict counts.
- Lines 111-114 of `WRITEUP/note/symmetric_extremal.tex` were re-read and match.
- `WRITEUP/SYMMETRIC.md` §3 ("Revised 6 November 2026") and `LRATCHECK20261105` exist.
- The overview sends the reader to `cb:rem:use` directly after the list.
- The phrasing matches sr.tex:257-258 and mb.tex:1097-1098 ("accepted by both checkers"; cake_lpr is the verdict that
  counts).

Remaining occurrences of the word:
- cb.tex: only the quoted project term at line 38 and the Lean names `certifiedKeys` and `rev_uncertified_leaf_passes`.
- "verified" does not occur. "proved" occurs only in negations (lines 28, 163 and 1183).
- The map has no "certif" except the label `cb:def:certifiedkeys` and that Lean name.
- No other section repeats the old wording: grep for "counts as certified", "uncertified node" and "certified record"
  over sections/*.tex finds nothing.

### F2 [completeness, major] the C3L package was named nowhere: resolved

New item at cb.tex:1484-1501, at the end of "Not covered, deliberately".
- `C3L/C3Encoding.lean` contains only two imports (Gen, Case).
- A parse of the four files finds 41 declarations: 39 `def`, 1 `structure` and 1 `abbrev`, and no theorem, lemma,
  example or instance. They split as follows:
  - Gen.lean: 33, in namespace `C3`; the `Tables.*` defs are in `C3.Tables`;
  - Case.lean: 4, in namespace `C3`;
  - Emit.lean: 4, in the root namespace (with `open C3`).
- A script compared the names in the item with the declaration list: all 41 names are there and no extra name is.
  Only the namespace name `C3` is set with `\lean` without being a declaration.
- Grouping the names into enumerations, helpers, variables and literal tables, and clauses matches the code.
- "writes, for parameters m and k, the base CNF ... and the node CNFs (the base CNF followed by the unit clauses of a
  node) as DIMACS files": checked against Emit.lean:3-6 and 25-53. `writeCnf` writes the header
  `p cnf nv (nc + #units)`, then the base clauses, then the units. `lakefile.toml` declares `lean_exe c3_dimacs` with
  root `C3Encoding.Emit`.
- "states no theorem (C3L/README.md)": README line 16.
- "agreement recorded in C3L/logs":
  - `compare_base.log`: 19 parameter pairs IDENTICAL (m = 11, k = 7 gives `bf0e502e...`);
  - `compare_nodes.log`: 40 MATCH;
  - `compare_all_nodes.log`: 1641 MATCH, 0 MISMATCH.
- "`c3_base_sound`, planned in PLAN.md, is not in the repository":
  - PLAN.md:74 states it;
  - no `.lean` file in the worktree contains the name (`.lake` and `.git` excluded);
  - the name occurs only in `C3L/PLAN.md`, `C3L/README.md` and `AUDIT3/reports/A2_threefold.md`.
- The pointer to item (ii) and `\S\ref{cb:sec:overview}` is correct and renders as "§1.1".

### F3 [completeness, major] the AUDIT2 Lean files were named nowhere: resolved

New paragraph "Audit scripts of results outside Stage 1" at cb.tex:1510-1519, directly after "Treated in another
section".
- AUDIT2 holds exactly five `.lean` files, and all five were read in full.
- `A1/A1Dump.lean` defines `cube` at line 5 and `main` at line 6, in the root namespace. `main` is an IO program that
  writes `caseTable` entries with `(treeOf s).leaves`, then `upTable`, then `V1L.hullLeaves`, to the file
  `args.head!`. Its comment (lines 2-3) gives the purpose: "for comparison with my Python decoding of the source files".
- The other four files contain only import, open and set_option lines, comments, and `#check`, `#print`,
  `#print axioms` and `#eval` commands.
- Names and namespaces confirmed:

  | name | location |
  |---|---|
  | `V2L.caseTable` | V2-L/V2L/Facts.lean:22 |
  | `V2L.upTable` | V2-L/V2L/Facts.lean:19 |
  | `V2L.treeOf` | V2-L/V2L/Trees/Table.lean:601 (namespace V2L opens at line 145) |
  | `V1L.hullLeaves` | V1-L/V1L/Leaves.lean:1249 |
  | `V2L.mirrorExclusionLine_final` | V2-L/V2L/FinalTree.lean:28 |
  | `V1L.hullVertexLine_of_leaves` | V1-L/V1L/Main.lean:115 |
  | `Mir.mirrorExclusionLine_of_unsat` | H3/MirrorEncoding/Line.lean:139 |

- "an adversarial review of the project's mirror-class result" is the title of `AUDIT2/TASK.md`.
- "outside Stage 1": H3-V1L-V2L is a Stage 2 unit (`reviews/doc-r1-completeness.md` §5), and the wording follows
  fd.tex:1242.
- No section restates these theorems as statements: there is no `\leanref` to a `V2L.`, `V1L.` or `Mir.` name.
  sr only describes them in prose, in Remark `sr:rem:mirror-line`.

Unit completeness: all 20 Lean files under C3LEAN, C2FINAL, C3L, AUDIT2, AUDIT3 and ES7SPLIT are now named in cb.tex.
The AUDIT3 and ES7SPLIT files are listed as treated in section sa.

## 2. Diff review, hunk by hunk

Hunks:
- (a) item (iii), lines 36-40;
- (b) Remark `cb:rem:use`, lines 1156-1163;
- (c) Remark `cb:rem:c2-reading`, lines 1272-1274;
- (d) the new C3L item, lines 1484-1501;
- (e) the new AUDIT2 paragraph, lines 1510-1519;
- the map rows `cb:thm:c3` and `cb:rem:use`.

Referee checks:
- **Statements.** No statement that restates a Lean declaration was changed. The two edited remarks have no Lean
  counterpart; their map rows have `-` in the Lean-name column. The label set (112 labels) is identical to the
  snapshot. The map still has 5 tab-separated fields per row and is ASCII only.
- **Claims about records.** All were checked against the sources (section 1). `C3LEAN/review/RevCtrl_pass.lean:307`
  is the theorem line of `rev_uncertified_leaf_passes` (namespace `C3Cover`).
- **Rigor.** No label is rounded up. C3L is described as a program that states no theorem, with its comparisons outside
  Lean. AUDIT2 is described as audit scripts. No hypothesis or CNF verdict is presented as proved.
- **Hygiene.** No machine path, no tool name, no macro definition and no package. cb.tex is ASCII only.
- **External references.** Only `sr:def:classes` (an export label) and `sa:sec` (defined at sa.tex:1); both were
  already there before the fix.

## 3. Compile

The wrapper `build/cb_recheck_r1_wrapper.tex` has the contract content. It was compiled twice from build with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
- Both runs exit 0 and give 18 pages.
- No errors, no "Missing $" and no overfull boxes.
- The only undefined references are `sr:def:classes` and `sa:sec`, which belong to other sections; this is expected in
  the standalone check.
- Run 2 printed "Label(s) may have changed". A third run was clean and left the `.aux` file unchanged, so this was
  normal convergence.
- Pages 1, 13, 14, 17 and 18 were rendered and inspected. Item (iii), Remark `cb:rem:use`, the C3L item and the AUDIT2
  paragraph are set cleanly.

## 4. Findings (all minor)

- **m1 (typography, introduced by the fix).** At cb.tex:1496-1497, "root namespace:" breaks at a line end as
  "names-pace" (p. 17 of the standalone PDF). Fix: write `name\-space`, which is a discretionary hyphen and defines no
  macro, or reword to "(no namespace)".
- **m2 (process; not a cb file).** `appendix_map.tex` was generated at 20:03, before the map edit at 20:41. Its rows
  481-482 still carry the old cb notes "certification checked outside Lean" and "certification not established".
  Regenerate it with `python3 tools/make_appendix.py`. A trial run on a scratch copy finished without errors and
  produced the new notes. That copy has since been deleted.
