# Polish round 1 for section `cb`: fix log

Files: `sections/cb.tex` (1,475 lines after the fix; 1,440 before) and `sections/cb.map.tsv` (100 rows plus header,
unchanged in number and order). Snapshot before editing: `snapshots/polish-r1-pre/`. Locations below are line numbers
of `sections/cb.tex` after the fix.

Inputs read: `reviews/cb-r1-fidelity.md`, `cb-r1-rigor.md`, `cb-r1-adversarial.md`, `cb-r1-claims.md`,
`cb-writer-concerns.md` (no overfull boxes listed). Lean declarations re-read before editing a statement:
`C3LEAN/C3Cover.lean` 34-422, 1700-1760, 2236-2327 and `C2FINAL/Central34Orbits.lean` (full). Records re-read:
`C3LEAN/README.md`, `C2FINAL/README.md`, `C3LEAN/logs/compile.log`, `C3LEAN/review/logs/revctrl_pass.log`,
`WRITEUP/note/symmetric_extremal.tex` 100-120, `WRITEUP/SYMMETRIC.md` §0, §1, §3, and the inventory `C3-C2-misc`.

## Findings

| # | report and id | summary | action | location after the fix | reason (if declined) |
|---|---|---|---|---|---|
| 1 | fidelity #1; claims M1 | head of export lemma `cb:lem:run` used a `tabular`; the first reference floated above the lemma | fixed: plain contract form `\leanref{...}, \leanref{...}`; checked in the PDF (head now on the lemma line, no overfull box) | 577 | |
| 2 | fidelity #2; rigor m5; adversarial 4; claims M7 | Remark `cb:rem:cert` said "a σ-split on K digits" | fixed: "a σ-split on the K smallest free residues of n (K σ bits, 2^K children)" | 566-568 | |
| 3 | fidelity #3; claims M9 | `mod` applied to possibly negative integers without a definition (overview, Remark `cb:rem:c2-reading`, Corollary `cb:cor:c2`) | fixed: Notation now defines x mod y for integers x as the least nonnegative residue; overview says "the residue of a−i modulo 17"; Corollary `cb:cor:c2` defines ρ_a(i) = ((a+17)∸i) mod 17 on {0,…,16} ("the residue of a−i modulo 17") | 100-101; 22-23; 1384-1385 | |
| 4 | fidelity #4; rigor m1; adversarial 3; claims M2; claims M3 | computer-assisted label missing on `cb:thm:c3`, `cb:lem:all-checked` and on the `decide +kernel` statements that have written proofs | fixed: every kernel-evaluation statement now carries "(Computer-assisted …)" in its statement ("in Lean, by kernel evaluation; written proof in …" for Facts `refl-h3`, `refl-h6`, `topcases`, `strata`, `roots-match` and Theorem `c2-refl`); every statement whose proof uses a computer-assisted fact on generated data carries "(Computer-assisted: the proof uses …)" (`all-checked`, `cor:roots`, `thm:c3`, `cor:c2`); the "Rigor labels and dependencies" paragraph states this policy; map notes updated (label "Lean-checked" kept) | 80-93; 750; 766; 771; 779; 788; 804; 1087; 1116; 1295; 1384 | |
| 5 | fidelity #5; rigor m4; adversarial 1 | "Each Lean declaration of the scope has its own statement below" is not literally true (families share one statement) | fixed: "Each Lean declaration of the scope, or each uniform family of generated declarations (certs0…certs126; batch0…batch126; the ten reflection_facts_H6_*; closedP1…closedP8), has a statement below whose head carries its Lean reference; for a family the head cites the first member, and the statement locates the others"; the head of `cb:lem:run` carries two declarations | 88-93 | |
| 6 | fidelity #6; rigor m7; adversarial 5; claims M4 | Remark `cb:rem:use`: "lrat-check verdicts alone carry no weight" is stronger than the source | fixed: source wording ("acceptance by lrat-check alone is not a certificate", "lrat-check verdicts are supporting only"), cited as lines 111-114 of `WRITEUP/note/symmetric_extremal.tex` (checked: the passage spans 111-114) with `LRATCHECK20261105`; conclusion "of the two recorded verdicts, only the cake_lpr verdict counts as a certificate" cited to `WRITEUP/SYMMETRIC.md` §3 (which says exactly this) | 1155-1158 | |
| 7 | fidelity #7 | overview item (1) omitted that the proof also uses `roots_codes_match` and `roots_match` | fixed: overview names Fact `cb:fact:roots-codes` (computer-assisted) and Fact `cb:fact:roots-match` (with written proof) | 14-18 | |
| 8 | rigor m2 | notation overloaded: B_a(V) predicate in Theorem `cb:thm:c2-refl`(ii) vs B_a = bitset(closedP_a); ρ for roots and for the reflection | fixed: the predicates of (ii) are now Img_a(V) and Inv_a(V) (B_a keeps its meaning, the Lean local `B` of `uncovered`); the reflection is ρ_a throughout the proof of `cb:thm:c2-refl`, in `cb:cor:c2` and `cb:rem:c2-scope`; ρ is used only for roots; proof of (ii) now names the conjunct it shows | 1302-1304; 1318-1338; 1384-1397 | |
| 9 | rigor m3 | statement of Proposition `cb:prop:refl` used r ↦ r* "defined in the proof" | fixed: statement defines r* = ((a+11)∸r) mod 11 (= a−r if r<a, = a+11−r if r>a) and lists the eight fixed two-token layers as [(b,σ),(b*,σ⊕f_b)] with b ∈ R, b < b*; the proof refers to the statement's r*; the restated list was re-checked against a transcription of `layerOptions`, `mirror`, `phi`, `refl` for all 11 top cases (exact match, four b with b<b* in every H6 case) | 984-987; 1014-1015 | |
| 10 | rigor m6; claims M11 | Coverage: `RevDiff.lean` "without theorems" (it contains the seven prelude theorems as copies) | fixed: "without theorems of its own" | 1473 | |
| 11 | adversarial 2; claims M5 | "All definitions and theorems of §§model–c3 are in C3Cover.lean" and the same for the C2 subsection are too broad (written steps; remarks cite review files) | fixed: "Every Lean reference in a statement head of … is to …; the statements tagged 'written step' have no Lean counterpart" (true: heads in these ranges cite only these files; remarks citing `RevCtrl_pass.lean` are not statement heads) | 155-157; 1183-1184 | |
| 12 | adversarial 6 | Remark `cb:rem:use`: the 90 and 720 dropped options "do not occur in the file" is imprecise (they are evaluated as options) | fixed: "are not roots of the file, so Theorem `cb:thm:c3` says nothing about them" (matches `C3LEAN/README.md` §6) | 1170-1172 | |
| 13 | claims M6 | Sources paragraph omitted the five auxiliary definitions at lines 335-365 | fixed: names `beqLayer`, `isOption`, `distinctCodes`, `codeSet`, `reflectionFacts` (lines 335-365, checked) and says "seven negative controls" | 52-55 | |
| 14 | claims M8 | Remark `cb:rem:reading`: s=2 "used for a layer of one orbit", but the top layer [(0,0)] carries s=0 | fixed: "used for a layer of one orbit other than the top layer (the one-orbit top layer [(0,0)] carries s=0)" (Lean docstring at `C3Cover.lean:36-37`) | 188-190 | |
| 15 | claims M10 | certificate lists said "lines 423–1713"; the data end at 1711 | fixed in `cb:def:certsN` and in its map row (checked: line 1711 closes `certs126`) | 648; map row `cb:def:certsN` | |
| 16 | rigor, "unsure" 1; fidelity, "not findings" 3 | Remark `cb:rem:keys` called `rev_parent_decodes` a "Lean-checked control", but its axioms are not printed | fixed: "the review's theorem … whose Lean proof is `decide +kernel`; its file compiles with exit status 0 (`C3LEAN/review/logs/revctrl_pass.log`), but the axioms of this theorem are not printed" (log checked: two `#print axioms` lines for the other two theorems, "guard: exit 0") | 423-425 | |
| 17 | claims, "not findings" 3 | commentary after Theorem `cb:thm:c2` said the kernel computes both bits; Lean's `\|\|` needs the second only when the first is false | fixed: "the disjunction of the bits … (the second bit is needed only when the first is 0); the disjunction is true for every V" | 1377-1379 | |
| 18 | rigor, "unsure" 2 | the Lean-checked label of the three Central34 theorems rests only on `C2FINAL/README.md` §6 | declined (no change needed) | Axioms paragraph 66-78; map notes | already stated explicitly in the Axioms paragraph and in the map notes; the reviewer reports no finding |
| 19 | rigor, "unsure" 3 | semantics of `Nat.lor`, `<<<`, `Nat.testBit` stated without proof | declined | Notation, "Binary digits", 133-138 | they state the meaning of Lean core operations (definitions); the statements are accurate; the reviewer reports no finding |
| 20 | writer concerns | overfull boxes > 1pt in the full-document build | none listed; none in the standalone build after the fix | - | - |

