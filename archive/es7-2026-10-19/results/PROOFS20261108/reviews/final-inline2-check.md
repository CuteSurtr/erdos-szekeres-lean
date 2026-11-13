# Final inline edits, round 2: independent check (lens: inline2)

Verdict: **pass**. All six edits of `build/final-inline2.diff` are true when checked against the Lean files and records
in REPO (commit `7e32ee259`). Every Lean name in them is correct, every `\ref` obeys the label rule, the edits agree with
the other places in the document that say the same thing, and the edited passages render cleanly. There is no blocker and
no major finding. The two minor findings are optional wording points in the sa hunk. One of them is older than this
diff.

Paths: section files are relative to STAGE, Lean files and records to RES. Line numbers refer to the current files.
Statement numbers come from `build/inline-check2/proofs.pdf` (188 pages). Under STAGE I wrote only this report and an
independent rebuild in `build/inline2-verify/`. Nothing under REPO was edited. Lean, lake and solvers were not run.
Two short Python text checks were run from a directory outside STAGE. Their criteria are given below.

## Findings

| # | severity | location | issue | fix |
|---|---|---|---|---|
| 1 | minor (optional; older than this diff) | sections/sa.tex:521 (first line of the sa hunk) | The edited sentence now gives `\lean{SymReduction.case_fourfold}`, `\lean{SymReduction.VariantChecks.group_form}`, `\lean{LayerLemma.Fourfold32}` and `\lean{LayerLemma.fourfold_heptagon_of_erase}` in the form that fd.tex:40-42 allows (only `ErdosSzekeres.` dropped). It still opens with the bare `\lean{Fourfold32}`. Read strictly by fd.tex:40-42, that name is `ErdosSzekeres.Fourfold32`, which does not exist; the class is `ErdosSzekeres.SymReduction.Fourfold32`. sa states no namespace convention of its own (compare sr.tex:114-119 and ar.tex:26), yet it writes the six class names bare 26 times (lines 446-593). The reader is not misled: "the class" and the contrast with "a same-text copy, `LayerLemma.Fourfold32`" identify the constant, and sa ties the class names to Definition 7.7 elsewhere (sa.tex:446, 508). Inside this one sentence, however, the naming is now mixed. | Either write `\lean{SymReduction.Fourfold32}` at sa.tex:521, or (better, since it covers all 26 uses) add one sentence to sa, for example before Remark `sa:rem:use`: "The names \lean{HalfTurn34}, \dots, \lean{Fourfold32} denote the propositions of Definition~\ref{sr:def:classes}, in the namespace \lean{ErdosSzekeres.SymReduction}." |
| 2 | minor (optional, wording) | sections/sa.tex:526 | "is the hypothesis of Theorem~\ref{ec:thm:fourfold} and of the form \lean{LayerLemma.fourfold_heptagon_of_erase} that its proof uses": the phrase "the form" never says which form is meant. ec calls this statement "fourfold, layer form" (ec.tex:215, Theorem 6.6), and so does the Lean docstring (`LEANEXT/es7corr/ES7Corollaries.lean:1201`, "**Fourfold, layer form.**"). The claim itself is true. | "... and of its layer form \lean{LayerLemma.fourfold_heptagon_of_erase}, which its proof uses". Add no `\ref`: `ec:thm:fourfold-erase` is not an export label. |

## The six edits, checked one by one

Each edit was checked for (1) its facts, (2) its Lean names, (3) its `\ref`s, (4) agreement with the rest of the
document and (5) rendering (pdftotext -layout and 110-dpi images of the PDF pages named).

### Edit 1: proofs.tex:52-53 (scope list)

Text: "\dirn{C3LEAN} and \dirn{C2FINAL} (the declarations of the latter are Lean-checked according to the record), in
Section~\ref{cb:sec};".

1. True. `C2FINAL` holds one Lean file, `C2FINAL/Central34Orbits.lean`: 298 lines, SHA-256 `b396a26b2430…` (recomputed).
   It has 17 definitions (`inner`, `choose2`, `choose3`, `subcases`, `mask`, `refl`, `bitset`, `uncovered`,
   `closedP1`-`closedP8`, `closed`), three theorems (:273, :284, :291) and three `#print axioms` lines (:296-298). I
   searched the whole checkout, excluding `.git` and `.lake`, for `Central34.all_cases_closed`, `closed_are_subcases`
   and `subcases_reflection`. The only hits are the Lean file and `C2FINAL/gen_lean.py`, so no Lean output exists. The
   git status of REPO is clean. This is the case of fd.tex:84-86. `C3LEAN/C3Cover.lean` has saved Lean output in
   `C3LEAN/logs/compile.log` (`#print axioms` lines for 27 declarations), so the plain label applies to it. The new
   wording attaches the qualifier to C2FINAL only, which fixes the reading that the earlier comma allowed.
