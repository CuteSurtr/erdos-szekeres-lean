# Diff audit of section `cb`, polish round 1

Compared: `snapshots/sections-r1pass/cb.tex` and `cb.map.tsv` (the version that passed the four-lens review; byte-identical
to `snapshots/polish-r1-pre/`) against `sections/cb.tex` (1,475 lines; 1,440 before) and `sections/cb.map.tsv`
(100 rows plus header in both). Fixer log: `reviews/cb-polish-r1-fix.md`. Round-1 reports read in full:
`reviews/cb-r1-fidelity.md`, `cb-r1-rigor.md`, `cb-r1-adversarial.md`, `cb-r1-claims.md` and `cb-writer-concerns.md`.
No earlier polish audit (`cb-p*-diff.md`, `cb-p*-referee.md`) exists. Paths below are relative to the staging area or
to the results directory `RES`.

**Verdict: PASS.** No blocker and no major finding; one minor finding (§5). Every hunk was checked against the Lean
source and the cited records. Every fix the fixer marked "fixed" is correct, and both "declined" items are acceptable.
My own wrapper compiles with exit 0 and has no overfull box.

## 1. The `.tex` hunks, one by one

1. **Overview, item (1)** (lines 14-18). It now says that the proof also uses Fact `cb:fact:roots-codes`
   (computer-assisted) and Fact `cb:fact:roots-match` (with a written proof). Checked against the Lean proof of
   `all_roots_covered` (`C3LEAN/C3Cover.lean:2251-2261`), which uses `roots_match` (`hrt`), `roots_codes_match`
   (`hmap`), `all_checked`, `checkRoot_sound`, `beqList_eq`, `beqNode_eq` and `Covered.mono`. Correct.
2. **Overview, item (2)** (lines 22-23). "The reflection that sends i to the residue of a−i modulo 17". This equals
   `Central34.refl` (`(a + 17 - i) % 17`, line 40) on `{0,…,16}`. Correct.
3. **Sources paragraph** (lines 52-55). `beqLayer` 335, `isOption` 340, `distinctCodes` 346, `codeSet` 351 and
   `reflectionFacts` 356, with the tuple ending at line 365, so "lines 335--365" is exact. There are seven negative
   controls, at 2266, 2270, 2274, 2278, 2282, 2286 and 2292. Correct, but see minor finding m1 (`all_checked` is still
   not named).
4. **Rigor labels and dependencies** (lines 80-94).
   - Every statement whose Lean proof is `decide +kernel` now carries "(Computer-assisted …)" in its statement:
     Facts `batches`, `refl-h3`, `refl-h6`, `topcases`, `strata`, `roots-match`, `roots-codes`, `roots-tsv` and
     `c2-sub`, and Theorems `c2-refl` and `c2`.
   - "Every statement whose proof uses one of the computer-assisted statements on generated data" is exactly the four
     statements listed. I located every `\ref` to Facts `batches`, `roots-codes`, `roots-tsv` and `c2-sub`, to Theorem
     `c2` and, transitively, to `all-checked`, `cor:roots`, `thm:c3` and `cor:c2`. The only proofs among them are the
     proofs of `cb:lem:all-checked`, `cb:cor:roots`, `cb:thm:c3` and `cb:cor:c2`; the other hits are in remarks,
     commentary and Coverage.
   - "Facts `refl-h3` to `roots-match`" renders as Facts 1.67 to 1.71, five consecutive facts. Each names its written
     proof (Proposition `cb:prop:refl` or `cb:prop:roots-match`; "written proof below" for `cb:thm:c2-refl`).
   - The family sentence and the two-declaration head of `cb:lem:run` are accurate.
5. **Notation** (lines 100-101). The least nonnegative residue is defined for integer x, and it agrees with the
   remainder for x ∈ ℕ. Correct.
6. **Opening of §cb:sec:model** (lines 155-157) and **opening of §cb:sec:c2** (lines 1183-1184). By script, all 68
   `\leanref`s in lines 153-1180 are `C3Cover.*` / `C3LEAN/C3Cover.lean:*`, and all 13 in lines 1181-1416 are
   `Central34.*` / `C2FINAL/Central34Orbits.lean:*`. Every other statement head in these ranges is tagged
   "written step". Correct.
7. **Remark `cb:rem:reading`** (lines 188-190). "Used for a layer of one orbit other than the top layer (the one-orbit
   top layer [(0,0)] carries s=0)". This agrees with the docstring at `C3Cover.lean:36-37` ("a one-orbit layer below
   the top carries no σ"), with `topCases` (`[(0,0)]`) and with `layerOptions` (singletons `[(r,2)]`). Correct.
8. **Remark `cb:rem:keys`** (lines 423-425).
   - `C3LEAN/review/RevCtrl_pass.lean:315` is `theorem rev_parent_decodes … := by decide +kernel`, inside
     `namespace C3Cover` (lines 1 and 317).
   - `C3LEAN/review/logs/revctrl_pass.log` prints the axioms of the other two theorems only, and ends with
     "guard: exit 0".
   - The wording no longer calls the theorem "Lean-checked", so the label is rounded down, not up.
