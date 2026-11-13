# LIT: prior work on ES(7), ES(8), symmetric configurations, and SAT/formal approaches

Search date: 21 October 2026. Task: `results/LIT/TASK.md` at 3d83517, budget H = 1.25 h.
A second search, on 6 November 2026, is in §6; where the two differ, §6 is the later record.

**How the sources were read.** In this session arXiv, Semantic Scholar, DBLP, Zenodo,
MathOverflow, Google Scholar and alphaXiv all returned proxy 403 to direct fetches. The only
working channel was the WebSearch tool, which returns titles, URLs and abstract-level snippets.
So for every source below, "read" means the abstract and the snippets the search returned. For
detail beyond the abstract (section-level statements) I rely on the repository's own survey
`docs/RELATED_WORK_2026-10-14.md` and mark such statements "(per the 14 Oct survey)". Every
search is in `searches.tsv`. ES(n) is the least N such that every N points in general position
in the plane contain n points in convex position. Numbers marked "(our arithmetic)" are
evaluations of a published formula, not values stated in the source.

## 1. Known values and bounds of ES(n) for n ≤ 8

| n | value / bounds | source |
|---|---|---|
| 3 | 3 | trivial |
| 4 | 5 | Esther Klein (credited in Erdős–Szekeres 1935) |
| 5 | 9 | Makai and Turán (unpublished, credited in Erdős–Szekeres 1960/61); Kalbfleisch–Kalbfleisch–Stanton 1970; Bonnice 1974 |
| 6 | 17 | Szekeres–Peters 2006 (computer proof); Marić 2019 (Isabelle/HOL); Heule–Scheucher 2024 (SAT, LRAT) |
| 7 | 33 ≤ ES(7) ≤ 113 (published) | lower: Erdős–Szekeres 1960/61; upper: Mojarrad–Vlachos 2016 (n ≥ 6), 113 (our arithmetic) |
| 8 | 65 ≤ ES(8) ≤ 408 (published) | lower: Erdős–Szekeres 1960/61; upper: Mojarrad–Vlachos 2016, 408 (our arithmetic) |

The chain of general upper bounds, evaluated at n = 7, 8 (our arithmetic):

| bound | n = 7 | n = 8 | source |
|---|---|---|---|
| C(2n−4, n−2) + 1 | 253 | 925 | Erdős–Szekeres 1935 |
| C(2n−4, n−2) | 252 | 924 | Chung–Graham 1998 |
| C(2n−4, n−2) − 2n + 7 | 245 | 915 | Kleitman–Pachter 1998 |
| C(2n−5, n−2) + 2 | 128 | 464 | Tóth–Valtr 1998 |
| C(2n−5, n−2) + 1 | 127 | 463 | Tóth–Valtr 2005 |
| Vlachos's appendix bound (n ≥ 6) | 114 | 414 | Vlachos, arXiv:1505.07549 (preprint; per the 14 Oct survey) |
| C(2n−5, n−2) − C(2n−8, n−3) + 2 (n ≥ 6) | **113** | **408** | Mojarrad–Vlachos, DCG 56 (2016) |
| limsup ES(n)/C(2n−5, n−2) ≤ 7/8 | – | – | Norin–Yuditsky, DCG 55 (2016); asymptotic only |
| 2^{n+o(n)}, 2^{n+O(√(n log n))} | – | – | Suk, JAMS 2017; Holmsen–Mojarrad–Pach–Tardos, JEMS 2020; asymptotic only |

Unreviewed and non-journal claims I am aware of:

- Koshelev–Koshka, arXiv:2604.20120 (April 2026), print a table of upper bounds in which the row
  attributed to Norin–Yuditsky reads 92 and 324 at n = 7 and 8 (as reported by the search
  snippet; the column alignment was not visible). Norin–Yuditsky state only a limsup with
  unquantified o(1) terms, so these are not proved finite values; the 14 Oct survey reaches the
  same conclusion.
