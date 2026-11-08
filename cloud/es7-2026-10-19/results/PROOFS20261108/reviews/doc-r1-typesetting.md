# Whole-document review doc-r1, lens: typesetting

Build checked: `build/doc-r1/proofs.pdf` (187 pages), `proofs.log`, `proofs.txt`, `proofs.toc`, `proofs.out`, `proofs.aux`
(all relative to STAGE). Scratch for this review: `build/doc-r1-typo/` (log parser, label checks, two tested preamble
patches and their test builds).

## Method

- **Log.** Parsed `proofs.log`, attributing every box warning to the section file being read and to the page shipped next
  (page numbers below are that page; for a paragraph that starts at a page foot they can be one page early). Found
  1 overfull box (49.4pt), 488 underfull hbox warnings (351 with badness 10000), 11 underfull vbox warnings, no errors,
  no undefined references, no rerun request, no missing characters or font substitutions. The 24 messages
  `ignored: Infinite glue shrinkage found in box being split` come from the appendix longtable (one per page) and
  have no visible effect.
- **Statement heads.** For each underfull line, located the enclosing statement in the source and kept the lines that lie
  in the head (before the bold closing `).` of the head). Result: 313 lines with badness 10000 in the heads of 138
  statements (list at the end).
- **Text.** Searched `proofs.txt` for `??` (none), backslash control words, braces and `$` (none; all `\` are set-minus
  signs), doubled words, raw label strings, `; ;`, line-end hyphenation inside identifiers (only `SHA-|256`), merged
  names from `\lean` with spaces (none: no `\lean`, `\dirn` or `\leanref` argument in the sources contains a space,
  macro or special character other than `'`). Checked every `Name~\ref{label}` in the sources and every
  "Lemma/Theorem/... N.M" in the text against the kind of the target: no mismatch (the only hits are external
  numberings: Rudin, Rockafellar, Baek, `MIRRORETV/PROOFS.md`, which the text names).
- **Pages viewed** (rendered at 70 dpi with pdftoppm, page 167 also zoomed): 1, 2, 3, 4, 5, 7, 8, 12, 18, 20, 23, 27,
  29, 32, 35, 37, 39, 40, 43, 44, 45, 55, 56, 61, 62, 63, 64, 69, 72, 73, 77, 78, 81, 90, 92, 97, 98, 100, 101, 102,
  106, 109, 112, 113, 114, 117, 119, 122, 123, 128, 129, 134, 137, 138, 142, 145, 146, 147, 148, 149, 150, 151, 152,
  153, 155, 160, 163, 167, 169, 175, 178, 180, 186, 187 (title page and contents; every section; all five tables;
  the largest displays; the pages with underfull vboxes; ten appendix pages; references).
- **TOC and outline.** Read `proofs.toc`, decoded the 98 bookmarks of `proofs.out`, ran `pdfinfo`.
- **Tests of the proposed fixes.** Compiled (nice, in `build/doc-r1-typo/`) the sections with the preamble plus the two
  patches given below; see F1 and F4.

## Findings

### F1 (major, front) Statement heads cannot break inside Lean names; 138 heads are set with very loose lines

amsthm sets a statement head in an `\hbox` and unboxes it into the first paragraph. `\lean`/`\dirn` use `\nolinkurl`,
whose break points are math-mode penalties; TeX does not create those in restricted horizontal mode, so inside a head a
name can break only at spaces (the preamble comment says as much). With `\es@sloppy` TeX then stretches the spaces.
Result: 313 lines with badness 10000 in 138 heads (fd 30 lines, ll 43, oc 45, pc 37, ec 14, sr 47, ar 50, mm 46, cb 1;
lg, mb and sa have none). On many pages the heads look broken, with interword gaps of several ems over 4 to 13
consecutive lines: p7 (Defs 1.5 to 1.10), p8 (Def 1.12, Lem 1.14), p12 (Lem 1.23), p20 (Lem 2.2), p23 (Lem 2.12,
13 lines), p43 (Lem 4.10), p44 (Lems 4.13 to 4.16), p55 (Lem 5.5, Def 5.6), p77 (Lem 7.5), p78 (Def 7.7), p81 (Lem 7.17),
p92 (Defs 8.4, 8.6), p98 (Cor 8.27, Thm 8.28), p102 (Lem 9.2), p103 (Lem 9.5), p106 (Prop 9.13).

Fix (preamble; tested): set `\lean` and `\dirn` as typewriter text with explicit break points, which survive the box.

```latex
\makeatletter
\def\es@tt#1{{\upshape\ttfamily\expandafter\es@ttloop\detokenize{#1}\es@ttstop}}
\def\es@ttloop#1{\ifx\es@ttstop#1\else\es@ttchar{#1}\expandafter\es@ttloop\fi}
\def\es@ttchar#1{#1\kern\z@\if.#1\allowbreak\else\if/#1\allowbreak\else\if_#1\allowbreak\fi\fi\fi}
\let\es@ttstop\relax
\renewcommand{\lean}[1]{\es@tt{#1}}
\renewcommand{\dirn}[1]{\es@tt{#1}}
\makeatother
```

(Put it in place of the two `\newcommand` lines, as `\newcommand`.) `\kern\z@` after each character prevents hyphenation
and ligatures; every current argument is alphanumeric plus `. _ / : - '`, which `\detokenize` handles; output glyphs
are unchanged (checked `_` and `'`). Full document with this patch and the one of F4, two passes: exit 0, no undefined
reference, overfull boxes 1 (the one of F3), underfull hbox warnings with badness 10000 351 -> 80 (fd 47 -> 4, oc 49 -> 6,
mm 57 -> 2, ec 14 -> 0, ar 54 -> 13, sr 47 -> 26, pc 38 -> 20), 187 -> 185 pages. Alternative without a preamble
change: put each `\leanref` of a head on its own line with `\\`, as mb and sa already do (their heads have no underfull
lines). After either fix all page references move; re-run the bottom-of-page check of F4. The tested files are
`build/doc-r1-typo/brk/lean_brk.tex` and `build/doc-r1-typo/head/patch.tex`; the full patched build is
`build/doc-r1-typo/full/fullw.pdf`.

### F2 (major, front) Raw label strings printed in the appendix

`tools/make_appendix.py` turns a note token into `Name~\ref{label}` only if the token is a label plus `)],;:.`; a part
suffix such as `(d)` defeats it, and the token is printed verbatim:

- p155, row Rem. 1.16 (`fd.map.tsv`, `fd:rem:orient-lean`): "of fd:lem:orient(d)";
- p169, row Lem. 6.39 (`ec.map.tsv`, `ec:lem:orbit-dvd`): "derives it from ec:thm:compat(a);";
- p180, row Prop. 10.36 (`mb.map.tsv`, `mb:prop:cap113`): "uses Theorem mb:thm:nine(a)" and "the proofs of mb:thm:nine(a)";
- p181, row Rem. 10.42 (`mb.map.tsv`, `mb:rem:axis`): "follows from mb:thm:refl32(b)".

Fix in the generator: accept `((?:\([a-z0-9]+\))*)` after the label and emit `\ref{label}` followed by the suffix
(together with F5, otherwise "uses Theorem mb:thm:nine(a)" becomes "Theorem Theorem 10.35(a)").

### F3 (major, front) Overfull line runs 49pt into the right margin (p167)

Appendix row Rem. 5.29 (`pc.map.tsv`, `pc:rem:word-scope`): the token `ENCBLEAN/logs/m8_fix_build.log:29,35,` fails the
generator's identifier pattern (`,35,`), so it is set in roman without break points; log: `Overfull \hbox (49.39687pt
too wide) in paragraph at lines 204--205` of `appendix_map.tex`; visible on p167 beyond the table rule and the
page-number edge. It is the only overfull box of the document. Fix: in the pc map write "lines 29 and 35 of
ENCBLEAN/logs/m8_fix_build.log", or let the generator accept `(?:,\d+)*` after a `:N` line number.

### F4 (major, front) Subsection heading alone at the foot of p101

"9.1. Reflection, configurations and sorting." (`mm.tex:94`) is the last line of p101; Definition 9.1 starts p102.
Cause: amsart subsection heads are run-in; when a statement follows directly, `\@trivlist` sets the pending head as a
one-line paragraph and `\@item` then adds `\@beginparpenalty` (-51), which invites a page break after the head. Any
reflow can strand another of the many "subsection + statement" pairs. Fix (preamble; tested on a synthetic page where
the unpatched head lands at the foot for 4 of 30 positions and the patched head never does; also in the full patched
build):

```latex
\makeatletter
\let\es@trivlist@orig\@trivlist
\def\@trivlist{\if@noskipsec\@beginparpenalty\@M\fi\es@trivlist@orig}
\makeatother
```

Not covered by this patch: a run-in subsection followed directly by `\paragraph` (cb 11.2 "Notation." + "Numbers."),
which in the patched build lands at the foot of p128. Re-check after any reflow: no page may end with a line of the form
"N.M. Title." (pdftotext plus a regular expression is enough).

### F5 (minor, front) Doubled names in appendix notes

"(Remark Remark 4.20)" p163 (`oc:thm:encoder`), "Lean encoding of Definition Definition 10.1" p178 (`mb:rem:config`),
"Lean encoding of Lemma Lemma 10.14" p179 (`mb:rem:boundary`), "how Lean proves Lemma Lemma 10.24" p180
(`mb:rem:generated`). The maps write "Remark oc:rem:parity" and the generator prepends the name again. Fix: when the
preceding token already is the name (singular or plural), emit only `~\ref{...}`; or drop the word in those four notes.

### F6 (minor, front) `; ;` and internal "export label" wording in appendix notes

The generator's `re.sub(r'(^|;\s*)export label(?=;|$)', r'\1', n)` leaves an empty item: "axioms.log; ; its proof uses"
in rows Lem. 3.7, Thm. 3.16, Thm. 3.20, Thm. 3.28, Lem. 3.30, Thm. 3.32 (p160 to 161). "export label" survives where it is
not a whole item: "(export label Lemma 4.14)" (Rem. 1.16), "(export label Lemma 4.7)" (Rem. 1.18), "export label (with
config_capacity113 as part (a))" (Thm. 10.35), "export label (with reflLine_eq_lineRefl)" (Thm. 10.38). The phrase is
workflow jargon a reader cannot interpret. Fix: delete every "export label" (and an emptied `;` item) in the generator.

### F7 (minor, front) ASCII notation in appendix notes

The maps must be ASCII, and the generator prints them as they are: about 80 occurrences of `<=`, `!=`, `->`, `=>`, `<->`,
`*`, `^`, `..`, `pi` and Greek letter names, for example "case beta'=delta' not covered" and "0<beta-alpha,
0<delta-beta, delta-alpha<pi" (p167), "n = s*k+e (e <= 1 ...)" (p186), "2*pi/m" (Rem. 1.13), "certs0..certs126" (p182).
Fix: a small translation table in the generator for non-identifier tokens (`<=` to `$\le$`, `!=` to `$\ne$`,
`->` to `$\to$`, `=>` to `$\Rightarrow$`, `pi` to `$\pi$`, Greek names, `a..b` to `a--b`).

### F8 (minor, front) Appendix: names and files of a row do not line up

In rows with several declarations, each `file:line` wraps to two lines in the 25% column while names take one or two,
so name i stands next to the second half of file i-1: p175 Lem. 9.2 (8 names, 16 file lines), p178 Def. 10.1
(8 names, 16 lines), p180 Lem. 10.28, p169 Def. 6.21, p186 Prop. 12.6. In the Note column the camel-case break points
split identifiers without a mark, so they read as two words: "general Position" (p175, Lem. 9.5), "Affine
Independent" (p153, Def. 1.4), "SYMLEAN/Symmetric Reduction.lean:423" (p180). Fix: set each declaration with its file
in one cell (name, then the file on a new indented line) and give that cell the width of the two columns; drop the
camel-case break rule or use it only where nothing else fits.

### F9 (minor, front) Paragraph headings are not distinguishable; ar sets them in bold

amsart sets `\paragraph` run-in in plain roman, so "Sources.", "Rigor.", "Axioms.", "Coverage." look like body text
(p29, p40, p64, p113). Only ar writes `\paragraph{\textbf{Sources.}}` (8 times, `ar.tex:25` to `:766`; p90, p100), which
also puts `\textbf` into `proofs.toc`. Fix: give `\paragraph` a bold or italic run-in style in the preamble and drop the
`\textbf` in ar.

### F10 (minor, front) Empty PDF metadata

`pdfinfo`: Title and Author are empty. Fix: `\hypersetup{pdftitle={Written proofs of the Lean-checked results, Stage 1:
symmetric point sets}}` (and pdfauthor if wanted) in `proofs.tex`.

### F11 (minor, front) Bibliography entries are never cited

There is no `\cite` in the document; the seven numbered entries [1] to [7] (p187) are not referred to, while the sections
cite the same works inline by author and title (Rudin p17 and p30, Rockafellar p20, Baek p115 and p150). Fix: cite the
entries with `\cite{...}` where the works are named, or set the list unnumbered as "Works cited".

### F12 (minor, front) Capitalisation of statement names differs by section

fd, sr and cb begin the short names in heads with a capital ("Definition 1.5 (General position; ...)"), the other nine
sections with a lower-case letter ("Lemma 3.5 (orientation of a regular-polygon triple; ...)"). Optional; amsart usage
is lower case.

### F13 (minor, lg) Odd unnumbered "Coverage" entry in the contents and the outline

`lg.tex:890` uses `\subsection*{Coverage}`, which gives an unnumbered "Coverage" line between 3.6 and 4 in the contents
(p1) and an unnumbered level-2 bookmark. Nine sections use `\paragraph{Coverage.}` (not listed); oc and cb use numbered
subsections (4.7, 11.11; cb refers to its own with `\S\ref{cb:sec:coverage}`). Fix: `\paragraph{Coverage.}` in lg.

### F14 (minor, fd) Quarter page left empty on p4

The sources table (`fd.tex:118`, a `center` + `tabular` of 15 files) does not fit at the foot of p4, so p4 ends with
"... SHA-256 hashes, are:" and about a quarter of the page blank (underfull vbox, badness 10000); the table opens p5.
Fix: let the list break (for example a two-column `itemize`, or the table in `\small` after the next paragraph).

### F15 (minor, fd) Very loose identifier paragraphs on p5 and p17

The "Axioms evidence" paragraph (`fd.tex:143`-`198`, p5; 7 lines with badness 10000, its first line "Axioms evidence.
Main library. The saved axiom audit" spread over the full width) and the Coverage paragraph (`fd.tex:1148`-`1179`,
p17; 10 lines) are long runs of Lean names. Fix: set them as itemized lists (one file or group per item) or inside
`{\raggedright ... \par}`.

### F16 (minor, mm) Loose identifier paragraphs and a gap on p101 and p112

The Sources paragraph (`mm.tex:32`-`56`, p101; 4 lines with badness 10000) and the Coverage paragraph
(`mm.tex:895`-`932`, p112; 6 lines) are set very loosely; p112 also shows a gap of about an inch before "Coverage."
(underfull vbox, badness 5504). Fix as in F15.

### F17 (minor, sa) Internal audit identifier in a heading

12.3 "The assembled bookkeeping of finding A1-F1" (`sa.tex:271`) shows in the contents an identifier that is explained
only in the text (finding F1 of audit A1). Suggest "The assembled statement (audit finding A1-F1)" or similar.

## Other observations (no finding)

- Underfull vboxes: p2 (contents), p5 (4927), p29, p40, p128, p129, p152 show no visible defect; p122 (mb, gap of about
  three lines before Definition 10.27) and p146 (sa, about five blank lines at the foot) are small reflow effects.
- Section heads near the foot: §2 on p18 and §4 on p39 have three lines of text after them; acceptable.
- Lemma 12.12 (p150) starts on the last line of the page with its lead-in sentence; acceptable.
- Body paragraphs with badness 10000 lines besides F15/F16: oc Coverage (p51, 3 lines), ar Coverage items (p100, 4),
  oc Sources item (p40, 1), pc items (p54, p56, p62, p63), mm p102, p106, mb p114, ar p93.
- All five tables (p5, p45, p61, p64, p146) fit the text width; the 64-digit hashes on p146 fit.
- Outline: 98 bookmarks, sections and subsections only; titles with math come out as "mt", "k=7", "ES(7)",
  "2^(m-1)", "7-gons" (via `\texorpdfstring`), all readable.

## Statement heads with underfull lines of badness 10000 (313 lines, 138 statements)

Page = page where the statement starts (can be one page early at a page foot); "n lines" when more than one.

- `fd` (17 statements, 30 lines): Def 1.1 (p6); Def 1.5 (p7); Def 1.6 (p7); Def 1.7 (p7); Def 1.9 (p7); Def 1.10 (p7, 3 lines); Lem 1.11 (p8); Def 1.12 (p8, 3 lines); Lem 1.14 (p8, 3 lines); Lem 1.15 (p9, 3 lines); Lem 1.20 (p11); Lem 1.22 (p11); Lem 1.23 (p12, 4 lines); Lem 1.24 (p12, 2 lines); Lem 1.26 (p12, 2 lines); Lem 1.33 (p15); Lem 1.38 (p16)
- `ll` (17 statements, 43 lines): Def 2.1 (p20); Lem 2.2 (p20, 5 lines); Def 2.3 (p21); Def 2.4 (p21); Lem 2.5 (p21, 2 lines); Lem 2.6 (p21, 3 lines); Def 2.11 (p23, 3 lines); Lem 2.12 (p23, 13 lines); Def 2.13 (p23); Lem 2.14 (p23, 4 lines); Lem 2.19 (p24, 2 lines); Lem 2.20 (p25); Lem 2.21 (p25); Lem 2.23 (p25); Def 2.27 (p26, 2 lines); Thm 2.28 (p27); Thm 2.29 (p27)
- `oc` (23 statements, 45 lines): Def 4.1 (p41, 2 lines); Lem 4.4 (p42); Lem 4.6 (p42); Lem 4.7 (p42); Def 4.9 (p43); Lem 4.10 (p43, 8 lines); Lem 4.13 (p44, 2 lines); Lem 4.14 (p44, 2 lines); Lem 4.15 (p44); Lem 4.16 (p44, 3 lines); Thm 4.18 (p44); Thm 4.19 (p45, 2 lines); Lem 4.22 (p46); Lem 4.23 (p46); Lem 4.25 (p46, 2 lines); Lem 4.26 (p47, 3 lines); Lem 4.27 (p47, 3 lines); Thm 4.28 (p47, 3 lines); Lem 4.30 (p48); Lem 4.31 (p48); Thm 4.32 (p48, 2 lines); Thm 4.33 (p48, 2 lines); Lem 4.39 (p50)
- `pc` (13 statements, 37 lines): Def 5.1 (p53, 2 lines); Lem 5.2 (p54, 3 lines); Lem 5.3 (p54, 3 lines); Lem 5.5 (p55, 6 lines); Def 5.6 (p55, 6 lines); Lem 5.8 (p56, 2 lines); Lem 5.10 (p56, 6 lines); Prop 5.17 (p58); Thm 5.19 (p59); Thm 5.22 (p59); Thm 5.23 (p60, 2 lines); Prop 5.24 (p60); Thm 5.30 (p62-63, 3 lines)
- `ec` (12 statements, 14 lines): Def 6.1 (p65, 2 lines); Thm 6.4 (p66); Thm 6.7 (p67); Lem 6.11 (p68); Prop 6.19 (p69); Def 6.21 (p70); Lem 6.27 (p71); Thm 6.28 (p71); Lem 6.31 (p72); Lem 6.32 (p72, 2 lines); Thm 6.35 (p73); Prop 6.36 (p73)
- `sr` (20 statements, 47 lines): Def 7.1 (p77); Def 7.3 (p77); Def 7.4 (p77, 2 lines); Lem 7.5 (p77, 10 lines); Def 7.6 (p78, 3 lines); Def 7.7 (p78, 6 lines); Lem 7.9 (p80); Def 7.13 (p80); Lem 7.14 (p80, 4 lines); Lem 7.16 (p81); Lem 7.17 (p81, 7 lines); Lem 7.18 (p82); Lem 7.19 (p82); Lem 7.20 (p82); Thm 7.21 (p83); Cor 7.24 (p84, 2 lines); Lem 7.30 (p85); Lem 7.32 (p85); Lem 7.33 (p86); Lem 7.38 (p87)
- `ar` (20 statements, 50 lines): Def 8.1 (p92); Lem 8.2 (p92, 2 lines); Lem 8.3 (p92, 2 lines); Def 8.4 (p92, 3 lines); Lem 8.5 (p92, 2 lines); Def 8.6 (p92, 4 lines); Lem 8.8 (p93, 2 lines); Def 8.10 (p93); Lem 8.11 (p93, 2 lines); Lem 8.12 (p93, 3 lines); Lem 8.15 (p94); Lem 8.17 (p94); Lem 8.18 (p95); Lem 8.19 (p95, 2 lines); Lem 8.20 (p95, 3 lines); Lem 8.21 (p95, 2 lines); Lem 8.22 (p96); Thm 8.25 (p97, 2 lines); Cor 8.27 (p98, 6 lines); Thm 8.28 (p98, 9 lines)
- `mm` (15 statements, 46 lines): Def 9.1 (p102); Lem 9.2 (p102, 6 lines); Def 9.3 (p102, 2 lines); Lem 9.5 (p103, 6 lines); Lem 9.6 (p103, 2 lines); Thm 9.10 (p105); Lem 9.12 (p106, 2 lines); Prop 9.13 (p106, 9 lines); Thm 9.17 (p108); Thm 9.18 (p108); Def 9.20 (p109, 4 lines); Lem 9.22 (p110, 4 lines); Thm 9.23 (p110, 2 lines); Lem 9.24 (p111, 2 lines); Thm 9.25 (p111, 3 lines)
- `cb` (1 statement, 1 line): Fact 11.68 (p137)
- `lg`, `mb`, `sa`: none.
