# Re-check of the front matter after the whole-document review, round 1

Inputs:
- `reviews/docfix-front-r1-fix.md` (the fixer's log);
- `snapshots/docfix-r1-pre/{proofs.tex, preamble.tex, bibliography.tex, make_appendix.py}` (before) and the current
  `proofs.tex`, `preamble.tex`, `bibliography.tex`, `tools/make_appendix.py` (after);
- the current section files and maps (read for every claim that the front matter makes about them);
- the records and Lean sources of the repository at 7e32ee259: `WRITEUP/P1/p1.tex` (bibliography),
  `WRITEUP/SYMMETRIC.md` §3, `LRATCHECK20261105/README.md`, the READMEs of `H`, `H2`, `H3`, `V1-L`, `V2-L`, `V2-L2`,
  `ENCBLEAN`, `C3L`, `ES8SLACK`, the Lean files of `AUDIT2`, `ENCBLEAN/geo/ES8Geo/Main.lean:91`,
  `ENCBLEAN/EncB/Cover.lean:110`, `H3/MirrorEncoding/Line.lean:94`, `V2-L/V2L/FinalTree.lean:28`,
  `MIRRORETV/lean/FarFlat.lean`, and `experiments/omission-compact-checker-2026-11-05/README.md`.

Paths are relative to STAGE (front files, sections, build, reviews), to RES (records), or to the repository root
(`ErdosSzekeres/`, `docs/`, `experiments/`). No git command, no Lean tool and no SAT tool was run.
`tools/make_appendix.py` was not run. To judge the generator, I used the fixer's scratch output
`build/front-r1/regen-live2/appendix_map.tex`. I first checked with `cmp` that it was made by a generator
byte-identical to the current `tools/make_appendix.py` (the copy in `build/front-r1/regen-live2/tools/`), from
section files and maps byte-identical to the current `sections/*` (all 24 files). The generator is deterministic,
so this file is exactly what the builder will get. I compiled it in a scratch copy, `build/recheck-front-r1/regen/`.

**Verdict: pass.** The fixer addressed 24 findings: 23 fixed, 1 declined (23).
- All 23 fixes are correct.
- The decline is right.
- The new text and code introduce no blocker or major problem.

The six major findings (3, 4, 5, 12, 13, 15) are resolved:
- 3, 4 and 5 in the front files.
- 12 and 15 in the preamble.
- 13 in the generator.

Six minor points remain (N1–N6 in section 4):
- two small inaccuracies in the new scope text (N1, N2);
- a reminder that `appendix_map.tex` must be regenerated (N3);
- three residuals that belong to section files or are cosmetic (N4–N6).

## 1. The 24 findings

| # | finding | fixer | re-check | evidence |
|---|---|---|---|---|
| 1 | consistency, minor: Dum25 missing; name form | fixed | **resolved** | `bibliography.tex:13` is identical to P1 (`WRITEUP/P1/p1.tex:1252`). sr now writes "B.~Dumitru" (`sections/sr.tex:286`). No "B. C. Dumitru" is left in any section. |
| 2 | consistency, minor: abstract omits the cited theorems | fixed (with 3) | **resolved** | The abstract (`proofs.tex:18-20`) names Baek's theorem and the cups–caps theorem as cited and not reproved. This agrees with fd's Purpose (`fd.tex:13-15`), with mb (`mb.tex:9-10, 108-109`; Theorems mb:thm:baek = 10.4 and mb:thm:capcup = 10.6, both `theorem` environments marked "cited") and with sa (`sa.tex:117-118`). I found no other published theorem that is cited and not proved. The textbook facts cited from Rudin and Rockafellar are standard facts, which the contract allows. |
| 3 | claims, **major**: abstract overclaims completeness | fixed | **resolved** | See the text after this table. |
| 4 | claims, **major**: "Stage 1" undefined; scope | fixed | **resolved** | See the text after this table. |
| 5 | claims, **major**: cited works missing from the bibliography | fixed | **resolved** | `Dum25`, `Sch26`, `CakeLPR` and `DT` are added. Each is character-identical to its P1 entry (`p1.tex:1249-1252, 1285-1286, 1315-1317`). The archive is now identifiable: title, version, date and DOI are in [9], and the scope section says that six of the bridge files of Section 10 are adapted from it. That claim agrees with `mb.tex:45-55`, which names Realization.lean as the project's own code and lists six files adapted from the archive. Residual: the in-text pointer at `mb.tex:47` was forwarded to the mb fixer and is still unchanged (N6, minor). |
| 6 | claims, minor: appendix intro does not fit the rows | fixed in the generator | **resolved (pending regeneration)** | The regenerated intro uses fd's path sentence (`docs/`, `experiments/`, `scripts/` are root-relative; `docs/SAT.md` exists only at the root). It explains the Lean column for remarks. It also states the three tags. In the regenerated appendix: 39 rows "written step" (none of them a remark); 3 rows "Mathlib" (fd:def:conv, oc:fact:sign, oc:def:keys, whose heads cite Mathlib); 61 remark rows with a dash, one of them with its file (sa:rem:control, `AssembledSizes.lean:30`). No remark head carries a `\leanref` (checked), so "a remark does not restate a Lean statement" is true. |
| 7 | claims, minor: undefined-label guard omits sa | fixed | **resolved** | `LABEL_KEY = re.compile(r'^(%s):' % '|'.join(KEYS))` (`make_appendix.py:29`). It is applied to every token that `LABEL_TOK` matches and whose label is not defined (`:277-279`). A label token cannot be absorbed into a math run (`:283`). |
| 8 | claims, minor: overfull token `m8_fix_build.log:29,35,` | fixed | **resolved** | `IDENT` accepts `(?:,\d+)*` (`make_appendix.py:26`). Regenerated row pc:rem:word-scope: `\texttt{ENCBLEAN/\allowbreak{}logs/...log:29,35}`. In the current (stale) appendix, `\esmapbreaks` (`preamble.tex:74`, used in a group at `proofs.tex:113-115`) makes `\_` in roman text breakable. The row now breaks at "m8_fix_ / build.log:29,35," (p171 of my build, rendered). Overfull boxes: 0 in both builds. |
| 9 | claims, minor: SMQH25 incomplete; header; no `\cite` | fixed | **resolved** | SMQH25 is identical to `p1.tex:1292-1295`. The header comment is true: Roc70 and Rud76 are not in P1 (checked). All 11 entries are cited from the scope section (11 `\bibcite` lines in `build/recheck-front-r1/proofs.aux`, no undefined citation). |
| 10 | claims, minor: empty PDF title | fixed | **resolved** | `pdfinfo`: Title "Written proofs of Lean-checked results, Stage 1: symmetric point sets". The document has no author line, so leaving the author empty is right. |
| 11 | completeness, minor: scope never stated | fixed (with 4) | **resolved** | See finding 4. |
| 12 | typesetting, **major**: heads cannot break inside Lean names | fixed | **resolved** | See the text after this table. Residual: N4, minor. |
| 13 | typesetting, **major**: raw labels with part suffixes | fixed in the generator | **resolved (pending regeneration)** | The regenerated notes read "Lemma~\ref{fd:lem:orient}(d)", "Theorem~\ref{ec:thm:compat}(a)", "Theorem~\ref{mb:thm:nine}(a)" (twice) and "Theorem~\ref{mb:thm:refl32}(b)". No raw label string is left in the regenerated appendix: none outside `\ref`/`\label` (script check). The official build still uses the 20:03 file, which shows all five (N3). |
| 14 | typesetting, **major**: overfull row on p167 | fixed | **resolved** | Same as 8. |
| 15 | typesetting, **major**: subsection heading stranded at a page foot | fixed | **resolved** | See the text after this table. |
| 16 | typesetting, minor: doubled names | fixed in the generator | **resolved (pending regeneration)** | The regenerated notes read "(Remark~\ref{oc:rem:parity})", "Lean encoding of Definition~\ref{mb:def:config}", "… of Lemma~\ref{mb:lem:boundary}" and "how Lean proves Lemma~\ref{mb:lem:polygons}". There are 0 doubled names in the regenerated appendix; the current file has 4. |
| 17 | typesetting, minor: "export label" residue; empty `; ;` items | fixed in the generator | **resolved (pending regeneration)** | The regenerated appendix has 0 occurrences of "export label" (the current file has 4) and no `; ;`. Two examples: "with \texttt{config\_capacity113} as part (a); (a) uses …" and "(Lemma~\ref{oc:lem:perm})". |
| 18 | typesetting, minor: ASCII notation in notes | fixed in the generator | **resolved (pending regeneration)** | I read all 60 converted notes against their map notes (extracted to `build/recheck-front-r1/math_notes.txt`). Every conversion is faithful, for example $x\ne\rho x$, $\rho^{m/2}$, $\alpha+2\pi-\delta\ne\pi$, $\exp(2\pi i/m)$ and $4\le\operatorname{card}s$. No `<=`, `!=`, `->`, `=>`, `^` or Greek letter name is left outside math and typewriter type. The only literal `*` is the glob `reflection_facts_*`. `omega` (the Lean tactic) and Greek fragments inside Lean names are untouched. Cosmetic residue: N5, minor. |
| 19 | typesetting, minor: names and files misaligned; camel-case splits | fixed in the generator | **resolved (pending regeneration)** | The table now has 3 columns, and each declaration is followed by its file on an indented line (rendered pp. 157 and 165 of the scratch build). All 470 regenerated rows agree with the current maps in label, kind, Lean names and files, in order (script check: 0 mismatches, no fallback cell). `tt_break` no longer breaks at camel humps. |
| 20 | typesetting, minor: `\paragraph` style; `\textbf` in ar | fixed | **resolved** | `\paragraph` is bold and run in (`preamble.tex:40-41`). No section has `\paragraph{\textbf`, and `proofs.toc` contains no `\textbf`. |
| 21 | typesetting, minor: empty PDF metadata | fixed | **resolved** | Same as 10. |
| 22 | typesetting, minor: numbered entries never cited | fixed | **resolved** | All 11 entries are cited ([1]–[11] on pp. 3–4). |
| 23 | typesetting, minor: capitalisation of short names in heads | declined, forwarded | **decline right** | The heads are in fd, sr and cb. This fixer may not edit section files, and the reviewer marked the change as optional. |
| 24 | build, minor: overfull box | fixed | **resolved** | Same as 8. |

**Findings 3 and 2 (abstract).** The abstract (`proofs.tex:13-26`) now says:
- each section gives a written proof that can be checked without Lean "with two exceptions";
- the two exceptions are the two cited published theorems, and computer-assisted statements, which are "reduced to a
  finite computation that is stated precisely and carried out by a machine; it is not carried out by hand, except
  where a section gives a proof by hand as well";
- a theorem with unproved hypotheses "is established here only as that conditional statement".

This matches fd's Purpose (`fd.tex:3-18`; "There are two exceptions") and its rigor labels. That includes the second
kind of computer-assisted statement (`fd.tex:88-91`) and the qualified label "computer-assisted in Lean"
(`fd.tex:94-98`). It covers the statements that the reviewer named with no hand proof: cb:fact:batches, cb:fact:c2-sub
and cb:thm:c2. No rigor label is rounded up. "Verified" occurs only inside the two CakeLPR paper titles in the
References, which the fixer flagged. "Certified" and "proved" (other than "reproved" / "unproved") do not occur.

**Findings 4 and 11 (scope).** The new unnumbered section "Scope of Stage 1" (`proofs.tex:31-97`) appears in the
contents and as the first bookmark. The title now reads "Written proofs of Lean-checked results, Stage 1: symmetric
point sets". I checked every claim against the maps and records:
- **Treated units.** The listed units are exactly those that the 12 maps cite.
  - LAYERLEAN is cited in ll and lg, and also in fd, oc and pc; the text says "mainly".
  - The LEANEXT subdirectories orbit, merged and keys are cited in oc, phase, linked and capstone in pc, and es7corr in
    ec.
  - ES8SYM and PRIMEFOLD are cited in ec, SYMLEAN in sr, ar and mb, MIRRORETV/lean in mm and mb, C3LEAN and C2FINAL in
    cb, and AUDIT3/A1_reduction and ES7SPLIT/review/equivalence in sa.
- **Records with Lean files.** I listed every RES directory that contains Lean files: AUDIT2, AUDIT3, C2FINAL, C3L,
  C3LEAN, ENCBLEAN, ES7SPLIT, ES8SLACK, ES8SYM, H, H2, H3, LAYERLEAN, LEANEXT, MIRRORETV, PRIMEFOLD, SYMLEAN, V1-L,
  V2-L and V2-L2. Each of them is named in the scope section.
- **Files not restated.**
  - No map row cites a file under LEANEXT/review, SYMLEAN/review or MIRRORETV/review. The only map row in a review
    directory is sa:thm:baek-seven in ES7SPLIT/review/equivalence, which is a treated unit.
  - The C3LEAN review and control files and `tools/prelude.lean` fall under "verbatim copies, tests and controls"
    (`cb.tex:1470-1483`).
  - `FarFlat.lean` holds estimates for the far-flat lower-bound construction of Theorem B (its header;
    `mm.tex:1025-1029`).
- **C3L and AUDIT2.** Both have 0 theorem lines.
  - C3L is the CNF generator; its README says "There are no theorems yet".
  - The five AUDIT2 files contain only `#check`, `#print`, `#print axioms` and `#eval` commands, plus the dump program
    with `cube` and `main`.
- **Later stages.**
  - `EncB.Geo.sixfold66_of_cubes64 (h : EncB.CubesUnsat64) : Sixfold66` is at `ENCBLEAN/geo/ES8Geo/Main.lean:91`.
    `CubesUnsat64` is `∀ c ∈ cubes64, ¬DimacsSatisfiable (cubeCnf (encB 6 8 11) c)` (`EncB/Cover.lean:110`). The geo
    copy of `Sixfold66` is at `ES8Geo/Capstone2.lean:1110`. So "derives its copy of Sixfold66 … from the
    unsatisfiability of 64 cube formulas" is exact, and it agrees with ll:rem:hyp.
  - H formalises `gen_etv.py` and `gen_cnf.py` including `--hull --mirror`, with soundness. H2 has the D3 encoding.
  - `Mir.MirrorExclusionLine` is a `def … : Prop` at `H3/MirrorEncoding/Line.lean:94`.
    `V2L.mirrorExclusionLine_final` (`FinalTree.lean:28`) has the hypotheses h1, hroot, hup and hleaves. Remark
    sr:rem:mirror-line identifies all of them as CNF-unsatisfiability facts. V1-L is sub-case (i) and V2-L2 is the
    `_v3` restatement.
  - The compact checker's README records `forces_convex_octagon_311 : ForcesConvexNGon 311 8` with the three standard
    axioms, "a second complete Lean check of ES(8) ≤ 311".
  - `ES8SLACK/proofs.md` holds the written proofs (P1–P4), as `ec.tex:916-920` also says.
- **Evidence outside Lean.** This paragraph is anchored on cake_lpr. "lrat-check … is a secondary check, whose
  verdicts are not counted" is the wording of `WRITEUP/SYMMETRIC.md` §3 (revised 6 November). The DT entry matches
  `LRATCHECK20261105/README.md`.
- **Works cited.**
  - The priority claims agree with sr:rem:records: Dumitru's computation "has priority" (`sr.tex:286-287`), and the
    Fourfold32 statement "is due to" Subercaseaux, Mackey, Qian and Heule (`sr.tex:299-300`).
  - Theorems 10.4 and 10.6 are the two cited theorems.

Two small inaccuracies remain (N1, N2). The scope section's `\ref`s to non-export labels (ll:rem:hyp, sr:rem:records,
sr:rem:mirror-line, mb:thm:capcup, the `:sec` labels) all resolve in the whole document. The standalone rule concerns
sections only.

