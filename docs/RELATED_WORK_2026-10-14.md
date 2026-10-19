# Related work survey — 14 October 2026

A literature check made while the ES(8) ≤ 312 certificate was being verified,
extended on the same day with a ten-angle search of the published and preprint
literature (all ten angles are integrated below; a second pass on 14 October
added the proof-technique, opinion, realizability and data angles). Statements
below are taken from the cited abstracts and papers; claims from preprints and
unreviewed records are marked as such. Numeric values derived from a stated
formula are marked "(our arithmetic)". No priority claim is made, and nothing
here asserts a result for this repository beyond what the [README](../README.md)
states: **65 ≤ ES(8) ≤ 311** is proved and kernel-checked (313 on 12 October,
312 on 14 October and 311 on 19 October 2026; see the
[311 record](../experiments/omission-final311-2026-10-14/README.md)), and every
counterexample search so far is negative (the realizable growth search had
tested more than 16,000 heptagon-free 32-point sets by 14 October, all
saturated; the committed [ES(7) record](../experiments/es7-search-2026-10-13/README.md)
lists 8,537 distinct order types as of 13 October).

Notation. ES(n) is the least N such that every N points in general position
contain n in convex position; some sources write N(n), f(n) or g(n) and some
write g(n) for the largest set *without* an n-gon (then g + 1 = ES). h(k) is
the empty-k-gon (k-hole) number. f(k,l) = C(k+l−4, k−2) + 1 is the cups–caps
number. For a triple (n, a, b) the Erdős–Tuza–Valtr quantity
N(n,a,b) = Σ_{i=n−b}^{a−2} C(n−2, i) is the conjectured largest size of a set
with no convex n-gon, no a-cap and no b-cup.

