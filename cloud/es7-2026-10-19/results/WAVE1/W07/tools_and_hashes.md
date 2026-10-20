# W07 tools and hash checks (2026-10-20)

Tools (built in this session, x86_64, 4 cores):
- CaDiCaL: github.com/arminbiere/cadical master at c60730422e758ef1cebe7aeddf2dda31c996bf04 (`./configure && make`)
- march_cu: github.com/marijnheule/CnC at 705b60c6491ef2b61988b3ce6ac674be1b90571d, Makefile CFLAGS + `-fcommon`
- cake_lpr: github.com/tanyongkiam/cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`;
  `./cake_lpr example.cnf example.lpr` prints `s VERIFIED UNSAT`; an empty proof gives
  `c empty clause not derived at end of proof` (no s line).

Hash checks (all match):
- base CNF m33k7int.sub.cnf regenerated (gen_etv.py 33 7 7 7 --mirror; mirgen.py --interior --yflip-unit):
  69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d  OK
- verify/ii_wave1.json: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e  OK
- results/Mii-S/cases.jsonl: bf77e23c6d9cdffb451a3ae63bdb972b4cc9589fbdca424e9cf0621f9e826f58 (matches ii_wave1.json)
- case U_L2 (U=[], L=[2], hullsplit.py case): 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53  OK (entry W07)

Top cubes: `march_cu U_L2.cnf -d 7 -o top.icnf` (171 s): number of cubes 128, including 0 refuted leaves;
sha256(top.icnf) = f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd.
Shard 7 of 12 = top lines 7,19,...,127 (11 cubes).