**Finding 12 (heads).** I checked the new `\lean`/`\dirn` (`preamble.tex:59-72`) as a macro:
- **Characters.** `\detokenize` gives catcode-12 characters. `\if` compares character codes, so `\if_#1` works although
  `_` has catcode 8 in the preamble.
- **Break points.** A penalty is inserted before the next character after `. / _` (0) and `:` (100), never after the
  last character. These are explicit penalties, so they survive amsthm's head box, which math-mode breaks do not.
- **Other behaviour.** `\kern0pt` blocks ligatures. Spaces are dropped as before. Math mode goes through `\text`. The
  commands are robust, which matters for the one moving argument, the `\dirn{MIRRORETV}` inside `\texorpdfstring` in
  the title of mm.
- **Arguments.** All 7,578 `\lean`/`\dirn`/`\leanref` arguments in the sections, the front files and both appendices
  use only `[A-Za-z0-9._/:'-]` (script check). Names with a prime render with the same glyph as before (compared with
  `build/doc-r1`).
- **Effect.** Badness-10000 hbox lines go from 351 (`build/doc-r1`) to 76 in my build. No overfull box, no font
  warning.
- **Pages named in the finding.** The heads of Lemmas 4.10 (p45) and 7.5 and Theorem 8.28 (p100), rendered, now break
  inside the names.