## Other changes

1. Fact `cb:fact:c2-sub`: the label "(Computer-assisted.)" moved to the start of the statement with "The statement is",
   so the body begins with a sentence instead of a display; "Equivalently …" unchanged in content (line 1351).
2. Coverage, "Covered" paragraph: "every definition of the scope has its own definition above" (same inaccuracy as
   finding 5) now reads "is covered by a definition above (the generated family certs0, …, certs126 by a single one)";
   `closedP1`–`closedP8` marked "(by a single definition)" (lines 1419-1420, 1444).
3. Remark `cb:rem:use`: added the project's own list of what the Lean check leaves open, with the status it records for
   each part (`C3LEAN/README.md` §6), and the trust base of the threefold theorem (Theorem 1 of `WRITEUP/SYMMETRIC.md`,
   §3 there), so the recorded trust gaps (recorded verdicts of deleted proofs, CNF encoding, geometry) are pointed to
   with the project's own labels and none is rounded up (lines 1176-1178).
4. Remark `cb:rem:c2-scope`: added, as for the threefold split, that of the two recorded checker verdicts only the
   cake_lpr verdict counts as a certificate, and the trust base of the central theorem (Theorem 4 of
   `WRITEUP/SYMMETRIC.md`, §3 there); checked: `C2FINAL/README.md` §2 and §6 use records with both verdicts
   (lines 1406-1408).
