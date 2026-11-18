# LOWERBOUND_PLAN_1115PM: next lower-bound experiments for ES(7) and ES(8) (track E7, 15 Nov 2026, written 17:00-18:30 KST)

**Status: a plan, not a result.** No compute was run for this file, and it makes no new claim. Every cost figure is
HEURISTIC, with its basis stated. Every value and odds figure is subjective. Labels quoted from other records are
theirs and were not re-checked here unless this file says so. Nothing here bounds ES(7) or ES(8). Nothing was launched.
Which experiments run, and when, is for the main session and the owner to decide.

Written by the workflow's track-E7 agent. The only repository write was this file. The agent also kept copies of the
roadmap agent outputs in its own scratchpad, for reading. No git, no e-mail, no web request. All commands were
read-only: file reads, listings of the ring's case folders, the `esr-*` unit list, `cpu_free.sh`, `free` and `df`.

## 0. Bottom line

- **Ten experiments, five per topic.** They are ranked below by expected value per CPU-hour; §7 shows the scoring.
  Ranks 5, 7 and 9 are k = 9 or radius-1 items whose gates are given in their sections.

| rank | id | experiment | CPU-h (HEURISTIC) | threads / memory | label if it succeeds |
|---|---|---|---|---|---|
| 1 | E8-1 | ABSAT8 sweep 2. Targets: the SMQH crossed 64-point set, all 1,592 stacking order types (359 with no recorded test) and the octagon-vertex deletions of the recorded one-octagon 65-point sets | ≈ 1-2 | 1 / 0.5 GB | CERTIFIED per CNF + PROVED soundness |
| 2 | E7-1 | ABSAT7: the same verified encoder at k = 7 on the two symmetric 32-point maxima, the 7 deletions of AlphaEvolve's 33-point set, the 1,911 near-full deletions and the 8,537-set pool; plus the DDSZ value check | ≈ 1-2 | 1 / 0.5 GB | CERTIFIED per CNF + PROVED soundness |
| 3 | E8-2 | CONE4 gate (4-fold, 14 layers, fixed phases) | ≈ 2 | 1 / 5 GB | COMPUTED (gate verdicts) |
| 4 | E7-4 | Near-mirror class M16+1 (16 mirror pairs + 1 free point) in the zcnf model: calibration only | ≈ 3, plus agent-hours | 1 / ≤ 6 GB | COMPUTED (calibration) |
| 5 | E8-5 | Two-arm one-descent pilot (k = 9); runs inside E8-4's scheduler | ≈ 2 | 1 / 4 GB of the k9 slice | COMPUTED (pilot) |
| 6 | E7-2 | Joint two-point (radius-1) extension model, built and validated at k = 7 | ≈ 2-20, plus about one agent-day | 1 / ≤ 2 GB | CERTIFIED per CNF, after a written soundness note |
| 7 | E8-3 | Radius 1 at k = 8 around AlphaEvolve's 65-point set: sizing only, after E7-2 | ≈ 2 | 1 / ≤ 4 GB | HEURISTIC (sizing) |
| 8 | E7-3 | (7,6,6)@31 seed miner over realized 32-point pools | ≈ 1-2 | 1 / < 0.5 GB | EXACT for mined subsets |
| 9 | E8-4 | k = 9 ring "two displaced layers": the remaining 20 cyclic and 93 linear cases | ≈ 40-45 | 2 / 13.2 GB slice | CERTIFIED per case |
| 10 | E7-5 | (7,5,7)@27 staged Knuth estimate, with ES7_FEASIBILITY's Step 0 | ≈ 35-50 for stages 0-1; ≈ 120 more for stage 2 | 4-15 / 1 GB each | HEURISTIC |

- **Recommended first block.** E8-1, E7-1, E8-2 and E7-3, about 5-7 CPU-h in all. They fit in one evening on at
  most 2 threads and at most 6 GB, beside the upper-bound jobs.
  - E7-3 ranks 8th by value per CPU-hour. It belongs in the block anyway, because it is light and is the only cheap
    item with any chance, though a tiny one, of a direct counterexample.
- **No cheap experiment can settle ES(7) = 33 or ES(8) = 65.** The cheap items yield either certified statements
  about named sets and families, or decisions about expensive lines.
  - A counterexample could come only from three places. E7-3, with tiny odds. A SAT answer in E7-1, E7-2, E8-1 or
    E8-3 that is then realized. A SAT case in E8-4, which concerns k = 9 symmetric sets only.
- **The two expensive items, E8-4 and E7-5, need the memory and threads the upper-bound jobs hold now.**
  - memguard gives the n66 track 17,000 MB of the 24,000 MB total.
  - `cpu_free.sh` printed 1 free thread at 17:08 KST.
  - The N66 cube units and the (20,15) loop have deadlines of about 18:44 tonight. Many Δ agent units are also
    running.

## 1. What is known (as recorded; labels are the records')

**ES(7).** 33 ≤ ES(7). The upper bounds are 113 (refereed) and 81 (unrefereed; NOVELTY20261113B).

- **32-point heptagon-free sets.** Examples: `ES7SPLIT/data/classical32.txt`, `SYM2/sym7_32points.txt` (half-turn),
  `SYMMAX/mirror_32points.txt` (mirror), and 8,537 distinct annealed order types (`inputs/distinct_K7*.txt`).
- **Theorem A** (RESULTS C1). No heptagon-free set of 33 or more points has a nontrivial isometric or affine
  symmetry.
  - Computer-assisted; the reduction and the mirror classes are Lean-checked.
  - Its weakest link is Theorem 1 (threefold 33). It rests on recorded verdicts, and the CNF-level check of
    Lemma 5 / H6M is still open (AUDIT3 §5 row 9).
- **ES7SPLIT** (written proofs, internally reviewed).
  - Every nontrivial z-split of a 33-point heptagon-free set is unbalanced.
  - Such a split exists iff N(7,5,7) ≥ 27. The direction from N(7,5,7) ≥ 27 is Theorem 6: glue a 6-point cap far
    below a 27-point witness.
- **ETV ladder.**
  - 26 ≤ N(7,5,7) ≤ 36: the N = 37 CNF is CERTIFIED (ETV7SAT20261113), on a written soundness argument.
  - N(7,5,6) = 25 is CERTIFIED.
  - N(7,6,6) = 30 is open.
