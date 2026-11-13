# Front matter re-check, final pass, round 1

Scope: the edit logged in `reviews/final-front-r1-fix.md`. Paths are relative to STAGE, to REPO (commit `7e32ee259`)
or to RES, as in the contract. I read the current files and the sources myself and did not rely on the fix log.

**Verdict: pass.** All three findings are resolved correctly. No blocker or major finding remains, and none was
introduced. One minor point is listed at the end; it is optional and comes from before this edit.

## Diff against `snapshots/final-r1-pre/` (`diff -u`)

- `proofs.tex`: two hunks. Lines 39-43 ("Treated here") and lines 91-93 ("Works cited"). Each old line is replaced, and
  the source line is split in two so that the following lines stay byte-identical.
- `preamble.tex`: one hunk. Lines 43-44 are inserted directly after the `\makeatother` on line 42.
- `bibliography.tex`: identical (exit 0).

Nothing else in the three front files changed. Neither version of the front files defines a label. The only new
references are one more `\ref{sr:sec}` and one more `\ref{mm:sec}`. Both are defined: Section 7 (sr) and Section 9
(mm), as the aux file shows. No section file was edited for these findings. `cb.tex` still reads `namespace` at
line 1496, and no section has a discretionary hyphen or a `\hyphenation`. The section changes since the snapshot are
those of the concurrent section fixers, and none of them concerns these findings.

## Findings of the round

### 1. [minor] proofs.tex "Works cited": citation forms. Resolved.

New text: "The sections cite published works inline, by author together with title or arXiv number, by author alone
or by name; the References list them." I checked every inline citation in the live sections:

- **Author with title:** Rockafellar (ll.tex:88), Rudin (fd.tex:1205, lg.tex:164; later "Rudin, op. cit." at
  fd.tex:1209), Baek (mb.tex:201, sa.tex:421-422), and Erdős and Szekeres (mb.tex:231-232).
- **Author with arXiv number:** Dumitru (sr.tex:287), Subercaseaux, Mackey, Qian and Heule (sr.tex:300-301), and
  Baek (sr.tex:291).
- **Author alone:** "M.~Schroeder's archive~\cite{Sch26}" (mb.tex:47). This is the only `\cite` in the sections.
- **By name:** Lean 4 and Mathlib (for example fd.tex:5-6).

The other names in the sections are named theorems (Carathéodory, Heine-Borel, Krein-Milman, Mazur-Ulam) or software
(cake_lpr, lrat-check, Batteries). None of them is a citation of a published work. Every work cited is in the
References, so the new sentence is accurate. It renders correctly on p.4.

### 2. [minor] proofs.tex "Treated here": main-library restatements outside fd and mb. Resolved.

New text: "...(Section~10); a few such declarations are also restated in Sections~7 and~9. These four sections list
the main-library files concerned, with their hashes." The section numbers render as 7 = sr and 9 = mm.

- **Which sections restate main-library declarations.** Statement heads cite `\leanref{...}{ErdosSzekeres/...}` only
  in fd (31), mb (35), mm (2, both in `mm:def:config`) and sr (1, `sr:lem:supports`). The other eight sections have
  none, and the maps agree. ll.tex:25, lg.tex:38-52, ar.tex:34-40 and oc.tex:536 only recall definitions and point to
  fd. sa.tex:356-359 and :403 recall the notions of mb's Baek theorem and point to mb. None of these passages is a
  statement environment that restates a main-library declaration. sa's ETV vendored-file mention stays a recall of
  mb's Theorem.
- **The declarations in REPO.** `ErdosSzekeres.Suk.convexPosition_of_strict_supports` is at
  `ErdosSzekeres/Suk/SupportingLines.lean:28` and is applied at `SYMLEAN/SymmetricReduction.lean:511`.
  `ErdosSzekeres.Omission.Configuration` is at `ErdosSzekeres/Omission/Realization.lean:9` and
  `Configuration.HasCap` at `:64`. Both are used throughout `MIRRORETV/lean/MirrorMain.lean`, for example
  `capacity16` at :1529 and `cfg` at :1584. So they are declarations "that these files use".
