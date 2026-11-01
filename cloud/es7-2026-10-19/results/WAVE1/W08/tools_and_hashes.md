# W08 tools and hash checks

Tools (built in /tmp/claude-0/w08/bin):
- CaDiCaL https://github.com/arminbiere/cadical at c60730422e758ef1cebe7aeddf2dda31c996bf04 (`./configure && make`)
- march_cu https://github.com/marijnheule/CnC at 705b60c6491ef2b61988b3ce6ac674be1b90571d (`make CFLAGS="-O3 -fcommon"`)
- cake_lpr https://github.com/tanyongkiam/cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`);
  bundled example: `cake_lpr example.cnf example.lpr` -> `s VERIFIED UNSAT`

Hashes (all match):
- base CNF m33k7int.sub.cnf regenerated (gen_etv.py 33 7 7 7 --mirror; mirgen.py --interior --yflip-unit):
  69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d  OK
- verify/ii_wave1.json: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e  OK
- entry: {"kind": "shard", "case": "U_L2", "shard": 8, "nshards": 12, "vm": "W08"}
- U_L2.cnf (hullsplit.py case BASE "" 2): 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53  OK
- top.icnf (`march_cu U_L2.cnf -d 7`, 166 s): 128 cubes, 0 refuted leaves,
  sha256 f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd (same as W07's U_L2/top.icnf)
- shard 8 of 12: top-cube indices 8,20,...,116 (10 cubes)
