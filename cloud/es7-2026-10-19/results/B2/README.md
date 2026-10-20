# Task B2: ETV ladder at k = 7 in the signotope model (cloud run, 20 Oct 2026)

Bottom line: no model, no closed cube in the breadth-first runs, no UNSAT claim for either rung.
The controls pass (except (6,6,6)@17, still open) and so does an end-to-end LRAT-checked pipeline control.
Knuth probes give tree-size ranges: (7,5,6)@26 looks feasible (about 10^2 to 10^3 core-hours);
(7,5,7)@27 looks infeasible with this pipeline (about 10^4 to 10^6 core-hours).

## Where it ran

`env.txt`: Linux VM `vm`, kernel 6.18.44, x86_64, **4 cores, 15 GB RAM**, start 2026-10-20
00:21 UTC. Everything below ran in this cloud session, on those 4 cores.

## Conventions

The triple is (k, a, u) = (gon size, cap bound, cup bound), which is Baek–Balko's (n, a, b).
N(k, a, u) = largest signotope with no a-cap, no u-cup and no convex k-gon. ETV's conjectured
value is f(k,a,u) = sum_{i=k-u}^{a-2} C(k-2, i). Orientation variable X(i,j,k), i<j<k, numbered
1..C(N,3) in lexicographic order; true = counterclockwise = cup triple. Ours (`tools/etv/gen_etv.py`)
and Baek–Balko's `etv_signotope` (`scripts/bb_emit.py`, imported from
github.com/jcpaik/erdos-szekeres-sat `lib/erdos.py`) share this numbering and polarity, so cubes
and models transfer between the two. f is symmetric in (a, u), and the y-reflection swaps caps
with cups, so (7,5,7) and (7,7,5) are the same instance.

Symmetry breaking in all main runs: the x-reflection lex-leader (`scripts/lexx.py`), which is
valid for every ETV instance.

## Tools built

- CaDiCaL (github.com/arminbiere/cadical, master, `-O3`); drat-trim and `lrat-check`
  (github.com/marijnheule/drat-trim); Baek–Balko's encoder (github.com/jcpaik/erdos-szekeres-sat).
- Reused from `results/B/scripts` without changes: `cnc2.py` (cube-and-conquer: one global
  queue ordered shallowest-first, then FIFO; exact `Fraction` weights 2^-depth; splits only on
  orientation variables 1..C(N,3); LRAT lane), `cncw.cpp` (incremental CaDiCaL worker),
  `controls.py`, `bb_emit.py`, `lexx.py`, `cover.py` (offline replay of the cube tree),
  `glue.py`, `sigcheckB.c` (brute-force checker), `knuth.py`, `lrat_leaves.py`.
- New: `lrat_rest.py` (LRAT-checks the closed cubes that the cnc2 LRAT lane did not reach
  before the run ended), `summarize.py`.

## 1. Encoder controls (`logs/controls.log`)

Each control is solved four ways: ours, Baek–Balko, ours + lex-leader, Baek–Balko + lex-leader,
with plain CaDiCaL. Every SAT model is brute-force checked by `sigcheckB` (signotope axioms on
all 4-subsets, no a-cap, no u-cup, no k-gon by two independent convexity tests).

- **46 of the 47 required controls pass, with all four variants agreeing and all models
  checked:** every k = 5 and k = 6 rung (SAT at f, UNSAT at f+1) except (6,6,6)@17;
  (7,4,7)@16 SAT and @17 UNSAT; positive controls (7,5,6)@25, (7,5,7)@26, (7,6,6)@30 SAT.
- **(6,6,6)@17 (the ES(6) = 17 analogue) did not finish.** Plain CaDiCaL on our encoding ran
  about 28 minutes (cap 30 min) and Baek–Balko's about 4 minutes before I stopped it to free the core;
  no result was recorded for either. A 10-minute cube-and-conquer attempt (1 worker) closed no
  cube. This control is open.

## 2. Cube-and-conquer pipeline control: (6,5,6)@16 (`logs/k6a5u6N16/`)

