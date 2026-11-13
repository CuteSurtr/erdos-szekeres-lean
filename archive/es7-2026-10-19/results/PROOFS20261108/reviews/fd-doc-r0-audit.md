# Section `fd`, round doc-r0: diff audit

**Lens:** diff.

**Inputs**
- Pre-edit snapshot: `snapshots/doc-r0-pre/fd.tex` and `snapshots/doc-r0-pre/fd.map.tsv`.
- Current files: `sections/fd.tex` (1244 lines) and `sections/fd.map.tsv`.
- Fix log: `reviews/fd-doc-r0-fix.md`.
- The notes it addressed: `reviews/fd-p1-diff.md` (m1, m2) and `reviews/fd-p1-referee.md` (m1). These are the three
  notes listed for `fd` in `build/open_minors.json`; there are no others.

**Path conventions.** Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`, `tools/`), to RES
(`LAYERLEAN/...`, `SYMLEAN/...`, `LEANEXT/...`, `MIRRORETV/...`) or to the repository root (`ErdosSzekeres/...`,
`lean-toolchain`, `lake-manifest.json`). "The toolchain source" means the source tree of the Lean v4.24.0 toolchain
named in `lean-toolchain`. "The pinned Mathlib" means the local Mathlib checkout whose `.git/HEAD` is
`f897ebcf72cd16f89ab4577d0c826cd14afaafc7`, the revision in `lake-manifest.json`.

**What was run.** Read-only tools only: cat, sed, grep, diff, cmp, shasum, python3 for text checks, one sympy script
(`build/fd_docr0audit_sym.py`, run under `nice -n 15`), and pdflatex, pdftotext and pdfinfo under `nice -n 15`. I did
not run lake, lean, elan, git or any solver. Nothing under REPO was modified, and `appendix_map.tex` was not
regenerated.

## Verdict: PASS

- **Findings.** There is no blocker, no major and no minor finding.
- **Notes.** All 3 notes marked fixed are fixed correctly. None was declined.
- **Hunks.** Every hunk is mathematically correct, every touched Lean citation matches the source, every new factual
  claim is true, and no rigor label is rounded up.
- **Hygiene.** No machine path or tool name appears.
- **Build.** Both pdflatex passes exit 0, with 0 errors and 0 overfull boxes.

## 1. Hunks checked

`diff -u` gives exactly 4 hunks in `fd.tex` (25 changed lines) and 1 changed row in `fd.map.tsv`. Outside these there
is no change: the first difference (`cmp`) is at line 54. Labels and `\ref` targets are unchanged (section 3).

| # | Location (current file) | Change | Check |
|---|---|---|---|
| 1 | Rigor labels, *Lean-checked*, lines 53-57 | "for a declaration whose proof uses Lean's `native_decide`" becomes "... uses Lean's `native_decide`, directly or through a declaration on which it depends, ..." | Correct. See 1a. |
| 2 | Axioms evidence, research files, lines 243-245 | "the six cited research files" becomes "the six research files of the table of sources" | Correct. See 1b. |
| 3 | Lemma `fd:lem:rot`(b), parenthetical, lines 414-419 | The matrix form $\rho_\theta(p)=c+R_\theta(p-c)=R_\theta p+(c-R_\theta c)$ "of Definition `fd:def:rot`" is now marked, together with $\rho_\theta(c)=c$, as a written step; `rotAff` is credited only with the affine law | Correct. See 1c. |
| 4 | Coverage, written steps, lines 1194-1197 | The `fd:lem:rot` item now starts "the matrix form of Definition `fd:def:rot` and the identity $\rho_\theta(c)=c$ in (b) (the latter a step of the proof of `LayerLemma.invariant_erase_centre`)" | Correct. See 1c. |
| map | Row `fd:lem:rot`, note column only | (b) now reads "rotAff (affine packaging: linear part R_theta, rho(p + v) = rho(p) + R_theta v)". The written steps now begin with the matrix form "of fd:def:rot" | Correct. See 1d. |

### 1a. Hunk 1 (native_decide allowance)

**Toolchain facts.** The toolchain source `Init/Core.lean` has:
- `namespace Lean` at line 2334;
- `axiom trustCompiler : True` at line 2340;
- `opaque reduceBool`, whose body is `have := trustCompiler; b` (lines 2361-2363), with the comment "This ensures that
  `#print axioms` will track use of `reduceBool`";
