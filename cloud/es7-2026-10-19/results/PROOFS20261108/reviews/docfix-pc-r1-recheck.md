# Section `pc`, whole-document review round 1: re-check of the fix

Inputs: `reviews/docfix-pc-r1-fix.md` (fix log), finding m11 of `reviews/doc-r1-consistency.md`, the pre-edit
snapshot `snapshots/docfix-r1-pre/pc.tex` and `pc.map.tsv`, the current `sections/pc.tex` and `sections/pc.map.tsv`.
Paths are relative to STAGE, or to RES for Lean sources.

Verdict: **pass**. The one finding is resolved correctly, and the edit introduces no new problem. One minor item
is left for the orchestrator: the generated appendix has not been regenerated yet (see "Remaining item").

## 1. Finding m11 (consistency, minor): "written observation(s)" is not in fd's vocabulary

Status: **resolved correctly**.

- fd defines the term the fixer adopted. fd.tex:48 ("Rigor labels") and fd.tex:77-79 say that a part marked "written
  step" does not carry the Lean-checked label, even where the text names a Lean counterpart elsewhere. fd.tex:1180
  ("Written steps") uses the term the same way. The CONTRACT's head tag is `[...; written step]`.
- Other sections use the term for remark content and parenthetical claims in the same way, for example sa.tex:116
  and :491 ("This remark is a written step; it is not Lean-checked") and ec.tex:800 ("(a written step)"). The new
  pc wording "written steps and are not Lean-checked" (pc.tex:66) follows sa.tex:116.
- All four text sites named in the finding were changed: pc.tex:66, 564, 596 and 1013. The four map notes
  (`pc:rem:alt-boundary`, `pc:rem:runB-example`, `pc:rem:gaps`, `pc:rem:runs`) now read "written step:" or "written
  steps:", the same pattern as `oc:lem:rot-add`, `ec:fact:prim`, `sa:rem:use` and `pc:lem:shift`.
- "observ" no longer occurs in `pc.tex`, `pc.map.tsv` or any other section file or map. It still occurs in the
  generated `appendix_map.tex` only (see "Remaining item").
- The fixer chose not to define a new term in fd. That is correct: fd's existing term covers this case, and fd is
  not among the fixer's files.

## 2. Diff review (`diff -u` against the snapshot)

`pc.tex` has 4 hunks, all terminology only. `pc.map.tsv` has 4 changed rows, and only in the note column: the
label, kind, lean_name and file_line columns are byte-identical. The 34 labels are identical to the snapshot. The
32 statement environments match the 32 map rows in label, order and kind. Each row has 5 tab-separated ASCII fields.

| Hunk | Old -> new | Referee check |
|---|---|---|
| pc.tex:66 (Rigor and axioms) | "are written observations" -> "are written steps and are not Lean-checked" | Matches fd's definition. "Not Lean-checked" is accurate: remarks carry no Lean head, and fd's convention allows a Lean counterpart named elsewhere (pc:rem:word-scope names ENCBLEAN counterparts, which are claims about records with their axioms evidence, not added mathematical claims). The rigor label is not rounded up. |
| pc.tex:564 (Remark pc:rem:gaps(2)) | "a written observation" -> "a written step", still "not part of the Lean statement" | The claim is correct. If all gaps are below pi, each sum of two gaps is 2pi minus the third, which is above pi. Any two of the last three disjuncts add up to 2pi + g_j < 2pi, impossible since g_j > 0. Only the ordering is needed. |
| pc.tex:596 (Remark pc:rem:runs) | "a written observation" -> "a written step", still "not Lean-checked" | The claim is correct. The five positions of alpha+pi give H1 (k=0), H2, H3, H1 (delta+pi, k=-1) and H3 (beta+pi, k=0). Any two runs together give not-H1, not-H2 and not-H3. |
| pc.tex:1013 (Coverage) | "written observations" -> "further written steps" | "Further" links back to the preceding sentence, which calls Lemma pc:lem:shift a written step. All four remarks do contain their proofs (citations of pc:lem:empty and the arguments above). |
| map notes, 4 rows | "written observation(s):" -> "written step(s):" | The notes agree with the text and with the appendix's second column ("written step"). |

