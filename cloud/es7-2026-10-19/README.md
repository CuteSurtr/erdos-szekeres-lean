# ES(7) > 33 search: cloud bundle, 19 October 2026

Inputs and tools for searching for 33 points in general position with no 7 in convex
position (which would show ES(7) > 33 and disprove the Erdős–Szekeres conjecture at
n = 7), or for rigorous partial results if none exists. Nothing here is a claimed result.
The research behind these tasks is in [plan/](plan/): `es7_plan.md` (ranked plan),
`es7_critique.md` (skeptical review, read it first), `es7_audit.md`, `es7_structure.md`,
`es7_methods.md`.

## Contents

- `inputs/distinct_K7*.txt` — 8,537 realizable heptagon-free 32-point sets. One per line:
  `label hash 32 x1 y1 ... x32 y32` (integers up to about 6.7e7; 1,492 sets repeat an
  x-coordinate, so rotate or perturb before x-sorting into a signotope).
- `inputs/nearfull_p2c.txt`, `inputs/nearfull_p2d.txt` — near-miss seeds (sets with one
  convex heptagon); `inputs/starts_K7_a.txt` — 168 heptagon-free 31-point sets derived from
  the classical construction; `inputs/alphaevolve_pts.json` — AlphaEvolve's 33-point set
  (exactly one convex 7-gon by our exact recount).
- `tools/trackB/` — signotope CNF generator `gen_cnf.py` (variables X(i,j,k), i<j<k, in
  lexicographic order; true = counterclockwise), one-point extension encoder `ext_cnf.py`,
  `sigcheck.py`, exact checker `brute_kgon.c`, realizer `realize.c`.
- `tools/trackA/` — exact C tools: `sat.c` (saturation test over all arrangement faces),
  `gen*.c`/`gen_core.h` (annealing), `cgon.c` (convex k-gon count), `verify.c`.
- `tools/etv/gen_etv.py` — Erdős–Tuza–Valtr encoder (no a-cap, no u-cup, no k-gon; options
  `--mirror`, `--hull`); `tools/etv/mircheck.py` — mirror-encoding validator.
- `tools/cnc/` — cube-and-conquer driver and CaDiCaL worker. Known bugs (see the critique):
  newest-first popping and float progress weights.
- `tools/decomp/` — decomposability and mirror checks, and published 16-point sets.

Build CaDiCaL and drat-trim from source in the cloud
(https://github.com/arminbiere/cadical, https://github.com/marijnheule/drat-trim).
Baek–Balko's encoder is at https://github.com/jcpaik/erdos-szekeres-sat (mode
`etv_signotope`), useful as an independent cross-check.

## Rules for any run

- Report only what the logs show. A SAT model of an abstract encoding is a signotope, not
  a point set, until realized with exact rational coordinates and re-checked by brute
  force. An UNSAT answer is a claim about one CNF; "certified" needs an LRAT check, and a
  theorem needs a verified encoding.
- Every encoder must pass positive and negative controls before its answers are used.
- Commit results under `cloud/es7-2026-10-19/results/<task>/` on this branch only, never
  on `main`, with no AI co-author or attribution trailers.