2. No Lean names.
3. `\ref{cb:sec}` was already there. proofs.tex is the front matter, not a section file.
4. It agrees with cb.tex:83-84 and 86-89, with the appendix rows 498-500, and with ar.tex:745, mb.tex:1110,
   sr.tex:82-83 and sr.tex:268-269 (every place that labels a C2FINAL declaration uses the qualified label).
5. PDF p. 3: one bullet over two lines, clean.

### Edit 2: sr.tex:298-299 (Remark 7.8, item Fourfold32)

Text: "(among the statements of this section, a hypothesis only of Theorem~\ref{sr:thm:variant} and of
Lemma~\ref{sr:lem:fourfold}, which its proof uses)".

1. True. In `SYMLEAN/SymmetricReduction.lean`, `Fourfold32` occurs only at :30 (module docstring), :496 (the
   definition), :763 (`case_fourfold (h4 : Fourfold32)`) and :1025 (`halfTurn_of_symmetric_counterexample (h3)
   (h4 : Fourfold32) (h5) (hm1) (hm0)`). The Lean proof of the variant calls `case_fourfold h4 …` at :1042. The written
   proof of Theorem 7.41 uses Lemma 7.37 at sr.tex:1010. Among the 46 rows of sr.map.tsv, only `sr:lem:fourfold` (:38)
   and `sr:thm:variant` (:42) take the class. Definition 7.7 defines it. Remark `sr:rem:redundant` discusses one of its
   hypotheses. Remark 7.42 mentions the group form, but sr.tex:1035 says that the group form is not restated as a
   numbered statement. So "among the statements of this section ... only" is exact. The word "its" in "which its proof
   uses" can only mean Theorem 7.41's proof.
2. `\lean{Fourfold32}` is correct under sr's local convention (sr.tex:114-119: names relative to
   `ErdosSzekeres.SymReduction`).
3. `sr:thm:variant` (7.41) and `sr:lem:fourfold` (7.37) are sr's own labels.
4. It agrees with edit 3, with sr.tex:11-12 and 241-243, with Remark 7.42 (sr.tex:1036, "it uses Fourfold32"), with
   sr's Coverage (sr.tex:1141-1147) and with the appendix rows 292 and 296. The Lean docstring's "only used by the
   variant" (SymmetricReduction.lean:493) is no longer echoed anywhere. ec.tex:154-155 only reports what the docstring
   says, so it does not conflict.
5. PDF p. 82, clean.

### Edit 3: sa.tex:521-527 (Remark 12.13, item s = 4)

1. Every claim is true.
   - *"Among the reduction theorems and case lemmas stated in this document, only Theorem 7.41 and the case lemma
     `SymReduction.case_fourfold` that its proof uses take this class as a hypothesis."* I grepped all twelve sections
     and all twelve maps for statements whose hypotheses include `Fourfold32`. The only ones on
     `SymReduction.Fourfold32` are `sr:lem:fourfold` and `sr:thm:variant`.
     - The ar theorems take every class except `Fourfold32` (ar.tex:15).
     - The three-class theorems of mb take `HalfTurn34`, `Threefold33` and `Fivefold35`.
     - The copy of the variant in `SYMLEAN/mirror/ReductionThreeClasses.lean` is only mentioned, at mb.tex:1135-1136.
     - The copies in `SYMLEAN/AffineReduction.lean` are not restated (ar.tex:28-32).

     "Case lemmas" and "reduction theorems" are the titles of sr §7.7 and §7.8.
   - *"so do some checks of that theorem in the review file ..., among them its group form"*.
     `SYMLEAN/review/VariantChecks.lean` does not import SymmetricReduction.lean. Its lines 1-1058 are a copy of
     SymmetricReduction.lean:1-1058 (`diff` finds no difference), so its class has the same full name and the same
     text. In the review part after the banner:
     - `group_form` (:1168) takes `(h4 : Fourfold32)`;
     - `fourfold36_of_fourfold32` (:1220) takes `(h4 : Fourfold32)`;
     - `variant_unfolded` takes the class only in unfolded form;
     - `case_fourfold36` and `variant_with_fourfold36` take `Fourfold36`.

     So "some" and "among them" are exact.
   - *"a same-text copy, `LayerLemma.Fourfold32`, is the hypothesis of Theorem 6.7 and of ... that its proof uses"*.
     In `LEANEXT/es7corr/ES7Corollaries.lean`, lines :1161-1166 (docstring and definition) have the same text as
     SymmetricReduction.lean:493-498 (`diff` finds no difference). Two theorems of the file take the copy:
     `fourfold_heptagon_of_erase` (:1203) and `fourfold_heptagon` (:1216), both with `(H : Fourfold32)`. No other
     theorem of the file does. The proof of the latter calls the former in Lean (:1229) and in writing (ec.tex:238).
