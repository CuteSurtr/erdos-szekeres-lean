# Diff audit of section `cb`, round doc-r0

Compared, with `diff -u`: `snapshots/doc-r0-pre/cb.tex` and `cb.map.tsv` against `sections/cb.tex` (1,486 lines) and
`sections/cb.map.tsv`. Fix log: `reviews/cb-doc-r0-fix.md`. Notes it addressed: `reviews/cb-p1-diff.md` (m1) and
`reviews/cb-p1-referee.md` (F1, F2, F3), as listed under key `cb` in `build/open_minors.json`. Paths are relative to
the staging area or to RES (`cloud/es7-2026-10-19/results`).

**Verdict: PASS.** No blocker and no major finding. There is one minor finding: the forward reference to the new
section `sa` (§4). The `.tex` diff has four hunks and the map is byte-identical. Every factual claim in the hunks was
checked against the Lean files and the records under RES. All four notes are fixed, and none was declined. My own
wrapper compiles with exit 0, with no error and no overfull box.

## 1. The `.tex` hunks

1. **Sources paragraph** (`cb.tex:51-56`; note m1). Every new line range was checked against
   `C3LEAN/C3Cover.lean` (2,327 lines, SHA-256 `4b64293df2ea…`, confirmed):
   - auxiliary definitions: `beqLayer` 335 to the end of `reflectionFacts` 365;
   - "facts about the roots", lines 367-409: `reflection_facts_H3` 367 to the `decide +kernel` of `strata` at 409;
   - "facts about the roots", lines 1720-1733: `roots_match` 1720, `roots_codes_match` 1725, and `roots_eq_tsv`
     1730-1733;
   - data: `tsvRootCodes` 413, `certs0` … `certs126` 423-1711, `certs` 1714, `bounds` 1717 and `certifiedKeys` 1737;
   - batch theorems: `batch0` 1740 to `batch126` 2244-2245 (127 theorems);
   - `all_checked` 2247; `all_roots_covered` 2251;
   - controls: `control_missing_record` 2266 to the end of `control_phi_mutant` 2297;
   - `end C3Cover` 2299 and `#print axioms` 2301-2327.

   A scan of all top-level declarations in lines 330-2299 finds none outside this inventory. `all_checked` is now
   named, so m1 is fixed. The ranges agree with the heads of `cb:lem:all-checked` (2247) and `cb:thm:c3` (2251) and
   with the Coverage list of the controls.
2. **Rigor paragraph** (`cb.tex:89-94`; note F1). It now reads "Each Lean declaration of the two files other than the
   seven negative controls of `C3LEAN/C3Cover.lean` (tests, listed in §`cb:sec:coverage`), or each uniform family
   …, has a statement below whose head carries its Lean reference".
   - A script extracted all top-level declarations of the two files: 336 in `C3Cover.lean` and 20 in
     `Central34Orbits.lean`. It also extracted every `\leanref` in the 100 statement heads of `cb.tex` (81
     references), counting a family member only when the head cites its first member (`certs0`, `batch0`,
     `reflection_facts_H6_1_0`, `closedP1`).
   - Exactly seven declarations have no head reference: the seven controls at lines 2266, 2270, 2274, 2278, 2282,
     2286 and 2292.
   - Every `\leanref` names an existing declaration, and its cited line contains that name.
   - The claim is therefore exact. Coverage lists the controls as "tests, not results".
   - Replacing "of the scope" by "of the two files" is right. The prelude, control and review files listed under "Not
     covered, deliberately" also contain declarations without statements.
3. **Paragraph after Fact `cb:fact:batches`** (`cb.tex:745-751`; note F2). I recounted the claims from the data with
   my own parser of lines 423-1711:
   - 910 certificates;
   - 554 with `ds` written as the numeral `0`, and 554 with value 0;
   - each of these 554 has exactly one key under `unpack` (base 2^64, stop at 0);
   - totals: 73,567 keys, 942 layer digits and 1,747 σ digits (76,256 nodes), as in `C3LEAN/c3cover_summary.json`.

   The mathematics is right. By `run` (`C3Cover.lean:262-275`), when ds = 0 the root is popped as a leaf, the single
   key is consumed, and the empty stack then requires ds/16 = 0 and no keys left. So these certificates name exactly
   one leaf, and Fact `cb:fact:batches` makes that leaf the root. Conversely, a passing certificate whose root is a
   leaf must have ds = 0.

   The claim that no project record states the number was checked by searching for the word 554:
   - in the text records (`*.md`, `*.txt`, `*.json`, `*.tex`, `*.log`, `*.py`) of all of RES;
   - in the TSV files of the `C3*` directories and `WRITEUP`.

   The hits are hashes, solver statistics, unrelated table cells and `A2/data/ctl_nb_r3.json` ("SAT": 554, another
   experiment). None states the number of single-leaf certificates. A search for "only leaf", "single leaf",
   "certified directly" and "root itself" finds nothing about C3 roots either. The notation agrees with Definitions
   `cb:def:cert` and `cb:def:keys`: c.ds and keys(c) = unpack(100000, c.ks). The new sentence lowers the rigor label
   ("not a Lean statement"); it does not raise it.
4. **Remark `cb:rem:use`** (`cb.tex:1152-1153`; note F2). The remark now reads "(our count from the certificate
   data; see the paragraph after Fact~`cb:fact:batches`)". This points to the paragraph of hunk 3. The rest of the
   remark is unchanged. It is commentary with no Lean declaration; its map note is still accurate.
