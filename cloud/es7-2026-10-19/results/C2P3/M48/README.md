# C2P3 M48: shard j = 48 of N = 50 of `lists/C2P3.tsv`

Task: `results/C2P3/TASK.md` at commit 4f653319, with V = M48, LIST = C2P3.tsv, j = 48, N = 50, H = 2.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 09:42:42Z (epoch 1793439762), END 1793447862 (11:57:42Z).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc, E2 patch) from the vendored `tools-src.tar.xz`. The manifest check passed for all 196 files. No code was cloned or downloaded.
- Sanity: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, sha256 b0061e90…d8ff1 (base.cnf) and 2476faff…bf472b48 (base.json). Both match.
- Cubes: `l2cubes.py` output for P1..P8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (9 rows, idx ≡ 48 mod 50)
| idx | unit | case | kind | cap | result |
|---|---|---|---|---|---|
| 48 | P6_7-15 | P6 | Q | 6000 | **certified** (solve 4782.19 s) |
| 98 | P6_2-10-16 | P6 | H | 1800 (run at 1610) | **certified** (solve 472.47 s) |
| 148 | P6_7-10-14 | P6 | H | 1800 (run at 724) | **certified** (solve 214.38 s) |
| 198, 248, 298, 348, 398, 448 | P5_1-2-12, P5_1-8-13, P5_2-6-9, P5_2-12-14, P5_6-11-14, P5_8-9-12 | P5 | H | 1800 | not reached (lane stopped with 732 s left before END) |

Counts by case and kind:
- certified: P6 Q 1, P6 H 2;
- timed out (UNKNOWN): 0;
- errors: 0;
- not reached: P5 H 6.

The lane capped the two H units below 1800 s because of the time left before END. Both still finished well inside those caps.

## Certified units (3)
| | min | median | max |
|---|---|---|---|
| solve s | 214.38 | 472.47 | 4782.19 |
| lrat-check s | 56.7 | 59.8 | 144.3 |
| cake_lpr s | 311.4 | 339.0 | 772.0 |
| proof size | 3.09 GB | 3.53 GB | 8.85 GB |

All three were checked by cake_lpr with an 8000 MB heap; no retry was needed.

## Other
- Largest solver RSS: 4405.04 MB (P6_2-10-16). The largest RSS of any process seen, cake_lpr, was about 8.2 GB.
- No SAT, no proof rejection and no memory or disk problem. Peak disk use was about 9 GB for the P6_7-15 proof, with 22 GB free.
- Files: `out.jsonl` (records), `lane.log.tail`, `units.tsv`, `run.sh`, `tools.txt`, `env.txt`.
