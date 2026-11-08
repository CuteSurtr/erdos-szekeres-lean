# Diff audit of section `cb`, round doc-r1

Compared with `diff -u`: `snapshots/doc-r1-pre/cb.tex` and `cb.map.tsv` against `sections/cb.tex` (1,486 lines) and
`sections/cb.map.tsv` (100 rows). Fix log: `reviews/cb-doc-r1-fix.md`. Its input is m1 of `reviews/cb-doc-r0-audit.md`.
The earlier notes are m1 of `reviews/cb-p1-diff.md` and F1-F3 of `reviews/cb-p1-referee.md`, all fixed in round
doc-r0. Paths are relative to the staging area or to RES (`cloud/es7-2026-10-19/results`).

**Verdict: PASS.** No blocker, no major, one minor finding (m1, a wording point; §4).
- Both diffs are empty, so this round has no hunk to check.
- The fixer resolved doc-r0 m1 by checking, without an edit. That is correct: I repeated all three checks on the
  current `sections/sa.tex`, which changed after the fixer's last check, and all pass.
- The four earlier fixes are still in place and still correct.
- My wrapper compiles with exit 0, no error and no overfull box.

## 1. The diff

- Running `diff -u` on `cb.tex` and on `cb.map.tsv` gives empty output (exit 0) for both. The SHA-256 of `cb.tex` is
  `d64b2f190c3b…` and that of `cb.map.tsv` is `a2ccffe2e859…`, the same in the snapshot and in `sections/`.
- So no hunk exists, and nothing changed: statement environments, labels, Lean references, map rows and rigor
  wording are all as audited in round doc-r0. No statement was touched, so no Lean declaration had to be re-read for
  fidelity. I re-read the Lean sources behind the passages that the notes concern (§2, §3).
- For context, `snapshots/doc-r0-pre` → `snapshots/doc-r1-pre` has exactly the four hunks of round doc-r0, and the map
  is unchanged there too. The four hunks are:
  - the Sources paragraph;
  - the Rigor paragraph;
  - the paragraph after Fact `cb:fact:batches`, with Remark `cb:rem:use`;
  - the Coverage paragraph "Treated in another section".

## 2. The note of this round (doc-r0 m1): checked, no edit; agreed

The note asked for three checks once `sections/sa.tex` existed. If `baek_seven` were not treated there, the sentence
"they are treated in Section~\ref{sa:sec}" (`cb.tex:1482-1486`) would need rewording.

The writer of `sa` kept editing after the fixer's last check. The fixer checked the saves of 19:05 and 19:07. I
checked the save of 19:10: SHA-256 `47abd30e2bbf…`, 43,405 bytes, 567 lines. The file did not change during my checks
and builds.

**(i) The label.** Line 1 is
`\section{Size arithmetic of the symmetric \texorpdfstring{$k=7$}{k=7} reduction}\label{sa:sec}`. The label
`sa:sec` is defined once in `sa.tex` and in no other section.

**(ii) Coverage.**
- *Script check.* A script listed every declaration of the three Lean files and matched it against the
  `\leanref{name}{file:line}` heads of `sa.tex`:
  - `AUDIT3/A1_reduction/SizeArith.lean`: 20 theorems (namespace `A1`, lines 16-79);
  - `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean`: 7 theorems (lines 6-24);
  - `ES7SPLIT/review/equivalence/BaekSeven.lean`: `baek_seven` (line 6).

  All 28 match by name and by line. `sa.tex` has 28 `\leanref`s and no other.
- *The example.* The anonymous `example` (`AssembledSizes.lean:30`) is Remark `sa:rem:control` (`sa.tex:312`).
- *`baek_seven`.* Theorem `sa:thm:baek-seven` (`sa.tex:341-348`) states it exactly as Lean does
  (`BaekSeven.lean:6-7`):
  - hypotheses: `{γ : Type}` with `[LinearOrder γ]`, `C : Config γ`, `S : Finset γ` and `17 ≤ S.card`;
  - conclusion: `C.HasNCap 4 S ∨ C.HasNGon 7 S`.

  Its written proof is the case n = 4 of the cited Theorem `mb:thm:baek`, with C(6,2)+2 = 17. This is also the Lean
  proof, `main 4 C S (e ▸ h)`.
- *sa's own Coverage.* The Coverage paragraph of `sa` (`sa.tex:544-567`) lists all 28 theorems and the example, by
  label.

**(iii) Resolution in the document.**
- *`build/cb_docr1audit_withsa.tex`* (preamble, `cb`, `sa`): two passes, both exit 0. `sa:sec` is written to the aux
  file as section 2, and no warning names `sa:sec`. The other undefined references are labels of sections outside
  this partial build.
