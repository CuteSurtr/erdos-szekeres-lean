# Fix log: section `cb`, round doc-r1

Input: `reviews/cb-doc-r0-audit.md` (diff audit of round doc-r0). It reports no blocker and no major finding, and one
minor finding (m1, its §4) on the Coverage paragraph "Treated in another section." (`cb.tex:1482-1486`). Snapshot
taken before editing: `snapshots/doc-r1-pre/cb.tex` and `cb.map.tsv`. Paths are relative to the staging area or to
RES (`cloud/es7-2026-10-19/results`).

**Result: the finding is resolved by the check it asks for; no edit was needed.** All three conditions of the
suggested fix hold, including the one that mattered (`baek_seven` is treated in Section `sa`). `cb.tex` and
`cb.map.tsv` are byte-identical to the snapshot.

| # | lens | finding (summary) | action | location | reason / evidence |
|---|---|---|---|---|---|
| 1 | diff (m1) | The paragraph says that `SizeArith.lean`, `AssembledSizes.lean` and `BaekSeven.lean` are treated in Section~`\ref{sa:sec}`, which could not be checked in round doc-r0 because `sections/sa.tex` did not exist. The risk was `BaekSeven.lean`: `baek_seven` is not size arithmetic, so the sentence would be a false coverage claim if `sa` did not treat it. Suggested fix: once `sa.tex` exists, check (i) it defines `\label{sa:sec}`; (ii) it covers the 20 theorems of `SizeArith.lean`, the 7 theorems and the control `example` of `AssembledSizes.lean`, and `baek_seven`; (iii) the full document resolves `sa:sec`. Reword the sentence for `BaekSeven.lean` only if it is treated elsewhere or not at all. | checked; no edit needed | `cb.tex:1482-1486` (unchanged) | All three checks pass (below). The rewording condition does not arise. The brief for the writer of `sa` in this run assigns it exactly these three files, `baek_seven` included, so the coverage is by design. |

## The three checks

The writer of `sa` was still finishing `sections/sa.tex` during this round. I waited until it existed, then ran
every check on the version saved at 19:05 (SHA-256 `e1beac4cd7fccf7c…`, 42,848 bytes). I repeated all of them, with
the same results, on the writer's next save at 19:07 (SHA-256 `72e6440a4661afba…`, 43,227 bytes), the current
version when this round ended. The cross-reference and completeness lenses of the whole-document review re-check
this once `sa` is final.

**(i) The label.** Line 1 of `sa.tex` is
`\section{Size arithmetic of the symmetric \texorpdfstring{$k=7$}{k=7} reduction}\label{sa:sec}`, and `sa:sec` is
defined exactly once.

**(ii) Coverage.**
- *Script check.* A script matched every `theorem` line of the three Lean files against the
  `\leanref{name}{file:line}` heads of `sa.tex`. All 28 match by name and line:
  - `SizeArith.lean`: 20 theorems (namespace `A1`, lines 16-79);
  - `AssembledSizes.lean`: 7 theorems (lines 6-24);
  - `BaekSeven.lean`: `baek_seven` (line 6).

  `sa.tex` has no other `\leanref`.
- *Statements.* The theorems are grouped as follows:
  - `sa:prop:rot` (5), `sa:prop:mirror` (2), `sa:prop:order` (3), `sa:lem:split` (1) and `sa:prop:table` (9);
  - `sa:prop:assembled` (6) and `sa:lem:big-order` (1);
  - `sa:thm:baek-seven` (1).

  The anonymous control `example` (`AssembledSizes.lean:30`) is Remark `sa:rem:control`.
- *`baek_seven`.* Theorem `sa:thm:baek-seven` states it: for a linearly ordered γ in `Type`, `C : Config γ`,
  `S : Finset γ` and `17 ≤ |S|`, the conclusion is HasNCap_C(4,S) or HasNGon_C(7,S). It is proved as the instance
  n = 4 of the cited Theorem `mb:thm:baek`, using C(6,2)+2 = 17. Remark `sa:rem:baek-seven` compares it with the
  `#check @main` output in `BaekSeven.out`.
