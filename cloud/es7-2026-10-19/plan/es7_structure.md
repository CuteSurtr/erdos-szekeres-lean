## Structure of a possible counterexample to ES(7) = 33: literature report, 19 Oct 2026

**How this was done.** I read `docs/RELATED_WORK_2026-10-14.md` and `experiments/es7-search-2026-10-13/README.md`, then checked the primary sources online. These were read as full text: Balko–Valtr (ENDM 2015), Szekeres–Peters (ANZIAM 2006), Morris–Soltan (BAMS 2000) pp. 437–444, and Aichholzer–Hackl–Vogtenhuber 2011. These were read in HTML through a fetch tool: Baek–Balko (SoCG 2025), Subercaseaux et al. 2025, Krapivin–Przybocki–Heule 2026, Dumitru 2025, Damásdi et al., HMPT, Suk, and Koshelev–Koshka.

Items marked **[own]** are my own computations or derivations, not literature. They took under 15 s of CPU in total, and the scripts are in `scratchpad/decomp/` (`check.py`, `sets.py`, `affine.py`, `n5.py`, `n5b.py`, `mirror.py`, `dpval.py`, `starts.py`, `starts2.py`). No repository file was modified and no process was touched; I only read `.cache/es7/grow/starts_K7_a.txt`.

---

### (1) Conditions any counterexample X must satisfy (X = 33 points in general position, no convex 7-gon)

