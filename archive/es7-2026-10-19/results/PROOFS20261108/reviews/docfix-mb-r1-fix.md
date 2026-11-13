# docfix-mb-r1: fixes to section mb after the whole-document review, round 1

Inputs: reviews/doc-r1-xref-mmmb.md (findings F1-F3 on mb; F4 concerns mm and is not in scope here).
Snapshot before editing: snapshots/docfix-r1-pre/mb.tex, snapshots/docfix-r1-pre/mb.map.tsv.
Files edited: sections/mb.tex, sections/mb.map.tsv. No statement environment, label, Lean name or file:line changed
(the label lists before and after are identical); no macro or package added.

| # | finding | action | location (after edit) | notes |
|---|---|---|---|---|
| 1 | xref-mmmb F1 (minor): Remark mb:rem:main3 omits the labels and references for the Lean-checked bookkeeping | fixed | sections/mb.tex:1102-1115 (items HalfTurn34 and Threefold33) | HalfTurn34 item: added "The bookkeeping of the subcase orbits, namely that the listed subcases of the eight parallelogram hull cases meet every orbit of second-layer subcases, is Lean-checked by kernel evaluation, so computer-assisted (Theorem cb:thm:c2); that the listed subcases are refuted rests on the records." Threefold33 item: "C3LEAN Lean-checks, by kernel evaluation and so computer-assisted (Theorem cb:thm:c3), only that the leaves named in it cover the 910 roots ...". Checked against the sources: C3LEAN/C3Cover.lean (all_roots_covered, line 2251; its finite checks are `decide +kernel`; the only occurrence of `native_decide` is the docstring saying it is not used) and C2FINAL/Central34Orbits.lean (all_cases_closed, line 291, `decide +kernel`; no `native_decide`). The wording now matches Remarks sr:rem:records and ar:rem:classes and the scope remark cb:rem:c2-scope. |
| 2 | xref-mmmb F2 (minor): dependency list incomplete | fixed | sections/mb.tex:96-110 (paragraph "Dependencies and rigour") | Added fd:lem:separation to the foundations lemmas (Step 5 of the proof of Lemma mb:lem:boundary uses its easy direction, and also proves it inline). fd:lem:pos-cycle, ll:thm:layers and lg:thm:nesting are cited only in remarks, so they are listed in a new sentence modelled on sr's dependency paragraph: "Two remarks refer to further results that no proof of this section uses: Remark mb:rem:generated (on the Lean proofs of Lemma mb:lem:polygons) to Lemma fd:lem:pos-cycle, and Remark mb:rem:main3 (on the hypotheses of Theorem mb:thm:main3) to Theorems ll:thm:layers, lg:thm:nesting, cb:thm:c2 and cb:thm:c3." cb:thm:c2 and cb:thm:c3 are included because the fix of finding 1 adds references to them. After the edit every cross-section label referenced in mb.tex appears in this paragraph, except mm:lem:slope and mm:thm:small, which occur only in the Coverage paragraph as pointers to where excluded declarations are treated. All labels used are fd labels or export labels of the contract; the environment words (Lemma/Theorem) match their targets (fd.tex:1077, 1109; ll.tex:523; lg.tex:443; cb.tex:1119, 1370). |
| 3 | xref-mmmb F3 (minor): [n] glossed as Finset.range n but also used for Fin n; P(c) not linked to mm's pts(C) | fixed | sections/mb.tex:116-118 (Conventions) and 259-261 (description of configurations before Definition mb:def:color) | Conventions: "Where [n] is the index set of a configuration of n points, or the domain or codomain of a cap map such as f:[k]->[n] (Subsection mb:ssec:bridge), it is the same set viewed as Lean's `Fin n`, as in Definition mm:def:config." After P(c): "it is the point set pts(c) of Definition mm:def:config(a)". Re-read the Lean declarations: ErdosSzekeres/Omission/Realization.lean:9 (`Configuration n` with `point : Fin n → Point`) and :64 (`HasCap`, `∃ f : Fin k → Fin n, StrictMono f ∧ ...`); the Baek-model uses of [n] (hasCap_of_list, hasNGon_heptagon/octagon, capacity16, geometric_capacity22) are `Finset.range n`. Every Fin-indexed use in mb.tex (lines 256, 258-259, 371, 717, 892 after the edit) is a configuration index set or a cap map, so it is covered by the new sentence; all other uses of [n] are subsets of the natural numbers. mm.tex's Conventions (line 86) gloss [m] as `Fin m`, and mm:def:config(a) defines pts(C) as `Finset.univ.image c.point`, the same Lean expression as P(c). |

Map sync: sections/mb.map.tsv row mb:rem:main3, note extended to "remark (no statement): status of the three hypotheses
of mb:thm:main3, with the records and rigor labels of their evidence; the case-split bookkeeping (cb:thm:c2, cb:thm:c3)
is Lean-checked by kernel evaluation, so computer-assisted". The map still has 42 rows, all with 5 fields and ASCII only,
one per statement environment of mb.tex; every label in the notes resolves to a label defined in a section file (the
check that tools/make_appendix.py makes).

Rigour vocabulary: the added text uses "Lean-checked", "computer-assisted" and "written proofs" only; no "verified",
"certified" or "proved" was added, and no hypothesis is presented as proved.

Compile check: build/mb_wrapper.tex, `nice -n 15 pdflatex -interaction=nonstopmode -halt-on-error` twice from build/:
both runs exit 0; no `!` errors; no "Missing $" or runaway messages; overfull boxes: 0. Undefined references in the
standalone build are only fd labels and export labels of other sections (ar, cb, lg, ll, mm, sr), as expected.

Declined: none.
