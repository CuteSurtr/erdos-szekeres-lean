# Section `fd` (Conventions and foundations), final pass round 1: independent re-check

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`), to RES (written `RES/...`) or to the
repository root (`ErdosSzekeres/...`). Lean core sources are cited from the Lean 4.24.0 source tree (the toolchain of
`lean-toolchain`), as `src/lean/...`. Nothing under REPO was modified; no Lean, Lake or solver was run.

## Verdict

**pass.** The one finding is resolved correctly. The edit introduces no blocker, major or minor defect. One new
**minor** finding is reported below (R1). It concerns the completeness of the extended search list in principle and
affects no claim of the document.

| # | finding (fix log) | severity | fixer's action | re-check |
|---|---|---|---|---|
| 1 | rule (a) does not search for `+native`, `Lean.ofReduceBool`, `Lean.ofReduceNat`, `debug.skipKernelTC` | minor | fixed | **resolved** (fd.tex:69-75, 79-83) |
| R1 | (new) the extended list still misses `bv_decide`/`bv_check`, the `(native := true)` configuration form and `debug.byAsSorry` | minor | - | open, optional; no claim affected |

## Inputs

- `snapshots/final-r1-pre/fd.tex`: SHA-256 `30a24eeedd68...`, 1324 lines. `sections/fd.tex`: `024e2fef3985...`, 1332 lines.
- `snapshots/final-r1-pre/fd.map.tsv` and `sections/fd.map.tsv`: both `81af16b44cbb...`, 41 lines (identical).

## 1. Finding 1: resolved

The finding allowed the change only if none of the four strings occurs outside comments in the Lean files cited by
the document. I checked that condition independently. My scripts are `build/fd_recheck_r1/imports.py`,
`imports_over.py`, `cited.py`, `scan.py` and `modules.py`. I did not reuse the fixer's scripts or file lists.

**Whole repository.** There are 1064 tracked `.lean` files at commit `7e32ee259`, the same set as on disk outside
`.lake`. A raw, case-sensitive search finds 0 occurrences of `+native`, `ofReduceNat` and `skipKernelTC`, and 4 of
`ofReduceBool`. All four are inside module doc comments (`/-! ... -/`):
`RES/ENCBLEAN/EncB/KernelCheck.lean:27`, `RES/ENCBLEAN/EncB/KernelCheckB.lean:55`, `RES/H/ETVEncoding/Audit.lean:9`
and `RES/H2/D3Encoding/Audit.lean:4`. I checked each in context.

**Who imports these four files.** I built the import graph over all 1064 files, resolving each import in the context
of its own Lake package (root package; `ENCBLEAN`; `ENCBLEAN/geo`, which requires `ENCBLEAN`; `H`, which requires the
root; `H2` and `H3`, which require `H`; `C3L`; `V1-L`; `V2-L`; `V2-L2`). Imports that do not resolve this way (401
of them, from standalone experiment and audit files) were linked to every file whose path ends with the module path,
which over-approximates the graph. Even so, the set of files that transitively import the four is only the four
themselves plus the root modules `RES/ENCBLEAN/EncB.lean`, `RES/H/ETVEncoding.lean` and `RES/H2/D3Encoding.lean`.

**Cited files.** The section files, the twelve maps, `appendix_map.tex`, `proofs.tex` and `bibliography.tex` contain
124 distinct `.lean` names. 122 of them resolve to 100 repository files; the bare names `Capstone2.lean`,
`KeyOrder.lean` and `OrbitConsistency.lean` are counted with both of their candidates. The other two names,
`MirrorPolygons.lean` and `small_polygons.lean` (mm.tex:53), are source files of the assembled
`RES/MIRRORETV/lean/MirrorMain.lean` (its line 9) and are not in the repository; the new sentence's qualifier "of the
repository" fits them. The forward import closure of the 100 files has 781 files (681 imported). This matches the
fixer's counts. A raw search of the 781 files finds none of the four strings, and none of the 7 files above is cited
or in the closure.

**Other ways of citing.** The claim also holds under broader readings of "cites":
- *Declaration level.* Every research declaration named without its file (`EncB.encB`, `EncB.CubesUnsat64`,
  `EncB.BlockCCW`, `EncB.wordSpec`, `EncB.Geo.*`, `D3.orient_reflC`, `Mir.*`, `V1L.*`, `V2L.*`) is defined in a file
  outside the 7 (for example `RES/ENCBLEAN/EncB/Coded.lean`, `Cover.lean`, `RES/H3/MirrorEncoding/Line.lean`).
  Such a file therefore does not import a file with a hit.
- *Module level.* The module names quoted in the text (`ErdosSzekeres.Definitions`, ..., `ErdosSzekeres.Vendor.ETV.Main.Main`)
  resolve to files in the closure. `ErdosSzekeres` itself is used as a namespace or as the main-library directory,
  and the main library has no hit.
- *Directory level.* `ErdosSzekeres/Vendor/ErdosSzekeresConvex/` (fd.tex:262) has four files, all in the closure.

**Outside comments, over the 781-file closure.** I used a scanner that handles nested block comments, line comments
and strings. It finds no `sorry`, `admit`, `axiom` declaration, `native_decide`, `+native`, or `native` of any kind;
no `ofReduceBool`, `ofReduceNat` or `reduceBool`/`reduceNat`; no `skipKernelTC` and no `debug.` option; and no
`bv_decide`/`bv_check`, `implemented_by`, `extern` or `addDeclWithoutChecking`. The options set are only
`maxHeartbeats`, `maxRecDepth`, `Elab.async`, `exponentiation.threshold`, `pp.*` and `linter.*`. The only `unsafe` is
`ErdosSzekeres/Omission/CoupledLrat.lean:13-14`. That file is an elaborator that evaluates two `String` arguments at
elaboration time and adds the result with the core `addDecl`, which runs the kernel check unless
`debug.skipKernelTC` is set (`src/lean/Lean/AddDecl.lean:18-28`), so it is not a soundness hole. So every
application of rule (a) remains valid in substance, as the new sentence says.

**Applications of rule (a).** I read each passage: fd.tex:253-264 and 318-320; ll.tex:49-51; lg.tex:64; oc.tex:91;
pc.tex:99-101; sr.tex:63-66; mm.tex:77-78; mb.tex:84-87; cb.tex:66; ec.tex:59; sa.tex:102-103. Each concerns files
named in the document. Those files and their imports lie in the 781-file closure, so the new sentence supplies the
four new strings for every application, as it claims.

**Parentheticals, checked against the Lean 4.24.0 sources.**
- `native_decide` is a synonym for `decide +native`: `src/lean/Init/Tactics.lean:1320` and `:1402`.
- `Lean.ofReduceBool` and `Lean.ofReduceNat` are "the axioms through which values computed by Lean's compiler or
  interpreter enter a proof": `src/lean/Init/Core.lean:2343-2403`. The kernel invokes the interpreter on
  `reduceBool`/`reduceNat`, and these two axioms turn the results into equations. A grep of `Init`, `Std` and `Lean`
  shows no other axiom of this kind; `Lean.trustCompiler : True` is only a marker.
- `debug.skipKernelTC` is "an option that skips the kernel's type check": `src/lean/Lean/Environment.lean:75-78`
  ("skip kernel type checker").

## 2. Diff review (`diff -u` snapshot vs current)

The map is identical. `diff -u` shows one hunk in fd.tex, containing two change blocks; every other byte of the file
is unchanged.
- **fd.tex:70-75 (rule (a) list).** The `sorry` parenthetical moved next to `sorry` with its wording unchanged, and
  "declaration and no" became "declaration, no". Added: `+native` with the synonym remark, `\lean{Lean.ofReduceBool}`
  or `\lean{Lean.ofReduceNat}` with the remark on the axioms, and `\lean{debug.skipKernelTC}` with the remark on the
  kernel check. Content and grammar are correct. `\texttt` is used for `decide +native`, which contains a space;
  `\lean` (`\nolinkurl`) only for names without spaces.
- **fd.tex:79-83 (new sentence).** It is a true raw-search claim (section 1 above). It covers imports, which rule (a)
  needs, and it says "of the repository", which correctly excludes the two non-repository names of mm.tex:53. The
  conclusion "every application of (a) ... remains valid" follows from it for the four new strings.
- **Checks.**
  - No statement environment, label or Lean statement was touched. The 43 `\label` lines are identical, so no Lean
    declaration needed re-reading.
  - No rigor label was rounded up or down. No "verified", "certified" or "proved" appears in lines 66-86, and no
    hypothesis is presented as proved.
  - There is no machine path and no tool name in fd.tex or fd.map.tsv.
  - No macro or package is defined. The new lines are ASCII only, with no trailing whitespace and no tabs.
  - Nothing outside the finding changed.

## 3. Compile check

From `build/` I compiled my own wrapper `fd_final_recheck_r1_wrapper.tex`, which has the contract's content, twice
with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`. The outputs are in `fd_final_recheck_r1_run1.txt`,
`fd_final_recheck_r1_run2.txt` and `fd_final_recheck_r1_wrapper.log`.
- Both runs exit with status 0. There are 0 errors (no `!` line, no "Missing $", no undefined control sequence), 0
  overfull boxes, and no rerun warning (the one "Rerun" match is the `rerunfilecheck` package banner).
