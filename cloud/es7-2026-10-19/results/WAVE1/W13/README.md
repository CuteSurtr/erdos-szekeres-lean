# W13: U_L4, shard 1 of 3: CLOSED

Entry from `verify/ii_wave1.json`: kind "shard", case U_L4 (U = {}, L = {4}), shard 1 of 3, est. 12.9 core-h.

## Environment and tools
Cloud VM, 4 cores, 15 GB RAM (`env.txt`). Tools (`tools.txt`):
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04
- march_cu (CnC 705b60c6491ef2b61988b3ce6ac674be1b90571d, built with -fcommon)
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`; the bundled example gives `s VERIFIED UNSAT`)

## sha256 checks (all match)
- regenerated `m33k7int.sub.cnf`: 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d
- `verify/ii_wave1.json`: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e
- `results/Mii-S/cases.jsonl`: bf77e23c6d9cdffb451a3ae63bdb972b4cc9589fbdca424e9cf0621f9e826f58
- case CNF `U_L4.cnf` (`hullsplit.py case BASE "" 4`): eb730ad3eebdd96f8daf71efb79c4932d861ddd0e0b1c8b38c6423112bf66df8
- top cubes `march_cu U_L4.cnf -d 7`: 128 cubes, 0 refuted leaves, 250 s;
  `U_L4-s1/top.icnf` sha256 c172b9354496170c210bab5707ff63b120495823df0ac3b38b04da125cbfcd08,
  the same value W12 (shard 0) and W14 (shard 2) recorded.

## Run
`close_march.py` here is a copy of `results/Mii-S/scripts/close_march.py` with `--top/--shard/--nshards`,
resume from leaves.jsonl (SPLIT records keep their children), and periodic leaves.icnf/open.icnf.
The recipe is unchanged: cadical --lrat -t 300, cake_lpr on every UNSAT, march_cu -d 6 on a timeout.
Shard 1 = the 43 top cubes with line index i, i mod 3 == 1.

Wall time 07:03 to 08:42 UTC, 4 jobs. The first segment's log file was replaced under the running
process by a `git pull --rebase` (output dir was inside the git tree). The 19 records it had written
were recovered from the open file handle, the process was restarted at 07:14 with its output outside
the tree and resumed from those records. The in-flight work at the restart (about 4 jobs x a few
minutes) was redone and is not counted below.

## Result
- 43 top cubes: 39 closed directly, 4 split; 11 splits in all (4 at depth 7, 4 at depth 13, 3 at depth 19).
- 710 leaves, all UNSAT with cake_lpr `s VERIFIED UNSAT`. No unchecked UNSAT, no SAT, no timeouts left;
  `open.icnf` is empty.
- Leaf depths: 7: 39, 13: 252, 17: 2, 18: 9, 19: 227, 23: 2, 24: 5, 25: 174.
- CPU (sum of recorded job times): 22,871 s = 6.35 core-h (cadical 17,819 s, cake_lpr 2,586 s,
  march splits 2,465 s), plus 250 s for the top march. LRAT proofs total 16.2 GB (deleted after checking).
- Cover (`covercheck.txt`, `results/Mii-S/scripts/covercheck.py`): leaves.icnf with the 85 top cubes of
  shards 0 and 2 gives `s COVERED`, while each part alone gives NOT COVERED. Restricting leaves.icnf to
  each of the 43 shard-1 top cubes gives `s COVERED` 43 times. All 710 leaves extend a shard-1 top cube.

Files: `U_L4-s1/leaves.jsonl` (all records), `leaves.icnf` (sha256
62e7896979ed2ab88fa051e8498d72566c2a984935f4be210ea99b9fb8a1ba3b), `open.icnf` (empty), `top.icnf`, `top.txt`.
