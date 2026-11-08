# Final inline edits: rules and consistency (lens: rules)

Verdict: **pass**. There is no blocker or major finding. There are three minor findings: one consistency gap in sr,
exposed by the corrected sa sentence, and two optional wording points.

Scope: the ten hunks of `build/final-inline.diff` in seven files: `proofs.tex`, `bibliography.tex`,
`sections/ec.tex` (2 hunks), `sections/cb.tex` (3), `sections/sa.tex`, `sections/ar.tex` and `sections/mb.tex`.
Paths are relative to STAGE, and record paths are relative to RES. Line numbers refer to the current files. Nothing
under STAGE or REPO was edited. Scratch output is in `build/verify-rules/` and `build/verify-rules-copy/`.

## Findings

| # | severity | location | issue | fix |
|---|---|---|---|---|
| 1 | minor | sections/sr.tex:298 (Remark `sr:rem:records`, PDF p. 82) | The item reads `\lean{Fourfold32} (used only by Theorem~\ref{sr:thm:variant})`. The edited sa sentence (sa.tex:521-523) now says that Theorem `sr:thm:variant` *and the case lemma* `case_fourfold` take this class as a hypothesis. The sa edit corrected the "only the variant" claim, but sr keeps the same claim. sr itself states `case_fourfold` as Lemma `sr:lem:fourfold` (sr.tex:889, head "conditional on \lean{Fourfold32}"; Coverage sr.tex:1140-1141), and in Lean it takes `(h4 : Fourfold32)` (`SYMLEAN/SymmetricReduction.lean:763`). The two sections now describe the users of the class differently. This has no effect on correctness: in a remark about which theorem each class serves, "used only by the variant" reads naturally. | Use the sa precision in sr, with own labels only. For example: `(a hypothesis only of Theorem~\ref{sr:thm:variant} and of Lemma~\ref{sr:lem:fourfold}, which its proof uses)`. |
| 2 | minor (optional) | sections/sa.tex:521-525 (PDF p. 156) | (i) The sentence begins "Among the reduction theorems stated in this document, only Theorem~\ref{sr:thm:variant} and the case lemma `case_fourfold` ...". sr separates "The case lemmas" (§7.7) from "The reduction theorems" (§7.8), so a case lemma is not among the reduction theorems in sr's terms. (ii) After the exhaustive "only ... and ...", the clause "a same-text copy, `LayerLemma.Fourfold32`, is the hypothesis of Theorem~\ref{ec:thm:fourfold}" names only one of the two es7corr theorems that take the copy. The edited ec Coverage (ec.tex:890-891, "the two fourfold theorems on Fourfold32") and ec.tex:155-156 name both, and so does the Lean source (`LEANEXT/es7corr/ES7Corollaries.lean:1203, 1216`). The clause is true, since it does not claim exclusivity, but it can be read as a complete list. | (i) Write "Among the reduction theorems and case lemmas stated in this document, ...". (ii) Write "... is the hypothesis of Theorem~\ref{ec:thm:fourfold} and of its layer form \lean{fourfold_heptagon_of_erase}". Add no `\ref`: `ec:thm:fourfold-erase` is not an export label. |
| 3 | minor (optional, wording) | sections/cb.tex:82-84 (PDF p. 134); also cb.tex:86-89 | In "its three theorems are \emph{Lean-checked according to the record}, the qualified label defined with the rigor labels at the beginning of this document, and so are its definitions", the appositive sits between the label and "and so are its definitions". On a first reading the last clause may attach to "the rigor labels". The paragraph "Rigor labels and dependencies" (cb.tex:86-89) still gives the qualified label only to the three theorems. It does not contradict the extension, but it does not repeat it. | Write "its three theorems and its definitions are \emph{Lean-checked according to the record}, the qualified label defined with the rigor labels at the beginning of this document." Optionally add "(as are its definitions)" after "Theorem~\ref{cb:thm:c2})" at cb.tex:88. |

## Per hunk: checks (a), (b), (c) and (e)

In every hunk, (b) holds: no `\ref` was added except own or export labels already used before the edit. (e) also
holds: no machine path and no tool name was added. The full build has no error, no undefined reference and no overfull
box.