- There are 10 underfull boxes. The same 10 appear when the snapshot is compiled the same way
  (`fd_final_recheck_r1_snapwrapper.tex`), shifted by 8 lines, and none is in the edited lines.
- The only undefined references are export labels of other sections, as expected: `ll:def:66-70`, `ll:def:hv`,
  `ll:def:peel`, `mb:thm:baek`, `oc:lem:perm`, `oc:lem:rot-inv`.
- The output has 17 pages. I rendered pages 1-2 (`fd_final_recheck_r1_p-01.png`, `-02.png`) and checked them: the
  passage typesets cleanly. The break after `debug.` in `debug.skipKernelTC` is the document's usual
  break-after-dot, as in `MirrorOdd.`/`hasConvexNGon_of_le` on page 1.

## 4. New finding

**R1 (minor; optional; fd.tex:69-75).** The extended search list of rule (a) is still not a complete list of the
ways to reach `Lean.ofReduceBool` or to bypass the kernel's checks. In Lean 4.24.0:
- `bv_decide` and `bv_check` build their proofs with `Lean.ofReduceBool` (`src/lean/Init/Tactics.lean:1795`;
  `src/lean/Lean/Elab/Tactic/BVDecide/Frontend/BVDecide.lean:298`).
- `decide (native := true)` and `decide (config := { native := true })` set the same option as `+native`
  (`valConfigItem`, `src/lean/Init/Tactics.lean:480`). Neither contains `+native` or `native_decide`.
