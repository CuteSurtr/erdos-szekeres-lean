# LIT: prior work on ES(7), ES(8), symmetric configurations, and SAT/formal approaches

Search date: 21 October 2026. Task: `results/LIT/TASK.md` at 3d83517, budget H = 1.25 h.

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
turned up. Bogdan (arXiv:2512.24061, December 2025) states that the case k = 7 is open, and the
erdosproblems.com page for Problem 107 (edited 11 April 2026) lists only the asymptotic bound.

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
- **Bogdan 2025** (arXiv:2512.24061, preprint): a SAT encoding of the 33-point, no-7-gon problem
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
  pentagons), and the Lovász form of the 2^{n−2} construction.
- **Erdős–Szekeres 1960/61; Kalbfleisch–Stanton 1995; Duque–Fabila-Monroy–Hidalgo-Toscano 2017**
  (arXiv:1602.03075): the 2^{n−2}-point construction, its corrected form, and a small-grid
  realization. None of them is about symmetry. Subercaseaux et al. call the classical
  construction asymmetric.
- **Szekeres–Peters 2006**, §5 (per the 14 Oct survey): a purely combinatorial 2^{k−2}
  construction in the signature-function model.

I found no paper on reflection-invariant (mirror-symmetric) point sets without large convex
polygons, none on dihedral symmetry, and none on 3-fold rotational symmetry at 33 points.

## 4. Questions (a) to (c)

**(a) Reflection-invariant 33-point sets contain a convex 7-gon.** We did not find prior work
stating that every set of 33 points in general position invariant under a reflection contains 7
points in convex position. The nearest published results concern other symmetry classes or sizes:
4-fold rotational symmetry at 32 points (Subercaseaux et al. 2025, no realizable 7-gon-free set),
and anchored subfamilies that are not described as symmetry classes (Bogdan 2025). Both are
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
2. Morris–Soltan 2000: survey and history.
3. Szekeres–Peters 2006 and Marić 2019: ES(6) = 17, computer and formal.
4. Heule–Scheucher 2024 and Subercaseaux et al. ITP 2024: the SAT encoding style, LRAT and
   cake_lpr checking, and Lean verification of an encoding. (a) uses the same trust model
   (cake_lpr verdicts, Lean statements of the encoding).
5. Subercaseaux–Mackey–Qian–Heule 2025: the only prior symmetric SAT study of 7-gon-free sets
   (4-fold, 32 points). It is the closest prior result to (a).
6. Bogdan 2025 and Krapivin–Przybocki–Heule 2026: recent computational work on the 32/33-point
   7-gon problem.
7. Mojarrad–Vlachos 2016, Suk 2017 and Holmsen–Mojarrad–Pach–Tardos 2020: the current upper bounds, for context.
8. Balko–Valtr 2017 and Baek–Balko 2025/2026: the abstract (colouring) models and the classes
   (decomposable sets) already known to satisfy the conjecture.

BibTeX for all of these is in `references.bib`.
