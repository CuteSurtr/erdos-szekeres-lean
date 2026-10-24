# W04: U_L2, shard 4 of 12 — CLOSED

Entry of `verify/ii_wave1.json`: kind "shard", case U_L2 (U = [], L = [2]), shard 4, nshards 12.
Ran in one cloud container (4 cores, 15 GB, see env.txt), 2026-10-20 06:55–08:33 UTC.

## Tools (hashes.txt)
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04
- march_cu from CnC 705b60c6 (built with -fcommon)
- cake_lpr a36874a8 (`make cake_lpr`; bundled example prints `s VERIFIED UNSAT`)

## sha256 checks (all match)
- m33k7int.sub.cnf regenerated: 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d
- verify/ii_wave1.json: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e
- U_L2.cnf (hullsplit.py case): 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53
- top.icnf (march_cu -d 7): 128 cubes, 0 refuted leaves,
  f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd
  (same file as W01 and W07 committed for their U_L2 shards)

## Result
- My part: top cubes with index i ≡ 4 (mod 12): 11 cubes.
- All 11 timed out at 300 s and were split by `march_cu -d 6` into 64 cubes each (0 refuted).
- All 704 children: CaDiCaL UNSAT (max 65 s) and cake_lpr `s VERIFIED UNSAT` on every one;
  0 unverified, 0 SAT, 0 open (open.icnf is empty).
- Cover: `covercheck.py U_L2_s4/leaves.icnf <the other 117 top cubes>` prints `s COVERED 821`,
  so the 704 leaves cover the 11 top cubes of this shard. summarize.py also checks each top cube
  separately: 11/11 covered.
- CPU (recorded): 18,620 s total = cadical 13,995 s on leaves + 900 s on the top-cube timeouts,
  cake_lpr 2,957 s, march_cu splits 769 s. About 45 core-min more was lost in the first run (NOTES.md).
  Largest LRAT proof 54 MB (deleted after checking).

## Files
- scripts/close_march.py: copy of results/Mii-S/scripts/close_march.py (first commit is the
  original) plus --shard/--nshards, --top, --work, --log, --presplit and resume from leaves.jsonl.
- scripts/summarize.py: writes leaves.icnf, open.icnf, summary.json from leaves.jsonl.
- U_L2_s4/: top.icnf, top.log, leaves.jsonl (all records), leaves.icnf (704 verified leaves,
  `a lits 0`, full cubes relative to U_L2.cnf), open.icnf (empty), summary.json.
- NOTES.md: the lost first-run records and how the run was restarted.