- Schroeder, Zenodo record 22842891 (19 Sept 2026, per the 14 Oct survey): ES(7) ≤ 81 and
  ES(8) ≤ 319 with a Lean development that uses `native_decide`. I could not reach Zenodo and
  the search engine did not index the record, so I have not read it myself in this session.
- This repository, branch main (commit c019a54): ES(8) ≤ 311, kernel-checked in Lean.

No paper from 2024 to 2026 that settles ES(7), or gives a peer-reviewed bound below 113 / 408,
turned up. B. Dumitru (arXiv:2512.24061, December 2025) states that the case k = 7 is open,
and the erdosproblems.com page for Problem 107 (edited 11 April 2026) lists only the asymptotic
bound.

## 2. Prior computer-assisted and formal work

- **Szekeres–Peters 2006** (ANZIAM J. 48, 151–164): ES(6) = 17, by an exhaustive search over a
  combinatorial model of "signature functions" that contains every realizable configuration.
  Three independent implementations were made, at a cost of roughly 1,500 CPU hours (secondary sources).
- **Marić 2019** (J. Autom. Reason. 62, 301–329): a new representation plus symmetry breaking
  and a SAT solver reduces the ES(6) = 17 proof to about half an hour, and the reduction is
  formalized in Isabelle/HOL.
- **Balko–Valtr 2017** (Eur. J. Combin. 66, 13–23; ENDM 49, 2015): a SAT attack on the
  Erdős–Tuza–Valtr refinement of the conjecture. It refutes a stronger conjecture of Peters and
  Szekeres about red–blue colorings of ordered 3-uniform hypergraphs. Instance generator at
  kam.mff.cuni.cz/~balko/ES_SAT.
- **Scheucher 2023** (Comput. Geom. Topol.; arXiv:2105.08406): a SAT model over acyclic
  chirotopes for Erdős–Szekeres numbers in dimensions 3 to 5 (for example g^(3)(7) = 13).
- **Heule–Scheucher 2024** (TACAS 2024; arXiv:2403.00737): h(6) = 30. Every 30 points in
  general position contain an empty hexagon, via an O(n⁴)-clause CNF solved in about 17,300 CPU
  hours with a checked proof. The paper also re-proves ES(6) = 17 in seconds, and shows that
  every 24 points contain a 6-hole or a 7-gon.
- **Subercaseaux–Nawrocki–Gallicchio–Codel–Carneiro–Heule 2024** (ITP 2024, LIPIcs 35;
  arXiv:2403.17370): Lean 4 verification of the h(6) = 30 encoding, with the LRAT proof checked
  by cake_lpr. About 4.7k lines of Lean; it found and fixed a small error in the original
  symmetry-breaking argument. ES(6) = 17 is also derived (`gon_6_theorem`, per the 14 Oct survey).
- **Dumitru 2025** (arXiv:2512.24061, preprint): a SAT encoding of the 33-point, no-7-gon problem
  (triple-orientation variables, the 4-point convexity criterion, convex-layer anchoring). It
  reports UNSAT certificates for a collection of "anchored subfamilies", with heavy-tailed run
  times. The abstract mentions no symmetry class and no complete case split.
- **Krapivin–Przybocki–Heule 2026** (arXiv:2607.02958, CICM 2026): "satisfiability modulo
  realizability". The largest set avoiding both 6-holes and 7-gons has 23 points. Per the 14 Oct
  survey, none of 200,000 abstract 32-point 7-gon-free solutions was realized.
- **Koshelev–Koshka 2026** (arXiv:2604.20120): SAT/ASP modelling plus "linear subreduction"
  (fixing abscissae so that realization is linear) for colored and empty-polygon variants. New
  exact values include h_nc(4,0;4,0) = 26. Not about ES(7) or ES(8).
- **Damásdi–Dong–Scheucher–Zeng** (SoCG 2024; Eur. J. Combin. 2026; arXiv:2312.01223):
  saturated n-gon-free sets of size (7/8)·2^{n−2} exist for every n ≥ 7, and the
  Erdős–Szekeres construction is saturated. Constructions are checked by computer.
