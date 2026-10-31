# C2P4 M44

Machine M44, shard j = 44 of N = 50 of `lists/C2P4.tsv`, budget H = 2.5 h, task commit a46b478d.
Start 2026-10-31 13:01:40Z (epoch 1793451700), END = 1793459800 (15:16:40Z). 4 cores, 15 GB RAM.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh` from the vendored sources (manifest: all 196 files match): CaDiCaL 3.0.1 (c6073042),
  cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity: both checkers reject the bad LRAT and accept the good one; cake_lpr example `s VERIFIED UNSAT`.
- Base CNF `p cnf 838032 16653336`; sha256 of base.cnf and base.json both match the TASK.
- Cubes P1..P8 from `l2cubes.py` byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (18: idx ≡ 44 mod 50)
| status | count | by case / kind |
|---|---|---|
| certified (UNSAT, both checkers) | 6 | P5: 1 Q (P5_8-10), 5 H (P5_1-6-13, P5_2-7-13, P5_6-7-15, P5_7-8-14, P5_9-11-12) |
| timed out (UNKNOWN) | 1 | P4: 1 Q (P4_5-16) |
| not reached | 11 | P4: 5 H; P3: 1 Q (P3_4-8), 5 H |
| errors / `certified: false` | 0 | |

All six P5 units of this shard are certified.

P4_5-16 started at 14:14:16Z with only ~1 h left, so lane.py cut its cap to 3143 s (not the list cap of 6000 s); it
ran 3115 s CPU without an answer. It is a timeout at the reduced cap, not at 6000 s.

Not reached: P4_1-5-11, P4_1-10-15, P4_2-8-9, P4_5-10-12, P4_6-12-13, P3_4-8, P3_1-4-9, P3_1-8-15, P3_4-6-10,
P3_4-13-14, P3_6-7-8.

### Certified units (6)
| | min | median | max |
|---|---|---|---|
| solve s | 101.4 | 417.5 | 588.3 |
| lrat-check s | 27.3 | 54.7 | 58.8 |
| cake_lpr s | 172.3 | 317.3 | 342.0 |
| proof bytes | 1.20 GB | 3.39 GB | 3.75 GB |

| unit | kind | solve s | proof bytes | lrat-check s | cake_lpr s |
|---|---|---|---|---|---|
| P5_8-10 | Q | 578.93 | 3552442732 | 58.7 | 330.6 |
| P5_1-6-13 | H | 588.33 | 3753576859 | 58.2 | 342.0 |
| P5_2-7-13 | H | 571.36 | 3711710013 | 58.8 | 336.7 |
| P5_6-7-15 | H | 263.67 | 3230630762 | 51.2 | 304.0 |
| P5_7-8-14 | H | 104.55 | 1198099355 | 27.3 | 172.3 |
| P5_9-11-12 | H | 101.41 | 1472325935 | 29.9 | 182.9 |

## Resources and incidents
- Largest solver RSS: 4466 MB (P5_2-7-13). No memory problem.
- No SAT, no proof rejection, no errors.
- Lane stopped at 15:06:46Z (593 s left before END); `lane done`.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`.
