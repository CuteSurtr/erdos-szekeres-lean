# Section `sr` (Reduction of symmetric sets to case classes), whole-document review round 2: fix log

Input: the three findings of `reviews/docfix-sr-r1-recheck.md` (M1 major; m1 and m2 minor), assigned as findings 1-3.

Paths are relative to STAGE (`sections/`, `build/`, `reviews/`, `snapshots/`, `tools/`) or to RES (Lean sources and
records). `sr.tex:N` refers to the edited file.

Snapshot taken before editing: `snapshots/docfix-r2-pre/sr.tex` (SHA-256 `d25ae5f7389b`, 1166 lines) and
`snapshots/docfix-r2-pre/sr.map.tsv` (`557f6af190d7`); these are the post-r1 hashes named in the recheck. After
editing: `sections/sr.tex` (`899f5cba0a8d`, 1170 lines) and `sections/sr.map.tsv` (`104dc98dcd9f`). No label was
removed or renamed (the `\label` lists of snapshot and file are identical). No statement head or statement text
changed.

## Summary

| # | finding | severity | action | location (edited file) |
|---|---|---|---|---|
| 1 | recheck M1: three `\ref{fd:lem:strict-supports}`, a label outside the contract's foundations export list | major | fixed (option (a): prose pointer, as ll did for "Convex hulls") | sr.tex:78-80 (Dependencies), 643-644 (proof of `sr:lem:supports`), 1131-1132 (Coverage, item Geometry); map note of `sr:lem:supports` kept |
| 2 | recheck m1: the Fourfold32 bullet lists a written proof as "computer-assisted evidence" | minor | fixed (suggested text, made slightly more precise) | sr.tex:297-300 (`sr:rem:records`); map note of `sr:rem:records` |
| 3 | recheck m2: Coverage calls the converse bridge only "the converse bridge", not marked conditional | minor | fixed | sr.tex:1164-1169 (Coverage, not-covered sentence) |

3 findings, 3 fixed, 0 declined.

## 1 (fixed): no `\ref` to a non-export fd label

Source check.
- CONTRACT.md (read at the start of this run) still lists the foundations export labels without
  `fd:lem:strict-supports` and says "Nothing else". So option (b) has not happened, and a fixer cannot edit the
  contract. The finding is right under the contract as it stands.
- `fd.tex:1042` heads the lemma `[Strict supporting lines; ...]\label{fd:lem:strict-supports}`. It is the only fd head
  with that title, so "the lemma titled ``Strict supporting lines'' in the foundations section" identifies it
  uniquely. (sr's own lemma has the same title, which is why the section is named.)
- Lean re-read: `ErdosSzekeres/Suk/SupportingLines.lean:28` (file prefix `6a8e12677685`, as in the Sources paragraph),
  `convexPosition_of_strict_supports (s : Finset Point) (hs : ∀ p ∈ s, ∃ q : Point, ∀ r ∈ s, r ≠ p → 0 < orient p q r)
  : ConvexPosition s`. The statement of `sr:lem:supports` (sr.tex:637-640) matches it and is unchanged.

Action. The wording follows ll (ll.tex:63 and 87, "the lemma titled ``Convex hulls'' in the foundations section").
- Dependencies (sr.tex:78-80): "Lemma sr:lem:supports is the lemma titled ``Strict supporting lines'' in the
  foundations section (the same declaration of the main library), repeated here with its short proof."
- Proof of `sr:lem:supports` (sr.tex:643-644): "This is the lemma titled ``Strict supporting lines'' in the foundations
  section, the same declaration of the main library; the short proof is repeated here because Lemma sr:lem:concyclic
  uses it."
- Coverage (sr.tex:1131-1132): "This is the lemma titled ``Strict supporting lines'' in the foundations section; the
  short proof is repeated here."
- Map note of `sr:lem:supports`: kept ("same declaration as fd:lem:strict-supports (proof repeated)"), as the finding
  allows. The note becomes a `\ref` only in `appendix_map.tex`, which is generated at document level and already lists
  the label as its own row (`appendix_map.tex:54`). A dry run of `tools/make_appendix.py` on a copy
  (`build/srfix-r2/regen/`; 470 rows, exit 0) renders the row as before.

After the fix, a scan of all section files and maps (fd excluded) finds no `\ref` to an fd label outside the export
list in any section file. The only remaining mention of `fd:lem:strict-supports` outside fd is that map note.

## 2 (fixed): the Fourfold32 bullet

Source check (`C4CUT/README.md`, 117 lines).
- Line 5: "**Statement.** Every set of 32 points ...": the statement has no rigor label. (C2FINAL, by contrast, has
  "Statement (claimed; computer-assisted)".)
- Lines 13-16 do label the parts of the evidence: "certificate accepted by both checkers", "exact computation" and
  "Encoder soundness: written proof, refereed". So the suggested "which gives no rigor label" would be slightly too
  broad. The new text says that C4CUT *states it* without a rigor label, which is exact.
- Line 68: cake_lpr printed `s VERIFIED UNSAT` for the final proof. So "a final certificate accepted by both checkers"
  agrees with the remark's convention (sr.tex:257-258: where a certificate is said to be accepted by both checkers,
  cake_lpr accepted it).
