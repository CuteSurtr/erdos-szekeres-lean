# W27 — wave 1, mirror sub-case (ii), entry kind "cases": U5_L, U_L9, U_L12

Run on one cloud VM (4 cores, 15 GB RAM; `env.txt`), 2026-10-20 06:55–10:27 UTC.

## Tools (built in this session)
| tool | commit | binary sha256 |
|---|---|---|
| CaDiCaL 3.0.1 | c60730422e758ef1cebe7aeddf2dda31c996bf04 | 65290002b9c189066ebc381ac5474b0c31479b7be5fe6408631c429fbcb68f37 |
| march_cu (CnC, `make CFLAGS="-O3 -fcommon"`) | 705b60c6491ef2b61988b3ce6ac674be1b90571d | 5239ba7c5f44f2468c721bc54991fa1374fee096b375f31271e18cee391061b2 |
| cake_lpr (`make cake_lpr`) | a36874a8b750b43fe4b385b8ddbf5b033e46a3fa | 1822ca1e5d0f925e8f3b73047941a8261bee65eef6ccb0e33bb49f92821a09ca |

cake_lpr on its bundled `example.cnf example.lpr` printed `s VERIFIED UNSAT`.
Only cake_lpr was used to check proofs (no drat-trim lrat-check).

## Hash checks (all match)
- base CNF regenerated (`gen_etv.py 33 7 7 7 --mirror`, then `mirgen.py ... --interior --yflip-unit`):
  `m33k7int.sub.cnf` = 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d ✓
- `verify/ii_wave1.json` = 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e ✓;
  `results/Mii-S/cases.jsonl` = bf77e23c6d9cdffb451a3ae63bdb972b4cc9589fbdca424e9cf0621f9e826f58 ✓
- case CNFs (`hullsplit.py case`): U5_L c2b7484c…9048 ✓, U_L9 887d573e…28fb4 ✓, U_L12 ab93db48…553b7 ✓

## Method
1. `scripts/direct.py`: plain `cadical --lrat -t 60` on each whole case (run in parallel). All three: UNKNOWN.
2. `scripts/close_march.py`: copy of `results/Mii-S/scripts/close_march.py` (`close_march_orig.py`,
   sha256 5215f5f1…d609) with the same recipe (`march_cu -d 7` top cubes, `cadical -t 300` per cube,
   `march_cu -d 6` split on timeout, cake_lpr on every UNSAT, proofs deleted after checking), made
   resumable (top cubes kept as `top.icnf`; SPLIT records carry their children), with
   `--shard/--nshards` and a `--deadline` after which no cube is started; writes `leaves.icnf`
   (cake_lpr-verified leaves only) and `open.icnf`.
3. Driver `scripts/run_w27.sh` ran the cases in listed order with 4 jobs, deadline 10:20 UTC.
   **Deviation:** at 09:05 it was clear that U5_L (far above its 30k core-s estimate) would use up the
   budget, so U_L12 was started early with 1 extra job alongside U5_L (5 solver processes on 4 cores
   from then on). U_L9 only got its top-cube march after the deadline.

## Results
| case | CNF sha256 | top.icnf sha256 (cubes / refuted) | verified leaves | splits | open | covercheck | CPU |
|---|---|---|---|---|---|---|---|
| **U_L12** | ab93db48…553b7 | 93828537e981e90dc6171e6c80f16f982fd48dc2b4dc6d939fca1c0335c198e9 (128 / 0) | 128 (all `s VERIFIED UNSAT`) | 0 | 0 | leaves.icnf `s COVERED 128` | 1.17 h |
| U5_L | c2b7484c…9048 | f968802ccaff7ea2ef2c8fafe3b9d69f1c6884d682a518de2872e258588ff596 (128 / 0) | 1213 (all verified) | 26 (×51–64 children) | 527 | leaves alone NOT COVERED (expected); leaves+open `s COVERED 1740` | 13.26 h |
| U_L9 | 887d573e…28fb4 | edfda640cdb0507fc72b4d77493d774a4321f02cd7e6b34fbd1bd97179939911 (128 / 0) | 0 | 0 | 128 | top `s COVERED 128` | 0.08 h |

CPU = whole-case attempt + top march + cadical + cake_lpr + split marches (wall seconds per job).
U5_L split: cadical 37,817 s, cake_lpr 4,818 s, splits 4,874 s; max cube depth 19.

- **U_L12: CLOSED** (every leaf cake_lpr-verified; leaves cover the case).
- **U5_L: OPEN** — 527 cubes in `U5_L/open.icnf` (depth-13/19 children of split top cubes, plus
  unstarted cubes); resumable from `leaves.jsonl` with the same script.
- **U_L9: OPEN** — not started beyond the top cubes; 128 cubes in `U_L9/open.icnf`.
- No SAT answer, no ERROR record, no UNSAT answer that cake_lpr failed to verify.

Files per case: `leaves.jsonl` (all records), `leaves.icnf`, `open.icnf`, `top.icnf`.
No CNF or proof files are committed.