- **Fidelity.** `sr:lem:supports` and `mm:def:config`(a),(b) restate the declarations faithfully: `Finset`, and the
  strict `0 < orient p q r` for `r ≠ p`; the fields `point`, `xOrder`, `generalPosition`; and all-triples caps with
  `orient < 0`. So "restated" is correct. Neither statement was touched by this edit.
- **Hashes.** I checked fd (8 files), mb (11), sr (1) and mm (1). For each section, every main-library file cited in
  its statement heads appears in its own Sources list, and the listed SHA-256 prefix matches `shasum -a 256` of the
  REPO file. Examples: sr.tex:42 `SupportingLines.lean` `6a8e12677685`; mm.tex:40 `Realization.lean`
  `ae4970e0808e`. "These four sections list the main-library files concerned, with their hashes" is therefore true.
  I re-ran this check at 22:00 on the current files with the same result.

### 3. [minor, typography] "names-pace" in cb. Resolved, in the preamble only.

- **The change.** `preamble.tex:43` is a one-line comment. `preamble.tex:44` is `\hyphenation{name-space
  name-spaces}`, placed directly after the `\makeatother` (line 42) that closes the block opened at line 19 with the
  statement tolerance. `\hyphenation` is a TeX primitive, so it adds no macro and no package.
- **Effect.** In the build, p.149 now reads "In C3L/C3Encoding/Gen.lean, name-|space C3:". No line anywhere in the
  PDF ends in "names-". The control builds show that the exception changes no other page.

## Compile

I built the whole document from STAGE with three passes of
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build/final-recheck-front-r1 proofs.tex`
at 21:56. I hashed all inputs (the front files, `appendix_map.tex` and `sections/*.tex`) before and after. They were
unchanged after the build and again at 22:00. I did not run `tools/make_appendix.py`.

- Every pass exits 0. The document has 188 pages.
- Errors (`^!`): 0. Lines containing "Warning": 0. Undefined references: 0. Multiply defined labels: 0.
- Overfull boxes: 0, so none above 1pt.
- Underfull hbox: 187 (76 with badness 10000). Underfull vbox: 15, page-level.
- rerunfilecheck reports that `proofs.out` did not change on pass 3.

**Control builds** (`build/final-recheck-front-r1-ctl/pre` and `.../post`) used the same live sections and
`appendix_map.tex`, once with the snapshot front files and once with the current ones, three passes each.

- Both builds exit 0, have 188 pages, 0 errors, 0 overfull boxes and 187 underfull hboxes. Underfull vboxes go from
  16 (pre) to 15 (post).
- Pages whose text differs: 3-32 and 149.
  - **Pages 3-32.** The non-space characters differ by exactly the characters of the two edited sentences. The rest is
    a reflow of about two lines through Section 1, absorbed by p.32. The per-page differences there are only
    positional, including pdftotext math-placement artifacts. No page in that range ends with a heading.
  - **Page 149.** It differs only by "names-pace" becoming "name-space".
- The text of the post build is identical to that of the main build.

The fix log says the reflow ends on p.7. With the sections as they are now, after concurrent section edits, it ends on
p.32. This does not affect the result.

## Hygiene

`proofs.tex`, `preamble.tex` and `bibliography.tex` contain no machine path and no tool name. The new text
has no rigor word: no "verified", "certified" or "proved", and no rigor label is raised or lowered. Pages 3, 4 and 149
were also checked visually; the layout is fine.

## Remaining points

- **[minor, optional; not introduced by this edit]** `bibliography.tex:1` is a source comment and is not rendered. It
  still says "The sections cite them inline, by author and title", which now disagrees with the rendered "Works cited"
  sentence. Under the byte-identical rule the fixer was right to leave it in this pass. A later pass may align it,
  for example "...inline, by author together with title or arXiv number, by author alone or by name; ...".
