# C2P4 M17

Task `results/C2P4/TASK.md` (commit a46b478d) with V = M17, LIST = C2P4.tsv, j = 17, N = 50, H = 2.5.
Start 2026-10-31 13:01:27 UTC (epoch 1793451687), END = 1793459787 (15:16:27 UTC). Machine: 4 cores, 15 GB RAM (`env.txt`).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: the manifest matched (196 files). CaDiCaL 3.0.1, cake_lpr and lrat-check (E2 patch) built from the vendored sources. Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both rejected the bad LRAT and both accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The sha256 of base.cnf (b0061e90…) and base.json (2476faff…) both match.
- Cubes: P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, 14 rows with idx ≡ 17 mod 50)

| unit | case | kind | cap | result |
|---|---|---|---|---|
| P5_1-7 | P5 | Q | 6000 | **certified** UNSAT (solve 4086.3 s) |
| P5_9-13 | P5 | Q | 2380 (shortened by END) | **certified** UNSAT (solve 1288.1 s) |
| P4_6-10 | P4 | Q | 561 (shortened by END) | UNKNOWN (timed out at 555 s) |
| 11 others | | | | not reached |

Counts by case and kind:
- Certified: 2, both P5 Q (this closes both P5 units on this shard).
- Timed out (UNKNOWN): 1, P4 Q (P4_6-10). Its cap was only 561 s instead of 6000 s because END was near, so it is still open.
- Not reached: 11.
  - P4 H: 5 (P4_1-5-15, P4_1-11-14, P4_2-8-13, P4_5-10-16, P4_7-8-10).
  - P3 Q: 1 (P3_4-12).
  - P3 H: 5 (P3_1-4-13, P3_1-9-12, P3_4-6-14, P3_5-6-8, P3_6-7-12).
- Errors: none. Every record with a proof has `certified: true`.

Certified units (n = 2; min / median / max):
- solve: 1288.1 / 2687.2 / 4086.3 s
- lrat-check: 79.7 / 108.4 / 137.1 s
- cake_lpr: 425.8 / 557.8 / 689.8 s (heap 8000 MB)
- proof size: 4.48 / 6.21 / 7.94 GB (4483373629 and 7936340786 bytes)

Largest solver RSS: 4421 MB (P5_1-7).

No SAT. No proof was rejected. No memory or disk problems: peak usage was about 8 GB RAM during cake_lpr, and at least 20 GB of disk stayed free.