- **Residual.** About 10 heads with many `\leanref`s still have 3–6 loose lines (N4).

**Finding 15 (stranded headings).** The patch has three parts:
- `\@trivlist` sets `\@beginparpenalty=\@M` while a run-in heading is pending.
- Until the next `para/begin`, `\@esphack` adds `\nobreak` after a vertical-mode `\write`, so the `\label` whatsit after
  `\begin{lemma}[…]` no longer creates a break point.
- `\paragraph` directly after a run-in heading adds `\nobreak` and skips `\@secpenalty`.

I checked it against the kernel in use (TeX Live 2026, `latex.ltx` `\@trivlist` and `\@esphack`) and amsart 2020/05/29.
- The flag is set after the heading paragraph has been ended by the original `\@trivlist`, and it is reset globally
  only by `para/begin`, so no save-stack buildup.
- In my build, no page from 4 to 156 has a line "N.M. Title." among its last two lines (pdftotext scan).
- Subsection 9.1 starts on p104 together with its definition.
- The underfull vbox count is 14, against 16 with the old front files (`build/front-r1/base`). The flagged pages (e.g.
  pp. 102 and 115, rendered) are ordinary section ends.

## 2. Diff of the front files, hunk by hunk

- **`proofs.tex`.**
  - `\hypersetup{pdftitle}` comes after the preamble, which loads hyperref.
  - `\title[running head]{… results,\\ Stage~1 …}` renders on two lines, with the full title in the running head.
  - The new abstract and the scope section are checked above. All `\ref`s resolve.
  - `\phantomsection\section*` gives the contents line and the bookmark.
  - `\begingroup\esmapbreaks … \endgroup` confines the `\_` change to the appendix. The bibliography (`cake\_lpr` in
    CakeLPR) is outside the group.
  - No machine path and no tool name (grep).