2. Every qualified name is correct.
   - `ErdosSzekeres.SymReduction.case_fourfold`: SymmetricReduction.lean opens the namespace at :54 and closes it at
     :1059.
   - `ErdosSzekeres.SymReduction.VariantChecks.group_form`: VariantChecks.lean opens the namespace
     `ErdosSzekeres.SymReduction.VariantChecks` at :1076 and closes it at :1301; `#print axioms` at :1304 uses the full
     name.
   - `ErdosSzekeres.LayerLemma.Fourfold32` and `.fourfold_heptagon_of_erase`: ES7Corollaries.lean has a single
     namespace, from :37 to :1233.

   The bare `\lean{Fourfold32}` is finding 1.
3. `sr:thm:variant` is an export label of sr, and `ec:thm:fourfold` one of ec. The lemma `sr:lem:fourfold` and the
   theorem `ec:thm:fourfold-erase` are not export labels, and the hunk correctly names them by their Lean names instead.
4. It agrees with edit 2, with ec.tex:154-156 ("the hypothesis of Theorems 6.6 and 6.7"), with ec's Coverage
   (ec.tex:886-891), with ec.map.tsv:7-8, sr.map.tsv:38, 42 and 43, and with sa's own item (5) (sa.tex:586-597). The
   appendix row of Remark 7.42 (from sr.map.tsv:43) writes `VariantChecks.group_form` under sr's convention. The
   appendix says that its notes are those of the section maps, so the two spellings name the same declaration (no
   finding).
5. PDF p. 156. The nested parentheses close correctly, and the bullet is clean. For the wording, see finding 2.

### Edit 4: ar.tex:746-747 (Remark on the classes, bullet "Exact computations")

Text: "that every leaf named by the keys of the certificates of Theorem~\ref{cb:thm:c3} and every subcase listed in the
data of Theorem~\ref{cb:thm:c2} has a record with the checker verdicts and a CNF hash equal to that of the rebuilt
formula is an exact computation outside Lean".

1. True, for both theorems. The 910 roots are no longer covered by the wording: a split root has no record of its own.
   - **C3.** The keys of the certificates name only leaves. `C3LEAN/README.md` §1 describes each certificate as its
     decision digits and "the keys of the leaves", and `certifiedKeys` is the list of those keys. The audit
     `C3LEAN/review/logs/indep_audit.json` records:
     - 73,567 leaves, all distinct;
     - `leaf_names_not_certified` 0;
     - `leaf_names_hash_checked` 73,567 and `leaf_records_hash_checked` 73,707;
     - `hash_mismatches` 0, against the base CNF `bf0e502e…`.

     `review/logs/audit_keys_orig.log` reports 73,567 keys and 0 failures. Both are Python computations
     (README §4).
   - **C2.** I recounted the data independently: the 2,297 entries of `closedP1`-`closedP8` (287 each, 288 for P6),
     parsed from the Lean file. The criterion was that of `C2FINAL/gen_lean.py`:15-32. A record qualifies if it has
     `status` UNSATISFIABLE, `lrat_check` "c VERIFIED", `cake_lpr` "s VERIFIED UNSAT" and a `cnf_sha256` listed under
     `matched` for its unit in `C2FINAL/hashmatch.json`. The records are those of `C2P*/*/out.jsonl` and
     `C2C34/logs/p8_units.tsv`. A re-solve record of `C2FINAL/pilot/out.jsonl` also qualifies if it has both verdicts
     and the hash under `computed_for_no_hash`.

     Result: 0 entries without a qualifying record. Six P8 entries rest only on a re-solve record (README §4), and that
     is also a record with both verdicts and the rebuilt hash, so the sentence holds as written.
2. No Lean names.
3. `cb:thm:c3` (11.82) and `cb:thm:c2` (11.98) are export labels of cb.
4. It agrees with cb.tex:36-43 (item (iii)), cb.tex:1161-1166 (Remark 11.83), cb.tex:1276-1280 (Remark
   `cb:rem:c2-reading`, "or a re-solve"), sr.tex:262-263 and 268-270, and mb.tex:1107-1117.
5. PDF p. 102, clean.

### Edit 5: cb.tex:62-63 (Sources and toolchain)

