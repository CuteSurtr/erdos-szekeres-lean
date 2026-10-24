# W02 setup (2026-10-20)

Tools (built in the session scratch dir):
- CaDiCaL: github.com/arminbiere/cadical master at c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1)
- march_cu: github.com/marijnheule/CnC at 705b60c6491ef2b61988b3ce6ac674be1b90571d, built with CFLAGS="-O3 -fcommon"
- cake_lpr: github.com/tanyongkiam/cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`; bundled example: `s VERIFIED UNSAT`

sha256 checks:
- regenerated base CNF m33k7int.sub.cnf (results/C/scripts/make_cnfs.sh): 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (expected 69c1dc8f...932d: match)
- verify/ii_wave1.json: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e (expected 6df36dab...c72e: match)
- case U_L2 (hullsplit.py case BASE "" "2"): 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53 (entry cnf_sha256 1d26b947...aa53: match)

Assignment (ii_wave1.json, vm W02): {"kind": "shard", "case": "U_L2", "shard": 2, "nshards": 12, "est_core_h": 14.8}

Top cubes: `march_cu U_L2.cnf -d 7 -o top.icnf` (single run, 172.6 s wall):
"number of cubes 128, including 0 refuted leaves"; sha256 of top.icnf f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd.
Shard 2 of 12 takes 0-based lines 2, 14, ..., 122: 11 cubes. Copy in U_L2.s2of12/top.icnf.

Runner: close_march.py here (close_march_orig.py is the unchanged copy of results/Mii-S/scripts/close_march.py).
Changes: --top/--shard/--nshards, resume from leaves.jsonl (split records carry their children),
leaves.icnf only lists cake_lpr "s VERIFIED UNSAT" leaves, open.icnf, --cases-pre, and a fix for a
loop in the original: when march_cu refutes a cube it prints only the empty cube, which the original
re-queues forever; here the cube gets one cadical retry with 3x the limit and otherwise stays open.
Command: BIN=... close_march.py U_L2.cnf OUT --depth 7 --timeout 300 --split-depth 6 --jobs 4 --shard 2 --nshards 12 --top top.icnf --hours 3.185 (no new cube after 10:15 UTC)
