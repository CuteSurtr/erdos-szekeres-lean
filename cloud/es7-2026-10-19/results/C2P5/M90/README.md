# C2P5 M90: C2P5B.tsv shard 40 of 50 (idx ≡ 40 mod 50), H = 5.25

Task `results/C2P5/TASK.md` at commit 81cb025f. The lane started at 15:26:47Z (session start 15:24:30Z, END = 1793478270 = 20:24:30Z) and finished all units at 18:58:30Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: all 196 manifest files match. It built CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8) and lrat-check (2e3b2dc + E2 patch) from the vendored sources. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one. The cake_lpr example gives `s VERIFIED UNSAT`.
- Base CNF: `p cnf 838032 16653336`. Both sha256 values match (base.cnf b0061e90…d8ff1, base.json 2476faff…2b48).
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (18): all certified
| case | Q certified | H certified |
|---|---|---|
| P1 | 1 (P1_4-13) | 4 |
| P2 | 1 (P2_6-7) | 6 |
| P3 | 1 (P3_1-9) | 5 |
| total | 3 | 15 |

- Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0. `certified: false`: 0.
- Every proof: lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`.

### Certified units (min / median / max)
- solve: 20.1 / 191.9 / 2211.0 s
  - Q: 402.0 / 1921.3 / 2211.0 s
  - H: 20.1 / 107.3 / 550.2 s
- lrat-check: 11.8 / 49.7 / 96.9 s
- cake_lpr: 106.5 / 289.0 / 487.3 s
- proof size: 0.215 / 3.19 / 5.66 GB

The largest solver RSS was 4418 MB (P1_3-10-12).

There were no SAT results, no proof rejections and no memory problems. Disk headroom stayed at 22 GB or more.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (18 records), `lane.log.tail`, `status.txt`.
