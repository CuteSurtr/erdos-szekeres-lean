# F6: case U_L8, part 0 of 2

**Result: my share is closed.** All 725 cubes of my share are covered by 788 leaves that cake_lpr
verified (`s VERIFIED UNSAT`). `open.icnf` is empty. No SAT result. cake_lpr rejected nothing.

## Run
- VM: 4 cores, 15 GB (`env.txt`). Tools and hashes: `tools.txt`. F (69c1dc8f...) and the U_L8 case
  CNF (6c05114f...) were rebuilt and match.
- Frontier: F7 had not committed one yet, so I built it from `WAVE1/W30/U_L8` at commit b1d2e4d
  (W30 had stopped at 10:15). It has 1450 cubes: the 2207 cubes W30 created (128 top cubes plus the
  sub-cubes of its 33 SPLIT records), minus 724 verified-closed and 33 split. It is identical to W30's
  `open.icnf`. `U_L8/frontier.icnf` is in Python's sorted order. F7 copied it (`F7/U_L8/frontier.icnf`
  is byte-identical), so the two shares are disjoint.
- Share: positions p with p mod 2 = 0, in reverse order. That is 725 cubes (`U_L8/share.icnf`, which is
  also `U_L8/top.icnf`).
- Driver: `close_march.py` is F2's driver plus one guard: a split that yields no cubes or an empty cube
  becomes SPLIT_FAIL, so it cannot loop forever. The guard never triggered. Review: `driver.diff`.
  `--timeout 300 --split-depth 6 --jobs 4`, with the deadline at 13:05 UTC.
- The run started at 10:27:09 UTC. At 10:28 I restarted it from its own leaves.jsonl, after 4 leaves,
  so that its output went to /opt/work/U_L8 outside the git tree (git pull --autostash could have raced
  with appends). `snap.sh` copied the output into `U_L8/`. The resume record shows a frontier of 721. The
  run finished at about 11:45 UTC with `open 0`.
- Skip file: before the start and at each snapshot, `refresh_skip.sh` (F1's `mkskip.py` over W30's and
  F7's U_L8 leaves.jsonl) found 0 cubes of my share already closed elsewhere. No cube was skipped.

## Numbers
| | |
|---|---|
| share cubes | 725 |
| verified leaves (`leaves.icnf`) | 788 (724 share cubes directly; 1 cube split into 64 sub-cubes, all closed) |
| open cubes | 0 |
| skipped as closed elsewhere | 0 |
| SAT | none |
| cake_lpr rejections / heap retries | 0 / 0 |
| CaDiCaL time (sum) | 14649 s |
| cake_lpr time (sum) | 2978 s |
| march_cu split time | 142 s |
| longest solve / largest LRAT proof | 300 s (the one split cube) / 255 MB |
| wall time | about 1.3 h on 4 cores |

(The `cpu_s` field in leaves.jsonl comes from process-wide `os.times()` deltas. With 4 threads it
over-counts, so do not use it.)

## Cover checks (my own Python, same algorithm as Mii-S covercheck.py; malformed lines rejected)
- Every share cube is covered by the leaves that extend it: 725/725. Every leaf extends a share cube:
  788/788. All leaves are distinct.
- W30 leaves (724) + F6 leaves (788) + F7's share (725 cubes, still open): `s COVERED` for the whole
  U_L8 case. So U_L8 is closed once F7's share is closed.
- The 64 sub-cubes come from march_cu. Whether they cover their parent is re-checked by the cover check
  on the case, which passes.

Proof files were deleted after checking. Every leaf is re-solved from scratch by `verify/v3/v3_check.py`.