9. **Remark `cb:rem:cert`** (lines 567-568). "A σ-split on the K smallest free residues of n (K σ bits, 2^K
   children)". This matches `Node.sigmaChildren` (`take K free`, `range (2^K)`, lines 127-129). `free` is filtered
   from `range 11`, so it is increasing, and `run` requires `K ≤ |free n|`. Correct.
10. **Head of Lemma `cb:lem:run`** (line 577). The plain contract form is used, with `run_sound` at 279 and
    `checkRoot_sound` at 323 (exact). In the PDF (page 7) the head is on the lemma line. There is no overfull box, and
    one underfull line (stretched spaces) reads normally.
11. **Definition `cb:def:certsN`** (line 648). "Lines 423--1711": `certs0` is at 423, `certs126` at 1668, and line 1711
    closes `certs126`. Exact.
12. **Lemma `cb:lem:all-checked`**, Facts `refl-h3`, `refl-h6`, `topcases`, `strata` and `roots-match`, Corollary
    `cb:cor:roots`, Theorem `cb:thm:c3`, Theorem `cb:thm:c2-refl`, Fact `cb:fact:c2-sub` and Corollary `cb:cor:c2`.
    These received only a label sentence, and for `cb:thm:c2-refl` also renamed predicates. I re-read each Lean
    declaration:
    - `all_checked` 2247;
    - `reflection_facts_H3` 367 and `reflection_facts_H6_*` 370-397;
    - `topCases_eq` 401 and `strata` 406;
    - `roots_match` 1720 and `all_roots_covered` 2251;
    - `subcases_reflection` 273 and `closed_are_subcases` 284.

    Hypotheses, conclusions and quantifier order are unchanged and still exact. The renaming `B_a(V)` → `Inv_a(V)`
    (with `A_a` → `Img_a`) matches the two conjuncts at `Central34Orbits.lean:278`. `B_a` now means only
    `bitset(closedP_a)`.
13. **Proposition `cb:prop:refl`, statement** (lines 984-987). The involution r* is now defined in the statement. A
    short literal transcription of `layerOptions`, `pairOptions`, `insTok`, `sortTok`, `mirror`, `phi` and `refl` (Lean
    truncated subtraction) gives the following for all 11 top cases:
    - the fixed points are exactly the listed layers: 10 for H3, and for each H6(a,s) the layer `[(r0,2)]` plus the
      eight layers `[(b,σ),(b*,σ⊕f_b)]`;
    - in every H6 case exactly four b ∈ R satisfy b < b*;
    - the case formula for r* agrees with `((a+11)∸r) mod 11` on R;
    - r0 is 6, 1, 7, 2, 8;
    - |O|, F and the kept counts are 190, 10, 100 and 153, 9, 81.

    0 mismatches. The proof (lines 1014-1015) now refers to the statement's r*, and the argument is unchanged.
14. **Remark `cb:rem:use`**.
    - (a) The lrat-check sentence (lines 1155-1158) quotes the source faithfully. `WRITEUP/note/symmetric_extremal.tex`
      runs from "Acceptance by" (line 111) to "supporting only" (line 114). `LRATCHECK20261105` exists.
      `WRITEUP/SYMMETRIC.md` §3 ("Trust base", line 202) says that only cake_lpr is trusted and that "where this
      section says 'both checkers', the certificate is the cake_lpr verdict". `C3LEAN/README.md` §4 confirms that a
      certified record carries both verdicts and that the proofs were not kept.
    - (b) "Are not roots of the file, so Theorem `cb:thm:c3` says nothing about them" (lines 1171-1172). This holds by
      Definition `cb:def:roots` and agrees with `C3LEAN/README.md` §6.
    - (c) The added pointers (lines 1176-1178) are accurate. `C3LEAN/README.md` §6 is "What is not checked" and gives
      a status for each part. Theorem 1 of `WRITEUP/SYMMETRIC.md` is the threefold theorem, and §3 is its trust base.
15. **Commentary after Theorem `cb:thm:c2`** (lines 1377-1379). Lean's `||` evaluates its second argument only when
    the first is `false`, so "the second bit is needed only when the first is 0" is correct.
16. **Corollary `cb:cor:c2`** (lines 1384-1398).
    - ρ_a is now ((a+17)∸i) mod 17 on {0,…,16}. This is the same map as in the proof of `cb:thm:c2-refl` and as
      `Central34.refl`.
    - T ⊆ I_a ⊆ {0,…,16}, so ρ_a(T) is defined.
    - The proof's last step (`refl(a,V) = map(ρ_a, V)` by Definition `cb:def:c2refl`, with the entries of V in I_a)
      is correct.
17. **Remark `cb:rem:c2-scope`** (lines 1406-1408).
    - The file header (`C2FINAL/Central34Orbits.lean:11`) and `C2FINAL/README.md` §2 and Status state that the records
      carry both verdicts, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.
    - Theorem 4 of `WRITEUP/SYMMETRIC.md` is the half-turn (central) theorem.
    - Correct.