- `axiom ofReduceBool` at line 2392.

`Lean/Elab/Tactic/ElabTerm.lean:421` builds the `native_decide` proof term with ``mkConst ``Lean.ofReduceBool``. The
docstring of the tactic (`Init/Tactics.lean:1405-1410`) says that `Lean.ofReduceBool` "will show up in `#print
axioms` for theorems using this method or anything that transitively depends on them". The two axiom names are
therefore right, and the widened wording ("directly or through a declaration on which it depends") is exactly what
`#print axioms` reports.

**The parenthetical "(no declaration cited in this section is of this kind)" under the wider reading.**
- **Declarations with a printed axioms line.** Every one shows only `propext`, `Classical.choice` and `Quot.sound`,
  so its dependency closure contains no `native_decide`.
- **Declarations without a printed line.** These are `HasConvexNGon.card_le`,
  `Suk.convexPosition_of_negative_triples`, the three `reflectY` simp lemmas, and the definitions `Invariant` (three
  copies), `rotAbout` (three copies) and `rotAff`. Their closures lie in the sources below, and none of these sources
  uses native evaluation:
  - **Main library.** `grep -r` over `ErdosSzekeres/` (including `Vendor/`) finds no `native_decide`,
    `decide +native`, `native := true`, `ofReduceBool`, `reduceBool` or `trustCompiler`.
  - **Research files.** The six research files of the table contain none of these strings. They import only
    `ErdosSzekeres.*` and `Mathlib.*` (all `import` lines listed).
  - **Pinned Mathlib.** `native_decide` occurs only in the docstring `Mathlib/Data/Nat/Prime/Defs.lean:152` and in the
    linter `Mathlib/Tactic/Linter/DeprecatedSyntaxLinter.lean` that forbids it.
  - **Other Lake packages.** The local checkouts of Batteries, Aesop, Qq and Plausible are at the manifest revisions
    (HEADs compared). These, ProofWidgets, ImportGraph, LeanSearchClient and Cli contain no `native_decide`,
    `decide +native` or `ofReduceBool`.
  - **Lean core.** In the toolchain's `Init/` and `Std/`, the only matches are the axiom declarations themselves and
    the docstring of the tactic, whose `example ... := by native_decide` is inside the docstring (lines 1402-1414).

So the parenthetical stays true. The sentence is consistent with the *Computer-assisted* bullet (lines 65-75; the `native_decide` clause is at lines 69-71). It
also agrees with the two other sections that mention `native_decide` (`cb.tex:64` and `ll.tex:43-45`): neither cites
a declaration of that kind.

### 1b. Hunk 2 (text search of the research files)

**The six files.** The table of sources (lines 118-138) lists 9 main-library files and exactly 6 research files:
- `LAYERLEAN/LayerLemma.lean`
- `SYMLEAN/SymmetricReduction.lean`
- `SYMLEAN/AffineReduction.lean`
- `LEANEXT/orbit/OrbitConsistency.lean`
- `MIRRORETV/lean/MirrorMain.lean`
- `SYMLEAN/mirror/ReductionThreeClasses.lean`

The new phrase therefore identifies this set. The phrase "table of sources" is used the same way at lines 1181, 1224
and 1239.

**Hashes.** I recomputed all 15 SHA-256 prefixes of the table, and all match.

**Text search.** In each of the six files, `grep` counts are 0 for `sorry`, `admit` and `native_decide`. A grep for an
`axiom` declaration keyword (optionally preceded by attributes or modifiers) also gives 0. The sentence is true.

### 1c. Hunks 3 and 4 (Lemma `fd:lem:rot`(b) and Coverage)

**Lean source re-read** (`LAYERLEAN/LayerLemma.lean`: 1148 lines, SHA-256 `afb8542dceb0…`, namespace
`ErdosSzekeres.LayerLemma` from line 37 to line 1148):
- `rotAbout` at :298-300 is the coordinate formula of Definition `fd:def:rot`.
- `rotAbout_eq_crot` is at :302, `rotAbout_injective` at :319 and `rotAbout_iterate` at :465.
- `rotAff` at :311-317 has `toFun := rotAbout c θ`, `linear := Matrix.toLin' !![cos θ, -sin θ; sin θ, cos θ]` and
  `map_vadd' p v`. That is, $\rho(v+p)=R_\theta v+\rho(p)$, which is the text's $\rho_\theta(p+v)=\rho_\theta(p)+R_\theta v$.
  `rotAff` does not state the matrix form.
