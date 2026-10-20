# WAVE4 H71

Case: U_L2 (case CNF sha256 1d26b9475d1609388bda1853cc22c1fba0bb73fb1a5f8a28adf9fbd3f15aaa53, matches cases.jsonl).
Task list: results/WAVE4/tasks/H71.json (at 1d3a72c), 6 cubes; top.icnf has 6 lines (sha256 f8a48cc11d5b295728a939e61121e542c418688869566a1696a4476a73f8ba64).

- Verified leaves: 6 (every one has cake_lpr `s VERIFIED UNSAT`).
- Cubes split: 0.
- Cubes still open: 0 (open.icnf is empty; driver printed `open 0`).
- Every given cube is covered by a verified leaf (each leaf equals its top cube): yes.
- Solve time (CaDiCaL wall): sum 181.23 s, median 30.68 s, max 35.51 s.
- Check time (cake_lpr): sum 64.38 s, median 10.73 s, max 12.95 s.
- SAT results: none. cake_lpr rejections: none. UNSAT_UNCHECKED records: none.

Driver: close_march.py = byte copy of results/WAVE2/F2/close_march.py (see driver.diff); run with
--depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 1.217, output dir /opt/work/out/U_L2.
Tools: tools.txt. Environment: env.txt.
