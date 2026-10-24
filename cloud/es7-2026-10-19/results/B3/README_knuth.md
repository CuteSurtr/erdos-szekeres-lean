# B3 (one of several concurrent B3 sessions): (7,5,7)@27 with march_cu lookahead cubes

Instance: Erdős–Tuza–Valtr rung (a, u, k) = (7,5,7) on 27 points, i.e. an x-sorted signotope on 27
points with no 5-cap, no 7-cup, no convex 7-gon (conjectured impossible; 26 is the conjectured
maximum). **Status: UNKNOWN. Not solved, no model found, nothing certified.**

Several B3 sessions wrote to this folder at the same time on identical 4-core VMs. This file
covers the session whose log is `progress.md` and whose files are `hard102/`, `lrat/`,
`es6_calib/`, `samples_d30.txt`, `samples_d24.txt`, `samples_d18.txt`, `probe*.log`, and
`scripts/{icube.cpp,descend.sh,sample_node.sh,estimate.py,probe.sh,applycube.py}`. Files under
`logs/` and `run2/`, and `scripts/{iworker.cpp,twolevel.py,project.py,...}`, belong to the other
sessions.

## Where it ran
Cloud VM `vm`: Linux 6.18 x86_64, **4 cores, 15 GB RAM**, no swap (`env.txt`). Wall time used was
00:29–04:15 UTC on 20 Oct 2026. For the whole run, 1 core ran the Kissat baseline and 3 cores ran
cubing and conquering.

Tools, built from source (HEAD of each repo on 20 Oct 2026):
- CaDiCaL;
- Kissat;
- drat-trim with lrat-check;
- `march_cu` from marijnheule/CnC (its Makefile needs `-fcommon` with current gcc);
- Baek–Balko `erdos-szekeres-sat`, `etv_signotope` mode, run through `results/B/scripts/bb_emit.py`.

The conquer worker is `scripts/icube.cpp`, an iCaDiCaL-style worker: one incremental CaDiCaL per
worker that solves its shard of the cubes as assumptions, keeps learned clauses across cubes, and
applies a wall-clock cap per cube.

Main CNF: `gen_etv.py 27 5 7 7` plus `lexx.py` (the x-reflection lex-leader), giving 21,533 vars
and 265,448 clauses (2,925 orientation variables). The CNF itself is not committed.

## Controls (`controls.json`, `controls.log`)
Both encoders were run, each with and without the lex-leader. CaDiCaL solved them, and sigcheckB
brute-force checked every SAT model.

| instance | expected | ours | Baek–Balko | ours+lexx | BB+lexx |
|---|---|---|---|---|---|
| (7,4,7)@16 | SAT | SAT 0.02 s | SAT 0.02 s | SAT 0.02 s | SAT 0.01 s |
| (7,4,7)@17 | UNSAT | UNSAT 1.4 s | UNSAT 1.2 s | UNSAT 1.2 s | UNSAT 0.95 s |
| (7,5,7)@26 (positive control) | SAT | SAT 0.24 s | SAT 0.17 s | SAT 0.23 s | SAT 0.21 s |
| (6,5,6)@16 = ES(6) | UNSAT | UNSAT 126.8 s | UNSAT 111.8 s | UNSAT 105.8 s | UNSAT 73.4 s |

All encodings agree, and every model passed the brute-force check.

The glue pipeline was tested on the (7,5,7)@26 control models (ours+lexx and BB+lexx). `glue.py 757`
put a 6-cap deep below each model, giving 32-element signotopes. sigcheckB found no convex 7-gon
(by both tests), max cap 6, max cup 6, and no signotope violations.

`realize.py` (ins-ff, lp, free; 150 CPU s) did **not** realize the 26-point control model: at
best 211 triples were violated. This proves nothing; KPH report a realization rate of about 1.6e-4
at this size.

## Cubing and conquering (7,5,7)@27
1. **Plain march_cu cubes are far too hard at practical depths.**
   - `march_cu -d 8` gave 256 cubes in 18 s; `-d 12` gave 4,096 cubes in 578 s. In both cases
     lookahead refuted **0** leaves.
   - Every sampled depth-12 cube and depth-20 cube took more than 120 s with CaDiCaL.
   - Lookahead pruning starts only around depth 30–48.
2. **Knuth estimator by random descent.** `descend.sh` and `sample_node.sh` run `march_cu -d 6`
   per step, pick a uniformly random cube (Python RNG), and then solve the node with plain CaDiCaL.
   The estimate for each sample is (product of surviving-cube counts) × (node time). Timeouts are
   counted at the cap, so every mean below is a lower bound.

   | cutoff depth | samples | timeouts | node time median / mean | estimated total, plain CaDiCaL at that cutoff |
   |---|---|---|---|---|
   | 18 | 5 | 2 (300 s cap; the other 3 ran with a 1500 s cap and solved in 186, 508, 1220 s) | 300 s / ≥ 503 s | **≥ 1.3e8 s ≈ 3.7e4 core-h** (±4.9e7 s, 1 s.e.; n = 5) |
   | 24 | 57 | 3 (300–400 s cap) | 13 s / ≥ 53 s | **≥ 8.9e8 s ≈ 2.5e5 core-h** (±2.1e8 s, 1 s.e.) |
   | 30 | 12 | 2 (300 s cap) | 0.44 s / ≥ 50 s | ≥ 5.4e10 s ≈ 1.5e7 core-h (±3.6e10 s) |

   - At depths 6–24, every one of the 57+ paths had all 64 of 64 cubes surviving at every level
     (product 64^4 = 1.7e7 at depth 24).
   - Node times are heavy-tailed: at depth 24, p25 = 3.9 s, p75 = 45 s, p90 = 171 s.
   - The deeper cutoff costs more in total: the estimate rises from depth 18 to 24 to 30.
     Splitting further only multiplies the cube count (×64 per 6 levels, with no pruning)
     faster than the per-cube time falls. CDCL inside one node does much better than
     lookahead splitting here. `estimate_output.txt` has the numbers.