- `invariant_erase_centre` is at :325, and line 330 is `have hcc : rotAbout c θ c = c := by`.

So:
- "its defining property being the identity $\rho_\theta(p+v)=\rho_\theta(p)+R_\theta v$" is accurate.
- "Lean proves the latter in the step at line 330 of the proof of `ErdosSzekeres.LayerLemma.invariant_erase_centre`,
  `LAYERLEAN/LayerLemma.lean:325`" is accurate.
- The statement of the lemma itself is unchanged, and its four `\leanref`s still resolve, to :302, :311, :465 and :319.

**Mathematics.** sympy (`build/fd_docr0audit_sym.py`) confirms four identities:
- $\rho(p)=c+R(p-c)$;
- $c+R(p-c)=Rp+(c-Rc)$;
- `map_vadd'`, that is, $\rho(v+p)=Rv+\rho(p)$;
- $\rho(c)=c$.

The written proof of (b) is unchanged and proves all three parts of (b).

**Rigor label.**
- The matrix form is not a Lean declaration. It is the coordinate formula of a Lean definition, rewritten with a
  matrix and expanded by linearity. Marking it as a written step is correct and conservative, and it matches the
  rule at lines 77-80 ("a part marked written step does not carry this label").
- The Lean-checked content of (b) is now exactly what `rotAff` states.
- No label is rounded up.

**Downstream use.** The proof of `fd:lem:affine-orient`(i) (line 568) uses the matrix form from `fd:lem:rot`(b).
- This is a written proof using a written step, which is fine.
- Part (i) keeps its own Lean tag, `OrbitConsistency.orient_rotAbout_inv`.
- No other section refers to `fd:lem:rot` (grep over all sections and maps).
- `ll:lem:rot`(b) in `ll.tex` (lines 405-407) states only the affine law for `rotAff`, which is the same reading.

**Coverage (hunk 4).**
- The item now names the matrix form, which is consistent with the lemma.
- The claim "We found no declaration in the files of the table of sources that states one of them in the form given
  here" still holds for the new item. I listed every `rot`/`crot` declaration in the six research files and grepped
  for `rotAbout` together with `*ᵥ`, `mulVec`, `toLin` or `!![`. The only hit is inside the proof of `rotAff`
  (:317).
- The other rotation identities are of other forms:
  - `toC_crot` and `rotAbout_eq_crot` (complex form);
  - `OrbitConsistency.rotAbout_polar`, :355 (polar form);
  - `LayerLemma.orient_rotAbout`, :472;
  - `LayerLemma.lin_rotAbout`, :794.
- The nine main-library table files contain no rotation.

### 1d. Map row

**Structure.**
- The TSV has 41 lines, each with 5 tab-separated fields.
- It uses LF endings only and contains no non-ASCII character.
- The 40 rows match the 40 statement environments in label, kind and order.
- In the `fd:lem:rot` row, the name and line columns equal the head's four `\leanref`s, and they are unchanged.

**Dry run of the appendix.** I imported `tools/make_appendix.py` and ran `collect_labels` and `note_tex` on all 40 fd
rows. KEYS was restricted to the eleven existing section files; see note N2. The result went to
`build/fd_docr0audit_maprows.tex`, and `appendix_map.tex` was left untouched.
- The token `fd:def:rot` becomes `Definition~\ref{fd:def:rot}`.
- `R_theta` and `rho_0` are set as `\texttt` with escaped underscores.

A scratch document (`build/fd_docr0audit_maptest.tex`) contains the preamble, `fd.tex` and these rows in the
generator's longtable. Both passes exit 0, with 0 errors and 0 overfull boxes, and the PDF shows "of Definition
1.12".

## 2. Fixer's dispositions

**Fixed: 3, all confirmed.**

