# WAVE4 H37: case U_L7

- Case U_L7 (U = "", L = "7"), case CNF sha256 c6d1c840d97921426e0f2d1d34213fb94293cc1783296ec2357d7883b804f099 (matches cases.jsonl).
- Cubes given: 196 (`results/WAVE4/tasks/H37.json` at 4bfd8e7), written in order to `U_L7/top.icnf` (196 lines).
- Driver: `close_march.py` (byte-identical to WAVE2/F2, see driver.diff), `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.22`, started 13:39:48 UTC, ended about 14:20 UTC with `open 0`.
- Verified leaves: 259, each with cake_lpr printing `s VERIFIED UNSAT`.
- Cubes split: 1 (a top cube that hit the 300 s cap; march_cu -d 6 gave 64 sub-cubes, 0 refuted, all 64 closed).
- Cubes still open: 0. `open.icnf` is empty.
- Cover: all 196 given cubes are covered by my leaves (each is a verified leaf, or split with every sub-cube a verified leaf).
- Time over the 259 verified leaves: solve sum 5296.0 s, median 7.16 s, max 285.53 s; check sum 1047.2 s, median 2.43 s, max 24.36 s. The split cube also used 300.0 s of solve time before it was split.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.
