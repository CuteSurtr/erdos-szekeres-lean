## Search methods for a heptagon-free 33-point set: literature review (19 Oct 2026)

### Bottom line
- **What has a record on problems like this.** On exact point-geometry feasibility problems, two kinds of method have documented wins. The first is SAT/CP restricted by a symmetry or a template. The second is coordinate local search with an exact incremental checker. Learning-guided search wins mostly on smooth optimization scores (grids, Heilbronn, kissing numbers, Ramsey graphs). On exact point-feasibility benchmarks it falls behind ILP and symmetric SAT.
- **AlphaEvolve already tried this exact problem.** Georgiev, Gómez-Serrano, Tao and Wagner (2025) used it to minimize the number of convex k-gons among 2^(k−2)+1 points, for k ≤ 8.
  - The paper reports sets with exactly one convex k-gon and says the lower bound was not improved (problem 6.58 of [arXiv 2511.02864](https://arxiv.org/abs/2511.02864), read via the [alphaxiv text](https://www.alphaxiv.org/abs/2511.02864.md)).
  - The public notebook disagrees. In [google-deepmind/alphaevolve_repository_of_problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems), `experiments/erdos_szekeres_happy_ending_problem`, last commit 22 Jun 2026, a code comment says the 33- and 65-point sets have **zero** k-gons. That comment is wrong.
- **What I checked.** I recounted both sets in exact rational arithmetic (each double is converted to an exact rational and scaled to integers).
  - The 33-point set has exactly 1 convex 7-gon (0-based indices 23, 32, 25, 14, 15, 17, 20 of `points_7`) and 32,055 convex 6-gons, with no collinear triple. The 65-point set has exactly 1 convex 8-gon (indices 29, 15, 57, 27, 0, 30, 1, 23).
  - Cross-checks: a separate point-in-triangle test confirms the 7-gon. A port of the notebook's own float scorer also counts it. A regular 9-gon control gives C(9,7) = 36.
  - Removing any one of the 7 heptagon vertices gives 7 heptagon-free 32-point sets, unrelated to the sets our own searches produced. All 7 are saturated under `.cache/es7/trackA/bin/sat`: 109,337 faces each, all covered, 0 extension faces, about 0.5 s each.

### Methods

Machine: 15 cores and 48 GB. Load average is about 13, so the running ES(7) jobs already use most cores.

**1. Cube-and-conquer SAT with symmetry breaking and proof logs**
- **What it found:**
  - h(6) = 30 ([Heule–Scheucher 2024](https://arxiv.org/abs/2403.00737)): 312,418 cubes, about 17,300 CPU h.
  - The 24-point "6-hole or 7-gon" lemma: 231 CPU h with the best cube length.
  - Lean verification ([Subercaseaux et al., ITP 2024](https://arxiv.org/abs/2403.17370)): verified encoding, cake_lpr check of about 25,900 CPU h, LRAT on the order of 180 TB, and the UNSAT result imported as an axiom.
  - All of this is from our survey `docs/RELATED_WORK_2026-10-14.md`.
- **How it applies:** this is our run33. It is the route to a proof (UNSAT would also give the Goodman–Pollack conjecture at k = 7). It finds a counterexample only through a SAT model that is then realized.
- **Transferable improvements:**
  - Cubes on consecutive-triple orientations, with the cube length tuned and the (+,−,+) patterns split further.
  - Injected sub-results, such as ES(6) = 17 on windows.
  - The layer-classification route (Section 6.4 of Heule–Scheucher).
- **Expected scale on the laptop:** h(6) alone would take about 48 days on 15 cores, or about 72 days with proof logging, and the proof would have to be checked as a stream. No credible estimate exists for 33 points, because the open frontier is not shrinking.
- **Biggest risk:** the heavy-tailed cubes. Also, any SAT model is very likely unrealizable (see 4).

**2. SAT/CP restricted by a symmetry**
- **What it found:**
  - No-three-in-line: [Prellberg 2026](https://arxiv.org/abs/2602.07751) used CP-SAT with 90° rotation and found 2n points for every n ≤ 60 (the previous frontier was 46). Symmetry gave about 4× fewer variables. n = 50 took about 1 h on a 384-thread EPYC, against about n = 20 in the same time without symmetry. n = 61 and 62 failed within 10^7 s.
  - Heule later reached n ≤ 76 (except 75) with SAT in the rot4 and rct4 symmetry classes, June–August 2026 ([MathWorld](https://mathworld.wolfram.com/No-Three-in-a-LineProblem.html)).
  - [Subercaseaux–Mackey–Qian–Heule](https://arxiv.org/abs/2506.00224): 4-fold symmetric heptagon-free 32-point sets took about 1 CPU-year and gave 310M abstract configurations. The inner 12 points were never realized, and that verdict is heuristic.
- **How it applies (my own analysis, not found in the literature):**
  - **Rotations.** 2-fold rotation is impossible for 33 points in general position: an odd count puts the centre in the set, and the centre is collinear with every pair p, −p. 11-fold is excluded, so 3-fold (run33m3) is the only rotation.
  - **Mirror symmetry is allowed:** 1 point on the axis plus 16 mirror pairs. In an x-sorted signotope with a vertical axis it is just the equivalences o(i,j,k) ⇔ o(34−k, 34−j, 34−i). I checked the sign rule on a 5-point example. This roughly halves the free variables. It is incompatible with the current `hm` normalization, so it needs plain x-sorting.
  - **Why mirror sets are plausible.** In the Morris–Soltan form of the classical construction, block T_i and block T_(n−2−i) are mirror images with cups and caps swapped. So mirror-symmetric extremal 32-point sets probably exist; the 32-point SAT control would test this.
  - **A built-in structural constraint.** A 4-point chain in one half that is concave as seen from the axis, together with its mirror image, gives 8 points in convex position. So each half must avoid such chains. Since f(6,4) = 16, each half must then contain a 6-chain of the other kind. This can be added as extra clauses.
  - **D3** (three mirror axes): the only option for 33 points is 5 orbits of 6 plus 1 orbit of 3 on the axes. It is a sub-case of 3-fold with about 1/6 of the variables, so it is quick to decide.
  - **Partial symmetry:** make only the outer layers symmetric and leave the inner core free. This is motivated by Subercaseaux et al., where the outer points of the 4-fold models were often realizable but the inner 12 never were.
- **Expected scale on the laptop:** the 2-fold 32-point instance was SAT in 51 s here. A mirror instance of similar size should give answers in minutes to hours (a guess). Run controls first: k = 5 should give 8 SAT and 9 UNSAT; k = 6 should give 17 UNSAT.
- **Biggest risk:** counterexamples may exist only without symmetry, and symmetric abstract models are rarely realizable.

**3. Templates and block constructions with SAT over fewer variables**
- **What it found:**
  - Weak Schur number WS(6): unstructured Monte Carlo search (NMC/NRPA) reached ≥ 582, later 583 ([Eliahou et al. 2013](https://link.springer.com/10.1007/978-3-642-37198-1_17)). Template constructions reached 642 (Rowley) and 646 ([arXiv 2112.03175](https://arxiv.org/abs/2112.03175)).
  - [Rowley](https://arxiv.org/abs/2203.13476) improved many multicolour Ramsey lower bounds using SAT-found "template graphs".
  - An integer-programming paper on circulant graphs for Ramsey bounds ([arXiv 2608.18769](https://arxiv.org/abs/2608.18769)) was seen by title and abstract only.
  - In the Erdős–Szekeres setting itself (from the survey): Baek–Balko's genetic search over blow-ups never beat 2^(k−2), up to k = 20. Their Theorem 8 rules out decomposable sets. Bogdan's layer-anchored templates gave UNSAT on 13 layer profiles, with single sub-cubes running up to 2.3×10^6 s.
- **How it applies:** a template must leave the decomposable class. Options:
  - a fixed convex-layer profile, using our O(n⁴) encoding;
  - the symmetric-outer / free-core template from 2;
  - a block skeleton: fix the order type inside each block (taken from realizable extremal 32-point sets) and leave only the between-block triples free;
  - Baek–Balko's Theorem 19 family.
- **Expected scale on the laptop:** minutes to days per template.
- **Biggest risk:** a template excludes counterexamples by design, and realizability is still needed for every model.

**4. Realizability testing and SAT modulo realizability**
- **What it found:**
  - [PointSAT (Krapivin–Przybocki–Heule 2026)](https://arxiv.org/abs/2607.02958) settled the 23-point problem with no 6-hole and no 7-gon. This took 1,727 + 2,326 core hours on 128 cores and realized 1,035 of 174,450 abstract solutions.
  - On 32 points with no 7-gon, it realized **0 of 200,000** abstract solutions in 2,191 core hours. The authors say the method does not scale much past 30 points.
  - Localizer (simulated annealing with an exact rational re-check) realizes order types of about 30 points in seconds but cannot prove that one is unrealizable.
  - Biquadratic final polynomials (an LP certificate of non-realizability) are complete for the classes classified up to 11 elements. Richter-Gebert's 14-element example has none.
  - Linear subreduction ([Koshelev–Koshka 2026](https://arxiv.org/abs/2604.20120)) fixes the x-coordinates so that orientations become linear in y. It realized 8.5% of 10-point signotopes with evenly spaced x and 37.7% with an exponential grid.
  - An SDP approach to non-realizability certificates exists ([Pacific J. Optim. 5(2)](http://www.ybook.co.jp/online-p/PJO/vol5/pjov5n2p211.pdf); authors not confirmed).
  - Items without links here are from our survey.
- **Key point:** at 32 points, searching abstract models first and realizing afterwards found nothing, while our coordinate searches produced thousands of realizable sets. So when the goal is finding a set, realizability should be built into the search, not checked at the end.
- **How it applies:**
  - Use Localizer instead of our realizers. Ours fail even on symmetric 32-point controls that are known to be realizable.
  - Use the final-polynomial LP to certify the 45 two-fold 32-point models as non-realizable, turning "not realized" into a proof.
  - **Fixed-x exact neighbourhood search (my proposal).** Fix all x-coordinates from a realizable set with one heptagon, free the y-coordinates of r points, and pose the no-7-gon clauses as an SMT (linear real arithmetic) or MILP problem. Every model is then a real point set.
    - With r = 1 this is the existing face enumeration.
    - r ≥ 2 reaches neighbourhoods the growth search cannot.
    - Alternate which coordinate is fixed (x, then y).
- **Expected scale on the laptop:** Localizer takes seconds to minutes per model. The LP certificate would involve about 1.2M Grassmann–Plücker relations (my estimate), so minutes to hours per model. The fixed-x search's scale is unknown; prototype it at 16/17 points first.
- **Biggest risk:** fixed-x slices may contain no counterexample, and big-M constraints in a MILP cause numeric trouble.

**5. Local search over coordinates**
- **What it found:**
  - Overmars ([UU-CS-2001-07](https://ics-archive.science.uu.nl/research/techreps/repo/CS-2001/2001-07.pdf), DCG 2003), empty-hexagon-free sets: random sets gave at most 18 points and growing in a region gave 22. Random backtracking with "Brownian" point moves reached 29 after about 4 days on a 500 MHz PC, never 30 in months — and 29 is the true maximum.
  - [Fabila-Monroy–López](https://ar5iv.labs.arxiv.org/html/1403.1288) (JGAA 2014), rectilinear crossing number: exact counting of convex quadrilaterals, random point moves with exponential steps, accepted if the count does not get worse, step halved when stuck. It improved best-known sets for most n from 46 to 99.
  - AlphaEvolve on this problem got exactly 1 heptagon at 33 points (above). Our own annealing gave 8,537 order types.
- **How it applies:** minimize the number of convex 7-gons on 33 points, breaking ties with a finer score (convex 6-gons, or orientation margins). Use multi-scale moves and moves that jump a point into another arrangement face. Seed from the AlphaEvolve 33-point set.
- **Expected scale on the laptop:** an exact 7-gon count for 33 points measured about 4 ms including process start-up, which is at least 10^7 evaluations per hour on 15 cores.
- **Biggest risk:** getting stuck at one 7-gon, and no certificate when it fails. Saturation itself is expected (Damásdi et al.), so it tells us little.

**6. Learning-guided search**
- **What it found:**
  - [Wagner 2021](https://arxiv.org/abs/2104.14516): a cross-entropy reinforcement-learning method refuted several graph conjectures.
  - [PatternBoost](https://arxiv.org/html/2411.00566):
    - It found a counterexample to Graham's hypercube conjecture (81 edges against 82 at d = 6).
    - It found 110 grid points with no isosceles triangle on 64×64 (previous 108, after a 3-month search) and 160 on 100×100 (previous 154).
    - It failed on some problems, including a pattern-avoiding permanent and box double covers.
  - [FunSearch](https://en.wikipedia.org/wiki/FunSearch) found a cap set of size 512 in dimension 8. An [open reimplementation](https://arxiv.org/abs/2503.11061) was tested on the no-isosceles problem.
  - [AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) matched about 75% and improved about 20% of 50+ problems, including kissing number 593 in dimension 11.
  - Tao et al. 2025: no-isosceles 112 on 64×64 and 164 on 100×100; Heilbronn improvements. [Tao's blog](https://terrytao.wordpress.com/2025/11/05/mathematical-exploration-and-discovery-at-scale/) warns that it is very good at exploiting loopholes in the verifier, for example by piling points almost on top of each other.
  - [Ramsey](https://arxiv.org/abs/2603.09172): five lower bounds raised by 1, e.g. R(3,13) ≥ 61.
  - [AlphaZero plus tabu search](https://www.ijcai.org/proceedings/2024/772) improved several extremal-graph bounds.
  - On no-three-in-line, learning methods lose to exact ones: ILP is optimal up to 19×19, PatternBoost only up to 14×14, and PPO only 10×10 ([arXiv 2512.11469](https://arxiv.org/abs/2512.11469)). Symmetric SAT reaches 60 and 76.
  - Apart from AlphaEvolve's problem 58, I found no application of these methods to convex position.
- **How it applies:** train PatternBoost on our 168k 32-point sets plus 33-point sets with one heptagon, with method 5 as the local search.
- **Expected scale on the laptop:** small transformers train on CPU in hours. LLM-evolution needs an API budget.
- **Biggest risk:** the objective is flat and the goal is a needle event. The model imitates its training data, which is all saturated sets. DeepMind already ran the LLM-evolution version of this experiment.

**7. Order-type databases** (from the survey)
- **What exists:** realizable order types up to 10 points online, and 11 points (about 96 GB) on request. 8,690,164 of the 11-point abstract types are non-realizable. Rote's NumPSLA tool ships an exclude list of about 8.7M non-realizable types for n ≤ 11 (185 MB).
- **How it applies:** exact non-realizability screening of 33-point abstract models through their 10- and 11-point subsets (92.6M and 193.5M per model), or lazily added "unrealizability" clauses, which PointSAT does not learn.
- **Expected scale on the laptop:** CPU-hours per model (estimate).
- **Biggest risk:** non-realizability at this size is usually global (PointSAT's best attempts violate about 122 orientations on average), so small-subset filters may catch little. The databases are no source of seed sets at 33 points.

### Ranking for finding a 33-point counterexample
1. Mirror, D3 and partial-symmetry SAT, followed by Localizer and the final-polynomial LP.
2. Fixed-x exact neighbourhood search seeded from 33-point sets with one heptagon.
3. Coordinate local search as a cheap long shot.
4. Keep run33 and run33m3 going; they are the proof direction.
5. PatternBoost or LLM evolution only as add-ons.
6. Not recommended: abstract-first SAT modulo realizability at 33 points (0 of 200,000 realized at 32).

A certified "no mirror-symmetric (or no 3-fold) heptagon-free 33-point signotope" would be a publishable result. Saturation counts are weak evidence.

### Points usable in the email
- AlphaEvolve's own run on this problem reached exactly one convex 7-gon at 33 points; the paper's text says so.
- The public notebook comment claiming zero 7-gons is wrong.
- Every 32-point heptagon-free set obtained from AlphaEvolve's set is saturated.

### Not confirmed
- The SDP paper's authors.
- The Ramsey numbers, which come from search summaries and the abstract only.
- The ICML 2026 gradient-flow result (from a listing page; the paper was not read).
- The circulant-IP paper (title and abstract only).
- Mackey's CMU thesis and the PNAS version of the AlphaEvolve paper (could not be reached).
- All laptop timings marked as estimates.
- Whether the mirror and D3 encodings are satisfiable at k = 6 or 7 (not run).

### Files
No repository file was changed; about 4 s of CPU was used. Everything is in `scratchpad/`:
- `ae/pts.json` — the AlphaEvolve point sets
- `ae/es.ipynb` — the notebook
- `chk/countk.c` — exact k-gon counter (compile with `-isysroot …/MacOSX26.5.sdk`; the default SDK fails to link)
- `chk/maxconvex.py`
- `chk/verify7.py`
- `chk/ae32_minus*.txt` — the seven derived 32-point sets