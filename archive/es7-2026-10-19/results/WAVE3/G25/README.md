# WAVE3 / G25

Task: `results/WAVE3/tasks/G25.json` (at commit 40e11ae): U4_L2 has 128 open cubes and U4-12_L has 52.
Machine: 4 cores, 15 GB (`env.txt`). Tools are in `tools.txt` (CaDiCaL c6073042 3.0.1, march_cu 705b60c6 built with
`-fcommon`, cake_lpr a36874a8; the example gives `s VERIFIED UNSAT`). F sha256 69c1dc8f…ffff932d matches. Both case
CNFs (hullsplit.py) match cases.jsonl. The driver is `close_march.py`, a byte copy of WAVE2/F2's; checks (a)–(c) are in `driver.diff`.
Options: `--name <case> --top <given cubes> --depth 7 --timeout 300 --split-depth 6 --jobs 4`. The cases ran one after the other.

**No SAT result. cake_lpr rejected nothing: every UNSAT leaf printed `s VERIFIED UNSAT`.**

| case | cubes given | verified leaves | splits | cubes still open | every given cube covered | solve s (sum) | check s (sum) | wall |
|---|---|---|---|---|---|---|---|---|
| U4-12_L | 52 | 52 | 0 | 0 | yes (52/52) — CLOSED | 62 | 139 | 11:20:24–11:21:15 |
| U4_L2 | 128 | 254 | 2 (64 sub-cubes each, 0 refuted) | 0 | yes (128/128) — CLOSED | 5886 | 981 | 11:21:15–11:56:03 |

- U4-12_L: each of the 52 given cubes is itself a verified leaf (`leaves.icnf` = `top.icnf` as a set). Max solve 5.8 s.
- U4_L2: 126 given cubes closed directly. Two cubes, `[-1896,-2247,-2572,-2872,3281,3265,3248]` and its
  complement-sign twin `[1896,2247,2572,2872,-3281,-3265,-3248]`, timed out at 300 s and were split by march_cu
  (depth 6, 64 sub-cubes each). All 128 sub-cubes are verified leaves. Max solve 230.7 s.  march time for splits: 719 s.
- Cover check: `cover_g25.py GIVEN leaves.icnf` is my own checker. It rejects lines not ending in ` 0`, and for each
  given cube it checks that the leaves consistent with it cover it. It prints `covered 52/52` for U4-12_L and
  `covered 128/128` for U4_L2. Every leaf extends a given cube. Neither case has a duplicate leaf. Both `open.icnf` files are empty.
- leaves.jsonl starts with `{"case", "case_sha256"}` in both cases.

## Incident (no effect on results)
At 11:50 I committed a progress snapshot. Its `git pull --rebase --autostash` rewound the working tree for a moment,
which removed the U4_L2 output directory. The driver's main thread then crashed in `finalize()` (mkstemp: no such
directory). The worker threads finished every queued cube and kept appending to leaves.jsonl. Any record appended
during the rewind could only be lost, never invented, and a lost record leaves its cube open. At 11:55 I resumed the
driver (output now under /opt/work, copied back into the repo for commits). It rebuilt the frontier from leaves.jsonl:
the frontier was empty, so it re-wrote `leaves.icnf` (254) and `open.icnf` (0) atomically. Lesson for later
runs: do not let the driver write into the git working tree while you commit with rebase.