- **`preamble.tex`.**
  - The `\@trivlist`/`\@esphack`/`para/begin` patch and the bold run-in `\paragraph` are checked under 15 and 20.
  - `\lean`/`\dirn` are checked under 12.
  - `\esmapbreaks` is defined inside `\makeatletter` (lines 59–75), so `\nfss@text` is read correctly. In math mode it
    keeps the kernel's behaviour.
  - No new package.
- **`bibliography.tex`.** Four new entries and the full SMQH25, each identical to P1. The order (Baek, de Moura,
  drat-trim, Dumitru, Erdős, mathlib, Rockafellar, Rudin, Schroeder, Subercaseaux, Tan) is alphabetical.
  `thebibliography{99}` gives the right label width for [11].
- **`tools/make_appendix.py`.**
  - `clean_note`: the three regexes and the empty-item filter give the outputs quoted under 17.
  - `label_ref`/`note_tex`: joining to a preceding name word, plural lists, part suffixes, and stopping on an
    undefined label of any key.
  - `lex_math`/`math_of`/`strength`/`split_punct`/`join_math`: the outputs were checked note by note (18).
  - `lean_cell`: tags, hanging indentation, and the fallback for unequal counts, which no row uses.
  - The new check that every map label is defined in its section.
  - Three-column longtable.
  - The new guards (labels defined, ASCII-only maps) make the builder's run stop on a bad map instead of printing it,
    which is the intended behaviour.

