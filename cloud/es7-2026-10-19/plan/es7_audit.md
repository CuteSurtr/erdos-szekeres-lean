AUDIT OF THE ES(7) AND ES(8) LOWER-BOUND SEARCHES (read-only; nothing modified, no process touched)

Compute used: about 2 s of single-core work. I ran `sat` on 4 of the 168 start sets, niced, writing only to the scratchpad. Everything else was reading files, logs and `ps`.

## 0. Headline findings

1. **The growth search only explores near the witness.** All 168 start sets in `.cache/es7/grow/starts_K7_a.txt` come from witness(7).
   - Provenance (recovered from this session's transcript, because the generator script was not kept): the first 400 rows of `.cache/es7/trackA/data/distinct_K7.txt` with max |coord| < 2^24, each with one random point removed (rng seed 7).
   - Only 168 rows pass that filter: 94 from A7w (random walks starting at witness(7)) and 74 from A7sv (stacking variants).
   - None of the 3,111 A7r sets or 1,461 A7n sets (annealing from random starts) passed. 90% of those have coordinates of about 2^25.6 to 2^26.
   - So the search is one-point relocations of witness-derived 32-point sets. This is the region where Baek–Balko's theorem and blow-up experiments make a counterexample least likely (see section 4).
2. **The cube-and-conquer is not converging, and its progress numbers are artifacts.**
   - run33: all open cubes share a 47-literal prefix. Every cube literal is an auxiliary cap/cup flag; none is an orientation variable.
   - The closed-weight metric is frozen by float64 rounding.
   - run33m3's "75%" is one weight-0.25 cube that the scheduler has starved (details in section 2).
3. **The symmetric "not realized" results tell us nothing.** Our realizers realized 0/30 of the 4-fold and 0/30 of the 5-fold hexagon-free 16-point models. Published work finds a sizeable share of these classes realizable.
4. **Saturation is tested per realization, not per order type.** The ES(7) README wording "8,537 distinct order types … saturated" overstates what was tested.

## 1. Realizable growth search (`.cache/es7/grow/grow.py`, `run_grow.sh`, `grow-*.log`, `old-logs/`)

**What it covers.**
- For each 31-point start set S, the program `sat` (trackA/bin/sat, same as ES8 `saturation/sat.c`) lists the faces where a 32nd point adds no convex 7-gon ("extension faces").
- `grow` takes at most ⌊3·4000/168⌋ = 71 random faces per set. That gives up to 11,928 children, of which 4,000 are kept at random.
- Each child T is tested exactly over all faces of its own arrangement for a 33rd point.
- The 31-point level is deterministic: every seed logs the identical top-10 counts [11718, 10975, …, 9823].

**How much was actually done.**
- Current logs: 4 instances × 10 completed seeds = 40 seeds × 4,000 = **160,000 tests of 32-point sets**, not 168,000. Every one had 0 extension faces.
- Partial seeds: 341, 501 (no output) and 761–764 (running now; ps shows 4 grow.py processes).
- `old-logs/`: 69 seed starts, none reached n=32. All crashed with "FATAL: coordinate bound 2^27 exceeded".

**How much of the space that is.**
- The face total over the 168 sets is not logged. The top ten are 9,823–11,718 (sum 105,018).
- My random sample of 4 start sets (indices 30, 81, 128, 131) had only 510, 60, 902 and 712 extension faces.
- So the neighbourhood is roughly 0.2M faces (order-of-magnitude estimate, n=4 sample).
- Coverage after 40 seeds:
  - For a 10k-face set, the per-seed chance of testing a given face is about 71/10,000 × 0.335. After 40 seeds that is about 9% coverage.
  - Sets with < 71 faces are re-tested in full every seed, so they are tested dozens of times.
- The same (S, face) always gives the same 32-point set. So **distinct sets tested are materially fewer than 160,000** (number unknown), and new seeds add less and less.

**Further bias.**
- `explicit_point` silently drops faces whose vertex lies beyond 2^24 (LIMIT/4). These are faces near infinity, which matter for exponentially spread constructions. The number dropped is not logged.
- Only depth 1 is explored: 31 → 32 → 33. One of the 32-point children is the original saturated set put back.

## 2. Cube-and-conquer (`.cache/es7/cnc/cnc.py`, `worker.cpp`, `run33/`, `run33m3/`)

The code is identical to `experiments/es7-search-2026-10-13/cnc/`. Both runs were started with `BASE_LIMIT=100000 GROW=1.0` (read from `ps eww`).

**run33** (n33k7hm: signotope with hull + mirror symmetry breaking; 47,002 vars, 679,535 clauses)
- Totals: 3,313 closed, 149 open, 6,774 jobs, 3,461 splits, no SAT.
- About 14.8 h of active compute, estimated from log intervals ≤ 120 s. The log's t-clock (606,626 s) includes pauses; there are 51 gaps over 5 minutes. The README's "17 hours" also counts paused time.
- Open cube depth: min 89, median 138, max 264 (10th–90th percentile 96–211). Every budget is 100,000.
- Trajectory: open count 125 → 204 → 149; max depth 167 → 337 → 264. There is no downward trend.
- Closed/jobs = 0.49, and the prefix trie has 1,217 internal nodes but only 148 branching nodes. Almost every split closes one child within 100k conflicts while the other carries on. The frontier behaves like about 150 long chains growing one level per two jobs.
- All open cubes share the same first 47 literals.
- **Every cube literal is an auxiliary chain flag.** The decoded literals are capV r=6, cupV r=4/6, with chain start points 1–4. Not one of the 5,456 orientation variables appears.
  - A positive flag literal can be set even when the chain does not exist, so the two branches overlap in configuration space.
  - The README's statement that open cubes "partition the unrefuted part of the space" holds for assignments, not for configurations.
- **The weight metric is broken.** closed_weight = 0.9999999999999991, while open weight = 6.1e-27. The sum misses 1 by 9e-16, which is 11 orders of magnitude more than all the open weight. The metric has been flat at 1 − 8.9e-16 since about 1.3 active hours, so no completion fraction can be read from it.

**run33m3** (3-fold, 11 orbits, auxiliary centre; 463,980 vars, 9.5M clauses)
- 501 closed, 34 open, 1,035 jobs, about 3.9 active hours on 2 workers.
- The "75% closed" is **one depth-2 cube [4, 554] of weight 0.25**. It was open at t≈9.4 h, before the restart at about 121.8 h, and it was never split during the roughly 1,000 jobs since.
  - This fits LIFO starvation in `take()`: a worker always pops its newest (deepest) cube and only steals when its own queue is empty. Resumed cubes go to the bottom of a queue.
- The other open cubes reach depth 160, all on orientation-orbit variables (≤ 2002).
- So 3-fold progress is about 4 hours of real work, plus two earlier 2-hour CaDiCaL runs (`experiments/es7-search-2026-10-13/symmetric/runs-summary.txt`).

**Other run33/run33m3 issues**
- GROW=1.0, so budgets never grow.
- On resume, the stored per-cube limits override BASE_LIMIT: m3 cubes stay at 50,000 although the environment says 100,000.
- No proof logs are kept, so a finish would only be a solver claim.

## 3. Other searches

**Saturation pool** (`experiments/es7-search-2026-10-13/saturation/final_summary.txt`, `diversity7.txt`)
- 8,537 sets: 1,656 witness-derived (A7w 701, A7w2e 700, A7sv 81, A7sv2 174) and 6,881 annealed (A7r/r2a/r2b/n/n2c/n2d).
- One realization per order type was tested.
- Hull sizes 3–6; c6 (convex-hexagon counts) about 8.5k–49k.

**Abstract one-point extension (signotope) tests** (`.cache/es7/trackB-sat/logs/ext_*.log`, swap_walk logs)
- witness(7): all 33 positions UNSAT, LRAT-verified.
- Also tested: c16 (20 sets, 340 positions), c32 (6 sets), sat32_a (1 set), and 56 realized 32-point sets from the swap walks. All UNSAT.
- This is the only test that goes beyond a single realization, and it covers fewer than 100 sets.

**Symmetric searches**
- Results: 32-point 2-fold SAT (45 models), 32-point 4-fold SAT (n32k7m4, not mentioned in the README), 33-point 11-fold UNSAT.
- Realization attempts: 2-fold 32-point 0/40 + 0/5; 4-fold 16-point 0/30; 5-fold 16-point (centre in set) 0/30 (`.cache/es7/symmetric/localizer/logs/`). `.cache/es7/trackB-sat/realize.c` did realize 10/26 non-symmetric 16-point models (`trackB-sat/logs/sample16_realize.log`).
- For comparison, Subercaseaux–Mackey–Qian–Heule (arXiv:2506.00224, HTML checked) report:
  - 5-fold 16-point: 948 assignments, 92 realizable. Getting 0/30 at that rate has probability about 4%.
  - 4-fold 16-point: 18 realizable, but the paper gives both 6 and 66 solutions, so this comparison is unconfirmed.
- **Conclusion: our realizers fail on extremal configurations,** which need coordinates spread over about 2^17. They succeed on generic chirotopes: calibration A realized 25/25 random symmetric 32-point chirotopes in a median 0.11 s.

**ES(8)** (`experiments/es8-lower-bound-search-2026-10-11/README.md`)
- 1,233 saturated order types come from 4,128 sampled trees out of about 1.2×10^21 labelled trees, so they are not the whole family. 359 order types above the coordinate bound are untested.
- Every one is decomposable. Baek–Balko Thm 8 (as cited in `docs/RELATED_WORK_2026-10-14.md`) already rules out decomposable counterexamples, though not their one-point extensions.
- Again one realization per order type was tested.

## 4. Blind spots, ranked by how much they could matter

1. **No search targets non-decomposable, non-blow-up structure.** Per our survey (not re-verified here), Baek–Balko show decomposable sets satisfy the conjecture, and their blow-up optimiser never beat 2^(k−2) up to k=20. Our growth search (168/168 witness-derived) and the ES(8) family both sit in exactly that region. Nobody has checked whether the 6,881 annealed 32-point sets are decomposable or blow-ups. A cheap structural classification would show whether any non-blow-up extremal sets exist to grow from.
2. **No complete small-case enumeration.**
   - K=5, 8 points: trivial from Aichholzer's order-type database (n ≤ 11).
   - K=6, 16 points: AllSAT on n16k6hm, then realization and classification as decomposable, blow-up or other, plus layer profiles.
   - Smaller maximal sets: Damásdi–Dong–Scheucher–Zeng (per our survey) say saturated sets of 7/8·2^(n−2) points exist.
   - The number of hexagon-free 16-point signotopes is unknown (unconfirmed), so a pilot is needed. This is the most direct way to learn the structure of extremal sets before guessing at K=7.
3. **The cube-and-conquer is the wrong tool for finding a counterexample.**
   - Any SAT model is abstract. Krapivin–Przybocki–Heule (arXiv:2607.02958, HTML checked) generated 200,000 abstract 32-point no-7-gon solutions in 2,191 core hours and realized none.
   - Showing UNSAT would mean proving ES(7)=33, a major open problem, and the frontier shows no convergence.
   - Options:
     - Re-purpose the 6 cores to realizability-guided search: PointSAT-style unit feedback from a realizer, at 33 points or from realized 32-point sets.
     - Or, if aiming at UNSAT, rebuild properly: orientation-only cubing, budgets that grow, FIFO or breadth-balanced scheduling, proof logging, and symmetry breaking over the choice of hull vertex.
4. **Realizer weakness on extremal sets** (section 3) makes every "not realized" verdict uninformative. Never tried:
   - log-scale or hierarchical coordinates;
   - fixed exponential abscissae with an LP in y (Koshelev–Koshka, arXiv:2604.20120, per our survey, not re-verified: 37.7% vs 8.5% of 10-point signotopes realized);
   - Subercaseaux et al.'s Localizer itself.
5. **Saturation was tested per realization.** All 8,537 + 160k + 1,234 tests are coordinate-specific; only the signotope test (< 100 sets) is stronger. Running that test (33 CaDiCaL calls, most finishing in about 0 s per the logs) on all 8,537 pool sets would strengthen the record cheaply. The test is still relative to one x-order, not fully order-type level (my reasoning, unconfirmed).
6. **Symmetry classes never tried at 33 points.**
   - Mirror (axial) symmetry: 16 pairs plus one point on the axis.
   - Dihedral D3, as a stronger restriction of the 3-fold run.
   - "Almost symmetric" sets: 3-fold on 30 points plus 3 free points.
   - Note: m=2, 4, 8, 16 with a centre are impossible (centre collinear with antipodal points), and m ≥ 7 gives a convex 7-gon, so 3-fold really is the only rotational class at 33.
7. **Growth mechanics.** Only depth-1 relocation; duplicate re-sampling; the 2^24 filter; faces near infinity dropped. Fixes:
   - deduplicate by order type;
   - exhaust each set's faces instead of re-sampling;
   - rescale the annealed sets into the coordinate bound;
   - try k=2–4 point deletions;
   - try bottom-up growth from small random sets.
8. **ES(8) family completeness** (359 untested order types, unknown family size). Low value for the ES(7) goal.

## 5. Bugs and doubtful assumptions

- **B1 (cnc.py):** float64 closed_weight is numerically frozen; run33's "fraction closed" is meaningless.
- **B2 (cnc.py `take`):** LIFO per-worker queues starve shallow cubes. run33m3's [4, 554] (0.25 of the weight) has sat untouched since ≤ t=9.4 h.
- **B3:** GROW=1.0 means budgets never grow, and BASE_LIMIT is ignored on resume.
- **B4:** CaDiCaL lookahead splits only on auxiliary flag variables. Positive-flag branches overlap in configuration space.
- **B5 (ES(7) README):** "8,537 distinct order types … saturated" should say one realization per order type. The ES(8) README itself says saturation depends on coordinates.
- **B6:** "About 168,000 tested" is really 160,000 tests (40 seeds) with many exact duplicates.
- **B7 (`.cache/es7/symmetric/localizer/run_batch.py`):** `realized_and_verified` also requires the set to be heptagon-free, so calibration A prints 0/25 although 25/25 were realized.
- **B8 (`.cache/es7/night-thaw.sh`):** the PIDs after `taskpolicy -B -p 81538` are on separate lines, so each runs as a command and only 81538 gets the background policy. The script is stale, so this is harmless now.
- **B9:** README wall-time figures for run33 include paused periods.
- **B10:** the ES(8) README header still says ES(8) ≤ 314; current is 311.
- **B11:** faces near infinity are dropped silently in `grow.py` `explicit_point`.
- **Checked and sound (no defect found):**
  - Hull and mirror symmetry breaking in `gen_cnf.py`, including the projective map and the single lex-leader clause.
  - The cap/cup K-gon encoding.
  - Uniformity of the 3-fold auxiliary centre: the centre can always be moved off collinearities by rotating one orbit slightly.
  - The ES(7) encoding is validated by ES(6)=17 with an LRAT check.

## Files

- Growth search: `.cache/es7/grow/grow.py`, `grow-{1..4}.log`, `old-logs/`, `starts_K7_a.txt`; start-set source `.cache/es7/trackA/data/distinct_K7.txt`.
- Cube-and-conquer: `.cache/es7/cnc/cnc.py`, `run33/state.json`, `run33/cnc.log`, `run33m3/state.json`, `run33m3/cnc.log`.
- Symmetric: `.cache/es7/symmetric/localizer/logs/calib.log`, `models_p1.log`, `.cache/es7/symmetric/cnf/n33k7m3.json`.
- Abstract extension tests: `.cache/es7/trackB-sat/logs/ext_*.log`, `swap_walk*.log`.
- My scratch scripts (no repo writes): `scratchpad/` (`starts.py`, `src.py`, `cubes.py`, `cubes2.py`, `varmap.py`, `s31_*.txt`).