**C1. X is not decomposable.**
- Definition: a set is decomposable if it is a single point, or it splits into decomposable A and B with A "deep below" B. "Deep below" means three things: A is lower in y; every point of B is above every line through two points of A; every point of A is below every line through two points of B.
- Theorem 8 of Baek–Balko: a decomposable set with more than S(a,u,k) = Σ_{i=k−a+2}^{u} C(k−2,i−2) points contains an a-cap, a u-cup or a convex k-gon. With a = u = k this gives the conjecture for decomposable sets.
- The classical construction P(a,u,k) is decomposable: it consists of decomposable clusters Q_i, each deep below the next.
- Source: [SoCG 2025 HTML](https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.13/LIPIcs.SoCG.2025.13.html).
- Caveat: the SoCG version omits the proof of Theorem 8. The journal version ([JCTA 2026](https://www.sciencedirect.com/science/article/pii/S0097316526000385)) returned 403, so I could not see the proof. Unconfirmed.

**C2. X contains split 7-gons but no genuine 7-gon.**
- A split k-gon is an a-cap and a u-cup that share their rightmost point, with a + u = k + 2.
- Baek–Balko Theorem 3: every set of 2^{k−2}+1 points contains a split k-gon, and this threshold is tight.
- So X contains split 7-gons (in every rotated frame). The obstruction is only that the two chains never also share their leftmost endpoint.
- Some 2^{k−2}-point sets even contain split (2k−4)-gons, so split polygons alone cannot decide the question.

**C3. Local cup/cap conditions.**
- From Baek's (7,4,7) case (any 17 points with no 4-cap contain a convex 7-gon; [arXiv 2206.04260](https://arxiv.org/abs/2206.04260)): every 17-point subset of X contains a 4-cap and, by reflection, a 4-cup, in every generic direction.
- From Schroeder's claim that 26 points force a 5-cap, a 6-cup or a 7-gon ([Zenodo 22842891](https://zenodo.org/records/22842891), unreviewed): every 26-point subset would contain a 5-cap or a 6-cup, and a 6-cap or a 5-cup. Unconfirmed.

**C4. Hole conditions.**
- h(6,7) = 24: any 24 points contain a 6-hole or a 7-gon. The upper bound is Heule–Scheucher's; the matching 23-point example is Krapivin–Przybocki–Heule Theorem 1.1 ([arXiv 2607.02958](https://arxiv.org/html/2607.02958)). So every 24-point subset S of X contains a 6-hole of S.
- Their Theorem 5.1: every abstract 23-point order type with no 6-hole and no 7-gon has exactly 3 hull points. So every 23-point subset of X without a 6-hole has a triangular hull. This is a computer proof (cube-and-conquer, 1,727 core-hours).

**C5. Projective normalization (Tóth–Valtr; proof of Theorem 2.4 in [Morris–Soltan](https://kam.mff.cuni.cz/~chvatal/MorSol00.pdf), p. 441–442).**
- For a hull vertex a, a projective map T makes "Z ∪ {a} is in convex position" equivalent to "T(Z) is a cap".
- So T(X∖a) is a 32-point set with no 6-cap and no 7-gon.
- **[own]** Conversely, adding the point at infinity back turns any such 32-point set into a counterexample. So ES(7) = 33 is equivalent to the Erdős–Tuza–Valtr case N(7,6,7) = 31. The project's encoding ("point 1 is extreme, the others sorted around it") already uses this.

**C6. Symmetry [own, elementary].**
- Under a rotation group of order s, the orbits have size s and there is at most one fixed point (the centre).
- If s is even and there is a centre, then p, the centre and −p are collinear, which violates general position.
- If s ≥ 7, an orbit is a regular s-gon and contains a convex 7-gon.
- For 33 points this leaves only **s = 3** (11 orbits, no centre). 2-fold and 4-fold 33-point instances are void, so the 3-fold run is the only rotational target.
- For 32 points the same argument gives s ∈ {2, 4}, matching Subercaseaux et al.
- Mirror symmetry is not excluded: 16 mirror pairs plus one point on the axis.

**C7. Every 32-point subset X∖{p} is an extremal heptagon-free set that is *not saturated*** (it extends by p).
- So a counterexample exists if and only if some heptagon-free 32-point set is unsaturated.
- Damásdi–Dong–Scheucher–Zeng prove the classical Erdős–Szekeres construction is saturated ([arXiv 2312.01223](https://arxiv.org/abs/2312.01223); Eur. J. Combin. 131 (2026) 104236).

**C8. Abstract consequences.**
- X would also be a 33-element signotope without a 7-gon. That refutes the Goodman–Pollack signotope conjecture at k = 7 ([Balko–Valtr](https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf); Baek–Balko).
- Balko–Valtr's 33-vertex colouring without a 7-gon is not pseudolinear. So the 4-point axiom is essential to the question, not decoration.
- HMPT run Suk's argument entirely in pseudo-configurations ([arXiv 1710.11415](https://ar5iv.labs.arxiv.org/html/1710.11415)). The asymptotic theory therefore never uses realizability. They state that no inequality in the chain 2^{n−2}+1 ≤ e(n) ≤ c(n) ≤ c′(n) = b(n) is known to be strict.

**C9. Trivial layer bound.** Every convex layer has at most 6 vertices, so X has at least 6 layers. Bonnice-style analysis of how the layers nest is already infeasible at n = 6: 17 hexagon-free points admit 70 nesting tuples (Morris–Soltan p. 444).

---

### (2) Structure of extremal sets for n = 5 and 6

**n = 5 (8 points, no convex pentagon)**
- Bonnice's Lemma 2.8: sets with layer types (3,3,2), (4,3,1) and (3,4,2) all contain a convex pentagon (Morris–Soltan §2.4, p. 443–444). So 8-point pentagon-free sets have layer type (4,4) or (3,4,1).
- Hirata–Katayama 1998 add a "convex quadrilateral cell decomposition". This comes via the survey, from a partly garbled OCR.
- Minimum number of convex pentagons: 0 for n ≤ 8, 1 at n = 9, 2 at n = 10, 7 at n = 11 ([Aichholzer–Hackl–Vogtenhuber 2011, Table 1](https://publications.ist.tugraz.at/files/publications/geometry/ahv-o5g5h-11.pdf)).
- No published count of pentagon-free 8-point order types was found.
- **[own]** I found 150 pentagon-free 8-point sets by local search.
  - All 98 of layer type (4,4) were decomposable in some direction.
  - Of the 52 of type (3,4,1), 16 were **not decomposable in any direction**. This holds even under a more permissive test that allows a shear at every level.
  - Exact integer witness: (824,663), (633,394), (155,682), (1622,644), (570,−372), (228,584), (296,578), (395,255). Its largest convex subset has 4 points and its layers are (3,4,1).
  - The sample is biased.

**n = 6 (16 points, no convex hexagon)**
- **How many?** Unpublished.
  - Szekeres–Peters count only the 6-point window states. There are 892 non-convex 6-point signatures obeying the 4-point rule. This equals the 908 six-element signotopes ([OEIS A006245](https://oeis.org/A006245)) minus 16 convex ones (our arithmetic). Each state is compatible with at most 18 successors.
  - Their proof split into 446 top-level cases and took about 3,000 GHz-hours ([paper](https://archive.austms.org.au/Publ/ANZIAM/V48P2/2409.html)). It does not count or describe 16-point sets.
  - Neither do Marić, Scheucher 2020/2023, Heule–Scheucher, or Koshelev–Koshka, so far as I could find.
- **Symmetric ones** ([Subercaseaux–Mackey–Qian–Heule, arXiv 2506.00224](https://arxiv.org/html/2506.00224), preprint):
  - 3-fold (with a centre): unsatisfiable.
  - 4-fold: 66 abstract solutions, 18 realizable, 9 up to isomorphism.
  - 5-fold: 948 solutions (also stated as 932), 92 realizable, 46 up to isomorphism.
- **Are they all of stacking type? No [own].**
  - I took the 4-fold set (their Table 1) and the 5-fold set (their Table 2).
  - Both check out as 16 points in general position whose largest convex subset has 5 points.
  - Neither is decomposable in any of the 128 and 360 combinatorially distinct directions, even under the permissive test.
  - My build of the classical construction is decomposable in 410 of 456 direction cells.
  - Layer sequences: 4-fold (4,4,4,4); 5-fold (5,5,5,1); classical (5,5,3,3).
- **Abstract versus realizable.** For n ≤ 6 the abstract and realizable values coincide ([Dobbins–Holmsen–Hubard](https://arxiv.org/abs/1305.2266)). A gap between the two models can first appear at n = 7.
- **What could generalize.**
  - Extremal sets already escape the decomposable/stacked class at n = 5 and n = 6. So Theorem 8 removes only part of the extremal landscape at n = 7.
  - **[own]** Your growth starts are mostly outside that class already. Of 15 sampled sets from `starts_K7_a.txt`, 13 are not decomposable in any direction (strict test); only s0 and s2217 are.
  - **[own] Mirror-symmetric extremal 32-point sets exist.** In the classical construction (Morris–Soltan Thm 2.6), define block T_{5−i} as the reflection y → −y of T_i. This is valid because the reflection swaps caps and cups and maps angle θ_i to −θ_i.
    - I verified the result exactly: 32 points in general position, closed under the reflection, no point on the axis, largest convex subset 6.
    - The check used an O(n⁴) dynamic program, validated against brute force on 40 random sets.
  - Subercaseaux et al. "suspect" that symmetric constructions exist for all k ≥ 7.

---

### (3) What others have already searched for n = 7

1. **Balko–Valtr 2015/2017** (Glucose SAT; [data page](https://kam.mff.cuni.cz/~balko/ES_SAT)).
   - Pure 2-colourings: a 33-vertex colouring with no 7-gon, which refutes the Peters–Szekeres strengthening.
   - Further pure-colouring bounds: N̂(5,6,7) ≥ 26, N̂(5,7,7) ≥ 27, N̂(6,6,7) ≥ 31, N̂(6,7,7) ≥ 32, N̂(4,7,7) = 17.
   - Restricted to pseudolinear colourings, they verified only N(4,7,7) = 16 and N(4,8,8) = 22. All pseudolinear results matched the conjectured values, and none of the counterexamples was pseudolinear.
   - The k = 6, a = u = 6 run did not finish in 266 h.
2. **Baek–Balko 2025.**
   - C_weak(7) > 33 by SAT, for pure colourings.
   - Their computer experiments found no signotope above the conjectured thresholds; parameters, solver and time are not stated.
   - A MATLAB genetic optimizer over blow-ups up to k = 20 never exceeded 2^{k−2}. This is heuristic, not exhaustive.
3. **Subercaseaux et al. 2025.**
   - 4-fold symmetric 32 points: about 1 CPU-year of enumeration, 310,187,713 non-isomorphic abstract models.
   - All of them share only 6 inner-12-point configurations, and none of those was realized. The outer points were often realizable.
   - Their conclusion that no realizable 4-fold 32-point set exists rests on failed realization attempts; no non-realizability certificate is given (my reading).
   - 2-fold symmetry is listed as future work, and 33 points are not mentioned.
4. **Krapivin–Przybocki–Heule 2026.**
   - 200,000 abstract 32-point solutions without a 7-gon; 0 realized in 2,191 core-hours (Localizer, 15 s timeout).
   - Mean 121.6 violated orientations, against 12.2, 38.0 and 21.8 for their 23-, 26- and 29-point problems.
   - On average only 42.4 orientations (0.9%) are flippable. Near-extremal abstract solutions are rigid.
5. **Dumitru 2025** ([arXiv 2512.24061](https://arxiv.org/html/2512.24061)).
   - 33-point SAT with convex-layer-size templates (for example 5⁶ and 4⁸).
   - Unsatisfiable for some anchored subfamilies; 13 runtimes are listed, up to 2.28×10⁶ s.
   - The case split is not shown to be complete, and no proof checking is described.
6. **Schroeder 2026** (Zenodo, unreviewed): ES(7) ≤ 81 and the Erdős–Tuza–Valtr case (7,5,6) = 25.
7. **Szekeres–Peters 2006**: the k = 7 analogue (P*_7) was out of reach. The 2016 Morris–Soltan chapter (Springer) was not retrievable.
8. **Not found anywhere**: mirror-symmetric searches; fixed-x-coordinate (linear) realizable searches for k-gons; ML or PatternBoost-style searches for heptagon-free sets; any published list of 32-point heptagon-free sets beyond the classical one. The [erdosproblems #107 forum](https://www.erdosproblems.com/forum/thread/107) mentions only Balko–Valtr.

---

### (4) Most promising leads and open questions

**L1. Climb the Erdős–Tuza–Valtr ladder at k = 7.** This is the strongest "smarter" route.
- **[own derivation]** In Morris–Soltan's proof of Thm 2.6, the classical blocks T_p…T_q can be replaced by one small, flattened set Y. Y needs no (q+2)-cap, no (7−p)-cup and no 7-gon. This works because an intermediate block contributes at most one point and the end blocks contribute a cap or a cup.
- Hence any realizable set with no a-cap, no b-cup and no 7-gon, of size above N(7,a,b) = Σ_{i=7−b}^{a−2} C(5,i), extends to a 33-point counterexample.
- This agrees with Balko–Valtr's hypergraph remark that their 17-vertex colouring extends to 33 vertices. The 1996 Erdős–Tuza–Valtr paper itself was not retrieved.
- Thresholds:

| Case (7,a,b) | Max conjectured | Status |
|---|---|---|
| (7,4,7) | 16 | proved (Baek) |
| (7,5,6) | 25 | Schroeder, unreviewed |
| (7,5,7) | 26 | open |
| (7,6,6) | 30 | open |
| (7,6,7) | 31 | equivalent to ES(7) |
| (7,7,7) | 32 | equivalent to ES(7) |

- So **27 points with no 5-cap and no 7-gon**, or **31 points with no 6-cap and no 6-cup**, would already disprove the conjecture.
- These SAT instances are far smaller and more constrained than 33 points. They are also in the size range where realizers succeed (see the 26/29-point statistics in item 4 above).
- If the signotope instance at 27 points comes back unsatisfiable, that is a new, publishable Erdős–Tuza–Valtr case: Baek–Balko say only a = 4 or u = 4 is known.
- Balko–Valtr's pure colourings at these exact parameters are ready-made negative controls.
- Caveat: failure at (7,5,7) does not exclude a counterexample. Only (7,6,7) and (7,7,7) are equivalent to ES(7).

**L2. Search only realizable configurations by fixing x-coordinates** ("linear subreduction", [Koshelev–Koshka, arXiv 2604.20120](https://arxiv.org/html/2604.20120)).
- Once the x-coordinates are fixed, every orientation constraint is linear in the y-coordinates. An SMT (linear real arithmetic) or MILP search over all signotopes then returns only real point sets.
- At 10 points, an exponential x-grid realizes 729,588 of 1,937,396 signotopes, against 165,048 for a uniform grid.
- Fixing x can lose some realizations. It pairs naturally with L1 at 26–31 points.

**L3. Mirror-symmetric 33-point SAT [own suggestion; no prior work found].**
- With a vertical axis and x-sorted labels 1..33 (point 17 on the axis), the mirror condition is σ(i,j,k) = σ(34−k, 34−j, 34−i). This roughly halves the triple variables.
- The instance is non-vacuous, since mirror-symmetric extremal 32-point sets exist (§2).
- There are two sub-cases: the axis point is a hull vertex if and only if the hull has an odd number of vertices.

**L4. Rigidity sits in the interior.** Subercaseaux's inner-points observation and the 0.9% flippability suggest fixing a realizable outer structure and searching only the inner points. Do this in the realizable direction (Dumitru's layer templates are abstract only). Keep several realizations per order type (the Aichholzer–Krasser caveat in our survey).

**L5. Exact optimization over blow-ups for k = 7.** Lemma 14 of Baek–Balko is a small integer program. Solving it exhaustively over all small base order types (for example ≤ 10 points from the Aichholzer database) would replace the genetic algorithm. It either rigorously closes the blow-up class at k = 7 or finds a counterexample.

**L6. Count near-misses.** Find the minimum number of convex 7-gons among 33 points. The pentagon analogue: the minimum is 1 at 9 points, 2 at 10, 7 at 11. Local search in coordinate space shows where the obstruction concentrates.

**L7. A census at n = 6.** Enumerate and classify every 16-point hexagon-free signotope: decomposable or not, symmetric or not, layer types, realizable or not. This would be new data on what extremal sets look like, and would show whether non-stacked types dominate.

**L8. Open in the literature.**
- Are all 2^{n−2}-point extremal sets saturated? (Only the classical construction is known to be.)
- Is the Goodman–Pollack conjecture true at k = 7?
- Is any inequality in the HMPT chain strict?
- Do 2-fold symmetric 32-point sets have realizations? (A realization would be a new symmetric extremal set, not a counterexample. By Shor's caveat in our survey, realize without enforcing the symmetry.)

**What this means for the current search.**
- Dead ends at 32 points are expected and carry little information. The classical set is saturated, and for n ≥ 7 there are saturated sets of only (7/8)·2^{n−2} points (28 points at n = 7).
- Excluding decomposable sets is a theorem, but extremal sets are richer than that class.
- For 33 points, only the 3-fold symmetry run is meaningful.
- Abstract-then-realize at 32/33 points has a 0 out of 200,000 record elsewhere (Krapivin–Przybocki–Heule). Moving to realizable-only methods and smaller Erdős–Tuza–Valtr targets is better supported by the literature than running the 33-point cube-and-conquer longer.

**For the email to Prof. Suk** (points only; nothing was drafted or sent):
- Ask about the (7,5,7) and (7,6,6) stepping-stone targets.
- Report that the published 4-fold and 5-fold extremal 16-point sets are not decomposable.
- Mention the mirror-symmetric extremal 32-point set and the mirror-symmetric 33-point idea.
- Ask whether he knows of unpublished pseudolinear runs by Balko–Valtr on the (7,5,7)-type cases.

---

### Not confirmed
- Baek–Balko: the proof of Theorem 8, and the parameters of their signotope experiments.
- Subercaseaux et al.: the 4-fold non-realizability is heuristic, and their counts are internally inconsistent (948 vs 932).
- Schroeder's results are unreviewed.
- The 1996 Erdős–Tuza–Valtr paper was not retrieved; the block-replacement argument in L1 is my derivation.
- Hirata–Katayama is known only through a partly garbled OCR.
- The 2016 Morris–Soltan chapter was not retrievable. I read "Morris–Soifer" in the task as Morris–Soltan; Soifer's book was not consulted.
- Pór–Valtr partitioned theorem ([KAM preprint](https://kam.mff.cuni.cz/kamserie/clanky/2002/s598.pdf)) and Károlyi–Tóth 2012 (forbidden subconfigurations): known only from search summaries. Both are asymptotic and give nothing at n = 7.
- The coordinates of Subercaseaux et al.'s Tables 1–2 were transcribed by a fetch tool. My checks (16 points, general position, no convex hexagon) are consistent with a correct transcription.
- The decomposability tests are my own code. They were validated only on the classical construction.