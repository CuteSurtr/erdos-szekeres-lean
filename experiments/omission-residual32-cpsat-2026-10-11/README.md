# Residual 32-hole search with CP-SAT — 11 October 2026

This bounded search is **inconclusive**. It found neither a 32-hole assignment
nor a proof that none exists in the 2,650-row residual catalog.
**ES(8) ≤ 313 remains unproved. The completed planar bound is 314.**

The input is the unchanged [2,650-row search catalog](../omission-residual32-rank-global-2026-10-10/README.md),
with decompressed SHA-256
`e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6`. As in that
record, each hole variable marks a missing residual state, state zero is
occupied, and each row requires at least its stated number of holes. A
residual population of at most 121, and hence ES(8) ≤ 313 by the existing
partition, needs every assignment to have at least 33 holes.

## Results

| Probe | Outcome |
| --- | --- |
| LP relaxation (`lp.py`, HiGHS) | optimum 27 |
| CP-SAT minimization (`cpsat.py`), OR-Tools 9.15.6755, 12 workers, seed 1 | best assignment 33 holes after 7.7 s; lower bound 28 after 21 s; no further change until the run was interrupted at 2,988 s |
| Discovery around the saved one-row 32-hole near-model (`probe.py`, then `retry.py` for four timeouts) | 72 candidate supports of 11–16 states; all 72 satisfiable in the necessary coupled model; no new omission row |

The best CP-SAT assignment in [results.json](results.json) has 33 holes, leaves
state zero occupied, and satisfies all 2,650 rows under exact integer replay.
Such assignments were already known; they are Boolean countermodels, not point
configurations. The final status `FEASIBLE` with bound 28 decides nothing about
32 holes. The previous 600-second SAT and SCIP probes ended the same way.

The discovery probe uses the frozen rank-aware coupled model of the
[rank search](../omission-residual32-rank-search-2026-10-10/README.md). Its
input is the only saved candidate in
[feasible34-checked-near-models.json](../omission-residual32-primal-resume-2026-10-10/feasible34-checked-near-models.json)
that violates exactly one current row, row 973. The candidate supports are
unions of its tight faces, generated exactly as in the original probe. A
satisfiable support means only that the necessary abstract conditions have a
model there, so no row can be derived from it. Four supports timed out under
the original 12-second limit and were all satisfiable within 150 seconds.

## Interpretation

The gap between the LP bound 27 and the required 33 is large, and the 28 bound
did not move in fifty minutes. Deciding the 32-hole question by branching alone
appears out of reach at this scale. Progress toward 313 probably needs
geometric rows that strengthen the LP bound substantially, rather than further
generic solver time. Any eventual exclusion would still need an exact
certificate, its literal row binding, and the existing Lean transfer.

## Reproduction

From the repository root, with OR-Tools, HiGHS, NumPy and Z3 installed:

```sh
python3 experiments/omission-residual32-cpsat-2026-10-11/lp.py
python3 experiments/omission-residual32-cpsat-2026-10-11/cpsat.py 12 3600 .cache/es313/cpsat-sols.jsonl 1
PROBE_SECONDS=720 python3 experiments/omission-residual32-cpsat-2026-10-11/probe.py > .cache/es313/probe.log
python3 experiments/omission-residual32-cpsat-2026-10-11/retry.py .cache/es313/probe.log
```

CP-SAT is multithreaded and nondeterministic; other runs may follow different
paths. `probe.py` differs from its parent only in the source catalog, candidate
input, output directory and time limit. The catalog's attribution to Michael
Schroeder's version-1 archive is recorded in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md).