## 3. Compile

- **Official build.** `build/recheck-front-r1`, at 21:17, from the live sections and the existing `appendix_map.tex`.
  Three passes of `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build/recheck-front-r1
  proofs.tex`.
  - Exit 0 on every pass.
  - 0 errors, 0 lines with "Warning", 0 undefined references or citations, 0 overfull boxes, 0 missing characters.
  - 188 underfull hbox (76 with badness 10000) and 14 underfull vbox.
  - 191 pages. `pdfinfo` gives the title.
  - Identical counts and `.aux` to the fixer's `build/front-r1` build.
- **Scratch build with the regenerated appendix.** `build/recheck-front-r1/regen`, same three passes.
  - Exit 0, 0 errors, 0 warnings, 0 overfull boxes. No underfull box inside the appendix. 187 pages.
  - Rendered pp. 157, 158, 165 and 187.

## 4. Remaining points (all minor)

- **N1** (`proofs.tex:91`). "The sections cite published works inline, by author and title". This is not true of
  every work: sr cites Dumitru and Subercaseaux–Mackey–Qian–Heule by author and arXiv number (`sr.tex:286, 299-300`),
  mb names Schroeder's archive by author only (`mb.tex:47`), and Lean 4 and Mathlib are named without authors. Suggested
  wording: "by author and title or arXiv number".