| hunk | intent | (a) LaTeX and rendering | (c) labels and consistency |
|---|---|---|---|
| proofs.tex:52-53 | (6) | Renders on one line, PDF p. 3: "C3LEAN, and C2FINAL, whose declarations are Lean-checked according to the record, in Section 11". The comma after C3LEAN attaches the relative clause to C2FINAL only, which is acceptable. | The phrase matches fd.tex:84-86 exactly ("the label of its declarations ... we write Lean-checked according to the record"). `C2FINAL` holds a single Lean file, `Central34Orbits.lean` (checked in REPO), so "its declarations" are exactly the cb ones. The phrase is consistent with proofs.tex:39 ("restate the Lean-checked results"): fd.tex:51 makes the qualified label a form of Lean-checked. `Section~\ref{cb:sec}` is the front matter's existing reference, moved to the next line. |
| bibliography.tex:1 | (7) | A comment, not typeset. | "(see Works cited)" names the paragraph at proofs.tex:92. "the front matter ... cites every entry by key" is still true: all 11 `\bibitem` keys are cited in proofs.tex, and the sections cite only `Sch26`, at mb.tex:47. |
| ec.tex:171-172 | (1) | PDF p. 68, clean. | The removed `\ref{fd:sec}` was one of the two section-level violations of the label rule. "the foundations section" is the document's usual name for fd (ll.tex:61, lg.tex:40/108, oc.tex:106, mm.tex:43/86, sr.tex:79/644/1133). The statement agrees with fd.tex:133-135 ($f^{[n]}$, $f^{[0]}=\mathrm{id}$) and fd.tex:152 (a later section may write $f^n$ and defines it where introduced). |
| ec.tex:890-891 | (5) | PDF p. 77, clean. | True in Lean: `ES7Corollaries.lean:1170, 1183, 1193` take `(H : Fivefold35)`, and `:1203, 1216` take `(H : Fourfold32)`. It matches ec.map.tsv:4-8 ("takes hypotheses: ...") and the five statements at ec.tex:179-229 (each begins "Assume Fivefold35" or "Assume Fourfold32"). `\lean{Fivefold35}` and `\lean{Fourfold32}` mean the es7corr copies, as in the same Coverage item (Definition `ec:def:cases`). The wording "conditional on" is fd's (fd.tex:120-122, "the hypotheses are named"). |
| cb.tex:62-63 | (4) | PDF p. 133, clean. | True: `C2FINAL/README.md:153` reads "Core Lean 4.24.0, `decide +kernel`, axioms `propext` only, about 6 s", and :249 reads "Lean 4.24.0, no Mathlib needed". The pointer "the paragraph ``Axioms'' below" is correct (cb.tex:70). The README is the only evidence that the C2FINAL file was checked at all. For C3LEAN a compile log exists, although it does not print the version either, which comes from the repository pin (fd.tex:46). So the qualification is right, and it agrees with ec.tex:41 and sa.tex:98, which also cite records for the toolchain. |
| cb.tex:81-84 | (4) | PDF p. 134, clean. | "Lean-checked according to the record" matches fd. The condition "(compile or build log, axiom output, pinned message)" is copied from fd.tex:84-85. Extending the label to the definitions agrees with fd.tex:116-118 (for a definition the label records only that Lean accepted it) and with the scope list. See finding 3 for wording. |
| cb.tex:1516-1517 | (1) | PDF pp. 149-150, clean. | The removed `\ref{sa:sec}` was the second violation of the label rule: sa has no export labels in the contract. "the last section, on size arithmetic" is accurate. sa is Section 12, the last numbered section, followed by Appendix A and the References. Its title is "Size arithmetic of the symmetric k = 7 reduction", and it treats the three files named, as sa.tex items (1)-(3) state. |
| sa.tex:521-523 | (2) | PDF p. 156, clean. The parenthesis nests correctly. | True. In sr, only Lemma `sr:lem:fourfold` (`case_fourfold`) and Theorem `sr:thm:variant` take `SymReduction.Fourfold32` (sr.map.tsv:38 and :42; no ar or mb map row mentions the class). The written proof of the variant uses the lemma (sr.tex:1009), and so does the Lean proof (`SymmetricReduction.lean:1042`). The copies of both declarations in `AffineReduction.lean` and `ReductionThreeClasses.lean` are verbatim duplicates and are not restated. `\lean{case_fourfold}` follows sa's own way of omitting namespaces (`\lean{Fourfold32}` for `ErdosSzekeres.SymReduction.Fourfold32`). "that its proof uses" fixes which copy is meant. No `\ref` to `sr:lem:fourfold` was added, correctly, since it is not an export label. Remaining inconsistency: finding 1. Wording: finding 2. |
| ar.tex:746 | (3) | PDF p. 102, clean. | "these two theorems" can only mean Theorems `cb:thm:c3` and `cb:thm:c2` of the previous sentence. The claim is consistent with cb.tex:1161-1166 (C3: every leaf names a record with recorded checker acceptances, and its CNF hash matches the base formula plus the units of the node, checked by Python outside Lean), with cb.tex:1276-1279 (C2: hashes rebuilt and matched by `C2FINAL/hashmatch.py`, or a re-solve), and with `C2FINAL/README.md` §4, where the pilot re-solve "rebuilds each CNF ... and requires the expected hash". The label sentence before it, "which is Lean-checked according to the record", is unchanged and correct. |
| mb.tex:1179-1180 | (5) | PDF p. 132, clean. | True in Lean: `SYMLEAN/mirror/ReductionThreeClasses.lean:4292-4294` and `:4303-4305` take `(h2 : HalfTurn34) (h3 : Threefold33) (h5 : Fivefold35)`. It matches the statement (mb.tex:1062-1066), mb.tex:112-113, Remark `mb:rem:main3` and mb.map.tsv:41. The form "(Theorem X, conditional on A, B and C)" is sr's Coverage style (sr.tex:1137-1146). |

