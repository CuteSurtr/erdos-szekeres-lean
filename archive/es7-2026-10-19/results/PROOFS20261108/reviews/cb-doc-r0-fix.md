# Fix log: section `cb`, round doc-r0

Inputs: the four notes under key "cb" of `build/open_minors.json` (from `reviews/cb-p1-diff.md`, m1, and
`reviews/cb-p1-referee.md`, F1-F3). Snapshot taken before editing: `snapshots/doc-r0-pre/cb.tex` and `cb.map.tsv`.
Paths are relative to the staging area or to RES (`cloud/es7-2026-10-19/results`). Line numbers of `cb.tex` refer to
the file after this round.

| # | lens | note (summary) | action | location | reason / evidence |
|---|---|---|---|---|---|
| 1 | diff (m1) | Sources paragraph: the inventory of lines 330-2299 of `C3LEAN/C3Cover.lean` omits `all_checked` (line 2247), which is neither a batch theorem nor the main theorem | fixed | `cb.tex:52-56` | Re-read `C3Cover.lean` 325-412, 1709-1745 and 2240-2299. Added "the theorem `all_checked` (line 2247)". Since the sentence is an inventory, the other items now carry their line ranges too, each checked against the file: facts about the roots 367-409 (`reflection_facts_H3` ... end of `strata`) and 1720-1733 (`roots_match` ... end of `roots_eq_tsv`); batch theorems 1740-2245 (`batch0` at 1740, `batch126` at 2244-2245); main theorem 2251; negative controls 2266-2297 (`control_missing_record` ... end of `control_phi_mutant`). "Facts about the roots" is the section's own name for these (subsection `cb:sec:written`). |
| 2 | referee (F1) | Rigor paragraph: "each Lean declaration of the scope ... has a statement below" is false for the seven negative controls | fixed | `cb.tex:89-91` | Now: "Each Lean declaration of the two files other than the seven negative controls of `C3LEAN/C3Cover.lean` (tests, listed in §`cb:sec:coverage`), or each uniform family ...". "Of the scope" became "of the two files" (the files named in the Overview), because the review and control files listed in Coverage also contain declarations without statements, so "scope" alone would still overstate. Checked by script: of the 336 top-level declarations of `C3Cover.lean` and the 20 of `Central34Orbits.lean`, exactly the seven controls (lines 2266-2292) have no map row, directly or through a family. |
| 3 | referee (F2) | "554 of the 910 roots" (certificates with ds = 0) is the document's own count; Remark `cb:rem:use` cites Fact `cb:fact:batches` for it, but that Fact does not state it | fixed | `cb.tex:747-751` and `1152-1153` | Recounted from `certs0` ... `certs126` (`C3Cover.lean` 423-1711): 910 certificates; 554 have ds written as the numeral 0 (554 with value 0), and each of them has exactly one key under `unpack` (base 2^64, stop at 0). Totals 73,567 keys, 942 layer digits and 1,747 σ digits agree with `C3LEAN/c3cover_summary.json`. A search for the word 554 in `C3LEAN`, `C3FINAL`, `C3U2`, `C3H6M` and `C3-S` finds only an unrelated "1,554" (a `C3U2` README table) and one log line, so no record states the count. The paragraph after the Fact now says that the number is our own count from the certificate data of `C3LEAN/C3Cover.lean`, is not a Lean statement, and is stated by no project record; the remark now reads "(our count from the certificate data; see the paragraph after Fact~\ref{cb:fact:batches})". In the same sentence the certificate is made explicit ($c.\mathsf{ds}$, the notation of Definition `cb:def:cert`) and "keys(c) has one entry" is added (verified above). |
| 4 | referee (F3) | Three Lean-checked files of the inventory unit C3-C2-misc (`AUDIT3/A1_reduction/SizeArith.lean`, `AUDIT3/A1_reduction/verify_A1-F1/AssembledSizes.lean`, `ES7SPLIT/review/equivalence/BaekSeven.lean`) are covered and mentioned nowhere | fixed (as instructed by the orchestrator) | `cb.tex:1482-1486` | New closing paragraph of Coverage, "Treated in another section.", one sentence: the three files are outside the scope of this section and are treated in Section~\ref{sa:sec}. Short neutral descriptions are taken from the file headers (`SizeArith.lean` lines 1-2 "the size arithmetic of the symmetric ES(7) reduction"; `AssembledSizes.lean` line 1; `BaekSeven.lean` lines 3-4 "Instantiation of the ported Baek ... theorem at n = 7"). It is a separate paragraph, not an item of "Not covered, deliberately", because the files are covered elsewhere. The document does not use the word "inventory" (no section does). `sa:sec` is not in the contract's export table; it is referenced on the orchestrator's instruction (new section `sa`), and it is undefined in the standalone check, as expected. |

No note was declined.

## Other changes

None besides the four notes (the source re-wrap of the edited paragraph after Fact `cb:fact:batches` is cosmetic).
The map `cb.map.tsv` is unchanged and still in sync: no statement environment, label, kind, Lean name or file:line
changed (by script: 100 statement environments, 100 rows, same labels and kinds in the same order). The only
statement environment touched is Remark `cb:rem:use`, and its map note ("commentary; scope and intended use ...")
remains accurate. No statement that corresponds to a Lean declaration was edited.

## Checks

- Compile: `build/cb_wrapper.tex`, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`, twice from
  `build/`: exit 0 on both passes; no errors; no overfull box of any size (so 0 above 1pt); no "Missing $"; no
  multiply defined label; no rerun warning after pass 2; 17 pages. Undefined references: `sr:def:classes` (export
  label of `sr`) and `sa:sec` (new section `sa`) only. The three underfull hboxes (heads of `cb:lem:run`,
  `cb:thm:c3`, `cb:fact:c2-sub`) existed before this round.
- Rendering of the four edited passages checked with `pdftotext`.
- Labels: 112, all `cb:`, distinct, same set and order as the snapshot; every `cb:` reference resolves.
- Wording: the counts of "verified", "certified" and "proved" are unchanged (0, 15, 3); no new uses.
- No machine path, no tool name, no `\newcommand`/`\def`/`\usepackage`/`\sloppy` in `cb.tex` or
  `cb.map.tsv`; the number of source lines longer than 122 characters is unchanged (15, all pre-existing).