18. **Coverage** (lines 1419-1420, 1444, 1473).
    - "Covered by a definition above (the generated family … by a single one)" and "(by a single definition)" are
      accurate.
    - `C3LEAN/review/RevDiff.lean` (620 lines) has no `theorem`, `lemma` or `example` after line 301, so "without
      theorems of its own" is correct.

## 2. The `.map.tsv` hunks

Eleven notes changed. The kinds, Lean names, file:line fields and the row order are unchanged.
- Each note agrees with the statement it describes, and with `C3LEAN/logs/compile.log`:
  - `reflection_facts_H3` and `reflection_facts_H6_1_0` depend on `[propext]`;
  - `topCases_eq`, `strata` and `roots_match` depend on no axioms;
  - `all_checked` depends on `[propext]`;
  - `all_roots_covered` depends on `[propext, Quot.sound]`.
- `cb:def:certsN` now says 423-1711. This is exact.
- By script: 100 statement environments and 100 rows, 5 columns each, 0 mismatches in label, kind, Lean names and
  file:line. No "written step" head carries a `\leanref`.

## 3. The fixer's dispositions

All 20 rows of the fix log were checked against the four reports and the writer concerns. Every round-1 finding is
accounted for:
- fidelity #1-#7, and its non-finding 3;
- rigor m1-m7, and its unsure points 1-3;
- adversarial 1-6;
- claims M1-M11, and its non-finding 3.

| fix-log rows | disposition | audit |
|---|---|---|
| 1-17 | fixed | Each is fixed correctly; evidence is in §1, items as follows: row 1 → item 10; row 2 → item 9; row 3 → items 2, 5 and 16; row 4 → items 4 and 12; row 5 → item 4; row 6 → item 14(a); row 7 → item 1; row 8 → items 12 and 16; row 9 → item 13; row 10 → item 18; row 11 → item 6; row 12 → item 14(b); row 13 → item 3; row 14 → item 7; row 15 → item 11; row 16 → item 8; row 17 → item 15. "Other changes" 1-8 were also checked and are correct. |
| 18 | declined | Acceptable. The Central34 "Lean-checked" label rests on `C2FINAL/README.md` §6, and the section says so in the Axioms paragraph and in the map notes. No Central34 log exists. Not an inaccuracy. |
| 19 | declined | Acceptable. The meanings of `Nat.lor`, `<<<` and `Nat.testBit` are definitions or basic facts of core Lean, stated accurately. |
| 20 | n/a | No overfull boxes were listed, and none occur. |

## 4. Compile check (own wrapper)

- `build/cb_p1diff_wrapper.tex` has the contract's content. It was run twice from `build/` with
  `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
- Both passes exit 0. The PDF has 17 pages.
- No `!` errors, no "Missing $", no multiply defined labels and **no overfull boxes** (of any size).
- The only undefined reference is `sr:def:classes`, on input lines 11 and 21. It is an allowed export label of section
  `sr`.
- Remaining warnings:
  - one underfull `\vbox` during output;
  - three underfull `\hbox` (badness 3364, 2671 and 4582) in the heads of `cb:lem:run`, `cb:thm:c3` and
    `cb:fact:c2-sub`. I looked at the rendered pages 7, 13 and 15: each head sits on its statement line and reads
    normally.
- Pass 2 printed "Label(s) may have changed". A third pass settles: that warning is gone and there is still no
  overfull box.
- Other pages looked at: 2, 11 and 16 (the Rigor paragraph, Proposition `cb:prop:refl` and Corollary `cb:cor:c2`).

## 5. Other checks and findings

Mechanical checks on both files:
- no machine path and no tool name in `cb.tex` or `cb.map.tsv`;
- no `\newcommand`, `\def`, `\usepackage`, `\input` or `\sloppy`;
- 112 labels, all `cb:`, distinct, the same set and order as the snapshot;
- every export label is defined once;
- the only out-of-section `\ref` is `sr:def:classes`;
- the number of occurrences of "verified", "certified" and "proved" is unchanged (17 before and after), and none of
  the new sentences adds one;
- the three new uses of "certificate" (lines 1156, 1158 and 1407) are attributed to the project's records.

**m1 (minor, imprecision; touched hunk).** `sections/cb.tex:52-55`, Sources paragraph.
- The sentence now reads as an inventory of lines 330-2299: auxiliary definitions, facts about the roots, data, batch
  theorems, the main theorem and seven controls, with exact ranges and counts.
- It still omits `all_checked` (`C3LEAN/C3Cover.lean:2247`), which is neither a batch theorem nor the main theorem.
- Suggested fix: "…, the batch theorems and \lean{all_checked}, the main theorem and seven negative controls".

## 6. Notes (not findings)

- The Rigor paragraph says that for a family "the statement locates the others". For `certs1`-`certs125`,
  Definition `cb:def:certsN` gives only the block 423-1711 and the line of `certs126`; this is adequate.
- Corollary `cb:cor:c2` now says "(Computer-assisted: a consequence of Theorem …)", and its proof still opens with
  "This is a consequence of Theorem …". The repetition is harmless.
