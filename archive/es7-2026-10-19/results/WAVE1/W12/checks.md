# W12 tool builds and hash checks

Tools (built in /home/user/tools, BIN=/home/user/tools/bin):
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1), ./configure && make
- march_cu from CnC 705b60c6491ef2b61988b3ce6ac674be1b90571d, make with CFLAGS += -fcommon
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, make cake_lpr; bundled example: `s VERIFIED UNSAT`

Hashes (all match the expected values):
- base m33k7int.sub.cnf (gen_etv.py 33 7 7 7 --mirror; mirgen.py --interior --yflip-unit, as in make_cnfs.sh): 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d
- verify/ii_wave1.json: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e
- results/Mii-S/cases.jsonl: bf77e23c6d9cdffb451a3ae63bdb972b4cc9589fbdca424e9cf0621f9e826f58
- case U_L4 (hullsplit.py case BASE "" 4): eb730ad3eebdd96f8daf71efb79c4932d861ddd0e0b1c8b38c6423112bf66df8 (entry: eb730ad3eebdd96f8daf71efb79c4932d861ddd0e0b1c8b38c6423112bf66df8)

Top cubes of U_L4: `march_cu U_L4.cnf -d 7 -o top.icnf`: 128 cubes, including 0 refuted leaves,
233.5 s; sha256 of top.icnf c172b9354496170c210bab5707ff63b120495823df0ac3b38b04da125cbfcd08; covercheck.py top.icnf: s COVERED 128.
Shard 0 of 3 takes the 43 cubes with line index 0, 3, ..., 126.
