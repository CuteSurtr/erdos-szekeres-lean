# ROOT(7) at 17 points: is there a REAL counterexample? (track R7, 15 November 2026, from 13:59 KST)

## Status (final, 18:05 KST; all R7 units stopped)

- **ROOT(7) is false for a REAL 17-point set (EXACT; claim `root7-real-17` filed 14:11:05 KST, verifier V1:
  CONFIRMED 14:15, [VERIFY_ROOT7_REAL17.md](VERIFY_ROOT7_REAL17.md)).** The claim's time field says 14:14; the file
  was actually published at 14:11:05.
  - The set is `/home/jay/research/data/roadmap-20261115/pm1115/r7/root7_real17.json` (SHA-256 `d9b5e6c4…ab7d6e`).
    Coordinates are small, |x|, |y| ≤ 8,412:
    `[[-2384,413],[-1837,269],[-751,1129],[-719,-13],[-717,-145],[210,539],[211,-184],[383,-293],[418,-334],[424,4678],
    [1067,2579],[1072,-383],[2049,-519],[2054,-589],[2073,7779],[2357,8412],[2384,-1781]]`.
  - x is strictly increasing and no three points are collinear.
  - It has 0 five-caps and no 7 points in convex position, so it is (5,7)-valid.
  - It has 170 four-caps, and **117 of them contain r**.
  - U = S − r has 290 convex hexagons, 9,808 weak Δs, and **0 rooted weak Δs** (exhaustive over 2^16 subsets).
- **Found at the same time by T1.** T1's own BFP-CEGAR (unit `esr-agx-t1-r7c17`) realized a different model at
  14:09:22; R7's hit came 4 s later. R7's checker confirms T1's set too: 169 four-caps, 111 at r, 314 hexagons in U,
  9,114 weak Δs, 0 rooted. T1 filed it as `root7-real-17-t1` (CONFIRMED 14:14 by another verifier). [corrected 15 Nov
  pm (C1 issues 9 and 14): the verifier was V1, the same as for `root7-real-17`; 14:14 is the verdict file's time
  (14:14:04), while its time field says 14:19]
- V1's verdict adds, on R7's set: ENV#(7) fails for this real set at U = P − r (16 points) and at U = P (17 points);
  CONJ-TS′(7) fails; weak D(5,7) holds (8,435 weak Δs); the mirror forms hold (V1 only, not claimed by R7).
- **T3's abstract model `root7_m17_s1` has no x-sorted real realization (EXACT; claim `root7-m17-nonreal-1` filed 14:08,
  verifier V2: CONFIRMED 14:09, [VERIFY_ROOT7_M17_NONREAL1.md](VERIFY_ROOT7_M17_NONREAL1.md)).** It duplicates T1's claim `root7-m17-t3-nonrealizable` on the same model. The certificate:
  - its 9-point sub-signotope on points 6,7,8,9,10,11,12,14,16, plus the vertical point at infinity V, carries a BFP
    certificate of 27 three-term Grassmann–Plücker inequalities, all multipliers 1;
  - a certificate on all 17 points + V also exists (486 inequalities);
  - no V-free certificate was found.
- **LP0(7) (P2's models): no satisfiable model of P2's scan is realizable (EXACT).** [corrected 15 Nov pm (C1 issue
  20): no model has an x-sorted realization; 20 of the 108 (W among them) have V-free certificates, i.e. no realization
  at all, and the other 88 only certificates with V; the sub-items below say so]
  - W = `w19_real17_oonn` has a V-free BFP certificate (claim `lp0-7-w19-nonreal`, V1 CONFIRMED 17:40).
  - All 21 real-block models: claim `lp0-7-realblock-nonreal`, V2 CONFIRMED 17:48.
  - The other 87 models, via their non-realizable blocks: claim `lp0-7-scan-all-nonreal`, V2 CONFIRMED 17:49.
  - A direct real search over two-point extensions of the five real 17-point ROOT(7) sets found no real LP0(7)
    counterexample. It covered 3.6 million valid 19-point sets, with up to 8 positions per cell of the first new
    point (HEURISTIC).
  - The m = 16 searches were stopped at 17:26 for this task.
- **16 points: open (no real or abstract 16-point counterexample found).** ROOT(7) is CERTIFIED for
  |S| ≤ 14 (ROUND6), so 15 and 16 are the open sizes. Details in the "16 points" section.
  - T3's blind CaDiCaL run on `root7_m16.cnf` timed out after 2,100 s, so the abstract m = 16 question is undecided.
  - No single-point deletion of either real 17-point set is a counterexample (EXACT, all 17 deletions of each). The
    closest is deleting point 4, which leaves 15 rooted Δs in both sets.
  - No abstract m = 16 counterexample lies within Hamming distance 40 (on the 560 triple signs) of the real
    configuration root7_real17 − point 4. This is COMPUTED: pysat CaDiCaL 1.9.5 "UNSAT under a cardinality
    assumption", with no proof.
  - One-point moves found nothing (HEURISTIC). The search covered all 272 bases B = S17 − {p, q} of both real sets
    and 574.6 million positions of a 16th point. 26.9 million of these made B + z (5,7)-valid, and 19.5 million got
    the full ROOT test (r ends a 4-cap). None is a counterexample.
  - The best real 16-point set found so far has **4** rooted Δs (HEURISTIC search; `r7/lns/f4.json`, 16:00). A
    second, independent descent reached the same 4-Δ pattern (`r7/lns/f4b.json`, exact17-confirmed). The
    path was 15 (deletions) → 12, 10 (annealing) → 9 (relaxed 17-point walk) → 6, 5, 4 (large-neighbourhood
    descent). `exact17.py` confirms the 9, the 6 and both 4s:
    - `lns/f4.json`: 131 four-caps, 111 at r, 110 hexagons in U, 13,040 weak Δs, 4 rooted;
    - `lns/f4b.json`: 121, 101, 110, 13,040, 4.
  - A blind CaDiCaL `--sat --seed=2` run on `root7_m16.cnf` gave no verdict in about 18 CPU-minutes.
  - No abstract m = 16 counterexample lies within Hamming distance 48 of the 9-Δ set, nor within 48 of the 4-Δ set
    (COMPUTED).
  - Both m = 16 units (Hamming ball around the 4-Δ set at radius 56; pipeline run 2 at f = 9) were stopped
    unfinished at 17:26 for the LP0 task.

## Statement

ROOT(7): if S is (5,7)-valid (no 5-cap, no convex 7-gon) and its rightmost point r ends a 4-cap, then U = S − r has a
weak Δ A (4-cap-free, meets every convex hexagon of U) with A ∪ {r} 4-cap-free (ROOT6_MAIN.md "Statement", n = 7).
T3 found the m = 17 ROOT(7) CNF satisfiable (claim `root7-m17-abstract`, V1 CONFIRMED 14:01), so ROOT(7) fails for an
abstract signotope on 17 points. Question of this track: does it fail for a real set of 17 (then 16) points?
**Answer for 17: yes** (CONFIRMED by V1).

## Method

- **Base CNF:** T3's `cnf/root7_m17.cnf` (round-6 encoder `root_cnf.py 7 17`; SHA-256 `44626ab2…`; 13,448 variables,
  251,616 clauses; variables 1..680 = lexicographic triples of 0..16, true = cup).
