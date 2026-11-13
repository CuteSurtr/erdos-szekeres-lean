# C3W3S / S0: σ-cube closure of mirror-kept two-orbit s = 1 roots (shard j = 0 of N = 12)

**Result: 18 of my 26 roots closed (9 directly, 9 at σ level 1, none needed level 2); 8 skipped because C machines had reached them. Nothing open. No SAT. No proof rejection. No memory problem.**

Task: `results/C3W3S/TASK.md` at 5f9d1dba, V = S0, j = 0, N = 12, H = 4.0. Run 06:03:57 to 07:58:30 UTC on 2026-10-21 (the root list ran out before the budget did).

## Tools and base check (`tools.txt`)

One VM, 4 cores, 15 GB RAM (`env.txt`). C3-S tools from a worktree of 132398c, unmodified; `sigma_cubes.py` copied from `results/C3PLAN/scripts` unmodified (cmp identical). CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (example: `s VERIFIED UNSAT`), lrat-check 2e3b2dc + E2 patch (sanity: `3 0 0` rejected by both checkers, `3 0 1 2 0` accepted by both). Base CNF `gen_case.py 11 7 none`: `p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da` (matches).

## Roots

The 301 rows of `results/C3W3/lists/C_s1two.tsv` with `h6m_kept` = yes, by decreasing row, positions ≡ 0 (mod 12): 26 roots (`roots.tsv`). Driver: `driver.py` (+ `refine.py` for level 2, which was never needed). The skip check (after `git pull`) ran before each batch of 3 roots. Direct attempts ran 3 in parallel (`close_node.py`, cap 300 s). Each root not closed directly then got `sigma_cubes.py … R 3 300 3`.

## Per root