- *`build/cb_docr1audit_full.tex`*: a copy of `proofs.tex` with `../` paths. It has the abstract, all twelve sections
  in document order, the placeholder `appendix_map.tex` and `bibliography.tex`.
  - Three passes, all exit 0; 152 pages.
  - No `!` error, no undefined reference of any kind, no multiply defined label, no rerun request and no overfull box.
  - `sa:sec` is Section 12, page 145, and `cb:sec` is Section 11. On page 145 the paragraph renders "… they are
    treated in Section 12."

**The descriptions in the paragraph.** I re-read the three Lean files and their logs:
- *`SizeArith.lean`.* Line 2 reads "the size arithmetic of the symmetric ES(7) reduction". Lines 13-56 are the
  reduction (11 theorems). Lines 58-80 are "Upper bounds of the table, given the case theorems" (9 theorems). The log
  `SizeArith.lean.log` has 20 axiom lines, all within {propext, Classical.choice, Quot.sound}.
- *`AssembledSizes.lean`.* Line 1 reads "Size bookkeeping for the assembled symmetric theorem". The log
  `AssembledSizes.lean.log` has the unused-variable warning for `hp` at 24:41, 7 axiom lines within the same set,
  and no error.
- *`BaekSeven.out`.* It has the `#check @main` output (lines 1-2) and the axioms of `baek_seven`: propext,
  Classical.choice, Quot.sound.

So "Lean-checked", "the size arithmetic of the reduction … to its case classes" and "an instance of Baek's theorem for
abstract configurations" are accurate. The word "theorem" in that phrase is the subject of m1.

**The fixer's other claims hold.**
- *Its builds.* `build/cb_docr1_full.log`: 152 pages, 0 errors, 0 overfull boxes, 0 undefined references, no
  multiply defined label and no rerun request; `sa:sec` is Section 12, page 145. `build/cb_docr1_withsa.log`: `sa:sec`
  is section 2, and no warning names it.
- *Its statements about the Lean sources.* All are correct (re-read above).
- *Its account of sa's statement groups.* Correct: `sa:prop:rot` 5, `sa:prop:mirror` 2, `sa:prop:order` 3,
  `sa:lem:split` 1, `sa:prop:table` 9, `sa:prop:assembled` 6, `sa:lem:big-order` 1, `sa:thm:baek-seven` 1.
- *Not checkable here.* The writer's brief for `sa` is not in the staging area. This does not matter, because the
  coverage itself was checked on the file.

## 3. The earlier notes (fixed in round doc-r0; text unchanged since)

| note | status | my re-check |
|---|---|---|
| p1-diff m1 (`all_checked` missing from the Sources inventory) | fixed | `cb.tex:52-56` names `all_checked` (line 2247). I re-read `C3LEAN/C3Cover.lean` (2,327 lines, SHA-256 `4b64293df2ea…`). Every range is exact: `beqLayer` … end of `reflectionFacts` 335-365; facts about the roots 367-409 (`reflection_facts_H3` … the `decide +kernel` of `strata`) and 1720-1733 (`roots_match` … `roots_eq_tsv`); data 413, 423-1717 (`certs0` … `bounds`) and 1737; `batch0` 1740 … `batch126` 2244-2245; `all_roots_covered` 2251; controls 2266-2297; `end C3Cover` 2299; `#print axioms` 2301-2327. |
| p1-referee F1 (Rigor paragraph overstated coverage) | fixed | By script: `C3Cover.lean` has 336 top-level declarations and `Central34Orbits.lean` has 20. Exactly seven have no head reference, directly or through a family head (`certs0`, `batch0`, `reflection_facts_H6_1_0`, `closedP1`): the seven controls at 2266, 2270, 2274, 2278, 2282, 2286 and 2292. With exact name matching, all 81 `\leanref` names are declarations, and each cited line contains its name. |
| p1-referee F2 (unsourced count 554) | fixed | My parser of `certs0` … `certs126` (lines 423-1711) gives 910 certificates. 554 of them have `ds` written as the numeral `0`, and each of those has exactly one key under `unpack` (base 2^64, stop at 0). The totals are 73,567 keys, 942 layer digits and 1,747 σ digits, so 76,256 nodes. A word search for 554 in the md, txt, json and tex records of `C3LEAN`, `C3FINAL`, `C3U2`, `C3H6M`, `C3-S`, `WRITEUP` and `AUDIT3` finds only unrelated hits ("1,554" in two `C3U2` tables, and two `AUDIT3/A4` data lines). So "no project record states it" stands. |
| p1-referee F3 (three files covered nowhere) | fixed; now fully | Fixed by the "Treated in another section" paragraph. Its pointer is now true (§2). |

No note was declined in either round.

## 4. Findings

