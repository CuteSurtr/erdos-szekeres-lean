# C2P5 M07: shard 7 of 37 of C2P5A.tsv

Values: V = M07, LIST = C2P5A.tsv, j = 7, N = 37, H = 4.5, Z = 81cb025f (TASK.md).
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 18:16:42Z (epoch 1793470602), END = 1793485902 (22:31:42Z).
The lane ran from 18:18:39Z to 19:14:36Z and finished all its units long before END.

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored `tools-src.tar.xz` only. Nothing was cloned or downloaded.
  All 196 manifest hashes match. The sources are CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, and lrat-check 2e3b2dc with the E2 patch.
- Sanity: both checkers reject the bad LRAT and accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. The base.cnf and base.json sha256 both match the expected values.
- Cubes: `l2cubes.py` output for a = 1..8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, `out.jsonl`)
Rows of C2P5A.tsv with idx ≡ 7 (mod 37): idx 7, 44, 81, 118.

| unit | case | kind | cap s | status | solve s | RSS MB | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|---|---|---|---|---|
| P4_2-8 | P4 | Q | 8000 | UNSAT, certified | 1912.62 | 4418.7 | 86.9 | 500.5 | 5.31 |
| P4_5-7-11 | P4 | H | 2400 | UNSAT, certified | 77.13 | 3093.7 | 25.3 | 169.9 | 1.11 |
| P4_6-7-10 | P4 | H | 2400 | UNSAT, certified | 30.02 | 2648.4 | 13.7 | 119.3 | 0.22 |
| P4_7-9-14 | P4 | H | 2400 | UNSAT, certified | 122.36 | 3421.1 | 32.7 | 213.1 | 1.58 |

Counts by case and kind:
- P4 Q: 1 certified.
- P4 H: 3 certified.
- Timed out (UNKNOWN): 0. Not reached: 0. Errors: 0.

Certified units (all 4), min / median / max:
- solve: 30.02 / 99.75 / 1912.62 s
- lrat-check: 13.7 / 29.0 / 86.9 s
- cake_lpr: 119.3 / 191.5 / 500.5 s (heap 8000 MB every time)
- proof size: 0.22 / 1.35 / 5.31 GB

The three H units on their own:
- solve: 30.02 / 77.13 / 122.36 s
- lrat-check: 13.7 / 25.3 / 32.7 s
- cake_lpr: 119.3 / 169.9 / 213.1 s
- proof size: 0.22 / 1.11 / 1.58 GB

Largest solver RSS: 4418.7 MB (P4_2-8).

There was no SAT result, no proof was rejected (both checkers accepted every proof) and there were no memory problems. Disk use peaked with the 5.3 GB proof of P4_2-8, which the lane then deleted.