Lean re-read (RES `LEANEXT/phase/PhaseClassification.lean`: 545 lines, SHA-256 `490efcd0a7e4...`, as pc states).
`inArc`, `arcHasAntipode`, `Alternating`, `RunMidB`, `RunMidD` and `RunMidA` are at :117, :120, :126, :132, :136 and
:140. `arc1_empty` through `arc1_empty'` are at :161-201, `alternating_iff_gaps_lt_pi` at :210, `runMidB_iff` at :251
(hypothesis `α + 2 * π - δ ≠ π`), `gap_classification` at :268 (conclusion: only the 4-way disjunction; the docstring
says "for exactly one of the three cyclic labellings") and `phase_trichotomy` at :285 (conclusion: (Alt ∨ A ∨ B ∨ D) ∧
(Alt → ¬A ∧ ¬B ∧ ¬D)). Definition pc:def:arc, Lemma pc:lem:empty, Theorems pc:thm:alternating, pc:thm:runB and
pc:thm:trichotomy, and Proposition pc:prop:gaps state these faithfully. No statement of a Lean declaration was
touched.

Independent check of the remark claims, in exact rational arithmetic with angles in units of pi and inArc taken
literally from the Lean definition. 87,949 ordered triples were tested, including gaps equal to pi:
- H1 ∨ H2 ∨ H3 always holds, and the runs are pairwise exclusive (pc:rem:runs).
- The four disjuncts of gap_classification are pairwise exclusive under the ordering alone (pc:rem:gaps(2)). Under
  genericity, exactly one disjunct and exactly one pattern hold.
- A gap equal to pi excludes alternation (pc:rem:alt-boundary).
- The triple (0, pi, 3pi/2) makes all four disjuncts false, and every hypothesis except beta-alpha≠pi holds
  (pc:rem:gaps(1)).
- At (0, pi/2, pi), RunMidB holds while delta-alpha<pi fails, with g3 = pi (pc:rem:runB-example).

Claims in the fix log about other files were checked:
- fd.tex:48, 77-79 and 1180 are as cited.
- sa.tex:112 and :486 are correct for the snapshot. sa.tex was edited afterwards (20:39), and the same sentences
  are now at :116 and :491. This affects only the log, not pc's output.
- The term was introduced in round doc-r0, as the log says (`reviews/pc-doc-r0-fix.md`, item 3).

Hygiene:
- There are no machine paths and no tool names in `pc.tex` or `pc.map.tsv`.
- No macros or packages are defined in the section.
- The word "proved" occurs at pc.tex:791 and :828. Both are pre-existing, outside the diff and not overclaims: the
  first quotes a Lean error message, the second says "is not proved".

## 3. Compile check

`build/pc_recheck_r1_wrapper.tex` (the contract wrapper) was compiled twice from `build/` with `nice -n 15 pdflatex
-interaction=nonstopmode -halt-on-error`.
- Both runs exit 0, with no `!` errors and no Missing, Runaway or Fatal messages.
- There are 0 overfull boxes and no multiply defined labels.
- There are 51 underfull boxes, at the same source line ranges as the fixer's snapshot build
  (`build/docfix_r1_pc_snapcheck/`), which also has 0 overfull boxes. The PDF has 13 pages.
- There are 14 undefined references, all allowed export labels: fd:def:{inv,ngon,orient,point,rot}, fd:lem:orient,
  ll:def:{hv,peel}, lg:def:polar, lg:lem:{polar,ruleA,ruleB,sinadd} and lg:thm:radius.
- The rendered text of the four changed passages reads correctly (pdftotext).

## Remaining item (minor; not a defect of pc.tex or pc.map.tsv)

- `appendix_map.tex`, lines 188, 191, 193 and 195, still shows the old notes ("written observation(s): ..."). The
  file was generated at 20:03, before the fix (20:37), and is made from the maps.
- Running `tools/make_appendix.py` on a scratch copy (`build/pc_recheck_r1_appendix/`) produces 470 rows. Its pc
  rows differ from the current appendix only in these four notes, which now read "written step(s): ...".
- Action for the orchestrator: rerun `python3 tools/make_appendix.py` once all section fixes of this round are in.

## Findings

| # | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| 1 | minor | appendix_map.tex:188, 191, 193, 195 (generated from pc.map.tsv) | Stale generated appendix still shows "written observation(s)" for the four pc remarks; the source maps are fixed | Rerun `python3 tools/make_appendix.py` (checked in a scratch copy: only these four notes change in the pc rows) |

No blocker or major finding remains or was introduced.
