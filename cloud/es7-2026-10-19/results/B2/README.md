# Task B2: ETV ladder at k = 7 in the signotope model (cloud run, 20 Oct 2026)

DRAFT: written during the run. Final numbers are filled in at the end (see "Status at end of run").

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

## 3. Main instances

PLACEHOLDER: filled in at the end.

## 4. Models, gluing, realization

PLACEHOLDER.