- *sa's own Coverage.* The Coverage paragraph of `sa` lists all 28 theorems and the example as covered, by label.

**(iii) Resolution.** Two builds in `build/`, so that the staging root (where the Build phase works) is not
touched:
- `build/cb_docr1_withsa.tex` (preamble, `cb`, `sa`): two passes, exit 0, no errors, no undefined-reference warning
  for `sa:sec` (the aux file defines it as section 2). The paragraph renders "… they are treated in Section 2."
- `build/cb_docr1_full.tex`, a copy of `proofs.tex` with `../` paths: all twelve sections in document order, the
  current placeholder `appendix_map.tex`, and `bibliography.tex`. Three passes, exit 0, 152 pages. It has no errors,
  no undefined reference of any kind, no multiply defined label, no rerun request and no overfull box. `sa:sec` is
  Section 12 (page 145), and the paragraph renders "… they are treated in Section 12."
- An earlier full build, on the 19:03 draft of `sa.tex`, showed six overfull boxes in `sa` statement heads. The
  19:05 version above has none. This concerns only `sa`; `cb` had none in either build.

## Lean sources re-read (the paragraph's descriptions)

No statement environment was touched. The three files behind the paragraph were re-read to confirm its wording:
- `AUDIT3/A1_reduction/SizeArith.lean`:
  - lines 1-2: "the size arithmetic of the symmetric ES(7) reduction";
  - lines 13-56: the reduction part (11 theorems); lines 58-80: the upper bounds of the size table (9 theorems);
  - log `SizeArith.lean.log`: 20 axiom lines, each within {propext, Classical.choice, Quot.sound}.
- `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean`:
  - line 1: "Size bookkeeping for the assembled symmetric theorem";
  - 7 theorems and the control `example` at line 30;
  - log `AssembledSizes.lean.log`: the unused-variable warning for `hp` (24:41) and 7 axiom lines within the same set.
- `ES7SPLIT/review/equivalence/BaekSeven.lean`:
  - lines 6-9: `baek_seven {γ : Type} [LinearOrder γ] (C : Config γ) (S : Finset γ) (h : 17 ≤ S.card) :
    C.HasNCap 4 S ∨ C.HasNGon 7 S`;
  - the proof is `main 4 C S (e ▸ h)` with `e : Nat.choose (4 + 2) 2 + 2 = 17` by `decide`;
  - `BaekSeven.out`: `#check @main`, which matches Theorem `mb:thm:baek`, and `baek_seven` depends on
    [propext, Classical.choice, Quot.sound].

So "Lean-checked", "the size arithmetic of the reduction of the symmetric $k=7$ theorem to its case classes", and
"an instance of Baek's theorem for abstract configurations" are accurate. The last one is the instance n = 4 of
`main` for an arbitrary `Config γ`.

## Observation (no change; not a finding of this round)

**Wording: "theorem" or "statement".**
- `cb` says "the reduction of the symmetric $k=7$ theorem to its case classes"; the introduction of `sa` says
  "statement".
- Both fit the records. `AUDIT3/reports/A1_reduction.md` speaks of the "reduction to the case theorems" and of "the
  assembled theorem" (A1-F1).
- In context, "theorem" refers to the reduction whose hypotheses are the case classes: Theorem `sr:thm:main` states
  them as hypotheses, so nothing is presented as proved.

I left it unchanged; the consistency lens may harmonize the two words.

## Checks

- `diff` of `sections/cb.tex` and `sections/cb.map.tsv` against `snapshots/doc-r1-pre/`: both empty. SHA-256 of
  `cb.tex`: `d64b2f190c3b…`.
- Compile: `build/cb_wrapper.tex` with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`, run twice from
  `build/`. Both passes exit 0, with no `!` error and no overfull box of any size (so 0 above 1pt); 17 pages. The only
  undefined references are `sr:def:classes` (input lines 11 and 21; an export label of `sr`) and `sa:sec` (line
  1486), which resolves once `sa` is in the build (above).
- No machine path and no tool name in `cb.tex` or `cb.map.tsv` (both unchanged).