| note | fix | audit |
|---|---|---|
| `fd-p1-diff` m1: "six cited research files" no longer identifies a set | the reviewer's suggested wording, verbatim (hunk 2) | **Confirmed** (1b). |
| `fd-p1-diff` m2: the allowance covered only direct use of `native_decide` | the suggested wording, with "on which it depends" for "it depends on" (hunk 1) | **Confirmed**. The parenthetical stays true (1a). |
| `fd-p1-referee` m1: the matrix form in (b) was implicitly credited to `rotAff` | the referee's second option: mark it as a written step, as for $\rho(c)=c$ (hunks 3, 4 and the map row) | **Confirmed** (1c, 1d). |

**Declined: 0.**

The referee's "Notes (no finding)" item about the notation $p_1,p_2,p_3$ in `fd:lem:orient`(d) was not in the open
list, and the fixer left it alone. This is acceptable. The points are introduced explicitly ("For all
$p_1,p_2,p_3\in R^2$"), so nothing is inaccurate or ambiguous.

**Other claims of the fix log.** The following were re-checked and are true:
- the 43 labels are identical, and in the same order;
- the `\ref` targets are identical;
- all 20 contract `fd:` labels are defined exactly once;
- the six research files import only `ErdosSzekeres.*` and `Mathlib.*`;
- the Mathlib `native_decide` occurrences are as stated;
- no table file states the matrix form;
- no other section refers to `fd:lem:rot`.

One claim of the log is wrong (note N1). It does not affect the section.

## 3. Compile check and hygiene

**Wrapper.** `build/fd_docr0audit_wrapper.tex` has the content of the contract wrapper (`diff` against
`build/fd_wrapper.tex` is empty). I ran, from `build/`, twice: `nice -n 15 pdflatex -interaction=nonstopmode
-halt-on-error fd_docr0audit_wrapper.tex`.
- Both passes exit 0, and the PDF has 16 pages.
- The log has 0 `!` errors, no "Missing $" and no "Undefined control sequence".
- There are **0 overfull boxes**, so none is above 1pt. There are 70 underfull boxes, which are cosmetic and as many
  as in round p1.
- No label is multiply defined, and there is no "may have changed" warning on pass 2.
- The only undefined references are `ll:def:66-70`, `ll:def:hv`, `ll:def:peel`, `mb:thm:baek`, `oc:lem:perm` and
  `oc:lem:rot-inv`. All six are contract export labels.

**Rendered text.** pdftotext shows the three edited passages as intended, with Definition 1.12 = `fd:def:rot` and
Lemma 1.14 = `fd:lem:rot`.

**Hygiene** (`fd.tex` and `fd.map.tsv`):
- There is no machine path (no absolute path into a private, user, home or temporary directory).
- There is no tool name and no non-ASCII character.
- There is no `\newcommand`, `\renewcommand`, `\def` or `\usepackage`.
- Rigor words in the changed lines: "Lean proves the latter" (line 418) describes where the Lean proof contains the
  step. It is the same wording as before the edit and is not a label. "verified" and "certified" still occur only in
  the sentence that bans them (line 82).

## 4. Findings

None.

## 5. Notes (no finding for the section)

**N1 (fix log only).**
- **The claim.** Check 1 of `reviews/fd-doc-r0-fix.md` says "The word 'axiom' does not occur in them at all" about
  the six research files. This is false.
- **Comments.** "axioms" occurs in doc comments at `SYMLEAN/SymmetricReduction.lean:16,50`,
  `SYMLEAN/AffineReduction.lean:16,50` and `SYMLEAN/mirror/ReductionThreeClasses.lean:42,76`.
- **Commands.** It also occurs in `#print axioms` commands at `MIRRORETV/lean/MirrorMain.lean:2662-2677` and
  `SYMLEAN/mirror/ReductionThreeClasses.lean:4221-4236, 4317-4322`.
- **No effect on the section.** None of these is an `axiom` declaration. The sentence in `fd.tex` ("no ... `axiom`
  declaration") is true, so no change to the section is needed.

**N2 (document level, not fd).**
- **The problem.** `tools/make_appendix.py` has `'sa'` in `KEYS`, but `sections/sa.tex` does not exist yet.
  `collect_labels()`, and therefore a document-level `python3 tools/make_appendix.py`, will stop with a missing-file
  error until section `sa` and its map are in place.
- **Current state.** `appendix_map.tex` is still the placeholder.
- **What works now.** The fd rows themselves generate and compile (1d).
