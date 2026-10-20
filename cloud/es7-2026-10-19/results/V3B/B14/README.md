# V3B / B14: shard 14 of 16

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04, cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa. The bundled example gives `s VERIFIED UNSAT`.
- F.cnf was regenerated and has sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, which matches.
- Input commit 066eaa9. verify/v3 taken from bdf319c.
- Manifest:
  - M.jsonl: 35153 leaves across 253 cases, sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549.
  - 10121 VERIFIED keys came from 21 files (V3T, V3A; there was no V3B out.jsonl at Z).
  - Mt.jsonl: n = 25032, sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7. This is the same as on the other V3B machines.
- Run: `v3_check.py --shard 14 --nshards 16 --skip-covers --jobs 4 --cap 1800`. The shard has 1564 leaves.
- Leaf verdicts: VERIFIED 1564, REJECTED 0, SAT 0, TIMEOUT 0. Unchecked: 0. Every VERIFIED record has cake_lpr `s VERIFIED UNSAT`.
- No REJECTED leaf has an empty cake_lpr field, so step 5 had no rechecks.
- Solve time: sum 26130.2 s, median 10.43 s, max 323.11 s.
- Check time: sum 6065.3 s, median 2.83 s, max 22.9 s.
- Wall time: from 12:40 to 15:00 UTC.
- No SAT, REJECTED or TIMEOUT leaves.