## (c) Every mention of the C2FINAL label

I searched all twelve sections, all twelve maps, proofs.tex and appendix_map.tex for `C2FINAL`, `Central34`,
`cb:thm:c2`, `cb:fact:c2-sub`, `cb:thm:c2-refl`, `cb:cor:c2` and "according to the record". Every mention that
attaches a label uses exactly "Lean-checked according to the record":
- proofs.tex:52 (new, the declarations of C2FINAL);
- cb.tex:83-84 (theorems and, new, the definitions), cb.tex:88 (the three theorems), and cb.tex:1328, 1377, 1391 (after
  `cb:thm:c2-refl`, `cb:fact:c2-sub` and `cb:thm:c2`);
- ar.tex:745, mb.tex:1110, sr.tex:82-83 and sr.tex:268-269;
- cb.map.tsv:97-99, mb.map.tsv:42, and appendix rows 399 and 498-500.

ar.tex:727/736/742, mb.tex:109/1105-1108, sr.tex:81/263 and the cb Coverage (cb.tex:1460-1465) name C2FINAL or its
theorems without a label. No mention gives the plain label "Lean-checked" to a C2FINAL declaration.

The map rows of the C2FINAL definitions (cb.map.tsv:85-94; appendix rows 486-495) carry no rigor note. This follows the
convention of all maps: none of the 115 definition rows carries one. These rows do not conflict with the extension at
cb.tex:84.

fd.tex:46 ("The Lean files were checked with Lean 4.24.0") and fd.tex:53 remain generic. The diff does not change them,
and fd.tex:84-86 itself defines the qualified form for such files. This is not a new issue.

## (b) Label rule, whole document

I audited every `\ref` in the twelve section files against the contract's rule (CONTRACT.md:68-69). The allowed labels
are own labels, the 20 listed `fd:` labels and the export labels of the table; sa has none. The current files have 0
violations. Run on the five section files of `snapshots/final-inline-pre/` (the other seven sections are unchanged),
the same audit finds exactly two: `fd:sec` at ec.tex:172 and `sa:sec` at cb.tex:1516. The edits remove both. Every `\ref` target in the document is defined, and no label is defined twice.

The front matter proofs.tex is not a section file. Its references to `:sec` labels and to `ll:rem:hyp`,
`sr:rem:mirror-line`, `mb:thm:capcup` and `sr:rem:records` predate this diff and are unchanged.

## (d) Appendix

I copied `sections/`, `tools/`, `proofs.tex`, `preamble.tex`, `bibliography.tex`, `appendix_map.tex` and `CONTRACT.md`
to `build/verify-rules-copy/` and ran `python3 tools/make_appendix.py` there, with bytecode writing disabled. It
printed "appendix_map.tex: 470 rows" and no warning. `cmp` against `STAGE/appendix_map.tex` reports the files as
identical (SHA-256 `cb953c74b2839fc1...` for both). The appendix therefore matches the current maps. No map changed in
this diff: the five maps in the snapshot are byte-identical to the current ones. The STAGE appendix (22:29:08) and
`tools/__pycache__` were not touched.

## Checks run (all read-only)

- CONTRACT.md in full; fd.tex:40-140 (rigor labels, the head rule, notation).
- Recomputed the diff of `snapshots/final-inline-pre/` against the current files. The set of changed lines equals that
  of `build/final-inline.diff` (33 lines). No other document file under STAGE changed after the final sweep (22:22),
  except the regenerated appendix.
- The `\ref` audit, run on the current files and on the pre-edit snapshot.
- The appendix regeneration in a copy, compared with `cmp`.
- PDF `build/inline-check/proofs.pdf` (188 pages): pdftotext of the whole document, and 100-dpi renders of pp. 3, 68,
  77, 102, 132, 133, 134, 150 and 156, all inspected. In proofs.log, 0 overfull boxes, 0 undefined references and no
  rerun request in the last pass; 201 underfull boxes, against 202 in the previous full build
  (`build/final-recheck-front-r1`).
- REPO, read-only: `C2FINAL/README.md` (§4, §6, :153, :249); the contents of the `C2FINAL` directory;
  `LEANEXT/es7corr/ES7Corollaries.lean:1150-1233`; `SYMLEAN/mirror/ReductionThreeClasses.lean:4292-4307`;
  `case_fourfold` in all Lean files under RES; `C3LEAN/README.md:10-14`; `C3LEAN/logs`; the repository
  `lean-toolchain` (v4.24.0).
- A scan of the added lines and of every document file (sections, maps, proofs.tex, bibliography.tex, preamble.tex,
  appendix_map.tex) for machine-path prefixes and tool names: 0 hits.