- **Baek–Balko** (SoCG 2025; JCTA 222, 2026): the conjecture holds for decomposable sets, and a
  relaxed "split k-gon" version holds with the threshold 2^{k−2} + 1 (computer-free).

## 3. Prior work on symmetric configurations

- **Subercaseaux–Mackey–Qian–Heule 2025** ("Automated Symmetric Constructions in Discrete
  Geometry", arXiv:2506.00224; CICM 2025): SAT encodings with built-in *rotational* symmetry,
  plus a local-search realizability solver. For 16 points without a convex hexagon, the 3-fold
  formula is UNSAT and the 4- and 5-fold formulas are satisfiable and realizable. For 32 points
  without a convex 7-gon, there is no realizable 4-fold symmetric set. The paper suspects that
  symmetric extremal constructions exist for all k ≥ 7. According to the 14 Oct survey it lists
  two-fold symmetry as future work. The abstract does not mention reflection symmetry, and I did
  not find any reflection or dihedral case in the snippets.
- **Morris–Soltan 2000** (Bull. AMS 37, 437–458): survey. It records symmetric or almost
  symmetric extremal constructions for variants of the problem (for example minimizing convex
  pentagons), and the Lovász form of the 2^{n−2} construction. Its p. 443 also states the
  Erdős–Tuza–Valtr inequality, in a form that is false as printed: "m(n,k,l) ≤
  Σ_{i=n−l}^{k−2} C(k−2, i)", where m(n,k,l) is the least number such that every set of that
  many points in general position contains n points in convex position, a k-cup or an l-cap.
  An n-cup or an n-cap is in convex position, so with k = l = n this would give
  ES(n) ≤ 2^{n−2}, against the lower bound ES(n) ≥ 2^{n−2} + 1 of Erdős–Szekeres 1960/61. The
  intended statement is the lower bound that Erdős, Tuza and Valtr proved by a construction,
  m(n,k,l) ≥ 1 + Σ_{i=n−l}^{k−2} C(n−2, i); they conjectured equality (as relayed by Balko–Valtr
  2015; their 1996 paper itself was not read). The inequality should not be cited from the
  survey. (Checked on 1 November 2026, after the search date above, against the full text of the
  survey; `MIRRORETV/README.md` §8.)
- **Erdős–Szekeres 1960/61; Kalbfleisch–Stanton 1995; Duque–Fabila-Monroy–Hidalgo-Toscano 2017**
  (arXiv:1602.03075): the 2^{n−2}-point construction, its corrected form, and a small-grid
  realization. None of them is about symmetry. Subercaseaux et al. call the classical
  construction asymmetric.
- **Szekeres–Peters 2006**, §5 (per the 14 Oct survey): a purely combinatorial 2^{k−2}
  construction in the signature-function model.

- **Dumitru 2025** (arXiv:2512.24061): the conclusion, as quoted in search snippets, says progress
  depends on stronger anchoring "for the hardest symmetric configurations". Symmetry appears there
  as something to break or anchor, not as a class that is solved.
- **Koshelev–Koshka 2026** (arXiv:2604.20120): per the snippet, a 25-point example with 3-fold
  symmetry for a hexagon-type variant, not for convex 7-gons.
- **Mackey, CMU 5th-year master's thesis, 2025** (csd.cmu.edu announcement): analyses the
  symmetric 16-point sets and describes 32-point 7-gon-free configurations as a larger open
  generalization. The text was not retrieved.

I found no paper on reflection-invariant (mirror-symmetric) point sets without large convex
polygons, none on dihedral symmetry, and none on 3-fold rotational symmetry at 33 points.

## 4. Questions (a) to (c)

**(a) Reflection-invariant 33-point sets contain a convex 7-gon.** We did not find prior work
stating that every set of 33 points in general position invariant under a reflection contains 7
points in convex position. The nearest published results concern other symmetry classes or sizes:
4-fold rotational symmetry at 32 points (Subercaseaux et al. 2025, no realizable 7-gon-free set),
and anchored subfamilies that are not described as symmetry classes (Dumitru 2025). Both are
preprints or proceedings, and neither covers reflections.

**(b) Possible symmetries of a 33-point 7-gon-free set, and the D3 case.** We did not find prior
work stating that a 33-point set in general position with no convex 7-gon can only have a
reflection, a 120° rotation, or both as nontrivial symmetries, and we did not find prior work
excluding the D3 case. The closest known result is the 3-fold UNSAT result for 16 points without
a convex hexagon (Subercaseaux et al. 2025), which is a different (n, k).

**(c) ES(8) ≤ 311.** The best peer-reviewed upper bound we found is Mojarrad–Vlachos 2016,
ES(n) ≤ C(2n−5, n−2) − C(2n−8, n−3) + 2 for n ≥ 6, which gives ES(8) ≤ 408 (our arithmetic). The
best earlier public bound we know of is Schroeder's unreviewed Zenodo record, ES(8) ≤ 319
(September 2026; reported from the 14 Oct survey, not re-read here because Zenodo was
unreachable). The value 324 in Koshelev–Koshka's 2026 table is attributed to Norin–Yuditsky,
whose result is only asymptotic, so it should not be cited as a proved bound. We did not find
prior work stating ES(8) ≤ 311 or any bound below 319. The lower bound ES(8) ≥ 65 is the
classical Erdős–Szekeres construction.

## 5. What someone checking (a) should cite

1. Erdős–Szekeres 1935 and 1960/61: the problem, the conjecture ES(n) = 2^{n−2} + 1 and the lower bound.
2. Morris–Soltan 2000: survey and history (not for the Erdős–Tuza–Valtr inequality, which its
   p. 443 misprints; see §3).
3. Szekeres–Peters 2006 and Marić 2019: ES(6) = 17, computer and formal.
4. Heule–Scheucher 2024 and Subercaseaux et al. ITP 2024: the SAT encoding style, LRAT and
   cake_lpr checking, and Lean verification of an encoding. (a) uses the same trust model
   (cake_lpr verdicts, Lean statements of the encoding).
5. Subercaseaux–Mackey–Qian–Heule 2025: the only prior symmetric SAT study of 7-gon-free sets
   (4-fold, 32 points). It is the closest prior result to (a).
6. Dumitru 2025 and Krapivin–Przybocki–Heule 2026: recent computational work on the 32/33-point
   7-gon problem.
7. Mojarrad–Vlachos 2016, Suk 2017 and Holmsen–Mojarrad–Pach–Tardos 2020: the current upper bounds, for context.
8. Balko–Valtr 2017 and Baek–Balko 2025/2026: the abstract (colouring) models and the classes
   (decomposable sets) already known to satisfy the conjecture.

BibTeX for all of these is in `references.bib`.

## 6. 6 November 2026 search

A read-only novelty check (four literature checks, three adversarial reviews and a synthesis) repeated and extended
the searches above. Unlike on 21 October, direct fetches worked: arXiv abstract and HTML pages, the arXiv API, Zenodo,
PDFs and the GitHub API. Its searches are recorded in that check's session journal, not in `searches.tsv`. Every
statement below that nothing was found is the result of a bounded search, so it is evidence, not proof of absence.

**Read in full** (or the stated part in full):
- Subercaseaux–Mackey–Qian–Heule (SMQH), arXiv:2506.00224v1.
- Mackey, M.S. thesis CMU-CS-25-108 (May 2025).
- Koshelev–Koshka, arXiv:2604.20120v1, including Table 1 and §9.1.2.
- Krapivin–Przybocki–Heule, arXiv:2607.02958v1.
- Georgiev–Gómez-Serrano–Tao–Wagner, arXiv:2511.02864v2: Section 38 only.
- Schroeder's Zenodo preprint: the record page, and PDF pp. 1–3, §8 and Appendix C.
- Tóth–Valtr 2005 (Theorem 1); Mojarrad–Vlachos: abstract and the Theorem 1.1 text of arXiv v2.
- Miyata–Moriyama–Imai, RIMS Kôkyûroku 1641 (2009) 8–15.
- drat-trim issues #31 and #42, pull request #43, and commits cbd2915 and 5cd8ac3 (GitHub API).
- erdosproblems.com Problem 107 and its forum thread.
- GLitchfield/erdos-szekeres-convex-poly: README, theorem statements and commit dates through the GitHub API. It was not
  built.

**Abstract, metadata or snippets only:**
- Dumitru, arXiv:2512.24061: abstract page and version history (one reader also queried the HTML text through a fetch
  tool's summaries). Its §7 and Table 1 were read in full on 4 November (`C6C7REVIEW/LITERATURE.md`).
- Baek, arXiv:2206.04260: abstract page (the full text of v2 was read on 4 November).
- Norin–Yuditsky (abstract; the ar5iv text only through a fetch tool's summary), Vlachos 2015, Heule–Scheucher 2024,
  Marić 2019 (metadata), Fukuda–Moriyama–Nakayama arXiv:math/0510500.
- SMQH's CICM 2025 chapter: Crossref metadata only (LNCS, 2026, pp. 29–47, doi:10.1007/978-3-032-07021-0_3).
- Bokowski–Richter 1990 and Bokowski–Sturmfels 1989: not read; their data come from the reference list of
  Miyata–Moriyama–Imai and a DBLP snippet.

**Not accessed:** the text of SMQH's CICM chapter; a possible ACM TALG version of SMQH (one search snippet, not
confirmed by Crossref); the JCTA version of Baek–Balko; Erdős–Tuza–Valtr 1996; Google Scholar, MathSciNet and zbMATH;
non-English sources beyond a few Russian- and Chinese-language web searches.

**Findings.**

1. **Symmetric sets: still nothing for k = 8.** SMQH reaches k = 7 only: no realizable fourfold 32-point set without a
   convex 7-gon, and a twofold 32-point realization listed as future work. It has nothing on k = 8 and no sixfold or
   sevenfold symmetry, and its realizer "can only determine realizability, not unrealizability" (footnote 2). Mackey's
   thesis covers only 16-point hexagon-free sets (3-, 4- and 5-fold); its §4.1 reports that an attempt at a fourfold
   32-point 7-gon-free set reached 24 realized points. Koshelev–Koshka's symmetric statements concern other forbidden
   configurations (empty hexagons under axial symmetry, k-fold lower bounds for h_mod(6,q)). Krapivin–Przybocki–Heule
   mention symmetry only by citing SMQH. Georgiev et al. (AlphaEvolve, §38) give 2^{k−2}-point sets with no convex
   k-gon for k ≤ 8, with no symmetry stated; a reviewer converted their 65-point set with exactly one convex octagon to exact
   integers and found its distances from the centroid pairwise distinct, so that set has no rotational symmetry; no
   64-point set of theirs was tested for symmetry. arXiv API sweeps (to 4 November),
   Zenodo searches (to 5 November), GitHub searches and about 15 web searches found no work on symmetric octagon-free
   sets and no symmetric 33-point heptagon result. The symmetric literature found still stops at k = 7.
2. **Upper bounds: unchanged.** Mojarrad–Vlachos (DCG 56 (2016), Theorem 1.1, n ≥ 6) is still the peer-reviewed
   record: ES(7) ≤ 113 and ES(8) ≤ 408. Schroeder's Zenodo record 22842891 is still version 1 (19 September 2026); its
   Theorem 1.1 is ES(7) ≤ 81 and ES(8) ≤ 319, not peer reviewed, and its Appendix C lists eight `native_decide`
   axioms for the octagon bound. Koshelev–Koshka's Table 1 lists 92 and 324 at n = 7, 8 in the Norin–Yuditsky row.
   These are not (7/8)·C(2n−5, n−2) (110.25 and 404.25), the paper gives no derivation, and Norin–Yuditsky prove only a
   limsup; so 324 is not a proved bound. This settles the column question left open in §1. The finite Vlachos values
   114 and 414 were checked only against that table. No arXiv or Zenodo item from 2023–2026 other than Schroeder's gives
   an explicit ES(7) or ES(8) bound. Dumitru's preprint (author Bogdan Dumitru per the arXiv metadata; the middle
   initial used earlier was not verified) is still v1 of 30 December 2025 and calls ES(7) open.
3. **Formal work: GLitchfield.** https://github.com/GLitchfield/erdos-szekeres-convex-poly is a public Lean 4
   repository, created 1 August 2026 and last pushed 20 October 2026, described as "Lean formal research on the exact
   Erdos-Szekeres happy-ending conjecture". When it became public is not known. Its theorem statements and commit
   history show a Lean proof of the Tóth–Valtr bound C(2n−5, n−2) + 2 (so ES(8) ≤ 464; committed 14 August 2026, with
   a self-reported audit listing no non-standard axioms), Lean proofs of explicit Suk-type and HMPT-type bounds with
   weaker constants than the published ones (16 and 18 August 2026), and an LRAT-replayed ES(6) = 17 (September 2026).
   So this repository's ES(8) ≤ 311 is not the first Lean-checked or kernel-only bound on ES(8), and its Suk and HMPT
   proofs are not the only formalizations. `docs/RELATED_WORK_2026-10-14.md` lines 1450–1451 ("the only other Lean
   formalization") are wrong on this point.
4. **lrat-check defect: publicly known.** The project's E2 finding (20 October 2026; again in `LRATCHECK20261105`) is
   an independent rediscovery. drat-trim issue #31 (22 July 2022) reported that lrat-check accepts an empty clause
   without a valid derivation; commit cbd2915 (19 October 2022) fixed it; commit 5cd8ac3 (21 April 2024) commented the
   fix out; master is still 2e3b2dc. Issue #42 and pull request #43 (both 29 September 2026, three weeks before E2)
   report the regression with the same reproduction (`p cnf 1 1` / `1 0` with proof `2 0 0` prints `c VERIFIED`) and a
   one-line fix; both were open with no maintainer response on 6 November. No paper on the defect was found. The
   project anchors every certificate on cake_lpr (Tan–Heule–Myreen, TACAS 2021), whose README defines success as the
   output line `s VERIFIED UNSAT` and does not document exit codes.
5. **Chord lemma and certificate methods: classical.** No published statement of the chord lemma (`CHORD20261105`)
   was found, but it is an elementary half-plane fact, and SMQH, Mackey's thesis and Dumitru use no angle-derived
   orientation rules. The non-realizability certificates of `SIX10LINUX20261105` are of classical types:
   - biquadratic final polynomials from the log-magnitude LP: Bokowski–Richter, Eur. J. Combin. 11 (1990) 21–34;
   - pooling them over rotation orbits gives symmetric biquadratic final polynomials, which exist exactly when a
     biquadratic final polynomial does: Bokowski–Sturmfels, *Computational Synthetic Geometry*, LNM 1355, Springer 1989, as stated in Theorem 1.1 of
     Miyata–Moriyama–Imai (the book was not read);
   - SDP certificates of non-realizability for symmetric realization problems: Miyata–Moriyama–Imai 2009;
   - facial reduction: Borwein–Wolkowicz 1981 (catalog records only).

   Models that violate 3-term Grassmann–Plücker relations are not chirotopes at all. Neither the lemma nor the
   certificates are a new result.

BibTeX for Mackey's thesis, Georgiev et al. and Miyata–Moriyama–Imai was added to `references.bib`; Koshelev–Koshka and
Krapivin–Przybocki–Heule were already there. Bokowski–Richter, Bokowski–Sturmfels, Borwein–Wolkowicz, the GLitchfield
repository and the drat-trim tracker are cited inline only.
