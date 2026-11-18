# NOVELTY20261113B: literature record of the novelty check of claims C1–C9 (13 November 2026)

**Rigor: evidence only (bounded literature search).** This record says what was searched, what was found and
how each claim compares with it. The word "new" is used here only in the sense "not found in the literature
by this search". It is never a priority claim. Absence of prior work in the sources below is evidence, not
proof. Titles and quotations keep their own wording.

**Main findings.**

1. **C5 (decomposition) has prior art, and two of its forms are false.**
   - The special case a = n is stated in a public repository (10 Aug 2026) and refuted there at n = 6 by a
     16-point set (committed 10 Oct 2026). The set was re-verified exactly (§8).
   - The same repository states an unproved split conjecture ("PASCAL-SPLIT", 2–4 Oct 2026). For u = k = n it
     is the project's strong form.
   - The strong form at (a, n) = (5, 6) fails on a real 15-point set derived from the public one (own exact
     check, §8).
   - The weak cap form with a < n was not found in the literature, and it survives these checks.
2. **C4 (N(7; 5, 7) ≤ 41) is one substitution into a printed lemma** (Javůrek's Lemma 3 with Baek's 16 and
   Schroeder's 25). The number itself was not found in print.
3. **C1, C2, C3, C6, C7, C8: the statements were not found.**
   - C1: no ES(8) bound at or below 310, no exact value for n ≥ 7, and no later version of Schroeder's
     preprint (81 and 319; refereed: 113 and 408).
   - C2: reductions of this kind are public (Javůrek; Schroeder). The statement is not, and public
     statements give only 380 from its hypothesis.
   - C3: 65 was not found. Printed statements give 78, not 84, by a two-line argument that is itself written
     nowhere.
   - C6: the equivalence was not found. Its easy direction follows from a printed lemma, and the threshold
     is a known incidence ratio.
   - C7: none of the numbers was found, and nothing sound for k = 8 or 9. The type of result is in print for
     k = 6 and 7.
   - C8: neither the split inequality nor any bound on N(8; 6, 6) below 70 was found. The first-layer
     formula is public.
4. **C9: every method component has precedent**, back to Chvátal–Komlós (1971) for the injective state map.
   Not found: a proof-assistant-checked bound for ES(7) or ES(8) better than Schroeder's 81 and 319.
5. **Unread sources that could change a verdict:** the journal version of Balko–Valtr (C4, C8), the journal
   version of Baek–Balko (C5, C8) and the comment thread of erdosproblems.com/107 (C1). See §5.

## 1. Date and scope

- **Date.** 13 November 2026. Access dates are 13 November 2026 unless stated.
- **Object.** Nine claims of the project (§2), as worded in the search brief.
- **Workflow.**
  1. Six searchers with separate sources.
     - `arxiv-recent`: arXiv only. A complete title-and-abstract scan of all 4,821 submissions of
       1 Sept – 13 Nov 2026 in math.CO, cs.CG, math.MG, cs.LO and cs.DM; a keyword-filtered scan of 2,291
       entries from January 2024 on; about 100 targeted queries.
     - `citations`: citation chasing with OpenAlex, Semantic Scholar, Crossref and the Zenodo and Figshare
       APIs.
     - `sites`: the Schroeder site and Zenodo record, Wikipedia, OEIS, the Erdős-problems database,
       formal-conjectures and public GitHub repositories.
     - `classics`: the classical literature on cups, caps and restricted Erdős–Szekeres numbers.
     - `symmetric-geometry`: symmetric and layered configurations (C6, C7).
     - `semantic`: Consensus (about 55 queries, three results each), the zbMATH Open API (about 25 queries)
       and web search.
  2. A synthesis, which re-opened primary sources where the searchers disagreed (§9).
  3. Nine adversarial attacks, one per claim, each told to find prior art with other search terms (§6).
  4. This record. While it was written, the exact checks on the public 16-point set were run once more (§8).
- **Covered.** arXiv to 13 Nov 2026; the citation graphs of OpenAlex and Semantic Scholar; Zenodo, Figshare,
  SSRN and OSF records; public GitHub repositories; zbMATH; OEIS; Wikipedia and MathWorld; the Stack
  Exchange keyword API; part of the 2025–2026 conference programmes.
- **Not covered.** MathSciNet, Google Scholar and DBLP (blocked); full-text search of arXiv; several
  paywalled journal texts (§5).
- **Labels.** "No prior art found", "partially anticipated" and "prior art found" are the labels of the
  searchers and the synthesis. Where the attack changed a label, both are given.
- **Trust in sources.** Several sources are unrefereed preprints or public repositories (Schroeder, Javůrek,
  GLitchfield, gotrevor). This is said where they are used. Repository dates are the dates written in files or
  commits; when the repositories became public is not established. Quotations are as reported by the
  searchers; several pages were read through a page-to-text tool.
- **Earlier checks.** NOVELTY20261106 (6 November) and the section "Novelty check" of RES33N20261113
  (13 November, 05:45–06:10 KST). The findings here are consistent with both. What this record adds is in §4.1
  and §10.
- **Later numbers.** The claims were checked as worded in §2. Records of the same day hold later numbers
  (ETV7SAT20261113: M(5; 7) ≤ 37; N66N20261113: N66 ≤ 59; both marked as in progress when read for this
  record). The comparison with the literature does not depend on them: no source has an upper bound for
  N(7; 5, 7) below the values of §3, or for N(8; 6, 6) below the cup-cap 70.
- **Process.** The searchers state that no project identifier, personal name or e-mail address was put into
  any query. One attack (C3) discloses that a few early read-only calls to a public repository went through
  the locally logged-in GitHub client.
- **Files.** This README is the whole record. It is written from the searcher, synthesis and attack reports,
  which are not stored in the repository. No other project file was changed, and nothing was committed,
  posted or sent.

## 2. Claims checked (wording of the search brief)

Notation. ES(n) is the least N such that every N points in general position in the plane contain n points in
convex position. A k-cap / k-cup is a set of k points on a concave / convex curve (x-monotone). N(n; a, b) is
the largest size of a set with distinct x-coordinates, in general position, with no a-cap, no b-cup and no
convex n-gon. The Erdős–Tuza–Valtr (ETV) conjecture says N(n; a, b) = Σ C(n−2, i) for i from n−b to a−2.
Schroeder and Javůrek write M_n(a, b) for the same number.

- **C1. Upper bounds on ES(8).** The project has ES(8) ≤ 310 (computer-assisted, checked in Lean,
  unrefereed). Comparison points known to the project: 408 (Mojarrad–Vlachos 2016, refereed), 319 and
  ES(7) ≤ 81 (M. Schroeder, preprint v1 of 19 Sept 2026, "Erdős–Szekeres: upper bounds for convex heptagons
  and octagons", michaelschroeder.ai and Zenodo DOI 10.5281/zenodo.22842891). *Question:* is there any newer
  version of that preprint, or any other 2025–2026 result, giving an ES(8) or ES(7) bound, or an exact value?
- **C2. A conditional reduction.** "If every 60-point set in general position with no 5-cap contains a convex
  octagon, then ES(8) ≤ 309" (obtained by level sets of the cup rank inside the residual part of Schroeder's
  omission method).
- **C3. An ETV-type bound for a = 5, n = 8.** Every 66-point set in general position (distinct x) contains a
  5-cap or a convex octagon, i.e. N(8; 5, 8) ≤ 65 (ETV value 42; cup-cap bound 84). *Question:* any bound for
  N(n; 5, n), or for any ETV number with a ≥ 5, better than the cup-cap bound?
- **C4. N(7; 5, 7) ≤ 41** (42 points contain a 5-cap or a convex heptagon), from Baek's theorem plus
  Schroeder's M₇(5,6) = 25. *Question:* which small ETV cases are settled in the literature (all n ≤ 6? which
  n = 7 cases?), by whom and how?
