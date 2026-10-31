# C3X: which method closes hard nodes of the 3-fold class fastest

Task: `TASK.md` (H = 1.0, Z = d88e0d49). Results and recommendation: `RESULTS.md`.

Files:
- `env.txt` — machine; `tools.txt` — tool commits, patches, sanity checks, base CNF sha256 (matches).
- `scripts/c3x.py BASE NODE METHOD BUDGET RECORDS` — one (node, method) run at a fixed wall budget on 4 cores:
  `ref` (C3-S `close_tree.py` unmodified, caps 300,300,600, `--cadopts=--sat --split-singles --jobs 4`, killed at budget+30 s),
  `march<D>` (march_cu `-d D` on base + node units, each cube solved by CaDiCaL `--sat --lrat`),
  `split` (all `tree_children` of the node, i.e. the next layer's orbit choice, solved with `--sat`),
  `opt` (4 CaDiCaL option sets not in `C3-S/logs/cadical_options.jsonl`, one per core, on the node CNF).
  Every UNSAT subproblem is checked by `controls.dual` (lrat-check E2 + cake_lpr), after the solve window.
- `scripts/run_all.sh`, `scripts/run_rest.sh` — the runners actually used (the first was stopped after 3 runs and the rest
  reprioritised for time); `scripts/table.py` — makes the RESULTS table.
- `records.jsonl` — one line per run, including every subproblem's status, times and checker lines; `run.log`.

Nodes: `0s0-1s1_2s1-8s1_6s1-9s0` and `0s0-1s1_6s0-9s1_5s0-10s1` (open depth-3 two-orbit nodes under roots
that timed out at 300 s), `0s0-1s1_6s1-10s0_2_7s0-9s0` (open depth 4) and `0s0-3s0_4` (one-orbit layer-2 root, not
attempted by any wave); the last two got no completed run within the hour.

Incidents (time only): an initial node list had a depth-5 node and an already certified node, so it was restarted after
~1 min; `run_rest.sh`'s wait loop matched a stale shell's command line and idled for ~10 min (01:48–01:58).
The ref run on the depth-4 node was killed at the stop and wrote no record.
