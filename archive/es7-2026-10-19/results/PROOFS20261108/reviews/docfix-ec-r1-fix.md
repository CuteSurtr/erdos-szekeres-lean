# docfix ec, round 1 (whole-document review findings)

Snapshot before editing: `snapshots/docfix-r1-pre/ec.tex`, `snapshots/docfix-r1-pre/ec.map.tsv`.
Files edited: `sections/ec.tex`, `sections/ec.map.tsv` only. No label removed or renamed (47 labels, map rows unchanged
in number and order); no macro or package added.

Lean declarations re-read for the statements touched:
- `convexNGon_of_layers` (LAYERLEAN/LayerLemma.lean:1066): `m * (t - 1) < (S.erase c).card` with natural `t - 1`;
  (R) matches.
- `centre_not_mem_of_even` (LAYERLEAN/LayerLemma.lean:582): `{m : ℕ}`, `0 < m`, `Even m`,
  `Invariant (rotAbout c (2 * Real.pi / m)) S`, `GeneralPosition S`, `p ∈ S`, `p ≠ c` ⊢ `c ∉ S`; (C) matches, and
  now says `m ∈ N` explicitly.
- `Fivefold35` / `Fourfold32` (LEANEXT/es7corr/ES7Corollaries.lean:1157/1164): definition text unchanged (head word only).
- `fourfold_heptagon` (ES7Corollaries.lean:1216): the call of `centre_not_mem_of_even (m := 4)` with
  `(by exact_mod_cast hinv)` is at line 1228, as the finding says.
- `fivefold_heptagon_of_erase` / `fourfold_heptagon_of_erase` (:1170/:1203): size side goals closed by `omega` on
  `5 * (7 - 1)` and `4 * (8 - 1)`; the proofs now write these with the truncated minus.

| # | finding | action | location (after the fix) | reason / note |
|---|---|---|---|---|
| 1 | xref-ocpcec F2, minor: cast-angle side condition stated only for ll:thm:reduction | fixed (both suggested fixes) | ec.tex:92-95 (Conventions); ec.tex:168-172 (item (C)); ec.tex:232-236 (proof of ec:thm:fourfold) | Checked: Lean applies `centre_not_mem_of_even (m := 4)` with `exact_mod_cast` at ES7Corollaries.lean:1228. The Conventions now say that in Theorem ll:thm:reduction and Lemma lg:lem:centre (items (R) and (C)) the angle is 2pi/m with m in N cast to R. Item (C) now starts "Let m in N", as lg states it. The application of (C) says that rotAbout(c,2pi/4) is the rotation of (C) for m=4 (the cast angle equals 2pi/4), with a pointer to the Conventions. |
| 2 | consistency m4, minor: (R) writes m(t-1) "(natural subtraction)" | fixed | ec.tex:161-167 (item (R)); ec.tex:189 and ec.tex:223 (proofs of ec:thm:fivefold-erase, ec:thm:fourfold-erase) | (R) now writes m(t ∸ 1) with `\mathbin{\dot{-}}` as ll does, and defines t ∸ 1 = max(t-1,0) (Lean's truncated subtraction on N), which also meets fd's convention. The two proofs write 5(7∸1)=5·6=30 and 4(8∸1)=4·7=28. Remark ec:rem:orbits keeps m(t-1): there t is 7 or 8, so the difference is ordinary (fd's "state the inequality" option). |
| 3 | consistency m8, minor: "case statements" vs "case classes" | fixed | ec.tex:7, 97 (head of ec:def:cases), 107 (head of ec:rem:cases), 175, 267 | All five occurrences, including ec.tex:259 (old numbering; Remark ec:rem:orbits), which the finding did not list, now say "case class(es)", as sr, ar, mb and sa do. Map notes of ec:def:cases and ec:rem:cases use the same term. |
| 4 | consistency m9, minor: \dirn{E2} collides with trust item (E2) of the k8 note | fixed | ec.tex:113 | Now cites the record `E2/logs/lrat_check_soundness.md`. LRATCHECK20261105/README.md names this file as "the record" of the defect; its content (an empty clause with no hints is accepted by the unpatched build) supports the sentence. |
| 5 | consistency m10, minor: "refereed" next to the document's "(not refereed)" | fixed | ec.tex:120-123 (C2ENC), ec.tex:129-131 (C4CUT), ec.tex:137-138 (new sentence after the list) | Both occurrences now say "refereed within the project". A new sentence after the list says that the reviews, audits and refereeing named in the list were all made within the project (internal reviews), and that none of them is an external peer review. This also covers AUDIT3 ("reviewed in the audit"). ar.tex:734 uses the compatible wording "reviewed or audited within the project". |
| 6 | claims F12, minor: "refereed" reported without saying the review was internal and done the same day | fixed (together with 5) | ec.tex:120-123, ec.tex:129-131 | Checked against the records. C2ENC/perturbation.md:3-5 says it was "Written 1 November 2026 ... and refereed with proof.md the same day (referee/NOTES.md §4: correct)", so the text now reads "refereed within the project on the day it was written: C2ENC/referee/NOTES.md, Section 4". C4CUT/README.md:16-18 refers to "The independent review of 1 November (review/)", and C4CUT/review/README.md describes a review run separately from the work it checks. The text now reads "refereed within the project: the review of 1 November 2026, C4CUT/review/README.md". The word "internal" is kept to the general sentence, so that it does not seem to contradict the record's "independent" (independent of the authors, but inside the project). |

Map (`sections/ec.map.tsv`): the notes of `ec:def:cases` ("the case classes: ...") and `ec:rem:cases` ("status of the
case classes ...; ... the records' reviews and refereeing were internal to the project") were updated. They are still
ASCII with 5 fields per row. The appendix needs regenerating (`python3 tools/make_appendix.py`) to pick up the two notes.

Compile check: `build/ec_wrapper.tex` was run twice with `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error`.
Both runs exited 0. There are no errors, no "Missing" messages and 0 overfull boxes. There are 21 underfull boxes, the
same count as the pre-edit snapshot compiled the same way; all are in statement heads with long Lean names. The only
undefined references are fd: and export labels of ll, lg, oc and sr, which is expected standalone.

Not addressed here (not assigned to this fixer): consistency M1 (the "computer-assisted" label of ec:prop:ex341),
consistency m7 ("conditional" in theorem heads) and claims F11 ("conditional" in the Coverage paragraph).
