# Related work survey — 14 October 2026

A literature check made while the ES(8) ≤ 312 certificate was being verified.
Statements below are taken from the cited abstracts and papers; claims from
preprints and unreviewed records are marked as such. No priority claim is made.

## Upper bounds for small n

| Source | Bound | Status |
| --- | --- | --- |
| Erdős–Szekeres 1935 | ES(n) ≤ C(2n−4, n−2) + 1 | classical |
| Tóth–Valtr 2005 | ES(n) ≤ C(2n−5, n−2) + 2 | published |
| [Mojarrad–Vlachos 2016](https://arxiv.org/abs/1510.06255) | ES(n) ≤ C(2n−5, n−2) − C(2n−8, n−3) + 2, giving **ES(7) ≤ 113** and **ES(8) ≤ 408** (our arithmetic) | published, Discrete Comput. Geom. |
| [Vlachos 2015](https://arxiv.org/abs/1505.07549) | limsup ES(n)/C(2n−5, n−2) ≤ 29/32 | asymptotic only |
| [Suk 2016](https://arxiv.org/abs/1604.08657), [HMPT 2020](https://arxiv.org/abs/1710.11415) | 2^{n+o(n)}, 2^{n+O(√(n log n))} | asymptotic; no value for n = 7, 8 |
| [Schroeder, Zenodo record 22842891](https://zenodo.org/records/22842891), 19 Sept 2026 | **ES(7) ≤ 81**, **ES(8) ≤ 319**, and the (7,5,6) Erdős–Tuza–Valtr case with 25 points; "formalized in Lean" with native evaluation and "an explicitly documented trust boundary" | public preprint, not peer reviewed; this repository's omission catalogs derive from its version-1 archive |

This repository's kernel-checked ES(8) ≤ 313 (and the pending 312) are below
every bound in this table. The heptagon figure ES(7) ≤ 81 shows that the same
catalog method applies to n = 7; nothing of the kind is attempted here yet.

## Abstract models and why they do not decide ES(7)

- [Balko–Valtr 2015](https://kam.mff.cuni.cz/~balko/ES_SAT) refuted the
  Peters–Szekeres strengthening of the conjecture by SAT: a red–blue coloring
  of the ordered complete 3-uniform hypergraph on **33 vertices with no 7-gon**
  exists in that abstract model (their page lists the coloring).
- [Baek–Balko, SoCG 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13)
  prove `ES_split(k) = 2^{k−2} + 1` for *split* k-gons and show that the
  *weak* k-gon version is also false at 33: `C_weak(7) > 33` (Theorem 7).
  They write that this "suggests that the Erdős–Szekeres Conjecture might be
  false", and that any proof of it must use point sets, not only abstract
  colorings. They could not find a 33-element *signotope* without a 7-gon.
- Consequently a SAT model of 33 points in the signotope setting (the one in
  [experiments/es7-search-2026-10-13](../experiments/es7-search-2026-10-13/README.md))
  may be satisfiable by unrealizable configurations. A SAT answer there is
  evidence only after realization; an UNSAT answer would prove ES(7) = 33.

## Where a counterexample cannot come from

- **Decomposable sets** (Baek–Balko, Theorem 8): sets built recursively by
  placing one part "deep below" another, which include the Erdős–Szekeres
  cup–cap constructions and Horton sets, satisfy the conjecture: every
  decomposable set of more than 2^{k−2} points contains k points in convex
  position. All stacking constructions tested in
  [the ES(8) family record](../experiments/es8-lower-bound-search-2026-10-11/README.md)
  are decomposable. The saturation tests there are stronger in one respect
  (the added point is arbitrary, not restricted to keep decomposability) but
  the theorem already excludes decomposable counterexamples outright.
- **Blow-ups** (same paper, Section 6): a construction generalizing all known
  2^{k−2}-point sets without k-gons; their optimization experiments found no
  larger such sets, even for k = 20.
- **Four-fold rotational symmetry** ([Subercaseaux–Mackey–Qian–Heule 2025](https://arxiv.org/abs/2506.00224)):
  about one CPU-year enumerated 310,187,713 non-isomorphic 4-fold symmetric
  abstract 32-point configurations without convex heptagons; **none is
  realizable**. Two-fold symmetry is listed as future work. Their `Localizer`
  (simulated-annealing realizability solver with exact rational verification)
  realizes order types of about 30 points in seconds.
- **Saturation** ([Damásdi–Dong–Scheucher–Zeng](https://arxiv.org/abs/2312.01223),
  Eur. J. Combin. 2026): for every n ≥ 7 there are saturated sets of only
  (7/8)·2^{n−2} points (no convex n-gon, every added point creates one), and
  the Erdős–Szekeres construction itself is saturated. Saturation of a
  2^{n−2}-point set is therefore expected and is not evidence of extremality
  on its own; the value of the saturation records here lies in the number of
  distinct order types covered, not in saturation as such.

## Computational attacks on 33 points

- [Bogdan, arXiv:2512.24061](https://arxiv.org/abs/2512.24061) (Dec 2025,
  preprint): triple-orientation variables, a 4-set convexity criterion with
  14 selector variables per 4-set (71 clauses), reduced CC-style 5-point
  axioms, and convex-layer anchoring templates with a sub-cubing parameter.
  UNSAT certificates for anchored subfamilies only; single sub-cubes took
  from 2.5 × 10³ s to 2.28 × 10⁶ s, "some subproblems taking weeks". The
  heavy-tailed behaviour matches the cube-and-conquer run recorded here.
- [Scheucher, CGT 2023](https://cgt-journal.org/index.php/cgt/article/view/12):
  the planar g(6) = 17 refutation takes about 10 CPU minutes with CaDiCaL
  plus DRAT checking; higher-dimensional instances needed up to 14 CPU days
  and certificates of hundreds of gigabytes. [Marić 2019](https://link.springer.com/article/10.1007/s10817-017-9423-7)
  formalized ES(6) = 17 in Isabelle/HOL with a verified SAT pipeline in about
  half an hour of solving.
- [Heule–Scheucher 2024](https://arxiv.org/abs/2403.00737) proved the empty
  hexagon number h(6) = 30 with 312,418 cubes and 17,300 CPU hours;
  [Subercaseaux et al., ITP 2024](https://arxiv.org/abs/2403.17370) verified
  the encoding and the LRAT proof in Lean 4 with cake_lpr, noting the
  framework also covers g(6) = 17.
- [Koshelev–Koshka, arXiv:2604.20120](https://arxiv.org/abs/2604.20120)
  (Apr 2026, preprint): SAT/ASP models with a "linear subreduction" that fixes
  abscissae to make realizability constraints linear; results on bicolored
  empty quadrilaterals (26 points) and axially symmetric sets (18 points force
  an empty hexagon).
- [Balko–Scheucher–Valtr 2022](https://arxiv.org/abs/2203.07518): projective
  versions of Erdős–Szekeres-type numbers; arbitrarily large sets without
  projective 8-holes.

## Consequences for this project

1. **Upper bounds.** ES(8) ≤ 313 improves the best published value (408) and
   the unreviewed 319; the heptagon catalog behind ES(7) ≤ 81 is an untried
   target for the same certificate pipeline.
2. **ES(7) searches.** Abstract SAT models cannot refute the conjecture by
   themselves (realizability is needed) and may not be able to prove it
   (unrealizable 33-point signotopes could exist). Realizable-only methods,
   such as the face-extension growth search in `.cache/es7/grow`, and
   symmetric SAT models with a realizability solver (3-fold or 11-fold for 33
   points, 2-fold for 32, none yet reported) are the natural next steps.
3. **Lower-bound evidence.** Decomposable constructions are excluded as
   counterexamples by theorem; future searches should leave that class.
4. **Formalization.** The kernel-checked arithmetic certificates used here
   avoid trusting a SAT solver or native evaluation; the Lean SAT-verification
   toolchain of the empty-hexagon work is an alternative for SAT-based results.
