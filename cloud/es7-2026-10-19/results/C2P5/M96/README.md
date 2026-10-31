# C2P5 M96 — list C2P5B.tsv, shard j = 46 of N = 50, H = 5.25 h (TASK.md at 81cb025f)

Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 15:13Z (epoch 1793459589), END = 1793477589 (20:13:09Z). The lane finished all units at 19:13:02Z.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built from the vendored `tools-src.tar.xz` (manifest: all 196 files match); nothing cloned or downloaded.
- CaDiCaL 3.0.1; cake_lpr example `s VERIFIED UNSAT`; bad LRAT rejected by lrat-check and cake_lpr, good LRAT accepted by both.
- Base CNF header `p cnf 838032 16653336`; base.cnf sha256 b0061e90…d8ff1 and base.json sha256 2476faff…bf472b48, both as expected.
- Cubes P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (18 = idx ≡ 46 mod 50)
| case | kind | units | certified | UNKNOWN | not reached | errors |
|---|---|---|---|---|---|---|
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 4 | 4 | 0 | 0 | 0 |
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **all** | | **18** | **18** | 0 | 0 | 0 |

All 18 are UNSATISFIABLE and certified: both lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`) accepted each proof.
- Q: P2_6-13 (1636.5 s solve), P1_5-10 (879.0 s), P3_1-15 (1537.4 s).
- H: P2_1-6-8, P2_3-6-7, P2_3-10-15, P2_4-8-9, P2_5-8-9, P2_7-8-12, P1_2-6-14, P1_3-4-13, P1_3-12-13, P1_5-6-13, P3_1-2-10, P3_1-8-10, P3_4-5-15, P3_4-11-14, P3_5-11-13.

Certified units (min / median / max):
- solve: 19.5 / 299.1 / 1636.5 s
- lrat-check: 13.3 / 56.2 / 85.3 s
- cake_lpr: 113.2 / 322.1 / 482.8 s
- proof size: 0.215 / 3.28 / 4.97 GB (214756591 / 3277063438.5 / 4966201382 bytes)

The largest solver RSS was 4476.7 MB (P2_6-13).

No SAT, no proof rejections, no errors, and no memory or disk problems (available memory stayed ≥ 6 GB and free disk ≥ 23 GB).
Files: `out.jsonl` (per-unit records), `lane.log.tail`, `units.tsv`, `run.sh`, `tools.txt`, `env.txt`.