- Lines 15 and 35-61, 79-82: each of the six cuts is justified by a certificate checked in exact rational arithmetic,
  and it is re-checked by `verify_cuts.py`. This supports "six cuts checked by exact computation".
- Lines 16-17: the certificate rests on the soundness of the layered encoder (its docstring argument and
  `SYM5/README.md` §2). This supports "a written proof of the encoder's soundness". The record's word "refereed" is not
  repeated: the document reserves its rigor terms for its own proofs.
- Other records: `WRITEUP/SYMMETRIC.md:166` and the proof of `prop:C` in `WRITEUP/note/symmetric_es7.tex` say
  "certified in C4CUT", and `prop:C` itself has no label. The text says nothing about those records, so it adopts
  neither "certified" nor a label.
- Lean re-read: `Fourfold32` (`SYMLEAN/SymmetricReduction.lean:496`, file prefix `6d5ec90a4215`). Its docstring says
  "only used by the variant `halfTurn_of_symmetric_counterexample`". The bullet's "used only by Theorem
  sr:thm:variant" is unchanged.

Action (sr.tex:297-300): "claimed in C4CUT, which states it without a rigor label. It rests on a final certificate
accepted by both checkers, on six cuts checked by exact computation and on a written proof of the encoder's soundness.
The statement is due to ..." The list no longer sits under "computer-assisted evidence".

Map: the note of `sr:rem:records` now ends "... with the rigor labels that the records claim (C4CUT states Fourfold32
without one)", in sync with the bullet.

## 3 (fixed): the converse bridge marked as conditional

Source check (`SYMLEAN/review/ReviewSanity.lean`, prefix `ec25136849a9`, re-read at lines 1585-1631).
- :1593 `theorem exclusionLine_of_mirrorOneAxis33 (h : MirrorOneAxis33) : MirrorExclusionLineCopy`: an implication with
  hypothesis `MirrorOneAxis33`.
- :1629 `theorem mirrorOneAxis33_iff_exclusionLine : MirrorOneAxis33 ↔ MirrorExclusionLineCopy`: no hypotheses; an
  equivalence that asserts neither side.

The finding is right: in the same sentence `VariantChecks.group_form` is marked conditional, and the Main results item
marks the forward bridge, but the converse was not marked.

Action (sr.tex:1164-1169). The wording is that of the Main results item (sr.tex:1146-1147):
"... and the converse bridge Review.exclusionLine_of_mirrorOneAxis33 (SYMLEAN/review/ReviewSanity.lean:1593, an
implication between two propositions, so conditional on its hypothesis MirrorOneAxis33) with the equivalence
Review.mirrorOneAxis33_iff_exclusionLine of the two propositions (line 1629 of the same file), which asserts neither of
them."
- The clause on the equivalence is added so that each result in the sentence has its status stated. The equivalence
  is unconditional, and it does not supply either class.
- The file and lines are unchanged (1593 and 1629, confirmed by grep).
- Remark `sr:rem:mirror-line` already calls the converse "the converse implication" and was not changed. The map note
  of that remark ("the converse and the equivalence ...") stays in sync.

## Checks

- Compile: `build/sr_wrapper.tex`, run twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode
  -halt-on-error`.
  - Both runs exit 0.
  - The log has 0 errors, 0 "Missing" messages, no multiply defined label and no rerun request.
  - Overfull boxes: 0 (0 above 1pt).
  - Undefined references, all foreign export labels:
    - fd: `def:{cp,gp,inv,ngon,orient,point,rot}` and `lem:{collinear,cp-hull,mono}`, all in the contract list;
    - `ar:thm:main`, `cb:thm:c2`, `cb:thm:c3`, `mb:thm:classes` and `mb:thm:main3`.

    `fd:lem:strict-supports` no longer appears.
- Underfull boxes: 48 underfull hboxes of badness 10000 before and after. The snapshot was compiled the same way
  (`build/sr_r2pre_wrapper.tex`). All are in statement heads with long Lean names, as before.
- Rendered pages: 2, 5, 9, 15 and 16 were checked as text, and pages 5 and 16 as images (`build/srfix-r2/p-05.png`,
  `p-16.png`). The new passages typeset cleanly.
- Hygiene (sr.tex and sr.map.tsv):
  - ASCII only;
  - no machine paths and no tool names;
  - no `\newcommand`, `\def` or `\usepackage`.
  - The 16 added lines contain none of "verified", "certified" or "proved".
- Map: 46 rows of 5 fields. Its labels are the statement labels of sr.tex, in the same order.

## Follow-up for the orchestrator

Regenerate `appendix_map.tex` with `python3 tools/make_appendix.py`, because the note of `sr:rem:records` changed. The
dry run on a copy succeeded.
