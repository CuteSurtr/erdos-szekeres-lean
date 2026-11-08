# Front matter fix after the whole-document review, round 1

Files edited (front files only): `proofs.tex`, `preamble.tex`, `bibliography.tex`, `tools/make_appendix.py`
(paths relative to STAGE). Snapshot of the previous versions: `snapshots/docfix-r1-pre/`. No section file, section map
or `appendix_map.tex` was edited, and `tools/make_appendix.py` was not run on STAGE: the existing `appendix_map.tex`
(generated 20:03 with the old generator) is still in place, and the builder has to regenerate it.

Result: 24 findings; 23 fixed, 1 declined (a section-file matter). No statement environment was touched, so no Lean
declaration had to be re-read for fidelity. The Lean names quoted in the new scope section were checked in the
records: `EncB.Geo.sixfold66_of_cubes64` (`ENCBLEAN/geo/ES8Geo/Main.lean:91`, type
`EncB.CubesUnsat64 → ErdosSzekeres.LayerLemma.Sixfold66` per `ES8Geo/Audit.lean:99`), `Mir.MirrorExclusionLine`
(`H3/MirrorEncoding/Line.lean:94`), and `V2L.mirrorExclusionLine_final` (`V2-L/V2L/FinalTree.lean:28`, whose
hypotheses are CNF unsatisfiability facts).

## Per finding

