# Section `pc`, final pass round 1: re-check of the fix

Inputs:
- the fix log `reviews/final-pc-r1-fix.md`;
- the pre-edit snapshot `snapshots/final-r1-pre/pc.tex` and `pc.map.tsv`;
- the current `sections/pc.tex` and `sections/pc.map.tsv`;
- the rule in `sections/fd.tex`;
- the Lean source in RES.

Paths are relative to STAGE, or to RES for Lean sources and records. REPO is at commit `7e32ee259`, and
`LEANEXT/phase` has no local changes.

Verdict: **pass**. The finding is resolved correctly. The edit changes nothing else and introduces no new problem.
One minor item remains for the orchestrator: the generated appendix has not been regenerated.

## 1. Finding 1 (minor): pc:thm:word labelled "computer-assisted" instead of "computer-assisted in Lean"

Status: **resolved correctly**.

**The rule.** `sections/fd.tex:92-96` reads: "If the Lean proof of a statement is a finite computation and this
document also gives a complete written proof of the statement that does not use the computation, the statement is
labelled *computer-assisted in Lean*, usually with a pointer to the written proof (as in 'computer-assisted in Lean;
written proof by hand')". fd.tex:10-13 announces the same qualified label.

**The Lean proof is a finite computation.**
- File: `LEANEXT/phase/PhaseClassification.lean`, 545 lines. Its SHA-256 is `490efcd0a7e48e80...`, matching the
  prefix in pc's Sources. The file uses `namespace PhaseClassification` at l. 36 and `end` at l. 545, so the full name
  is `PhaseClassification.word_dichotomy`.
- l. 539-543: `theorem word_dichotomy : ∀ s : Fin 6 → Bool, (∀ i : Fin 6, s (i + 3) = !s i) → ((∀ i, s (i+1) = !s i)
  ∨ ∃ i, s i ∧ s (i+1) ∧ s (i+2)) ∧ ¬ ((∀ i, ...) ∧ ∃ i, ...) := by decide`.
- The proof is the single tactic `decide`. The file has no `native_decide`, `sorry`, `admit` or `axiom`. Its other
  hits for "decide" are in comments.
- `LEANEXT/phase/logs/axioms.log:16` lists `[propext, Classical.choice, Quot.sound]`.

**The statement is faithful.** The statement of pc:thm:word (pc.tex:770-775) is unchanged and still matches l. 539
exactly:
- the same premise;
- (i) is the disjunction and (ii) the negated conjunction;
- the quantifier order is the same;
- Boolean atoms are read as `= true`, as fixed at pc.tex:767.

The head's name and `file:line` are correct.

**The hand proof (pc.tex:796-822) is complete without the computation.** I re-did it by hand.
- The premise at i = 0, 1, 2 forces s = (x, y, z, ¬x, ¬y, ¬z), so at most 8 words satisfy it. The converse stated
  there is also correct, although it is not needed.
- All 8 rows of the table are right. The words are PPPAAA, PPAAAP, PAPAPA, PAAAPP, APPPAA, APAPAP, AAPPPA and AAAPPP,
  with runs at 0, 5, 4, 1, 2 and 3 (the runs at 5 and 4 wrap around) and the two alternating words.
- The argument for (ii) is general: alternation means s(i) and s(i+1) are never both true.
- The "shorter argument" for (i) is also valid. An equal pair {i, i+1} gives the equal pair {i+3, i+4} with the
  opposite value, so one of the two pairs is PP, at j, j+1. Then either s(j+2) = P, or s(j-1) = s(j+5) = ¬s(j+2) = P.
- As a cross-check only, not part of the proof, I enumerated all 64 functions. Exactly 8 satisfy the premise. All 8
  match the table, and the dichotomy holds for each. The word PPAPPA of the M7 remark falsifies the mutated statement.
  The M7 record also checks out: `LEANEXT/phase/mutants.py:23` and `LEANEXT/phase/logs/mutants.log:7` say what pc.tex
  states.

So the qualified label is required by fd's rule. It is neither rounded up nor rounded down. The statement keeps its
Lean-checked status through the Lean reference in the head, as fd.tex prescribes.

**All three sites carry fd's example phrase verbatim.**
- the head, pc.tex:769: "discrete dichotomy, computer-assisted in Lean; written proof by hand; Lean: ...";
- the Coverage entry, pc.tex:998;
- the map note of row `pc:thm:word`.

The wording agrees with:
- pc's introduction (pc.tex:23-24, unchanged);
- ec's analogous head (ec.tex:785, "computer-assisted in Lean; written proof by hand; Lean: ...") and its map note;
- the recommendation N1 in `reviews/docfix-fd-r1-recheck.md`.

The paragraph "Rigor and axioms" (pc.tex:63-102) and "How Lean checks it" (pc.tex:777-794) needed no change, and none
was made. No other section and no part of `proofs.tex` refers to the rigor label of pc:thm:word.

## 2. Diff review (`diff -u` against the snapshot)

- `pc.tex` has 2 hunks, each one changed line:
  - l. 769 (the head): ", computer-assisted;" becomes ", computer-assisted in Lean; written proof by hand;".
  - l. 998 (Coverage): ", computer-assisted)" becomes ", computer-assisted in Lean; written proof by hand)".
  - The line count is still 1014, and the 34 `\label`s are identical and in the same order.
- `pc.map.tsv` has 1 changed row, `pc:thm:word`, and only in its note column. Columns 1-4 of all rows are
  byte-identical. In the new note:
  - "written proof by hand (8 words) given" moved to the front.
  - The Lean details now follow "Lean proof:".
  - No content was dropped.
  - The note's claims are true: the proof is `decide`, there is no `native_decide`, the decision runs over 64
    functions, and the conclusion is evaluated only for the 8 that satisfy the premise. The last point holds because
    the decision procedure for an implication evaluates the premise first; pc.tex:782-784 says the same.
- Map integrity:
  - The header is unchanged, and all 33 lines have 5 tab-separated fields.
  - The map is ASCII only, with no CR characters and a final newline.
  - The 32 statement environments match the 32 rows in label, order and kind.
- Hygiene:
  - There are no machine paths and no tool names in `pc.tex` or `pc.map.tsv`.
  - Neither file has non-ASCII bytes.
  - No macros or packages are added.
  - No mathematics, Lean statement or record claim changed.
- Fix-log claims I checked:
  - the line numbers;
  - the hash prefix;
  - axioms.log l. 16;
  - "no line added or removed";
  - 34 labels and 33 map lines;
  - the compile results;
  - the cited fd lines 92-96.

  All are correct.

## 3. Compile check

`build/pc_final_recheck_r1_wrapper.tex` (the contract wrapper) was compiled twice from `build/` with `nice -n 15
pdflatex -interaction=nonstopmode -halt-on-error`.
- Both runs exit 0.
- There are 0 `!` errors and no Missing, Runaway or Fatal messages.
- There are 0 overfull boxes, no multiply defined labels and no rerun request. The PDF has 12 pages.
- There are 14 undefined references, all to allowed export labels: fd:def:{inv,ngon,orient,point,rot},
  fd:lem:orient, ll:def:{hv,peel}, lg:def:polar, lg:lem:{polar,ruleA,ruleB,sinadd} and lg:thm:radius.
- The rendered head reads "Theorem 1.28 (discrete dichotomy, computer-assisted in Lean; written proof by hand; Lean:
  PhaseClassification.word_dichotomy, LEANEXT/phase/PhaseClassification.lean:539)". The Coverage entry reads
  "word_dichotomy (Theorem 1.28, computer-assisted in Lean; written proof by hand)."

