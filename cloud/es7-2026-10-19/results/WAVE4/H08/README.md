# WAVE4 H08: case U_L2

Task file `results/WAVE4/tasks/H08.json` (at e0f250b): case **U_L2** (U = [], L = [2]),
**325 cubes given**. Case CNF sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53
(matches cases.jsonl); F sha256 69c1dc8f...ff932d (matches). Driver: byte copy of
`results/WAVE2/F2/close_march.py` (see driver.diff), run with `--depth 7 --timeout 300
--split-depth 6 --jobs 4 --hours 2.222`, 12:54:25Z to 14:10Z on 4 cores. Tools: tools.txt.

Result:
- No SAT result. No cake_lpr rejection, no UNSAT_UNCHECKED record, no TIMEOUT record.
- **692 verified leaves** (every one: CaDiCaL exit 20 and cake_lpr `s VERIFIED UNSAT`, no heap retry).
- **6 cubes split** (each after a 300 s CaDiCaL timeout): 2 of the given cubes (march_cu -d 6
  gave 54 and 63 sub-cubes) and 4 of their sub-cubes (64 sub-cubes each).
  Leaf count check: 323 + 54 + 63 - 4 + 4*64 = 692.
- **0 cubes still open**; `U_L2/open.icnf` is empty.
- **Every given cube is covered by the leaves**: walking from each of the 325 cubes of top.icnf
  through the SPLIT records (`subs`) in leaves.jsonl ends in a cube of leaves.icnf every time;
  all 692 leaves are used, none uncovered. (Split covers rest on march_cu's cube output and are
  to be re-checked by the cover check.)
- Time over the 692 leaves: solve sum 10196.6 s, median 8.73 s, max 296.66 s;
  cake_lpr check sum 2405.5 s, median 2.49 s, max 22.89 s. The 6 timed-out solves add
  1800.1 s, and the 6 march_cu splits took 171.5-495.1 s (2171.0 s total).

Files: `U_L2/top.icnf` (the 325 given cubes, in file order), `U_L2/leaves.icnf`,
`U_L2/open.icnf`, `U_L2/leaves.jsonl`, plus env.txt, tools.txt, driver.diff, close_march.py.
