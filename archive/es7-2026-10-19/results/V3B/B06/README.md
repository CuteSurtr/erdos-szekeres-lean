# V3B B06 (shard 6 of 16)

Ran from 12:38 to 15:03 UTC on 2026-10-20, using 4 cores (see env.txt).

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa. Its bundled example prints `s VERIFIED UNSAT`.
- F.cnf sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d. This matches the expected value.
- Input commit: 066eaa9. verify/v3 commit: bdf319c.
- jtree leaves:
  - WAVE1: 119 dirs, 30151 leaf lines, 71 skipped records
  - WAVE2: 86 dirs, 5156 leaf lines
  - WAVE3: 5 dirs, 232 leaf lines
- M.jsonl: 35153 leaves in 253 cases, 0 problems. sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
- VERIFIED keys: 10121, from 21 files. There were no V3B out.jsonl files at Z.
- Mt.jsonl: n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7. This is the same Mt.jsonl that the other V3B machines produced.

## Results (out.jsonl)
- My shard has 1565 leaves (idx % 16 == 6). The run was `--skip-covers`.
- All 1565 are VERIFIED (cake_lpr `s VERIFIED UNSAT`).
- REJECTED: 0. SAT: 0. TIMEOUT: 0. Unchecked: 0.
- No REJECTED leaf had an empty cake_lpr field, so no step-5 rechecks were needed.
- Solve time: sum 27772.0 s, median 10.56 s, max 304.55 s.
- Check time: sum 6746.1 s, median 3.16 s, max 24.73 s.
