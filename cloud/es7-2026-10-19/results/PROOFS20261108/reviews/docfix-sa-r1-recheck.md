# docfix sa, round 1: re-check (lens "recheck")

Inputs: fix log `reviews/docfix-sa-r1-fix.md`; snapshot `snapshots/docfix-r1-pre/sa.tex` and `.map.tsv`; current
`sections/sa.tex` (SHA-256 3efcd8f363b1...) and `sections/sa.map.tsv` (SHA-256 f0340ff6344a...); the source reviews
`reviews/doc-r1-xref-srarcbsa.md` (finding 3), `reviews/doc-r1-consistency.md` (m1, with M1), `reviews/doc-r1-typesetting.md`
(F17), `reviews/doc-r1-claims.md` (F7). Lean sources read (read-only, paths relative to RES):
`AUDIT3/A1_reduction/SizeArith.lean` (all 103 lines), `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean` (all 39
lines), `ES7SPLIT/review/equivalence/BaekSeven.lean` and `BaekSeven.out`, `SYMLEAN/SymmetricReduction.lean:418-425`
(reflLine), `AUDIT3/reports/A1_reduction.md` (finding A1-F1, lines 31, 68, 100-106). Hashes of the three Lean files
still match the table in sa.tex. No lake/lean/solver was run.

**Verdict: pass.** All three findings are resolved correctly. The four hunks of sa.tex and the two changed map notes
are correct and introduce no new problem. One minor follow-up for the orchestrator (regenerate the appendix); no
blocker, no major.

## 1. The three findings

| # | finding | status | evidence |
|---|---|---|---|
| 1 | xref-srarcbsa 3 (minor): "(This is also shown after Definition sr:def:classes.)" | resolved | sa.tex:473-474 now reads "(This is also shown at the end of Definition~\ref{sr:def:classes}.)". In the current sr.tex the definition environment of sr:def:classes runs from line 211 to `\end{definition}` at line 238, and its last sentences (lines 233-237) give the same argument as sa: fixed points of reflLine_{a,u} for u_0^2+u_1^2=1 are p = a+du, and p = a+tu gives d = t and reflLine(p) = a+2tu-tu = p. So "at the end of" is exact. The other pointer (sa.tex:564, "the remark that follows Definition sr:def:classes") still names sr:rem:records, the first remark after the definition (sr.tex:244). Note: sr.tex was being edited by its own fixer while I checked (last seen 20:44:36); the definition's last paragraph and the following remark were intact in every read. |
| 2 | consistency m1 (minor): sa's reason for "not computer-assisted" also fits ec:prop:ex341 | resolved | The paragraph "Rigor" (sa.tex:104-118), the end of the proof of sa:lem:split (sa.tex:220-223) and both map notes now give the reason that M1 proposes: no statement is a finite computation; `decide` only closes side facts inside the proofs, never a whole statement. Checked against the Lean files: (a) all 20 theorems of SizeArith.lean and all 7 of AssembledSizes.lean bind natural-number variables (1 to 4 of them, e.g. `c3_no32 (k e : Nat)`, `c5_gap (k e : Nat)`, `order_split (s : Nat)`); `baek_seven` binds `{γ : Type} [LinearOrder γ] (C : Config γ) (S : Finset γ)`; the control (AssembledSizes.lean:30) is `¬ (∀ n k : Nat, n = 2 * k → 32 ≤ n → 17 ≤ k)`, the negation of such a statement. (b) `decide` occurs exactly three times in the three files: SizeArith.lean:55 (after `rcases hcases with rfl \| ... ` the five goals are the closed instances s = 2..6 of the conclusion), BaekSeven.lean:8 (`Nat.choose (4 + 2) 2 + 2 = 17`), AssembledSizes.lean:31 (`(by decide)` for `32 ≤ 32`). (c) The written proofs establish all three by hand: sa:lem:split (2,4,6 even, s≠3, s≠5), the proof of sa:thm:baek-seven (C(6,2)+2 = 15+2 = 17), sa:rem:control (32 ≤ 32). The new wording separates sa from ec:prop:ex341, whose proof (ec.tex:790) says it is "a finite computation with closed numerals". fd.tex is unchanged since the snapshot (its rule, fd.tex:65-75: decide "only for facts that the written proof does not need, or establishes by hand" does not make a statement computer-assisted); the sa wording holds under that rule, under the M1 rewrite ("side facts inside a proof of a statement that is not itself a finite computation") and under the F7 alternative ("computer-assisted in Lean" for kernel-evaluation proofs), since no sa proof is a kernel evaluation of the whole statement. The fixer's decision not to claim that no proof "decides" a statement (omega is a decision procedure, as the paragraph "Conventions" says) is right. |
| 3 | typesetting F17 (minor): internal audit identifier in the heading of 12.3 | resolved | sa.tex:276: `\subsection{Size bookkeeping for the assembled statement (audit finding A1-F1)}`, label sa:ssec:assembled unchanged (still used at sa.tex:121). The heading now tells the reader of the contents that A1-F1 is an audit finding, which was the point of the suggestion. The deviation from the suggested wording is justified: the subsection holds the size bookkeeping (sa:prop:assembled, sa:lem:big-order, the control), not the assembled statement; the wording follows the file header (AssembledSizes.lean:1, "Size bookkeeping for the assembled symmetric theorem (finding A1-F1)") and the introduction (sa.tex:18-20). The A1 report confirms "A1-F1 (minor)" as a finding of the audit (A1_reduction.md:68). The title has no math, so the PDF bookmark is plain text; it renders as a one-line run-in heading (page 4 of the wrapper). |

