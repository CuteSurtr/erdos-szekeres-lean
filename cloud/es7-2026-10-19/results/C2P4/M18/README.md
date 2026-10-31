# C2P4 M18

Run settings: V = M18, LIST = C2P4.tsv, j = 18, N = 50, H = 2.5, TASK commit a46b478d. The run started at 1793451704 (2026-10-31 13:01:44 UTC), with END = 1793459804 (15:16:44 UTC). One lane ran (`run.sh`). It started at 13:04:35Z and stopped at 15:12:56Z ("stop: 227 s left").

## Tools and checks (details in `tools.txt`)
- `C2P/vendor/build_tools.sh` built the tools from the vendored sources. All 196 files match the manifest. The tools are CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8 and lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Checker sanity test: lrat-check and cake_lpr both reject the bad LRAT and both accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- The base CNF header is `p cnf 838032 16653336`. Both sha256 values match: base.cnf `b0061e90…d8ff1` and base.json `2476faff…b48`.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (14 rows with idx ≡ 18 mod 50)

| status | P3 Q | P3 H | P4 Q | P5 Q | P5 H | P6 H | total |
|---|---|---|---|---|---|---|---|
| certified UNSAT | 0 | 0 | 0 | 1 | 2 | 1 | 4 |
| timed out (UNKNOWN) | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| not reached | 1 | 5 | 2 | 0 | 2 | 0 | 10 |
| error / not certified | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Certified units:

| unit | kind | cap used s | solve s | lrat-check s | cake_lpr s | proof bytes | RSS MB |
|---|---|---|---|---|---|---|---|
| P5_1-9 | Q | 6000 | 4557.67 | 133.6 | 739.1 | 8003462804 | 4390.9 |
| P6_2-3-16 | H | 1800 | 243.63 | 57.4 | 332.4 | 3182117317 | 4361.6 |
| P5_1-9-10 | H | 1186 | 338.62 | 60.6 | 327.8 | 3267240010 | 4358.3 |
| P5_2-8-11 | H | 448 | 402.36 | 59.3 | 346.1 | 3414050514 | 4401.0 |

The lane shortened the caps of the last two units because END was near. Both units still finished well inside their caps.

Min / median / max over the 4 certified units:
- solve: 243.63 / 370.49 / 4557.67 s
- lrat-check: 57.4 / 59.95 / 133.6 s
- cake_lpr: 327.8 / 339.25 / 739.1 s
- proof size: 3.18 / 3.34 / 8.00 GB

Not reached: P5_6-8-15, P5_7-10-11 (P5 H); P4_1-7, P4_9-12 (P4 Q); P3_4-13 (P3 Q); P3_1-4-14, P3_1-9-13, P3_4-6-15, P3_5-6-9, P3_6-7-13 (P3 H).

## Other
- The largest solver RSS was 4401 MB. There were no memory problems: 15 GB RAM, 4 cores.
- There was no SAT answer and no proof was rejected. Every record has `"certified": true`.
- The peak disk use was about 8 GB for the P5_1-9 proof, which the lane deleted after both checks.