- **C5. A decomposition conjecture.** Every set with no a-cap and no convex n-gon is the union of a set with
  no (a−1)-cap and a set with no convex (n−1)-gon. Special case a = n: every set with no convex n-gon is the
  union of two sets with no convex (n−1)-gon (this would give ES(n) − 1 ≤ 2 (ES(n−1) − 1)). *Question:* does
  this or a similar partition/covering statement appear anywhere (Erdős–Szekeres partition problems, "convex
  position Ramsey" decompositions, Baek–Balko "decomposable sets", Ramsey-remainder)?
- **C6. A two-layer lemma.** Two concentric regular m-gons (radius ratio ρ, angular offset δ) contain m + 1
  points in convex position if and only if ρ > cos(π/m + δ) / cos(π/m), for m ≥ 4.
- **C7. Rotationally symmetric point sets with no convex octagon.** Maximum size exactly 60 for 6-fold
  symmetry and 64 for 7-fold symmetry; lower bounds 61, 52, 56 for 3-, 4-, 5-fold symmetry; for convex 9-gons
  an 8-fold symmetric set of 120 points. Comparison point known: Subercaseaux–Mackey–Qian–Heule,
  arXiv:2506.00224 (symmetric sets for hexagons and heptagons).
- **C8. An additive split.** The residual part of an octagon-free set has at most N(8; 5, 8) + N(8; 6, 6)
  points; and N(8; 6, 6) ≤ 64 from an internal state count. *Question:* any literature on the "first layer"
  ETV cases a + b = n + 4 (the only n-gons are (a−1)-cap + (b−1)-cup), beyond Baek (a = 4) and Schroeder
  ((5,6;7) = 25)? Is a general formula "ETV value = cup-cap bound minus C(a+b−6, a−3)" or a proof strategy
  for it discussed anywhere?
- **C9. Method-level prior art.** State catalogs / "omission" counting for cups and caps (Schroeder),
  monotone paths and line partitions (Moshkovitz–Shapira; Fox–Pach–Sudakov–Suk), SAT encodings by signotopes
  (Balko–Valtr, Scheucher, Marić, Heule–Scheucher), formal verification of ES-type results in
  Lean/Isabelle/Coq (e.g. ES(6) = 17, empty hexagon number 30).

## 3. Verdicts

| Claim | Verdict | Closest prior art | Sources (URLs) |
|---|---|---|---|
| **C1** ES(8) ≤ 310; later versions or better bounds | **No prior art found.** Synthesis and attack agree. | Schroeder v1 (19 Sept 2026, unrefereed): "33 ≤ ES(7) ≤ 81, 65 ≤ ES(8) ≤ 319". Still the only version: the Zenodo versions API returns total = 1 (created and modified 2026-09-19), the author's sitemap lists only the v1 PDF and the companion page, and a v2 PDF URL returns 404. Refereed: Mojarrad–Vlachos, Theorem 1.1, 113 and 408; Tóth–Valtr 2005, 127 and 463. No bound in Javůrek (1 Nov 2026), Dumitru or Zeng. Caveat: Koshelev–Koshka, Table 1, prints 92 and 324 in a Norin–Yuditsky row; Norin–Yuditsky prove only limsup ≤ 7/8. 310 is below 319, 324 and 408. | [Schroeder DOI](https://doi.org/10.5281/zenodo.22842891), [Zenodo versions API](https://zenodo.org/api/records/22842891/versions), [v1 PDF](https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf), [companion page](https://michaelschroeder.ai/research/ErdosSzekeres/companion), [arXiv:1510.06255](https://arxiv.org/abs/1510.06255), [Tóth–Valtr 2005](https://library.slmath.org/books/Book52/files/30toth.pdf), [arXiv:1509.03332](https://arxiv.org/abs/1509.03332), [arXiv:2604.20120](https://arxiv.org/abs/2604.20120), [Figshare 34875984](https://doi.org/10.6084/m9.figshare.34875984), [arXiv:2512.24061](https://arxiv.org/abs/2512.24061), [SSRN 7334758](https://doi.org/10.2139/ssrn.7334758), [erdosproblems.com/107](https://www.erdosproblems.com/107) (HTTP 403 for most readers) |
| **C2** N(8; 5, 8) ≤ 59 ⇒ ES(8) ≤ 309 | **Partially anticipated.** The kind of reduction is public. The statement was not found and does not follow from public statements. | Javůrek: ES(n+1) ≤ 3B_n − 3 with B_n − 1 = M_{n+1}(n−1, n+1), and the conditional "B6 ≤ 27, hence ES(7) ≤ 78" through the ETV case (7; 5, 7); nothing numerical for octagons. Schroeder: Theorem 3.2 (ES(n) ≤ C_n + D_n + 2), Lemma 7.5 (Baek's 4-cap capacity as 23 rows of the residual catalogue), Theorem 4.3 (D₇ ≤ B + 5), §9 conditionals; further capacities "are open tasks". Classical: ES(n) ≤ p(n) + 1 (Mojarrad–Vlachos Theorem 4.3, after Tóth–Valtr). Cup-rank rows appear in Baek's a = 4 proof. | [Figshare 34875984](https://doi.org/10.6084/m9.figshare.34875984), [Schroeder v1 PDF](https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf), [arXiv:1510.06255](https://arxiv.org/abs/1510.06255), [arXiv:2206.04260](https://arxiv.org/abs/2206.04260), [Tóth–Valtr 2005](https://library.slmath.org/books/Book52/files/30toth.pdf) |
| **C3** N(8; 5, 8) ≤ 65 | **Partially anticipated.** 65 was not found. The baseline from printed statements is 78, not 84. | Endpoint split (Javůrek's Lemma 3) with Baek's N(8; 4, 8) = 22 and the cup-cap value N(8; 5, 7) ≤ 56 gives 78; this is written nowhere for a = 5. Bounds below cup-cap with a ≥ 5 exist for a = n−1 (Mojarrad–Vlachos Theorem 4.2: 31, 111, 406 against 35, 126, 462), for a = n (Chung–Graham), and in Schroeder (M₇(5,6) = 25, M₇(6,6) ≤ 49, M₈(7,7) ≤ 193; unrefereed). Balko–Valtr 2015: cup-cap is the best known general bound. The case a = 5, b = n is listed as open by GLitchfield, gotrevor and Javůrek. Baek's 2018 KAIST abstract announces a Suk-type bound for ETV(a,n,n), with no written proof. | [arXiv:2206.04260](https://arxiv.org/abs/2206.04260), [arXiv:1510.06255](https://arxiv.org/abs/1510.06255), [Balko–Valtr 2015](https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf), [Schroeder v1 PDF](https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf), [Figshare 34875984](https://doi.org/10.6084/m9.figshare.34875984), [Chung–Graham](https://www.lix.polytechnique.fr/Labo/Ilan.Vardi/chung_graham.pdf), [KAIST abstract](https://mathsci.kaist.ac.kr/~sangil/seminar/2018-09-10/), [EtvCapFiveAll.lean](https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/ESBlueprint/C/EtvCapFiveAll.lean), [experiment 0112](https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/experiments/0112-etv-parameter5-signotope.md), [es7-ladder PLAN.md](https://raw.githubusercontent.com/gotrevor/es7-ladder/master/docs/PLAN.md) |
| **C4** N(7; 5, 7) ≤ 41; settled small ETV cases | **Partially anticipated** (synthesis); **prior art found** (attack). C4 is one substitution into a printed lemma. The number 41 was not found in print. | Javůrek's Lemma 3, M_k(a,b) ≤ M_k(a−1,b) + M_k(a,b−1), at (7; 5, 7) with Baek's Theorem 1.6 (16) and Schroeder's Theorem 5.2 (25). Javůrek's Lemma 2 isolates the same number (B₆ − 1 = M₇(5,7)) and leaves the 27-point exclusion open. Refereed statements alone give 16 + 35 = 51; cup-cap 56; lower bound 26. Settled cases: n ≥ a+b−3 (cups-caps); all n ≤ 6 (an inference, §6); a = 4 or b = 4 (Baek); (7; 5, 6) = 25 (Schroeder; gotrevor by SAT). | [arXiv:2206.04260](https://arxiv.org/abs/2206.04260), [Schroeder v1 PDF](https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf), [Figshare 34875984](https://doi.org/10.6084/m9.figshare.34875984), [arXiv:2607.02958](https://arxiv.org/abs/2607.02958), [Balko–Valtr 2015](https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf), [es7-ladder](https://github.com/gotrevor/es7-ladder), [es7-ladder PLAN.md](https://raw.githubusercontent.com/gotrevor/es7-ladder/master/docs/PLAN.md), [experiment 0112](https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/experiments/0112-etv-parameter5-signotope.md), [jcpaik/erdos-tuza-valtr](https://github.com/jcpaik/erdos-tuza-valtr), [arXiv:2403.17370](https://arxiv.org/abs/2403.17370), [SoCG 2025](https://doi.org/10.4230/LIPIcs.SoCG.2025.13), [Szekeres–Peters](https://doi.org/10.1017/S144618110000300X) |
| **C5** decomposition conjecture | **Prior art found.** The special case a = n is public and false at n = 6. A stronger form of the general statement is public as an unproved conjecture. The weak cap form with a < n was not found verbatim. | GLitchfield repository (unrefereed): experiment 0096 (10 Aug 2026) asks for the two-class split and proves the doubling consequence in Lean; the fixture split6-counterexample-v1.json (committed 10 Oct 2026) is a 16-point set with no convex hexagon and no bipartition into two pentagon-free sets; the predecessor-half conjecture (4 Sept 2026) is a Lean theorem there for k ≤ 6; the PASCAL-SPLIT notes (2–4 Oct 2026) state a split for all (a, u, k). gotrevor: Pascal split L1(a, b) on the first diagonal, false at (5, 6) for abstract 2-colourings. Classical splits lower cap or cup lengths but not the polygon size. | [split6 fixture](https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/harness/research/examples/split6-counterexample-v1.json), [facts file](https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/harness/research/examples/convexity-axioms7-v1.json), [experiment 0096](https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/experiments/0096-strong-predecessor-property-b.md), [predecessor-half note](https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/plans/predecessor-half-conjecture.md), [PASCAL-SPLIT note](https://github.com/GLitchfield/erdos-szekeres-convex-poly/blob/main/docs/research/archive-2026-09-28-to-10-05/claude-pascal-20261002/HANDOFF.md), [PSL survey note](https://github.com/GLitchfield/erdos-szekeres-convex-poly/blob/main/docs/research/archive-2026-09-28-to-10-05/claude-survey-20261004/PROBLEM.md), [HUMAN-P756.md](https://raw.githubusercontent.com/gotrevor/es7-ladder/master/docs/HUMAN-P756.md), [SoCG 2025](https://doi.org/10.4230/LIPIcs.SoCG.2025.13), [arXiv:1510.06255](https://arxiv.org/abs/1510.06255), [arXiv:2206.04260](https://arxiv.org/abs/2206.04260), [Bárány–Károlyi survey](https://www.renyi.hu/~barany/cikkek/85.pdf), [ETV 1993 report](http://web.archive.org/web/20170706013611/ftp://ftp.inf.fu-berlin.de/pub/reports/tr-b-93-01.ps.gz) |
| **C6** two-layer lemma | **No prior art found** for the equivalence. The easy direction follows from a printed lemma, and the threshold is a known incidence ratio. | Dehnhardt–Harborth–Lángi, Lemma 1 (points of an outer polygon beyond exactly the same edge of an inner polygon are in convex position with it): the "if" half in generic form, with no regular polygons, threshold or converse. Hang Lung 2010 school paper: three concentric regular pentagons plus the centre, and a one-point criterion with no threshold. Mathar, eq. (12) and (26): the same ratio, in a circumscription problem. | [Dehnhardt–Harborth–Lángi](https://www.math.u-szeged.hu/~zlangi/publications/ErdosSzekeres.pdf), [arXiv:1301.6293](https://arxiv.org/abs/1301.6293), [Hang Lung 2010](https://hlma.hanglung.com/assets/3EE1F601-28F3-4DD9-ABDE-6D75F6E2D4CF/013.pdf), [Ábrego–Fernández-Merchant](https://cgt-journal.org/index.php/cgt/article/download/75/79/800), [arXiv:2506.00224](https://arxiv.org/abs/2506.00224), [CMU-CS-25-108](http://reports-archive.adm.cs.cmu.edu/anon/2025/CMU-CS-25-108.pdf), [Math.SE 3983965](https://math.stackexchange.com/questions/3983965/visualizing-lower-bound-for-the-happy-ending-problem-small-cases) |
| **C7** symmetric sets with no convex octagon or 9-gon | **Partially anticipated.** None of the numbers and nothing sound for k = 8, 9 was found. The type of result and the method are in print for k = 6, 7. The attack's "prior art found" is in the must-cite sense only. | Subercaseaux–Mackey–Qian–Heule: 16 points with no 6-gon, 4- and 5-fold exist, 3-fold does not; 32 points with no 7-gon, only s ∈ {1, 2, 4} possible, 4-fold not realizable, 2-fold open; "we suspect that there are symmetric constructions for all k ≥ 7". Mackey's thesis: hexagons only. Hang Lung 2010: an exactly 5-fold 16-point hexagon-free set. Warrier 2024: a hand-made, roughly 7-fold 36-point arrangement for octagons, unsound. Unsymmetric 64-point sets: Baek–Balko, AlphaEvolve. | [arXiv:2506.00224](https://arxiv.org/abs/2506.00224), [CMU-CS-25-108](http://reports-archive.adm.cs.cmu.edu/anon/2025/CMU-CS-25-108.pdf), [arXiv:2607.02958](https://arxiv.org/abs/2607.02958), [arXiv:2604.20120](https://arxiv.org/abs/2604.20120), [arXiv:2511.02864](https://arxiv.org/abs/2511.02864), [Hang Lung 2010](https://hlma.hanglung.com/assets/3EE1F601-28F3-4DD9-ABDE-6D75F6E2D4CF/013.pdf), [Warrier 2024](https://indianmathsoc.org/pdf/Mathstudent-V93-part3-4-2024.pdf), [OEIS A006788](https://oeis.org/A006788), [automatic-symmetries](https://github.com/bsubercaseaux/automatic-symmetries), [SoCG 2025](https://doi.org/10.4230/LIPIcs.SoCG.2025.13) |
| **C8** residual ≤ N(8; 5, 8) + N(8; 6, 6); N(8; 6, 6) ≤ 64 | **Partially anticipated.** The split inequality and the bound were not found. The first layer, its formula and the split device are public. | For (8; 6, 6) the literature has only cup-cap 70 and the lower bound 50. Balko–Valtr 2015 name k = a+u−4 "this first nontrivial case". gotrevor: "Cups-caps allows C(a+b-4, a-2) vertices; the diagonal value is exactly C(a+b-6, a-3) fewer" (a Lean identity for the conjectured value). Mojarrad–Vlachos Theorem 3.6: the same expression for a different quantity h(m, l). Baek–Balko Lemma 9: the ETV sum counts down-sets with a bounding-box condition. Schroeder: Lemma 5.3 (the same endpoint split, for the balanced heptagon part), "Dn ≤ Mn(n − 2, n)", D₈ ≤ 124. | [Balko–Valtr 2015](https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf), [HUMAN-P756.md](https://raw.githubusercontent.com/gotrevor/es7-ladder/master/docs/HUMAN-P756.md), [arXiv:1510.06255](https://arxiv.org/abs/1510.06255), [arXiv:2206.04260](https://arxiv.org/abs/2206.04260), [SoCG 2025](https://doi.org/10.4230/LIPIcs.SoCG.2025.13), [Schroeder v1 PDF](https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf), [ES_SAT data page](https://kam.mff.cuni.cz/~balko/ES_SAT), [MathOverflow 277192](https://mathoverflow.net/questions/277192/a-new-polygon-forcing-theorem), [KAIST abstract](https://mathsci.kaist.ac.kr/~sangil/seminar/2018-09-10/) |
| **C9** methods | **Prior art found** for every component. Not found: a proof-assistant-checked bound for ES(7) or ES(8) better than 81 and 319. | State maps and counting: Chvátal–Komlós 1971, Moshkovitz–Shapira, Norin–Yuditsky, Mojarrad–Vlachos, Baek, Baek–Balko, Schroeder. Monotone paths: Fox–Pach–Sudakov–Suk. SAT on signotopes or triple orientations: Szekeres–Peters, Balko–Valtr, Marić, Scheucher, Heule–Scheucher, Subercaseaux et al., Krapivin–Przybocki–Heule. Formal: Marić (Isabelle), Subercaseaux et al. (Lean), Baek (Lean), Schroeder (Lean), and bounds valid for all n in GLitchfield, linrock (Lean) and meesu (Isabelle). | [Chvátal–Komlós](https://doi.org/10.4153/CMB-1971-028-8), [arXiv:1206.4001](https://arxiv.org/abs/1206.4001), [arXiv:1105.2097](https://arxiv.org/abs/1105.2097), [arXiv:1509.03332](https://arxiv.org/abs/1509.03332), [MathOverflow answer 91128](https://mathoverflow.net/a/91128), [arXiv:2411.19823](https://arxiv.org/abs/2411.19823), [arXiv:1510.06255](https://arxiv.org/abs/1510.06255), [arXiv:2206.04260](https://arxiv.org/abs/2206.04260), [SoCG 2025](https://doi.org/10.4230/LIPIcs.SoCG.2025.13), [Schroeder DOI](https://doi.org/10.5281/zenodo.22842891), [Balko–Valtr 2015](https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf), [Marić](https://doi.org/10.1007/s10817-017-9423-7), [arXiv:2105.08406](https://arxiv.org/abs/2105.08406), [arXiv:2403.00737](https://arxiv.org/abs/2403.00737), [arXiv:2403.17370](https://arxiv.org/abs/2403.17370), [arXiv:2506.00224](https://arxiv.org/abs/2506.00224), [arXiv:2607.02958](https://arxiv.org/abs/2607.02958), [arXiv:2607.00815](https://arxiv.org/abs/2607.00815), [arXiv:2610.36648](https://arxiv.org/abs/2610.36648), [arXiv:2609.25199](https://arxiv.org/abs/2609.25199), [jcpaik/erdos-tuza-valtr](https://github.com/jcpaik/erdos-tuza-valtr), [es7-ladder](https://github.com/gotrevor/es7-ladder), [GLitchfield](https://github.com/GLitchfield/erdos-szekeres-convex-poly), [linrock](https://github.com/linrock/math-proofs/blob/cd3cf0b176e95209584bf35555a7c0e501255f6e/erdos-107/Solution.lean), [meesu](https://github.com/meesu/isabelle-convex-polygon) |

How to read the table.
- **Yes/no result of the attack** ("is there prior art that a careful author would have to cite?"): C1 no,
  C2 no, C3 no, C4 yes, C5 yes, C6 no, C7 yes, C8 no, C9 yes.
- The attackers did not use one threshold. For C7 the "yes" means must-cite partial anticipations only; that
  attack states that no source contains C7 or any of its numbers. C2, C3 and C8 have must-cite precedents and
  a "no".
- Counted by one rule (the statement, a stronger statement, a refutation, or a printed lemma that gives it in
  one step is public): **prior art for C4, C5, C9; none found for C1, C2, C3, C6, C7, C8.**

## 4. Papers and sources found or updated

### 4.1 Not in the project's records before this check

"Not in the records" means: no hit for the author, title or repository name in the READMEs under `results/`, in
`results/LIT` or in `docs/` (grep, 13 November). The GLitchfield repository itself was known (NOVELTY20261106);
the files listed here were not.

- **T. Javůrek (Javurek), "Uncovered hull vertices and upper bounds for convex polygons"** ([Figshare][jav];
  working draft of 31 Oct 2026, v1 posted 1 Nov 2026; unrefereed; not on arXiv).
  - *Proves.* "Lemma 2. For n ≥ 4, B_n − 1 = M_{n+1}(n − 1, n + 1), ES(n + 1) − 2 = M_{n+1}(n, n + 1)"; Lemma 3,
    the endpoint split M_k(a, b) ≤ M_k(a−1, b) + M_k(a, b−1); "Theorem 5. For every n ≥ 4,
    ES(n + 1) ≤ 3B_n − 3". Conditional: "Excluding 28 original points with no heptagon and an uncovered hull
    vertex proves B6 ≤ 27, hence ES(7) ≤ 78". "Exact local witnesses establish B6 ≥ 27". "No improved
    numerical upper bound is established in this paper."
  - *Why it matters.* Closest prior art for C2 and C4. It names the ETV case (7; 5, 7) as the exclusion that
    would improve ES(7), which is the target of ETV7SAT20261113.
- **GLitchfield/erdos-szekeres-convex-poly, SPLIT(6) fixture** ([fixture][gl-split6], committed 10 Oct 2026;
  [facts file][gl-facts]).
  - *Contains.* "SPLIT(6) counterexample: 16 integer points in general position with no convex hexagon and no
    bipartition into two pentagon-free sets"; "SPLIT(6) is FALSE for real point sets"; the split exists for
    every set of at most 15 points (signotope SAT; their claim).
  - *Why it matters.* It refutes the a = n case of C5 at n = 6. Verified exactly (§8).
- **Same repository, split and half-subset notes** ([experiment 0096][gl-0096], [predecessor-half
  note][gl-half], [PASCAL-SPLIT note][gl-pascal], [PSL survey note][gl-survey], [research plan][gl-plan]).
  - *Contains.* The two-class split question with a Lean-proved doubling consequence (10 Aug 2026). The
    predecessor-half conjecture (4 Sept 2026), a Lean theorem there for k = 4, 5, 6 and open for k = 7, 8.
    PASCAL-SPLIT / PSL for all (a, u, k) (2–4 Oct 2026), unproved. A band-stack statement FBDL(6), also
    refuted there at 16 points ([fixture][gl-fbdl]). The plan calls the half conjecture "Not known from the
    literature" and intends to "publish as a short note or MathOverflow question".
  - *Why it matters.* Prior art for C5: the special case, a weaker half-subset form, and a stronger form of
    the general statement.
- **Same repository, cap parameter 5** ([experiment 0112][gl-0112], 4 Sept 2026; [Lean node][gl-cap5];
  [status table][gl-status]).
  - *Contains.* The Lean node `etvCapFive_all` is a `sorry` and is listed as an open conjecture. SAT at the
    signotope level: (6, 5, 6) SAT at 15 points and UNSAT at 16; (7, 5, 7) SAT at 26 points and UNKNOWN at 27
    after a 10,800 s limit. "No upper bound is claimed" for n = 7. Nothing at n = 8.
  - *Why it matters.* C3 and C4: the case a = 5 is posed there as open, with no bound.
- **gotrevor/es7-ladder** ([repository][gt], 5–7 Oct 2026, unrefereed; [PLAN.md][gt-plan];
  [HUMAN-P756.md][gt-p756]; [LOCALITY.md][gt-local]).
  - *Contains.* "P(7,5,6) holds at 26" (6 Oct 2026): SAT on x-sorted signotopes, all 49,582 subcubes UNSAT,
    82 CPU h, "answer-only" ("no DRAT/LRAT proof was logged"); it does not cite Schroeder. A table of the
    k = 7 rungs, with (5, 7), (6, 6), (6, 7), (7, 7) open. The first-diagonal hole formula with a Lean lemma
    `d1N_add_holes`. The Pascal split conjecture L1(a, b), with "L1(5,6) is false" for abstract 2-colourings
    (49 colourings on 23–25 vertices; no failure on 40 signotope samples). Rungs with k ≤ 6 and (7, 4, 7) hold
    for arbitrary 2-colourings of triples. The projective symmetry break is noted as invalid with cap/cup
    constraints.
  - *Why it matters.* C4 (an independent confirmation of (7; 5, 6) = 25), C5 and C8 (the split and the
    formula are public), C9.
- **Dehnhardt–Harborth–Lángi, "A partial proof of the Erdős–Szekeres conjecture for hexagons"**
  ([author-hosted PDF][dhl]). *Proves* Lemma 1 on points beyond exactly the same edge of an inner polygon.
  *Why it matters:* the easy direction of C6 is a one-line corollary.
- **R. J. Mathar, "Tightly Circumscribed Regular Polygons"** ([arXiv:1301.6293][mathar]). *Contains* eq. (12):
  the radius ratio at which a vertex of one concentric regular polygon lies on a side of the other,
  cos[j_i φ_n − (j_o + 1/2) φ_m] / cos(φ_m/2); eq. (26) adds a rotation. *Why it matters:* the same expression
  as the C6 threshold, in a circumscription problem.
- **Hang Lung Mathematics Awards 2010, "The Erdős–Szekeres Conjecture ('Happy End Problem')"** ([PDF][hl10];
  a school paper). *Contains* a 16-point hexagon-free set of type (5,5,5,1), "3 concentric regular pentagons
  with different sizes and their centre O", and "Lemma 13. Any point set of (5, 2) containing a convex hexagon
  if and only if the line joining the points inside the pentagon intersect two adjacent sides of the
  pentagon". *Why it matters:* an early exactly 5-fold extremal set (C7) and a two-layer criterion without a
  threshold (C6).
- **Ábrego–Fernández-Merchant, "Bounds on the Crossing Number of m-Fold Symmetric Configurations of Points in
  the Plane"** ([Computing in Geometry and Topology 5(2)][afm]; preliminary version CCCG 2024). *Contains*
  layered m-fold symmetric sets ("we refer to the orbit Lj := [wj] (which is a regular m-gon with vertices wj
  and its m − 1 rotations) as a layer") with lemmas on k-edges, halving lines and crossings. *Why it matters:*
  related work on the objects of C6 and C7; not an anticipation.
- **P. B. Warrier, "The physiognomy of the Erdős–Szekeres conjecture (happy ending problem)"** ([The
  Mathematics Student 93 (3–4), 2024, pp. 28–48][warrier]). *Contains* a hand-made, roughly 7-fold
  arrangement for the octagon problem: a regular heptagon, points "along each vertex" and the centre, 36
  points with printed coordinates. It concludes P(8) = 37, against the proven ES(8) ≥ 65. *Why it matters:*
  an earlier, unsound attempt at the template of C7 (§8, E7).
- **OEIS A006788, comment of 15 Sep 2002** ([entry][oeis-a006788]) on a(n) = floor(2^(n−1)/n), a(7) = 9: "This
  is the number of nested polygons needed to produce a graph that is always concave, see the MathWorld
  article." *Why it matters:* a one-line unproven remark with the same count as nine heptagons in 64 points
  (C7).
- **V. Chvátal, J. Komlós, "Some combinatorial theorems on monotonicity"** ([Canad. Math. Bull. 14 (1971)
  151–157][ck71]). *Proves* cups-caps for an arbitrary real function on the pairs of an ordered set,
  F(p, q) = C(p+q−2, p−1), by an injective map from vertices to antichains of maximal labels. *Why it
  matters:* the state-map argument of C9, 43 years before Moshkovitz–Shapira.
- **Mulrenin–Pohoata–Zakharov, "Color avoidance for monotone paths"** ([arXiv:2411.19823][mpz]; Discrete
  Analysis 2025:23). *Contains* the down-set map with its injectivity, credited to Chvátal–Komlós and
  Seidenberg, and the principle of injecting "into a significantly smaller space than the collection of
  down-sets". *Why it matters:* the omission principle in print, for another problem (C9).
- **S. Norin, MathOverflow answer 91128** ([13 March 2012][norin-mo]). *Contains* the two-letter-word encoding
  of each point. *Why it matters:* the public origin of the Norin–Yuditsky method (C9).
- **linrock/math-proofs, erdos-107** ([Solution.lean][linrock], Lean; linked from
  [formal-conjectures][fc107]) and **meesu/isabelle-convex-polygon** ([repository][meesu], Isabelle/HOL).
  *Contain* `f_le_erdosSzekeresUpper : ∀ n ≥ 3, f n ≤ Nat.choose (2 * n - 4) (n - 2) + 1` and
  `EZ_bound_final`, the 1935 bound (253 and 925 at n = 7, 8). *Why it matters:* proof-assistant-checked bounds
  valid for n = 7, 8 exist outside Schroeder's work (C9).
- **S. Szeider, "Streaming LRAT Certificates into Lean Theorems"** ([arXiv:2607.00815][szeider]) and
  **M. Tatarevic, "An upper bound of 60 for the Ramsey number R(3,3,3,3)"** ([arXiv:2610.36648][tat]). *Why
  they matter:* the closest recent analogues of a certificate-to-Lean pipeline (C9). Neither treats convex
  polygons.
- **MathOverflow question 277192** ([2017][mo277192]). *Contains* computed forcing numbers for a cap, a cup
  and one polygon type; they match the first-layer ETV values for n ≤ 6 only (for example 14 for 5-cap, 5-cup,
  (4,4)-hexagon). *Why it matters:* a minor precedent for C4 and C8.
- **Adamczewski–Bloom, "FrontierMath Erdős"** ([arXiv:2609.25050][fm]). *Contains* Erdős problem 107 in a
  list of problems open as of August 2026. *Why it matters:* state of C1.

### 4.2 Sources the project already uses: status, and passages that matter here

- **M. Schroeder, "Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons"** ([DOI][sch-doi];
  [PDF][sch-pdf]; [companion page][sch-comp]). *Status:* no update. Zenodo has exactly one version
  ([versions API][sch-ver]) and the author's [sitemap][sch-site] lists only the v1 PDF and the companion page.
  *Passages that matter here:* Theorem 3.2; Theorem 4.3; Theorem 5.2 (M₇(5,6) = 25); Lemma 5.3; Lemma 7.5;
  Propositions 7.3, 7.4 and 7.6; Section 9; footnote 1 on the 92/324 table entries ("We have not located their
  finite derivation in the cited proof"). "External peer review is not claimed."
- **Koshelev–Koshka, "Combinatorial Geometry of Erdős–Szekeres Type Problems: SAT/ASP Modeling and Linear
  Subreduction"** ([arXiv:2604.20120][kk], still v1). Table 1 prints 92 and 324 for n = 7, 8 in a row "2015,
  Norin–Yuditsky, (7/8 + o(1)) C(2n−5, n−2)", with no derivation. *Why it matters:* a referee may quote 324
  instead of 408 as the figure before 2026. k-fold symmetry is used there for empty-hexagon variants only.
- **Krapivin–Przybocki–Heule, "Toward Satisfiability Modulo Realizability"** ([arXiv:2607.02958][kph],
  CICM 2026). "PointSAT can find a set of 26 points with no 5-cap or 7-gon"; "For the 32 point problem, we ran
  PointSAT for 2191 core hours, and it generated 200,000 abstract solutions but did not find any solutions."
  *Why it matters:* the lower bound 26 for (7; 5, 7) is realized (C4). Nothing on octagons or symmetric sets
  (C7).
- **Baek–Balko, "The Erdős–Szekeres conjecture revisited"** ([SoCG 2025][bb]; journal version
  [J. Combin. Theory Ser. A 222 (2026) 106195][bb-jcta], 29 pages against 15). The ETV formula "is known to be
  true only in the trivial case k ≥ a + u − 3 and Baek [1] proved it when a or u equals 4". It is proved there
  for split polygons and for decomposable sets. *Why it matters:* C3, C4, C5, C8. The journal text was not
  accessible (§5).
- **Mojarrad–Vlachos, "An improved upper bound for the Erdős–Szekeres conjecture"**
  ([arXiv:1510.06255][mv]). More than the source of 408: Theorem 4.2 bounds N(n; n−1, n) below cup-cap
  ("the set S of f(n − 1, n − 1) + g(n, n − 2) + 1 points ... Then S contains an (n − 1)-cap or a convex
  n-gon"), and Theorem 3.6 has the expression C(m+l−4, l−2) − C(m+l−6, l−3), the first-layer ETV value, for
  the convexification function h(m, l). *Why it matters:* C3 and C8.
- **Balko–Valtr, "A SAT attack on the Erdős–Szekeres conjecture"** ([EuroComb 2015 extended
  abstract][bv15]; [data page][bv-data]). "The gap between known bounds for N(a, u, k) appears first for
  k = a+u-4"; Proposition 3.2, N(4, k, k) ≤ C(k, 2) − 1; SAT on pseudolinear colourings: "we have
  N(4, 7, 7) = 16 and N(4, 8, 8) = 22"; the abstract analogue fails at (5, 6, 7) and (6, 6, 7). *Why it
  matters:* C4 and C8. The journal version is unread (§5).
- **E. Mackey, "Pinwheels and Polygons"** ([CMU-CS-25-108][mackey]). Opened in full by the synthesis and by
  the C7 attack (65 pages): 16-point hexagon-free sets with 3-, 4- and 5-fold symmetry only; for 7-gons,
  4-fold "realizations with no more than 24 points"; nothing on octagons. *Why it matters:* it removes an
  unread comparison point for C7.
- **B. Dumitru** ([arXiv:2512.24061][dum], still v1) and **Z. Zeng** ([SSRN][zeng], abstract only): partial SAT
  attacks on the 33-point problem, with no bound ("this paper does not determine ES(7)"). *Why they matter:*
  no competing ES(7) or ES(8) bound (C1).
- **J. Baek, KAIST seminar abstract, 10 Sept 2018** ([page][baek-kaist]). It announces an adaptation of Suk's
  argument to ETV(a, n, n) and an improvement of order √n for a = 4. *Why it matters:* the only trace of a
  general-a upper-bound idea for ETV numbers (C3); no written proof was found.
- **Georgiev–Gómez-Serrano–Tao–Wagner** ([arXiv:2511.02864][ae], v3): AlphaEvolve re-found 2^(k−2)-point sets
  up to k = 8, with no improvement and no symmetry statement (C1, C7).

## 5. Sources that could not be read

- **Balko–Valtr, European J. Combin. 66 (2017) 13–23** ([DOI][bv17]). HTTP 403 for every searcher, the
  synthesis and the attacks; the thesis copy timed out or returned 429. Read instead: the 2015 extended
  abstract, the slides and the data page. It may list pseudolinear SAT verifications beyond (4, 7, 7) and
  (4, 8, 8), in particular (5, 6, 7), which would predate Schroeder's M₇(5,6) = 25 as a computer verification
  (C4, C8).
- **Baek–Balko, J. Combin. Theory Ser. A 222 (2026) 106195** ([DOI][bb-jcta]), full text: HTTP 403 although
  open access. The SoCG 2025 version omits the proofs of Lemma 9 and Theorems 7 and 8 (C5, C8).
- **erdosproblems.com/107 and its comment thread** ([page][ep107]): HTTP 403 for three searchers, the
  synthesis and all attacks. One searcher read it (last edited 11 April 2026; no explicit bounds for 7 or 8
  points; two comments from December 2025). A recent comment on ES(7) or ES(8) would be missed (C1).
- **Springer version of Subercaseaux–Mackey–Qian–Heule** ([CICM 2025, LNCS 16136, pp. 29–47][smqh-springer]):
  login redirect. Only arXiv v1 was read; an added remark on octagons would be missed (C7).
- **Schroeder's appendices A–C and the 240 MB archive** ([Zenodo record][sch-rec]). The attacks read the
  documentation files of the archive by range requests. The Lean modules, the certificate data and the
  "literature supplement" on the 92/324 entries were not inspected (C1, C2, C8).
- **Javůrek's "companion paper on uncovered vertices and exact mutations"**, mentioned in [his draft][jav]:
  not found on Figshare or OpenAlex. His appendix was read only in part (C2, C4).
- **GLitchfield repository** ([repository][gl]): HALVING.md and the run logs behind the SPLIT(6)
  counterexample are in a git-ignored folder and not public. Only selected documents of the repository were
  read. Whether the planned MathOverflow question or short note exists is unknown (C5).
- **MathOverflow and Math.StackExchange**: blocked for the searchers and for page fetches. They were searched
  only through the Stack Exchange keyword API, which matches all query words and cannot search by formula. An
  elementary source for C6, or a question on the two-set split, could be missed (C5, C6).
- **Erdős–Tuza–Valtr, "Ramsey-remainder", European J. Combin. 17 (1996) 519–532** ([DOI][etv96]): blocked. One
  searcher read the 1993 FU Berlin technical report from an [archive copy][etv93]; numbering and added remarks
  of the journal version are unchecked (C3, C5, C8).
- **Google Scholar and DBLP**: blocked. Citers come from OpenAlex and Semantic Scholar only, and the Schroeder
  DOI is not indexed by Semantic Scholar (C1).
- **Not opened in full:** Marić ([J. Automated Reasoning 2019][maric]); Károlyi ([Discrete Appl. Math.
  2001][karolyi01]); Pór–Valtr (DCG 2002); Károlyi–Tóth ([DCG 2012][kt12]); Morris–Soltan (2016 book chapter);
  Suk's 2025 survey ([zbMATH listing][suk25]); Zeng's SSRN full text; Seidenberg 1959; Romig's Zenodo PDF
  ([record][romig], files restricted); Bonnice 1974; Dehnhardt's 1981 Diplomarbeit. None is expected to
  contain an octagon bound, but none was verified (C1, C5, C6, C9).
- **Search limits.** The shared web-search budget ran out in every attack (after 13 to about 50 queries).
  Not run for that reason: several non-English queries; programme checks for CCCG 2026, GD 2026, EuroComb 2025
  (C7 attack) and ITP/CPP/CICM 2026 (C9 attack); phrase searches for pages citing Schroeder's DOI (C1 attack).
  Consensus returned three results per query. arXiv has no full-text search, so a paper that mentions these
  topics only in its body can be missed.

## 6. Adversarial prior-art attack, claim by claim

Each attack was told to refute the "not found" verdict with other search terms. "Result" is its yes/no answer.

### C1 (ES(8) ≤ 310). Result: no prior art found

- No source states ES(8) ≤ 310 or better, an ES(7) bound below 81, an exact value for n ≥ 7, or a later
  version of the Schroeder preprint.
- **Strongest candidate.** [Schroeder v1][sch-pdf]: "We prove ES(7) ≤ 81 and ES(8) ≤ 319". [Companion
  page][sch-comp]: "Version 1 · 19 September 2026", "No external peer review is claimed." It is weaker than
  310.
- **Re-checked on 13 November.**
  - Schroeder: the [versions API][sch-ver] gives total = 1; the author's site lists 11 items up to
    9 Nov 2026, one on this topic; OpenAlex shows 0 citing works.
  - arXiv API, date-sorted, with further terminology (convex k-gon, convexly independent, happy ending,
    signotopes, order types, cups and caps, monotone paths): nothing with a bound for n = 7 or 8.
    [Dumitru][dum] and [Koshelev–Koshka][kk] are still v1.
  - Reference pages: [Wikipedia][wiki] (edited 11 Aug 2026), "The value of f(N) is unknown for all N > 6";
    [MathWorld][mathworld] (updated 12 Nov 2026) gives no numeric bound for 7 or 8; the [Erdős-problems data
    file][teorth] still has problem 107 open; [formal-conjectures 107.lean][fc107] has no numeric variant.
  - [Norin–Yuditsky][ny] re-read: only limsup ≤ 7/8. So the 92/324 row of Koshelev–Koshka's Table 1 has no
    finite theorem behind it.
- **Items of 2026 found and read, none with a bound.** [GLitchfield][gl] (Lean-checked ES(6) = 17 and explicit
  Tóth–Valtr, Suk and HMPT bounds; "none of them improves on the published bound");
  [BrettRey/erdos-problem-107][brettrey] (an ES(6) = 17 SAT pipeline, Lean bridge unfinished);
  [Edou Nze][edou] (a Lean treatise on the classical bound); [Krapivin–Przybocki–Heule][kph];
  [Bhattacharjee–Bhattacharya][bbh] (dimensions 3 and 4 only).
- **Not credible, or not a bound.** [Anderson][anderson] (its "theorem" is only the existence of f(n));
  [Romig][romig] (conditional, restricted class); [Walker][walker] (a blueprint; abstract only).
- **Self-match.** The only public page with an ES(8) figure below 319 is the project's own public repository.
  Search engines still show its README with 314, an older state. It is not prior art.
- **Limits.** Budget out after 29 queries. Unread: erdosproblems.com/107, DBLP, MathOverflow and
  StackExchange, the Semantic Scholar citations of Suk 2017 (HTTP 429), the viXra combinatorics listing (404),
  the SoCG/CCCG/GD 2026 programmes.

### C2 (N(8; 5, 8) ≤ 59 ⇒ ES(8) ≤ 309). Result: no prior art found; "partially anticipated" stands

- No source states this reduction, any other bound on ES(8) from 5-cap-free octagon-free sets, or a stronger
  statement.
- **Not derivable from public statements.** [Javůrek][jav]'s Lemmas 2–3, cups-caps (M₈(6,7) ≤ 126) and
  [Schroeder][sch-pdf]'s C₈ ≤ 193 give only ES(8) ≤ 2 + 193 + 59 + 126 = 380 from the hypothesis. That is
  worse than the unconditional 319. C2 needs the project's own catalogue (the 310 composition).
- **Closest sources.**
  1. Schroeder supplies the mechanism: Theorem 3.2; Lemma 7.5 with Proposition 7.6, which carry Baek's 4-cap
     capacity into the residual catalogue as 23 rows ("Baek's theorem [1, Theorem 1.6] says that 23 points
     force a four-cap or an octagon. Each image therefore has occupied capacity 22, and requires six
     omissions."). Section 9 has conditionals only under full ETV ("ETV would make C7 + D7 + 2 = 58 and place
     C8 + D8 + 2 in [114, 121]") and calls further capacities "open tasks". For heptagons, Theorem 4.3
     ("D7 ≤ B + 5", B = M₇(5,6)) already feeds an a = 5 ETV number into the residual part. C2 is the 5-cap
     analogue of Lemma 7.5 for octagons, which Schroeder does not state.
  2. Javůrek has the same template one size down: "Excluding 28 original points with no heptagon and an
     uncovered hull vertex proves B6 ≤ 27, hence ES(7) ≤ 78"; "The projective test uses 27 points with no five
     cup and no heptagon". For octagons his parameter is M₈(6,8), and he gives no number.
  3. [Mojarrad–Vlachos][mv], the classical ancestor: Lemma 3.3, h(m+1, l+1) ≤ h(m+1, l) + h(m, l+1);
     Theorems 3.4–3.6; Theorem 4.2. The same shape (a residual quantity bounded through smaller cap
     parameters), but for h, not for N(n; a, b).
- [Baek][baek] has no ETV-to-ES upper-bound statement; P(n, 5, n−1) appears only as a node of its Figure 2.
- Method level: the GLitchfield repository has a Lean lemma on cup-rank layers ([file][gl-layer]; "Exact
  ending-cup rank layers reduce the excluded cap size by one", as reported by the C8 attack).
- **Limits.** Budget out after 13 queries; non-English, thesis and MathOverflow searches were not run. Unread:
  erdosproblems.com/107, the JCTA text of Baek–Balko, the EuroCG/CCCG/Eurocomb proceedings, Javůrek's
  companion paper. Of Schroeder's archive only the 12 documentation files were read.

### C3 (N(8; 5, 8) ≤ 65). Result: no prior art found; "partially anticipated" stands, with baseline 78

- No source states N(8; 5, 8) ≤ 65, a smaller bound, or any explicit bound on N(n; 5, n), n ≥ 7, below
  cup-cap.
- **78 from printed statements**, re-derived by the attack in two ways:
  - [Mojarrad–Vlachos][mv] Theorem 3.4, "h(m, 4) ≤ C(m−1,2) + 1", gives h(8, 4) ≤ 22, and the proof of their
    Theorem 4.2 run on an (8,5)-free set gives f(7, 5) + 22 = 56 + 22;
  - the endpoint split ([Javůrek][jav]'s Lemma 3) with [Baek][baek]'s N(8; 4, 8) = 22 and cup-cap
    N(8; 5, 7) ≤ 56.
  Neither derivation is written anywhere for a = 5. Going below 78 from the literature would need a bound on
  the first-layer number N(8; 5, 7) below 56. None exists: [Balko–Valtr][bv15]'s Proposition 3.2 saves one
  point, for a = 4 only.
- **Open status.** In print: Balko–Valtr ("The best known upper bound for N(a, u, k) is
  N(a, u, k) ≤ C(a+u−4, a−2), which is obtained from the trivial estimate") and [Baek–Balko][bb]. Three public
  projects of 2026 list a = 5, b = n as open: the [GLitchfield status table][gl-status] and [experiment
  0112][gl-0112]; [gotrevor][gt-plan] ("the next open rungs are P(7,5,7) [27] and P(7,6,6) [31]"); Javůrek
  ("The full exclusion at 28 points remains open in our experiments").
- **Restricted classes only.**
  - Baek–Balko's Theorem 8 gives 42 for decomposable sets. Its proof is omitted in the SoCG version.
    [GLitchfield's notes][gl-general] assert a gap in the published proof; that is their claim and was not
    verified.
  - GLitchfield's Lean lemmas on five-cap-free sets all carry extra hypotheses (decomposable, or a gap with
    four-cap-free sides).
  - [Schroeder][sch-pdf]'s D₈ ≤ 124 covers five-cap-free octagon-free sets but is weaker than cup-cap. His
    paper and archive documentation contain no five-cap capacity; the literature note of 15 Sept 2026 in the
    [archive][sch-rec] says "Any extension to our five-cap-free class needs an additional argument; it does
    not follow by changing a parameter in Baek's theorem."
- [Baek's 2018 KAIST abstract][baek-kaist]: Suk's argument "can be directly adapted to prove an improved bound
  of ETV(a, n, n)". It gives no statement or number.
- **ETV numbers with a ≥ 5 below cup-cap that do exist.** a = n: [Chung–Graham][cg98]. a = n−1:
  Mojarrad–Vlachos Theorem 4.2, [Vlachos][vla], [Norin–Yuditsky][ny]. Schroeder (unrefereed): M₇(5,6) = 25,
  M₇(6,6) ≤ 49, M₈(7,7) ≤ 193. [gotrevor][gt]: P(7,5,6) at 26 by SAT (answer-only). None for 5 ≤ a ≤ n−2 with
  b = n ≥ 7.
- **Further places checked, all negative.** Programmes of EuroCG 2025 and 2026, SoCG 2026, CCCG 2025, Eurocomb
  2025, GD 2025 and 2026; two theses (Charles University 2026, ELTE 2025); home pages; queries in Russian,
  Chinese, Hungarian, Japanese and Czech.
- **Limits.** Not read: Erdős–Tuza–Valtr 1996 (in this attack), Balko–Valtr EJC 2017, the JCTA version of
  Baek–Balko, erdosproblems.com/107. No forward-citation sweep through third-party indexes. The number 78 is
  a derivation, not a published statement, so a referee may quote 84.

### C4 (N(7; 5, 7) ≤ 41). Result: prior art found, in the must-cite sense

- C4 is not stated verbatim anywhere reached, and nothing stronger is proved. But the inequality that
  produces it is printed as a numbered lemma, in the paper that isolates this number.
- **Strongest candidate.** [Javůrek][jav], Lemma 3: "For a, b ≥ 3, Mk(a, b) ≤ Mk(a − 1, b) + Mk(a, b − 1).
  Proof. In an eligible set let Y consist of the right endpoints of (a − 1) caps. Its complement has no
  (a − 1) cap. We show that Y has no (b − 1) cup." Lemma 2 identifies B₆ − 1 = M₇(5,7). C4 is Lemma 3 at
  (7; 5, 7) plus two cited values: 16 ([Baek][baek], Theorem 1.6, refereed) and 25 ([Schroeder][sch-pdf],
  Theorem 5.2, unrefereed; independently by SAT in [gotrevor][gt]).
- **What is not in print** is the evaluation. Javůrek never bounds B₆ from above and writes "We do not use
  the claimed certificates of [5] as assumptions." In his notation C4 reads B₆ ≤ 42, which gives nothing for
  ES(7) through his Theorem 5 (3·42 − 3 = 123).
- **A trap with the number 41.** Schroeder's table lists the D₇ baseline as 41 (Proposition 7.4:
  D_n ≤ C(2n−6, n−4) − C(2n−8, n−5)), improved to 30 by Theorem 4.3. D₇ carries the no-junction condition, so
  D₇ ≤ 41 does not give M₇(5,7) ≤ 41. C4 extends the same number to the full class.
- **Schroeder's archive uses half of the split.** `literature/BACKGROUND_MACHINERY_2026_09_15.md` in the
  [archive][sch-rec]: "Its four-cap theorem gives M₇(4,7)≤16" and "a residual30 candidate must have at least
  14 four-cap starts and 14 four-cap ends". The other half is his Lemma 5.3 ("both parts have size at most
  25"). The two are never added.
- **Nothing stronger exists.** The 27-point exclusion is open in three public efforts:
  [gotrevor][gt-plan] ("P(7,5,7)@27 ... 16/36 sampled subcubes timed out at 90 s, 0 SAT → ≥ 811 CPU h"; not
  run); Javůrek (a 28-point pilot with three timeouts and one unchecked sub-case); [GLitchfield experiment
  0112][gl-0112] ("whether 27 points force a 5-cap, a 7-cup, or a convex heptagon is undecided at a
  three-hour CaDiCaL budget").
- **Settled small ETV cases (answer to the question).**
  1. n ≥ a+b−3: by cups-caps ([Baek][baek]: "immediate consequences of this theorem").
  2. All triples with n ≤ 6. This is an inference, not a sentence in a paper: ES(6) = 17
     ([Szekeres–Peters 2006][sp06]; Marić 2019 in Isabelle/HOL; Scheucher 2020 by SAT; the Lean corollary
     `gon_6_theorem` in [Subercaseaux et al. 2024][itp24]) plus Baek's Theorem 1.5 ("the statement P(n, a, b)
     implies P(n, a', b')"). Direct SAT confirmations on x-sorted signotopes: [GLitchfield 0112][gl-0112]
     ((6, 5, 6) is exactly 16) and the gotrevor controls ([LOCALITY.md][gt-local]). [Balko–Valtr][bv15]
     verified the stronger abstract statement "for k = 6 and for all possible values of a and u, except for
     the case a = u = k".
  3. a = 4 or b = 4, all n: Baek, with a [Lean 4 formalization][baek-lean]. Earlier, by SAT on pseudolinear
     colourings (Balko–Valtr 2015): N(4, 7, 7) = 16 and N(4, 8, 8) = 22.
  4. (7; 5, 6) and (7; 6, 5) = 25: Schroeder (19 Sept 2026; Lean with native evaluation; unrefereed) and,
     independently, gotrevor (6 Oct 2026; SAT; no proof log).
  5. Open at n = 7: (5, 7), (6, 6), (6, 7), (7, 7) and mirrors. The abstract analogues fail at n = 7
     (Balko–Valtr: N^(4,7,7) = 17, N^(5,6,7) ≥ 26, N^(5,7,7) ≥ 27, N^(6,6,7) ≥ 31; [Baek–Balko][bb]:
     C_weak(7) > 33), so a proof must use geometric or signotope axioms.
- **Limits.** Budget out after about 20 queries; theses, MathOverflow, OEIS, non-English sources and
  conference abstracts were not searched. Unread: erdosproblems.com/107, the full texts of Balko–Valtr 2017
  and Erdős–Tuza–Valtr 1996, the DBLP listings. M₇(5,6) = 25 rests on two independent but unrefereed
  computations.

### C5 (decomposition). Result: prior art found, for both halves

- **Special case a = n: stated, and refuted at n = 6.**
  - [Experiment 0096][gl-0096] (dated 2026-08-10, committed 11 Aug 2026): "Can every realizable coloring with
    no strong `k`-polygon be partitioned into two vertex classes that both avoid a strong `(k-1)`-polygon?
    Such a partition would give the exact doubling recurrence without first constructing a decomposition
    tree." In Lean ([file][gl-bicol]): the hypothesis `StrongPredecessorBicoloringAt`, with a proved step to
    the bound 2^(k−2).
  - [Fixture][gl-split6] (committed 2026-10-10T23:47:56Z): "SPLIT(6) counterexample: 16 integer points in
    general position with no convex hexagon and no bipartition into two pentagon-free sets". [Facts
    file][gl-facts]: "SPLIT(6) is FALSE for real point sets"; the split exists up to 15 points (their SAT
    claim).
  - Re-verified exactly by the attack, and again for this record (§8, E1).
  - Wording. The "special case" of C5 is the a = n instance of the strong form (ETVTHY20261113 §3). The a = n
    instance of the weak form reads "(n−1)-cap-free ∪ (n−1)-gon-free" and is weaker. The 16-point set does
    not refute it (E2).
- **A weaker public statement.** [Predecessor-half conjecture][gl-half] (4 Sept 2026): "every set of n points
  in general position with no k points in convex position contains ⌈n/2⌉ points with no k−1 points in convex
  position". "Levels 4, 5 and 6 are proved; level 7 and above are open." It has the same doubling consequence,
  and C5 at a = n implies it.
- **General cap form: a stronger statement is public.** This corrects the synthesis, which had reported the
  general form as found nowhere.
  - [PASCAL-SPLIT][gl-pascal] (notes dated 2–4 Oct 2026, committed 2026-10-06T14:08:38Z): "X = A + E where:
    - A has no a-cap, no (u-1)-cup and no (k-1)-gon; - E has no (a-1)-cap, no u-cup and no (k-1)-gon." It is
    also called PSL ([survey note][gl-survey]: "never failed, even on general signotopes").
  - With u = k = n: E has no (a−1)-cap and no (n−1)-gon, and A has no (n−1)-gon. Every such split is a C5
    split, so PSL implies C5. Read against ETVTHY20261113 §3, PSL at u = k = n is the project's strong form;
    the condition "A has no (u−1)-cup" is then implied.
  - Status in the source: unproved; aimed at decomposable sets, where it would give Baek–Balko's Theorem 8 by
    induction. Reported there: exhaustive for decomposable colourings to n ≤ 9 and for all signotopes to
    n ≤ 8; no failure in 190k checks at k = 6 and 6k at k = 7. The notes add that "a Pascal split for general
    sets would imply the Erdős–Szekeres conjecture".
  - A stronger "peel" variant is reported false there, at 14 and 11 points in (5,5,6) ([note][gl-uniform]).
  - The repository's 16-point set refutes PSL on the diagonal (a = u = k = 6) for real point sets. It does
    not touch a < n, because every 16-point hexagon-free set contains a 5-cap.
- **a = 4.** [gotrevor, L1(4, b)][gt-p756]: read for point sets, a 4-cap-free, b-gon-free set is A ⊔ B with A
  (b−1)-gon-free and B a cup of at most b − 2 points ("a 'transversal cup'. Baek's Δ has the same shape, but
  he avoids claiming that `S − Δ` is gon-free"). It implies C5 at (a, n) = (4, b). Their report: exhaustive
  for arbitrary 2-colourings at b = 5 and 6, sampled at b = 7 and 8, no hand proof. "L1(5,6) is false" for
  abstract 2-colourings; that does not refute C5 at (5, 7), which asks less of both parts.
- **Not found:** the weak cap form with a < n, verbatim. The refereed literature has nothing closer.
  - Splits that lower cap or cup lengths but not the polygon size: [Schroeder][sch-pdf] Theorem 3.2
    (S = H ⊔ R) and Theorem 4.3; [Mojarrad–Vlachos][mv] Lemmas 2.4–2.5; [Baek][baek]'s Δ-removal for a = 4.
  - Partitions into convex sets go the other way: Ramsey-remainder, Károlyi, Pór–Valtr ([Bárány–Károlyi
    survey][bk01], Section 3; [Tóth–Valtr survey][tv05]).
  - [Baek–Balko][bb] "decomposable" means "A is deep below B", a different notion; no partition conjecture is
    among its open problems.
  - [Devillers–Hurtado–Károlyi–Seara][dhks], Theorem 2.1, n_M(m, k) = k (f(m) − 1) + 1, is the trivial
    coloured variant.
  - MathOverflow [396018][mo396018] and [429884][mo429884], Math.StackExchange [5074510][mse5074510]:
    inductive ideas of the opposite direction only.
- **Own exact checks** (§8). The weak form holds on the public set and on its 5-cap-free subsets (E2, E3).
  The strong form fails at (5, 6) on a derived 15-point set (E4).
- **Limits.** Budget out after about 23 queries; conference abstract lists, OEIS, further non-English queries
  and author home pages were not searched. Dates are commit dates. Not read: erdosproblems.com/107, the JCTA
  version of Baek–Balko, the journal text of Balko–Valtr 2017. The n = 7 and n = 8 instances of the two-set
  split are undecided.

### C6 (two-layer lemma). Result: no prior art found

- **Reading of the claim.** ρ = inner radius / outer radius < 1, and δ is the offset normalised to (0, π/m).
  The threshold is where an outer vertex lies on the line of an inner side.
- **Nearest sources** (all opened by the attack).
  1. [Dehnhardt–Harborth–Lángi][dhl], Lemma 1: "Let P and Q be polygons with Q ⊂ int P ⊂ E2. Let X ⊂ V(P) be
     a set of points beyond exactly the same edge of Q. Then V(Q) ∪ X is a set of points in convex position".
     An outer vertex is beyond exactly one inner edge iff ρ > cos(π/m + δ)/cos(π/m); that computation is the
     attack's, not the paper's. So the "if" direction is a one-line corollary. The paper has no regular
     polygons, no threshold and no converse. Its journal details were not verified.
  2. [Hang Lung 2010][hl10], pp. 278–280: "a point Q can join with a convex n-gon P1P2...Pn to form a convex
     (n + 1)-gon iff Q ∈ U(P1P2...Pn)", next to the three concentric regular pentagons. It covers only "whole
     inner polygon plus one outer vertex", and it has no numeric threshold.
  3. [Mathar][mathar], eq. (12): "cos[ji φn − (jo + 1/2)φm] / cos(φm/2)"; eq. (26) with a rotation term. The
     same closed form for n = m, in a circumscription problem. The paper has no convex-position statement.
  4. [Ábrego–Fernández-Merchant][afm]: the same layered objects, with lemmas on k-edges, halving lines and
     crossings. Related work, not an anticipation.
  5. [Mackey's thesis][mackey]: only the remark "when convex layers of size 5 are enforced, the addition of
     even a single point can complete a convex 6-gon". [Subercaseaux–Mackey–Qian–Heule][smqh]: no geometric
     criterion; "concentric", "regular" and "polar" do not occur.
- **Why the result is "no".** The non-trivial content of C6 is the converse (below the threshold no split of
  a outer and b inner points with a + b = m + 1 is convex, for every m ≥ 4) together with the explicit
  threshold. No source states or implies it.
- **Limits.** The lemma is elementary, so a folklore or olympiad-style source cannot be excluded. The budget
  ran out after about 50 queries, and several planned queries never ran. math.stackexchange.com is blocked
  for page fetches. Two Kvant problem pages returned 404. Bonnice 1974 and Dehnhardt's 1981 Diplomarbeit were
  not accessed. Older elementary-geometry literature was not searched.

### C7 (symmetric sets). Result: prior art found in the must-cite sense only; "partially anticipated" stands

- No source contains C7, a stronger statement, or any of its numbers (60, 64, 61, 52, 56 for octagons; 120
  for 9-gons).
- **Strongest candidate (unchanged).** [Subercaseaux–Mackey–Qian–Heule][smqh] (arXiv v1, the only arXiv
  version; CICM 2025): the same method and the same type of statement at k = 6 and 7.
  - 16 points, no 6-gon: "The formula enforcing a 3-fold symmetry is unsatisfiable, while the formulas with a
    4-fold and 5-fold symmetry are satisfiable." Nine and 46 non-isomorphic realizable configurations.
  - 32 points, no 7-gon: "only 7-gon-free s-fold rotational symmetries could exist with s ∈ {1, 2, 4}";
    "there does not exist a realizable 4-fold symmetry on 32 points without a 7-gon"; 2-fold left open.
  - Section 7: "we suspect that there are symmetric constructions for all k ≥ 7".
  - It has no "8-gon" or "octagon", no 6- or 7-fold case, and no maximum size under a prescribed symmetry
    below 2^(k−2). Its [code repository][smqh-code] holds only 16-point hexagon files.
- [Mackey's thesis][mackey] (65 pages, read): hexagons on 16 points with 3-, 4- and 5-fold symmetry; for
  7-gons, 4-fold "realizations with no more than 24 points (corresponding to six layers of size four)". No
  octagons.
- **Added by the attack.**
  1. [Warrier 2024][warrier]: "there can be an arrangment of 64 points in which there are no convex octagons.
     To validate this ... We will create an arrangment that makes up a regular heptagon and then add 3 points
     along each vertex using trial and error"; the result is a 36-point, roughly 7-fold set. So the sentence
     of the synthesis that nothing exists on rotationally symmetric octagon-free sets needs this exception.
     The paper is unsound (§8, E7) and does not anticipate 64, 60 or any exactness statement.
  2. [Hang Lung 2010][hl10]: an exactly 5-fold 16-point set of type (5,5,5,1), with proof. It is the k = 6
     instance of the template that a 7-fold 64-point set follows (64 = 1 + 9·7). Their attempt at 32 points
     for k = 7, by pasting two copies, failed.
  3. [OEIS A006788][oeis-a006788], the comment of 2002 (§4.1): vague and unproven.
  4. The [Math.StackExchange post of 2021][mse21]: a 2023 comment reports a convex hexagon in the asker's
     16-point "polar grid" set. It is not a valid symmetric example; the synthesis had listed it as one.
- **Other 2025–2026 work read, none with symmetric octagon-free sets.** [Krapivin–Przybocki–Heule][kph];
  [Koshelev–Koshka][kk]; [Dumitru][dum]; [Baek–Balko][bb]; [AlphaEvolve][ae], section 38. The
  [GLitchfield][gl] repository lists the known 64-point octagon-free sets as "Erdős–Szekeres, Valtr blow-ups,
  Baek–Balko Theorem 19"; none is symmetric.
- **Limits.** The Springer chapter is paywalled. The 4-fold non-existence at 32 points rests on six inner
  12-point configurations reported as non-realizable, with no proof in v1; the 5-fold count appears there as
  948 and as 932. Not run (budget): German, Korean, French, Spanish, Hungarian and Czech queries; the CCCG
  2026, GD 2026 and EuroComb 2025 programme checks; phrase queries on concentric regular heptagons.

### C8 (additive split; N(8; 6, 6) ≤ 64). Result: no prior art found; "partially anticipated" stands

- **Part 1, the split.**
  - [Schroeder][sch-pdf] has the device and the objects, but not the statement. Lemma 5.3, proof: "The set S∪
    contains no five-cap: joining the end of such a cap to an actual outgoing five-cup extends one of them to
    a six-chain. Its complement contains no five-cup. By theorem 5.2 and reflection, both parts have size at
    most 25". That is the same endpoint split into two ETV classes, for the balanced heptagon part. Section
    9: "For residual upper bounds we use Dn ≤ Mn(n − 2, n)" and "M8(6, 6) ≥ 50. A set counted by M8(6, 6)
    has no six-cup, hence no residual junction, so D8 ≥ 50." Proposition 7.3: residual universe
    210 − 56 = 154; the attack notes 154 = 84 + 70, the cup-cap evaluation of the C8 split.
  - The attack's assessment: D₈ ≤ M₈(5,8) + M₈(6,6) is a one-line corollary of his definition of D_n, but it
    is not written there.
  - Additive bounds of other kinds: [Mojarrad–Vlachos][mv] Lemma 3.3 (convexifying-point classes);
    [Vlachos][vla] Theorem 4 (balanced plus residual, with cup-cap counts); [Norin–Yuditsky][ny] (a split by
    word classes).
- **Part 2, N(8; 6, 6) ≤ 64** (ETV value 50, cup-cap 70). Nothing below 70 was found for general point sets.
  [Balko–Valtr][bv15]: cup-cap is the best known bound; their [slides][bv-slides] give [31, 70] for (6, 6, 7)
  in the abstract setting. [Baek–Balko][bb]: Theorem 8 makes 50 exact for (6, 6, 8) on decomposable sets
  only; Theorems 4 and 6 give the forcing number 51 for split 8-gons.
- **Answers to the questions.**
  - First-layer cases with a ≥ 5: only (7; 5, 6) = 25 (Schroeder; [gotrevor][gt] by SAT). gotrevor has no
    n = 8 content.
  - The formula "cup-cap minus C(a+b−6, a−3)": explicit only in [gotrevor's note][gt-p756] (Lean lemma
    `d1N_add_holes`, "proved for all a, b ≥ 4"; an identity for the conjectured value, not a proof that the
    value holds). Implicit in Baek–Balko's Lemma 9. The same expression for other objects: Mojarrad–Vlachos
    Theorem 3.6, "h(m, l) ≤ C(m+l−4, l−2) − C(m+l−6, l−3)", and Schroeder's Proposition 7.4.
  - Mojarrad–Vlachos Theorem 3.6 gives no bound on a first-layer N(n; a, b): by Definition 3.1 a
    convexifying point is defined through an arbitrary disjoint set B and arbitrary n, and yields no convex
    polygon inside S. This is "no implication follows from the definitions", not a proof that none exists.
  - Proof strategies: those of gotrevor's note, mostly closed (the Pascal split L1, false at (5, 6) for
    2-colourings; a three-part split L2(5,6), unrefuted; hole injection through Baek's α-statistic, "Step 3
    fails at a = 5"), and [Baek][baek]'s Conjecture 5 for a = 4. No other was found.
  - Balko–Valtr's colourings (N^(5,6,7) ≥ 26, N^(6,6,7) ≥ 31) show that the abstract analogue fails on the
    first layer.
- **Added by the attack.** [Baek's 2018 KAIST abstract][baek-kaist] (first layer with a = 4 only; the
  ETV(a, n, n) remark is asymptotic and unpublished). GLitchfield's cap-parameter-5 workstream ([experiment
  0112][gl-0112]; "two-side" bounds proved only in the decomposable class, [audited note][gl-audit]). A
  machine-written [report on problem 107][epaday] (28 Jul 2026), which re-verifies (7; 4, 7) = 16 at the
  signotope tier.
- **Limits.** Unread: the full texts of Erdős–Tuza–Valtr 1996, Balko–Valtr 2017 and the JCTA version of
  Baek–Balko; Balko's thesis; erdosproblems.com/107. Both repositories are unrefereed.

### C9 (methods). Result: prior art found; the synthesis list was incomplete in all three families

1. **State catalogs and omission counting.**
   - [Chvátal–Komlós 1971][ck71] (read in full): "For each v ∈ V(D) consider the set P_v ... Let X_v denote
     the 'maximal' points of P_v ... Because there are only C(p+q, p) such thin subsets ... the assignment
     v → X_v cannot be a coloring." This is the down-set state map of Moshkovitz–Shapira and of Schroeder's
     Lemma 5.1.
   - Seidenberg (1959) is named as the root by [Norin–Yuditsky][ny], the [Moshkovitz–Shapira][ms] abstract
     and [Mulrenin–Pohoata–Zakharov][mpz]. It was not read (paywalled).
   - [Norin's MathOverflow answer][norin-mo] of 13 March 2012 is the public origin of the two-letter-word
     encoding, three months before the Moshkovitz–Shapira arXiv posting.
   - None of these has capacity or omission inequalities for convex-polygon avoidance, finite certificates,
     or n = 7, 8. Those appear only in [Schroeder][sch-pdf].
2. **SAT on triple orientations and signotopes.**
   - Earlier than Balko–Valtr: [Schewe 2008][schewe], "transforming the problem of finding suitable oriented
     matroids into a satisfiability problem".
   - [Balko–Valtr's data page][bv-data]: a generator for arbitrary (a, u, k, N), and colourings showing that
     the abstract analogue of ETV fails at 17 (a = 4, k = 7), 26 (5, 6; 7), 27 (5; 7), 31 (6, 6; 7),
     32 (6; 7), 33 (k = 7), 23 (a = 4, k = 8) and 30 (a = 4, k = 9) vertices.
   - [jcpaik/erdos-szekeres-sat][baek-sat]: a second public encoder for ETV instances.
   - Also: [Subercaseaux–Mackey–Heule–Martins][smhm] (CICM 2024); [Marshall][marshall] (signotope SAT with
     cake_lpr, for geometric thickness).
3. **Formal verification.**
   - Bounds valid for every n ≥ 3, hence for n = 7, 8: GLitchfield [`tothValtr_upper`][gl-tv] (Lean;
     C(2n−5, n−2) + 2, i.e. 128 and 464); linrock [`f_le_erdosSzekeresUpper`][linrock] (Lean; 253 and 925);
     meesu [`EZ_bound_final`][meesu] (Isabelle/HOL; 253 and 925). All three are self-reported; none was built.
   - So "no Lean-checked upper bound for ES(n), n ≥ 7, other than Schroeder's" is too strong. The supported
     form: no proof-assistant-checked bound better than Schroeder's 81 and 319 was found.
   - Further items: [Edou Nze][edou] (Lean 4; g(4) = 5 and a cup-cap identity); [Bhattacharjee–
     Bhattacharya][bbh] (Lean 4 kernel check of higher-dimensional lower-bound certificates);
     [Florath][florath] (LRAT checked inside Lean); the [mathlib Archive][mathlib-es] (the monotone-subsequence
     theorem by Seidenberg's pigeonhole proof); Baek's formalization is archived in [Lean Pool][leanpool].
   - Caveat: [GLitchfield's bibliography][gl-bib] reports that Marić's public Isabelle archive stops at five
     points. Not verified.
- **Limits.** Budget out after 26 queries; the Japanese and Chinese queries and the EuroCG and ITP/CPP/CICM
  2026 queries were not run. Unread: Seidenberg 1959, Romig's PDF, Marić's repository page, the CCCG 2025
  proceedings. Scanned with no further result: the Eurocomb 2025 abstracts, the CCCG 2026 accepted list, the
  EuroCG 2025 and 2026 accepted lists, DROPS, the AFP combinatorics and geometry topics.

## 7. What must be cited if this is written up

1. **Bounds (C1).**
   - [Schroeder v1][sch-doi] (81, 319; unrefereed): the direct comparator and the source of the method.
   - [Mojarrad–Vlachos][mv] (113, 408): the refereed bound. [Tóth–Valtr 2005][tv05] (127, 463).
   - [Koshelev–Koshka][kk], Table 1, with the remark that its 92/324 row has no located derivation.
   - [Javůrek][jav]: a concurrent conditional route that establishes no number.
2. **ETV numbers (C2, C3, C4, C8).**
   - Erdős–Tuza–Valtr ([1993 report][etv93]; [journal][etv96]) for the conjecture.
   - [Baek][baek]: a = 4 (Theorem 1.6), the monotone implication (Theorem 1.5), the cup-rank rows, Conjecture
     5; its [Lean formalization][baek-lean].
   - [Balko–Valtr 2015][bv15] (and the 2017 journal version): cup-cap as the best known general bound, the
     "first nontrivial case", the pseudolinear SAT values, the failure of the abstract analogues.
   - [Mojarrad–Vlachos][mv]: Theorem 4.2 (a = n−1), Theorem 4.3 after Tóth–Valtr, and Theorem 3.6 as the same
     expression for a different quantity.
   - [Schroeder][sch-pdf]: Theorem 3.2, Theorem 4.3, Theorem 5.2, Lemma 5.3, Lemma 7.5, Section 9,
     D_n ≤ M_n(n−2, n).
   - [Javůrek][jav]: Lemmas 2 and 3, Theorem 5, and the open 27-point exclusion.
   - [Baek–Balko][bb]: Lemma 9 (the down-set count) and Theorem 8 (decomposable sets).
   - [gotrevor/es7-ladder][gt]: the independent SAT confirmation of (7; 5, 6) and the explicit hole formula.
     The formula is to be cited, not claimed.
   - [Krapivin–Przybocki–Heule][kph]: the realized 26-point set for (7; 5, 7).
   - State the C3 comparison as 65 against 78 (derivable from the literature), 84 (cup-cap) and 42 (ETV
     value). Present C4 as a corollary.
3. **Decomposition (C5), if a split or doubling statement is mentioned at all.**
   - [GLitchfield][gl]: [experiment 0096][gl-0096], the [predecessor-half note][gl-half], the [SPLIT(6)
     fixture][gl-split6] and the [PASCAL-SPLIT notes][gl-pascal].
   - [gotrevor][gt-p756]: the first-diagonal Pascal split L1.
   - The cups-caps endpoint split and Baek's Δ-removal as classical ancestors.
   - State the cap form only in its weak version, as a conjecture of this project. Do not state the a = n
     split as a conjecture for all n.
4. **Two-layer lemma (C6).** [Dehnhardt–Harborth–Lángi][dhl], Lemma 1, for the easy direction;
   [Mathar][mathar], eq. (12), for the ratio; [Hang Lung 2010][hl10] for the concentric-pentagon example;
   [Ábrego–Fernández-Merchant][afm] and [Subercaseaux–Mackey–Qian–Heule][smqh] as related work on layered
   symmetric sets.
5. **Symmetric sets (C7).** [Subercaseaux–Mackey–Qian–Heule][smqh] (arXiv and the CICM 2025 version) as the
   comparison point; [Mackey's thesis][mackey]; [Krapivin–Przybocki–Heule][kph]; [Baek–Balko][bb] and
   [AlphaEvolve][ae] for unsymmetric 64-point sets; [Hang Lung 2010][hl10] as an early 5-fold example;
   optionally [Warrier 2024][warrier], as an unsound earlier attempt.
6. **Methods (C9).** Seidenberg 1959 and [Chvátal–Komlós][ck71]; [Moshkovitz–Shapira][ms];
   [Fox–Pach–Sudakov–Suk][fpss]; [Norin–Yuditsky][ny]; [Mojarrad–Vlachos][mv]; [Baek][baek];
   [Baek–Balko][bb]; [Schroeder][sch-doi]; [Szekeres–Peters][sp06]; [Balko–Valtr][bv15]; [Marić][maric];
   Scheucher ([2020][sch18], [2021][sch21]); [Heule–Scheucher][hs]; Subercaseaux et al. ([2024][itp24],
   [2025][smqh]); [Szeider][szeider] for the certificate-to-Lean step; [GLitchfield][gl-tv],
   [linrock][linrock] and [meesu][meesu] for proof-assistant-checked bounds valid for all n.

## 8. Exact checks made during the check (not literature)

These are computations by the search agents on public data, plus one re-run for this record. They are not
literature. The re-run used a separate pure-Python script with exact integers, on one thread, in under 30 s
in total; its scripts were kept only in the session scratchpad. Method: convex position by the
no-point-in-a-triangle test on all 5- and 6-subsets; caps and cups by the signs of consecutive triples in
x-order; all subsets enumerated. **Re-run these with the project's checker before any record relies on them.**

The public 16-point set ([fixture][gl-split6]), as quoted by the `sites` searcher:

    (0, 1955462), (100, 131926), (217072, 178235), (307547, 135238), (417839, 222390), (456150, 156464),
    (458421, 159647), (460439, 156196), (650282, 138663), (650399, 406161), (748098, 173456),
    (748347, 173421), (810326, 177127), (852854, 116288), (1285030, 101269), (1918751, 0)

- **E1. The fixture is as described.** Distinct x, no collinear triple, 292 convex pentagons, 0 convex
  hexagons, 47 five-caps and 72 five-cups in the given direction (longest cap 5, longest cup 5), largest
  pentagon-free subset 8, and 0 of the 32,768 bipartitions (65,536 ordered) with both sides pentagon-free.
  Agreeing runs: `sites`, the synthesis, the C5 attack, and the re-run for this record. The values 292 and 0
  are also the expected values stored in the fixture.
- **E2. The weak cap form at (a, n) = (6, 6) holds on this set.** Partitions (A, B) with A 5-cap-free and B
  pentagon-free: 5,175 in the given direction (C5 attack; re-run). Over all 240 combinatorially distinct
  directions the number lies between 2,529 and 12,099 (synthesis: "at least 2,529"; re-run).
- **E3. The weak form at (5, 6) holds on its 5-cap-free subsets.** Of the 136 subsets with 14 or 15 points, 40
  are 5-cap-free in some direction (2 with 15 points, 38 with 14). That is 877 (subset, direction) pairs, the
  number the synthesis reports, or 433 distinct x-orders. Each has a partition into a 4-cap-free part and a
  pentagon-free part (at least 273 partitions; re-run).
- **E4. The strong form fails at (a, n) = (5, 6).** Delete the point (0, 1955462) and reflect y → −y. The 15
  remaining points have no 5-cap and no convex hexagon (72 four-caps, 47 five-cups, 220 convex pentagons).
  There are exactly 60 partitions into two pentagon-free sets (120 ordered), all of sizes 7 + 8, and in none
  of them is either part 4-cap-free. There are 316 partitions (A, B) with A 4-cap-free and B pentagon-free,
  so the weak form holds on this set. The synthesis reports three independent implementations in agreement;
  the re-run for this record is a fourth. 15 is the ETV value for (6; 5, 6), so the failure is at the extremal
  size, as in E1.
- **E5. The FBDL(6) fixture** ([file][gl-fbdl]; `sites`, not re-run): 367 convex pentagons, 0 hexagons; this
  set does split into two pentagon-free sets, in 132 ways.
- **E6. Reading of C6.** With ρ = inner/outer radius and δ ∈ (0, π/m), brute force on random instances with
  m = 4..8 agrees with the criterion every time: 191 instances (synthesis), 288 (`symmetric-geometry`), 1,437
  (C6 attack). For m = 3 it fails (92 of 399 trials in the attack), consistent with the hypothesis m ≥ 4.
  This checks the reading of the claim only.
- **E7. Warrier's printed coordinates** ([paper][warrier]; C7 attack, exact integers, two methods).
  - The 36-point set contains 9 points in convex position: (358,119), (562,179), (566,260), (574,584),
    (573,608), (365,642), (192,515), (217,435), (349,135). It also has a collinear triple: (256,260),
    (562,179), (596,170).
  - The 30-point, roughly 6-fold "heptagon-free" set contains a convex heptagon: (396,143), (602,149),
    (586,246), (209,563), (199,568), (140,597), (219,262).
  - The 16-point, roughly 5-fold set is hexagon-free (largest convex subset 5).
  - Re-run for this record on the coordinates quoted above only: the nine points and the seven points are in
    convex position, and the triple is collinear. The paper itself was not re-opened.
- **E8. Arithmetic.** ETV values (8; 5, 8) = 42, (7; 5, 7) = 26, (7; 5, 6) = 25, (8; 6, 6) = 50,
  (8; 5, 7) = 41, with cup-cap bounds 84, 56, 35, 70, 56. Mojarrad–Vlachos gives 113 and 408. The first-layer
  identity "ETV value = cup-cap minus C(a+b−6, a−3)" was checked numerically for 4 ≤ a, b ≤ 13 (`classics`),
  and the count of Baek–Balko's Lemma 9 by brute force for a, u ≤ 7 (`classics`).

## 9. Disagreements and how they were settled

Between searchers (settled by the synthesis):
- **C5.** `sites` reported the public 16-point counterexample. `symmetric-geometry` saw the same repository,
  but only its August and September files, and reported the split as an open hypothesis. The other four found
  nothing. Settled by opening the fixture and re-verifying it.
- **C5, wording.** `classics` noted that a = n in the general statement gives a part with no (n−1)-cap, not a
  part with no convex (n−1)-gon. ETVTHY20261113 §3 settles it: there is a weak and a strong form, and the
  "special case" is the strong form.
- **C2, C3, C4, C7.** The labels differed; the facts did not. C3 and C4 were decided by the baseline that
  follows from printed statements (78 and 41).
- **C8, the formula.** `symmetric-geometry` had seen no general first-layer formula. `sites` quoted it from
  [gotrevor][gt-p756]; three others found the same expression in [Mojarrad–Vlachos][mv] Theorem 3.6 or
  implicit in [Baek–Balko][bb]'s Lemma 9. Both primary sources were opened.
- **C8, Mojarrad–Vlachos Theorem 3.6.** `arxiv-recent` asked whether a convexifying point gives a convex
  polygon inside the set, which would give N(8; 6, 6) ≤ 50. By Definition 3.1 it does not (§6, C8).
- **Krapivin–Przybocki–Heule.** `semantic` wrote that PointSAT "also finds 32 points with no 7-gon". The
  [paper][kph] says the opposite (quoted in §4.2). Only the 26-point and 29-point problems were solved.
- **n ≤ 6.** Several searchers wrote that all ETV cases with n ≤ 6 are settled. It is kept as an inference
  (§6, C4).
- **Zenodo identifiers.** Searchers cite different DOIs for the same deposits (Romig 21972394 and 22998974;
  Edou Nze 22132974 and 22132975; Bhattacharjee–Bhattacharya 23483598 and 23485633). A Zenodo listing shows
  22998974, 22132975 and 23485633 as the current records. None contains a planar bound.

Between the synthesis and the attacks (the attack prevails):
- **C4.** "Partially anticipated" became "prior art found": the endpoint split is a printed lemma of Javůrek,
  not only folklore.
- **C5.** "The general cap form was found nowhere" became "a stronger statement (PASCAL-SPLIT) is public".
- **C7.** "Nothing was found on rotationally symmetric sets with no convex octagon" needs the exception of
  Warrier's unsound attempt, and the Math.StackExchange example of 2021 is not valid.
- **C9.** "No Lean-checked upper bound for ES(n), n ≥ 7, other than Schroeder's" was reworded (§6, C9).

## 10. Consequences for the project's records and wording

Nothing was changed. These points follow from §3–§9.

- **ETVTHY20261113 §3 and §3.5; DELTA2N20261113 §4.1.**
  - §3.5 lists the a = n split as open, with 90 hexagon-free sets of 15–16 points that all split. The public
    16-point set does not split (E1). The statement is false at n = 6.
  - §3.2 reports the strong form at (5, 6) as holding on 90 random sets, and DELTA2N §4.1 lists (5, 6) strong
    and (6, 6) strong as "open from m = 12". Both are settled negatively by real point sets: (6, 6) at 16
    points (E1) and (5, 6) at 15 points (E4).
  - So the strong chain M(5; n) ≤ M(4; n−1) + M(5; n−1) "by decomposition" breaks at n = 6, although the
    value 15 it would give there is true. Only the weak form can stand as a conjecture; DELTA2N certifies it
    at n = 6.
  - ETVTHY §3 says "We did not search the literature for this formulation." That search is now done: the
    strong form is PASCAL-SPLIT at u = k = n ([note][gl-pascal]); the weak form with a < n was not found.
- **FLAYER20261113 §8.2.** The split PS(a, b) there is the statement L1(a, b) of [gotrevor][gt-p756] and the
  first-diagonal case of PASCAL-SPLIT. Cite both. This check was not asked about PS(5, 5). Whether FLAYER's
  14-point sets without a split bear on PASCAL-SPLIT as tested in that repository was not examined.
- **C3.** Compare 65 with 78, 84 and 42 (§7).
- **C4.** A corollary, not a result. Do not confuse it with Schroeder's D₇ baseline 41.
- **C6.** Claim the converse and the closed-form threshold, not the whole equivalence.
- **C7.** "No printed instance at k = 8 was found" is supported. "Nothing exists" is not.
- **C8.** The first-layer formula is public; cite it.
- **C9.** Use the supported form of §6. NOVELTY20261106, "Do not claim", already has the ES(8) ≤ 464 point.
- **C1.** A comparison table must address the 92/324 row. Search engines show the project's public README with
  ES(8) ≤ 314, an older state.
- **Outside the nine claims.** ETV7SAT20261113 (items 3 and 4 of its status block, as read for this record)
  states colouring versions of (7; 5, 6) and (7; 5, 7) with weak heptagons. [Balko–Valtr's data page][bv-data]
  lists colourings of 26 vertices (no red 5-path, no blue 6-path, no 7-gon) and of 27 vertices (no red 5-path,
  no 7-gon) in their model; [Baek][baek]'s Theorem 2.7 and [Baek–Balko][bb]'s Theorem 7 are weak-polygon
  statements for a = 4 and for the diagonal. This check did not compare the definitions. That comparison is
  needed before those statements are written up.

## Link definitions

All URLs below come from the search inputs.

[sch-doi]: https://doi.org/10.5281/zenodo.22842891
[sch-pdf]: https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf
[sch-comp]: https://michaelschroeder.ai/research/ErdosSzekeres/companion
[sch-ver]: https://zenodo.org/api/records/22842891/versions
[sch-rec]: https://zenodo.org/records/22842891
[sch-site]: https://michaelschroeder.ai/sitemap
[mv]: https://arxiv.org/abs/1510.06255
[ny]: https://arxiv.org/abs/1509.03332
[vla]: https://arxiv.org/abs/1505.07549
[kk]: https://arxiv.org/abs/2604.20120
[jav]: https://doi.org/10.6084/m9.figshare.34875984
[dum]: https://arxiv.org/abs/2512.24061
[zeng]: https://doi.org/10.2139/ssrn.7334758
[ep107]: https://www.erdosproblems.com/107
[baek]: https://arxiv.org/abs/2206.04260
[baek-lean]: https://github.com/jcpaik/erdos-tuza-valtr
[baek-sat]: https://github.com/jcpaik/erdos-szekeres-sat
[baek-kaist]: https://mathsci.kaist.ac.kr/~sangil/seminar/2018-09-10/
[tv05]: https://library.slmath.org/books/Book52/files/30toth.pdf
[bv15]: https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf
[bv-data]: https://kam.mff.cuni.cz/~balko/ES_SAT
[bv-slides]: https://kam.mff.cuni.cz/~balko/prezentace/A_SAT_attack_on_the_Erdos-Szekeres-conjecture.pdf
[bv17]: https://doi.org/10.1016/j.ejc.2017.06.010
[bb]: https://doi.org/10.4230/LIPIcs.SoCG.2025.13
[bb-jcta]: https://doi.org/10.1016/j.jcta.2026.106195
[etv93]: http://web.archive.org/web/20170706013611/ftp://ftp.inf.fu-berlin.de/pub/reports/tr-b-93-01.ps.gz
[etv96]: https://doi.org/10.1006/eujc.1996.0045
[cg98]: https://www.lix.polytechnique.fr/Labo/Ilan.Vardi/chung_graham.pdf
[gl]: https://github.com/GLitchfield/erdos-szekeres-convex-poly
[gl-split6]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/harness/research/examples/split6-counterexample-v1.json
[gl-facts]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/harness/research/examples/convexity-axioms7-v1.json
[gl-fbdl]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/harness/research/examples/fbdl6-counterexample-v1.json
[gl-0096]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/experiments/0096-strong-predecessor-property-b.md
[gl-half]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/plans/predecessor-half-conjecture.md
[gl-plan]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/plans/research-plan-2026-09-03.md
[gl-bicol]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/ErdosSzekeres/StrongPredecessorBicoloring.lean
[gl-pascal]: https://github.com/GLitchfield/erdos-szekeres-convex-poly/blob/main/docs/research/archive-2026-09-28-to-10-05/claude-pascal-20261002/HANDOFF.md
[gl-survey]: https://github.com/GLitchfield/erdos-szekeres-convex-poly/blob/main/docs/research/archive-2026-09-28-to-10-05/claude-survey-20261004/PROBLEM.md
[gl-uniform]: https://github.com/GLitchfield/erdos-szekeres-convex-poly/blob/main/docs/research/archive-2026-09-28-to-10-05/claude-uniform-20261003/NOTES.md
[gl-general]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/research/archive-2026-09-28-to-10-05/claude-general-picture/GENERAL-PICTURE.md
[gl-audit]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/research/archive-2026-09-28-to-10-05/claude-audit-6k2k-20261002/AUDITED-PROOF-6k2k.md
[gl-0112]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/experiments/0112-etv-parameter5-signotope.md
[gl-cap5]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/ESBlueprint/C/EtvCapFiveAll.lean
[gl-status]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/harness/status.md
[gl-layer]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/ESBlueprint/B/NotContainsCapSetEndingCupRankLayerOfNoCapSucc.lean
[gl-tv]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/ErdosSzekeres/TothValtrUpper.lean
[gl-bib]: https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/bibliography.md
[gt]: https://github.com/gotrevor/es7-ladder
[gt-plan]: https://raw.githubusercontent.com/gotrevor/es7-ladder/master/docs/PLAN.md
[gt-p756]: https://raw.githubusercontent.com/gotrevor/es7-ladder/master/docs/HUMAN-P756.md
[gt-local]: https://raw.githubusercontent.com/gotrevor/es7-ladder/master/docs/LOCALITY.md
[kph]: https://arxiv.org/abs/2607.02958
[itp24]: https://arxiv.org/abs/2403.17370
[sp06]: https://doi.org/10.1017/S144618110000300X
[bk01]: https://www.renyi.hu/~barany/cikkek/85.pdf
[dhks]: https://web.mat.upc.edu/carlos.seara/data/publications/articles/chromESFinal.pdf
[dhl]: https://www.math.u-szeged.hu/~zlangi/publications/ErdosSzekeres.pdf
[mathar]: https://arxiv.org/abs/1301.6293
[hl10]: https://hlma.hanglung.com/assets/3EE1F601-28F3-4DD9-ABDE-6D75F6E2D4CF/013.pdf
[afm]: https://cgt-journal.org/index.php/cgt/article/download/75/79/800
[warrier]: https://indianmathsoc.org/pdf/Mathstudent-V93-part3-4-2024.pdf
[oeis-a006788]: https://oeis.org/A006788
[mse21]: https://math.stackexchange.com/questions/3983965/visualizing-lower-bound-for-the-happy-ending-problem-small-cases
[smqh]: https://arxiv.org/abs/2506.00224
[smqh-springer]: https://link.springer.com/chapter/10.1007/978-3-032-07021-0_3
[smqh-code]: https://github.com/bsubercaseaux/automatic-symmetries
[mackey]: http://reports-archive.adm.cs.cmu.edu/anon/2025/CMU-CS-25-108.pdf
[ae]: https://arxiv.org/abs/2511.02864
[fm]: https://arxiv.org/abs/2609.25050
[mo277192]: https://mathoverflow.net/questions/277192/a-new-polygon-forcing-theorem
[mo396018]: https://mathoverflow.net/questions/396018/happy-ending-problem-why-not-a-proof-by-induction
[mo429884]: https://mathoverflow.net/questions/429884/happy-ending-problem-why-not-a-proof-by-induction-cont
[mse5074510]: https://math.stackexchange.com/questions/5074510/how-many-convex-and-disjoint-n-1-gons-guarantee-a-convex-n-gon
[norin-mo]: https://mathoverflow.net/a/91128
[ck71]: https://doi.org/10.4153/CMB-1971-028-8
[mpz]: https://arxiv.org/abs/2411.19823
[ms]: https://arxiv.org/abs/1206.4001
[fpss]: https://arxiv.org/abs/1105.2097
[maric]: https://doi.org/10.1007/s10817-017-9423-7
[sch18]: https://arxiv.org/abs/1807.10848
[sch21]: https://arxiv.org/abs/2105.08406
[hs]: https://arxiv.org/abs/2403.00737
[schewe]: https://arxiv.org/abs/0801.2582
[smhm]: https://arxiv.org/abs/2311.03645
[marshall]: https://zenodo.org/records/23842786
[szeider]: https://arxiv.org/abs/2607.00815
[tat]: https://arxiv.org/abs/2610.36648
[leanpool]: https://arxiv.org/abs/2609.25199
[florath]: https://arxiv.org/abs/2606.16688
[mathlib-es]: https://github.com/leanprover-community/mathlib4/blob/master/Archive/Wiedijk100Theorems/AscendingDescendingSequences.lean
[linrock]: https://github.com/linrock/math-proofs/blob/cd3cf0b176e95209584bf35555a7c0e501255f6e/erdos-107/Solution.lean
[meesu]: https://github.com/meesu/isabelle-convex-polygon
[fc107]: https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/107.lean
[edou]: https://doi.org/10.5281/zenodo.22132975
[bbh]: https://doi.org/10.5281/zenodo.23485633
[romig]: https://doi.org/10.5281/zenodo.22998974
[anderson]: https://doi.org/10.5281/zenodo.17490793
[walker]: https://doi.org/10.17605/osf.io/bvdqw
[brettrey]: https://github.com/BrettRey/erdos-problem-107
[wiki]: https://en.wikipedia.org/wiki/Happy_ending_problem
[mathworld]: https://mathworld.wolfram.com/HappyEndProblem.html
[teorth]: https://raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml
[epaday]: https://erdosproblemaday.com/report/107
[karolyi01]: <https://doi.org/10.1016/S0166-218X(00)00234-1>
[kt12]: https://doi.org/10.1007/s00454-012-9424-6
[suk25]: https://api.zbmath.org/v1/document/8144033