| # | finding | action | location |
|---|---|---|---|
| 1 | Dum25 missing; name form | fixed. Added `Dum25` exactly as P1 ("B. Dumitru", arXiv:2512.24061). The sr fixer has already changed sr.tex to "B.~Dumitru" (sr.tex:286), so section and bibliography now agree (the records say the middle initial was never verified: `LIT/RELATED.md:237`, `NOVELTY20261106/README.md:132`). | bibliography.tex |
| 2 | abstract omits cited theorems | fixed (with 3): the abstract names both exceptions. | proofs.tex abstract |
| 3 | abstract overclaims completeness | fixed. The new sentence says that each section gives a written proof checkable without Lean "with two exceptions": Baek's theorem and the cups-caps theorem of Erdős and Szekeres are cited, not reproved; statements marked computer-assisted are reduced to a finite computation, stated precisely and carried out by a machine, not by hand "except where a section gives a proof by hand as well". That last clause matches fd's revised Purpose paragraph and its qualified label "computer-assisted in Lean". The abstract also says that a theorem with unproved hypotheses "is established here only as that conditional statement". | proofs.tex abstract |
| 4 | "Stage 1" undefined; scope | fixed. New unnumbered front section "Scope of Stage 1", which appears in the contents and the bookmarks (`\phantomsection\section*`). (a) Treated records and their sections: LAYERLEAN; LEANEXT orbit, merged, keys, phase, linked, capstone, es7corr; ES8SYM/lean; PRIMEFOLD/compat/lean; SYMLEAN SymmetricReduction, AffineReduction and mirror/ReductionThreeClasses; MIRRORETV/lean; C3LEAN; C2FINAL; AUDIT3/A1_reduction; ES7SPLIT/review/equivalence. Also the main-library declarations restated in fd and mb. (b) What these records contain that is not restated: copies, tests, controls, `#print`/`#check`, the review files in LEANEXT/review, SYMLEAN/review and MIRRORETV/review, and MIRRORETV/lean/FarFlat.lean. C3L and AUDIT2 state no theorems (checked: 0 theorem/lemma lines). (c) Planned for Stage 2: ENCBLEAN, H, H2, H3, V1-L, V2-L, V2-L2. Planned for Stage 3: the compact checker and the rest of the main library. (d) ES8SLACK is not treated; written proofs are in ES8SLACK/proofs.md. The abstract points to this section. Title changed to "Written proofs of Lean-checked results, Stage 1: symmetric point sets", broken by hand after "results,", with the full title kept as the running head. | proofs.tex |
| 5 | works cited but not listed | fixed. Added `Sch26`, `CakeLPR` and `DT`, copied from P1 (with `Dum25`, see 1). The archive is now identified in the References (title, version, date, DOI), and the scope section says that six bridge files of Section 10 are adapted from it. Not done here: the in-text pointer at mb.tex:47 is in a section file. Forwarded to the mb fixer as optional ("archive (title, DOI in the References)"). | bibliography.tex; proofs.tex "Works cited" |
| 6 | appendix intro does not fit the rows | fixed in the generator. The intro now uses fd's path sentence (ErdosSzekeres/, docs/, experiments/, scripts/ root-relative). It says that for a remark the Lean column names the declarations the remark discusses and that a remark does not restate a Lean statement. Rows without a Lean name now print the tag found in the statement head: "written step" (39 rows), "Mathlib" (fd:def:conv, oc:fact:sign, oc:def:keys), or a dash for remarks (61 rows). | tools/make_appendix.py |
| 7 | undefined-label guard omits sa | fixed: `LABEL_KEY` is built from `KEYS`. Tested: a note with `sa:lem:nonexistent` now stops the generator. | tools/make_appendix.py |
| 8 | overfull token `m8_fix_build.log:29,35,` | fixed. `IDENT` accepts a line list `(?:,\d+)*`, so the path is set in typewriter type with break points. The existing (stale) appendix is input with `\esmapbreaks` (new preamble macro: an escaped underscore in roman text is a break point, as in identifiers), so the current build has no overfull box either. The pc map note is unchanged. | tools/make_appendix.py; preamble.tex; proofs.tex |
| 9 | SMQH25 differs from P1; entries not tied to the text | fixed. Full P1 entry (CICM 2025, LNCS 16136, 29-47, doi). New header comment. Every entry is now cited with `\cite` from the front matter ("Works cited", "Evidence outside Lean"). The sections keep their inline citations, so the standalone compile rule is unaffected. | bibliography.tex; proofs.tex |
| 10 | empty PDF metadata | fixed: `\hypersetup{pdftitle=...}`; pdfinfo shows the title. pdfauthor not set: the document has no author line. | proofs.tex |
| 11 | scope never stated | fixed (same change as 4). | proofs.tex |
| 12 | heads cannot break inside Lean names | fixed. `\lean` and `\dirn` are now robust commands built on `\es@tt`, which sets typewriter text with explicit penalties: 0 after `. / _`, 100 after `:`, none after the last character (so "docs/," never breaks before the comma; the reviewer's version did break there, p3). A `\kern0pt` after each character prevents ligatures and hyphenation. Math mode is handled through `\text`. All `\lean`/`\dirn` arguments in the sections, the appendix and the front files (3,178 distinct file-argument pairs) and all 1,231 distinct `\leanref` arguments use only `[A-Za-z0-9._/:'-]` (checked), and none is used in math mode or in a moving argument. Same-sections comparison (frozen copy): badness-10000 lines 342 to 79, all underfull hbox 463 to 209. Penalty 700 was also tested (as `\nolinkurl` uses): 121 and 249, so 0 was kept. | preamble.tex |
| 13 | raw label strings with part suffixes | fixed. `LABEL_TOK` accepts `(a)`, `(b)(ii)`, ... after a label; the output is `\ref{label}(a)`. All five cases now resolve (fd:rem:orient-lean, ec:lem:orbit-dvd, mb:prop:cap113 twice, mb:rem:axis). | tools/make_appendix.py |
| 14 | overfull row on p167 | fixed (same as 8). | as 8 |
| 15 | subsection heading stranded at a page foot | fixed, and the reviewer's patch was extended. (a) `\@trivlist`: `\@beginparpenalty=\@M` while a run-in heading is pending (the reviewer's patch). Alone, this left 2 headings stranded in the full document and 5 of 46 in a synthetic test. Cause: the `\label` after `\begin{lemma}[...]` puts a `\write` whatsit in the vertical list after that penalty, and the next glue is a legal break point. (b) Until the next paragraph starts (`para/begin` hook), `\@esphack` adds `\nobreak` in vertical mode. (c) A `\paragraph` that directly follows a run-in heading (cb 11.2) ends that heading's line with `\nobreak` and no `\@secpenalty`. Checks: synthetic test 9/46 (old preamble) to 0/46. Full document: 3 pages ending with "N.M. Title." (old front files) to 0. No page ends with a paragraph heading, in the official build and in both regenerated-appendix builds. | preamble.tex |
| 16 | doubled names ("Remark Remark 4.20") | fixed. A label directly after a name word (singular or plural) is attached with `~` and gets no second name. Plural lists ("Theorems A, B and C") get bare references. A wrong name word is replaced by the right one, with a warning on stderr (none occurs now). | tools/make_appendix.py |
| 17 | "export label" residue; empty `; ;` items | fixed. `clean_note` turns "export label (with X)" into "with X" and "(export label L)" into "(L)", deletes the remaining "export label", and drops empty items. | tools/make_appendix.py |
| 18 | ASCII notation in notes | fixed. Runs of ASCII mathematics become math: `<= >= != -> => <->`, `ne`, `notin`, Greek letter names (not `omega`, which in the notes is the Lean tactic), `x^n` and `x^(..)`, `R_theta`, `a*b` (juxtaposition after a number, otherwise `\cdot`), `|S|`, `exp`/`det`/`card`/`id`. Ranges `a..b` become en dashes, also between identifiers (`closedP1`--`closedP8`), and `...` becomes `\dots`. A run never crosses a label or `; : .`; after a comma it continues only with an expression that has an operator; unmatched brackets and clause punctuation stay outside the math. All about 60 converted notes were read (e.g. "$0<\beta-\alpha,0<\delta-\beta,\delta-\alpha<\pi$", "$x\ne\rho x$", "$\exp(2\pi i/m)$, m cast to C"). | tools/make_appendix.py |
| 19 | names and files misaligned; camel-case splits | fixed. The table now has 3 columns: Statement 0.10, "Lean declaration; file and line" 0.49, Note 0.35. Each declaration is followed by its file and line on an indented line (`\hangindent`), so pairs cannot drift apart. The camel-case break rule is dropped, and there is no break after the last character. All 470 rows keep exactly their kinds, labels, Lean names and files (row-by-row comparison of old and regenerated appendix). | tools/make_appendix.py |
| 20 | `\paragraph` plain roman; ar uses `\textbf` | fixed: `\paragraph` is now bold and run in. The `\textbf` wrappers in ar have meanwhile been removed by the ar fixer (no `\paragraph{\textbf` left), so all sections look the same. | preamble.tex |
| 21 | empty PDF metadata (same as 10) | fixed. | proofs.tex |
| 22 | numbered entries never cited | fixed: all 11 entries are cited from the scope section (and keep their numbers). | proofs.tex |
| 23 | capitalisation of short names in heads (fd, sr, cb vs the rest) | declined for the front fixer. The heads are in section files, which this fixer may not edit, and the reviewer marks the change as optional. Forwarded to the fd, sr and cb fixers. | sections/fd.tex, sr.tex, cb.tex |
| 24 | build: overfull box (same as 8 and 14) | fixed. | as 8 |

## Compile check

Whole document from STAGE into `build/front-r1` (live sections at about 21:20, existing `appendix_map.tex`, three passes
of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build/front-r1 proofs.tex`):
- every pass exits 0;
- errors 0, lines containing "Warning" in the log 0, undefined references or citations 0;
- overfull boxes 0;
- underfull hbox 188 (76 with badness 10000);
- 191 pages;
- no page ends with a stranded heading;
- pdfinfo Title "Written proofs of Lean-checked results, Stage 1: symmetric point sets".

Additional checks, in scratch copies under `build/front-r1/`:
- `regen-live/`: a copy of the live sections and maps with the new generator gives 470 rows. The full build is clean:
  0 errors, 0 overfull, 187 pages, no stranded heading.
- `exp/` against `base/`: same frozen sections, old and new front files (the figures quoted under 12 and 15).
- `wrap/`: standalone section wrappers for cb, sa and fd compile with the new preamble (exit 0, no overfull). Only the
  expected cross-section references are undefined.

## For the builder

- Regenerate `appendix_map.tex` with the new `tools/make_appendix.py` (it was run only on scratch copies here). The
  appendix then shrinks by about 4 pages. `\esmapbreaks` in `proofs.tex` stays harmless after regeneration.
- The References entry `CakeLPR` contains the word "Verified" because it is part of the paper's title, copied from P1.
  It is not a rigor label of this document.
