# Section `fd` (Conventions and foundations), final pass round 1: fix log

Input: the one finding assigned to `fd` in the final pass, round 1.

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`), to RES (research records) or to the
repository root (`ErdosSzekeres/...`). `fd.tex:N` refers to the edited file.

Snapshot taken before editing: `snapshots/final-r1-pre/fd.tex` (SHA-256 `30a24eeedd68`, 1324 lines) and
`snapshots/final-r1-pre/fd.map.tsv` (SHA-256 `81af16b44cbb`, 41 lines). After editing: `sections/fd.tex`
(`024e2fef3985`, 1332 lines) and `sections/fd.map.tsv` (unchanged, `81af16b44cbb`).

`diff` of the snapshot and the edited file: two hunks only, both in the paragraph "Rigor labels" (fd.tex:70-75 and
fd.tex:79-83). No label was added, removed or renamed. No statement environment was touched, so no Lean declaration
had to be re-read and the statement map needs no change.

## Summary

| # | finding | severity | action | location (edited file) |
|---|---|---|---|---|
| 1 | rule (a) does not search for `+native`, `Lean.ofReduceBool`, `Lean.ofReduceNat`, `debug.skipKernelTC` | minor | fixed | fd.tex:69-75 (search list of rule (a)); fd.tex:79-83 (new sentence after the list of kinds) |

1 finding, 1 fixed, 0 declined.

## 1 (fixed): the search list of rule (a)

The finding asked for a change only if none of the four strings occurs outside comments in the Lean files cited by
the document. That is the case. In fact none occurs at all, even in comments, in the cited files and in the project
files they import.

### Search (read-only; scripts `build/fd_final_r1_cited.py`, `build/fd_final_r1_imports.py`,
`build/fd_final_r1_importers.py`; list of cited files `build/fd_final_r1_cited_files.txt`)

- **Cited files.** The twelve section files contain 124 distinct `.lean` names. They come from three places: the
  file arguments of the `\leanref` heads (42 distinct), the sources paragraphs and tables, and running text. 122 of
  the names resolve to files of the repository at commit `7e32ee259`. That gives 100 files, counting both
  candidates for the bare names `Capstone2.lean`, `KeyOrder.lean` and `OrbitConsistency.lean`, which occur in
  `LEANEXT` and in `ENCBLEAN/geo/ES8Geo`. The remaining two names, `MirrorPolygons.lean` and `small_polygons.lean`
  (mm.tex:53), are source files listed in the header of `MIRRORETV/lean/MirrorMain.lean` and are not in the
  repository. Every `.lean` name in the twelve maps, in `appendix_map.tex`, in `proofs.tex` and in
  `bibliography.tex` is among the 100 files. The directory
  `ErdosSzekeres/Vendor/ErdosSzekeresConvex/`, cited by directory in fd.tex:262, is covered by the import closure
  and by the whole-repository search below.
- **Raw search of the 100 cited files** (comments included) for `+native`, `ofReduceBool`, `ofReduceNat` and
  `skipKernelTC`: 0 occurrences.
- **Transitive project imports of the cited files:** 781 project files (the 100 cited files plus 681 imported
  ones; the only other import roots are `Init`, `Mathlib` and `Std`). Raw search: 0 occurrences.
- **Whole repository:** 1064 `.lean` files, which are exactly the tracked `.lean` files (`git ls-files`). The search
  skips `.lake`. Raw occurrences: `+native` 0, `ofReduceNat` 0, `skipKernelTC` 0, `ofReduceBool` 4. The 4 are all in
  module doc comments (`/-! ... -/`, "Axiom audit: ... no `Lean.ofReduceBool`"), at
  `ENCBLEAN/EncB/KernelCheck.lean:27`, `ENCBLEAN/EncB/KernelCheckB.lean:55`, `H2/D3Encoding/Audit.lean:4` and
  `H/ETVEncoding/Audit.lean:9`. The only files that import these four are the root modules `ENCBLEAN/EncB.lean`,
  `H2/D3Encoding.lean` and `H/ETVEncoding.lean`. No file imports those root modules, and the document cites none of
  these seven files. Outside comments the four strings never occur in the repository.
- For information only, with comments removed and the whole repository searched: no `native` at all (so neither
  `native_decide` nor a `native := true` configuration), no `reduceBool` or `reduceNat`, no `bv_decide`, no `debug.`
  option, and no `implemented_by` or `extern`.

### Sources for the new parentheticals (Lean 4.24.0 source tree, the toolchain of `lean-toolchain`)

- `src/lean/Init/Tactics.lean:1320` and `:1402`: "`native_decide` is a synonym for `decide +native`".
  `:1346-1347`: "`decide +native` uses the native code compiler (`#eval`) to evaluate the `Decidable` instance,
  admitting the result via the `Lean.ofReduceBool` axiom".