- **Brute force** (ES7_FEASIBILITY, HEURISTIC).
  - ES(7) = 33 at 33 points: about 1e3-1e4 CPU-years at the central reading.
  - Cheapest reading: 4-42 CPU-years, for the weaker (7,5,7)@27 statement.
- **Search side** (COMPUTED unless noted).
  - **Task A:** all 8,544 sets (8,630 with the near-full deletions) are abstractly saturated in the x-sorted signotope
    model. CaDiCaL 3.0.1, no proofs; the pool was tested in two sweep directions.
  - **A2:** 411,693 neighbourhood instances (r = 3-7), all UNSAT.
  - **D2:** no geometric extension face in 1,918 near-full deletions.
  - **Symmetric maxima, this morning:** a face sweep of the two 32-point symmetric maxima found no extension face
    (roadmap map, D2's satcount, one tool, no independent re-check). A durable copy of the output is in
    `/home/jay/research/data/roadmap-20261115/scratchpad-snapshot-20261115/ext32/`.
  - **lower7 probe:** the colouring-27 repair is dead; the forced 5-cap is PROVED. 0 SAT in 10,611 (7,6,6)@31
    window calls around mid30.
- **AlphaEvolve's 33-point set (AE33)** has exactly one convex 7-gon, at JSON indices
  {14, 15, 17, 20, 23, 25, 32} (A/README §1, exact recount).
- **273 near-full sets** (`inputs/nearfull_p2c.txt`, `nearfull_p2d.txt`) have 33 points and exactly one convex 7-gon
  each. Deleting a heptagon vertex gives 1,911 32-point sets, 86 of them not in the pool (A/README §1).

**ES(8).** 65 ≤ ES(8) ≤ 308. The upper bound is computer-assisted, unrefereed and uncommitted.

- **ABSAT8_INDEPENDENT** (CERTIFIED + PROVED soundness; V1 and V3 CONFIRMED).
  - Covered: 35 named 64-point sets. They are the 17 pilot sets, w1-w3, the 8 octagon-vertex deletions of AE65
    (AlphaEvolve's 65-point set) and the 7 seven-fold types. The record does not claim that the first 28 are pairwise
    distinct order types.
  - No realization of any of them extends by one point without a convex octagon.
  - Encoder: `l1enc` (`/home/jay/research/data/roadmap-20261115/pm1115/l1/src/l1enc.cpp`). Usage
    `l1enc points.txt k out.cnf`; it takes 4-64 points and any k. `l1enc_big` is the GMP variant.
  - Measured cost: about 0.29 CPU-s per 64-point set (ABSAT0). A cake_lpr heap of 300 MB suffices.
- **Symmetric table at k = 8.**
  - Exact: mirror 46, 6-fold 60, 7-fold 64.
  - Lower bounds only (Lean-checked, LEANLB): 3-fold ≥ 61, 4-fold ≥ 52, 5-fold ≥ 56, half-turn ≥ 64.
  - Symmetric counterexamples to ES(8) = 65 are excluded for mirror, 6-fold, 7-fold and order ≥ 8. They are open
    for 2-, 3-, 4- and 5-fold.
- **AE65** has exactly one convex octagon, with vertices {0, 1, 15, 23, 27, 29, 30, 57}.
- **Stacking family** (`experiments/es8-lower-bound-search-2026-10-11`).
  - 1,592 order types come from certified trees.
  - The 1,233 types within sat.c's coordinate bound were tested geometrically, and all are saturated.
  - **359 types with larger coordinates "remain untested"** (README lines 238-272); no later record read here tests
    them.
- **One-octagon 65-point sets** in the same experiment: `anneal/init_w8p_1-4` and `init_v8p_1-3`. Each is an
  octagon-free 64-point set plus one point, with exactly one octagon. The `m65w_*` outputs are byte-identical to these
  start sets.
- **k = 9 ring** (SATOPEN addendum, 09:40).
  - CERTIFIED so far: 155 of 175 cyclic and 2 of 95 linear cases.
  - Remaining: 20 cyclic cases and 93 linear. A listing of the case folders at 17:05 shows that all 20 cyclic cases
    have P = 1 or P = 13.
- **K9ARM probe:** no zero; the 112-point seed bottoms out at 1,344 convex 9-gons (HEURISTIC).

## 2. ES(7): five experiments

### E7-1. ABSAT7: certified order-type-level one-point non-extendability at k = 7, plus the DDSZ value check

**Statement.**

- For each set S: S is a named 32-point heptagon-free set with exact integer coordinates in general position. For
  every realization S' of the labelled order type of S, and every point p with S' ∪ {p} in general position, S' ∪ {p}
  contains a convex 7-gon through p.

**Targets, in order.**

1. **The two 32-point symmetric maxima,** `SYMMAX/mirror_32points.txt` and `SYM2/sym7_32points.txt`. Neither was
   ever tested in an abstract model. Their geometric face sweeps from this morning are COMPUTED for these coordinates
   only (`scratchpad-snapshot-20261115/ext32/`).
2. **The 7 heptagon-vertex deletions of AE33** (`inputs/alphaevolve_pts.json`, key `points_7`).
   - Deleting a vertex v off the heptagon leaves the heptagon in place, so only these 7 deletions matter.
   - UNSAT for all 7 therefore gives a clean statement. No 33-point heptagon-free set contains a 32-subset with the
     order type of a 32-subset of AE33, in any realization. In words: moving one point of this near miss (one of the 274 recorded one-heptagon sets)
     never helps.
3. **The 1,911 heptagon-vertex deletions of the 273 near-full sets.** The same statement then holds for all 274
   recorded one-heptagon 33-point sets.
4. **The 8,537-set pool.** This upgrades Task A's COMPUTED result in two ways: from one or two x-sorted sweep
   directions to every realization, and to CERTIFIED.
5. **Value check (agent work, seconds of compute).** The check needs an explicit DDSZ saturated heptagon-free set of
   non-maximum size (arXiv:2312.01223; ABSAT8 §9).
   - The suggested start is n = 7: 28 points built from DDSZ's 8-point (4,5)-cup-cap-saturated set. Their
     construction uses "sufficiently small" ε and δ, so an explicit instance must be built first.
   - Verify its geometric saturation exactly with an exhaustive face sweep (D2's satcount), then run l1enc at k = 7.
   - If UNSAT: order-type non-extendability also holds for a saturated set that is not maximum. Then the ABSAT
     results are evidence of saturation, not of maximality.
   - If SAT: the abstract test sees more than geometric saturation.
   - This one check calibrates what E7-1 and E8-1 mean.

**Encoding and soundness direction.**

- **Encoder.** `l1enc set.txt 7 out.cnf`, unchanged; use `l1enc_big` where the coordinates are too large.
  - The families are R2 + AC + OCT, with OCT built from the 4-chains of the convex 6-gons of S.
  - Size of a 32-point CNF (from l1enc's formulas): 496 variables, 32 × 870 = 27,840 R2 clauses and C(32,3) = 4,960 AC
    clauses, plus OCT.
- **Soundness.** The proof in ABSAT8_INDEPENDENT §3 is written for any n and any convex polygon Q: Cramer for R2,
  barycentric coordinates for AC, the visibility and slot lemmas for OCT. It therefore covers k = 7.
  - Direction: a real point with no 7-gon through it gives a model, so UNSAT excludes it.
  - The order-type invariance of §3 carries over unchanged.
- **Required before any claim.**
  - One paragraph stating the k-generic reading.
  - The §6 controls at k = 7:
    - C2: the sets are heptagon-free (`l1check`);
    - C3: delete and re-extend;
    - a C4-type control on AE33 − v for v off the heptagon, encoded with `--allow-kgon`. The real v must satisfy every
      clause;
    - C1: real points;
    - C7: both directions of OCT on subsets.
  - A VERIFY step by a second agent with its own code, as V1 and V3 did for ABSAT8.

**Size and cost (HEURISTIC).**

- ABSAT0 measured about 0.29 CPU-s per 64-point set, and a 32-point CNF is several times smaller.
- So allow ≤ 0.3 s per set: about 0.9 CPU-h for all ≈ 10,450 sets, plus 0.5-1 CPU-h of controls.
- Keep the LRATs as zstd (tens of KB each), record the CNF hashes and regenerate the CNFs on demand.

**Outcomes.**

- **All UNSAT.** CERTIFIED per CNF plus PROVED soundness, for these named sets only. Nothing about ES(7) beyond them.
- **Any SAT.** That is an abstract one-element extension with no 7-gon through p: a 33-element abstract candidate.
  - Realizability is open: a realization search is needed, then an exact check with `l1check` or brute force.
  - Report it at once and claim nothing.

**Resources.** 1 thread; unit MemoryMax 500M, with the cake_lpr heap at 200-300 MB. ABSAT8's peak RSS was about
310 MB at 64 points. About 1-2 h wall. The work directory goes under `~/research/data/`.

### E7-2. Joint two-point (radius-1) extension model, built and validated at k = 7

**Statement.**

- For each base B (B = S minus one or two points, S named): for every realization B' of the order type of B, and all
  points p, p' with B' ∪ {p, p'} in general position, B' ∪ {p, p'} contains a convex 7-gon.

**Targets** (about 237 CNFs).

1. The 3-fold and 5-fold 31-point maxima, `SYMMAX/c3_31points.txt` and `c5_31points.txt` (2 CNFs).
2. Radius 1 around the two 32-point maxima: B = S − u, with u up to the symmetry (16 + 16 = 32 CNFs).
   - This tests 33-point sets that share 31 points with a symmetric maximum. It is a set-specific relative of the
     near-mirror and near-half-turn classes, at a small fraction of their cost.
3. Radius 1 around AE33: B = AE33 − {u, v}, with {u, v} meeting the heptagon. That is C(33,2) − C(26,2) = 203 CNFs.

**Encoding sketch** (the "Task A design" of the ES(8) synthesis, item 5; a new encoder).

- **Variables.**
  - X(a,b) = [orient(a,b,p) > 0] and X'(a,b) = [orient(a,b,p') > 0] for a < b in B.
  - W(a) = [orient(a,p,p') > 0] for a in B.
- **Families.**
  - R2 and AC for p and for p', exactly as in l1enc.
  - 3-term Grassmann–Plücker clauses on the 5-sets {a, b, c, p, p'}. The 5-sets with a single new point are covered by
    R2.
  - Acyclicity clauses for the triangles that contain p or p'.
  - 7-gon clauses through p only and through p' only: l1enc's OCT, in X and in X'.
  - 7-gon clauses through both: one family per convex 5-gon Q of B and per placement of p and p' in its edge slots.
- **The soundness note must handle the two-point placements.**
  - Placements on two non-adjacent edges follow from the slot lemma.
  - Placements on adjacent edges, or on the same edge, need W literals. The shared vertex must stay a vertex, and the
    order of p and p' along the edge must be convex.
  - Proving this is the main job of the written note.
- **Direction.** Real p, p' with no 7-gon give a model, so UNSAT excludes them. No completeness is needed.
- **Positive controls.**
  - Delete two points of real heptagon-free sets and re-insert them. The CNF must be SAT, and the real points must
    satisfy every clause.
  - Real-point sampling as in ABSAT8 §6.
  - A k = 6 run: UNSAT is forced at 15 + 2 = 17 points, because ES(6) = 17, and SAT is expected for smaller bases.

**Size and cost (HEURISTIC).**

- **CNF size at n = 31.** 961 variables. About 50k R2 clauses, 9k AC clauses, 10^5-5·10^5 GP clauses, ≤ 10^6
  one-point 7-gon clauses, and ≤ 3·10^6 two-point clauses (convex 5-gons of B × about 30 placements). In total
  ≤ 5·10^6 clauses, under 1 GB.
- **Solve time: unknown.** The one-point versions take under 0.1 s, and Task A's restricted r = 2 neighbourhoods
  averaged 3.4 conflicts per call.
  - At 10 s to 5 min per CNF, 237 CNFs cost 0.7-20 CPU-h.
  - Size on 3 CNFs first.
- **Development.** About one agent-day for the encoder, the note and the controls.

**Outcomes.**

- **All UNSAT.** CERTIFIED radius-1 statements for these named bases, plus a validated tool for E8-3.
- **Any SAT.** An abstract 33-element candidate with two new elements; realizability is open.

**Prior work.** At k = 7, Task A's N1 neighbourhoods (r = 2, 3; COMPUTED) were more restricted. The new points went
into the deleted points' x-slots plus one extra gap, and the x-sorted signotope was fixed. The joint model has neither
restriction and covers all realizations.

**Resources.** 1 thread, ≤ 2 GB.

### E7-3. (7,6,6)@31 seed miner

**Statement.**

- **The search.** In realized heptagon-free 32-point sets, look exactly for 31- or 30-point subsets with no 6-cap and
  no 6-cup in some sweep direction.
- **A 31-point hit** is an exact (7,6,6) witness, so N(7,6,6) ≥ 31. That contradicts the Erdős–Tuza–Valtr value 30.
  - ES(7) = 33 implies N(7,6,6) = 30, by ETV 1996 as recalled in ES7_FEASIBILITY §7 and in the roadmap map. This was
    not re-checked here.
  - So a hit would also refute ES(7) = 33.
- **A 30-point hit** is a seed for exact window insertion runs at 31 points.

**Encoding.**

- **The miner** is exact integer C.
  - For each set, it takes each of the O(n²) combinatorially distinct sweep directions (sorted pair slopes).
  - It computes the x-order and all 6-caps and 6-cups, then tests whether at most 2 points hit all of them.
- **No soundness question.** Subsets of heptagon-free sets are heptagon-free, and every hit is re-checked by brute
  force (EXACT).
- **Window runs on seeds** use the probe's unchanged `nbwin_v2.py` on `gen_etv 31 6 6 7`, the Lean-verified
  generator.
  - Window verdicts are COMPUTED.
  - A SAT model is only a signotope and needs a realization plus an exact check.
- **Pools** (SYNTHESIS §2.3 item 2): A's 8,537 sets, F2's 93 glued sets and D2's swept states.

**Cost (HEURISTIC).**

- The miner: ≤ 1 CPU-h, the synthesis' figure.
- Windows at r = 6: 7,242 calls, about 0.2-0.65 CPU-h per seed, scaled from the lower7 probe (r = 2-5 measured,
  152 CPU-s in all).
- Cap the windows at 5 seeds.

**Outcomes.**

- **A 31-point hit** is decisive, after the exact checks and an independent recount.
- **30-point hits with all windows UNSAT** are weak negative evidence. The probe's rule still forbids a bulk window
  sweep.
- **No hits** record that the realized pools contain no (7,6,6) near-witness. That too is weak evidence.

**Before any "untried" wording.** Read Balko–Valtr (EJC 2017) and write the double-gluing note (ES7SPLIT
Corollary 4, applied twice).

**Resources.** 1 thread, < 0.5 GB.

### E7-4. Near-mirror class M16+1 in the zcnf model: calibration only

**Target statement** (only if the whole class is later run and certified).

- No 33-point heptagon-free set in general position contains a 32-point subset made of 16 pairs symmetric under one
  reflection.
- Whether this covers isometric or also affine reflections must be fixed by the soundness note.
- Theorem A does not cover this class: at an odd size, its mirror case needs an axis point.

**Encoding.**

- **Base:** SYMZ's `zcnf.py` (mirror, 16 pairs, no axis point), extended by one unpaired element q with
  v_q = (1, x_q, y_q).
- **Rules for q.**
  - Keep SYMZ §1's facts 1-7 for the core and for Z.
  - The pair identity χ(Z, L_i, q) = χ(R_i, L_i, q) = χ(Z, R_i, q) still holds.
  - The group-action identity must not be applied to triples that contain q.
  - Convexity variables for subsets that contain q get no orbit identification.
  - WLOG x_q > 0, by reflecting the whole set.
- **Split** by the height rank t ∈ {0, …, 16} of q among the pairs: 17 CNFs. General position gives y_q ≠ b_i.
- **Direction.** A real near-mirror configuration gives a model, so UNSAT excludes it.
- **Before any run.** A written soundness note, plus controls on real near-mirror sets: exact evaluation of the CNF on
  real configurations (for example at k = 6), and SAT controls at sizes where such sets exist.
- **Do not use the x-sorted overlay.** It encodes only the combinatorial reversal. Record C's m33k7 and hm33k7 runs on
  it never closed (critic lower7:3).

**Cost (HEURISTIC).**

- **Calibration.** Run t = 0 and one middle t.
  - SYMZ's mirror33 (695,928 variables, 14,080,656 clauses) took 964 s.
  - The critic's stop rule: stop if a position takes more than 10 times that, about 2.7 h.
  - Budget: ≤ 3 CPU-h.
- **Full class.** 17 positions at 0.3-2.7 h each: about 5-46 CPU-h of solving.
- **Certification is the obstacle.**
  - AUDIT3 §5 row 1 lists a cake_lpr heap of 30,000 MiB for mirror33 and mirror34 (4.1-4.4 GB proofs). That is above
    the 24 GB cap.
  - So each position would have to be split into cubes whose proofs fit a ≤ 10 GB heap.
  - Realistic total to CERTIFIED: 50-300 CPU-h.

**Outcomes.**

- **Within 10 times SYMZ:** the owner decides whether to fund the class.
- **Slower:** park it and record why.
- **SAT at a position:** an abstract candidate only. The zcnf model is a relaxation; the fourfold 32-point formula is
  SAT although no real set exists (SYMZ §2). A realization would be needed.

**Resources.**

- 1 thread. Solve without LRAT for the calibration.
- Memory: CaDiCaL on 15-30 M clauses needs about 2-4 GB by the k9 ratio (3.9 GB for 29.8 M clauses). The house rule
  of 150-250 B per literal gives up to about 10 GB.
- So measure on the first CNF. Use a unit with MemoryMax 6G under memguard.

### E7-5. (7,5,7)@27 staged Knuth estimate (ES7_FEASIBILITY §6, with its Step 0)

**Statement: none; this is a cost estimate.**

- **What it measures:** the cost of a cube-and-conquer proof of N(7,5,7) = 26, i.e. UNSAT of `gen_etv 27 5 7 7`
  (20,078 variables, 261,082 clauses).
- **Pipeline:** B2's (cncw lookahead splitting), on CaDiCaL 3.0.1 from
  `~/research/data/erdos810-20261106/cadical/build/libcadical.a`. The library exists; `results/B2/scripts/cncw.cpp`
  and `knuth.py` exist. march_cu is not installed.
- **A SAT leaf** would be a signotope only and would need a realization.
  - If realized, ES7SPLIT Theorem 6 turns it into a 33-point heptagon-free set.
  - The odds are negligible.

**Stages.** Only the order of ES7_FEASIBILITY's runs changes; its decision rule stays as written.

- **Stage 0** (2-4 thread-h, 1 unit).
  - Rebuild cncw. Time one dive on n33k7hm (`gen_cnf 33 7 --hull --mirror`, not yet generated), then 20-50 random
    dives.
  - Apply ES7_FEASIBILITY's 33-point stop rule: an estimate ≥ 1e6 CPU-h stops 33-point brute force for good, and the
    record says so.
  - Time one dive on `etv757_27.cnf` to set the probe budgets.
- **Stage 1** (about 30-50 thread-h: 4-6 units for one night).
  - Probes at the deep cutoffs, depths about 24 and 30.
  - Plus the calibration arm: 4 random 1/1024 sub-trees of (7,5,6)@26, each run to completion. B2's mean is about
    1.1 core-h per sub-tree, heavy-tailed.
  - **Why the deep cutoffs come first.**
    - Suppose the tree were complete to depth d. B2's mean of 205,458 core-h would then put the mean leaf at about
      44 s at d = 24 and about 0.7 s at d = 30.
    - So 150 or more uncensored probes per cutoff cost a few core-hours, plus dive time. Dives take about 150-250 s
      per 30-40 nodes, scaled from ES7_FEASIBILITY's 400-560 s on the larger 33-point CNF.
    - B3 also found that the estimate rises with depth (18 < 24 < 30). The deep cutoffs are therefore the more
      tail-aware basis for a "stop".
- **Stage 2** (about 120 thread-h; only if stage 1 is inconclusive).
  - The depth-18 cutoff, which ES7_FEASIBILITY's "go" rule needs.
  - At d = 18, on the same complete-tree reading, the mean leaf is about 0.8 core-h (B2's mean / 2^18). So 150
    uncensored probes need about 120 core-h.
  - That is more than one night's 3-4 units per cutoff provide. Expect censoring, and so a lower bound only, unless
    this arm gets most of a night.

**Outcomes** (ES7_FEASIBILITY §6).

- **Go:** the bias-corrected, tail-checked figure is ≤ 1e5 CPU-h. Then a cluster proposal (the owner's call).
- **Stop:** the lower bound is ≥ 1e6 CPU-h. Then drop brute force on (7,5,7)@27 too and turn to structure.
- **Otherwise:** inconclusive.
- No outcome proves anything about ES(7).

**Resources.**

- Stage 0: 1 thread, 1 GB.
- Stage 1: 4-6 threads for 8 h, 1 GB each, with memguard.
- Stage 2: up to 15 units for a night, only when the upper-bound jobs are off.

## 3. ES(8), and the adjacent k = 9 problem: five experiments

### E8-1. ABSAT8 sweep 2: further named 64-point families at radius 0

**Statement.** For each set S, ABSAT8_INDEPENDENT §2's theorem: for every realization of the labelled order type of S
and every point p in general position, there is a convex octagon through p.

**Targets.**

1. **`SYMEVEN/lit/smqh_crossed_k8_64points.txt`.** 64 points, centrally symmetric, largest convex subset 7, SHA-256
   `82ed0a5b…`. It was built by a crossed-labelling Lemma-14 blow-up of the 16-point Table 1 set of
   Subercaseaux–Mackey–Qian–Heule (SMQH) (SYMEVEN §6.2).
   - **First compare it with `c2_64points_k8_bb`,** which is already certified. ES8SYM §5 calls that file "this
     blow-up of the SMQH set", so the two may be the same order type.
   - Compare invariants first: the convex 4- and 7-gon counts. `c2_64points_k8_bb` has 841,636 convex 7-gons.
   - If they agree, compare the canonical chirotope under relabelling and reflection.
   - A crossed set on Mackey's base (SYMEVEN `lit/crossed_all_x_mackey.out`) would be a further target, if built.
2. **All 1,592 stacking order types** of `experiments/es8-lower-bound-search-2026-10-11`.
   - The 1,234 files in `family/sets/` cover 1,233 types.
   - The 359 types beyond sat.c's coordinate bound must be regenerated with `family/generate.py` (exact least-offset
     coordinates). **No record read here tests them**; the experiment README says they "remain untested".
   - The synthesis dropped "family-wide abstract saturation" at an estimated 60+ CPU-h. The measured cost is now about
     0.29 CPU-s per set (ABSAT0), so about 0.13 CPU-h for all 1,592.
   - Whether DDSZ Prop. 14 or Baek–Balko already cover these types must be checked in the papers before any value
     statement.
3. **The octagon-vertex deletions of the seven one-octagon 65-point sets** (`anneal/init_w8p_1-4`, `init_v8p_1-3`).
   - Deleting the added point returns witness(8)'s order type, which is already certified as `ot0000`.
   - Deleting one of the other 7 octagon vertices gives up to 7 new 64-point sets per near miss, at most 49 in all.
   - With ABSAT8's AE65 deletions, this closes the "move one point" neighbourhood of every recorded one-octagon
     65-point set.

**Encoding.**

- `l1enc` or `l1enc_big`, unchanged, at k = 8. V1 and V3 confirmed the encoder, the soundness proof and the
  certificates.
- Controls as in ABSAT8 §6: C2 and C3 on every set, C1 on a sample, and a C4-type control on the near misses with
  `--allow-kgon`.
- `l1check` reads at most 64-bit input, so the regenerated large-coordinate sets need a GMP variant of it for C2.

**Cost (HEURISTIC).**

- About 0.2 CPU-h of compute for about 1,650 sets at 0.29 CPU-s each, plus 0.5-1 CPU-h of controls.
- Agent time: regenerating the 359 representatives, and settling whether target 1 is a new order type.

**Outcomes.**

- **All UNSAT.** CERTIFIED + PROVED for these order types. That covers the whole stacking family at order-type level,
  including the 359 types with no recorded test, and one literature construction. Nothing about ES(8) = 65 beyond them.
- **Any SAT.** An abstract 65-element candidate; realizability is open.

**Resources.**

- 1 thread, 500 MB unit, ≤ 1 h wall.
- Each 64-point CNF is about 6 MB; ABSAT8's 28 CNFs took 179 MB. Keep the hashes and regenerate on demand.

### E8-2. CONE4 gate (4-fold, 14 layers)

**Statement: the gate (COMPUTED, at fixed phases).**

- Take 12 fixed t = 14 phase vectors φ: 8 LBK8SYM annealing optima and 4 random ones.
- At each φ, the CNF is encoder A (4, 8, 14) + Y(1,2) + chord + radius-cone units. Two variants: (a) root units only;
  (b) root units plus threshold chains.
- UNSAT at φ means that no 4-fold 56-point octagon-free set has phases φ.

**The line it gates.**

- An exact finite phase-arrangement CEGAR toward CERTIFIED "the largest 4-fold octagon-free set has 52 points".
- That would exclude 4-fold counterexamples to ES(8) = 65. ROT45CHORD closed 0 of 12 4-fold cubes in 14.9 h.

**Encoding and soundness.**

- LBK9OCT's cone and threshold families (`cone_rules.py`, `thr_rules2.py`; they take `m t`, the cone rules for even m)
  are ported to m = 4 through `lpcegar2.py`'s first SAT call.
- Direction: as at k = 9, a real configuration gives a model.
- But the k = 9 soundness note was written for m = 8 and carries ALGAN §1's floating-point caveats. A gate verdict is
  therefore evidence only.

**Steps.**

1. **Record the known negative.** ALGAN model 30 (sha `aee5ecf0…`) satisfies encoder A + chord + cone + cell(B ≤ 4)
   + binorder at (4, 8, 14). This is COMPUTED by the proposer's scripts; the base and cell counts were not re-run.
2. **Positive control.** Fix the empty-tuple bug in `posctrl.py`. Then run it on all 15 known 52-point sets, their
   mirrors and their subsets, at B = 2 and B = 4.
3. **The gate.** 24 calls, capped at 10 min each.

**Cost.** About 2 CPU-h (synthesis). The calls take 3-4 GB, so use a unit with MemoryMax 5G, RLIMIT_AS 4G and no swap.

**Outcomes.**

- **(a) is SAT at any vector:** park CONE4 and record why.
- **UNSAT at all 12:** build the exact abstraction.
  - A C++ int64 generator, with the Python generator kept as its checker.
  - A 2 CPU-h pilot, then a 30 CPU-h box.
  - The full line costs 60-200 CPU-h, with p ≈ 0.05-0.15 (synthesis).

### E8-3. Radius 1 at k = 8: sizing the joint two-point model around AE65

**Target statement.**

- No 65-point octagon-free set in general position contains a 63-subset with the order type of AE65 − {u, v}, for
  the pairs covered.
- AE65 has exactly one octagon, so only the pairs meeting it matter: C(65,2) − C(57,2) = 484 pairs.
- All 484 together would close the radius-1 ("move two points") neighbourhood of AE65, one of the eight recorded
  one-octagon 65-point sets.

**Encoding.**

- E7-2's model at k = 8, used only after it has been validated at k = 7.
- The two-point octagon family runs over the convex hexagons of the base; witness(8) alone has 5,252,469 of them. Full
  emission would be about 10^8 clauses.
- So add that family lazily (CEGAR on the current model), and certify the final CNF's UNSAT with cake_lpr.

**Sizing** (HEURISTIC, about 2 CPU-h).

- Bases: witness(8) at q = 37 (interior) and q = 0 (hull vertex), as the synthesis specified, plus one AE65 pair.
- Measure the CEGAR rounds, the final CNF size, the solve time and the LRAT size.
- The full run is 20-300 CPU-h (synthesis), and only after sizing.

**Outcome.** Sizing data only (HEURISTIC), plus a go/no-go for the 484-pair run.

**Resources.** 1 thread. Memory to be measured; the lazy family is meant to keep it under 4 GB.

**Dropped variant: enumerate-then-test.** N_0 ≥ 241,524 abstract extensions of witness(8) − 0, and the blocking
clauses would need 70-120 GB.

### E8-4. k = 9 ring "two displaced layers": the remaining 20 cyclic and 93 linear cases

**Statement** (once all 270 cases are certified, combined with Theorems 1 and 3-6).

- In every 8-fold rotationally symmetric 128-point set in general position with no convex 9-gon, the cyclic order of
  the 16 layer phases is not a spiral with at most two layers displaced.
- Context: the best known 8-fold set has 120 points. 128 is the PRIMEFOLD conjecture case at k = 9, which is adjacent
  to ES(8) but not part of it.

**Cases.**

- The exact list is `SATOPEN20261113/tools/k9/ring_cases.py`: 95 linear and 175 cyclic cases after Theorems 3-4.
- **Remaining cyclic cases (20):** `cycx_kK_p1` for K = 4..13 and `cycx_kK_p13` for K = 3..12. These cut the order at
  its very end. None of their folders had a cake_lpr verdict at 17:05.
- **Remaining linear cases (93):** `ex2_J_K`.

**Encoding.**

- **Base:** BASE0 = encoder A (8, 9, 16) + chord + cone + threshold-order + cell (B = 2) + bin-order. 497,712
  variables, 29,778,662 clauses, sha `b2a30933…`.
- **Each case adds unit clauses only:** 91 Y units per cyclic case, 78 per linear case.
- **Direction.** A real configuration gives, after the perturbation and reflection lemmas (SOUNDNESS.md §0 and §5), an
  intended assignment that satisfies BASE0 + units. So each UNSAT certifies its case.
  - It inherits LBK9OCT's unrefereed soundness and ALGAN §1's three floating-point steps (see S2).
- **Counting rules.**
  - A case counts only with `VERIFIED_LINES 1`.
  - `verify_cycx.py`, plus a linear analogue that still has to be written, checks the units and the hashes.
  - A completeness note derived from `ring_cases.py` is still owed (SATOPEN addendum).

**Cost (HEURISTIC).**

- **Cyclic cases.** Measured: 387-779 s at P = 2 and 12 (mean about 500 s), and about 360 s at P = 7. The time rises
  toward the ends of the order.
  - P = 1 and 13 are untimed. Assume 600-1,000 s, which gives about 3-6 CPU-h for the 20.
- **Linear cases.** Only the two central cases are timed (1,355 and 1,399 s). 93 × about 23 min ≈ 36 CPU-h; the
  extremes are untimed.
- **cake_lpr:** 80-114 s per case at heap 8,500, about 3 h for all 113.
- **Total:** about 40-45 CPU-h.
- **Disk.**
  - Raw LRAT is about 1.0-1.3 GB per cyclic case and about 2 GB per linear case, about 210 GB in transit.
  - The proofs are kept as zstd. Disk is fine: 685 GB were free at 17:08.

**Memory.**

- CaDiCaL takes about 3.9 GB per case, and cake_lpr about 8.8 GB resident.
- So the ring needs a 13.2 GB slice for 2 solvers, or for 1 solver + 1 checker (MEMB 13.2, as on 15 Nov at 02:37).
- That slice cannot sit beside the n66 track (17,000 MB) under the 24 GB total. Run the ring after the N66 campaign
  stops.
- At 2 solvers: about 20-25 h wall.

**First steps.**

- Pilot one P = 1 cyclic case and the two most extreme linear cases, to replace the extrapolations.
- Only then queue the rest with `sched.py` (`MAXJOBS=2 MEMB=13.2`).
- Run `check.sh` on every solved but unchecked folder before counting.

**Outcomes.**

- **All UNSAT.** The second ring is complete: CERTIFIED per case, on unrefereed soundness. The bulk of the 15!/2
  orders stays open, and nothing about 128 points follows.
- **A SAT case.** A candidate (phase order plus model) that must go through the exact pipeline (`cand2pts.py` +
  `exact_check.sh`). A real 128-point 8-fold set would settle the k = 9 symmetric case positively.

### E8-5. Two-arm one-descent pilot (k = 9); it runs inside E8-4's scheduler

**Target statement** (of the full line).

- After reflection, no 8-fold 128-point set without a convex 9-gon has a phase order ψ1..ψ15 with exactly one
  descent, at some a ∈ {4, …, 11}. Theorem 4 already removes a ≤ 3 and a ≥ 12.
- Label: CERTIFIED per cube, with a script-checked cover.
- This is the family of the 104- and 112-point records: spiral distance 4, two interleaved runs.

**Pilot** (COMPUTED, about 2 CPU-h).

- One unsplit cube each at a = 4 and a = 7, on BASE0 + the one-descent units.
- 1 h cap, no LRAT, inside the ring's scheduler and memory slice, never as a second scheduler.

**Then.**

- Continue only if a = 7 closes.
- Split the 8 cases by bin cubes: 25-400 CPU-h and 50-250 GB of zstd proofs (synthesis).
- Run S3 (label8.py) before writing anything up.

## 4. Side evidence tasks (not experiments)

These are cheap. They raise the trust in existing lower-bound statements; none of them is an experiment.

- **S1. Threefold split check.** A CNF-level check of Lemma 5 and Lemma H6M of the threefold split (AUDIT3 §5 row 9).
  - Cost: < 1 CPU-h at about 1.4 GB. Basis (roadmap map): C3LEAN's `indep_audit` streamed the threefold base in 21 s
    at 1.39 GB.
  - It closes the one named open check of Theorem 1, the weakest link of "no symmetric 33-point counterexample".
- **S2. Exact k = 9 floating-point steps.** Make the three steps exact: the `thr_rules2` bisection, `cell_thr.py` and
  encoder A's angle family (ALGAN §9.1's uniform-Farkas recipe). Then compare the regenerated clause files byte for
  byte with BASE0.
  - Cost: minutes if the files are identical, otherwise about 24 CPU-h of re-solves (roadmap map).
  - Needed before any k = 9 paper claim, and so before E8-4 or E8-5 is written up.
- **S3. label8.py.** Run it on `c8_104pts_13layers` and `c8_112pts_14layers`. This gives their run structure exactly,
  in Z[√2]. Minutes.
- **S4. Colouring-27 rings.** Re-run the phase-A rings through `certify_cnf.sh` into a work dir; the verifier's LRATs
  live in a scratchpad. Phase A stays COMPUTED until then. Low value, because the repair is dead.

## 5. Considered and not recommended (reasons from the records)

- **ES(7)@33 brute force, in any encoding:** about 1e3-1e4 CPU-years at the central reading (ES7_FEASIBILITY).
- **Heuristic 33-point searches.**
  - They have all failed: N2 (60 runs), annealing, AlphaEvolve.
  - 8,630 sets are abstractly saturated in the x-sorted model (COMPUTED).
  - Theorem A excludes the symmetric targets.
- **x-sorted mirror overlay `m33full`** (= record C's m33k7). It is C/C2's formula, which never closed.
- **Near-half-turn class C16+1.** One position already implies Theorem 4, which cost about 550-700 CPU-h (critic
  lower7:3).
- **Colouring-27 repair:** dead (the forced 5-cap is PROVED).
- **Bulk (7,6,6)@31 window sweep around mid30:** 0 SAT in 10,611 calls at r = 2-5, and the probe's rule forbids it.
- **Radius-1 enumerate-then-test at k = 8:** see E8-3.
- **`lpc8.py` on the 104 seed:** 104 + 8 = 112 is not the record size, and the 112 seed bottoms out at 1,344.
- **The k = 12 transfer:** floating point cannot sign the 991-point set.
- **The k = 9 bulk:** at least 4,100 CPU-h by the existing splits.
- **CONE4 bin bisection, and its S2 and S5 variants:** dropped by the ES(8) synthesis.
- **3-fold and 4-fold k = 8 construction templates:** 4-20 CPU-h, low odds.
- **ALGAN BFP-CEGAR:** stopped after 163 rounds.
- **The 5-fold odd-m cone port:** it needs a new written soundness argument. Consider it only after E8-2's gate.
- **The half-turn case at k = 8 (66 points):** it would cost far more than Theorem 4 did at k = 7.
- **N(9), the cluster tree:** it has no convergent route without a lookahead cuber, and installing march_cu needs the
  owner's OK.

## 6. Schedule under the house caps (16 threads, 24 GB)

- **Phase I: one evening, beside other work.** At most 2 threads and at most 6 GB.
  - Sequential: E8-1, then E7-1, in one 500 MB unit, 1 thread.
  - Then E8-2 in a 5 GB unit, and E7-3 at < 0.5 GB.
  - About 5-7 CPU-h in all.
  - Every CERTIFIED item gets a VERIFY step by a second agent with its own code, and its proofs are kept as zstd.
- **Phase II: about one agent-day plus at most 10 CPU-h.**
  - E7-2: the encoder, the soundness note, the controls and the k = 7 runs.
  - Then the E8-3 sizing.
  - The E7-4 encoder, its note and the calibration.
  - Each runs on 1 thread, at most 6 GB.
- **Phase III: when the n66 track's memory and at least 2 threads are free, for 1-3 nights.**
  - E8-4 (ring), with E8-5's pilot inside its scheduler. It needs the 13.2 GB slice.
  - E7-5 stages 0-1 (4-6 threads at 1 GB each).
  - The two can share a night: 2 + 6 threads and 13.2 + 6 GB, plus memguard. That is within the caps only if nothing
    else of size runs.
  - Stage 2 of E7-5 needs a dedicated night.
- **Before any public wording:** a literature check, because NOVELTY20261113B does not cover saturation.

## 7. Scoring (how the ranking was made; subjective, HEURISTIC)

**Value scale (subjective).**

| value | what it stands for |
|---|---|
| 10 | a real counterexample to ES(7) = 33 or ES(8) = 65 |
| 6 | a CERTIFIED exclusion of a whole symmetric class of counterexamples |
| 3 | an abstract counterexample candidate that still needs a realization, or a calibrated decision about a program of ≥ 1e4 CPU-h |
| 2 | a CERTIFIED statement for a natural family, or a complete case ring |
| 1 | CERTIFIED statements for a few named sets, a decision about a line of ≤ 300 CPU-h, or a validated new tool |
| 0.5 | sizing data, or weak negative evidence |

E is the expected value over the outcomes, and C the central CPU-h figure. Agent time is not counted.

| id | C | outcomes (P × value) | E | E / C |
|---|---|---|---|---|
| E8-1 | 1.5 | all UNSAT 0.97 × 2; SAT 0.03 × 3 | 2.03 | 1.35 |
| E7-1 | 1.5 | all UNSAT 0.98 × 1.8 (incl. the DDSZ check); SAT 0.02 × 3 | 1.82 | 1.21 |
| E8-2 | 2 | gate passes 0.3 × 1.6 (decision + option on a p ≈ 0.1, value-6 line); fails 0.7 × 1 | 1.18 | 0.59 |
| E7-4 | 3 | viable 0.4 × 1.5; not viable 0.6 × 0.8 | 1.08 | 0.36 |
| E8-5 | 2 | a = 7 closes 0.4 × 1; not 0.6 × 0.5 | 0.70 | 0.35 |
| E7-2 | 6 | all UNSAT 0.95 × 2 (radius-1 statements + tool); SAT 0.05 × 3 | 2.05 | 0.34 |
| E8-3 | 2 | sizing 0.5, plus option value 0.1 | 0.60 | 0.30 |
| E7-3 | 1.5 | 31-point hit 0.002 × 10; otherwise 0.3 | 0.32 | 0.21 |
| E8-4 | 42 | all UNSAT 0.98 × 2; SAT 0.02 × 4 | 2.04 | 0.05 |
| E7-5 | 40 (stages 0-1) | decisive 0.4 × 3; inconclusive 0.6 × 1 | 1.80 | 0.045 (stage 2 alone: E ≈ 1.5 at C ≈ 120, about 0.013) |

- The probabilities are guesses. Their bases:
  - every comparable test so far was UNSAT: Task A, A2, D2 and ABSAT8, with 0 SAT;
  - ES7_FEASIBILITY's priors straddle its go threshold;
  - the near-symmetric critic expected the near-mirror class to be slow.
- Changing any one probability by a factor of 2 does not change the top three; this was checked by hand on the table
  above. E8-4 and E7-5 stay at the bottom because
  of their cost, not their value.

## 8. Sources read, and what was not checked

**Read.**

- ROADMAP20261115: `README.md` (§3, §4, §6), `SYNTHESIS.md` (§2.3, §2.4, §3, §4), `ES7_FEASIBILITY.md`,
  `ABSAT8_INDEPENDENT.md`.
- STATUS20261115_1000, "Lower bounds" section.
- SATOPEN20261113, C.1-C.6 and the 15 November addendum.
- The work notes of `lower7/probe1`, `lower8/probe1` and `lower8/probe2`.
- `es7feas/` (sizes, times) and `es7feas-critic/` (the cad33 run).
- From `agent_results_roadmap.jsonl`: the four lower7 and four lower8 design programs, their critiques, the two
  roadmap maps quoted above and the lower8 synthesis.
- The ABSAT8 verdict files in `pm1115/claims/`. The other claims there concern Δ and the upper bound and were not
  used.
- Records consulted for facts and paths: A/README, ES7SPLIT, SYMZ, SYMEVEN §6.2, ES8SYM §5, AUDIT3 §5 row 1, and
  `experiments/es8-lower-bound-search-2026-10-11/README.md`.
- Live state, read-only: the ring's case folders, `systemctl --user list-units 'esr-*'`, `cpu_free.sh`, and
  `STATUS_campaign.md` of the N66 campaign.

**Not checked.**

- The afternoon Δ and upper-bound records. They do not bear on lower bounds, beyond the resource picture.
- Whether DDSZ Prop. 14 or Baek–Balko cover the 1,592 stacking types.
- Whether the SMQH crossed set and `c2_64points_k8_bb` are the same order type.
- The ETV 1996 implication for (7,6,6), which is recalled, not re-checked.
- The P = 1/13 and extreme linear ring timings, which are extrapolated.
- The two-point model's clause counts, which are estimates.
- Every cost figure is HEURISTIC, and no experiment here has been run.