3. **Full CnC of one hard depth-30 node** (seed 102; it timed out at 300 s as a single job;
   `hard102/`).
   - `march_cu -d 10` gave 945 cubes plus 28 refuted leaves, in 336 s.
   - 3 incremental workers with a 600 s cap per cube ran for 72 min of wall time.
   - Result: **931 UNSAT, 14 cubes still open after 600 s each, 0 SAT.**
   - Summed cube time is ≥ 12,611 s. UNSAT cube times: median 0.43 s, p90 5.7 s, p99 61 s,
     max 487 s.
   - Solved-over-time is in `hard102/progress.txt`: 231 cubes after 60 s, 495 after 26 min, 918
     after 56 min, all 945 attempted after 72 min.
   - So this node was **not** closed, and it is one of about 1e9 depth-30 nodes. An easy depth-30
     node (seed 7) closed in 2.65 s: 109 cubes plus 73 refuted leaves.
4. **Calibration on ES(6)**, (6,5,6)@16 + lexx, where monolithic CaDiCaL takes 106 s:
   - `march_cu -d 8` CnC: 271 s of conquer time.
   - Default dynamic `march_cu`: 27,173 cubes, 694 s of cubing plus 1,208 s of conquer.
   - So lookahead CnC cost 2.6–18× the monolithic CPU time on the solvable sibling instance.
5. **Baseline: plain Kissat**, one core, whole instance with lexx. It ran from 00:42 to 04:06 UTC
   (12,218 s) with no answer, and was killed.
6. **LRAT spot-check** (`lrat/summary.txt`).
   - 4 cubes of node 102, at the 20th/50th/80th/95th percentile of solve time, were checked with
     `cadical --lrat` and lrat-check against the node CNF plus the cube units. All 4 gave
     `c VERIFIED`; proofs were 0.4–17 MB, checked in 0.1–0.3 s.
   - Negative test: the same proof checked against the CNF with one cube unit removed is rejected.
   - Only these 4 cubes were checked. **Nothing is certified.**

**Correction during the run.** The first `probe.sh` used `shuf --random-source=<(yes SEED)`, which
always picks line 63 of 64. So `probe_757_seed1.log`, `probe2.log`, `probe3.log` and
`probe_es6_seed1.log` all follow **one deterministic path** (it happens to be a hard one); they are
not random samples. Their `est_nodes` columns are not Knuth estimates. Use the `samples_*.txt`
files instead.

## Models
None. No cube or node returned SAT, so nothing went to brute-force checking, gluing or
realization beyond the controls above.

## Projection and assessment
- **Best estimate.** Proving (7,5,7)@27 UNSAT with this encoding (ours + x-reflection
  lex-leader), march_cu cubing and plain CaDiCaL costs about **4e4 to 2.5e5 core-hours**
  (roughly 4 to 30 core-years).
  - The low end is the depth-18 Knuth estimate: ≥ 3.7e4 core-h, from only 5 samples, 2 of them
    censored at 300 s.
  - The high end is the depth-24 estimate: ≥ 2.5e5 core-h from 57 samples.
  - Every figure is a censored lower bound for its cutoff, and tails are heavy. One hard depth-30
    node alone has ≥ 12,600 s with 14 cubes still open.
  - Cutting shallower than 18 (nodes of 20 min or more) might be cheaper still. It was not
    measured, because a single sample needs more than an hour.
  - An independent B3 session's two-level projection on the same VM type, in
    `logs/projection_interim.json`, gave about 1.7e5 core-h (95% CI 1.0e5–2.4e5). That is inside
    this range.
- **Not laptop-tractable.** On 4 cores this is about 1 to 7 years.
- **Cluster-tractable, at the scale of the large published SAT proofs.**
  - 4e4 core-h is about the Pythagorean triples problem (about 3.5e4 CPU-h) and twice the empty
    hexagon proof.
  - 2.5e5 core-h is above Schur number five (about 1.2e5 CPU-h).
  - Either is far beyond KPH's 23-point theorem (1,727 core-h).
- **Before anyone spends cluster time:**
  - Run a proper pilot at cutoff depth 12–18 with many more samples and longer caps.
  - Add stronger symmetry breaking: march's lookahead refutes nothing in the first 24 levels.
  - Add the cardinality lemmas from plan #1 (A/B-tested on ES(6)).
  - Use proof-producing conquer, since only 4 cubes were LRAT-checked here.
- **The positive direction is cheap to test:** (7,5,7)@26 solves in 0.2 s. But a model at 27
  would still be only an abstract signotope until it is realized.