- **BFP certificates** come from FLAYER's `bfp.py` and T1's `t1lib.py`, copied unchanged.
  - An LP proposes a support; the multipliers are recomputed in exact rationals.
  - `bfp.verify_certificate` and `t1lib.check_cert` check each certificate.
  - R7's own `tools/certcheck.py` rebuilds the sub-chirotope from the model signs and checks it again. Negative
    control: flipping one sign the certificate uses makes it reject.
- **CEGAR driver `tools/cegar17.py`** (adapted from T1's `cegar.py`):
  - pysat CaDiCaL 1.9.5 with the CaDiCaL `--sat` options; the CNF is streamed in.
  - It starts from T3's model plus that model's BFP cut.
  - Before every solve the phases of all 13,448 variables are forced to the previous model. So each solve repairs the
    last model locally, and the learned clauses are kept.
  - Each certified obstruction is forbidden at every placement, in T1's four symmetry families: order-preserving,
    vertical mirror, and horizontal reflection with and without the mirror. These cuts are sound for real x-sorted
    sets (T1's record, Model and soundness).
  - A model without a certificate goes to `realize_sig.py` (90 s, seeds 1-2). A hit is re-checked by `exact17.py`.
- **Exact check of a hit, `tools/exact17.py`** (own code, Python integers only). It checks:
  - x strictly increasing and no collinear triple;
  - no 5-cap;
  - no 7 points in convex position (monotone-chain hull, cross-checked against "every 4-subset convex");
  - r ends a 4-cap;
  - all 2^16 subsets A of U: none is 4-cap-free, meets every convex hexagon of U and keeps A + r 4-cap-free.
- **m = 16 driver `tools/cegarm.py`** (lazy variant, any m):
  - Certified obstructions are kept as patterns. Each model is scanned (numpy) at every placement and in all 4
    families, and only the violated instances are added as clauses. These are the same clauses as
    `t1lib.cut_clauses`, so the same soundness argument applies.
  - BFP runs only on models that contain no known pattern. It is tried first on recent obstruction supports and
    their one-point extensions.
  - `tools/seed_phases.py` sets every variable of `root_cnf.py 7 16` to its defining condition on a real
    configuration.

## Results

| # | model (sign-string SHA-256) | source | 4-caps / at r / hexagons in U | realizer | BFP (minimal obstruction) |
|---|---|---|---|---|---|
| 0 | `72a678a9c704fc63…` (`root7_m17_s1`) | T3, CaDiCaL `--sat --seed=1` | 163 / 109 / 205 | T3: seeds 1-2 × 120 s, none (min margin −1.02e-5, 7 violated) | 9 pts + V, 27 ineq, mult 1 (full 17 + V: 486 ineq; no V-free cert found) — claim `root7-m17-nonreal-1` |
| 1 | `f5a84b8a0a0bb165…` | CEGAR iter 1 (0.8 s, Hamming 18 from #0) | 166 / 115 / 274 | – | 11 pts + V, 56 ineq |
| 2 | `3a7f367ae501628e…` | iter 2 (0.0 s, Hamming 1) | 168 / 116 / 282 | – | 14 pts + V, 225 ineq |
| 3 | `adbf1c0d756fae69…` | iter 3 (0.0 s, Hamming 1) | 167 / 115 / 282 | – | 12 pts + V, 136 ineq |
| 4 | `33825503aa93d027…` | iter 4 (0.0 s, Hamming 2) | 170 / 117 / 290 | **REALIZED** (seed 1, start 0, 10 bits, 0.3 s) | none (BFP-feasible) |

Model 4's realization is `root7_real17.json`. The exact check found 0 rooted weak Δs: **ROOT(7) fails** (EXACT). The
whole run took 14:05:26–14:09:26 KST.

**Deletions (EXACT, `tools/deletions.py` + `exact17.py`).** In each of the two real 17-point sets, every S − p
(p = 0..16) is (5,7)-valid and satisfies ROOT(7). The numbers of rooted Δs are:

- R7's set: 172, 230, 143, 95, **15**, 48, 175, 49, 61, 415, 92, 29, 215, 131, 56, 56. For p = 16 the new right end
  ends no 4-cap, so ROOT(7) holds vacuously there.
- T1's set: 124, 185, 88, 92, **15**, 52, 103, 34, 41, 636, 87, 46, 182, 80, 72, 72. Again none for p = 16.

So neither set gives a 16-point counterexample by one deletion.

## 16 points (from 14:13 KST)

Every search below only proposes candidates. A candidate counts only after `exact17.py` accepts it.

1. **Lazy BFP-CEGAR, unrestricted** (`tools/cegarm.py`, unit `esr-agw-r7-m16a`, 14:13–14:19). The run used T3's
   `root7_m16.cnf` (SHA-256 `bf8587c0…`; 9,205 variables, 154,471 clauses). Phases were forced to the real
   configuration root7_real17 − point 4 (`tools/seed_phases.py`), and the 9 m = 17 patterns were loaded. It found
   no model in 6 minutes; stopped and replaced by item 2.
2. **Hamming-ball search** (`tools/cegarm2.py`, unit `esr-agw-r7-m16b`, 14:19–14:29). Same CNF and seed. A pysat
   ITotalizer on the 560 "differs from the seed" literals bounds the distance, and the radii are tried in order:

   | radius | result | time |
   |---|---|---|
   | 6 | empty | 0.2 s |
   | 12 | empty | 1.0 s |
   | 18 | empty | 2.7 s |
   | 24 | empty | 9.2 s |
   | 32 | empty | 27.5 s |
   | 40 | empty | 106 s |
   | 48 | stopped unfinished (paused 14:25, unit stopped 14:29 for the 1-thread budget) | – |

   Label COMPUTED: solver verdict under an assumption, with no proof. "Empty" means that no assignment of the m = 16
   ROOT(7) CNF has its triple signs within that distance of the seed.
3. **One-point moves** (`tools/move16.cpp`, search only; driver `tools/move_driver.py`, unit `esr-agw-r7-mv1`, from
   14:25).
   - For each real 17-point counterexample S (R7's and T1's m17_it4) and each pair {p, q}, the base is
     B = S − {p, q}, a real 15-point set: 136 bases per set.
   - A 16th point z is tried around every vertex of the arrangement of the 105 lines through pairs of B and the 15
     vertical lines (4 directions × 4 offset scales), then at 2 million random multi-scale offsets.
   - Each z with B + z (5,7)-valid gets the full ROOT test.
   - Bases are ordered by how few rooted Δs their deletions S − p and S − q leave.
   - **Result (14:25:14–14:33:33):** all 272 bases done, about 2 s each.
     - 574,615,072 positions were tried.
     - 26,900,994 of them made B + z (5,7)-valid.
     - 19,538,637 got the full ROOT test.
     - 0 were reported, 0 verified, and no base timed out.
   - Label HEURISTIC: a search, not an exhaustive cell enumeration. Log `move/run1/bases.jsonl`, `move/run1/driver.log`.
4. **Annealing over real 16-point sets** (`tools/anneal16.cpp`, `tools/anneal16b.cpp`, driver `tools/anneal_driver.py`).
   - The search moves one point at a time to minimize the number f of rooted Δs. States that are not (5,7)-valid, or
     whose r ends no 4-cap, are rejected.
   - Starts: deletions S17 − p, coordinates × 2^16.
   - Results so far (HEURISTIC):

     | version | moves | run | result |
     |---|---|---|---|
     | v1 | random multi-scale | 1 × 300 CPU-s, 14:34–14:44 | f 15 → **12** at 23 s, then a plateau |
     | v2 | crosses the nearest of 12 random lines through two other points, else random | 1 × 200 CPU-s, 14:45–14:51 | f 15 → **10** at 12 s, then a plateau |

   - The 16-point prefixes of the round-6 pool of real (5,7)-valid sets are much farther from a counterexample:
     1,990 scored, best f = 594 (`tools/pool_starts.py`).
5. **Walks over real 17-point sets** (`tools/anneal17.cpp`, `tools/anneal17b.cpp`; units `esr-agw-r7-ann17`,
   `-ann17b`, `-ann17c`; 50 % CPU, from 14:52).
   - The objective g is the minimum over p of the rooted-Δ count of S − p. g = 0 would be a real 16-point
     counterexample. By T1's 16th-point lemma, every 16-point counterexample that has a valid extension left of r
     lies inside some 17-point counterexample.
   - Starts: R7's set and T1's three sets (all have g = 15, at p = 4).
   - **Constrained** (state must stay a 17-point counterexample), 1 × 300 CPU-s: g stayed at 15. About 157,000
     moves stayed inside the counterexample region, and none of them changed g, so the region looks rigid under
     single-point moves.
   - **Relaxed** (any 17-point set; objective g + 0.02·(f17, or 200 if S is not valid)), 1 × 240 CPU-s: g 15 → **9**
     at 131 s (deleting point 14). `exact17.py` confirms 9 rooted Δs for that 16-point set (m16/seed_g9.json:
     122 four-caps, 106 at r, 141 hexagons in U). Since 15:11 the search runs in chain mode: each start continues
     from its best state.
6. **Blind SAT** (unit `esr-agw-r7-blind16`, 50 % CPU, 14:34–15:11): CaDiCaL 2.1.3 `--sat --seed=2` on
   `root7_m16.cnf` (T3 used seed 1). Stopped without a verdict after about 37 min wall (about 18 CPU-min), to free
   the slot for item 7.
7. **Hamming-ball search around the g = 9 state** (`tools/cegarm2.py`, unit `esr-agw-r7-ballg9`, 50 % CPU, from
   15:11). Seed: m16/seed_g9.json.

   | radius | result | time |
   |---|---|---|
   | 6 | empty | 0.6 s |
   | 12 | empty | 3.5 s |
   | 18 | empty | 9.8 s |
   | 24 | empty | 24 s |
   | 32 | empty | 72 s |
   | 40 | empty | 292 s |
   | 48 | empty | 738 s |
   | 64 | stopped unfinished at 15:31 (slot given to item 9) | – |

   Label COMPUTED. The chain-mode continuation of the relaxed walk from the g = 9 state found no improvement in
   300 CPU-s (15:10–15:20).
8. **Large-neighbourhood descent** (`tools/lns16.cpp`, driver `tools/lns_driver.py`, unit `esr-agw-r7-lns`, 50 % CPU,
   from 15:22).
   - Each step takes one point of the 16-point set and tries every move16 candidate position for it: about 114,000
     arrangement-vertex neighbours plus 200,000 random offsets.
   - Candidates first pass an exact prefilter; survivors get the full rooted-Δ count. The step moves to the best
     position if it improves f; on ties it moves to a random best position with probability 0.3.
   - Starts: the g = 9 set, the f = 10 set (v2 annealing), and R7's set − point 4. Each start continues from its own
     best state.
   - **Run 1 (15:22–15:42, 600 CPU-s): f 9 → 6** at step 289 (365 steps, 8.75 million full counts). `exact17.py`
     confirms the 6 (`lns/f6.json`: valid, 147 four-caps, 111 at r, 112 hexagons in U, 6 rooted Δs).
   - From 15:43 the run continues from the f = 6 set only (unit `esr-agw-r7-lns2`). It reached f = 5 at 15:56 and
     **f = 4 at 16:00** (`lns/f4.json`).
     - The f = 4 set spans very different scales: r = (3000172318, −38491433675) lies far below the rest, and there
       are near-twin pairs.
   - A second descent ran from the f = 6 set, 15:50–16:01 (unit `esr-agw-r7-lns3`, `tools/lns16b.cpp`). It also
     accepts moves to a worse best position, with probability exp(−d/0.5), and found no improvement.
   - A second plain descent ran from the f = 4 set, 16:01–16:11 (unit `esr-agw-r7-lns4`). It found no improvement,
     and neither did the main descent's run 2 (16:03–16:23, 305 steps, seed 2).
   - The 4 rooted Δs of the f = 4 set are {2,3,7,8,10}, {2,3,7,8,10,12}, {2,3,7,8,11,13} and {4,5,6,10,11,14}. U has
     110 convex hexagons; the set has 131 four-caps, 111 of them at r.
   - **Depth-2 descent** (`tools/lns16c.cpp`, unit `esr-agw-r7-lns5`, 16:11–16:41, from the f = 4 set). When the
     best move of point i does not improve f, it takes each of the 4 best positions of i and relocates a random second
     point optimally. **No improvement** in 900 CPU-s: 279 steps, 209 depth-2 attempts, 14.7 million full counts. So
     f = 4 is a robust local minimum.
   - From 16:41 (unit `esr-agw-r7-lns7`): fresh descents from the g = 9 and f = 10 sets with new seeds (101, 102, …),
     to look for other trajectories.
     - Seed 101 from g = 9 went 9 → 8 → 6 → **4** by 16:50, along a different path. `exact17.py` on the result
       (`lns/f4b.json`): valid, 121 four-caps, 101 at r, 110 hexagons in U, 4 rooted Δs.
     - Its 4 rooted Δs are {2,3,8,9,10}, {2,3,8,9,10,12}, {2,3,8,9,11,13} and {4,5,6,10,11,14}. Up to relabeling, this
       is the same pattern as in the first f = 4 set. Both trajectories ended in the same kind of local minimum
       (HEURISTIC observation).
   - The pipeline's first descent (from m17_it3, after a walk to g = 11) reached f = 9 (586 steps, 16:39–16:59).
     Run 2 (T1's it4) walked to g = 9 and is descending.
10. **Hamming-ball search around the f = 4 set** (`tools/cegarm2.py`, unit `esr-agw-r7-ballf4`, 50 % CPU, from 16:53;
    seed `m16/seed_f4.lits` from `lns/f4.json`).

    | radius | result | time |
    |---|---|---|
    | 6 | empty | 0.3 s |
    | 12 | empty | 2.1 s |
    | 18 | empty | 5.8 s |
    | 24 | empty | 10.6 s |
    | 32 | empty | 54 s |
    | 40 | empty | 156 s |
    | 48 | empty | 515 s |

    Label COMPUTED. Radius 56 runs next; after the last radius the search continues unrestricted, with phases forced
    to the f = 4 set.
   - **Diverse starts** (unit `esr-agw-r7-lns6`, 16:23–16:31): a plain descent from m17_it3 minus point 4 (f = 15)
     made no progress in 7 min. The f = 15 deletions look like local minima for single-point moves; descent works
     only after a randomized walk.
   - **Pipeline** (`tools/pipe.py`, unit `esr-agw-r7-pipe`, from 16:31): a relaxed 17-point walk (240 CPU-s) from a
     real 17-point set, then a descent (600 CPU-s) from its best deletion. It cycles m17_it3, T1's it4 and R7's set,
     with seeds 11, 12, …
9. **Diverse real 17-point counterexamples** (`tools/cegarm3.py`, m = 17, units `esr-agw-r7-div17`/`-div17b`, 50 %
   CPU, from 15:31). This is the lazy BFP-CEGAR on `root7_m17.cnf`, but every model must differ from each known
   counterexample model in at least 30 triple signs. Each real hit is scored by its single-point deletions (anneal17
   evaluator).
   - First run (15:31–15:34): its distance constraint was **not enforced**. An ITotalizer output used as a positive
     assumption does not force a lower bound. Fixed in div17b with a sequential-counter at-least encoding.
   - That first run still produced a new real 17-point counterexample, `div17/real/m17_it3_s1.json`. `exact17.py`:
     valid, 173 four-caps, 119 at r, 261 hexagons in U, 0 rooted (EXACT; not filed). It is 18 sign flips from T3's
     model, and its best deletion again leaves 15 rooted Δs, at point 4.
   - div17b (15:34–15:50, 4 iterations, every model at distance exactly 30 from T3's model):

     | iteration | outcome |
     |---|---|
     | 1 | BFP-certified, 16-point V-free obstruction (309 inequalities) |
     | 2 | BFP-feasible, but `realize_sig.py` seeds 1-2 × 90 s failed (best minimum margin −1.1e-7 and −8.3e-8, one violated triple each); no late certificate; HEURISTIC block |
     | 3, 4 | only full 17-point + V certificates (531 and 524 inequalities), so the cuts are weak |

     At 2-3 min per iteration the run was too slow, and it was stopped to free the slot for a second large-neighbourhood
     descent (item 8).

**Controls for the m = 16 tools.**
- `move16` control mode against `exact17.py`, all agreeing:
  - re-adding a deleted point reproduces the deletion counts: 15 (three ways, including z = new r), 172 and 415;
  - 61 valid perturbed configurations give equal rooted counts (`move/ctl_compare.py`: 61 compared, 0 mismatches).
- The `anneal16` evaluator reproduces `exact17.py` on the deletions 4, 9, 0 and 11 (15, 415, 172, 29), and reports
  "vacuous" for deletion 16, where r ends no 4-cap.
- `anneal17` evaluates the four real 17-point sets as counterexamples (f17 = 0), each with minimum deletion count 15 at
  p = 4. This agrees with `exact17.py` and `deletions.py` for R7's set and T1's m17_it4.

## LP0(7) model W of P2: realizability (from 17:26 KST, coordinator's request)

The m = 16 searches were **stopped at 17:26** (units `esr-agw-r7-pipe`, `esr-agw-r7-ballf4`). The thread went to this
task.

- **Task.** P2's claim `lp0-7-false-abstract`: a 19-point (5,7)-valid signotope W on which LP0(7) fails. W restricted
  to its points 0, 1, 4, …, 18 is R7's real set `root7_real17.json`; points 2 and 3 are new. Is W realizable?
- **Fixed-block test** (`tools/extend2.py`, search only). Keep the 17 real points fixed and put each new point into its
  cell: strict linear sign conditions with every pair of block points plus the x-order, solved as an LP maximizing
  the normalized slack.
  - For all three of P2's W files the cell of each new point is **empty for this block**: max slack −0.126 / −0.134
    (oonn), −0.198 (onn), −0.126 / −0.132 (oonon). [corrected 15 Nov pm (C1 issue 9): HEURISTIC; these are float LP
    slacks from a search, with no exact certificate (V2's verdict on lp0-7-realblock-nonreal: "LP-slack context remark
    not checked (search only)")]
  - This holds only for this block realization; another realization of the same 17-point order type could behave
    differently.
- **`realize_sig.py` on W** (seed 1, 60 s): no realization; best minimum margin −1.2e-5 with 29 violated triples.
- **BFP: W = `w19_real17_oonn` is not realizable by ANY point configuration (EXACT).**
  - The 19-point chirotope (no V) carries a biquadratic-final-polynomial certificate with 686 three-term
    Grassmann–Plücker inequalities and positive integer multipliers (largest about 6.1e30).
  - Verified by `bfp.verify_certificate`, `t1lib.check_cert` and R7's own `tools/certcheck.py`.
  - The greedy shrink (120 CPU-s) found no smaller support.
  - File `r7/lp0/bfp_oonn_full_noV.json`. [note 15 Nov pm (C1 issue 9): claim `lp0-7-w19-nonreal`, V1 CONFIRMED
    (verdict file 17:37:28); the file's SHA-256 `8b7257fa…` is in the Files table below and equals the file on disk
    (checked by H1 at about 19:05)]
- **All 21 real-block W models are not realizable (EXACT; claim `lp0-7-realblock-nonreal`, V2 CONFIRMED 17:48).**
  [corrected 15 Nov pm (C1 issue 20): one of the 21 has only a certificate with V, so "no x-sorted realization" (next
  sub-items)]
  These are the 21 satisfiable models of P2's `lp0scan_k2.jsonl` with block R7's set (11) or T1's m17_it4 (10).
  - Run by `tools/lp0_bfp_batch.py`, unit `esr-agw-r7-lp0b`, 17:32–17:45.
  - 20 carry V-free certificates on all 19 points, so they have no realization at all. One (block r7, pattern
    onn…) carries a certificate with V, so it has no x-sorted realization. Sizes: 588–746 inequalities.
  - All 21 were rechecked by `tools/certcheck.py` (`r7/lp0/certcheck_all.txt`: 21 × True).
  - With the block fixed, every first new point's cell is empty: all 42 slacks are < 0, the largest −0.065.
    [corrected 15 Nov pm (C1 issue 9): HEURISTIC, float LP slacks; not checked by V2]
  - Files: `r7/lp0/batch/` and `r7/lp0/batch_SHA256SUMS.txt`.
- **The other 87 satisfiable W models of the scan are not realizable either (EXACT; claim `lp0-7-scan-all-nonreal`,
  V2 CONFIRMED 17:49).** [corrected 15 Nov pm (C1 issue 20): their certificates all use V, so these 87 have no x-sorted
  realization; realizations that are not x-sorted are not excluded]
  - Their blocks are T3's model and seven CEGAR models of R7 and T1. All are non-realizable, with certificates on
    9–14 points + V.
  - Each block certificate, re-indexed into W, is valid on W's own sign string: 87/87, by `tools/lp0_inherit.py` +
    `certcheck.py`.
  - So **none of the 108 satisfiable models of P2's scan has an x-sorted realization**.
  - This does not exclude other, realizable models with the same position patterns: the scan kept one model per
    pattern.
- **Direct real search for an LP0(7) counterexample W = S + 2 points (HEURISTIC, no hit).** Tool: `tools/lp0real.cpp`
  (search only; the trusted check is `tools/lp0check.py`).
  - Blocks S: the five real 17-point ROOT(7) counterexamples (R7's, T1's it4/it5/it6, R7's m17_it3).
  - Both new points lie left of r, at positions around every vertex of the arrangement of the current points (lines
    through pairs plus vertical lines; 4 directions × 3 scales). The z2 cells are deduplicated by sign vector.
  - W must be (5,7)-valid with some convex hexagon inside R1, i.e. made of points that end a 4-cap. By Lemma M, r
    stays unrootable.

    | block | valid z2 cells | valid W tested | hits |
    |---|---|---|---|
    | R7 | 82 | 118,587 | 0 |
    | T1 it4 | 82 | 105,295 | 0 |
    | m17_it3 | 86 | 122,785 | 0 |
    | T1 it5 | 80 | 101,771 | 0 |
    | T1 it6 | 76 | 90,280 | 0 |

  - Controls:
    - the C++ full check agrees with `lp0check.py` on 12 real 19-point pool sets, 3 of them with P0 missing a gon;
    - `lp0check.py` on R7's 17-point set gives 0 weak Δs through r and P0 meeting all 306 hexagons (LP0 holds
      there, as P2's k = 0 case requires).
  - **5-scale rerun** (`tools/lp0real5.cpp`, offsets 1e-1 … 1e-8, unit `esr-agw-r7-lp0r3`, 17:52–17:53): the same
    numbers of distinct valid z2 cells (82 / 82 / 86), which suggests the z2 cells are saturated. Valid W tested:
    166,208 (R7), 151,512 (T1 it4), 175,502 (m17_it3). **0 hits.**
  - **Up to 8 representatives per z2 cell** (`tools/lp0realK.cpp`, env R7K=8, unit `esr-agw-r7-lp0r4`, 17:54–18:03).
    The arrangement seen by z3 depends on where z2 sits inside its cell, so this run takes up to 8 positions per cell.

    | block | z2 positions | valid W tested | hits |
    |---|---|---|---|
    | R7 | 539 | 787,194 | 0 |
    | T1 it4 | 546 | 714,058 | 0 |
    | m17_it3 | 567 | 816,995 | 0 |
    | T1 it5 | 532 | 685,804 | 0 |
    | T1 it6 | 509 | 612,849 | 0 |

    In total 3.6 million valid 19-point sets were tested, with **0 hits** (HEURISTIC).

## Controls

- `exact17.py` on T1's real 15-point ROOT(6) set (n = 6) gives 86 four-caps, 37 at r, 254 pentagons in U, 992 weak Δs
  and 0 rooted, as in ROOT6_M15_REALIZE.md.
- `exact17.py` on T1's real 17-point set matches T1's own counts (169 / 111 / 314 / 0).
- The m = 16 phase assignment from root7_real17 − point 4 satisfies all 154,471 clauses of `root7_m16.cnf` except 15
  rows. Those 15 rows are its 15 rooted Δs. This is a positive control of the encoder at m = 16 on a real
  configuration, and it also checks `seed_phases.py`.

## Shared with T1 (coordinator's request, 14:09)

- `obstructions.jsonl`: R7's 4 certified patterns (k, withV, sub-signature, certificate, points, model).
- `obstructions.cnf`: the matching m = 17 clauses, grouped under a `c cut …` header each.
- `patterns_m17_all.jsonl`: the 9 distinct patterns of R7 and T1 (T1's from `t1/r7c17/models.jsonl`, each certificate
  re-verified exactly on import).

## Files (work dir `/home/jay/research/data/roadmap-20261115/pm1115/r7/`)

| file | SHA-256 |
|---|---|
| `root7_real17.json` (the real counterexample: P, signs) | `d9b5e6c453fb6f75ab0bbdab77fe0545682caafd059c5d36ddfda35dd7ab7d6e` |
| `cg17/real/m17_it4_s1.json` (realizer output) | `858357e062f1e13bf5eb299613b0ea19ebab1e62f8b3df4ee5cbee1c750c109a` |
| `cg17/real/m17_it4_s1.exact17.json` (exact check output) | – |
| `cg17/feasible/m17_it4.json` (CEGAR model) | `564da3e523e333ce69fba20abe17aad9827ebd3afc176a5bcca463a0521ffce0` |
| `cg17/models.jsonl`, `cg17/cuts.cnf`, `cg17/cegar.log` | `f347325c…`, `5d5b68ab…`, `87660b79…` |
| `root7_m17_s1.json` (copy of T3's model) | `8d6bedc1aa674552b67b9a24f22f6ceac8e58fa93c3c6395e33bc88cdf9efebd` |
| `bfp/s1_min.json` (9 pts + V certificate) | `0cc6d86ab8929f38e94b84bd1792b8929ae628549b9fce6db3c5e21da1a230fd` |
| `bfp/s1_full_withV.json` (17 pts + V, 486 ineq) | `c2a860670a137e7aa6506cad317faeb1caf2649a22f1aa75e507322b7f1e8263` |
| `init_s1.lits` (T3's full model, 13,448 literals) | `3b11a22919c2abc1fc0caa07ab168f36e97a84d9cd17055206148ed0befd01e7` |
| `tools/exact17.py` (own exact point-set checker) | `b2aa7a5da7483e9e4b7b3d44ecef47054297dabf3c70fb63379225d7bcf561f8` |
| `tools/certcheck.py` (own certificate checker) | `a9ac06f4e7b966494e1e9135b60ac1e60da63ffc24e99a001dfa5138aed790d8` |
| `tools/cegar17.py`, `tools/cegarm.py` | `7cff4540…`, `b8f0a5fd…` |
| `tools/seed_phases.py`, `tools/deletions.py` | `0dcda7c0…`, `d3a67f7b…` |
| `tools/bfp.py`, `tools/t1lib.py` (T1 copies) | `147b3690…`, `634345bf…` (= T1's files) |
| `obstructions.jsonl`, `obstructions.cnf`, `patterns_m17_all.jsonl` | `e4db9033…`, `a52ed6c9…`, `89755e92…` |
| `m16/seed_r7del04.lits` | `26486bfe…` |
| T3's `cnf/root7_m16.cnf` (input of the m = 16 run) | `bf8587c0be3743eb8531a712eddf22f6f66225150f53ad9f293593daf0af1962` |
| `lns/f4.json`, `lns/f4b.json` (best real 16-point sets, 4 rooted Δs) | `d7e0b287…`, `db3ce7dc…` |
| `lns/f6.json`, `m16/seed_g9.json` | `c1f815cf…`, `2becda82…` |
| `div17/real/m17_it3_s1.json` (extra real 17-point counterexample, not filed) | see `div17/` |
| `lp0/bfp_oonn_full_noV.json` (W, V-free certificate, 686 ineq) | `8b7257fabd0d1ff70e9bdd9da4b054665fca23dec8f7ff07af4d628cf9a256b7` |
| `lp0/batch/` (21 real-block W models + certificates), `lp0/batch_SHA256SUMS.txt` | `4aab1ec6…` (sums file) |
| `lp0/inherit/` (87 abstract-block W models + re-indexed certificates), `lp0/inherit_SHA256SUMS.txt` | `69212f16…` (sums file) |
| `lp0/real/` (two-point real search: blocks, logs, empty hit files) | – |
| `tools/move16.cpp`, `anneal16(b).cpp`, `anneal17(b).cpp`, `lns16(b,c).cpp`, `lp0real(5).cpp` (C++ search) | `c2862d98…`, …, `df1ac9ef…` |
| `tools/extend2.py`, `lp0_bfp_batch.py`, `lp0_inherit.py`, `lp0check.py`, `make_claim16.py` | `41ad746d…`, `527c7133…`, `e9d29c41…`, `07068377…`, `578fd2e8…` |

## Units started by R7 (all stopped; none running at 18:04)

| units | what |
|---|---|
| `esr-agw-r7-bfp0`, `-cg17`, `-del` | m = 17: BFP on T3's model, the CEGAR (its hit is the real set), the deletions |
| `-m16a`, `-m16b`, `-blind16`, `-ballg9`, `-ballf4` | m = 16 abstract searches: CEGAR, Hamming balls, blind CaDiCaL |
| `-mv1`, `-ann`, `-ann2`, `-ann17`, `-ann17b`, `-ann17c`, `-pool` | m = 16 real searches: one-point moves, annealing, 17-point walks, pool scoring |
| `-lns`, `-lns2` … `-lns7`, `-pipe` | m = 16 large-neighbourhood descents and the walk-then-descent pipeline |
| `-div17`, `-div17b` | diverse real 17-point counterexamples |
| `-wreal`, `-ext2`, `-ext3`, `-lp0b`, `-lp0i`, `-lp0r`, `-lp0r2`, `-lp0r3`, `-lp0r4` | LP0(7): realizer, cell tests, BFP batch, re-indexed certificates, real search |

All ran with CPUQuota ≤ 100 % in total (two 50 % units at most from 14:34). One exception was a 50 s foreground
`realize_sig.py` run at 17:26, without BLAS pinning (up to about 8 threads); after that every numpy job ran inside a
pinned unit.

## What remains

- **16 points (and 15) for ROOT(7): open.**
  - The abstract m = 16 CNF is undecided: blind CaDiCaL ran 35 CPU-min with seed 1 (T3) and about 18 CPU-min with
    seed 2 (R7), without a verdict.
  - Deciding UNSAT would need a long, probably cubed, LRAT-certified run. That was not attempted (budget).
- **Real-set search.** The best real 16-point set has 4 rooted Δs (`lns/f4.json`, `lns/f4b.json`; same pattern).
  - Next tries: other starting families (the pipeline on T1's and R7's sets), wider moves (two points at once), and
    more abstract searches around the 4-Δ sets.
- **Not done:** abstract m = 15 for ROOT(7) (T3 had it queued); a certificate for any of the COMPUTED "empty ball"
  statements.
- **Optional:** file the extra real 17-point set `div17/real/m17_it3_s1.json` for verification. Not needed, since
  `root7-real-17` is CONFIRMED.
- **LP0(7) for real sets: open.** Every satisfiable model of P2's two-point scan is non-realizable, but the scan kept
  only one model per pattern. A CEGAR over P2's extension CNF with BFP cuts would settle the patterns abstractly.
  Larger k, or blocks other than the five real ROOT(7) sets, were not tried.

## Resume

```bash
R7=/home/jay/research/data/roadmap-20261115/pm1115/r7; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
CNF16=/home/jay/research/data/roadmap-20261115/pm1115/t3/cnf/root7_m16.cnf; CNF17=/home/jay/research/data/roadmap-20261115/pm1115/t3/cnf/root7_m17.cnf
$PY $R7/tools/exact17.py $R7/root7_real17.json 7                      # exact check of the real 17-point set (~2 s)
$PY $R7/tools/exact17.py $R7/lns/f4.json 7                            # the best real 16-point set: 4 rooted Deltas
$PY $R7/tools/certcheck.py $R7/root7_m17_s1.json $R7/bfp/s1_min.json  # own check of the 9 + V certificate
$PY $R7/tools/deletions.py $R7/root7_real17.json $R7/del_r7 7          # all single deletions
U="systemd-run --user -p CPUQuota=50% -p MemoryMax=1200M -p MemorySwapMax=0 -p RuntimeMaxSec=<s> --nice=10 --working-directory=$R7"
# Hamming-ball CEGAR around a real 16-point configuration (seed lits from tools/seed_phases.py points.json 7 out.lits)
$U --unit=esr-agw-r7-ball $PY -u tools/cegarm2.py $CNF16 m16/<dir> <deadline_epoch> 1 m16/seed_f4.lits patterns_m17_all.jsonl 16 7 90 6,12,18,24,32,40,48
# large-neighbourhood descent (chain mode) from a 16-point start file (16, then "x y" lines)
$U --unit=esr-agw-r7-lns -E LNS_BIN=lns16 -E SEED0=201 $PY -u tools/lns_driver.py lns/<dir> <deadline_epoch> 600 150000 lns/start_f4.txt
# walk-then-descent pipeline from real 17-point sets
$U --unit=esr-agw-r7-pipe $PY -u tools/pipe.py <dir> <deadline_epoch> 240 600 150000 anneal/s17_t1it4.txt anneal/s17_r7.txt
# diverse real 17-point counterexamples (repel distance 30 from the listed models), with deletion scores
$U --unit=esr-agw-r7-div -E R7_REPEL=<model.json,...> -E R7_REPEL_D=30 -E R7_COLLECT=1 $PY -u tools/cegarm3.py $CNF17 <dir> <deadline_epoch> 1 init_s1.lits patterns_m17_all.jsonl 17 7 90
# C++ tools: g++ -O2 -march=native -o tools/X tools/X.cpp  for X in move16 anneal16 anneal16b anneal17 anneal17b lns16 lns16b lns16c
```