For comparison I built the snapshot under the same preamble in `build/pc_final_recheck_r1_snap/`. It also has 0
overfull boxes. The only log difference is 2 additional underfull hboxes at pc.tex:770-771, the longer head, with
badness 3271 and 10000. On the page, the head's two lines have stretched interword spaces, and in pdftotext's raw
reading order the words "Lean:" and "every" are moved after the statement. This is the document's established look
for long heads: pc has many badness-10000 head lines, for example Definition 1.6 (pc.tex:271-272) and the arc lemmas
(pc.tex:373-374), and Proposition 1.25 on the same page is similar. The preamble's high tolerance in statements
exists for this purpose. Removing it would mean rewording beyond the finding. Not a finding.

## Remaining item (minor; not a defect of pc.tex or pc.map.tsv)

- `appendix_map.tex` (generated at 21:39, before the fix at 21:46) still shows the old note of `pc:thm:word` at l. 206
  ("computer-assisted: decide ...").
- I ran `tools/make_appendix.py` on a scratch copy of the sections (`build/pc_final_recheck_r1_appendix/`, with
  bytecode writing disabled). It produces 470 rows.
  - The pc row becomes "computer-assisted in Lean; written proof by hand (8 words) given; Lean proof: decide (...), no
    `native_decide`".
  - The same regeneration also picks up this round's pending changes to rows of ec, mb, cb and sa.
  - The scratch appendix compiles twice with exit 0, 0 errors and 0 overfull boxes, and the pc row typesets correctly.
- Action for the orchestrator: run `python3 tools/make_appendix.py` once all final-round section fixes are in.

Observation, not a finding: the fixer's dry run imported the generator, which wrote
`tools/__pycache__/make_appendix.cpython-314.pyc` (21:47). Like any bytecode cache, it embeds the absolute source path.
It is not a .tex or .tsv output. If `tools/` is ever copied out of the staging area, leave `__pycache__` behind.

## Findings

| # | Severity | Location | Issue | Fix |
|---|---|---|---|---|
| 1 | minor | appendix_map.tex:206 (generated from pc.map.tsv) | The generated appendix is stale: the pc:thm:word note still reads "computer-assisted: decide ...". The source map is fixed. | Rerun `python3 tools/make_appendix.py` after all final-round fixes. Checked in a scratch copy: the pc row changes as intended and the appendix compiles cleanly. |

No blocker or major finding remains or was introduced.
