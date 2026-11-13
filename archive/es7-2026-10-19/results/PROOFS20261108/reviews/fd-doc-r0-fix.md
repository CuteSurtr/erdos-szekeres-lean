# fd, document round doc-r0: fixer log

**Inputs**
- Notes: `build/open_minors.json`, key `fd`. There are three notes: m1 and m2 from `reviews/fd-p1-diff.md`, and m1 from `reviews/fd-p1-referee.md`.
- Snapshot taken before editing: `snapshots/doc-r0-pre/fd.tex` and `snapshots/doc-r0-pre/fd.map.tsv`.

**Paths.** Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `tools/`), to RES (`LAYERLEAN/...`, `SYMLEAN/...`, `H2/...`) or to the repository root (`ErdosSzekeres/...`).

**What was run.** Read-only tools only: cat, sed, grep, diff, shasum, python3 for text checks, and pdflatex/pdftotext under `nice -n 15`. I did not run lake, lean, elan, git or any solver.

## Notes

| # | note (lens, location) | summary | action | location now | check / reason |
|---|---|---|---|---|---|
| 1 | diff m1; fd.tex:242-244 (axioms evidence, research files) | "the six cited research files" no longer identifies a set. Coverage also cites `H2/D3Encoding/Geometry.lean` and `SYMLEAN/review/ReviewSanity.lean`, and the axioms paragraph cites `SYMLEAN/AffineReductionAxioms.lean`. | **fixed** | fd.tex:243-245 | The text now reads: "A text search of the six research files of the table of sources finds no sorry, admit, axiom declaration or native_decide". See check 1 below. |
| 2 | diff m2; fd.tex:53-56 (rigor labels, Lean-checked) | The allowance of `Lean.ofReduceBool` and `Lean.trustCompiler` covered only a proof that uses `native_decide` directly. `#print axioms` also reports these axioms for indirect use. | **fixed** | fd.tex:53-57 | The text now reads: "for a declaration whose proof uses Lean's native_decide, directly or through a declaration on which it depends, the two further axioms ... are allowed as well". See check 2 below. |
| 3 | referee m1; fd.tex:411-417, Lemma `fd:lem:rot`(b) | Part (b) is tagged `rotAff`, so the matrix form ρ(p)=c+R(p−c)=Rp+(c−Rc) was implicitly Lean-checked. `rotAff` does not state it. | **fixed** (the referee's second option: mark it like ρ(c)=c) | fd.tex:414-419 | See check 3 below. |

**Check 1 (note 1).**
- **The six files.** The table of sources lists exactly six research files: `LAYERLEAN/LayerLemma.lean`, `SYMLEAN/SymmetricReduction.lean`, `SYMLEAN/AffineReduction.lean`, `LEANEXT/orbit/OrbitConsistency.lean`, `MIRRORETV/lean/MirrorMain.lean` and `SYMLEAN/mirror/ReductionThreeClasses.lean`.
- **Hashes.** I recomputed the SHA-256 prefixes, and all six match the table.
- **Text search.** grep finds no `sorry`, no `admit`, no `axiom` declaration and no `native_decide` in any of them. The word "axiom" does not occur in them at all.
- **Other cited research files.** The same search is clean for `Geometry.lean`, `ReviewSanity.lean` and `AffineReductionAxioms.lean`. I did not add them to the sentence: their declarations are not cited as Lean-checked (Coverage says so), and `AffineReductionAxioms.lean` repeats `AffineReduction.lean` plus print commands.

**Check 2 (note 2).**
- **Toolchain.** `Init/Core.lean` of the v4.24.0 toolchain declares `axiom trustCompiler : True` (:2340), which `reduceBool` references (:2361-2363), and `axiom ofReduceBool` (:2392). So the note is right.
- **The parenthetical.** "(no declaration cited in this section is of this kind)" must still hold under the wider reading.
  - **Declarations with a printed axioms line.** Every cited declaration that has one shows only standard axioms.
  - **The others.** These are `HasConvexNGon.card_le`, `Suk.convexPosition_of_negative_triples`, the three `reflectY` simp lemmas, and the definitions `Invariant` ×3, `rotAbout` ×3 and `rotAff`. Their closures lie in Mathlib, in the main-library files that were text-searched (fd.tex:189-196), and in the six research files.
  - **Imports.** The six research files import only `ErdosSzekeres.*` and `Mathlib.*`.
  - **Mathlib.** The pinned Mathlib (`f897ebcf72cd…`) mentions `native_decide` only in a docstring (`Mathlib/Data/Nat/Prime/Defs.lean:152`) and in the linter that forbids it (`Mathlib/Tactic/Linter/DeprecatedSyntaxLinter.lean`).
  - **Result.** The parenthetical stays true.

**Check 3 (note 3).**
- **What `rotAff` states.** `rotAff` (LayerLemma.lean:311-317) has `toFun := rotAbout c θ`, `linear := Matrix.toLin' !![cos θ, -sin θ; sin θ, cos θ]` and `map_vadd'`, which says ρ(v+p) = R v + ρ(p). The matrix form is not stated there. So the note is right.
- **New parenthetical.** It now says that the matrix form ρ(p)=c+R(p−c)=Rp+(c−Rc) of Definition `fd:def:rot` and the identity ρ(c)=c are written steps, and that Lean proves the latter at line 330 of the proof of `invariant_erase_centre` (LayerLemma.lean:325).
- **What stays Lean-checked.** The Lean-checked content of (b) is now exactly what `rotAff` states: the affine law with linear part R_θ.
- **Why the second option.** The matrix form, and in particular its second expression (obtained by linearity), is not a Lean declaration. Marking it as a written step is the conservative label and agrees with the rule at fd.tex:76-79. Its written proof (the proof of (b)) is unchanged.
- **Lean source re-read before and after the edit.** LayerLemma.lean:298-300 (`rotAbout`), :311-317 (`rotAff`) and :325-333 (`invariant_erase_centre`, with `have hcc : rotAbout c θ c = c` at :330) are unchanged, and the cited lines still carry the declarations.
- **No table file states the matrix form.** I listed every rotation declaration in the 15 files of the table. They give only:
  - the complex form (`rotAbout_eq_crot`, `toC_crot`);
  - the polar form (`OrbitConsistency.rotAbout_polar`, :355);
  - a tangent-functional identity (`LayerLemma.lin_rotAbout`, :794);
  - orientation identities.

  So the Coverage sentence "We found no declaration in the files of the table of sources that states one of them in the form given here" stays true.
- **Other sections.** No other section refers to `fd:lem:rot`. `ll:lem:rot`(b) in ll.tex states only the affine law for `rotAff`, which is the same reading.

## Other changes

1. **Coverage, written steps (fd.tex:1194-1197).** This follows from note 3. The `fd:lem:rot` item now starts: "the matrix form of Definition `fd:def:rot` and the identity ρ(c)=c in (b) (the latter a step of the proof of `LayerLemma.invariant_erase_centre`)".
2. **Map `sections/fd.map.tsv`, row `fd:lem:rot` (note column only).**
   - The (b) entry now reads "rotAff (affine packaging: linear part R_theta, rho(p + v) = rho(p) + R_theta v)".
   - The written steps now begin "the matrix form rho(p) = c + R_theta (p - c) = R_theta p + (c - R_theta c) of fd:def:rot and rho(c) = c in (b) (the latter proved in Lean inside invariant_erase_centre, ...)".
   - Label, kind, Lean names and lines are unchanged.
   - The TSV still has 41 lines, each with 5 fields, ASCII only and LF line endings.
   - A dry run of `note_tex` from `tools/make_appendix.py` on this row succeeds; the token `fd:def:rot` becomes `Definition~\ref{fd:def:rot}`.
   - **`appendix_map.tex` was not regenerated here.** It needs a run at document level.
3. **Not acted on.** The referee's "Notes (no finding)" remark that p_1, p_2, p_3 clash with coordinate subscripts in `fd:lem:orient`(d) is not in the open list. It is style only, so I left the text unchanged.

## Checks after editing

**Compile.** I ran `build/fd_wrapper.tex` twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
- Both passes exit 0, and the PDF has 16 pages.
- There are 0 errors and 0 "Missing $".
- There are 0 overfull boxes, so none is above 1pt.
- No label is multiply defined, and there is no rerun warning.
- The only undefined references are `ll:def:66-70`, `ll:def:hv`, `ll:def:peel`, `mb:thm:baek`, `oc:lem:perm` and `oc:lem:rot-inv`, all export labels of other sections.
- pdftotext shows the three edited passages as intended.

**Diff against the snapshot.** fd.tex has exactly four hunks (rigor labels, axioms sentence, `fd:lem:rot`(b) parenthetical, Coverage). fd.map.tsv has one changed row.

**Labels, references and map.**
- The 43 labels are identical to the snapshot, in the same order, and none was removed or renamed.
- No new `\ref` target was added: `fd:def:rot` was already referenced.
- The 40 statement environments still match the 40 map rows in label, kind and order.

**Hygiene.**
- fd.tex and fd.map.tsv contain no machine path, no tool name and no non-ASCII character.
- There is no `\newcommand` or `\usepackage`.
- "verified" and "certified" occur only in the existing sentence that bans them.