| row | root | stratum | result | direct solve s | σ cubes | solve s | check s |
|---|---|---|---|---|---|---|---|
| 300 | 0s0-5s1_7s1-9s1 | H6(5,1)/two | closed directly | 67.7 (UNSATISFIABLE) | 0/0 certified | 68 | 41 |
| 288 | 0s0-5s1_6s1-7s0 | H6(5,1)/two | closed at σ level 1 | 300.1 (UNKNOWN) | 8/8 certified | 1820 | 378 |
| 276 | 0s0-5s1_2s1-8s1 | H6(5,1)/two | closed at σ level 1 | 300.1 (UNKNOWN) | 8/8 certified | 1036 | 277 |
| 264 | 0s0-5s1_2s0-8s0 | H6(5,1)/two | closed at σ level 1 | 300.1 (UNKNOWN) | 8/8 certified | 751 | 289 |
| 252 | 0s0-5s1_1s1-8s0 | H6(5,1)/two | closed directly | 63.5 (UNSATISFIABLE) | 0/0 certified | 64 | 43 |
| 240 | 0s0-5s1_1s0-9s1 | H6(5,1)/two | closed directly | 93.1 (UNSATISFIABLE) | 0/0 certified | 93 | 29 |
| 228 | 0s0-5s1_1s0-2s1 | H6(5,1)/two | closed at σ level 1 | 300.1 (UNKNOWN) | 8/8 certified | 1438 | 296 |
| 216 | 0s0-4s1_6s0-9s1 | H6(4,1)/two | closed at σ level 1 | 300.1 (UNKNOWN) | 8/8 certified | 1597 | 292 |
| 204 | 0s0-4s1_5s1-10s1 | H6(4,1)/two | closed at σ level 1 | 300.1 (UNKNOWN) | 8/8 certified | 996 | 306 |
| 192 | 0s0-4s1_2s0-9s0 | H6(4,1)/two | closed at σ level 1 | 300.1 (UNKNOWN) | 8/8 certified | 980 | 283 |
| 180 | 0s0-4s1_1s1-9s0 | H6(4,1)/two | closed directly | 60.5 (UNSATISFIABLE) | 0/0 certified | 60 | 34 |
| 168 | 0s0-4s1_1s1-10s1 | H6(4,1)/two | closed at σ level 1 | 300.1 (UNKNOWN) | 8/8 certified | 2062 | 314 |
| 156 | 0s0-4s1_1s0-3s0 | H6(4,1)/two | closed directly | 41.0 (UNSATISFIABLE) | 0/0 certified | 41 | 25 |
| 144 | 0s0-3s1_5s1-9s1 | H6(3,1)/two | closed directly | 242.5 (UNSATISFIABLE) | 0/0 certified | 242 | 41 |
| 132 | 0s0-3s1_5s0-7s0 | H6(3,1)/two | closed directly | 43.9 (UNSATISFIABLE) | 0/0 certified | 44 | 35 |
| 120 | 0s0-3s1_4s1-5s0 | H6(3,1)/two | closed at σ level 1 | 300.1 (UNKNOWN) | 8/8 certified | 1990 | 331 |
| 108 | 0s0-3s1_4s0-10s1 | H6(3,1)/two | closed directly | 161.2 (UNSATISFIABLE) | 0/0 certified | 161 | 34 |
| 96 | 0s0-3s1_1s1-4s1 | H6(3,1)/two | closed directly | 98.8 (UNSATISFIABLE) | 0/0 certified | 99 | 36 |
| 84 | 0s0-3s1_1s0-4s1 | H6(3,1)/two | skipped (record 0s0-3s1_1s0-4s1 in C3W3/C12/out.jsonl) | – | – | – | – |
| 72 | 0s0-2s1_5s0-8s1 | H6(2,1)/two | skipped (record 0s0-2s1_5s0-8s1 in C3W3/C0/out.jsonl) | – | – | – | – |
| 60 | 0s0-2s1_4s1-5s0 | H6(2,1)/two | skipped (record 0s0-2s1_4s1-5s0 in C3W3/C6/out.jsonl) | – | – | – | – |
| 48 | 0s0-2s1_3s1-7s1 | H6(2,1)/two | skipped (record 0s0-2s1_3s1-7s1 in C3W3/C12/out.jsonl) | – | – | – | – |
| 36 | 0s0-2s1_3s0-4s1 | H6(2,1)/two | skipped (record 0s0-2s1_3s0-4s1 in C3W3/C0/out.jsonl) | – | – | – | – |
| 24 | 0s0-2s1_5s1-6s0 | H6(2,1)/two | skipped (record 0s0-2s1_5s1-6s0_8s0-9s0 in C3W3/C6/out.jsonl) | – | – | – | – |
| 12 | 0s0-1s1_5s0-6s1 | H6(1,1)/two | skipped (record 0s0-1s1_5s0-6s1_2s0-3s0 in C3W3/C12/out.jsonl) | – | – | – | – |
| 0 | 0s0-1s1_2s0-5s1 | H6(1,1)/two | skipped (record 0s0-1s1_2s0-5s1_4s1-8s1 in C3W3/C0/out.jsonl) | – | – | – | – |

Solve and check seconds are per-node sums (3 jobs share 4 cores, so they are not wall-clock). For σ-closed roots the total includes the 300 s direct timeout.

## Totals

- 26 roots: 9 closed directly, 9 closed at σ level 1 (72 cubes, all certified), 0 at σ level 2, 0 open, 8 skipped (`skips.log`: records already present in `results/C3W3/C0`, `C6`, `C12`). Rows 108 and above were all done here. Rows 84 and below were skipped.
- Records: `out_direct.jsonl` has 18 records: 9 UNSAT certified and 9 UNKNOWN at 300 s. `out_sigma.jsonl` has 72 records, all UNSAT and certified (`c VERIFIED` + `s VERIFIED UNSAT`).
- Solve time 13,542 s, check time 3,086 s (summed).
- No SAT, no `PROOF NOT ACCEPTED`, no rechecks (no `recheck.jsonl`), no memory problem (peak use about 3 GB of 15).

## Files

`env.txt`, `tools.txt`, `roots.tsv`, `driver.py`, `refine.py`, `out_direct.jsonl`, `out_sigma.jsonl`, `skips.log`, `driver.log.tail`, `README.md`.