Contents: [Upper bounds](#upper-bounds) · [Lower bounds and extremal sets](#lower-bounds-and-extremal-sets) ·
[Abstract models](#abstract-models-and-why-they-do-not-decide-es7) ·
[Empty polygons and SAT methodology](#empty-polygons-and-transferable-sat-methodology) ·
[Higher dimensions and variants](#higher-dimensions-and-variants) ·
[Proof techniques](#proof-techniques-for-finite-bounds) · [Realizability](#realizability) ·
[Computational data](#computational-data) · [Surveys and expert opinion](#surveys-and-expert-opinion) ·
[Consequences](#consequences-for-this-project) · [Omitted items](#omitted-items)

## Upper bounds

### The general chain, evaluated at n = 7 and n = 8

All values in the two numeric columns are our arithmetic from the stated
formulas. [Tóth–Valtr 2005](https://library.slmath.org/books/Book52/files/30toth.pdf)
reproves every entry up to its own; the 1998 journal data are also collected
on the [UCSD Erdős problems page](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/Convex.html)
(which stops at 2005 and still says the lower bound is known only for n ≤ 5).

| Source | Bound | n = 7 | n = 8 | Status |
| --- | --- | --- | --- | --- |
| Erdős–Szekeres 1935 | C(2n−4, n−2) + 1 | 253 | 925 | classical |
| Chung–Graham 1998 (n ≥ 4) | C(2n−4, n−2) | 252 | 924 | published, DCG 19 |
| Kleitman–Pachter 1998 (n ≥ 4) | C(2n−4, n−2) − 2n + 7 | 245 | 915 | published, DCG 19 |
| Tóth–Valtr 1998 (n ≥ 3) | C(2n−5, n−2) + 2 | 128 | 464 | published, DCG 19 |
| [Tóth–Valtr 2005](https://library.slmath.org/books/Book52/files/30toth.pdf) (n ≥ 5) | C(2n−5, n−2) + 1 | 127 | 463 | published, MSRI 52 |
| [Vlachos 2015](https://arxiv.org/abs/1505.07549) (n ≥ 6, appendix) | C(2n−5, n−2) − C(2n−8, n−5) + C(2n−10, n−7) + 2 | 114 | 414 | arXiv preprint; also limsup ES(n)/C(2n−5, n−2) ≤ 29/32 |
| [Mojarrad–Vlachos 2016](https://arxiv.org/abs/1510.06255) (n ≥ 6) | C(2n−5, n−2) − C(2n−8, n−3) + 2 | **113** | **408** | published, Discrete Comput. Geom.; best published small-n bound |
| [Norin–Yuditsky 2016](https://arxiv.org/abs/1509.03332) | limsup ES(n)/C(2n−5, n−2) ≤ 7/8 | — | — | published, DCG; o(1) terms unquantified, so no value at any fixed n |
| [Suk 2016](https://arxiv.org/abs/1604.08657) (JAMS 2017), [HMPT 2020](https://arxiv.org/abs/1710.11415) (JEMS) | 2^{n+o(n)}, 2^{n+O(√(n log n))} | — | — | asymptotic; no value for n = 7, 8 |
| [Schroeder, Zenodo record 22842891](https://zenodo.org/records/22842891), 19 Sept 2026 | **ES(7) ≤ 81**, **ES(8) ≤ 319**, and the (7,5,6) Erdős–Tuza–Valtr case with 25 points; "formalized in Lean" with native evaluation and "an explicitly documented trust boundary" | 81 | 319 | public preprint, not peer reviewed; this repository's omission catalogs derive from its version-1 archive |
| **This repository** | ES(8) ≤ 311, kernel-checked 19 Oct 2026 (312 on 14 Oct, 313 on 12 Oct) | — | **311** | see [README](../README.md) and the [311 record](../experiments/omission-final311-2026-10-14/README.md) |

Remarks on the table.

- Mojarrad–Vlachos's Theorem 1.1 is stated for n ≥ 6 (the abstract omits the
  restriction); (7/16)·C(2n−4, n−2) = 110.25 and 404.25 is only its asymptotic
  shape and is not a bound at n = 7, 8. Likewise (7/8)·C(2n−5, n−2) = 110.25
  and 404.25 (our arithmetic) are *not* valid bounds: Norin–Yuditsky's proof is
  non-inductive and its error terms are not made explicit. The correct
  published comparison for ES(8) ≤ 311 is therefore 408, not 404. Schroeder's
  footnote 1 (Zenodo record, unreviewed) notes that Koshelev–Koshka's table
  lists 92 and 324 under Norin–Yuditsky and that he "has not located their
  finite derivation"; the deleted "mate" set Q′ of that proof (at most
  |P|/(n−2) points) is exactly the term a finite derivation would have to
  account for, so 92/324 should not be cited as proved values.
- No paper from 2021–2026 improving the HMPT exponent, and no unconditional
  small-n bound below 113/408 other than Schroeder's unreviewed record, was
  found. [Conlon–Fox–He–Mubayi–Suk–Verstraëte 2024](https://arxiv.org/abs/2405.03455)
  (preprint) still uses HMPT as the current upper bound.
- [Bogdan, arXiv:2512.24061](https://arxiv.org/abs/2512.24061) (Dec 2025,
  preprint) gives no numeric ES(7) bound, cites only Suk and HMPT, and states
  that "the case k = 7 remains open". The 2025 SAT literature therefore
  contains no published competitor to a heptagon catalog at n = 7.

This repository's kernel-checked ES(8) ≤ 311 (and the earlier 312 and 313) is below
every bound in this table. The heptagon figure ES(7) ≤ 81 shows that the same
catalog method applies to n = 7; nothing of the kind is attempted here yet.

### Conditional bounds by convex-hull shape

[Strunk 2013](https://link.springer.com/article/10.1007/s00454-012-9474-9)
(Discrete Comput. Geom. 49; the title "Two Upper Bounds for the Erdős–Szekeres
Number with Conditions" is sometimes misattributed to Koshelev) uses the
Tóth–Valtr projective method for n ≥ 4. Theorem 1: C(2n−5, n−2) − 2n + 9
points force a convex n-gon if no point lies inside a triangle of three
consecutive hull vertices (121 at n = 7, 455 at n = 8). Corollary 3: if the
hull is an (n−1)-gon, C(2n−5, n−2) − 2n + 10 points suffice (122 / 456).
Theorem 2 (hull an (n−1)-gon, s points inside a consecutive-vertex triangle):
C(2n−5, n−2) − n − Σ_{i=1}^{n−4} min{i, s} + 6 (125 / 460 at s = 0). Only the
abstract was read. These are the only published hull-shape case analyses after
Tóth–Valtr; they gain at most about 2n − 9 over the unconditional bound, so a
catalog method is a qualitatively different tool.

### The Erdős–Tuza–Valtr refinement

[Erdős–Tuza–Valtr 1996](https://doi.org/10.1006/eujc.1996.0045) (Eur. J.
Combin. 17; text not retrieved, statement taken from Baek 2022 and Baek–Balko
2025, which agree) conjecture that for 2 ≤ a, b ≤ n ≤ a+b−2 the largest set
with no convex n-gon, no a-cap and no b-cup has N(n,a,b) = Σ_{i=n−b}^{a−2}
C(n−2, i) points, prove the matching construction, and prove the conjecture
equivalent to ES(n) = 2^{n−2} + 1 (monotone in a, b for fixed n). Trivially
true when n ≥ a+b−3 (cups–caps). The known cases are:

- a = 4 or b = 4, every n: [Baek 2022/2024](https://arxiv.org/abs/2206.04260)
  (Eur. J. Combin. 124, 104085): any C(n−1, 2) + 2 points with distinct
  x-coordinates and no three collinear contain a 4-cap or a convex n-gon;
  "the first new case since 1935". The proof is for a purely combinatorial
  model and is formalized in Lean 4 in
  [jcpaik/erdos-tuza-valtr](https://github.com/jcpaik/erdos-tuza-valtr)
  (`theorem main`: E(n,4,n) ≤ C(n−1,2) + 2; cups–caps in `Main/CapCup.lean`;
  Apache-2.0). Values: 17 points at n = 7, 23 at n = 8 (our arithmetic). This
  repository already ports that development; see
  [THIRD_PARTY.md](THIRD_PARTY.md). The paper's tools are weak (a,b)-gons (a
  cap and a cup sharing both endpoints), slope labels in {1,2} for 4-cap-free
  sets, an injective (α,β) statistic into a triangular grid and "interweaved
  laced" (n−1)-cups; its Conjecture 5 says C(n−1,2) + k points force k
  mutually interweaved laced (n−1)-cups (proved for k = 1, 2, n). Baek's
  [2018 KAIST seminar abstract](https://mathsci.kaist.ac.kr/~sangil/seminar/tag/백진언)
  records the state before his proof: ETV(4,n,n) = C(n+1,2) + 1 "must hold if
  the ES conjecture does" but was unverified, the best bound C(n+2,2) − 1 was
  due to Balko–Valtr 2015, and Suk's argument adapts to C(n+2,2) − C√n.
- (7,5,6) with 25 points: Schroeder's Zenodo record (unreviewed); 25 is
  exactly the ETV value, so the claim is "ETV holds at (7,5,6)". His
  Theorem 5.2 states that 26 points force a 5-cap, a 6-cup or a convex
  heptagon, over a 35-state universe [4]×[3] with 9 missing states,
  C(33,9) − C(31,7) = 35,937,525 eligible hole sets, a CNF of 461 variables
  and 93,169 clauses and an LRAT proof of 381,647 additions; the heptagon
  certificates use the (cup, cap) state convention and the octagon ones
  (cap, cup), which matters when importing catalogs.
- Everything else with 5 ≤ a, b is open ([Baek–Balko 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13)
  state the formula "is known to be true only in the trivial case k ≥ a+u−3 and
  Baek proved it when a or u equals 4").

Conjectured maxima N(n,a,b), our arithmetic from the formula, as targets for
cup–cap–polygon catalogs:

| n = 7 | value | n = 8 | value |
| --- | --- | --- | --- |
| (7,7,7) | 32 | (8,8,8) | 64 |
| (7,6,7) | 31 | (8,7,8) | 63 |
| (7,6,6) | 30 | (8,7,7) | 62 |
| (7,5,7) | 26 | (8,6,7) | 56 |
| (7,5,6) | 25 | (8,6,6) | 50 |
| (7,4,7) | 16 (proved, Baek) | (8,5,8) | 42 |
| | | (8,5,7) | 41 |
| | | (8,4,8) | 22 (proved, Baek) |

Vlachos's intermediate functions are of the same kind: Theorem 4 of
[Vlachos 2015](https://arxiv.org/abs/1505.07549) says f(n−1,n−1) + g(n,n−2) + 1
points contain an n-cup, an (n−1)-cap or a convex n-gon (n ≥ 6), with g built
from explicit weights w_i(m,l) counting "good" points (left endpoints of short
caps); Mojarrad–Vlachos's h(m,4) ≤ C(m−1, 2) + 1 (Theorem 3.4) is numerically
Baek's threshold, so the two auxiliary functions should be compared before any
novelty claim about cap-restricted catalogs.

### Interior-point variants

[Koshelev 2009](https://arxiv.org/abs/0910.2700) (arXiv survey of his
Russian-journal papers; journal pages unreachable) defines h(n,k) as the
forcing number for a convex n-gon with at most k interior points and proves
h(6,1) ≤ g(7) ≤ 127 via Tóth–Valtr (Theorem 2; Conjecture 2: h(6,1) = 17) and,
for n ≥ 6, h(n, C(n−3, ⌈(n−3)/2⌉) − ⌈n/2⌉) > 2^{n−2} + 1 (Theorem 4). Any
improvement of ES(7) improves h(6,1) through Theorem 2: if the conjecture
holds the inequality reads h(6,1) ≤ g(7) = 33, and Schroeder's unreviewed
ES(7) ≤ 81 would already give h(6,1) ≤ 81 against the published 127 (our
inference from the stated inequality). Koshelev–Koshka 2026 (preprint) later
settled h(6,1) = 18 by ASP; see the SAT section. His claimed h(6) ≤ 463 is
discussed under empty polygons.

## Lower bounds and extremal sets

### The 2^{n−2} construction and its correct form

- [Erdős–Szekeres 1960/61](https://users.renyi.hu/~p_erdos/1960-09.pdf)
  (Ann. Univ. Sci. Budapest 3–4; scan read via OCR) first constructs the
  cups–caps extremal set S_{k,l} of C(k+l−4, k−2) points and the
  2^{n−2}-point set S = ∪ S_k with slope bands such that a convex polygon meets
  the middle blocks in one point each, giving at most n − 1 points; it states
  the conjecture f_0(n) = 2^{n−2} ("We are unable to prove or disprove this
  conjecture") and credits n = 4 to Klein and n = 5 to Makai and Turán
  (unpublished).
- [Morris–Soltan 2000](https://kam.mff.cuni.cz/~chvatal/MorSol00.pdf)
  (Bull. AMS 37) record that the 1961 proof had "some inaccuracies" corrected
  by Kalbfleisch–Stanton (Utilitas Math. 47, 1995; only the
  [zbMATH record](https://api.zbmath.org/v1/document/_search?search_string=au%3AKalbfleisch%20ti%3Aconvex&results_per_page=20)
  is online), and present the clean Lovász form: blocks T_i with C(n−2, i)
  points, no (i+2)-cap and no (n−i)-cup, all slopes of absolute value ≤ 1,
  placed near unit-circle points at angles π/4 − iπ/(2(n−2)); a convex set
  meets T_k in a cap of ≤ k+1 points, T_l in a cup of ≤ n−l−1 points and each
  intermediate block in ≤ 1 point. Section 5.3 notes the Kalbfleisch–Stanton
  coordinates "grow very quickly".
- [Duque–Fabila-Monroy–Hidalgo-Toscano 2016/17](https://arxiv.org/abs/1602.03075)
  (DCG) realize the Erdős–Szekeres construction on an integer grid of size
  O(n² log³ n) for n = 2^{t−2} points, the natural form for exact integer
  certificates.
- [Szekeres–Peters 2006](https://archive.austms.org.au/Publ/ANZIAM/V48P2/2409.html)
  (ANZIAM J. 48), Section 5, give a purely combinatorial version: for
  n = 2^{k−2} there is a signature function with no convex k-subset, so the
  extremal construction lives in the abstract model and an abstract witness at
  2^{k−2} carries no information; only a 2^{k−2} + 1 witness would.
- [Fox–Pach–Sudakov–Suk 2012](https://arxiv.org/abs/1105.2097) (Proc. LMS):
  N_3(2,n) = C(2n−4, n−2) + 1 exactly for 2-colored ordered triples, so the
  cups–caps bound is tight even without any geometry; all improvements of
  ES(n) must use the interaction between the polygon condition and cups/caps.

### Structure of extremal sets

- [Hirata–Katayama 1998](https://ehime-u.repo.nii.ac.jp/records/2158)
  (Bull. Fac. Educ. Ehime Univ. 19(1), 1–4; [PDF](https://ehime-u.repo.nii.ac.jp/record/2158/files/AN00024797_1998_19_1-1.pdf);
  OCR of a scan, Theorems 3.2–3.3 partly garbled): by Bonnice's layer types
  an 8-point pentagon-free set is of type (4,4), (4,3,1), (3,4,1) or
  (3,3,2), Bonnice's Lemma 2.2 excludes (4,3,1) and (3,3,2), and every
  remaining set has a "convex quadrilateral cell decomposition" (an inner
  quadrilateral plus four outer quadrilaterals, Theorem 3.1); Theorems
  3.2–3.3 give converse sufficient conditions and Theorem 4.1 re-proves
  ES(5) = 9. The first 8-point examples are credited to
  Kalbfleisch–Kalbfleisch–Stanton 1970. Extremal 2^{k−2}-sets are therefore
  not unique already at k = 5. No analogous classification of hexagon-free
  16-sets or heptagon-free 32-sets was found, and no order-type counts are
  published (see [Computational data](#computational-data) for what the
  Aichholzer database would allow).
- [Baek–Balko 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/LIPIcs.SoCG.2025.13/LIPIcs.SoCG.2025.13.pdf)
  (SoCG 2025; journal version [JCTA 222 (2026) 106195](https://doi.org/10.1016/j.jcta.2026.106195)),
  Section 6: an (X,Y)-blow-up replaces each interior point p_i of a set S by a
  rotated cup–cap-free block P'(y_i+2, x_i+2); Lemma 14 gives the linear
  constraints (x_i + y_i ≤ k−1; x_i + y_j ≤ k−1−s_{i,j} for i < j, with s_{i,j}
  the longest convex chain from p_i to p_j). All known 2^{k−2} constructions
  are blow-ups (x_i = i−1, y_i = k−i−1 on k−1 points reproduces an
  unpublished construction of Valtr); Section 6.2 gives a genuinely new family
  (Theorem 19) from a (2m−2)-point set M; a MATLAB genetic optimizer never
  exceeded 2^{k−2} up to k = 20.
- [Damásdi–Dong–Scheucher–Zeng](https://arxiv.org/abs/2312.01223) (Eur. J.
  Combin. 2026): the explicit 8-point (4,5)-cup–cap-saturated set
  {(−60,40), (−40,20), (−20,16), (0,10), (5,−50), (15,−40), (25,−40),
  (125,−230)} is checked by a SageMath face-enumeration script, the same
  primitive as a realizable growth search; sat_c(4,4) = 6, sat_c(4,5) = 8
  versus ram_c(4,5) = 10; saturated n-gon-free sets of size
  2^{n−2} − 2^{n−5} = (7/8)·2^{n−2} exist for all n ≥ 7 (56 points at n = 8,
  28 at n = 7, our arithmetic).
- [Horton 1983](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/sets-with-no-empty-convex-7gons/0E7C17D71D9FA4A08B265441FBEB32D7)
  (Canad. Math. Bull. 26): S_k = {(i, d(i))} with c = 2^k + 1 and d(i) built
  from the binary expansion of i has no empty convex 7-gon. Horton sets are
  decomposable and contain large non-empty convex polygons, so they are
  useless as ES counterexample seeds but cheap structured test inputs.

### Where a counterexample cannot come from

- **Decomposable sets** (Baek–Balko, Theorem 8): sets built recursively by
  placing one part "deep below" another, which include the Erdős–Szekeres
  cup–cap constructions and Horton sets, satisfy the conjecture: every
  decomposable set of more than 2^{k−2} points contains k points in convex
  position (more precisely, more than Σ_{i=k−a+2}^{u} C(k−2, i−2) points force
  an a-cap, a u-cup or k points in convex position). All stacking
  constructions tested in
  [the ES(8) family record](../experiments/es8-lower-bound-search-2026-10-11/README.md)
  are decomposable. The saturation tests there are stronger in one respect
  (the added point is arbitrary, not restricted to keep decomposability) but
  the theorem already excludes decomposable counterexamples outright.
- **Blow-ups** (same paper, Section 6): a construction generalizing all known
  2^{k−2}-point sets without k-gons; their optimization experiments found no
  larger such sets, even for k = 20. A 33-point counterexample must therefore
  be neither decomposable nor a blow-up satisfying Lemma 14.
- **Four-fold rotational symmetry** ([Subercaseaux–Mackey–Qian–Heule 2025](https://arxiv.org/abs/2506.00224),
  preprint): about one CPU-year enumerated 310,187,713 non-isomorphic 4-fold
  symmetric abstract 32-point configurations without convex heptagons; the
  inner 12 points admit only 6 configurations and **none is realizable**.
  Two-fold symmetry is listed as future work. Their `Localizer`
  (simulated-annealing realizability solver with exact rational verification)
  realizes order types of about 30 points in seconds. For 16 points without a
  hexagon: 3-fold UNSAT; 4-fold 66 abstract solutions, 18 realizable (9
  non-isomorphic); 5-fold about 940 solutions, 92 realizable (46
  non-isomorphic).
- **Abstract order types without a 7-gon on 32 points**
  ([Krapivin–Przybocki–Heule 2026](https://arxiv.org/abs/2607.02958), CICM
  2026, preprint): 200,000 SAT solutions of the 32-point, no-7-gon instance
  were passed to `Localizer` with partial-realization feedback; **none was
  realized** in 2,191 core hours (mean 121.6 violated orientations).
- **Saturation** ([Damásdi–Dong–Scheucher–Zeng](https://arxiv.org/abs/2312.01223),
  Eur. J. Combin. 2026): for every n ≥ 7 there are saturated sets of only
  (7/8)·2^{n−2} points (no convex n-gon, every added point creates one), and
  the Erdős–Szekeres construction itself is saturated. Saturation of a
  2^{n−2}-point set is therefore expected and is not evidence of extremality
  on its own; the value of the saturation records here lies in the number of
  distinct order types covered, not in saturation as such.
- **Relaxations.** [Tóth–Valtr 2005](https://library.slmath.org/books/Book52/files/30toth.pdf)
  note that even for families of pairwise disjoint convex sets the best lower
  bound is still the point bound 2^{n−2}; no published relaxation suggests a
  mechanism for beating 2^{n−2} in the plane. No machine-learning search
  (PatternBoost, FunSearch, RL) targeting ES counterexamples was found.

## Abstract models and why they do not decide ES(7)

### The models

[Szekeres–Peters 2006](https://archive.austms.org.au/Publ/ANZIAM/V48P2/2409.html)
define Σ_n (all sign functions on ordered triples, no axioms) and Σ*_n (signs
obeying the realizable 4-point patterns: along σ(abc), σ(abd), σ(acd), σ(bcd)
at most one sign change, 8 of 16 patterns). Σ* is the rank-3 signotope model
([Baek–Balko](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13),
citing Felsner–Weil), equivalently x-monotone pseudoline arrangements,
pseudo-configurations, CC-systems and acyclic rank-3 chirotopes
([Scheucher 2023](https://cgt-journal.org/index.php/cgt/article/view/12);
[Dobbins–Holmsen–Hubard 2014](https://arxiv.org/abs/1305.2266)). Knuth's
9-point non-realizable example lies in Σ*, so Σ* is strictly larger than the
realizable sets. Polygon notions in colorings
([Baek–Balko](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13)):
a *split* k-gon is a red a-path and blue u-path (a + u = k + 2) sharing only
the rightmost vertex; a *weak* k-gon shares both end-vertices and may share
others; a *strong* k-gon (Peters–Szekeres) shares only the two ends. In
signotopes every weak k-gon is strong, so a signotope SAT model need only
forbid strong k-gons. Theorems 5–7 of Baek–Balko impose no consistency axiom
at all. In Szekeres–Peters's original formulation an ε-chain (cup or cap)
requires only its *consecutive* triples to have sign ε, a k-subset is "convex
relative to σ" iff it is a cup–cap pair with common endpoints and total
length k, and the four-point "packet" rule (2.3) is the same as the clauses
forbidding the sign subsequences 101 and 010 in Schroeder's and this
project's encodings; (P_{σ,5}) on 5 points is proved there by an eight-step
combinatorial implication chain, and each of the 892 "concave" 6-point
signatures is compatible with at most 18 others. Transitivity is the
abstract axiom behind all of this: [Fox–Pach–Sudakov–Suk](https://arxiv.org/abs/1105.2097)
(Section 6) call a k-uniform family transitive if edges {i_1..i_k} and
{i_2..i_{k+1}} force all k-subsets of {i_1..i_{k+1}}, and Lemma 6.2 says a
transitive ordered k-graph containing a monotone n-path is complete on it,
which is why a monotone path of cups is a clique of cups.

### Status by model and k

| Model | k ≤ 5 | k = 6 | k = 7 | k = 8 | Source |
| --- | --- | --- | --- | --- | --- |
| Pure colorings Σ, strong k-gon | holds (Peters–Szekeres, k = 5 exhaustive) | open after 266 h of Glucose on 17 vertices (a = u = 6) | **fails**: 33-vertex coloring with no 7-gon | **fails**: 65 vertices | [Balko–Valtr 2015](https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf), [data page](https://kam.mff.cuni.cz/~balko/ES_SAT) |
| Pure colorings, weak k-gon | — | — | **fails**: C_weak(7) > 33 | — | Baek–Balko Thm 7 |
| Pure colorings, split k-gon | holds for all k: C_split(k,k,k) = 2^{k−2} + 1 | | | | Baek–Balko Thm 6 |
| Signotopes / acyclic chirotopes | holds | **holds**: every 17-element 3-signotope has a strong 6-gon (Szekeres–Peters; chirotopes with DRAT, Scheucher) | **open**; no 33-element witness found by Baek–Balko, by Balko–Valtr, or by this project's SAT runs | open | as cited |
| Realizable point sets | 5, 9 | 17 | 33 ≤ ES(7) ≤ 81 (unreviewed) / 113 (published) | 65 ≤ ES(8) ≤ 311 (this repository) | |

Known abstract upper bounds are weak: C_weak(k) ≤ C_strong(k) ≤ C(2k−4, k−2) + 1
(253 at k = 7, 925 at k = 8, our arithmetic; Baek–Balko), and for
pseudo-configurations g(n) ≤ C(2n−5, n−2) + 1 (127 / 463, our arithmetic;
Dobbins–Holmsen–Hubard extend the Tóth–Valtr proof). Nobody has narrowed
these: C_strong(7) ≤ 253 leaves the whole range 34..253 open in the pure
model, and no values of C_weak or C_strong are given even for k ≤ 6. For
n ≤ 6, f = g = h_0 = h_1 = 2^{n−2} + 1 (DHH), so the abstract / realizable
split can only begin at n = 7. [HMPT 2020](https://arxiv.org/abs/1710.11415)
remark that none of the inequalities in the chain
2^{n−2} + 1 ≤ e(n) ≤ c(n) ≤ c′(n) = b(n) is known to be strict, so an
abstract (pseudo-configuration) 33-point counterexample would be a new
result before any realization.

### ETV thresholds in the abstract models

The [Balko–Valtr data page](https://kam.mff.cuni.cz/~balko/ES_SAT) stores
colorings at N = 17 (no red 4-path, 7-gon), 23 (4-path, 8-gon), 26 (5-path,
blue 6-path, 7-gon), 27 (5-path, 7-gon), 30 (4-path, 9-gon), 31 (6-path,
6-path, 7-gon), 32 (6-path, 7-gon), 33 (7-gon). Each N is exactly 1 + the
conjectured ETV value (16, 22, 25, 26, 29, 30, 31, 32; our arithmetic), so in
the axiom-free model every listed case fails precisely at threshold, including
(7,4,7) and (7,5,6). Restricted to pseudolinear (signotope) colorings the
conjectured values hold in every tested case: N(4,7,7) = 16 and N(4,8,8) = 22,
and "none of the counterexamples is pseudolinear". The first separation between
the pure and signotope models is therefore (4,7,7): 17 versus 16. Baek's
theorem is false for pure colorings, so any proof of an ETV case with
5 ≤ a, b — including the (7,5,6) = 25 claim — must use 4-point consistency,
not cup/cap counting alone.

- [Balko–Valtr 2015](https://kam.mff.cuni.cz/~balko/ES_SAT) refuted the
  Peters–Szekeres strengthening of the conjecture by SAT: a red–blue coloring
  of the ordered complete 3-uniform hypergraph on **33 vertices with no 7-gon**
  exists in that abstract model (their page lists the coloring, with a C++
  generator taking (a,u,k,N) to DIMACS). [Baek's generator](https://github.com/jcpaik/erdos-szekeres-sat)
  (Kissat, `python main.py n a b N`) is the companion to Baek–Balko.
- [Baek–Balko, SoCG 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13)
  prove `ES_split(k) = 2^{k−2} + 1` for *split* k-gons and show that the
  *weak* k-gon version is also false at 33: `C_weak(7) > 33` (Theorem 7).
  They write that this "suggests that the Erdős–Szekeres Conjecture might be
  false", and that any proof of it must use point sets, not only abstract
  colorings. They could not find a 33-element *signotope* without a 7-gon, and
  state that the signotope version of the conjecture is equivalent to a
  conjecture of Goodman and Pollack (Congr. Numer. 32, 1981, not retrieved;
  the conjecture f(n) = g(n) is also the subject of DHH 2014).
- Consequently a SAT model of 33 points in the signotope setting (the one in
  [experiments/es7-search-2026-10-13](../experiments/es7-search-2026-10-13/README.md))
  may be satisfiable by unrealizable configurations. A SAT answer there is
  evidence only after realization; an UNSAT answer would prove ES(7) = 33 and,
  because the signotope model is the Goodman–Pollack setting, also the
  Goodman–Pollack conjecture at k = 7 and (through
  [DHH 2014](https://arxiv.org/abs/1305.2266)) the Bisztriczky–Fejes Tóth
  convex-body conjecture at 7.

### Monotone paths and transitive colorings

The cup–cap number is exactly realized in several abstract settings, which is
why no cup/cap-only catalog can beat C(2n−4, n−2) + 1:
[Fox–Pach–Sudakov–Suk 2012](https://arxiv.org/abs/1105.2097) (N_3(2,n));
[Moshkovitz–Shapira 2014](https://arxiv.org/abs/1206.4001) (Adv. Math.;
N'_3 = N_3 for transitive colorings, multicolor values counted by
high-dimensional partitions); [Balko 2019](https://arxiv.org/abs/1905.06000)
(JCTA; 3-monotone colorings). [Eliáš–Matoušek 2013](https://arxiv.org/abs/1111.3824)
generalize cups/caps to k-th-order monotone tuples, where the abstract and
geometric bounds already match at k = 3. Surveys of the ordered-Ramsey side:
[Balko 2025](https://arxiv.org/abs/2502.02155) (preprint; Section 3.1 maps
ES(n) ≤ R_<(MP^(3)_n) = C(2n−4, n−2) + 1 and lists nothing on k-gons beyond
Balko–Valtr and Baek–Balko), [Gishboliner–Jin–Sudakov 2023](https://arxiv.org/abs/2308.04357)
(off-diagonal and polynomial regimes), [Suk–Zeng 2024](https://arxiv.org/abs/2411.15649)
(preprint; a 3-uniform monotone-path number equivalent to the multicolor
triangle Ramsey number). [Cordovil–Duchet 2000](https://www.math.tecnico.ulisboa.pt/~rcordov/eujc0317.pdf)
(Eur. J. Combin. 21) give the oriented-matroid form: a subset is in convex
position iff its induced chirotope is alternating in some order; the only
bound there is Ramsey-type.

## Empty polygons and transferable SAT methodology

### Exact hole numbers

h(3) = 3, h(4) = 5, h(5) = 10 (Harborth 1978, Elem. Math. 33; statement via
[Bhattacharya–Das](https://arxiv.org/abs/1108.3895)), h(6) = 30, h(k) = ∞ for
k ≥ 7 ([Horton 1983](https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/sets-with-no-empty-convex-7gons/0E7C17D71D9FA4A08B265441FBEB32D7)).
The hexagon chain: Gerken 2008 (DCG 39; details via the
[Erdős problems page](https://fanchung.ucsd.edu/erdosprb/erdos/newproblems/EmptyConvex.html)
and Scheucher) proved that a convex 9-gon forces a 6-hole, hence
h(6) ≤ g(9) ≤ 1717, sharp in that an 8-gon does not suffice;
[Nicolás 2007](https://portal.mardi4nfdi.de/entity/Q2464368) independently
gave h(6) ≤ g(25); Valtr 2008 simplified Gerken to h(6) ≤ g(15) (secondary,
via [Scheucher 2023](https://cgt-journal.org/index.php/cgt/article/view/12));
[Koshelev 2007/2009](https://mathnet.ru/eng/mais52) claimed
h(6) ≤ max{g(8), 400} = 463, but Scheucher's footnote 1 states the 50-page
Russian paper "suddenly stops" and the proof is incomplete, so 463 should not
be cited as established (with ES(8) ≤ 311 it would still read 400, our
arithmetic, moot after h(6) = 30). The Erdős problems page still shows 463 and is stale.
[Overmars 2003](https://research-portal.uu.nl/en/publications/sets-without-empty-convex-6-gons/)
(DCG 29) found the 29-point 6-hole-free set by local search with an exact
incremental checker; its layers are 3, 4, 7, 7, 7, 1 and it has no 8-gon.

### The h(6) = 30 pipeline, in detail

[Heule–Scheucher 2024](https://arxiv.org/abs/2403.00737) (TACAS 2024) proved
h(6) = 30 with 312,418 cubes and 17,300 CPU hours;
[Subercaseaux–Nawrocki–Gallicchio–Codel–Carneiro–Heule, ITP 2024](https://arxiv.org/abs/2403.17370)
verified the encoding and the LRAT proof in Lean 4 with cake_lpr, noting the
framework also covers g(6) = 17. Transferable details:

- Variables o_{a,b,c} (orientation), c_{i;a,b,c} (containment), h_{a,b,c}
  (3-hole); a 6-hole is one 20-literal clause per 6-subset. Signotope-style
  axioms on non-realizable 4-patterns cut the space from 2^{Θ(n³)} to
  2^{Θ(n²)}. The trusted encoding has O(n⁶) clauses; auxiliaries u⁴, v⁴, u⁵
  give an O(k·n⁴) encoding with the same propagation power (one subproblem:
  1,171,942 clauses / 243 s versus 444,238 clauses / 39 s). Automatic
  bounded-variable addition was "extremely slow".
- Symmetry breaking: x-sorted points, p₁ extremal with p₂…p_n counterclockwise
  (unit clauses o_{1,a,b}), reflection broken by a lexicographic predicate
  whose "main purpose is to halve the number of cubes". The choice of the
  first hull point is *not* broken: "breaking it can potentially reduce the
  search space by at least a factor of 3 … we therefore left it on the table".
- Cubes: assignments to consecutive o_{a,a+1,a+2} of length ℓ = 21, with no
  three consecutive true and no four consecutive false; each alternating
  (+,−,+) pattern is split further on o_{b,b+2,b+4}, which brought the hardest
  cubes under an hour. The off-the-shelf splitter March (depth 13) was about
  ten times worse than no partitioning. CaDiCaL 1.9.3 with
  `--sat --reducetarget=10 --forcephase --phase=0`; LRAT piped concurrently to
  cakeLPR; 180 TB of LRAT (DRAT estimated 78 TB). g(6) ≤ 17 solves in 8.53 s
  with 1,108 cubes at ℓ = 12.
- Theorem 2: 24 points force a 6-hole or a 7-gon; "All known point sets
  witnessing h(6) ≥ 30 contain a 7-gon." Table 2 for that instance shows the
  total time is non-monotone in the cube length: ℓ = 21 → 312,418 cubes,
  606.55 CPU h; ℓ = 15 → 7,393 cubes, 231.27 CPU h (best); ℓ = 7 → 57 cubes,
  521 CPU h, longest cube 105,938 s; unpartitioned ≈ 1,000 CPU h. Appendix B:
  "millions of signotopes on 23 elements with no 7-gon and no 6-hole", all
  tested ones non-realizable by bi-quadratic final polynomials.
- Section 6.4: for n = 29 with ℓ = 22, 581,428 cubes of which 116,305 (20.00%)
  were satisfiable, every first solution having the Overmars layer sizes;
  adding one structural clause per cube made all UNSAT, proving every
  6-hole-free 29-point set has exactly 3 hull points and ≥ 4 on the second
  layer — a classification route that yields the 30-point bound.
- Lean side (ITP 2024): `hole_6_theorem`, `gon_6_theorem`, a six-step
  `symmetry_breaking` proof (rotate to distinct x, translate, projective map
  (x,y) ↦ (y/x, 1/x), sort, reflect, restore the point at infinity), which
  also corrected an error in Heule–Scheucher's transformation; the CNF's
  unsatisfiability is *asserted as an axiom* discharged by cake_lpr
  (25,876.5 CPU hours on Bridges-2, about 50% above the original run because
  of proof logging); ≈ 4.7k LOC, ≈ 300 person-hours; g(6) = 17 encoder < 1 s
  and solve 28 s versus 787 s for Marić's CNF. Future work: formalize Horton's
  h(7) = ∞; the authors are "optimistic" about an eventual resolution of
  g(7). Repository: [EmptyHexagonLean](https://github.com/bsubercaseaux/EmptyHexagonLean).

### Other SAT encodings of Erdős–Szekeres-type problems

- [Szekeres–Peters 2006](https://archive.austms.org.au/Publ/ANZIAM/V48P2/2409.html):
  signature functions with the 8-of-16 quadruple rule; 892 "concave" 6-point
  signatures, 446 independent top-level assignments each taking 1–20 hours on
  < 2 GHz workstations, ≈ 3,000 GHz-hours in all; 20,312,212 partial
  signatures survived the U₁₃ check and 23,339 the one-bit check; three
  independent implementations (one by B. McKay). The 9-point / 5-gon case runs
  in under a second.
- [Marić 2019](https://link.springer.com/article/10.1007/s10817-017-9423-7)
  (J. Autom. Reasoning 62; [institutional record](https://research.matf.bg.ac.rs/handle/123456789/597?mode=full))
  formalized ES(6) = 17 in Isabelle/HOL with a verified SAT pipeline in about
  half an hour of solving (≈ 1 GHz hour); points indexed by hull-peeling depth
  with 5-tuple axioms; O(n⁶) clauses; relied on an unverified encoder. The
  Isabelle sources were not located online.
- [Scheucher 2020](https://arxiv.org/abs/1807.10848) (two disjoint 5-holes;
  CGTA): the cleanest documented planar signotope encoding — orientation
  variables with cyclic/swap clauses, 4-tuple axioms forbidding −+− and +−+,
  auxiliaries for 4-gons, point-in-triangle and 5-holes; 825,689 constraints
  on 23,392 variables; without injecting Harborth's h(5) = 10 on every window
  of 10 consecutive points "none of the tested solvers terminated within
  days"; glucose 4.0 ≈ 2 h solve + 2 h drat-trim (3.1 GB certificate); 15
  points force two interior-disjoint 5-holes, 17 force two with disjoint
  hulls. [Bhattacharya–Das 2013](https://arxiv.org/abs/1108.3895) prove 19
  points force two disjoint empty pentagons and H(4,5) = 12.
- [Scheucher, CGT 2023](https://cgt-journal.org/index.php/cgt/article/view/12):
  the planar g(6) = 17 refutation takes about 10 CPU minutes with CaDiCaL
  plus DRAT checking; higher-dimensional instances needed up to 14 CPU days
  and certificates of hundreds of gigabytes. Acyclic chirotopes encoded with
  3-term Graßmann–Plücker relations (Θ(n^{r+2}) clauses); a k-gon excluded by
  one clause per k-subset via a triangulation at the leftmost point; no
  symmetry breaking. Gerken's h(6) ≤ g(9) re-proved with 14 instances
  (3.8 GB) in ≈ 1 CPU hour, valid for acyclic rank-3 chirotopes. "Acyclic
  chirotopes on n = 29 points without 6-holes were found within a few minutes,
  but for n = 30 the computations did not terminate within months" — the
  regime before cube-and-conquer.
- [Bogdan, arXiv:2512.24061](https://arxiv.org/abs/2512.24061) (Dec 2025,
  preprint): triple-orientation variables, a 4-set convexity criterion with
  14 selector variables per 4-set (71 clauses), reduced CC-style 5-point
  axioms, and convex-layer anchoring templates with a sub-cubing parameter.
  UNSAT certificates for anchored subfamilies only; single sub-cubes took
  from 2.5 × 10³ s to 2.28 × 10⁶ s, "some subproblems taking weeks". The
  heavy-tailed behaviour matches the cube-and-conquer run recorded here.
  Exact sizes: 5,456 orientation + 572,880 selector variables; 2,905,320
  convexity clauses, 4,272,048 seven-set clauses of length 280, 9,493,440
  partial 5-point clauses, 16,670,808 in all before hull constraints; Kissat
  via PySAT, single thread; no proof format, hardware or coverage reported.
  Finished UNSAT layer vectors (hull-layer sizes, H = anchored points):
  (6,6,6,3,6,6) H = 33; 3¹¹ H = 33; (3,3,4,3,3,6,6,5) H = 33; 5⁶ H = 30;
  4⁸ H = 32; (4,3,4,4,4,4,4,4) H = 31; (4,3,3,5,4,6,3,4) H = 32;
  (3,5,3,5,3,3,5,5) H = 32; (3,4,3,4,4,3,4,4,3) H = 32. Open vectors are not
  listed, nor the total number of layer profiles or total CPU time; summing
  the 13 listed rows gives ≈ 7.0 × 10⁶ s ≈ 81 days (our arithmetic). The
  companion repository [esc-paper](https://github.com/bogdan27182/esc-paper)
  holds only a README and `es_sat_gen.py` (PySAT → DIMACS; `--n`, `--k`,
  `--layers`, `--offsets`, `--no-hull`, `--count-only`; no license shown),
  with no point sets, layer-template files or UNSAT certificates. The
  280-literal 7-gon clauses and partial 5-point axioms give far weaker
  propagation than the O(n⁴) signotope encoding.
- [Subercaseaux–Mackey–Qian–Heule 2025](https://arxiv.org/abs/2506.00224)
  (preprint): orientation variables unified along orbits of a permutation
  (e.g. four 4-cycles on 16 points), dynamic ordering variables giving ≈ 43·n⁴
  clauses, 112·C(n,4) collinearity clauses, convex-layer and quadrant unit
  clauses, Sinz cardinality constraints, enumeration with a modified
  allsat-cadical; `Localizer` is C with simulated annealing and an
  exponentially shrinking move radius, exact rational verification in Python,
  every realizable order type with n ≤ 10 solved in < 50 ms on 8 threads of an
  M1 MacBook Pro. Each thread starts from uniform random points in [0,1]²,
  picks a point with probability proportional to its unsatisfied triple
  constraints and moves it inside a shrinking ball, threads share a top-K
  leaderboard, and a move costs O(n²); the previous local-search realizer
  "could not solve any instance with n = 30 in less than a minute". Localizer
  cannot prove unrealizability and does not handle collinear points. For the
  16-point symmetric runs the text gives 948 five-fold assignments in one
  place and 932 in another (the code README says 932); Appendix C lists
  integer coordinates for one 4-fold and one 5-fold hexagon-free 16-point
  set, and some unrealized assignments were certified non-realizable through
  a known unrealizable 10-point subset. For the 32-point run the outer 28
  points were often realizable while the six inner-12 configurations never
  were; the paper does not say how their non-realizability was established
  (exact certificate or heuristic failure), so the 4-fold case is closed only
  up to that step. Code:
  [automatic-symmetries](https://github.com/bsubercaseaux/automatic-symmetries);
  the CICM 2025 venue is stated in the repository. A 2025 CMU master's thesis
  by Mackey ([announcement](https://csd.cmu.edu/calendar/5th-year-masters-thesis-presentation-ethan-mackey),
  text not retrieved) analyses the 4-gon and 5-gon statistics of the realized
  16-point sets. (The 3-fold / 11-fold suggestion below is this project's,
  not the paper's.)
- [Krapivin–Przybocki–Heule 2026](https://arxiv.org/abs/2607.02958) (CICM
  2026, preprint; code [PointSAT](https://github.com/andrewkrapivin/PointSAT),
  MIT): "satisfiability modulo realizability" — SAT over abstract order types
  (CaDiCaL/Kissat with scrambled formulas), `Localizer` as a 15-second
  realizability oracle, partial-realization feedback (orientations of the best
  point set added as unit clauses) and a flippability heuristic dropping
  flippable variables (2.0% of triples on 23 points); no unrealizability
  lemmas are learned. Main theorem: the largest set avoiding both 6-holes and
  7-gons has exactly 23 points (1,727 core hours of cube-and-conquer on 128
  cores for the 3-point-hull lemma; 2,326 core hours, 174,450 abstract
  solutions, 1,035 realized for the construction). Ablation: 42 of 6,494
  abstract solutions realized with both heuristics, 3 / 8 with one, 0 with
  neither. Table (core hours / abstract solutions / realized): 23 points, no
  6-hole and no 7-gon → 200,000 / 423; 26 points, no 5-cap / no 7-gon →
  1,193 / 200,000 / 32; 29 points, no 6-hole → 3,433 / 18,806 / 4 (about 858
  core hours per realization); 32 points, no 7-gon → 2,191 / 200,000 /
  **0**. An initial 23-point attempt realized none of more than 37,000
  abstract solutions before the heuristics were added. The flippable-triple
  fraction is 0.9% on the 32-point instance (2.0% on 23 points) and the mean
  number of violated orientations of the best partial realization 121.6
  versus 12.2, which the authors summarize as the method "does not scale well
  beyond about 30 points"; the abstract solutions showed 29 convex-layer
  profiles against 17 among realized ones (most common (3,4,4,6,5,1)). The
  realizability oracle is Localizer's local search; the paper does not state
  an exact rational re-check of its own, so any realization taken from it
  should be re-verified exactly. Ships `7gon-32.cnf`,
  `6hole-29-compact.cnf`, `7gon-6hole-23-compact.cnf` and
  `7gon-no-5-cap-no-sb-26.cnf`, with `.or` (orientation) and `.real`
  (realization) outputs.
- [Koshelev–Koshka, arXiv:2604.20120](https://arxiv.org/abs/2604.20120)
  (Apr 2026, preprint): SAT/ASP models with a "linear subreduction" that fixes
  abscissae to make realizability constraints linear; results on bicolored
  empty quadrilaterals (26 points) and axially symmetric sets (18 points force
  an empty hexagon; this last claim was not located in the retrieved text and
  should be re-verified). Variables for colour, orientation, "outside
  triangle" and "≤ q interior points"; Kissat 4.0.4, MiniSat, Glucose, Z3,
  clingo. Results include h(6,≥2) = 17 (ASP, 70 min at n = 17) and
  h(6,1) = 18 (190 min at n = 18) as Theorem 1, h(4,0;3,0) = 26,
  20 ≤ h(4,0;4,3) ≤ 21, 23 ≤ h(4,0;4,2) ≤ 25; they also correct a
  miscitation, stating that Nyklová's h(6,5) ≤ 19 is only an upper bound
  (the KAM preprint read for this survey states h(6,5) = 19; the two sources
  disagree and the point was not resolved here). Realizability data
  (Table 2): all signotopes with N ≤ 8 are realizable; of 1,937,396 abstract
  10-point signotopes in their family, 165,048 (≈ 8.5%, our arithmetic) are
  realized with uniform abscissae x_i = i and 729,588 (≈ 37.7%) with an
  exponential grid; the "linear subreduction" fixes the abscissae so that
  the orientation predicates become linear in the y-coordinates and Z3
  searches all admissible signotopes at once, at the stated price that fixed
  abscissae may exclude realizations (so UNSAT there is not a
  non-realizability proof). They know no case where the realizable value is
  smaller than the signotope value because all maximal signotopes are
  non-realizable. Code and coordinates:
  [koshelevv/Erdos-Szekeres](https://github.com/koshelevv/Erdos-Szekeres);
  they state that Scheucher's original project repository is unavailable.
- [Balko–Scheucher–Valtr 2022](https://arxiv.org/abs/2203.07518) (DCG 72,
  2024): projective versions of Erdős–Szekeres-type numbers; arbitrarily large
  sets without projective 8-holes. Also: ES^p(k) = k for k ≤ 5, ES^p(6) = 9
  (Harborth–Möller, re-verified by SAT), ES^p(7) ≥ 18, and
  2^{k − c log k} ≤ ES^p(k) ≤ 2^{k + c'√(k log k)}; projective convex position
  is strictly weaker than affine, so any projective reduction must track the
  line at infinity so that cups and caps stay affine objects.

### k-gon / k-hole interplay and counting

- [Nyklová 2003](https://kam.mff.cuni.cz/kamserie/clanky/2000/s498.pdf)
  (Studia Sci. Math. Hungar. 40; KAM preprint read): h(n,k) is the forcing
  number for a convex n-gon with ≤ k interior points; h(6,7) = h(6,6) = ES(6)
  = 17 and h(6,5) = 19; h(n,k) does not exist for k below roughly 2^{n/4}
  (Horton sets).
- [Bárány–Valtr 2004](https://www.renyi.hu/~barany/cikkek/97.pdf) (Studia
  Sci. Math. Hungar. 41): sets with only ≈ 1.6195 n² empty triangles,
  1.9396 n² empty quadrilaterals, 1.02 n² empty pentagons and 0.2 n² empty
  hexagons; even hole-minimizing sets have Θ(n²) 6-holes.
- [Aichholzer et al. 2015](https://publications.ist.tugraz.at/files/publications/geometry/afghhhuvv-okkps-15.pdf)
  (CGTA 48): table of bounds on the minimum numbers of k-holes, including
  h_6(n) ≥ n/229 − 4 (Valtr, derived from Koshelev's 463 and inheriting its
  caveat; the proceedings version used Gerken's 1717 for ⌊(n−1)/858⌋ − 2);
  convex-position sets maximize k-holes for large n; Horton sets have Ω(n³)
  k-holes.
- [Aichholzer–Balko–Hackl–Kynčl–Parada–Scheucher–Valtr–Vogtenhuber 2020](https://arxiv.org/abs/1703.05253)
  (JCTA 173): h_5(n) = Ω(n log^{4/5} n) via a computer-checked structural
  lemma about 5-holes crossed by a separating line; superseded by
  [Astudillo-Marbán–Solé-Pi 2026](https://arxiv.org/abs/2603.18484)
  (preprint): Ω(n^{20/11}) 5-holes without computer assistance.
- [Suk–Zhou 2026](https://arxiv.org/abs/2606.05721) and
  [Andričík–Dományová–Džavoronok–Džuklevski–Šafránek 2026](https://arxiv.org/abs/2606.08762)
  (both preprints): the maximum number of k-holes in a set with no (k+1)-hole
  is between (c₁/k)^{⌊k/3⌋} n^{⌊k/3⌋} and (c₂/k)^{⌈k/2⌉} n^{⌈k/2⌉}; for
  n = k + a with a ≤ k/2 − 1 the maximum is exactly 2^a.
- [Valtr 1992](https://link.springer.com/article/10.1007/BF02187831) (DCG 7):
  Horton sets of every size and perturbed lattice sections without 7-holes of
  diameter Θ(√n); dense grids contain large convex polygons, so 7-hole-free
  and 7-gon-free sets live far apart.
- [Bergold–Orthaber–Scheucher–Schröder 2024/26](https://arxiv.org/abs/2409.01723)
  (GD 2024): Gerken's theorem generalizes to convex drawings, so the
  9-gon ⇒ 6-hole implication is valid at the signotope level.
- Peripheral 2026 items: [Džuklevski et al.](https://arxiv.org/abs/2505.15366)
  (Theoret. Comput. Sci. 1077; Maker–Breaker empty-polygon games) and
  [Aichholzer–Bergold–Fink–Löffler–Schnider–Tkadlec 2026](https://arxiv.org/abs/2603.05339)
  (EuroCG preprint; the empty monochromatic convex 4-hole question of
  Devillers–Hurtado–Károlyi–Seara remains open).

## Higher dimensions and variants

- Small values ([Morris–Soltan 2000](https://kam.mff.cuni.cz/~chvatal/MorSol00.pdf),
  Section 4): N_d(n) = n for n ≤ d+1; N_d(d+2) = d+3; N_d(n) = 2n − d − 1 for
  d+2 ≤ n ≤ ⌊3d/2⌋+1 (Bisztriczky–Soltan); N_3(6) = 9. Conjecture 4.2:
  N_d(n) = 4·N_d(n−d) − 3 beyond that range (for d = 2 equivalent to
  ES(n) = 2^{n−2} + 1); it predicts N_3(7) = N_4(8) = N_5(9) = 13 (our
  arithmetic). Károlyi's recursion N_d(n) ≤ N_{d−1}(n−1) + 1 gives
  N_d(n) ≤ C(2n−2d−1, n−d) + d.
- [Scheucher 2023](https://cgt-journal.org/index.php/cgt/article/view/12):
  g^{(3)}(7) = 13, g^{(4)}(8) ≤ h^{(4)}(8) ≤ 13, g^{(5)}(9) ≤ h^{(5)}(9) ≤ 13,
  h^{(3)}(7) ≤ 14, all sharp for acyclic chirotopes and matching Conjecture
  4.2 at its first unknown entries; the abstract witnesses were mostly
  non-realizable (bi-quadratic final polynomials), one rank-4 12-point witness
  was realized with integer coordinates: the 12 points of R³ with no convex
  7-gon are {(526,446,232), (0,756,64), (612,660,342), (708,638,193),
  (546,563,134), (616,622,174), (414,0,370), (548,594,151), (884,1334,722),
  (452,668,180), (587,659,156), (579,692,0)}. A rank-4 chirotope on 18
  elements without 8-holes took 100 CPU days to find. The supplemental data
  were at `page.math.tu-berlin.de/~scheuch/suppl/ES/highdim/` (root 404 on
  14 Oct 2026). The arXiv version is [arXiv:2105.08406](https://arxiv.org/abs/2105.08406)
  (2021, revised 2022; EuroComb 2021 extended abstract).
- Peripheral variants (one line each). [Suk–Zeng 2022/26](https://arxiv.org/abs/2211.15968)
  (CPC 35; SoCG 2023): the largest general-position subset guaranteed in N
  points of R^d with no d+2 on a hyperplane is < N^{1/2 + 1/(2d) + o(1)}
  for odd d and < N^{1/2 + 1/(d−1) + o(1)} for even d (containers) —
  general, not convex, position. [Balko–Bhore–Martínez-Sandoval–Valtr 2020](https://www.sciencedirect.com/science/article/pii/S0195669820300780)
  (Eur. J. Combin.; abstract snippets only): k-convex sets (a polygonization
  meeting every line in ≤ k components) of size Ω(log^k n) exist in every
  n-point set, and there are arbitrarily large 3-convex sets whose largest
  convex subset has O(log n) points, so this relaxation loses the 2^{k−2}
  barrier entirely, unlike split k-gons. [Károlyi–Tóth 2012](https://portal.mardi4nfdi.de/entity/Q452006)
  (DCG 48; review summary only): forbidding a fixed order type with ≥ 4
  points and triangular hull puts the forcing number for a convex n-gon into
  one of three growth classes (linear, polynomial, exponential); the
  thresholds were not retrieved. [Károlyi 2001](https://www.renyi.hu/~barany/cikkek/85.pdf)
  (Discrete Appl. Math. 109; via Bárány–Károlyi Theorem 5): for k > d ≥ 3
  and N large every N-point set in R^d partitions into convex subsets of
  size ≥ k, so the Ramsey remainder vanishes in dimension ≥ 3 and the planar
  remainder phenomenon has no higher-dimensional analogue.
- [Pohoata–Zakharov 2022](https://arxiv.org/abs/2208.04878) (preprint):
  ES_d(n) = 2^{o(n)} for every d ≥ 3 (error term n / log₍₅₎ n), disproving
  the Morris–Soltan prediction ES_d(n) = Ω(2^{2n/d}) implied by Conjecture 4.2
  — the recursion holds at small n and fails asymptotically. Lower bound
  ES_d(n) ≥ 2^{c_d n^{1/(d−1)}} by
  [Károlyi–Valtr 2003](https://link.springer.com/doi/10.1007/s00454-003-0009-4)
  (DCG; via secondary sources). Their R³ cups/caps via edge projections is the
  only higher-dimensional cup–cap argument found.
- [Bukh–Chao–Holzman 2021](https://arxiv.org/abs/2007.08972) (CPC): arbitrarily
  large sets in R^d with no ℓ-hole for ℓ = O(4^d d log d).
- Collinearity relaxations. [Conlon–Fox–He–Mubayi–Suk–Verstraëte 2024](https://arxiv.org/abs/2405.03455)
  (preprint): (3ℓ−1)·2^{n−5} < ES_ℓ(n) < ℓ²·2^{n+C√(n log n)} for the least N
  forcing ℓ collinear points or n in convex position (at ℓ = 3 the lower bound
  is 2^{n−2}, our arithmetic), with a three-parameter cups–caps theorem.
  [Furukawa 2025](https://arxiv.org/abs/2501.03645) (preprint): in R^d,
  ES_d(l,n) ≤ (l−d−1)·C(ES_d(n)−1, d) + ES_d(n) via a maximal general-position
  subset, and a warning that projection does not commute with collinearity
  constraints. [Furukawa 2024](https://arxiv.org/abs/2409.03122) (preprint):
  lines with a concurrency parameter, ES_L(l,n) ≤ c(n+l−1)·C(2n−4, n−2).
- Lines and flats. [Bárány–Roldán-Pensado–Tóth 2013/15](https://arxiv.org/abs/1307.5666):
  for lines, 2·C(n−4, ⌈n/2⌉−1)² ≤ ES_l(n) ≤ C(2n−4, n−2), the dual cups–caps
  number is again C(k+l−4, k−2) + 1, and ES_l(6) ≥ 15 with upper bound 70.
  [Bárány–Kalai–Pór 2021/22](https://arxiv.org/abs/2103.13185) (DCG):
  N(k,d,n) for k-flats exists and reduces to planar ES through generic
  sections, so any small-n improvement of ES(n) improves N(k,d,n) when
  d − k = 2.
- Convex bodies and pseudo-configurations. [Dobbins–Holmsen–Hubard 2014](https://arxiv.org/abs/1305.2266)
  (Mathematika 60): g(n) = h_1(n) and 2^{n−2} + 1 ≤ f(n) ≤ h_0(n) ≤ h_1(n) =
  g(n) ≤ C(2n−5, n−2) + 1; [HMPT 2020](https://arxiv.org/abs/1710.11415)
  extend Suk's bound to pseudo-configurations and hence to disjoint and
  non-crossing convex bodies; [Fox–Pach–Sudakov–Suk 2012](https://arxiv.org/abs/1105.2097)
  give 2^{n² log n} for bodies sharing ≤ 2 boundary points.

## Proof techniques for finite bounds

- **Projective reduction plus cup–cap counting** ([Tóth–Valtr 2005](https://library.slmath.org/books/Book52/files/30toth.pdf)):
  send a hull vertex x to a point x' below which no line of the other points
  passes, so every (n−1)-cap of P' \ {x'} extends to a convex n-gon; then
  P'' has no (n−1)-cap and no n-cup, and the Chung–Graham partition into right
  endpoints of (n−2)-caps (A, |A| ≤ C(2n−6, n−3)) and the rest
  (B, |B| ≤ C(2n−6, n−2)), with equality forced and a largest-slope argument,
  yields the +1. Mojarrad–Vlachos's Theorem 4.3 (ES(n) ≤ p(n) + 1, where p(n)
  forces an (n−1)-cap or a convex n-gon) is the same reduction. The exact
  construction: a point y outside conv(P) so close to the hull vertex x that
  no line through two points of P \ {x} meets the segment xy, a line ℓ
  through y missing conv(P), and a projective map T sending ℓ to infinity
  and xy to the vertical half-line below x′; then every m-cap of
  Q′ = P′ \ {x′} extends by x′ to a convex (m+1)-gon, so Q′ has no n-cup and
  no (n−1)-cap and |Q′| ≤ f(n−1, n) − 1 = C(2n−5, n−2). Observation 1 (the
  junction lemma): a point that is rightmost of a cap and leftmost of a cup
  extends one of them. The equality case is structured: every b ∈ B starts an
  (n−1)-cup ending in A and every a ∈ A ends an (n−2)-cap starting in B, the
  same "balanced equality" analysis as the catalog exclusions below.
  Kleitman–Pachter's "vertical" sets satisfy the recurrence
  f_v(n,m) ≤ f_v(n−1,m) + f(n,m−1) − 2 and f_v(n,m) ≤ C(n+m−4, n−2) + 7 − n
  − m, which is sharp, bounding what pure cup–cap counting can add. This is
  the ancestor of the omission method described in [OMISSION.md](OMISSION.md).
- **The omission skeleton** ([Schroeder, Zenodo 22842891](https://zenodo.org/records/22842891),
  unreviewed; full v1 PDF read): ES(n) ≤ C_n + D_n + 2 for n ≥ 6 (Theorem
  3.2), where C_n = M_n(n−1, n−1) is the *balanced* maximum (no (n−1)-cap, no
  (n−1)-cup, no n-gon) and D_n the *residual* maximum (no (n−2)-cap, no
  n-gon, no point both ending an (n−2)-cup and starting an (n−3)-cap).
  Steps: (i) Proposition 2.1, the projective reduction with the explicit map
  T_t(x,y) = ((x−t)/(y+t²), 1/(y+t²)) after moving a hull vertex to the
  origin, after which the root is leftmost and all its triples are cups, so
  ES(n) ≤ Q_n + 2 with Q_n the largest size avoiding an (n−1)-cap and an
  n-gon; (ii) the residual partition by the slope-minimizing partner p(x):
  U = {x : p(x) > x} has no (n−2)-cap, L = {x : p(x) < x} no (n−1)-cup, the
  junction points G ⊂ U are moved so that H = L ∪ G is balanced and
  R = U \ G residual; (iii) Lemma 3.1, the "three-chain bridge", is
  Norin–Yuditsky's Claim 3.3 with eight terminal cases tabulated. Heptagon:
  D_7 ≤ M_7(5,6) + 5 via a ≤ 5-point set meeting every six-cup (Theorem
  4.3), M_7(5,6) = 25 (Theorem 5.2), C_7 ≤ 49 (Proposition 5.6; primary
  formula 151,801 variables and 4,017,399 clauses, proof 1,989,465 additions
  with 84,721,022 hints, compact source 190,932 clauses), total
  49 + 30 + 2 = 81. Octagon: C_8 ≤ 193 (Proposition 7.2; 252 down-sets of
  [5]², 2,685 "hereditary convex" cyclic families of sizes 8/9/10
  (1,584/780/321) each of admissible capacity 7 by Lemma 6.3, a weighted
  omission tree of 1,590 branches and depth 14 assuming ≤ 58 holes with
  minimum margin 21, hence ≥ 59 holes); D_8 ≤ 124 (Proposition 7.6; a
  154-state universe = the 210 down-sets of [4]×[6] minus the 56 with maximal
  cell (1,6); 1,187 omission rows = 1,164 hereditary-convex families with
  demand |K| − 7 plus 23 "four-cap block images" of demand 6 using Baek's
  theorem that 23 points force a 4-cap or an octagon; tree of 7,314 branches,
  depth 21, minimum margin 1, hence ≥ 30 holes); ES(8) ≤ 193 + 124 + 2 = 319.
  Proposition 7.4, D_n ≤ C(2n−6, n−4) − C(2n−8, n−5), is the general
  residual baseline and with the cup–cap bound for C_n recovers
  Mojarrad–Vlachos exactly. Trust: `es7_le_81` / `es8_le_319` over
  `Finset (ℝ × ℝ)`, axioms propext, Classical.choice, Quot.sound plus 19
  (heptagon) and 8 (octagon) `native_decide` axioms; Lean 4.32.0-rc1; 208
  modules; full rebuild 1,290 s on ARM64 macOS; `ConvexPosition` proved
  equivalent to Mathlib's `ConvexIndependent`. Section 9 gives floors
  C_7 ≥ 30, D_7 ≥ 26 (a checked 26-point residual example), C_8 ≥ 62 and
  D_8 ≥ 50 (via M_8(6,6) ≥ 50), so the additive bound cannot go below 58
  (n = 7) or 114 (n = 8); under ETV, C_8 = 62 and D_8 ≤ 57. "Hereditary
  convexity" and "four-cap compression" appear to be the author's coinages;
  no citation, discussion or second record of the preprint was found (19
  views, 9 downloads on the record). This repository's 312 proof uses the
  same skeleton with the balanced bound lowered to 189 and the residual to
  121 (1 + 189 + 121 = 311), kernel-checked without `native_decide`.
- **Right-endpoint and word labellings.** [Norin–Yuditsky](https://arxiv.org/abs/1509.03332)
  label each point by words over {α,β} and {γ,δ} from the longest cups/caps
  ending or starting at it (Lemma 2.2 / Corollary 2.3: pairwise distinct in
  a (k+2,l+2)-free set, giving a bijective, Seidenberg-style proof of
  ES′(k+2, l+2) ≤ C(k+l, k)); Theorem 3.1 is the Tóth–Valtr reduction to
  (n, n−1)-free sets; Lemma 3.2: no point both ends an (n−1)-cup and starts
  an (n−2)-cap; Claims 3.3–3.4: points ending an (n−2)-cup and starting both
  an (n−2)-cap and an (n−1)-cup each have a "mate", and the mate set Q′ with
  |Q′| ≤ |P|/(n−2) is deleted; Claim 3.6: R_i ∈ R(δ*γ) ⇒ L_i ∈ L(β*αα) with
  |L(β*αα)| = (1/8 + o(1))·C(2n−5, n−2). This is a finite state space of size
  ≈ C(2n−5, n−2), the language in which the project's state catalogs can be
  described; the deletion of Q′ is the non-explicit term that blocks a
  finite-n value.
- **Down-set (Ferrers) state labelling.** [Moshkovitz–Shapira 2014](https://arxiv.org/abs/1206.4001)
  (Adv. Math. 262) prove N_3(q,n) = P_{q−1}(n) + 1, where P_d(n) counts
  d-dimensional partitions in an n × … × n box with entries ≤ n, i.e.
  N_3(q,n) − 1 is the number of down-sets of [n]^{q−1} (q = 2 gives
  C(2n,n) + 1 in their convention, in which a path of length n has n+2
  vertices; q = 3 uses MacMahon's product formula). The pigeonhole proof
  labels each pair u < v by (1 + n_b, 1 + n_w), the longest black and white
  monotone paths ending with that edge, and each vertex by the down-set
  generated by its labels; equal down-sets at u < v are impossible because
  some t < u would extend a monochromatic path through {t,u,v}. This is the
  origin of the Ferrers/down-set states used by Schroeder ("down-set
  encodings of ordered paths are established machinery") and by this
  repository's catalogs, whose state counts are the binomials
  C(a+b−4, a−2). [Conlon et al. 2024](https://arxiv.org/abs/2405.03455)
  (preprint) reuse the same lattice L(m−2, n−2) without general position:
  f_ℓ(m,n) ≤ c(min{m−1,n−1} + ℓ)·C(m+n−4, n−2) and
  f_ℓ(m,n) > ((ℓ−1)/2)·C(m+n−4, n−2) − ((ℓ−3)/2)·C(m+n−6, n−3), the largest
  antichain min{m−1, n−1} controlling how many states one collinear point
  can absorb.
- **Good points and subadditivity.** Vlachos's "(m,4)-good" points and the
  weights w_i(m,l); Mojarrad–Vlachos's Lemma 3.3 h(m+1,l+1) ≤ h(m+1,l) +
  h(m,l+1) with base cases h(m,4) ≤ C(m−1,2) + 1, h(4,l) ≤ C(l−1,2) + 1 and
  Theorem 3.6 h(m,l) ≤ C(m+l−4, l−2) − C(m+l−6, l−3).
- **Convex-layer case analysis.** Bonnice's nested-hull types prove ES(5) = 9
  (Lemma 2.8 in Morris–Soltan: types (3,3,2), (4,3,1), (3,4,2) force a
  pentagon); Bonnice remarked that for n = 6 a 17-point set can have 70 layer
  tuples so the approach "can hardly be applied". Marić's hull-depth indexing,
  Strunk's hull-shape conditions and Bogdan's anchoring templates are the
  same decomposition; the project's finite state catalogs are the modern
  replacement.
- **Polygon ⇒ hole implications** (Gerken, Valtr, Scheucher) are purely
  combinatorial and valid for acyclic rank-3 chirotopes; so is Károlyi's
  central-projection recursion in higher dimensions.
- **Ramsey remainder.** [Bárány–Károlyi 2001](https://www.renyi.hu/~barany/cikkek/85.pdf)
  (LNCS 2098) record rr(k) (points left over after partitioning a large set
  into convex polygons of size ≥ k): rr(3) = 0, rr(4) = 1,
  rr(k) ≥ 2^{k−2} − k + 1 (so rr(7) ≥ 26, our arithmetic), and Open Problem 4
  rr(k) = 2^{k−2} − k + 1, whose solution "could make an essential step to
  settle" the conjecture. The 1996 ETV paper's primary object was this
  remainder: per the zbMATH review (R. Faudree; [Erdős bibliography entry](https://emis.univie.ac.at/classics/Erdos/cit/85805073.htm);
  full text not retrieved) rr(k) is the least r such that every large set in
  a class splits into "regular" sets of size ≥ k plus ≤ r leftovers, with
  rr(k) = (k−1)(k−2) = r(k, k−1) − 1 for posets (regular = chain or
  antichain), rr(k) = r_{c,k}(k) − 1 for c-coloured complete r-uniform
  hypergraphs, and a sharp planar value conditional on the Erdős–Szekeres
  conjecture. Károlyi 2001 (see Higher dimensions) shows rr = 0 in R^d for
  d ≥ 3. The partition side was carried further by
  [Pór–Valtr 2002](https://kam.mff.cuni.cz/kamserie/clanky/2002/s598.pdf)
  (DCG 28; KAM preprint read): any finite X in general position minus at
  most c′(k) = f(k) − 1 points (optimal; rr(k) − 1 for large |X|) is a union
  of at most c(k) = k^{O(k²)} convex k-clusterings (k equal-size parts with
  every transversal a convex k-gon), while the best lower bound on c(k) is
  exponential; Bárány–Károlyi's Theorem 4 (Károlyi) says 4N points split into
  N vertex-disjoint convex quadrilaterals iff no odd subset meets every
  convex quadrilateral evenly, with F_4(n) ≥ 5n/22, F_5(n) ≥ n/10,
  F(n) ≤ 5n/18.
- **Why the positive-fraction and partition methods are silent at n = 7, 8.**
  [Suk 2017](https://arxiv.org/abs/1604.08657) (JAMS 30; full text read):
  Theorem 2.4, taken from the proof of Pór–Valtr's Theorem 4, needs
  |P| ≥ 2^{32k} to find a k-cup or k-cap whose k−1 support regions each hold
  ≥ |P|/2^{32k} points with every transversal convex; the parameters are
  k = ⌈n^{2/3}⌉, t = ⌈n^{1/3}/2⌉, K = ⌈n^{2/3}⌉, α = 3n^{−1/3} log n, the
  cups–caps theorem is applied with f(n, ⌈2n^{2/3}⌉) and
  f(iK, n − iK + K), and there is no projective step (only a rotation making
  x_i x_{i+1} vertical). Two reusable finite lemmas: Lemma 2.1 (all 4-subsets
  convex ⇒ the set is convex) and Observation 3.1 (a k-left-cap in Q_{i−1}
  plus an ℓ-right-cap in Q_i is k+ℓ points in convex position), the latter a
  candidate for certifying convexity of unions in catalog assembly.
  Pór–Valtr's Theorem 4 gives the positive-fraction constant
  ε_k = k·2^{−32k} (improving Pach–Solymosi's α^{−k}) and Section 6 shows
  ε_k ≤ β^{−k} for some β > 1 is necessary; its proof finds 4k points in
  convex position among 4^{4k} and samples convex 4k-subsets. [HMPT 2020](https://arxiv.org/abs/1710.11415)
  (JEMS 22; full text read): Theorem 1.2, any pseudo-configuration with
  ≥ 4^n points has n in convex position; Theorem 2.4, for a convex k-set X in
  P with N ≥ 2^{4k} the k spikes hold P_1..P_k with ∏|P_i| ≥ N^k / 2^{8k²};
  each spike carries a vertical and a horizontal partial order (any two
  points comparable in exactly one), so |P_i| ≤ v_i h_i by Dilworth, chains
  split into left/right and inner/outer convex chains bounded by the
  transitive-colouring theorem, with constraints d_i < n, b_i + a_{i+1} < n,
  Σ c_i < 2n and N < 2^{n + 2n log n / k + 8k} at k ≈ ½√(n log n); Remark
  1.4 makes the constant (8√2/3) + o(1). The homogeneous version
  ([Bárány–Károlyi 2001](https://www.renyi.hu/~barany/cikkek/85.pdf), after
  Bárány–Valtr) has C(4) ≥ 1/22, C(5) ≥ 1/352, C(n) ≤ 2^{−(n−2)} and
  Solymosi's C(n) ≈ 2^{−16n²} (as typeset), with a doubly exponential
  same-type-lemma constant in general. None of these constants is
  quantitatively relevant at 33 or 65 points.
- **Ambient-dependent chain conditions cost an exponential.**
  [Valtr 2007](https://kam.mff.cuni.cz/kamserie/clanky/2004/s671.pdf)
  (DCG 37; KAM preprint read): a k-cap or k-cup is *open* in X if no point
  of X with abscissa strictly between its endpoints lies above it; the least
  f(k,l) forcing an open k-cap or open l-cup exists (Theorem 2) and satisfies
  2^{C(⌊k/2⌋+⌊l/2⌋−2, ⌊k/2⌋−1)} ≤ f′(k,l) ≤ f(k,l) ≤ 2^{C(k+l−2, k−1) − 1}
  (Theorem 3; f′ = k-cap or open l-cup), i.e. the open version is doubly
  exponential; corollaries bound the empty l-gon threshold in k-convex
  configurations. A caution for state definitions that depend on the ambient
  set, as the residual junction conditions do, and a link from cup–cap
  catalogs to empty-polygon problems.
- **Flag algebras.** [Goaoc–Hubard–de Joannis de Verclos–Sereni–Volec](https://arxiv.org/abs/1811.02236)
  (SoCG 2015; arXiv 2018) run semidefinite programs over realizable order
  types of up to 8 points: the minimum density of 5-point subsets in convex
  position is c_5 ≥ 0.0608516 (previously 5!4!/9! > 0.00793 from ES(5) = 9;
  upper bound 0.0625), c_6 ≥ 0.0018311 (previously 11!6!/17! > 0.0000808 from
  ES(6) = 17; upper 0.005822), c_4 ≥ 0.37843917 (below the known 277/729);
  a refined bound needed more than 700 SDPs. The only LP/SDP certificate
  approach to convex-position questions found; a density bound on 7-gons or
  on cup–cap states would be a new certificate type, feasible at least to 8
  points. No LP or integer-programming certificate for ES(n) or for cups and
  caps was found in the literature.
- **Peripheral Erdős–Szekeres-type generalizations**, listed to delimit the
  literature (details from listings unless stated):
  [Gowers–Long 2021](https://arxiv.org/abs/1609.08688) (CPC 30; Loh's
  2-increasing sequences of triples in [n]: trivial n² upper bound, a log*
  improvement via triangle removal, an n^{3/2} lower bound; a 2025 preprint,
  arXiv 2512.10438, strengthens several results);
  [Bucić–Sudakov–Tran 2023](https://arxiv.org/abs/1910.13318) (JEMS 25;
  monotone and lex-monotone n×…×n subarrays in arrays of at most triple- and
  quadruple-exponential size, answering Fishburn–Graham, later improved by
  Girão–Kronenberg–Scott); [Suk–Zeng 2022/24](https://arxiv.org/abs/2112.01750)
  (SoCG 2022, DCG 71; a sequence of n reals has k sequential blocks of size
  Ω(n/k²) with all transversals monotone, the k = 1 level of the hierarchy,
  showing what sharp positive-fraction constants look like);
  [Pinelis 2006](https://arxiv.org/abs/math/0611802) (preprint, read; ordered
  vertex sequences without general position, F(k) = R(k,13;4) for k ≥ 4,
  every strict n-gon with n ≥ 13 has a convex sub-4-gon, F(4) ≥ 8; no cups
  or caps); [Archy Will He 2015/19](https://arxiv.org/abs/1511.02334)
  (unreviewed preprint; claims a one-directional reduction of the conjecture
  to the unsatisfiability of first-order formulae over multisets of Boolean
  variables, with no computational results; cited neither by Schroeder nor
  by Baek–Balko, so to be treated with caution).
- **Verified SAT infrastructure** (for any future SAT-derived lemma):
  [cube-and-conquer](https://www.cs.utexas.edu/~marijn/publications/cube.pdf)
  (Heule–Kullmann–Wieringa–Biere, HVC 2011: the cutoff heuristic is "of
  crucial importance", a factor-10 change in D "hardly influences" the
  partition); [LRAT](https://arxiv.org/abs/1612.02353) (Cruz-Filipe–Heule–
  Hunt–Kaufmann–Schneider-Kamp, CADE 2017; Coq and ACL2 checkers) versus
  DRAT-trim; [native LRAT in CaDiCaL and Lrat-Trim](https://drops.dagstuhl.de/opus/volltexte/2023/18483/)
  (Pollitt–Fleury–Biere, SAT 2023), which is why 2024–2026 computations use
  CaDiCaL ≥ 1.9 with `--lrat`; [cake_lpr](https://research.chalmers.se/en/publication/534843)
  (Tan–Heule–Myreen, TACAS 2021 / STTT 2023; verified to machine code,
  compositional format for parallel checking); Lean core's
  [`Std.Tactic.BVDecide.LRAT.check`](https://lean-lang.org/doc/api/Std/Tactic/BVDecide/LRAT/Checker.html)
  with `check_sound` (trust = kernel plus compiler via `Lean.ofReduceBool`,
  no axiom; impractical at 180 TB but usable for per-cube certificates);
  [Trestle](https://reservoir.lean-lang.org/@FormalSAT/trestle) (FormalSAT;
  `EncCNF`/`VEncCNF` verified encodings, solver typeclasses; its README lists
  verified checkers as planned while Codel's thesis proposal says one exists,
  a discrepancy to note). Mathlib's only Erdős–Szekeres statement is the
  monotone-subsequence theorem
  ([Archive, Theorem 73](https://github.com/leanprover-community/mathlib4/blob/master/Archive/Wiedijk100Theorems/AscendingDescendingSequences.lean)),
  so the project's convex-position definitions have no upstream to align with.

## Realizability

### Complexity and what a verdict requires

- Realizability of abstract order types / signotopes is ∃R-complete (Mnëv–
  Shor universality, as summarized in the
  [∃R compendium](https://arxiv.org/abs/2407.18006), preprint: entries CG1,
  simple order-type realizability, and CG9, pseudoline stretchability, are
  ∃R-complete even for simple arrangements, oriented-matroid realizability
  is called "a canonical ∃R-complete problem", and simple pseudoline
  arrangements are in bijection with uniform acyclic rank-3 oriented
  matroids). The [Handbook chapter on pseudoline arrangements](https://page.math.tu-berlin.de/~felsner/Paper/pseudol.pdf)
  (Felsner–Goodman, 3rd ed. 2017, author preprint) collects the finite facts:
  every arrangement of ≤ 8 pseudolines is stretchable (Goodman–Pollack 1980,
  Thm 5.3.2); every simple arrangement of 9 is stretchable except the
  non-Pappus (Ringel) one (Richter 1989, Thm 5.3.3); an arrangement with a
  face bounded by ≥ n−1 pseudolines is stretchable (Thm 5.3.4); a stretchable
  simple arrangement may have a combinatorial symmetry that no straight-line
  realization has (Shor 1991, Thm 5.3.5 — a caveat for symmetric SAT models,
  whose realizations may have to break the symmetry); stretchability is
  decidable in singly exponential time and polynomial space, ≤ 2^{4n log n
  + O(n)} arithmetic operations (Thm 5.3.7); the Bokowski–Sturmfels infinite
  minor-minimal non-realizable family means no finite list of forbidden
  subarrangements characterizes stretchability; isotopy holds for ≤ 9 lines
  and fails at 14 (Suvorov). The smallest non-realizable abstract order types
  have 9 points (Knuth; Koshelev–Koshka confirm all signotopes with N ≤ 8 are
  realizable), and there are 13 of them among Euclidean abstract types (our
  subtraction from Table 5.6.1: 158,830 − 158,817).
- A failed realization attempt is therefore not evidence of
  non-realizability; a non-realizability proof needs a certificate. The
  Handbook lists four algorithmic routes: inequality reduction, solvability
  sequences, final polynomials ("every nonrealizable one does have a final
  polynomial", by Lombardi's effective real Nullstellensatz) and Bokowski's
  rubber-band heuristic. The LP-detectable subclass is the Bokowski–Richter
  bi-quadratic final polynomial (BFP; products of Graßmann–Plücker bracket
  relations with sign constraints), used by Scheucher 2023 and
  Heule–Scheucher 2024. Its limits are known exactly:
  [Fukuda–Miyata–Moriyama 2013](https://ar5iv.labs.arxiv.org/html/1204.0645)
  (DCG) report that every non-realizable oriented matroid in their classes
  up to 11 elements admits a BFP, while
  [Richter-Gebert 1996](https://emis.dsd.sztaki.hu/journals/DMJDMV/vol-01/07.html)
  (Documenta Math. 1) exhibits Ω14⁻, a non-realizable rank-3 oriented matroid
  on 14 elements with no BFP (its twin Ω14⁺ is realizable, has a symmetry no
  realization has and a disconnected realization space); the smallest known
  non-realizable OM without a BFP is in OM(3,14). So for 14 or more points a
  failed BFP search proves nothing, and a "non-realizable" verdict on a
  33-point model needs a general final polynomial or an exact algebraic
  decision, not BFP failure plus Localizer failure.
  [Richter-Gebert 1993 / Fukuda–Moriyama–Nakayama 2005 (Combinatorica 2009 with Richter-Gebert)](https://arxiv.org/abs/math/0510500)
  show every non-Euclidean oriented matroid (one on which oriented-matroid LP
  can cycle), uniform or not, admits a BFP — the one structural class where
  the cheap certificate is guaranteed. Neither paper mentioned here nor the
  2025–2026 SAT papers contains an exact non-realizability certificate for a
  30-plus-point configuration in the Erdős–Szekeres literature: the
  Subercaseaux et al. "none realizable" verdict on the six inner-12
  configurations and PointSAT's 0 of 200,000 are heuristic failures, not
  proofs. [Schewe 2008/10](https://arxiv.org/abs/0801.2582) (DCG) is the
  template for the exact route: enumerate by SAT every oriented matroid
  compatible with a combinatorial structure, then refute each with final
  polynomials (used to show no minimal vertex triangulation of the
  orientable genus-6 surface embeds polyhedrally in R³); if the number of
  33-point heptagon-free signotopes up to symmetry were small, refuting each
  would prove ES(7) = 33 without an UNSAT proof.

### Counting abstract versus realizable types

- Simple pseudoline arrangements number > 2^{0.2604 n²}
  ([Dallant 2024](https://arxiv.org/abs/2402.13923), SoCG 2024; upper bound
  2^{0.6496 n²} in [Dallant 2025](https://arxiv.org/abs/2502.20909), preprint)
  versus 2^{Θ(n log n)} realizable order types (n^{4n+o(n)} by
  Goodman–Pollack–Sturmfels). At n = 33 that is at least about 2^{283}
  signotopes (our order-of-magnitude arithmetic): a random satisfying
  assignment of a 33-point signotope SAT instance is almost surely
  non-realizable.
- Exact small counts. Realizable order types ([OEIS A063666](https://oeis.org/A063666);
  Aichholzer database): 1, 2, 3, 16, 135, 3,315, 158,817, 14,309,547,
  2,334,512,907 for n = 3..11, with no term for n = 12. Abstract order types
  ([Rote, NumPSLA 2025](https://arxiv.org/abs/2503.02336), preprint; Handbook
  Table 5.6.1; [Aichholzer–Krasser 2005/06](https://publications.ist.tugraz.at/files/publications/geometry/ak-aoten-05a.pdf),
  CGTA 36): n = 9: 158,830; n = 10: 14,320,182 (10,635 non-realizable);
  n = 11: 2,343,203,071 (8,690,164 non-realizable); n = 12: 691,470,685,682;
  n = 13: 366,477,801,792,538 — with no realizable/non-realizable split for
  n ≥ 12, so sub-configuration filtering of a 33-point model is exact only
  for 10- and 11-point subsets. Non-realizable fractions 0.074% at n = 10 and
  0.37% at n = 11 (our arithmetic). Projective abstract order types at
  n = 11: 41,848,591 with 155,214 non-realizable (Aichholzer–Krasser Table
  1), matching the uniform rank-3 oriented-matroid counts of
  Fukuda–Miyata–Moriyama (312,356 on 10 elements, 312,114 realizable, 242
  non-realizable by subtraction; 41,848,591 on 11, 41,693,377 realizable);
  rank 3 on 9 elements including degenerate classes: 461,053 oriented
  matroids, 460,779 realizable, 274 non-realizable; uniform OM(3,9): 4,382
  with one non-realizable class; rank 4 on 8: 181,472 / 177,504 / 3,968.
  Fukuda et al. realize by an extended solvability-sequence method (exact
  coordinates when it succeeds), random realizations for the remaining
  variables and Gröbner bases for the one irrational rank-3 case (Perles)
  and two rank-4 cases; uniform (general-position) types have open
  realization spaces, so rational realizations exist whenever any does.
- How the 11-point classification was done (Aichholzer–Krasser): abstract
  types are generated purely combinatorially, by inserting a pseudoline into
  the dual arrangement in all combinatorially possible ways, because
  extending a single realization "cannot guarantee completeness"; realizability
  is decided by refined coordinate heuristics plus the Bokowski–Richter BFP
  algorithm, which "were sufficient to completely settle the case for
  n = 11" with deterministically checkable results; the database stores one
  point set per order type in 16-bit integer coordinates; realizability is
  described as NP-hard with "no practical algorithms known, not even for
  small sets, say of size 10 or 11", and no database for n ≥ 12 exists for
  storage and time reasons. The same realize-or-refute pipeline is the exact
  filter for the 11-point subsets of a 33-point signotope. NumPSLA
  enumerates all abstract order types in streaming fashion (n = 10 in
  10–20 s, n = 11 in about 30 min, n = 12 in about 200 CPU hours, n = 13 in
  about 3,200 CPU days on a cluster), skips known non-realizable types for
  n ≤ 11 through an exclude file of 8,699,559 entries (184.6 MB), reports
  hull size, symmetry, halving lines and crossing number per class, has no
  k-gon filter and does not test realizability; code at
  [guenterrote/NumPSLA](https://github.com/guenterrote/NumPSLA). Adding a
  convex-k-gon counter would give exact counts of pentagon-free and
  hexagon-poor abstract versus realizable types up to n = 12 (nobody has
  published these; any such number would be this project's own computation).

### Extension and growth searches

- [Bergold–Felsner–Scheucher 2023](https://arxiv.org/abs/2303.04079)
  (SoCG 2023): rank-3 signotopes always extend (Levi's enlargement lemma;
  Richter-Gebert's counterexample is for pseudoplanes in R³), and more
  generally signotopes of odd rank are extendable, while SAT found
  non-extendable examples in ranks 4, 6, 8, 10 and 12. So an abstract growth
  search never gets stuck and explores a far larger tree than a realizable
  face-extension search, and its dead ends carry no information about
  realizable sets; conversely a stuck realizable search says nothing about
  the signotope model. Aichholzer–Krasser's remark cuts the other way too: a
  realizable-only growth search that extends specific kept realizations can
  only reach the order types obtainable from those realizations, and may miss
  realizable 33-point types reachable only through other realizations of the
  same 32-point order type. The signotope definition used throughout (sign
  function on r-subsets with at most one sign change along every
  (r+1)-subset) and the Felsner–Weil (Discrete Appl. Math. 2001) bijection
  with simple Euclidean pseudoline arrangements are restated in
  [Bergold–Egeling–Hoang 2024/25](https://arxiv.org/html/2411.19208v2)
  (preprint), confirming that the project's SAT model is the uniform rank-3
  oriented-matroid model with a marked top cell.

### Coordinate size and exact verification

- Worst case: a realizable order type on n points can need area and grid
  2^{2^{Θ(n)}} (Goodman–Pollack–Sturmfels; Handbook Thm 5.6.4, ∃R
  compendium Thms 2.2–2.3), so a float-then-rationalize realizer can in
  principle miss realizable types, and a realizable 33-point SAT model could
  require coordinates beyond floating-point reach. Typical case:
  [Scheucher 2020/21](https://arxiv.org/abs/2007.15334) (preprint) shows at
  least n^{4n+o(n)} order types — "essentially" all of them in the counting
  sense — have polynomial-size integer realizations;
  [van der Hoog–Miltzow–van Schaik 2019](https://ar5iv.labs.arxiv.org/html/1907.04645)
  (preprint / Utrecht thesis) show that after perturbing each point of a
  realization by a uniform offset in a disk of radius δ ≤ 1/2, snapping to a
  grid of width pδ/n³ preserves the order type with probability ≥ 1 − p
  (max coordinate ≤ ⌊2n³/(pδ)⌋, ≤ 2n·log(n³/(pδ)) + 2n bits in all; expected
  bits per coordinate ≤ log(n²/δ) + 2), so realizability of smoothed
  instances is decidable in "expected NP-time" while the problem stays
  ∃R-complete — and they note that perturbing an *abstract* order type
  "would likely yield a non-realizable map";
  [Cardinal–Fabila-Monroy–Hidalgo-Toscano 2019/20](https://arxiv.org/abs/2001.08062)
  (CCCG 2019): n uniform random points in a convex domain of R^d can be
  rounded to a grid of step ∝ 1/n^{d+1+ε} without changing the chirotope,
  O(n log n) bits in all, against the worst-case step 1/2^{2^{Ω(n)}} even
  for d = 2. Modest-precision rationals therefore suffice for generic
  configurations; the hard residue is specific rigid types, which an
  extremal heptagon-free set might be.

### Empirical realizability rates

- Koshelev–Koshka's 8.5% (uniform abscissae) versus 37.7% (exponential
  grid) on 10-point signotopes argue for adaptive x-coordinates;
  Krapivin–Przybocki–Heule realized 0 of 200,000 32-point 7-gon-free
  abstract order types, 4 of 18,806 29-point 6-hole-free ones and 1,035 of
  174,450 23-point (no 6-hole, no 7-gon) ones, and write that
  "almost all abstract order types are not realizable"; Heule–Scheucher
  found millions of 23-element signotopes with no 7-gon and no 6-hole, all
  tested ones non-realizable; Subercaseaux et al. found 0 realizable among
  the 6 inner-12-point 4-fold symmetric configurations, 18 of 66 (4-fold)
  and 92 of 932 (5-fold) among 16-point hexagon-free symmetric solutions,
  and the same group's earlier
  [pentagon-minimization work](https://arxiv.org/abs/2311.03645) (CICM 2024)
  realized its SAT-found abstract configurations with ≤ 16 points through
  operations-research tools (μ₅(n) ≤ C(⌊n/2⌋,5) + C(⌈n/2⌉,5), MaxSAT-optimal
  for n ≤ 16), in contrast to the 32-point failure of 2026. A cheap exact
  pre-filter, used by Subercaseaux et al., is to check all 10- and 11-point
  subsets of a candidate against the known non-realizable abstract types.
- Exact higher-dimensional values (Scheucher 2023) are exact only in the
  chirotope model; the same gap applies to the small-n planar values above 6.

## Computational data

| Instance | Method | Cost | Certificate | Source |
| --- | --- | --- | --- | --- |
| ES(6) = 17 (signatures) | 446-way split, custom search | ≈ 3,000 GHz-hours (1,500 h on < 2 GHz) | three implementations | [Szekeres–Peters 2006](https://archive.austms.org.au/Publ/ANZIAM/V48P2/2409.html) |
| ES(6) = 17 | SAT + Isabelle/HOL | ≈ 1 GHz hour; 787 s for the CNF under CaDiCaL (2024) | formal, unverified encoder | [Marić 2019](https://link.springer.com/article/10.1007/s10817-017-9423-7) |
| ES(6) = 17 | signotope SAT | ≈ 2 CPU h (2020); ≈ 10 CPU min, 668 MB DRAT, 12 min check (2023) | DRAT-trim | [Scheucher 2020](https://arxiv.org/abs/1807.10848), [2023](https://cgt-journal.org/index.php/cgt/article/view/12) |
| ES(6) = 17 | O(n⁴) encoding, 1,108 cubes | 8.53 s (205,153 conflicts); 28 s in the Lean pipeline | LRAT | [Heule–Scheucher 2024](https://arxiv.org/abs/2403.00737), [ITP 2024](https://arxiv.org/abs/2403.17370) |
| h(6) ≤ 30 | 312,418 cubes, CaDiCaL 1.9.3 | 17,300 CPU h; 25,876.5 CPU h with proof logging | 180 TB LRAT, cake_lpr; UNSAT as a Lean axiom | same |
| 24 points ⇒ 6-hole or 7-gon | cubes, ℓ = 15 optimal | 231 CPU h (606 CPU h at ℓ = 21) | LRAT | Heule–Scheucher Table 2 |
| h(6) ≤ g(9) (Gerken) | 14 chirotope instances | ≈ 1 CPU h, 6.2 GB DRAT | DRAT-trim | Scheucher 2023 |
| g^{(3)}(7) ≤ 13 / h^{(3)}(7) ≤ 14 / h^{(4)}(8) ≤ 13 / h^{(5)}(9) ≤ 13 | chirotope SAT, CaDiCaL 1.0.3, single CPU on a 1 TB RAM node (up to 300 GB used); instances 245 MB / 433 MB / 955 MB / 4.2 GB | ≈ 2 / ≈ 19 (`--unsat`) / ≈ 7 / ≈ 3 CPU days | DRAT 35 GB (39 GB in arXiv v2) / 314 GB / 297 GB / 117 GB; DRAT-trim ≈ 1 / 12 / 6 / 3 CPU days | [Scheucher 2023](https://cgt-journal.org/index.php/cgt/article/view/12), [arXiv:2105.08406](https://arxiv.org/abs/2105.08406) |
| Rank-4 18-element chirotope without 8-holes (lower-bound witness) | chirotope SAT | 100 CPU days | realized with integer coordinates | Scheucher 2023 |
| All abstract order types, n = 11 (2,343,203,071) classified realizable / not | combinatorial generation, coordinate heuristics, BFP linear programs | not stated | deterministic certificates; 8,690,164 non-realizable | [Aichholzer–Krasser 2005/06](https://publications.ist.tugraz.at/files/publications/geometry/ak-aoten-05a.pdf) |
| All abstract order types, n = 12 (691,470,685,682) and n = 13 (366,477,801,792,538) | NumPSLA streaming enumeration | ≈ 200 CPU h; ≈ 3,200 CPU days on a cluster | counts only, no realizability split | [Rote 2025](https://arxiv.org/abs/2503.02336) (preprint) |
| 16 points, 3-/4-/5-fold symmetric, no 6-gon | symmetric SAT + Localizer | not stated | UNSAT / 66 solutions, 18 realized / 932 (or 948) solutions, 92 realized; integer coordinates for two sets | [Subercaseaux et al. 2025](https://arxiv.org/abs/2506.00224) |
| h(6,≥2) = 17; h(6,1) = 18 | ASP (clingo) | 70 min; 190 min | — | [Koshelev–Koshka 2026](https://arxiv.org/abs/2604.20120) (preprint) |
| M_7(5,6) = 25 (26 points force a 5-cap, 6-cup or 7-gon) | omission catalog over 35 states, 9 holes | — | CNF 461 vars / 93,169 clauses; LRAT 381,647 additions; `native_decide` | [Schroeder 2026](https://zenodo.org/records/22842891) (unreviewed) |
| C_7 ≤ 49; C_8 ≤ 193; D_8 ≤ 124 (⇒ ES(7) ≤ 81, ES(8) ≤ 319) | weighted omission trees | full Lean rebuild 1,290 s (ARM64 macOS, 208 modules) | 4,017,399-clause primary formula, 1,989,465-addition proof; trees of 1,590 and 7,314 branches; 27 `native_decide` axioms in all | same |
| 23 points, no 6-hole and no 7-gon (exact) | SAT modulo realizability, 128 cores | 1,727 + 2,326 core hours | all cubes UNSAT; 1,035 realizations | [Krapivin–Przybocki–Heule 2026](https://arxiv.org/abs/2607.02958) |
| 32 points, 4-fold symmetric, no 7-gon | allsat enumeration | ≈ 1 CPU year | 310,187,713 configurations, none realizable | [Subercaseaux et al. 2025](https://arxiv.org/abs/2506.00224) |
| 33 points, layer-anchored sub-cubes | Kissat, single thread | 2.5 × 10³ s to 2.28 × 10⁶ s per sub-cube | none reported | [Bogdan 2025](https://arxiv.org/abs/2512.24061) |
| 17 vertices, pure colorings, a = u = 6 | Glucose | did not terminate in 266 h | — | [Balko–Valtr 2015](https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf) |
| N ≤ 14 / 17 / 20 hole-type instances | Kissat 4.0.4 and decompositions | < 12 s / < 1,000 s / < 70,000 s; decompositions 350–880 CPU h | — | [Koshelev–Koshka 2026](https://arxiv.org/abs/2604.20120) |
| ES(8) ≤ 313 (12 Oct 2026) | omission catalogs (balanced bound 190, residual 121), kernel-checked arithmetic | ≈ 120 CPU h kernel check | Lean kernel, three standard axioms | [313 record](../experiments/omission-final313-2026-10-11/README.md) |
| ES(8) ≤ 312 (14 Oct 2026) | balanced bound 189 from the 3,131-row balanced catalog; budget-62 search of 187,464 nodes in 6.2 h on 8 workers | ≈ 58 CPU h kernel check (2,169 modules, 30–170 s each) | 93,988-leaf tree replayed with unbounded integers; Lean kernel, three standard axioms, no `native_decide` | [312 record](../experiments/omission-final312-2026-10-13/README.md) |

Order-type data. The [Aichholzer–Aurenhammer–Krasser database](http://www.ist.tugraz.at/aichholzer/research/rp/triangulations/ordertypes/)
(TU Graz; page live in 2026) holds one point set per realizable order type for
n ≤ 10 (`otypes03.b08` … `otypes10.b16`, 8- or 16-bit coordinates; the 96 GB
n = 11 file by e-mail request), with per-order-type result files for n ≤ 9
including "Number of k-gons" (`kgons03.b08` … `kgons09.b08`) and "Number of
empty k-gons" (`ekgons…`), crossing numbers and hull sizes; free for
non-commercial use. Filtering `kgons08.b08` for zero 5-gons over the 3,315
8-point types would give the number of pentagon-free 8-point order types; the
number appears on no page retrieved and would be this project's own
computation, as would the analogous hexagon counts at n = 10, 11.
[Aichholzer–Hackl–Vogtenhuber 2011](https://publications.ist.tugraz.at/files/publications/geometry/ahv-o5g5h-11.pdf)
(XIV Spanish Meeting on Computational Geometry; extended in LNCS 7579)
computed from the database that the minimum number of convex 5-gons is 0 for
n = 5, 6, 7, 8 and 1 for n = 9 (ES(5) = 9 re-derived from data), that an
8-point set has 56 five-tuples, at most 408 non-convex 5-gons and 56–410
5-gons in all, and that convex position maximizes the number of 5-holes for
n ≥ 86 (Theorem 3.6); these are realizable seeds with small integer
coordinates, unlike SAT-derived signotopes. No published count exists of
16-point order types (realizable or abstract) without a convex hexagon: not in
Szekeres–Peters 2006 (whose abstract gives no count of 16-point hexagon-free
signatures and no running time), Marić 2019, Scheucher 2020/2023,
Heule–Scheucher 2024, Koshelev–Koshka 2026 or the symmetric-SAT papers (which
count only the 3-/4-/5-fold symmetric ones, 0 / 18 / 92 realizable). Likewise
no list of 32-point heptagon-free or 64-point octagon-free sets beyond the
classical construction is published: Baek–Balko report "many examples" from
blow-ups without data, Subercaseaux et al. release code and 16-point sets
only, Bogdan's repository has no point sets, and PointSAT's 32-point run
realized nothing. [Baek's generator](https://github.com/jcpaik/erdos-szekeres-sat)
writes `.color` files with lines `i j k C` (or `.unsat`); its colorings are of
the ordered hypergraph, not signotopes, so the four-point axiom must be imposed
separately before any realization attempt. The Duque–Fabila-Monroy–
Hidalgo-Toscano grid bound O(n² log³ n) for the classical 2^{t−2}-point sets
(32 points at t = 7, 64 at t = 8) gives the coordinate range a certificate for
them needs; no explicit 32- or 64-point coordinate table appears on the
abstract page.

## Surveys and expert opinion

Direct quotations are marked with quotation marks; everything else is a
paraphrase of the cited text. No talk, interview or paper by Valtr, Suk or
Balko stating a personal belief for or against the exact conjecture was found
beyond neutral "open / conjectured" phrasing; the only hedged statement is
Baek–Balko 2025, and the pro-truth statements are Szekeres 1973, Graham 2006
and Pach 2017.

### The originators

- [Morris–Soltan 2000](https://kam.mff.cuni.cz/~chvatal/MorSol00.pdf)
  (Bull. AMS 37, p. 438): Erdős repeatedly attributed the conjecture to
  Szekeres and in his 1979 Ohio State proceedings paper weakened "Szekeres
  conjectured N(n) = 2^{n−2} + 1" to "Probably N(n) = 2^{n−2} + 1"; Szekeres
  in his 1973 reminiscences: "Of course we firmly believe that
  N(n) = 2^{n−2} + 1 is the correct value"; Erdős's 1997 paper offers $500;
  Chung and Graham offered $100 for N(n) = O((4−c)^n), answered by Suk. The
  survey also says that despite many mathematicians' efforts the problem is
  far from solved, and that Bonnice's hull-nesting method can hardly reach
  n = 6 because 17 hexagon-free points admit 70 nesting tuples.
  Goodman–Pollack conjectured that N(n) ≤ 2^{n−2} + 1 holds for pseudoline
  arrangements, with N_ps(n) ≤ C(2n−5, n−2) + 2 by the same arguments.
- Erdős himself, [1980](https://static.renyi.hu/~p_erdos/1980-41.pdf)
  (Haifa 1979, LNM 792) and [1982](https://static.renyi.hu/~p_erdos/1982-33.pdf)
  (Singapore 1981): states the problem as Klein's, credits Klein with
  H(4) = 5 and Makai–Turán with H(5) = 9, writes that Szekeres (not he)
  conjectured H(n) = 2^{n−2} + 1, records 2^{n−2} + 1 ≤ H(n) ≤ C(2n−4, n−2),
  offers no prize for this problem in either paper, and says of the
  empty-polygon variant that it is doubtful n_k exists for all k. Together
  with the later 5:1 prize asymmetry this is the primary record of Erdős's
  own distance from the exact formula.
- [Szekeres–Peters 2006](https://archive.austms.org.au/Publ/ANZIAM/V48P2/2409.html)
  (ANZIAM J. 48; [Cambridge copy](https://doi.org/10.1017/S144618110000300X)):
  the authors say that when (P_k) and (Q_k) were proposed they looked like a
  hazardous extrapolation from a few unconvincing cases, that Makai–Turán's
  unpublished n = 5 proof gave only modest support, that they considered the
  abstract strengthening (P_{σ,k}) unlikely a priori (it held, surprisingly,
  for all σ on 9 points at k = 5), and that verifying (P*_7) would be of great
  interest but was out of reach in 2006. (P*_7) in the 4-point-constraint
  model is essentially this project's 33-point signotope instance.

### Published experts

- [Tóth–Valtr 2005](https://library.slmath.org/books/Book52/files/30toth.pdf):
  the cups–caps bound "is tight for any n, m. But it does not imply that the
  bound for ES(n) is tight as well"; the lower bound is "conjectured" sharp;
  written when it was known sharp only for n ≤ 5. Valtr's published stance is
  strictly neutral.
- [Bárány–Károlyi 2001](https://www.renyi.hu/~barany/cikkek/85.pdf): "a very
  old conjecture" (Open Problem 1), on whose truth the authors express no
  opinion; the only belief stated is for Open Problem 6 (empty hexagon,
  answer yes, since proved). Füredi's conjecture log f_d(n) = O(n^{1/(d−1)})
  versus Morris–Soltan's "exponential lower bound" expectation
  (Pohoata–Zakharov later sided with Füredi's growth order).
- [Graham 2006/07](https://mathweb.ucsd.edu/~ronspubs/07_04_favorite_problems.pdf)
  (INTEGERS 7(2), #A15; UCSD copy): Problem 4 offers $1000 to prove *or
  disprove* f(n) = 2^{n−2} + 1, says it is suspected by many people that the
  lower bound is the truth, says the problem is known for n ≤ 5 (not citing
  Szekeres–Peters), and misprints the Tóth–Valtr bound as C(2n−5, n−2) + 5.
  A verified 33-point heptagon-free set would therefore be a prize-winning
  disproof.
- [Suk](https://mathweb.ucsd.edu/~asuk/ES2016.pdf) (2016 slides; DIMACS and
  Georgia Tech abstracts): ES(4) = 5 (Klein 1933), ES(5) = 9 (Makai 1935),
  ES(6) = 17 (Szekeres–Peters 2006), and for n ≥ 7 ES(n) "still unknown";
  consistently "conjectured to be optimal", never a belief statement.
  [Mubayi–Suk 2018](https://arxiv.org/abs/1808.00453) (Mathematika): the
  conjecture is verified for n ≤ 6 and determining ES_2(n) exactly for n ≥ 7
  is described as one of the longest-standing open problems in Ramsey theory
  and discrete geometry — citable wording for an introduction.
- [HMPT 2020](https://ar5iv.arxiv.org/html/1710.11415) (JEMS): "a classical
  conjecture" whose bound cannot be improved if true; no position on its
  truth; none of the inequalities in the chain 2^{n−2} + 1 ≤ e(n) ≤ … ≤ b(n)
  is known to be strict.
- [Baek–Balko 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13):
  the weak-k-gon failure at 33 "suggests that the Erdős–Szekeres Conjecture
  might be false"; a proof must use point sets. Balko's public abstracts
  ([KAM noon lecture 2016](https://kam.mff.cuni.cz/noon_lectures/2016/nl20160531.html);
  the [split-polygon talk abstract](https://mathweb.ucsd.edu/~asuk/balko.pdf),
  c. 2024–25) say only "still open" and announce the split version in which
  2^{k−2} + 1 is exactly right.
- [Balko–Valtr 2015](https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf):
  "For pseudolinear colorings, all our results matched the values from
  Conjecture 3.1"; the Goodman–Pollack version "might be true even if the
  previous strengthening is not".
- [Koshelev 2009](https://arxiv.org/abs/0910.2700) (preprint survey):
  Conjecture 1 (g(n) = 2^{n−2} + 1) proved for n ≤ 6 (crediting Szekeres,
  McKay and Peters for g(6) = 17), otherwise "neither proved nor disproved".
- [Heule–Scheucher 2024](https://arxiv.org/abs/2403.00737): "All known point
  sets witnessing h(6) ≥ 30 contain a 7-gon"; the 6-gon and 7-gon encodings
  are "similar and more simple" than holes.
- [Subercaseaux et al. 2024](https://arxiv.org/abs/2403.17370): "optimistic"
  that the Lean pipeline "could lead to an eventual resolution of g(7)".
- [Koshelev–Koshka 2026](https://arxiv.org/abs/2604.20120) (preprint): no
  case is known where the realizable value is smaller than the signotope
  value, because all maximal signotopes found are non-realizable.
- [Bogdan 2025](https://arxiv.org/abs/2512.24061) (preprint): "the case k = 7
  remains open".
- [Balko 2025 survey](https://arxiv.org/abs/2502.02155) (preprint):
  Conjecture 3 is ES(n) = 2^{n−2} + 1, "known for n ≤ 6, open above".
- [Eppstein 2018](https://assets.cambridge.org/97811084/23915/excerpt/9781108423915_excerpt.pdf)
  (*Forbidden Configurations in Discrete Geometry*, Chapter 1 excerpt): notes
  Suk's 2^{k + 6k^{2/3} log k} with a footnote that Tardos further improved
  the low-order term, and phrases Open Problem 1.1 as the existence of some k
  and a set of 2^{k−2} + 1 points in general position with no convex k-gon —
  a mainstream textbook framing the question as a counterexample search.

### Journalism, problem lists and teaching material

- [Quanta, 30 May 2017](https://quantamagazine.org/a-puzzle-of-clever-connections-nears-a-happy-end-20170530)
  (Hartnett): Pach is quoted to the effect that before Suk nobody would have
  been shocked if the truth were close to 4^n, that after Suk the conjecture
  is known to be roughly true, which makes it more believable, and that Erdős
  and Szekeres were on the right track; Graham calls Suk's argument clever
  and elementary; Tardos explains why the cap-and-cup gain is small. The only
  on-record plausibility statements by Pach found; they support the 2^n
  shape, not the exact value, and nothing in the article asserts ES(7) = 33.
- [Kalai's blog, 4 May 2016](https://gilkalai.wordpress.com/2016/05/04/the-erdos-szekeres-polygon-problem-solved-asymptotically-by-andrew-suk/):
  reports Suk's result as settling the order of magnitude; neither the post
  nor its single comment takes a position on the exact value.
- [Erdős Problem #107](https://www.erdosproblems.com/107) (Bloom; revised
  2025-10-20 and 2026-04-11): states the prizes as $500 for a proof and only
  $100 for a disproof per Erdős 1997 (*Math. of Paul Erdős I*, 47–67; the
  wording of the disproof clause is second-hand, the paper not retrieved)
  and Graham's $1000; calls HMPT the current best bound; carries a "looks
  difficult" tag by JineonBaek and no formalization entry; the
  [forum thread](https://www.erdosproblems.com/forum/thread/107) notes the
  Balko–Valtr refutation of the Szekeres–Peters strengthening (Alfaiz, 11 Dec
  2025) and points to problem 216 on h(6) = 30 (BorisAlexeev, 29 Dec 2025).
  The page omits ES(6) = 17. [Open Problem Garden](https://www.openproblemgarden.org/category/convex_polygons)
  (DeVos, 2009) carries the bare statement with no status. The main
  community problem lists record no dissent from the conjecture.
- [Science News, 18 Mar 2003](https://www.sciencenews.org/?p=25610)
  (Peterson): three years before Szekeres–Peters, the problem was reported as
  solved only for k = 3, 4, 5 and the 17-point case as not yet shown, quoting
  Szekeres that a simple-minded argument would not do and Morris–Soltan that
  the problem is far from solved. [Scientific American, 10 Aug 2026](https://www.scientificamerican.com/article/how-the-happy-ending-problem-launched-a-new-branch-of-math-and-a-romance/)
  (Murtagh): the most recent popular coverage found; says no case above the
  hexagon is confirmed and the $500 is unclaimed, quotes no mathematician,
  does not mention n = 7, and misprints the formula as 2(n−2)+1.
- [Jungić, *Introduction to Ramsey Theory*, §6.2](https://opentext.uleth.ca/Ramsey/sec_ES2.html)
  (open textbook): Conjecture 6.2.2 with N(3..6) = 3, 5, 9, 17, the record
  bound attributed to Tóth–Valtr 2005, Erdős's $500; no opinion and no
  mention of Suk — representative of teaching material, which presents the
  conjecture as expected-true. [Wikipedia](https://en.wikipedia.org/wiki/Happy_ending_problem)
  (accessed 14 Oct 2026) is consistent with the table above (f(5) = 9 first
  published by Kalbfleisch–Kalbfleisch–Stanton 1970; h(6) = 30).
- Stale or erroneous web references: the UCSD [convex](https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/Convex.html)
  and [empty-convex](https://fanchung.ucsd.edu/erdosprb/erdos/newproblems/EmptyConvex.html)
  problem pages omit everything after 2005–2009 (no Vlachos, Mojarrad–Vlachos,
  Norin–Yuditsky, Suk; still 463 for h(6); "n ≤ 5" on the mathweb copy, "n ≤ 6"
  on a newer fanchung copy seen only in a search summary) and should be used
  only for the 1998 journal data; erdosproblems.com omits ES(6) = 17; Graham
  2006/07 says n ≤ 5 and misprints the Tóth–Valtr constant; Scientific
  American 2026 misprints the conjectured formula.

## Consequences for this project

1. **Upper bounds.** ES(8) ≤ 311 (kernel-checked 19 October 2026, after 313
   on 12 October and 312 on 14 October) improves the best published value
   (408) and the unreviewed 319 by eight points; the heptagon catalog behind ES(7) ≤ 81 is an untried
   target for the same certificate pipeline. The comparison figure is 408
   (Mojarrad–Vlachos), not 404 (Norin–Yuditsky's constant is not a bound at
   n = 8). Schroeder's own floors for the additive scheme (C_8 ≥ 62,
   D_8 ≥ 50, so C_8 + D_8 + 2 ≥ 114; under ETV the sum lies in [114, 121])
   place 312 inside the window [114, 319] in which the balanced-plus-residual
   method can still move; gains beyond about 114 would need a joint argument
   on the two parts or a direct bound on Q_n. For n = 7 the same floors give
   58, and "Either D_7 ≤ 29 or C_7 ≤ 48 would give ES(7) ≤ 80". Partial
   Erdős–Tuza–Valtr cases with 5 ≤ a, b are open territory and natural
   intermediate milestones: proving all (7,a,b) cases is
   equivalent to ES(7) = 33; the project's cup–cap–polygon catalogs must
   reproduce Baek's exact (n,4,n) values (16 at n = 7, 22 at n = 8) as a
   correctness check, and the (8,6,6) and (8,7,7) targets are 50 and 62.
   Koshelev's h(6,1) ≤ ES(7) is a free corollary of any ES(7) bound.
2. **ES(7) searches.** Abstract SAT models cannot refute the conjecture by
   themselves (realizability is needed) and may not be able to prove it
   (unrealizable 33-point signotopes could exist). Realizable-only methods,
   such as the face-extension growth search in `.cache/es7/grow`, and
   symmetric SAT models with a realizability solver (3-fold or 11-fold for 33
   points, 2-fold for 32, none yet reported) are the natural next steps.
   Heule's group has already pushed 200,000 abstract 32-point 7-gon-free
   solutions through `Localizer` without a realization, which supports the
   realizable-only strategy; the published `7gon-32.cnf` is a benchmark for
   the project's encoder, and the eight Balko–Valtr colorings are negative
   controls a correct signotope encoding must reject. An UNSAT signotope run
   at 33 would also settle the Goodman–Pollack conjecture at k = 7. Two
   caveats from the realizability literature: a realizable-only growth search
   that extends kept realizations can miss realizable order types reachable
   only through other realizations of the same 32-point type
   (Aichholzer–Krasser), so several realizations per order type should be
   kept; and a symmetric abstract model may be realizable only without its
   symmetry (Shor, Handbook Thm 5.3.5), so Localizer-style realizers should
   not be constrained to symmetric coordinates. Any exact non-realizability
   claim for a 33-point candidate needs a final polynomial; BFP linear
   programs are complete only below 14 points.
3. **Lower-bound evidence.** Decomposable constructions and blow-ups are
   excluded as counterexamples by theorem; future searches should leave that
   class and can seed from Baek–Balko's Theorem 19 family, Duque et al.'s
   small-grid realizations, or the Hirata–Katayama cell decompositions.
   Horton sets, grids and h(6)-extremal sets (all contain 7-gons) are not
   candidates. Six-hole density (every 24-subset of a 33-point 7-gon-free set
   contains a 6-hole, by Heule–Scheucher's Theorem 2; our inference) is a
   cheap filter for the growth search.
4. **Formalization.** The kernel-checked arithmetic certificates used here
   avoid trusting a SAT solver or native evaluation; the Lean SAT-verification
   toolchain of the empty-hexagon work is an alternative for SAT-based
   results, with the difference that its CNF unsatisfiability is an axiom
   discharged by cake_lpr. Lean core's verified LRAT checker could admit
   per-cube certificates without an axiom; Trestle's `VEncCNF` is the natural
   home for a verified 33-point encoder; the six-step canonical-position
   lemma of EmptyHexagonLean is the formal counterpart of the projective
   reduction. Baek's Lean development (already ported here) is the only other
   Lean formalization of a geometric Erdős–Szekeres-type theorem.
5. **Scope of the 312 proof.** Whether the omission argument uses only
   orientation (signotope-level) information has not been checked. If it
   does, the bound would also hold for pseudo-configurations and non-crossing
   convex bodies, where the best published value is 463; no such claim is
   made here, and any step using coordinates should be flagged before one is.
   Schroeder states the same caveat for his archive ("a signotope
   interpretation of the complete proof has not been audited"); HMPT 2020,
   which carries every step of the cup–cap machinery to
   pseudo-configurations, is the reference against which such an audit would
   be made.
6. **SAT engineering, if pursued.** Use the O(n⁴) signotope encoding, cubes on
   consecutive-triple orientations with the (+,−,+) refinement and an
   experimentally chosen ℓ, unit-clause symmetry breaking plus the reflection
   predicate, injected sub-Ramsey facts (ES(6) = 17 on windows, cup–cap
   bounds) as Scheucher did with h(5) = 10, concurrent LRAT checking, and the
   layer-classification route of Heule–Scheucher Section 6.4 as an
   alternative to a monolithic UNSAT run. Cross-check cube statistics against
   Bogdan's 13 finished layer vectors.

## Omitted items

Findings dropped from the survey and why.

- No retrievable primary source: Milans–Stolee–West 2015 (WVU page refused
  the connection); Goodman–Pollack 1981 (Congr. Numer. 32); Lovász 1979 and
  the original Chung–Graham and Kleitman–Pachter 1998 papers (cited through
  Tóth–Valtr 2005 and the UCSD page); Koshelev's 2011 "almost empty hexagon"
  paper and his mathnet.ru pages (503/504); Gerken's TUM thesis (blocked);
  Károlyi 2001 full text (ScienceDirect/CORE blocked; cited via the
  Bárány–Károlyi survey); ETV 1996 full text (zbMATH review only); Valtr's
  1993 FU-Berlin technical report; Mojarrad's 2017 EPFL thesis (record
  surfaced, not opened); Erdős 1997, *Some of my favorite problems and
  results* (the $500 / $100 wording is second-hand via Morris–Soltan and
  erdosproblems.com); Kalbfleisch–Stanton 1995 (citation only; zbMATH 403).
- Realizability classics known only through the Handbook chapter or the ∃R
  compendium, not retrieved themselves: Sturmfels 1987 (realizability over Q
  equivalent to Hilbert's tenth problem over Q; AMS 403), Bokowski–Sturmfels
  1986, Bokowski–Richter 1990, Shor 1991, Mnëv 1988, Felsner–Weil 2001,
  Krasser's 2003 TU Graz thesis, Bokowski's rubber-band heuristic.
- Blocked or unreadable: MathOverflow / Math.StackExchange (fetch blocked, no
  thread found by search); Matoušek, *Lectures on Discrete Geometry*,
  Chapter 3 (table of contents only); Brass–Moser–Pach, *Research Problems in
  Discrete Geometry* (publisher metadata only); Spektrum.de coverage (403);
  Scheucher's 2019/20 TU Berlin dissertation (both PDF URLs 404, depositonce
  renders by JavaScript; only the [Math Genealogy record](https://www.mathgenealogy.org/id.php?id=264081)
  and a search snippet saying Part I treats k-holes were retrieved — no
  quote could be verified); Mackey's 2025 CMU thesis text (announcement
  only, cited above as such); Scheucher's supplemental ES/highdim data
  (root 404).
- Search snippets only: the 0.2721 pseudoline constant and the OT₃
  double-exponential bound; the "n ≤ 6" fanchung copy of the UCSD page.
- Numbers not carried over: the Goaoc et al. journal entry cites
  "64,056,405 order types of size 8", which does not match the 3,315
  unlabelled realizable 8-point types and was not reconciled, so it is
  omitted; the Suk JAMS record and ETV 1996 record were cited by arXiv and DOI
  rather than by the OpenAlex queries through which they were found.
- False leads checked and discarded: Fabila-Monroy–Hahn–Leaños,
  arXiv 2606.07806 ("blow-ups" there are density Ramsey objects, unrelated
  to Baek–Balko blow-ups); García-Davila et al., arXiv 2303.17792 (a 16-point
  hexagon-free set mentioned only in passing per a snippet).
- Searches were budget-limited; a date-sorted arXiv math.CO check for 2026,
  the formal-conjectures / erdosproblems.com formalization entries, the
  Felsner–Weil signotope papers, Peters–Szekeres follow-ups and
  Koshelev–Koshka's finite 92/324 derivation remain unchecked. The
  Moshkovitz–Shapira and Fox–Pach–Sudakov–Suk texts were read only to 100k
  characters; Mathlib's `ErdosSzekeres` file was not located (404 at two
  paths), and Baek's `erdos-tuza-valtr` repository, found by one angle, could
  not be found by URL guess by another (an inconsistency between agents, not
  between sources).