- **N2** (`proofs.tex:39-42`). The main-library restatements are attributed to Sections 1 and 10 only. Two other
  sections also restate main-library declarations:
  - Section 9: mm:def:config restates `ErdosSzekeres.Omission.Configuration` and `Configuration.HasCap` from the bridge
    file `ErdosSzekeres/Omission/Realization.lean`, and mm lists that file with its hash (`mm.tex:36-40`).
  - Section 7: sr:lem:supports restates `ErdosSzekeres.Suk.convexPosition_of_strict_supports`, the same declaration as
    fd's.

  The categories are right; only the section pointers are incomplete. Suggested wording: "mainly in Section 1 and
  Section 10 (also restated in Sections 7 and 9)".
- **N3** (builder; `appendix_map.tex`). The official appendix is still the file generated at 20:03 by the old
  generator. It still shows the defects of findings 6, 13, 16, 17, 18 and 19: five raw labels, four doubled names,
  four "export label" residues, ASCII notation and the four-column layout. Before the final build, regenerate it with
  the current `tools/make_appendix.py`. That output is the one verified above (470 rows, clean build).
- **N4** (sections sr, pc, ar, ll, oc; residual of 12). 76 badness-10000 lines remain: sr 26, pc 19, ar 13, ll 8,
  oc 6, mm 2, ec 1, mb 1. Most are in about 10 heads that cite many declarations, each with 3–6 loose lines. Examples
  are Definition 5.6 (p58) and Lemma 7.17 (p83), and the first head line of Theorem 8.28 (p100). The preamble cannot
  do more without breaking inside identifiers. The fix is in the section files: one `\leanref` per line (`\\`), as mb
  and sa do.
- **N5** (generator; residual of 18). In two notes, a list or clause comma ends up inside the math:
  - fd:lem:rot: "linear part $R_{\theta},\rho(p+v)=\rho(p)+R_{\theta}v$";
  - mb:thm:nine: "$(a=3,b=6),C(8,2)=28$".

  In addition, fd:rem:affine-orient-lean prints the ASCII coordinates as $(p0,p1)$ rather than $(p_0,p_1)$, and
  pc:thm:word prints "Fin $6\to$ Bool". All are readable and faithful, so they are cosmetic. To fix them, end a math
  run at a comma that is followed by a new clause, or reword the two map notes.
- **N6** (mb; residual of 5). `mb.tex:47` still names "M. Schroeder's archive" without a pointer to [9]. The fixer
  forwarded this to the mb fixer as optional. The archive is now identified in the References and in the scope
  section.
