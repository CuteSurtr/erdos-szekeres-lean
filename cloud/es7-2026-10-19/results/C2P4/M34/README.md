# C2P4 M34: shard 34 of 50 of `lists/C2P4.tsv`, budget 2.5 h

Task: `results/C2P4/TASK.md` at commit a46b478d, with V = M34, LIST = C2P4.tsv, j = 34, N = 50, H = 2.5.
Machine: 4 cores, 15 GB RAM, no swap (`env.txt`). Started 2026-10-31 13:01:34 UTC. The lane ran 13:04:39–15:06:38 UTC with END = 1793459794 (15:16:34 UTC).

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` built everything from the vendored `tools-src.tar.xz`. All 196 manifest files matched. Nothing was cloned or downloaded.
  - Built: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), and lrat-check (2e3b2dc) with the E2 patch.
- Sanity checks:
  - Both checkers reject the bad LRAT: lrat-check `c FAILED`, cake_lpr `pivot must be non-zero`.
  - Both accept the good one: `c VERIFIED` / `s VERIFIED UNSAT`.
  - The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF (`SYMZ/zcnf.py rot 17 7 --m 2 --hull`):
  - Header `p cnf 838032 16653336`.
  - sha256 b0061e90…8ff1 (base.cnf) and 2476faff…2b48 (base.json). Both match.
- Cubes: `C2C34/l2cubes.py` for a = 1..8 is byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19 rows with idx ≡ 34 mod 50, `units.tsv`)

| | P5 Q | P5 H | P4 Q | P4 H | P3 Q | P3 H | total |
|---|---|---|---|---|---|---|---|
| certified | 1 | 1 | 0 | 0 | 0 | 0 | 2 |
| UNKNOWN (cap cut by END) | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| not reached | 0 | 3 | 1 | 5 | 1 | 6 | 16 |
| errors / certified false | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

- **Certified:**
  - P5_6-15 (Q, cap 6000): solve 5357.1 s, proof 9.16 GB, lrat-check 154.4 s, cake_lpr 757.0 s.
  - P5_1-2-13 (H, nominal cap 1800, cap given by the lane 982): solve 294.7 s, proof 3.28 GB, lrat-check 54.3 s, cake_lpr 313.8 s.
  - Over the 2 certified units (min / median / max):
    - solve: 294.7 / 2825.9 / 5357.1 s
    - lrat-check: 54.3 / 104.4 / 154.4 s
    - cake_lpr: 313.8 / 535.4 / 757.0 s
    - proof size: 3.28 / 6.22 / 9.16 GB
- **UNKNOWN:** P5_2-6-9 (H) started at 15:01:26, just before the start cutoff. The lane cut its cap to 307 s to keep the end window, and it timed out at 303.6 s. That is not a timeout at its nominal 1800 s cap, so it is still open and should be run again in full.
- **Not reached:**
  - P5: P5_2-13-15, P5_6-12-14, P5_8-10-12.
  - P4: P4_5-6 (Q), P4_1-3-6, P4_1-9-11, P4_2-6-13, P4_5-8-15, P4_6-9-14.
  - P3: P3_1-10 (Q), P3_1-2-5, P3_1-7-13, P3_4-5-10, P3_4-10-14, P3_5-10-12, P3_7-10-11.

## Resources and anomalies
- The largest solver RSS was 4406 MB (P5_1-2-13). There were no memory problems.
- Peak disk use was about 9.2 GB of proof on a disk with 29 GB free. Every proof was deleted after its checks.
- No SAT, no proof rejected and no errors.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.
