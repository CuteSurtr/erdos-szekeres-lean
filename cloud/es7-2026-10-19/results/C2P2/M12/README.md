# C2P2 M12 — shard j = 12 of N = 42 of C2P2.tsv, H = 2.5 h (TASK at d266d2c3)

Machine: 4 cores, 15 GB RAM (`env.txt`). Start 06:47:04Z, lane END 09:02:04Z (start + 2.5 h − 15 min).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (manifest: all 196 files match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch. Nothing cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF: `p cnf 838032 16653336`, sha256 base.cnf b0061e90…d8ff1 and base.json 2476faff…2b48 — both match.
- Cubes P1..P8 from `C2C34/l2cubes.py`: byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (8 rows: idx ≡ 12 mod 42)
| unit | case | kind | list cap | status | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|---|---|
| P8_3-13 | P8 | Q | 6000 | **certified** UNSAT | 3346.97 | 111.5 | 601.0 | 6 887 546 490 | 4415 |
| P6_1-3 | P6 | Q | 2400 | **certified** UNSAT | 857.96 | 68.3 | 374.9 | 4 099 853 801 | 4363 |
| P6_1-8-12 | P6 | H | 1800 | **certified** UNSAT | 503.87 | 59.1 | 335.5 | 3 570 768 517 | 4354 |
| P6_2-3-4 | P6 | H | 1800 (run at 1030) | **certified** UNSAT | 70.74 | 24.6 | 161.3 | 1 112 718 566 | 3099 |
| P6_2-10 | P6 | Q | 2400 (run at 769, END-limited) | UNKNOWN (timed out) | 760.04 | – | – | – | 4383 |
| P6_3-8-14 | P6 | H | 1800 | not reached | | | | | |
| P6_7-12 | P6 | Q | 2400 | not reached | | | | | |
| P6_9-11-13 | P6 | H | 1800 | not reached | | | | | |

Counts:
- Certified 4: P8 Q 1, P6 Q 1, P6 H 2.
- Timed out 1: P6 Q 1 (P6_2-10, cap reduced to 769 s by the lane's END rule, not its full 2400 s).
- Not reached 3: P6 Q 1, P6 H 2.
- Errors 0.

Certified units (min / median / max):
- solve: 70.74 / 680.9 / 3346.97 s
- lrat-check: 24.6 / 63.7 / 111.5 s
- cake_lpr: 161.3 / 355.2 / 601.0 s
- proof: 1.11 / 3.84 / 6.89 GB

The first-wave timeout P8_3-13 (cap 6000) is now certified, in 3347 s.

Largest solver RSS: 4415 MB (P8_3-13). No memory problem.

No SAT, no proof rejection, no `"certified": false` record, no ERROR status.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (5 records), `lane.log.tail`.
