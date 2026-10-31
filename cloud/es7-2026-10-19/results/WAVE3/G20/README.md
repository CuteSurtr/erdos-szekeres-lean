# WAVE3 G20: open cubes of case U5_L

Task file `results/WAVE3/tasks/G20.json` (commit 9a26cc2): one case, U5_L, with 527 open cubes.
Run on 2026-10-20, 10:56 to 12:28 UTC, on 4 cores with 15 GB RAM (`env.txt`). Tools and their commits are in `tools.txt`.
F's sha256 is 69c1dc8f…ffff932d, regenerated here. The case CNF `hullsplit.py case F.cnf 5 ""` has sha256
c2b7484c…2762d2… (c2b7484cf0dfcb0254745e913db06842919f8482e698de8038dc278860ed9048), which is the value in cases.jsonl.

The driver `close_march.py` is a byte-identical copy of `results/WAVE2/F2/close_march.py`. What I checked is in
`driver.diff`: a fresh mkdtemp directory per job, atomic tmp+rename writes of leaves.icnf and open.icnf, a first
leaves.jsonl record with case and case_sha256, and leaves only when cake_lpr prints `s VERIFIED UNSAT`.
`--skip` was not used.

Run: `close_march.py U5_L.cnf OUT --name U5_L --top <527 given cubes, in file order> --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.66`.
The driver was restarted once, about 4 minutes in, so that its output directory sits outside the git tree
(there was a rebase/autostash race on leaves.jsonl). It resumed from leaves.jsonl, which holds 2 `resume` records.
The 2 solver jobs that were running at the restart were killed and their cubes re-solved; no records were lost.

| case | cubes given | verified leaves | split cubes | cubes still open | every given cube covered |
|------|------------:|----------------:|------------:|-----------------:|:------------------------:|
| U5_L | 527 | 842 | 5 (64 sub-cubes each, march_cu -d 6, 0 refuted) | 0 | yes |

- **U5_L is CLOSED.** All 842 leaves are UNSAT, and cake_lpr printed `s VERIFIED UNSAT` for each one.
- **No SAT results, and no cake_lpr rejections** (no UNSAT_UNCHECKED, TIMEOUT or SAT records).
- Times: CaDiCaL solve 10,200 s in total (the longest one took 228.5 s, so none hit the 300 s cap). cake_lpr check took 2,691 s. The 5 march_cu splits took 1,878 s.
  The 5 splits came from solver timeouts. Child CPU was 63,306 s in total. The largest LRAT proof was 186 MB (not committed). Wall time was about 85 min.
- Cover check, done independently of the driver:
  - every given cube is either a leaf or split, with all of its children leaves;
  - every leaf extends a given cube;
  - leaves.icnf equals the set of verified UNSAT records in leaves.jsonl;
  - every line has the form `a … 0`;
  - open.icnf is empty.

Files in `U5_L/`: `top.icnf` (the 527 given cubes, sha256 aa6babb6…), `leaves.icnf` (842 full cubes over F's
variables), `leaves.jsonl`, and `open.icnf` (empty).
