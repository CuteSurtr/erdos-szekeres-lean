# Final pass, round 1, section pc: fixes

Files edited: `sections/pc.tex` and `sections/pc.map.tsv` (snapshot before editing: `snapshots/final-r1-pre/`).
Line numbers refer to the edited `sections/pc.tex` (1014 lines, as before; no line was added or removed).

## Finding 1 (minor): Theorem pc:thm:word labelled "computer-assisted" instead of "computer-assisted in Lean"

- Action: fixed.
- Locations: head of Theorem `pc:thm:word` (l. 769); Coverage paragraph, entry for `word_dichotomy` (l. 998); row
  `pc:thm:word` of `sections/pc.map.tsv` (note column).
- Rule: `sections/fd.tex` ll. 92-96: if the Lean proof of a statement is a finite computation and the document also
  gives a complete written proof that does not use the computation, the statement is labelled "computer-assisted in
  Lean", usually with a pointer to the written proof, as in "computer-assisted in Lean; written proof by hand".
- Check against the source: `LEANEXT/phase/PhaseClassification.lean` (545 lines, SHA-256 `490efcd0a7e4...`, the hash
  given in pc's Sources), l. 539:
  `theorem word_dichotomy : ∀ s : Fin 6 → Bool, (∀ i : Fin 6, s (i + 3) = !s i) → ((∀ i : Fin 6, s (i + 1) = !s i) ∨
  ∃ i : Fin 6, s i ∧ s (i + 1) ∧ s (i + 2)) ∧ ¬ ((∀ i : Fin 6, s (i + 1) = !s i) ∧ ∃ i : Fin 6, s i ∧ s (i + 1) ∧
  s (i + 2)) := by decide`.
  The Lean proof is the single tactic `decide`, a finite computation. The statement of `pc:thm:word` (ll. 769-775)
  still matches the declaration exactly: the same premise, the disjunction (i) and the negated conjunction (ii), the
  same quantifier order, with Boolean atoms read as `= true` as fixed at l. 767. The head's name, file and line are
  correct. `LEANEXT/phase/logs/axioms.log` l. 16 lists `propext`, `Classical.choice` and `Quot.sound`.
- Completeness of the hand proof (ll. 796-821), checked step by step without the machine computation:
  - The premise at i = 0, 1, 2 gives s = (x, y, z, ¬x, ¬y, ¬z), so there are at most 8 such words.
  - The table lists all 8 words with the claimed property. Each row was checked by hand: the word, the run position
    mod 6, or the alternation including the wrap-around pair (5, 0).
  - (ii) follows from alternation alone, since s(i) and s(i+1) are never both true.
  - The shorter argument for (i) in parentheses is also correct. An equal pair {i, i+1} gives the equal pair
    {i+3, i+4} with the opposite value, so one of the two pairs is PP, at j, j+1. If s(j+2) = P there is a run at j.
    Otherwise s(j-1) = s(j+5) = ¬s(j+2) = P, and there is a run at j-1.

  As a cross-check only (not part of the proof), a small enumeration confirmed the eight rows of the table and the
  dichotomy for them. So the document gives a complete written proof that does not use the computation. Under fd's
  rule the label is "computer-assisted in Lean", and the finding is right.
- Head, old wording:
  `\begin{theorem}[discrete dichotomy, computer-assisted; \leanref{PhaseClassification.word_dichotomy}{LEANEXT/phase/PhaseClassification.lean:539}]\label{pc:thm:word}`
- Head, new wording:
  `\begin{theorem}[discrete dichotomy, computer-assisted in Lean; written proof by hand; \leanref{PhaseClassification.word_dichotomy}{LEANEXT/phase/PhaseClassification.lean:539}]\label{pc:thm:word}`
- Coverage, old wording: "\lean{word_dichotomy} (Theorem~\ref{pc:thm:word}, computer-assisted)."
- Coverage, new wording: "\lean{word_dichotomy} (Theorem~\ref{pc:thm:word}, computer-assisted in Lean; written proof
  by hand)."
- Map note, old wording: "computer-assisted: decide (evaluated during elaboration and again by the kernel over the 64
  functions Fin 6 -> Bool; the conclusion only for the 8 satisfying the premise), no native_decide; written proof by
  hand (8 words) given"
- Map note, new wording: "computer-assisted in Lean; written proof by hand (8 words) given; Lean proof: decide
  (evaluated during elaboration and again by the kernel over the 64 functions Fin 6 -> Bool; the conclusion only for
  the 8 satisfying the premise), no native_decide"
- Notes:
  - All three places use the requested wording verbatim. It is fd's example phrase and agrees with pc's
    introduction (ll. 23-24, unchanged).
  - In the map note, the existing item "written proof by hand (8 words) given" was moved to the front so that the
    phrase reads as one unit, and the Lean details are now introduced by "Lean proof:". No information was removed.
  - The paragraph "Rigor and axioms" (ll. 63-102) needed no change. It lists `word_dichotomy` among the 16 logged
    theorems and says that `decide` occurs only in its proof.
  - In the PDF the longer head breaks after "Lean:", as the long heads on the same page do (for example
    Proposition 1.25 of the standalone build). No box is overfull.

## Checks

- Diff against the snapshot: only l. 769 and l. 998 of `pc.tex` and the row `pc:thm:word` of `pc.map.tsv` changed.
  Everything else is byte-identical. The 34 `\label`s are unchanged (same list in the same order), and the map has
  33 lines (header and 32 rows), as before.
- Map: the header is unchanged, every row has 5 tab-separated fields, and the file is ASCII only. A dry run of the
  appendix generator's note typesetting typeset the new note without error. This dry run called `clean_note` and
  `note_tex` from `tools/make_appendix.py` and did not write `appendix_map.tex`. `appendix_map.tex` was not
  regenerated because it is outside this fixer's edit set. It picks up the new note when the generator is next run.
  Importing the module refreshed its bytecode cache `tools/__pycache__/make_appendix.cpython-314.pyc`, a cache of
  the unchanged `tools/make_appendix.py`.
- Compile: from `build/`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error pc_wrapper.tex`, run twice.
  - Both runs exit 0, with 0 errors and 0 "Missing $".
  - 0 overfull hboxes and 0 overfull vboxes, so none above 1pt.
  - No multiply defined labels and no rerun request.
  - Undefined references only to export labels of other sections: `fd:def:inv`, `fd:def:ngon`, `fd:def:orient`,
    `fd:def:point`, `fd:def:rot`, `fd:lem:orient`, `lg:def:polar`, `lg:lem:polar`, `lg:lem:ruleA`, `lg:lem:ruleB`,
    `lg:lem:sinadd`, `lg:thm:radius`, `ll:def:hv` and `ll:def:peel`. None is to a `pc:` label.
  - A comparison build of the snapshot under a separate job name was removed afterwards.
- `pc.tex` and `pc.map.tsv` contain no machine paths and no tool names.