- `debug.byAsSorry` elaborates `by` blocks as `sorry` (`src/lean/Lean/Elab/Term/TermElabM.lean:1280`) without the
  lower-case string `sorry` in the source.

None of these occurs in the repository: a raw search finds no `bv_`, no `byAsSorry`, no `native :=` and no `debug.`,
and every `native` is inside a comment. So no application of (a) is affected and no claim of the document is false.
The fixer followed the finding's own list, as the final-pass rules require.

If a later pass touches rule (a), a short fix would be: search for any `native` instead of `+native`; add `bv_decide`
and `bv_check`; widen `debug.skipKernelTC` to any `debug.` option; and widen the global sentence to match. The
searches above already confirm that it would stay true.

## 5. Notes (no action needed)

- **Unit-level reading.** The raw claim of the new sentence relies on "Lean file ... that this document cites"
  meaning files named in the document, or files holding declarations it names. Two comment-only occurrences
  (`KernelCheck.lean:27`, `KernelCheckB.lean:55`) lie in the unit `ENCBLEAN`, which ll.tex:743 and lg.tex:103 name as
  a unit. If someone read that as citing every file of the unit, the words "outside comments" would make the claim
  hold under every reading. No application of (a) concerns those files.
- **Raw versus outside comments (predates this edit).** Rule (a) does not say whether its text search excludes
  comments. Read raw, the old strings do occur in comments in the closure. `native_decide` appears in "no
  `native_decide`" remarks at `RES/C3LEAN/C3Cover.lean:13`, `RES/ENCBLEAN/EncB/Gen.lean:35`,
  `RES/V1-L/V1L/Cover.lean:8` and `RES/V2-L/V2L/Facts.lean:11`. `admit` appears as part of "admits" at
  `ErdosSzekeres/Suk/BaseOrder.lean:17`. All are comments. This was not introduced by the edit and was outside the
  finding.