**m1 (minor; wording, cross-section consistency; `cb.tex:1483-1484`).**
- *The issue.* The paragraph that points to Section `sa` describes the first two files as "the size arithmetic of
  the reduction of the symmetric $k=7$ \emph{theorem} to its case classes".
- *What `sa` says.* The section the reader is sent to uses "statement" for the same object, deliberately:
  - `sa.tex:4`: "the reduction of the symmetric $k=7$ statement to its case classes";
  - `sa.tex:10-12`: the audit "claims no theorem", quoting `AUDIT3/README.md`;
  - `sa.tex` Remark `sa:rem:use`(4): the classes `HalfTurn34`, `Threefold33` and `Fivefold35` "are not proved in Lean
    or in this document".
- *Why it is only minor.* In this document the composite claim holds only conditionally on those classes, and an
  unattributed "theorem" can be read as calling it established. The records do call it a theorem: Theorem A
  (computer-assisted), `WRITEUP/SYMMETRIC.md` §0; "the assembled theorem", `AUDIT3/reports/A1_reduction.md`. Also,
  "reduction … to its case classes" already signals the dependence. So this is a small imprecision with no effect on
  correctness, not an overclaim.
- *Status.* The fixer noticed this and left it for the consistency lens. Round doc-r0 accepted the wording before
  `sa` existed.
- *Suggested fix.* Replace "theorem" by "statement" in that parenthetical, matching `sa.tex:4`. Do not attribute it
  as "Theorem A": in this document "Theorem A" already names the mirror reduction of Section `mm` (`mm.tex:1, 599`).

There are no overfull boxes, so there are no box findings.

## 5. Compile check (own wrapper)

- `build/cb_docr1audit_wrapper.tex` is the contract's wrapper: `\documentclass[10pt]{amsart}`, `\input{../preamble}`,
  `\input{../sections/cb}`. I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` from `build/`.
- Passes 1 and 2 both exit 0. The PDF has 17 pages: no `!` error, no "Missing $", no multiply defined label and **no
  overfull box** of any size (so none above 1pt).
- Undefined references: `sr:def:classes` (input lines 11 and 21; an export label of `sr`) and `sa:sec` (line 1486;
  resolved in the full build, §2). Both are expected in the standalone check.
- Other warnings:
  - one underfull `\vbox` during output;
  - three underfull `\hbox` (badness 3364, 2671 and 4582) in the heads of Lemma 1.53 (`cb:lem:run`), Theorem 1.82
    (`cb:thm:c3`) and Fact 1.97 (`cb:fact:c2-sub`). These are the same as in rounds p1 and doc-r0.
- Pass 2, with a fresh aux file, printed "Label(s) may have changed". A third pass (exit 0) settles: no rerun
  warning, and still no error and no overfull box.
- Page 17, rendered and in `pdftotext`, shows the paragraph "Treated in another section". The `\dirn` path breaks
  cleanly after `AUDIT3/A1_`, and the reference reads "Section ??" in the standalone build, as expected.

Mechanical checks of `cb.tex` and `cb.map.tsv`:
- no machine path and no tool name;
- no `\newcommand`, `\def`, `\usepackage`, `\input` or `\sloppy`;
- 112 labels, all `cb:` and distinct; the export labels `cb:lem:run`, `cb:thm:c3` and `cb:thm:c2` are each defined
  once;
- the only references outside `cb:` are `sr:def:classes` and `sa:sec`;
- "verified" occurs 0 times, "certified" 15 times as a substring (3 as a whole word, each "counts as certified",
  attributed to the project) and "proved" 3 times, each in a negation. These counts are unchanged.

Map: 100 statement environments and 100 rows of 5 fields, matched by script. Label, kind, Lean names and file:line
all agree (0 mismatches), and no head tagged "written step" carries a Lean name.

## 6. Notes (not findings)

- *`sa:sec` and the contract.* `sa:sec` is not in the contract's export table, because `sa` is the section added in
  this run. The reference was added on the orchestrator's instruction in round doc-r0, and this round's instructions
  name `sa:` labels. It resolves in the full document. I treat it as allowed, as round doc-r0 did. It is the only
  reference in the document to another section's `:sec` label.
- *sa is still being edited.* The checks above hold for the save of `sa.tex` with SHA-256 `47abd30e2bbf…`. They should
  be repeated on the final `sa.tex`; the cross-reference and completeness lenses of the whole-document review are the
  natural place. The claim in `cb` depends only on `sa` defining `sa:sec` and treating the 28 theorems, the example and
  `baek_seven`.
- *"The size arithmetic of the reduction".* As round doc-r0 noted, this one-line description leaves out the second
  part of `SizeArith.lean`, the upper bounds of the size table. It also matches the title of Section `sa`, so it is
  acceptable as it stands.
