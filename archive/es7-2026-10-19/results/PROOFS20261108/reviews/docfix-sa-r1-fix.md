# docfix sa, round 1 (whole-document review)

Pre-edit snapshot: `snapshots/docfix-r1-pre/sa.tex`, `snapshots/docfix-r1-pre/sa.map.tsv`.
Edited: `sections/sa.tex`, `sections/sa.map.tsv` (nothing else). Labels unchanged; map columns label/kind/lean_name/file_line
unchanged; only two map notes changed.

| # | finding | action | location (new lines) | reason / check |
|---|---|---|---|---|
| 1 | xref-srarcbsa 3, minor: "(This is also shown after Definition sr:def:classes.)" | fixed | sa.tex:473-474, proof of Lemma sa:lem:model(b) | Checked sr.tex:228-235. The fixed-point argument for reflLine with u_0^2+u_1^2=1 (both directions, through d) is the last paragraph inside the definition environment of sr:def:classes, which ends at sr.tex:236. The text now reads "(This is also shown at the end of Definition sr:def:classes.)". The other pointer, sa.tex:564 ("the remark that follows Definition sr:def:classes", i.e. sr:rem:records at sr.tex:242), is correct and unchanged. |
| 2 | consistency m1, minor: the reason given for "not computer-assisted" also fits ec:prop:ex341 | fixed | sa.tex:104-115 (paragraph "Rigor"); sa.tex:220-223 (end of the proof of sa:lem:split); sa.map.tsv notes of sa:lem:split and sa:thm:baek-seven | New reason: no statement of the section is a finite computation. The Lean-checked statements are universally quantified (over N; for baek_seven over linearly ordered types, configurations and finite sets), and the control is the negation of such a statement. decide only closes side facts inside these proofs and never evaluates a whole statement: the five closed instances s = 2..6 of the conclusion of A1.order_split, C(6,2)+2 = 17 in baek_seven, and 32 <= 32 in the control. The written proofs also check these facts by hand. This separates sa from ec:prop:ex341, a closed statement that decide evaluates as a whole. When this fix was made, fd.tex had not changed (its rigor block still matched the snapshot). The wording holds under the current fd definition (fd.tex:65-75: "decide only for facts that the written proof ... establishes by hand") and under the fd fix proposed in consistency M1 ("side facts inside a proof of a statement that is not itself a finite computation"). It also holds under the alternative in claims F7 (a label "computer-assisted in Lean" for statements whose Lean proof is a kernel evaluation), since no sa proof evaluates a whole statement. I left out a sentence claiming that no Lean proof "decides" a statement, because omega is a decision procedure (paragraph "Conventions"); it builds a proof term that the kernel checks and is not kernel evaluation. |
| 3 | typesetting F17, minor: an internal audit identifier in the heading of 12.3 | fixed | sa.tex:276 | New title: "Size bookkeeping for the assembled statement (audit finding A1-F1)". It follows the header of AssembledSizes.lean ("Size bookkeeping for the assembled symmetric theorem (finding A1-F1)") and tells the reader of the contents that A1-F1 is an audit finding. I did not use the reviewer's suggestion "The assembled statement (audit finding A1-F1)" word for word: the subsection contains the size bookkeeping, not the assembled statement. Label sa:ssec:assembled is unchanged. |

## Lean declarations re-read (no statement text changed)

- `A1.order_split`, `AUDIT3/A1_reduction/SizeArith.lean:52` (proof lines 53-56: Nat.lt_or_ge; omega to s in {2,...,6};
  rcases with rfl; decide on each closed disjunction). The statement of sa:lem:split matches.
- `baek_seven`, `ES7SPLIT/review/equivalence/BaekSeven.lean:6-9` (decide only for `Nat.choose (4 + 2) 2 + 2 = 17`).
  The statement of sa:thm:baek-seven matches.
- The anonymous example at `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean:30-31` (`by decide` for 32 <= 32).
- `ErdosSzekeres.SymReduction.reflLine`, `SYMLEAN/SymmetricReduction.lean:423-425`. The formula in sa:lem:model(b)
  matches it and the argument at the end of sr:def:classes.

## Checks

- Compile: `build/sa_wrapper.tex`, compiled twice from `build/` with nice -n 15 pdflatex: exit 0 both times, no errors,
  0 overfull boxes, and no undefined references other than the expected references to other sections' labels. There is
  one underfull \vbox in the output routine (the pre-edit text, compiled the same way, had two). Still 8 pages. I looked
  at the rendered pages 2-4.
- No machine paths, tool names, or new macros in sa.tex or sa.map.tsv. The map is ASCII.
- Appendix: the note conversion of `tools/make_appendix.py` was tried in a dry run on the two new notes (imported, not
  run; mb:thm:baek becomes a \ref). `appendix_map.tex` was not regenerated, because it is outside this fixer's scope.
  It must be regenerated to pick up the two new notes.
- Follow-up for the orchestrator: if the fd fixer words the "side facts" rule differently, the sa paragraph "Rigor"
  (sa.tex:107-115) may need only a light wording alignment; its claims stay true under each proposed fd convention.
