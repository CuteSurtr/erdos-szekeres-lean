# Final inline edits: accuracy review (lens: accuracy)

Verdict: **pass**. Every hunk of `build/final-inline.diff` is true when checked against the Lean files and records in
REPO (commit `7e32ee259`), the surrounding text, all twelve section maps and the appendix map. There is no blocker
and no major finding. The six findings below are minor; four of them are optional.

Paths: section files are relative to STAGE, Lean files and records relative to RES. Line numbers refer to the
current files. Statement numbers come from the build in `build/inline-check/proofs.pdf` (188 pages). Nothing under
STAGE or REPO was edited. Scratch output is in `build/final-inline-accuracy/`: a text dump of the PDF and
`c2_closed_check.py`, a short exact recount of the C2FINAL data.

## Findings

| # | severity | location | issue | fix |
|---|---|---|---|---|
| 1 | minor | sa.tex:525 (unchanged context of the sa hunk) | The sentence now tries to be exhaustive, but it says that `LayerLemma.Fourfold32` is the hypothesis of Theorem `ec:thm:fourfold` (6.7) only. The same copy is also the hypothesis of Theorem `ec:thm:fourfold-erase` (6.6, `fourfold_heptagon_of_erase`, `LEANEXT/es7corr/ES7Corollaries.lean:1203`, `(H : Fourfold32)`). ec.tex:155-156 and the new ec Coverage sentence (ec.tex:890-891, "the two fourfold theorems on Fourfold32") both say this. The text is true but incomplete. | `ec:thm:fourfold-erase` is not an export label, so name it by its Lean name: "... is the hypothesis of Theorem~\ref{ec:thm:fourfold} and of the layer form \lean{LayerLemma.fourfold_heptagon_of_erase} that its proof uses; ...". |
| 2 | minor | sr.tex:298 (outside the diff) | "\lean{Fourfold32} (used only by Theorem~\ref{sr:thm:variant})" makes the claim that hunk (2) corrected in sa.tex. `case_fourfold` (Lemma `sr:lem:fourfold`, 7.37; `SYMLEAN/SymmetricReduction.lean:763`, `(h4 : Fourfold32)`) also takes the class. sa now says so, and sr does not, so the two sections differ. | "(a hypothesis only of Theorem~\ref{sr:thm:variant} and of Lemma~\ref{sr:lem:fourfold}, which its proof uses)". Both are sr's own labels. |
| 3 | minor | sa.tex:522 | The text writes `\lean{case_fourfold}` without its namespace. fd.tex:40-42 allows only the prefix `ErdosSzekeres.` to be omitted, and sa states no namespace convention (sr.tex:114 and ar.tex:26 each state one). Read strictly, the name is `ErdosSzekeres.case_fourfold`, which does not exist. The declaration is `ErdosSzekeres.SymReduction.case_fourfold`. The context (the case lemma that the variant's proof uses) and the appendix row for Lemma 7.37 identify it, so the reader is not misled. The same sentence already wrote `\lean{Fourfold32}` and `\lean{VariantChecks.group_form}` relative to `SymReduction`, yet gave `\lean{LayerLemma.Fourfold32}` with its namespace. | `\lean{SymReduction.case_fourfold}`, or add `(\dirn{SYMLEAN/SymmetricReduction.lean:763})`. |
| 4 | minor (optional) | ar.tex:746 | "every piece named in the data of these two theorems has a record with the checker verdicts and a CNF hash equal to that of the rebuilt formula". I checked this for the pieces of the paragraph, the SAT units: (a) all 73,567 leaves named by the keys of Theorem `cb:thm:c3` (`C3LEAN/review/logs/indep_audit.json`: `leaf_names_not_certified` 0, 73,707 leaf records hash-checked, `hash_mismatches` 0; `C3LEAN/review/logs/audit_keys_orig.log`: 0 failures); (b) all 2,297 subcases listed in `closedP1`-`closedP8` of Theorem `cb:thm:c2`, recounted by `c2_closed_check.py` with the criterion of `C2FINAL/gen_lean.py`: 0 without a record that has status UNSAT, both checker verdicts, and a hash in `hashmatch.json` "matched" (or a §4 re-solve with the computed hash). However, the data of `cb:thm:c3` also name the 910 roots (the certificates' root codes and `tsvRootCodes`), and a root that is split further has no record of its own. A reader who takes "piece" to mean "node" gets a false statement. | "every leaf named by the keys of the certificates of Theorem~\ref{cb:thm:c3} and every subcase listed in the data of Theorem~\ref{cb:thm:c2} has a record ...". |
| 5 | minor (optional) | cb.tex:62-63 | "(for C2FINAL/Central34Orbits.lean according to its README ...)" is true: `C2FINAL/README.md` §6 says "Core Lean 4.24.0", and line 249 says "lean Central34Orbits.lean # Lean 4.24.0". The contrast it implies is not quite right, though. The Lean version of `C3LEAN/C3Cover.lean` also rests only on its README (`C3LEAN/README.md`:10 and :227) and on the repository `lean-toolchain` (v4.24.0); `C3LEAN/logs/compile.log` and `review/logs/main_compile.log` print no version. The real difference is that C3Cover has saved Lean output and C2FINAL has none. | Optional: "Both files are checked with Lean~4.24.0 according to their READMEs; for \dirn{C3LEAN/C3Cover.lean} a compile log is saved, for \dirn{C2FINAL/Central34Orbits.lean} no Lean output (paragraph ``Axioms'' below)." |
| 6 | minor (optional) | proofs.tex:52-53 | "\dirn{C3LEAN}, and \dirn{C2FINAL}, whose declarations are Lean-checked according to the record," is true for C2FINAL (see check 1). Because of the comma before "and", the clause can also be read as covering C3LEAN. For C3LEAN that reading is wrong, since C3Cover is Lean-checked with a saved compile log. It would be an under-claim, and cb corrects it. | "\item \dirn{C3LEAN} and \dirn{C2FINAL} (the declarations of the latter are Lean-checked according to the record), in Section~\ref{cb:sec};". |

## Checks, hunk by hunk

1. **proofs.tex:52-53 (scope list).** `C2FINAL` has exactly one Lean file, `Central34Orbits.lean` (298 lines, SHA-256
   `b396a26b2430...`). Its declarations are 17 definitions (`inner`, `choose2`, `choose3`, `subcases`, `mask`, `refl`,
   `bitset`, `uncovered`, `closedP1`-`closedP8`, `closed`) and three theorems (lines 273, 284, 291), all in namespace
   `Central34`, followed by three `#print axioms` lines. A search of REPO, which has no untracked files, for
   `Central34`, `all_cases_closed`, `closed_are_subcases` and `subcases_reflection` finds no Lean output. The hits
   are the Lean file itself, `C2FINAL/README.md`, `C2FINAL/gen_lean.py`, and mentions without output in
   `C2ENC/class_table.md`, `AUDIT3/reports/A5_central_geometry.md` (row 12: the auditor recomputed in Python) and
   `WRITEUP/SYMMETRIC.md`. This is exactly the case of fd.tex:84-86, so the qualified label applies to all the
   file's declarations. True.
2. **bibliography.tex:1-2 (comment).** The front matter cites all 11 entries by key: Bae25, Lean4, DT, Dum25, ES35,
   Mathlib, Roc70, Rud76, Sch26, SMQH25 and CakeLPR, at proofs.tex:88-99. The paragraph "Works cited" exists at
   proofs.tex:92. The sections name the works inline (Rockafellar in ll, Rudin in fd and lg, Dumitru and
   Subercaseaux in sr, Schroeder and Erdős–Szekeres in mb, Baek throughout), and mb also uses `\cite{Sch26}`. True.
   The comment is not typeset.
3. **ec.tex:171-172.** fd.tex:133-135 writes $f^{[n]}$ for the $n$-th iterate ($f^{[0]}=\mathrm{id}$), and fd is
   titled "Conventions and foundations". True. No cross-section `\ref{..:sec}` remains in any section file.
4. **ec.tex:890-891.** `ES7Corollaries.lean`: `fivefold_heptagon_of_erase` (:1170), `fivefold_heptagon` (:1183) and
   `fivefold_heptagon_of_centre_not_mem` (:1193) each take `(H : Fivefold35)`. `fourfold_heptagon_of_erase` (:1203) and
   `fourfold_heptagon` (:1216) each take `(H : Fourfold32)`. No other unproved hypothesis occurs. These are
   `LayerLemma`'s copies, as listed in the same Coverage item (Definition `ec:def:cases`). No other theorem of the ec
   Coverage takes an unproved proposition (`RefuteC6.part_a`, `thr_m*`, `PCompat.*` and `L0*` were checked). True.
5. **cb.tex:62-63.** The README of Central34Orbits.lean (`C2FINAL/README.md` §6, line 153) says "Core Lean 4.24.0",
   and line 249 agrees. The paragraph "Axioms" directly follows (TOC: section*.76) and explains why there is no
   Lean output. The file has no `import`. True; see finding 5.
6. **cb.tex:80-84.** The qualified label is extended to all declarations of `Central34Orbits.lean`. This matches
   fd.tex:84-86 ("the label of its declarations") and fd.tex:115-117 (for a definition the label records only that
   Lean accepted it). All 17 definitions occur in the statements of the three theorems, so the README record "axioms
   `propext` only" covers them through the dependency closure, and the README's reproduction line runs the whole
   file. "three theorems ... and so are its definitions" lists every declaration kind in the file. The cb map, the
   appendix rows 486-500 and the paragraph "Rigor labels and dependencies" (cb.tex:86-88) agree. True.
7. **cb.tex:1516-1517.** sa ("Size arithmetic of the symmetric $k=7$ reduction") is Section 12, the last numbered
   section; only Appendix A and the References follow, and "on size arithmetic" removes any doubt. sa.tex:9-27
   treats `SizeArith.lean`, `AssembledSizes.lean` and `BaekSeven.lean`. True.
8. **sa.tex:521-526.** `SymmetricReduction.lean`: `case_fourfold (h4 : Fourfold32)` (:763) and
   `halfTurn_of_symmetric_counterexample (h3) (h4 : Fourfold32) (h5) (hm1) (hm0)` (:1024-1025). The Lean proof of the
   latter calls `case_fourfold h4 ...` (:1042), and its written proof uses Lemma 7.37 (sr.tex:1008-1010).
   `heptagon_of_nontrivial_isometry` (:997) does not take the class. The search was exhaustive: every Lean file of
   REPO containing `Fourfold32` was checked (the copies in `AffineReduction.lean`, `AffineReductionAxioms.lean`,
   `SymmetricReductionAxioms.lean`, `mirror/ReductionThreeClasses.lean` (RTC):789/1050, `review/ReviewSanity.lean` and
   `review/VariantChecks.lean`, and `LEANEXT/es7corr`), and so were all maps and section files. The only numbered
   statements taking `SymReduction.Fourfold32` are `sr:lem:fourfold` and `sr:thm:variant`. The ar theorems take the
   five classes without `Fourfold32` (ar.tex:15; RTC :1510-1554 pass `h2 h3 h5 hm1 hm0`). mb's three-class theorems do not take it, and the
   RTC copy of the variant is only mentioned (mb.tex:1135-1136). The ec theorems take the `LayerLemma` copy. So the
   "only ... and ..." claim is exhaustive. `VariantChecks.group_form` (:1168-1170) and `fourfold36_of_fourfold32`
   (:1220) take `(h4 : Fourfold32)`, and `variant_unfolded` takes the class in unfolded form, which confirms "so do
   some checks". True; see findings 1-3.
9. **ar.tex:746.** "these two theorems" means `cb:thm:c3` and `cb:thm:c2` (ar.tex:743-745). The recounts are
   described in finding 4. `C2FINAL/gen_lean.py`:15-32 admits a subcase only through such a record.
   `C3LEAN/README.md` §4 describes the two exact checks for C3. True for the leaves and listed subcases; see finding
   4.
10. **mb.tex:1179.** `mirror/ReductionThreeClasses.lean`: `heptagon_of_nontrivial_isometry_3` (:4292) and
    `heptagon_of_nontrivial_affineEquiv_3` (:4303) each take exactly `(h2 : HalfTurn34) (h3 : Threefold33)
    (h5 : Fivefold35)`. This matches the header (:30-31), mb.map.tsv:41 and Remark `mb:rem:main3`. True.

The build in `build/inline-check` has 0 errors, 0 warnings and 0 undefined references. pass3 has 188 pages. The text
of every edited passage was read in the PDF.
