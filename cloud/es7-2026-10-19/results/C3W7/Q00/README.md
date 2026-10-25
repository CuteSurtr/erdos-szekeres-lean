# C3W7 / Q00: nine-bit σ-cubes of the H3/one roots, shard 0 of 36 of `W7.tsv`

**Result: of my 54 units, 3 were certified, 45 timed out at 900 s and 6 were not reached (3 of those were
started and then killed at END). No SAT, no proof rejection, no memory problem, and no unit ended early.**
That is far below the C3H1/X1 pilot, where all 8 nine-bit cubes of one six-bit cube closed in 450–662 s.

## Setup

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 2026-10-25 10:46:11 UTC, END 15:01:11 UTC
(start + 4.5 h − 15 min). Task `results/C3W7/TASK.md` at 39bb1bac. Details are in `tools.txt`.

- Tools: worktree of cad4e050 at `/opt/c3u2`, TOOLS = `.../results/C3U2/tools`, used unmodified. `compose.py` was not run.
- CaDiCaL 3.0.1 c60730422e; cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`); lrat-check 2e3b2dc0 with the E2 patch.
  Sanity test on {1},{-1}: `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`, which matches.
- Units: the rows of `lists/W7.tsv` with row ≡ 0 (mod 36), 54 of them (`units.tsv`). There were 3 lanes (`lane0.sh`–`lane2.sh`,
  `setsid nohup`), and lane k took positions ≡ k (mod 3). Each unit ran
  `close_tree.py base.cnf out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02`.
  No records were seeded.
- At END the three lane process groups were killed. They were running the units at positions 48, 49 and 50, which started
  14:48–14:50 UTC; those killed solves left no records.

## Per unit

The full table is in `units_result.tsv`: position, lane, row, node, result, solve s and check s.

| unit (row) | node | solve s | check s |
|---|---|---|---|
| 0 | `0s0_1__2s0-3s0-4s0-5s0-6s0-7s0-8s0-9s0-10s0` | 738.0 | 112.4 |
| 288 | `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0-8s0-9s0-10s0` | 880.0 | 97.2 |
| 576 | `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0-8s0-9s0-10s0` | 755.5 | 96.0 |

These are the certified units. Each one has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

The other 45 reached units all ended `UNKNOWN` at 900 s (solve_s 900.1–900.3). Each got its layer-split record of 45
children, which were left unsolved and appear in `open_frontier`, as intended. No unit was unsplittable.
The 6 units not reached are positions 48–53 (rows 1728, 1764, 1800, 1836, 1872 and 1908, all under `0s0_4`).

## Totals

| root | units | certified | timed out | not reached |
|---|---|---|---|---|
| 0s0_1 | 15 | 2 | 13 | 0 |
| 0s0_2 | 14 | 1 | 13 | 0 |
| 0s0_3 | 14 | 0 | 14 | 0 |
| 0s0_4 | 11 | 0 | 5 | 6 |
| total | 54 | 3 | 45 | 6 |

Per parent six-bit cube: each of my 54 units has a different parent, so this machine holds 1 of the 8 nine-bit cubes
of 54 parents. Three parents have all their units on this machine certified (1 of 1 each):
`0s0_1__2s0-3s0-4s0-5s0-6s0-7s0`, `0s0_1__2s1-3s0-4s0-5s1-6s0-7s0` and `0s0_2__1s0-3s0-4s1-5s0-6s0-7s0`.
None of these parents is closed by this machine alone. Of the other parents, 45 have a unit that timed out and 6 a unit
that was not reached; the per-unit table gives the parent of each.

Solve times of the 3 certified units: min 738.0, Q1 746.8, median 755.5, Q3 817.8, p90 855.1, max 880.0 s.
All 3 were certified above 300 s. Check times were 96.0–112.4 s.

All of my units have bits 9 and 10 equal to 0 (row ≡ 0 mod 36 gives row ≡ 0 or 4 mod 8). All 3 certified units also
have 8s0.

## SAT, rejections, memory, early ends

- SAT: none.
- PROOF NOT ACCEPTED: none. No certified-looking record has cake_lpr `none`, so `recheck.jsonl` was not needed.
- Memory: about 13 GB was available throughout, with 3 lanes and `--jobs 1` each.
- No unit ended in under 72 s without a certificate.
- Every solve ran with 3 concurrent CaDiCaL jobs on 4 cores. That may explain part of the gap to the pilot times.