- `src/lean/Init/Core.lean:2392` (`axiom ofReduceBool (a b : Bool) (h : reduceBool a = b) : a = b`) and `:2403`
  (`axiom ofReduceNat (a b : Nat) (h : reduceNat a = b) : a = b`). The docstrings of `reduceBool`/`reduceNat` say that
  the kernel invokes the Lean interpreter to evaluate them, and that the compiler and interpreter become part of the
  trusted code base.
- `src/lean/Lean/Environment.lean:75-78`: `debug.skipKernelTC`, "skip kernel type checker. WARNING: ... your proofs
  will not be checked by the Lean kernel".

### Old wording (fd.tex:69-75 of the snapshot)
```
    exists as well; together with a text search of the file and of the project files it imports that
    finds no \texttt{sorry}, no \texttt{admit}, no \texttt{axiom} declaration and no
    \texttt{native\_decide} (a declaration that uses \texttt{sorry} compiles with a warning only, so the
    search, not the exit status, excludes it);
  \item a \texttt{\#guard\_msgs} command, compiled in a build whose log is saved, that pins the output of
    \texttt{\#print axioms} for the declaration or for a declaration whose statement or proof uses it.
  \end{enumerate}
```

### New wording (fd.tex:69-83)
```
    exists as well; together with a text search of the file and of the project files it imports that
    finds no \texttt{sorry} (a declaration that uses \texttt{sorry} compiles with a warning only, so the
    search, not the exit status, excludes it), no \texttt{admit}, no \texttt{axiom} declaration, no
    \texttt{native\_decide}, no \texttt{+native} (as in \texttt{decide +native}, of which
    \texttt{native\_decide} is a synonym), no \lean{Lean.ofReduceBool} or \lean{Lean.ofReduceNat} (the
    axioms through which values computed by Lean's compiler or interpreter enter a proof) and no
    \lean{debug.skipKernelTC} (an option that skips the kernel's type check);
  \item a \texttt{\#guard\_msgs} command, compiled in a build whose log is saved, that pins the output of
    \texttt{\#print axioms} for the declaration or for a declaration whose statement or proof uses it.
  \end{enumerate}
  A text search of every Lean file of the repository that this document cites, and of the project files
  these import, finds none of the strings \texttt{+native}, \texttt{ofReduceBool}, \texttt{ofReduceNat}
  and \texttt{skipKernelTC}, so every application of~(a) in this document remains valid, also where it
  reports only a search for \texttt{sorry}, \texttt{admit}, \texttt{axiom} declarations and
  \texttt{native\_decide}.
```

Notes on the edit:
- The parenthetical about `sorry` keeps its words. It moved next to `\texttt{sorry}` so that it still refers to the
  item it explains now that the list is longer. "declaration and no" became "declaration, no" because the list goes on.
- The new sentence says "of the repository" because the two names in mm.tex:53 are cited but are not files of the
  repository. It names the four strings that were actually searched for (substrings, so `Lean.ofReduceBool`,
  `Lean.ofReduceNat` and `debug.skipKernelTC` are covered). Several sections apply rule (a) or report a text
  search or scan. In `fd` these are fd.tex:253-264 and fd.tex:318-320. The other sections are `ll`, `lg`, `oc`,
  `pc`, `sr`, `mm`, `mb` and `sa`; their line numbers are left out because other fixers may be editing those files.
  These passages report the absence of some or all of `sorry`, `admit`, `axiom` and
  `native_decide`. The new sentence supplies the four new strings for every cited file and its imports, so none of
  these passages needs to change.
- Vocabulary: no "verified", "certified" or "proved"; no new macros. `\texttt` is used for `decide +native` because
  it contains a space; `\lean` only for space-free names.

## Compile check

From `build/`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error fd_wrapper.tex`, run twice (logs
`build/fd_final_r1_run1.txt`, `build/fd_final_r1_run2.txt`):
- exit 0 on both runs; 0 errors (no `!` lines, no "Missing $", no undefined control sequence);
- overfull boxes: 0 (so 0 over 1pt); no rerun warning;
- undefined references: only export labels of other sections, as expected in the standalone check
  (`ll:def:66-70`, `ll:def:hv`, `ll:def:peel`, `mb:thm:baek`, `oc:lem:perm`, `oc:lem:rot-inv`);
- 17 pages. Pages 1-2, which contain the edited passage, were rendered (`build/fd_final_r1_p-01.png`, `-02.png`) and
  checked visually. The only line break inside a Lean name is after `debug.` in `debug.skipKernelTC`, a break point
  the preamble allows after `.`.

No machine path and no tool name in `sections/fd.tex` or `sections/fd.map.tsv` (checked with grep).