Text: "Both files are checked with Lean~4.24.0 according to their READMEs; for \dirn{C3LEAN/C3Cover.lean} a compile log
is saved, for \dirn{C2FINAL/Central34Orbits.lean} no Lean output (paragraph ``Axioms'' below)."

1. True.
   - `C3LEAN/README.md`:10 says "core Lean 4.24.0", and :227 says "Lean 4.24.0".
   - `C2FINAL/README.md`:153 says "Core Lean 4.24.0", and :249 says "Lean 4.24.0".
   - `C3LEAN/logs/compile.log` exists. It holds `#print axioms` output and resource lines but prints no version, so the
     version of both files rests on the READMEs, as the text now says.
   - `C3LEAN/C3Cover.lean` has the SHA-256 `4b64293df2ea…` that the README and cb.tex:51 give.
   - The `C2FINAL` directory holds no Lean output. The three files in `evidence/central34-cover/` are outputs of the SAT
     solver and of the two proof checkers for the hull cover.

   The pointer to the paragraph "Axioms" (cb.tex:70-84) is right.
2. No Lean names.
3. No `\ref`.
4. It agrees with fd.tex:46, ec.tex:41 and sa.tex:98, which also cite records for the toolchain, and with the
   paragraph "Axioms".
5. PDF p. 133, clean.

### Edit 6: cb.tex:83-84 and 88-89 (qualified label for the definitions)

1. True. "its three theorems and its definitions" covers every declaration of `Central34Orbits.lean`: the 17
   definitions and the three theorems listed under edit 1. The label follows from fd.tex:84-86 ("the label of its
   declarations") and fd.tex:115-118 (for a definition, the label records only that Lean accepted it). The appositive
   "the qualified label defined with the rigor labels ..." now attaches to the label. At 88-89, "as do its
   definitions" refers to `C2FINAL/Central34Orbits.lean`, the nearest antecedent.
2. No Lean names.
3. Only cb's own labels (`cb:thm:c2-refl`, `cb:fact:c2-sub`, `cb:thm:c2`), all already there.
4. I searched for "according to the record" in every section, map, proofs.tex and the appendix. No place gives the
   plain label to a C2FINAL declaration. The rows for the C2FINAL definitions (cb.map.tsv:85-94; appendix rows 486-495)
   say only "definition", as every definition row of every map does. The paragraph "Rigor labels and dependencies"
   does not mention the definitions of C3Cover; they are Lean-checked by fd.tex:115-118. This is unchanged and causes
   no conflict.
5. PDF p. 134, clean.

## Checks on the whole document

- **Diff.** The diff recomputed from `snapshots/final-inline2-pre/` against the current files equals
  `build/final-inline2.diff`: six edits in five files. Since the snapshot, the only other document file that changed
  is `appendix_map.tex`, which was regenerated. The maps did not change. The appendix text of the new build equals
  that of `build/inline-check`, after whitespace is normalized and the repeated longtable headers are removed. Only
  the positions of those headers differ.
- **Label rule.** I audited every `\ref` in the twelve section files against CONTRACT.md:68-69: own labels, the 20
  listed `fd:` labels and the export labels of the table. The audit found 0 violations and no label defined twice, and
  every export label is defined.
- **Rebuild.** I built the document independently into `build/inline2-verify/`: three `nice -n 15 pdflatex` passes,
  each exiting with 0. The result has 188 pages, no error, no undefined reference, no overfull box, no rerun request
  and no LaTeX warning other than underfull boxes. Its `pdftotext` output is identical to that of
  `build/inline-check2/proofs.pdf`, so the build given with the task matches the current sources.
- **Underfull boxes.** There are 202 underfull boxes, against 201 in `build/inline-check`. The difference is only in
  page-level `\vbox` warnings, which come from shifted page breaks: the one at p. 103 is gone, and new ones occur at
  p. 94 (badness 3525) and p. 156 (badness 3049). I inspected both pages. The vertical space before §8.1 and before
  Remark 12.13 is slightly larger, with no visible defect. No finding.
- **Hygiene.** The added lines contain no machine path and no tool name.

## What could not be confirmed

- **The Lean version of either file.** Neither saved log prints a version. Both READMEs state 4.24.0, which agrees with
  the repository pin. The edit claims only "according to their READMEs", and that much is confirmed.
- **The README record for `Central34Orbits.lean`.** `C2FINAL/README.md` §6 records "axioms propext only, about 6 s".
  No Lean output exists that could confirm this, and Lean was not run. This is exactly why the text uses the
  qualified label.
- **The recorded checker verdicts.** They were not replayed. None of the edits claims more than that the records exist
  and that their hashes match.
