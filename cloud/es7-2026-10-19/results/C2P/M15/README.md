# C2P M15 (LIST = C2P.tsv, j = 15, N = 42, H = 3.0, TASK.md at 01909a07)

Restart of M15. The earlier attempt (TASK.md at fb2c59af) stopped at step 1, and its files were replaced. Start 03:23:18Z (epoch 1793416998). END = 06:08:18Z (1793426898). The lane finished at 05:58:57Z ("stop: 560 s left").

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built the tools from the vendored sources only, and all 196 manifest files matched:
  - CaDiCaL c6073042 (3.0.1);
  - cake_lpr a36874a8;
  - lrat-check from drat-trim 2e3b2dc, with the E2 patch.
- Sanity checks: the cake_lpr example printed `s VERIFIED UNSAT`. Both checkers rejected the bad LRAT and accepted the good one.
- Base CNF: the header is `p cnf 838032 16653336`, and the sha256 of base.cnf (b0061e90…) and of base.json (2476ffaf…) both match.
- Cubes: for each of P1..P8 the output is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, `out.jsonl`, `lane.log.tail`, `run.sh`)
53 units (idx ≡ 15 mod 42), none of them cover units: certified 8, timed out (UNKNOWN) 2, not reached 43, errors 0.

| case | H certified | H not reached | Q certified | Q UNKNOWN | Q not reached |
|---|---|---|---|---|---|
| P8 | 3 | 0 | 1 | 1 (P8_3-10, 2382.7 s at cap 2400) | 0 |
| P7 | 4 | 2 | 0 | 1 (P7_3-11, 2380.1 s at cap 2400) | 0 |
| P6 | 0 | 5 | 0 | 0 | 2 |
| P5 | 0 | 6 | 0 | 0 | 1 |
| P4 | 0 | 6 | 0 | 0 | 1 |
| P3 | 0 | 6 | 0 | 0 | 1 |
| P2 | 0 | 6 | 0 | 0 | 1 |
| P1 | 0 | 4 | 0 | 0 | 2 |

Certified units: P8_1-15 (Q), P8_1-14-16, P8_1-9-11, P8_9-10-11, P7_2-5-12, P7_8-11-12, P7_8-13-14 and P7_1-4-8 (all H). The last of these, P7_1-4-8, ran with a reduced cap of 551 s and finished in 253.5 s.

Over the 8 certified units (min / median / max):
- solve: 22.1 / 217.8 / 965.8 s;
- lrat-check: 11.4 / 46.2 / 65.5 s;
- cake_lpr: 101.6 / 271.9 / 379.5 s, all at heap 8000 MB with no retry;
- proof size: 0.214 / 3.247 / 4.512 GB. Every proof was deleted after checking.

The largest solver RSS was 4384 MB (P7_3-11). The machine has 15 GB.

No SAT. No proof rejection, no `"certified": false` record, no ERROR status and no memory problem.