5. **Coverage, new paragraph "Treated in another section."** (`cb.tex:1482-1486`; note F3).
   - All three files exist, and their headers support the parenthetical descriptions:
     - `AUDIT3/A1_reduction/SizeArith.lean` (20 theorems; lines 1-2: "the size arithmetic of the symmetric ES(7)
       reduction");
     - `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean` (7 theorems and one control `example`; line 1:
       "Size bookkeeping for the assembled symmetric theorem");
     - `ES7SPLIT/review/equivalence/BaekSeven.lean` (`baek_seven`; lines 3-4: "Instantiation of the ported Baek
       (ETV a = 4) theorem at n = 7: 17 points (in an abstract configuration)"). The statement is about an arbitrary
       `Config γ`, so "an instance of Baek's theorem for abstract configurations" is accurate.
   - "Lean-checked" is supported by the logs `SizeArith.lean.log`, `AssembledSizes.lean.log` (one unused-variable
     linter warning) and `BaekSeven.out`. All three logs print axioms within {propext, Classical.choice, Quot.sound}.
     It is also supported by `AUDIT3/reports/A1_reduction.md` (trust row 4; lines 106 and 262) and by
     `ES7SPLIT/README.md:76`.
   - The "symmetric k = 7 theorem to its case classes" phrasing matches the T_C3/T_C5/T_C4/T_C2/T_M34/T_M33 targets
     of `SizeArith.lean`.
   - Whether Section `sa` treats these files cannot be checked yet: see finding m1 in §4.

## 2. The `.map.tsv`

The file is unchanged (empty diff). A script matched the 100 statement environments to the 100 rows by label and
kind, with 0 mismatches. The only statement environment touched, Remark `cb:rem:use`, has the row
`cb:rem:use remark - - commentary; …`, which still fits. No statement that corresponds to a Lean declaration was
edited. The Lean source behind the touched remark was re-read: `all_roots_covered`, 2251-2261, and the certificate
data.

## 3. The fixer's dispositions

| note | disposition | audit |
|---|---|---|
| m1 (diff) | fixed | Correct; hunk 1. All line ranges are exact. |
| F1 (referee) | fixed | Correct; hunk 2. Checked by script: exactly the seven controls have no head reference. |
| F2 (referee) | fixed | Correct; hunks 3-4. 554 single-leaf certificates were recounted, and no record states the number. |
| F3 (referee) | fixed, as instructed by the orchestrator | Correct as far as it can be checked now; it depends on section `sa` (m1 below). |

No note was declined. The fix log's other statements also hold:
- labels: 112, all `cb:`, distinct, and the same as the snapshot in set and order;
- the counts of "verified", "certified" and "proved" are unchanged at 0, 15 and 3;
- 15 source lines exceed 122 characters, both before and after.

## 4. Findings

**m1 (minor; touched hunk 5, `cb.tex:1482-1486`).** The paragraph says the three files "are treated in
Section~\ref{sa:sec}". This cannot be checked at audit time:
- `sections/sa.tex` does not exist yet;
- no other section mentions the three files;
- `sa:sec` is undefined in the standalone build;
- `sa:sec` is not an export label in `CONTRACT.md`. It is the contract-mandated `<key>:sec` label of the section this
  run adds, and this round's instructions allow `sa:` labels.

The risk is specific to `BaekSeven.lean`. The announced topic of `sa` is the size arithmetic of the symmetric k = 7
reduction, and `baek_seven` is not size arithmetic: it instantiates the vendored abstract Baek theorem. If `sa` does
not state and prove `baek_seven`, the sentence becomes a false coverage claim for that file.

*Fix:* when `sa.tex` lands, confirm three things:
- it defines `\label{sa:sec}`;
- it covers the 20 theorems of `SizeArith.lean`, the 7 theorems of `AssembledSizes.lean` (and its control
  `example`) and `baek_seven`;
- the full document resolves `sa:sec`.

If `baek_seven` goes elsewhere or is not treated, reword the sentence for that file and give the reason.

No overfull boxes, so no box findings.

## 5. Compile check (own wrapper)

- `build/cb_docr0audit_wrapper.tex` uses the contract's wrapper text. It inputs `../preamble` and `../sections/cb`.
- I ran `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice from `build/`. Both passes exit 0.
- The PDF has 17 pages: no `!` error, no "Missing $", no multiply defined label, and **no overfull box** of any size.
- The only undefined references are `sr:def:classes` (input lines 11 and 21; an allowed export label of `sr`) and
  `sa:sec` (input line 1486; the new section).
- Remaining warnings: one underfull `\vbox` during output and three underfull `\hbox` (badness 3364, 2671 and 4582).
  These are the heads of `cb:lem:run`, `cb:thm:c3` and `cb:fact:c2-sub`, and they are unchanged from earlier rounds.
- The fresh aux file made pass 2 print "Label(s) may have changed". A third pass settles: no rerun warning and still
  no overfull box.
- `pdftotext` and rendered pages 2 and 17 show the four edited passages:
  - "§1.11" in the Rigor paragraph;
  - "Fact 1.65" in the remark;
  - the new Coverage paragraph, whose `\dirn` path breaks cleanly after `AUDIT3/A1_`.
- Mechanical checks of `cb.tex` and `cb.map.tsv`:
  - no machine path and no tool name;
  - no `\newcommand`, `\def`, `\usepackage` or `\sloppy`;
  - the only references outside `cb:` are to `sr:def:classes` and `sa:sec`.

## 6. Notes (not findings)

- In hunk 2, a comma before "other than" would block the misreading "the two files other than the seven negative
  controls". The intended reading is the only sensible one.
- In hunk 5, the parenthetical "(the size arithmetic of the reduction …)" leaves out the second part of
  `SizeArith.lean`, the upper bounds of the size table given the case theorems. As a one-line description, this is
  acceptable.
- In hunk 3, "the certificate c" means the certificate of the root. This is clear from the preceding sentence, and
  `roots_codes_match` gives the one-to-one correspondence in order.
