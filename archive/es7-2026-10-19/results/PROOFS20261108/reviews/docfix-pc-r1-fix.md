# Section `pc`, whole-document review round 1: fix log

Input: finding m11 of `reviews/doc-r1-consistency.md` (the only finding assigned to `pc` in this step). The pre-edit
snapshot is in `snapshots/docfix-r1-pre/` (`pc.tex`, `pc.map.tsv`). Paths are relative to STAGE, or to RES for Lean
sources.

Result: 1 finding, fixed; 0 declined. No statement of a Lean declaration changed, and no label was removed or
renamed (34 labels, the same as before). The map stays in sync: 33 rows, the same labels, kinds, Lean names and
file:line columns; only four note fields changed.

## Findings

| # | Finding (lens, severity) | Action | Location (current pc.tex / pc.map.tsv) | What was checked / done |
|---|---|---|---|---|
| 1 | m11 (consistency, minor): pc introduces "written observation(s)", a term not in fd's rigor vocabulary; other sections say "written step" | fixed | pc.tex lines 66, 564, 596, 1013; pc.map.tsv rows `pc:rem:alt-boundary`, `pc:rem:runB-example`, `pc:rem:gaps`, `pc:rem:runs` (note column) | The finding is correct. fd defines three rigor labels and uses "written step" for a statement or part that carries no Lean label (paragraph "Rigor labels" from fd.tex:48, the "written step" sentence at fd.tex:77-79, and fd's "Written steps" paragraph at fd.tex:1180-1186). The CONTRACT uses the same tag, and sa uses it for a remark: "This remark is a written step; it is not Lean-checked" (sa.tex:486, sa.tex:112). The term "written observation" occurs only in pc (no other section or map uses it). It entered in round doc-r0 (reviews/pc-doc-r0-fix.md, note 3). Defining a new term in fd is outside this fixer's files, so I used fd's existing term. Changes: (a) "Rigor and axioms", line 66: "the mathematical claims they add to the Lean statements are written steps and are not Lean-checked" (was "are written observations"; wording parallel to sa.tex:112). (b) Remark pc:rem:gaps(2), line 564: "(a written step, not part of the Lean statement)". (c) Remark pc:rem:runs, line 596: "(a written step, not Lean-checked)". (d) Coverage, line 1013: "Remarks ... contain further written steps (with proofs) that are not Lean statements" ("further" links it to the preceding sentence, "Lemma pc:lem:shift is a written step"). (e) Map notes: "written observation:" became "written step:" (three rows) and "written observations:" became "written steps:" (pc:rem:gaps). This is the same note pattern as oc:lem:rot-add, ec:fact:prim, sa:rem:use and pc:lem:shift. The generated appendix already classes these four remarks as "written step" in its second column (appendix_map.tex:188, 191, 193, 195), so the notes now agree with it. Re-read for the remarks touched: `PhaseClassification.gap_classification` (RES `LEANEXT/phase/PhaseClassification.lean:268`) concludes only the four-way disjunction, and its docstring says "for exactly one of the three cyclic labellings", as pc:rem:gaps(2) states. `PhaseClassification.phase_trichotomy` (`:285`) concludes exactly (i) ∧ (ii), with no mutual exclusion of runs, as pc:rem:runs states. `alternating_iff_gaps_lt_pi` (`:210`), `runMidB_iff` (`:251`) and the definitions `inArc`, `arcHasAntipode`, `Alternating`, `RunMid{B,D,A}` (`:117-140`) match pc:thm:alternating, pc:thm:runB and pc:def:arc, on which the four remarks rely. I also re-checked both remark arguments. In pc:rem:gaps(2), two of the last three disjuncts add up to 2π+g_j<2π, and the first disjunct makes each sum of two gaps >π. In pc:rem:runs, the five positions of α+π relative to β and δ give H1, H2, H3, H1 (k=−1), H3. Both are correct and unchanged. |

## Checks

- Compile: `build/pc_wrapper.tex`, run twice from `build/` with `nice -n 15 pdflatex -interaction=nonstopmode
  -halt-on-error`. Both runs exit 0, with no `!` errors and no "Missing"/"Runaway" messages. There are 0 overfull boxes
  in total (so 0 above 1pt) and no multiply defined labels. The 14 undefined references are all export labels of fd,
  ll and lg (fd:def:{inv,ngon,orient,point,rot}, fd:lem:orient, ll:def:{hv,peel},
  lg:def:polar, lg:lem:{polar,ruleA,ruleB,sinadd}, lg:thm:radius), which are expected in the standalone check.
- Layout: the pre-edit snapshot, built with the same preamble (`build/docfix_r1_pc_snapcheck/`), has 51 underfull
  lines, 0 overfull boxes and 13 pages. The edited file gives 51 underfull lines at identical source line ranges,
  0 overfull boxes and 13 pages.
- Hygiene: there are no machine paths and no tool names in `pc.tex` or `pc.map.tsv`. "observ" no longer
  occurs in either file. The 34 labels are identical to the snapshot. Every map row has 5 tab-separated fields.

## For the orchestrator

- `appendix_map.tex` still shows the old notes for the four remark rows (lines 188, 191, 193, 195). It is generated
  from the maps, so rerun `python3 tools/make_appendix.py` (this fixer may edit only `pc.tex` and `pc.map.tsv`).
