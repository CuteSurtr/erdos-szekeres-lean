# WAVE3 / G24

Task: close the open cubes in `results/WAVE3/tasks/G24.json` (commit 40e11ae).
Environment is in `env.txt`, tools in `tools.txt`, and the driver review in `driver.diff`.
The driver is `close_march.py`, a byte-identical copy of `results/WAVE2/F2/close_march.py`.
It was run with `--name <case> --top <cubes> --depth 7 --timeout 300 --split-depth 6 --hours 2.6`.
U15_L4 ran with `--jobs 3` and U3_L9 with `--jobs 1`, at the same time.
Run time was 11:20 to about 11:29 UTC on 2026-10-20.

F (`/opt/work/F.cnf`) was regenerated and its sha256 is 69c1dc8f…932d, which matches.
Each case CNF was built with `hullsplit.py case F.cnf U L OUT.cnf`, and its sha256 matches `cases.jsonl`.
The cubes given were written as `top.icnf` in the order of the task file.

| case | cubes given | verified leaves | open | every given cube covered | CaDiCaL solve (s, sum / max) | cake_lpr check (s, sum) |
|---|---|---|---|---|---|---|
| U15_L4 | 128 | 128 | 0 | yes: CLOSED | 452.4 / 25.7 | 366.6 |
| U3_L9  | 32  | 32  | 0 | yes: CLOSED | 439.3 / 202.8 | 132.7 |

- Every given cube was solved directly within the 300 s cap. Nothing was split, so each leaf in `leaves.icnf` is exactly one of the given cubes (the set of leaves equals the set of given cubes, checked).
- Every leaf has cake_lpr output exactly `s VERIFIED UNSAT`. There were no SAT results, no cake_lpr rejections and no timeouts.
- `leaves.jsonl` starts with `{"case", "case_sha256"}`.
- Overlap: the 128 U15_L4 cubes are, as a set, the top cubes of `results/WAVE2/S5/U15_L4/top.icnf`. S5 also closed all 128 of them. This run closes them independently.
- U3_L9's 32 cubes are exactly `results/WAVE1/W34/U3_L9/open.icnf`. Together with W34's 93 verified leaves they cover W34's 125-cube top file. Its 1 march-refuted cube still needs whatever handling the cover check applies to W34's top file.