## 2. Diff review (snapshot vs current; 4 hunks in sa.tex, 1 hunk with 2 rows in sa.map.tsv)

- **Hunk 1, sa.tex:104-118 (paragraph "Rigor").** Mathematics and record claims verified as in finding 2 above. No
  statement text changed; the labels "Lean-checked" and "written proofs (not refereed)" are unchanged; "not
  computer-assisted" is not a rounding up, because each machine-closed side fact is also established by hand in the
  written proof. The references (sa:thm:baek-seven, sa:rem:control, sa:lem:split) are own labels. "the value
  binom(6,2)+2 = 17" is Lean's `Nat.choose (4 + 2) 2 + 2 = 17` with 4+2 evaluated, as the proof of the theorem shows.
- **Hunk 2, sa.tex:220-223 (end of the proof of sa:lem:split).** Faithful to the Lean proof (SizeArith.lean:53-56:
  `Nat.lt_or_ge`, `omega` to s ∈ {2,...,6}, `rcases ... with rfl` and `decide`, then `Or.inr` for s ≥ 7). The
  statement (sa.tex:205-207) is unchanged and matches line 52. The cross-reference to the paragraph "Rigor" is
  correct.
- **Hunk 3, sa.tex:276 (subsection title).** See finding 3.
- **Hunk 4, sa.tex:473-474 (proof of sa:lem:model(b)).** See finding 1. The displayed sigma (sa.tex:438-440) still
  equals `reflLine` at SymmetricReduction.lean:423-425.
- **Map (sa.map.tsv rows sa:lem:split and sa:thm:baek-seven).** Only the note column changed; label, kind,
  lean_name and file_line are unchanged; 13 rows, 5 fields each, ASCII only. A dry run of the note conversion of
  `tools/make_appendix.py` (imported, nothing written; script `build/sa_recheck_r1_notes.py`) converts both notes
  without error; `mb:thm:baek` becomes `Theorem~\ref{mb:thm:baek}` and `>=` becomes `\textgreater{}=`.
- No machine path, no tool name, no `\newcommand`/`\def`/`\usepackage` in sa.tex or sa.map.tsv; the
  words "verified"/"certified" do not occur; "proved" occurs only in negations or for this document's written steps
  (unchanged text).

## 3. Compile check

`build/sa_recheck_r1_wrapper.tex` (contract wrapper), compiled twice from `build/` with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`: exit 0 both runs; no `!` error, no "Missing", no
overfull box, no hyperref warning, no multiply defined label; one underfull \vbox in the output routine (the fixer
reported the same). 8 pages. Undefined references (51 occurrences) are only fd: labels and export labels of ll, lg,
ec, sr, ar, mm, mb, as expected standalone; no sa: label is undefined. Pages 2, 3, 4 and 6 (the four changed
passages) were rendered and inspected: the paragraph "Rigor", the end of the proof of Lemma 1.4, the heading 1.3 and
the parenthesis in the proof of Lemma 1.12 typeset cleanly.

## 4. Remaining findings

- **minor (orchestration, not a defect of the fix):** `appendix_map.tex` (generated 20:03, before the fix) still
  has the old notes at lines 505 (sa:lem:split: "omega plus decide on the five closed cases s = 2..6, which the
  written proof checks by hand; not computer-assisted") and 511 (sa:thm:baek-seven: "C(6,2)+2 = 17 (decide in Lean,
  checked by hand; not computer-assisted)"), which is the wording consistency m1 objected to. Fix: run
  `python3 tools/make_appendix.py` from STAGE after all docfixes of this round. The fixer flagged this correctly and
  it was outside its scope.

## 5. Observations (no finding)

- The control's Lean proof also uses `rfl` for 32 = 2*16, which the kernel checks by evaluation. The paragraph "Rigor"
  enumerates only the uses of `decide`, which is literally correct and matches fd's rule (stated for `decide`);
  Remark sa:rem:control names the `rfl` and checks 32 = 2*16 by hand. No change needed.
- fd's M1 fix has not been made yet (fd.tex unchanged since 18:44). If the fd fixer adopts wording other than M1's
  "side facts", the paragraph "Rigor" may need only a wording alignment; its claims are true under each proposed
  convention.