A known UNSAT rung, run through exactly the pipeline used for the main instances (cnc2.py, base
budget 20,000 conflicts, growth 1.25 per depth, 1 worker):
- all cubes closed in about 3 minutes: 43 jobs, 21 splits, **22 closed leaves**, exact closed
  weight **1/1**;
- `cover.py` replays the event log from the root: every event hits an open leaf, every split
  literal is an orientation variable, the leaves partition the space (sum 2^-d = 1 exactly) and
  match the saved state;
- **all 22 leaf cubes were re-solved from scratch with `cadical --lrat` and VERIFIED by
  `lrat-check`** (15 by the cnc2 lane, 7 by `lrat_rest.py`), and all 22 are also UNSAT on the
  Baek–Balko CNF with the same lex-leader.
So (6,5,6)@16 is a certified UNSAT of our CNF (with lex-leader). It is a pipeline check, not a new result.

## 3. Main instances (`logs/k7a5u7N27/`, `logs/k7a5u6N26/`)

Setup: our CNF plus the x-reflection lex-leader. (7,5,7)@27 has 21,533 variables and 265,448
clauses (2,925 orientation variables). (7,5,6)@26 has 17,128 variables and 214,030 clauses
(2,600 orientation variables). `cnc2.py` ran with base budget 20,000 conflicts and growth 1.25
per depth. (7,5,7)@27 had 2 workers, (7,5,6)@26 had 1. The LRAT lane sampled closed cubes at
rate 0.05 and cross-checked each sampled cube on the Baek–Balko CNF. Both runs started at
00:34 UTC. **A container restart killed every process at about 03:36 UTC**, about 15 minutes
before the planned 03:50 stop. `cnc2.py` cannot resume, so the runs ended there, after about
3 h 2 min. Both event logs replay cleanly with `cover.py`: every event hits an open leaf, every
split is on an orientation variable, and the leaves partition the space exactly. For 757 the
open set in the last saved `state.json` is a few events behind the log, because the kill came
between saves. The event log is authoritative.

Every 30 minutes (from `report30.jsonl`; the closed weight was exactly 0/1 throughout):

| min | (7,5,7)@27 open | depth histogram | (7,5,6)@26 open | depth histogram |
|---|---|---|---|---|
| 30 | 81 | 6:47, 7:34 | 58 | 5:6, 6:52 |
| 60 | 138 | 7:118, 8:20 | 91 | 6:37, 7:54 |
| 90 | 184 | 7:72, 8:112 | 125 | 6:3, 7:122 |
| 120 | 232 | 7:24, 8:208 | 152 | 7:104, 8:48 |
| 150 | 274 | 8:238, 9:36 | 176 | 7:80, 8:96 |
| 180 | 312 | 8:200, 9:112 | 201 | 7:55, 8:146 |
| end | 316 | 8:196, 9:120 | 203 | 7:53, 8:150 |

- (7,5,7)@27: 315 jobs, all splits, **0 closed cubes, closed weight exactly 0**, about 6.1
  worker-hours.
- (7,5,6)@26: 202 jobs, all splits, **0 closed cubes, closed weight exactly 0**, about 3.0
  worker-hours.
- Because no main-run cube closed, the cnc2 LRAT lane never fired on these runs.
  **Neither rung has an UNSAT claim of any kind.**

**Tree size: Knuth probes** (`logs/knuth/`). `knuth.py` uses the same worker and split
heuristic, with a fixed budget of 20,000 conflicts per node, and follows a random child down
to a closed leaf. It ran on the 4th core: (7,5,7)@27 from 01:13 to 03:00, then (7,5,6)@26 from
03:00 to 03:36. Every probe ended in a closed leaf (none censored, none SAT). Costs are wall
seconds of one dedicated worker process (4 processes on 4 cores), about 12–15 s per node,
mostly the split lookahead.

| instance | probes | leaf depths | nodes (median; min–max) | core-hours: median; mean; bootstrap 90% of mean; min–max |
|---|---|---|---|---|
| (7,5,6)@26 | 11 | 12–20 | 6.6e4; 8.2e3–2.1e6 | 201; 1,117; 336–2,000; 23–5,082 |
| (7,5,7)@27 | 17 | 16–28 | 1.7e7; 1.3e5–5.4e8 | 62,610; 205,458; 59,166–372,863; 636–1,575,593 |