5. Corollary `cb:cor:roots`: "(using the computer-assisted Facts …)" replaced by the uniform label "(Computer-assisted:
   the proof uses Facts …)" (line 1087; part of finding 4).
6. Corollary `cb:cor:c2`, proof: the last step now cites Definition `cb:def:c2refl` (refl(a,V) = map(ρ_a,V) on entries
   in I_a) instead of re-deriving the residue (lines 1395-1397; follows from finding 3).
7. Remark `cb:rem:keys`: avoided the word "proved" for a Lean proof ("whose Lean proof is decide +kernel").
8. Map TSV notes updated (no row added, removed or retitled; kinds, names and lines unchanged): `cb:def:certsN`
   (423-1711), `cb:lem:all-checked`, `cb:fact:refl-h3`, `cb:fact:refl-h6`, `cb:fact:topcases`, `cb:fact:strata`,
   `cb:fact:roots-match`, `cb:cor:roots`, `cb:thm:c3` (also "certificates' own"), `cb:thm:c2-refl`, `cb:cor:c2`.
   The six fact/theorem rows keep "Lean-checked" and add "computer-assisted in Lean (decide +kernel)". A script
   compared all 100 rows with the statement heads (label, kind, Lean names, file:line, order): 0 mismatches, 5 columns
   each.

No proof that passed was weakened or restructured; no label was added, removed or renamed (112 labels, all `cb:`, no
duplicates; export labels `cb:lem:run`, `cb:thm:c3`, `cb:thm:c2` each defined once on the same statements). No
statement body begins with a list. Every edited Lean-referenced statement was compared again with its declaration
(`run_sound`, `checkRoot_sound`, `all_checked`, `reflection_facts_*`, `topCases_eq`, `strata`, `roots_match`,
`all_roots_covered`, `subcases_reflection`, `closed_are_subcases`): only labels and local symbol names changed; the
mathematical content, hypotheses, quantifier order and the truncated subtractions are as before.

## Compile check

`build/cb_wrapper.tex` (inputs `../preamble` and `../sections/cb`), run twice from `build/` with
`nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error cb_wrapper.tex`: both passes exit 0, 17 pages, no errors,
no "Missing $", no multiply defined labels. The only undefined reference is `sr:def:classes` (input lines 11 and 21),
an export label of section `sr`. Overfull boxes: 0 (none of any size). Remaining warnings: one underfull `\vbox` during
output and three underfull `\hbox` in statement heads (input lines 578-579, 1116-1119, 1351-1352: the heads of
`cb:lem:run`, `cb:thm:c3`, `cb:fact:c2-sub`); the three heads were inspected in the rendered pages and read normally.
No machine path and no tool name occurs in `cb.tex` or `cb.map.tsv` (checked by search).