Probe leaf cubes were re-solved from scratch with `cadical --lrat` and checked with
`lrat-check` (`logs/knuth/lrat_leaves.jsonl`). Every leaf checked was VERIFIED and was also
UNSAT on the Baek–Balko CNF. This only shows that the leaves the probes reach are genuinely
refutable, and cheaply so (5–20 s, 8–22 MB proofs).

**Convergence assessment (honest).**
- The breadth-first runs show **no convergence**: open counts rise steadily, and the frontier
  is still at depth 8–9, while the probes say leaves close only at depth 12–20 (7,5,6) or 16–28
  (7,5,7). With shallowest-first order and budgets growing ×1.25 per level, nothing will close
  until the frontier reaches those depths.
- Knuth estimates are unbiased but heavy-tailed, and they understate the true mean when the
  rare deep branches are not sampled. Treat them as ranges:
  - **(7,5,6)@26: roughly 10^2 to 10^4 core-hours** with this exact pipeline. That is feasible
    on a few dozen cores in a day or two, and consistent with Schroeder's (unreviewed) claim
    N(7,5,6) = 25 being reachable.
  - **(7,5,7)@27: roughly 10^4 to 10^6+ core-hours.** Not feasible with this pipeline without
    much better splitting, cheaper nodes (the lookahead dominates node cost), or proved
    lemmas. This agrees with the critique's warning based on KPH's large solution space at 26.
- Neither estimate is a certified bound on anything.

## 4. Models, gluing, realization

- **No SAT model was found at (7,5,6)@26 or (7,5,7)@27** (no SAT cube in the C&C runs, no SAT
  probe), so there is nothing to glue or realize.
- The glue and check chain was validated on the positive-control models: the (7,5,7)@26,
  (7,5,6)@25 and (7,6,6)@30 models each pass `sigcheckB`. `glue.py` turns each into a
  32-element signotope, which passes `sigcheckB` with k = 7 (signotope axioms, no convex
  7-gon). At the conjectured maximum, 32 is the expected size; a rung-beating model would give
  33.
- Realizer check: `tools/realizer/run_models.py --signotope` on the (7,5,7)@26 control model
  (120 CPU-s, methods ins-ff and lp) did **not** realize it (`logs/realizer_ctl757_26.json`).
  At KPH's rate of about 1.6e-4 realizable abstract solutions at this size this is expected,
  and proves nothing. The realizer's positive calibration is in `results/F`.

## What remains

1. (6,6,6)@17 control: run both encoders to completion (plain CaDiCaL took more than 30 min on
   1 core; cube-and-conquer or a longer run is needed).
2. (7,5,6)@26 looks within reach: about 10^2–10^4 core-hours by the probes. Use a
   depth-first or budget-adaptive C&C, or start from a fixed depth-12 to 14 cube split, on
   many cores, with LRAT on every leaf (leaves check in seconds). Resume support in `cnc2.py`
   (load `state.json`) is needed, since this session lost its runs to a container restart.
3. (7,5,7)@27 needs a better method before compute is spent: cheaper split selection (the
   full-lookahead over about 2,900 variables dominates the 15 s nodes), cardinality lemmas
   (with proofs), or the critique's realizable-anchored experiments.
4. The UNSAT answers here are claims about one CNF. Even a fully closed, all-LRAT run is only
   "LRAT-checked UNSAT of this encoding, cross-validated against Baek–Balko", not a theorem.

## Files

- `env.txt`: execution environment.
- `scripts/`: everything used (see "Tools built").
- `logs/controls.log`: per-control results (46 records).
- `logs/<instance>/`:
  - `progress.jsonl` (every 60 s);
  - `report30.jsonl` (every 30 min: open count, depth histogram, exact closed weight);
  - `events.jsonl.gz`, `state.json.gz`, `cover.json`, `lrat.jsonl`, `final.json` (when the run
    finished).
- `logs/knuth/`: probe logs and LRAT checks of probe leaves.
- `summary.json`: output of `scripts/summarize.py`.
- No CNF or proof files are committed.
